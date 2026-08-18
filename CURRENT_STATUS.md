# 当前状态

状态：CURRENT（当前）
最后更新：2026-08-17
适用范围：整个北极航线项目
权威字段：当前里程碑与状态矩阵

## 当前里程碑

**Demo RC1 冻结基线已建立（2026-08-16）。**

精确标识符以
[`work_package_a/docs/DEMO_RC1_BASELINE_20260816.md`](work_package_a/docs/DEMO_RC1_BASELINE_20260816.md)
为权威。

**RC2 功能完善阶段进行中（2026-08-17，分支 `rc2-development`）。**
RC1 保持冻结；RC2 状态见 [`RC2_DEVELOPMENT_STATUS.md`](RC2_DEVELOPMENT_STATUS.md)。

**Route Geospatial Integrity（2026-08-17，分支 `demo-engineering`）。**
针对“Viewer 航线视觉穿过 LAND 但 Hard violations=0 / Coverage Gate=PASS”
的矛盾完成独立机器审计：**OVERALL = PASS**（48/48 冻结路线，waypoint/edge/
LAND/DATA_UNAVAILABLE/角切/时间映射/投影一致性全部 0 违规）。根因是 Viewer
格子与路线使用两套不同投影导致像素空间错位（Case C，坐标变换 bug），已最小修复。
权威记录：[`ROUTE_GEOSPATIAL_INTEGRITY_AUDIT_20260817.md`](ROUTE_GEOSPATIAL_INTEGRITY_AUDIT_20260817.md)，
机器制品：`work_package_a/data/output/rc2-smoke/route-geospatial-integrity.json`。

**Temporal Semantics Audit（2026-08-17，分支 `demo-engineering`）。**
完成 A/B/C/D/Orchestrator/Frozen/Live/Viewer 全链路时间语义审计：
`issue_time`=可见性门禁、`valid_time`=环境/预测有效时刻、
`knowledge_as_of`=固定知识截止、`simulation_time`=仿真时刻；
当前 145 risk frames = 单一 knowledge 快照 × 145 个 valid_time
（**不能直接当播放器帧**）；+6h replan = 时钟推进 + 同窗后缀重规划
（非数据刷新）；正式路径无 future-data leakage。
状态 = **AUDITED / DOCUMENTED**（无 correctness blocker；4 个结构性 gap
已记录）。权威：
[`TEMPORAL_SEMANTICS_AUDIT_20260817.md`](TEMPORAL_SEMANTICS_AUDIT_20260817.md)，
速查：[`TIME_MODEL_QUICK_REFERENCE.md`](TIME_MODEL_QUICK_REFERENCE.md)。

**Causal Replay Feasibility Audit（2026-08-17，分支 `demo-engineering`）。**
对两场景归档 manifest 做严格 causal 扫描（`knowledge_as_of == simulation_time`、
`issue_time <= simulation_time`，1h tick × 145）：A = 20/145 ready、
first `2026-08-16T11:00Z`、最长 19h；B = 45/145 ready、first
`2026-08-15T10:00Z`、最长 44h。结论：**严格 144h tick-by-tick causal
replay 不被历史证据支持（PARTIAL）**；原因是多数记录 `issue_time` 为单次
事后 conservative retrieval。无软件 correctness bug；已明确区分
`knowledge_as_of` 与 `max_source_issue_time`。权威：
[`CAUSAL_REPLAY_FEASIBILITY_AUDIT_20260817.md`](CAUSAL_REPLAY_FEASIBILITY_AUDIT_20260817.md)，
架构设计：[`SIMULATION_REPLAY_ARCHITECTURE.md`](SIMULATION_REPLAY_ARCHITECTURE.md)，
机器制品：`causal-replay-feasibility.json`。

**Causal Replay Engine MVP（2026-08-18，分支 `demo-engineering`）。**
Strategy B 主路径落地并真实运行：
`arctic_route_orchestrator/src/arctic_route_orchestrator/replay/`（models/
digests/runner/route_integrity/validation）+ `causal_replay_mvp.py` +
`replay_inspect.py`；Scenario B 因果回放
12h=13 snapshots/31s、24h=25/91s、44h=45/317s 全部 PASS（engine + 机器
验证 + 确定性 13/13 digest 一致）；C 四层因风险窗 44h < ETA ~48h 真实
fail-closed（PLANNING-HORIZON ARCHITECTURE BLOCKER，未伪造）。权威：
[`CAUSAL_REPLAY_MVP_20260818.md`](CAUSAL_REPLAY_MVP_20260818.md)。

**Causal Planning Horizon Resolution（2026-08-18 第二轮）。**
Replay Window 与 Risk Forecast Window 已解耦：
common causal valid end = `2026-08-18T15:00Z`（77h，非 replay_end 44h）；
`c907455` 的 44h cap 判定为 replay scoping gap（已修复）。真实 C：
**v2 complete-route = PASS**（ETA≈50.45h，route integrity PASS）；
**v3 four-layer = main_corridor 内部 cap 阻塞**（cap=full_recommended
ETA≈50.5h，low_risk/fastest 无余量 → PlanningHorizonExceeded；v3 合同
边缘 + 数据 horizon 硬上限）。12h 集成回放：13 snapshots、
plan_revision 1→13、12×REPLAN_TRIGGERED、validation PASS；
determinism 13/13 digest 一致（generated_at 墙钟不同）。性能：
12h≈36–38min、RSS≈824MB、C 规划占耗时 ≥95%。

## 当前状态重定义（审计后）

```text
RC1 = FROZEN
RC2 = FROZEN

Demo Candidate 1 = ESTABLISHED

Demo Candidate 2
= GEOSPATIALLY VALIDATED ENGINEERING CHECKPOINT
  （历史上一轮的“ESTABLISHED / Pre-Demo Finalization”结论
   在 Route Geospatial Integrity 审计前不可直接信任）

Current blocker（Viewer 双投影导致视觉穿 LAND）= RESOLVED
Temporal Semantics = AUDITED / DOCUMENTED
Causal Replay Feasibility = PARTIAL（A 19h / B 44h 末期窗口）
Strategy B = CAUSAL REPLAY ENGINE MVP ESTABLISHED（engine；C 层 blocker）
Strategy B C 规划 = v2 complete-route PASS；v3 four-layer = contract-edge blocker
Next = v3 合同 proposal / replay Presentation Viewer
```

## 当前版本

- contracts 0.3.0 / corridor 2.2.0 / 场景 murmansk_dikson_august_2026_demo_v1 v1.0.0
- A 0.4.2、B 0.2.0、C 0.4.0、D 0.1.0、orchestrator 0.1.0
- bundle：`a-bundle-32cafad4ee280f286d8eb049`
- RunContext：`run-00000000-0000-4000-8000-0000000b0005`

## 状态矩阵

| 领域 | 状态 |
|---|---|
| A 数据 / TOPAZ originalGrid 重建 | PASS |
| 空间覆盖 gate（unknown-navigable = 0） | PASS |
| B 风险构建（hard_mask=land_sea_mask_plus_unknown_v1） | PASS |
| C 初始规划（v3 四层） | PASS |
| 6 小时重规划 | PASS |
| D 真实 v3 制品消费 | PASS |
| 业务语义确定性可复现（r6 与 r7） | PASS |
| 可中断 per-stage 超时机制 | PASS（单元测试） |
| worker 模式完整 RC1 E2E | PASS（真实 worker 全链 ×3 + 真实 C 超时中断） |
| 离线运行时依赖审计 | PASS（无外部依赖） |
| 同 VHD 备份副本 | PASS（非独立灾备） |

## RC2 状态速览（2026-08-17）

| 领域 | 状态 |
|---|---|
| hard_reason（LAND/DATA_UNAVAILABLE） | PASS（B 产生、C codec/schema、D 消费） |
| coverage preflight 正式化 | PASS（orchestrator 阶段 + schema + gate，单测通过） |
| RC1 golden regression | PASS（r6/r7 digest/checksums） |
| D 解释性增强（coverage 命令） | PASS |
| worker 真实冒烟（成功/超时） | PASS（成功 ×3；真实 C 45.2s 超时中断） |
| 第二场景迁移 | PASS（corridor 1.2.0 + 无冰语义修复；coverage/连通/v2/v3 smoke/replan/D 全 PASS） |
| Tromsø 144h qualification | PASS（v3 四层 + 6h 重规划 + D；145 帧 gate=true） |
| 双场景 regression | PASS（RC1 golden + RC2 Scenario B 144h golden） |
| 内存归因（4GB vs 0.8GB） | PASS（A 帧双份驻留 × bbox 差异；已量化） |
| 2-worker 并发 benchmark | NOT BENEFICIAL（0.95×；保持串行） |
| RC2 内存优化（consumer_view + 生命周期释放） | PASS（mur 4.18→2.81GB；Tromsø 144h 1.40→0.97GB） |
| RC2 Frozen Baseline | ESTABLISHED（2026-08-17；Scenario B golden 见 WP A docs） |
| Route Geospatial Integrity（新 gate） | PASS（2026-08-17；48/48 冻结路线；waypoint/edge/LAND/DU/角切/时间/投影 0 违规；机器制品 + 正式文档） |
| Temporal Semantics（新审计） | AUDITED / DOCUMENTED（2026-08-17；issue_time/valid_time/knowledge_as_of/simulation_time 语义、145 帧结构、+6h replan、因果/事后模式、无泄漏；见时间审计文档） |
| Causal Replay Feasibility（新机器审计） | PARTIAL（2026-08-17；A ready 20/145 first 08-16T11:00Z longest 19h；B ready 45/145 first 08-15T10:00Z longest 44h；全窗 tick-by-tick 不被历史证据支持；无软件 bug） |
| Causal Replay Engine MVP（Strategy B） | ESTABLISHED（2026-08-18；真实 12h/24h/44h PASS；确定性 13/13；C 四层 = PLANNING-HORIZON BLOCKER，fail-closed） |
| Causal Planning Horizon（第二轮） | RESOLVED（window 解耦；common end 77h；v2 complete-route PASS；v3 four-layer = main_corridor contract-edge blocker，非 scoping bug） |
| Scenario Mode / Temporal Provenance（D 诚实展示） | PASS（2026-08-17；demo-state 与 Viewer 展示 scenario_mode/simulation/knowledge_as_of） |
| Demo Engineering | Demo Candidate 2 = GEOSPATIALLY VALIDATED ENGINEERING CHECKPOINT（冻结 A/B 展示 + 真实经纬度风险/数据质量地图 + Compare 模式 + Live 按钮/进度 + preflight + 离线 viewer；Viewer 双投影 bug 已修复） |

## 当前非阻塞技术债

见 [`TECH_DEBT.md`](TECH_DEBT.md)，要点：TD-1 worker 模式全链冒烟；
TD-2 hard_reason 语义；TD-3 独立备份目标；TD-4 可选规划优化。

## 下一步（按优先级）

1. 本轮 Causal Replay Engine MVP 本地 commits（不 push；由操作者审核后手动推送）；
2. NEXT：解除 C planning-horizon blocker（replay-local 子层规划或短窗 C
   合同 proposal）→ replay-driven Presentation Viewer；
3. 并行：causal-ready 采集（实时 publication evidence）→ 全窗 replay；
   Pre-demo 彩排/恢复演练/独立备份。

> 历史事实保留：上一轮文档中的“Demo Candidate 2 ESTABLISHED（2026-08-17）”
> 是审计前的历史结论，不作为当前状态；当前状态以本文件与
> `ROUTE_GEOSPATIAL_INTEGRITY_AUDIT_20260817.md` 为准。

详见 [`POST_RC1_PLAN.md`](POST_RC1_PLAN.md)。

## RC2 之前冻结

无 correctness/safety bug 或操作者明确决定，不得修改：数据产品、corridor 2.2.0、
场景、风险语义、C 成本、A 插值、hard-mask 策略、规划算法、RC1 制品。
