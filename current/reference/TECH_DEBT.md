---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
  - PLANNED
Document Role: CANONICAL
Scope: non-blocking items + NEXT PHASE technical debt
Canonical For: registered technical debt and next-phase work
Branch: research-validation-system
Last Verified: 2026-08-22
---

# 技术债登记

状态：CURRENT（当前）
最后更新：2026-08-22
范围：非阻塞事项 + Research Validation System Enhancement Phase

## Research Validation 优先级映射（2026-08-21 23:18）

| Priority | Existing debt / new gap | Current state |
|---|---|---|
| P0 | interface ownership/version registry; C→D candidate presentation proposal | REGISTRY COMPLETE; candidate proposal DRAFT |
| P1 | winter scenario + provenance-complete 12-type artifact | 9/12 ROWS COMPLETE; GFS SOURCE/CADENCE BLOCKED |
| P2 | fixed-grid benchmark, then adaptive-grid proposal | FORMAL B BUILD COMPLETE; BASELINE/MEDIUM C COUPLING COMPLETE; REPEATABILITY PLANNED |
| P3 | C edge traversal cache/shared-search/incremental feasibility | EXACT SAMPLE + DEFAULT-OFF 50K LRU VALIDATED EXPERIMENTALLY; FORMAL GATE NEXT |
| P4 | D professional navigation and research validation views | NAVIGATION AIDS BROWSER PASS; RESEARCH VIEWS PLANNED |

## Research Validation acceleration findings（2026-08-22 00:24）

| ID | Item | State | Next control |
|---|---|---|---|
| TD-55 | Winter 12-type dataset/artifact | PARTIAL / 9_OF_12_COMPLETE | resolve GFS source and 6 h/3 h cadence; do not start B before exact resolver passes |
| TD-56 | B Murmansk default-grid integration expectation | OPEN FINDING | default 11×26 grid has no node in the narrow destination allowed region; requires B/C/contracts owner review, not an experimental-profile patch |
| TD-57 | C repeated risk-sampling cost | EXPERIMENTAL LRU PASS | 14.77% median gain at 50k; formal ingress/12-route equality before promotion |
| TD-58 | D canvas aspect distortion | RESOLVED / BROWSER_E2E_PASS | `object-fit: contain` preserves 1024×1024 canonical map; scale uses haversine centre-latitude distance |
| TD-59 | B grid refinement grows C search super-linearly | MEASURED / EXPERIMENTAL | 112→341 nodes produced 10.51→75.00 s; require bounded fine pilot and repeated-run variance before acceptance |
| TD-60 | February static-mask knowledge-time policy | CONTROLLED / RETROSPECTIVE_DIAGNOSTIC_PASS | explicit August cutoff accepted cached GEBCO; preserve cutoff in future bundle evidence |
| TD-61 | NCEI winter source and cadence mismatch | BLOCKER | 202602 archive paths absent; f000 adapter is 6 h while coverage gate is 3 h; A owner proposal required |

既有 TD 编号保留为历史追踪；当前执行顺序以
[`CURRENT_ROADMAP.md`](../CURRENT_ROADMAP.md) 为准。

## HIGH / NEXT PHASE（Route Geospatial Integrity PASS 后）

| ID | 事项 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| TD-11 | Route Geospatial Integrity | ~~HIGH / BLOCKER~~ → **RESOLVED** | 2026-08-17 已建立机器 gate（48/48 PASS）并并入 demo preflight | 历史：审计前 Viewer 双投影导致视觉穿 LAND（见 `ROUTE_GEOSPATIAL_INTEGRITY_AUDIT_20260817.md`） |
| TD-15 | Temporal Semantics Audit / canonical time model | ~~HIGH~~ → **RESOLVED / DOCUMENTED** | 2026-08-17 审计完成：issue_time/valid_time/knowledge_as_of/simulation_time 语义、145 帧结构、+6h replan、因果/事后模式、无泄漏 | 4 个结构性 gap 已记录（causal 相等非硬门、B 无显式 horizon、D 丢失 as_of/mode、route 无 mode） |
| TD-16 | Simulation Snapshot schema | HIGH | NEXT PHASE（未开始） | 二维时间模型：simulation_time × forecast valid_time/lead；需合同设计，本轮未改 schema |
| TD-17 | Rolling A→B→C→D replay pipeline | HIGH | NEXT PHASE（未开始） | 当前 145 帧是单一 knowledge 快照，不能直接当播放器帧；需每 tick 固定知识边界重算 |
| TD-18 | Simulation-clock Viewer | HIGH | **ESTABLISHED / BROWSER_E2E_PASS（2026-08-20）** | 主控 = simulation_time；risk horizon（current/+6/+12/+24）与 C route state 已分离，切 horizon 不改变船位 |
| TD-19 | GEBCO real-world coastline integrity | HIGH | **FOUNDATION ESTABLISHED（2026-08-19）** | EPSG:4326 canonical transform、coastline/L2 gate、GEBCO land mask 与 risk cells 已对齐 |
| TD-20 | knowledge cutoff vs max-source-issue distinction | ~~HIGH~~ → **AUDITED / DOCUMENTED** | 2026-08-17：契约层允许 `as_of > max issue`（A 单测证明）；orchestrator intake 强制相等（生产约定）；causal replay 需放开 | 下一轮改 intake：接受逻辑 knowledge_as_of + visible_record_set_digest |
| TD-21 | causal equality enforcement（knowledge_as_of == simulation_time） | HIGH | NEXT PHASE（未开始） | 当前 frozen_forecast 只强制 as_of<=start；causal 模式需显式硬门 |
| TD-22 | scenario_mode presentation propagation | ~~HIGH~~ → **RESOLVED** | 2026-08-17：demo-state + Viewer 展示 scenario_mode/simulation/knowledge_as_of | route/B 层仍不携带 mode（下一轮 contract proposal） |
| TD-23 | rolling A visibility revision（normal tick + knowledge 前进） | HIGH | NEXT PHASE（未开始） | A 单层支持（same generation）；orchestrator 未端到端演练 |
| TD-24 | event-driven B recompute（data_revision 变化才重算） | HIGH | NEXT PHASE（未开始） | 当前每 run 一次 full window |
| TD-25 | event-driven C replan（replan policy 触发才重算） | HIGH | NEXT PHASE（未开始） | policy 已存在；rolling 路径未接入 |
| TD-26 | causal-ready historical evidence | HIGH | NEXT PHASE（未开始） | 当前 A=19h / B=44h 末期窗口；需实时 publication evidence 采集 |

2026-08-18 更新：

| ID | 事项 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| TD-27 | Causal Replay Engine MVP（runner/models/digests/validation） | ~~HIGH~~ → **ESTABLISHED** | 真实 12h/24h/44h Scenario B 回放 PASS（engine + determinism 13/13） | `arctic_route_orchestrator/replay/`；C 层 blocker 见下 |
| TD-28 | C planning-horizon blocker（风险窗 44h < ETA ~48h；layered 依赖 full_voyage 锚点） | **HIGH / BLOCKER** | 真实 fail-closed（v3 + v2 probe） | 需 replay-local 子层规划或短窗 C 合同 proposal；禁止伪造未来风险 |
| TD-29 | B suffix window identity per tick（内容复用但 window digest 变化） | 中 | DOCUMENTED | 事件以 B_REUSED 表达；下一轮可考虑 stable window identity |

2026-08-18 第二轮更新：

| ID | 事项 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| TD-30 | Replay/Risk/Planning 三窗口解耦 | ~~HIGH~~ → **RESOLVED** | common causal valid end=08-18T15:00Z（77h）；c907455 44h cap 判定为 scoping gap | preflight 输出三窗口；runner 已解耦 |
| TD-31 | v2 complete-route causal planning | ~~HIGH~~ → **ESTABLISHED** | 12h 集成 PASS（plan_revision 1→13、route integrity PASS） | v3 four-layer 失败时 fallback；`--v2-only` 可跳过 v3 |
| TD-32 | v3 four-layer main_corridor contract edge | **HIGH** | 真实 blocker（cap=full_recommended ETA≈50.5h，低风险目标无余量） | 需 C 合同 proposal（余量语义 / horizon-limited partial plan），本轮不改 C |
| TD-33 | 集成回放性能（12h≈36–38min，RSS≈824MB） | 中 | DOCUMENTED | C 规划占 ≥95%；可选项：objective 并发 / replan 频率评审（下一轮） |

2026-08-18 第三轮（Semantic Hardening）更新：

| ID | 事项 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| TD-32 | v3 four-layer main_corridor contract edge | ~~HIGH~~ → **RESOLVED** | destination-anchor 层 ceiling 改为 `min(request horizon, layer ceiling)`；真实 77h 窗口实验复现旧失败并证明 72h cap 全 PASS（路由与 full_voyage 逐位一致、integrity PASS）；C 单测 97 PASS，RC1/RC2 frozen regression PASS | 生产 C 最小修正 commit `0186caa` |
| TD-33 | 集成回放性能 | 中 | **IMPROVED** | objective 级 1/2/3 worker：157.2s / 100.9s / 80.5s（speedup 1.56×/1.95×，结果逐位一致）；3h v3 smoke ≈13.4min；**12h v3+3w 权威 = 2071.4s（~34.5min），与旧 v2 串行 12h（~36–38min）持平但包含完整 v3 四层**；详见 MVP 报告 §20.6 |
| TD-34 | Revision semantics 拆分（data / b_input / risk_content / risk_window / observation_sequence / plan / navigation） | ~~HIGH~~ → **RESOLVED** | runner 不再用 observation_sequence 冒充 data_revision；honest replan reasons 已机器验证（smoke 每 tick `time`，无伪造 DATA） | C 合同 `observation.data_revision == input_revision` 保留，replay 适配层翻译 |
| TD-35 | Semantic digest 硬化（risk / route 业务内容敏感，墙钟不敏感） | ~~HIGH~~ → **RESOLVED** | mutation tests：route waypoint 改 → digest 变；risk payload 改 → digest 变；generated_at/runtime 改 → digest 不变 | `risk_semantic_digest` NaN-safe 确定性序列化 |
| TD-36 | NavigationExecutionState（同船 replan origin） | **HIGH / v1 ESTABLISHED** | node-aligned v1：replan origin = accepted route 最后到达 waypoint（显式 snap tolerance、无 teleport、completed_track 不可变、switch-gate 拒绝不采纳）；到达后无 replan origin | edge-interior 起点 / 任意 lon/lat start / production contract 后续 |
| TD-37 | 受控 objective 级并行 | **HIGH / ESTABLISHED** | replay-local ProcessPoolExecutor，tick/layer/B 严格串行；3h smoke 与 12h 权威均 3 workers，组合峰值 ≈3.10GiB（<4.5–5GiB 红线）；并行/串行业务结果逐位一致 | 默认 3 workers；内存红线 6–6.5GiB 不变 |

2026-08-19（Strategy B Performance Hardening）更新：

| ID | 事项 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| TD-38 | 集成回放性能（12h） | 中 | **IMPROVED** | interval=2h pre-planning gate：旧 2071.4s → 1306.8s（speedup 1.59×，约 21.8min）；C candidate 13→8、rejected 7→2、pre-gate skip 5；业务轨迹与旧 12h 13/13 一致（plan_revision 1→6、route/risk digest 全等） | 仍可进一步研究 DAG 调度取消 layer barrier 与 recommended-first lazy 模式 |
| TD-38a | 24h 扩展验证 | 中 | **PASS（optional）** | 24h interval=2h：1743.2s（约 29min）、25 snapshots、candidate 14、accepted 12、rejected 2、skip 11、plan_revision 1→12、validation PASS、12h 前缀与权威 12h 13/13 一致 | 44h 因语义稳定与资源优先不再本轮跑 |
| TD-39 | waypoint-aligned pre-gate | 中 | **EXPERIMENT / NOT ADOPTED** | 真实数据 route waypoint ETA 非整点（12:17/14:34...），只按 waypoint 对齐会在 12h 内全 skip、plan 卡在 1，不等价旧 accepted 序列 | 已保留 `--replan-waypoint-aligned-only` 开关与测试作为实验；生产 gate = interval 版 |
| TD-40 | 连续船位（moving-vessel）字段 | 中 | **ESTABLISHED / REPLAY-LOCAL** | NavigationExecutionState 暴露 current_edge_index/segment ETAs/effective_speed_knots/executed & cumulative distance；validation stationary-vessel + cumulative 单调 PASS | Viewer 下一阶段直接消费后端船位，不自行插值；edge-interior replan 起点属 production contract 后续 |
| TD-41 | Edge-interior C planner origin | 高 | **CONTRACT GAP（Future）** | C 只接受 grid-node start；本轮以 next-waypoint deferred adoption 保证物理船位不瞬移（node-aligned v1 + explicit adoption semantics），但真正的 edge-interior 任意点位起点仍需 C contract proposal | Physical motion = PASS；Edge-interior planning ≠ PASS |
| TD-42 | Moving Ship（UI 呈现） | 中 | **ESTABLISHED / BROWSER_E2E_PASS（2026-08-20）** | Firefox 已验证 Simulation Clock 驱动的连续船位；逐帧渲染遵守后端 ETA/linear lon-lat contract | 船头朝向与视觉 polish 仍可后续处理 |
| TD-43 | Presentation Adapter + Contract | 中 | **ESTABLISHED（2026-08-19）** | `replay/presentation.py` + `scripts/replay_presentation.py`；任意仿真时刻船位 = accepted route ETA + `vessel_state_at`；adoption audit 机器可读；T1–T7 + audit 测试；Viewer 不再直接读 replay internals | 下一轮 Viewer 只消费 presentation state；60 FPS 平滑不维护业务速度 |
| TD-44 | 统计口径：REPLAN_DECIDED 的候选/采纳计数 | 中 | **FIXED（2026-08-19）** | 旧 summary 只把 REPLAN_TRIGGERED 计为 accepted；已把 REPLAN_DECIDED 计入 candidate_computed / candidate_accepted（修正后 latest-head 12h：candidate 12 / accepted 6 / rejected 6 / skip 1） | 复跑验证 manifest+13/13 snapshot+risk+route digest 与首次全等 |
| TD-45 | deferred pending 期间的 interval gate 优化 | 低 | **NEXT（不本轮做）** | deferred adoption 使 accepted plan 在 pending 期间不刷新，interval gate 在更多 tick 放行 C（latest-head 12h 约 34min，vs 旧 immediate 约 21.8min）；可将来在 pending plan 存在且 TIME-only 时跳过 | 本轮按约束不做 Planner 性能优化；下轮若需要可加“pending-plan gate”并保持语义等价 |
| TD-19 | GEBCO real-world coastline integrity | 高 | **FOUNDATION ESTABLISHED（2026-08-19）** | `replay/geospatial.py`：EPSG:4326 canonical transform、basemap metadata、L2 coastline gate + 本地 GEBCO_2026 land_sea_mask real smoke（水域 PASS / 穿陆 FAIL） | 下一轮并入 demo preflight 作为正式 L2 门禁；data already local |
| TD-46 | GEBCO `land_sea_mask` 极性误解 | 高 | **CORRECTED（2026-08-19）** | 上一轮 foundation 按 `1=land` 解释；项目规范语义实为 `1=sea, 0=land_or_coast`。已修正 `LandMaskSampler` 与 smoke 描述；真实 12h route L2 = PASS（0 land cell） | 后续所有 L2 / Viewer land overlay 必须沿用 `1=sea` |
| TD-47 | 受限 sandbox 无法跑浏览器/socket | 中 | **RESOLVED FOR THIS ROUND / BROWSER_E2E_PASS** | 默认受限 profile 仍阻断 daemon/socket；attended run 通过允许的 escalated local Firefox path 完成真实浏览器验证，console/network 均 PASS | 后续 CI 仍需提供可复现浏览器执行环境 |
| TD-48 | Viewer superseded route 绘制 | 低 | **ESTABLISHED / BROWSER_E2E_PASS（2026-08-20）** | Adapter 输出 `superseded_future_route`，D 以灰色虚线显示，adoption 后保留过去 future segment | 后续可做 richer animation，不改变语义 |
| TD-49 | Dynamic Risk / Hard Reason overlay | 中 | **CURRENT MVP PASS / BROWSER_E2E_PASS（2026-08-20）** | Orchestrator 输出 presentation-ready current/horizon selections；D 按 Simulation Clock 对齐风险与 hard reason，`unknown != safe` | 当前语义已完成；后续只做视觉 polish |
| TD-50 | Dynamic Risk presentation horizons | 中 | **ESTABLISHED / BROWSER_E2E_PASS（2026-08-20）** | Current/+6/+12/+24h 已有 exact/floor/out-of-range unavailable contract；不复用 stale frame；Simulation Time 切换不变 | 若未来扩大 frame range，继续保持 fail-closed selection |
| TD-51 | replay_viewer_export.py editor diagnostics | 中 | **RESOLVED / EDITOR_ENVIRONMENT（2026-08-20）** | 四个 unresolved-import 红线来自缺少 repo-local interpreter/type-checker 配置；`pyrightconfig.json` 指向 `.venv` + `src`，无 production `sys.path` hack；py_compile/ruff/import smoke PASS | CI 若引入 Pyright，使用同一 repo-local config |

2026-08-21（Viewer Presentation Polish）更新：

| ID | 事项 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| TD-52 | Viewer coarse risk/hard presentation grid | 中 | **AUDITED / PRESENTATION-MITIGATED** | 当前 31×11、约 0.3667°×1.2° 来自 B v3 target-grid realization；A/GEBCO 约 0.05°，D 不是数据根因。D 已采用 exact-cell pixel-aligned Presentation Mode，未插值或改变 hard semantics；若未来需要细化，必须在 B/presentation artifact 层版本化。 |
| TD-53 | Viewer vessel heading visual | 低 | **ESTABLISHED / BROWSER_E2E_PASS** | D 使用 active authoritative route segment bearing 旋转 top-down icon；位置仍是 backend ETA + Simulation Clock。当前 12h artifact 的可见 segment heading 为 0°，后续长窗可补充非零 heading 视觉彩排。 |
| TD-54 | Rich replanning transition animation | 低 | NEXT / NON-BLOCKING | 当前 pending/adopted/superseded 视觉语义已 PASS；可增加非语义 pulse/fade，但不得改 adoption time、route data 或 completed track。 |

> 当前 P0 已被 TD-11 消解；TD-12–14 是下一阶段的正式路线，不作为本轮
> correctness 审计范围。

| ID | 事项 | 优先级 | RC1 阻塞 | 原因 | 建议下一步 |
|---|---|---|---|---|---|
| TD-3 | 独立/异地备份 | 中 | 否 | 两份副本都在同一 VHD | 需要外部路径 |
| TD-4 | 可选规划器性能优化 | 低 | 否 | 144h 单目标 ≈96s 已可接受 | 仅在演示耗时需要时 |
| TD-8 | 正式 v3 objective 级 2-worker 集成（可选） | 低 | 否 | prototype 1.48×；需 timeout/lease/atomic-publication 硬化 | 仅当演示 stage 耗时需要时 |
| TD-9 | 测试并行化 | 低 | 否 | 当前 L0/L1 秒级，L3 为串行长任务 | 仅当 L3 排队成为瓶颈时 |
| TD-10 | 第三场景 | 低 | 否 | A/B 已证明 multi-scenario | POST-DEMO / RC3 |

已解决的问题不在此列出；TD-1/TD-2/TD-5（worker 全链、hard_reason、真实超时）、
TD-6（第二走廊数据覆盖）与 TD-7（RC1 内存 footprint：consumer_view + 生命周期
释放，mur 4.18→2.81GB）已于 RC2 实现并移除；Demo Viewer 交互（地图图层、
风险着色、Compare 模式、Live 进度）已于 Demo Candidate 2 完成并移除，见
`DEMO_ENGINEERING_STATUS.md` 与 `最终交付说明.md` 的“历史已解决问题”；
TD-11（Route Geospatial Integrity，含 Viewer 双投影修复）已于 2026-08-17
审计轮实现并移除（机器制品：
`work_package_a/data/output/rc2-smoke/route-geospatial-integrity.json`）。
