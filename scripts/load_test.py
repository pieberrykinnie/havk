#!/usr/bin/env python3
"""Load test hitting schedule endpoint at 500 rps."""
import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor

API_URL = "http://localhost:8000/schedule"
PAYLOAD = {
    "phone": "+1555001",
    "crop": "maize", 
    "area_m2": 1000,
    "lat": 0.0,
    "lon": 0.0
}

def make_request():
    try:
        resp = requests.post(API_URL, json=PAYLOAD, timeout=1)
        return resp.status_code == 200
    except:
        return False

def load_test():
    start = time.time()
    success = 0
    total = 0
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for _ in range(500):  # 500 requests
            futures.append(executor.submit(make_request))
            time.sleep(0.002)  # 500 rps = 0.002s between requests
        
        for future in futures:
            total += 1
            if future.result():
                success += 1
    
    duration = time.time() - start
    rps = total / duration
    success_rate = success / total * 100
    
    print(f"Load test complete:")
    print(f"- Requests: {total}")
    print(f"- Success rate: {success_rate:.1f}%")
    print(f"- RPS: {rps:.1f}")

if __name__ == "__main__":
    load_test()