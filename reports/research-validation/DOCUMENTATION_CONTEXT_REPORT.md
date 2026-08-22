---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: Winter A freeze audit documentation context
Canonical/Supporting: Supporting audit; canonical status remains under current/
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Documentation Context Report

## 1. 审计口径（2026-08-22 21:56 +08:00）

本报告按“代码、schema、配置、制品及生产者/消费者校验优先于文档”的顺序核对
Winter A 冻结状态。未读取 archive 作为当前事实来源，未修改 canonical 状态文档，
未运行 B/C pipeline。

## 2. 当前 SSOT（2026-08-22 21:56 +08:00）

| 问题 | 当前单一事实来源（SSOT） | 审计用途 |
|---|---|---|
| 文档导航 | `DOCUMENTATION_INDEX.md` | 决定应信任的 current 文档 |
| 当前阶段与能力 | `current/CURRENT_STATUS.md` | Research Validation 当前状态 |
| 下一里程碑 | `current/CURRENT_ROADMAP.md` | Winter A→B→C→D 顺序 |
| 研究决策 | `current/decisions/RESEARCH_VALIDATION_DECISIONS.md` | 冻结边界与已批准决策 |
| Winter 场景状态 | `current/reference/WINTER_SCENARIO_STATUS.md` | Winter 数据与门槛状态 |
| Winter 数据策略 | `current/proposals/WINTER_DATA_POLICY_PROPOSAL.md` | CARRA 与 cadence 提案 |
| 文档维护规则 | `standards/AGENT_DOCUMENTATION_RULES.md` | 状态、归属与归档规则 |

当前 phase 为 **Research Validation Experiment Phase**。`main`、
`rc2-development`、`demo-engineering` 的既有证据保持冻结；主动研发分支为
`research-validation-system`。A 负责 DatasetBundle，B 负责 RiskFrame，C 负责路线，
Orchestrator 负责流水线/制品适配，D 是唯一 Viewer runtime owner。

## 3. Winter 相关文档（2026-08-22 21:56 +08:00）

| 文档 | 角色 | 当前用途 |
|---|---|---|
| `current/reference/WINTER_SCENARIO_STATUS.md` | CANONICAL | Winter 场景当前状态 |
| `current/proposals/WINTER_DATA_POLICY_PROPOSAL.md` | DRAFT proposal | 数据源与 cadence 决策依据 |
| `reports/research-validation/WINTER_DATA_FEASIBILITY_REPORT.md` | SUPPORTING | 初始可行性证据 |
| `reports/research-validation/WINTER_DATA_ACQUISITION_REPORT.md` | SUPPORTING | 早期 9/12 下载证据 |
| `reports/research-validation/WINTER_SOURCE_VALIDATION_REPORT.md` | SUPPORTING | 官方源验证证据 |
| `reports/research-validation/WINTER_MET_SOURCE_COMPARISON.md` | SUPPORTING | 气象候选源比较 |
| `reports/research-validation/WINTER_DATA_RESOLUTION_ROUND4_REPORT.md` | HISTORICAL SUPPORTING | 9/12 与 CARRA adapter 尚未完成时的检查点 |
| `work_package_a/docs/WINTER_DATASET_DELIVERY_20260822.md` | PRODUCER SUPPORTING | 本轮 A bundle 交付记录 |

## 4. 一致性问题（2026-08-22 21:56 +08:00）

| # | 文档陈述 | 实际证据 | 结论 |
|---:|---|---|---|
| 1 | `CURRENT_STATUS` 仍写 9/12、CARRA adapter pending、bundle 未实现 | 已有可解析、12/12 完整的 tracked `a.dataset-bundle.v2` | canonical 状态滞后 |
| 2 | `WINTER_SCENARIO_STATUS` 同时出现 `FROZEN`、`READY_FOR_GENERATION`、`NOT_IMPLEMENTED`、`BLOCKED_WITH_DECISION` | bundle 已生成并冻结，但 B 尚未开始 | 同一文档内部冲突 |
| 3 | 多处文字使用结束时间 `2026-02-21T12Z` | scenario config 与 bundle 的 `requested_end` 均为 `2026-02-21T00Z` | 场景窗口口径冲突 |
| 4 | 交付文字把 `generation_id=0` 描述为 bundle 字段 | `a.dataset-bundle.v2` 无该字段；generation 属于 RunContext/执行身份 | 字段归属错误 |
| 5 | 文字称所有变量补齐到 12Z | 气象只到 00Z；小时类型缺 01Z/02Z | 尾部覆盖陈述不成立 |
| 6 | 文档声称新文件 Ruff clean | 当前 focused Ruff 检出 47 项，主要为中文全角标点规则及一处 E501 | 验证陈述需修正 |

历史 Round4 报告在其生成时是正确检查点，不应改写历史结论；应由 canonical current
文档明确标注其已被 2026-08-22 的 A bundle 交付所 supersede。

## 5. 状态同步建议（2026-08-22 21:56 +08:00）

本轮仅提出建议，不直接修改 canonical 文档：

```text
WINTER_DATASET_STATUS = FROZEN_ARTIFACT_READY
A_TO_B_FORMAL_HANDOFF = BLOCKED_BY_MISSING_RUN_CONTEXT
B_WINTER_VALIDATION = NOT_STARTED
C_WINTER_VALIDATION = NOT_STARTED
D_WINTER_VISUALIZATION = NOT_STARTED
```

同时应统一官方场景窗口为配置定义的 144 小时：
`2026-02-15T00Z` 至 `2026-02-21T00Z`。若研究目标确需延长至 12Z，应建立新的场景修订
与新 bundle，不应修改当前冻结 bundle 的事实含义。
