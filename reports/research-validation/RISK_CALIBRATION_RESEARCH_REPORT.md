---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - EXPERIMENTAL
  - BLOCKED
  - PLANNED
Document Role: SUPPORTING
Scope: Winter B 风险尺度语义、Risk Calibration Shadow Experiment、候选方法比较与后续校准门禁
Canonical For: NO; current phase and next gate remain in current/CURRENT_STATUS.md and current/CURRENT_ROADMAP.md
Branch: research-validation-system
Last Verified: 2026-08-23
Related Canonical Docs:
  - ../../current/CURRENT_STATUS.md
  - ../../current/CURRENT_ROADMAP.md
  - ../../current/decisions/RESEARCH_VALIDATION_DECISIONS.md
  - ../../current/reference/TECH_DEBT.md
---

# Risk Calibration Research 报告

## 1. Executive Summary（2026-08-23 22:01 +08:00）

本轮建立了隔离的 `Risk Calibration Shadow Experiment`：它只读绑定已冻结的 Winter
`bc.risk-frame.v2` committed window，输出 `research.risk-calibration-shadow-comparison.v1`
sidecar，不修改正式 `RiskFrame`、risk formula、weights、`0.2/0.4/0.6/0.8` threshold，
也不馈入 C 或 D。

当前 `risk_score` 的可支持语义是 **weighted normalized hazard index**。正式 L1–L5 是
该 index 的工程离散层，不是事故概率、经过验证的 severity，也不是 navigation-facing
operational action level。下一阶段建议把主校准目标定义为 **operational action level**；若未来
需要概率，应以独立输出和概率校准证据表达。

实际 comparison 只执行了冻结 equal-width baseline 和 fit-only quantile statistical strata。
后者产生更多 L3–L5 只代表相对分布重分层，不是科学改进。Expert rule、Physics constraint
gate、Ordinal calibration 因缺少规则集、逐格 component attribution、船型物理界限和 ordinal
labels，均保持 `BLOCKED`。

```text
SHADOW INFRASTRUCTURE = IMPLEMENTED / UNIT_PASS / REAL_ARTIFACT_DIAGNOSTIC
CURRENT WINTER SPLIT = DIAGNOSTIC_ONLY_NOT_EXTERNAL_CALIBRATION
SCIENTIFIC CALIBRATION = NOT ESTABLISHED
FORMAL WEIGHT / THRESHOLD CHANGE = NOT APPROVED
```

### Key Delta Table（2026-08-23 22:01 +08:00）

| Claim | Before | After / Evidence | Verdict |
|---|---|---|---|
| Shadow runner | NOT_IMPLEMENTED | builder、CLI、config、11 tests | IMPLEMENTED / UNIT_PASS |
| Formal source binding | frame-index 统计 | manifest/window/frame digest、cadence、hard semantics | PASS |
| Statistical candidate | 方案描述 | fit-only comparator 已运行 | EXECUTED_DESCRIPTIVE |
| Expert / Physics / Ordinal | 无充分证据 | blocker 与所需证据显式发布 | BLOCKED |
| Formal RiskFrame / threshold | FROZEN | 未写、未覆盖、未重算 | PRESERVED |

### Claim Matrix（2026-08-23 22:01 +08:00）

| Claim | Status | Validation Level | Limitation |
|---|---|---|---|
| Sidecar 确定性 | PASS | 两次 real-artifact 输出 byte-identical | 单场景 |
| 输入不可变性绑定 | PASS | FAIL_CLOSED_UNIT + REAL_ARTIFACT | 不等于模型校准 |
| 时间/空间样本直接重叠 | 避免 | 6-frame purge、3-row guard | purge 宽度未科学批准 |
| 无 time/space leakage | NOT PROVEN | NOT_VALIDATED | 需独立 ScenarioRunGroup |
| Statistical thresholds 更优 | NOT ESTABLISHED | DESCRIPTIVE_ONLY | 无 labels/outcome |
| Route utility | NOT_EVALUATED | NOT_IMPLEMENTED | C metrics 不是标签 |
| Scientific calibration | NOT ESTABLISHED | BLOCKED | 不批准阈值变更 |

## 2. Scope / Non-Scope（2026-08-23 22:01 +08:00）

Scope：research-only sidecar、冻结源 identity 绑定、风险等级语义、四类 candidate 的证据成熟度、
fit-only statistical comparator，以及 separation、monotonicity、stability、future route utility。

Non-scope：不修改 B formula/weights/normalization/formal threshold/RiskFrame；不运行 RiskBuild、
C、D 或 replay；不以 Viewer 色彩为目标；不把已有 C metrics 当 calibration label。

## 3. Starting Baseline / Current Status（2026-08-23 22:01 +08:00）

| Identity | Value |
|---|---|
| Scenario | `tromso_isfjorden_february_2026_research_v1` |
| DatasetBundle | `a-bundle-a2146dd0adbaa7db77a6beb7` |
| RunContext | `run-441b03c8-d45b-5414-b0e8-b7fd0d990c22` |
| RiskWindow | `risk-window-sha256-b5bed6bb48893e32620710e8c765dc60ec37a2fc384f0c49014b92f0a1c056b2` |
| Grid / cadence | 31×11 / 145 hourly frames |
| Model | `demo_unvalidated_rule_baseline.v2` |
| Formula / level policy | `deterministic_environment_components_v2` / `c_equal_width_floor_v1` |

Winter finite count `31,543`、mean `0.119016`、median `0.106969`、P95 `0.226415`、max
`0.400563`；L1 为 93.069778%。这证明等宽 level 在本场景分辨率较低，不能单独证明其行动
语义错误。

## 4. Git Final State（2026-08-23 22:01 +08:00）

| Repo | Branch | Start HEAD | Delta | Push |
|---|---|---|---|---|
| B | `research-validation-system` | `2d034bf5` | 4 个 shadow 新文件 | NOT PERFORMED |
| governance | `research-validation-system` | `c6e22a60` | report、decision、tech debt | NOT PERFORMED |
| A/C/D/contracts/orchestrator | `research-validation-system` | 见最终 matrix | none | NOT PERFORMED |

B 开始前已有 user-owned `risk_explanation`、README/CHANGELOG/VALIDATION/service 等未提交改动；
governance 同期出现 D risk-explanation canonical 改动。本轮不重置、不覆盖、不混入 calibration
commits。精确 end HEAD、ahead/behind 和 dirty 状态见最终交付回复。

## 5. Filesystem & Resource Safety（2026-08-23 22:01 +08:00）

| Observation | Result |
|---|---|
| Tracked writes | B 4 个新增文件；governance 既有 report/decision/debt |
| Runtime writes | `.runtime/experiments/risk-calibration-shadow-winter-v1-final/**` |
| Frozen artifact writes | NONE |
| Pre-run MemAvailable / shadow peak RSS | 约 5.7 GiB / 106,456 KiB |
| Process swap / heavy pipeline | 0 / NOT RUN |
| Windows host physical free space | UNKNOWN |

旧 runtime comparison 未删除；因 split/provenance 不同，降级为 `SUPERSEDED RUNTIME
DIAGNOSTIC`。最终证据只引用 `...-final/comparison-a.json`。

## 6. Code / Architecture Changes（2026-08-23 22:01 +08:00）

- `calibration_shadow.py`：formal identity/cadence/hard semantics validation、comparison、digest、
  approved-root no-clobber writer。
- `run_risk_calibration_shadow.py`：显式 `--output-root` CLI。
- `risk_calibration_shadow_winter_v1.json`：冻结源 identity、purged split、comparators。
- `test_calibration_shadow.py`：determinism、identity、holdout、hard semantics、cadence、路径安全。

架构保持：shadow module 不进入 `RiskBuildService`、formal store、C 或 D。

## 7. Semantic / Contract Changes（2026-08-23 22:01 +08:00）

### 风险等级语义定义（2026-08-23 22:01 +08:00）

| Concept | 当前支持 | 定义 / 边界 |
|---|---|---|
| Hazard index | YES | normalized components 的 weighted composite |
| Formal L1–L5 | ENGINEERING BASELINE | hazard index 的 equal-width discretization |
| Operational action level | NOT CALIBRATED | 推荐主目标；需专家/行动 labels |
| Severity | NOT CALIBRATED | 需后果或物理严重度定义 |
| Probability | NOT SUPPORTED | score/level 均不能解释为事故概率 |

sidecar 为 `EXPERIMENTAL_UNREGISTERED`，不是 shared contract；没有 Winter-only 字段进入
`bc.risk-frame.v2`。`DATA_UNAVAILABLE != SAFE` 由 `hard_mask/reason/level/confidence` 联合校验。

## 8. Experiments / Candidate Comparison（2026-08-23 22:01 +08:00）

| Candidate | Target semantics | Status | Evidence gate |
|---|---|---|---|
| Equal-width baseline | discretized hazard index | EXECUTED_REFERENCE | frozen control |
| Expert rule | operational action level | BLOCKED | rulebook、专家一致性、适用船型/走廊 |
| Physics gate | non-compensatory severity guard | BLOCKED | component sidecar、approved vessel limits |
| Statistical quantile | relative hazard stratum | EXECUTED_DESCRIPTIVE | 仅描述，非绝对风险 |
| Ordinal calibration | ordinal operational severity/action | BLOCKED | immutable labels、adjudication、external scenarios |

指标：`separation` 仅描述阈值切分后的 score variance/median；`monotonicity` 仅检查 mapping
不下降；`stability` 比较 fit time/spatial blocks 的 threshold range；`route utility` 本轮
`NOT_EVALUATED`，未来检查 route stability、Pareto separation、decision regret 与 fail-closed
success。上述描述指标不能替代 outcome/physical validation。

## 9. Real Artifact Shadow Result（2026-08-23 22:01 +08:00）

### Immutable split 与 leakage controls（2026-08-23 22:01 +08:00）

| Split | Total | Finite | Hard | Time frames | Rows |
|---|---:|---:|---:|---|---|
| fit | 18,018 | 14,742 | 3,276 | `[0,91)` | `[0,18)` |
| validation | 748 | 340 | 408 | `[97,114)` | `[21,25)` |
| test | 825 | 125 | 700 | `[120,145)` | `[28,31)` |
| guard/excluded | 29,854 | 16,336 | 13,518 | purge/cross-regions | guard |

formal `valid_time` 严格 hourly 且与 RiskWindow start/end 对齐。该 split 避免直接重叠，但单一
scenario/run/corridor/vessel 只能是 `DIAGNOSTIC_ONLY_NOT_EXTERNAL_CALIBRATION`。

fit-only quantile thresholds 为：

```text
0.084861 / 0.105463 / 0.122786 / 0.151477
```

| Evidence | Result | Interpretation |
|---|---:|---|
| Validation exact agreement / mean abs delta | 17.65% / 1.544 | 行为差异，不是 improvement |
| Test exact agreement / mean abs delta | 28.00% / 1.760 | test finite 仅 125 |
| Temporal / spatial threshold max range | 0.072931 / 0.033408 | 存在分布敏感性 |
| Test L1/L2/L3/L4/L5 | 35/24/2/14/50 | relative strata 会产生更多高 level |

因此 statistical candidate 只保留为 comparator，不进入 formal threshold proposal。

## 10. Performance（2026-08-23 22:01 +08:00）

| Task | Wall | Peak RSS | Result |
|---|---:|---:|---|
| Real shadow run A | 0.71 s | 106,456 KiB | PASS |
| Real shadow run B | 0.67 s | 106,268 KiB | PASS |
| Targeted 11 tests | 0.13 s | not separately measured | PASS |
| B full pytest | 57.04 s | 408,504 KiB | 90 pass / 1 historical fail |
| B focused（exclude known full-window file） | 12.56 s | 357,428 KiB | 85 pass / 1 warning |

以上是工程观测，不是专业 benchmark；未运行 B RiskBuild、C、D 或 replay。

## 11. Correctness / Validation（2026-08-23 22:01 +08:00）

| Validation | Result | Classification |
|---|---|---|
| py_compile / shadow Ruff | PASS / PASS | SYNTAX/LINT_PASS |
| Shadow targeted tests | 11 passed | UNIT_PASS |
| B full pytest | 90 passed / 1 known default-grid failure | PARTIAL / PRE-EXISTING_FAILURE |
| B focused pytest | 85 passed / 1 ecCodes warning | FOCUSED_PASS |
| B full Ruff | all checks passed | LINT_PASS |
| Governance tests | 11 passed | DOC_CONTRACT_PASS |
| Manifest/index binding | exact SHA/digest/count/order | REAL_ARTIFACT_PASS |
| Canonical frame digest | 145/145 | REAL_ARTIFACT_PASS |
| hard semantics | 49,445 cells checked | FAIL_CLOSED_PASS |
| C/D/replay | NOT RUN | OUT_OF_SCOPE |

full-suite 唯一失败仍是既有 Murmansk default 11×26 grid 的
`allowed_region_has_no_grid_node`；它不经过 shadow module。warning 为本机缺少 ecCodes，相关
archive restart test 仍通过。

## 12. Determinism / Reproducibility（2026-08-23 22:01 +08:00）

两次输出 byte-identical：

```text
artifact_id = risk-calibration-shadow-sha256-e9f9a6299db53728d85fe71d28968c8b8945ad8aa787531823f95bfb4d857892
file_sha256 = 59f15697c9529951f4e9da1f196b0a192a94aec62331d494f376af6e13717cb2
```

identity 绑定 config SHA、producer version、RiskWindow digest、manifest SHA、frame-index SHA、
145-frame set SHA 和 split policy。旧 sidecar 不作为本轮证据。

## 13. Artifacts / Provenance（2026-08-23 22:01 +08:00）

| Artifact | Role | Identity / SHA | Mutated? |
|---|---|---|---|
| Winter RiskWindow | authoritative input | `b5bed6bb...` | NO |
| Formal manifest / frame-index | source binding | `3a711f4c...` / `bc19e22b...` | NO |
| Shadow config | experiment identity | `d3ed5b13...` | new tracked |
| comparison A/B | runtime diagnostic twin | artifact `e9f9a629...` | new runtime |

writer 只允许显式 output root 下 no-clobber create，拒绝 source 内写入、路径逃逸和并发同名
发布；sidecar 不注册进 formal B store。

## 14. Known Limitations / Tech Debt / Unexpected Findings（2026-08-23 22:01 +08:00）

1. 单一 Winter identity 不具 external validity；test finite 仅 125。
2. 缺专家 action、near miss、减速/偏航、船体响应或事故 labels。
3. 缺 approved vessel physics limits；component attribution 尚非正式 artifact。
4. 6-hour/3-row purge 尚无自相关长度证据证明充分。
5. separation/mapping monotonicity 是构造性指标，不能替代外部验证。
6. C 12 candidates 同源且有 geometry 重复，不能当 12 个独立 calibration samples。

Unexpected：独立审查发现初版 runner 未绑定 commit manifest、未完整校验
`hard_mask/confidence`，且 runtime 遗留不同 split policy sidecar。提交前已补齐 fail-closed
binding、no-clobber output 和新增测试；旧文件保留但降级。并行 user-owned risk-explanation
worktree 未被本轮合并或改写。

## 15. Decision / Recommended Next Step（2026-08-23 22:01 +08:00）

1. 冻结 proposal：L1–L5 主目标采用 `operational_action_level`；probability 独立表达。
2. 建 labels：双专家独立标注 + adjudication，记录 vessel/corridor/horizon/action/confidence。
3. 外层按 `ScenarioRunGroup(scenario,run,corridor,vessel)` 留出 test；内层连续 time block +
   spatial block 做 purged validation。
4. 由 B 正式发布 component sidecar，并批准 vessel limits 后再执行 physics gate。
5. 顺序：equal-width control → expert rules → expert+physics → ordinal；quantile 仅作 comparator。
6. labels 和至少两个独立场景通过后，才运行 C shadow route utility 并提交 config/version proposal。
7. 审批前 formal threshold、RiskFrame、C、D 保持不变。

本轮提升的是研究可证伪性和接口隔离，不是视觉红色面积。
