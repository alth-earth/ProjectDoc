# Strategy B Semantic Hardening（2026-08-18）

状态：RUNNING（最终结果待 12h 长验证完成后定稿）
分支：`demo-engineering`（各工作包本地提交；PUSH = NOT PERFORMED）

## 1. Revision / Replan Semantics（已实现）

当前 replay 模型已把以下概念拆开，不再混用：

| 字段 | 语义 | 变化条件 |
|---|---|---|
| `data_revision` | A visible record set 业务身份 | visible digest 变化 |
| `b_input_revision` | B 真正消费的 relevant input 身份 | relevant digest 变化 |
| `risk_content_revision`（=`risk_revision`） | B 风险业务内容重算 | B 重新 build |
| `risk_window_revision` | Planner 可见 suffix window 身份 | 每 tick 窗口推进（内容可复用） |
| `observation_sequence` | 向 ReplanTriggerEvaluator 提交的观察序号（C 合同要求严格单调的 input_revision） | 每次 replan evaluation |
| `plan_revision` | 已采纳 route 业务结果修订 | 计划发布/采纳 |
| `navigation_state_revision` | 已执行船舶状态修订 | 每 tick 位置推进 |

**关键修复**：`observation_sequence` 不再冒充 `data_revision`。C 合同
（`_validate_formal_replan`）要求 `observation.data_revision == request.input_revision`，
这是 planning fence 的严格单调要求；replay 内部保留真实的 `data_revision`，
并在事件/原因层做诚实翻译：仅当真实 A 数据或 B 风险内容变化时才报告 `data`。

上一轮 12h 事件里每 tick 出现 `time,data` 的原因已定位：
`observation.data_revision` 被 runner 用单调 input_revision 伪造，且
`risk_revision` 传入的是每 tick 变化的 suffix window identity，两者都让
C 的 trigger evaluator 误报 DATA。修复后：

- 真实 Scenario B 后续 12h 无新增 causal-visible record；
- 每 tick 的 replan reason 应为 `time`（滚动规划 policy：min_interval=30min）；
- 事件增加 `RISK_CONTENT_UPDATED` / `RISK_WINDOW_ADVANCED` 区分内容与窗口。

## 2. Semantic Digest Hardening（已实现 + mutation tests）

`replay_semantic_digest` 排除墙钟与派生身份（`generated_at` / `created_at` /
`published_at` / `elapsed` / `compute_ms` / `resource_identity` /
`resource_digest` / `commit_id` / `content_digest` / `revision` / `route_id`），
同时新增两个纯业务 digest：

- `risk_semantic_digest`：valid_time / as_of / model_version / provenance /
  source summaries / risk_score / risk_level / confidence / hard_mask /
  hard_reason / environment_speed_factor；
- `route_semantic_digest`：objective / plan_kind / start_time / layer /
  focus windows / waypoints(lon/lat/eta) / 全部业务 metrics /
  replan_reasons。

Mutation tests（`tests/unit/test_replay_digests.py`）：

| 变更 | 期望 | 结果 |
|---|---|---|
| 仅改 `generated_at` / plan_id / resource identity | digest SAME | PASS |
| 改一个 route waypoint | digest DIFFERENT | PASS |
| 改 risk confidence / payload 业务值 | digest DIFFERENT | PASS |
| 改 runtime / elapsed / PID | digest SAME | PASS（排除字段） |

## 3. v3 Four-Layer Contract Edge（已解决，生产 C 最小修正）

### 3.1 根因

`FourLayerPlanningService.execute` 对每个 layer：

```python
layer_elapsed = min(request.maximum_elapsed, cutoff, full_end - start)
```

当 `full_recommended ETA < 72h` 时 main_corridor 的 anchor 变为 destination，
但 `layer_elapsed` 被 recommended ETA（≈50.45h）截断；fastest/low_risk 到达
destination 需要更长合法时间 → `PlanningHorizonExceeded`。

### 3.2 Replay-local 实验（真实 77h causal 窗口）

实验：`scripts/v3_contract_experiment.py`，commit
`risk-window-sha256-7b89a6…`（Scenario B 10:00Z → 08-18 15:00Z）：

| 层 | 当前 cap | 候选 cap（anchor==destination 时 `min(request, cutoff)`） |
|---|---:|---:|
| full_voyage | PASS（ETA 50.43/50.53/50.45h） | 同左 |
| main_corridor_24_72h | **PlanningHorizonExceeded** | PASS（72h cap；三目标路由与 full_voyage 逐位一致） |
| rolling_0_24h | PASS（22.7h） | 同左 |
| executable_0_6h | PASS（4.6h） | 同左 |

全部候选路由 Route Geospatial Integrity = PASS（LAND=0、DU=0、hard=0、
corner-cutting=0）。

### 3.3 实施与回归

work_package_c `layered.py` 最小修正：当 layer anchor == destination 时
`layer_elapsed = min(request.maximum_elapsed, cutoff)`；否则保留原语义。
新增单测 `test_destination_anchor_layer_allows_objectives_beyond_recommended_eta`。

```text
C unit/integration  = 97 passed
RC1 golden          = PASS（r6/r7 路由 digests 不变）
RC2 144h regression = PASS（layer-set digests 不变）
```

冻结基线不受影响：RC1/RC2 的 v3 制品在所有 objective 都已在 recommended ETA
内到达时结果逐位相同；修正只放宽“其他 objective 需要更长合法到达时间”的场景。

## 4. NavigationExecutionState（已实现 v1）

`NavigationExecutionState`（replay-local，`replay/models.py`）：

```text
status / navigation_state_revision / accepted_plan_revision /
accepted_plan_digest / executed_until / current_position /
current_node / edge_progress / completed_track /
remaining_distance_km / snap_adjustment_km /
last_distance_delta_km / expected_travel_km
```

Same-vessel 规则（v1）：

- replan origin = accepted route 在 simulation_time 前最后到达的 waypoint，
  snap 到最近可通航 grid node（显式 tolerance `max_snap_km=30km`，距离写入
  `snap_adjustment_km` 并记录 provenance；禁止静默 teleport）；
- C planner 仅接受 grid node start，v1 不实现任意 lon/lat 起点；
- completed_track 不可变：新 replan 只改未来段；
- 成功 replan 立即采纳为新 accepted route（MVP policy，文档明确）；
- RouteSwitchGate 拒绝的候选不会成为 current_plan（本轮修复）；
- 到达 destination 后不再生成 replan origin。

机器校验新增：`navigation_state_revision` 单调、`accepted_plan_revision`
单调、completed_track 不缩短、单 tick 位移 ≤80km（无 teleport）。

## 5. Objective-Level Parallelism（已实现 + benchmark）

`replay/parallel.py`：单次 C planning request 内 three objectives 并行
（ProcessPoolExecutor），replay tick / layer / B build 保持严格串行。
运行时仅 patch orchestrator 进程内 `PreparedRiskPlanning._private_planner`
（C production 零改动，exit 恢复）；worker 从不可变 risk store 重建同一
committed window，与串行结果逐位一致（expanded counts 也一致）。

CPU 环境：32 logical CPUs（16C/32T），7.4GiB RAM，无 CPU quota。

### Benchmark（同一真实 77h request，3 objectives）

| workers | wall (s) | speedup vs 1 | extra vs 2 | parent RSS (MB) | child RSS max (MB) | 结果一致性 |
|---|---:|---:|---:|---:|---:|---|
| 1 | 157.2 | 1.00 | – | 132 | – | baseline |
| 2 | 100.9 | 1.56× | – | 93 | 112 | identical |
| 3 | 80.5 | 1.95× | 1.25× | 94 | 113 | identical |

选择：3 workers 满足额外 speedup ≥1.15× 且内存健康 → 长验证默认 3（若真实
replay 内存超过 4.5GiB 则回退 2）。

## 6. Same-Vessel Smoke（进行中）

3h smoke（`sb-c-sem-hard-3hb`，v3 four-layer + 3 workers）：

```text
snapshot_count   = 4（10:00Z → 13:00Z，1h tick）
v3 four-layer    = SUPPORTED（4 层 × 3 目标，plan_revision=1）
B builds         = 1；B reuse = 3；risk_content_revision=1；
                   risk_window_revision=4
replan policy    = 每 tick TIME 触发；switch gate 拒绝候选 →
                   PLAN_REUSED（无伪造 DATA；无 ROUTE_CHANGED）
navigation       = ACTIVE；node [5,7]→[6,7]；remaining 909→856km；
                   completed_track 单调；no teleport
total duration   = 801.0s（~13.4min）
mean tick        = 200.3s（tick0=262.2s，replan ≈177–183s）
peak parent RSS  = 823.6MB（3 workers；组合峰值 ≈3.25GB，
                   低于 4.5–5GiB 并发红线）
validation       = snapshots / replay / manifest 全 PASS
```

## 7. 12h Authoritative Replay（PASS）

首轮 `sb-c-sem-hard-12h`（v3 + 3 workers）2118.8s 完成，但机器 validation
发现 `completed_track shrank`：replan 采纳新计划后，历史段被新计划覆盖而缩短
（违反“历史不可重写”）。已修复：`merge_completed_track` 追加式合并（只增不
减，按 lon/lat/eta 去重），回归测试 PASS（commit `809b38b`）。
最终权威运行 `sb-c-sem-hard-12hb`：

```text
snapshot_count        = 13；total = 2113.9s（~35.2min）；mean tick = 162.6s
v3 four-layer         = SUPPORTED 全段（12 routes/tick）
B builds              = 1；B reuse = 12；risk_content = 1；risk_window = 13
REPLAN_TRIGGERED      = 5（time only）；ROUTE_CHANGED = 5；PLAN_REUSED = 7
plan_revision         = 1 → 6
navigation            = node [5,7]→[11,7]；remaining 909.7→665.1km；
                        completed_track 1→7 单调；no teleport
route integrity       = PASS（末 tick 12 routes）
validation            = 13/13 snapshot + replay + manifest 全 PASS
peak parent RSS       = 823.6MB；组合峰值 ≈3.10GiB
```

## 8. Determinism（复跑中）

`sb-c-sem-hard-12hb-det` 独立复跑（同一配置、workers=3），完成后对比
13/13 snapshot semantic digest 与 manifest semantic digest。

## 9. Known Limitations / Gaps

- NavigationExecutionState 为 node-aligned v1；edge-interior 起点、任意
  lon/lat start、NavigationExecutionState production contract 属后续；
- C `ReplanObservation.data_revision` 仍受合同限制等于 input_revision，
  replay 在适配层做诚实翻译（C contract proposal 可后续解耦）；
- Full 144h historical causal replay 仍不被当前 provenance 支持；
- GEBCO L2 coastline / 最终 Viewer / moving-ship 动画仍属后续阶段。
