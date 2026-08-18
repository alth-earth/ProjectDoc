# Strategy B Performance Hardening + Moving-Vessel Semantics（2026-08-19）

状态：报告完成（2026-08-19，本地 commit，未 push）
范围：Scenario B same-vessel causal replay 的性能硬化与船舶运动语义

## 1. Executive Summary

Strategy A（frozen retrospective）保持冻结；Strategy B（same-vessel
causal replay）继续为唯一主开发路径。本轮没有修改 C 的算法或四层合同，
而是先做 replan 成本审计，再用 replay-local pre-planning gate 削减必然被
Switch Gate 拒绝的 candidate 计算。

结果：

```text
12h authoritative replay:
  old = 2071.4s（≈34.5min）
  new = 1306.8s（≈21.8min）
  speedup = 1.59×，节省 ≈12.7min

C candidate computations: 13 → 8
rejected candidates:       7 → 2
pre-planning gate skips:   5

业务轨迹: 新旧 13/13 snapshot 逐一一致
（plan_revision 1→6、route/risk semantic digest 全等）

determinism: PASS
  manifest digest IDENTICAL
  snapshot digest 13/13 IDENTICAL
  risk route digest IDENTICAL
  wall-clock allowed to differ
```

Moving-vessel 语义已在 `NavigationExecutionState` 中补齐连续船位字段，并增加
stationary-vessel / cumulative-distance 机器校验。

## 2. Git

| repo | branch | HEAD | origin | ahead/behind | working tree |
|---|---|---|---|---|---|
| root | demo-engineering | 7f7aa8f | origin/demo-engineering | ahead 1 | `work_package_d/`（历史遗留未跟踪） |
| arctic_route_orchestrator | demo-engineering | fee3491 | origin/demo-engineering | ahead 2 | clean |
| work_package_c | demo-engineering | 42e951c | origin/demo-engineering | 0 | clean |
| work_package_a | demo-engineering | c6d0718 | origin/demo-engineering | 0 | clean |
| work_package_b | demo-engineering | 6269420 | origin/demo-engineering | 0 | clean |
| work_package_d | demo-engineering | 7681bf6 | origin/demo-engineering | 0 | clean |
| arctic_route_contracts | demo-engineering | 54ee071 | origin/demo-engineering | 0 | clean |

> 本轮结束后上方 HEAD / ahead 以 Git 真实状态为准（见最终报告）。

## 3. Filesystem Safety

```text
Writes outside /root/my_project = NONE
```

所有代码、测试、日志、PID、heartbeat、cache、replay 制品与 Git metadata 均位于
`/root/my_project/**`。长任务临时目录复用
`/root/my_project/.runtime/causal-replay-mvp/{logs,tmp,cache}`。

## 4. Strategy A Freeze

- RC1 golden regression：PASS
  - initial = `layer-set-sha256-51824e96...`
  - replanned = `layer-set-sha256-ec74a145...`
- RC2 second-scenario regression：PASS
  - `layer-set-sha256-e135e32d...` initial
  - `layer-set-sha256-6e101345...` replanned
- frozen digests / checksums 未改动；Strategy A 无语义变化。

## 5. Replan Cost Audit（旧 12h）

旧权威 12h（`sb-c-sem-hard-12hc`）：

```text
C candidate computations = 13（initial 1 + replan 12）
accepted = 6（initial + 5 ROUTE_CHANGED）
rejected = 7

accepted tick_seconds total = 991.2
rejected tick_seconds total = 1080.2
rejected 占比 ≈ 52%（tick_seconds 口径，含少量引擎开销）
```

结论：当前性能瓶颈不是核数不够，而是大量“必然被 Switch Gate 拒绝”的
TIME-only candidate 被重复计算。

## 6. Pre-Planning Gate

实现位置：
`arctic_route_orchestrator/src/arctic_route_orchestrator/replay/runner.py`
（`_should_skip_replan`）。

语义：

- 只允许跳过 TIME-only 重规划；任何 A data 或 B risk-content 变化
  （`DATA_REVISION_CHANGED` / `DATA_BECAME_VISIBLE` /
  `RISK_CONTENT_UPDATED` / `RISK_REVISION_CHANGED`）无条件放行；
- `--replan-min-interval-hours=2`：accepted plan 未满 2h 时跳过；
- 不替代 Switch Gate；跳过的 tick 发布 `REPLAN_SKIPPED` 事件；
- fail-closed：route 剩余 horizon 不足 2h 时不跳过。

实验对比：

```text
Policy A  当前 1h  baseline（旧）：12h = 2071.4s, 13 candidates
Policy B  2h interval gate（新）：12h = 1306.8s,  8 candidates
Policy C  waypoint-aligned gate ：3h = 278.3s（仅 initial），但 12h
          plan 卡在 1，与旧 accepted 序列不等价 → NOT ADOPTED
```

Waypoint-aligned 实验收录为技术债 TD-39（真实 route waypoint ETA 非整点，
如 12:17 / 14:34，只按当前 accepted route waypoint 对齐会在整点永远跳过）。

## 7. Moving-Vessel Semantics

`NavigationExecutionState` 新增（业务数据，非 UI 像素）：

```text
current_edge_index
current_segment_start_eta
current_segment_end_eta
effective_speed_knots
speed_source = waypoint_eta_linear_interpolation
executed_distance_km
cumulative_travelled_km
```

船位规则：

```text
position = interpolate(route waypoint ETA, simulation_time)
speed    = segment_km / (segment ETA span)（effective，非标称常量）
```

校验：

- validate_replay：active 船在 Δsimulation>0 时不允许静止；
- cumulative travelled 只增不减；completed_track append-only；
- no teleport（>80km/tick 标记）；
- 12h 新 run：cumulative 0.0 → 244.63km，`position_changes=12`，PASS。

## 8. Objective-Parallel 复查

1-tick 基准（真实 77h 窗口，v3 all layers）：

```text
per-call pool：167.1s C planning / 258.5s total
persistent pool + worker cache：167.5s C planning / 260.7s total
```

结论：worker 内组件重建不是当前瓶颈；不引入额外复杂度，默认保持 per-call
pool（persistent 作为显式 opt-in 保留）。

## 9. 12h Authoritative（2h pre-planning gate）

```text
replay_id = sb-perf-12h-gate2
window    = 2026-08-15T10:00Z → 22:00Z（12h, 1h snapshots）
snapshots = 13
total     = 1306.8s（≈21.8min）
C planning= 1172.3s

C candidate computations = 8（initial 1 + replan 7）
accepted = 6（initial + 5）
rejected = 2（12:00 / 13:00）
pre-gate skips = 5

plan_revision = 1 → 6
replan reasons = 全部 time（honest，无伪造 DATA）
B builds = 1；B reuse = 12；risk_content = 1；risk_window = 13
peak RSS ≈ 823.9MB（parent）；组合 ≈3.1GiB
validation：snapshots / replay / manifest 全 PASS
route integrity：末 tick 12 routes PASS
```

与旧 12h 业务等价性：

```text
13/13 snapshot：plan_revision / current_position / current_node /
edge_progress / remaining_distance_km / completed_track / status 全部一致
final route_semantic_digests：IDENTICAL
risk_semantic_digest：IDENTICAL
```

## 10. Determinism

同一 `replay_id`、独立输出根二跑（`sb-perf-12h-gate2-det`，1264.8s）：

```text
manifest semantic digest = IDENTICAL（fb60ec97...）
snapshot digest           = 13/13 IDENTICAL
risk semantic digest      = IDENTICAL
route semantic digest     = IDENTICAL
wall-clock / heartbeat    = DIFFERENT（允许）
```

## 11. 24h Extended Validation（optional）

```text
status = PASS
replay_id = sb-perf-24h-gate2（10:00Z → 次日 10:00Z，1h snapshots）
snapshots = 25
total     = 1743.2s（≈29.1min）
C planning= 1571.0s

C candidate computations = 14（initial 1 + replan 13）
accepted = 12（initial + 11）
rejected = 2
pre-gate skips = 11

plan_revision = 1 → 12
replan reasons = 全部 time（honest）
B builds = 1；B reuse = 24；risk_content = 1；risk_window = 25
peak RSS ≈ 824.3MB
validation：snapshots / replay / manifest 全 PASS

12h 前缀对比权威 12h：13/13 无差异（ship state / plan revision / track）
rejected 计算占比 = 21.0%
cumulative distance 0.0 → 489.26km；position_changes = 24；无 stationary /
teleport / track rewind
```

24h PASS 后再加跑并不必要；Full 144h 仍由 provenance 限制（NOT SUPPORTED）。

## 12. Resource Profile

```text
CPU = 32 logical（AMD Ryzen 9 7940HX，16C/32T）
memory = 7.4GiB total, 4.0GiB swap
正常任务红线 = ≤5–6GiB；3 workers 组合峰值 ≈3.1GiB
OOM = 0；swap = 0
```

## 13. Tests / Regression

```text
orchestrator replay unit : 34 passed（含 pre-gate 与 vessel motion）
work_package_c suite     : 142 passed
ruff                     : All checks passed（orchestrator + C）
RC1 golden regression    : PASS
RC2 second-scenario      : PASS
```

## 14. Documentation

- 新增 `STRATEGY_B_PERFORMANCE_HARDENING_20260819.md`（本文件）；
- 更新 `CURRENT_STATUS.md`、`TECH_DEBT.md`、
  `SIMULATION_REPLAY_ARCHITECTURE.md`、`TIME_MODEL_QUICK_REFERENCE.md`、
  `DEMO_ENGINEERING_STATUS.md`、`CAUSAL_REPLAY_MVP_20260818.md`、
  `STRATEGY_B_SEMANTIC_HARDENING_20260818.md`、`DOCUMENTATION_INDEX.md`、
  `ARCTIC_ROUTE_SYSTEM.md`、`DEMO_RUNBOOK.md`、`POST_RC1_PLAN.md`、
  `项目梳理报告.md`、`最终交付说明.md`；
- `arctic_route_orchestrator/CHANGELOG.md` 新增本轮条目。

## 15. Current Status

```text
Strategy A
= FROZEN RETROSPECTIVE FALLBACK

Strategy B
= SAME-VESSEL CAUSAL REPLAY + PERFORMANCE HARDENED

A causal visibility       PASS
B causal risk             PASS
C v3 four-layer           PASS
Navigation execution      PASS
Vessel motion semantics   PASS
Snapshot / Manifest       PASS
Semantic determinism      PASS
Route integrity           PASS

12h authoritative replay：
  old 34.5min → new 21.8min（1.59×）

Full 144h historical causal replay
= NOT SUPPORTED BY CURRENT PROVENANCE
```

## 16. Next Phase

```text
Replay-driven Presentation Viewer
→ GEBCO
→ L2 coastline integrity
→ Simulation Timeline
→ Dynamic B Risk
→ Dynamic C Route
→ MOVING SHIP（正式功能，不可遗漏；必须沿 route ETA 随 simulation clock
   连续移动，replan 后继续从当前船位航行）
→ Replanning Event Animation
```

技术建议：下一轮 Viewer 只消费后端 Snapshot 给出的 vessel position，
不自行猜测像素速度。

## 17. Commits（本轮）

```text
orchestrator:
  946c7b4 perf: add causal replay pre-planning gate and vessel motion audit
```

```text
root:
  7f7aa8f docs: establish strategy B performance hardening and moving-vessel status

orchestrator:
  946c7b4 perf: add causal replay pre-planning gate and vessel motion audit
  fee3491 docs: record strategy B performance hardening and 24h validation
```

## 18. Push

```text
PUSH = NOT PERFORMED
```

请操作者回来后人审并手动 push。
