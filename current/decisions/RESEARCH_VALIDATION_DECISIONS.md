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
Last Verified: 2026-08-21
---

# Research Validation Decisions

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
