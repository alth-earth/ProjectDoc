---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - BLOCKED
Document Role: SUPPORTING
Scope: Round4 official-source validation for missing winter meteorology
Canonical/Supporting: Supporting evidence; current/reference/WINTER_SCENARIO_STATUS.md is canonical
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Winter Source Validation Report

## Verdict（2026-08-22 12:58 +08:00）

`Winter Data Status = BLOCKED_WITH_DECISION`.

The existing nine complete winter rows remain intact. The current NOAA NCEI
Grid 4 direct and THREDDS objects for February 2026 are still unavailable at
the exact URLs used by A. A stronger official alternative now has catalogue
evidence: **C3S CARRA single levels** covers the target month and East Arctic
domain, publishes 3-hourly analyses at 2.5 km, and lists all three missing
variables. It is not yet an A source and has not been downloaded or published.

Two gates prevent a truthful `READY` verdict:

1. the environment has no CDS personal access token and has not recorded the
   dataset-terms acceptance required by the CDS API;
2. A has no approved CARRA adapter, including the mandatory conversion from
   CARRA grid-relative wind components to canonical true-east/true-north.

No summer record, stale frame, interpolation, fake value, or relaxed coverage
policy was used.

## Source Inventory（2026-08-22 12:58 +08:00）

| Dataset | Provider / endpoint | Current status | Reason |
|---|---|---|---|
| GFS Grid 4 analysis | NOAA NCEI archive: `https://www.ncei.noaa.gov/oa/prod-model/global-forecast-system/access/grid-004-0.5-degree/analysis` | DIRECT_BLOCKED | Exact `20260215` `.inv` is HTTP 404; A uses this path for byte-range selection. |
| GFS Grid 4 analysis | NOAA NCEI THREDDS: `https://www.ncei.noaa.gov/thredds/fileServer/model-gfs-g4-anl-files` | DIRECT_BLOCKED | Exact `.inv` is HTTP 404; root catalogue jumps from `202311` to `202606`. |
| GFS Grid 4 archive order | NOAA NCEI HAS / DSI 6182 | OFFLINE_ORDER_CANDIDATE | Official metadata says 2006-present is orderable, but this requires an external order/email workflow and is not an A checkpointed adapter. |
| GDAS | NOAA NCEI GDAS product and HAS | CANDIDATE_NOT_VALIDATED | Official product is 00/06/12/18Z and has historical access, but exact three-variable content and a machine-consumable February subset were not proven; no A adapter exists. |
| CFSv2 Operational Analysis | NOAA NCEI CFS/CDAS | REJECT_AS_PRIMARY | Six-hourly products exist, but catalogue freshness is inconsistent and visibility was not proven; no A adapter exists. |
| CARRA single levels | C3S/ECMWF CDS, `reanalysis-carra-single-levels` | RECOMMENDED_PENDING_APPROVAL | Official catalogue covers through 2026-05-31, including February; 3-hourly analysis, 2.5 km, wind/temperature/visibility, East domain, CC-BY-4.0. |
| ERA5 single levels | C3S/ECMWF CDS, `reanalysis-era5-single-levels` | PARTIAL_CANDIDATE | Hourly 0.25-degree wind and 2 m temperature are explicit; visibility is not exposed in the reviewed CDS single-level selection, so it is not a complete three-variable source. |
| Copernicus Marine catalogue | Copernicus Marine Data Store | NOT_A_MET_SOURCE | Existing credentials and products supplied ocean/wave/ice rows; no verified standalone atmospheric product for all three missing variables was identified. Marine credentials do not authorize CDS. |

Validation time for live HTTP/catalogue probes: 2026-08-22 12:58 +08:00.

## Current A Source Path（2026-08-22 12:58 +08:00）

A currently owns one retrospective meteorological path:

```text
NCEI GFS Grid 4 f000 analysis
  -> inventory selects UGRD 10 m, VGRD 10 m, TMP 2 m, VIS surface
  -> strict HTTP byte ranges
  -> source snapshot + request metadata
  -> normalized wind_field / temperature / visibility records
```

Code evidence:

- `work_package_a/src/arctic_route_data/forecast_acquisition.py:36-43`
  defines the two NCEI endpoints;
- lines 451-536 define the six-hour `f000` retrospective publication and
  `nominal_interval_hours=6.0`;
- lines 1117-1145 define exact object names and GRIB inventory selectors.

The adapter failure is therefore source-object resolution, not a parsing,
Viewer, B, or C failure.

## Official Catalogue Evidence（2026-08-22 12:58 +08:00）

### NOAA NCEI（2026-08-22 12:58 +08:00）

The [official GFS product page](https://www.ncei.noaa.gov/products/weather-climate-models/global-forecast)
still describes Grid 4 analysis as 2007-present and exposes HTTPS, TDS, and HAS.
The [dataset metadata](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc%3AC00634)
states that data from 2006-present can be ordered from archive storage. This
means “not present on current direct paths” must not be rewritten as “NOAA never
has the data”. The executable A direct path remains blocked, while HAS is an
external-order recovery path requiring operator identity and a new ingest step.

The [GDAS product page](https://www.ncei.noaa.gov/products/weather-climate-models/global-data-assimilation)
confirms four daily cycles and archive/order access. It does not by itself prove
that a February 2026 subset contains A's exact surface visibility field, so GDAS
remains a candidate rather than accepted evidence.

### C3S / ECMWF CARRA（2026-08-22 12:58 +08:00）

The [official CARRA catalogue](https://cds.climate.copernicus.eu/datasets/reanalysis-carra-single-levels)
states:

- East domain includes Svalbard, the Barents Sea, and northern Scandinavia;
- temporal coverage is 1991-present, with 3-hourly analyses;
- horizontal resolution is 2.5 km;
- variables include 10 m u/v wind, 2 m temperature, and visibility.

The machine-readable CDS collection returned:

```text
id = reanalysis-carra-single-levels
temporal end = 2026-05-31T00:00:00Z
provider = ECMWF
license = CC-BY-4.0
DOI = 10.24381/cds.713858f6
```

The requested 2026-02-15 to 2026-02-21 window is therefore inside the current
catalogue extent. Catalogue evidence proves availability metadata, not a
successful payload retrieval.

CARRA u/v are described relative to the local projected grid orientation. A's
public contract requires true-east/true-north wind. Any adapter must retain the
projection/rotation evidence and transform vectors before normalization; direct
renaming is prohibited.

### ERA5 and Copernicus Marine（2026-08-22 12:58 +08:00）

The [ERA5 catalogue](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels)
provides hourly 10 m u/v and 2 m temperature at 0.25-degree CDS resolution, but
the reviewed selection did not expose visibility. ERA5 cannot currently replace
the complete three-variable set.

Copernicus Marine successfully supplied the existing ocean, ice, water-level,
and wave records. Its catalogue and credentials are a separate service from
C3S CDS; no Marine product was accepted as an atmospheric substitute.

## Environment and Reproducible Evidence（2026-08-22 12:58 +08:00）

| Check | Result |
|---|---|
| HTTP/HTTPS proxy | configured; unchanged |
| Git proxy | none configured |
| `/root/.cdsapirc` | absent |
| repo-local CDS token | absent |
| `cdsapi` client | not installed in A environment |
| Copernicus Marine credentials | present, mode 600; values not logged; not valid for CDS |
| CARRA unauthenticated catalogue | PASS |
| CARRA retrieval | NOT_ATTEMPTED: token and terms gate |
| NCEI exact direct object | HTTP 404 on archive and THREDDS |
| Windows host physical free space | UNKNOWN |

Machine-readable probes are retained only as runtime evidence under:

```text
/root/my_project/.runtime/winter-source-validation-round4/
```

No system/global proxy or credential configuration was modified.

## Controlled Resolution Gate（2026-08-22 12:58 +08:00）

Recommended decision: approve a **CARRA 3-hour analysis adapter** for the three
meteorological rows as one atomic source family. This preserves the current
3-hour research target and does not change `scenario.v2`,
`a.dataset-bundle.v2`, risk formula, or hard-reason semantics.

Approval must precede implementation and requires:

1. operator-supplied CDS personal access token and manual dataset-terms acceptance;
2. adapter design for East-domain subset, time selection, issue-time evidence,
   projection/vector rotation, source snapshot, checksum, and restart recovery;
3. one-frame real-source smoke before the six-day acquisition;
4. exact 49-time coverage for each of the three rows at 3-hour cadence;
5. A doctor and 12-type coverage without `--allow-incomplete` before persisting
   a winter bundle.

Until those gates pass, status remains `BLOCKED_WITH_DECISION`, not `READY`.
