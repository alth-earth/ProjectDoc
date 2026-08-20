# Arctic Route Governance

Document Status: ACTIVE_CANONICAL
Scope: whole-project governance + documentation
Canonical For: project entry point
Branch: demo-engineering
Last Verified: 2026-08-20

## What This Is

This repository holds the **whole-project governance and documentation** for the
Arctic Route Planning system.  It is NOT a code repository.  Code lives in the
individual work-package repositories under `/root/my_project/`.

`/root/my_project` itself is a **plain workspace** — not a Git repository.

## Repository Layout

```
/root/my_project/
  arctic_route_governance/   ← this repo (governance + docs)
  arctic_route_contracts/   ← shared contracts / schemas
  arctic_route_orchestrator/ ← A-B-C-D root coordinator + replay engine
  work_package_a/           ← data preparation / causal visibility
  work_package_b/           ← dynamic risk
  work_package_c/           ← time-dependent planning
  work_package_d/           ← display / visualization / viewer
```

## Branch Mapping

| Branch              | Meaning                     | Status   |
|---------------------|-----------------------------|----------|
| `main`              | RC1 frozen baseline         | FROZEN   |
| `rc2-development`   | RC2 frozen baseline          | FROZEN   |
| `demo-engineering`  | current active development  | ACTIVE   |

## A/B/C/D Responsibilities

| Package | Role                            |
|---------|---------------------------------|
| A       | Data preparation / causal visibility |
| B       | Dynamic risk assessment          |
| C       | Time-dependent route planning    |
| D       | Display / visualization / viewer |

**Orchestrator** = A-B-C-D root coordinator.  It owns:
- replay execution
- navigation execution state
- replan lifecycle
- presentation adapter (business projection of replay internals)
- L1/L2 presentation eligibility preflight
- presentation artifact export

**D** owns the Viewer application: HTML/JS/CSS, Simulation Clock UI,
moving ship rendering, route/track/pending rendering, static server,
proof renderer.  D consumes only JSON/PNG artifacts produced by the
Orchestrator — it never imports orchestrator private Python modules.

## Where to Find Things

| Question                | Answer                                          |
|-------------------------|-------------------------------------------------|
| Current state?          | `current/CURRENT_STATUS.md`                     |
| Current roadmap?       | `current/CURRENT_ROADMAP.md`                    |
| System architecture?    | `current/architecture/ARCTIC_ROUTE_SYSTEM.md`   |
| Replay architecture?    | `current/architecture/SIMULATION_REPLAY_ARCHITECTURE.md` |
| Demo operation?         | `current/operations/DEMO_RUNBOOK.md`            |
| Recovery?               | `current/operations/RECOVERY_RUNBOOK.md`        |
| Technical debt?         | `current/reference/TECH_DEBT.md`               |
| Time model?             | `current/reference/TIME_MODEL_QUICK_REFERENCE.md`|
| Governance standard?    | `standards/ENGINEERING_GOVERNANCE_STANDARD.md`  |
| RC1 frozen docs?        | `frozen/rc1-main/`                              |
| RC2 frozen docs?        | `frozen/rc2-rc2-development/`                   |
| Historical reports?     | `reports/`                                      |
| Old plans / superseded? | `archive/`                                      |
| Local operator docs?    | `local/` (gitignored)                          |

## Documentation Governance Rules

All documentation work must follow [`standards/ENGINEERING_GOVERNANCE_STANDARD.md`](standards/ENGINEERING_GOVERNANCE_STANDARD.md).
Key rules:

- **SSOT**: each fact domain has exactly one canonical document.
- **No patch append**: do not add information at the end of a doc; put it in the right section.
- **Semantic placement**: tests → test docs, cache → environment docs, next steps → roadmap.
- **Archive 3-step**: back-fill → compare → converge before archiving.
- **Historical reports**: never rewrite to look current; add correction notes.
- **New headings**: carry real timestamp like `### X.Y Title (YYYY-MM-DD HH:MM +08:00)`.
- **Status taxonomy**: ACTIVE_CANONICAL / ACTIVE_SUPPORTING / FROZEN_RC1 / FROZEN_RC2 / HISTORICAL_REPORT / SUPERSEDED / DEPRECATED / ARCHIVED / LOCAL_ONLY.

## Quick Start for a New Agent

1. Read this README.
2. Read `DOCUMENTATION_INDEX.md`.
3. Read `current/CURRENT_STATUS.md`.
4. Read `current/CURRENT_ROADMAP.md`.
5. You now know the project state, what's next, and where everything lives.
```
```
