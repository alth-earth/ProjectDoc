---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
Document Role: CANONICAL
Scope: documentation navigation map
Canonical For: which document to trust for each question
Branch: research-validation-system
Last Verified: 2026-08-30
---

# 文档索引

**该信任哪份文件？** 本索引回答这个问题。

本仓库是 Arctic Route 规划系统的**文档与治理中枢**（非代码仓库）。索引按"问题 → 文档"组织，
并给出各类文档的可信等级与冲突解决顺序。除特别说明外，路径均相对于本文件所在目录
（`arctic_route_governance/`）。

## 一、当前文档（今天的项目状态，可信任）

| 问题 | 文档 |
|----------|----------|
| 项目现在处于什么状态？ | [current/CURRENT_STATUS.md](current/CURRENT_STATUS.md) |
| 下一步做什么？ | [current/CURRENT_ROADMAP.md](current/CURRENT_ROADMAP.md) |
| 系统架构？ | [current/architecture/ARCTIC_ROUTE_SYSTEM.md](current/architecture/ARCTIC_ROUTE_SYSTEM.md) |
| 仿真回放架构？ | [current/architecture/SIMULATION_REPLAY_ARCHITECTURE.md](current/architecture/SIMULATION_REPLAY_ARCHITECTURE.md) |
| 如何运行演示？ | [current/operations/DEMO_RUNBOOK.md](current/operations/DEMO_RUNBOOK.md) |
| 如何恢复？ | [current/operations/RECOVERY_RUNBOOK.md](current/operations/RECOVERY_RUNBOOK.md) |
| 技术债有哪些？ | [current/reference/TECH_DEBT.md](current/reference/TECH_DEBT.md) |
| 研究验证缺口分析？ | [current/RESEARCH_VALIDATION_GAP_ANALYSIS.md](current/RESEARCH_VALIDATION_GAP_ANALYSIS.md) |
| 研究决策记录？ | [current/decisions/RESEARCH_VALIDATION_DECISIONS.md](current/decisions/RESEARCH_VALIDATION_DECISIONS.md) |
| 合约归属登记？ | [current/reference/CONTRACT_OWNERSHIP_REGISTRY.md](current/reference/CONTRACT_OWNERSHIP_REGISTRY.md) |
| 并行开发归属？ | [current/DEVELOPMENT_OWNERSHIP.md](current/DEVELOPMENT_OWNERSHIP.md) |
| 合约变更提案模板？ | [standards/CONTRACT_CHANGE_PROPOSAL_TEMPLATE.md](standards/CONTRACT_CHANGE_PROPOSAL_TEMPLATE.md) |
| 冬季场景就绪状态？ | [current/reference/WINTER_SCENARIO_STATUS.md](current/reference/WINTER_SCENARIO_STATUS.md) |
| 时间模型？ | [current/reference/TIME_MODEL_QUICK_REFERENCE.md](current/reference/TIME_MODEL_QUICK_REFERENCE.md) |
| 文档治理 / AI 写作 / 工程报告规则？ | [standards/AGENT_DOCUMENTATION_RULES.md](standards/AGENT_DOCUMENTATION_RULES.md) |

## 二、当前提案（current/proposals/）

进行中或已批准的提案（含机读 schema/示例），是"当前真相"的一部分：

| 提案 | 说明 |
|------|------|
| [WINTER_DATA_POLICY_PROPOSAL.md](current/proposals/WINTER_DATA_POLICY_PROPOSAL.md) | Winter 气象数据源与时间间隔策略（A-WINTER-MET-001，已批准） |
| [ROUTE_PRESENTATION_CONTRACT_PROPOSAL.md](current/proposals/ROUTE_PRESENTATION_CONTRACT_PROPOSAL.md) | 路线候选展示合约提案 |
| [`risk-explanation.v1.schema.json`](current/proposals/risk-explanation.v1.schema.json) | 逐格风险解释 sidecar v1 Schema 提案 |
| [`risk-explanation.v1.example.json`](current/proposals/risk-explanation.v1.example.json) | 逐格风险解释 sidecar v1 设计示例 |

## 三、治理标准（standards/）

| 文档 | 角色 |
|------|------|
| [CONTRACT_CHANGE_PROPOSAL_TEMPLATE.md](standards/CONTRACT_CHANGE_PROPOSAL_TEMPLATE.md) | 跨包合约变更提案强制模板 |
| [AGENT_DOCUMENTATION_RULES.md](standards/AGENT_DOCUMENTATION_RULES.md) | 文档治理、AI/Agent 协作与工程运行报告的统一规范 |

## 四、冻结基线（frozen/，历史基线，勿修改）

| 阶段 | 位置 | 说明 |
|-------|----------|------|
| RC1（`main` 分支） | [frozen/rc1-main/](frozen/rc1-main/) | RC1 冻结基线（`RC1_FROZEN_STATUS.md`） |
| RC2（`rc2-development` 分支） | [frozen/rc2-rc2-development/](frozen/rc2-rc2-development/) | RC2 冻结基线（`RC2_DEVELOPMENT_STATUS.md`） |

> 冻结文档与当前文档冲突时，以当前文档为准；冻结文档本身不得修改。

## 五、研究验证支持报告（reports/research-validation/）

`reports/research-validation/` 下的审计、冒烟与门禁报告**支持**当前规范文档；
它们不是项目真相的平行来源。按主题分组如下：

### 5.1 启动与各轮次总览

| 报告 | 说明 |
|------|------|
| [RESEARCH_VALIDATION_PHASE_KICKOFF_REPORT.md](reports/research-validation/RESEARCH_VALIDATION_PHASE_KICKOFF_REPORT.md) | 研究验证阶段启动报告 |
| [RESEARCH_VALIDATION_ACCELERATION_REPORT.md](reports/research-validation/RESEARCH_VALIDATION_ACCELERATION_REPORT.md) | 研究验证加速报告 |
| [RESEARCH_VALIDATION_ROUND2_REPORT.md](reports/research-validation/RESEARCH_VALIDATION_ROUND2_REPORT.md) | 第二轮实验结果 |
| [RESEARCH_VALIDATION_ROUND3_REPORT.md](reports/research-validation/RESEARCH_VALIDATION_ROUND3_REPORT.md) | 第三轮真实实验结果 |

### 5.2 文档与数据源审计

| 报告 | 说明 |
|------|------|
| [DOCUMENT_AUDIT_REPORT.md](reports/research-validation/DOCUMENT_AUDIT_REPORT.md) | 文档审计 |
| [DOCUMENTATION_CONTEXT_REPORT.md](reports/research-validation/DOCUMENTATION_CONTEXT_REPORT.md) | 文档上下文报告 |
| [ARCHITECTURE_CONTRACT_AUDIT.md](reports/research-validation/ARCHITECTURE_CONTRACT_AUDIT.md) | 架构/合约审计 |
| [DATA_SOURCE_TRANSITION_AUDIT.md](reports/research-validation/DATA_SOURCE_TRANSITION_AUDIT.md) | 数据源迁移审计 |

### 5.3 风险管道、标定与解释

| 报告 | 说明 |
|------|------|
| [RISK_PIPELINE_AUDIT_AND_WINTER_DATA_VALIDATION_REPORT.md](reports/research-validation/RISK_PIPELINE_AUDIT_AND_WINTER_DATA_VALIDATION_REPORT.md) | A→B→C→D 风险管道审计 + Winter 数据验证 |
| [RISK_CALIBRATION_RESEARCH_REPORT.md](reports/research-validation/RISK_CALIBRATION_RESEARCH_REPORT.md) | B 风险标定研究 |
| [RISK_EXPLANATION_SIDECAR_DESIGN_REPORT.md](reports/research-validation/RISK_EXPLANATION_SIDECAR_DESIGN_REPORT.md) | 逐格风险解释 sidecar 设计 |

### 5.4 接口冻结与并行开发状态

| 报告 | 说明 |
|------|------|
| [B_C_D_INTERFACE_STATUS.md](reports/research-validation/B_C_D_INTERFACE_STATUS.md) | B/C/D 接口与 D 研究第一阶段状态 |
| [B_INTERFACE_FREEZE_AUDIT.md](reports/research-validation/B_INTERFACE_FREEZE_AUDIT.md) | B 接口冻结审计 |
| [C_INTERFACE_FREEZE_AUDIT.md](reports/research-validation/C_INTERFACE_FREEZE_AUDIT.md) | C 接口冻结审计 |
| [D_INTERFACE_FREEZE_AUDIT.md](reports/research-validation/D_INTERFACE_FREEZE_AUDIT.md) | D 接口冻结审计 |
| [D_INTERFACE_READY_REPORT.md](reports/research-validation/D_INTERFACE_READY_REPORT.md) | D 接口就绪报告 |

### 5.5 B/C/D 研究增强分析

| 报告 | 说明 |
|------|------|
| [B_RESEARCH_ENHANCEMENT_ANALYSIS.md](reports/research-validation/B_RESEARCH_ENHANCEMENT_ANALYSIS.md) | B 包研究增强分析 |
| [C_RESEARCH_ENHANCEMENT_ANALYSIS.md](reports/research-validation/C_RESEARCH_ENHANCEMENT_ANALYSIS.md) | C 包研究增强分析 |
| [D_RESEARCH_ENHANCEMENT_ANALYSIS.md](reports/research-validation/D_RESEARCH_ENHANCEMENT_ANALYSIS.md) | D 包研究增强分析 |

### 5.6 Winter A：数据源、可用性与采集

| 报告 | 说明 |
|------|------|
| [WINTER_DATA_FEASIBILITY_REPORT.md](reports/research-validation/WINTER_DATA_FEASIBILITY_REPORT.md) | Winter 12 类数据可行性 |
| [WINTER_DATA_ACQUISITION_REPORT.md](reports/research-validation/WINTER_DATA_ACQUISITION_REPORT.md) | Winter 数据采集报告 |
| [WINTER_DATA_AVAILABILITY_FOLLOWUP.md](reports/research-validation/WINTER_DATA_AVAILABILITY_FOLLOWUP.md) | Winter 数据可用性跟进 |
| [WINTER_DATA_RESOLUTION_ROUND4_REPORT.md](reports/research-validation/WINTER_DATA_RESOLUTION_ROUND4_REPORT.md) | Winter 数据分辨率第 4 轮 |
| [WINTER_SOURCE_VALIDATION_REPORT.md](reports/research-validation/WINTER_SOURCE_VALIDATION_REPORT.md) | Winter 数据源验证 |
| [WINTER_MET_SOURCE_COMPARISON.md](reports/research-validation/WINTER_MET_SOURCE_COMPARISON.md) | 气象源对比（NCEI vs CARRA） |
| [WINTER_SUMMER_DATA_SOURCE_COMPARISON.md](reports/research-validation/WINTER_SUMMER_DATA_SOURCE_COMPARISON.md) | Winter vs Summer 数据源对比 |
| [WINTER_NCEI_LINK_FAILURE_ANALYSIS.md](reports/research-validation/WINTER_NCEI_LINK_FAILURE_ANALYSIS.md) | NCEI 链接失败分析 |
| [WINTER_TEMPORAL_COVERAGE_AUDIT.md](reports/research-validation/WINTER_TEMPORAL_COVERAGE_AUDIT.md) | Winter 时间覆盖审计 |
| [WINTER_CARRA_PLAN_B_OPERATION_GUIDE.md](reports/research-validation/WINTER_CARRA_PLAN_B_OPERATION_GUIDE.md) | CARRA 备选方案操作指南 |
| [WINTER_A_FREEZE_AUDIT_REPORT.md](reports/research-validation/WINTER_A_FREEZE_AUDIT_REPORT.md) | Winter A 冻结审计 |

### 5.7 Winter B：基线、冒烟与风险验证

| 报告 | 说明 |
|------|------|
| [WINTER_B_BASELINE_CONFIG_DECISION.md](reports/research-validation/WINTER_B_BASELINE_CONFIG_DECISION.md) | Winter B 基线配置决策 |
| [WINTER_B_SMOKE_REPORT.md](reports/research-validation/WINTER_B_SMOKE_REPORT.md) | Winter B 冒烟报告 |
| [WINTER_B_RISK_VALIDATION_REPORT.md](reports/research-validation/WINTER_B_RISK_VALIDATION_REPORT.md) | Winter B 风险验证报告 |
| [WINTER_RISK_DISTRIBUTION_AUDIT.md](reports/research-validation/WINTER_RISK_DISTRIBUTION_AUDIT.md) | Winter 风险分布审计 |

### 5.8 Winter C：验证与最终报告

| 报告 | 说明 |
|------|------|
| [WINTER_C_SMOKE_REPORT.md](reports/research-validation/WINTER_C_SMOKE_REPORT.md) | Winter C 冒烟报告 |
| [WINTER_C_ROUTE_VALIDATION_REPORT.md](reports/research-validation/WINTER_C_ROUTE_VALIDATION_REPORT.md) | Winter C 路线验证 |
| [WINTER_C_VALIDATION_FINAL_REPORT.md](reports/research-validation/WINTER_C_VALIDATION_FINAL_REPORT.md) | Winter C 验证最终报告 |

### 5.9 Winter 身份、交接与 bundle

| 报告 | 说明 |
|------|------|
| [WINTER_EXPERIMENT_IDENTITY_SETUP_REPORT.md](reports/research-validation/WINTER_EXPERIMENT_IDENTITY_SETUP_REPORT.md) | Winter 实验身份建立 |
| [WINTER_EXPERIMENT_IDENTITY_AUDIT.md](reports/research-validation/WINTER_EXPERIMENT_IDENTITY_AUDIT.md) | Winter 实验身份审计 |
| [WINTER_BUNDLE_REISSUE_AUDIT.md](reports/research-validation/WINTER_BUNDLE_REISSUE_AUDIT.md) | Winter bundle 重发审计 |
| [WINTER_BUNDLE_REISSUE_REPORT.md](reports/research-validation/WINTER_BUNDLE_REISSUE_REPORT.md) | Winter 不可变 bundle 重发报告 |
| [WINTER_HANDOFF_VALIDATION_REPORT.md](reports/research-validation/WINTER_HANDOFF_VALIDATION_REPORT.md) | Winter 正式交接验证 |
| [WINTER_FORMAL_HANDOFF_REPORT.md](reports/research-validation/WINTER_FORMAL_HANDOFF_REPORT.md) | Winter 正式交接报告 |

### 5.10 Winter 组合查看器

| 报告 | 说明 |
|------|------|
| [WINTER_COMBINED_VIEWER_INTEGRATION_REPORT.md](reports/research-validation/WINTER_COMBINED_VIEWER_INTEGRATION_REPORT.md) | Winter 组合查看器集成（最新 Winter 门禁证据） |

## 六、竞赛演示闭环报告（reports/governance/）

| 报告 | 角色 |
|--------|------|
| [FINAL_CONSISTENCY_CLOSURE_20260820.md](reports/governance/FINAL_CONSISTENCY_CLOSURE_20260820.md) | 归档的一致性闭环证据 |
| [ROOT_GOVERNANCE_AUDIT_FINAL_20260820.md](reports/governance/ROOT_GOVERNANCE_AUDIT_FINAL_20260820.md) | 归档的根治理审计证据 |
| [PHASE10_AUDIT_20260820.md](reports/governance/PHASE10_AUDIT_20260820.md) | 第 10 阶段审计 |
| [STRATEGY_B_GOVERNANCE_REFACTOR_20260820.md](reports/governance/STRATEGY_B_GOVERNANCE_REFACTOR_20260820.md) | Strategy B 治理重构 |
| [TEST_RUN_REPORT_20260820.md](reports/governance/TEST_RUN_REPORT_20260820.md) | 测试运行报告 |

## 七、历史报告（reports/，证据而非当前真相）

按主题组织的历史报告；它们是证据，不代表当前状态，不得改写为"当前"。

### 7.1 审计（reports/audits/）

| 报告 | 说明 |
|------|------|
| [CAUSAL_REPLAY_FEASIBILITY_AUDIT_20260817.md](reports/audits/CAUSAL_REPLAY_FEASIBILITY_AUDIT_20260817.md) | 因果回放可行性审计 |
| [ROUTE_GEOSPATIAL_INTEGRITY_AUDIT_20260817.md](reports/audits/ROUTE_GEOSPATIAL_INTEGRITY_AUDIT_20260817.md) | 路线地理空间完整性审计 |
| [TEMPORAL_SEMANTICS_AUDIT_20260817.md](reports/audits/TEMPORAL_SEMANTICS_AUDIT_20260817.md) | 时间语义审计 |

### 7.2 Strategy B（reports/strategy-b/）

| 报告 | 说明 |
|------|------|
| [CAUSAL_REPLAY_MVP_20260818.md](reports/strategy-b/CAUSAL_REPLAY_MVP_20260818.md) | 因果回放 MVP |
| [STRATEGY_B_PERFORMANCE_HARDENING_20260819.md](reports/strategy-b/STRATEGY_B_PERFORMANCE_HARDENING_20260819.md) | 性能加固 |
| [STRATEGY_B_SEMANTIC_HARDENING_20260818.md](reports/strategy-b/STRATEGY_B_SEMANTIC_HARDENING_20260818.md) | 语义加固 |
| [STRATEGY_B_SHIP_MOTION_SEMANTICS_20260819.md](reports/strategy-b/STRATEGY_B_SHIP_MOTION_SEMANTICS_20260819.md) | 船舶运动语义 |
| [STRATEGY_B_VIEWER_FOUNDATION_20260819.md](reports/strategy-b/STRATEGY_B_VIEWER_FOUNDATION_20260819.md) | Viewer 基础 |
| [STRATEGY_B_VIEWER_MVP_20260819.md](reports/strategy-b/STRATEGY_B_VIEWER_MVP_20260819.md) | Viewer MVP |
| [VIEWER_PRESENTATION_POLISH_20260821.md](reports/strategy-b/VIEWER_PRESENTATION_POLISH_20260821.md) | Viewer 展示打磨 |
| [VIEWER_PRODUCT_MAINLINE_20260820.md](reports/strategy-b/VIEWER_PRODUCT_MAINLINE_20260820.md) | Viewer 产品主线 |
| [VIEWER_RISK_HORIZONS_20260820.md](reports/strategy-b/VIEWER_RISK_HORIZONS_20260820.md) | Viewer 风险视界 |
| [GRID_PRESENTATION_AUDIT_20260821.md](reports/strategy-b/GRID_PRESENTATION_AUDIT_20260821.md) | 网格展示审计 |

### 7.3 决策（reports/decisions/）

| 报告 | 说明 |
|------|------|
| [D_SELECTION_EVALUATION_v2_vs_v3.md](reports/decisions/D_SELECTION_EVALUATION_v2_vs_v3.md) | D 选择评估：v2 vs v3 |

## 八、归档（archive/：被取代、废弃、治理前）

归档文档不再代表当前真相，仅作为演化证据保留。

| 类别 | 位置 | 说明 |
|----------|----------|------|
| 被取代（旧计划等） | [archive/superseded/](archive/superseded/) | 旧冲刺计划、演示状态、交付说明等 |
| 已整合的旧工程治理标准 | [archive/superseded/ENGINEERING_GOVERNANCE_STANDARD.md](archive/superseded/ENGINEERING_GOVERNANCE_STANDARD.md) | 已整合进统一规范，仅作历史审计 |
| 治理前归档 | [archive/pre-governance/](archive/pre-governance/) | 治理建立前的系统文档快照 |
| 已废弃 | [archive/deprecated/](archive/deprecated/README.md) | 当前 N/A |
| 归档映射与比对表 | [archive/归档文件映射表与全量比对表.md](archive/归档文件映射表与全量比对表.md) | 归档文件映射与全量比对 |

## 九、本地（local/，操作员专用，gitignored）

| 类别 | 位置 |
|----------|----------|
| 本地操作环境 | [local/LOCAL_OPERATOR_ENV.md](local/LOCAL_OPERATOR_ENV.md) |

## 十、子项目文档

各子项目拥有自己的 README、CHANGELOG 与文档：

| 仓库 | 路径 | 角色 |
|------|------|------|
| Contracts（合约） | ${ARCTIC_ROUTE_ROOT}/arctic_route_contracts/ | 共享合约 / schema |
| Orchestrator（编排器） | ${ARCTIC_ROUTE_ROOT}/arctic_route_orchestrator/ | A→B→C→D 根协调器 + 回放引擎 |
| A（数据） | ${ARCTIC_ROUTE_ROOT}/work_package_a/ | 环境数据采集 |
| B（风险） | ${ARCTIC_ROUTE_ROOT}/work_package_b/ | 动态风险 |
| C（规划） | ${ARCTIC_ROUTE_ROOT}/work_package_c/ | 随时间变化的规划 |
| D（展示） | ${ARCTIC_ROUTE_ROOT}/work_package_d/ | 可视化 / 查看器 |

## 十一、冲突解决顺序

1. 当前代码 + 测试（ground truth，最高优先）。
2. `current/` 规范文档（本仓库）。
3. 子项目 README。
4. 历史报告（`reports/`）。
5. 归档（`archive/`）。

规则：
- 冻结文档与当前文档冲突时，当前文档胜出。
- 历史报告与当前文档冲突时，当前文档胜出，但历史报告应携带修正说明。
- 历史报告不得被改写为"当前"；发现错误时在顶部加修正说明（见治理标准）。

## 快速入口

- 新人先读：[README.md](README.md) → 本文档 → [current/CURRENT_STATUS.md](current/CURRENT_STATUS.md) → [current/CURRENT_ROADMAP.md](current/CURRENT_ROADMAP.md)。
- 写文档或提交工程运行报告前先读：[standards/AGENT_DOCUMENTATION_RULES.md](standards/AGENT_DOCUMENTATION_RULES.md)。
- 跨包合约变更：[standards/CONTRACT_CHANGE_PROPOSAL_TEMPLATE.md](standards/CONTRACT_CHANGE_PROPOSAL_TEMPLATE.md)。
