# Temporal Semantics Audit & Simulation-Time Architecture（2026-08-17）

> 状态：**AUDITED / DOCUMENTED（无 correctness blocker）**
> 范围：A/B/C/D/Orchestrator/Frozen/Live/Viewer 全部时间字段与因果语义。
> 本轮只做审计、时间模型与文档；未开发播放器、未修改跨包合同、
> 未重生成任何 frozen baseline。

## 1. Executive Summary

项目已经存在完整、且大部分实现良好的一组时间语义，核心不变量“可见性用
`issue_time`、环境时刻用 `valid_time`、知识截止用 `knowledge_as_of`”在
A/B/C 正式路径中均有代码强制。审计没有发现“把 `valid_time` 当可见性”或
“今天下载的历史数据被当作当时已发布预测”的 correctness bug。

但审计发现四个需要记录的结构性 gap：

1. **当前 145 risk frames 是“固定知识快照下的 145 个 valid_time 帧”，不是
   145 个 simulation tick 的滚动重算**，因此不能直接当播放器帧；
2. **`knowledge_as_of == simulation_time` 只是文档/测试级约束**，
   `frozen_forecast` 模式只强制 `as_of <= start`，没有硬编码相等；
3. **D/Viewer 丢失时间维度**：demo-state 只保留 risk frame `valid_time`，
   不保留 `as_of_time`/`scenario_mode`，Viewer 无法区分 CAUSAL 与
   RETROSPECTIVE；
4. **B 没有显式 `current/+6h/+12h/+24h` horizon 字段**，预测时界隐含在
   valid_time 轴上（lead 信息只在 A sidecar 中）。

这些是下一阶段 Simulation-clock replay 设计前必须补的语义，但不是当前合同的
正确性 blocker。

## 2. Why This Audit Was Needed

“145-frame playback”“+6h replanning”“Frame initial / Frame replan”等说法容易
让人误以为系统已经在模拟时钟上滚动重算。本轮需要先证明每个时间字段的真实
含义，否则动态 Viewer 会把：

- 固定知识快照的 valid_time 轴误当 simulation tick；
- 同一 knowledge 下的 +6h departure 重规划误当数据刷新；
- wall-clock generated_at 误当模拟时间。

## 3. Time Domains

| 域 | 描述 | 典型字段 |
|---|---|---|
| T1 Environmental / Valid Time | 数据描述或预测有效的真实/模拟环境时刻 | `valid_time` |
| T2 Knowledge / Availability Time | 系统从何时起被允许知道某数据 | `issue_time`、`knowledge_as_of`、`observed_at`、`ingest_time`、retrieval 证据 |
| T3 Forecast Model Time | 预测参考时刻与 lead | `forecast_reference_time`、`forecast_lead_hours` |
| T4 Simulation Time | 历史回放/仿真当前推进时刻 | `SimulationClock.current_time`、`simulation_start/end`、C `start_time` |
| T5 B Prediction Time | B 在哪个知识边界生成风险帧（当前无 per-horizon 字段） | `RiskFrame.as_of_time`（= knowledge_as_of）、`valid_time` |
| T6 C Planning Time | 规划参考、出发、ETA、采样时刻、time bucket | `start_time`、`eta`、`eta_hours`、`time_bucket` |
| T7 Replanning Time | 重规划触发与观察时刻 | `replan_time`、`ReplanObservation.observed_at/risk_valid_time` |
| T8 Ship / Voyage Time | 航线执行时间 | waypoint `eta`（绝对 UTC）、`eta_hours`（相对时长） |
| T9 Artifact / Provenance Time | 制品生成、运行创建、发布时刻 | `generated_at`、`created_at`、`orchestrator_generated_at` |
| T10 Wall-clock / Execution Time | 机器真实运行时间 | heartbeat、`elapsed`、`timeout`、`compute_ms` |

## 4. Canonical Time Glossary

| Canonical concept | Existing field(s) | Owner | UTC? | Abs/Rel | Domain | Meaning | Source of truth | Causal? | Persisted? |
|---|---|---|---|---|---|---|---|---|---|
| source issue / availability gate | `issue_time`（A record / bundle / sidecar / SourceReference） | A | 是 | 绝对 | T2 | 从该 UTC 时刻起允许交给模拟系统；证据模型驱动 | manifest + sidecar evidence | 是（门禁） | 是 |
| environment / forecast valid time | `valid_time` | A/B/C | 是 | 绝对 | T1/T3 | 数据描述或预测有效的环境时刻 | record / RiskFrame | 否（不代表可知） | 是 |
| evidence observation time | `observed_at` | A | 是 | 绝对 | T2/T10 | 证据被观察到/采集到的时刻 | issue_time_evidence | 否 | 是 |
| A registration time | `ingest_time` | A | 是 | 绝对 | T2/T10 | A 实际登记时刻（审计用） | manifest | 否 | 是 |
| knowledge cutoff | `knowledge_as_of`（bundle.as_of_time / PreparedWindow.as_of_time / B envelope / RiskFrame.as_of_time / C request.as_of_time） | A→B→C | 是 | 绝对 | T2/T5 | 本次计算允许知道的信息截止 | bundle `as_of_time`（= 最大 issue_time，orchestrator intake 强制） | 是 | 是 |
| simulation time | `SimulationClock.current_time`、RunContext `simulation_start/end` | A/orchestrator | 是 | 绝对 | T4 | 仿真当前推进时刻；正式入口要求 == bundle.requested_start | SimulationClock | 因果模式下 == knowledge_as_of | 运行态 |
| forecast reference time | `forecast_reference_time`（sidecar metadata） | A | 是 | 绝对 | T3 | 预测 cycle/参考时刻 | sidecar | 否 | 是 |
| forecast lead | `forecast_lead_hours`（sidecar metadata） | A | n/a | 相对 | T3 | 参考时刻之后的预测步长 | sidecar | 否 | 是 |
| B prediction as-of | `RiskFrame.as_of_time`（= build 的 knowledge_as_of） | B | 是 | 绝对 | T5 | 该风险帧建立在哪个知识边界上；**不是**源 issue_time | BInputEnvelope | 是 | 是 |
| C planning departure | RoutePlan `start_time`（= service request.start_time） | C | 是 | 绝对 | T6 | 路线出发/规划参考时刻 | RunContext.simulation_start / +6h | 是（因果下） | 是 |
| waypoint timestamp | Waypoint `eta` | C | 是 | 绝对 | T6/T8 | 到达该 waypoint 的绝对 UTC 时刻 | 搜索累积 travel | 否 | 是 |
| voyage duration | `eta_hours` | C | n/a | 相对 | T8 | 出发到终点的航行时长 | 搜索累积 | 否 | 是 |
| time bucket | `time_bucket`（A* state） | C | n/a | 相对出发 | T6 | `elapsed // 60min`，非绝对模拟时间 | planner | 否 | 运行态 |
| replan time | `replan_time = simulation_start + replan_after_hours` | orchestrator | 是 | 绝对 | T7 | 正式 +6h 重规划触发/出发时刻 | execution-spec | 否 | 是（run-report） |
| replan observation | `observed_at` / `risk_valid_time` / `data_revision` / `risk_revision` | C/orchestrator | 是 | 绝对 | T7 | 触发评估输入 | service.py | 否 | run-report |
| artifact wall time | `generated_at` / `created_at` | A/B/C/orchestrator | 是 | 绝对 | T9/T10 | 生成/创建墙钟；**禁止用于因果门禁** | utc_now / spec | 否 | 是 |
| execution wall time | heartbeat / elapsed / timeout / compute_ms | all | 是 | 相对 | T10 | 机器执行时间 | worker/watchdog | 否 | 运行态 |
| presentation frame index | `frame_index`（D spatial） | D | n/a | 相对 | T1 | risk 帧在 demo-state 中的下标（0/6） | D build | 否 | 是 |

## 5. A Time Semantics

### 5.1 issue_time evidence model（IMPLEMENTED）

- `IssueTimeMethod`：`explicit_catalog` / `http_last_modified` /
  `dataset_attribute` / `copernicus_service_sync` / `conservative_retrieval`；
- `IssueTimeEvidence`：`issue_time, method, authority, reference, observed_at,
  raw_value, authoritative`；`copernicus_service_sync` 与
  `conservative_retrieval` 构造时强制 `authoritative=False`；
- 合理性检查：`issue_time <= observed_at + 10min`；动态产品在 valid-time
  范围前后 45 天内；
- sidecar 一致性：`_validate_issue_time_evidence` 强制
  `sidecar.metadata.issue_time_evidence.issue_time == sidecar.issue_time`，
  且非权威方法不能配 `quality_flag=good`；
- 质量合成：availability evidence 与 content QC 分开，最终
  `quality_flag = worse(availability, content)`（`suspect != known-wrong`）。

### 5.2 可见性执行（IMPLEMENTED）

- manifest 查询：`valid_time BETWEEN ? AND ? AND issue_time <= as_of`；
- A prefetch：`list_available/get_latest_before/get_bracketing(..., as_of=)`，
  `_validated_source_record` 对每条候选强制 `issue_time <= as_of`；
- AB cache：`reset_generation(generation_id, simulation_time=...)` 只把
  `issue_time <= 新时刻` 的 static 帧挂到新代次；
- bundle：`as_of_time` 必须等于所选记录最大 issue_time（orchestrator intake
  强制），且任何 record `issue_time > as_of` 拒绝。

### 5.3 forecast reference / lead（IMPLEMENTED，条件性）

sidecar metadata 中 `forecast_reference_time` 与 `forecast_lead_hours` 必须
同时出现或同时缺失；出现时强制
`valid_time == forecast_reference_time + forecast_lead_hours`。真实 GFS 记录
示例（Scenario B）：reference `2026-08-11T06:00:00Z`、lead `0.0`、
valid `2026-08-11T06:00:00Z`、issue `2026-08-11T11:49:03.736798Z`
（`conservative_retrieval`、`authoritative=false`、`quality_flag=suspect`）。

### 5.4 simulation clock（IMPLEMENTED）

- `SimulationClock(start, speed, running)`：`play/pause/tick/seek`；
  `seek` 递增 generation 并通知订阅者；tick 用 real_elapsed×speed，不把 UI
  墙钟写入模型时间；
- 正式入口要求：`prepare_window_for_b` 的 `start_time == clock.current_time`；
  `resolve_dataset_bundle_for_b` 要求 `clock.current_time == bundle.requested_start`；
- 正式运行中时钟只被推进一次：`_advance_clock_without_seek(clock, +6h)`，
  不 bump generation。

### 5.5 causal vs retrospective（PARTIAL）

- `frozen_forecast`：contracts `context.py`、B `context.py`、C
  `service.py` 均强制 `as_of_time <= simulation_start`（“不晚于”）；
- `retrospective_best_estimate`：允许 `knowledge_as_of > simulation_start`，
  且必须显式保存在 RunContext `scenario_mode`；
- 文档（AB_INTERFACE §11）写明因果模式 `PreparedWindow.as_of_time ==
  模拟时钟`；**代码没有硬编码相等**，由调用方/测试保证 → GAP。

## 6. issue_time Evidence Model（与文档一致性）

文档、schema、代码三者一致：

| 文档声明 | 代码位置 | 一致性 |
|---|---|---|
| 5 种 method | `issue_time.py::IssueTimeMethod` | 一致 |
| evidence 7 字段 | `IssueTimeEvidence` + `to_dict()` | 一致 |
| sidecar.issue_time == evidence.issue_time | `ingestion.py::_validate_issue_time_evidence` | 一致（有测试） |
| ARCO = 非权威 | `IssueTimeEvidence.__post_init__` 强制 | 一致 |
| GFS conservative retrieval = suspect | 实际记录 quality_flag=suspect | 一致 |
| evidence 持久化 | manifest `metadata_json` | 一致 |

## 7. knowledge_as_of / simulation_time

真实 frozen 数据（Scenario A / B）：

- `simulation_start = 2026-08-11T06:00:00Z`；
- `knowledge_as_of = bundle.as_of_time`：A = `2026-08-16T10:02:51.780511Z`，
  B = `2026-08-15T09:37:34.830829Z`；
- 即当前 Demo 两个场景都是 **retrospective_best_estimate**：
  `knowledge_as_of > simulation_start`；
- 全部 145 risk frames 的 `as_of_time` 都等于该固定值；
- 因此当前 Demo **不是** causal replay：模拟时钟停在 06:00Z（初始）与
  12:00Z（重规划），知识截止始终是后来下载完成时刻。

## 8. Forecast Reference / Lead / Valid Time

- A 层：`forecast_reference_time + forecast_lead_hours == valid_time`
  在 sidecar 摄取时强制（对带该元数据的产品）；
- B 层：`RiskFrame` 不携带 lead；B 只消费可见的 A 支撑帧并按目标 valid_time
  插值/nearest；
- C 层：按 ETA 的绝对时间采样 risk 帧，不关心 lead；
- 当前合同没有把 `lead` 作为 BC/CD 公共字段传播 → schema gap（建议下一轮
  在 SimulationSnapshot 中补 `forecast_reference_time/forecast_lead_hours`）。

## 9. B Time Semantics

### 9.1 145 frames 的真实结构

`RiskBuildService.build_window()` 对**一个固定的 BInputEnvelope**（固定
knowledge_as_of、固定 generation、固定 RunContext 窗口）一次性生成
`(end-start)/1h + 1` 帧：

- 每帧 `valid_time = requested_start + index*1h`；
- 每帧 `as_of_time = envelope.knowledge_as_of`（全部相同）；
- 每帧 `generated_at` 相同（单次 build 的墙钟）；
- 每帧独立做 `_resolve_field`：只使用 `issue_time <= knowledge_as_of` 的
  支撑帧，按 valid_time 做 exact/linear/nearest；
- confidence = `min(quality_confidence[quality_flag], temporal_method_confidence)`。

**结论：当前 145 risk frames = 单一 knowledge/as-of 快照下的逐小时
valid_time 风险序列（结构 A），不是 145 个 simulation tick 的滚动重算
（结构 B），也不是每 tick 重新发布的预测集合。**

### 9.2 current / +6h / +12h / +24h

当前**不存在**显式 `current/+6h/+12h/+24h` 预测字段。风险帧只有 `valid_time`
轴；某一 valid_time 帧是“站在同一 as_of 上对那一小时的确定性风险描述”。
`+6h` 只作为：执行 spec `replan_after_hours=6` 与 D 选择 frame index 6。
若未来要表达“simulation_time=t 时发布的 current/+6h/+12h/+24h 预测”，需要
新的二维模型（见 §23）。

## 10. C Time Semantics

### 10.1 四层（与 schema/artifact 一致）

| layer | focus window | 终点锚点 | 说明 |
|---|---|---|---|
| `full_voyage` | start → full ETA | goal | 全航程推荐线为其他层参考 |
| `main_corridor_24_72h` | start+24h → min(start+72h, full_end) | 推荐线 72h 截止前最后非起点航点 | 计划路径 0→72h 锚点，展示 24–72h 窗口 |
| `rolling_0_24h` | start → start+24h | 24h 锚点 | 0–24h 滚动 |
| `executable_0_6h` | start → start+6h | 6h 锚点 | 0–6h 可执行 |

每层独立跑 `plan_candidates`（3 目标），departure 均为 `request.start_time`。

### 10.2 time_bucket

A* 状态 `(node, time_bucket, heading_code)` 中：

```text
time_bucket = int(elapsed.total_seconds() // time_bucket_size.total_seconds())
```

`elapsed = arrival_time - departure_time`，所以 **bucket 是相对出发的航行
已耗时桶（60min），不是绝对模拟时间**。

### 10.3 ETA → risk frame

- 边采样：`sample_time = departure_time + travel_hours * fraction`
  （fraction ∈ {0, 0.5, 1} 起步，travel 由环境速度因子迭代两次）；
- RiskSampler 按 `valid_time` 排序帧，用绝对 `sample_time` bisect 找
  bracketing 帧并线性插值；`hard_mask` 两帧 OR；
- 约束：所有 `RiskFrame.as_of_time <= request.as_of_time`（service 强制），
  `start_time` 必须在 RunContext 模拟窗内，`maximum_elapsed` 不超过
  场景终点与 216h 上限。

## 11. D / Viewer Time Semantics

- D 消费 initial/replanned 两套 v3 制品与 risk store frame 0/6；
- demo-state `spatial.frames[].valid_time` = risk 帧的 valid_time：
  frame 0 = `2026-08-11T06:00:00Z`（initial departure 时刻的环境帧）、
  frame 6 = `2026-08-11T12:00:00Z`（replan departure 时刻的环境帧）；
- 这两个 frame **是同一 knowledge 快照下的两个 valid_time 帧**，不是两个
  simulation snapshot，也不是两次滚动 B 重算；
- D 模型不保存 `as_of_time` 与 `scenario_mode` → 丢失因果维度（GAP）。

## 12. Orchestrator Time Semantics

- `ExecutionSpec`：`generated_at`（墙钟）、`replan_after_hours=6`、
  `input_revision`、`per_stage_timeout_seconds`；
- intake：`bundle.as_of_time == 最大 issue_time`；`clock = SimulationClock(
  bundle.requested_start)`；`knowledge_as_of = bundle.as_of_time`；
- 阶段：initialization → b_build → coverage_preflight → endpoint →
  c_initial_planning → b_suffix_commit → c_replanning → output_publication；
- 重规划：`replan_time = simulation_start + 6h`；时钟 `_advance_clock_without_
  seek`（不 bump generation）；suffix commit = 同一批帧从 +6h 起的切片；
  新 C 请求 `start_time=+6h`、`as_of_time` 不变；observation 见下。

## 13. Frozen vs Live Time Semantics

| 项 | Frozen | Live（demo_live_worker） |
|---|---|---|
| 出发时刻 | initial = simulation_start；replanned = +6h | `query.start + 6h` |
| knowledge | 固定 bundle.as_of_time | 复用冻结 risk commit 的 as_of |
| 风险帧 | 冻结 145 帧 | 冻结窗口切片（同一帧数据） |
| 结果标记 | FROZEN_VALIDATED | LIVE_COMPUTED |
| 计算墙钟 | 历史执行 | 现场 ~56s（worker watchdog 110s） |

Live 是“用冻结风险帧在 +6h 出发点重算推荐路线”，不是“用新数据重算风险”。

## 14. Wall-clock vs Simulation Time

- `generated_at`（B/C 制品、execution-spec）只表示生成墙钟，审计确认没有任何
  因果门禁使用它；
- heartbeat/elapsed/timeout/compute_ms 是机器执行时间，禁止进入业务时间轴；
- `SimulationClock.tick(real_elapsed)` 是唯一把墙钟时间映射到模拟时间的入口
  （running + speed），正式运行实际只用一次无 generation 的推进。

## 15. Causality / Future Leakage Audit

检查结论：**正式路径未发现 future-data leakage**。

- A：`issue_time <= knowledge_as_of` 在 manifest、prefetch、cache、bundle、
  exact-bundle resolver 五处独立执行；
- B：`_resolve_field` 先过滤 `issue_time <= knowledge_as_of`，缺失即可见支撑
  直接 `future_information_leakage` 拒绝；RiskFrame formal 校验再查
  `source.issue_time <= as_of`；
- C：`risk_as_of_times <= request.as_of_time` 强制；
- 未发现用 `valid_time <= simulation_time` 替代 availability 的正式路径；
  legacy 适配器需显式 `--acknowledge-valid-time` 才允许（legacy 边界内）；
- `mtime`/文件名/目录状态不会补造 issue_time（ISSUE_TIME_POLICY §5 明确禁止，
  代码只有证据驱动的 resolver）。

风险点（非 blocker）：`knowledge_as_of == simulation_time` 在 causal 模式
无硬编码相等；`retrospective_best_estimate` 的语义只在 RunContext，D/Viewer
不展示，现场演示存在“被理解为当时预测”的表述风险。

## 16. retrospective_best_estimate

传播链（真实证据）：

| 层 | 是否携带 | 证据 |
|---|---|---|
| scenario config | 是 | `mode = "retrospective_best_estimate"` |
| RunContext | 是 | `scenario_mode = "retrospective_best_estimate"`（A/B 两场景真实值） |
| bundle | 否（隐含） | as_of_time 晚于 simulation_start，无显式 mode 字段 |
| B RiskFrame | 否 | 无 mode 字段；as_of_time 隐式表示 |
| C RoutePlan | 否 | schema 无 `scenario_mode`（确认） |
| run-report identity | 否 | 含 as_of/simulation，不含 mode |
| demo-state / Viewer | 否 | 无 mode/CAUSAL badge |

→ GAP：模式信息没有传播到 D/Viewer。建议下一轮在 demo-state 与 Simulation
Snapshot 中显式带 `scenario_mode`，Viewer 展示 `CAUSAL` /
`RETROSPECTIVE BEST ESTIMATE`。

## 17. Temporal Invariants

| ID | 不变量 | 状态 |
|---|---|---|
| T-01 | 所有持久化业务时间戳 UTC | **IMPLEMENTED**（ensure_utc + schema date-time） |
| T-02 | causal: `knowledge_as_of == simulation_time` | **PARTIAL**（文档/测试；代码只强制 as_of<=start） |
| T-03 | A frame 仅当 `issue_time <= knowledge_as_of` 可见 | **IMPLEMENTED**（A/B/C 多层） |
| T-04 | valid_time 不代表可知 | **IMPLEMENTED**（正式路径无 valid-time 可见性门禁） |
| T-05 | `forecast_reference_time + lead == valid_time` | **IMPLEMENTED（条件性）**：sidecar 含该元数据时强制；BC/CD 不传播 lead → GAP |
| T-06 | source issue_time ≠ B prediction issue time | **IMPLEMENTED**：B 无 prediction-issue 字段；RiskFrame.as_of_time=knowledge |
| T-07 | wall-clock generated_at 不得用于因果门禁 | **IMPLEMENTED** |
| T-08 | 路线风险采样时间 = departure + ETA 推进 | **IMPLEMENTED** |
| T-09 | retrospective 必须显式标注 | **PARTIAL**：RunContext 有；D/Viewer/route 无 |

## 18. Time Conversion / Dependency Matrix

| From | To | Rule | Owner | Code location | Tested? |
|---|---|---|---|---|---|
| forecast_reference_time + lead | valid_time | 相等校验 | A | `ingestion.py:_validate_sidecar` | 是 |
| issue_time / knowledge_as_of | visibility | `issue_time <= knowledge_as_of` | A/B/C | manifest/service/_resolve_field/RiskFrame | 是 |
| simulation_time | knowledge_as_of | causal 相等（约定） | A/orchestrator | AB_INTERFACE；调用方 | 测试级 |
| simulation_start | C departure | `start_time` | orchestrator/C | service.py `_planning_request` | 是 |
| departure + travel_hours | waypoint eta | 绝对 UTC | C | planner `_build_result` | 是 |
| departure + travel×fraction | risk sample time | 绝对 UTC | C | `_evaluate_edge` | 是 |
| sample time | risk frame index | bisect by valid_time | C | `RiskSampler._bracket` | 是 |
| simulation_start + replan_after_hours | replan_time | +6h | orchestrator | service.py:303 | 是 |
| replan_time | suffix window start | 同帧切片 | B | `publish_suffix_window` | 是 |

## 19. Real End-to-End Example（Scenario B，Tromsø → Isfjorden）

全部来自真实制品（`output-tromso-144h-r2`）：

```text
Scenario mode        = retrospective_best_estimate
Simulation start     = 2026-08-11T06:00:00Z
Simulation end       = 2026-08-17T06:00:00Z
Knowledge_as_of      = 2026-08-15T09:37:34.830829Z   (= bundle.as_of_time = max issue_time)

A visible frame 0    : issue_time varies by source (e.g. GFS wind 2026-08-11T11:49:03Z,
                       conservative_retrieval, suspect, authoritative=false)
                       valid_time = 2026-08-11T06:00:00Z
A visible forecast   : forecast_reference_time = 2026-08-11T06:00:00Z
                       forecast_lead_hours = 0.0
                       valid_time = 2026-08-11T06:00:00Z

B risk frame 0       : valid_time = 2026-08-11T06:00:00Z, as_of_time = knowledge_as_of
B risk frame 6       : valid_time = 2026-08-11T12:00:00Z, as_of_time = knowledge_as_of
B 145 frames         : 2026-08-11T06:00Z .. 2026-08-17T06:00Z, one as_of, one generated_at

C initial route      : as_of_time = knowledge_as_of, start_time = 06:00:00Z
                       ETA first = 06:00:00Z, ETA last = 2026-08-13T10:24:16.881224Z
                       focus full_voyage = 06:00Z -> 2026-08-13T10:25:10.630548Z
C replanned route    : as_of_time = knowledge_as_of, start_time = 12:00:00Z
                       ETA first = 12:00:00Z, ETA last = 2026-08-13T11:51:17.454209Z

Replanning           : trigger_time = 2026-08-11T12:00:00Z
                       reasons = ["time", "data"]
                       observed_at = 12:00:00Z, risk_valid_time = 12:00:00Z
                       suffix commit start = 12:00:00Z, count = 139

D frame labels       : "Frame initial · 2026-08-11T06:00:00Z"
                       "Frame replan · 2026-08-11T12:00:00Z"  (risk valid times)
```

注意：GFS 记录 issue_time（11:49Z）晚于 simulation_start（06:00Z），因此
在 causal 模式 06:00Z 它**不可见**；当前 retrospective 模式用
knowledge_as_of（08-15）让它可见——这正是“what happened at valid_time”与
“what was knowable by simulation_time”的区别。

## 20. Meaning of Current 145 Frames

```text
CURRENT 145 B FRAMES SEMANTICS
= 单一 knowledge/as-of 快照（固定 knowledge_as_of）
  × 逐小时 valid_time（requested_start .. requested_end，闭区间）
  × 每帧独立从“当时可见”的 A 支撑帧 exact/linear/nearest 计算

可以直接作为 simulation playback ticks 吗？
= NO
```

原因：所有帧共享同一 `as_of_time`，不是每个 simulation tick 的滚动重算；
valid_time 轴不能冒充 simulation 轴。要回放需要重新生成 rolling
Simulation Snapshots（每 tick 固定新的 knowledge 边界并重算 B/C）。

## 21. Meaning of +6h Replanning

```text
+6h = simulation clock 推进到 simulation_start + 6h（无新数据、无新知识）
    + C 从 +6h 出发点以同一风险窗后缀（139 帧）重新规划四层
    + 触发原因 time + data（risk_valid_time 前进、risk_revision 改变）
```

即：它同时是“executable horizon 边界（0–6h）”“一次正式 replanning 触发”
与“demo 固定 fixture（replan_after_hours=6）”，但**不是 B 风险数据刷新**。

## 22. Current Gaps / Ambiguities

1. `knowledge_as_of == simulation_time` 无代码硬门（T-02 PARTIAL）；
2. B 无 `current/+6h/+12h/+24h` 显式字段；lead 不跨 BC/CD 传播；
3. D/Viewer 丢失 `as_of_time` 与 `scenario_mode`，当前 retrospective 无法
   在 UI 区分；
4. route artifact 不携带 scenario_mode；
5. `frame initial / frame replan` 标签语义是 risk valid time，易被误解为
   simulation snapshot；
6. 145 帧不能直接做播放器（§20）。

## 23. Recommended Canonical Time Model

下一轮合同设计建议（本轮不改任何 schema）：

```text
A source record   : source_issue_time, valid_time,
                    forecast_reference_time, forecast_lead_hours,
                    ingest_time, observed_at
RunContext        : simulation_start, simulation_end, scenario_mode
B RiskFrame       : knowledge_as_of（= prediction as-of）, valid_time,
                    generated_at
C RoutePlan       : planning_as_of（= request.as_of_time）,
                    departure_time, route_eta (absolute), eta_hours
D Snapshot        : simulation_time, knowledge_as_of, scenario_mode
```

禁止把 `issue_time` 直接复用为 B/C 通用字段；B/C 应显式使用
`knowledge_as_of` / `planning_as_of`。

## 24. Simulation Snapshot Candidate

基于审计结果的候选（不修改 production contracts）：

```text
SimulationSnapshot
├── simulation_time
├── knowledge_as_of
├── scenario_mode                # causal | retrospective_best_estimate
├── data_cutoff: {max_issue_time, frames_visible}
├── B
│   ├── prediction_as_of         # = knowledge_as_of
│   ├── current                  # valid_time == simulation_time
│   ├── +6h / +12h / +24h        # forecast_lead_hours 显式化
│   └── full_hourly               # 可选
├── C
│   ├── planning_as_of
│   ├── executable_0_6h
│   ├── rolling_0_24h
│   ├── main_corridor_24_72h
│   └── full_voyage
├── ship_state
├── coverage / hard_reason / data_quality
└── events
```

回放方式：答辩前预计算真实 snapshots（每 tick 固定知识边界重跑 A→B→C→D），
Viewer 只做快速回放，不做前端伪造插值。

## 25. Next Implementation Phase

```text
Simulation Snapshot schema
  ↓
rolling A→B→C→D replay pipeline（真实重算，非前端插值）
  ↓
GEBCO georeferenced basemap
  ↓
Simulation-clock Viewer（主控 = simulation_time）
  ↓
动态 B forecast（current/+6h/+12h/+24h）
  ↓
动态 C routes（四层 × 三目标）
  ↓
Moving Ship（executed route + route eta + simulation_time）
  ↓
Replanning Events（B_UPDATED / PLAN_COMPUTED / ROUTE_CHANGED /
  EXECUTABLE_ROUTE_CHANGED / REPLAN_TRIGGERED / LIVE_REPLAN_COMPLETED）
```

本轮停止于审计、模型与文档；等待下一阶段指令。
