---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - BLOCKED
Document Role: SUPPORTING
Scope: Winter experiment identity setup round
Canonical/Supporting: Supporting delivery report; canonical state is current/reference/WINTER_SCENARIO_STATUS.md
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Winter Experiment Identity Setup Report

## 1. Current State（2026-08-22 22:24 +08:00）

```text
WINTER_DATASET_STATUS = FROZEN_ARTIFACT_READY
A_TO_B_FORMAL_HANDOFF = BLOCKED_BY_BUNDLE_MINIMUM_HORIZON
B_WINTER_VALIDATION = NOT_STARTED
C_WINTER_VALIDATION = NOT_STARTED
D_WINTER_VISUALIZATION = NOT_STARTED
```

The intended transition to `READY_FOR_B_VALIDATION` was not made because the existing contract
generator rejected the frozen bundle. Scientific and interface truth takes priority over forcing the
requested milestone.

## 2. Created Files（2026-08-22 22:24 +08:00）

Created governance evidence:

- `WINTER_EXPERIMENT_IDENTITY_AUDIT.md`
- `WINTER_HANDOFF_VALIDATION_REPORT.md`
- this setup report

Not created:

- formal Winter RunContext;
- formal Winter ExecutionSpec;
- B/C/D artifacts.

## 3. RunContext Identity（2026-08-22 22:24 +08:00）

Expected binding was scenario `tromso_isfjorden_february_2026_research_v1`, corridor
`tromso_to_isfjorden_outer`, vessel `nordic_odyssey_reference_v1`, and bundle
`a-bundle-bd8957c4f10c7c73f395de23`. Generation failed before publication because the bundle's
minimum horizon does not cover the scenario end.

## 4. ExecutionSpec Identity（2026-08-22 22:24 +08:00）

No orphan ExecutionSpec was committed. Existing schema v1 cannot legally embed bundle SHA, Git
versions, or B/C configuration paths. A future spec will use the existing strict fields and share the
valid RunContext run/scenario identity; external version evidence remains in the experiment report.

Current code baselines:

| Component | Version | Git HEAD |
|---|---|---|
| contracts | 0.3.0 | `c19e910fa408bd4bd30bc83f621f82ebc41910ff` |
| A | 0.4.2 | `60b01edaabf281368a8a28ffa08a8db8f0e5a52b` |
| B | 0.2.0 | `a6dfa6c196d36ae17eed17aea19e6ea11c51287a` |
| C | 0.4.0 | `beae73a7151d47c6c5f91c06db198e256738dc43` |
| Orchestrator | 0.1.0 | `89e61e33e01d468db4d23df0be9498140a67fe84` |

B configuration remains pending approval. Existing Tromsø medium config is evidence, not an
automatically approved Winter production profile. C's current `planner/default.toml` remains
unchanged.

## 5. Handoff Validation（2026-08-22 22:24 +08:00）

Bundle identity, source coverage and shared configs passed their lightweight checks. The mandatory
RunContext gate failed on the 132 h minimum horizon; consequently RunContext schema validation,
ExecutionSpec binding and Orchestrator intake could not truthfully pass.

| Validation | Result |
|---|---|
| contracts shared-config CLI | PASS; 2 corridors / 8 scenarios / 1 vessel |
| contracts focused tests | 19 passed in 0.59 s |
| contracts Ruff | PASS |
| Orchestrator execution-spec/intake/schema focused tests | 5 passed in 0.79 s |
| Orchestrator focused Ruff | PASS |
| bundle consumer verification | PASS; 0.06 s wall, 22,696 KiB peak RSS |
| RunContext official creation | EXPECTED FAIL-CLOSED; under 1 s |
| B/C/D pipeline | NOT_RUN |

## 6. Documentation Changes（2026-08-22 22:24 +08:00）

- `CURRENT_STATUS.md`: source acquisition/bundle complete; identity gate blocked.
- `CURRENT_ROADMAP.md`: next work changed from data acquisition to corrected immutable bundle
  publication and identity validation.
- `WINTER_SCENARIO_STATUS.md`: conflicting 9/12, generation-ready and not-implemented statements
  were replaced by one canonical state.
- `DOCUMENTATION_INDEX.md`: latest Winter gate evidence now points to this report.

No archive or historical report was modified.

## 7. Remaining Risks（2026-08-22 22:24 +08:00）

1. Existing frozen bundle cannot bind the 144 h scenario under current contracts.
2. Publishing a corrected bundle will produce a new ID/digest; references must not be silently
   reused.
3. B production grid/model profile remains pending approval.
4. ExecutionSpec v1 does not own external file SHA or code/config version metadata; this is recorded
   as an interface boundary, not patched ad hoc.

## 8. Next Recommended Step（2026-08-22 22:24 +08:00）

Authorize A to publish a new immutable bundle from the same verified records with
`requested_end=minimum_required_end=2026-02-21T00Z`. Preserve the current bundle unchanged. Then
create RunContext and ExecutionSpec via existing generators, run intake-only, and begin Winter B
Risk Validation only after `READY_FOR_B_VALIDATION` is genuinely achieved.

```text
PUSH = NOT PERFORMED
B/C/D PIPELINE = NOT RUN
FROZEN BUNDLE = UNCHANGED
CONTRACT/ALGORITHM/VIEWER = UNCHANGED
```
