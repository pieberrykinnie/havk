.PHONY: all services seed chat demo quickstart

# Start all backend services (infra)
services:
	cd infra && docker compose up -d

# Seed test farmers with realistic data
seed:
	python3 scripts/seed_farmers.py

# Run a simulated chat loop (sends messages, checks responses)
chat:
	python3 scripts/simulate_chat.py

# Run everything in sequence
demo: services seed chat
	@echo "Demo complete."

# Quickstart: spin up full stack
quickstart: services
	@echo "Starting dashboard..."
	cd dashboard && pnpm install --frozen-lockfile && pnpm dev &
	@echo "Full stack ready:"
	@echo "- API: http://localhost:8000"
	@echo "- Dashboard: http://localhost:5173"
	@echo "- Redis: localhost:6379"
	@echo "- Supabase: localhost:54322"