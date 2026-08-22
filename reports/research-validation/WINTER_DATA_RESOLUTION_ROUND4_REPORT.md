---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - BLOCKED
Document Role: SUPPORTING
Scope: Round4 winter meteorological source resolution
Canonical/Supporting: Supporting round report; current status and winter scenario status remain canonical
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Winter Data Resolution Round4 Report

## 1. Executive Summary（2026-08-22 13:03 +08:00）

Round4 moved the winter chain from an undifferentiated `BLOCKED_BY_GFS` state to
`BLOCKED_WITH_DECISION`. C3S CARRA is now the evidence-backed recommended source
for `wind_field`, `temperature`, and `visibility`; it covers the target month and
domain at 3-hour cadence. No data were downloaded because CDS credentials/terms
and an approved projection-aware A adapter are still absent.

| Claim | Before | After | Evidence | Verdict |
|---|---|---|---|---|
| Required winter coverage | 9/12 | 9/12 | A archive + coverage diagnostic | PRESERVED |
| NCEI direct source | 202602 missing | exact paths still 404 | live archive/THREDDS probes | BLOCKED |
| Official alternative | unresolved | CARRA source validated | CDS catalogue/STAC | SOURCE_VALIDATED |
| Cadence blocker | described as 6h vs 3h | record metadata takes precedence; v2 accepts 3h/6h | A code/tests | CORRECTED |
| Winter bundle | not generated | not generated | fail-closed coverage | PRESERVED |
| Data strategy | none | CARRA 3h DRAFT proposal | `A-WINTER-MET-001` | PENDING_APPROVAL |

Claim matrix:

| Capability | Level |
|---|---|
| Official source catalogue validation | VALIDATED |
| CARRA payload download | NOT_RUN |
| CARRA A adapter | NOT_IMPLEMENTED |
| Winter DatasetBundle.v2 | NOT_IMPLEMENTED |
| Winter B/C/D chain | NOT_RUN |

## 2. Scope / Non-Scope（2026-08-22 13:03 +08:00）

Scope: official source inventory, live metadata/URL probes, A cadence/code audit,
candidate comparison, policy proposal, fail-closed A validation, and current-doc
synchronization.

Non-scope: A/B/C/D algorithm changes, contract/schema changes, frozen artifact
mutation, summer substitution, synthetic meteorology, 48-hour replay, heavy
integration, B/C/D winter runs, and remote Git operations.

## 3. Starting Baseline（2026-08-22 13:03 +08:00）

- Branch: `research-validation-system` in all eight repositories.
- Winter scenario: `tromso_isfjorden_february_2026_research_v1`.
- Window: 2026-02-15 00:00Z through 2026-02-21 00:00Z.
- Existing evidence: eight Copernicus types, 1,064 records, plus one GEBCO
  static row; 9/12 required rows complete.
- Missing rows: wind, temperature, visibility.
- No winter DatasetBundle, RiskFrame, route, or Viewer artifact.

## 4. Git Final State（2026-08-22 13:03 +08:00）

Final commit hashes are recorded in the delivery summary after local commit.
Only A documentation and governance documentation changed. Contracts,
Orchestrator, B, C, D, frozen branches, and artifacts remained untouched.
`PUSH = NOT PERFORMED`.

## 5. Filesystem and Resource Safety（2026-08-22 13:03 +08:00）

- Active writes were under `/root/my_project/**` only.
- Runtime probes/logs were written under `.runtime/**`; no unique evidence was
  placed in `/tmp`.
- Start memory: 7.4 GiB total, 4.6 GiB available; swap nearly unused.
- WSL logical filesystem: 882 GiB available; Windows host physical free space
  remains `UNKNOWN`.
- No heavy replay or concurrent acquisition was run.
- A slow Copernicus Marine catalogue filter was terminated after it failed to
  return promptly; it downloaded no data and left only empty runtime output.

## 6. Source Investigation（2026-08-22 13:03 +08:00）

The NCEI product catalogue still advertises GFS analysis and archive ordering,
but both exact executable URLs used by A return HTTP 404 for 2026-02-15. The
current THREDDS root omits December 2023 through May 2026. HAS/tape order is a
real official recovery candidate but requires an operator order and a new
checkpointed ingest path.

CARRA's official machine-readable catalogue reports coverage through 2026-05-31,
provider ECMWF, CC-BY-4.0, and DOI `10.24381/cds.713858f6`. The product page
lists 3-hourly analyses, 2.5 km East Arctic coverage, 10 m u/v wind, 2 m
temperature, and visibility. It is the only reviewed atomic three-variable
candidate.

ERA5 is a valid wind/temperature source but did not prove visibility in the
reviewed CDS selection. GDAS and CFS remain unaccepted because exact variable
inventory/access was not proven. Copernicus Marine does not provide an accepted
substitute and its credentials are not CDS credentials.

## 7. Download Result（2026-08-22 13:03 +08:00）

```text
DOWNLOAD_STATUS = NOT_STARTED
REASON = APPROVAL_AND_CREDENTIAL_GATE
NEW_SOURCE_RECORDS = 0
EXISTING_RECORDS_MUTATED = 0
```

The environment has no `.cdsapirc`, no CDS personal access token, no recorded
CARRA terms acceptance, and no `cdsapi` client in A's environment. More
importantly, production source policy remains DRAFT. Downloading an isolated
file that cannot enter A's provenance pipeline would not advance the formal
chain and was deliberately avoided.

## 8. Policy Decision（2026-08-22 13:03 +08:00）

Recommended, not approved: CARRA 3-hour analyses for all three missing rows.

- Option A, uniform 3 h: preferred; exact source cadence, one product family.
- Option B, uniform 6 h NCEI: valid contingency if direct/HAS objects become
  available; formal v2 already permits 6 h.
- Option C, per-variable cadence/source: technically supported but not preferred
  because it adds heterogeneous provenance and confidence interpretation.

No global cadence relaxation is proposed. A already uses record-declared
cadence before a metadata-free fallback. B resolves continuous fields between
bracketing times and lowers interpolation confidence; C consumes B output and
must not repair A gaps.

## 9. Source-Normalization Risk（2026-08-22 13:03 +08:00）

CARRA 10 m u/v are grid-relative in a Lambert conformal domain. A requires true
east/true north. The adapter must retain projection metadata and perform a
tested vector rotation before publication. This is the highest technical risk
after credentials; a simple variable rename would violate A's contract.

## 10. Validation Results（2026-08-22 13:03 +08:00）

| Gate | Result |
|---|---|
| A focused source/coverage/bundle tests | 51 PASS; one environment warning about unavailable ecCodes library in `.venv` plugin discovery |
| A relevant-file Ruff | PASS |
| A full `src tests` Ruff | 2 pre-existing E501 findings in `curvilinear.py` and its test; no Round4 code changed |
| A doctor | 5,232 checked; 0 errors; 0 warnings |
| 12-type coverage | PARTIAL 9/12; fail-closed; no bundle persisted |
| B smoke | NOT_RUN: no winter bundle |
| C smoke | NOT_RUN: no winter RiskFrame |
| 48h replay / heavy integration | NOT_RUN by scope |

## 11. Performance and Timing（2026-08-22 13:03 +08:00）

This was source validation, not a benchmark. Focused A tests completed in 3.33 s
wall with 212,988 KiB maximum RSS. A doctor completed in 23.78 s with 241,312
KiB maximum RSS. The 12-type coverage diagnostic completed in 118.75 s with
1,673,920 KiB maximum RSS and zero swap. It was the only larger data-load check
and ran alone. No payload download timing exists because the download was gated
before execution.

## 12. Documentation and Contract Impact（2026-08-22 13:03 +08:00）

Added:

- `WINTER_SOURCE_VALIDATION_REPORT.md`;
- `WINTER_MET_SOURCE_COMPARISON.md`;
- draft `WINTER_DATA_POLICY_PROPOSAL.md`;
- this Round4 report.

Updated current status, roadmap, winter status, technical debt, documentation
index, Round3 correction note, and A README/changelog. No contract file or schema
version changed.

## 13. Unexpected Findings（2026-08-22 13:03 +08:00）

1. The earlier cadence blocker was overstated: six-hour NCEI records are already
   formally supported; zero winter records caused the diagnostic to show the
   3-hour fallback.
2. NOAA's catalogue says archive data are available while current direct
   services omit the target month. The correct distinction is
   `DIRECT_BLOCKED / OFFLINE_ORDER_CANDIDATE`, not “data never existed”.
3. CARRA is a materially better fit than ERA5 for the exact three-row gap, but
   its wind vector orientation makes adapter correctness non-trivial.
4. Copernicus Marine and Copernicus Climate credentials are separate.

## 14. Remaining Blockers and Recovery（2026-08-22 13:03 +08:00）

1. A owner reviews `A-WINTER-MET-001`.
2. Operator creates/provides a CDS personal access token and accepts CARRA terms;
   credentials stay untracked and values are never logged.
3. Implement an additive CARRA adapter only after approval.
4. Run one-frame East-domain smoke with vector-rotation verification.
5. Acquire only three missing rows with checkpoints.
6. Run doctor and exact 12-type coverage without incomplete mode.
7. Persist a winter bundle only if `all_required_complete=true`, then allow B/C
   smoke in sequence.

Alternative recovery: operator places a verified NCEI HAS order and A adds a
checkpointed ingest path using the existing GFS inventory semantics.

## 15. Final Verdict（2026-08-22 13:03 +08:00）

```text
WINTER DATA STATUS = BLOCKED_WITH_DECISION
OFFICIAL SOURCE PATH = IDENTIFIED
REAL WINTER MET DOWNLOAD = NOT_STARTED
FORMAL WINTER DATASET BUNDLE = NOT_GENERATED
SCIENTIFIC PROVENANCE = PRESERVED
PUSH = NOT PERFORMED
```

Round4 succeeded at source-resolution and decision preparation, not at data
completion. `READY` would be false until real CARRA or recovered NCEI records
pass the full A gate.
