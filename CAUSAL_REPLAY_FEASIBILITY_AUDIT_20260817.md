# Causal Replay Feasibility Audit（2026-08-17）

> 状态：**PARTIAL CAUSAL WINDOW AVAILABLE**
> 机器制品：`work_package_a/data/output/rc2-smoke/causal-replay-feasibility.json`
> 扫描器：`work_package_a/scripts/causal_replay_feasibility_audit.py`

## 1. Executive Summary

对 Scenario A（Murmansk）与 Scenario B（Tromsø）的归档 manifest 做严格
causal 扫描后，结论：

```text
Scenario A  causal replay feasibility:
  FULL WINDOW            = NO
  EARLIEST READY         = 2026-08-16T11:00:00Z
  LONGEST READY WINDOW   = 2026-08-16T11:00Z → 2026-08-17T06:00Z（19h，20 ticks）
  REASON                 = 1211 条动态记录共享同一次 conservative_retrieval
                            issue_time（窗口末期），早期 tick 只有 1 条静态记录

Scenario B  causal replay feasibility:
  FULL WINDOW            = NO
  EARLIEST READY         = 2026-08-15T10:00:00Z
  LONGEST READY WINDOW   = 2026-08-15T10:00Z → 2026-08-17T06:00Z（44h，45 ticks）
  REASON                 = Copernicus ocean/ice/water/wave 只有 08-15 批次
                           可见；GFS wind/temp/vis 虽早可见但 12 类不齐
```

这不是软件 correctness bug，而是**历史证据（provenance）限制**：大部分记录
的 `issue_time` 是单次事后采集的 conservative retrieval 时刻，因此早期
simulation tick 在严格 causal 语义下无数据可见。

## 2. Scope

- 数据：A manifest（`data/manifest/manifest.sqlite3`），route
  `offshore_murmansk_to_offshore_dikson`（1212 条）与
  `tromso_to_isfjorden_outer`（1537 条）；
- 时间轴：两场景正式 simulation window
  `2026-08-11T06:00:00Z → 2026-08-17T06:00:00Z`，1h tick（145 ticks）；
- 规则：`knowledge_as_of == simulation_time`；
  `source.issue_time <= simulation_time` 才可见；**不使用**
  retrospective bundle.as_of_time 作为 cutoff；
- B 输入就绪判断：12 类 formal 类型 × 全窗口逐小时 exact/bracketing/nearest
  （static 取 prior）+ bbox 包含走廊 data_bbox；
- 不运行 B/C，不生成风险帧；Level 3（真实 spatial coverage preflight）
  标记为 NOT RUN。

## 3. Existing Retrospective Baseline

RC1/RC2 是 **validated retrospective frozen baselines**：

- Scenario A：bundle as_of_time = `2026-08-16T10:02:51.780511Z`；
- Scenario B：bundle as_of_time = `2026-08-15T09:37:34.830829Z`；
- 两者都远晚于 simulation_start（`2026-08-11T06:00Z`）；
- 它们证明“事后用完整数据重算”可行，但不证明“当时可知”。

## 4. Knowledge Cutoff Semantics

三个概念必须分开：

```text
knowledge_as_of        = 系统允许知道信息的逻辑截止（causal 下 == simulation_time）
max_source_issue_time  = 实际 materialized/可见记录中最大的 issue_time
visible_record_set     = knowledge_as_of 下真正暴露给下游的记录集合
```

约束：`max_source_issue_time <= knowledge_as_of`。

## 5. bundle.as_of_time Audit

代码证据：

| 层 | 行为 | 位置 |
|---|---|---|
| A `DatasetBundle.create/from_dict` | 只强制 `record.issue_time <= as_of_time`（上界，允许 cutoff > max issue） | `work_package_a/src/arctic_route_data/bundle.py` |
| contracts `DatasetBundleIdentity` 校验 | 同样只强制 `issue_time <= as_of` | `arctic_route_contracts/src/arctic_route_contracts/bundle.py:220` |
| orchestrator intake | **强制相等**：`bundle.as_of_time == max(selected issue_time)`，否则 `a_artifact_knowledge_cutoff_mismatch` | `arctic_route_orchestrator/src/arctic_route_orchestrator/intake.py` |
| B/C 传播 | `bundle.as_of_time` → `BInputEnvelope.knowledge_as_of` → `RiskFrame.as_of_time` → `request.as_of_time` | B `context.py`、C `service.py` |

结论：**契约层可以表达“逻辑截止 > 最大 selected issue_time”（MODEL 支持）；
生产入口（orchestrator intake）把两者强制相等（PRODUCTION CONVENTION）。
这是架构/约定 gap，不是契约 blocker。**

## 6. knowledge_as_of vs max_source_issue_time

- 当前生产 flow 中 `bundle.as_of_time == max_source_issue_time`；
- 契约允许 `bundle.as_of_time > max_source_issue_time`（A 单测
  `test_bundle_accepts_logical_cutoff_later_than_max_selected_issue_time`
  已新增证明）；
- 未来 causal replay 需要：knowledge_as_of 每 tick 推进、max_source_issue
  只是结果统计、visible_record_set_digest 标记集合变化；
- 建议字段（本轮只设计）：`knowledge_as_of`、`max_source_issue_time`、
  `visible_record_set_digest`、`data_revision`。

## 7. Simulation Clock / Generation Semantics

`SimulationClock`（`work_package_a/src/arctic_route_data/clock.py`）：

| 操作 | generation | 知识边界 | 缓存 |
|---|---|---|---|
| `play()` + `tick(real_elapsed)` | **不变** | 可随 prefetch 单调前进 | 同一代次可增补新可见帧 |
| `seek(new_time)`（含 rewind/jump） | **+1** | 重置（A `_on_seek`） | `cache.reset_generation(new_gen, simulation_time=...)` 只保留 `issue_time <= 新时刻` 的 static |
| `pause()/set_speed()` | 不变 | 不变 | 不变 |

代码证明：
- `tick()` 只改 `_current_time`；
- `seek()` 唯一递增 `_generation_id` 并通知订阅者；
- cache `put()` 在同一 generation 内接受 `issue_time <= 更新的
  knowledge_as_of` 的新帧（`FutureInformationError` 只挡未来帧）；
- 正式 run 使用 `_advance_clock_without_seek` 做 +6h 前推（same generation）。

因此：

```text
normal monotonic tick      → same generation，knowledge 可单调前进
seek / rewind / jump       → generation++，缓存按新时刻重解析
```

架构上**支持** normal tick + 变化 knowledge cutoff；但 orchestrator 正式路径
目前固定传 bundle.as_of，未端到端演练该模式 → 属 rolling replay 架构 gap，
不是 correctness blocker。

## 8. Audit Method

1. 从 manifest 读取 route 全部归档记录（data_id/data_type/category/
   issue_time/valid_time/quality/bbox/evidence）；
2. 每 tick `t`：`visible = {r | r.issue_time <= t}`；
3. 每类型统计可见数、最新 issue/valid、coverage 起止、quality 汇总、
   evidence authoritative 汇总；
4. `B_INPUT_READY`：对 12 类 × 全窗口逐小时判断 exact/bracketing/nearest/
   static-prior 支撑且 bbox 包含走廊 bbox；
5. 附加 12h/24h/48h 滚动窗口就绪度；
6. 汇总：total/ready ticks、first ready、最长连续 ready 区间、
   full-window feasible、evidence 统计（含 conservative retrieval 延迟）。

## 9. Scenario A Timeline

```text
2026-08-11T06:00  FAIL  visible=1（仅 GEBCO static；全部动态记录不可见）
...
2026-08-16T10:00  FAIL  visible=1（动态记录 issue=10:02:51 尚未到 tick）
2026-08-16T11:00  PASS  visible=1212（12 类全齐，全窗口支撑成立）
2026-08-16T12:00  PASS
...
2026-08-17T06:00  PASS  （end）
```

ready = 20/145；first = `2026-08-16T11:00Z`；最长连续 = 19h（至 end）。
12h/24h/48h 滚动窗口 first-ready 相同（缺类型直到最终批次才补齐）。

## 10. Scenario B Timeline

```text
2026-08-11T06:00  FAIL  visible=1（仅 static）
2026-08-11T12:00  FAIL  visible=166（+GFS wind/temp/vis 55×3）
                        缺 ocean_current / sea_ice_* / water_level / wave
...
2026-08-15T09:00  FAIL  visible=181（仍缺 Copernicus 类型）
2026-08-15T10:00  PASS  visible=1537（12 类全齐）
...
2026-08-17T06:00  PASS  （end）
```

ready = 45/145；first = `2026-08-15T10:00Z`；最长连续 = 44h（至 end）。

## 11. Source Visibility

| 项 | A | B |
|---|---|---|
| 归档记录 | 1212 | 1537 |
| simulation_start 时可见 | 1 | 1 |
| 早期可见动态类型 | 无 | GFS wind/temp/vis（issue 08-11T11:16/11:49） |
| 最终批次 | 1211 条 @ 08-16T10:02:51 | Copernicus 类型 @ 08-15T09:34–09:37 |

## 12. B Input Readiness

判断规则与 B `_resolve_field` 对齐（exact/bracketing、categorical nearest、
static prior、bbox containment）。早期 tick 的 blockers 实例：

- A @ 08-11T12:00：缺 11 类（除 land_sea_mask）；
- B @ 08-11T12:00：缺 8 类（ocean_current、sea_ice_concentration/drift/
  edge/thickness/type、water_level、wave）。

`B_INPUT_READY = YES` 只在 12 类全窗口支撑成立时出现；`PARTIAL` 指部分类型
可见但整体不足（已统计 partial_ticks）。Level 3（真实 spatial coverage
preflight）未运行——需要完整 B build，本轮明确不做。

## 13. Conservative Retrieval Impact

| 指标 | A | B |
|---|---|---|
| conservative_retrieval 记录 | 1211/1212 | 1536/1537 |
| explicit_catalog 记录 | 1（GEBCO static） | 1（GEBCO static） |
| issue_time > valid_time 记录数 | 989 | 790 |
| 延迟中位数（小时） | 59.0 | 53.5 |
| 延迟最大值（小时） | 124.0 | 99.6 |

量化结论：绝大多数动态帧的可见时刻 = 事后下载时刻，比 valid_time 晚约
2–5 天。这是 causal replay 早期 tick 不可行的直接原因。

## 14. Continuous Causal-ready Windows

| window | A first ready | A 最长连续 | B first ready | B 最长连续 |
|---|---|---|---|---|
| full | 08-16T11:00 | 19h（20 ticks） | 08-15T10:00 | 44h（45 ticks） |
| +12h | 08-16T11:00 | 19h | 08-15T10:00 | 44h |
| +24h | 08-16T11:00 | 19h | 08-15T10:00 | 44h |
| +48h | 08-16T11:00 | 19h | 08-15T10:00 | 44h |

即使 12h 短窗也不早于最终批次：缺类型是整类缺失，不是 coverage 边缘问题。

## 15. Software vs Provenance Limitations

| 类型 | 结论 |
|---|---|
| SOFTWARE CORRECTNESS BUG | 无（未发现 causal 模式误用未来帧；visible 规则与 B 支撑规则均按代码验证） |
| SOFTWARE / ARCHITECTURE GAP | orchestrator intake 强制 `bundle.as_of == max issue`；normal tick + 变化 knowledge 未端到端演练；D 此前不展示 scenario_mode（本轮已补最小诚实展示） |
| HISTORICAL EVIDENCE LIMITATION | 归档 issue_time 主要是 conservative retrieval，早期 tick 无因果可见数据；这是 provenance 限制，不是程序失败 |

## 16. Final Feasibility Verdict

```text
Scenario A: PARTIAL_CAUSAL_WINDOW_AVAILABLE（19h，末期）
Scenario B: PARTIAL_CAUSAL_WINDOW_AVAILABLE（44h，末期）

严格 tick-by-tick 的 144h causal replay：
NOT CURRENTLY SUPPORTED BY HISTORICAL EVIDENCE
```

可行窗口位于 simulation window 末尾，本质上等价于“末期一次 frozen-forecast
式 causal build”，不是早期逐步回放。

## 17. Recommended Next Step

1. 保留 RC1/RC2 为 validated retrospective frozen baselines（不重新解释）；
2. 下一轮用**最长可用因果窗口**（优先 Scenario B 的 44h，起点
   `2026-08-15T10:00Z`）做 short-window rolling replay MVP（12–24h 子窗口）；
3. 并行建立新的 causal-ready 采集（实时保存 publication evidence /
   explicit_catalog 或 http_last_modified），为完整 144h causal replay
   提供证据；
4. 架构上放开 `knowledge_as_of` 与 `max_source_issue_time` 的绑定
   （contract 已支持；改 orchestrator intake 为可选逻辑截止 + visible set
   digest），并端到端演练 normal tick + knowledge 前进。
