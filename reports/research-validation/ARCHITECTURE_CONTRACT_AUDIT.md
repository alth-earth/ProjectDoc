---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - PLANNED
Document Role: SUPPORTING
Scope: A/B/C/D/Orchestrator architecture and contract evidence audit
Canonical Current State: NO
Canonical Architecture: ../../current/architecture/ARCTIC_ROUTE_SYSTEM.md
Branch: research-validation-system
Last Verified: 2026-08-21
---

# Architecture and Contract Audit

## 当前 producer-consumer 链（2026-08-21 23:18）

| Boundary | Producer output | Consumer input | State |
|---|---|---|---|
| Contracts→all | corridor/scenario/vessel/RunContext identities | package loaders | IMPLEMENTED + VALIDATED |
| A→B | `PreparedWindow`, persisted `a.dataset-bundle.v2` | `BInputEnvelope` exact resolver | IMPLEMENTED + VALIDATED |
| B→C | `bc.risk-frame.v2` hourly frames | `RiskSourcePlanningIngress` | IMPLEMENTED + VALIDATED |
| C output | `RoutePlan.v2`; `FourLayerRoutePlanSet.v3` | artifact consumers / Orchestrator | IMPLEMENTED + VALIDATED |
| Replay→presentation | navigation snapshots/events/risk frames | `replay.viewer-bundle.v1` | IMPLEMENTED + VALIDATED |
| C candidates→replay Viewer | candidate sets with geometry/metrics | D candidate UI | NOT_IMPLEMENTED / NOT_PUBLISHED |

## A/B/C/D 真实能力（2026-08-21 23:18）

- **A** publishes standardized arrays, temporal/provenance metadata and exact artifact identity.
  `PartitionedABCache` is A-owned internal acceleration, not the B public contract.
- **B** consumes only A public objects and emits risk score/level, hard mask/reason, confidence and
  environment speed factor on a realized rectilinear target grid. It does not plan routes.
- **C** consumes validated B frames, owns final speed/ETA/cost/search/replanning, and can atomically
  publish four required layers with fastest/low_risk/recommended for exactly 12 routes.
- **D** owns HTML/JS/CSS/static runtime and consumes only bundle/PNG data. It never imports B/C
  internals or calculates authoritative risk/route/ship physics.
- **Orchestrator** coordinates replay/navigation and owns validation/projection/export. It does not
  own a second Viewer runtime.

## 12-route evidence and publication gap（2026-08-21 23:18）

`work_package_c/src/arctic_route_planning/contracts/layered.py` defines four required layers and
requires three objectives per layer; `FourLayerRoutePlanSet` rejects any total other than 12.
RC1 r6/r7 initial and replanned v3 JSON/GeoJSON prove real artifact publication and D's static v3
loader can consume all 12.

Current replay export is different: `arctic_route_orchestrator/scripts/replay_viewer_export.py`
publishes `presentation.route-candidates.v1` with `status=NOT_PUBLISHED`, empty `candidates`, and
reason `candidate_geometry_and_metrics_not_published`. Current 48h bundle route revisions are
successive authoritative plans, not simultaneous candidates.

## Contract ownership risk（2026-08-21 23:18）

Shared package owns identities and cross-run context; B/C schemas also live in package repositories;
presentation schemas are implemented in Orchestrator. Before parallel development, create a registry
with contract name/version, owner, producer, consumer, compatibility promise, fixtures and tests.

## Backward-compatible proposal direction（2026-08-21 23:18）

Do not mutate frozen schemas. A future `presentation.route-candidates.v2` should add versioned
candidate sets keyed by planning layer and decision time, with objective, geometry, metrics,
source RiskFrame IDs, selected candidate and provenance. V1 empty status must remain valid; export
must fail closed when geometry or metrics are incomplete. Orchestrator projects but does not invent;
D displays but does not rank.

Adaptive grid similarly needs a proposal carrying grid policy/version, realized coordinate digest,
parent mapping and compatibility with C's one-dimensional strictly increasing regular axes.
