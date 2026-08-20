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
| Presentation Adapter | ESTABLISHED | REAL_ARTIFACT_HTTP_SMOKE_PASS |
| GEBCO L2 Preflight | ESTABLISHED | REAL_ARTIFACT_HTTP_SMOKE_PASS |
| Replay-driven Viewer MVP | COMPLETE | BROWSER_E2E_PASS |
| Simulation Timeline | COMPLETE | BROWSER_E2E_PASS |
| Moving Ship | COMPLETE | BROWSER_E2E_PASS |
| Deferred Adoption Presentation | COMPLETE | BROWSER_E2E_PASS |
| Dynamic Risk Overlay (current frame) | COMPLETE | BROWSER_E2E_PASS |
| Risk Horizon Presentation (Current/+6h/+12h/+24h) | COMPLETE | BROWSER_E2E_PASS |
| Hard Reason / Availability Overlay | COMPLETE | BROWSER_E2E_PASS |
| Route / Replanning Visualization | MVP COMPLETE | BROWSER_E2E_PASS |
| Presentation / Engineering Mode | COMPLETE | BROWSER_E2E_PASS |
| Presentation Layer Controls | COMPLETE | BROWSER_E2E_PASS |
| Final Viewer UI Polish | NEXT | IMPLEMENTED |

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
| Risk horizon selections | Current/+6h/+12h/+24h with fail-closed availability | presentation.risk-overlay.v1 |
| Product-round integration | 2 passed / 2334.71s / 38:54 | `.runtime/test-logs/orchestrator-integration-horizons-20260820.log` |

## Viewer Product Mainline（2026-08-20 22:50 +08:00）

The governance phase is closed for this milestone. The current product
milestone is **Viewer Product Mainline**. The existing formal artifact
`sb-viewer-baseline-12h-det` is exported through the Orchestrator adapter and
rendered by D. A real Firefox browser run verified GEBCO, active route,
completed track, continuous vessel motion, current-risk frames, separate hard
reasons, pending/adopted route states, controls, and zero console errors.

The Viewer contract is now:

- Orchestrator owns presentation export and validates formal B risk frames;
- D is the sole Viewer runtime owner and uses one Simulation Clock;
- `REPLAN_DECIDED` exposes pending future state, while `REPLAN_ADOPTED`
  changes the active route at the effective time;
- completed track remains append-only; `DATA_UNAVAILABLE` and other hard
  reasons are not rendered as safe risk;
- current/+6h/+12h/+24h risk selections are presentation-complete; exact,
  floor, and unavailable semantics are explicit in the export contract;
- Presentation Mode defaults to a clean demo view, while Engineering Debug
  remains available; Risk, Hard/Availability, Routes, and Completed Track are
  independently toggleable;
- 10:30 +6h displays 16:00 / actual +5h30m; 10:30 +12h/+24h show UNAVAILABLE
  because their requested valid times exceed the 22:00 formal frame range.

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

- `/root/my_project` is a **recovery / historical safety source** that still retains
  its original ProjectDoc Git repo (`demo-engineering` @ `3812b5d`). It is intentionally
  NOT retired this round. Governance docs live in `arctic_route_governance/` (this repo),
  which is the canonical governance source. Final root-Git retirement is a human-reviewed
  cutover step (not performed by automation).
- Branch mapping: main=RC1 frozen, rc2-development=RC2 frozen, demo-engineering=active.
- Documentation follows `standards/ENGINEERING_GOVERNANCE_STANDARD.md`.

## Known Limitations

1. Full 144h historical causal replay is not supported by current provenance.
2. Pending-Plan Gate (performance debt): deferred adoption causes TIME-only candidates to be recomputed during pending period, increasing runtime from ~21.8 min to ~34 min. Tracked as TD.
3. Edge-interior planner origin: physical vessel position may differ from planner origin node at mid-edge replan. Tracked as TD.
4. The default restricted sandbox blocks browser daemon/socket startup, but the
   attended run used the available escalated local Firefox path and completed
   the browser E2E baseline. This is an execution-environment note, not a
   product verification gap.
5. Rich route-transition animation, final visual polish, demo rehearsal, and
   final freeze remain open. Horizon availability is intentionally bounded by
   the existing formal artifact and is not extrapolated.

## What Is NOT Done

- Dynamic Risk + Hard Reason + Current/+6h/+12h/+24h horizon presentation are
  complete; unavailable horizons fail closed.
- Superseded route visualization and adoption-state presentation are complete
  at MVP level; richer animation remains NEXT.
- Final UI polish (NEXT)
- Demo rehearsal (NOT STARTED)
- Final freeze (NOT STARTED)
