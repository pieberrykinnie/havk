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