from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


def test_global_stats():
    # create two farmers
    f1 = {"phone": "+15551234555", "crop": "maize", "area_m2": 100, "lat": 0, "lon": 0}
    f2 = {"phone": "+15556667777", "crop": "wheat", "area_m2": 200, "lat": 1, "lon": 1}
    client.post("/farmers", json=f1)
    client.post("/farmers", json=f2)

    resp = client.get("/stats/global")
    assert resp.status_code == 200
    data = resp.json()
    assert data["farmers"] >= 2
    assert data["total_area_m2"] >= 300
    assert "leaderboard" in data
    assert any(
        float(v) >= 100 for v in data["leaderboard"].values()
    )