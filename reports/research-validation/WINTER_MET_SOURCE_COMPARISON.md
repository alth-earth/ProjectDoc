---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - BLOCKED
Document Role: SUPPORTING
Scope: official winter meteorological source comparison
Canonical/Supporting: Supporting source decision evidence
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Winter Meteorological Source Comparison

## Candidate Matrix（2026-08-22 12:58 +08:00）

| Source | Wind | Temperature | Visibility | Cadence | Spatial | Provenance / access | Recommendation |
|---|---|---|---|---|---|---|---|
| NOAA NCEI GFS Grid 4 direct | YES in product | YES | YES | 6 h `f000` analysis in current A adapter | 0.5° global | NOAA NCEI; direct archive + THREDDS; exact February paths 404 | Keep as first recovery path if direct objects return; do not redownload existing nine rows. |
| NOAA NCEI GFS HAS order | EXPECTED | EXPECTED | EXPECTED, must inspect inventory | 6 h analyses | 0.5° global | DSI 6182, official offline order; operator email/order required | Viable recovery investigation, but not unattended or adapter-ready. |
| NOAA NCEI GDAS | YES | YES | UNPROVEN | 6 h cycles; some products expose +03 support | 0.25°/0.5°/1° global | Official NCEI HTTPS/HAS; exact target product not validated | Do not adopt until exact GRIB inventory and provenance path are proven. |
| NOAA NCEI CFSv2 CDAS | YES | YES | UNPROVEN | 6 h | roughly 0.5° products | Official NCEI; catalogue freshness inconsistent | Reject as primary; lower fit and no visibility proof. |
| C3S CARRA single levels | YES | YES | YES | 3 h analysis | 2.5 km East Arctic domain | ECMWF/C3S, DOI `10.24381/cds.713858f6`, CC-BY-4.0, CDS token + terms | **Recommended, pending proposal approval and vector-rotation adapter.** |
| C3S ERA5 single levels | YES | YES | NOT PROVEN IN CDS SELECTION | 1 h | 0.25° CDS grid | ECMWF/C3S, Copernicus licence, CDS token + terms | Useful fallback for two variables only; not an atomic three-row solution. |
| Copernicus Marine | no accepted atmosphere product | no accepted atmosphere product | no accepted atmosphere product | N/A | N/A | Marine catalogue and separate credentials | Do not cross service boundaries or derive missing atmosphere from ocean products. |

## Selection Criteria（2026-08-22 12:58 +08:00）

An accepted source must satisfy all of the following:

1. official provider and stable dataset identity;
2. target window 2026-02-15 00:00Z through 2026-02-21 00:00Z;
3. full corridor bbox `[10.0, 68.5, 22.0, 79.5]`;
4. real 10 m vector wind, 2 m air temperature, and visibility;
5. explicit valid time, issue/retrieval evidence, units, grid/projection, and licence;
6. resumable source snapshot and immutable A publication;
7. no replacement of unknown/missing values with safe values;
8. no change to B risk formula or C route semantics.

## Recommendation Rationale（2026-08-22 12:58 +08:00）

CARRA is the only reviewed official catalogue that simultaneously proves all
three variable names, the target month, a 3-hour analysis product, and an Arctic
domain matching Tromsø–Isfjorden. Its higher resolution is not a reason to
change B's target grid; A must preserve the source grid and B remains the owner
of presentation/planning regridding.

The recommendation is conditional. CARRA wind vectors are grid-relative, so a
new A adapter must implement and test projection-aware vector rotation. CDS
download also requires a personal access token and manual terms acceptance.
Those are acceptance gates, not details to bypass.

## Rejected Shortcuts（2026-08-22 12:58 +08:00）

- reuse summer GFS frames for February;
- repeat or interpolate a six-hour frame to manufacture three-hour source records;
- infer visibility from temperature/humidity in A or D;
- use ERA5 wind/temperature while silently marking visibility safe;
- treat Copernicus Marine username/password as CDS authorization;
- publish CARRA u/v without proving conversion to true-east/true-north.
