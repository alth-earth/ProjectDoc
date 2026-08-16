# Recovery Runbook

Status: CURRENT
Last Updated: 2026-08-16
Applies To: restoring the RC1 demo from local copies

## Primary Paths

| Item | Location |
|---|---|
| Main data | `work_package_a/data` (raw/ready/source_snapshots/manifest) |
| Copy 1 | `frozen_demo_backup/murmansk_dikson_aug2026` (same VHD) |
| Copy 2 | `frozen_demo_backup_secondary/murmansk_dikson_aug2026` (same VHD) |
| Bundle | `work_package_a/data/output/bundles/murmansk_dikson_august_2026_demo_v1.bundle.json` |
| RunContext | same dir `*.run-context.json` (run …0b0005) |
| v3 outputs | `data/output/golden/mur-v3-smoke-20260816-r6/output` (and r7) |
| D snapshots | `data/output/golden/mur-v3-smoke-20260816-r6/d-snapshot-*.json` |
| Contracts/configs | `arctic_route_contracts/configs` (+ copies in both backups) |

> `frozen_demo_backup_secondary` is a **same-VHD redundant copy**, not an
> independent disaster-recovery backup.

## Restore Order

1. Restore `work_package_a/data` (manifest + ready + raw + source_snapshots)
   from a copy if the main tree is lost.
2. Restore bundle + RunContext from the copy.
3. Restore contracts/configs if needed.
4. Run doctor:
   ```bash
   cd /root/my_project/work_package_a
   ./.venv/bin/python -m arctic_route_data.cli doctor --data-root <restored-root>
   ```
   Expected `ok:true`.
5. Coverage gate:
   `./.venv/bin/python scripts/coverage_audit.py …` → `unknown_navigable_nodes = 0`.
6. Smoke validation: `arctic-route-orchestrator intake` against the restored
   bundle/RunContext (PASS expected).

## Verification Evidence

- Backup doctor PASS (1212 records, 0 errors) recorded in execution logs.
- r6/r7 outputs + D snapshots copied into `execution/` of both copies.
