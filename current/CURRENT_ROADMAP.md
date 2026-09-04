---
Overall Status: ACTIVE
Content Status:
  - IN_PROGRESS
  - PLANNED
Document Role: CANONICAL
Scope: research validation roadmap
Canonical For: next work, phase gates, and dependency order
Branch: research-validation-system
Last Verified: 2026-09-04 19:17 +08:00
Supersedes: competition-demo Viewer Product Mainline roadmap
---

# Research Validation System Roadmap

## 阶段目标（2026-08-21 23:18）

当前目标是把已冻结的比赛演示链提升为可重复、可比较、可审计的研究验证系统。
顺序是 **先接口，后场景，再算法实验，最后专业展示**。所有研究产物必须使用新
identity，不覆盖 RC1/RC2/demo frozen artifact。

## P0 接口冻结与多人开发门禁（2026-08-21 23:18）

状态：`REGISTRY_BASELINE_COMPLETED / ROUTE_CANDIDATE_EXTENSION_ACCEPTED`。Ownership
registry、change-proposal template 和 development ownership 已建立；
`presentation.route-candidates.v1` 已通过真实 Winter 12-route producer/consumer 验收，
其他 breaking proposal 仍需逐项审批。

1. 建立 A→B、B→C、C route plan、C→D candidate presentation、Viewer bundle
   的 ownership/version/producer/consumer registry。
2. 把既有接口标为 `FROZEN_COMPATIBLE`，把 proposed extension 标为
   `DRAFT`；禁止直接改旧 schema 的既有字段语义。
3. `presentation.route-candidates.v1` backward-compatible proposal 已实施并验收：明确
   planning layer、objective、geometry、metrics、selection、provenance 与空包 fallback。
4. 建立 B Adaptive Grid proposal 的 compatibility gate：grid identity、parent
   mapping、C regular-grid 可消费性和 fail-closed 重采样证据。
5. 多人协作时每个 owner 只改自己的 producer 和 tests；消费者先接受旧版和新
   proposal 的 empty/unsupported 状态，再接入真实新 artifact。

退出条件：接口 registry 经 A/B/C/D/Orchestrator owner 审阅；proposal 有 schema、
fixtures、compatibility tests 和 rollback path。

## P1 Winter Scenario（2026-08-23 10:20 +08:00）

状态：`WINTER_A_B_C_COMPLETED / D_DYNAMIC_RETROSPECTIVE_REAL_E2E_PASS / CAUSAL_REPLAY_PENDING`。

1. CARRA、Copernicus 与 GEBCO 的 12 类真实数据及 1,212-record Winter source set 已冻结；
   不再把数据获取列为当前 blocker。
2. A 已发布新的 immutable bundle `a-bundle-a2146dd0adbaa7db77a6beb7`，其
   `requested_end=minimum_required_end=2026-02-21T00Z`；旧 132 小时 minimum bundle
   保留为 superseded 历史 evidence，未覆盖或删除。
3. Matching `RunContext.v2` 与 strict `ExecutionSpec.v1` 已发布并通过 schema、identity 与
   binding 验证；Orchestrator exact archive intake-only PASS。
4. intake 的 logical cutoff 门禁已与共享 contract 对齐为
   `max(issue_time) <= as_of_time`；仍 fail closed，未改变 records 或 schema。
5. B 首轮已在 medium 显式 grid/model config 上生成 145 个 formal hourly RiskFrame，并完成
   unknown/hard 与 Summer/Winter 分布审计；不改 risk formula 或 level policy。
6. C 已消费精确 committed window，发布 4 层 × 3 目标的 12-route v3 artifact；
   endpoint、schema、codec 与 12-route integrity 全部 PASS。
7. C→D candidate sidecar 已通过 schema 与真实 artifact consumer 验收；同一 Winter
   identity 的 combined risk/route/ETA-simulation package 与 Firefox Browser E2E 已通过。
8. 原始冻结身份的真实 `retrospective_dynamic_replay` 已发布完整到达态：25 个 snapshots、
   119 个事件、9 个 revision 资源（每版 4×3=12），并在默认 Viewer 展示 8 轮
   pending/adopted/superseded 与终态 `ARRIVED`；该模式保留 issue time，明确是事后动态投影。
9. C RC2 objective-level 三 worker 已接回正式 Orchestrator 初始/重规划路径；真实运行
   `max_parallel_tasks=3`、36 次 planning call、`tasks_submitted=108`，tick/layer/B/adoption 仍串行。

P1 formal handoff、B 风险分布、C 路线、D combined visualization 与事后动态回放门槛均已
满足。当前 navigation timeline 由真实 replay 源和 C waypoint ETA 延展组成，但整体仍是
`retrospective_post_hoc_dynamic_projection`，不升级为 causal replay。下一 gate 是取得
issue-time 可追溯的 Winter causal window；在此之前不要把该包标为导航级或冻结生产基线。

## P1.1 Winter v3 动态重规划制品（2026-09-04 19:17 +08:00）

状态：`COMPLETED / REAL_RETROSPECTIVE_E2E_PASS / CAUSAL_PENDING`。

在不重新下载 Winter A 数据、不覆盖 v2、也不重建 AppImage 的条件下，使用新的 C/Orchestrator
配置重新完成 2026-02-15T00:00Z→2026-02-21T00:00Z 全窗口回放，并发布不可变
`winter-rebuilt-20260215-viewer-package-v3`。C planner profile 为
`winter_motion_reserve_5pct`（`operational_speed_reserve_fraction=0.05`，只影响规划 ETA），
replanning profile 为 `winter_dynamic_replay`（6h interval、1% gain、1% hysteresis、最大
风险回退 0%）；Orchestrator CLI 通过 `--planner-name`/`--replanning-name` 显式记录和传播
配置摘要，worker 不加载默认配置。

- 回放以 6 小时 tick 产生 25 snapshots、6 个 plan revisions；真实事件包含 5 组
  `REPLAN_DECIDED → REPLAN_ADOPTED → ROUTE_CHANGED`，终态 `ARRIVED`，最终
  `pending_route=null`。3 worker 的 summary 为 `requested/effective/max=3/3/3`、36 次
  planning calls、108 个 objective tasks。
- v3 初始 full-voyage 三个运行候选与实际采用路线均为 `CURVE`；R1–R6 六套
  candidate-motion transport 已全部绑定；R3 的 executable/fastest `RAW` 只保留为未采用
  比较层及真实 `minimum_radius_exceeded` 证据。海陆、unknown、时间覆盖、走廊、操纵性、自交、
  最大速度、ETA 和风险非劣化门禁保持不变。
- 包 assembly 为 `winter-viewer-sha256-1a50c77c012285404d96d3de1cdb0cd563214371911c6ae0c066c3280f5e8afd`；
  `bundle.json` SHA-256 为 `3772a5d621bd058ef58d6b8aadc0254a15f3bd44cc027b7e10c4c63ceacf58ed`，
  `checksums.json` SHA-256 为 `a96c61138f089a962e21dbaa481521db3213376f2bcbcb90aafe8ce2cb2627ff`；20 个白名单
  文件中含 `publish-summary.json`，覆盖其余 19 个文件的 checksum。
  包扫描、严格 JSON 和全量 checksum 通过，未打包 D 的 HTML/CSS/JS。
- v3 已经当前 AppImage 的外部 `artifacts/inbox → 重新扫描 → ready` 流程验证；v2 从
  外部 ready 退役到 `invalid/winter-rebuilt-20260215-viewer-package-v2-retired-20260904`，
  原始 v2 输出与历史摘要仍保留。AppImage 本身保持原二进制，Windows EXE 仍由 Windows
  团队执行原生构建和验收。

本阶段的 v3 结论只覆盖工程回放与 Viewer 展示能力。下一 gate 仍是 issue-time 完整可追溯的
Winter causal window；在该门禁通过前，不得把 post-hoc 投影标记为 causal、实时预测、导航
级或实船资格。

## P1.5 B Risk Calibration Protocol（2026-08-23 20:45 +08:00）

状态：`RESEARCH_AUDIT_COMPLETED / SCIENTIFIC_CALIBRATION_NOT_ESTABLISHED`。

当前 `demo_unvalidated` risk 是 11 个 normalized component 的 weighted sum；固定
`0.2/0.4/0.6/0.8` 仅是 equal-width engineering policy。Winter 31,543 个 finite cells 中
93.069778% 为 L1，证明 level resolution 与当前 score distribution 不匹配，但不能单独证明
threshold 错误或允许按展示效果重标。

下一 gate：

1. 明确 level 对应 expert action、physics severity、ordinal outcome 或 probability 中的哪一种；
2. 建立跨场景、跨时间块、跨 corridor/vessel 的 immutable calibration/validation dataset；
3. 由 B 以 backward-compatible shadow sidecar 发布 normalized components 与 additive
   contribution，禁止 D 反算；
4. 比较现行 baseline、expert+physics constraints、descriptive percentile 与有标签
   outcome calibration；只有 evidence review 通过后才提交新 config/version proposal；
5. 旧 weights、thresholds、RiskFrame 与 Winter/Summer artifacts 保持冻结。

退出条件：目标语义、gold/weak labels、split policy、评价指标、OOD/fail-closed gate 和 rollback
方案均获批准，并有至少两个独立场景的 shadow result；本阶段不以“颜色更丰富”为验收条件。

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

状态：`EXACT_SAMPLE_PROFILE + BOUNDED_LRU_EXPERIMENT_VALIDATED + RC2_PARALLEL_FORMAL_PATH_RESTORED`。

真实 medium B frame search 记录 705,469 次 sample 请求，其中 242,992 次精确重复。
50k default-off LRU 的 3-run median 从 76.281 s 降至 65.012 s（14.77%），额外 sampled
RSS 约 38.6 MiB，完整规划语义摘要不变。下一步进入 committed ingress、三目标和四层
equality gate，不直接引入共享搜索。

现已把 3-worker objective-level ProcessPool 接回正式 C initial/replan execution；真实
Winter replay report 记录 requested/effective/max=3、36 次 planning call、108 tasks 和 worker provenance。并行
池以单次 C planning invocation 为生命周期，tick/layer/B/adoption 仍串行。继续评估：重复搜索与 cache
profiling、同 layer 多目标共享 immutable inputs、shared-search feasibility，以及
incremental replanning proposal。任何优化都必须通过 serial/parallel semantic digest
equivalence、RSS 上限和 determinism tests；禁止多个 heavy replay 并行。

## P4 D Professional Navigation Visualization（2026-08-21 23:18）

状态：`WINTER_COMBINED_REAL_E2E_PASS / DYNAMIC_RETROSPECTIVE_REPLAY_PUBLISHED / SUMMER_FALLBACK_PRESERVED`。

1. 已接入真实 `presentation.route-candidates.v1`，支持四层 selector、三目标 compare、
   canonical metrics、candidate geometry 与 display-only highlight；空候选继续明确
   `SINGLE_ROUTE_FALLBACK`。
2. 已增加 run/scenario、RiskFrame schema、grid/frame/candidate-set metadata；DatasetBundle
   identity 等未发布字段明确显示 `not published`，不从私有 artifact 推断。
3. `risk-explanation.v1` optional consumer 与点击格点面板已通过测试；只显示 producer 字段
   并在缺失/invalid/mismatch 时失败关闭。B 同次公式 trace、immutable artifact/manifest 与
   Orchestrator SHA/identity transport 已在另一 Winter holdout 身份闭合；当前恢复的原始冻结
   身份因精确 A source trace 已退役而不带 sidecar，D 诚实显示 unavailable，不生成
   contributor，也不影响基础风险/路线/仿真。
4. 保留 Research Validation / Operational Replay / Engineering Debug 三态和单一
   Simulation Clock。

经纬网格、坐标标签、haversine 中心纬度比例尺、grid-north 指示、独立 layer toggle 与
344px/528px 风险时域布局已通过 Firefox。同一 Winter identity 的 145-frame risk、每个
revision 的 12-route candidates、真实 replay events、ETA-driven navigation simulation
已由 Orchestrator 组装并通过 Research View Browser E2E；现有 Summer frozen fallback
继续保留。当前动态包明确是 retrospective，不得升级为 causal replay。explanation
consumer 仍可选且失败关闭；当前原始冻结身份没有 sidecar，其他身份的真实 sidecar 和
synthetic fixture 都不能提升本包的 producer 成熟度或被跨身份复用。

## 全局验收与资源规则（2026-08-21 23:18）

- 文档修改不触发 heavy replay；代码修改先 lint/unit/focused integration。
- 48h/full replay 只在阶段退出时串行运行，并记录 wall time、peak RSS、artifact digest。
- Windows 宿主物理剩余空间在宿主核验前一律 `UNKNOWN`；WSL `df -h /` 不作为宿主
  磁盘证据。
- 代理失败先检查环境；只对单条命令临时直连，不修改全局代理。
- 不 push、merge、rebase、reset；冻结分支和 frozen artifact 不修改。
