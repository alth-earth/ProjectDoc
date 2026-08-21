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

## Current verdict（2026-08-22 00:02）

| Item | State | Evidence |
|---|---|---|
| A generic winter-capable acquisition interfaces | IMPLEMENTED | GFS/NCEI, Copernicus, GEBCO and deterministic ice derivations already support explicit UTC windows |
| Winter scenario configuration | IMPLEMENTED | `tromso_isfjorden_february_2026_research_v1` uses existing `scenario.v2` without schema changes |
| Scenario validation | VALIDATED | contracts loader/CLI/unit test |
| Winter 12-type source dataset | BLOCKED_BY_DATASET | no matching local artifact found; no network acquisition run in this round |
| Winter `PreparedWindow` / `DatasetBundle.v2` | NOT_IMPLEMENTED | depends on complete source acquisition and QC |
| Winter B/C/D artifacts | NOT_IMPLEMENTED | downstream work prohibited until A publication passes |

The configuration is not a winter artifact and is not evidence that the 12
required sources are complete for the selected period.

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
| Artifact state | none |

The February window is a reproducible research target, not a claim about source
availability or winter representativeness. Changing the target period requires
a new scenario revision and a recorded source-availability review.

## Existing acquisition capability（2026-08-22 00:02）

| Data group | Existing path | Winter readiness |
|---|---|---|
| wind, temperature, visibility | GFS/NCEI acquisition and normalization | interface implemented; target-window records unverified |
| wave | Copernicus global wave | interface implemented; target-window records unverified |
| ocean current, water level | Copernicus Arctic physical products | interface implemented; target-window records unverified |
| ice concentration/drift/thickness | Copernicus Arctic physical products | interface implemented; target-window records unverified |
| ice type/edge | neXtSIM concentration components and deterministic derivation | interface implemented; target-window records unverified |
| land/sea mask | GEBCO-derived static mask | existing local/static capability; exact bundle binding still required |

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

Current blocker: `BLOCKED_BY_DATASET`. No complete local February 2026 12-type
bundle was found. This round intentionally did not perform network downloads,
credential use or large acquisition.

Next controlled action:

1. run source metadata/availability probes only;
2. record proxy state and use per-command direct connection only if required;
3. estimate download bytes and Windows-host free space separately—WSL `df` is
   not host-disk evidence;
4. acquire one source group at a time with resumable manifests;
5. run A doctor/exact resolver before starting B;
6. preserve partial downloads as incomplete evidence, never as a formal bundle.

## Downstream acceptance（2026-08-22 00:02）

After A passes, B must record winter risk/hard/unknown distributions and model
identity without changing the frozen risk formula. C must pass route integrity,
coverage and determinism gates. D may consume only Orchestrator presentation
artifacts and must label scientific status `demo_unvalidated` until calibration
evidence exists.

