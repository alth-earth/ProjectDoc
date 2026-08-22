---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
  - BLOCKED
Document Role: CANONICAL
Scope: winter research scenario configuration, data readiness, and acceptance gates
Canonical For: what winter capability exists and what remains blocked
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Winter Scenario Status

## Round4 source decision（2026-08-22 13:03 +08:00）

| Item | State | Evidence |
|---|---|---|
| Existing winter rows | 9/12 COMPLETE (AM) → 12/12 COMPLETE (PM) | CARRA 3 类补齐 + 方案 (a) 补采非 CARRA 末尾时次 |
| NCEI direct recovery | BLOCKED | archive and THREDDS exact February objects return 404 |
| CARRA catalogue | SOURCE_VALIDATED | 3-hourly analyses, 2.5 km, East Arctic domain, all three variables, target month covered |
| CARRA acquisition | COMPLETE | 147 帧全发布（route_id 已修正为 `tromso_to_isfjorden_outer`），doctor ok |
| Source/cadence proposal | APPROVED | `A-WINTER-MET-001` 已批准 2026-08-22 |
| Winter DatasetBundle | READY_FOR_GENERATION | 12/12 complete；12h 缺口已闭合（方案 a），G6 默认 horizon=144 全 complete |

Canonical verdict is now `BLOCKED_WITH_DECISION`: a credible official source is
identified, but production use is gated by approval, authentication, source
normalization and real-payload validation. The previous `BLOCKED_BY_GFS` label
remains historical context, not the current source strategy.

The previous 6 h/3 h wording is also narrowed: the metadata-free service
fallback is 3 h, while actual NCEI retrospective records declare 6 h and formal
bundle validation allows either cadence. Missing NCEI objects are the current
runtime blocker. The recommended CARRA path meets 3 h without relaxing policy.

## Round5 closure（2026-08-22 下午 +08:00）

| Item | State | Evidence |
|---|---|---|
| CARRA 3 类补齐 | COMPLETE | 147 帧全发布，`tromso_to_isfjorden_outer`，doctor ok（5379 校验 0 error） |
| 非 CARRA 末尾补采（方案 a） | COMPLETE | 8 类动态源补 02-21T03/06/09/12Z，`scripts/winter_non_carra_tail_acquisition.py`，doctor ok（5461 校验 0 error） |
| land_sea_mask | STATIC (unchanged) | GEBCO 派生静态掩膜，与时间无关，无需补时次 |
| 12h 末端缺口 | CLOSED | 数据末端对齐至 02-21T12Z |
| Winter source dataset | **12/12 COMPLETE** | 12 类在 02-15T00Z..02-21T12Z 全部 complete |
| G6（默认 `horizon=144`） | PASS | `all_required_complete=True`，12 类全 complete，无需退用 `--horizon-hours 132` |
| winter_bundle 冻结 | FROZEN | `data/tromso_to_isfjorden_outer_winter_20260215T000000Z_bundle.json`（generation_id 0），replay 不带 `--allow-incomplete` 闸门通过；doctor ok 5461/0 |

Canonical verdict is now `READY_FOR_GENERATION`: all twelve required winter sources
are complete for the 2026-02-15..02-21T12Z window; the previously documented 9/12
partial state and 12h tail gap are both resolved. Downstream B/C/D artifacts may
proceed once a `DatasetBundle` is persisted (per A required outputs).

## Current verdict（2026-08-22 02:34 +08:00）

| Item | State | Evidence |
|---|---|---|
| A generic winter-capable acquisition interfaces | IMPLEMENTED | GFS/NCEI, Copernicus, GEBCO and deterministic ice derivations already support explicit UTC windows |
| Winter scenario configuration | IMPLEMENTED | `tromso_isfjorden_february_2026_research_v1` uses existing `scenario.v2` without schema changes |
| Scenario validation | VALIDATED | contracts loader/CLI/unit test |
| Winter source dataset | **12_OF_12_COMPLETE** | CARRA 3 类补齐 + 方案 (a) 补采 8 类动态非 CARRA 末尾时次；G6 默认 horizon=144 全 complete |
| Winter GFS rows | BLOCKED_BY_SOURCE (historical) | NCEI 202602 direct paths absent; 已被 CARRA（风/温/能见度）与 Copernicus 替代覆盖，6 h 记录不再必需 |
| Winter `PreparedWindow` / `DatasetBundle.v2` | NOT_IMPLEMENTED | depends on complete source acquisition and QC |
| Winter B/C/D artifacts | NOT_IMPLEMENTED | downstream work prohibited until A publication passes |

The configuration is not a winter artifact and is not evidence that the 12
required sources are complete for the selected period.

Feasibility history is in
[WINTER_DATA_FEASIBILITY_REPORT.md](../../reports/research-validation/WINTER_DATA_FEASIBILITY_REPORT.md);
current acquisition evidence is in
[WINTER_DATA_ACQUISITION_REPORT.md](../../reports/research-validation/WINTER_DATA_ACQUISITION_REPORT.md).

## Configuration skeleton（2026-08-22 00:02）

| Field | Value |
|---|---|
| Scenario | `tromso_isfjorden_february_2026_research_v1` |
| Version | `0.1.0` |
| Corridor | `tromso_to_isfjorden_outer` `1.2.0` |
| Mode | `retrospective_best_estimate` |
| Window | 2026-02-15 00:00Z → 2026-02-21 00:00Z |
| Horizon | 144 h |
| Required profile | existing 12 formal data types |
| Optional | bathymetry, long-term restricted area |
| Artifact state | nine source rows complete; DatasetBundle not persisted |

The February window is a reproducible research target, not a claim about source
availability or winter representativeness. Changing the target period requires
a new scenario revision and a recorded source-availability review.

## Existing acquisition capability（2026-08-22 00:02）

| Data group | Existing path | Winter readiness |
|---|---|---|
| wind, temperature, visibility | CARRA single-levels (East Arctic) | COMPLETE (147 帧, 2026-08-22)；CARRA 单层级地表风为真东/真北，无需旋转 |
| wave | Copernicus global wave | 49 records, COMPLETE |
| ocean current, water level | Copernicus Arctic physical products | 145 each, COMPLETE; current is detided fallback |
| ice concentration/drift/thickness | Copernicus Arctic physical products | 145 each, COMPLETE |
| ice type/edge | neXtSIM concentration components and deterministic derivation | 145 each, COMPLETE |
| land/sea mask | GEBCO-derived static mask | cached row COMPLETE under explicit later retrospective cutoff |

A supports `retrospective_best_estimate` and `frozen_forecast`, explicit UTC
windows, source snapshots, issue/valid/ingest provenance and atomic publication.
This makes the configuration technically consumable, but does not remove data,
credentials, coverage or source-version gates.

## Required A outputs（2026-08-22 00:02）

Before B may consume the scenario, A must produce:

1. source snapshot and manifest for all 12 required types;
2. one-valid-time-per-frame normalized records with UTC issue/valid/ingest time;
3. complete coverage and QC with no synthetic zero fill;
4. immutable `PreparedWindow` and persisted `a.dataset-bundle.v2`;
5. matching RunContext and exact-resolver proof;
6. source/grid/provenance digests and recorded missing/unknown counts.

## Blockers and acquisition plan（2026-08-22 00:02, superseded by Round5）

Former blocker: `BLOCKED_WITH_DECISION` — only the three meteorological rows
(CARRA) remained missing. This is now **resolved** (see Round5): CARRA 3 类补齐
+ 方案 (a) 补采 8 类动态非 CARRA 末尾时次，12/12 complete，12h 缺口闭合。

Remaining controlled action before downstream B/C/D:

1. persist the immutable `PreparedWindow` and `a.dataset-bundle.v2` for the
   2026-02-15..02-21T12Z window (A required output #4);
2. run exact coverage / doctor without incomplete mode as the bundle gate;
3. preserve all twelve completed rows and never substitute summer data.

## Downstream acceptance（2026-08-22 00:02）

After A passes, B must record winter risk/hard/unknown distributions and model
identity without changing the frozen risk formula. C must pass route integrity,
coverage and determinism gates. D may consume only Orchestrator presentation
artifacts and must label scientific status `demo_unvalidated` until calibration
evidence exists.
