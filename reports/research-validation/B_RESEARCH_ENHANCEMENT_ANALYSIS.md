---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - PLANNED
Document Role: SUPPORTING
Scope: B risk grid, performance, winter readiness, and research gaps
Canonical Current State: NO
Branch: research-validation-system
Last Verified: 2026-08-21
---

# B Research Enhancement Analysis

## 当前实现（2026-08-21 23:18）

`RiskBuildService.build_window()` realizes `TargetGridConfig` over the requested bbox, selects and
interpolates A variables for each output hour, then emits latitude×longitude RiskFrames. The code
default is 0.75° latitude × 2.2° longitude; the explicit Tromsø RC2 config is 0.375° × 1.25° and
realizes 31×11 cells over 10–22°E, 68.5–79.5°N (actual spacing about 0.3667°×1.2°). Tests using the
default config therefore realize 16×7; 31×11 is not a global default.

The model is an 11-component deterministic weighted rule, emits score/level 1–5, hard mask/reason,
confidence and speed factor, and is correctly labelled `demo_unvalidated`. Unknown inputs fail closed;
current canonical reasons are NONE/LAND/DATA_UNAVAILABLE/OTHER.

## 性能与内存（2026-08-21 23:18）

Cost scales approximately with output hours × cells × variables; each hour may perform one or two
xarray spatial interpolations per variable, and the full frame tuple is materialized. Read-only NumPy
consumer views avoid copies and A cache defaults to 512 MiB, but B has no isolated latency/RSS
benchmark by grid and horizon. The historical ~0.97 GiB measurement is end-to-end worker evidence,
not a B-only metric.

## 冬季与 Adaptive Grid readiness（2026-08-21 23:18）

A already supports ice concentration, drift, thickness and deterministic ice type/edge derivation,
plus exact bundle resolution. No current winter scenario or provenance-complete winter artifact was
found. Adaptive grid is not implemented: configuration is exact-key fixed rectilinear, and C requires
strictly increasing one-dimensional axes matching RiskFrame coordinates.

## 研究建议与风险（2026-08-21 23:18）

1. Freeze the current grid policy/config/grid digest evidence and correct the 31×11 vs 16×7 wording.
2. Build a real winter 12-type A bundle before claiming winter validation.
3. Benchmark fixed grids first: B wall time/RSS, hard/unknown share, aliasing and downstream C
   route/ETA/integrity.
4. Prototype adaptive grid only as a versioned sidecar with parent mapping and cross-package tests.
5. Treat model calibration as a separate research stream with new model identity; do not overwrite
   `demo_unvalidated` evidence.

Risks: uncalibrated numeric output, no winter artifact, no B-only benchmark, default/config grid
ambiguity, and current treatment of non-finite land mask as LAND rather than a distinct availability
reason.
