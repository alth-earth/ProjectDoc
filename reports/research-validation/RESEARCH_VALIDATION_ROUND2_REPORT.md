---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - BLOCKED
  - PLANNED
Document Role: SUPPORTING
Scope: Research Validation Experiment Phase Round 2 implementation and evidence
Canonical/Supporting: Supporting engineering report; current/ remains canonical
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Research Validation Round 2 Report

## Key delta（2026-08-22 01:11 +08:00）

| Claim | Before | After | Evidence | Verdict |
|---|---|---|---|---|
| Winter feasibility | config skeleton; dataset unknown | 12/12 local February rows absent | read-only target-corridor inventory | BLOCKED_BY_DATASET |
| B grid experiment | synthetic kernel only | 78 real formal B frames × 3 grids | B formal comparison | EXPERIMENTAL / PASS |
| B→C scaling | not measured | 112-node 10.51 s; 341-node 75.00 s | real B frames + real C search | EXPERIMENTAL / PASS |
| C cache evidence | component profile | edge geometry hit/miss counters | unit + benchmark | IMPLEMENTED / UNIT_PASS |
| Candidate presentation | PLANNED | backward-compatible DRAFT proposal | ownership/field/invariant review | PLANNED |
| Frozen semantics | unchanged | unchanged | diff/contract boundary audit | PRESERVED |

The round achieved its evidence goal without changing contract schema versions,
risk semantics, C route/ETA/search semantics, production defaults, frozen
artifacts, replay data, or D Viewer code.

## Winter data result（2026-08-22 01:11 +08:00）

`tromso_isfjorden_february_2026_research_v1` remains a validated configuration,
not an artifact. A can express the acquisition and publication workflow, but the
local target corridor has zero February 2026 records for all 12 required data
types. No download was attempted. The only local GEBCO mask is issued after the
scenario window, so a retrospective static-product exception also needs an
explicit knowledge-time decision.

Canonical state:
[WINTER_SCENARIO_STATUS.md](../../current/reference/WINTER_SCENARIO_STATUS.md).
Supporting matrix:
[WINTER_DATA_FEASIBILITY_REPORT.md](WINTER_DATA_FEASIBILITY_REPORT.md).

## B formal grid experiment（2026-08-22 01:11 +08:00）

One A public PreparedWindow supplied 78 hourly formal frames to sequential B
builds. All outputs used the existing risk model and `bc.risk-frame.v2`.

| Profile | Grid | Cells/frame | B build | Sampled RSS | JSON bytes |
|---|---:|---:|---:|---:|---:|
| baseline | 16×7 | 112 | 4.032 s | 920,720 KiB | 1,062,380 |
| medium | 31×11 | 341 | 3.861 s | 922,696 KiB | 2,202,408 |
| fine | 60×21 | 1,260 | 3.914 s | 925,136 KiB | 6,744,836 |

The complete run took 94.06 s wall and 954,704 KiB maximum RSS. B-only timing
was nearly flat at this scale; artifact volume increased materially. RSS includes
the already-loaded A window and is not B incremental memory.

All finite navigable cells remained Level 1 for this summer artifact. Hard Level
5 cells stayed separate: LAND plus DATA_UNAVAILABLE. No Level 2–4 signal appeared,
so grid refinement did not create risk contrast or scientific validity.

## B-C coupling result（2026-08-22 01:11 +08:00）

| Grid | Nodes | Planning | Peak RSS | Expansions | Generated | Status |
|---|---:|---:|---:|---:|---:|---|
| baseline | 112 | 10.506 s | 97,336 KiB | 2,247 | 4,232 | SUCCESS |
| medium | 341 | 75.001 s | 122,420 KiB | 15,349 | 20,839 | SUCCESS |

Medium/baseline ratios were 3.045× nodes, 7.139× planning time, 1.258× sampled
RSS and 6.831× expansions. The complete sequential C command took 86.29 s and
121,080 KiB maximum RSS without swap.

Fine has 1,260 nodes, 3.70× medium. No runtime was fabricated and no fine search
was started without an explicit wall/expansion budget. The next grid decision
must account for C cost, not just B generation speed.

## C optimization direction（2026-08-22 01:11 +08:00）

Only observational counters were added to the existing edge-geometry cache.
The medium run recorded 248,720 hits and 1,783 misses/entries. This proves
geometry reuse, not risk-sample reuse: ETA and valid time are part of sampling.

The approved next evidence step is exact sample-key counting, followed by a
shadow cache and only then a bounded default-off LRU if repeats are material.
Shared search, heuristic changes and incremental replanning remain out of scope.

## Route presentation proposal（2026-08-22 01:11 +08:00）

C's validated 4 layers × 3 objectives remain real. The replay Viewer still does
not consume them because Orchestrator publishes candidate status
`NOT_PUBLISHED`. Proposal `RVS-RCP-001` defines an optional additive
`presentation.route-candidates.v1` package with C-owned geometry/objective/
metrics/provenance and Orchestrator-owned projection. It is `DRAFT`; no schema,
producer or consumer changed.

## Code and documentation changes（2026-08-22 01:11 +08:00）

### B（2026-08-22 01:11 +08:00）

- real formal grid experiment helper and sequential CLI;
- unit test, README/CHANGELOG and formal comparison report;
- unpublished experimental frame transport for bounded C measurement.

### C（2026-08-22 01:11 +08:00）

- real-frame coupling helper and sequential CLI;
- observational edge-cache counters in planner/profile output;
- unit tests, README/CHANGELOG, coupling report and optimization proposal.

### Governance（2026-08-22 01:11 +08:00）

- winter feasibility report and canonical winter status update;
- candidate presentation proposal and registry link;
- current status/roadmap/gap/debt/index synchronization.

No file changed in A, D, Orchestrator or `arctic_route_contracts`.

## Validation（2026-08-22 01:11 +08:00）

| Scope | Command | Result | Level |
|---|---|---|---|
| B | `uv run pytest -q -m 'not integration'` | 61 passed, 8 deselected | UNIT_PASS |
| B | `uv run ruff check .` | clean | LINT_PASS |
| B | `python -m py_compile` experiment files | pass | SYNTAX_PASS |
| C | `uv run pytest -q -m 'not integration'` | 146 passed | UNIT_PASS |
| C | `uv run ruff check .` | clean | LINT_PASS |
| C | `python -m py_compile` experiment files | pass | SYNTAX_PASS |
| B formal experiment | 3 profiles, real A archive | success | EXPERIMENTAL_REAL_DATA_PASS |
| C coupling experiment | baseline + medium | success | EXPERIMENTAL_REAL_DATA_PASS |

Heavy integration, 48h replay, 12h determinism twin-run and Browser E2E were not
run because no replay, production export, D runtime or authoritative semantics
changed. Their prior evidence is inherited, not requalified by this report.

## Unexpected findings（2026-08-22 01:11 +08:00）

1. The first B execution completed all three expensive builds but failed while
   formatting the final report because the harness referenced a nonexistent
   aggregate `DatasetBundle.provenance_complete` attribute. The fix now derives
   completeness from coverage items and writes each profile summary immediately.
   The failed output was preserved under `.runtime` and never published.
2. `baseline` is the B code-default 16×7 control, while the current Tromsø
   presentation grid is the 31×11 `medium` profile. Reports now use both name and
   dimensions to avoid ambiguity.
3. B runtime did not rise with cell count in this bounded experiment, but C
   planning rose super-linearly. Optimizing only B would miss the system limit.
4. The February GEBCO issue date creates a separate retrospective knowledge-time
   decision even if dynamic winter data later becomes available.

## Remaining next（2026-08-22 01:11 +08:00）

1. Probe remote winter metadata and credentials without downloading bulk data.
2. Repeat B/C measurements to establish variance and isolate B incremental RSS.
3. Add exact risk-sample repetition counters before implementing any cache.
4. Run a fine-grid C pilot only with explicit wall time, expansion and memory caps.
5. Obtain C/Orchestrator/D owner review for `RVS-RCP-001`; do not publish
   candidates until the atomic real-artifact gate passes.

Round status: `RESEARCH_VALIDATION_EXPERIMENT_PHASE = EVIDENCE_BASELINE_PASS`.
