"""FastAPI application entry-point for IrrigaBot backend.

This minimal scaffold will expand as additional routes and business logic are implemented.
"""
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, PositiveFloat

# pylint: disable=wrong-import-position
# Reordering import to avoid circular side effects
from backend.ml.et import WeatherInputs, et0_fao56
from backend.models.farmer import FarmerProfile
from backend.settings import settings
from backend.cache import get_cached_et0, set_cached_et0
from backend.ml.agent import QLearningAgent

# ----------------------------
# RL agent global instance
# ----------------------------

ACTIONS = [-1, 0, 1]  # -10%, 0%, +10%
_agent = QLearningAgent(ACTIONS)

# Track last action associated with farmer phone numbers
_last_action_by_phone: dict[str, int] = {}

# ----------------------------
# Request / Response Schemas
# ----------------------------
class ScheduleRequest(BaseModel):
    """Payload for schedule calculation.

    Attributes
    ----------
    phone : str | None
        Farmer phone number (E.164).
    crop : str
        Crop name (unused in simple prototype but retained for future Kc).
    area_m2 : PositiveFloat
        Field area in square metres.
    lat : float
        Latitude (deg). Currently unused; placeholder for API weather fetch.
    lon : float
        Longitude (deg).
    """

    phone: str | None = Field(None, description="Farmer phone number (E.164)")
    crop: str = Field(..., examples=["maize", "wheat"])
    area_m2: PositiveFloat
    lat: float
    lon: float


class ScheduleResponse(BaseModel):
    et0_mm: float  # mm/day
    advised_litres: float  # litres to apply over entire field


# ----------------------------
# In-memory farmer storage (fallback if Supabase not configured)
# ----------------------------

_farmers: dict[str, FarmerProfile] = {}


# ----------------------------
# Farmer endpoints
# ----------------------------


@app.post(
    "/farmers",
    response_model=FarmerProfile,
    status_code=status.HTTP_201_CREATED,
    summary="Create or update farmer profile",
    tags=["farmers"],
)
async def upsert_farmer(profile: FarmerProfile) -> FarmerProfile:
    """Persist farmer profile via Supabase REST or fallback in-memory store."""

    try:
        from supabase import create_client  # type: ignore

        import os

        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")

        if url and key:
            client = create_client(url, key)
            client.table("farmers").upsert(profile.model_dump()).execute()
        else:
            raise ImportError("Supabase env not configured")
    except Exception:  # pylint: disable=broad-except
        # Fallback to in-memory dictionary for local dev / unit tests
        _farmers[profile.phone] = profile

    return profile


@app.get(
    "/farmers/{phone}",
    response_model=FarmerProfile,
    summary="Retrieve farmer profile",
    tags=["farmers"],
)
async def get_farmer(phone: str) -> FarmerProfile:  # noqa: D401
    """Return farmer profile from Supabase or memory, 404 if missing."""

    profile: FarmerProfile | None = None

    try:
        from supabase import create_client  # type: ignore

        import os

        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")

        if url and key:
            client = create_client(url, key)
            data, _ = client.table("farmers").select("*").eq("phone", phone).single().execute()
            if data:
                profile = FarmerProfile(**data)
    except Exception:  # pylint: disable=broad-except
        profile = _farmers.get(phone)

    if profile is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Farmer not found")

    return profile


# ----------------------------
# Helper (mock weather)
# ----------------------------

def _mock_weather_inputs() -> WeatherInputs:
    """Return deterministic weather used for baseline tests.

    Values are loaded from :mod:`backend.settings` to allow env overrides.
    """
    return WeatherInputs(
        t_mean=settings.T_MEAN,
        net_radiation=settings.NET_RADIATION,
        wind_speed_2m=settings.WIND_SPEED_2M,
        slope_vp_curve=settings.SLOPE_VP_CURVE,
        psychrometric_constant=settings.PSYCHROMETRIC_CONSTANT,
        sat_vp=settings.SAT_VP,
        actual_vp=settings.ACTUAL_VP,
    )


@app.post(
    "/schedule",
    response_model=ScheduleResponse,
    summary="Calculate irrigation schedule for next day",
    tags=["schedule"],
)
async def compute_schedule(req: ScheduleRequest) -> ScheduleResponse:
    """Return simple water advice based on ET₀ times area.

    *Assumptions:* crop coefficient (Kc)=1, application efficiency 100%.
    """
    # Attempt to reuse ET₀ from cache (24h TTL)
    et0_cached = get_cached_et0(req.lat, req.lon)

    if et0_cached is not None:
        et0 = et0_cached
    else:
        weather = _mock_weather_inputs()
        et0 = et0_fao56(weather)
        set_cached_et0(req.lat, req.lon, et0)
    # RL agent decides adjustment action
    action = _agent.select_action("global")
    adj_factor = 1 + 0.1 * action  # convert -1/0/1 to -10%/0/+10%

    mm_depth = et0 * settings.KC * adj_factor
    # 1 mm over 1 m^2 equals 1 litre water
    litres = round(mm_depth * req.area_m2, 2)

    # Save action for feedback update
    if req.phone:
        _last_action_by_phone[req.phone] = action

    return ScheduleResponse(et0_mm=et0, advised_litres=litres)


# ----------------------------
# Feedback endpoint
# ----------------------------


class FeedbackRequest(BaseModel):
    phone: str = Field(..., description="Farmer phone number (E.164)")
    rating: str = Field(..., description="dry|ok|wet", examples=["ok"])


@app.post(
    "/feedback",
    status_code=status.HTTP_200_OK,
    summary="Record farmer feedback and update RL agent",
    tags=["feedback"],
)
async def submit_feedback(req: FeedbackRequest) -> dict[str, str]:  # noqa: D401
    """Update RL agent based on farmer qualitative feedback."""

    reward_map = {"ok": 1.0, "dry": -1.0, "wet": -1.0}
    reward = reward_map.get(req.rating, 0.0)

    action = _last_action_by_phone.get(req.phone, 0)

    # Single-state environment ("global")
    _agent.update("global", action, reward, "global")

    return {"status": "recorded"}


app = FastAPI(title="IrrigaBot API", version="0.1.0")


@app.get("/health", summary="Health check", tags=["meta"])
async def health_check() -> JSONResponse:
    """Return simple service liveliness indicator.

    Returns
    -------
    JSONResponse
        `{ "status": "ok" }` with HTTP 200.
    """
    return JSONResponse({"status": "ok"}, status_code=status.HTTP_200_OK)