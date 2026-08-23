---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - PLANNED
Document Role: SUPPORTING
Scope: Winter B risk-score semantics, observed distribution, threshold validity, component observability, and calibration research options
Canonical For: NO; current phase and next gate remain in current/CURRENT_STATUS.md and current/CURRENT_ROADMAP.md
Branch: research-validation-system
Last Verified: 2026-08-23
Related Canonical Docs:
  - ../../current/CURRENT_STATUS.md
  - ../../current/CURRENT_ROADMAP.md
  - ../../current/reference/TECH_DEBT.md
---

# Risk Calibration Research 报告

## 1. Executive Summary（2026-08-23 20:45 +08:00）

当前 `demo_unvalidated_rule_baseline.v2` 的 `risk_score` 是 11 个环境分量经固定区间归一化后
的加权和，不是事故概率、遇险概率、适航概率或经过历史航行结果标定的严重度。因而
`0.1`、`0.2`、`0.3` 只能解释为当前工程规则下约 10%、20%、30% 的加权归一化危险负荷；
它们没有独立的物理单位，也不能直接解释为 10%、20%、30% 的事故风险。

对现有 145 帧 Winter `bc.risk-frame.v2` 的只读复核确认：31,543 个 finite cells 的均值为
`0.119016`、中位数为 `0.106969`、P95 为 `0.226415`、最大值为 `0.400563`；等宽阈值
`0.2/0.4/0.6/0.8` 将其中 93.069778% 映射为 L1、6.927052% 映射为 L2，仅 1 个 cell
进入 L3，L4/L5 为 0。该结果证明当前 level 显示分辨率与本场景 score 分布不匹配，但不能
单独证明阈值错误，因为当前场景可能确实以中低复合风险为主。

科学结论是：**当前风险尺度具有确定性、单调性和工程可比较性，但科学标定有效性尚未建立**。
加权平均还存在单因子稀释风险：wave 即使达到配置饱和值，单独最大只贡献 `0.13`，wind
单独最大只贡献 `0.10`，均仍落在 L1；只有多个危险因子同地同刻叠加，或高权重 ice
因子达到高值，才容易跨越 `0.2`。这与“极端单项危险是否应触发更高行动等级”并非同一问题。

### Key Delta Table（2026-08-23 20:45 +08:00）

| Claim | Before | After / Evidence | Verdict |
|---|---|---|---|
| `risk_score` 科学含义 | 未正式解释 | weighted normalized hazard index；不是 probability | CONFIRMED |
| `0.2/0.4/0.6/0.8` 阈值 | 当前实现 | equal-width engineering bins，无标定证据 | SCIENTIFIC VALIDITY NOT ESTABLISHED |
| Winter finite L1 | 约 93% | 29,357 / 31,543 = 93.069778% | CONFIRMED |
| 高风险响应 | 视觉上不明显 | 145/145 帧存在 `>=0.3`；仅 1 帧/1 cell `>=0.4` | CONFIRMED / COMPRESSED |
| 11 分量实际贡献 | 未知 | RiskFrame 不含 contribution；只能确认结构权重上限 | NOT OBSERVABLE FROM CURRENT ARTIFACT |
| Calibration method | 未决定 | 建立五类候选及证据门禁 | PLANNED, NOT SELECTED |
| B weights / thresholds / artifacts | 冻结 | 零修改、零重算 | PRESERVED |

### Claim Matrix（2026-08-23 20:45 +08:00）

| Claim | Status | Validation Level | Evidence | Limitation |
|---|---|---|---|---|
| 公式是 11 分量归一化加权和 | PASS | CODE_AUDIT | B config + `_demo_unvalidated_risk` | 未评价权重科学性 |
| Winter 分布统计可复现 | PASS | REAL_ARTIFACT_AUDIT | 145 个既有 RiskFrame 只读扫描 | 未重建 artifact |
| unknown 没有被当成 safe | PASS | AUTHORITATIVE_PASS | NaN/confidence=0/hard + `DATA_UNAVAILABLE` | 来源 footprint 仍有缺口 |
| 当前等级阈值具科学有效性 | FAIL | NOT_VALIDATED | 无 expert/outcome calibration evidence | 仅工程 baseline |
| 极端单因子会触发高等级 | NOT ESTABLISHED | STRUCTURAL_AUDIT | 单因子最大贡献受 weight 限制 | 缺逐格 contributor |
| C 对现有 risk variation 有响应 | PASS | REAL_E2E_PASS | low-risk 与 fastest metrics 有差异 | 不等于 B 已校准 |
| 本轮改变 B 行为 | NO | FROZEN_BASELINE | B Git tree 与 artifacts 未修改 | N/A |

## 2. Scope / Non-Scope（2026-08-23 20:45 +08:00）

Scope：只读检查 B 配置与实现、既有 Winter RiskFrame、既有 raw/source 统计、现有 C 路线
metrics 与已有 risk-explanation proposal；计算 score 分布、percentile、level、纬度带和逐帧
统计；提出 calibration research 路径。

Non-scope：不修改 B weights、normalization bounds、thresholds、risk formula、RiskFrame、C/D；
不重新生成 A/B/C/D artifact；不以 Viewer 视觉效果为优化目标；不把统计 percentile 直接批准为
新 operational threshold；不声称已完成事故概率或安全等级标定。

## 3. Starting Baseline / Current Status（2026-08-23 20:45 +08:00）

| Identity / Configuration | Value |
|---|---|
| Scenario | `tromso_isfjorden_february_2026_research_v1` |
| DatasetBundle | `a-bundle-a2146dd0adbaa7db77a6beb7` |
| RunContext | `run-441b03c8-d45b-5414-b0e8-b7fd0d990c22` |
| RiskWindow | `risk-window-sha256-b5bed6bb48893e32620710e8c765dc60ec37a2fc384f0c49014b92f0a1c056b2` |
| Risk schema | `bc.risk-frame.v2` |
| Grid / cadence | 31×11 / 145 hourly frames |
| Model | `demo_unvalidated_rule_baseline.v2` |
| Calibration status | `demo_unvalidated` |
| Formula | `deterministic_environment_components_v2` |
| Level policy | `c_equal_width_floor_v1` |
| Hard policy | `land_sea_mask_plus_unknown_ice_free_v1` |

`formal artifact` 表示 schema、identity、provenance、时序和发布过程通过正式门禁；它不表示模型
已经 scientific calibration。当前 B 可以支持重复研究和 route tradeoff 实验，但不能把 level
解释为经实船事故、专家行动等级或物理危险界限验证的分类。

## 4. Git Final State（2026-08-23 20:45 +08:00）

| Repo | Branch | Start HEAD | End HEAD | Start tracking | Code change | Push |
|---|---|---|---|---|---|---|
| governance | `research-validation-system` | `cf4fb831` | 本报告 commit | equal to origin | docs only | NOT PERFORMED |
| contracts | `research-validation-system` | `c19e910f` | unchanged | equal to origin | none | NOT PERFORMED |
| orchestrator | `research-validation-system` | `9d29ad5c` | unchanged | equal to origin | none | NOT PERFORMED |
| A | `research-validation-system` | `b40c689f` | unchanged | equal to origin | none | NOT PERFORMED |
| B | `research-validation-system` | `2d034bf5` | unchanged | equal to origin | none | NOT PERFORMED |
| C | `research-validation-system` | `8d906950` | unchanged | equal to origin | none | NOT PERFORMED |
| D | `research-validation-system` | `69e84853` | unchanged | equal to origin | none | NOT PERFORMED |

本报告不写自引用 commit hash；最终交付回复报告 governance 精确 end HEAD、ahead/behind 与
working tree。未执行 push、merge、rebase 或 reset。

## 5. Filesystem & Resource Safety（2026-08-23 20:45 +08:00）

| Observation | Result |
|---|---|
| Active writes | governance docs；`.runtime/risk-calibration-research/**`；`.runtime/test-logs/**` |
| Frozen artifact writes | NONE |
| Initial / final MemAvailable | 约 4.2 GiB / 4.1 GiB |
| Initial / final swap used | 34 MiB / 34 MiB |
| Analysis peak RSS | 20,828 KiB |
| B full pytest peak RSS | 407,072 KiB |
| B focused pytest peak RSS | 357,484 KiB |
| OOM / process swap | 0 / 0 |
| Heavy replay / artifact regeneration | NOT RUN |
| Windows host physical free space | UNKNOWN；`df` 仅反映 WSL VHD 逻辑空间 |

## 6. Code / Architecture Changes（2026-08-23 20:45 +08:00）

本轮没有 production code 或 architecture change。新增内容仅为 supporting research report，
并把其入口同步到 canonical documentation index/status/roadmap。只读分析脚本与统计 JSON 位于
`.runtime/risk-calibration-research/`，不进入 Git，也不成为生产依赖。

权属保持：B 继续拥有 risk meaning；C 消费正式 RiskFrame；Orchestrator 投影；D 只展示。

## 7. Semantic / Contract Changes and Problem（2026-08-23 20:45 +08:00）

### Risk score meaning（2026-08-23 20:45 +08:00）

实现可写为：

```text
risk_score = clip(sum(weight_i * normalized_component_i), 0, 1)
```

11 个 weight 之和为 1，每个 component 通过 `identity`、`absolute`、`vector_magnitude` 或
`inverse_linear` 变换到 `[0,1]`。因此：

| Score | 当前可支持解释 | 当前不可支持解释 |
|---:|---|---|
| 0.1 | 当前规则下 10% weighted normalized hazard load；L1 | 10% 事故概率、绝对安全 |
| 0.2 | L1/L2 边界，实际实现落入 L2 | 经验证的操作禁限线 |
| 0.3 | 当前规则下 30% weighted load；L2 | 30% 遇险概率或严重度 |

### Threshold validity（2026-08-23 20:45 +08:00）

当前映射为 `clip(floor(risk_score*5)+1,1,5)`：`[0,.2)→L1`、`[.2,.4)→L2`、
`[.4,.6)→L3`、`[.6,.8)→L4`、`[.8,1]→L5`。其工程优点是简单、确定、跨场景固定；
科学缺口是没有 evidence 证明这些边界对应专家行动、实船结果、物理危险点或统计 outcome。

本轮不改变 `bc.risk-frame.v2`、level policy 或任何 shared contract，semantic delta 为 `NONE`。

## 8. Experiments / Calibration Options（2026-08-23 20:45 +08:00）

| Option | 能回答的问题 | 优点 | 主要风险 / 证据门槛 | 本轮决定 |
|---|---|---|---|---|
| Expert rule calibration | 哪些组合应触发行动等级 | 可编码航海知识与 fail-closed gate | 专家一致性、船型/海区迁移性 | 候选；需 Delphi/双盲复核 |
| Historical voyage/outcome | score 是否预测减速、偏航、事故/near miss | 可建立外部效度 | 标签稀缺、选择偏差、事故极不平衡 | 优先数据建设 |
| Statistical percentile mapping | 当前分布如何分层 | 快速、可做场景内可视分析 | 每个数据集强制均衡，破坏绝对跨场景含义 | 仅 diagnostic baseline |
| Machine-learning calibration | 从 features/score 到 outcome probability/ordinal level | 可拟合非线性与交互 | 需足量独立标签、漂移监测、可解释和校准评估 | 后置候选 |
| Physics constraints | 单因子极端是否必须 non-compensatory | 可保证单调、安全边界 | 需要船型/载况/海况物理依据 | 与专家规则共同评估 |

Winter empirical quintile edges 为 `0.081311 / 0.098550 / 0.115074 / 0.142084`。它们证明
`0.2` 已位于 Winter finite distribution 的高尾部，却不能直接替换正式 thresholds；若直接使用
quintile，任意平静场景也会固定产生 20% “L5”，从而失去绝对风险含义。

建议研究设计将现行等宽 policy 作为 frozen control，并在新 identity 下运行 shadow calibration；
所有候选先输出对比 sidecar，不覆盖既有 RiskFrame。

## 9. Authoritative Run / Real Validation and Evidence（2026-08-23 20:45 +08:00）

### Distribution（2026-08-23 20:45 +08:00）

| Statistic | Winter finite risk |
|---|---:|
| count | 31,543 |
| min / P10 / P25 | 0.035493 / 0.072510 / 0.085331 |
| P50 / mean | 0.106969 / 0.119016 |
| P75 / P90 / P95 | 0.132515 / 0.179519 / 0.226415 |
| P99 / max | 0.335272 / 0.400563 |

| Level | Count | Finite share |
|---|---:|---:|
| L1 | 29,357 | 93.069778% |
| L2 | 2,185 | 6.927052% |
| L3 | 1 | 0.003170% |
| L4 | 0 | 0% |
| L5 | 0 | 0% |

145/145 帧均存在 `risk_score >= 0.3` 的 finite cell；只有
`2026-02-15T18:00Z` 存在一个 `>=0.4` cell，坐标约 `(78.7667N, 22.0E)`，值为
`0.400563`。逐帧平均最高为 `0.163581`（`2026-02-17T00:00Z`），最低为 `0.089260`
（`2026-02-15T14:00Z`）。这说明风险不是时空常量，但等宽 level 丢失了大量 L1 内部差异。

### Spatial evidence（2026-08-23 20:45 +08:00）

| Latitude band | Mean | P95 | Max | `>=0.2` share |
|---|---:|---:|---:|---:|
| 68.5–72N | 0.113109 | 0.202057 | 0.316830 | 5.22% |
| 72–76N | 0.120398 | 0.224317 | 0.365217 | 6.31% |
| 76–79.5N | 0.128635 | 0.335538 | 0.400563 | 12.77% |

该纬带分层是描述性证据，不控制海陆比例、数据 availability、时刻或各环境变量，因此不能
解释为纬度造成风险上升。

### Extreme-event response and component contribution（2026-08-23 20:45 +08:00）

| Component | Weight / 最大结构贡献 | Saturation definition | Current evidence |
|---|---:|---|---|
| ice concentration | 0.24 | 1.0 | raw max 1.0；逐格贡献未发布 |
| ice thickness | 0.14 | 3 m | raw max 0.817 m；逐格贡献未发布 |
| ice type | 0.05 | class value 4 | raw max 2；逐格贡献未发布 |
| ice edge | 0.02 | 1 | raw max 1；逐格贡献未发布 |
| ice drift speed | 0.06 | 1.5 m/s | raw vector components 存在；逐格 magnitude/contribution 未发布 |
| wave height | 0.13 | 8 m | raw max 8.090 m；source 层可达 saturation |
| ocean current speed | 0.07 | 2 m/s | raw vector components 存在；逐格贡献未发布 |
| wind speed | 0.10 | 30 m/s | raw u/v extrema 存在；同格 magnitude/contribution 未发布 |
| freezing deficit | 0.05 | 243.15 K → 1 | raw min 233.876 K；source 层可达 saturation |
| visibility deficit | 0.10 | 0 m → 1 | raw min 46.383 m；接近 saturation |
| water level magnitude | 0.04 | 3 m | raw magnitude max 0.821 m |

表中的“最大结构贡献”是 config weight，不是本次 Winter 实际贡献占比。现有 RiskFrame 不包含
component arrays 或 `contribution_i`，无法只读恢复某格点的精确分解；强行用 raw extrema
相乘会破坏时空共址关系。已有 `risk-explanation.v1` 仍是 DRAFT，producer 未实现。

结构上，单独饱和的 wave 只贡献 0.13、wind 只贡献 0.10，仍是 L1；ice concentration
单独饱和贡献 0.24，可进入 L2。ice family 五项权重合计 0.51，但只有同格同刻共同达到高值
才可能接近该贡献。这是“weighted-average compensation”研究风险，不是已证实模型缺陷。

## 10. Performance（2026-08-23 20:45 +08:00）

| Task | Wall time | Peak RSS | Note |
|---|---:|---:|---|
| Existing RiskFrame read-only scan | 0.13 s | 20,828 KiB | 145 JSON frames；无 artifact write |
| B full existing pytest | 54.38 s | 407,072 KiB | 68 pass / 1 known fail |
| B focused existing pytest | 约 10.31 s command wall；pytest 9.25 s | 357,484 KiB | 63 pass / 1 warning |
| Governance tests | 0.08 s | not separately measured | 11 pass |

以上是本轮工程观测，不是专业 benchmark。未运行 B RiskBuild、C planning、Viewer、replay 或
artifact regeneration；因此没有新的模型生成性能结论。

## 11. Correctness / Validation（2026-08-23 20:45 +08:00）

| Validation | Result | Classification |
|---|---|---|
| Existing Winter RiskFrame scan | 145/145 read；identity matches | REAL_ARTIFACT_AUDIT_PASS |
| B full existing tests | 68 passed，1 failed，1 warning | PARTIAL / PRE-EXISTING FAILURE |
| Known failure | `allowed_region_has_no_grid_node` in A→B→C default-grid integration | OUT OF SCOPE / UNCHANGED |
| B existing tests excluding known full-window test file | 63 passed，1 warning | UNIT/FOCUSED_PASS |
| B Ruff | all checks passed | PASS |
| Governance tests | 11 passed | PASS |
| Frozen RiskFrame aggregate hash | `99040d14...1a2f990` | RECORDED / UNCHANGED BY READ-ONLY SCAN |

Warning 为本机缺少 ecCodes 导致 `cfgrib` backend plugin load warning；相关 archive restart test
仍通过。本轮没有新增 test 或代码，因此不把已知 integration failure 归因于 calibration audit。

## 12. Determinism / Reproducibility（2026-08-23 20:45 +08:00）

统计输入固定为 committed RiskWindow，frame index SHA-256 为
`bc19e22b9249971cf67372161be8671abc9312833ed42b57bb7f788d4bf77cce`；145 个 frame
文件按 `frame_ids` 顺序读取，聚合 frame-content hash 为
`99040d1457a2e00f65bd66598b95169be8a58aae9d395156d5ba093cf1a2f990`。

分析只使用 Python 标准库、确定 percentile 线性插值和固定纬度带；输出保存在
`.runtime/risk-calibration-research/winter-risk-statistics.json`。未执行 RiskBuild，故本轮不新增
RiskFrame producer determinism claim；既有 formal committed window 作为输入事实继承。

## 13. Artifacts / Provenance（2026-08-23 20:45 +08:00）

| Artifact / Evidence | Role | Mutated? |
|---|---|---|
| Winter committed RiskWindow | authoritative input | NO |
| B model config | formula/weights/bounds evidence | NO |
| B service implementation | transform/level/fail-closed evidence | NO |
| Existing pipeline audit | raw source and C route evidence | NO |
| `.runtime/.../winter-risk-statistics.json` | reproducible supporting analysis | new runtime only |
| `RISK_CALIBRATION_RESEARCH_REPORT.md` | supporting research decision evidence | new tracked report |

现有 C full-voyage 路线对比为：low-risk 相比 fastest，average risk 低 3.813%、maximum risk
低 20.611%、integrated risk 低 3.283%，代价是 distance 增 0.783%、ETA 增 0.551%。它证明
C 对当前 risk variation 有响应，但不证明 B score 已具 outcome calibration。

## 14. Known Limitations / Tech Debt / Limitations（2026-08-23 20:45 +08:00）

1. 没有事故、near miss、船长行动、减速、偏航或船体响应标签，无法建立外部效度。
2. 当前 RiskFrame 不发布逐格 component contribution；实际 11 分量贡献比例为
   `NOT_AVAILABLE`，只有结构 weight 可审计。
3. Winter 单场景、单 corridor、单 vessel 不能支持跨季节、跨海区、跨船型 threshold 结论。
4. Summer/Winter 数据源体系并非完全同质，季节差异仍是 observational comparison。
5. Equal-width level 丢失 L1 内连续差异；percentile level 又会牺牲绝对可比性。
6. Weighted average 允许因子间补偿；是否应增加 extreme single-factor gate 必须先取得物理和
   专家证据，不能由视觉需求决定。
7. B 全套现有 tests 仍有一个 default-grid/corridor integration failure；本轮未改 C 或测试假设。

### Unexpected Findings / Corrections（2026-08-23 20:45 +08:00）

- “L1 占绝大多数”不等于场内没有梯度：所有 145 帧都有 `>=0.3` cell，北部 P95 是南部的
  约 1.66 倍；主要信息损失发生在 level discretization。
- raw source 中 wave、freezing deficit、visibility 存在接近或达到配置 saturation 的极值，
  但最终 score 仍低，提示需要研究共址、权重稀释与 availability，而非先改颜色。
- 旧风险管线审计中的“当前 Viewer 为 Summer”是当时事实；当前 canonical status 已记录
  Winter combined Viewer REAL_E2E_PASS。本报告只审计 B calibration，不回写历史报告。

## 15. Decision / Recommended Next Step（2026-08-23 20:45 +08:00）

最终 verdict：

```text
CURRENT RISK SCALE = DETERMINISTIC ENGINEERING BASELINE
SCIENTIFIC CALIBRATION = NOT ESTABLISHED
WEIGHT / THRESHOLD CHANGE = NOT APPROVED
```

建议下一 gate 不是直接选定某一种 calibration method，而是建立可证伪的 calibration protocol：

1. 先定义 level 的 operational target：专家行动等级、物理危险类别、ordinal severity，或
   outcome probability；一个版本只允许一种主语义。
2. 建立 immutable calibration dataset：覆盖平静、普通冬季、极端冰/浪/风场景，并按 voyage、
   time block、corridor、vessel 分组切分，避免时空泄漏。
3. 由 B producer 在 shadow mode 发布逐格 normalized component 与 additive contribution
   sidecar；不从 D 反算，也不覆盖 `bc.risk-frame.v2`。
4. 先评估 expert + physics constraints 与现行 baseline；percentile mapping 只作为描述性
   comparator。若有足够 outcome labels，再评估 ordinal/statistical/ML calibration。
5. 验收指标按目标语义选择：ordinal confusion 和 cost-weighted error；若输出概率，再使用
   reliability curve、Brier score、ECE；同时检查 monotonicity、OOD fail-closed、route decision
   utility 与 route stability。
6. 任何候选使用新 config identity/version 做 shadow comparison，经专家与实验评审批准后才可
   形成 contract/config change proposal；旧 Winter/Summer artifacts 保持冻结。

与 SY-202607“面向航行应用的风险评估与导航决策方法”对齐时，应展示真实证据链：
`environment → calibrated/qualified risk evidence → route tradeoff → navigation decision`。
当前系统已证明 environment output change 和 route response；下一研究价值是把 risk level 从
可重复工程指数提升为可解释、可验证、与航行行动相关的量，而不是制造更多红色区域。
