# IrrigaBot

[![Python CI](https://github.com/youruser/irriga-bot/actions/workflows/python-ci.yml/badge.svg)](./.github/workflows/python-ci.yml) [![Node CI](https://github.com/youruser/irriga-bot/actions/workflows/node-ci.yml/badge.svg)](./.github/workflows/node-ci.yml)

Early-stage monorepo for the **IrrigaBot** hackathon prototype (HAVK 2025).  Follow the [implementation plan](.cursor/implementation-plan.md) for progress.

> Under construction – see docs folder soon.

## Quick API test
With the dev containers running:
```bash
curl -s http://localhost:8000/health | jq
# { "status": "ok" }
```

### Compute schedule example
```bash
curl -s -X POST http://localhost:8000/schedule \
  -H "Content-Type: application/json" \
  -d '{"crop":"maize","area_m2":1000,"lat":0,"lon":0}' | jq
```

### Submit feedback example
```bash
curl -s -X POST http://localhost:8000/feedback \
  -H "Content-Type: application/json" \
  -d '{"phone":"+1555001","rating":"ok"}'
```

## Twilio Webhook (Local Test)

In the Twilio console set your messaging webhook to:
```
https://<ngrok-url>/twilio
```

For local simulation inside Python:
```python
from twilio_functions.handler import handle_sms
print(handle_sms({"Body": "join"}))
```

## Dashboard

```bash
cd dashboard
pnpm install --frozen-lockfile
pnpm dev
```
Visit http://localhost:5173 to view the React dashboard.