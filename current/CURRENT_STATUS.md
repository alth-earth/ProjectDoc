---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
  - PLANNED
Document Role: CANONICAL
Scope: whole-project current state
Canonical For: current phase, capability evidence, blockers, and ownership
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Research Validation System Current Status

## 第二阶段加速结果（2026-08-22 00:24）

| Workstream | Current state | Evidence |
|---|---|---|
| P0 Contract Registry | IMPLEMENTED / DOCUMENT_VALIDATED | ownership/version/status registry, proposal template, development ownership matrix |
| P1 Winter configuration | IMPLEMENTED / UNIT_VALIDATED | new `scenario.v2` identity; contracts 19 PASS |
| P1 Winter data/artifact | BLOCKED_BY_DATASET | no matching 12-type source bundle; no winter artifact fabricated |
| P2 B fixed-grid experiment | EXPERIMENTAL / UNIT_VALIDATED | baseline/medium/fine profiles, deterministic spatial-kernel benchmark, B 60 non-integration PASS |
| P3 C component profiling | EXPERIMENTAL / UNIT_VALIDATED | real planner components on labelled synthetic fixture; C 145 non-integration PASS |
| P3 edge geometry cache identity | IMPLEMENTED / UNIT_VALIDATED | cache key now includes sample count; focused regression included |
| P4 professional navigation aids | IMPLEMENTED / BROWSER_E2E_PASS | Firefox: graticule, coordinate labels, scale bar, grid north, independent toggle |

No core contract version, A acquisition implementation, B risk formula/level
policy, C search algorithm/route semantics, Orchestrator export, frozen artifact,
or 48h replay was changed.

## 当前阶段（2026-08-21 23:18）

项目已从 Competition Demo Freeze 转入 **Research Validation System
Enhancement Phase**。冻结演示基线保留在 `demo-engineering`，当前开发只在
`research-validation-system` 进行。这个阶段先冻结接口事实和验证口径，再开展
B/C/D 并行研究；不把规划中的冬季场景、自适应网格或候选路线展示写成已有能力。

| Branch | Meaning | Status |
|---|---|---|
| `main` | RC1 baseline | FROZEN |
| `rc2-development` | RC2 baseline | FROZEN |
| `demo-engineering` | competition demo baseline | FROZEN |
| `research-validation-system` | research validation enhancement | ACTIVE |

`/root/my_project` 是多个仓库的工作区，当前没有 root Git。各子仓库分别维护自己的
`research-validation-system` 分支。

## 当前真实架构（2026-08-21 23:18）

| Module | Research-stage role | Runtime boundary |
|---|---|---|
| A | Environmental Data Acquisition | 发布 `PreparedWindow` / `a.dataset-bundle.v2` 与 provenance |
| B | Risk Assessment and Forecast | 消费 A 公共 bundle，发布 `bc.risk-frame.v2` |
| C | Risk-aware Navigation Decision | 消费 B risk frame，发布 route plan / layered route set |
| D | Visualization and Validation Platform | 只消费已发布 presentation artifact；唯一 Viewer runtime owner |
| Orchestrator | Pipeline / Artifact / Presentation Adapter | 编排 A→B→C，执行 replay，验证并投影 presentation bundle |

```text
A PreparedWindow / DatasetBundle.v2
  -> B BInputEnvelope / bc.risk-frame.v2
  -> C RiskSourcePlanningIngress
  -> RoutePlan.v2 or FourLayerRoutePlanSet.v3
  -> Orchestrator replay/presentation export
  -> replay.viewer-bundle.v1
  -> D Viewer
```

## 能力与证据等级（2026-08-21 23:18）

| Capability | Implementation | Validation | Current qualification |
|---|---|---|---|
| A 12-type public data bundle | IMPLEMENTED | AUTHORITATIVE_PASS | 夏季 RC1/RC2 制品；winter artifact 未建立 |
| B hourly deterministic risk frame | IMPLEMENTED | AUTHORITATIVE_PASS | 模型仍为 `demo_unvalidated`，不是科学标定结论 |
| B fixed target grid | IMPLEMENTED | UNIT/ARTIFACT_PASS | RC2 显式 31×11；代码默认配置可为 16×7 |
| B adaptive grid | NOT_IMPLEMENTED | NOT_RUN | 研究计划，不得隐式改变 C regular-grid contract |
| C three objectives | IMPLEMENTED | AUTHORITATIVE_PASS | fastest / low_risk / recommended |
| C four layers × three objectives | IMPLEMENTED | AUTHORITATIVE_PASS | `FourLayerRoutePlanSet.v3` 明确验证 12 路线 |
| C causal replay planning | IMPLEMENTED | AUTHORITATIVE_PASS | 12h determinism inherited；48h product artifact verified |
| D presentation Viewer | IMPLEMENTED | BROWSER_E2E_PASS | Firefox；单 Simulation Clock；artifact driven |
| 48h replay Viewer | IMPLEMENTED | BROWSER_E2E_PASS | 49 snapshots、2881 minute states、49 risk frames |
| C route candidates in replay Viewer | NOT_IMPLEMENTED | NOT_PUBLISHED | bundle 明确 `status=NOT_PUBLISHED`, `candidates=[]` |
| Winter scenario configuration | IMPLEMENTED | UNIT_PASS | config skeleton only; formal dataset remains blocked |
| Winter A→B→C→D artifact | NOT_IMPLEMENTED | BLOCKED_BY_DATASET | no winter source/bundle evidence |
| B fixed-grid experiment harness | IMPLEMENTED | UNIT_PASS / EXPERIMENTAL | synthetic spatial kernel, not formal RiskFrame build |
| C component profiler | IMPLEMENTED | UNIT_PASS / EXPERIMENTAL | synthetic fixture through real planner components |
| D professional navigation aids | IMPLEMENTED | BROWSER_E2E_PASS | bundle metadata only; canonical transform/aspect preserved |

## 冻结语义（2026-08-21 23:18）

- A→B 只通过公共 `PreparedWindow` / `DatasetBundle.v2` 和匹配的
  `RunContext`；B 不扫描 A 私有 cache、SQLite 或 raw 目录。
- B→C 以 `bc.risk-frame.v2` 为正式边界；unknown fail closed，
  `DATA_UNAVAILABLE != safe`。
- C 拥有最终路线、速度、ETA 和重规划决策；D 不重新计算。
- `REPLAN_DECIDED != REPLAN_ADOPTED`，pending route 不提前替换 authoritative
  route，completed track append-only。
- D 是唯一 Viewer runtime owner；Orchestrator 只拥有 replay 与 presentation
  adapter/export。
- 当前正规网格是 rectilinear regular grid。Adaptive Grid 在 contract proposal
  通过前只能作为隔离实验。

## 当前事实缺口（2026-08-21 23:18）

1. Contract ownership registry 已建立；尚待各 owner 对未来 candidate/adaptive
   proposal 逐项审批，registry 本身不等于 proposal 批准。
2. C 已有 12-route 输出，但 replay export 没有发布候选 geometry/metrics；不能把
   19 个时间修订版误称为 19 个候选。
3. 有冬季采集能力，没有冬季 scenario + 12-type frozen bundle + B/C/D 验证链。
4. B 规则模型未标定；已有合成固定网格 kernel 基线，但正式 A→B build 的独立
   latency/RSS 与下游 C 差异仍未测；adaptive grid 未实现。
5. C 已有可重复 component profiler，显示 risk sampling 嵌套于 edge traversal 是
   首要热点；共享搜索、bounded memoization 与 incremental replanning 未实现。
6. D 已建立基础专业导航辅助层；route candidate compare 与研究 provenance/
   uncertainty 交互仍取决于真实 presentation contract。

详细依据见
[RESEARCH_VALIDATION_GAP_ANALYSIS.md](RESEARCH_VALIDATION_GAP_ANALYSIS.md)。

## 当前阻塞与风险（2026-08-21 23:18）

| Risk | State | Handling |
|---|---|---|
| 多人并行前 contract 所有权不清 | CONTROLLED | registry/template/目录 ownership 已建立；breaking proposal 仍需 owner approval |
| winter artifact 不存在 | BLOCKED_BY_DATASET | config 已验证；下一步先 source availability probe |
| B grid policy 与 C regular-grid 假设耦合 | EXPERIMENTAL BASELINE | synthetic fixed-grid kernel 完成；formal bounded build/C comparison 待做 |
| C candidate 未投影到 replay bundle | PLANNED | backward-compatible presentation proposal |
| 当前 demo baseline 回退 | CONTROLLED | frozen branch/artifact 不改；研究 artifact 使用新 identity |
| B Murmansk default-grid integration expectation | OPEN FINDING | 未筛选 B suite 在 allowed-region endpoint mapping 失败；不在本轮改配置语义 |

## 本轮验证边界（2026-08-21 23:18）

本轮没有运行 48h replay、heavy integration 或新的 determinism twin-run。
Contracts 19 PASS；B 60 个 non-integration tests PASS（8 integration deselected）；
C 145 个 non-integration tests PASS；D 63 PASS；三个改动仓库 Ruff clean，D JS
syntax PASS。Firefox 使用现有 48h artifact 重跑展示回归：required resources 200，
console errors/warnings 0；10:00/10:30 船位与 13:30/15:00 adoption 状态未回退。
12h authoritative determinism 仍为继承证据。
