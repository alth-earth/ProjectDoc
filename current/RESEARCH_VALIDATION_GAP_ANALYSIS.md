---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
  - PLANNED
Document Role: CANONICAL
Scope: verified capability and gap baseline for research validation
Canonical For: what exists, what is missing, and what may be developed next
Branch: research-validation-system
Last Verified: 2026-08-22
Related Canonical Docs: CURRENT_STATUS.md, CURRENT_ROADMAP.md
---

# Research Validation Gap Analysis

## 判定方法（2026-08-21 23:18）

`Implemented` means code/schema exists; `Validated` requires tests or real artifact evidence;
`Frozen` refers only to a named baseline; `Planned` and `Not implemented` are never promoted by
design intent alone. Code/schema/config/producer-consumer tests outrank docs, and current docs outrank
historical reports.

## 模块总表（2026-08-21 23:18）

| 模块 | 已有能力 | 已验证证据 | 缺口 | 建议 |
|---|---|---|---|---|
| Contracts | identity loaders plus ownership/change gate; 8 scenario configs | 19 tests; winter config loader/CLI | future proposal owner approvals | apply registry/template per change |
| A | 12-type acquisition/normalization/QC/provenance, PreparedWindow, DatasetBundle.v2, exact resolver, ice data interfaces | RC1/RC2 summer frozen bundles; local winter matrix audited | no real winter dataset/artifact; all 12 February rows absent | metadata-only remote availability probe, then provenance-complete bundle |
| B | hourly deterministic risk plus synthetic and formal fixed-grid experiment harnesses | 78 formal frames on 16×7/31×11/60×21 | `demo_unvalidated`; incremental RSS/variance not isolated; no adaptive grid | repeat bounded formal comparison before proposal |
| C | time-dependent A*, 12-route publication, profiler, BC benchmark, edge-cache counters | baseline 10.51 s; medium 75.00 s on real B frames | no bounded risk memoization/shared/incremental search; fine not run | measure repeated exact sample keys first |
| Orchestrator | causal replay, navigation execution, process-level objective parallelism, preflight, presentation export | 12h authoritative/inherited; 48h real artifact | presentation candidate package empty | versioned projection from real C artifact only |
| D | 48h Viewer plus graticule/labels/scale/grid north and aspect-preserving map | fresh Firefox BROWSER_E2E_PASS | no real candidate compare; limited provenance/uncertainty views | consume proposed artifact; expose published quality |

## A 与 Winter Scenario（2026-08-21 23:18）

A can technically acquire and represent sea-ice concentration, drift, thickness, type and edge,
with explicit UTC windows and causal visibility. Existing formal evidence is July/August; the old
9-type long window is legacy evidence and cannot satisfy the current 12-type chain. Therefore:

- winter data interface: `IMPLEMENTED`;
- winter scenario config identity: `IMPLEMENTED / UNIT_VALIDATED`;
- winter frozen DatasetBundle: `NOT_IMPLEMENTED / BLOCKED_BY_DATASET` (zero local February records for all 12 types);
- winter A→B→C→D validation: `NOT_RUN`.

## B Grid and scientific gap（2026-08-21 23:18）

Grid generation belongs to B. `TargetGridConfig.realize()` uses fixed maximum angular steps and
endpoint-covering linspace. The explicit RC2 Tromsø policy yields 31×11; code default tests yield
16×7. C constructs a matching `RegularGrid`; D renders exact cells. The Viewer is not the root cause
of coarse cells.

The summer 12h audit found all 255 navigable water cells at Level 1, plus 65 LAND and 21
DATA_UNAVAILABLE hard cells. That is the artifact's actual model/scenario distribution, not a D
threshold bug. Finer cells may improve spatial representation but do not create scientific risk
variation or calibration.

The first synthetic spatial-kernel experiment now covers 112/341/1260 cells
without changing the production default. It demonstrates deterministic output
and linear output-byte growth, but fixed xarray overhead dominates its ~24.6 ms
runtime. It is not evidence of full RiskFrame build performance.

Remaining P2 formal experiment matrix:

| Measure | Why |
|---|---|
| B wall time and peak RSS by grid/horizon | isolate cost from end-to-end replay |
| risk/hard/unknown distribution | prevent availability regression |
| spatial aliasing and coastline agreement | quantify resolution benefit |
| C route/ETA/risk/integrity | measure downstream semantic effect |
| config/grid/content digests | prevent cross-grid cache pollution |

## C 12-route and performance gap（2026-08-21 23:18）

C's v3 set is real: four fixed layers × three objectives, exactly 12 routes, atomic publication.
However each objective invokes an independent A*. Existing optimizations cache geometry and
precompute risk arrays; Orchestrator can run objective searches in a controlled ProcessPool. There is
no shared objective queue, Pareto frontier, retained search tree, D* Lite or LPA*.

The synthetic component profile attributes ~92% inclusive time to risk sampling
inside edge traversal and confirms six samples per evaluated edge. The existing
geometry cache key now includes `minimum_samples`, closing one correctness gap.
P3 should next share only objective-independent immutable traversal under a complete key. Search
labels cannot be reused across objective weights, layers, heading/time state, risk revision or
generation without new correctness proof. Acceptance requires all 12 route business digests equal to
the serial baseline and measured wall-time/RSS improvement.

## C→D route candidate gap（2026-08-21 23:18）

The static RC1 path proves D can consume a complete v3 set. The current replay product path does not:

```text
C FourLayerRoutePlanSet.v3 (12 real routes)
  -> Orchestrator replay accepts one authoritative navigation route
  -> replay_viewer_export publishes route_candidates NOT_PUBLISHED
  -> D truthfully shows the authoritative/evolving route only
```

The 19 revisions in a 48h bundle are decisions over time, not objective candidates. Required proposal
fields include decision time, layer, objective, route/layer-set IDs, geometry, distance, ETA, cost,
risk/confidence metrics, risk source IDs, generation/revision and selected/authoritative state.

## Environment layer readiness（2026-08-21 23:18）

B uses multiple A variables internally, but the current replay Viewer bundle publishes total risk,
hard availability, basemap, route/navigation and summaries—not full sea-ice/wind/wave/current fields
or trustworthy contributor decomposition for every cell. D must not read A private artifacts or
reconstruct B. Environment layers remain `PLANNED` until Orchestrator has a reviewed presentation
contract and presentation-ready data.

## Interface freeze proposal（2026-08-21 23:18）

| Contract | Owner | Current version | Freeze decision | Proposed work |
|---|---|---|---|---|
| scenario/corridor/vessel/RunContext | contracts | current package schemas | FROZEN_COMPATIBLE | new winter identity only |
| A→B environment bundle | A | `a.dataset-bundle.v2` + PreparedWindow | FROZEN_COMPATIBLE | no breaking change |
| B→C risk frame | B producer / C schema consumer | `bc.risk-frame.v2` | FROZEN_COMPATIBLE | adaptive grid proposal separate/versioned |
| C route plan | C | `RoutePlan.v2`, `FourLayerRoutePlanSet.v3` | FROZEN_COMPATIBLE | performance internal if digests equal |
| C→D candidate presentation | Orchestrator projection; C semantics; D consumer | v1 empty status | GAP / backward compatible | versioned candidate sets |
| Viewer bundle | Orchestrator producer / D owner | `replay.viewer-bundle.v1` | FROZEN_COMPATIBLE | optional versioned fields, fail closed |

No contract was changed in this kickoff. Proposals require owner approval, schemas, fixtures,
producer/consumer tests, migration and rollback before implementation.

## 多人协作建议（2026-08-21 23:18）

- B owner: winter baseline consumption and fixed-grid benchmark; no C/D edits.
- C owner: profile/traversal-cache experiment behind unchanged output contract; no B model edits.
- D owner: professional/research UI against frozen or proposed presentation fixtures; no A/B/C reads.
- Orchestrator owner: candidate/environment projection and compatibility tests only.
- Integration owner: approves schema proposal, pins artifact identities, runs one heavy workload at a
  time and compares semantic digests.

Directory-level write ownership and integration order are now canonical in
[`DEVELOPMENT_OWNERSHIP.md`](DEVELOPMENT_OWNERSHIP.md); contract ownership is
canonical in
[`CONTRACT_OWNERSHIP_REGISTRY.md`](reference/CONTRACT_OWNERSHIP_REGISTRY.md).
