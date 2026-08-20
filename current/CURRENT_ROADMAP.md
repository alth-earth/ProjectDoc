---
Document Status: ACTIVE_CANONICAL
Scope: project roadmap / next phases
Canonical For: what to do next, milestone sequence
Branch: demo-engineering
Last Verified: 2026-08-20
Supersedes: archive/superseded/ABC_10_DAY_SPRINT.md
---

# Current Roadmap

## Current Phase: Viewer Backend Foundation Ready

The causal replay engine, performance hardening, physical vessel motion,
deferred adoption, Presentation Adapter, GEBCO L2 preflight, and
Replay-driven Viewer MVP are all established.  The project is ready to
advance toward final demo readiness.

## Milestone Sequence

### 1. Dynamic Risk Overlay (NEXT)

Consume B risk frames via the Presentation Adapter.  Risk overlay is
driven by `simulation_time`, not A forecast lead.  Support at least
current risk frame; optionally add +6h / +12h / +24h.  Presentation
horizon = `risk.valid_time - simulation_time`.

### 2. Hard Reason Overlay

Distinguish LAND, DATA_UNAVAILABLE, OTHER in the viewer.  `unknown != safe`.
Do not render unknown as safe.

### 3. Superseded Route Visualization

Show superseded future route (faded) when a new plan is adopted, if the
Adapter can reliably provide it.  Do not fabricate.

### 4. Replanning Event Animation

Animate the transition from pending to adopted route at the correct
`effective_adoption_time`.  Visual cue for REPLAN_DECIDED vs REPLAN_ADOPTED.

### 5. Route / Objective Controls

Allow viewer to select route revision, objective, layer for inspection.

### 6. Final UI Polish

Styling, layout, responsive design, debug panel toggle.

### 7. Demo Rehearsal

End-to-end offline demo run with real artifacts.  Verify timing,
narration, and fallback.

### 8. Final Freeze

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
