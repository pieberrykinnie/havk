from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)

SAMPLE = {
    "phone": "+15551234567",
    "crop": "maize",
    "area_m2": 1000,
    "lat": 0.0,
    "lon": 0.0,
}

def test_create_and_get_farmer():
    resp = client.post("/farmers", json=SAMPLE)
    assert resp.status_code == 201
    data = resp.json()
    assert data["phone"] == SAMPLE["phone"]

    # Retrieve
    resp2 = client.get(f"/farmers/{SAMPLE['phone']}")
    assert resp2.status_code == 200
    assert resp2.json()["crop"] == SAMPLE["crop"]