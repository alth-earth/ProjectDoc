---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
  - PLANNED
Document Role: CANONICAL
Applicability: CURRENT
Scope: whole-project current state
Canonical For: current phase, capability evidence, blockers, and ownership
Branch: research-validation-system
Last Verified: 2026-09-04 19:59 +08:00
---

# 研究验证系统当前状态

## 2026-09-04 19:17 +08:00 Winter 动态重规划 Viewer v3 收口

2026-02-15 Winter 窗口已在不重新下载 A 数据、不过度放宽安全门禁的前提下，重新执行
C 规划、正式 motion 和 Orchestrator 动态回放，并发布不可变 Viewer 制品
`winter-rebuilt-20260215-viewer-package-v3`。v2 未被覆盖；v1 不在当前外部制品库中。
本包的展示模式为 `retrospective_post_hoc_dynamic_projection`：它保留真实 source
`issue_time`，用于事后动态投影，不是历史因果回放、实时预测、导航级或实船资格。

- 身份保持闭合：A `a-bundle-fbbbfbb6e14bec5162408046`（bundle digest
  `fbbbfbb6e14bec5162408046781cd64eb6659f22b0b07d6005b0acf70e473bba`）、RiskWindow
  `risk-window-sha256-86bdb614c5137ba9ef9129713b5575423e97bac3522bea9ff89f45f879a03ecb`、
  场景 `tromso_isfjorden_february_2026_research_v1` 与同次 replay 均一致。
- C 使用命名配置 `winter_motion_reserve_5pct`（规划 ETA 速度预留 5%，只作用于规划）和
  `winter_dynamic_replay`（6 小时最小间隔、1% route gain、1% hysteresis、最大风险回退
  容差 0%）；Orchestrator CLI 显式传播配置名/摘要，worker 不再偷偷加载默认配置。
- 完整回放为 2026-02-15T00:00Z→2026-02-21T00:00Z、6 小时 tick、25 snapshots、6 个
  plan revisions、5 组 `REPLAN_DECIDED → REPLAN_ADOPTED → ROUTE_CHANGED`，终态
  `ARRIVED` 且 `pending_route=null`。3 个持久 worker 的可审计 summary 为
  `requested/effective/max=3/3/3`、36 次 planning call、108 个 objective tasks。
- v3 初始三个 full-voyage candidate 和每一条实际采用路线均为正式 `CURVE` motion；R1–R6
  六套 candidate-motion transport 均已随包绑定。R3 的 executable/fastest `RAW` 记录只作为
  未采用的比较层，保留真实 `minimum_radius_exceeded` 失败原因，不被伪装为曲线或当前运行
  路线。硬掩膜、unknown fail-closed、时间覆盖、走廊、操纵性、自交、最大船速、ETA 和风险
  非劣化门禁未放宽。
- v3 assembly 为
  `winter-viewer-sha256-1a50c77c012285404d96d3de1cdb0cd563214371911c6ae0c066c3280f5e8afd`；
  `bundle.json` SHA-256 为
  `3772a5d621bd058ef58d6b8aadc0254a15f3bd44cc027b7e10c4c63ceacf58ed`，
  `checksums.json` SHA-256 为
  `a96c61138f089a962e21dbaa481521db3213376f2bcbcb90aafe8ce2cb2627ff`。包共 20 个文件，含
  `publish-summary.json`，checksum 覆盖其余 19 个文件；仅含白名单数据/manifest/preflight，
  不复制 D 的 HTML/CSS/JS；扫描、严格 JSON、allowlist 与全量 checksum 通过，第二次发布逐
  文件确定性比对也通过。
- 当前 AppImage 未重建，仍使用
  `arctic_route_control_center/release/Arctic_Route_Control_Center-x86_64.AppImage`；v3
  已通过当前 AppImage 的 `artifacts/inbox → 重新扫描 → 提升为 ready` 流程进入
  `/root/.local/share/arctic-route-control-center/artifacts/ready/`。旧 v2 已移入
  `artifacts/invalid/winter-rebuilt-20260215-viewer-package-v2-retired-20260904/`，其原始
  D 输出与历史摘要保留作审计证据。
- 截图已在最终 v3 二进制上重新生成并绑定最终 assembly、bundle/checksums 摘要，目录为
  `output/playwright/winter-rebuilt-20260215-current-standard-v3/`；浏览器回归确认运行后
  路线层、三目标筛选、候选高亮仍可操作，锁定只保护实际运行 candidate/motion/ETA。Risk
  Explanation 保留真实 `PARTIAL/COMPLETE/UNAVAILABLE` 语义。

该 v3 只更新外部 Viewer 制品和 replay 证据，不改变 D `app.js`，也不把 C 的研究 motion
模型提升为导航资格。严格 causal Winter 版本仍需 issue-time 可追溯数据窗口；未完成该门禁
前不得将 v3 标记为 causal 或生产冻结基线。

## 2026-09-03 六包控制中心与 Linux AppImage 发行

已新增根级整合项目 `arctic_route_control_center`，不搬移 A/B/C/D 业务所有权。发行入口为
本地 C/S Web 控制面：启动器保留命令台、后端只监听 loopback，并自动打开默认浏览器。

- Contracts：界面可只读查看 Corridor、Scenario、Vessel；正式任务只开放 6 个显式
  release allowlist 场景。research、RC2 smoke、winter development、holdout 场景不进入
  可执行下拉框；Contracts 当前配置总数已由测试从过时的 8 修正为 10。
- A：界面展示 15 个注册类型，但只允许 12 个正式必需类型和 2 个合同可选类型；
  `vessel_traffic` 保持诊断模拟并在 UI 禁用。共享场景唯一决定时间和模式，frozen template
  只接受显式 UTC materialization anchor；不会再错误叠加 `--start/--end/--mode`。
- 凭据与独立 CARRA：设置格式保持 v1 向后兼容，同时保存外部 `.env.copernicus` 与
  `.cdsapirc` 两个绝对路径，分别服务 Marine 与 CDS/CARRA，互不覆盖且不读取/回显内容。
  正式 `a_carra_acquire`/`acquire-carra` 只接受已登记 East domain 走廊、UTC 3 小时边界、
  最长 216 小时及风场/温度/能见度；只发布 A manifest/来源证据，不创建 Contracts 场景，
  也不把 retrospective reanalysis 冒充实时预测或 `frozen_forecast`。一个真实 3 小时
  temperature 周期完成下载、解析、发布和二次缓存复用；原始缓存与来源快照摘要一致。
- Orchestrator：长任务使用白名单 job spec 和独立 worker；所有用户输入文件必须位于外部
  `data_root`。统一 Viewer publisher 已改为公开包入口，补齐 dynamic replay、motion candidate
  set、formal motion 强制、strict JSON、完整文件/checksum/preflight/12-route/身份复核、最终目录
  原子发布，以及冻结程序内部 exporter dispatch。sidecar 派生改为通用包内函数，不再预创建
  一个下游必然拒绝的输出目录。
- D：仍是只读 consumer。`artifacts/inbox` 中未完成制品只识别、不提供给 Viewer；通过
  Schema、checksum、PUBLISHED、12 routes、preflight 和 formal motion 后才可原子提升到
  `artifacts/ready`。随包默认只包含当前 `work_package_d/viewer/checksums.json` 所列冻结制品
  和普通 Web 资源，不包含重复的 self-contained HTML 或历史 output/backup。运行锁定现在
  只保护实际 candidate、运动来源、ETA 与“设为运行路线”；路线层、三目标显隐和候选卡片
  高亮仍可操作，且浏览器回归证明它们不改变同一时刻的船位或运行路线身份。
- 发行裁剪：不包含 A 23GB 数据、凭据、RC1/RC2/demo-engineering 分支内容、legacy CNN、
  Torch/safetensors、B calibration/grid 实验、C synthetic/legacy CLI 与 experimental cache。
  可写配置、数据、任务、日志、缓存和新制品全部位于 AppImage 外部。
- Linux x86_64 AppImage 已在 WSL Ubuntu 24.04 构建，产物
  `arctic_route_control_center/release/Arctic_Route_Control_Center-x86_64.AppImage`，SHA256
  `cc9fd06f100e777cc43d7e0aac69b6de2662530eeba3946a6d23a7ad49e4acbf`，大小
  `184113656` bytes（后续重建会改变）；
  冻结自检确认七个包 metadata、ecCodes 2.48.0、当前 12-route Viewer、真实 A worker、
  Orchestrator stage/exporter 内部入口和 HTTP 端点可用。构建来源另以实际源码树摘要记录，
  PyInstaller 的 `direct_url.json`/`uv_cache.json` 已从发行物移除；最终 AppImage 解包扫描
  27047 个文件无凭据、原始数据、缓存、未授权实验构件或构建机绝对路径。
  由于构建主机 glibc 2.39，广泛旧 Linux 兼容发布仍应在 Ubuntu 22.04 基线上复建。
- Windows x64 未在 WSL 交叉构建；整合项目已交付原生 Windows PowerShell build/verify、
  ecCodes DLL/definitions 门禁、中文说明和团队 AI 提示词。只有在干净 Windows x64 机器完成
  EXE 自检与 loopback/worker 验收后，才能登记 Windows PASS。
- 当前控制中心 `28 passed`、A 完整 `make check` `216 passed`、D `124 passed`、
  Orchestrator Viewer/exporter 定向回归 `35 passed`，各自 Ruff PASS。A 的 causal replay
  测试对本机历史 manifest 采用 fail-closed 断言，`ready_ticks=0` 不再被错误当作测试失败。
  冻结 AppImage 的双凭据
  设置、CARRA catalog、控制中心 API、制品库与默认 D Viewer 已经真实 Chromium 冒烟。

能力边界不变：当前默认包是 retrospective dynamic research replay，不是 strict causal、
实船标定或导航资格。C formal motion producer 仍传递依赖 research smoothing 源码；首版裁剪
发行只消费已有 formal motion 制品，不承诺在发行包内从零生成新的 motion。

## 2026-09-02 原始冻结身份恢复与到达态最终收口

2026-09-01 的 3-snapshot/v7 与后续 holdout/v13 是排障中间包；它们误把另一数据身份设为
默认，造成风险覆盖、12 路线集合和 selected route 与 2026-08-31 结果不同。当前默认已经
恢复为原始冻结身份：

- identity：scenario `tromso_isfjorden_february_2026_research_v1`、DatasetBundle
  `a-bundle-a2146dd0adbaa7db77a6beb7`、RiskWindow
  `risk-window-sha256-b5bed6bb48893e32620710e8c765dc60ec37a2fc384f0c49014b92f0a1c056b2`；
  初始 layer-set 为 `layer-set-sha256-4f70866a4a1532c21101a378c63e643563459da7864dd2b93c1d457b4c97d404`，
  selected route 为 `route-v3-sha256-d2afafc7ad94780e8064d9fb99eb2e68976753dfa575663db87e14272e7d0b53`；
- replay：`winter-original-frozen-dynamic-v1`，25 snapshots、9 个不可变 plan revision、
  119 events；`REPLAN_DECIDED/REPLAN_ADOPTED/ROUTE_CHANGED` 各 8 次，终态 `ARRIVED`、
  pending 为空；每版均为四层×三目标=12 条真实路线；
- Viewer：assembly
  `winter-viewer-sha256-a375b431ed7c431487300988a7dc6c298cbecaf3a8e77ec4bc1371cf6be894e7`，
  145 个 RiskFrame、8,641 个分钟采样、9 个 candidate set、9 个 motion set；
- motion：正式参数 `max_trim_fraction=0.49`、`sample_spacing_m=250.0`。R1–R4 为
  `CURVE`；R5–R7 因 `integrated_risk_increased` 回退，R8–R9 因几何条件回退。R1
  full-voyage 为 982 样本、最小曲率半径约 7,464 m、最大偏离约 723 m，曲线约比 raw
  RoutePlan 短 2.17 km。6:00 snapshot 中的旧 revision 是 event overlay 问题，不是 B 样条
  未运行；采用时刻现直接由真实 event 覆盖；
- execution：RC2 objective-level 三核仍在正式 initial/replan 路径生效，报告为
  `requested/effective/max=3/3/3`、36 planning calls、108 tasks；tick、四层 barrier、B 和
  adoption gate 保持串行；
- explanation：当前原始冻结 RiskWindow 不带 sidecar。其精确 A source record 已在
  2026-08-26 detided-retirement 中物理退役，无法从最终 RiskFrame 反推同次公式 trace；
  不能错配后续 holdout sidecar，也不能伪造 contributor。因此 `Explanation unavailable`
  是诚实降级，不影响 RiskFrame、路线或仿真；
- Viewer 行为：待采用、已替代、当前路段均由 event/revision/formal motion 驱动；当前路段
  与 route-polyline 开关解耦；completed track 追加到 22 个权威 waypoint 并在到达后保留；
  风险格只在 basemap bbox 内绘制；风险时域 344/528 px 均为 145 ticks、8 px 最小 tick、
  绿色均值/黄色最大值和横向滚动。

当前回归：C `736 passed`、Orchestrator `145 passed`，另 formal integration
`2 passed, 1 warning`（1009.42 秒、退出码 0）、D unit `107 passed`；三仓所改文件定向
Ruff 通过，C/O 全仓 Ruff 各被无关既有脚本格式问题阻挡。真实浏览器逐 revision、
到达态、三目标独立选择、原始折线工程开关、completed-track、console=0 与 344/528 px
布局均通过。
这些仍是工程研究仿真证据，不是 strict causal replay、实船标定或导航资格。

## 2026-09-03 冬季重建与可解释 viewer 包（2026-09-03 09:09 +08:00）

2026-09-02 对 2026-02-15 冬季窗口执行了合规重建，产出**全新身份的正式可解释制品**，
替代上一节 "Explanation unavailable" 的诚实降级状态（旧 `a-bundle-a2146dd0…` 的
ocean_current 使用 detided 后备数据，其精确 A source record 已随 2026-08-26 detided
退役物理删除，无法重建同次 B formula trace）。

- 采集合规：`winter_window_acquisition.py --require-total-current` 对
  2026-02-15T00Z..2026-02-21T00Z 全窗口重新采集。ocean_current 145 帧全部为
  `current_component=total`、`tide_included=true`、来源
  `ARCTIC_ANALYSISFORECAST_PHY_TIDE_002_015`（TOPAZ 含潮总流），无 detided fallback
  （`source_fallback_reason=None`）。CARRA 三类型 49 帧/类、海冰 5 类与 water_level 145
  帧、wave 49 帧、land_sea_mask static 全部完整覆盖窗口。数据根
  `.runtime/winter-rebuild-20260215/data`（新目录，A 正式 data 根未动）。
- 新身份（无法复现旧 `a2146dd0` digest，属全新 bundle）：
  - DatasetBundle `a-bundle-fbbbfbb6e14bec5162408046`（digest
    `fbbbfbb6…473bba`，1,212 记录）；
  - RunContext `run-bd3c3ba5-015c-4953-97a2-c7e3cfbefc01`（config_digest 按 bundle
    身份重算，`5258a2e8…`）；
  - RiskWindow `risk-window-sha256-86bdb614c5137ba9ef9129713b5575423e97bac3522bea9ff89f45f879a03ecb`
    （145 帧，unknown_navigable_nodes=0）；B 以
    `build_window_with_explanation_trace` 同次构建并发布 explanation。
  - plan-set（12 路线）、route-candidates
    `route-candidates-sha256-df488dcc…`（selected
    `route-v3-sha256-e677def9…`）、route-motion-set
    `route-motion-set-sha256-32fe1c26…` + candidate-set。
- explanation 恢复：`risk-explanation.v1` artifact
  `risk-explanation-sha256-66bd366e4b3179880b67d8c601c4e48c6e4c50c7e3dbebe8807b97fab03b913a`
  + manifest（绑定 86bdb614 窗口，artifact_sha256 实测一致）；viewer bundle 已嵌入
  `risk_explanation` 与 `risk_explanation_transport`（status PUBLISHED）。逐帧逐格状态
  为源数据缺测的可解释结果。
- Viewer 包：`work_package_d/output/winter-rebuilt-20260215-viewer-package-v1/`
  （preflight overall/l2 PASS、12 routes、145 risk frames；checksums 与 A bundle/manifest
  checksum 全量一致；code-reviewer 验收 6/6 PASS）。
- 统一发布流程：`publish_viewer_package.py`（orchestrator/scripts）内置
  `scenario_identity.verify_viewer_identity` 四元组强校验（scenario_id + dataset_bundle
  + risk_window + selected_candidate），并透传 `--risk-explanation-manifest` 使 viewer
  包携带同身份 explanation。后续冬季窗口重建应走该统一脚本。
- 保留语义（非缺陷）：`quality_flag=suspect` 是非权威回溯采集（`authoritative=False`）
  的保守 provenance 标记，content_qc 为 good；explanation `publication_status=PARTIAL`
  源自 `demo_unvalidated` 模型标定语义，与全仓历史一致。走廊坐标
  `tromso_to_isfjorden_outer` v1.2.0 未改动。
- 本文件只登记当前状态；完整运行证据、资源数据与已知限制见
  [Winter B 风险验证报告 §12](../reports/research-validation/WINTER_B_RISK_VALIDATION_REPORT.md)，
  不在此复制细节。
- Viewer 制品选择器（2026-09-03 10:09 +08:00）：顶栏可选择 `work_package_d/output/`
  下已完成 viewer 制品包（显示“航线 · 模拟时间”，默认仍为当前 `viewer/bundle.json`）。
  清单由 `scripts/build_viewer_package_index.py` 生成 `viewer/packages.json`（支持
  `configs/viewer_package_overrides.json` 手工覆盖），`replay_viewer_serve.py` 新增
  `--packages-dir` 只读前缀挂载，前端新增 `viewer/package_picker.js|css`（  下拉、右键
  “属性”弹窗、切换失败自动回退默认）。本地 HTTP 冒烟与静态验收通过；真实浏览器交互
  验证 `RUN / PASS`（Firefox 155，2026-09-03），含切换、属性弹窗与恶意参数回退，期间修复
  app.js 钩子未 `await` 的 bug，用法见 DEMO_RUNBOOK Mode H、证据见报告 §12.4。
- git（本轮）：orchestrator 提交 `15b4c6c`（统一发布脚本 + scenario_identity），
  governance 提交 `6f0cae0`（重建登记）；未 push；并发 agent（codex）的 3 个
  工作树改动未被混入提交。

## 2026-09-01 22:52 +08:00 holdout 中间基线（已由原始冻结到达态包替代）

本轮已把默认 Viewer 从“静态/单路线 fallback”切换到同一真实 Winter holdout 回放的
资源链；B-spline 没有改变 C 的航点、ETA、风险、采用门或安全语义。

| 现象 / 声明 | 根因 | 当前证据与状态 |
|---|---|---|
| 待采用、已替代、当前路段消失 | 默认 bundle 没有同身份 replay revision 资源；当前路段又受旧路线图层开关影响 | 已解耦；正式 `motion_samples`/revision 状态驱动；DOM 显示 `R2 待采用`、`R2 已采用`、`R3 待采用`，`rev1=superseded / rev2=current / rev3=pending` |
| 只有一项路线 | 旧 Viewer 入口消费空/单路线 fallback，不是 C 没有生成候选 | 新 manifest 的每个 revision 均为 4 层×3 目标=12 条，D candidate set `PUBLISHED`、12/12 integrity PASS |
| 风险时域图空、颜色异常 | 344px flex 子项被压缩；最小柱宽和横向滚动缺失 | 145 帧、tick 8px、bar 3.35px、横向滚动；Firefox 344px/528px 均 PASS，绿色均值/黄色最大值可见 |
| `Explanation unavailable` | 当前恢复的原始冻结身份没有可重建的同次 B trace | 精确 A source record 已退役；不跨身份复用 sidecar、不从 RiskFrame 反推原因；基础风险/路线/仿真保持可用 |
| 曲线是否“更弯” | 观察窗口/缩放不足，不是 B-spline 破坏航线；几何仍受约束 | 继续展示局部放大、最小曲率半径和最大偏离；不放大平滑幅度、不绕过安全门 |

### Winter holdout 动态回放证据（历史中间包，非当前默认）

- 真实数据源为 `tromso_isfjorden_winter_holdout_20260222_v1`，回放制品为
  `retrospective_dynamic_replay`；保留原始 `issue_time`，因此这是**事后动态投影**，不是
  当时可用信息的 causal replay。严格 causal Winter 窗口仍因 issue-time 覆盖不足保持
  fail-closed。
- 回放 `winter-retro-holdout-resource-v4`：3 个 6 小时 snapshots、145 个 RiskFrame、
  3 次候选计算均接受、无 planning blocker；事件实际包含
  `REPLAN_DECIDED`、`REPLAN_ADOPTED`、`ROUTE_CHANGED`。
- 真实不可变 plan-revision index 记录 `rev1=superseded`、`rev2=current`、
  `rev3=pending`；D 默认包状态为 `PUBLISHED_RETROSPECTIVE_DYNAMIC_REPLAY`，时间线为
  3,145 个 1 分钟仿真时刻，正式 `cd.route-motion-set.v1` gate 有效。
- B 已对同一 RiskWindow 真实生成并发布 `risk-explanation.v1`：artifact
  `risk-explanation-sha256-28a2329d38e98540be23e8756d6314874dcb13d4e482c70876cfabb7e31ef39c`，
  manifest `risk-window-sha256-6ebe9d4560d04dc01b27bba2239af7f0f9a96dc779aaaad0d2ad17619700ee7c`；
  D v7 已嵌入并通过 readback。145 帧逐格状态为 `COMPLETE=29,433`、`PARTIAL=17,402`、
  `UNAVAILABLE=2,610`，后两者是源数据缺测的可解释结果，不是 sidecar 整包缺失。

### C RC2 三核并行证据

正式 Orchestrator 初始规划和重规划均重新接入 C 的 objective-level
`ProcessPoolExecutor`：tick、layer、B 和 adoption gate 保持串行，只并行
`fastest/low_risk/recommended` 三个目标。真实回放 report 为
`requested_workers=3`、`effective_workers=3`、`max_parallel_tasks=3`、
`planning_calls=12`、`tasks_submitted=36`、`parallel_active=true`；worker PID 列表作为
跨调用 provenance 保留。`ExecutionSpec.v1` 维持 RC2 三 worker 兼容默认，`v2` 可显式记录
profile。

### B / O 状态边界（v4 中间基线记录）

- B 的 `allowed_region_has_no_grid_node` 是 Murmansk 默认粗网格在窄 destination allowed
  region 没有节点的既有数据/端点问题；已改为预期 fail-closed 测试，不扩大网格、不伪造
  节点。Tromsø fine holdout 正向路径通过。
- 此处曾记录 O 形式化重集成未重跑；2026-09-02 已在最终工作树重新执行两个 formal
  integration 参数用例并取得 `2 passed, 1 warning`、退出码 0，现行结论以上方最终收口
  章节为准。

支持证据：

- [Winter 动态重规划与 C RC2 三核并行工程运行报告](../reports/research-validation/WINTER_DYNAMIC_REPLANNING_RC2_PARALLEL_RUN_REPORT.md)

## 2026-09-01 Viewer 根因收口（历史 baseline 与当前默认路径）

- 旧默认 Winter package 没有同身份 replay，曾用单路线加 `PLAN_COMPUTED` 占位；严格 causal
  入口现在仍在缺源时显示 `UNAVAILABLE_IDENTITY_BOUND_CAUSAL_REPLAY_REQUIRED` 并保持空事件。
  当前默认路径已显式选择真实 `retrospective_dynamic_replay`（不是 causal），因此在通过
  identity/index 校验后展示真实 `REPLAN_DECIDED/ADOPTED`、多 revision、pending/superseded
  状态；不会人工伪造事件。
- “当前路段”不再受原始折线图层开关控制，优先按 C formal `motion_samples` 的 ETA 窗口截取；
  曲线面板只展示局部放大、最小曲率半径与相对权威航点最大偏离，不改 geometry 或安全门。
- 风险时域图原因为 344px 下 flex tick 宽度被压到 0px；现保留 145 个小时帧、横向滚动并设置
  tick/bar 最小宽度，Firefox 344px/528px 回归均通过，绿色/黄色柱值可见。

## D 风险解释消费者门禁（2026-08-23 21:51 +08:00）

> 历史基线章节。当前默认原始冻结身份的 sidecar 缺失状态见本文顶部；本节只保留 optional
> consumer 的不变边界，以及曾在另一 holdout 身份上通过的生产/传输验证。

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| D 可选消费者 | BROWSER_E2E_PASS | 合成 sidecar + 真实 Winter base；missing/invalid/PARTIAL/COMPLETE；Firefox 点击格点面板 |
| RiskFrame 权威性 | PRESERVED | level/score/confidence 只读 `bc.risk-frame.v2`；risk/route/simulation 不变 |
| 身份失败关闭 | PASS | schema、RiskWindow、RiskFrame、网格/坐标不匹配时拒绝 sidecar |
| 浏览器控制台/网络 | PASS | 0 错误；0 警告；8 个必需资源 HTTP 200 |
| D 回归 | PASS | `91 passed / 3 causal-replay-only skipped`；Ruff/JS 语法 PASS |
| B 生产者构件 | ENGINEERING_CHAIN_PASS / UNCALIBRATED | 同次公式求值 trace + `risk-explanation.v1`；`demo_unvalidated` / `research_unvalidated` |
| Orchestrator 不可变传输 | ENGINEERING_CHAIN_PASS | `risk-explanation-manifest.v1` content-addressed artifact，SHA/identity readback；D 可选消费 |

D 的 `risk-explanation.v1` 支持是可选、增量且 explanation-scope 失败关闭。sidecar 缺失或
不匹配时，Viewer 显示 `Explanation unavailable`，基础 Winter RiskFrame、route candidates
与 ETA simulation 继续工作。`PARTIAL` 不补零或自动生成 reason；`COMPLETE` 仅展示生产者
字段。该历史浏览器 E2E 的 PARTIAL/COMPLETE 内容是明确标记的合成 B fixture；当前真实
Winter v7 sidecar 已另行完成工程链 readback，但仍不证明科学标定或导航资格。

## B 风险标定研究门禁（2026-08-23 20:45 +08:00）

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| 当前 B 标尺 | DETERMINISTIC_ENGINEERING_BASELINE | 11 个归一化分量的加权和；`demo_unvalidated` |
| 科学标定 | NOT_ESTABLISHED | 无专家/结果/物理阈值验证 |
| 冬季有限分布 | REAL_ARTIFACT_AUDIT_PASS | 均值 `0.119016`；P95 `0.226415`；93.069778% L1 |
| 阈值变更 | NOT_APPROVED | `0.2/0.4/0.6/0.8` 保持冻结基线 |
| 分量归因 | PRODUCER ENGINEERING_PASS / UNCALIBRATED | B 同次公式 trace + immutable sidecar 已发布；D 可选消费者 BROWSER_E2E_PASS；RiskFrame 仍不变 |
| B/C/D 运行时语义 | PRESERVED | 零代码、零构件修改；C 路线响应证据继承 |

当前 `risk_score` 只能解释为加权归一化风险指数，不是事故概率或经过实船结果
标定的严重度。等宽 level 策略对本冬季分布存在明显压缩，但这不足以单独批准新阈值。
下一门禁是定义 operational target、建立跨场景 calibration dataset，并比较
expert/physics/statistical/outcome-based 方法；现有 sidecar 只证明工程归因链，不提升校准等级。

支持证据：

- [风险标定研究](../reports/research-validation/RISK_CALIBRATION_RESEARCH_REPORT.md)

## 冬季组合研究查看器（2026-08-23 20:14 +08:00）

> 历史 checkpoint；2026-09-01 最新动态回放与并行判定见本文顶部，当前默认 Viewer 已使用
> 真实 retrospective dynamic replay，但严格 causal 仍保持 pending/fail-closed。

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| 冬季组合展示 | REAL_E2E_PASS | 单一 scenario/run/bundle/RiskWindow/candidate 身份；145 帧；12 条路线 |
| D 冬季研究视图 | REAL_E2E_PASS | Firefox；风险/硬约束/路线/船舶/运行/暂停/图层选择器 |
| 浏览器控制台/网络 | PASS | 0 错误；0 警告；8 个必需资源 HTTP 200（含可选消费者验证器） |
| 航行仿真 | EXPERIMENTAL / REAL_E2E_PASS | 3,206 个 1 分钟状态；C 所选路线航路点 ETA 投影 |
| 冬季因果回放/重规划 | SOURCE_REQUIRED / FAIL_CLOSED | Orchestrator 仅接受同身份 causal-replay manifest；当前 Winter 无合格源，默认不发布事件 |
| A/B/C/合约/冻结构件 | PRESERVED | 本轮零修改、零重算 |

当前 Viewer 已不再混用 Summer replay 与 Winter candidates。Orchestrator 失败关闭绑定
active DatasetBundle、RunContext、145 帧提交态 RiskWindow、C v3 方案集、12 条路线
candidate sidecar 与完整性证据；D 再次校验组合身份，并显式显示 scenario、
DatasetBundle、RunContext、RiskWindow 与 assembly ID。航行时间线来自 C 全航程
recommended waypoint ETA，`source_replay=null`，并显式标记需要身份绑定 causal replay；
因此该里程碑证明冬季研究航行仿真，不证明冬季因果回放或动态重规划。传入合格源后才
原样展示真实多 revision 与 `REPLAN_DECIDED/ADOPTED`。

支持证据：

- [冬季组合 Viewer 集成](../reports/research-validation/WINTER_COMBINED_VIEWER_INTEGRATION_REPORT.md)

## D 研究可视化第一阶段历史门槛（2026-08-23 16:59 +08:00）

> 该表记录第一阶段结束时的状态；当前组合 Browser 状态以上方最新里程碑为准。

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| B→C 接口 | STABLE | `bc.risk-frame.v2` 提交窗口边界；unknown 失败关闭 |
| C→Orchestrator 接口 | STABLE | 真实 Winter `cd.four-layer-route-plan-set.v3`；4×3 原子发布 |
| Orchestrator→D 接口 | STABLE | `presentation.route-candidates.v1` 精确投影；不重排/不重算 |
| D 研究视图 | IMPLEMENTED / UNIT_PASS | 4 层选择器、3 目标对比、构件指标、候选几何 |
| 既有冻结 Viewer 回退 | BROWSER_E2E_PASS | Firefox；NOT_PUBLISHED → `SINGLE_ROUTE_FALLBACK`；控制台 0；必需资源 HTTP 200 |
| 冬季组合 Viewer | REAL_E2E_PASS / REPLAY_SOURCE_REQUIRED | 同一 Winter risk/route/candidate bundle 已通过；动态重规划需额外同身份 replay 制品 |

D 现在只在完整、scenario 匹配的 12 路线 PUBLISHED 包下启用研究视图；
用户路线选择是 display-only 高亮，不修改 C 的 `selected_candidate_id`。缺失
sidecar、4×3 不完整、metrics/geometry 非法、硬约束违规或 scenario 不匹配均失败
关闭回到现有权威路线。真实 Winter sidecar 的 metrics/identity 已由 78 项 D
测试验证；现有 48h 冻结 bundle 的 Operational Replay 由 Firefox 复测通过，但由于尚无
冬季组合 bundle，本轮不得声明 Winter Research Browser E2E。

支持证据：

- [B/C/D 接口状态](../reports/research-validation/B_C_D_INTERFACE_STATUS.md)

## 冬季 C 验证与 D 并行接口门禁（2026-08-23 10:20 +08:00）

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| A/B 冻结输入 | PRESERVED | bundle、RunContext、ExecutionSpec、145 帧 RiskWindow 身份不变 |
| C 冬季消费者 | PASS | 精确提交窗口、正式溯源、31×11 端点映射 |
| C 冬季验证 | COMPLETED / EXPERIMENTAL | `cd.four-layer-route-plan-set.v3`；4×3=12；完整性 12/12 PASS |
| 冬季路线决策 | OBSERVED_CHANGE | 对比夏季权威初始：11/22 航路点不同，+11.658 km，+2.951 h |
| C→D 候选 sidecar | INTERFACE_PASS | `presentation.route-candidates.v1` 已发布；12 个候选；失败关闭回退保留 |
| D 并行开发 | READY | D v3 加载器 4 层/12 方案；规范风险指标摄取 PASS |
| D 冬季可视化 | PHASE_1_UNIT_PASS | 候选地图/对比已实现；组合 bundle 与 Winter Browser E2E 未完成 |

本轮首次完成真实 Winter C 正式 v3 规划。推荐线为 921.379560 km、53.405581 h，
avg/max 风险为 0.105651/0.189369。Summer Viewer 未发布路线级风险指标，故只对
有证据的 geometry/distance/ETA 做比较；不补造 Summer 风险数值，也不把观察性差异写成
已隔离的季节因果。

支持证据：

- [冬季 C 冒烟](../reports/research-validation/WINTER_C_SMOKE_REPORT.md)
- [冬季 C 路线验证](../reports/research-validation/WINTER_C_ROUTE_VALIDATION_REPORT.md)
- [D 接口就绪](../reports/research-validation/D_INTERFACE_READY_REPORT.md)
- [冬季数据可用性跟进](../reports/research-validation/WINTER_DATA_AVAILABILITY_FOLLOWUP.md)
- [冬季 C 最终报告](../reports/research-validation/WINTER_C_VALIDATION_FINAL_REPORT.md)

## 冬季 B 首次科学运行（2026-08-23 02:44 +08:00）

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| 冬季 DatasetBundle | FROZEN_ARTIFACT_READY | active `a-bundle-a2146dd0adbaa7db77a6beb7`，1,212 条记录，SHA/摘要不变 |
| A→B 正式交接 | READY_FOR_B_VALIDATION | 固定 RunContext/ExecutionSpec，精确 bundle 输入恢复 PASS |
| B 冬季验证 | COMPLETED / EXPERIMENTAL | medium 31×11；145 个正式 `bc.risk-frame.v2`；schema/存储/回读 PASS |
| 冬季风险分布 | OBSERVED_CHANGE | 夏季/冬季相同 realized 网格对比可用；有限均值 `0.045027961 → 0.119015786` |
| 未知可航行节点 | 观察到 0 | Winter `unknown_navigable_nodes=0`；硬约束/原因一致性不匹配 `0` |
| C 冬季验证 | NOT_STARTED | 本轮明确未运行 C 规划器 |
| D 冬季可视化 | NOT_STARTED | 本轮明确未运行 D/Viewer |

当前结论：冬季 B 已完成第一轮工程/研究验证，证明在相同 medium realized 网格、逐小时
时间间隔和 B 模型配置下，冬季输出风险分布发生变化。B 模型仍是
`demo_unvalidated`，且夏季/冬季数据源体系不同，因此该结果不是科学标定或仅由冬季
月份导致的因果结论。`DATA_UNAVAILABLE` 必须与有限风险分布分开解读。

支持证据：

- [冬季 B 基线决策](../reports/research-validation/WINTER_B_BASELINE_CONFIG_DECISION.md)
- [冬季 B 冒烟报告](../reports/research-validation/WINTER_B_SMOKE_REPORT.md)
- [冬季风险分布审计](../reports/research-validation/WINTER_RISK_DISTRIBUTION_AUDIT.md)
- [冬季 B 验证报告](../reports/research-validation/WINTER_B_RISK_VALIDATION_REPORT.md)

## 冬季正式交接里程碑（2026-08-23 01:16 +08:00；B 首轮结果见上方最新里程碑）

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| 冬季必需覆盖率 | 12_OF_12_COMPLETE | 1,212 条记录的冻结 A bundle |
| 冬季 DatasetBundle | FROZEN_ARTIFACT_READY | active `a-bundle-a2146dd0adbaa7db77a6beb7`；144 h 最小；解析/摘要/doctor 通过 |
| 冬季 RunContext | PUBLISHED / SCHEMA_PASS | `run-441b03c8-d45b-5414-b0e8-b7fd0d990c22`；官方原子生成器 |
| 冬季 ExecutionSpec | PUBLISHED / SCHEMA_PASS | 严格 `orchestrator.execution-spec.v1`；身份对齐 |
| A→B 正式交接 | READY_FOR_B_VALIDATION | 精确归档仅摄取 PASS；B 未开始 |
| 交接时的冬季 B/C/D | NOT_STARTED | 交接完成时的下游起点；B 首轮结果见上方最新里程碑 |

当前交接里程碑结论：冬季数据源采集、修正后的 A 不可变 bundle、匹配的 `RunContext.v2`、
严格的 `ExecutionSpec.v1` 以及 Orchestrator 仅摄取全部通过。该阶段只完成摄取；
后续 B 首轮结果见本文件顶部最新里程碑。旧的 132 小时最小 bundle 继续作为被取代的
历史证据保留。

支持证据：

- [冬季数据源验证](../reports/research-validation/WINTER_SOURCE_VALIDATION_REPORT.md)
- [气象数据源对比](../reports/research-validation/WINTER_MET_SOURCE_COMPARISON.md)
- [冬季身份审计](../reports/research-validation/WINTER_EXPERIMENT_IDENTITY_AUDIT.md)
- [冬季交接验证](../reports/research-validation/WINTER_HANDOFF_VALIDATION_REPORT.md)
- [冬季不可变 bundle 重新发布](../reports/research-validation/WINTER_BUNDLE_REISSUE_REPORT.md)
- [冬季正式交接](../reports/research-validation/WINTER_FORMAL_HANDOFF_REPORT.md)

接口稳定化结论：A→B `DatasetBundle.v2 + RunContext.v2`、B→C
`bc.risk-frame.v2 + committed hourly window`、C 正式 v2/v3 与 Orchestrator→D
展示基线均可保持现有版本。冬季 B 验证必须先审计 unknown 是否被
正确硬掩膜；C route candidates 在 Replay Viewer 仍为 `NOT_PUBLISHED`。

## 第三阶段真实实验结果（2026-08-22 02:34 +08:00）

> 历史第三阶段检查点；上方的冬季身份门禁才是当前状态。

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| 冬季 Copernicus 采集 | PARTIAL / 8_TYPES_DOWNLOADED | 1,064 条目标窗口记录、八个不可变源快照、精确端点 |
| 冬季 12 类 A 覆盖率 | PARTIAL / 9_OF_12_COMPLETE | 八个 Copernicus 行 + 缓存的 GEBCO 掩膜完整；bundle 未持久化 |
| 冬季 GFS | BLOCKED_BY_SOURCE_AND_CADENCE | NCEI 202602 object/THREDDS 路径缺失；直接清单 404；6 h 适配器 vs 3 h 覆盖率门控 |
| A 归档完整性 | VALIDATED | doctor 检查 5,232 项，0 错误，0 警告 |
| C 精确采样画像 | EXPERIMENTAL / REAL_B_FRAME_PASS | 705,469 请求；242,992 次精确重复；34.444% 复用上限 |
| C 有界 LRU | IMPLEMENTED / EXPERIMENTAL_DEFAULT_OFF | 5 万上限；中位数 76.281 s → 65.012 s；完整路线摘要不变 |
| B-C 优化 medium 路径 | EXPERIMENTAL / VALIDATED | 固定 B 输入与端点；每模式 3 次独立运行；无合约/发布变更 |

在此历史检查点，尚无冬季 DatasetBundle、RiskFrame、路线或 Viewer 构件。C LRU
仅通过实验基准可用，不用于正式入口。未运行完整 48 小时回放、重型集成与
确定性双跑。

## 第二阶段真实实验结果（2026-08-22 01:11 +08:00）

> 历史第二阶段检查点；上方第三阶段表格才是当前状态。

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| 冬季 12 类可行性 | BLOCKED_BY_DATASET | 全部 12 个本地目标走廊行均无 2026 年 2 月记录；未下载/未伪造 |
| B 正式固定网格对比 | EXPERIMENTAL / REAL_DATA_PIPELINE_PASS | 16×7、31×11、60×21 各 78 个正式帧；B 构建 4.03/3.86/3.91 s |
| B→C 耦合基线 | EXPERIMENTAL / REAL_B_FRAMES + REAL_C_SEARCH_PASS | 推荐路线在 112 节点时 10.51 s，341 节点时 75.00 s |
| C 缓存可观测性 | IMPLEMENTED / UNIT_PASS | 既有边几何缓存报告命中/未命中/条目；行为不变 |
| 路线候选展示 | DRAFT / PLANNED | 向后兼容提案；当前 bundle 仍为 NOT_PUBLISHED |

正式 B 对比因冬季数据受阻而使用既有夏季归档，其输出未发布到 B 存储。
C 基准解码公共 `bc.risk-frame.v2` 文档并运行真实 C 组件，但未经过提交窗口的正式入口；
它是实验性耦合证据，而非完整集成声明。

## 第二阶段加速结果（2026-08-22 00:24）

> 历史准备阶段检查点；上方第三阶段表格取代其冬季与缓存就绪行。

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| P0 合约登记 | IMPLEMENTED / DOCUMENT_VALIDATED | 归属/版本/状态登记、提案模板、开发归属矩阵 |
| P1 冬季配置 | IMPLEMENTED / UNIT_VALIDATED | 新 `scenario.v2` 身份；合约 19 PASS |
| P1 冬季数据/构件 | BLOCKED_BY_DATASET | 无匹配的 12 类源 bundle；未伪造冬季构件 |
| P2 B 固定网格实验 | EXPERIMENTAL / UNIT_VALIDATED | 合成核 + 正式 78 帧对比；B 61 项非集成 PASS |
| P3 C 组件画像 | EXPERIMENTAL / UNIT_VALIDATED | 组件画像 + 真实帧 BC 基准；C 146 项非集成 PASS |
| P3 边几何缓存身份 | IMPLEMENTED / UNIT_VALIDATED | 缓存键现包含样本数；含定向回归 |
| P4 专业导航辅助 | IMPLEMENTED / BROWSER_E2E_PASS | Firefox：经纬网格、坐标标签、比例尺、格北、独立开关 |

本轮未改动任何核心合约版本、A 采集实现、B 风险公式/等级策略、C 搜索算法/路线语义、
Orchestrator 导出、冻结构件或 48 小时回放。

## 当前阶段（2026-08-21 23:18）

项目已从 Competition Demo Freeze 转入 **研究验证系统增强阶段**。冻结演示基线保留在
`demo-engineering`，当前开发只在 `research-validation-system` 进行。这个阶段先冻结接口
事实和验证口径，再开展 B/C/D 并行研究；不把规划中的冬季场景、自适应网格或候选路线
展示写成已有能力。

| 分支 | 含义 | 状态 |
|---|---|---|
| `main` | RC1 基线 | FROZEN |
| `rc2-development` | RC2 基线 | FROZEN |
| `demo-engineering` | 竞赛演示基线 | FROZEN |
| `research-validation-system` | 研究验证增强 | ACTIVE |

`${ARCTIC_ROUTE_ROOT}` 是多个仓库的工作区，当前没有 root Git。各子仓库分别维护自己的
`research-validation-system` 分支。

## 当前真实架构（2026-08-21 23:18）

| 模块 | 研究阶段角色 | 运行时边界 |
|---|---|---|
| A | 环境数据采集 | 发布 `PreparedWindow` / `a.dataset-bundle.v2` 与溯源 |
| B | 风险评估与预报 | 消费 A 公共 bundle，发布 `bc.risk-frame.v2` |
| C | 风险感知导航决策 | 消费 B risk frame，发布 route plan / layered route set |
| D | 可视化与验证平台 | 只消费已发布 presentation artifact；唯一 Viewer 运行时 owner |
| Orchestrator | 流水线 / 构件 / 展示适配器 | 编排 A→B→C，执行 replay，验证并投影展示 bundle |

```text
A PreparedWindow / DatasetBundle.v2
  -> B BInputEnvelope / bc.risk-frame.v2
  -> C RiskSourcePlanningIngress
  -> cd.route-plan.v2 or cd.four-layer-route-plan-set.v3
  -> Orchestrator replay/presentation export
  -> replay.viewer-bundle.v1
  -> D Viewer
```

`cd.route-plan.v3` 是 four-layer v3 集合内的单路线 schema，不是顶层
ExecutionSpec planning contract。当前 Replay Viewer 消费 `replay.viewer-bundle.v1`，
不直接消费 four-layer aggregate。

## 能力与证据等级（2026-08-21 23:18）

| 能力 | 实现 | 验证 | 当前资格 |
|---|---|---|---|
| A 12 类公共数据 bundle | IMPLEMENTED | ARTIFACT_PASS | 夏季 RC1/RC2 + active Winter 144 h 最小冻结 bundle |
| B 逐小时确定性风险帧 | IMPLEMENTED | AUTHORITATIVE_PASS | 模型仍为 `demo_unvalidated`，不是科学标定结论 |
| B 固定目标网格 | IMPLEMENTED | UNIT/ARTIFACT_PASS | RC2 显式 31×11；代码默认配置可为 16×7 |
| B 自适应网格 | NOT_IMPLEMENTED | NOT_RUN | 研究计划，不得隐式改变 C regular-grid contract |
| C 三目标 | IMPLEMENTED | AUTHORITATIVE_PASS | fastest / low_risk / recommended |
| C 四层 × 三目标 | IMPLEMENTED | AUTHORITATIVE_PASS | `FourLayerRoutePlanSet.v3` 明确验证 12 路线 |
| C 因果回放规划 | IMPLEMENTED | AUTHORITATIVE_PASS | 12h 确定性继承；48h 产品构件已验证 |
| D 展示 Viewer | IMPLEMENTED | BROWSER_E2E_PASS | Firefox；单一 Simulation Clock；artifact driven |
| 48h 回放 Viewer | IMPLEMENTED | BROWSER_E2E_PASS | 49 快照、2881 分钟状态、49 风险帧 |
| C 路线候选展示 | IMPLEMENTED | INTERFACE_PASS | 真实 Winter 12 路线 sidecar 已发布；既有冻结 Viewer bundle 仍保持 NOT_PUBLISHED |
| 冬季场景配置 | IMPLEMENTED | CONFIG_VALIDATED | 144 h scenario；12/12 源行完整 |
| 冬季 DatasetBundle | IMPLEMENTED | FROZEN_ARTIFACT_READY | active bundle ID/digest/SHA 已冻结；最小/请求视界均为 144 h |
| 冬季 A→B 交接 | IMPLEMENTED | READY_FOR_B_VALIDATION | RunContext/ExecutionSpec/schema/精确仅摄取 PASS |
| 冬季 B RiskFrame / C/D 构件 | B,C,D_IMPLEMENTED | B,C_FORMAL_VALIDATED / D_REAL_E2E_PASS | B 145 帧；C 12 路线 v3；D 组合 Firefox PASS |
| B 固定网格实验平台 | IMPLEMENTED | UNIT_PASS / EXPERIMENTAL_REAL_DATA | 正式 builder 对比已完成；输出仍未发布 |
| C 组件画像 / BC 基准 | IMPLEMENTED | UNIT_PASS / EXPERIMENTAL_REAL_DATA | 真实 B 帧与真实 C 搜索；提交态入口未演练 |
| D 专业导航辅助 | IMPLEMENTED | BROWSER_E2E_PASS | 仅 bundle 元数据；规范变换/纵横比保留 |

## 冻结语义（2026-08-21 23:18）

- A→B 只通过公共 `PreparedWindow` / `DatasetBundle.v2` 和匹配的
  `RunContext`；B 不扫描 A 私有 cache、SQLite 或 raw 目录。
- B→C 以 `bc.risk-frame.v2` 为正式边界；unknown 失败关闭，
  `DATA_UNAVAILABLE != safe`。
- C 拥有最终路线、速度、ETA 和重规划决策；D 不重新计算。
- `REPLAN_DECIDED != REPLAN_ADOPTED`，pending route 不提前替换权威
  route，completed track 追加写。
- D 是唯一 Viewer 运行时 owner；Orchestrator 只拥有 replay 与展示
  adapter/export。
- 当前正规网格是 rectilinear regular grid。Adaptive Grid 在 contract proposal
  通过前只能作为隔离实验。

## 当前事实缺口（2026-08-21 23:18）

1. Contract ownership registry 已建立；尚待各 owner 对未来 candidate/adaptive
   proposal 逐项审批，registry 本身不等于提案批准。
2. C→D 已发布真实 Winter 12 路线候选集；本轮 replay 还发布了 3 个不可变 revision，
   每个 revision 均为四层×三目标=12 条路线，并由事件/index 驱动 pending/current/superseded。
3. 冬季场景、12 类源行、144 h 最小冻结 bundle、匹配的 RunContext/ExecutionSpec、B 145 帧
   RiskFrame、C 12 路线验证、B explanation transport 与 D 组合 Browser E2E 已建立。下一
   缺口仅是 issue-time 可追溯的 strict Winter causal replay；当前 3,145 状态时间线来自
   真实 retrospective replay + C waypoint ETA 延展，不能作 causal 证据。
4. B 规则模型未标定；正式固定网格 build 已测，但进程 RSS 包含已加载 A window，
   独立增量内存与重复运行方差仍未测；adaptive grid 未实现。
5. C baseline/medium 联合性能已测；medium exact-sample 50k LRU 已在 default-off
   基准中取得 14.77% 中位数收益。RC2 三 worker 已接入正式 initial/replan；共享搜索与
   增量重规划仍未实现。
6. D 已建立基础专业导航辅助层、研究视图、候选几何、四层三目标对比、
   冬季组合 Browser E2E 与可选逐格风险解释消费者。真实 B 贡献者生产者与
   Orchestrator 不可变传输已完成；独立环境因子层合约仍待实现。

详细依据见
[RESEARCH_VALIDATION_GAP_ANALYSIS.md](RESEARCH_VALIDATION_GAP_ANALYSIS.md)。

## 当前阻塞与风险（2026-08-21 23:18）

| 风险 | 状态 | 处理 |
|---|---|---|
| 多人并行前合约所有权不清 | CONTROLLED | registry/模板/目录所有权已建立；breaking 提案仍需 owner 批准 |
| Winter A/B/C/D 门禁 | D_DYNAMIC_RETROSPECTIVE_REAL_E2E_PASS | 正式身份、B 145 帧/sidecar、C 每 revision 12 路线与 D Firefox PASS；strict causal 仍 pending |
| B 网格策略与 C regular-grid 假设耦合 | EXPERIMENTAL EVIDENCE | baseline+medium 的正式有界 build/C 对比已完成；fine 需要显式预算 |
| C 候选展示 | CONTROLLED / INTERFACE_PASS | 提案已接受；真实 Winter sidecar PASS；冻结 bundle 回退不变 |
| 当前演示基线回退 | CONTROLLED | 冻结分支/构件不改；研究构件使用新身份 |
| B Murmansk 默认网格集成预期 | EXPECTED_FAIL_CLOSED | 粗网格在窄 allowed-region 无 grid node；已用定向测试固定语义，不扩大网格或伪造节点 |

## 正式交接验证边界（2026-08-23 01:16 +08:00）

> 本节记录正式交接当时的仅摄取边界；B 首轮结果以本文顶部的最新里程碑为准。

冬季正式身份双 schema、重建身份、run/spec 绑定与精确归档仅摄取 PASS。Contracts 19 PASS；
Orchestrator fast 84 PASS、2 deselected；两仓库 Ruff clean。最终三件套仅摄取 wall
`3:26.43`、peak RSS `978,740 KiB`。本轮没有运行 B/C/D、48h 回放、重型集成或新的
确定性双跑；这些旧证据均未提升为本轮重验。
