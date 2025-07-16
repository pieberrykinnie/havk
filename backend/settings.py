"""Application settings module.

Environment-driven constants are defined here to centralise configuration.
Values can be overridden via environment variables with the prefix `IRRIGA_`.
Example:
```
export IRRIGA_T_MEAN=26
```
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global settings container.

    Defaults replicate the deterministic values used during early prototyping.
    """

    # Weather defaults for mock calculations
    T_MEAN: float = 25.0
    NET_RADIATION: float = 18.0
    WIND_SPEED_2M: float = 2.0
    SLOPE_VP_CURVE: float = 0.07
    PSYCHROMETRIC_CONSTANT: float = 0.066
    SAT_VP: float = 3.2
    ACTUAL_VP: float = 1.2

    # Agronomic defaults
    KC: float = 1.0  # crop coefficient

    model_config = SettingsConfigDict(env_prefix="IRRIGA_", case_sensitive=False)


settings = Settings()  # Singleton-style instance