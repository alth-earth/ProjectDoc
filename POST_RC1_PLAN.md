# RC1 之后计划

状态：CURRENT（当前）
最后更新：2026-08-16
适用范围：Demo RC1 之后的下一阶段

## 演示前必做

1. **worker 模式完整 RC1 E2E 冒烟**：用新的可中断 worker 路径
   （`arctic-route-orchestrator run`，即超时改造后的正式入口）完整跑一次 v3，
   消除“r6/r7 由旧内联路径产生、worker 路径只过单测”的验证缺口。
2. **Live Demo 模式彩排**：按 `DEMO_RUNBOOK.md` Mode B 完整走一遍，确认
   冻结结果加载正常、现场小窗 ≤2 分钟。
3. **恢复演练**：按 `RECOVERY_RUNBOOK.md` 从两份同 VHD 副本恢复，确认
   doctor、覆盖 gate、D 加载均通过。
4. **独立备份**：仅在外部故障域（如 `/mnt/d/...`、外接 SSD、NAS、远程主机）
   提供后执行，并同步更新恢复文档。

## 演示前可选

- D 展示/交互完善（地图图层、基于冻结结果的风险动画）；
- 性能遥测（把 benchmark 表格持久化到 `data/output/golden/`）。

## RC1 之后 / RC2

- TD-2：`hard_reason` 语义（LAND / DATA_UNAVAILABLE / OTHER），非阻塞；
- TD-4：可选规划器优化（仅当演示耗时需要时）；
- 更多走廊/场景（按文档约定优先迁移 Tromsø）；
- 生产化相关（校准、船型、政策层）。

## 明确不在范围内

- 更换 TOPAZ / NEXTsim / wave 产品选择；
- 修改 corridor 2.2.0 或 smoke 网格；
- 弱化 fail-closed / unknown→safe；
- 替换 time-dependent A* 基线。
