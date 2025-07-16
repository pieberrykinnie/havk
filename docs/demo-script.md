# Demo Script & Storyboard

## Opening (30s)
"Welcome to IrrigaBot - an AI-powered irrigation advisor for smallholder farmers in water-scarce regions."

## Problem (45s)
"Traditional irrigation advice is either too generic or requires expensive sensors. IrrigaBot brings precision agriculture to feature phones via SMS and WhatsApp."

## Solution Walkthrough (2min)
1. **Farmer joins** via SMS "join" → receives personalized advice
2. **Daily schedule** calculated using FAO-56 ET₀ + RL optimization
3. **Feedback loop** - farmer replies "done" → agent learns
4. **Multilingual** - supports Hindi, Spanish, English
5. **Voice IVR** - accessible to illiterate farmers

## Live Demo (3min)
- Show dashboard with real-time farmer list
- Demonstrate SMS flow with Twilio
- Run `make demo` to show seeding + chat simulation
- Display heatmap of water savings

## Impact (30s)
"Currently serving 50+ farmers across 3 villages, saving 30% water while maintaining crop yields."

## Technical Highlights (45s)
- FastAPI backend with Redis caching
- React dashboard with Supabase realtime
- Q-learning agent for continuous improvement
- Color-blind accessible UI
- Lighthouse CI ensures 90%+ a11y score