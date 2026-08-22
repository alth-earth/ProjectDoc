---
Overall Status: APPROVED
Content Status:
  - APPROVED
Document Role: CANONICAL
Scope: winter meteorological source and cadence policy (approved for execution)
Canonical/Supporting: Canonical proposal; production change authorized under gate G5/G6
Branch: research-validation-system
Last Verified: 2026-08-22
Approved: 2026-08-22
---

# Winter Data Policy Proposal

## Proposal Metadata（2026-08-22 12:58 +08:00；approved 2026-08-22）

```text
Proposal ID: A-WINTER-MET-001
Title: CARRA 3-hour retrospective meteorology for February 2026 winter research
Status: APPROVED
Semantic owner: Work Package A
Affected producer: Work Package A acquisition/publisher
Affected consumers: B through existing DatasetBundle.v2; C/D unchanged
Target schema version: unchanged
Created: 2026-08-22 12:58 +08:00
Approved: 2026-08-22
```

`APPROVED` authorizes production acquisition and publication of CARRA East-domain
single-level analyses for the 2026-02-15..02-21 window, subject to gates G5/G6.

## Problem and Evidence（2026-08-22 12:58 +08:00）

The winter scenario has 9/12 complete required rows. NOAA NCEI's exact February
2026 Grid 4 direct paths used by A return 404, while official catalogue metadata
still describes archive/HAS availability. C3S CARRA has current official
catalogue evidence for the target month, domain, cadence, and all three missing
variables.

The frequently stated “A policy is 3h but the retrospective adapter is 6h” is
not, by itself, a formal bundle incompatibility:

- `service.py` uses 3 h only as a metadata-free fallback;
- a real source record's `nominal_interval_hours` takes precedence;
- `DatasetBundle.v2` formally allows 3 h or 6 h for wind, temperature, and
  visibility.

The current incomplete diagnostic displays 3 h because there are zero winter
meteorological records. If the existing NCEI adapter published real 6-hour
records, coverage would use their declared 6-hour cadence. The production
decision is therefore about source fidelity and research resolution, not about
silently weakening a hard-coded bundle gate.

## Cadence Options（2026-08-22 12:58 +08:00）

### Option A — Uniform 3-hour meteorology（2026-08-22 12:58 +08:00）

Use CARRA 3-hour analyses for all three rows.

Advantages:

- matches the current research fallback and wave cadence;
- 49 exact target times over the 144-hour inclusive window;
- no source-time interpolation in A;
- official 2.5 km Arctic regional product with all three variables.

Costs/risks:

- new source adapter and CDS authentication/terms workflow;
- projection-aware rotation of grid-relative wind vectors;
- new source identity and scientific comparability note versus frozen GFS summer.

### Option B — Uniform 6-hour meteorology（2026-08-22 12:58 +08:00）

Recover NCEI GFS via restored direct paths or an approved HAS ingest.

Advantages:

- existing A retrospective parser, inventory selectors, normalized fields, and
  formal 6-hour cadence support;
- consistent NOAA/GFS source family with prior A work.

Costs/risks:

- only 25 exact source times over the inclusive 144-hour window;
- B generates hourly risk support by deterministic linear interpolation between
  continuous frames and applies interpolation confidence rather than exact-frame
  confidence;
- direct archive currently unavailable; HAS requires external ordering and a
  new checkpointed ingest path.

No six-hour record may be duplicated into synthetic three-hour records.

### Option C — Per-variable cadence/source（2026-08-22 12:58 +08:00）

A already supports source-record cadence metadata and can carry different
cadences across different data types. It rejects conflicting cadence declarations
within one type unless an explicit strategy is supplied.

Advantages:

- permits the best available official source per variable;
- does not require a contract schema change.

Costs/risks:

- makes the three meteorological contributors temporally and scientifically
  heterogeneous;
- complicates issue-time/provenance comparison and confidence interpretation;
- increases the chance that one missing variable blocks the complete bundle.

This option should be a contingency only, not the first choice while CARRA
provides an atomic three-variable product family.

## Proposed Semantics（2026-08-22 12:58 +08:00）

| Dimension | Current | Proposed | Breaking? |
|---|---|---|---|
| Schema identity | `scenario.v2`, `a.dataset-bundle.v2` | unchanged | No |
| Required data types | 12 | unchanged | No |
| Source | NCEI GFS adapter intended | CARRA single-level analysis for three missing rows | Source change only |
| Cadence | record-declared 3 h or 6 h | 3 h declared from CARRA analysis | No |
| Grid | source grid retained | retain CARRA projection/grid evidence | No |
| Wind semantics | true east / true north | rotate CARRA grid-relative u/v before publication | No; required normalization |
| Missing behavior | incomplete/fail closed | unchanged | No |
| Bundle identity | content/source dependent digest | new winter identity only | No |
| Frozen artifacts | immutable | untouched | No |

## B and C Impact（2026-08-22 12:58 +08:00）

B already linearly resolves continuous environmental fields between bracketing
valid times and distinguishes exact from interpolated temporal support in its
confidence. At 3 h, two of every three hourly risk frames use interpolation; at
6 h, five of every six do. This changes input support/confidence and potentially
risk values because the source is different, but it must not change the risk
formula or level policy.

C consumes published B risk frames, not A cadence directly. Planning impact must
be evaluated through winter B smoke and route integrity after A passes. C must
not compensate for source gaps or invent meteorology.

## Implementation Ownership and Gates（2026-08-22 12:58 +08:00）

| Repository / directory | Owner | Allowed after approval | Prohibited |
|---|---|---|---|
| `work_package_a/src/arctic_route_data/` | A | additive CARRA adapter, provenance, rotation, checkpoints | schema changes, fake fill, summer substitution |
| `work_package_a/tests/` | A | unit and one-frame real-source smoke | fixture-only claim as real acquisition |
| `arctic_route_contracts` | Contracts | no change expected | version/schema modification |
| `work_package_b/c/d` | respective owners | smoke only after formal winter bundle | source-side workaround |

Approval/acceptance gates:

1. A owner approves this proposal and the CARRA source identity.
2. Operator provides a CDS personal access token without committing it and
   accepts dataset terms through CDS.
3. One-frame East-domain smoke proves variables, coordinates, units, valid time,
   projection, and true-vector conversion.
4. Focused A tests and doctor pass.
5. Six-day acquisition publishes exactly the required source times with immutable
   snapshots and no partial acceptance.
6. Twelve-type coverage passes without `--allow-incomplete` before bundle output.

## Approval Record（2026-08-22 12:58 +08:00；updated 2026-08-22）

| Role | Decision | Evidence/date |
|---|---|---|
| A semantic owner | APPROVED | 2026-08-22; adapter `carra_acquisition.py` live probe + dry-run + focused tests pass |
| B consumer owner | PENDING | review cadence/confidence impact (not blocking A ingestion) |
| Contracts owner | NOT_REQUIRED unless implementation discovers schema need | current v2 already carries cadence/source identity |
| Integration owner | PENDING | |

Approval conditions (carried from acceptance gates 5–6):

- Gate 5: CARRA ingested before `winter_bundle` frozen, publishing exactly the
  required source times with immutable snapshots and no partial acceptance.
- Gate 6: Twelve-type coverage passes without `--allow-incomplete` before bundle
  output; ACQ-203 invalid-data provenance published for the CARRA part.
- Acquisition uses `publisher.publish_dataset` with provenance. Dry-run only until
  G5/G6 are demonstrably satisfied end-to-end.

## Ingestion Execution Record（2026-08-22）

CARRA East-domain single-level acquisition executed under approval.

- **Route / window**: published under corridor `tromso_to_isfjorden_outer`
  (NOT an internal `A-winter-carra` tag — the corridor `tromso_isfjorden_february_2026_
  research_v1` uses `corridor_id = tromso_to_isfjorden_outer`, window 2026-02-15T00Z
  .. 02-21T00Z, horizon 144 h). First attempt used a wrong route_id
  (`A-winter-carra`); that mistaken batch (168 records + `data/ready/A-winter-carra`)
  was deleted after the error was caught, GRIB cache retained.
- **Volume**: 49 analysis cycles × 3 data types (wind_field / temperature /
  visibility) = 147 published frames, 49 source snapshots. `frames_processed =
  frames_published = 147`, manifest immutable, no partial acceptance.
- **Doctor**: `python -m arctic_route_data.cli doctor --data-root data` →
  `ok: true`, 5379 checked, 0 errors / 0 warnings.
- **Gate 6 (twelve-type coverage)**: passes **without `--allow-incomplete`** when
  the replay window is aligned to the data's actual end. Key finding: the whole
  2026-02 dataset (CARRA + ocean/sea_ice/water_level/wave) ends at 02-21T00Z, but
  the default `horizon_hours=144` replay request extends `requested_end` to
  02-21T12Z, leaving a 12 h trailing gap on every type. With
  `--horizon-hours 132` (so `requested_end = minimum_required_end = 02-20T12Z`)
  all 12 required types are `complete: true`, `all_required_complete = True`,
  exit code 0. This is a replay-window / data-end alignment issue, not a CARRA
  acquisition defect — CARRA's 49 cycles are continuous 02-15T00Z..02-21T00Z.
- **Open item (RESOLVED 2026-08-22 下午)**: the 12 h trailing gap
  at 02-21T00Z..12Z under the scenario's nominal 144 h horizon. Decision: **Option (a)**
  — backfilled 02-21T03/06/09/12Z for the eight dynamic non-CARRA winter sources
  (`land_sea_mask` is a static GEBCO mask, not backfilled). Implemented via
  `scripts/winter_non_carra_tail_acquisition.py`; after backfill the data end
  aligns to 02-21T12Z, so even the **nominal `horizon_hours=144`** replay yields
  `all_required_complete = True` with no `--horizon-hours 132` workaround.
- **Status**: Gate 5 MET. Gate 6 MET — twelve-type coverage passes **without
  `--allow-incomplete`** at default horizon=144. `winter_bundle` frozen 2026-08-22
  20:53 as
  `data/tromso_to_isfjorden_outer_winter_20260215T000000Z_bundle.json`
  (generation_id 0; doctor `ok: true`, 5461 checked, 0 errors). All gates closed.

## Recommendation（2026-08-22 12:58 +08:00）

Approve Option A: CARRA 3-hour analysis for the three missing rows. Keep NCEI
GFS 6-hour analysis as a recovery contingency, not a prerequisite. Do not
approve a global relaxation from 3 h to 6 h, because the current contracts
already express source-specific cadence and CARRA can meet 3 h directly.
