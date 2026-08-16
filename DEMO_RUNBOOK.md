# Demo Runbook

Status: CURRENT
Last Updated: 2026-08-16
Applies To: competition/acceptance demo execution

## Prerequisites

- WSL with `/root/my_project` intact; RC1 artifacts and two same-VHD copies present;
- No network required for the frozen chain (offline audit PASS);
- Python environments: `work_package_a/.venv`, `work_package_b/.venv`,
  `work_package_c/.venv`, `work_package_d/.venv`, `arctic_route_orchestrator/.venv`.

## RC1 Identifiers

See `work_package_a/docs/DEMO_RC1_BASELINE_20260816.md` (authoritative).
Bundle `a-bundle-32cafad4ee280f286d8eb049`; RunContext run-…0b0005;
initial layer-set `layer-set-sha256-51824e96…`; replanned `…ec74a145…`.

## Pre-demo Checks

```bash
cd /root/my_project/work_package_a && ./.venv/bin/python -m arctic_route_data.cli doctor --data-root data
cd /root/my_project/arctic_route_orchestrator && ./.venv/bin/python scripts/offline_demo_audit.py
```

Expected: doctor `ok:true`, audit prints `external network dependency = NONE`.

## Mode A — Full Validation Mode (≈25–30 min)

```bash
cd /root/my_project/arctic_route_orchestrator
C_ASTAR_PROGRESS_SECONDS=30 UV_CACHE_DIR=$PWD/.uv-cache UV_PYTHON_INSTALL_DIR=$PWD/.uv-python \
  UV_PYTHON_DOWNLOADS=never ./.mamba-env/bin/uv run --locked arctic-route-orchestrator run \
  --execution-spec /root/my_project/work_package_a/data/output/golden/mur-v3-smoke-20260816-r6.execution-spec.json \
  --bundle /root/my_project/work_package_a/data/output/bundles/murmansk_dikson_august_2026_demo_v1.bundle.json \
  --run-context /root/my_project/work_package_a/data/output/bundles/murmansk_dikson_august_2026_demo_v1.run-context.json \
  --a-data-root /root/my_project/work_package_a/data \
  --b-config /root/my_project/work_package_b/configs/models/demo_unvalidated_smoke_grid_v4.json \
  --c-config-root /root/my_project/work_package_c/configs \
  --contracts-config-root /root/my_project/arctic_route_contracts/configs \
  --risk-store-root /tmp/rc1-smoke/risk-store \
  --output-dir /tmp/rc1-smoke/output
```

Expected timings (r7): init ≈9 min, b_build ≈15 s, c_initial ≈8 min,
replan ≈8.5 min, total ≈25–30 min. Outputs under `output/` with
`run-stage-report.json` status `completed`.

## Mode B — Live Demo Mode (≤2 min live)

1. Load frozen results: open
   `work_package_a/data/output/golden/mur-v3-smoke-20260816-r6/output/routes/v3/initial.json`
   and `replanned.json` in D.
2. Generate D snapshots:
   ```bash
   cd /root/my_project/work_package_d
   ./.venv/bin/arctic-route-display snapshot --v3 <initial.json> --output d-snapshot-initial.json
   ./.venv/bin/arctic-route-display snapshot --v3 <replanned.json> --output d-snapshot-replanned.json
   ```
3. Live slice (optional, already validated): run a small-window replanning case
   only if it was previously verified; label it clearly as live computation.

Everything loaded from frozen artifacts must be labeled "precomputed RC1
result"; anything computed live must be labeled "live".

## Failure Recovery

- **C stage too slow**: worker timeout now terminates the stage and writes a
  TIMEOUT stage report; restart with the same frozen inputs.
- **Schema error in D**: use the local schema
  `work_package_c/schemas/four-layer-route-plan-set-v3.schema.json`; D loads it
  offline.
- **No network**: no demo path needs it; if an import fails, check the proxy
  env and revert to command-scoped direct mode (see `LOCAL_OPERATOR_ENV.md`).
- **Wrong bundle suspicion**: compare digest with `DEMO_RC1_BASELINE_20260816.md`.
