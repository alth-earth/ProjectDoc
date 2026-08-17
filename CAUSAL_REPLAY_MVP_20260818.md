# Scenario B Causal Replay Engine MVP（2026-08-18）

> 状态：**CAUSAL REPLAY ENGINE MVP = ESTABLISHED（ENGINE LEVEL）**
> C 规划层：**PLANNING-HORIZON ARCHITECTURE BLOCKER（真实 fail-closed）**
> 机器产物：`work_package_a/data/output/rc2-smoke/causal-replay-mvp/`

## 1. Executive Summary

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
1. 解除 C planning-horizon blocker：
   - 评估 replay-local 子层规划（executable/rolling 独立锚点）
   - 或引入可证明的短窗 C 合同（需 contract proposal）
2. causal-ready 采集（实时 publication evidence）→ 全窗回放
3. Replay-driven Presentation Viewer（下一阶段）
```
