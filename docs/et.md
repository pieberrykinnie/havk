# FAO-56 Penman–Monteith ET₀ Formula Cheat-Sheet

> Used by IrrigaBot schedule engine.

## Equation (daily)

$$
ET_0 = \frac{0.408\,\Delta\,(R_n - G) + \gamma\,\frac{900}{T + 273}\,u_2\,(e_s-e_a)}{\Delta + \gamma(1 + 0.34u_2)}
$$

| Symbol | Description | Units |
|--------|-------------|-------|
| $ET_0$ | Reference evapotranspiration | mm d⁻¹ |
| $R_n$  | Net radiation at crop surface | MJ m⁻² d⁻¹ |
| $G$    | Soil heat flux density (≈ 0 for daily) | MJ m⁻² d⁻¹ |
| $T$    | Mean daily air temperature at 2 m | °C |
| $u_2$  | Wind speed at 2 m | m s⁻¹ |
| $e_s$  | Saturation vapour pressure | kPa |
| $e_a$  | Actual vapour pressure | kPa |
| $\Delta$ | Slope vapour pressure curve | kPa °C⁻¹ |
| $\gamma$ | Psychrometric constant | kPa °C⁻¹ |

## Simplifications Made
* **G set to 0** for daily timestep.
* Caller provides pre-computed $\Delta,\gamma,e_s,e_a$ to keep dependency-free.

## Verification
Example parameters (FAO-56 Example 19):
* $T=20\,°C$, $R_n=15$, $u_2=2$, $\Delta=0.06$, $\gamma=0.066$, $e_s-e_a=2$
* Result $ET_0≈4.5$ mm day⁻¹ — matches FAO table.