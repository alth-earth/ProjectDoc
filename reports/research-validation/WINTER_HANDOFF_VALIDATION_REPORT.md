---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - BLOCKED
Document Role: SUPPORTING
Scope: A-to-B Winter formal handoff precondition validation
Canonical/Supporting: Supporting validation evidence
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Winter Handoff Validation Report

## 1. Verdict（2026-08-22 22:24 +08:00）

```text
A_TO_B_FORMAL_HANDOFF = BLOCKED_BY_BUNDLE_MINIMUM_HORIZON
READY_FOR_B_VALIDATION = NO
```

## 2. Validation Matrix（2026-08-22 22:24 +08:00）

| Check | Result | Evidence |
|---|---|---|
| bundle JSON parse | PASS | `a.dataset-bundle.v2` strict producer/consumer parse |
| bundle ID/digest identity | PASS | content-addressed values match |
| bundle file SHA-256 | PASS | `5cf81c…795` |
| 12 required data types | PASS | 1,212 records; all coverage rows complete |
| bundle `formal_run_eligible` property | PASS / INSUFFICIENT ALONE | property checks v2 + coverage completeness, not scenario minimum horizon |
| shared config validation | PASS | 2 corridors, 8 scenarios, 1 vessel |
| scenario requested window | PASS | 15T00Z → 21T00Z |
| minimum horizon covers scenario | FAIL | minimum ends 20T12Z, 12 h early |
| RunContext generation | FAIL_CLOSED | official CLI returned contract error; no file created |
| RunContext schema/identity | NOT_RUN | no legal RunContext exists |
| ExecutionSpec publication | NOT_RUN | prevented to avoid orphaned runnable-looking identity |
| Orchestrator intake | NOT_RUN | requires RunContext |
| B/C/D execution | NOT_RUN | explicitly out of scope |

## 3. Reproduction（2026-08-22 22:24 +08:00）

The official generator was invoked with the current config root, frozen bundle, explicit run UUID
and creation timestamp. It returned:

```text
error: DatasetBundle minimum_required_end does not cover the scenario
```

No output RunContext was left behind. Runtime evidence is stored at
`.runtime/test-logs/winter-run-context-create.log` and is not a Git artifact.

## 4. Fail-closed Decision（2026-08-22 22:24 +08:00）

No manual RunContext, reduced simulation end, altered scenario, modified bundle, or schema extension
was used. This is a real formal handoff failure even though raw coverage reaches the requested end.

An important interface finding is that `DatasetBundleIdentity.formal_run_eligible=True` is necessary
but not sufficient for a scenario-bound formal run. `create_run_context()` applies the additional
minimum-horizon gate, and Orchestrator intake applies an equality gate. Reports must not promote the
bundle-level property directly to `READY_FOR_B_VALIDATION`.

The least-risk recovery is a new immutable A bundle identity generated with
`minimum_horizon_hours=144`, using the already validated records and preserving the existing bundle.
That action requires a separate A publication round and is not performed here.
