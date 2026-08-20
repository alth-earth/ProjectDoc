---
Document Status: ACTIVE_CANONICAL
Scope: project roadmap / next phases
Canonical For: what to do next, milestone sequence
Branch: demo-engineering
Last Verified: 2026-08-20
Supersedes: archive/superseded/ABC_10_DAY_SPRINT.md
---

# Current Roadmap

## Current Phase: Viewer Product Mainline（2026-08-20 22:50 +08:00）

The causal replay engine, performance hardening, physical vessel motion,
deferred adoption, Presentation Adapter, GEBCO L2 preflight, and
Replay-driven Viewer MVP are all established. The real-browser baseline and
current-frame risk product path are now established. Governance completion is
closed for this phase.

## Milestone Sequence

### 1. Dynamic Risk Overlay — Current Frame + Horizons (COMPLETE)

Consumed formal B risk frames via the Presentation Adapter. The current frame
is driven by `simulation_time`, not A forecast lead; selection is the latest
`valid_time` at or before the simulation time. Presentation horizon is
`risk.valid_time - simulation_time`.

Current/+6h/+12h/+24h selections are exported by the Orchestrator with
requested/actual valid times, actual horizon seconds, selection method, and
availability. Floor selection is used only within the formal frame range;
out-of-range requests are unavailable and never reuse a stale frame.

### 2. Hard Reason / Availability Overlay (COMPLETE)

Distinguish LAND, DATA_UNAVAILABLE, OTHER in the viewer.  `unknown != safe`.
Do not render unknown as safe.

### 3. Superseded Route Visualization (MVP COMPLETE)

Show superseded future route (faded) when a new plan is adopted, if the
Adapter can reliably provide it.  Do not fabricate.

### 4. Replanning Event Presentation (MVP COMPLETE)

The Viewer presents the transition from pending to adopted route at the correct
`effective_adoption_time`, with distinct `REPLAN_DECIDED` and
`REPLAN_ADOPTED` event state. Rich animation remains a later polish item.

### 5. Presentation Mode and Layer Controls (COMPLETE)

Presentation Mode hides engineering diagnostics by default. Engineering Debug
remains available, and Risk, Hard/Availability, Routes, and Completed Track can
be toggled independently without changing business semantics.

### 6. Route / Objective Controls

Allow viewer to select route revision, objective, layer for inspection.

### 7. Final UI Polish

Styling, layout, responsive design, debug panel toggle.

### 8. Demo Rehearsal

End-to-end offline demo run with real artifacts.  Verify timing,
narration, and fallback.

### 9. Final Freeze

Freeze demo-engineering as demo baseline.  Tag and document.

## Technical Debt (tracked, do not implement prematurely)

### TD: Pending-Plan Gate

Deferred adoption causes TIME-only candidates to be recomputed during the
pending period, increasing 12h runtime from ~21.8 min to ~34 min.
Future: skip C replan when TIME trigger + pending valid plan exists + A
unchanged + B risk-content unchanged + remaining horizon safe.

### TD: Edge-Interior Planner Origin

Physical vessel position may differ from planner origin node at mid-edge
replan.  This is a known semantic gap, tracked for future investigation.

### TD: Full 144h Causal Provenance

Current provenance does not support full 144h historical causal replay.
Future causal-ready acquisition would need to be designed.

## What NOT to Do

- Do not implement Pending-Plan Gate prematurely.
- Do not rewrite A* / D* Lite / LPA*.
- Do not use Numba / Cython / parallel workers for planner.
- Do not regenerate RC1 / RC2.
- Do not run new 12h / 24h / determinism replays unless backend causal
  semantics change.
- Do not download large datasets without purpose.
- Do not push to remote.
