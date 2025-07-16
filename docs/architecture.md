# Architecture Overview – IrrigaBot

```mermaid
flowchart LR
  UserSMS((SMS/WhatsApp)) --> TwilioWebhook
  TwilioWebhook --> NLU
  NLU --> API
  API -- data --> Supabase[(DB)]
  API -- cache --> RedisEdge[(Redis)]
  API -- ET & RL --> ML
  DB --> Dashboard
```

*Draft – will evolve as services are implemented.*

## Local Development Stack
Set up via `infra/docker-compose.yml`, launching:
* **api** – placeholder until backend service built.
* **redis** – Edge cache.
* **supabase-db** – Postgres-compatible DB on port 54322.

Run:
```bash
cd infra
docker compose up -d
```