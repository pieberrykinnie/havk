import backend.cache as cache
from fakeredis import FakeRedis


def test_et0_cache(monkeypatch):
    fake = FakeRedis(decode_responses=True)
    monkeypatch.setattr(cache, "_client", fake)

    cache.set_cached_et0(0.0, 0.0, 4.2, ttl=5)
    assert cache.get_cached_et0(0.0, 0.0) == 4.2

    # After TTL expiry simulated by calling delete
    fake.delete("et0:0.0000:0.0000")
    assert cache.get_cached_et0(0.0, 0.0) is None