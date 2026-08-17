# 技术债登记

状态：CURRENT（当前）
最后更新：2026-08-17
范围：非阻塞事项 + NEXT PHASE（地理时序 Demo Viewer 阶段）

## HIGH / NEXT PHASE（Route Geospatial Integrity PASS 后）

| ID | 事项 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| TD-11 | Route Geospatial Integrity | ~~HIGH / BLOCKER~~ → **RESOLVED** | 2026-08-17 已建立机器 gate（48/48 PASS）并并入 demo preflight | 历史：审计前 Viewer 双投影导致视觉穿 LAND（见 `ROUTE_GEOSPATIAL_INTEGRITY_AUDIT_20260817.md`） |
| TD-15 | Temporal Semantics Audit / canonical time model | ~~HIGH~~ → **RESOLVED / DOCUMENTED** | 2026-08-17 审计完成：issue_time/valid_time/knowledge_as_of/simulation_time 语义、145 帧结构、+6h replan、因果/事后模式、无泄漏 | 4 个结构性 gap 已记录（causal 相等非硬门、B 无显式 horizon、D 丢失 as_of/mode、route 无 mode） |
| TD-16 | Simulation Snapshot schema | HIGH | NEXT PHASE（未开始） | 二维时间模型：simulation_time × forecast valid_time/lead；需合同设计，本轮未改 schema |
| TD-17 | Rolling A→B→C→D replay pipeline | HIGH | NEXT PHASE（未开始） | 当前 145 帧是单一 knowledge 快照，不能直接当播放器帧；需每 tick 固定知识边界重算 |
| TD-18 | Simulation-clock Viewer | HIGH | NEXT PHASE（未开始） | 主控 = simulation_time；区分 risk horizon（current/+6/+12/+24）与 C 四层 |
| TD-19 | GEBCO real-world coastline integrity | HIGH | NEXT PHASE（未开始） | 需 CRS/bbox/transform/coastline/bathymetry；与风险帧对齐后复跑 Geo Integrity gate |
| TD-20 | knowledge cutoff vs max-source-issue distinction | ~~HIGH~~ → **AUDITED / DOCUMENTED** | 2026-08-17：契约层允许 `as_of > max issue`（A 单测证明）；orchestrator intake 强制相等（生产约定）；causal replay 需放开 | 下一轮改 intake：接受逻辑 knowledge_as_of + visible_record_set_digest |
| TD-21 | causal equality enforcement（knowledge_as_of == simulation_time） | HIGH | NEXT PHASE（未开始） | 当前 frozen_forecast 只强制 as_of<=start；causal 模式需显式硬门 |
| TD-22 | scenario_mode presentation propagation | ~~HIGH~~ → **RESOLVED** | 2026-08-17：demo-state + Viewer 展示 scenario_mode/simulation/knowledge_as_of | route/B 层仍不携带 mode（下一轮 contract proposal） |
| TD-23 | rolling A visibility revision（normal tick + knowledge 前进） | HIGH | NEXT PHASE（未开始） | A 单层支持（same generation）；orchestrator 未端到端演练 |
| TD-24 | event-driven B recompute（data_revision 变化才重算） | HIGH | NEXT PHASE（未开始） | 当前每 run 一次 full window |
| TD-25 | event-driven C replan（replan policy 触发才重算） | HIGH | NEXT PHASE（未开始） | policy 已存在；rolling 路径未接入 |
| TD-26 | causal-ready historical evidence | HIGH | NEXT PHASE（未开始） | 当前 A=19h / B=44h 末期窗口；需实时 publication evidence 采集 |

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
