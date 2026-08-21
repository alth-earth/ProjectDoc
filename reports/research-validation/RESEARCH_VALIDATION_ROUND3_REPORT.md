---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
  - BLOCKED
Document Role: SUPPORTING
Scope: Research Validation Experiment Phase Round3 delivery evidence
Canonical/Supporting: Supporting round report; current status and roadmap remain canonical
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Research Validation Round3 Report

## Key delta（2026-08-22 02:34 +08:00）

| Claim | Before | After | Evidence | Verdict |
|---|---|---|---|---|
| Winter source rows | 0/12 local February rows | 9/12 coverage-complete | A replay coverage + source snapshots | PARTIAL |
| Winter Copernicus | metadata feasibility only | 8 types, 1,064 records | immutable A archive | VALIDATED_SOURCE_DATA |
| Winter bundle | NOT_IMPLEMENTED | still not persisted | `all_required_complete=false` | BLOCKED_BY_GFS |
| C exact sample reuse | unknown | 34.444% exact repeats | shadow run | EXPERIMENTAL_PASS |
| C bounded LRU | PLANNED | default-off 50k implementation | unit + real B-frame matrix | EXPERIMENTAL_VALIDATED |
| Medium C runtime | 75 s single baseline observation | 76.281 s off / 65.012 s LRU medians | 3 independent runs per mode | 14.77% improvement |
| Contracts / semantics | frozen | unchanged | diff and tests | PRESERVED |

## Winter acquisition result（2026-08-22 02:34 +08:00）

The scenario identity and 144-hour window were loaded from shared contracts.
Configured proxy and project-local Copernicus credentials were used without
changing global settings or logging secret values. Metadata probes established
February coverage for every configured Copernicus dataset.

Eight types were acquired in serialized, per-type checkpoints: wave (49) and
seven hourly rows (145 each), totaling 1,064 winter records. The existing
same-corridor GEBCO mask passed explicit retrospective coverage, bringing the A
coverage count to 9/12. A doctor checked 5,232 archive items with no error or
warning. Acquisition added approximately 2.546 GiB; Windows host physical free
space remains unknown.

The result remains `PARTIAL`. NCEI's object listing reports `KeyCount=0` for
202602, THREDDS exposes no 202602 catalog, and the exact inventory returned 404
through both proxy and one-command direct access. The current NCEI adapter also
produces 6-hour f000 analyses while A's dynamic coverage policy expects 3-hour
intervals. No policy was weakened and no summer row was accepted as winter.

Detailed evidence: [WINTER_DATA_ACQUISITION_REPORT.md](WINTER_DATA_ACQUISITION_REPORT.md).

## C cache experiment（2026-08-22 02:34 +08:00）

An experimental sampler adapter supplies three explicit modes:

- `off`: canonical sampling plus a request counter;
- `shadow`: exact-key reuse measurement, always delegates;
- `bounded_lru`: exact successful-value cache with a mandatory positive cap.

The key is scoped to one risk-window fingerprint and includes risk layer, exact
UTC requested time and IEEE-754 coordinate bits. There is no rounding, time
bucket, global cache, persistence or cross-window reuse. Production ingress
does not instantiate this adapter.

On the fixed 31×11, 78-frame medium input, shadow mode found 242,992 repeated
requests among 705,469. The 50k LRU served 232,261 hits per run. Off/LRU complete
route semantic digests matched across all six measurements, as did 15,349
expansions, 20,839 generated states, route metrics, ETAs, costs and source IDs.

| Mode | Runs | Median | Range | Median sampled RSS |
|---|---:|---:|---:|---:|
| off | 3 | 76.281 s | 75.671–76.884 s | 122,416 KiB |
| bounded LRU | 3 | 65.012 s | 64.833–65.242 s | 161,988 KiB |

This proves a low-risk optimization direction, not production readiness.
Committed-window ingress, all three objectives, four layers, replan windows and
hard/unavailable fixtures remain promotion gates.

Detailed evidence:
[C_RISK_SAMPLE_CACHE_EXPERIMENT.md](../../../work_package_c/C_RISK_SAMPLE_CACHE_EXPERIMENT.md).

## B-C joint conclusion（2026-08-22 02:34 +08:00）

No B code, grid or RiskFrame semantics changed. The existing real medium B
experiment document was frozen by SHA-256 and consumed by real C search. The
result establishes that C-side exact memoization can recover about 14.77% median
latency at 341 nodes for a bounded recommended route, at about 38.6 MiB sampled
RSS cost.

The next joint experiment should keep B output immutable and let the C owner
run the formal-ingress/12-route equality matrix. Fine-grid search remains out of
scope until an explicit wall-time and memory budget is approved.

## Code and documentation changes（2026-08-22 02:34 +08:00）

Code changes are limited to `work_package_c`:

- experimental exact sampler modes and bounded LRU;
- benchmark CLI cache mode/capacity;
- complete semantic route digest and source fingerprints;
- unit tests for exact keys, eviction, failures and equality.

Documentation changes update A's winter truth, C experiment evidence, canonical
winter/current status, roadmap and ownership lanes. A/B contracts, B code, C
A* search, route/ETA semantics, D, Orchestrator, frozen artifacts and schema
versions were not modified.

## Validation（2026-08-22 02:34 +08:00）

| Validation | Result | Level |
|---|---|---|
| A archive doctor | 5,232 checked; 0 errors/warnings | VALIDATED |
| A 12-type diagnostic | 9 complete; 3 incomplete; no bundle persisted | PARTIAL_FAIL_CLOSED |
| C targeted tests | 7 passed | UNIT_PASS |
| C non-integration suite | 152 passed | UNIT_PASS |
| C Ruff | clean | LINT_PASS |
| Medium shadow | one real B-frame run | EXPERIMENTAL_PASS |
| Medium off/LRU | 3 independent runs each | EXPERIMENTAL_PASS |
| 48h/full integration/twin-run | not run | INHERITED / OUT_OF_SCOPE |

## Next owner actions（2026-08-22 02:34 +08:00）

1. **A owner:** resolve an approved official February meteorological source and
   the 6 h/3 h cadence policy; acquire only three missing types.
2. **A integration owner:** run 12/12 exact coverage without incomplete mode,
   then persist a new winter bundle identity.
3. **C owner:** add committed-window, three-objective, four-layer and replan
   equality fixtures for the default-off LRU.
4. **B owner:** consume winter only after A passes; keep current formula, level
   and hard-reason semantics frozen.
5. **D owner:** wait for real downstream winter/presentation artifacts; do not
   read A private data or fabricate layers.

Research status remains credible: winter acquisition is materially advanced but
blocked, while the C optimization direction is measured and bounded but not
promoted to production.
