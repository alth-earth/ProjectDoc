# 恢复手册

状态：CURRENT（当前）
最后更新：2026-08-16
适用范围：从本地副本恢复 RC1 演示环境

## 主要路径

| 制品 | 位置 |
|---|---|
| 主数据 | `work_package_a/data`（raw/ready/source_snapshots/manifest） |
| 副本 1 | `frozen_demo_backup/murmansk_dikson_aug2026`（同一 VHD） |
| 副本 2 | `frozen_demo_backup_secondary/murmansk_dikson_aug2026`（同一 VHD） |
| Bundle | `work_package_a/data/output/bundles/murmansk_dikson_august_2026_demo_v1.bundle.json` |
| RunContext | 同目录 `*.run-context.json`（run …0b0005） |
| v3 输出 | `data/output/golden/mur-v3-smoke-20260816-r6/output`（及 r7） |
| D 快照 | `data/output/golden/mur-v3-smoke-20260816-r6/d-snapshot-*.json` |
| contracts/配置 | `arctic_route_contracts/configs`（两份副本中也有备份） |

> `frozen_demo_backup_secondary` 是**同 VHD 冗余副本**，不是独立灾备。

## 恢复顺序

1. 若主目录丢失，先从副本恢复 `work_package_a/data`
   （manifest + ready + raw + source_snapshots）。
2. 从副本恢复 bundle 与 RunContext。
3. 必要时恢复 contracts/配置。
4. 运行 doctor：
   ```bash
   cd /root/my_project/work_package_a
   ./.venv/bin/python -m arctic_route_data.cli doctor --data-root <恢复后的根目录>
   ```
   预期 `ok:true`。
5. 覆盖 gate：
   `./.venv/bin/python scripts/coverage_audit.py …` → `unknown_navigable_nodes = 0`。
6. 冒烟验证：对恢复后的 bundle/RunContext 运行
   `arctic-route-orchestrator intake`（预期 PASS）。

## 验证证据

- 备份 doctor PASS（1212 条记录、0 错误）记录在执行日志中；
- r6/r7 输出与 D 快照已增量同步到两份副本的 `execution/` 目录。
