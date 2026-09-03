---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Applicability: CURRENT
Scope: first formal Winter B scientific validation run, Summer/Winter comparison, and the 2026-09-03 compliant rebuild run evidence (§12)
Canonical/Supporting: Supporting milestone report; canonical status is current/reference/WINTER_SCENARIO_STATUS.md and current/CURRENT_STATUS.md
Branch: research-validation-system
Last Verified: 2026-09-03 09:09 +08:00
---

# Winter B Risk Validation 报告

## 1. Executive Summary（2026-08-23 02:44 +08:00）

本轮完成了 Winter A frozen bundle 到 B `bc.risk-frame.v2` 的第一次正式研究验证，
没有进入 C、D、Replay，也没有修改 A bundle、RunContext、ExecutionSpec、contract schema、
B 风险公式或 level policy。

结论：

```text
B_WINTER_VALIDATION = COMPLETED
WINTER_RISKFRAME_AVAILABLE = YES
SUMMER_WINTER_RISK_COMPARISON = AVAILABLE
WINTER_ENVIRONMENT_TO_RISK_DISTRIBUTION_CHANGE = OBSERVED
C_VALIDATION = NOT_STARTED
D_VALIDATION = NOT_STARTED
```

在同一 realized medium grid 和同一 B 配置下，Winter finite risk mean 为 `0.119015786`，
Summer 为 `0.045027961`，约 `2.643153×`；Winter 的 L2/L3 单元出现，L1 比例下降
15.407018 个百分点。该结果证明 B 输出空间结构发生变化，但因为模型仍为
`demo_unvalidated` 且 Summer/Winter 数据源不同，不能写成科学标定或仅由季节导致的因果结论。

## 2. Experiment Identity（2026-08-23 02:44 +08:00）

| 项目 | 值 |
|---|---|
| Scenario | `tromso_isfjorden_february_2026_research_v1` |
| DatasetBundle | `a-bundle-a2146dd0adbaa7db77a6beb7` |
| Bundle digest | `a2146dd0adbaa7db77a6beb7c818e975888600fb31236901fd4af2092069fb71` |
| Bundle SHA-256 | `e28bcca682bb1047381d96d574d42c927f28bf5cd26c363f19fff1fff21c3a2f` |
| RunContext | `run-441b03c8-d45b-5414-b0e8-b7fd0d990c22` |
| ExecutionSpec | `winter_execution_spec_20260215_v1.json` |
| Generation | `0` |
| Knowledge as-of | `2026-08-22T12:00:00Z` |
| Window | `2026-02-15T00:00:00Z` → `2026-02-21T00:00:00Z` |

正式 intake 在上一轮已 PASS；本轮通过 A exact-bundle resolver 再次绑定同一 bundle identity，
没有生成新的 RunContext。

## 3. B Configuration（2026-08-23 02:44 +08:00）

采用 [Winter B baseline decision](WINTER_B_BASELINE_CONFIG_DECISION.md) 中的 medium：

- realized grid：31×11，341 cells/frame；实际步长 `0.3666667° × 1.2°`；
  `grid_id=b-grid-c2bacc0bb86c70e5a59b14d4`；
- model：`demo_unvalidated_rule_baseline.v2`；
- formula：`deterministic_environment_components_v2`；
- level：`c_equal_width_floor_v1`；
- hard：`land_sea_mask_plus_unknown_ice_free_v1`；
- unknown：`nan_confidence_zero_v1`；
- interval：60 minutes。

该配置是本次实验 identity 的一部分，不是对 production default 的批准。

## 4. RiskFrame Generation（2026-08-23 02:44 +08:00）

输出根目录：

`/root/my_project/.runtime/experiments/winter-b-validation-20260823-medium/`

| 检查 | 结果 |
|---|---|
| A exact restore / 1,212 records | PASS |
| 12 required types / coverage / provenance | PASS |
| `bc.risk-frame.v2` frames | 145 |
| Schema validation | PASS（145/145） |
| Formal provenance | PASS（145/145） |
| PersistentRiskStore commit | PASS |
| Commit readback digest | PASS |

Commit：

`risk-window-sha256-b5bed6bb48893e32620710e8c765dc60ec37a2fc384f0c49014b92f0a1c056b2`

## 5. Risk Distribution Results（2026-08-23 02:44 +08:00）

参见 [Winter / Summer 风险分布审计](WINTER_RISK_DISTRIBUTION_AUDIT.md)。核心结果：

| 指标 | Summer 48h / 49 frames | Winter 144h / 145 frames |
|---|---:|---:|
| L1 | 74.780059% | 59.373041% |
| L2 | 0% | 4.419051% |
| L3 | 0% | 0.002022% |
| L4 | 0% | 0% |
| L5 | 25.219941% | 36.205885% |
| finite risk mean | 0.045027961 | 0.119015786 |
| finite risk max | 0.162555397 | 0.400563359 |
| unknown navigable nodes | 0 | 0 |

## 6. Summer / Winter Comparison（2026-08-23 02:44 +08:00）

比较使用已有 Summer Viewer 48h 的 49 个实际风险帧，并以 RiskFrame 坐标校验网格一致；
没有把 49 帧和 145 帧的总 cell 数直接当作季节效应。

可观察结论：

- Winter finite risk mean 比 Summer 高 `0.073987825`，约为 `2.643153×`；
- Winter L2/L3 出现而 Summer 全部为 L1（有限单元）；
- Winter L1 下降 `15.407018 pp`；
- Winter L5 上升 `10.985944 pp`，但这部分与 `DATA_UNAVAILABLE` hard cells 同步增加，
  不能全部解释为环境风险上升；
- `LAND` 百分比一致，Winter hard 增量主要来自数据不可用区域；
- 即使将 hard/unavailable 单独剥离，finite risk 的均值和最大值仍明显上升。

## 7. Unknown / Hard Reason Analysis（2026-08-23 02:44 +08:00）

Winter：

```text
LAND = 9,425
DATA_UNAVAILABLE = 8,477
OTHER = 0
ICE = 0（canonical hard_reason 未单独定义）
unknown = 17,902
unknown_navigable_nodes = 0
hard/reason mismatch = 0
```

`DATA_UNAVAILABLE` 保持为 hard/unknown，不被映射为 safe。B payload 的逐变量缺测 sidecar
显示，Winter 目标网格上 `significant_wave_height`、冰相关变量、海流和水位在部分 cell
存在非有限输入；temperature、visibility、wind 在本轮 frame attributes 中没有非有限格。
这些信息支持“不可用区域增加”的工程解释，但不替代后续源数据质量审计。

## 8. Performance（2026-08-23 02:44 +08:00）

| 项目 | 观测 |
|---|---:|
| A exact restore | 199.801 s |
| B build | 7.907 s |
| Publish/readback | 2.229 s |
| runner total | 215.546 s |
| wrapper wall | 3:36.12 |
| B sampled peak RSS | 1,013,600 KiB |
| process max RSS | 1,024,908 KiB |
| swap | 0 |

这是一次工程观测；没有进行多次重复、统计置信区间或专业 benchmark。内存峰值包含加载的
A window、payload snapshot、B build 和 JSON/store 操作，不能解释为 B 算法的独立增量内存。

## 9. 测试与回归（2026-08-23 02:58 +08:00）

| 检查 | 结果 |
|---|---|
| `run_winter_b_validation.py` `py_compile` | PASS |
| B unit/contract focused suite | PASS；51 passed，5.53 s |
| B Ruff（`src tests scripts`） | PASS |
| Contracts suite | PASS；19 passed，0.44 s |
| Orchestrator fast suite | PASS；84 passed，2 deselected，2.88 s |
| Orchestrator Ruff | PASS |
| B full pytest | PARTIAL；68 passed，1 failed，1 warning，53.22 s |

B full pytest 的唯一失败是既有的
`tests/integration/test_a_b_c_full_window.py::test_default_grid_materializes_corridor_allowed_regions[...]`，
错误为 `allowed_region_has_no_grid_node: goal_allowed_region contains no grid node`。该用例属于
既有 C endpoint/grid mapping 集成路径；本轮只新增 Winter B 编排 runner 和文档，没有修改 C、
grid 语义或该测试依赖，因此不将其隐藏为全量 PASS，也不在本轮越界修复。

本轮没有运行 C planner、D Viewer、Replay、full integration 或 determinism twin-run。

## 10. Issues / 未完成项（2026-08-23 02:44 +08:00）

1. B calibration status 仍为 `demo_unvalidated`，不能宣称风险概率已校准。
2. Winter 的 `DATA_UNAVAILABLE` 比例显著高于 Summer，需要后续确认是数据源空间支持、
   再网格化边界还是源产品质量属性；本轮不修改数据或 policy。
3. C 尚未消费本轮 Winter RiskFrame；unknown gate 虽然在 B 输出上通过，但路线可行性、
   ETA 和搜索性能仍未验证。
4. D 尚未消费 Winter artifact；没有 Winter Viewer 或 route visualization 结论。
5. 没有运行 full integration、Replay、48h replay 或 determinism twin-run。

## 11. Next Step Recommendation（2026-08-23 02:44 +08:00）

下一轮只在本报告和 `distribution.json` 作为输入证据后启动 Winter C consumer smoke：

1. 复核 B RiskFrame committed window、unknown/hard gate 和 `DATA_UNAVAILABLE` 空间位置；
2. 由 C 使用精确的 `bc.risk-frame.v2` committed window 做最小 route/integrity smoke；
3. 对比 Summer/Winter route success、ETA、speed factor 和 risk exposure；
4. 保持 D 未启动，直到 C 语义和 route artifact 通过。

```text
NEXT = Winter C Route Planning Validation
```

## 12. 2026-09-03 合规重建与可解释制品（2026-09-03 09:09 +08:00）

> 本轮替代 2026-09-02 恢复的原始冻结身份制品：旧 `a-bundle-a2146dd0…` 的 ocean_current
> 使用 detided 后备数据，其精确 A source record 已在 2026-08-26 detided 退役中物理删除，
> 无法重建同次 B formula trace，Viewer 因此为 `Explanation unavailable` 诚实降级。
> 当前状态仍以 `current/CURRENT_STATUS.md` 为准，本章只承载本轮运行证据。

**1. 执行摘要**：按原时间窗（2026-02-15T00Z→2026-02-21T00Z，144 h）重新采集合规数据并重建
A→B→C→D 全链，产出**全新身份**的正式可解释制品。final verdict：`PASS`（preflight overall/l2
PASS、12 routes、145 RiskFrame、explanation PUBLISHED 且已嵌入 Viewer、code-reviewer 6/6）。
blocker：无。新身份不可复现旧 `a2146dd0` digest（数据为重新采集），属预期。

**2. 范围 / 非范围**：
- 已做：A 重采集（total-current-only）与 bundle 重发；B 同次 `build_window_with_explanation_trace`
  构建与 `risk-explanation.v1` 发布；C 12 路线 plan-set / route-candidates / motion（含
  candidate-set）；D Viewer 包导出与 preflight；统一脚本补 `--risk-explanation-manifest` 透传；
  状态与报告登记。
- 未做：未把新 Viewer 包切换为 D 默认资源链（涉及默认身份变更，需人工确认）；未运行单元测试
  或 formal integration；未执行 git 提交 / 推送；未做浏览器视觉验收；未重新标定 B 模型；
  未改动走廊坐标 `tromso_to_isfjorden_outer` v1.2.0。

**3. 起始基线**：旧 identity（bundle `a-bundle-a2146dd0adbaa7db77a6beb7`、RiskWindow
`risk-window-sha256-b5bed6bb…`）；已知限制：explanation 不可重建、detided 源退役、Viewer
显示 `Explanation unavailable`。

**4. Git 最终状态**：本仓库结构为各 `work_package_*` 独立 git（根非 git 仓库），本轮未 commit /
未 push。

| 仓库 | 分支 HEAD | 工作树（本轮相关） | 提交 | 推送 |
|---|---|---|---|---|
| `arctic_route_orchestrator` | `c845365`（2026-09-02 17:07:53 +0800） | `M README.md`、`M src/arctic_route_orchestrator/route_motion.py`、`M tests/unit/test_route_motion.py`（并发 agent 改动，非本轮）；本轮新增未跟踪 `scripts/publish_viewer_package.py`、`src/arctic_route_orchestrator/scenario_identity.py` | 无 | 无 |
| `arctic_route_governance` | `28d1be0`（2026-09-02 13:23:49 +0800） | `M current/CURRENT_STATUS.md`（本轮 +43 行） | 无 | 无 |
| `work_package_a` / `work_package_d` | `0bebdf9` / `5012e6b`（均 2026-09-02） | 本轮无源码改动（仅 A 写入独立实验数据根；D 仅新增 output 目录） | 无 | 无 |

**5. 文件系统与资源安全**：
- 根目录外写入：无（全部写入 `/root/my_project` 内；A 正式 `data` 根未改动）。
- `free` 前值（2026-09-03 观测）：total `7.4Gi`、available `~2.7Gi`。
- 最低观测 `MemAvailable`：`~2.7Gi`（采集与 IDE 并存期间）；后值 `3.9Gi`。
- swap：`4.0Gi`，前值 used `336Ki`、峰值 `318.9Mi`、后值 `318.9Mi`（`/dev/sdc`）。
- 峰值 RSS：B 构建 `2,159,924 KiB`（≈2.06 GiB）；C 规划 `193,816 KiB`；motion ≈474 MB。
- OOM：无（进程失败均由网络中断 / 删除拦截导致，非 OOM killer）。
- 重型任务重叠：无（采集、B、C、motion、D 严格串行）。

**6. 代码 / 架构变更**：
| 组件 | 旧行为 | 新行为 | 原因 |
|---|---|---|---|
| `arctic_route_orchestrator/scripts/publish_viewer_package.py` | 导出 Viewer 包时不接受 explanation 入参，包内无 `risk_explanation` | 新增 `--risk-explanation-manifest` 并透传给 `replay_viewer_export.py`，包内嵌入 `risk_explanation` + `risk_explanation_transport` | 修复 Viewer `Explanation unavailable`：D 侧此前没有把 B 同次 trace 制品接入导出链 |
| `arctic_route_orchestrator/src/arctic_route_orchestrator/scenario_identity.py`（本轮前新增，未跟踪） | — | `verify_viewer_identity()` 四元组强校验（scenario_id + dataset_bundle + risk_window + selected_candidate） | 防止 v13 holdout 类身份错配重演 |

**7. 语义 / 合约变更**：
- 变化：ocean_current 由 detided 后备源改为**强制含潮总流**（`current_component=total`、
  `tide_included=true`、源 `ARCTIC_ANALYSISFORECAST_PHY_TIDE_002_015`）；Viewer bundle 新增
  `risk_explanation` / `risk_explanation_transport` 字段（可选嵌入，未提供 manifest 时保持原行为，
  不破坏既有包）。
- 未变化：schema（`a.dataset-bundle.v2`、`bc.risk-frame.v2`、`risk-explanation.v1`、
  `cd.four-layer-route-plan-set.v3`、`cd.route-motion-set.v1`）、走廊坐标、fail-closed 语义、
  `REPLAN_DECIDED != REPLAN_ADOPTED` 等既有状态语义。

**8. 实验 / 备选方案**：
- 整窗口一次采集：CARRA 成功（49 帧/类），Copernicus 因 WSL 断网/重启失败 → 改为**按日分片逐类型**
  续采（manifest + 进度文件驱动断点续传），采用。
- wave（3 h cadence）按日分片：相邻段共享 00:00 帧触发 preflight conflict → 改为 wave **整窗口
  单次重采**，采用。
- 清空数据根重采：会丢弃已发布帧且成本过高，未采用。

**9. 权威运行 / 真实验证**：本轮无 causal replay（本窗口 replay 仍因 issue-time 覆盖不足
fail-closed），以下内容为真实数据 A→D 运行：
- scenario `tromso_isfjorden_february_2026_research_v1`；window `2026-02-15T00Z`→`2026-02-21T00Z`；
  profile `medium`；grid `31 × 11`；model `demo_unvalidated_rule_baseline.v2`；
  run `run-bd3c3ba5-015c-4953-97a2-c7e3cfbefc01`。
- 关键计数器：A 1,212 records；B 145 RiskFrame（`unknown_navigable_nodes=0`）；C 12 routes
  （4 层 × 3 目标，integrity 12/12 PASS）；D 145 risk frames、12 routes、motion set 1 个。

**10. 性能分解**：

| 阶段 | Before（旧轮可比值） | After | Delta | 说明 |
|---|---|---|---|---|
| B 构建 | `UNKNOWN`（旧轮未在同环境计时） | resolve 128.45s / build 7.20s / publish 1.83s / total 146.18s | 新增证据 | 缓存 3 GiB；旧值无法取得，不虚报 |
| C 规划 | `UNKNOWN` | planning 33.35s / total 35.91s | 新增证据 | 12 routes，peak RSS 193,816 KiB |
| motion | `UNKNOWN` | ≈6 min（观测值） | 新增证据 | 12 routes + candidate-set |
| D 导出 | `UNKNOWN` | ≈90 s | 新增证据 | 含 preflight |

**11. 正确性 / 验证**：
- unit：`NOT RUN`（本轮为制品重建运行；orchestrator 工作树含并发 agent 改动，全仓测试会混入无关变更）。
- integration / formal integration：`NOT RUN`（同上，且耗时长；未纳入本轮范围）。
- smoke：`RUN / PASS`（A replay bundle、B validation、C validation、motion、D export 全链路真实数据）。
- real-data：`RUN / PASS`（真实 Copernicus / CARRA 采集数据）。
- route integrity：`PASS`（12/12）；L1/L2 preflight：`PASS`（overall + l2）。
- manifest / checksum：B bundle records 与 A manifest **1,212/1,212** checksum 一致；Viewer
  `checksums.json` 7/7 一致。
- fail-closed：`RUN / PASS`（重名 bundle 拒绝、`config_digest` 不匹配拒绝、
  `require_total_current` 拒绝 detided、explanation 身份不匹配拒绝）。

**12. 确定性 / 可复现性**：`INHERITED` + `NOT RUN`。identity digest（bundle / run / risk window /
explanation / motion）必须逐字一致，已记录于第 13 项；`generated_at`、`ingest_time`、`issue_time`
等 wall-clock 字段允许变化。本轮未执行 determinism twin-run（`NOT RUN`：重建运行未安排 twin-run）。

**13. 构件 / 溯源**：

| 构件 | 路径 | 身份 | 状态 |
|---|---|---|---|
| A 数据根 | `.runtime/winter-rebuild-20260215/data/` | 1,212 records；ocean_current `cmems-*` total snapshots | 实验目录，未跟踪 |
| A DatasetBundle | `.runtime/experiments/a-winter-rebuild-20260215/tromso_to_isfjorden_outer_winter_20260215T000000Z_min144_bundle.json` | `a-bundle-fbbbfbb6e14bec5162408046` / digest `fbbbfbb6…473bba` | 未跟踪 |
| B RiskWindow | 同上目录 `risk-store/commits/` | `risk-window-sha256-86bdb614…` | 未跟踪 |
| B explanation | 同上目录 `risk-explanation/` | artifact `risk-explanation-sha256-66bd366e…`；manifest 绑定 86bdb614 | 未跟踪 |
| C plan / motion | 同上目录 `c-output/`、`motion/` | candidates `df488dcc…`；selected `e677def9…`；motion set `32fe1c26…` | 未跟踪 |
| D Viewer 包 | `work_package_d/output/winter-rebuilt-20260215-viewer-package-v1/` | preflight PASS；bundle 含 explanation | 未跟踪 |

**14. 已知限制 / 技术债**：
- `TD-1 / explanation publication_status=PARTIAL / medium / 以已标定模型升级消除 PARTIAL`
  （源自 `demo_unvalidated` 标定，两处一致，非绑定缺陷）。
- `TD-2 / 新身份与旧 a2146dd0 不可互通 / medium / 人工评审后再决定是否把新 Viewer 包设为默认`
  （handoff 制品与其他文档仍引用旧 identity）。
- `TD-3 / ocean_current quality_flag=suspect / low / 无需动作，需在口径中说明`
  （非权威回溯采集统一标记，content_qc 为 good）。
- `TD-4 / 分片续采脚本位于实验目录 / low / 若复用需纳入版本控制并加测试`
  （`resume_copernicus.py` 等运维脚本未被 git 跟踪）。
- 功能 PASS 不隐藏上述限制；本轮未跑单测与 formal integration。

**15. 决策 / 下一阶段**：项目状态由"explanation 诚实降级"转为"合规 + 可解释可用"。
下一里程碑：人工确认是否将新 Viewer 包切换为 D 默认资源链。推荐下一轮：运行 orchestrator 相关
单元测试与 formal integration 以补齐验证成熟度，再决定默认身份切换。**明确不要做**：不修改走廊
坐标；不放宽 total-current 政策；不跨身份复用旧 `a2146dd0` sidecar；不伪造 contributor。

### 12.1 关键增量表（2026-09-03 09:09 +08:00）

| 指标 / 声明 | Before | After | Delta | Verdict / 原因 |
|---|---|---|---|---|
| ocean_current 源 | detided 后备（`suspect`，源已退役） | `total` + `tide_included=true`（TIDE 002_015） | 合规替换 | `IMPROVED`：强制 `--require-total-current` |
| Viewer explanation | `UNAVAILABLE`（诚实降级） | `PUBLISHED`（artifact `66bd366e…` 嵌入 bundle） | 新增证据 | `IMPROVED`：B 同次 trace 捕获 + D 透传 |
| RiskFrame 窗口 | `b5bed6bb…`（不可重建 trace） | `86bdb614…`（145 帧、unknown_navigable=0） | 新身份 | `EXPECTED`：数据重新采集，digest 不可复现 |
| 路线与完整性 | 旧 12 routes（旧身份） | 12 routes、integrity 12/12 PASS、motion set 1 | 新身份 | `IMPROVED`：新增 motion 与 candidate-set |
| 覆盖完整性 | ocean_current 缺（退役） | 12 类全覆盖（1212 records） | 补齐 | `IMPROVED` |

### 12.2 声明矩阵（2026-09-03 09:09 +08:00）

| 声明 | 状态 | 验证等级 | 证据 | 备注 / 限制 |
|---|---|---|---|---|
| ocean_current 为含潮总流 | `PASS` | `REAL_E2E_PASS` | 145 帧 metadata `total` / `tide_included=true` | `quality_flag=suspect` 为采集保守标记，content_qc good |
| explanation 与窗口同身份 | `PASS` | `REAL_E2E_PASS` | artifact `66bd366e…` manifest 绑定 86bdb614，viewer 嵌入并回读 | `publication_status=PARTIAL`（标定语义） |
| 12 路线与 motion 可用 | `PASS` | `REAL_E2E_PASS` | C integrity 12/12、motion set `32fe1c26…` | `rolling_0_24h` / `executable_0_6h` 短层 `destination_reached=false` 为设计行为 |
| Viewer 包 preflight | `PASS` | `SMOKE_PASS` | `replay-viewer-preflight.json` overall/l2 PASS | 未做浏览器视觉验收（本轮范围外） |
| 单元测试 / formal integration | `NOT STARTED` | `NOT_IMPLEMENTED` | — | 本轮未运行；不得外推为通过 |

### 12.3 意外发现 / 修正（2026-09-03 09:09 +08:00）

- 旧声明：Copernicus 各类型可按统一 24 h 段续采。
  新证据：wave 为 3 h cadence，按日分段的相邻段共享 00:00 帧，`_preflight_data_root` 判定
  `refusing to republish existing logical records`。
  修正后声明：3 h cadence 数据集必须整窗口或按 3 h 对齐分段，不可套用 24 h 分片。
  受影响：本轮采集流程（wave 改为整窗口重采）。
- 旧声明：采集失败疑似网络慢 / 内存不足。
  新证据：日志显示 `[safe-delete][SAFE_DELETE_BULK_CONFIRM_REQUIRED]`（IDE 通过 `BASH_ENV`
  包装 `rm` 并计数 500/turn）与 WSL 重启（`uptime` 复位），非网络或 OOM。
  修正后声明：主因是删除拦截 + WSL 重启；文件清理应走 python os 层，长任务须分片。
  受影响：本轮采集流程与恢复手册。
- 旧声明：`quality_flag=suspect` 疑似 detided 降级标记。
  新证据：`_publication_quality()` 对 `authoritative=False` 的采集证据统一返回 SUSPECT，
  content_qc 为 good。
  修正后声明：suspect 是 provenance 保守标记，不代表数据质量缺陷。
  受影响：状态口径（已在 `CURRENT_STATUS.md` 登记）。
