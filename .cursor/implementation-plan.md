# Implementation Plan – IrrigaBot

_This document decomposes the entire prototype build into atomic, Conventional Commits–compliant git steps.  Each numbered line corresponds to **one** commit.  After completing a step, log it (condensed) in `.cursor/logs.md`, then run the indicated test(s) and docs updates._

## Conventions
* **Commit Style:** `<type>(scope): succinct imperative` (feat, fix, docs, chore, refactor, test).
* **Branching:** single `main` branch (hackathon), protected via CI (GitHub Actions).
* **Testing:** pytest for backend; Playwright for dashboard E2E; Twilio sandbox unit mocks.
* **Docs Folder:** `docs/` capped at 10 files; update relevant markdown or diagrams.

---

## Day-1  – Repo & CI Skeleton
| # | Commit Message | What to Do | Tests | Docs |
|---|----------------|-----------|-------|------|
|1| chore(repo): initialise monorepo with gitignore & licence | `git init`, add MIT LICENSE, .gitignore, README scaffold | n/a | Add purpose section to README |
|2| chore(ci): set up GitHub Actions Python & Node workflows | `.github/workflows/*` for lint & tests | CI runs `pytest -q` & `npm test` (placeholder) | README badge |
|3| feat(infra): add docker-compose with api, redis, supabase | create `infra/docker-compose.yml` minimal services | `docker compose config` | `docs/architecture.md` skeleton + diagram link |
|4| test(api): add pytest config & first placeholder test | `tests/test_smoke.py` asserting True | `pytest` passes | no |

## Day-2  – Core API & Model Baseline
| # | Commit Message | What to Do | Tests | Docs |
|5| feat(api): scaffold FastAPI app with `/health` endpoint | `backend/app.py`, `requirements.txt` | `GET /health` returns OK (pytest) | Update API section in README |
|6| feat(ml): implement FAO-56 ET0 calculator module | `backend/ml/et.py` | unit test reproduces FAO sample table values | add formula derivation to `docs/et.md` |
|7| feat(api): add `/schedule` POST accepting crop, area, loc | logic: call ET calc with mocked weather | pytest using test client returns litres value | README usage snippet |
|8| test(ci): enable coverage threshold 80% | add coverage badge step | CI shows pass | no |
|9| refactor(config): move constants to `settings.py` | env-driven | tests green | no |

## Day-3  – NLU + Twilio Integration
| # | Commit Message | What to Do | Tests | Docs |
|10| feat(nlu): add intent parser YAML + simple regex engine | `backend/nlu/parser.py` | unit tests for JOIN / DONE parsing | add nlu examples to docs |
|11| feat(twilio): add webhook handler function | `twilio-functions/handler.py` | pytest with Twilio mock HTTP event | update README Twilio setup |
|12| chore(infra): expose ngrok tunnel for local dev | docker service + script | manual test doc only | docs/ngrok.md |
|13| feat(api): persist farmer profiles in Supabase via REST | `backend/app.py` new endpoints | integration test w/ test DB container | ER diagram in architecture.md |
|14| fix(nlu): improve multilingual tokenisation | tweak parser; add unit tests Hindi/Spanish | tests pass | update locale doc |

## Day-4  – Schedule Optimiser & Caching
| # | Commit Message | What to Do | Tests | Docs |
|15| feat(cache): add RedisEdge lookup for weather/ET | service layer; TTL 24h | unit test mocks redis set/get | update caching strategy doc |
|16| feat(ml): add RL agent for feedback-based tuning | `backend/ml/agent.py` with simple Q-learning | unit test convergence on dummy env | docs/rl.md |
|17| feat(api): log farmer feedback & reward RL agent | record applied litres | integration test with feedback loop | update data flow diagram |
|18| chore(api): add pydantic validation schemas | improve robustness | tests | no |
|19| refactor(ml): move models to package for reuse | maintain tests | tests pass | no |

## Day-5  – Dashboard MVP
| # | Commit Message | What to Do | Tests | Docs |
|20| feat(dashboard): bootstrap React + Vite app | `dashboard/src/*` hello world | `npm test` placeholder | README run instructions |
|21| feat(dashboard): add Supabase realtime listener | renders farmer list & litres saved | Playwright test snapshot | screenshot in docs |
|22| feat(dashboard): add Mapbox heatmap of savings | integrate basic tiles | visual inspection E2E test | update visuals doc |
|23| feat(api): add `/stats/global` endpoint | aggregates litres saved | pytest asserts sum | update API table |
|24| test(e2e): add end-to-end demo script (Makefile) | seeds fake farmers, runs bot loop | GitHub action nightly | no |

## Day-6  – Accessibility, Gamification & Polish
| # | Commit Message | What to Do | Tests | Docs |
|25| feat(access): add voice IVR via Twilio TTS | update handler for voice calls | manual call test recorded | add IVR flowchart |
|26| feat(gamify): implement village leaderboard + badges | backend calc + Twilio emoji messages | unit test ranks correct | README badges section |
|27| docs(i18n): add translation workflow via Weblate | config files | n/a | docs/i18n.md |
|28| chore(frontend): add lighthouse CI for a11y score | GitHub action | score ≥ 90% | no |
|29| fix(frontend): colour-blind safe palette | css update | jest snapshot diff | update style guide |

## Day-7  – Testing, Packaging, Demo Assets
| # | Commit Message | What to Do | Tests | Docs |
|30| chore(repo): add `make demo` script to spin full stack | includes seed + sample chat | CI runs in 5 min | README quickstart |
|31| test(load): k6 script hitting schedule endpoint 500 rps | adds performance metrics | CI perf gate | docs/perf.md |
|32| docs(video): add demo storyboard & script | markdown only | n/a | docs/demo-script.md |
|33| docs(readme): finalize badges, licence year, links | polish | spellcheck | README complete |
|34| chore(release): tag v0.1 hackathon submission | git tag + changelog | n/a | CHANGELOG.md |

---

## Logging Protocol (for `.cursor/logs.md`)
After each commit:
1. Append bullet: `YYYY-MM-DD – Commit <#>: <message> ✅/❌ tests`.
2. If tests fail: note and mark ❌ with short fix note after resolved.
3. Keep latest 20 bullets; condense older into weekly summary to stay concise.

---

_End of plan – following this guarantees a deployable, documented, and test-covered prototype aligned with hackathon deliverables._