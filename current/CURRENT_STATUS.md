---
Document Status: ACTIVE_CANONICAL
Scope: whole-project current state
Canonical For: current milestone, capability matrix, maturity
Branch: demo-engineering
Last Verified: 2026-08-20
---

# Current Status

## Strategy Summary

| Strategy | Definition | Status |
|----------|-----------|--------|
| A | FROZEN RETROSPECTIVE FALLBACK | FROZEN |
| B | SAME-VESSEL CAUSAL REPLAY + PERFORMANCE HARDENED + PHYSICAL VESSEL MOTION HARDENED + VIEWER BACKEND BASELINE FROZEN | ACTIVE |

Strategy A (frozen retrospective fallback) is kept as a safety net.
Strategy B (same-vessel causal replay) is the active mainline.
Full 144h historical causal replay = NOT SUPPORTED BY CURRENT PROVENANCE.

## Capability Matrix

| Capability | Status | Maturity |
|-----------|--------|----------|
| Causal replay engine | COMPLETE | AUTHORITATIVE_PASS |
| Performance hardening | COMPLETE | AUTHORITATIVE_PASS |
| Physical vessel motion | COMPLETE | AUTHORITATIVE_PASS |
| Deferred replan adoption | COMPLETE | AUTHORITATIVE_PASS |
| Presentation Adapter | ESTABLISHED | SMOKE_PASS |
| GEBCO L2 Preflight | ESTABLISHED | SMOKE_PASS |
| Replay-driven Viewer MVP | COMPLETE | REAL_ARTIFACT_SMOKE_PASS |
| Simulation Timeline | COMPLETE | MVP_PASS |
| Moving Ship | COMPLETE | MVP_PASS |
| Deferred Adoption Presentation | COMPLETE | MVP_PASS |
| Dynamic Risk Overlay | NEXT | NOT_IMPLEMENTED |
| Final Viewer UI Polish | NOT STARTED | NOT_IMPLEMENTED |

## Key Metrics (latest authoritative)

| Metric | Value | Source |
|--------|-------|--------|
| 12h replay duration | ~21.8 min (pre-hardening) / ~34 min (post-deferred) | STRATEGY_B_PERFORMANCE_HARDENING report |
| 12h baseline | PASS | sb-viewer-baseline-12h-det |
| Determinism | PASS (inherited, not re-run this round) | STRATEGY_B_VIEWER_MVP report |
| Manifest digest | 1bdcbce5... | causal-replay-manifest.json |
| A bundle | a-bundle-32cafad4ee280f286d8eb049 | work_package_a |
| L2 preflight | PASS | replay-viewer-preflight.json |
| Timeline frames | 721 | bundle.json |

## Version Summary

| Package | Version |
|---------|---------|
| arctic_route_contracts | 0.3.0 |
| work_package_a | 0.4.2 |
| work_package_b | 0.2.0 |
| work_package_c | 0.4.0 |
| work_package_d | 0.1.0 |
| arctic_route_orchestrator | 0.1.0 |

## Ownership

| Capability | Owner |
|-----------|-------|
| Replay / Snapshot / Manifest | Orchestrator |
| Navigation execution / replan lifecycle | Orchestrator |
| Presentation Adapter (business semantics) | Orchestrator |
| L1/L2 preflight | Orchestrator |
| Presentation artifact export | Orchestrator |
| Viewer application (HTML/JS/CSS) | D |
| Simulation Clock UI | D |
| Ship / route / track rendering | D |
| Static server | D |
| Proof renderer | D |

## Governance

- `/root/my_project` is a plain workspace (no root Git repo).
- Governance docs live in `arctic_route_governance/` (this repo).
- Branch mapping: main=RC1 frozen, rc2-development=RC2 frozen, demo-engineering=active.
- Documentation follows `standards/ENGINEERING_GOVERNANCE_STANDARD.md`.

## Known Limitations

1. Full 144h historical causal replay is not supported by current provenance.
2. Pending-Plan Gate (performance debt): deferred adoption causes TIME-only candidates to be recomputed during pending period, increasing runtime from ~21.8 min to ~34 min. Tracked as TD.
3. Edge-interior planner origin: physical vessel position may differ from planner origin node at mid-edge replan. Tracked as TD.
4. Browser runtime may be environment-blocked; proof PNG + bundle tests substitute for live browser smoke.
5. Dynamic Risk Overlay not yet implemented.

## What Is NOT Done

- Dynamic Risk Overlay (NEXT)
- Hard Reason overlay (NEXT)
- Superseded route visualization (NEXT)
- Replanning event animation (NEXT)
- Final UI polish (NOT STARTED)
- Demo rehearsal (NOT STARTED)
- Final freeze (NOT STARTED)
