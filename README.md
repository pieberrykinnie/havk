# IrrigaBot

[![Python CI](https://github.com/youruser/irriga-bot/actions/workflows/python-ci.yml/badge.svg)](./.github/workflows/python-ci.yml) [![Node CI](https://github.com/youruser/irriga-bot/actions/workflows/node-ci.yml/badge.svg)](./.github/workflows/node-ci.yml) [![Lighthouse CI](https://github.com/youruser/irriga-bot/actions/workflows/lighthouse.yml/badge.svg)](./.github/workflows/lighthouse.yml)

AI-powered irrigation advisor for smallholder farmers in water-scarce regions. Built for the HAVK 2025 hackathon.

## Quickstart

```bash
make quickstart
```

This spins up the full stack:
- Backend API (FastAPI)
- Dashboard (React + Vite) 
- Redis cache
- Supabase database

Then visit http://localhost:5173 for the dashboard.

## Features

- **SMS/WhatsApp Bot** - multilingual irrigation advice
- **Voice IVR** - accessible to illiterate farmers  
- **Real-time Dashboard** - live farmer monitoring
- **RL Optimization** - learns from farmer feedback
- **Multilingual** - Hindi, Spanish, English support
- **Accessible** - color-blind safe, Lighthouse 90%+ a11y

## Documentation

- [Architecture](docs/architecture.md)
- [API Reference](docs/api.md) 
- [Demo Script](docs/demo-script.md)
- [Performance](docs/perf.md)

## License

MIT © 2025 IrrigaBot Team