---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: first formal Winter B scientific validation run and Summer/Winter comparison
Canonical/Supporting: Supporting milestone report; canonical status is current/reference/WINTER_SCENARIO_STATUS.md
Branch: research-validation-system
Last Verified: 2026-08-23
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
