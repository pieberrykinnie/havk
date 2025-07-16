# Development Logs – IrrigaBot

_Use this file to record progress **after each commit** as dictated in implementation-plan.md. Keep only the latest ~20 granular entries and condense older ones into weekly summaries._

## Log Format
```
YYYY-MM-DD – Commit <#>: <commit message> ✅ tests
```
Example:
```
2025-07-18 – Commit 1: chore(repo): initialise monorepo ✅
```

---

## Current Session
2025-07-16 – Commit 1: chore(repo): initialise monorepo ✅
2025-07-16 – Commit 2: chore(ci): add GitHub Actions workflows and badges ✅
2025-07-16 – Commit 3: feat(infra): add docker-compose with api, redis, supabase ✅
2025-07-16 – Commit 4: test(api): add pytest config & smoke test ✅
2025-07-16 – Commit 5: feat(api): scaffold FastAPI app with /health endpoint ✅
2025-07-16 – Commit 6: feat(ml): add FAO-56 ET0 calculator & unit test ✅
2025-07-16 – Commit 7: feat(api): add /schedule endpoint with ET0 calc & tests ✅
2025-07-16 – Commit 8: test(ci): enforce 80% coverage threshold in pytest step ✅
2025-07-16 – Commit 9: refactor(config): centralise constants in settings.py env-driven ✅
2025-07-16 – Commit 10: feat(nlu): add YAML intent patterns & regex parser with tests ✅
2025-07-16 – Commit 11: feat(twilio): add webhook handler, tests, README snippet ✅
2025-07-16 – Commit 12: chore(infra): add ngrok service & start script ✅
2025-07-16 – Commit 13: feat(api): add farmer persist endpoints with Supabase fallback ✅
2025-07-16 – Commit 14: fix(nlu): add accent stripping & transliteration, new multilingual patterns & tests ✅
2025-07-16 – Commit 15: feat(cache): add Redis-based ET₀ cache layer with tests & docs ✅
2025-07-16 – Commit 16: feat(ml): add Q-learning agent, convergence test & RL doc ✅
2025-07-16 – Commit 17: feat(api): add feedback endpoint and RL reward loop ✅
2025-07-16 – Commit 18: chore(api): centralise validation types (PhoneStr, RatingStr) and refactor schemas ✅
2025-07-16 – Commit 19: refactor(ml): add package __init__ and re-export models; updated imports/tests ✅
2025-07-16 – Commit 20: feat(dashboard): bootstrap React + Vite hello world, README instructions ✅
2025-07-16 – Commit 21: feat(dashboard): add Supabase realtime farmer list listener ✅
2025-07-16 – Commit 22: feat(dashboard): integrate Mapbox heatmap with realtime farmers ✅
2025-07-16 – Commit 23: feat(api): add /stats/global endpoint, tests, README example ✅