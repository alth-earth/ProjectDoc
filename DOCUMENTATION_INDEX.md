---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
Document Role: CANONICAL
Scope: documentation navigation map
Canonical For: which document to trust for each question
Branch: research-validation-system
Last Verified: 2026-08-23
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
| Research gap analysis? | [current/RESEARCH_VALIDATION_GAP_ANALYSIS.md](current/RESEARCH_VALIDATION_GAP_ANALYSIS.md) |
| Research decisions? | [current/decisions/RESEARCH_VALIDATION_DECISIONS.md](current/decisions/RESEARCH_VALIDATION_DECISIONS.md) |
| Contract ownership? | [current/reference/CONTRACT_OWNERSHIP_REGISTRY.md](current/reference/CONTRACT_OWNERSHIP_REGISTRY.md) |
| Parallel development ownership? | [current/DEVELOPMENT_OWNERSHIP.md](current/DEVELOPMENT_OWNERSHIP.md) |
| Contract proposal template? | [standards/CONTRACT_CHANGE_PROPOSAL_TEMPLATE.md](standards/CONTRACT_CHANGE_PROPOSAL_TEMPLATE.md) |
| Winter scenario readiness? | [current/reference/WINTER_SCENARIO_STATUS.md](current/reference/WINTER_SCENARIO_STATUS.md) |
| Time model? | [current/reference/TIME_MODEL_QUICK_REFERENCE.md](current/reference/TIME_MODEL_QUICK_REFERENCE.md) |
| Governance / report rules? | [standards/ENGINEERING_GOVERNANCE_STANDARD.md](standards/ENGINEERING_GOVERNANCE_STANDARD.md) |

## Frozen (historical baselines, do not modify)

| Phase | Location |
|-------|----------|
| RC1 (main branch) | [frozen/rc1-main/](frozen/rc1-main/) |
| RC2 (rc2-development branch) | [frozen/rc2-rc2-development/](frozen/rc2-rc2-development/) |

## Research Validation Supporting Reports（2026-08-23 10:20 +08:00）

The audit and kickoff reports under `reports/research-validation/` support the
current canonical documents; they are not parallel sources of project truth.

Latest Winter gate evidence:
[WINTER_COMBINED_VIEWER_INTEGRATION_REPORT.md](reports/research-validation/WINTER_COMBINED_VIEWER_INTEGRATION_REPORT.md).

Latest A→B→C→D risk identity and Winter data evidence:

- [RISK_PIPELINE_AUDIT_AND_WINTER_DATA_VALIDATION_REPORT.md](reports/research-validation/RISK_PIPELINE_AUDIT_AND_WINTER_DATA_VALIDATION_REPORT.md)

Latest B risk calibration research evidence:

- [RISK_CALIBRATION_RESEARCH_REPORT.md](reports/research-validation/RISK_CALIBRATION_RESEARCH_REPORT.md)

Latest B/C/D interface and D Research Phase 1 evidence:

- [B_C_D_INTERFACE_STATUS.md](reports/research-validation/B_C_D_INTERFACE_STATUS.md)

Latest per-cell risk explanation sidecar design:

- [RISK_EXPLANATION_SIDECAR_DESIGN_REPORT.md](reports/research-validation/RISK_EXPLANATION_SIDECAR_DESIGN_REPORT.md)
- [`risk-explanation.v1` schema proposal](current/proposals/risk-explanation.v1.schema.json)
- [`risk-explanation.v1` design example](current/proposals/risk-explanation.v1.example.json)

Latest Winter C and D-interface evidence:

- [WINTER_C_SMOKE_REPORT.md](reports/research-validation/WINTER_C_SMOKE_REPORT.md)
- [WINTER_C_ROUTE_VALIDATION_REPORT.md](reports/research-validation/WINTER_C_ROUTE_VALIDATION_REPORT.md)
- [D_INTERFACE_READY_REPORT.md](reports/research-validation/D_INTERFACE_READY_REPORT.md)
- [WINTER_DATA_AVAILABILITY_FOLLOWUP.md](reports/research-validation/WINTER_DATA_AVAILABILITY_FOLLOWUP.md)

Latest Winter B validation evidence:

- [WINTER_B_BASELINE_CONFIG_DECISION.md](reports/research-validation/WINTER_B_BASELINE_CONFIG_DECISION.md)
- [WINTER_B_SMOKE_REPORT.md](reports/research-validation/WINTER_B_SMOKE_REPORT.md)
- [WINTER_RISK_DISTRIBUTION_AUDIT.md](reports/research-validation/WINTER_RISK_DISTRIBUTION_AUDIT.md)
- [WINTER_B_RISK_VALIDATION_REPORT.md](reports/research-validation/WINTER_B_RISK_VALIDATION_REPORT.md)

Current interface freeze evidence:

- [B Interface Freeze Audit](reports/research-validation/B_INTERFACE_FREEZE_AUDIT.md)
- [C Interface Freeze Audit](reports/research-validation/C_INTERFACE_FREEZE_AUDIT.md)
- [D Interface Freeze Audit](reports/research-validation/D_INTERFACE_FREEZE_AUDIT.md)

Focused Round 2 evidence:

- [WINTER_DATA_FEASIBILITY_REPORT.md](reports/research-validation/WINTER_DATA_FEASIBILITY_REPORT.md)
- [WINTER_SOURCE_VALIDATION_REPORT.md](reports/research-validation/WINTER_SOURCE_VALIDATION_REPORT.md)
- [WINTER_MET_SOURCE_COMPARISON.md](reports/research-validation/WINTER_MET_SOURCE_COMPARISON.md)
- [WINTER_DATA_POLICY_PROPOSAL.md](current/proposals/WINTER_DATA_POLICY_PROPOSAL.md)
- [ROUTE_PRESENTATION_CONTRACT_PROPOSAL.md](current/proposals/ROUTE_PRESENTATION_CONTRACT_PROPOSAL.md)
- B: `B_FORMAL_GRID_COMPARISON_REPORT.md`
- C: `BC_COUPLING_PERFORMANCE_REPORT.md` and `C_OPTIMIZATION_PROPOSAL.md`

## Competition Demo Closure Reports（2026-08-21 23:18）

| Report | Role |
|--------|------|
| [FINAL_CONSISTENCY_CLOSURE_20260820.md](reports/governance/FINAL_CONSISTENCY_CLOSURE_20260820.md) | Archived closure evidence |
| [ROOT_GOVERNANCE_AUDIT_FINAL_20260820.md](reports/governance/ROOT_GOVERNANCE_AUDIT_FINAL_20260820.md) | Archived governance audit evidence |

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
| Deprecated | [archive/deprecated/](archive/deprecated/README.md) (currently N/A) |

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
