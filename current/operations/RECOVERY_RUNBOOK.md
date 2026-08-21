---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: CANONICAL
Scope: recovery of RC1 demo environment + git/governance rollback
Canonical For: how to recover from backup and how to roll back governance
Branch: research-validation-system
Last Verified: 2026-08-20
---

# 恢复手册

状态：CURRENT（当前）
最后更新：2026-08-20
适用范围：从本地副本恢复 RC1 演示环境；Git 仓库与治理迁移恢复

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

## Git 仓库恢复

Git 历史是工程基线的不可再生资产。当某仓库的 `.git` 损坏、被误删或 history 被污染时，
按以下双保险顺序恢复（两套证据互相独立，任一可用即可恢复）：

### 双保险策略

1. **文件系统级 `.git` 副本（冷备）**：在任何 destructive 操作（reset、filter-branch、
   rebase、迁移）之前，先对整个 `.git` 目录做 exact copy：
   ```bash
   cp -a /path/to/repo/.git /safe/backup/repo.git-<timestamp>
   ```
   恢复时反向 `cp -a` 回原位置即可，保留全部 objects / refs / config。
2. **Git bundle（可移植备份）**：用于跨环境或长期留存：
   ```bash
   git bundle create /safe/backup/repo-<commit>.bundle --all
   git bundle verify /safe/backup/repo-<commit>.bundle   # 必须 PASS
   ```
   恢复时 `git clone repo.bundle recovered-repo` 或 `git fetch repo.bundle`。

### 完整性校验（恢复前后必做）

```bash
git fsck --full            # 必须无 dangling/error
git bundle verify <b>.bundle
git log --oneline | head   # 确认 HEAD 与预期一致
git status                 # 确认 working tree 预期
```

### 真实恢复记录（本工程已验证）

- 根仓库 `/root/my_project` 的 `.git` 曾丢失；通过**此前制作的 exact-copy 副本**恢复：
  `cp -a` 回 `.git` 后 `git fsck --full` PASS、bundle `verify` PASS、完整 history 保留。
- 经验：**destructive 操作前必须同时具备 filesystem copy 与 bundle 两套证据**，
  且 bundle 在恢复前要用 `git bundle verify` 确认自包含可用。

## 治理迁移回滚

当 `arctic_route_governance` 的某次迁移/重写引入错误时，不要重写已发布到 origin 的
history。优先：

1. 用 `git revert <bad-commit>` 产生反向提交（保留审计轨迹）；
2. 或在新 commit 中修正内容（本工程默认策略：保留上一轮迁移 commit，仅追加修正）；
3. 若需彻底回到迁移前状态且尚未 push，可用 `git reset --hard <pre-migration>`——
   **但本工程禁止对 root recovery repo 与已 push 的 governance history 做此操作**。

> 根仓库 `/root/my_project/.git` 在本轮治理中**刻意保留**作为 recovery / historical
> safety source，不删除、不重置、不重写。最终 retirement 由人工审核后另行执行。
