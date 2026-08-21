---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
  - BLOCKED
Document Role: SUPPORTING
Scope: February 2026 winter source acquisition and A coverage evidence
Canonical/Supporting: Supporting evidence; current/reference/WINTER_SCENARIO_STATUS.md is canonical
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Winter Data Acquisition Report

## Verdict（2026-08-22 02:34 +08:00）

Status: `PARTIAL / 9_OF_12_COVERAGE_COMPLETE / BLOCKED_BY_GFS`.

Eight real Copernicus data types were downloaded for
`tromso_isfjorden_february_2026_research_v1`, atomically archived by A, and
validated for the complete 2026-02-15 00:00Z → 2026-02-21 00:00Z interval.
The existing same-corridor GEBCO land/sea mask passes A's explicit
retrospective-best-estimate coverage check at an August knowledge cutoff.
Wind, temperature and visibility remain incomplete. No 12-type
`DatasetBundle.v2`, winter RiskFrame or route was persisted or fabricated.

## Environment and source probes（2026-08-22 02:34 +08:00）

| Check | Result |
|---|---|
| HTTP/HTTPS proxy | configured at loopback; unchanged |
| Git proxy | none configured |
| Copernicus credentials | repo-local file exists, mode 600; values not logged |
| Copernicus metadata | four configured datasets describe successfully |
| NCEI object listing | `202602/` returns `KeyCount=0` |
| NCEI THREDDS root | jumps from `202311` to `202606`; no `202602` catalog |
| One-command direct retry | exact 2026-02-15 inventory also HTTP 404 |
| Windows host physical free space | `UNKNOWN` |

No system or global proxy setting was modified. The direct test unset proxy
variables for that command only. Metadata evidence and logs are under
`/root/my_project/.runtime/winter-acquisition-round3/`.

Copernicus catalogue coordinates independently cover February 2026:

| Dataset | Catalogue start | Cadence |
|---|---|---:|
| Arctic PHY detided | 2021-07-05 | 1 h |
| Arctic total current | 2018-01-01 | 15 min |
| Arctic neXtSIM | 2019-08-01 | 1 h |
| Global wave | 2022-11-01 03:00Z | 3 h |

## Acquired records（2026-08-22 02:34 +08:00）

| Data type | Records | Coverage | Snapshot | Result |
|---|---:|---|---|---|
| wave | 49 | 3 h, exact endpoints | `cmems-459a340e0e75cd0d` | COMPLETE |
| ocean_current | 145 | 1 h, exact endpoints | `cmems-ce247b7441ca5f8b` | COMPLETE, detided fallback |
| water_level | 145 | 1 h, exact endpoints | `cmems-71359619c107b098` | COMPLETE |
| sea_ice_concentration | 145 | 1 h, exact endpoints | `cmems-7514d08d07964d26` | COMPLETE |
| sea_ice_drift | 145 | 1 h, exact endpoints | `cmems-3bd14ca9a132e54b` | COMPLETE |
| sea_ice_thickness | 145 | 1 h, exact endpoints | `cmems-0d9fa0112a011d6f` | COMPLETE |
| sea_ice_type | 145 | 1 h, exact endpoints | `cmems-9926cc6a737bd722` | COMPLETE |
| sea_ice_edge | 145 | 1 h, exact endpoints | `cmems-0ed78031f444a19f` | COMPLETE |
| land_sea_mask | 1 static | retrospective resolver accepted | `gebco-2026-d5a7e2fe3915-7baad866` | COMPLETE, reused cache |
| wind_field | 0 winter | none | none | BLOCKED |
| temperature | 0 winter | none | none | BLOCKED |
| visibility | 0 winter | none | none | BLOCKED |

The preferred total-with-tide current product returned `NoServiceAvailable` for
the request. A followed its existing explicit fallback policy and acquired the
detided Arctic PHY dataset. It did not add total and detided currents. The
fallback is retained in each manifest record and must remain visible in future
research interpretation.

## A validation（2026-08-22 02:34 +08:00）

`arctic-data doctor --data-root data` checked 5,232 archive items with zero
errors and zero warnings. A separate 12-type replay diagnostic used:

```text
mode = retrospective_best_estimate
simulation_time = 2026-02-15T00:00:00Z
knowledge_as_of = 2026-08-21T19:00:00Z
horizon = minimum horizon = 144 h
```

It reported all eight new Copernicus rows and the cached static mask as
`complete=true`, with complete provenance and no missing interval. The three
GFS rows had `has_start_support=false` and `covers_requested_window=false`.
`all_required_complete=false`; diagnostic `--allow-incomplete` returned no
persisted bundle (`bundle_output=null`, `bundle_persisted=false`). Summer GFS
records selected as the nearest available evidence did not pass coverage and
were not accepted as winter data.

## GFS blocking conditions（2026-08-22 02:34 +08:00）

Two independent blockers exist:

1. The official NCEI machine-readable object and THREDDS paths currently expose
   no February 2026 Grid 4 analysis objects. The exact inventory returns 404
   through both configured proxy and one-command direct access.
2. A's retrospective adapter intentionally emits 6-hour f000 analyses, while
   current dynamic coverage policy reports a 3-hour expected interval. Even if
   the remote archive reappears, 25 six-hour records cannot silently satisfy a
   3-hour gate. The A owner must approve a source/cadence resolution; this round
   did not weaken coverage or synthesize intermediate fields.

Potential resolution paths must remain proposals until verified: source
restoration, an A-supported official 3-hour retrospective product, or an
explicit versioned 6-hour research policy. Copying summer records or interpolating
missing meteorology is prohibited.

## Resource and recovery evidence（2026-08-22 02:34 +08:00）

| Task | Wall time | Max RSS | Swap |
|---|---:|---:|---:|
| wave | 31.51 s | 859,960 KiB | 0 |
| ocean current | 94.26 s | 925,768 KiB | 0 |
| water level | 46.41 s | 616,880 KiB | 0 |
| ice concentration | 39.02 s | 606,920 KiB | 0 |
| ice drift | 66.84 s | 871,276 KiB | 0 |
| ice thickness | 42.86 s | 581,908 KiB | 0 |
| ice type + edge | 149.00 s | 3,699,708 KiB | 0 |
| A doctor | 22.56 s | 237,240 KiB | 0 |

The acquisition added approximately 2.546 GiB across immutable Copernicus
source snapshots and normalized raw records. Each completed type is a separate
atomic recovery checkpoint; future work must reuse these snapshot IDs and must
not redownload or delete them. neXtSIM type/edge shared one network load but
published separate derived snapshots. No `.part` file is an accepted artifact.

WSL logical capacity was sufficient, but Windows host physical free space was
not verified and remains `UNKNOWN`.

## Controlled next action（2026-08-22 02:34 +08:00）

1. A owner resolves the official GFS source availability and 6 h versus 3 h
   cadence policy without changing frozen summer evidence.
2. Acquire only the three missing meteorological rows; reuse all nine complete
   rows.
3. Re-run doctor and 12-type exact coverage without `--allow-incomplete`.
4. Persist a new experimental winter DatasetBundle only when all 12 rows pass.
5. Only then allow B, C and D winter artifacts.
