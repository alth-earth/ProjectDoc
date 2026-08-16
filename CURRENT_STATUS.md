# Current Status

Status: CURRENT
Last Updated: 2026-08-16
Applies To: entire Arctic Route project
Authoritative For: current milestone and status matrix

## Current Milestone

**Demo RC1 Frozen Baseline established (2026-08-16).**

Exact identifiers are authoritative in
[`work_package_a/docs/DEMO_RC1_BASELINE_20260816.md`](work_package_a/docs/DEMO_RC1_BASELINE_20260816.md).

## Current Versions

- contracts 0.3.0 / corridor 2.2.0 / scenario murmansk_dikson_august_2026_demo_v1 v1.0.0
- A 0.4.2, B 0.2.0, C 0.4.0, D 0.1.0, orchestrator 0.1.0
- bundle `a-bundle-32cafad4ee280f286d8eb049`
- RunContext `run-00000000-0000-4000-8000-0000000b0005`

## Status Matrix

| Area | Status |
|---|---|
| A data / TOPAZ originalGrid rebuild | PASS |
| Spatial coverage gate (unknown-navigable = 0) | PASS |
| B risk build (hard_mask=land_sea_mask_plus_unknown_v1) | PASS |
| C initial planning (v3 four layers) | PASS |
| 6 h replanning | PASS |
| D real v3 artifact consume | PASS |
| Business-semantic deterministic reproducibility (r6 vs r7) | PASS |
| Interruptible per-stage timeout mechanism | PASS (unit tests) |
| Worker-mode full RC1 E2E | NOT RUN |
| Offline runtime dependency audit | PASS (NONE) |
| same-VHD backup copies | PASS (not independent disaster backup) |

## Current Non-blocking Tech Debt

See [`TECH_DEBT.md`](TECH_DEBT.md). Highlights:
TD-1 worker-mode full-chain smoke; TD-2 hard_reason semantics; TD-3 independent
backup target; TD-4 optional planner optimization.

## Next Actions (priority)

1. Worker-mode full RC1 smoke (pre-demo mandatory);
2. Live Demo Mode rehearsal;
3. Recovery rehearsal from the two same-VHD copies;
4. Independent backup once an external path is provided.

See [`POST_RC1_PLAN.md`](POST_RC1_PLAN.md).

## Frozen Until RC2

Do not change without a correctness/safety bug or explicit operator decision:
data products, corridor 2.2.0, scenario, risk semantics, C cost, A interpolation,
hard-mask policy, planning algorithm, RC1 artifacts.
