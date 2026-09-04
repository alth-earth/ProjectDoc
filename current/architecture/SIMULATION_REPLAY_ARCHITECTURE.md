---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - PLANNED
Document Role: CANONICAL
Scope: simulation replay engine + presentation adapter + viewer artifact boundary
Canonical For: how replay snapshots, digests, presentation export and Viewer handoff work
Branch: research-validation-system
Last Verified: 2026-09-04 19:17 +08:00
---

# Simulation Replay Architecture（设计 + 实现，2026-08-17 起，经 2026-08-20 治理审计）

## 0.1 Current implementation evidence（2026-09-01 23:40 +08:00）

当前回放引擎支持显式 `causal_replay` 与 `retrospective_dynamic_replay` 两种模式。真实
Winter holdout 回放 `winter-retro-holdout-resource-v4` 产生 3 个 snapshots、17 个事件
和 3 个 content-addressed plan revisions；每个 revision 都是四层×三目标（12 条）资源，
并记录 `REPLAN_DECIDED`、`REPLAN_ADOPTED` 与 `ROUTE_CHANGED`。后者保留原始 issue time，
只声明事后动态投影；严格 causal 窗口仍按 issue-time 门禁失败关闭。

RC2 objective-level 三核并行已进入正式 Orchestrator 初始/重规划路径：真实 summary 为
`requested_workers=3`、`effective_workers=3`、`max_parallel_tasks=3`、36 个 objective
tasks；tick、layer、B 和 adoption gate 继续串行。`worker_pids` 仅作为跨调用 provenance，
不能解释成同时运行的 9 核。

### 2026-09-04 19:17 +08:00 Winter v3 dynamic replay evidence

最新的 2026-02-15 Winter 重建回放位于
`.runtime/replays/winter-rebuilt-20260215-retro-dynamic-v3/`，并通过
`winter-rebuilt-20260215-viewer-package-v3` 投影到外部 Viewer。它复用同一 A Bundle、145
帧 RiskWindow 和同身份 Risk Explanation，回放窗口为
`2026-02-15T00:00:00Z → 2026-02-21T00:00:00Z`，6 小时 tick，共 25 snapshots、6 个 plan
revisions 和 5 组真实 `REPLAN_DECIDED → REPLAN_ADOPTED → ROUTE_CHANGED`；最终
`ship_state.status=ARRIVED` 且 `pending_route=null`。

该运行明确标记为 `retrospective_post_hoc_dynamic_projection`，保留原始 `issue_time`，不
表示严格 causal replay、实时预测或导航/实船资格。C 使用
`winter_motion_reserve_5pct`（规划速度预留 5%，不改船模最大速度/环境速度）和
`winter_dynamic_replay`（6h interval、1% gain、1% hysteresis、最大风险回退容差 0%）；
Orchestrator 通过命名 CLI 参数传播 profile 与 digest，worker 不重新读取默认配置。初始
三个 full-voyage 候选和实际采用路线均为 `CURVE`；R1–R6 六套 candidate-motion transport
均已绑定。未采用的 R3 executable/fastest `RAW` 仅保留为比较层和真实
`minimum_radius_exceeded` 失败证据。

v3 assembly 为
`winter-viewer-sha256-1a50c77c012285404d96d3de1cdb0cd563214371911c6ae0c066c3280f5e8afd`；
`bundle.json` 和 `checksums.json` 的 SHA-256 分别为
`3772a5d621bd058ef58d6b8aadc0254a15f3bd44cc027b7e10c4c63ceacf58ed` 和
`a96c61138f089a962e21dbaa481521db3213376f2bcbcb90aafe8ce2cb2627ff`。发布器只写包内相对
引用/摘要，20 个白名单文件中 `publish-summary.json` 与其余 18 个数据/manifest 文件均由
checksum 覆盖（不含 checksums 自身）；当前 AppImage 不重建，外部导入流程负责
`inbox → validation → ready`。

> 状态：**DESIGN + ENGINE MVP IMPLEMENTED（2026-08-18） + VIEWER MVP IMPLEMENTED（2026-08-19）**
> 已实现：replay models/digests/runner/validation/inspector；真实 12h/24h/44h
> Scenario B 回放 PASS（engine level）；C 四层因风险窗 < ETA 保持
> PLANNING-HORIZON ARCHITECTURE BLOCKER（诚实 fail-closed）；
> Viewer（`work_package_d`）消费 Presentation Adapter 导出的 `bundle.json`，
> Simulation Clock 驱动渲染，船舶连续运动已验证（12h baseline 0 land cell）。
> 详细结果：[`CAUSAL_REPLAY_MVP_20260818.md`](../../reports/strategy-b/CAUSAL_REPLAY_MVP_20260818.md)、
> [`STRATEGY_B_VIEWER_MVP_20260819.md`](../../reports/strategy-b/STRATEGY_B_VIEWER_MVP_20260819.md)
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

Winter v3 的受控 profile `winter_dynamic_replay` 将最小间隔设为 6 小时、路线收益阈值设为
1%、风险迟滞设为 1%，并将最大风险回退容差固定为 0%。因此候选最大风险不得恶化；这些
参数只改变是否进入 Switch Gate，不绕过海陆、unknown、时间覆盖、走廊、操纵性或 ETA 等
正式门禁。v3 全窗口实际产生 5 组 `REPLAN_DECIDED → REPLAN_ADOPTED → ROUTE_CHANGED`；
中边决定保留到下一执行节点采用，船位不跳跃。

## 9. C Plan Revision

- 只在 replan policy 触发时重算；
- 重算只重做被触发目标（MVP：recommended；扩展：四层 × 三目标）；
- 每次发布获得新 `plan_revision` 与 layer-set digest；
- `ROUTE_CHANGED / EXECUTABLE_ROUTE_CHANGED` 事件按需产生。

Winter v3 的 `PlannerConfig` 通过向后兼容的
`operational_speed_reserve_fraction` 设为 0.05，仅在 ETA 规划时使用预留后的速度；船模
最大速度、环境可用速度和正式安全门禁不被修改。命名 profile 为
`winter_motion_reserve_5pct`，serial/parallel worker 使用同一 config digest。该运行发布 6
个不可变 revision，每版保留四层×三目标=12 条候选；初始三个 full-voyage 候选及所有实际
采用路线的 formal motion 均为 `CURVE`。若某一未采用 comparison candidate 只有 RAW，必须
保留其真实状态（v3 的 R3/R4 executable 即如此），不得通过 D 改标。

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

Winter v3 manifest 记录 `planner_name=winter_motion_reserve_5pct`、
`replanning_name=winter_dynamic_replay` 及各自摘要，且包含 25 个 snapshot 资源和 113 个
事件；manifest semantic digest 为
`bbe77ec8caa07364959d1436ad4675f87a3f66c7c9c068153265514c8c1d0b6b`。plan revision index
为 `planning-revisions/index-6920b194a63e6cb8c55298fd9fc5f45482b94f1b8955cb61698b61c2b28ad55c.json`，
由 Viewer exporter 以包内相对引用传输，不能携带构建机绝对路径。

## 12. Event Model

| event | 状态 |
|---|---|
| `CLOCK_TICK` | CURRENTLY AVAILABLE（v3 25 个 tick 均写入 manifest/snapshot） |
| `DATA_BECAME_VISIBLE` | DERIVABLE（A 可见集合变化可推出） |
| `DATA_REVISION_CHANGED` | DERIVABLE（digest 变化） |
| `B_UPDATED` | DERIVABLE（risk commit 变化） |
| `RISK_REVISION_CHANGED` | DERIVABLE（commit_id 变化） |
| `PLAN_COMPUTED` | CURRENTLY AVAILABLE（v3 初始 revision 已记录） |
| `ROUTE_CHANGED` | CURRENTLY AVAILABLE（v3 5 次，并与 adopted revision 绑定） |
| `EXECUTABLE_ROUTE_CHANGED` | DERIVABLE（executable_0_6h digest） |
| `REPLAN_TRIGGERED` | CURRENTLY AVAILABLE（由 `REPLAN_DECIDED` 的真实原因记录） |
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

Winter v3 的 6 小时回放实际记录 5 次 deferred adoption；每次决定、到达执行节点后的采用
和路线变化都带 revision 身份，最终快照为 `ARRIVED` 且 `pending_route=null`。Viewer 的
运行锁只固定实际运行 candidate、motion、ETA 与路线来源；路线层、三目标显隐和候选卡片
高亮属于展示状态，不得改变运行身份或船位。

此前 latest-head 12h 审计（历史证据）：0 `IMMEDIATE`、4 `NEXT_WAYPOINT_DEFERRED`
（rev2–5，另有 rev6 22:00 决策窗口外待生效）、决策时刻全部 mid-edge、
跨 adoption 无跳变。

## 13.2 Viewer MVP + L2 Preflight（2026-08-19）

- Presentation preflight：`replay/preflight.py` 把 artifact validation、L2
  GEBCO coastline、canonical EPSG:4326 transform、layer coverage 合并为
  `presentation_eligible` 唯一 verdict；`replay_viewer_preflight.py` CLI；
- L2 gate 改为 raster-cell traversal（mask grid，oversample <= 2x cell），
  不再按固定经纬度步长采样；语义对齐项目规范 `1=sea, 0=land_or_coast`；
- Viewer (in `work_package_d`) consumes only `viewer/bundle.json`, produced by the
  orchestrator Presentation Adapter (`scripts/replay_viewer_export.py`): Simulation
  Clock drives basemap / route / track / vessel / pending; the browser interpolates
  only on backend segments at 60 FPS and does **not** invent business speed. The
  Viewer implementation lives in `work_package_d/viewer/` (app.js, embed.py,
  render_proof.py, pngcodec.py), owned solely by D; the orchestrator does not host
  the Viewer runtime.
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

Winter v3 使用更明确的 `retrospective_post_hoc_dynamic_projection` 标识：它可以由真实 C
重算、Switch Gate 和 replay event 展示多个 revision/adoption，但因为保留的 source
`issue_time` 晚于仿真起点，不能解释为当时可用信息驱动的 causal 决策。该模式不自动获得
实时预测、导航级或实船资格。

## 17. Causal Replay Mode（Mode B）

```text
knowledge_as_of = simulation_time（每 tick）
visible set 由 issue_time <= t 决定
B/C 仅在 revision 变化时重算
CAUSAL 标识
```

当前历史证据只能支持末期短窗（A 19h / B 44h）→ MVP 从
`2026-08-15T10:00Z`（Scenario B）开始。

Winter v3 不属于 Mode B；严格 causal 版本仍需一个 issue-time、publication-time 和完整
12 类覆盖均可审计的输入窗口，未满足前保持 fail-closed。

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

> 2026-09-01 更新：真实 Winter holdout 已先以明确标注的
> `retrospective_dynamic_replay` 发布 revision/event 资源并接入 Viewer；以下计划仍适用于
> 严格 issue-time causal 版本，不能将事后投影升级为 causal replay。

2026-09-04 的 v3 已在原始 Winter 重建身份上完成 144h retrospective dynamic replay（25
 snapshots、6 revisions、5 adopted chains、ARRIVED），因此本节后续工作只针对严格 causal
 版本，不再重复下载或重建已有 A 数据。

1. 建立 causal-ready 采集（实时 publication evidence / explicit_catalog /
   http_last_modified 保存）；
2. 新数据窗满足 12 类逐小时支撑后再扩全窗；
3. 再接入 GEBCO L2 coastline integrity（Geo Integrity gate 扩展）；
4. 最后做 moving ship / replan 动画 / timeline UI。
