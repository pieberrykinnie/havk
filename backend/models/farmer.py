"""Pydantic model for farmer profiles."""
from pydantic import BaseModel, Field, PositiveFloat

from backend.schemas import PhoneStr


class FarmerProfile(BaseModel):
    phone: PhoneStr
    crop: str
    area_m2: PositiveFloat
    lat: float
    lon: float

    class Config:
        json_schema_extra = {
            "example": {
                "phone": "+15551234567",
                "crop": "maize",
                "area_m2": 1200,
                "lat": 1.23,
                "lon": 36.78,
            }
        }