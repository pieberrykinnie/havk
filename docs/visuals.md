# Dashboard Visuals

The dashboard renders a **Mapbox heatmap** of total irrigated area (proxy for water savings) using realtime data from the `farmers` table.  Each farmer contributes a point where the heatmap weight equals `area_m2 / 1000`.

Environment variable `VITE_MAPBOX_TOKEN` must be set in `dashboard/.env`.