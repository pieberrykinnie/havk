from backend.ml import WeatherInputs, et0_fao56


def test_et0_sample_case():
    """Validate ET0 against worked FAO example (approx.).

    FAO-56 Example 19 (simplified, daily):
    - t_mean: 20 °C
    - net radiation (Rn): 15 MJ m-2 day-1
    - wind speed 2 m: 2 m s-1
    - slope vp curve (delta): 0.06 kPa °C-1
    - psychrometric constant (gamma): 0.066 kPa °C-1
    - es - ea: 2.0 kPa  (we'll use sat_vp=3, actual_vp=1)

    Expected ET0 ~ 4.5 mm/day (tolerance 0.2).
    """
    inputs = WeatherInputs(
        t_mean=20.0,
        net_radiation=15.0,
        wind_speed_2m=2.0,
        slope_vp_curve=0.06,
        psychrometric_constant=0.066,
        sat_vp=3.0,
        actual_vp=1.0,
    )
    et0 = et0_fao56(inputs)
    assert 4.3 <= et0 <= 4.7