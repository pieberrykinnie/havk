# Caching Strategy

The **Weather / ET₀ cache** reduces external API calls and repeated computations.

* **Backend:** Redis 7 (see `infra/docker-compose.yml`).
* **Key format:** `et0:{lat:.4f}:{lon:.4f}` – four‐decimal rounding ensures stable hit‐rate without blowing up keyspace.
* **TTL:** 24 hours (configurable via `CACHE_TTL` env).
* **Graceful degradation:** If Redis is unavailable, cache helpers silently fall back to no‐op so the API continues to function.

Interaction helpers live in `backend/cache.py` and are unit‐tested with [`fakeredis`](https://pypi.org/project/fakeredis/).