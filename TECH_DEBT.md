# 技术债登记

状态：CURRENT（当前）
最后更新：2026-08-17
范围：非阻塞事项 + NEXT PHASE（地理时序 Demo Viewer 阶段）

## HIGH / NEXT PHASE（Route Geospatial Integrity PASS 后）

| ID | 事项 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| TD-11 | Route Geospatial Integrity | ~~HIGH / BLOCKER~~ → **RESOLVED** | 2026-08-17 已建立机器 gate（48/48 PASS）并并入 demo preflight | 历史：审计前 Viewer 双投影导致视觉穿 LAND（见 `ROUTE_GEOSPATIAL_INTEGRITY_AUDIT_20260817.md`） |
| TD-12 | GEBCO georeferenced Presentation View | HIGH | NEXT PHASE（未开始） | 需要 CRS/bbox/lon-lat transform/coastline/bathymetry；Land/sea 与风险帧对齐 |
| TD-13 | 145-frame 动态 Risk Presentation Frames | HIGH | NEXT PHASE（未开始） | 当前仅 2 张 spatial 帧（frame 0/6），不得宣称 145 帧动画已完成 |
| TD-14 | Simulation Clock / Ship / Replan Event | HIGH | NEXT PHASE（未开始） | P3–P5：Timeline、Moving Ship（视觉插值，不发明 risk frame）、+6h Replan 事件 |

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
