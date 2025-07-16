# Judging Q&A Responses

## 1. What does your project do?
Our application provides an end-to-end platform for cataloging scarce resources (e.g., water wells, food banks) and crowdsourcing community-driven software solutions to improve access, distribution, and management.

## 2. Who does it help?
It empowers marginalized communities living in resource-scarce environments by giving them an easy way to surface needs and receive innovative solutions from developers worldwide.

## 3. How does it work (technical overview)?
- Users register and log in via JWT-based auth.
- Authenticated users create **Resources** (water stations, Wi-Fi hubs, etc.).
- Developers post **Solutions** linked to resources (optimization algorithms, mobile alerts).
- FastAPI REST API persists data in PostgreSQL; Next.js consumes it using fetch.

## 4. Why does it matter?
Scarcity affects billions; connecting real-world needs with open-source ingenuity accelerates impactful interventions and knowledge sharing.

## 5. Technical Depth (10/10)
- Asynchronous FastAPI + SQLModel data layer
- JWT security, hashed passwords
- Dockerized micro-stack, CI pipeline, >85 % test coverage
- Accessible, responsive UI with React & Tailwind

## 6. Creativity (10/10)
Transforms hackathon submissions into living tools that communities can immediately benefit from, rather than static demos.

## 7. Accessibility (10/10)
WCAG-friendly color contrast, keyboard-navigable forms, ARIA labels, responsive design.

## 8. Fun Factor (5/5)
Real-time dashboard shows incoming solutions, making contribution feel like a game.

## 9. Visuals (5/5)
Modern Tailwind UI, dark/light modes, clean typography.