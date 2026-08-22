---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
  - PLANNED
Document Role: CANONICAL
Scope: verified capability and gap baseline for research validation
Canonical For: what exists, what is missing, and what may be developed next
Branch: research-validation-system
Last Verified: 2026-08-23
Related Canonical Docs: CURRENT_STATUS.md, CURRENT_ROADMAP.md
---

# 研究验证缺口分析

## 判定方法（2026-08-21 23:18）

`Implemented` 表示代码/模式存在；`Validated` 需要测试或真实制品证据；`Frozen` 仅指具名基线；`Planned` 与 `Not implemented` 绝不因设计意图本身而被提升。代码/模式/配置/生产者-消费者测试优于文档，当前文档优于历史报告。

## 模块总表（2026-08-21 23:18）

| 模块 | 已有能力 | 已验证证据 | 缺口 | 建议 |
|---|---|---|---|---|
| Contracts | 标识加载器 + 所有权/变更门禁；8 个场景配置 | 19 个测试；冬季配置加载器/CLI | 未来提案负责人批准 | 每次变更套用登记册/模板 |
| A | 12 类型采集/规整化/QC/溯源、PreparedWindow、DatasetBundle.v2、精确解析器、CARRA 与冰数据接口 | RC1/RC2 summer bundles；Winter active bundle + RunContext/ExecutionSpec + exact intake-only | Winter B 尚未执行 | 固定本轮 identity，下一轮只读交给 B |
| B | 逐时确定性风险 + 合成与正式固定网格实验框架 | 16×7/31×11/60×21 上的 78 个正式帧 | `demo_unvalidated`；Winter unknown/hard policy 尚未实证；无自适应网格 | Winter formal build 前先冻结 profile 与 unknown gate |
| C | 时变 A*、12 航线发布、剖析器、BC 基准、默认关闭的有界样本 LRU | medium LRU 3 次运行中位数 65.012 s 对比关闭 76.281 s；语义摘要相等 | 无正式接入/12 航线缓存门禁；无共享/增量搜索；fine 未运行 | 跨接入、层与目标验证缓存 |
| Orchestrator | 因果重放、导航执行、进程级目标并行、预检、展示导出 | 12h 权威/继承；48h 真实制品 | 展示候选包为空 | 仅基于真实 C 制品的版本化投影 |
| D | 48h Viewer + 经纬网/标注/比例尺/网格北与保宽高比地图 | 全新 Firefox BROWSER_E2E_PASS | 无真实候选比较；溯源/不确定性视图有限 | 消费拟议制品；暴露已发布质量 |

## A 与 Winter 场景（2026-08-23 01:16 +08:00）

A 可采集并表达 12 个必需 Winter 类型，含显式 UTC 窗口、溯源与因果可见性。CARRA/Copernicus/GEBCO 源集已作为冻结的 1,212 条记录 active bundle `a-bundle-a2146dd0adbaa7db77a6beb7` 发布。其 requested/minimum horizon 均为 144 h；matching RunContext、strict ExecutionSpec 与 exact archive intake-only 已通过。因此：

- winter 数据接口：`IMPLEMENTED`；
- winter 场景配置标识：`IMPLEMENTED / UNIT_VALIDATED`；
- winter 源行：`COMPLETE / 12_OF_12`；
- winter 冻结 DatasetBundle：`FROZEN_ARTIFACT_READY`；
- winter 实验标识：`READY_FOR_B_VALIDATION`；
- winter A→B intake：`PASS`；
- winter B→C→D 验证：`NOT_RUN`。

## B 网格与科学缺口（2026-08-21 23:18）

网格生成归属 B。`TargetGridConfig.realize()` 使用固定的最大角步长与覆盖端点的 linspace。显式 RC2 Tromsø 策略得到 31×11；代码默认测试得到 16×7。C 构建匹配的 `RegularGrid`；D 渲染精确单元。Viewer 并非粗单元的根本原因。

summer 12h 审计发现全部 255 个可航水域单元为 Level 1，外加 65 个 LAND 与 21 个 DATA_UNAVAILABLE 硬单元。这是制品实际的模型/场景分布，而非 D 的阈值缺陷。更细单元可能改善空间表达，但不产生科学风险变化或校准。

首个合成空间核实验在不改变生产默认的情况下现覆盖 112/341/1260 单元。它展示了确定性输出与线性输出字节增长，但固定的 xarray 开销主导其约 24.6 ms 运行时间。它并非完整 RiskFrame 构建性能的证据。

剩余 P2 正式实验矩阵：

| 度量 | 原因 |
|---|---|
| 按网格/horizon 的 B 墙钟时间与峰值 RSS | 从端到端重放中隔离成本 |
| risk/hard/unknown 分布 | 防止可用性回归 |
| 空间混叠与海岸线一致 | 量化分辨率收益 |
| C 航线/ETA/风险/完整性 | 度量下游语义影响 |
| 配置/网格/内容摘要 | 防止跨网格缓存污染 |

## C 12 航线与性能缺口（2026-08-21 23:18）

C 的 v3 集是真实的：四固定层 × 三目标，精确 12 航线，原子发布。但每个目标调用独立的 A*。既有优化缓存几何并预计算风险数组；Orchestrator 可在受控 ProcessPool 中运行目标搜索。没有共享目标队列、Pareto 前沿、保留搜索树、D* Lite 或 LPA*。

合成组件剖析将约 92% 的包含时间归因于边遍历内的风险采样。精确 medium 运行发现 34.444% 的重复样本键；一个默认关闭的 50k LRU 以一次完整语义摘要和约 38.6 MiB 额外采样 RSS 将中位数运行时间改善 14.77%。P3 接下来应通过正式接入与全部 12 航线验证该精确样本适配器。搜索标签不得跨目标权重、层、朝向/时间状态、风险修订或代次复用，除非有新的正确性证明。验收要求全部 12 航线业务摘要与串行基线相等，且测得墙钟时间/RSS 改善。

## C→D 航线候选缺口（2026-08-21 23:18）

静态 RC1 路径证明 D 可消费完整的 v3 集。当前重放产品路径则不能：

```text
C FourLayerRoutePlanSet.v3 (12 条真实航线)
  -> Orchestrator 重放接受一条权威导航航线
  -> replay_viewer_export 发布 route_candidates 为 NOT_PUBLISHED
  -> D 仅如实显示权威/演进航线
```

48h bundle 中的 19 次修订是随时间发生的决策，并非目标候选。所需提案字段包含决策时间、层、目标、航线/层集 ID、几何、距离、ETA、成本、风险/置信度指标、风险源 ID、代次/修订以及 selected/authoritative 状态。

## 环境层就绪度（2026-08-21 23:18）

B 在内部使用多个 A 变量，但当前重放 Viewer bundle 发布总风险、硬可用性、底图、航线/导航与摘要——并非每个单元的完整海冰/风/浪/流场，或可信的贡献分解。D 不得读取 A 私有制品或重建 B。环境层在 Orchestrator 具备经审阅的展示契约与展示就绪数据前保持 `PLANNED`。

## 接口冻结提案（2026-08-21 23:18）

| Contract | Owner | Current version | Freeze decision | Proposed work |
|---|---|---|---|---|
| scenario/corridor/vessel/RunContext | contracts | current package schemas | FROZEN_COMPATIBLE | new winter identity only |
| A→B environment bundle | A | `a.dataset-bundle.v2` + PreparedWindow | FROZEN_COMPATIBLE | no breaking change |
| B→C risk frame | B producer / C schema consumer | `bc.risk-frame.v2` | FROZEN_COMPATIBLE | adaptive grid proposal separate/versioned |
| C route plan | C | `RoutePlan.v2`, `FourLayerRoutePlanSet.v3` | FROZEN_COMPATIBLE | performance internal if digests equal |
| C→D candidate presentation | Orchestrator projection; C semantics; D consumer | v1 empty status | GAP / backward compatible | versioned candidate sets |
| Viewer bundle | Orchestrator producer / D owner | `replay.viewer-bundle.v1` | FROZEN_COMPATIBLE | optional versioned fields, fail closed |

本次启动未变更任何契约。提案在实施前需要负责人批准、模式、fixtures、生产者/消费者测试、迁移与回滚。

## 多人协作建议（2026-08-21 23:18）

- B 负责人：冬季基线消费与固定网格基准；不得编辑 C/D。
- C 负责人：在不变输出契约下进行剖析/遍历缓存实验；不得编辑 B 模型。
- D 负责人：针对冻结或拟议展示 fixtures 的专业/研究 UI；不得读取 A/B/C。
- Orchestrator 负责人：仅做候选/环境投影与兼容性测试。
- 集成负责人：批准模式提案、钉住制品标识、一次运行一个重型工作负载并比较语义摘要。

目录级写所有权与集成顺序现已在 [`DEVELOPMENT_OWNERSHIP.md`](DEVELOPMENT_OWNERSHIP.md) 中规范化；契约所有权在 [`CONTRACT_OWNERSHIP_REGISTRY.md`](reference/CONTRACT_OWNERSHIP_REGISTRY.md) 中规范化。
