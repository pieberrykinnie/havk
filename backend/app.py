"""FastAPI application entry-point for IrrigaBot backend.

This minimal scaffold will expand as additional routes and business logic are implemented.
"""
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, PositiveFloat

# pylint: disable=wrong-import-position
# Reordering import to avoid circular side effects
from backend.ml.et import WeatherInputs, et0_fao56
from backend.settings import settings

# ----------------------------
# Request / Response Schemas
# ----------------------------
class ScheduleRequest(BaseModel):
    """Payload for schedule calculation.

    Attributes
    ----------
    crop : str
        Crop name (unused in simple prototype but retained for future Kc).
    area_m2 : PositiveFloat
        Field area in square metres.
    lat : float
        Latitude (deg). Currently unused; placeholder for API weather fetch.
    lon : float
        Longitude (deg).
    """

    crop: str = Field(..., examples=["maize", "wheat"])
    area_m2: PositiveFloat
    lat: float
    lon: float


class ScheduleResponse(BaseModel):
    et0_mm: float  # mm/day
    advised_litres: float  # litres to apply over entire field


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
    weather = _mock_weather_inputs()
    et0 = et0_fao56(weather)
    mm_depth = et0 * settings.KC
    # 1 mm over 1 m^2 equals 1 litre water
    litres = round(mm_depth * req.area_m2, 2)
    return ScheduleResponse(et0_mm=et0, advised_litres=litres)


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