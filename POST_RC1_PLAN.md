# Post-RC1 Plan

Status: CURRENT
Last Updated: 2026-08-16
Applies To: next phase after Demo RC1

## Pre-demo Mandatory

1. **Worker-mode full RC1 E2E smoke** — run one full v3 through the new
   interruptible worker path (`arctic-route-orchestrator run` after the
   timeout change) to close the r6/r7 old-inline vs worker-path gap.
2. **Live Demo Mode rehearsal** — follow `DEMO_RUNBOOK.md` Mode B end-to-end,
   confirm <2 min live slice and frozen-result loading.
3. **Recovery rehearsal** — follow `RECOVERY_RUNBOOK.md` from the two same-VHD
   copies; confirm doctor + coverage gate + D load.
4. **Independent backup** — only when an external fault domain is provided
   (e.g. `/mnt/d/...`, external SSD, NAS, remote host); update recovery docs.

## Pre-demo Optional

- Display/UI polish in D (map layers, risk animation from frozen results).
- Performance telemetry (persist benchmark tables in `data/output/golden/`).

## Post-RC1 / RC2

- TD-2: `hard_reason` semantics (LAND / DATA_UNAVAILABLE / OTHER), non-blocking.
- TD-4: optional planner optimization (only if demo timing requires it).
- More corridors/scenarios (Tromsø as the documented migration path).
- Productionization concerns (calibration, vessel models, policy layers).

## Explicitly Not In Scope

- Changing TOPAZ/NEXTsim/wave product choices;
- Changing corridor 2.2.0 or the smoke grid;
- Weakening fail-closed / unknown→safe;
- Replacing the time-dependent A* baseline.
