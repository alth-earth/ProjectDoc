# Simulation Replay Architecture（候选设计，2026-08-17）

> 状态：**DESIGN ONLY**（不修改 production contracts，不实现播放器）
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

只设计，不实现：

```text
completed_track          = executed route waypoints with eta <= simulation_time
current_position         = 由 executed route + simulation_time 插值（视觉插值，
                           不发明 risk frame）
current_executable_route = executable_0_6h（当前生效）
superseded_future_route  = 被 replan 替换的旧未来计划
latest_planned_route     = 最新 full_voyage / rolling
```

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
