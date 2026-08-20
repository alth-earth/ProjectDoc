---
Document Status: ACTIVE_CANONICAL
Scope: documentation navigation map
Canonical For: which document to trust for each question
Branch: demo-engineering
Last Verified: 2026-08-20
---

# Documentation Index

**Which file should I trust?** This index answers that question.

## Current (trust these for today's project state)

| Question | Document |
|----------|----------|
| Where are we now? | [current/CURRENT_STATUS.md](current/CURRENT_STATUS.md) |
| What's next? | [current/CURRENT_ROADMAP.md](current/CURRENT_ROADMAP.md) |
| System architecture? | [current/architecture/ARCTIC_ROUTE_SYSTEM.md](current/architecture/ARCTIC_ROUTE_SYSTEM.md) |
| Replay architecture? | [current/architecture/SIMULATION_REPLAY_ARCHITECTURE.md](current/architecture/SIMULATION_REPLAY_ARCHITECTURE.md) |
| How to run a demo? | [current/operations/DEMO_RUNBOOK.md](current/operations/DEMO_RUNBOOK.md) |
| How to recover? | [current/operations/RECOVERY_RUNBOOK.md](current/operations/RECOVERY_RUNBOOK.md) |
| Technical debt? | [current/reference/TECH_DEBT.md](current/reference/TECH_DEBT.md) |
| Time model? | [current/reference/TIME_MODEL_QUICK_REFERENCE.md](current/reference/TIME_MODEL_QUICK_REFERENCE.md) |
| Governance / report rules? | [standards/ENGINEERING_GOVERNANCE_STANDARD.md](standards/ENGINEERING_GOVERNANCE_STANDARD.md) |

## Frozen (historical baselines, do not modify)

| Phase | Location |
|-------|----------|
| RC1 (main branch) | [frozen/rc1-main/](frozen/rc1-main/) |
| RC2 (rc2-development branch) | [frozen/rc2-rc2-development/](frozen/rc2-rc2-development/) |

## Historical Reports (evidence, not current truth)

| Category | Location |
|----------|----------|
| Audits | [reports/audits/](reports/audits/) |
| Strategy B reports | [reports/strategy-b/](reports/strategy-b/) |
| Decisions | [reports/decisions/](reports/decisions/) |
| Governance refactor | [reports/governance/](reports/governance/) |

## Archive (superseded, deprecated, pre-governance)

| Category | Location |
|----------|----------|
| Superseded (old plans, etc.) | [archive/superseded/](archive/superseded/) |
| Pre-governance archives | [archive/pre-governance/](archive/pre-governance/) |
| Deprecated | [archive/deprecated/](archive/deprecated/) |

## Local (operator-only, gitignored)

| Category | Location |
|----------|----------|
| Local operator env | [local/LOCAL_OPERATOR_ENV.md](local/LOCAL_OPERATOR_ENV.md) |

## Subproject Documentation

Each subproject has its own README, CHANGELOG, and docs:

| Repo | Path |
|------|------|
| Contracts | /root/my_project/arctic_route_contracts/ |
| Orchestrator | /root/my_project/arctic_route_orchestrator/ |
| A (Data) | /root/my_project/work_package_a/ |
| B (Risk) | /root/my_project/work_package_b/ |
| C (Planning) | /root/my_project/work_package_c/ |
| D (Display) | /root/my_project/work_package_d/ |

## Conflict Resolution Order

1. Current code + tests (ground truth).
2. current/ canonical docs (this repo).
3. Subproject READMEs.
4. Historical reports (reports/).
5. Archive (archive/).

If a frozen doc conflicts with current, current wins. If a historical report conflicts with current, current wins, but the historical report should carry a correction note.
