---
Overall Status: DRAFT
Content Status:
  - COMPLETED
  - PLANNED
Document Role: CANONICAL
Scope: backward-compatible publication of real C layered route candidates to D
Canonical/Supporting: Canonical proposal only; not an approved or implemented contract change
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Route Presentation Contract Proposal

## Proposal identity and status（2026-08-22 01:11 +08:00）

| Field | Value |
|---|---|
| Proposal | `RVS-RCP-001` |
| State | `DRAFT / PLANNED` |
| Semantic owner | C for route candidates; Orchestrator for presentation projection |
| Consumer owner | D |
| Target package | additive `presentation.route-candidates.v1` inside `replay.viewer-bundle.v1` |
| Existing schema versions | unchanged |

This proposal does not authorize implementation. Current Viewer truth remains
`status=NOT_PUBLISHED`, `candidates=[]`.

## Current capability and gap（2026-08-22 01:11 +08:00）

C has validated `cd.four-layer-route-plan-set.v3`: four layers × three
objectives, atomically complete, for 12 real route results. D's static loader can
consume this shape. The replay Viewer does not receive it because Orchestrator
currently projects only authoritative, pending and superseded route state and
explicitly emits candidate status `NOT_PUBLISHED`.

The missing capability is the presentation projection at C→Orchestrator→D. It
is not evidence that C lacks candidates, and D must not invent or rank them.

## Proposed optional package（2026-08-22 01:11 +08:00）

```json
{
  "schema_version": "presentation.route-candidates.v1",
  "status": "PUBLISHED",
  "candidate_set_id": "...",
  "layer_set_id": "...",
  "decision_time": "...Z",
  "selected_candidate_id": "...",
  "provenance": {"source_schema": "cd.four-layer-route-plan-set.v3"},
  "candidates": [
    {
      "candidate_id": "...",
      "layer": "full_voyage",
      "objective": "recommended",
      "geometry": {"type": "LineString", "coordinates": []},
      "distance_km": 0,
      "arrival_eta": "...Z",
      "travel_hours": 0,
      "risk_metrics": {
        "average_risk": 0,
        "maximum_risk": 0,
        "integrated_risk": 0,
        "minimum_confidence": 0,
        "hard_violation_count": 0
      },
      "provenance": {}
    }
  ]
}
```

All numeric values, geometry, objective and selection identity must be copied
from validated C output or the Orchestrator's actual adoption state. The example
zeros are schema placeholders, not demo values or defaults.

## Publication invariants（2026-08-22 01:11 +08:00）

1. `PUBLISHED` requires one complete same-identity `layer_set_id`, generation,
   revision and decision time; partial sets fail closed.
2. Exactly the C-published layer/objective cardinality is projected. Orchestrator
   validates and packages but does not recompute metrics or choose a winner.
3. `selected_candidate_id` refers to C/Orchestrator authoritative selection; D
   only highlights it.
4. Geometry remains C route geometry. D may style it but cannot spline or move it
   as business data.
5. Missing or incompatible data remains `NOT_PUBLISHED` or `UNAVAILABLE` with an
   empty list. No fallback candidate is fabricated.
6. Candidate comparison does not alter authoritative/pending/adopted route state.

## Backward compatibility（2026-08-22 01:11 +08:00）

The package is optional in `replay.viewer-bundle.v1`. An old producer remains
valid and a new D consumer shows the existing single-route UI when absent or
`NOT_PUBLISHED`. An old D consumer may ignore the optional package. Existing
required fields and `presentation.route-candidates.v1` empty semantics are not
renamed or reinterpreted.

If implementation requires changing existing field units, cardinality,
selection meaning or failure behavior, this additive proposal is insufficient
and a versioned breaking-change proposal is required.

## Acceptance gate（2026-08-22 01:11 +08:00）

- C fixture proves complete 4×3 identity and metrics;
- Orchestrator producer tests prove atomic projection and partial-set rejection;
- D consumer tests cover absent, NOT_PUBLISHED, PUBLISHED and incompatible data;
- selected/recommended distinction is explicit and never computed in D;
- focused real-artifact integration compares projected values to source C JSON;
- frozen Viewer bundle and current single-route replay regressions remain green;
- C, Orchestrator and D owners approve before status changes from DRAFT.
