# Strategy B Viewer Foundation（2026-08-19）

状态：本报告随本轮完成（本地 commit，未 push）
范围：Strategy B causal replay + continuous physical vessel motion +
deferred replan adoption 联合在最新 HEAD 成立，并建立 Replay Presentation
Adapter / Presentation Contract 与 GEBCO / L2 地理基础。

## 1. Executive Summary

```text
Strategy A             = FROZEN RETROSPECTIVE FALLBACK（未改动）
Strategy B             = SAME-VESSEL CAUSAL REPLAY
                         + PERFORMANCE HARDENED
                         + PHYSICAL VESSEL MOTION HARDENED
                         + VIEWER BACKEND BASELINE FROZEN

12h latest-head authoritative = PASS（最新 HEAD 联合基线）
latest-head determinism       = PASS（见 §7）
Presentation Adapter          = ESTABLISHED
GEBCO Presentation Foundation = ESTABLISHED / IN PROGRESS
L2 coastline integrity         = NEXT（gate contract + 本地真实数据 smoke PASS）
Simulation Timeline            = NEXT
Dynamic Risk / Route           = NEXT
Moving Ship Presentation       = NEXT
Replanning Animation           = NEXT
Full 144h historical causal replay = NOT SUPPORTED BY CURRENT PROVENANCE
```

本轮没有继续泛化优化 Planner。核心结论是：在最新 HEAD（ship-motion + deferred
adoption 之后的代码）上，性能硬化（2h pre-planning gate）与连续物理船位语义
联合成立；真实 12h 中所有已采纳 replan 都是 `NEXT_WAYPOINT_DEFERRED`（没有
`IMMEDIATE`），决策时 `physical_at_waypoint = false`，跨 adoption 无跳变。

## 2. Git Baseline

| repo | branch | HEAD | ahead/behind | working tree |
|---|---|---|---|---|
| root | demo-engineering | c5508fd（起始） | ahead 2 | work_package_d/（历史遗留未跟踪） |
| arctic_route_orchestrator | demo-engineering | abbc12b（起始） | ahead 1 | 本轮新增/修改 |
| work_package_a | demo-engineering | c6d0718 | 0 | clean |
| work_package_b | demo-engineering | 6269420 | 0 | clean |
| work_package_c | demo-engineering | 42e951c | 0 | clean |
| work_package_d | demo-engineering | 7681bf6 | 0 | clean |
| arctic_route_contracts | demo-engineering | 54ee071 | 0 | clean |

结束 HEAD / ahead 以 `git status` 为准；本轮只做本地 commit，`PUSH = NOT
PERFORMED`。

## 3. Filesystem / Resource Safety

```text
Writes outside /root/my_project = NONE
swap use                          = 0
OOM                               = 0
double heavy replay               = 无（始终只跑一个 12h/C replay）
```

运行记录（latest-head 12h）：

```text
command = causal_replay_mvp --replay-id <id> --window-hours 12
          --planning-workers 3 --replan-min-interval-hours 2
          --parallel-pool-mode percall
output root = work_package_a/data/output/rc2-smoke/causal-replay-mvp/<id>
log         = .runtime/causal-replay-mvp/logs/replay-<id>.out
peak RSS    = 824.3 MB（parent）
```

## 4. Latest-HEAD 12h Authoritative

最新 HEAD 联合基线以 `sb-viewer-baseline-12h`（首次）与
`sb-viewer-baseline-12h-det`（同配置独立目录复跑）为准。二者业务语义一致，
复跑摘要以最终表为准（见 §7）。

```text
window        = 2026-08-15T10:00Z → 22:00Z（12h, 1h snapshots）
snapshots     = 13
total         = 2044.9s（authoritative det；首次 1976.4s）
C planning    = 1894.7s
plan_revision = 1 → 5（窗口内；另有 rev6 于 22:00 决策、窗口外待生效）
validation    = snapshots PASS / replay PASS / manifest PASS
route integrity = PASS（首末 snapshot 各 12 routes）
risk / content = risk_content_revision 1；risk_window_revision 13
peak RSS      = 822.7 MB
```

候选 / 采纳 / 拒绝计数以修正后的复跑 summary 为权威（见最终表）。注意：旧版
summary 只把 `REPLAN_TRIGGERED` 计为 accepted，没有把 `REPLAN_DECIDED`
计为已采纳候选，本轮已修正该统计 bug 并复跑验证。

```text
candidate computations（修正后）= 12
accepted（含 initial）          = 6（initial + 5 REPLAN_DECIDED）
rejected                      = 6
pre-gate skips                = 1
```

## 5. Adoption Audit（真实 12h，latest HEAD）

对 accepted candidate / replan decision 的机器可读审计结果（
`PresentationAdapter.adoption_audit()`）：

```text
accepted replan（窗口内已生效）= 4（rev2–rev5）
IMMEDIATE                    = 0
NEXT_WAYPOINT_DEFERRED       = 4
窗口外待生效决策              = 1（rev6，22:00 决策，计划 23:40 生效）

physical_at_waypoint：全部 false（mid-edge 决策，edge_progress > 0）
snap_adjustment_km：
  min=0.0  median=0.0  p95=0.0  max=0.0
  （origin waypoint 已落在可通航 grid node，无需 snapping）
```

每个决策都显式给出：

```text
decision_time / physical_lon / physical_lat
physical_current_edge_index / physical_edge_progress
physical_at_waypoint / planner_origin_node / planner_origin_lon/lat
snap_adjustment_km / adoption_mode
scheduled_adoption_time / effective_adoption_time / route_changed_time
plan_revision before/after / completed_track_length before/after
```

回答历史问题：过去报告认为“真实 12h replans 恰好都在 waypoint / 都是
IMMEDIATE”——这在旧实现（planner snap 立即改写当前 plan）下成立，但在最新
HEAD 的 deferred adoption 语义下不成立：真实 13:00 / 15:00 / 17:00 / 20:00 /
22:00 决策全部发生在 edge 内部（`physical_at_waypoint=false`），并以
`NEXT_WAYPOINT_DEFERRED` 在后续执行节点生效。

## 6. Presentation Adapter / Contract

新增：

```text
src/arctic_route_orchestrator/replay/presentation.py
scripts/replay_presentation.py
```

Adapter 只做“backend business semantics → stable presentation semantics”，
不重新计算 Planner、不改变 route、不重新解释 risk 业务规则、不自行制造船速、
不改变 adoption timing。Viewer 不需要理解 replay 内部实现细节。

最小输出 contract 覆盖：

```text
simulation_time / knowledge_as_of / scenario_mode
vessel: status lon lat speed_mps speed_knots current_edge_index
        edge_progress executed_distance_km cumulative_travelled_km
        remaining_distance_km physical_position_source
plan:   accepted_plan_revision completed_track
        current_authoritative_segment accepted_future_route
        pending_candidate pending_adoption superseded_future_route
risk:   risk_content_revision risk_window_revision current_resource
        available_valid_range hard_reason_resource presentation_horizons
events: REPLAN_TRIGGERED / REPLAN_SKIPPED / PLAN_REUSED /
        REPLAN_ADOPTED / ROUTE_CHANGED / ARRIVED（及原始事件）
```

船位任何渲染时刻由后端 route ETA 决定：

```text
render simulation_time
→ 当前 accepted plan revision（route-changed 事件索引）
→ accepted_route waypoint ETA（snapshot 已保存，物理时钟语义）
→ vessel_state_at(t) → continuous lon/lat / speed / segment
```

Snapshot cadence（1h）≠ vessel render cadence。Adapter 通过
`state_at(t)` / `vessel_at(t)` 支持任意时刻查询（如 10:05 / 10:10），前端
只做 60 FPS 平滑，不维护 `shipSpeedPixelsPerSecond`，不在 CSS 里估计航速。

## 7. Determinism（Latest HEAD）

同一配置、独立输出目录复跑：

```text
replay_id（rerun） = sb-viewer-baseline-12h-det
manifest semantic digest = IDENTICAL（1bdcbce5...）
snapshot semantic digest = 13/13 IDENTICAL
route semantic digest    = IDENTICAL
risk semantic digest     = IDENTICAL
wall-clock / PID / heartbeat / generated_at = 允许不同
```

结论以复跑最终比对为准。

## 8. GEBCO / L2 Foundation

本轮做基础（不做最终 Viewer / 不做大量下载）：

```text
replay/geospatial.py：
  - BasemapMetadata（projection=EPSG:4326, bbox, width/height, source,
    version/provenance）
  - CanonicalGeographicTransform（risk/route/completed track/vessel 共享
    同一个 transform；projection_consistency_gate 防二次变换）
  - LandMaskSampler + load_netcdf_land_mask（读本地 GEBCO_2026
    land_sea_mask .nc）
  - l2_coastline_gate（route edges/track/waypoints 线性 lon/lat 采样，
    LAND/DATA_UNAVAILABLE fail-closed）
```

本地已存在真实 GEBCO 2026 派生 land_sea_mask：

```text
source        = GEBCO_2026 / CEDA OPeNDAP
snapshot      = gebco-2026-d5a7e2fe3915-7baad866
doi           = https://doi.org/10.5285/4f68d5c7-45eb-f999-e063-7086abc036fa
resolution    = 0.05 deg（~5.5 km）
scenario B bbox ≈ lon 10.0–22.05, lat 68.5–79.55
```

真实数据 smoke（L2 gate contract + harness；极性修正声明：本地 GEBCO
`land_sea_mask` 规范语义为 `1=sea,0=land_or_coast`）：

```text
海域路线 (18.40, 70.50) → (18.40, 73.00)：PASS（0 violation）
陆域路线 (15.00, 68.50) → (16.00, 68.50)：FAIL（LAND sample）
```

L2 本轮是 contract + test harness + 本地数据 smoke（实际运行），不是全场景
corridor 门禁；正式 L2 门禁并入 demo preflight 属下一轮。

## 9. Tests

```text
orchestrator replay presentation unit : T1 snapshot→presentation 映射
                                        T2 连续船位（任意时刻）
                                        T3 stationary regression
                                        T4 arrival
                                        T5 completed track append-only
                                        T6 deferred adoption 语义
                                        T7 PLAN_REUSED/REPLAN_SKIPPED
                                           无假 route_changed
                                        + adoption audit（IMMEDIATE/DEFERRED）
                                        + 旧 schema 任意时刻拒绝
geospatial unit                       : canonical transform / 共享 transform
                                        gate / L2 synthetic / L2 真实数据 smoke
ruff                                   : PASS
unit suite（not integration）          : 70 passed, 2 deselected
```

## 10. Next Recommendation

下一轮进入正式 Viewer：

```text
GEBCO real basemap
→ L2 coastline gate（并入 demo preflight）
→ Simulation Timeline
→ Dynamic Risk（presentation horizons）
→ Dynamic Route
→ MOVING SHIP（消费 adapter vessel_at，不自行猜测航速）
→ Replanning Animation（区分 REPLAN_DECIDED / REPLAN_ADOPTED）
```

## 11. Push

```text
PUSH = NOT PERFORMED
```

请操作者回来后人审并手动 push。
