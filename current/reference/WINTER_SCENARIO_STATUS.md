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

## Current verdict（2026-08-22 02:34 +08:00）

| Item | State | Evidence |
|---|---|---|
| A generic winter-capable acquisition interfaces | IMPLEMENTED | GFS/NCEI, Copernicus, GEBCO and deterministic ice derivations already support explicit UTC windows |
| Winter scenario configuration | IMPLEMENTED | `tromso_isfjorden_february_2026_research_v1` uses existing `scenario.v2` without schema changes |
| Scenario validation | VALIDATED | contracts loader/CLI/unit test |
| Winter source dataset | PARTIAL / 9_OF_12_COMPLETE | eight Copernicus rows acquired plus cached GEBCO mask; A coverage diagnostic passed these nine |
| Winter GFS rows | BLOCKED_BY_SOURCE_AND_CADENCE | NCEI 202602 paths absent; adapter 6 h cadence conflicts with current 3 h dynamic coverage gate |
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
| wind, temperature, visibility | GFS/NCEI acquisition and normalization | BLOCKED: no 202602 archive path and unresolved 6 h/3 h cadence gate |
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

## Blockers and acquisition plan（2026-08-22 00:02）

Current blocker: `BLOCKED_BY_GFS`. The Copernicus and static rows must be reused;
only the three meteorological rows remain missing. A diagnostic retrospective
cutoff explicitly accepted the later GEBCO release. No formal bundle may be
published while the GFS rows fail start support and horizon coverage.

Next controlled action:

1. resolve NCEI February availability and the 6 h analysis versus 3 h coverage gate;
2. acquire only wind, temperature and visibility from an approved A source;
3. keep Windows-host free space `UNKNOWN` until host verification;
4. rerun doctor/exact coverage without incomplete mode before starting B;
5. preserve the nine completed rows and never substitute summer data.

## Downstream acceptance（2026-08-22 00:02）

After A passes, B must record winter risk/hard/unknown distributions and model
identity without changing the frozen risk formula. C must pass route integrity,
coverage and determinism gates. D may consume only Orchestrator presentation
artifacts and must label scientific status `demo_unvalidated` until calibration
evidence exists.
