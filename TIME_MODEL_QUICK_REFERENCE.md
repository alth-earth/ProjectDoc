# Time Model Quick Reference（2026-08-17）

面向后续开发者的最短时间速查。完整审计见
[`TEMPORAL_SEMANTICS_AUDIT_20260817.md`](TEMPORAL_SEMANTICS_AUDIT_20260817.md)。

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
