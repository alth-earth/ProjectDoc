---
Document Status: HISTORICAL_REPORT
Canonical Current State: NO
Report Date: 2026-08-20
Scope: project governance refactor round
Branch: demo-engineering
---

# Strategy B Governance Refactor (2026-08-20)

## Summary

This round performed a project governance refactor: migrating root-level
documentation into a dedicated governance repository, migrating viewer
implementation ownership from orchestrator to work_package_d, and establishing
canonical SSOT documentation.

## Key Changes

1. Root `/root/my_project/.git` retired (plain workspace now).
2. `arctic_route_governance/` established as dedicated governance repo with
   current/frozen/reports/standards/archive structure.
3. All three branches preserved (main=RC1, rc2-development=RC2, demo-engineering=active).
4. Viewer implementation migrated from orchestrator to work_package_d.
5. Orchestrator now owns `scripts/replay_viewer_export.py` (backend artifact producer).
6. D owns HTML/JS/CSS, static server, proof renderer, pngcodec.
7. `ENGINEERING_GOVERNANCE_STANDARD.md` established with documentation governance rules.
8. `CURRENT_STATUS.md` rewritten as whole-project SSOT.
9. `CURRENT_ROADMAP.md` created replacing stale 10-day plan.
10. `DOCUMENTATION_INDEX.md` rewritten as canonical SSOT navigation map.
11. `ARCTIC_ROUTE_SYSTEM.md` updated to A-B-C-D architecture.

## Git Commits

| Repo | Commit | Message |
|------|--------|---------|
| governance | b690c79 | refactor: migrate Arctic Route governance into dedicated repository |
| orchestrator | 54cccf0 | refactor: hand off viewer presentation runtime to work_package_d |
| D | 03f1a3a | feat: adopt replay-driven viewer application |

## Bug Fixes

- `pngcodec.py read_png_rgb`: bytearray slice assignment was a copy, not a view;
  fixed to use direct indexing into decoded buffer.
- `replay_viewer_export.py`: basemap was written as raw RGB bytes, not PNG;
  fixed to call `_write_png`.

## Tests

- D: 50 passed (including 6 pngcodec round-trip tests)
- Orchestrator unit: 60 passed (2.3s)
- Orchestrator other: 13 passed (0.5s)
- Orchestrator integration: NOT RUN (pre-existing slow, not affected by changes)
- D ruff: All checks passed
- Orchestrator ruff: All checks passed
- D render_proof: valid PNG produced at 10:30Z
- D JS syntax: PASS
- GEBCO L2 preflight: PASS (real Scenario B route)
- Bundle export: PASS (721 timeline frames)

## Resource Safety

- free -h start: 6.2Gi available, swap 0B
- Lowest available: ~6.0Gi
- Swap peak: 0B (never used)
- OOM: NO
- Heavy-task overlap: orchestrator test (292MB RSS, single process, no risk)
- Writes outside /root/my_project: NONE
