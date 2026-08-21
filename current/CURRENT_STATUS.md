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
Last Verified: 2026-08-21
---

# Research Validation System Current Status

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
| Winter scenario | NOT_IMPLEMENTED | NOT_RUN | A 有通用冰数据接口，但无冬季正式 artifact 证据 |

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

1. shared contracts、B/C repo-local contracts 和 Orchestrator presentation schemas
   分散，尚无统一 ownership/version index。
2. C 已有 12-route 输出，但 replay export 没有发布候选 geometry/metrics；不能把
   19 个时间修订版误称为 19 个候选。
3. 有冬季采集能力，没有冬季 scenario + 12-type frozen bundle + B/C/D 验证链。
4. B 规则模型未标定；没有 B 独立 grid/horizon 耗时和 RSS 基线；adaptive grid
   未实现。
5. C 已建立 objective-level 受控并行，但 replay 规划仍是主要耗时；共享搜索和
   incremental replanning 尚未实现。
6. D 已适合演示和验证，但 route candidate compare、专业导航图层和研究证据交互
   尚未建立。

详细依据见
[RESEARCH_VALIDATION_GAP_ANALYSIS.md](RESEARCH_VALIDATION_GAP_ANALYSIS.md)。

## 当前阻塞与风险（2026-08-21 23:18）

| Risk | State | Handling |
|---|---|---|
| 多人并行前 contract 所有权不清 | BLOCKED for parallel implementation | P0 建立 registry 与 version proposal |
| winter artifact 不存在 | BLOCKED for winter validation | P1 建 scenario/data acceptance，不复用夏季数据冒充 |
| B grid policy 与 C regular-grid 假设耦合 | PLANNED | 固定网格对照先行，adaptive sidecar 后行 |
| C candidate 未投影到 replay bundle | PLANNED | backward-compatible presentation proposal |
| 当前 demo baseline 回退 | CONTROLLED | frozen branch/artifact 不改；研究 artifact 使用新 identity |

## 本轮验证边界（2026-08-21 23:18）

本轮是文档治理和只读能力审查，没有修改 A/B/C/D/Orchestrator 业务代码，也没有
运行 48h replay、heavy integration 或新的 determinism twin-run。既有 Firefox E2E、
48h artifact 和 12h authoritative determinism 均为继承证据，不写成当轮重跑。
