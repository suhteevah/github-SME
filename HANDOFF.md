# HANDOFF.md — Course Review Agent Pipeline

## Last Updated
2026-03-29

## Project Status
🟡 SCAFFOLDING — Skill designed, architecture defined, awaiting first course package from client

## Assigned Course List (updated 2026-03-29)

Source: `GitHub Course List.xlsx` from client

| Head | Course Domain | Course Title | Duration |
|------|---------------|-------------|----------|
| 1 | Distributed AI | Scale Tasks Asynchronously | 1.5h |
| 1 | API & App Engineering | Build & Document Microservice | 2h |
| 1 | DevOps & Automation | Manage Code with Git Bots | 1.5h |
| 2 | DevOps & Automation | Automate Issue Summaries | 1.5h |
| 3 | DevOps & Automation | Test Agent Outputs | 1.5h |
| 3 | Observability & Governance | Trace & Scale Latency | 1.5h |
| 3 | Observability & Governance | Enforce AI Guardrails | 1.5h |

**7 courses total** — all GitHub-tool-focused, across 4 domains.

Previously selected courses no longer on list (likely reassigned or dropped):
- ~~Speed Up CI Pipeline~~
- ~~Orchestrate Agents Efficiently~~
- ~~Containerise & Deploy Fast~~

## Current State

### What's Done
- [x] SKILL.md written with full agent pipeline architecture
- [x] CLAUDE.md (soul file) written with coding standards, architecture, and integration notes
- [x] HANDOFF.md (this file) created
- [x] Skill packaged as .skill file for installation
- [x] Upwork proposal submitted at $45/hr (flat rate per course applies: $200-$360)
- [x] Core engine built (`src/engine.py`) — file classification, manifest building, review prompts, result storage
- [x] Scripts stubbed: `review_course.py`, `review_single.py`, `validate_links.py`
- [x] Course list received from client (7 courses, 3 heads)

### What's Next (in order)
1. **AWAIT:** Client response on Upwork — interview/acceptance
2. **RECORD:** 1-minute intro video using their C# audition script template
3. **BUILD:** Implement the agent pipeline (Rust + Python scripts)
   - Start with Python scripts (fastest to deploy)
   - Port to Rust agents once pipeline is validated
4. **TEST:** Run pipeline against sample course materials (create fixtures)
5. **DEPLOY:** Process first real course package when it arrives

### Blocking Issues
- No course materials received yet — need client to assign courses
- 1-minute intro video not yet recorded (required for evaluation)
- Tier assignment (Regular $200 / Senior $280 / Special $360) not confirmed — push for Special

### Course Priority Ranking (submitted to client via Upwork)
1. **Manage Code with Git Bots** (1.5h) — Core GitHub + automation expertise
2. **Build & Document Microservice** (2h) — Longest course, highest revenue, API design strength
3. **Scale Tasks Asynchronously** (1.5h) — Directly maps to OpenClaw distributed AI work
4. **Enforce AI Guardrails** (1.5h) — High strategic value, positions for Special tier
5. **Test Agent Outputs** (1.5h) — Meta-credibility: building agent testing pipeline right now
6. Automate Issue Summaries (1.5h) — Available but less differentiated
7. Trace & Scale Latency (1.5h) — Available but most ops-heavy, least AI-aligned

### Agent Implementation Priority
Build in this order (Python first, fastest to revenue):
1. `review_single.py` — Review any single file (most immediately useful)
2. `review_course.py` — Full course pipeline orchestrator
3. `validate_links.py` — URL checker (quick win, reusable)
4. `check_versions.py` — Version currency validator (web search powered)
5. `generate_lab.py` — Lab generator (needed for deliverable #7 in contract)
6. `prep_screencast.py` — Screencast preparation (needed before recording)
7. `incorporate_feedback.py` — Feedback incorporation (needed for revision rounds)

### Key Files
- Skill definition: `course-review-agent/SKILL.md`
- Soul file: `CLAUDE.md`
- This file: `HANDOFF.md`
- Course list source: `C:\Users\Matt\Downloads\GitHub Course List.xlsx`
- Upwork message draft: `C:\Users\Matt\Documents\Obsidian\Upwork Course Priority Ranking.md`

### Notes for Next Session
- **Waiting on Aryan** — course priority ranking sent, awaiting response/assignment
- The Upwork contract specifies milestone-based payments:
  - 25% at outline creation/reviews
  - 35% at content reviews/validation/code testing
  - 20% at screencast/demo delivery
  - 20% at talking head video recording + digital signature
- Client expects 1 round of internal feedback + 2 rounds of client feedback per deliverable
- Talking head videos are 35-45 minutes of recording per course
- Matt needs to record the 1-minute C# audition video ASAP — this is mandatory for evaluation
- Digital signature required for client platform
- Original 5 courses were trimmed to 7 different ones — 3 dropped (Speed Up CI Pipeline, Orchestrate Agents Efficiently, Containerise & Deploy Fast)
