---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
Document Role: CANONICAL
Scope: whole-project governance + documentation
Canonical For: project entry point
Branch: research-validation-system
Last Verified: 2026-08-30
---

# Arctic Route 治理仓库

## 这是什么

本仓库存放 Arctic Route 规划系统的**全项目治理与文档**。它不是代码仓库；
代码位于 `${ARCTIC_ROUTE_ROOT}` 下的各工作包子仓库中。

`${ARCTIC_ROUTE_ROOT}` 是一个普通的多仓库工作区，本身不是 Git 仓库。本治理仓库是
规范的文档之家；根目录的历史文档（如有）仅作为证据存在。

## 路径约定（2026-08-24）

本文档及全工作区文档中的 `${ARCTIC_ROUTE_ROOT}` 是**工作区根目录占位符**。
它的作用是指向**包含各工作包目录的公共根目录**——即 `arctic_route_contracts/`、
`arctic_route_governance/`、`arctic_route_orchestrator/`、`work_package_a/` 至
`work_package_d/` 等子仓库的共同父目录（本机当前为 `/root/my_project`）。

解析优先级：

1. 环境变量 `ARCTIC_ROUTE_ROOT`（若已设置，优先使用）；
2. 默认取当前所在目录（解包/克隆后的工作区根目录）；
3. 以上均不可用时的最后回退为 `$HOME`。

校验规则：任何候选根目录必须包含 `arctic_route_contracts/` 目录，否则视为无效
并报错（防止三个来源指向不同副本导致路径错乱）。

Shell 中使用方式：先执行 `export ARCTIC_ROUTE_ROOT=/path/to/root`，文档中的命令
（如 `cd ${ARCTIC_ROUTE_ROOT}/work_package_a`）即可直接运行。

## 仓库布局

```
${ARCTIC_ROUTE_ROOT}/
  arctic_route_governance/   ← 本仓库（治理 + 文档）
  arctic_route_contracts/   ← 共享合约 / schema
  arctic_route_orchestrator/ ← A-B-C-D 根协调器 + 回放引擎
  work_package_a/           ← 数据准备 / 因果可见性
  work_package_b/           ← 动态风险
  work_package_c/           ← 随时间变化的规划
  work_package_d/           ← 展示 / 可视化 / 查看器
```

## 分支映射

| 分支 | 含义 | 状态 |
|---------------------|-----------------------------|----------|
| `main` | RC1 冻结基线 | FROZEN |
| `rc2-development` | RC2 冻结基线 | FROZEN |
| `demo-engineering` | 竞赛演示基线 | FROZEN |
| `research-validation-system` | 研究验证增强 | ACTIVE |

## A/B/C/D 职责

| 包 | 角色 |
|---------|---------------------------------|
| A | 环境数据采集 |
| B | 风险评估与预报 |
| C | 风险感知导航决策 |
| D | 可视化与验证平台 |

**Orchestrator** = 流水线 / 构件 / 展示适配器以及 A-B-C-D 根协调器。它拥有：
- 回放执行
- 导航执行状态
- 重规划生命周期
- 展示适配器（回放内部状态的业务投影）
- L1/L2 展示资格预检
- 展示构件导出

**D** 拥有 Viewer 应用：HTML/JS/CSS、Simulation Clock UI、移动船舶渲染、
路线/轨迹/待定渲染、静态服务器、证明渲染器。D 只消费 Orchestrator 产生的
JSON/PNG 构件——它从不导入 Orchestrator 的私有 Python 模块。

## 到哪里找什么

| 问题 | 答案 |
|-------------------------|-------------------------------------------------|
| 当前状态？ | `current/CURRENT_STATUS.md` |
| 当前路线图？ | `current/CURRENT_ROADMAP.md` |
| 系统架构？ | `current/architecture/ARCTIC_ROUTE_SYSTEM.md` |
| 回放架构？ | `current/architecture/SIMULATION_REPLAY_ARCHITECTURE.md` |
| 演示操作？ | `current/operations/DEMO_RUNBOOK.md` |
| 恢复？ | `current/operations/RECOVERY_RUNBOOK.md` |
| 技术债？ | `current/reference/TECH_DEBT.md` |
| 时间模型？ | `current/reference/TIME_MODEL_QUICK_REFERENCE.md` |
| 文档与工程报告治理标准？ | `standards/AGENT_DOCUMENTATION_RULES.md` |
| RC1 冻结文档？ | `frozen/rc1-main/` |
| RC2 冻结文档？ | `frozen/rc2-rc2-development/` |
| 历史报告？ | `reports/` |
| 旧计划 / 被取代？ | `archive/` |
| 本地操作文档？ | `local/`（gitignored） |

## 文档治理规则

所有文档工作与工程运行报告必须遵循 [`standards/AGENT_DOCUMENTATION_RULES.md`](standards/AGENT_DOCUMENTATION_RULES.md)。
关键规则：

- **SSOT**：每个事实领域恰好只有一份规范文档。
- **禁止追加补丁**：不要在文档末尾追加信息；放到正确的小节。
- **语义化放置**：测试 → 测试文档，缓存 → 环境文档，下一步 → 路线图。
- **归档三步法**：归档前先回填 → 比对 → 收敛。
- **历史报告**：永不改写为"看起来是当前"；如需修正则加修正说明。
- **新标题**：携带真实时间戳，如 `### X.Y 标题（YYYY-MM-DD HH:MM +08:00）`。
- **状态分类**：分开记录文件生命周期（`Overall Status`）、事实角色（`Document Role`）、内容状态（`Content Status`）与验证成熟度。
- **工程报告**：固定保留 15 个区块、关键增量表、声明矩阵与验证成熟度；未运行项必须如实说明。

## 新 Agent 快速上手

1. 阅读本 README。
2. 阅读 [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md)。
3. 阅读 `current/CURRENT_STATUS.md`。
4. 阅读 `current/CURRENT_ROADMAP.md`。
5. 现在你已了解项目状态、下一步以及一切文档的位置。
