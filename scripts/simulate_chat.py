#!/usr/bin/env python3
"""Simulate chat loop: send schedule and feedback for each farmer."""
import requests
import random
import time

API_SCHEDULE = "http://localhost:8000/schedule"
API_FEEDBACK = "http://localhost:8000/feedback"

for i in range(1, 6):
    phone = f"+1555000{i}"
    schedule_payload = {
        "phone": phone,
        "crop": "maize",
        "area_m2": 1000,
        "lat": 0.0,
        "lon": 0.0,
    }
    resp = requests.post(API_SCHEDULE, json=schedule_payload)
    print(f"Schedule for {phone}: {resp.json()}")
    time.sleep(0.2)
    feedback_payload = {
        "phone": phone,
        "rating": random.choice(["ok", "dry", "wet"]),
    }
    resp2 = requests.post(API_FEEDBACK, json=feedback_payload)
    print(f"Feedback for {phone}: {resp2.json()}")
    time.sleep(0.2)