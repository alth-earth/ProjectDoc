---
Document Status: FROZEN_RC1
Branch: main
Frozen At: 2026-08-16
Canonical Current State: NO
Scope: Demo RC1 frozen baseline (challenge-cup demo delivery)
Canonical For: what RC1 was, what passed, what was NOT completed at freeze
Related Canonical Docs: current/CURRENT_STATUS.md, current/CURRENT_ROADMAP.md
---

# RC1 Frozen Status (main @ 29aa74d — "8-16demo交付")

> **FROZEN ≠ COMPLETE.** This document records RC1 as it actually stood at the
> 2026-08-16 freeze. Items that were NOT RUN / NOT COMPLETED at freeze are
> explicitly listed. Later Strategy B / RC2 / Viewer capabilities are NOT
> back-ported into RC1.

## 1. RC1 Identity

| Field | Value |
|---|---|
| Branch | `main` (frozen, do not modify) |
| Freeze commit | `29aa74d` ("8-16demo交付") |
| Synced to GitHub | yes (main) |
| Project type | 挑战杯 (Challenge Cup) demo — engineering demo pass = success |
| Authoritative baseline doc | `work_package_a/docs/DEMO_RC1_BASELINE_20260816.md` |

## 2. RC1 Version Vector (at freeze)

| Component | Version |
|---|---|
| contracts | 0.3.0 |
| corridor | 2.2.0 (`murmansk_dikson_august_2026_demo_v1` v1.0.0) |
| A `arctic_route_data` | 0.4.2 |
| B `arctic_route_risk` | 0.2.0 |
| C `arctic_route_planner` | 0.4.0 |
| D `arctic_route_display` | 0.1.0 |
| orchestrator | 0.1.0 |

## 3. RC1 Artifact Identities

| Artifact | Identity |
|---|---|
| A bundle | `a-bundle-32cafad4ee280f286d8eb049` |
| RunContext | `run-00000000-0000-4000-8000-0000000b0005` |
| Initial layer-set | `layer-set-sha256-51824e96…` |
| Replanned layer-set | `layer-set-sha256-ec74a145…` |
| Scenario | `murmansk_dikson_august_2026_demo_v1` (144 h, corridor 2.2.0) |
| Historical alternate scenario | `tromso_isfjorden_august_2026_demo_v1` (kept as separate evidence, not RC1 main) |

## 4. What PASSED at RC1 Freeze

| Capability | Evidence |
|---|---|
| A TOPAZ originalGrid reconstruction | unit + E2E (r6/r7) |
| Spatial coverage gate (unknown-navigable = 0) | PASS |
| B risk build (`land_sea_mask_plus_unknown_v1`) | PASS |
| C initial planning (v3 four-layer) | PASS |
| 6-hour replanning | PASS |
| D real v3 artifact consumption | PASS |
| Business-semantic determinism (r6 vs r7) | PASS |
| Per-stage interruptible timeout | PASS (unit test) |
| Offline runtime dependency audit | PASS (no external deps) |
| Same-VHD backup copy | PASS (not an independent DR target) |

## 5. What was NOT COMPLETED at RC1 Freeze (FROZEN / NOT_COMPLETED_AT_FREEZE)

| Capability | Status at freeze | Later resolution |
|---|---|---|
| Worker-mode full RC1 E2E smoke | **NOT RUN** (TD-1) | Completed during RC2 (real worker success + timeout smoke, 2026-08-17) |
| `hard_reason` semantics | **NOT IN RC1** (TD-2) | Added in RC2 (`hard_reason` optional field) |
| Independent backup target | **NOT RUN** (TD-3) | Still pending (operator decision) |
| Live Demo rehearsal | **NOT RUN** | Performed later (Strategy B / Viewer era) |
| Viewer / moving-ship presentation | **NOT IN RC1** | Built in Strategy B Viewer foundation + MVP (2026-08-19), migrated to D |
| Strategy B causal mainline | **NOT IN RC1** | Became active mainline on `demo-engineering` (frozen RC1/RC2 untouched) |

> Explicitly out of RC1 scope and frozen: data products, corridor 2.2.0, scenarios,
> risk semantics, C cost, A interpolation, hard-mask policy, planning algorithm,
> RC1 artifacts. RC1 must remain a regression / golden reference only.

## 6. Relationship to Later Stages

- **RC2** (`rc2-development`, frozen 2026-08-17): extended RC1 with ice-free
  semantics, second scenario (Tromsø 144h), `hard_reason`, coverage preflight.
  RC2 is a separate frozen baseline — see `../rc2-rc2-development/RC2_DEVELOPMENT_STATUS.md`.
- **Strategy B / Viewer**: `demo-engineering` active development. Strategy B is the
  active same-vessel causal mainline; the Viewer was migrated from orchestrator to
  `work_package_d` and reached MVP PASS (2026-08-19). None of this is part of RC1.

## 7. RC1 Freeze Invariants (must not regress)

- Do not modify `main` history or RC1 artifacts.
- Do not rewrite RC1 digests.
- RC1 is the golden baseline for regression checks (e.g. `rc1_golden_regression.py`).
