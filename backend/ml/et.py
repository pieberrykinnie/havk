"""FAO-56 Penman-Monteith reference evapotranspiration (ET₀) calculator.

Implements Equation 6 from FAO Irrigation & Drainage Paper 56.
All variables use SI units.

Reference: https://www.fao.org/3/x0490e/x0490e06.htm#6.2

The equation:

ET₀ = [0.408·Δ·(Rₙ − G) + γ·(900/(T+273))·u₂·(eₛ − eₐ)] \
       / [Δ + γ·(1 + 0.34·u₂)]

where
* ET₀  : reference evapotranspiration (mm day⁻¹)
* Δ    : slope vapour pressure curve (kPa °C⁻¹)
* Rₙ   : net radiation at crop surface (MJ m⁻² day⁻¹)
* G    : soil heat flux density (MJ m⁻² day⁻¹) – can be set 0 for daily timestep
* γ    : psychrometric constant (kPa °C⁻¹)
* T    : mean daily air temp at 2 m height (°C)
* u₂   : wind speed at 2 m (m s⁻¹)
* eₛ   : saturation vapour pressure (kPa)
* eₐ   : actual vapour pressure (kPa)

Note: For hackathon purposes we assume **G = 0** (daily ET₀) and caller supplies
pre-calculated Δ, γ, eₛ, eₐ. This keeps implementation lightweight.
"""
from __future__ import annotations

from typing import NamedTuple


class WeatherInputs(NamedTuple):
    """Minimal set of weather parameters for ET₀ calculation."""

    t_mean: float  # °C
    net_radiation: float  # MJ m-2 day-1 (Rₙ)
    wind_speed_2m: float  # m s-1 (u₂)
    slope_vp_curve: float  # kPa °C-1 (Δ)
    psychrometric_constant: float  # kPa °C-1 (γ)
    sat_vp: float  # kPa (eₛ)
    actual_vp: float  # kPa (eₐ)


def et0_fao56(inputs: WeatherInputs, soil_heat_flux: float = 0.0) -> float:
    """Compute reference evapotranspiration ET₀ (mm day⁻¹).

    Parameters
    ----------
    inputs : WeatherInputs
        All meteorological variables required by equation.
    soil_heat_flux : float, optional
        G term in equation (MJ m-2 day-1). For daily ET₀ use default 0.

    Returns
    -------
    float
        ET₀ in millimetres per day, rounded to 3 decimal places for stability.
    """
    delta = inputs.slope_vp_curve
    rn = inputs.net_radiation
    g = soil_heat_flux
    gamma = inputs.psychrometric_constant
    t = inputs.t_mean
    u2 = inputs.wind_speed_2m
    es_minus_ea = inputs.sat_vp - inputs.actual_vp

    numerator = 0.408 * delta * (rn - g) + gamma * (900 / (t + 273)) * u2 * es_minus_ea
    denominator = delta + gamma * (1 + 0.34 * u2)

    et0 = numerator / denominator
    return round(et0, 3)