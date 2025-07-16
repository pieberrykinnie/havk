.PHONY: all services seed chat demo

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