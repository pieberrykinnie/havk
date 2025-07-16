# HAVK Hackathon – Project Plan

## Key Dates
| Event | Date & Time (CDT) |
|-------|------------------|
| Hackathon Start | **Fri, 11 Jul 2025 13:00** |
| Submission Deadline | **Fri, 18 Jul 2025 13:00** |
| Buffer Reserved | 18 Jul 2025 09:00 – 13:00 |

---

## Objectives
1. Deliver a production-ready web application that addresses a critical scarcity problem.
2. Prepare all required hackathon artifacts:
   - 5-minute demo video
   - GitHub repository with ≥85 % test coverage
   - Devpost description, pitch deck, technical docs, judging Q&A
3. Maximize scoring on weighted criteria (Technical Depth, Creativity, Accessibility, Fun Factor, Usability, Visuals).

---

## High-Level Timeline & Milestones
| Phase | Calendar Days | % of Total Time | Major Deliverables |
|-------|---------------|-----------------|--------------------|
| **Planning & Setup** | Jul 11 (Day 1) | 15 % | Concept lock-in, repo initialized, backlog drafted |
| **Design & Architecture** | Jul 12 AM (Day 2) | 5 % | System diagram, API contracts, UI wireframes |
| **Core Development** | Jul 12 PM – Jul 15 (Days 2-5) | 45 % | Backend APIs, DB schema, frontend pages, auth, CI pipeline |
| **Integration & Testing** | Jul 15 PM – Jul 16 (Days 5-6) | 15 % | End-to-end flows, unit & integration tests (≥85 % coverage) |
| **Polish & Accessibility** | Jul 16 PM – Jul 17 (Days 6-7) | 10 % | UI polish, a11y checks, performance tuning |
| **Docs & Media** | Jul 17 (Day 7) | 7 % | README, technical docs, pitch deck, judging Q&A draft |
| **Demo Video** | Jul 17 PM – Jul 18 AM | 5 % | 2-min walkthrough with voice-over, captions |
| **Packaging & Submission** | Jul 18 AM (Day 8) | 3 % | Submission ZIP, Devpost entry, final review |

> **Total**: 100 % of 1-week duration (with 4-hour safety buffer before deadline).

---

## Resource Allocation
| Team Member | Primary Role | Hour Budget | Focus Areas |
|-------------|-------------|------------|-------------|
| Alice | Project Lead / Full-Stack | 40 h | Architecture, task triage, backend reviews |
| Bob | Backend Engineer | 35 h | FastAPI endpoints, database schema, APIs |
| Carol | Frontend Engineer | 35 h | Next.js pages, UI state, accessibility |
| Dave | DevOps & QA | 25 h | CI/CD, testing framework, coverage reports |
| Eve | Designer & Media | 20 h | UX flows, visuals, demo video, pitch deck |

*All hours are estimates; daily stand-ups will rebalance workload as needed.*

---

## Risk Management & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Scope creep | Medium | High | Strict backlog; “must/should/could” tagging |
| Integration bugs late in cycle | Medium | High | Daily automated builds & tests |
| Video production delays | Low | Medium | Draft storyboard by Jul 16; fallback to GIF walkthrough |
| External API downtime | Low | Medium | Cache critical data; offline demo mode |

---

## Gantt Chart
```mermaid
gantt
  dateFormat  YYYY-MM-DD
  title  HAVK Desert Hackathon – 1-Week Timeline

  section Planning & Design
  Ideation & Setup           :a1, 2025-07-11, 1d
  Architecture & Wireframes  :a2, after a1, 0.5d

  section Development
  Backend Development        :b1, 2025-07-12, 3d
  Frontend Development       :b2, parallel b1, 3d

  section Testing & Polish
  Integration & Testing      :c1, 2025-07-15, 1d
  UI Polish & Accessibility  :c2, after c1, 1d

  section Docs & Media
  Documentation & Q&A        :d1, 2025-07-17, 0.5d
  Demo Video Creation        :d2, parallel d1, 0.5d

  section Submission
  Final Packaging & Submit   :e1, 2025-07-18, 0.25d
```

---

## Deliverables Checklist
- [ ] production_ready_code/ with passing tests & lint
- [ ] DEMO_VIDEO.mp4 (≈2 min)
- [ ] submission_package/
  - [ ] LIVE_DEMO.html
  - [ ] PITCH_DECK.pdf
  - [ ] TECHNICAL_DOCUMENTATION.md
  - [ ] JUDGING_RESPONSES.md
- [ ] PROJECT_PLAN.md committed

---

## Daily Stand-Up Agenda (15 min)
1. *Yesterday*: What did you complete?
2. *Today*: What will you do?
3. *Blockers*: Anything in your way?

---

*Let’s execute and HAVK the desert!*