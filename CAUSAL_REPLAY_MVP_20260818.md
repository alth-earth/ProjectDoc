# Scenario B Causal Replay Engine MVP（2026-08-18）

> 状态（第二轮，2026-08-18）：**CAUSAL REPLAY ENGINE + ROUTE PLANNING
> MVP = ESTABLISHED**
> - Causal forecast window 已与 replay window 解耦（common end
>   `2026-08-18T15:00Z`，77h）；
> - **v2 complete-route C 规划 = PASS**（真实 route，ETA ≈ 50.45h，
>   3 目标 × 13 ticks 全部 Route Geospatial Integrity PASS）；
> - **v3 four-layer = 仍被 main_corridor 内部 cap 阻塞**
>   （cap = full_recommended ETA ≈ 50.5h < 72h anchor，low_risk/fastest
>   目标需要更多余量 → PlanningHorizonExceeded；这是 v3 合同边缘 +
>   数据 horizon 硬上限的组合，非 replay scoping bug）；
> - 12h 集成回放：13 snapshots、plan_revision 1→13、
>   12×REPLAN_TRIGGERED/ROUTE_CHANGED、validation PASS；
> - Determinism：13/13 snapshot digest + manifest digest 一致，
>   `generated_at`（墙钟）不同。
> 机器产物：`work_package_a/data/output/rc2-smoke/causal-replay-mvp/`

## 0. 第二轮结论（Window Decoupling + C Integration）

### 0.1 三窗口语义（已落地）

```text
Replay Window         = 发布多少 snapshots（12h / 24h / 44h 可选）
Risk Forecast Window  = B 因果可见输入共同支持的 valid 范围
                        = 2026-08-15T10:00Z → 2026-08-18T15:00Z（77h）
Planning Window       = C 可用 risk 范围（= risk forecast end，77h；
                        场景合同 horizon 96h 仅用于 corridor 对齐）
```

代码位置：`runner.py` 的 `risk_forecast_end` / `planning_valid_end` /
`_replay_configuration` / `_c_run_context`；preflight 输出
`risk_forecast_window` / `planning_window_candidate` /
`common_causal_valid_end`。

### 0.2 c907455 Review

- 它把 B requested_end 与 C maximum_elapsed 都 cap 到 replay_end（44h），
  同时 C 查询必须匹配已提交窗口 → 是当时 44h blocker 的直接原因；
- 但解耦到 77h 后 v3 仍在 main_corridor 失败（见 0.4），因此：
  **44h blocker = REPLAY SCOPING GAP（已修复）；77h 下的 v3 blocker =
  v3 合同边缘 + 数据 horizon 硬上限（真实）**。

### 0.3 Existing C 真实结果

```text
v2 complete-route（fastest/low_risk/recommended）：PASS
  ETA ≈ 50.45h ≤ 77h causal forecast
  route integrity：LAND=0 / DU=0 / hard=0 / corner=0（逐目标）

v3 four-layer：FAIL（main_corridor_24_72h）
  layer_elapsed = min(77h, 72h, full_end-start) ≈ 50.5h
  anchor = destination（full ETA < 72h）
  fastest/low_risk 需 >50.5h → PlanningHorizonExceeded
```

### 0.4 最终 blocker 分类

```text
不是 replay scoping bug（已解耦验证）
不是 C 算法正确性 bug（v2 同参数成功）
是 v3 layered 合同边缘：main_corridor cap = full_recommended ETA，
  其他 objective 无余量；数据 horizon 77h 无法放大 cap
```

### 0.5 第三轮更新（2026-08-18 Semantic Hardening）

```text
v3 four-layer contract edge = RESOLVED
  destination-anchor 层 ceiling = min(request horizon, layer ceiling)
  真实 77h 窗口：旧 cap 复现 PlanningHorizonExceeded；
  72h 候选 cap 下四层 × 3 目标全 PASS，main_corridor 与 full_voyage
  路由逐位一致，Route Geospatial Integrity 全 PASS
  生产 C 最小修正 commit 0186caa；C 97 tests + RC1/RC2 regression PASS

Revision semantics = RESOLVED
  data / b_input / risk_content / risk_window / observation_sequence /
  plan / navigation 已拆分；honest replan reasons 机器验证

Semantic digests = HARDENED（mutation tests PASS）

NavigationExecutionState = v1 ESTABLISHED（node-aligned same-vessel）

Objective parallelism = ESTABLISHED（1/2/3 worker benchmark：
  157.2s / 100.9s / 80.5s，结果逐位一致；长验证默认 3）

3h same-vessel v3 smoke = PASS（4 snapshots，validation PASS，
  RSS≈824MB）
12h authoritative replay = 见 §20.6（本轮运行）
```

## 1. Executive Summary（第一轮保留）

Strategy B 主路径首次在真实 Scenario B 数据上运行：

```text
Scenario B
CAUSAL
replay_start = 2026-08-15T10:00:00Z
knowledge_as_of == simulation_time（每 tick）
issue_time <= knowledge_as_of（真实 manifest 门禁）

12h：13 snapshots，31s，PASS（engine + validation + determinism）
24h：25 snapshots，91s，PASS
44h：45 snapshots，317s，PASS（最大 causal 证据窗口）

C planning：真实 A*/v2 尝试均 fail-closed
  PlanningHorizonExceeded（44h 因果风险窗 < ~48h 航线 ETA）
  → 四层 C 路线本轮不可生成（架构 blocker，非伪造）
```

## 2. Scope

- 输入：A manifest（`tromso_to_isfjorden_outer`，1537 条）、A raw 归档、
  B `demo_unvalidated_tromso_smoke_grid_v1.json`、C planner 配置、
  Scenario B frozen run-context；
- 输出：replay snapshots、`causal-replay-manifest.json`、
  `replay-summary.json`、checkpoint、heartbeat；
- 严格 causal：`knowledge_as_of == simulation_time`；
  `issue_time <= knowledge_as_of`；`max_source_issue_time <= knowledge_as_of`；
- 不修改 RC1/RC2、不重新下载、不补造 issue_time、不降低门禁。

## 3. Strategy A Freeze

```text
Strategy A = RETROSPECTIVE FALLBACK = FROZEN / PRESERVED
RC1 / RC2 = validated retrospective frozen baselines
```

本轮回归：A 172 tests、contracts 18、orchestrator 25、D 39、demo preflight
`READY FOR DEMO`、demo build OK、temporal audit PASS。RC1/RC2 制品目录
未被修改（git clean），digest 无漂移。

## 4. Strategy B Architecture

实现于 `arctic_route_orchestrator/src/arctic_route_orchestrator/replay/`：

- `models.py`：SimulationSnapshot / ReplayManifest / RevisionState / events；
- `digests.py`：visible_record_set_digest、b_relevant_input_digest（A 排序规则）、
  replay_semantic_digest（排除 wall-clock）；
- `runner.py`：tick 生命周期、A 可见性解析、B 构建/复用、suffix window、
  C 尝试（v3 + v2 probe）、checkpoint/heartbeat/原子发布；
- `route_integrity.py`：C 语义路线完整性审计（waypoint/edge/角切）；
- `validation.py` + `scripts/replay_inspect.py`：机器验证与最小 inspector。

## 5. Operational Preflight

`scripts/causal_replay_preflight.py`（真实 manifest 扫描）：

```text
replay_start            = 2026-08-15T10:00:00Z
knowledge_as_of         = 2026-08-15T10:00:00Z
max_source_issue_time   = 2026-08-15T09:37:34.830829Z（<= knowledge ✓）
risk_horizon_hours      = 44.0（window-capped；动态类型覆盖至 08-18T15:00Z）
executable_0_6h         = SUPPORTED
rolling_0_24h           = SUPPORTED
main_corridor_24_72h    = NOT_SUPPORTED（44h < 72h）
full_voyage             = CANDIDATE_NOT_SUPPORTED（44h < 冻结 ETA ~47.9h）
```

## 6. C Horizon Support（真实结果）

12h/24h/44h 三次真实回放中，C 初始规划（v3 four-layer）均抛出：

```text
PlanningHorizonExceeded: no complete route fits inside the available risk time window
```

v2 probe 独立复现同一结果。44h 搜索真实展开 29,871+ states、max_bucket=43，
确认不是输入错误，而是**风险窗 44h < 到达终点所需 ETA（~48h）**。

结论：

```text
supported_layers   = ()
unsupported_layers = executable_0_6h, rolling_0_24h,
                     main_corridor_24_72h, full_voyage
reason             = CAUSAL MVP PLANNING-HORIZON ARCHITECTURE BLOCKER
                     （layered API 依赖 full_voyage 锚点；v2 API 需要可达终点）
```

未伪造任何未来风险、未重复最后一帧、未降低 fail-closed。

## 7. Replay Lifecycle（实现）

```text
tick(t)
  → knowledge_as_of = t
  → visible = {r | r.issue_time <= t}
  → visible / b-relevant digests
  → B rebuild（首次或 relevant 变化）or reuse（suffix window 每 tick）
  → C 尝试/复用（replan policy；当前因 horizon blocker 保持 NOT_READY）
  → SimulationSnapshot(t) 原子发布 + checkpoint + heartbeat
→ ReplayManifest + summary
```

## 8. Snapshot Schema（落地）

`orchestrator.replay-snapshot.v1`：identity（scenario/mode/replay_id/index/
simulation_time/knowledge_as_of）、visibility（max_source_issue_time/
visible digest/b-relevant digest/data_revision/b_input_revision/
newly_visible/quality）、risk（risk_revision/prediction_as_of/valid range/
resource identity+digest/presentation horizons 0/6/12/24）、planning
（plan_revision/planning_as_of/departure/supported/unsupported/blockers）、
readiness、events、ship_state=DEFERRED、snapshot_digest。

## 9. Manifest Schema（落地）

`orchestrator.replay-manifest.v1`：replay_id/scenario/mode/start/end/cadence/
snapshot_count/snapshots（index/time/resource/digest）/events/resources
（相对路径）/provenance/semantic_digest。

## 10. Revision Semantics（真实运行）

```text
12h/24h/44h 运行：
  data_revision     = 1（tick0 全部 1537 条可见；此后无新记录）
  b_input_revision  = 1（B relevant 集合不再变化）
  risk_revision     = 1（B 只构建一次）
  plan_revision     = 0（C blocker）
  B_REUSED          = 每 tick 一次（suffix window identity 变化，内容复用）
```

这正是设计预期：**A 不变 → B 复用；快照每小时存在但 revision 不空转**。

## 11. B Reuse / Recompute

- 首次 tick：A `prepare_window_for_b(knowledge_as_of=t0)` → B full window
  `[t0, replay_end]`（12h=13 帧 / 24h=25 帧 / 44h=45 帧），commit 一次；
- 后续 tick：`publish_suffix_window(frames, start=t)`（只写 manifest/pointer，
  帧内容复用）；`b_relevant_input_digest` 不变 → 无 B 重建；
- 满足 §40-45：A 可见集合变化但 B relevant 不变时 B 必须复用（本窗口
  内未出现新记录，两个 digest 均恒定）。

## 12. C Replan Semantics

`ReplanTriggerEvaluator` 已接入 runner（`ReplanObservation{observed_at,
risk_valid_time, data_revision, risk_revision, route metrics}`）；由于当前
没有初始 plan，policy 未产生 C recompute——记录为 `PLANNING_NOT_READY`，
不伪造触发。

## 13. Real 12h Result

```text
snapshot_count          = 13
B builds                = 1（B reuse 12）
C replans               = 0（blocker）
route changes           = 0
events                  = CLOCK_TICK×13, DATA_BECAME_VISIBLE, DATA_REVISION_CHANGED,
                          B_UPDATED, RISK_REVISION_CHANGED, PLANNING_NOT_READY,
                          B_REUSED×12
total duration          = 31.1s
peak RSS                = 465MB
validation              = PASS（snapshots + manifest）
```

## 14. Real 24h Result

```text
snapshot_count = 25，B builds = 1，C replans = 0
total duration = 90.9s，peak RSS = 539MB
validation     = PASS
```

## 15. Optional 44h Result

```text
snapshot_count = 45，B builds = 1，C replans = 0
total duration = 317.2s，peak RSS = 649MB
C 真实搜索     = 44h horizon，fastest 目标 90s/29,871 expansions 后
                PlanningHorizonExceeded（v2 probe 同）
validation     = PASS
```

## 16. Determinism

同一 replay-id、同一配置、两次独立运行（不同输出目录）：

```text
12h：13/13 snapshot digests 完全一致
manifest semantic digest 完全一致
```

已修复的确定性问题：B RiskFrame `generated_at` 曾用墙钟进入内容身份 →
改为 knowledge 时刻（tick），并规范 snapshot digest 计算（排除自身字段）。

## 17. Resource Profile

```text
峰值 RSS：465–649MB（远低于 6GiB 红线）
最长阶段：tick0（A 解析 + B build + C 搜索）≈ 243s（44h 窗口）
其余 tick：≈ 2s（digest + suffix + snapshot）
内存/磁盘：无 OOM、无 swap 恶化
```

## 18. Known Limitations

1. C 四层无法在本因果窗口生成（风险窗 44h < ETA ~48h；layered 依赖
   full_voyage 锚点）→ 架构 blocker，需下一轮设计（短窗 anchor 或
   replay-local 子层合同）；
2. 当前证据窗口在 simulation window 末期（A 19h / B 44h），不是早期回放；
3. B 每 tick 的 suffix commit 产生新的 window identity（RISK window 变化），
   但内容复用——已在事件中如实表达为 B_REUSED；
4. ship_state 为 DEFERRED；
5. 无 GEBCO/UI/动画（本轮范围外）。

## 19. Next Step

```text
1. 保留 v2 complete-route 为因果回放主规划路径（已集成、已审计）；
2. v3 four-layer：合同 proposal（main_corridor 余量语义或
   horizon-limited partial plan），本轮不改 C；
3. causal-ready 采集（实时 publication evidence）→ 全窗回放；
4. Replay-driven Presentation Viewer（下一阶段）。

## 20. 性能分析 / 耗时分析（2026-08-18 实测）

### 20.1 12h 集成回放总耗时

| run | snapshots | total (s) | mean tick (s) | peak RSS (MB) |
|---|---:|---:|---:|---:|
| sb-c-12h3 | 13 | 2169 | 166.9 | 824 |
| det1b | 13 | 2244 | 171.1 | 824 |
| det2b | 13 | 2218 | 175.5 | 824 |

### 20.2 分阶段耗时

```text
tick0（A 解析 + B 77h build + v2 初始 3 目标）  ≈ 245–255s
重规划 tick（v2 3 目标，horizon 76→65h）        ≈ 155–193s（中位 ~164s）
引擎开销（digest/suffix/snapshot/checkpoint）    ≈ 2–5s/tick
B build 次数                                     1（后续 12 tick 全复用）
```

### 20.3 C 搜索画像（A* 日志）

```text
每 objective：expanded ≈ 9k–20k，rate ≈ 270–345 exp/s
fastest/recommended：≈ 30–90s；low_risk：≈ 60–120s（风险权重更高，
  需探索更多低风险路径）
max_bucket：44–50（ETA 桶 ≈ 48h + 余量）
```

### 20.4 内存与磁盘

```text
峰值 RSS ≈ 824MB（远低于 6GiB 红线；与纯 engine 轮 649MB 相比
  +27% 来自 C planner）
无 OOM / swap；磁盘产物 ≈ MB 级（snapshots 为小型 JSON，
  risk frames 内容寻址共享）
```

### 20.5 对比与结论

```text
纯 engine 回放（无 C）：12h=31s、24h=91s、44h=317s
集成 C 回放（v2 complete-route）：12h≈36–38min
→ C 规划占耗时 ≥95%；引擎开销可忽略
→ 每 tick 固定成本 ≈ 3 目标 × ~55s 平均搜索 + 引擎 2–5s
→ 未来优化方向（不在本轮）：objective 并发（EXPERIMENTAL）、
  或 replan policy 降低 TIME 频率（需合同评审）
```

### 20.6 第三轮：Semantic Hardening + 受控多核（2026-08-18 实测）

#### objective 级并行 benchmark（同一真实 77h request，3 objectives）

| workers | wall (s) | speedup vs 1 | extra vs 2 | parent RSS (MB) | child RSS max (MB) | 业务结果 |
|---|---:|---:|---:|---:|---:|---|
| 1（串行） | 157.2 | 1.00× | – | 132 | – | baseline |
| 2 | 100.9 | 1.56× | – | 93 | 112 | 与串行逐位一致 |
| 3 | 80.5 | 1.95× | 1.25× | 94 | 113 | 与串行逐位一致 |

#### 3h same-vessel v3 smoke（workers=3）

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
peak parent RSS  = 823.6MB（3 workers，远低于 4.5–5GiB 并发红线）
validation       = snapshots / replay / manifest 全 PASS
```

#### 12h authoritative replay（workers=3，v3 four-layer）

权威运行 `sb-c-sem-hard-12hb`（completed-track 追加修复后；首轮
`sb-c-sem-hard-12h` 因该 invariant FAIL 作废并作为 reproducer）：

```text
snapshot_count        = 13（10:00Z → 22:00Z）
total duration        = 2113.9s（~35.2min）
mean tick             = 162.6s（tick0=298.4s；replan tick 117–190s，
                          horizon 缩短后逐 tick 变快）
v3 four-layer         = SUPPORTED 全 13 tick（4 层 × 3 目标 = 12 routes/tick）
B builds              = 1；B reuse = 12
risk_content_revision = 1（内容全程复用）
risk_window_revision  = 13（每 tick suffix 前移）
replan evaluations    = 12；REPLAN_TRIGGERED = 5（time only）
ROUTE_CHANGED         = 5（14:00 / 16:00 / 18:00 / 20:00 / 22:00）
PLAN_REUSED           = 7（policy 触发但 switch gate 拒绝候选）
plan_revision         = 1 → 6
navigation            = ACTIVE 全段；node [5,7]→[11,7] 单调推进；
                        remaining 909.7→665.1km 单调下降；
                        completed_track 1→7 只增不减；无 teleport
route integrity       = 末 tick 12 routes 全 PASS（LAND=0 / DU=0 /
                        hard=0 / corner=0）
validation            = 13/13 snapshot PASS + replay PASS + manifest PASS
peak parent RSS       = 823.6MB；组合峰值（3 workers）≈3.10GiB
                        （低于 4.5–5GiB 并发红线，无 swap）
```
```
