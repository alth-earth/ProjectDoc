---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
Document Role: CANONICAL
Scope: cross-repository contract ownership, version, compatibility, and change gates
Canonical For: who may change each interface and how consumers must handle it
Branch: research-validation-system
Last Verified: 2026-08-23
---

# 契约所有权登记册

## 登记规则（2026-08-22 00:02）

本登记册记录已实施的接口。标记为 `FROZEN_COMPATIBLE` 的行并不冻结实现内部，而是冻结既有字段的可见含义与失败行为。`DRAFT` 提案不是契约，不得被生产代码消费。

每个契约有唯一的模式负责人、一个或多个生产者、显式消费者、机器可读 fixtures 以及生产者-消费者测试。已发布制品不可变：修正以新标识/修订创建，而非覆盖先前发布。

## 所有权登记（2026-08-22 00:02）

| 契约 | 模式/语义负责人 | 生产者 | 消费者 | 当前版本 | 状态 | 兼容性边界 |
|---|---|---|---|---|---|---|
| 共享走廊/场景/船舶标识 | `arctic_route_contracts` | contracts loaders/configs | A、B、C、Orchestrator、D 元数据 | package schemas、scenario.v2 | FROZEN_COMPATIBLE | 允许新场景 ID/配置；既有标识含义不得变更 |
| Run Context | `arctic_route_contracts` | 共享上下文构建器 | A、B、C、Orchestrator | RunContext v2 | FROZEN_COMPATIBLE | UTC 与场景/走廊/船舶/代次标识保持精确 |
| A→B Prepared Window | A | `work_package_a` | B | `PreparedWindow` 公共 API | FROZEN_COMPATIBLE | B 不得检查 A 的 SQLite/raw/私有目录 |
| A→B 数据集 Bundle | A（含共享标识校验） | `work_package_a` | B、Orchestrator 校验 | `a.dataset-bundle.v2` | FROZEN_COMPATIBLE | 不可变载荷/边车标识；缺失数据保持显式 |
| B 输入信封 | B | `work_package_b` 适配器 | B 风险服务 | `BInputEnvelope` | ACTIVE_INTERNAL | 可在 B 内部演进，同时保留 A 公共与 RiskFrame 边界 |
| B→C 风险帧 | B 拥有发布与风险语义；C 为必需兼容性审阅者 | `work_package_b` | C、Orchestrator 展示投影 | `bc.risk-frame.v2` | FROZEN_COMPATIBLE | 风险等级、硬掩膜/原因、置信度、速度因子、网格与时间语义不变 |
| B 已提交风险窗口 | B | `work_package_b` 存储 | C 接入、重放 | 当前 committed-window API | FROZEN_COMPATIBLE | 原子发布；无陈旧代次或越窗回退 |
| C 航线计划 | C | `work_package_c` | Orchestrator、D 静态回退 | `cd.route-plan.v2` | FROZEN_COMPATIBLE | C 仍为航线、速度、ETA、目标与成本的负责人 |
| C 分层航线计划 | C | `work_package_c` | Orchestrator、D 静态加载器 | `cd.four-layer-route-plan-set.v3` | FROZEN_COMPATIBLE | 精确四层 × 三目标；原子完整集发布 |
| C→D 航线状态展示 | Orchestrator 投影；C 拥有航线语义 | Orchestrator | D Viewer | `replay.viewer-bundle.v1` 中当前航线状态 | FROZEN_COMPATIBLE | authoritative/pending/superseded 与采用顺序不得重新解释 |
| 候选航线展示 | Orchestrator 投影；C 拥有候选语义 | Orchestrator | D Viewer | `presentation.route-candidates.v1` | IMPLEMENTED_EMPTY | `NOT_PUBLISHED` + 空列表在真实几何/指标导出前为权威 |
| 风险叠加展示 | Orchestrator 投影；B 拥有风险语义 | Orchestrator | D Viewer | `presentation.risk-overlay.v1` | FROZEN_COMPATIBLE | 当前/horizon 有效性与不可用失败关闭行为保留 |
| Viewer bundle | Orchestrator 生产者；D 拥有运行时消费 | Orchestrator | D Viewer | `replay.viewer-bundle.v1` | FROZEN_COMPATIBLE | 允许可选增量包；必需 v1 字段与单时钟语义保留 |

`cd.route-plan.v3` 是 `cd.four-layer-route-plan-set.v3` 内的单路线 schema，不是
ExecutionSpec 可选择的顶层 planning contract；v3 顶层必须使用 four-layer set identity。

## 不可变制品要求（2026-08-22 00:02）

- 标识包含模式版本，以及适用的场景、代次、修订、时间与内容摘要。
- 已发布对象只读。修正获得新修订或新制品标识，并保留到被取代对象的溯源。
- 消费者拒绝不兼容版本、标识不匹配、部分原子组、未知必填字段或时间覆盖不足。
- 缺失/未知/不可用绝不变成零、安全、最近已知回退或臆造的航线候选。

## 向后兼容性（2026-08-22 00:02）

兼容变更是增量的可选字段/包，其缺失保留先前行为。重命名/删除字段、变更单位、极性、时间含义、目标含义、失败行为、基数、原子性或标识计算即便 JSON 仍可解析也属破坏性。

消费者可同时支持新旧版本，但在无法解释某发布时必须显式呈现 unsupported/unavailable 状态。

## 破坏性变更流程（2026-08-22 00:02）

1. 依据 [CONTRACT_CHANGE_PROPOSAL_TEMPLATE.md](../../standards/CONTRACT_CHANGE_PROPOSAL_TEMPLATE.md) 创建提案。
2. 指明负责人、受影响生产者/消费者、精确语义增量，以及为何增量扩展不足。
3. 在集成前添加旧/新 fixtures、模式校验、生产者测试、消费者测试、兼容性测试与失败测试。
4. 定义制品迁移、回滚与冻结基线回归。
5. 取得每个受影响边界的负责人批准；`DRAFT` 非批准。
6. 先实施生产者，再实施选择加入的消费者支持。不得覆盖旧制品。
7. 运行聚焦集成与语义摘要比较；重型重放仅在阶段退出门禁运行。

## 开放提案（2026-08-22 00:02）

| 拟议领域 | 状态 | 必需负责人审阅 |
|---|---|---|
| 冬季实验标识 | FORMAL HANDOFF COMPLETE；READY_FOR_B_VALIDATION | contracts + A + Orchestrator 接入负责人 |
| B 网格实验剖面 | EXPERIMENTAL，无正式 RiskFrame 变更 | B + C 兼容性审阅者 |
| 自适应/非均匀网格契约 | PLANNED | B + C + Orchestrator |
| [含真实几何/指标的候选航线展示](../proposals/ROUTE_PRESENTATION_CONTRACT_PROPOSAL.md) | DRAFT / PLANNED；当前载荷仍为 NOT_PUBLISHED | C + Orchestrator + D |
| 环境因素展示包 | PLANNED | A/B 语义负责人 + Orchestrator + D |
