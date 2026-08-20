# Simulation Replay Architecture（候选设计，2026-08-17）

> 状态：**DESIGN + ENGINE MVP IMPLEMENTED（2026-08-18）**
> 已实现：replay models/digests/runner/validation/inspector；真实 12h/24h/44h
> Scenario B 回放 PASS（engine level）；C 四层因风险窗 < ETA 保持
> PLANNING-HORIZON ARCHITECTURE BLOCKER（诚实 fail-closed）。
> 详细结果：[`CAUSAL_REPLAY_MVP_20260818.md`](CAUSAL_REPLAY_MVP_20260818.md)
> 依据：`CAUSAL_REPLAY_FEASIBILITY_AUDIT_20260817.md`、
> `TEMPORAL_SEMANTICS_AUDIT_20260817.md`

## 1. Goals

1. 让 Simulation Clock 成为演示主控，而不是 frame 选择器；
2. A→B→C→D 只在“必要变化”时重算（event-driven，非每小时全量）；
3. 每个 tick 都能发布 SimulationSnapshot，但 risk/plan revision 可复用；
4. 严格区分 CAUSAL 与 RETROSPECTIVE，避免把事后数据当当时预测；
5. 预计算真实 snapshots，Viewer 只做快速回放，不做前端伪造插值。

## 2. Non-goals

- 不实现 GEBCO、moving ship、timeline UI、replan 动画；
- 不把 145 个 valid_time 帧当 145 个 simulation snapshot；
- 不每小时盲目全量重跑 B/C；
- 不降低 issue_time 门禁、不补造 publication time；
- 不重生成 RC1/RC2 frozen baseline。

## 2.1 Implementation Status（2026-08-18）

| 组件 | 状态 |
|---|---|
| SimulationSnapshot / ReplayManifest | IMPLEMENTED（orchestrator-local schema） |
| visible / B-relevant digest | IMPLEMENTED（A 排序规则） |
| Causal replay runner（tick/B reuse/suffix/snapshot/checkpoint） | IMPLEMENTED |
| Replay validation + inspector CLI | IMPLEMENTED |
| 真实 12h/24h/44h Scenario B replay | PASS（engine；C blocker 如实记录） |
| Causal forecast window 解耦 | IMPLEMENTED（common end 77h；replay ≠ risk ≠ planning window） |
| v2 complete-route C 规划 | IMPLEMENTED + 12h 集成 PASS（route integrity PASS） |
| v3 four-layer C 规划 | RESOLVED（第三轮：destination-anchor 层 ceiling 放宽；真实 77h 窗口四层全 PASS；生产 C 修正 commit 0186caa） |
| Revision semantics 拆分 | IMPLEMENTED（data / b_input / risk_content / risk_window / observation_sequence / plan / navigation） |
| Semantic digest 硬化 | IMPLEMENTED（risk/route 业务 digest + mutation tests） |
| NavigationExecutionState v1 | IMPLEMENTED（node-aligned same-vessel replan origin） |
| Objective-level 并行（1/2/3 worker） | IMPLEMENTED + benchmark（157.2s/100.9s/80.5s，结果逐位一致） |
| Presentation Adapter（2026-08-19） | ESTABLISHED（`replay/presentation.py`；任意仿真时刻船位由 accepted route ETA + `vessel_state_at` 重建；adoption audit 机器可读；T1–T7 测试） |
| GEBCO / L2 基础（2026-08-19） | ESTABLISHED（`replay/geospatial.py`：EPSG:4326 canonical transform、basemap metadata、L2 coastline gate harness + 本地 GEBCO_2026 land_sea_mask real smoke） |

## 3. Canonical Time Model

```text
knowledge_as_of        = 逻辑知识截止（causal: == simulation_time）
max_source_issue_time  = 可见记录中最大 issue_time（结果统计，不是门禁）
visible_record_set_digest = knowledge 下 A 暴露集合的身份
simulation_time        = 时钟当前时刻
valid_time             = 环境/预测有效时刻
```

不变量：`max_source_issue_time <= knowledge_as_of`。

## 4. SimulationClock

- `tick(real_elapsed)`：单调前推，**same generation**，knowledge 可单调前进；
- `seek(new_time)` / rewind / jump：**generation++**，缓存按新时刻重解析；
- 正式 run 的 +6h 前推继续使用 `_advance_clock_without_seek`（same
  generation）。

## 5. Knowledge Boundary

- A 每 tick 以 `knowledge_as_of = simulation_time` 解析可见集合；
- 可见集合用 `visible_record_set_digest` 标识；
- `data_revision` 只在可见集合实际变化时递增。

## 6. A Visibility Revision

```text
tick(t)
  → A.resolve_visible(knowledge_as_of=t)
  → visible_set(t)
  → digest(t)
  → changed = digest(t) != digest(t-1)
  → data_revision += 1 if changed
```

复用现有 `PartitionedABCache` 与 `prefetch(..., knowledge_as_of=...)`；
normal tick 下不 reset generation。

## 7. B Risk Revision

- B 只在 `data_revision` 变化或显式策略要求时重算；
- 同一 knowledge 下重复 tick 复用同一 `risk_revision`（含 committed window
  digest）；
- B 输出保持通用 `RiskFrame(as_of_time, valid_time)`，**不**新增
  current/+6/+12/+24 核心字段；
- Current/+6/+12/+24 作为 **presentation projection**：
  `presentation_lead_hours = valid_time - simulation_time`。

## 8. Replanning Policy

复用现有 `ReplanTriggerEvaluator`（TIME / DATA / RISK / DEVIATION / EVENT /
MANUAL，min_interval/hysteresis）与 `ReplanObservation{observed_at,
risk_valid_time, data_revision, risk_revision, ...}`：

- `data_revision` 变 → DATA 候选；
- `risk_revision` 变 → DATA 候选；
- `risk_valid_time` 前推 → TIME 候选；
- 未触发 → C 复用当前 plan_revision。

## 9. C Plan Revision

- 只在 replan policy 触发时重算；
- 重算只重做被触发目标（MVP：recommended；扩展：四层 × 三目标）；
- 每次发布获得新 `plan_revision` 与 layer-set digest；
- `ROUTE_CHANGED / EXECUTABLE_ROUTE_CHANGED` 事件按需产生。

## 10. Snapshot Model

候选 `SimulationSnapshot`（字段以审计结果为准）：

```text
identity:
  scenario, scenario_mode, simulation_time, knowledge_as_of, snapshot_index
data_visibility:
  max_source_issue_time, visible_record_set_digest, data_revision,
  newly_visible_records, quality_summary
risk_state:
  risk_revision, prediction_as_of, available_valid_range,
  current, plus_6h, plus_12h, plus_24h, resources
planning_state:
  plan_revision, planning_as_of, departure_time,
  executable_0_6h, rolling_0_24h, main_corridor_24_72h, full_voyage
ship_state:
  completed_track, current_position, current_executable_route,
  superseded_future_route, latest_planned_route
coverage / hard_reason / data_quality
events
```

## 11. Replay Manifest

候选 `SimulationReplayManifest`：

```text
scenario, scenario_mode,
simulation_start, simulation_end, tick_cadence,
snapshot_count,
snapshots: [{index, simulation_time, resource, snapshot_digest}],
events: [{time, type, revision, description}],
available_modes, provenance
```

Viewer 流程：`Manifest → Snapshot(t) → Presentation Resources`，不自行猜帧。

## 12. Event Model

| event | 状态 |
|---|---|
| `CLOCK_TICK` | DERIVABLE（每 tick 存在；当前无事件流） |
| `DATA_BECAME_VISIBLE` | DERIVABLE（A 可见集合变化可推出） |
| `DATA_REVISION_CHANGED` | DERIVABLE（digest 变化） |
| `B_UPDATED` | DERIVABLE（risk commit 变化） |
| `RISK_REVISION_CHANGED` | DERIVABLE（commit_id 变化） |
| `PLAN_COMPUTED` | CURRENTLY AVAILABLE（run-report 阶段记录） |
| `ROUTE_CHANGED` | DERIVABLE（layer-set digest / waypoints 对比） |
| `EXECUTABLE_ROUTE_CHANGED` | DERIVABLE（executable_0_6h digest） |
| `REPLAN_TRIGGERED` | CURRENTLY AVAILABLE（ReplanDecision.reasons） |
| `LIVE_REPLAN_STARTED / COMPLETED` | CURRENTLY AVAILABLE（demo serve API） |

## 13. Ship State

第三轮已实现 v1（replay-local，node-aligned），设计目标不变：

```text
completed_track          = executed route waypoints with eta <= simulation_time
current_position         = 由 executed route + simulation_time 插值（视觉插值，
                           不发明 risk frame）
current_executable_route = executable_0_6h（当前生效）
superseded_future_route  = 被 replan 替换的旧未来计划
latest_planned_route     = 最新 full_voyage / rolling
```

v1 明确限制：replan origin 只能是 grid node（C planner 合同），当前实现
使用 accepted route 最后到达 waypoint snap 到最近可通航 node（显式
tolerance + `snap_adjustment_km` 记录）；edge-interior 任意起点、连续
NavigationExecutionState production contract 与 moving-ship 动画属后续。

## 13.1 Presentation Adapter（2026-08-19）

Viewer 不直接读 replay 内部实现；`PresentationAdapter(manifest, snapshots)`
把 backend business semantics 投影成稳定 presentation contract：

```text
SimulationSnapshot / ReplayManifest
        ↓
PresentationAdapter（state_at(t) / vessel_at(t) / adoption_audit()）
        ↓
Viewer（只消费 presentation state + 60 FPS 平滑，不猜业务速度）
```

关键点：

- snapshot cadence（1h）≠ vessel render cadence；`vessel_at(t)` 用当前
  accepted plan 的 route waypoint ETA + `vessel_state_at` 计算任意时刻船位；
- `accepted_route`（physical-clock ETA）在 snapshot 中持久化，Adapter 不重算
  Planner、不改 route、不解释 risk 业务规则、不改 adoption timing；
- adoption audit 区分 `IMMEDIATE` / `NEXT_WAYPOINT_DEFERRED`，并同时报告
  `scheduled_adoption_time`（计划生效）与 `effective_adoption_time` /
  `route_changed_time`（实际生效，1h tick 评估）；
- `REPLAN_SKIPPED` / `PLAN_REUSED` 不渲染成 route 变化；`REPLAN_ADOPTED` /
  `ROUTE_CHANGED` 才是 adopted-route 切换。

真实 latest-head 12h 审计：0 `IMMEDIATE`、4 `NEXT_WAYPOINT_DEFERRED`
（rev2–5，另有 rev6 22:00 决策窗口外待生效）、决策时刻全部 mid-edge、
跨 adoption 无跳变。

## 13.2 Viewer MVP + L2 Preflight（2026-08-19）

- Presentation preflight：`replay/preflight.py` 把 artifact validation、L2
  GEBCO coastline、canonical EPSG:4326 transform、layer coverage 合并为
  `presentation_eligible` 唯一 verdict；`replay_viewer_preflight.py` CLI；
- L2 gate 改为 raster-cell traversal（mask grid，oversample <= 2x cell），
  不再按固定经纬度步长采样；语义对齐项目规范 `1=sea, 0=land_or_coast`；
- Viewer MVP 只消费 `viewer/bundle.json`（由 Presentation Adapter 生成）：
  Simulation Clock 驱动 basemap/route/track/vessel/pending；浏览器 60 FPS
  仅在 backend segment 上插值，不维护业务速度；`viewer/` 含 build_basemap /
  build_bundle / embed / render_proof / app.js；
- 真实 Scenario B 12h：L2 = 5 route revisions + completed tracks 全 PASS
  （0 land cell）；presentation eligible = True。

## 14. Artifact Reuse

- Snapshot 保存 identity/timestamps/revisions/digests/resource 引用/
  选中指标/事件元数据；
- 风险网格与路线引用 presentation resources，不复制大数组：
  `144 snapshots × full duplicate arrays` 明确禁止；
- 复用现有 committed risk store、layer-set、checksums。

## 15. Incremental / Event-driven Execution

```text
Simulation Clock tick(t)
        ↓
knowledge cutoff advances to t
        ↓
A resolves newly-visible records
        ↓
visible_record_set_changed ?
      /             \
    NO               YES
    │                 │
reuse data       new data_revision
    │                 ↓
    │              B update（可选窗口/增量）
    │                 ↓
    └────────┬────────┘
             ↓
       Replan Policy（TIME/DATA/RISK/DEVIATION/EVENT/MANUAL）
             ↓
       should_replan?
          /      \
        NO        YES
        │          ↓
     reuse C    C replan（被触发目标）
        │          │
        └────┬─────┘
             ↓
       D SimulationSnapshot(t)
             ↓
       ReplayManifest + resources
```

## 16. Frozen Retrospective Mode（Mode A）

保持 RC1/RC2 现状：

```text
knowledge_as_of = bundle.as_of_time（固定，晚于 simulation_start）
one-shot B full window → initial → +6h suffix replan
FROZEN_VALIDATED / RETROSPECTIVE BEST ESTIMATE 标识
```

## 17. Causal Replay Mode（Mode B）

```text
knowledge_as_of = simulation_time（每 tick）
visible set 由 issue_time <= t 决定
B/C 仅在 revision 变化时重算
CAUSAL 标识
```

当前历史证据只能支持末期短窗（A 19h / B 44h）→ MVP 从
`2026-08-15T10:00Z`（Scenario B）开始。

## 17.1 Performance Hardening（2026-08-19）

瓶颈定位：12h 回放耗时的 ≥95% 是 C 规划；其中一半以上的 C candidate 最终被
Switch Gate 拒绝（旧 12h：13 candidate → 7 rejected）。

Pre-planning gate（replay-local，不替代 Switch Gate）：

```text
  time-only + accepted-plan-age < interval（2h）
  → REPLAN_SKIPPED，不启动 C

  A data / B risk-content 变化 → 始终放行
  route 剩余 horizon 不足 interval → 不放行（fail-closed）
```

真实结果：

```text
12h candidate:   13 → 8
12h wall time:   2071.4s → 1306.8s（1.59×）
business:        13/13 snapshot 与旧 run 逐一一致
```

保持的边界：

- Replay ticks 仍严格串行；并行只限单次 C request 内三个 objective；
- 跳过的是“会重新生成同一份被拒 candidate”的 work，不是跳过业务决策；
- 每个跳过 tick 均发布 `REPLAN_SKIPPED` 事件并计入 summary，可审计。

## 18. Viewer Contract

- 主控：`simulation_time`；
- 次选择：B horizon（current/+6h/+12h/+24h）与 C 四层 × 三目标；
- 必显示：`scenario_mode`（CAUSAL / RETROSPECTIVE BEST ESTIMATE）、
  simulation_start、knowledge_as_of、risk valid time；
- 禁止把 145 valid_time 帧当 simulation ticks。

## 19. MVP Plan

```text
Scenario B，起点 2026-08-15T10:00Z，12–24h 子窗口
SimulationClock tick（1h）
  → A 可见集合变化（首个 tick 一次性可见 1537 条）
  → B 构建（一次；后续 tick 无新数据 → risk_revision 复用）
  → replan policy（TIME 触发一次；DATA 不触发）
  → C 重规划（触发时）
  → SimulationSnapshot(t) + ReplayManifest
→ 离线回放验证
```

## 20. Full 144h Expansion Plan

1. 建立 causal-ready 采集（实时 publication evidence / explicit_catalog /
   http_last_modified 保存）；
2. 新数据窗满足 12 类逐小时支撑后再扩全窗；
3. 再接入 GEBCO L2 coastline integrity（Geo Integrity gate 扩展）；
4. 最后做 moving ship / replan 动画 / timeline UI。
