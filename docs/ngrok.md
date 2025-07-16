# Exposing IrrigaBot Locally with ngrok

This project uses **ngrok** to expose the local FastAPI server (running inside the `api` container) to Twilio for webhook testing.

## Prerequisites
1. Sign up for a free ngrok account and retrieve your **authtoken**.
2. Export your token once per shell:
   ```bash
   export NGROK_AUTHTOKEN="<your-token>"
   ```

## Start Tunnel
```bash
cd infra
./start-ngrok.sh
```
The tunnel URL will appear in the container logs and the local dashboard at <http://localhost:4040>.

## Configure Twilio
In the Twilio console, set your Messaging webhook to:
```
https://<random>.ngrok-free.app/twilio
```

## Stop Tunnel
```bash
cd infra
docker compose stop ngrok
```