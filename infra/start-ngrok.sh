#!/usr/bin/env bash
# Start ngrok tunnel for local dev (requires NGROK_AUTHTOKEN set)
set -euo pipefail

if [[ -z "${NGROK_AUTHTOKEN:-}" ]]; then
  echo "❌ NGROK_AUTHTOKEN env var not set. Obtain it from https://dashboard.ngrok.com/get-started/your-authtoken" >&2
  exit 1
fi

cd "$(dirname "$0")"
echo "🚀 Starting ngrok tunnel..."
docker compose up -d ngrok

echo "✅ ngrok started. Inspect dashboard at http://localhost:4040"