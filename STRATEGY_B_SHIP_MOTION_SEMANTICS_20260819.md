# Strategy B Ship Motion Semantics（2026-08-19）

状态：本报告随本轮完成（本地 commit，未 push）
范围：仅 NavigationExecutionState / ship position / speed / route adoption /
completed track / no-teleport / arrival 的后端业务语义。

## 1. Executive Summary

```text
SHIP PHYSICAL MOTION           = PASS
Planner Origin                 = NODE-ALIGNED v1（独立于 physical position）
Deferred Replan Adoption       = IMPLEMENTED（mid-edge 决策不瞬移）
No-replan continuous motion    = PASS
Completed track                = APPEND-ONLY
Arrival                        = ARRIVED / speed=0 / position=destination
Edge-interior planner origin   = FUTURE CONTRACT WORK
```

上一轮已经具备连续 position 字段，但 replan 时 C 的 grid-node start 与
physical position 没有完全分离。本轮做了三点硬性修正：

1. 新增纯 kinematics 模块 `replay/vessel_motion.py`：`vessel_state_at(t)`
   可在任意 `simulation_time` 返回连续 physical position / speed / status；
2. `physical_position` 与 `planner_origin_node` 分离：planner snap 不再写回
   物理船位；
3. replan 采用 next-waypoint deferred adoption：mid-edge 决策时船继续沿旧
   accepted route 航行，新路线在下一个执行节点生效（不瞬移）。

## 2. Git Baseline

所有仓库位于 `demo-engineering`，本轮不建分支、不 merge/rebase/reset/push。
开始 HEAD：orchestrator `fee3491`、root `8f31f6b`。结束时见 Git 状态。

## 3. Filesystem Safety

```text
Writes outside /root/my_project = NONE
```

## 4. Ship Movement Verdict

```text
PASS
```

船由 `simulation_time` 推进、沿 accepted route 的 waypoint ETA 连续移动；
`Snapshot` 1h cadence 不等于船只能每小时跳一次（`vessel_state_at` 支持任意
时刻查询）。

## 5. Position Model

```text
source       = accepted RoutePlan waypoints + ETA
segment      = (waypoint_i, waypoint_i+1)
interpolation= linear lon/lat，与 C RegularGrid.edge_sample_points 保持
               同一 route-edge 几何 contract（高纬差异已记录）
fraction     = (t - T_i) / (T_i+1 - T_i)
physical_pos = 按上述 fraction 位于 segment 上
```

## 6. Speed Model

```text
segment_speed = segment_distance / (T_i+1 - T_i)
units         = m/s + knots（集中转换，MPS_PER_KNOT=0.5144444）
```

真实 12h artifact audit：

```text
speed knots: count=13, min=9.632, mean=9.656, median=9.653, p95=9.684, max=9.684
1h vessel travel: mean≈20.4km（median≈17.9km, max≈28.0km）
no stationary-while-underway
```

## 7. Movement Without Replanning

`vessel_state_at(t1) < vessel_state_at(t2) < vessel_state_at(t3)`
（unit T4 + 5min 高频采样测试）验证：同一 plan、时钟推进 → executed distance
严格递增、position 变化、speed>0。

## 8. Replan / Adoption Semantics

```text
decision_time         = 产生 candidate 的 simulation_time
physical_position_at_decision = 决策时真实船位（不移动）
planner_origin_node   = accepted route 上可计算的 grid node
mode                  = IMMEDIATE（正好在 waypoint）| NEXT_WAYPOINT_DEFERRED
effective_adoption_time = 下个 waypoint ETA（deferred）
```

mid-edge 决策时：

```text
accept candidate
-> physical vessel 继续当前 segment
-> 到达 planner_origin_node 时 REPLAN_ADOPTED / ROUTE_CHANGED
-> 新路线生效（未来部分）
```

## 9. No Teleport

unit `test_deferred_replan_keeps_physical_position_until_adoption`：decision
前后 `vessel_state_at` 位置/速度逐位一致。Snapshot 级 `validate_replay` 仍保留
`>80km/tick` teleport 检查。

## 10. Snap Audit（真实 12h artifacts）

```text
snap_adjustment_km: count=13, min=0.0, mean=8.25, median=5.10, p95=17.94, max=17.94
grid edge: median=40.77km（mean=42.8, min=40.77, p95=48.9）
1h travel: mean≈20.4km
```

结论：实际 snap 中位数约 5km、最大 18km，远小于 grid edge；
physical / planner 分离后 snap 只影响 planner origin，不影响船位。

## 11. Completed Track

```text
APPEND-ONLY = PASS
```

`merge_completed_track` 保持既有 track 前缀；新路线只改变未来。

## 12. Arrival

```text
t >= final ETA -> status=ARRIVED, position=destination, speed=0
```

不允许越过终点。

## 13. Navigation Status

```text
NOT_STARTED（t < departure）
UNDERWAY（departure <= t < arrival）
ARRIVED（t >= arrival）
```

validation 同时向后兼容历史 `ACTIVE`。

## 14. Short Real Smoke

```text
replay_id = sb-ship-motion-2h（10:00Z -> 12:00Z）
snapshots = 3
duration  = 573.5s（C planning 476.6s）
status    = UNDERWAY on every snapshot
speed     = 9.632 knots / 4.955 m/s（tested edges）
position  : 70.3333N -> 70.4938N -> 70.6542N（连续推进）
cumulative: 0.0 -> 17.84 -> 35.68 km
planner origin: [5,7] -> [6,7] -> [6,7]（adjustment 0；与 physical 分离）
adoption  = NONE（无 replan 被采纳；候选被 Switch Gate 拒绝）
validation: snapshots / replay / manifest 全 PASS
```

## 15. Tests

- `tests/unit/test_vessel_motion.py`：T1 segment speed / T2 exact waypoint /
  T3 mid-edge / T4 continuous progress / T5 arrival / T6 invalid ETA /
  5min 高频采样；
- `tests/unit/test_replay_navigation.py`：deferred replan 不瞬移、completed
  track append-only、模型 new fields roundtrip、replan reasons；
- `tests/unit` suite 42 项 PASS；ruff 全绿。

## 16. Known Limitation

```text
Planner Origin = NODE-ALIGNED v1
Edge-interior C origin = EDGE_INTERIOR_ORIGIN_CONTRACT_GAP（future）
```

## 17. Viewer Readiness

```text
YES（后端已能回答任意 simulation_time 的 position / speed / segment /
executed / remaining / arrival；Viewer 直接消费即可，不猜像素速度）
```

## 18. Current Project Status（navigation 相关）

```text
Strategy A = FROZEN RETROSPECTIVE FALLBACK
Strategy B = SAME-VESSEL CAUSAL REPLAY
Ship motion semantics = PASS
Physical motion = CONTINUOUS
Speed = DERIVED FROM ROUTE DISTANCE / ETA
No-replan movement = PASS
No teleport on replan = PASS
Completed track = APPEND-ONLY
Planner origin = NODE-ALIGNED v1（explicit adoption semantics）
Edge-interior planner origin = FUTURE CONTRACT WORK
```

## 19. Commits

本轮 commit 以 Git log 为准（orchestrator）。

## 20. Push

```text
PUSH = NOT PERFORMED
```
