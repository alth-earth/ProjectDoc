---
Document Status: ACTIVE_CANONICAL
Scope: time model quick reference (issue/valid/knowledge/simulation/generated)
Canonical For: time-field semantics and causality rules
Branch: demo-engineering
Last Verified: 2026-08-20
---

# Time Model Quick Reference（2026-08-17）

面向后续开发者的最短时间速查。完整审计见
[`TEMPORAL_SEMANTICS_AUDIT_20260817.md`](../../reports/audits/TEMPORAL_SEMANTICS_AUDIT_20260817.md)。

## 总原则

```text
issue_time       = A 数据可见性门禁（什么时候系统允许知道）
valid_time       = 数据描述/预测有效的环境时刻（不代表那时可知）
knowledge_as_of  = 逻辑知识截止（causal 下 == simulation_time；
                    不是“已选数据最新 issue_time”）
max_source_issue_time = 当前可见/已选记录中最大的 issue_time（结果统计）
simulation_time  = 仿真当前时刻（causal 下 == knowledge_as_of）
generated_at     = 墙钟生成时刻（禁止用于因果）
```

## 字段速查

| field | meaning | owner | DO | DON'T |
|---|---|---|---|---|
| `issue_time` | A 可见性门禁 UTC | A | 用作 visibility gate：`issue_time <= knowledge_as_of` | 当 valid_time；当 ingest_time；当 B 通用预测发布时间 |
| `valid_time` | 环境/预测有效时刻 | A/B/C | 描述环境时刻；作为 risk 帧时间轴 | 当可知时刻；当 simulation_time |
| `knowledge_as_of` | 固定知识截止 | A→B→C | 保持全链一致；bundle.as_of_time 精确相等 | 每 tick 随意变动而不 bump generation |
| `max_source_issue_time` | 可见记录最大 issue_time | A | 作为可见性统计/数据集合摘要 | 当 knowledge_as_of 本身 |
| `visible_record_set_digest` | 可见记录集合身份 | A | 判断 data_revision 是否变化 | 当数据内容 digest |
| `data_revision` | 输入集合版本 | A/orchestrator | 集合变化时 +1 | 每 tick 无脑 +1 |
| `simulation_time` | 仿真推进时刻 | A/orchestrator | 因果模式与 knowledge_as_of 相等；作为 departure/ETA 轴 | 从 generated_at/heartbeat 推断 |
| `forecast_reference_time` | 预测参考时刻 | A | 与 lead 一起保存；校验 reference+lead==valid_time | 当 issue_time |
| `forecast_lead_hours` | 预测步长 | A | 与 reference 成对出现 | 单独使用；用 lead 冒充 simulation offset |
| `ingest_time` | A 登记时刻 | A | 只做审计 | 当 issue_time |
| `observed_at` | 证据观测时刻 | A | 保存在 evidence | 当生产者发布时间 |
| `as_of_time` | B/C 计算的知识边界（RiskFrame / RoutePlan） | B/C | 从 bundle.as_of_time 原样传播 | 从源 issue_time 重新推断 |
| `start_time` | C 出发/规划参考 | C | = simulation_start（initial）或 +6h（replan） | 与 simulation_end 混淆 |
| `eta` | waypoint 绝对 UTC 到达时刻 | C | 作为 ship position 时间戳 | 当航行时长 |
| `eta_hours` | 出发到终点时长 | C | 相对时长 | 当绝对时间 |
| `time_bucket` | A* 状态时间桶 | C | 相对出发 elapsed // 60min | 当绝对模拟时间 |
| `replan_time` | +6h 重规划时刻 | orchestrator | = simulation_start + replan_after_hours | 当新数据到达时刻 |
| `generated_at` | 制品生成墙钟 | B/C/orchestrator | 只做 provenance | 用于因果门禁 |
| `heartbeat/elapsed/timeout/compute_ms` | 机器执行时间 | all | 监控/报告 | 进入模拟时间轴 |

## 当前事实（frozen demo）

- Scenario A/B 都是 `retrospective_best_estimate`：
  `knowledge_as_of`（08-16 / 08-15）**晚于** `simulation_start`（08-11 06:00Z）；
- 145 risk frames = 单一 knowledge 快照 × 145 个逐小时 valid_time；
- `+6h replanning` = 时钟推进 +6h + 同一风险窗后缀重规划，不是数据刷新；
- Viewer 的 “Frame initial / Frame replan” = risk valid_time 标签
  （06:00Z / 12:00Z），不是 simulation snapshot。
- Causal feasibility：A=PARTIAL（末期 19h，first ready 08-16T11:00Z）；
  B=PARTIAL（末期 44h，first ready 08-15T10:00Z）；严格 144h tick-by-tick
  causal replay 不被历史证据支持。

## 时钟语义

- `tick()`：单调前推，**same generation**，knowledge 可前进；
- `seek()/rewind/jump`：**generation++**，缓存按新时刻重解析；
- 正式 +6h 前推 = same generation（`_advance_clock_without_seek`）。

## Replay 修订语义（2026-08-18 实测）

- `data_revision`：A 可见集合变化才 +1（Scenario B 回放中恒为 1）；
- `b_input_revision`：B relevant 集合变化才 +1（同样恒为 1）；
- `risk_content_revision`（= `risk_revision`）：B 业务内容重建才 +1
  （回放中 1 次构建，后续 suffix 复用内容）；
- `risk_window_revision`：Planner 可见 suffix window 身份推进才 +1
  （内容不变但窗口前移是合法的 presentation 变化）；
- `observation_sequence`：向 ReplanTriggerEvaluator 提交的观察序号
  （C 合同 `data_revision == input_revision` 的单调 fence；不是业务
  data revision，replay 事件层做诚实翻译）；
- `plan_revision`：switch gate 采纳新 route 才 +1（C 重算但候选被拒绝时
  不 +1）；
- `navigation_state_revision`：已执行船舶位置/状态推进才 +1；
- Snapshot 可每小时存在，B/C revision 不必每小时变化；
- 确定性：`generated_at` 恢复为墙钟 provenance；semantic digest 排除
  wall-clock 与 resource/route 等派生身份，且包含纯业务
  `risk_semantic_digest` / `route_semantic_digest`（mutation tests PASS）；
  实测 13/13 snapshot digest + manifest digest 一致。

## 三窗口（2026-08-18 落地）

- `replay window`：发布多少 snapshots（与预测能力无关）；
- `risk forecast window`：B 因果可见输入共同支持的 valid 范围
  （Scenario B = 08-15T10:00Z → 08-18T15:00Z，77h）；
- `planning window`：C 实际可用 risk 范围（≤ risk forecast end）；
- `valid_time > simulation_time` 不是泄漏；因果门禁只有
  `issue_time <= knowledge_as_of`；
- v2 complete-route 因果规划 PASS；v3 four-layer **RESOLVED**
  （destination-anchor 层 ceiling = min(request horizon, layer ceiling)；
  真实 77h 窗口四层全 PASS + integrity PASS）。

## 船舶运动时间语义（2026-08-19）

- 船位由 `route waypoint ETA + simulation_time` 插值决定；
  `speed = segment_km / segment ETA span`（effective，非像素速度）；
- `NavigationExecutionState.current_position` 是连续船位；
  `current_node` 是 replan 用最近可通航节点（显式 snap）；
- `executed_distance_km` = 当前 accepted plan 内已航行距离；
  `cumulative_travelled_km` = 全历史累计（只增不减）；
- run 结束时 vessel motion：
  `cumulative 0.0 → 244.63km`、`position_changes=12`、无 stationary /
  teleport / history rewind；
- ETA 是 authoritative motion timeline；Viewer 不用前/后端像素速度。

新增（ship-motion 轮）：

```text
physical_position        = 任意 simulation_time 的连续执行船位
speed_mps / speed_knots  = 由 segment distance / ETA span 推出
planner_origin_node      = 仅给 C 的 grid-node 起点，不移动物理船位
replan_decision_time     = candidate 产生时刻
effective_adoption_time  = deferred plan 在下一个 waypoint 生效的时刻
adoption_status          = NONE / IMMEDIATE / DEFERRED / PENDING
```

## 因果检查清单（改代码时）

1. 新增数据读取路径：先 `issue_time <= knowledge_as_of`；
2. 新增时间字段：显式写它是 绝对/相对、UTC、业务/墙钟、因果/非因果；
3. 不要把 `valid_time` 写进可见性条件；
4. 不要把 `generated_at`/mtime/文件名当 issue_time；
5. normal tick 中 knowledge 单调前进不必 bump generation；倒退/跳跃必须
   `seek()`（bump generation）；
6. `knowledge_as_of` 与 `max_source_issue_time` 是不同概念：
   `max_source_issue_time <= knowledge_as_of`；
7. normal monotonic tick 不 bump generation；只有 seek/rewind/jump 才 bump；
8. 145 帧不能直接当播放器帧；播放器帧必须来自滚动 Simulation Snapshots。
