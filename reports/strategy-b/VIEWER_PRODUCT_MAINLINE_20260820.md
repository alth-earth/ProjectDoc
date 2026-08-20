---
Document Status: ACTIVE_SUPPORTING
Scope: Viewer Product Mainline engineering closure
Canonical For: browser E2E, risk presentation, route/replanning presentation
Branch: demo-engineering
Last Verified: 2026-08-20
---

# Viewer Product Mainline Engineering Report（2026-08-20 21:13 +08:00）

## 1. Key Delta

| Claim | Before | After | Evidence | Verdict |
|---|---|---|---|---|
| Browser E2E | NOT PROVEN | BROWSER_E2E_PASS | Firefox against local D server; screenshots, DOM/state, console and HTTP checks | PASS |
| Dynamic Risk | NOT_IMPLEMENTED | BROWSER_E2E_PASS | `presentation.risk-overlay.v1` current frames rendered from formal B frames | PASS |
| Hard Reason | NEXT | BROWSER_E2E_PASS | Separate LAND / DATA_UNAVAILABLE / OTHER layer; unknown is not safe | PASS |
| Route / replanning | backend/UI baseline only | BROWSER_E2E_PASS | pending, adopted, superseded, completed-track states at 13:00/13:30/15:00 | PASS |
| Viewer owner | D | D | D owns HTML/JS/CSS, clock and renderer; Orchestrator exports | PRESERVED |
| Ship movement | artifact/state PASS | BROWSER_E2E_PASS | 10:00, 10:30, 11:00 positions and Play observation | REGRESSION PASS |

## 2. Scope and authority

No new replay, historical data acquisition, governance migration, root-Git
retirement, or remote push was performed. The real existing artifact was used:

`work_package_a/data/output/rc2-smoke/causal-replay-mvp/sb-viewer-baseline-12h-det/`

The flow is:

`formal A/B/C artifact → Orchestrator presentation export → D Viewer runtime`.

The Orchestrator does not own Viewer runtime. D does not read raw weather data,
recalculate B risk, or infer hard reasons.

## 3. Browser E2E evidence

Browser automation actually launched Firefox through the local Playwright CLI
against `http://127.0.0.1:8131/`, served by D's
`scripts/replay_viewer_serve.py`. The default sandbox initially blocked the
browser/socket path; the attended run used the permitted escalated local
browser path. This is recorded as an environment constraint, not substituted
for a browser pass.

Verified in the real browser:

- page loaded; title was `Arctic Route Replay Viewer`;
- GEBCO basemap, authoritative route, completed track, risk and hard layers,
  and ship were visible;
- Play changed the button to Pause and advanced the Simulation Clock and ship;
- Pause, scrub, and 1x/2x/4x/8x controls worked;
- scrub to 10:30 yielded the expected continuous vessel position;
- at 13:00 and 13:30 active revision remained 1 and pending revision 2;
- at 15:00 active revision became 2 and the superseded route was visible;
- browser console errors/warnings: 0; static requests: all 200; no 404 or
  failed fetch; canvas rendered successfully.

Proof images are kept outside Git under `.runtime`:

- [10:00 risk view](/root/my_project/.runtime/viewer-proof/risk-10-00.png)
- [13:30 pending view](/root/my_project/.runtime/viewer-proof/risk-replan-13-30.png)
- [15:00 adopted view](/root/my_project/.runtime/viewer-proof/risk-replan-15-00.png)

## 4. Dynamic Risk contract

The Orchestrator now exports `presentation.risk-overlay.v1` from formal
`bc.risk-frame.v2` files in the same real artifact. The export validates schema,
scenario, array shape, duplicate valid times, and provenance, and fails closed.
It does not recalculate B.

- Source: formal `bc.risk-frame.v2`; provenance in bundle: `formal`.
- Bundle cadence: 3600 seconds; 13 frames from 10:00 through 22:00 UTC.
- Semantic level range: 1–5; the Viewer preserves the backend level.
- Current selection: latest `valid_time` at or before `simulation_time`.
- Horizon: `risk.valid_time - simulation_time`; it is not A forecast lead.
- Risk cadence is hourly; ship rendering remains continuous and independent.
- `hard_reason` remains a separate layer. `LAND`, `DATA_UNAVAILABLE`, and
  `OTHER` are not converted to a green/low-risk value.
- Risk cells and GEBCO/route/ship use the same canonical lon/lat projection.

The current-frame MVP is complete. +6h/+12h/+24h presentation controls are
explicitly NEXT and were not claimed as delivered.

## 5. Ship evidence

Browser/state checks produced the following positions on the authoritative
physical route:

| Simulation time | Latitude | Longitude |
|---|---:|---:|
| 10:00 | ~70.3333 | 18.4000 |
| 10:30 | ~70.4135 | 18.4000 |
| 11:00 | ~70.4938 | 18.4000 |

The position is derived from route-edge ETA and the backend linear lon/lat
interpolation contract. Pixel speed is **NO**. Browser Play visibly advanced
the same Simulation Clock and vessel state; risk-frame cadence did not control
ship motion.

## 6. Replanning evidence

| Time | Active | Pending | Event / visual meaning |
|---|---:|---:|---|
| 13:00 | 1 | 2 | `REPLAN_DECIDED`; pending future route appears, active route unchanged |
| 13:30 | 1 | 2 | pending route remains; vessel continues on authoritative physical route |
| 15:00 | 2 | 3 | `REPLAN_ADOPTED`; revision 2 becomes active and prior future route is superseded |

The completed-track prefix did not regress. `PLAN_REUSED` and
`REPLAN_SKIPPED` are event/debug state only and do not switch the route.

## 7. Verification levels

- `BROWSER_E2E_PASS`: Firefox page, map, layers, controls, motion, replan
  states, console and network.
- `REAL_ARTIFACT_HTTP_SMOKE_PASS`: D server endpoints, bundle, basemap and
  preflight from the existing artifact.
- `UNIT_PASS`: D full suite, 53 passed; targeted presentation tests, 8 passed.
- `REAL_E2E_PASS`: Orchestrator integration rerun for the changed presentation
  export/risk artifact semantics; result is recorded in the round test log.
- `FROZEN_BASELINE`: inherited 12h authoritative determinism; not twin-run in
  this round.

## 8. Regression commands

- D: `53 passed`; Ruff clean; `node --check viewer/app.js` clean.
- Orchestrator fast: `73 passed, 2 deselected`; Ruff clean.
- Orchestrator integration: see
  `.runtime/test-logs/orchestrator-integration-20260820.log`.

## 9. Unexpected findings and handling

1. Restricted sandbox browser/socket startup was blocked. An attended
   escalated local Firefox run supplied genuine browser evidence; the product
   result is not mislabeled as HTTP-only.
2. The existing artifact's risk metadata did not itself contain the spatial
   matrices needed by a geographic overlay. The Orchestrator adapter therefore
   reads the co-located immutable formal risk-frame files and emits a
   presentation-ready projection; D still performs no B computation.
3. A first export validation exposed a matrix-shape check defect. It was fixed,
   then the export and bundle tests were rerun successfully.
4. The first server trace exposed a missing `favicon.ico` request (404). D
   now serves a local `favicon.svg`; the final browser run had 0 console
   errors/warnings and all six static resources returned 200.
5. No route/track land crossing, transform mismatch, NaN position, browser
   rendering exception, or final-run console error was observed.

## 10. Performance and elapsed-time analysis

This is an engineering observation, not a professional benchmark. The local
Firefox navigation timing measured approximately 49 ms to `loadEventEnd` and
48 ms to `DOMContentLoaded` for the self-contained local Viewer page. The
resource timing probe measured:

| Resource | Transfer | Duration |
|---|---:|---:|
| `bundle.json` | 442,950 B | 5 ms |
| `app.js` | 13,186 B | 14 ms |
| `style.css` | 3,911 B | 13 ms |
| `gebco_basemap.png` | 14,238 B | 3 ms |
| `favicon.svg` | small local asset | 200 final request |

The on-disk bundle was 442,650 B; the bundle includes 721 one-minute timeline
entries and 13 hourly risk frames. Scrub and Play remained responsive in the
browser run; no multi-second freeze or visible frame stall was observed. Risk
rendering uses precomputed presentation-ready cells and only selects the
current frame at render time; D does not traverse raw forecast grids or run B
logic per frame. Ship interpolation remains continuous and independent of the
hourly risk cadence.

Measured verification elapsed times:

| Verification | Result | Elapsed |
|---|---|---:|
| D full pytest | 53 passed | 1.43 s |
| D targeted presentation tests | 8 passed | included in test run; targeted pass |
| Orchestrator fast pytest | 73 passed, 2 deselected | 2.53 s |
| Orchestrator integration | 2 passed, 73 deselected | 2,334.73 s / 38:54 |

The inherited authoritative 12h replay timing is not re-run evidence for this
round; the recent closure recorded approximately 2,495.25 s / 41:35. The
38:54 integration result above is the only heavy verification run started in
this round, and it was run because the presentation export/risk artifact
semantics changed.

## 11. Remaining product work

- current/+6h/+12h/+24h risk horizon controls;
- richer, non-semantic route adoption animation;
- final presentation polish, demo rehearsal, and final freeze.

These are product NEXT items, not governance repair work.

## 12. Git and push boundary

Local commits are created in the changed package repositories only. The
deprecated `/root/my_project` documentation Git repository remains untouched;
its pre-existing untracked `work_package_d/` directory is not staged. Push is
not performed.
