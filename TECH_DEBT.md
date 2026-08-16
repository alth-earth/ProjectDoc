# Technical Debt Register

Status: CURRENT
Last Updated: 2026-08-16
Scope: non-blocking items only

| ID | Item | Priority | RC1 Blocker | Reason | Suggested Next Step |
|---|---|---|---|---|---|
| TD-1 | Worker-mode full RC1 E2E not run | High | No | r6/r7 used old inline path; worker timeout path is unit-tested only | Pre-demo: run one full v3 via worker path |
| TD-2 | `hard_reason` semantics (LAND vs DATA_UNAVAILABLE vs OTHER) | Medium | No | Both map to hard today; safe but not distinguishable in audit/UI | Post-RC1 contract change |
| TD-3 | Independent/offsite backup | Medium | No | Both copies are same VHD | Requires external path |
| TD-4 | Optional planner performance optimization | Low | No | 144h single objective ≈96s is acceptable | Only if demo timing requires |
| TD-5 | Per-stage timeout not yet exercised on real full chain | High | No | Worker watchdog tested with fake workers | Covered by TD-1 |

Resolved items are NOT listed here; see `最终交付说明.md` Historical/Resolved.
