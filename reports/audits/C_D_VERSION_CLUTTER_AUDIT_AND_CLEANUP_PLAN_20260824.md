---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: C/D 工作包版本、合同、Schema、文档与旧分支的清理审计与可执行建议
Canonical For: 哪些 C/D 产物属于当前真相路径，哪些可以安全移除或归档
Branch: research-validation-system
Last Verified: 2026-08-24
Related Canonical Docs:
  - ../standards/ENGINEERING_GOVERNANCE_STANDARD.md
  - ../standards/AGENT_DOCUMENTATION_RULES.md
  - ../standards/CONTRACT_CHANGE_PROPOSAL_TEMPLATE.md
  - ../../../work_package_c/docs/CD_CONTRACT.md
  - ../../../work_package_c/docs/BC_CONTRACT.md
  - ../../../work_package_d/README.md
---

# C/D 版本、合同与旧文件清理审计报告

## 1. 执行摘要

**目标**：以"最近最新基本完备"为准绳，识别 C/D 工作包中已退役的多版本 Schema、旧合同、历史报告、重复 fixture 与旧 git 分支，给出可安全移除/归档的清单与分阶段执行建议，终止"每次改动能只打补丁"的状态。

**核心结论**：

- C 包当前主力是 **v3 四层规划 + v2 单路线后备 + selection-rationale.v1 sidecar**；`bc.risk-frame.v2` 是当前风险输入。
- D 包当前主力是 **Winter Combined Research Viewer + `presentation.route-candidates.v1` + 可选 risk-explanation/selection-rationale consumers**；旧 demo/preflight/RC1 相关代码仍残留。
- 可清理项集中在：v1 Schema/适配器、归档 handoff/README、历史 demo 报告、RC1 fixture 命名、`output/` 历史产物、根目录巨型备份。
- **不可删除项**：v2 路线合同（仍是强制后备）、当前 `CD_CONTRACT.md`/`BC_CONTRACT.md`、v3 schema、selection-rationale schema、当前分支 `research-validation-system`。

**建议行动**：分三阶段执行——先文档/产物（低风险）、再 fixture/schema（中风险）、最后 git 分支（高风险），每阶段后跑全量 `make check`。

---

## 2. 范围 / 非范围

| 范围 | 说明 |
|---|---|
| C 包 `src/arctic_route_planning/` | 旧 v1/v2 适配器、legacy_contracts、过期注释 |
| C 包 `schemas/` | route-plan-v1、risk-frame-v1 是否仍被引用 |
| C 包 `docs/` | 带 `_归档_20260815` / `.archive-20260814-pre-governance` 后缀的文件 |
| C 包根目录 | `README_归档_*.md`、`work_package_c_handoff_归档_*.md`、pre-governance 文档 |
| C 包 `output/` | demo、demo-long、legacy-smoke 等历史产物 |
| D 包 `tests/fixtures/` | `v3_initial_rc1.json`、`v3_replanned_rc1.json` 等命名含 RC1 的 fixture |
| D 包根目录 | 大量历史 demo/viewer/competition 报告 |
| D 包 `README.md` | RC1/RC2/Demo Candidate 等已沉淀为历史的大段内容 |
| 根目录 | `frozen_demo_backup/`、`frozen_demo_backup_secondary/`、`.tar.gz` 备份 |
| 各子项目 git 分支 | rc1、rc2-development、demo-engineering 是否仍需保留 |

| 非范围 | 说明 |
|---|---|
| A/B/Orchestrator/Contracts 包内部清理 | 除非它们与 C/D 合同直接相关 |
| `arctic_route_governance/frozen/rc1-main/`、`frozen/rc2-rc2-development/` | 这是治理层面的冻结基线，按治理标准应保留为 HISTORICAL，不由本次清理触碰 |
| `arctic_route_governance/reports/` 中的历史报告 | 已经是归档区，本次只新增本报告 |
| 当前 C→D 合同语义变更 | 若清理涉及删除 v2 schema，需走 CCP，本次报告只建议，不执行 |

---

## 3. 起始基线

| 维度 | 基线 |
|---|---|
| 当前活跃分支 | `research-validation-system`（C/D/Gov 均 checkout） |
| C 包测试基线 | 175 passed（2026-08-24 修复审计 14 问题后） |
| D 包测试基线 | 100 passed / 3 skipped（selection-rationale consumer 落地后） |
| 主要合同文档 | `work_package_c/docs/CD_CONTRACT.md`、`work_package_c/docs/BC_CONTRACT.md` |
| 主要 Schema | C: v3 四层/v3 路线/v2 路线/selection-rationale/v2 risk-frame；D: 消费 v3/v2 + selection-rationale |

---

## 4. Git 最终状态（当前，未提交）

| 仓库 | 当前分支 | 其他本地分支 | 其他远程分支 |
|---|---|---|---|
| work_package_c | research-validation-system | main, rc1, rc2-development, demo-engineering | origin/main, origin/rc1, origin/rc2-development, origin/demo-engineering, origin/research-validation-system |
| work_package_d | research-validation-system | main, rc1, rc2-development, demo-engineering | origin/main, origin/rc1, origin/rc2-development, origin/demo-engineering, origin/research-validation-system |
| arctic_route_governance | research-validation-system | main, rc2-development, demo-engineering | origin/HEAD→demo-engineering, origin/main, origin/rc2-development, origin/demo-engineering, origin/research-validation-system |

> 注：`origin/HEAD -> demo-engineering` 提示 governance 仓库默认分支仍为旧分支，建议改为 `research-validation-system`。

---

## 5. 文件系统与资源安全

本次为审计报告，未执行删除。预估待清理项：

- 文本文件（md/json/schema）：约 30–50 个
- 大型备份目录：`frozen_demo_backup/`（约 6,200 文件）、`frozen_demo_backup_secondary/`（量级相似）
- 建议：大型备份不直接 `rm`，先确认是否为唯一副本；若为重复备份，可合并后归档到 `.archive/` 或外部存储。

---

## 6. 现状盘点

### 6.1 C 包 Schema 版本现状

| Schema 文件 | 当前用途 | 建议 |
|---|---|---|
| `four-layer-route-plan-set-v3.schema.json` | 主力输出 | **保留** |
| `four-layer-route-plan-set-v3.geojson.schema.json` | 主力输出 GeoJSON | **保留** |
| `route-plan-v3.schema.json` | 主力（四层内单路线） | **保留** |
| `route-plan-v3.geojson.schema.json` | 主力 GeoJSON | **保留** |
| `route-plan-v2.schema.json` | 当前 v2 后备 + selection-rationale 基准 | **保留**（见 §7.1） |
| `route-plan-v1.schema.json` | 无代码引用 | **删除** |
| `risk-frame-v2.schema.json` | 当前 BC 输入 | **保留** |
| `risk-frame-v1.schema.json` | 仅 `legacy_contracts.py` 的 `adapt_risk_frame_v1` 与 `test_legacy_contracts.py` | 若确认无需迁移旧 B 产物则 **删除**；否则迁移到 `archive/` |
| `selection-rationale-v1.schema.json` | 当前 sidecar | **保留** |

### 6.2 C 包源码中的版本残留

| 位置 | 现状 | 建议 |
|---|---|---|
| `src/arctic_route_planning/adapters/legacy_contracts.py` | 仅 `adapt_risk_frame_v1` | 随 risk-frame-v1 schema 一并评估 |
| `src/arctic_route_planning/adapters/legacy_b.py` | 旧 B 适配器 | 检查是否仍被 `cli.py legacy-*` 命令使用；若已废弃则删除 |
| `src/arctic_route_planning/contracts/models.py` | v2 RoutePlan 仍是正式模型 | 保留 |
| `src/arctic_route_planning/publishing/models.py` | `ROUTE_PLAN_SCHEMA_VERSION = "cd.route-plan.v2"` | 保留；v2 仍是后备 |
| `src/arctic_route_planning/publishing/layered_serialization.py` | `_as_v2` 仍用于 v3→v2 投影 | 保留 |

### 6.3 C 包文档与根目录归档文件

C 包当前存在两类"旧版本"：

1. **pre-governance 归档（2026-08-14 前）**：
   - `README.archive-20260814-pre-governance.md`
   - `docs/ACCEPTANCE.archive-20260814-pre-governance.md`
   - `docs/ARCHITECTURE_TRACE.archive-20260814-pre-governance.md`
   - `docs/CD_CONTRACT.archive-20260814-pre-governance.md`
   - `docs/DECISIONS.archive-20260814-pre-governance.md`
   - `docs/SHARED_CONTEXT_MIGRATION.archive-20260814-pre-governance.md`
   - `工作包C项目整体认识与继续开发指南.archive-20260814-pre-governance.md`

2. **2026-08-15 归档**：
   - `README_归档_20260815.md`
   - `work_package_c_handoff_归档_20260815.md`
   - `docs/ACCEPTANCE_归档_20260815.md`
   - `docs/DECISIONS_归档_20260815.md`
   - `docs/STATUS_AND_TODO_归档_20260815.md`

这些文件被当前文档反复引用（如 `README.md` 第 16、58、101 行），造成**当前真相路径被历史文件污染**。按治理标准，归档文件应作为 HISTORICAL 保留，但不应成为日常维护的引用目标。

### 6.4 D 包历史报告与 fixture

D 包根目录堆积大量历史运行报告：

- `COMPETITION_DEMO_FINAL_POLISH_REPORT.md`
- `COMPETITION_DEMO_FREEZE_VALIDATION_REPORT.md`
- `DEMO_FREEZE_VALIDATION_REPORT.md`
- `DEMO_REHEARSAL.md`
- `ENVIRONMENT_LAYER_READINESS.md`
- `REPLAY_48H_EXTENSION_REPORT.md`
- `RISK_DISTRIBUTION_AUDIT.md`
- `VIEWER_DEMO_REHEARSAL_REPORT.md`
- `CURRENT_BASELINE.md`
- `HANDOFF.md`

这些报告大多属于 **HISTORICAL 证据**，只有 `CURRENT_BASELINE.md`、`HANDOFF.md` 可能仍需维护。

D 包 fixture 仍使用 RC1 命名：

- `tests/fixtures/v3_initial_rc1.json`
- `tests/fixtures/v3_replanned_rc1.json`

虽然内容仍是有效的 v3 fixture，但命名携带旧阶段烙印，建议重命名为 `v3_initial.json` / `v3_replanned.json`。

### 6.5 根目录巨型备份

- `frozen_demo_backup/`：约 6,200 文件，4657 + 1541 个子树
- `frozen_demo_backup_secondary/`：量级相似
- `my_project_docs_backup.tar.gz`

`frozen_demo_backup_secondary/` 名称暗示它是二次备份，极可能与 `frozen_demo_backup/` 重复或冗余。

---

## 7. 关键语义 / 合约判断

### 7.1 v2 路线合同不能删除

`cd.route-plan.v2` 在当前架构中承担两个角色：

1. **selection-rationale 的基准计划类型**：`build_selection_rationale(selected_v2, baseline_v2)` 要求 v2 RoutePlan。
2. **v3 的向后兼容后备**：`layered_serialization.py` 中 `_as_v2` 将 v3 投影回 v2，用于语义校验。

因此 `route-plan-v2.schema.json` 与 `contracts/models.py` 中的 `RoutePlan` 必须保留。

### 7.2 v1 risk-frame 与 v1 route-plan 可以删除

- `route-plan-v1.schema.json` 无任何代码/测试引用。
- `risk-frame-v1` 仅在 `legacy_contracts.py` 和 `test_legacy_contracts.py` 中。若项目不再需要从旧 B v1 迁移，可整体删除；若仍需保留迁移能力，建议将 `adapt_risk_frame_v1` 与 schema 一并移入 `archive/` 子目录，并从主 `adapters/__init__.py` 中移除导出。

### 7.3 四层 v3 是当前 C→D 主合同

`cd.four-layer-route-plan-set.v3` 与 `cd.route-plan.v3` 是当前主合同；`selection-rationale.v1` 是已批准的 sidecar。这些必须保留。

---

## 8. 实验 / 备选方案

不适用。本次为清理审计，非算法/架构实验。

---

## 9. 权威运行 / 真实验证

不适用。但建议清理执行后，对每个工作包跑全量 `make check`：

```bash
cd /root/my_project/work_package_c && UV_OFFLINE=1 make check
cd /root/my_project/work_package_d   && UV_OFFLINE=1 make check
```

---

## 10. 性能 / 资源影响

预期收益：

- 减少 `git status`、`ruff check`、文件搜索的噪音。
- 降低新成员理解成本：当前真相路径更清晰。
- 释放磁盘：若删除/归档 `frozen_demo_backup_secondary/`，可释放数 GB（需确认大小）。

风险：

- 误删仍被引用的 fixture/schema 会导致测试失败。
- 归档文件移动后，当前文档中的链接会失效。

---

## 11. 正确性 / 验证

| 验证项 | 方法 |
|---|---|
| Schema 无引用 | `grep -r "route-plan-v1"` / `grep -r "risk-frame-v1"` |
| Fixture 无引用 | 重命名后跑 D 测试 |
| 文档链接有效 | 移动归档文件后，全局搜索旧路径并更新或删除链接 |
| 功能未退化 | C/D `make check` 全绿 |
| 分支删除安全 | 确认 `origin` 上已存在等效分支，再删本地旧分支 |

---

## 12. 确定性 / 可复现性

本次清理不改动算法输出，只移除/归档未使用产物。确定性由现有测试守护。

---

## 13. 构件 / 溯源

待清理的构件清单见 §6。建议清理前对 C/D 两个仓库分别做一次 tag：

```bash
cd work_package_c && git tag -a pre-cleanup-2026-08-24 -m "Baseline before version clutter cleanup"
cd work_package_d && git tag -a pre-cleanup-2026-08-24 -m "Baseline before version clutter cleanup"
```

---

## 14. 已知限制 / 技术债

- 部分历史报告（如 D 的 `DEMO_REHEARSAL.md`）可能包含尚未迁移到当前文档的关键数字；清理前需按治理标准"归档三步法"回填。
- `frozen_demo_backup/` 可能包含真实数据副本，删除前需确认是否有外部备份。
- 旧 git 分支若已被他人使用，删除本地分支不影响远程，但需沟通。

---

## 15. 建议的清理路线图

### 第一阶段：低风险文档/产物清理（1 天内）

目标：减少视觉噪音，不触碰代码。

> **状态：✅ 已完成（2026-08-24）**——以下 6 项全部落地，C/D `make check` 全绿（C 175 passed / D 100 passed + 3 skipped）。

1. **C 包根目录**：将 4 个 pre-governance / 2026-08-15 归档文件移入 `docs/archive/`，并更新 `README.md` 中的引用。✅
2. **C 包 docs**：将 8 个 `*.archive-20260814-pre-governance.md` / `*_归档_20260815.md` 移入 `docs/archive/`。✅
3. **D 包根目录**：创建 `reports/archive/`；将 8 个历史 demo/viewer/competition 报告移入；保留 `CURRENT_BASELINE.md`、`HANDOFF.md`、`README.md`、`CHANGELOG.md`。✅
4. **D 包 README.md**：将 RC1/RC2/Demo Candidate 1/2 等历史大段折叠为"历史背景见 reports/archive/..."一句话链接。✅
5. **根目录**：`my_project_docs_backup.tar.gz` 移入 `.archive/` 或确认后删除。⏸️ **未执行**（用户排除大型备份清理）。
6. **C 包 output/**：删除 `output/legacy-smoke/`；`output/demo/` 与 `output/demo-long/` 保留（synthetic-demo 默认输出）。✅

### 第二阶段：中风险 Schema / Fixture / 适配器清理（1–2 天）

目标：移除已退役的技术债务。

> **状态：✅ 已完成（2026-08-24）**——根据预读修正边界，legacy CLI/适配器/risk-frame-v1 schema 仍服役故保留；其余项落地。

1. **C 包 schema**：
   - 删除 `route-plan-v1.schema.json`（确认无引用）。✅
   - 评估 `risk-frame-v1.schema.json` + `legacy_contracts.py` + `test_legacy_contracts.py`：legacy 适配器仍服役，**保留**。✅（经预读确认）
2. **C 包适配器**：检查 `legacy_b.py` 是否被 CLI 使用；若否，删除。✅ **保留**（仍被 `legacy-*` CLI 命令与测试引用）。
3. **D 包 fixture**：将 `v3_initial_rc1.json` / `v3_replanned_rc1.json` 重命名为 `v3_initial.json` / `v3_replanned.json`，并更新所有测试引用。✅
4. **D 包 `demo/` 子包**：评估是否仍属于当前 Winter 主线。✅ **保留**（仍被 CLI 与测试引用，未归档）。

### 第三阶段：高风险 git 分支与大型备份（2–3 天，需团队确认）

目标：终止多分支并存。

> **状态：⏸️ 用户排除**——不删旧 git 分支，不删大型备份。

1. **设置默认分支**：将 governance 仓库的 `origin/HEAD` 从 `demo-engineering` 改为 `research-validation-system`。⏸️
2. **删除本地旧分支**：在 C/D/Gov 三个仓库中删除 `rc1`、`rc2-development`、`demo-engineering` 本地分支。⏸️
3. **清理远程旧分支**：若团队同意，删除 `origin/rc1`、`origin/rc2-development`、`origin/demo-engineering`。⏸️
4. **大型备份**：`frozen_demo_backup/`、`frozen_demo_backup_secondary/`、`my_project_docs_backup.tar.gz` 保留。⏸️

### 明确不做

- 不重写 C→D 合同语义。
- 不删除 `route-plan-v2`、v3 四层 schema、selection-rationale schema。
- 不删除 `arctic_route_governance/frozen/` 下的冻结基线。
- 不删除 `arctic_route_governance/archive/` 与 `reports/` 中已规范归档的历史报告。

---

## 16. 意外发现 / 修正

| 旧假设 | 新证据 | 修正后的声明 |
|---|---|---|
| D 已完全转向 Winter Research Viewer | D README 仍保留大量 RC1/RC2/Demo Candidate 段落 | D 当前代码已以 Winter 为主，但文档未同步收敛 |
| `frozen_demo_backup_secondary/` 可能是唯一备份 | 名称与目录结构暗示它是二次副本 | 需用 `diff -r` 或 checksum 比对后再决定 |
| C 包只有 v3 在服役 | v2 RoutePlan 仍是 selection-rationale 与 v3 投影的必需品 | v2 schema 与模型必须保留 |

---

## 17. 决策 / 下一阶段

**推荐决策**：

1. 批准执行第一阶段（低风险文档/产物清理），因为它不影响任何代码或测试。
2. 第二阶段需要用户确认是否仍需要 `risk-frame-v1` 旧 B 迁移能力。
3. 第三阶段需要团队确认远程旧分支与大型备份的处理策略。

**下一里程碑**：完成第一阶段后，C/D 工作包的当前真相路径应仅包含：

- 当前分支：`research-validation-system`
- 当前合同：`CD_CONTRACT.md`、`BC_CONTRACT.md`
- 当前 Schema：v3 四层/v3 路线/v2 路线/selection-rationale/v2 risk-frame
- 当前文档：`README.md`、`CHANGELOG.md`、`docs/` 内 ACTIVE 文档

**明确不要做什么**：

- 不要一次性删除所有旧文件。
- 不要把旧分支直接 `--force` 删除而不打 tag。
- 不要把 `frozen_demo_backup/` 直接 `rm -rf` 而不确认备份状态。
