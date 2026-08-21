---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - PLANNED
Document Role: SUPPORTING
Scope: D Viewer, 48h replay, research visualization, and presentation gaps
Canonical Current State: NO
Branch: research-validation-system
Last Verified: 2026-08-21
---

# D Research Enhancement Analysis

## 已实现与已验证（2026-08-21 23:18）

D owns the only Viewer runtime under `work_package_d/viewer/`. It consumes
`replay.viewer-bundle.v1`, basemap metadata and PNG output from Orchestrator; it does not import
orchestrator/B/C Python internals. Current functionality includes GEBCO basemap, exact-cell risk and
hard availability, Current/+6/+12/+24 horizon selection with unavailable fail-closed state,
authoritative/pending/superseded routes, completed track, ETA-derived moving ship and heading, one
Simulation Clock, play/pause/scrub/speed, presentation/debug modes, route evolution and summary panels.

The frozen 48h product report records a real 10:00→+48h timeline with 49 replay snapshots, 2881
minute presentation states, 49 formal risk frames and route evolution R1–R19 with R20 pending. Firefox
E2E evidence covers load, risk/horizons, moving ship, pending/adopted transitions, controls and clean
console/network. These are inherited baselines; this documentation round did not relaunch Firefox.

## Route candidates and environment readiness（2026-08-21 23:18）

The Viewer can consume an optional candidate list and truthfully renders an empty-state, but current
export publishes `presentation.route-candidates.v1` as `NOT_PUBLISHED` with no candidate geometry or
metrics. Therefore fastest/low_risk/recommended comparison in the replay Viewer is NOT_IMPLEMENTED.
Route revisions must not be relabelled as objective candidates.

The bundle has aggregate B risk cells and hard reasons plus summaries. It does not publish complete
presentation-ready sea ice, wind, wave, current and temperature layers or per-cell contributor
decomposition. Those professional layers are NOT_IMPLEMENTED. D must not bypass the adapter to read A
private files or recompute B.

## 研究展示缺口（2026-08-21 23:18）

| Capability | State | Dependency |
|---|---|---|
| Candidate layer/objective compare | NOT_IMPLEMENTED | versioned Orchestrator projection of real C v3 data |
| Artifact/provenance research inspector | PARTIAL | bundle identity exists; UI needs structured evidence view |
| Grid/resolution/comparison view | NOT_IMPLEMENTED | presentation metadata + UX |
| Environment factor layers | NOT_IMPLEMENTED | reviewed presentation contract and exported cells/vectors |
| Cell/ship risk explanation | PARTIAL | summaries exist; contributor fields generally absent |
| Professional navigation symbology | PLANNED | D-only presentation work after semantic inputs exist |

## 性能与数据策略（2026-08-21 23:18）

Current Viewer consumes presentation-ready JSON/cells and a cached basemap; it does not load NetCDF or
run raw-grid risk calculations per animation frame. Ship rendering is continuous while risk frames are
hourly. Research additions should preserve frame-index/cache selection, avoid copying all layers into
every minute state, and measure bundle bytes, initial load, scrub/horizon switch latency and browser
memory. Large environment grids should use optional/lazy presentation packages rather than duplicating
raw A arrays in the main bundle.

## P4 建议（2026-08-21 23:18）

1. Freeze current v1 Viewer compatibility and explicit NOT_PUBLISHED/unavailable states.
2. Add candidate fixtures only after the C→D proposal has real geometry/metrics and provenance.
3. Add a research inspector for artifact identity, grid policy, valid/issue/knowledge times, hard/unknown
   distribution and validation level.
4. Add environment layers one contract at a time; preserve hard masks and uncertainty separately.
5. Require Firefox E2E and console/network checks for each new optional package, while keeping the
   frozen 48h bundle runnable unchanged.
