from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


def test_schedule_endpoint():
    payload = {"phone": "+1555001", "crop": "maize", "area_m2": 1000, "lat": 0.0, "lon": 0.0}
    resp = client.post("/schedule", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert set(data.keys()) == {"et0_mm", "advised_litres"}
    # For given mocked weather ET0 ~? compute: we'll assert litres positive
    assert data["advised_litres"] > 0