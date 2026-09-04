---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
  - PLANNED
Document Role: CANONICAL
Scope: phase history and architecture decisions relevant to research validation
Canonical For: why current boundaries and roadmap priorities exist
Branch: research-validation-system
Last Verified: 2026-09-04 22:17 +08:00
---

# Research Validation Decisions

> 本文按批次保留历史决策原文；其中关于候选发布、动态回放和 sidecar 的旧状态不覆盖
> 2026-09-01 当前事实，当前状态以 [`CURRENT_STATUS.md`](../CURRENT_STATUS.md)、
> [`CURRENT_ROADMAP.md`](../CURRENT_ROADMAP.md) 和本轮运行报告为准。

## 第1批：RC1 / RC2 冻结与可恢复基线（2026-08-21 23:18）

**背景。** RC1 建立了 Murmansk–Dikson 12-type formal 数据、B 风险、C 四层三目标和
D 静态制品链；RC2 建立了 Tromsø 走廊的完整性、修复和 Viewer 基线。

**问题。** 研究阶段若直接覆盖这些配置或 artifact，将失去回归参照。

**分析。** 冻结分支、scenario identity、bundle digest 和 route/risk semantic digest 是
可恢复性的共同基础。

**决策。** `main`、`rc2-development`、`demo-engineering` 分别作为 RC1、RC2、比赛演示
冻结基线；研究只在 `research-validation-system` 产生新 identity 和新 artifact。

**影响。** 冻结内容可被读取和回归，不在本阶段修改或迁移。

## 第2批：Strategy B causal replay（2026-08-21 23:18）

**背景。** 静态事后重算无法证明“当时可见的数据如何导致当时决策”。

**问题。** risk、route、ship 和 replan 必须共享因果时间边界。

**分析。** 已实现的 replay 把 `knowledge_as_of`、`simulation_time`、risk revision、plan
revision 和 navigation state 分开，并以 semantic digest 验证业务确定性。

**决策。** Strategy B same-vessel causal replay 继续作为研究主线；Strategy A 仅保留为
frozen retrospective fallback。`REPLAN_DECIDED` 与 `REPLAN_ADOPTED` 继续分离。

**影响。** 新算法必须先通过时间因果和 deterministic artifact 门禁，不能只给单次图像。

## 第3批：48h replay extension（2026-08-21 23:18）

**背景。** 12h Viewer 不足以展示长期风险 horizon 和多次 route evolution。

**问题。** 前端循环时间或复制 12h timeline 会伪造业务数据。

**分析。** 现有 48h artifact 是真实 timeline-driven replay，含 49 snapshots、2881 minute
states、49 risk frames 和连续的 route revision/event sequence。

**决策。** 48h artifact 作为 Competition Demo 的冻结产品证据；研究阶段继承但不在文档
治理轮重跑。未来扩展必须由 backend replay 生成，不由 D 伪造。

**影响。** 48h Firefox E2E 是 inherited evidence，不等于本轮重验。

## 第4批：C route candidates 与 Viewer 发布缺口（2026-08-21 23:18）

**背景。** C 的 `FourLayerRoutePlanSet.v3` 强制四层、每层三目标，共 12 路线；RC1
initial/replanned artifact 已验证。

**问题。** 当前 replay Viewer bundle 明确输出
`presentation.route-candidates.v1`、`status=NOT_PUBLISHED`、空 candidates。Viewer 中的
route revisions 是时间演化，不是同一决策时刻的候选集合。

**分析。** 直接在 D 把 revision 命名为 fastest/low-risk/recommended 会制造不存在的语义。

**决策。** C 的 12-route 能力记为 `IMPLEMENTED + AUTHORITATIVE_PASS`；C→D candidate
presentation 记为 `NOT_IMPLEMENTED / NOT_PUBLISHED`。先设计 backward-compatible
presentation proposal，Orchestrator 只投影，D 只展示。

**影响。** P0 完成前不开发多路线 Viewer 产品功能。

## 第5批：风险网格与夏季分布（2026-08-21 23:18）

**背景。** Viewer 曾表现为粗栅格，夏季风险大部分为 Level 1。

**问题。** 需要区分 A source resolution、B target grid、C planning grid 和 D rendering。

**分析。** A GEBCO 约 0.05°；RC2 B 显式政策为 0.375°×1.25°，实际 Tromsø 网格
31×11、约 0.3667°×1.2°；C 继承 B regular grid；D 按原 cell 绘制。12h 风险审计的
255 个可导航 water cells 全为 Level 1，另有 65 LAND + 21 DATA_UNAVAILABLE；这是真实
B artifact/model/scenario 分布，不是 Viewer threshold bug。

**决策。** 不在 D 平滑或重分类风险。P2 先做固定网格与性能/路线对照，再决定是否提出
adaptive grid contract；B 仍标记 `demo_unvalidated`。

**影响。** 视觉粗糙的主要瓶颈在 B target grid，但更细网格不自动解决科学标定问题。

## 第6批：Winter Scenario（2026-08-21 23:18）

**背景。** 夏季场景风险变化不足以支持季节性研究结论。

**问题。** A 已有 sea-ice concentration/drift/thickness/type/edge 的采集、派生和公共
bundle 接口，但仓库没有当前正式冬季 scenario + 12-type artifact 证据。

**分析。** “接口能采”不等于“冬季能力已验证”；旧 9-type 长窗和 July/August 配置
不能冒充 winter baseline。

**决策。** Winter Scenario 标记 `PLANNED`。先提新 scenario identity，再建立真实
provenance-complete A bundle；B/C/D 后续消费，不修改旧 scenario 或旧模型结果。

**影响。** P1 的第一验收点属于 contracts/A data，不属于 B 算法或 D 展示。

## 第7批：多人并行前接口冻结（2026-08-21 23:18）

**背景。** A/B/C/D 将由多人并行开发，而当前 shared、repo-local 与 presentation
contracts 分散。

**问题。** 未明确 owner/version/compatibility 时，Adaptive Grid、C 性能和 D candidate
展示容易相互破坏。

**分析。** 当前 AB/BC/CD 是 artifact/cache handoff 与局部受控并行，不是统一常驻 worker
流水线，也没有需要本轮改造的 reader-writer runtime。

**决策。** P0 先建立 contract registry 和 proposal gate；不做 ABCD 多进程同步改造。

**影响。** 后续每个 owner 修改 producer 和 tests，跨包字段只通过经审批的新版本扩展。

## 第8批：Winter Experiment Identity Fail-closed（2026-08-22 22:24 +08:00）

**背景。** Winter 12 类 source records 与 `a.dataset-bundle.v2` 已冻结，需要建立 matching
`RunContext.v2` 与 Orchestrator `ExecutionSpec.v1` 后才能进入 B validation。

**问题。** 冻结 bundle 的 requested window 为 144 h，但
`minimum_required_end=2026-02-20T12Z`，只覆盖 132 h；scenario 在
`2026-02-21T00Z` 结束。官方 RunContext 生成器按现有 contract 拒绝该不一致。

**分析。** 手写 RunContext、缩短 scenario 或向 strict ExecutionSpec 添加 Winter-only
字段都会绕过既有接口门禁。直接改 frozen bundle 还会破坏其 content-addressed identity。

**决策。** 当前 handoff 保持 `BLOCKED_BY_BUNDLE_MINIMUM_HORIZON`。不创建孤立
ExecutionSpec，不修改 frozen bundle，不修改 contract。下一轮由 A owner 发布一个使用
同一已验证 source record set、但 minimum horizon 为 144 h 的新 immutable bundle
identity，再通过官方生成器和 intake-only 门禁。

**影响。** B/C/D 继续 `NOT_STARTED`；当前 bundle 保留为 A acquisition evidence，但不能
作为该 144 h scenario 的正式 A→B experiment identity。ExecutionSpec 不承载 bundle SHA、
Git 版本或 B/C 配置路径，这些继续由 RunContext、CLI 参数和 experiment report 分工记录。

## 第9批：Winter A 不可变 Bundle 重发（2026-08-23 00:48 +08:00）

**背景。** 旧 bundle 的 1,212 条真实 source records 已通过 coverage/provenance，但其
minimum horizon 只有 132 小时，无法绑定 144 小时 scenario。

**问题。** 直接修改旧 JSON、缩短 scenario 或伪造尾部 coverage 都会破坏不可变制品和
fail-closed handoff。

**分析。** A 正式 producer 支持独立的 requested/minimum horizon 参数。使用同一 records
与 source snapshots，并显式传入 144 小时 minimum，可发布一个新的 content-addressed
identity；不需要重新下载，也不改变 `a.dataset-bundle.v2`。

**决策。** 发布 active bundle `a-bundle-a2146dd0adbaa7db77a6beb7`，其
`requested_end=minimum_required_end=2026-02-21T00Z`。旧 bundle
`a-bundle-bd8957c4f10c7c73f395de23` 保留不变，作为 superseded 历史 A evidence。官方
RunContext generator 只做内存态接受性验证，本轮不持久化 RunContext/ExecutionSpec，
不运行 intake。

**影响。** `A_TO_B_FORMAL_HANDOFF` 从 minimum-horizon blocker 前进到
`WAITING_FOR_RUN_CONTEXT`；B/C/D 仍为 `NOT_STARTED`。下一门槛是 Formal Handoff，
不是 Winter B 执行。

## 第10批：Winter Formal Handoff 与 Cutoff 接口收敛（2026-08-23 01:16 +08:00）

**背景。** Active 144 小时 bundle 已可生成 RunContext，需要发布正式 experiment identity
并执行 intake-only。

**问题。** 官方 RunContext/ExecutionSpec schema 与 binding 均通过后，Orchestrator intake
仍以 `as_of_time == max(record.issue_time)` 拒绝 Winter retrospective bundle。共享 time
contract 的不变量实际为 `max(issue_time) <= as_of_time`；logical cutoff 可晚于最后一条记录。

**分析。** Bundle 已以 exact record IDs、checksums、source snapshots 和 content digest 锁定
可见集合。要求 cutoff 与 max issue 相等不会增加可复现性，反而拒绝合法 retrospective
identity；但任何 future-issued record 仍必须 fail closed。

**决策。** 用官方 CLI 发布 matching `RunContext.v2`，复用 strict
`orchestrator.execution-spec.v1`，并把 intake 门禁收敛为
`max(issue_time) <= as_of_time`。不修改 bundle、schema 或 B/C/D 算法。Exact archive
intake-only PASS 后，状态提升为 `READY_FOR_B_VALIDATION`。

**影响。** Winter B 可以在下一轮消费固定 identity；B/C/D 仍为 `NOT_STARTED`。B→C 的
unknown/hard policy 是下一 gate 的 conditional blocker，不能由 C 或 D 兜底。

## 第11批：Risk Calibration Shadow 边界（2026-08-23 22:01 +08:00）

**背景。** Winter finite risk 均值为 `0.119016`，93.069778% 映射为 L1；现行
`demo_unvalidated_rule_baseline.v2` 缺少航行行动或事故结果标定。

**问题。** 按展示效果改变 threshold 会把分布颜色与科学语义混为一谈；单场景 quantile
又会强制产生高等级，无法形成跨场景绝对含义。

**分析。** 当前 `risk_score` 只能作为 weighted normalized hazard index。正式 L1–L5 是
equal-width engineering discretization，不是 probability、validated severity 或 operational
action level。已有 C route metrics 来自同一 RiskWindow，不能作为独立 calibration labels。

**决策。** 冻结正式 B formula、weights、threshold 和 RiskFrame；所有候选先进入独立
research-only sidecar，不馈入 C/D。统计 quantile 只允许 `EXECUTED_DESCRIPTIVE`；Expert、
Physics、Ordinal 方法在规则、component attribution、物理限值和 labels 齐备前保持
`BLOCKED`。下一阶段主目标优先定义为 `operational_action_level`，并按独立
ScenarioRunGroup 做外层验证。

**影响。** Shadow infrastructure 可用于复现实验设计和证据门禁，但当前 Winter 单场景结果
仍是 `DIAGNOSTIC_ONLY_NOT_EXTERNAL_CALIBRATION`，不得批准正式 threshold 变化。

## 第13批：Winter v4 路线连续性与展示平滑边界（2026-09-04 22:17 +08:00）

**背景。** v3 浏览器证据暴露了首段路线偏离权威航点、revision 切换时船位大跳跃和候选
比较线与正式运行线混淆。用户同时质疑 D 的平滑绘制是否把路线写死。

**审计结论。** 原始 R1 的前八个航点经度固定为 `18.4`、纬度递增，北向拓扑正确；D 中没有
Winter 经纬度或 route ID 常量。当前 `route_visual_smoothing.js` 是通用、数据驱动的
screen-space 二次 Bezier paint layer，读取每个制品 candidate 的 `geometry.coordinates`。
20 CSS px 圆角、40% trim 上限等只是可测试的展示策略；该层不读取或改变 motion、ETA、风险、
运行 candidate 或 adoption。formal active path 与船位只来自 C `motion_samples`。历史
`route_smoothing.js` 和 research sidecar 不在默认 Viewer 加载路径。

**决策。** C producer 默认关闭 AnyAngle shortcut，并把所有 raw waypoint 保留为 formal
motion anchor；修正 adaptive trust 的 candidate↔raw 距离方向。D 增加 2 km waypoint binding、
25 km formal/timeline continuity gate，候选 overlay 永不替换 active formal path，并在真实
`REPLAN_ADOPTED` 事件时间更新 active revision。保持所有海陆、unknown、时间、走廊、操纵性、
自交、最大速度、ETA 和风险非劣化硬门禁，不用展示平滑掩盖规划问题。

**证据。** 不重新下载 A/B 数据生成不可变 v4；R2–R6 均为身份绑定 `CURVE` adoption，最大
相邻 adoption 位置差约 0.710 km，超过 25 km 的瞬移为 false，终态 `ARRIVED`。v4 assembly 为
`winter-viewer-sha256-f3113a19243bce88f712717ad91bddd9d3c76d93c6d84ac3c57e930496dff1ad`；
bundle/checksums SHA-256 分别为 `f993ac113ac7280e9378710fdc84a825338ebd6ea4b5193ce8679aeb5c3b114a` /
`92ca583e52d41d277d22750631f083b0de798cb5ce8f9b105ef7a1d0123f7d33`。v3 已撤回到外部
`artifacts/invalid/`，但源码、交付压缩包和历史结论保留；当前 AppImage 已重建以包含 D
连续性修正。

**后果。** v4 是 `retrospective_post_hoc_dynamic_projection` 的工程展示，不是 strict causal、
实时预测、导航级或实船资格。后续若改变平滑策略，必须先验证其输入来自当前制品并证明
`authoritative_semantics_unchanged=true`；不得新增第二条运行几何来源。

## 第12批：Winter v3 动态重规划与 Viewer 发布边界（2026-09-04 19:17 +08:00）

**背景。** v2 Viewer 制品虽已可导入，但运行路线仍可能显示 `RAW_PASSTHROUGH`，且缺少
完整的动态 replay、revision、motion 身份绑定。用户要求在不重新下载数据、不重建 AppImage
的前提下获得可审计的动态重规划展示。

**决策。** 复用 2026-02-15 Winter A Bundle、145 帧 RiskWindow 和同身份 Risk Explanation，
使用 C 的 `winter_motion_reserve_5pct`（规划速度预留 5%，不修改船模最大速度或环境可用
速度）及 `winter_dynamic_replay`（最小间隔 6 小时、路线收益阈值 1%、风险迟滞 1%、最大
风险回退容差 0%）重新生成 C plan/motion，并由 Orchestrator 以显式
`--planner-name`/`--replanning-name` 完成全窗口回放。新建不可变
`winter-rebuilt-20260215-viewer-package-v3`，不覆盖 v2；通过当前 AppImage 的外部
`inbox → 重新扫描 → ready` 流程导入。

**证据。** 回放窗口为 2026-02-15T00:00Z→2026-02-21T00:00Z，6 小时 tick、25 snapshots、
6 revisions；存在 5 组真实 `REPLAN_DECIDED → REPLAN_ADOPTED → ROUTE_CHANGED`，终态
`ARRIVED` 且 `pending_route=null`。三个持久 worker 的 summary 为
`requested/effective/max=3/3/3`、36 planning calls、108 objective tasks。v3 初始三个
full-voyage 候选及全部实际采用路线为正式 `CURVE`；R1–R6 六套 candidate-motion transport
均已绑定，R3 executable/fastest `RAW` 仅作为未采用比较层，保留真实
`minimum_radius_exceeded` 原因。v3 assembly 为
`winter-viewer-sha256-1a50c77c012285404d96d3de1cdb0cd563214371911c6ae0c066c3280f5e8afd`，
`bundle.json` SHA-256 为 `3772a5d621bd058ef58d6b8aadc0254a15f3bd44cc027b7e10c4c63ceacf58ed`，
`checksums.json` SHA-256 为 `a96c61138f089a962e21dbaa481521db3213376f2bcbcb90aafe8ce2cb2627ff`；包共 20 个
白名单文件，`publish-summary.json` 也纳入其余 19 个文件的 checksum。

**替代方案。** 不采用以下方案：沿用 v2 的 raw fallback；在 D 伪造 replan/event 或把比较
层 RAW 改标为 CURVE；放宽海陆、unknown、时间覆盖、走廊、操纵性、自交、最大速度、ETA 或
风险非劣化门禁；重新下载已有 A 数据；重建 AppImage 以掩盖外部制品问题；把 retrospective
reanalysis 改名为 causal 或实时预测。

**理由。** C 的 formal motion 与 Switch Gate 必须继续是 producer；D 只能消费并投影版本化
资源。命名配置和 digest 写入 replay manifest，可证明 worker 使用同一参数；延迟采用事件保留
中边决策与无跳跃船位；仅实际采用路线必须取得 CURVE，未采用比较层保留 RAW 才符合事实。

**后果。** 当前 v3 具备工程级动态 Viewer 回放和身份闭合证据，但仍标记为
`retrospective_post_hoc_dynamic_projection`，不具备严格因果、实时预测、导航级或实船资格。
AppImage 二进制保持不变；v2 外部 ready 目录已退役到
`artifacts/invalid/winter-rebuilt-20260215-viewer-package-v2-retired-20260904`，v2 原始输出
与历史摘要保留作审计证据。截图必须在修正后的 v3 上重新生成并绑定 assembly、bundle 和
checksums 摘要；严格 causal Winter window 仍是下一 gate。
