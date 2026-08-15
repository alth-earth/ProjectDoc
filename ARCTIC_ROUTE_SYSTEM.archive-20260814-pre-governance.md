> **文档治理归档声明**
>
> - 本文件角色：2026-08-14 文档治理前的系统导航原文，仅供历史追溯。
> - 改造时间：2026-08-14（Asia/Shanghai）。
> - 原文件去向：现行系统与架构权威仍使用 [ARCTIC_ROUTE_SYSTEM.md](ARCTIC_ROUTE_SYSTEM.md)。
> - 改造原因：原文是简短导航，尚未集中说明稳定合同、运行身份、模块所有权、失败边界和实验旁支。
> - 使用限制：本声明之后的正文逐字保留，但不再作为当前架构依据。

<!-- ORIGINAL CONTENT START -->

# 北极航线系统工作区导航（2026-08-14）

当前唯一有效排期是 [A–B–C 十个自然日并行冲刺](ABC_10_DAY_SPRINT.md)：
Day 7 前冻结真实 v2 主线，Day 8–9 在同一输入上验收 v3，Day 10 只做回归、阻断修复和
发布冻结。十天是开发期限，不改变 216/144 h 航区上限。

当前有效工程与依赖方向：

```text
arctic_route_contracts
          │
          ├───────────────┐
          ▼               ▼
work_package_a → work_package_b → work_package_c → [待实现 D]
       ▲                 ▲                 ▲
       └──── arctic_route_orchestrator（只调用公共 API）────┘

work_package_b_handoff（设计/历史审计，不参与运行）
```

| 目录 | 当前状态 | 首读文件 |
|---|---|---|
| `arctic_route_contracts/` | v0.3.0；两条走廊 +48 h 政策、共享事实、RunContext v2 | [README](arctic_route_contracts/README.md) |
| `work_package_a/` | v0.4.2；12 类正式基线、精确 bundle 恢复、深快照与 payload attestation | [README](work_package_a/README.md) |
| `work_package_b/` | v0.2.0；配置化 `demo_unvalidated` 风险、full/suffix committed source、Mamba + uv | [README](work_package_b/README.md) |
| `work_package_b_handoff/` | v2 设计约束与旧 ZIP 审计；不再是运行工程 | [README](work_package_b_handoff/README.md) |
| `work_package_c/` | v0.4.0；v2 三目标、v3 四层整组、正式 committed ingress 与重规划 | [README](work_package_c/README.md) |
| `arctic_route_orchestrator/` | v0.1.0 交付中；公共 API 编排、run report 与制品摘要 | [README](arctic_route_orchestrator/README.md) |

2026-08-14 收到一个基于旧 B 综合风险网格训练的轻量 CNN 权重。它不是 A 12 类直连模型，也
不是原生逐小时长窗；当前只作为 `experimental_unverified` 单步 shadow 候选，规则 B 主线和
BC v2 合同不变。审计与接入审批入口见
[新模型 Handoff](work_package_b_handoff/工作包B-新风险模型整合与续开发Handoff.md)。

正式演示顺序固定为：按候选航程评估并物化共享 Scenario → A 按相同 UTC 窗重新采集并生成
经独立覆盖复核的 DatasetBundle v2 → 生成不可变 RunContext → B → C → D。不能按文件名混用不同日期、
场景、船型或摘要的旧产物。

运行时域按候选航程距离、保守航速和余量动态物化，不固定为“9 天”：Murmansk–Dikson 当前默认
168 h、允许 144–216 h；Tromsø–Isfjorden 默认 96 h、允许 72–144 h。来源无法覆盖所需完整窗时
必须返回 `forecast_coverage_insufficient`，不能静默截短。

当前最重要的未完成项：

1. 完成主航区恰好 12 类必需数据的真实 168 h DatasetBundle v2、doctor、168/168 replay、
   RunContext 与跨进程 exact resolver；可选层单独报告，不阻塞基线；
2. 用该 bundle 运行 B 的 169 帧 full commit、C v2 三目标和 `+6 h` suffix 重规划。现有
   96/168/216 h、双走廊同摘要和归档重启夹具只证明工程合同；
3. 在同一正式 B committed window 与 execution lease 上完成 C v3 四层 × 三目标实源验收。
   v3 合同、codec、原子整组 store、编排和夹具测试已经实现；这不等于实源或科学标定完成；
4. 完成根级运行器、机器可读报告、SHA-256 清单和两次断网复现；
5. 有余量才迁移 Tromsø–Isfjorden 96 h 实源；D 明确延期。

另有一个独立的性能阻断：2026-08-14 本地 formal-shape 长运行在 0.75°×2.2° 网格完成到 C v2
初始三目标与 B suffix commit，但重规划未产出、v3 未开始。有效制品活动约 56 分钟，之后工具
回合未正确收口；代理/联网不是瓶颈。详见
[长运行复盘](arctic_route_orchestrator/docs/INCIDENT_2026-08-14_LONG_INTEGRATION_RUN.md)。

当前唯一历史长窗 bundle 为
`work_package_a/data/output/bundles/tromso-native-20260811T1600Z.json`（SHA-256
`9a41120ff222c818f9a65a48e52f6cb78b5687541294c619d6aa64c2540be0a0`）：它是 v1、旧
`tromso_to_svalbard` corridor、9 类数据，`coverage_complete=false`，仅保留回归审计，不能
改名或拼接成当前正式 RunContext。

## 当前外部来源状态

- 历史 GFS 走 NCEI 档案；冻结场景走明确周期的 GFS 预报。两者分别表示“事后最佳
  估计”和“当次冻结预测”，不能混称。
- Copernicus 含潮总流已设为首选、detided 流为显式后备，二者永不相加；含潮总流的
  最新代码路径仍需补一次真实发布 smoke。
- neXtSIM 冰型和 15% 冰密集度派生冰缘已经有采集/派生实现与合同测试；升级后的
  `source_valid_mask.v2` 路径仍需在源服务恢复后补真实 smoke。
- GEBCO 水深/陆海分类和 EMODnet 分类信息层已有小窗实源 smoke；EMODnet 当前目录不能
  冒充 7 月法律状态的历史重建。

来源入口以官方当前页面为准：

- [NOAA/NCEI GFS 档案](https://www.ncei.noaa.gov/products/weather-climate-models/global-forecast)
- [Copernicus 北极含潮总流](https://data.marine.copernicus.eu/product/ARCTIC_ANALYSISFORECAST_PHY_TIDE_002_015/description)
- [Copernicus neXtSIM 海冰](https://data.marine.copernicus.eu/product/ARCTIC_ANALYSISFORECAST_PHY_ICE_002_011/description)
- [GEBCO 2026](https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2026-grid)
- [EMODnet Web Service](https://emodnet.ec.europa.eu/en/emodnet-web-service-documentation)

这是科研演示系统，参考船型与算法参数均未真实标定，不得用于真实导航。
