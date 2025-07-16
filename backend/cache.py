"""Redis-based caching utilities.

This module abstracts access to the Redis instance defined in `docker-compose.yml`.
It is intentionally minimal: only string keys & JSON-encoded payloads.
"""
from __future__ import annotations

import json
import os
from typing import Any, Optional

import redis

from redis.exceptions import RedisError

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL", 60 * 60 * 24))  # 24 hours default

_client: redis.Redis[str] = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


# ---------------------------------------------------------------------------
# Weather / ET₀ helpers
# ---------------------------------------------------------------------------

def _et0_key(lat: float, lon: float) -> str:  # noqa: D401
    """Return Redis key for ET₀ at a given coordinate rounded to 4 dp."""

    return f"et0:{lat:.4f}:{lon:.4f}"


def get_cached_et0(lat: float, lon: float) -> Optional[float]:  # noqa: D401
    """Return cached ET₀ value if present and not expired."""

    try:
        raw = _client.get(_et0_key(lat, lon))
        return float(raw) if raw is not None else None
    except RedisError:
        return None


def set_cached_et0(lat: float, lon: float, et0: float, ttl: int = CACHE_TTL_SECONDS) -> None:  # noqa: D401
    """Store ET₀ in Redis with TTL (seconds)."""

    try:
        _client.setex(_et0_key(lat, lon), ttl, et0)
    except RedisError:
        # Swallow cache errors; not critical path
        pass


__all__ = [
    "get_cached_et0",
    "set_cached_et0",
]