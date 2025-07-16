from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)

PHONE = "+15551112222"


def test_feedback_updates_agent():
    payload = {"phone": PHONE, "crop": "maize", "area_m2": 1000, "lat": 0.0, "lon": 0.0}
    client.post("/schedule", json=payload)

    # Send positive feedback
    fb = {"phone": PHONE, "rating": "ok"}
    resp = client.post("/feedback", json=fb)
    assert resp.status_code == 200
    assert resp.json()["status"] == "recorded"