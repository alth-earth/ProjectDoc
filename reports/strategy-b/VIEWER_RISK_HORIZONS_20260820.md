---
Document Status: ACTIVE_SUPPORTING
Scope: Viewer Product Mainline risk horizons and demo presentation
Canonical For: editor diagnostics, horizon semantics, browser regression
Branch: demo-engineering
Last Verified: 2026-08-20
---

# Viewer Risk Horizons Product Report（2026-08-20 22:50 +08:00）

## 1. Key Delta

| Claim | Before | After | Evidence | Verdict |
|---|---|---|---|---|
| export editor diagnostics | 4 unresolved-import redlines | repo-local resolution contract | `pyrightconfig.json`, `.venv` import smoke, py_compile, Ruff | PASS / EDITOR_ENVIRONMENT |
| Current Risk | PASS | PASS | D 54 tests and Firefox | BROWSER_E2E_PASS |
| +6h | NEXT | floor/exact semantics | 10:30 → requested 16:30, actual 16:00, +5h30m | BROWSER_E2E_PASS |
| +12h | NEXT | explicit unavailable when out of range | 10:30 → requested 22:30, no stale fallback | BROWSER_E2E_PASS |
| +24h | NEXT | explicit unavailable | 10:30 → requested 2026-08-16 10:30, no stale fallback | BROWSER_E2E_PASS |
| Hard Reason | PASS | PASS | independent layer and toggles | BROWSER_E2E_PASS |
| Replanning visual | MVP baseline | pending/adopted + presentation controls | 13:30 / 15:00 screenshots and state checks | BROWSER_E2E_PASS |
| Presentation Mode | NEXT | demo view with Debug hidden by default | real Firefox toggle and screenshot | BROWSER_E2E_PASS |

## 2. P0 Editor Diagnostics Closure

No project `pyright`, `basedpyright`, or `mypy` configuration was present, and
none of those executables was installed in the existing environment. The
Orchestrator `.venv` itself resolves all four imports. A repo-local
`pyrightconfig.json` now points analysis at `.venv` and `src`; no global editor
settings and no production `sys.path` mutation were used.

| # | Line | Diagnostic class | Root cause | Fix | Verification |
|---:|---:|---|---|---|---|
| 1 | 19 | `IMPORT_RESOLUTION` | `numpy` was analyzed outside the Orchestrator `.venv` | `venvPath=.` + `venv=.venv` | import smoke resolves `.venv/lib/python3.13/site-packages/numpy` |
| 2 | 21–25 | `IMPORT_RESOLUTION` | `arctic_route_orchestrator.replay.geospatial` was outside editor `src` roots | execution environment `extraPaths=["src"]` | import smoke resolves `src/.../geospatial.py` |
| 3 | 26 | `IMPORT_RESOLUTION` | same missing `src` resolution for preflight | same repo-local config | import smoke resolves `src/.../preflight.py` |
| 4 | 27 | `IMPORT_RESOLUTION` | same missing `src` resolution for presentation | same repo-local config | import smoke resolves `src/.../presentation.py` |

The runtime script had no `TYPE_ERROR` or `REAL_RUNTIME_ERROR`: `py_compile`
passed, Ruff passed, and the real artifact export completed with L1/L2 PASS.
The environment did not contain a configured type-checker binary, so this
round records the editor-equivalent root cause and configuration closure
instead of installing a new tool.

## 3. Horizon Contract

The existing `presentation.risk-overlay.v1` remains compatible and gains a
presentation-ready selection index. The Orchestrator owns the selection
semantics; D only reads the index and renders the selected frame.

Each horizon selection contains:

```text
requested_horizon_hours
requested_valid_time
actual_valid_time
actual_horizon_seconds
selection_method
availability
reason
frame_index
risk_id
```

Rules:

- `Current`: latest `valid_time <= simulation_time`;
- future horizons: exact match when available, otherwise floor to the latest
  valid time at or before the requested valid time;
- future target must remain inside the formal frame range;
- an out-of-range request is `UNAVAILABLE` with `actual_valid_time=null` and
  `frame_index=null`;
- no horizon request reuses the final frame as a silent forecast;
- horizon selection never changes `simulation_time`, vessel position, route,
  or event state;
- `DATA_UNAVAILABLE` and unavailable horizons are never converted to safe risk.

The real artifact has formal frames 10:00–22:00 UTC. Examples:

| Simulation | Request | Requested valid time | Actual valid time | Actual horizon | Availability |
|---|---|---|---|---:|---|
| 10:00 | +6h | 16:00 | 16:00 | +6h | AVAILABLE |
| 10:00 | +12h | 22:00 | 22:00 | +12h | AVAILABLE |
| 10:00 | +24h | next day 10:00 | — | — | UNAVAILABLE |
| 10:30 | +6h | 16:30 | 16:00 | +5h30m | AVAILABLE |
| 10:30 | +12h | 22:30 | — | — | UNAVAILABLE |
| 18:00 | +6h | next day 00:00 | — | — | UNAVAILABLE |

## 4. Browser E2E

Firefox was launched against D's local server at `127.0.0.1:8131` using the
Playwright CLI. The following were checked in the real browser:

- page, GEBCO, active route, completed track, ship and risk/hard layers;
- Current, +6h, +12h, +24h controls;
- exact/floor display and unavailable horizon display;
- Simulation Clock remained unchanged while switching horizon;
- ship remained at the same simulation position while horizon changed;
- Risk, Hard/Availability, Routes, and Completed Track toggles;
- Presentation Mode hides the Debug panel; Engineering Debug restores it;
- Play/Pause and continuous movement;
- 13:30: active 1, pending 2, decision at 13:00;
- 15:00: active 2, pending 3, `REPLAN_ADOPTED` at 15:00, next decision also
  visible, completed track length 3, superseded route length 22;
- console errors/warnings: 0;
- required static resources: 6/6 HTTP 200, including favicon.

Proof images are in `.runtime` and are not committed:

- [Current 10:00](/root/my_project/.runtime/viewer-proof/horizon-current-10-00.png)
- [+6h at 10:30](/root/my_project/.runtime/viewer-proof/horizon-plus6-10-30.png)
- [+24h unavailable](/root/my_project/.runtime/viewer-proof/horizon-unavailable-plus24-10-30.png)
- [pending 13:30](/root/my_project/.runtime/viewer-proof/replan-pending-13-30.png)
- [adopted 15:00](/root/my_project/.runtime/viewer-proof/replan-adopted-15-00.png)
- [Presentation Mode adopted](/root/my_project/.runtime/viewer-proof/presentation-mode-adopted-15-00.png)

## 5. Ship and route invariants

The browser still uses backend ETA-derived continuous vessel motion:

```text
10:00  lat ~70.3333
10:30  lat ~70.4135
11:00  lat ~70.4938
pixel speed = NO
```

At 10:30, changing Current → +6h → +12h → +24h left the clock at 00:30
and the vessel at latitude ~70.4135. At 15:00 the active revision changed to
2 only at adoption; revision 3 remained pending. `PLAN_REUSED` and
`REPLAN_SKIPPED` remain event/debug state and do not switch routes.

## 6. Performance and elapsed time

This is an engineering observation on local loopback, not a professional
benchmark.

| Resource / check | Observation |
|---|---:|
| `bundle.json` on disk | 1,435,325 B |
| `bundle.json` browser transfer | 1,435,625 B |
| `app.js` browser transfer | 17,982 B |
| `style.css` browser transfer | 4,323 B |
| `gebco_basemap.png` browser transfer | 14,238 B |
| `favicon.svg` browser transfer | 535 B |
| DOMContentLoaded | 174 ms |
| loadEventEnd | 180 ms |
| D full pytest | 54 passed / 1.41 s |
| Orchestrator fast | 77 passed, 2 deselected / 2.48 s |
| Orchestrator integration | 2 passed, 77 deselected / 2,334.71 s (38:54) |

The bundle grew from the current-frame MVP because 721 timeline positions now
carry four explicit horizon selections. The local browser remained responsive
for scrub and horizon switching; no multi-second freeze was observed. The
existing 12h authoritative replay timing remains a separate inherited fact:
latest-head 2,044.9 s / ~34.1 min, not re-run in this round. It must not be
confused with the integration suite wall time.

## 7. Validation levels

- `EDITOR_ENVIRONMENT`: four editor import diagnostics closed with repo-local
  interpreter/type-resolution configuration.
- `UNIT_PASS`: Orchestrator horizon tests 4 passed; D full suite 54 passed.
- `REAL_ARTIFACT_HTTP_SMOKE_PASS`: regenerated bundle and L1/L2 preflight PASS.
- `BROWSER_E2E_PASS`: Firefox horizon, layer, mode, motion, replan,
  console/network checks.
- `REAL_E2E_PASS`: Orchestrator integration 2 passed after export semantics
  changed.
- `FROZEN_BASELINE`: 12h authoritative determinism inherited, not twin-run.

## 8. Remaining work

- richer non-semantic route-transition animation;
- final visual polish and demo rehearsal;
- final Demo Freeze.

No new scenario, data acquisition, 12h/24h replay, governance migration, root
Git retirement, or push was performed.
