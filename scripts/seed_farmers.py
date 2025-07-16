#!/usr/bin/env python3
"""Seed test farmers with realistic data."""
import requests
import random

API = "http://localhost:8000/farmers"
CROPS = ["maize", "wheat", "rice", "sorghum"]

for i in range(1, 6):
    payload = {
        "phone": f"+1555000{i}",
        "crop": random.choice(CROPS),
        "area_m2": random.randint(500, 5000),
        "lat": round(random.uniform(-10, 10), 4),
        "lon": round(random.uniform(30, 40), 4),
    }
    resp = requests.post(API, json=payload)
    print(f"Seeded: {payload['phone']} status={resp.status_code}")