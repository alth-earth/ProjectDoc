---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
Document Role: CANONICAL
Scope: parallel development ownership and repository write boundaries
Canonical For: who may modify each research stream and integration sequence
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Research Validation Development Ownership

## Ownership matrix（2026-08-22 00:02）

| Role | Primary directories | Owns | Must not change |
|---|---|---|---|
| Contracts owner | `arctic_route_contracts/configs`, contract models/schemas/tests | shared identities and approved version proposals | A/B/C/D business implementation |
| A owner | `work_package_a/src`, A configs/tests/docs | acquisition, provenance, normalization, A publication | risk, route, Viewer semantics |
| B owner | `work_package_b/src`, B configs/tests/docs | risk model, fixed-grid experiments, RiskFrame production | A private data, C route/ETA, D rendering |
| C owner | `work_package_c/src`, C configs/tests/docs | planning, final speed/ETA, route/replan, profiling | B risk formula, A acquisition, D UI |
| D owner | `work_package_d/viewer`, D tests/docs | visualization and validation runtime | A/B/C private reads or business recomputation |
| Orchestrator owner | `arctic_route_orchestrator/replay`, `scripts`, tests | pipeline, replay, adapter/export | second Viewer runtime or invented B/C semantics |
| Governance/integration owner | `arctic_route_governance/current`, reports, integration fixtures | proposals, evidence levels, merge order, phase gates | unilateral semantic ownership |

## Parallel work rules（2026-08-22 00:02）

- One writer per file and one semantic owner per contract.
- B, C and D experiments use disjoint repositories and versioned fixtures.
- Cross-package changes start with an approved proposal; direct consumer-driven
  edits to another producer are prohibited.
- No two heavy replay/integration workers run concurrently. Unit/lint jobs may
  run independently when memory remains within the recorded budget.
- Experimental output uses a new identity/path and never overwrites frozen RC1,
  RC2, Summer or 48h artifacts.

## Integration order（2026-08-22 00:02）

```text
proposal + fixtures
  -> producer implementation/tests
  -> consumer opt-in/tests
  -> focused integration
  -> semantic digest and resource review
  -> one serialized phase-exit replay
```

An `Experimental` implementation is not promoted to `Validated` until the
declared producer-consumer and artifact gates pass.

## Round3 handoff lanes（2026-08-22 02:34 +08:00）

| Owner | Ready input | Authorized next work | Blocking gate |
|---|---|---|---|
| A | nine complete winter source rows | resolve only three GFS rows and cadence policy | no winter bundle until 12/12 exact coverage |
| B | unchanged medium summer RiskFrame fixture | consume a future immutable winter bundle only after A gate | no direct A cache/raw reads |
| C | exact sample profile and default-off 50k LRU | formal ingress + 3 objectives + 4 layers equality tests | no production enablement yet |
| D | no new winter presentation artifact | remain on existing bundle | no source data bypass or fabricated layer |
| Governance | runtime logs and reports | approve A cadence decision and C promotion gate | evidence labels remain EXPERIMENTAL/PARTIAL |

A acquisition and C cache work are disjoint. They may be developed by separate
owners, but heavy acquisition, benchmark and replay jobs remain serialized on
the current 7 GiB WSL host.
