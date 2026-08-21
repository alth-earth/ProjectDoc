---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - PLANNED
Document Role: SUPPORTING
Scope: C layered planning, performance, candidate publication, and research gaps
Canonical Current State: NO
Branch: research-validation-system
Last Verified: 2026-08-21
---

# C Research Enhancement Analysis

## 已实现和验证的能力（2026-08-21 23:18）

`FourLayerRoutePlanSet` enforces fixed order for full_voyage,
main_corridor_24_72h, rolling_0_24h and executable_0_6h, with exactly
fastest/low_risk/recommended in each layer and exactly 12 routes. The service plans full voyage first,
uses its recommended route to anchor lower layers, and the latest store atomically validates and
publishes the complete set. Unit/integration tests and RC1 r6/r7 initial/replanned JSON/GeoJSON/D
snapshots verify the implementation. This is engineering validation under `demo_unvalidated`, not
scientific calibration or navigation approval.

## 当前搜索结构和性能（2026-08-21 23:18）

The implementation performs four layers × three independent weighted time-dependent A* searches.
`RiskSampler` already precomputes NumPy arrays/axes/times and uses bisect; A* caches edge geometry,
distance, heading, samples, heuristic distance and calm speed. Historical profiling improved about
52 to 325 expansions/s. RC1 r7 records C initial 484.289s and replan 509.751s; the process was about
98% single-core with roughly 4 GiB peak RSS. Orchestrator later adds objective-level process parallelism
and interval pre-gating, but each objective remains an independent search.

## 尚未实现的能力（2026-08-21 23:18）

| Capability | State | Qualification |
|---|---|---|
| Multi-objective shared search | NOT_IMPLEMENTED | no shared label/open queue or Pareto frontier |
| Incremental replanning search | NOT_IMPLEMENTED | trigger/publication exist; replanning reruns full execute |
| D*/LPA* | NOT_IMPLEMENTED | theoretical/deferred only |
| Candidate comparison in replay Viewer | NOT_IMPLEMENTED | C data exists; presentation package is NOT_PUBLISHED |

Safe reuse candidates include immutable topology/geometry, edge samples and objective-independent
traversal under a complete cache key. Labels/open/closed sets cannot be blindly shared across
objectives, layers, time/heading state, generation or risk revisions.

## P3 研究顺序（2026-08-21 23:18）

1. Profile repeated risk sampling and edge traversal on a fixed artifact.
2. Split edge traversal from objective-specific cost, then test a same-layer immutable traversal cache.
3. Require cache keys to bind risk content digest, grid/model/planner config, start/end, departure time
   bucket, sample configuration and hard policy.
4. Only after semantic equivalence, assess shared multi-objective expansion or Pareto labels.
5. Treat incremental replanning as a separate proposal; do not adopt D*/LPA* by default.

Acceptance must include all 12 business digests equal to serial baseline, atomic publication,
determinism/cancellation/revision fences, measured speedup, and peak RSS below an agreed WSL ceiling.
Historical 4 GiB is evidence, not a permanent budget; a provisional research gate should stay below
4.5 GiB on the current ~7 GiB host.

## C→D boundary recommendation（2026-08-21 23:18）

C v2/v3 artifacts already carry candidates/objectives. Orchestrator should publish a versioned,
backward-compatible candidate presentation package with layer/objective identity, plan/layer-set IDs,
geometry, ETA/distance/cost/risk/confidence, source risk IDs, generation/revision and selected state.
Missing or partial data must remain explicit NOT_PUBLISHED/DATA_UNAVAILABLE. D must not synthesize or
rank alternatives.
