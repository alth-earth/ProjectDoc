---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
Document Role: CANONICAL
Scope: cross-repository contract ownership, version, compatibility, and change gates
Canonical For: who may change each interface and how consumers must handle it
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Contract Ownership Registry

## Registry rules（2026-08-22 00:02）

This registry records implemented interfaces. A row marked `FROZEN_COMPATIBLE`
does not freeze implementation internals; it freezes the observable meaning of
existing fields and failure behavior. `DRAFT` proposals are not contracts and
must not be consumed by production code.

Every contract has one schema owner, one or more producers, explicit consumers,
machine-readable fixtures, and producer-consumer tests. Published artifacts are
immutable: corrections create a new identity/revision rather than overwriting a
previous publication.

## Ownership registry（2026-08-22 00:02）

| Contract | Schema / semantic owner | Producer | Consumer | Current version | Status | Compatibility boundary |
|---|---|---|---|---|---|---|
| Shared corridor/scenario/vessel identities | `arctic_route_contracts` | contracts loaders/configs | A, B, C, Orchestrator, D metadata | package schemas, scenario.v2 | FROZEN_COMPATIBLE | New scenario IDs/configs allowed; existing identity meaning cannot change |
| Run Context | `arctic_route_contracts` | shared context builder | A, B, C, Orchestrator | RunContext v2 | FROZEN_COMPATIBLE | UTC and scenario/corridor/vessel/generation identity remain exact |
| A→B Prepared Window | A | `work_package_a` | B | `PreparedWindow` public API | FROZEN_COMPATIBLE | B must not inspect A SQLite/raw/private directories |
| A→B Dataset Bundle | A with shared identity validation | `work_package_a` | B, Orchestrator validation | `a.dataset-bundle.v2` | FROZEN_COMPATIBLE | Immutable payload/sidecar identity; missing data stays explicit |
| B input envelope | B | `work_package_b` adapter | B risk service | `BInputEnvelope` | ACTIVE_INTERNAL | May evolve inside B while preserving A public and RiskFrame boundaries |
| B→C Risk Frame | B owns publication and risk semantics; C is required compatibility reviewer | `work_package_b` | C, Orchestrator presentation projection | `bc.risk-frame.v2` | FROZEN_COMPATIBLE | Risk level, hard mask/reason, confidence, speed factor, grid and time semantics unchanged |
| B committed risk window | B | `work_package_b` store | C ingress, replay | current committed-window API | FROZEN_COMPATIBLE | Atomic publication; no stale generation or out-of-window fallback |
| C route plan | C | `work_package_c` | Orchestrator, D static fallback | `cd.route-plan.v2` | FROZEN_COMPATIBLE | C remains owner of route, speed, ETA, objective and costs |
| C layered route plan | C | `work_package_c` | Orchestrator, D static loader | `cd.four-layer-route-plan-set.v3` | FROZEN_COMPATIBLE | Exactly four layers × three objectives; atomic complete-set publication |
| C→D route state presentation | Orchestrator projection; C owns route semantics | Orchestrator | D Viewer | current route state in `replay.viewer-bundle.v1` | FROZEN_COMPATIBLE | authoritative/pending/superseded and adoption ordering cannot be reinterpreted |
| Candidate route presentation | Orchestrator projection; C owns candidate semantics | Orchestrator | D Viewer | `presentation.route-candidates.v1` | IMPLEMENTED_EMPTY | `NOT_PUBLISHED` + empty list is authoritative until real geometry/metrics are exported |
| Risk overlay presentation | Orchestrator projection; B owns risk semantics | Orchestrator | D Viewer | `presentation.risk-overlay.v1` | FROZEN_COMPATIBLE | Current/horizon validity and unavailable fail-closed behavior preserved |
| Viewer bundle | Orchestrator producer; D owns runtime consumption | Orchestrator | D Viewer | `replay.viewer-bundle.v1` | FROZEN_COMPATIBLE | Optional additive packages allowed; required v1 fields and one-clock semantics preserved |

## Immutable artifact requirements（2026-08-22 00:02）

- Identity includes schema version plus the applicable scenario, generation,
  revision, time and content digests.
- A published object is read-only. A correction receives a new revision or
  artifact identity and retains provenance to the superseded object.
- Consumers reject incompatible versions, identity mismatch, partial atomic
  groups, unknown required fields or insufficient temporal coverage.
- Missing/unknown/unavailable never becomes zero, safe, last-known fallback or
  a fabricated route candidate.

## Backward compatibility（2026-08-22 00:02）

Compatible changes are additive optional fields/packages whose absence retains
the previous behavior. Renaming/removing a field, changing units, polarity,
time meaning, objective meaning, failure behavior, cardinality, atomicity or
identity calculation is breaking even if JSON still parses.

A consumer may support old and new versions concurrently, but must surface an
explicit unsupported/unavailable state when it cannot interpret a publication.

## Breaking-change process（2026-08-22 00:02）

1. Create a proposal from
   [CONTRACT_CHANGE_PROPOSAL_TEMPLATE.md](../../standards/CONTRACT_CHANGE_PROPOSAL_TEMPLATE.md).
2. Name the owner, affected producers/consumers, exact semantic delta and why an
   additive extension is insufficient.
3. Add old/new fixtures, schema validation, producer tests, consumer tests,
   compatibility tests and failure tests before integration.
4. Define artifact migration, rollback and frozen-baseline regression.
5. Obtain owner approval from every affected boundary; `DRAFT` is not approval.
6. Implement producer first, then opt-in consumer support. Do not overwrite old artifacts.
7. Run focused integration and semantic-digest comparison; run heavy replay only
   at the phase exit gate.

## Open proposals（2026-08-22 00:02）

| Proposed area | State | Required owner review |
|---|---|---|
| Winter experiment identity | SCENARIO + DATASET FROZEN; RUN CONTEXT BLOCKED BY MINIMUM HORIZON | contracts + A + Orchestrator intake owner |
| B grid experiment profiles | EXPERIMENTAL, no formal RiskFrame change | B + C compatibility reviewer |
| Adaptive/non-uniform grid contract | PLANNED | B + C + Orchestrator |
| [Candidate route presentation with real geometry/metrics](../proposals/ROUTE_PRESENTATION_CONTRACT_PROPOSAL.md) | DRAFT / PLANNED; current payload remains NOT_PUBLISHED | C + Orchestrator + D |
| Environment factor presentation packages | PLANNED | A/B semantic owners + Orchestrator + D |
