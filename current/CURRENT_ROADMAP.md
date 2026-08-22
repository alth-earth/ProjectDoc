---
Overall Status: ACTIVE
Content Status:
  - IN_PROGRESS
  - PLANNED
Document Role: CANONICAL
Scope: research validation roadmap
Canonical For: next work, phase gates, and dependency order
Branch: research-validation-system
Last Verified: 2026-08-23
Supersedes: competition-demo Viewer Product Mainline roadmap
---

# Research Validation System Roadmap

## 阶段目标（2026-08-21 23:18）

当前目标是把已冻结的比赛演示链提升为可重复、可比较、可审计的研究验证系统。
顺序是 **先接口，后场景，再算法实验，最后专业展示**。所有研究产物必须使用新
identity，不覆盖 RC1/RC2/demo frozen artifact。

## P0 接口冻结与多人开发门禁（2026-08-21 23:18）

状态：`REGISTRY_BASELINE_COMPLETED`。Ownership registry、change-proposal
template 和 development ownership 已建立；具体 breaking proposal 仍需逐项审批。

1. 建立 A→B、B→C、C route plan、C→D candidate presentation、Viewer bundle
   的 ownership/version/producer/consumer registry。
2. 把既有接口标为 `FROZEN_COMPATIBLE`，把 proposed extension 标为
   `DRAFT`；禁止直接改旧 schema 的既有字段语义。
3. 审批已建立的 `presentation.route-candidates` backward-compatible proposal，明确
   planning layer、objective、geometry、metrics、selection 和 provenance。
4. 建立 B Adaptive Grid proposal 的 compatibility gate：grid identity、parent
   mapping、C regular-grid 可消费性和 fail-closed 重采样证据。
5. 多人协作时每个 owner 只改自己的 producer 和 tests；消费者先接受旧版和新
   proposal 的 empty/unsupported 状态，再接入真实新 artifact。

退出条件：接口 registry 经 A/B/C/D/Orchestrator owner 审阅；proposal 有 schema、
fixtures、compatibility tests 和 rollback path。

## P1 Winter Scenario（2026-08-23 00:48 +08:00）

状态：`FROZEN_ARTIFACT_READY / WAITING_FOR_RUN_CONTEXT`。

1. CARRA、Copernicus 与 GEBCO 的 12 类真实数据及 1,212-record Winter source set 已冻结；
   不再把数据获取列为当前 blocker。
2. A 已发布新的 immutable bundle `a-bundle-a2146dd0adbaa7db77a6beb7`，其
   `requested_end=minimum_required_end=2026-02-21T00Z`；旧 132 小时 minimum bundle
   保留为 superseded 历史 evidence，未覆盖或删除。
3. 新 bundle 已通过 parse/digest/coverage/provenance/doctor，并被官方 RunContext
   generator 在内存中接受；本轮按边界没有持久化 RunContext 或 ExecutionSpec。
4. 下一轮创建 matching RunContext 与 strict ExecutionSpec，运行 Orchestrator
   intake-only；通过后才标记 `READY_FOR_B_VALIDATION`。
5. B 随后在已批准的显式 grid/model config 上先做 input/grid/unknown/risk distribution 基线；
   不改 risk formula 或 level policy。C/D 只在上游 acceptance 后接入。

退出条件：matching RunContext、ExecutionSpec 与 Orchestrator intake 全部 PASS；随后 B
risk distribution、C route integrity、D artifact presentation 依次提供独立证据。

## P2 B Adaptive Grid（2026-08-21 23:18）

状态：`FORMAL_FIXED_GRID_EXPERIMENT_COMPLETED / BC_BASELINE_MEDIUM_COMPLETED`。

已完成 baseline 16×7、medium 31×11、fine 60×21 的真实 B formal build；
baseline/medium 已进入真实 C recommended search。默认生产配置未变。B 节点从
112 增至 341 时 C planning time 从 10.51 s 增至 75.00 s；fine 只记录 1,260
节点容量，不在无显式预算时启动规划。

先运行固定网格对照：16×7 default、31×11 RC2 和至少一个研究候选。记录 B latency、
RSS、hard/unknown 比例、risk aliasing、C route/ETA 差异和 planner failure。只有对照证据
证明固定网格不足后，才开发隔离 adaptive-grid sidecar；不得直接替换
`bc.risk-frame.v2` 的 regular-grid 语义。

退出条件：新 grid policy 有新 version/digest、可逆 parent mapping、跨包 compatibility
tests 和性能收益证据。

## P3 C Performance Optimization（2026-08-21 23:18）

状态：`EXACT_SAMPLE_PROFILE + BOUNDED_LRU_EXPERIMENT_VALIDATED`。

真实 medium B frame search 记录 705,469 次 sample 请求，其中 242,992 次精确重复。
50k default-off LRU 的 3-run median 从 76.281 s 降至 65.012 s（14.77%），额外 sampled
RSS 约 38.6 MiB，完整规划语义摘要不变。下一步进入 committed ingress、三目标和四层
equality gate，不直接引入共享搜索。

保留现有 3-worker objective-level ProcessPool 基线。依次评估：重复搜索与 cache
profiling、同 layer 多目标共享 immutable inputs、shared-search feasibility，以及
incremental replanning proposal。任何优化都必须通过 serial/parallel semantic digest
equivalence、RSS 上限和 determinism tests；禁止多个 heavy replay 并行。

## P4 D Professional Navigation Visualization（2026-08-21 23:18）

状态：`FOUNDATION_BROWSER_E2E_PASS`。

1. 接入真实 route candidate presentation contract，支持 layer/objective compare；空候选
   继续明确 NOT_PUBLISHED。
2. 增加 artifact identity、provenance、grid/resolution、data quality、uncertainty 和
   comparison 视图；不以视觉插值掩盖缺测。
3. 评估专业导航图层和环境 contributor，但只消费 Orchestrator 已发布数据。
4. 保留 Presentation / Engineering Debug 双模式和单 Simulation Clock。

经纬网格、坐标标签、haversine 中心纬度比例尺、grid-north 指示和独立 layer
toggle 已通过 Firefox。后续仍以真实 candidate/provenance/environment presentation
contract 为前置条件。

## 全局验收与资源规则（2026-08-21 23:18）

- 文档修改不触发 heavy replay；代码修改先 lint/unit/focused integration。
- 48h/full replay 只在阶段退出时串行运行，并记录 wall time、peak RSS、artifact digest。
- Windows 宿主物理剩余空间在宿主核验前一律 `UNKNOWN`；WSL `df -h /` 不作为宿主
  磁盘证据。
- 代理失败先检查环境；只对单条命令临时直连，不修改全局代理。
- 不 push、merge、rebase、reset；冻结分支和 frozen artifact 不修改。
