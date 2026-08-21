---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - EXPERIMENTAL
  - BLOCKED
  - PLANNED
Document Role: SUPPORTING
Scope: second-stage research validation acceleration implementation and evidence
Canonical Current State: NO
Branch: research-validation-system
Last Verified: 2026-08-22
Related Canonical Docs: ../../current/CURRENT_STATUS.md, ../../current/CURRENT_ROADMAP.md
---

# Research Validation Acceleration Report

## Key delta（2026-08-22 00:34）

| Priority | Before | After | Validation level | Verdict |
|---|---|---|---|---|
| P0 contract ownership | no unified registry/change gate | registry, proposal template and directory ownership | DOCUMENT_VALIDATED | COMPLETED BASELINE |
| P1 winter scenario | no winter identity or artifact | configuration skeleton exists; data/artifact absent | UNIT_PASS + BLOCKED_BY_DATASET | PARTIAL / TRUTHFUL |
| P2 B grid research | no isolated grid benchmark | baseline/medium/fine profiles and deterministic kernel benchmark | EXPERIMENTAL + UNIT_PASS | BASELINE ESTABLISHED |
| P3 C profiling | no repeatable component profile | real planner components profiled on labelled synthetic fixture | EXPERIMENTAL + UNIT_PASS | BASELINE ESTABLISHED |
| P3 cache correctness | sample count absent from geometry cache key | `minimum_samples` included and regression tested | UNIT_PASS | FIXED |
| P4 D navigation platform | demo map without professional aids | graticule, labels, haversine scale, grid north, aspect preservation | BROWSER_E2E_PASS | FOUNDATION ESTABLISHED |

Research credibility was kept ahead of feature count. No winter artifact,
adaptive grid, route candidate, environment layer or scientific calibration is
claimed.

## Scope and frozen boundaries（2026-08-22 00:34）

Unchanged:

- all RC1, RC2, Summer and 48h artifacts;
- all contract schema versions and existing field semantics;
- A acquisition/normalization/publication implementation;
- B risk formula, level policy, hard reasons and production grid default;
- C A* state/search, objective, route, ETA and replanning semantics;
- Orchestrator replay and presentation export;
- D ship position, single Simulation Clock, risk/horizon and route adoption semantics.

No heavy replay, full integration, network acquisition or determinism twin-run
was executed. The 12h authoritative determinism result remains inherited.

## P0 Contract Ownership Registry（2026-08-22 00:34）

Canonical additions:

- `current/reference/CONTRACT_OWNERSHIP_REGISTRY.md` identifies owner,
  producer, consumer, current version, status and compatibility boundary for
  A→B, B→C, C route plans, C→D presentation and Viewer bundle contracts;
- `standards/CONTRACT_CHANGE_PROPOSAL_TEMPLATE.md` requires semantic delta,
  fixtures, compatibility/failure behavior, resource evidence, rollback and
  owner approval;
- `current/DEVELOPMENT_OWNERSHIP.md` assigns repository write boundaries and
  producer-first integration order.

`FROZEN_COMPATIBLE` freezes observable meaning and failure behavior, not
implementation internals. `DRAFT` never authorizes production consumption.

## P1 Winter Scenario Preparation（2026-08-22 00:34）

| Field | Published configuration value |
|---|---|
| scenario | `tromso_isfjorden_february_2026_research_v1` |
| schema | existing `scenario.v2` |
| mode | `retrospective_best_estimate` |
| window | 2026-02-15 00:00Z → 2026-02-21 00:00Z |
| horizon | 144 hours |
| requirements | existing 12 formal data types |
| artifact | none |

The generic A interfaces can represent winter time windows and ice variables,
but no matching local provenance-complete 12-type source set was found. No
download was started. Current state is therefore:

```text
configuration = IMPLEMENTED / UNIT_VALIDATED
source dataset = BLOCKED_BY_DATASET
A DatasetBundle = NOT_IMPLEMENTED
B/C/D winter chain = NOT_IMPLEMENTED
```

The source and acceptance plan is canonical in
`current/reference/WINTER_SCENARIO_STATUS.md`.

## P2 B Grid Experimental Framework（2026-08-22 00:34）

The production `TargetGridConfig` default remains 0.75° latitude × 2.2°
longitude. Experimental profiles are isolated under
`configs/experiments/tromso_grid_profiles_v1.json`.

| Profile | Realized grid | Cells | Mean spatial kernel | Output bytes | Process peak RSS |
|---|---:|---:|---:|---:|---:|
| baseline | 16×7 | 112 | 24.610 ms | 9,856 | 131,880 KiB |
| medium | 31×11 | 341 | 24.622 ms | 30,008 | 132,136 KiB |
| fine | 60×21 | 1,260 | 24.534 ms | 110,880 | 132,136 KiB |

The deterministic benchmark uses synthetic arrays and B's xarray
linear/nearest regridding methods. Output bytes scale with cells, while fixed
xarray overhead dominates these small runs. The timing is not a full
RiskFrame-build or scientific-performance claim. A bounded formal A→B fixture
and downstream C comparison remain `PLANNED`.

Runtime JSON:
`/root/my_project/.runtime/test-logs/b-grid-kernel-20260822.json`.

## P3 C Profiling and low-risk hardening（2026-08-22 00:34）

The profiler drives the real `TimeDependentAStar`, `RiskSampler`, vessel and
cost implementations over a labelled 9×13, 13-frame synthetic fixture and all
three objectives.

| Component | Calls | Inclusive time | Inclusive / total |
|---|---:|---:|---:|
| total planner | — | 1.338443 s | 100% |
| edge traversal | 1,623 | 1.322514 s | 98.81% |
| risk sampling | 9,741 | 1.233091 s | 92.12% |
| heuristic | 972 | 0.002908 s | 0.22% |
| objective calculation | 2,595 | 0.009706 s | 0.73% |

Inclusive rows overlap. The profile confirms six risk samples per evaluated
edge and makes traversal/sampling—not heuristic—the next evidence target.

One correctness hardening was safe now: `_edge_cache` previously keyed only
`(start, end)`, although `_edge_geometry` accepts different sample counts. The
key now includes `minimum_samples`; a focused test proves three- and five-point
requests remain separate. No unbounded risk/traversal cache, shared search or
incremental algorithm was introduced.

Runtime JSON:
`/root/my_project/.runtime/test-logs/c-component-profile-20260822.json`.

## P4 D Professional Navigation Foundation（2026-08-22 00:34）

The Viewer now has an independently switchable `Navigation aids` layer:

- latitude/longitude graticules and labels reuse canonical `project(lon, lat)`;
- scale distance uses haversine distance across the map at centre latitude;
- north arrow denotes grid north for the north-up EPSG:4326 map;
- non-finite/degenerate bounds fail closed by drawing no navigation aids;
- `object-fit: contain` preserves the 1024×1024 canonical map aspect ratio;
- Presentation Mode now actually hides engineering gate badges.

The layer consumes only `bundle.basemap` metadata. It does not fetch A/B/C data
or compute risk, route, ETA, heading or vessel position.

### Firefox evidence

Firefox 1539 via Playwright CLI opened the existing 48h artifact on
`127.0.0.1:8142`.

| Check | Result |
|---|---|
| page / basemap / risk / hard / route / vessel | PASS |
| Navigation aids visible and default enabled | PASS |
| independent navigation toggle | PASS |
| canonical projection metadata | EPSG:4326, exact bundle bbox |
| 10:00 vessel latitude | 70.333333 |
| 10:30 vessel latitude | 70.413543; moved continuously |
| 13:30 route state | active R1, pending R2 |
| 15:00 route state | active R2, pending R3, correct same-tick ordering |
| console errors / warnings | 0 / 0 |
| required static requests | all HTTP 200 |

Proofs remain runtime-only:

- `/root/my_project/.runtime/viewer-proof/research-navigation/navigation-aids-aspect-corrected.png`
- `/root/my_project/.runtime/viewer-proof/research-navigation/navigation-aids-15h-adopted.png`

## Regression and resource evidence（2026-08-22 00:34）

| Repository | Validation | Result | Wall / max RSS where measured |
|---|---|---|---|
| contracts | full pytest + Ruff | 19 PASS; Ruff clean | 0.53 s / 38,732 KiB pytest |
| B | non-integration pytest + Ruff + syntax | 60 PASS, 8 deselected; clean | 6.62 s / 338,252 KiB pytest |
| C | non-integration pytest + Ruff + syntax | 145 PASS; clean | 2.87 s / 101,748 KiB pytest |
| D | full pytest + Ruff + Node syntax | 63 PASS; clean | 1.41 s / 70,568 KiB pytest |
| Orchestrator | fast non-integration pytest + Ruff | 80 PASS, 2 deselected; clean | 3.03 s / 125,976 KiB pytest |
| Browser | real Firefox static-artifact regression | BROWSER_E2E_PASS | engineering observation only |

Memory remained safe: before bounded suites, available RAM was approximately
5.5–6.0 GiB of 7.4 GiB with 4.0 GiB swap. No two heavy jobs ran concurrently.

The Viewer bundle remained exactly 6,167,478 bytes because no export contract
changed. `app.js` is 49,362 bytes, `style.css` 7,769 bytes and `index.html`
6,165 bytes. Navigation redraw adds only a small fixed set of graticule strokes
and labels; Firefox interaction remained responsive. This is an engineering
observation, not a professional browser benchmark.

## Validation discrepancy and unexpected findings（2026-08-22 00:34）

1. Running B without marker filtering entered existing integration tests and
   failed the Murmansk default-grid allowed-region assertion: the 11×26
   default grid contains no node in the narrow destination region. The new
   experiment did not change that default. Fixing corridor/grid semantics needs
   B/C/contracts owner review and was intentionally not attempted.
2. Browser inspection exposed pre-existing CSS stretching of the square canvas
   into a non-square map area. This would make a scale bar and all geography
   visually misleading; aspect preservation was fixed in D and revalidated.
3. C profiling review exposed the missing sample-count dimension in the
   geometry cache key. It was fixed with no A* redesign.
4. Winter configuration is technically valid, but data availability remains
   unproven. Configuration must not be presented as a winter artifact.

## Local commits and changed repositories（2026-08-22 00:34）

| Repository | Commit | Purpose |
|---|---|---|
| contracts | `c19e910fa408bd4bd30bc83f621f82ebc41910ff` | winter scenario skeleton |
| A | `cd60e9172f0530b9424117661ff234df2edf66bf` | record dataset blocker only |
| B | `1f6eeb90c80762e53aeb2037040386f8fc1004a1` | fixed-grid experiment harness/report |
| C | `c6914948d747baef8bc819c3261774b1777f25db` | component profiler/cache hardening/report |
| D | `ec95f8ccb28e968c4dd19c785966153bf6834425` | professional navigation aids/tests/docs |
| Orchestrator | unchanged | no export or runtime change required |

Governance contains the registry, ownership/status/roadmap updates and this
report. No remote operation was performed.

## Current qualification and next sequence（2026-08-22 00:34）

| State | Items |
|---|---|
| IMPLEMENTED + VALIDATED | contract registry baseline, winter config, C cache identity, D navigation aids |
| EXPERIMENTAL + UNIT_VALIDATED | B grid kernel harness, C component profiler |
| BLOCKED_BY_DATASET | winter source set and A winter artifact |
| PLANNED | formal grid comparison, bounded traversal cache study, adaptive-grid proposal, real candidate/environment presentation |

Recommended next order:

1. contracts/A owners perform winter source metadata availability probes;
2. B owner runs one isolated formal fixed-grid fixture after A evidence exists;
3. C owner profiles one bounded formal fixture and estimates bounded-cache hit
   rate/RSS before implementation;
4. C/Orchestrator/D owners draft route-candidate presentation proposal using
   real C artifacts;
5. integration owner runs one serialized phase-exit replay only after a
   producer-consumer boundary changes.

Current verdict: **RESEARCH_VALIDATION_ACCELERATION = PASS**, with winter data
correctly blocked and algorithmic optimizations still experimental/planned.
