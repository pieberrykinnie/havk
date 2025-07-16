# Performance Testing

## Load Testing
The `scripts/load_test.py` script simulates 500 requests per second to the `/schedule` endpoint.

Run locally:
```bash
python3 scripts/load_test.py
```

Expected results:
- Success rate: >95%
- RPS: ~500
- Response time: <100ms

## CI Performance Gate
The GitHub Actions workflow runs this load test and fails if:
- Success rate drops below 90%
- Average response time exceeds 500ms