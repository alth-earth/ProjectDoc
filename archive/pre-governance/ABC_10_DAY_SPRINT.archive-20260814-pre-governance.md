> **文档治理归档声明**
>
> - 本文件角色：2026-08-14 文档治理前的十日冲刺原文，仅供历史追溯。
> - 改造时间：2026-08-14（Asia/Shanghai）。
> - 原文件去向：现行排期仍使用 [ABC_10_DAY_SPRINT.md](ABC_10_DAY_SPRINT.md)。
> - 改造原因：原文未纳入本轮全量盘点、各包统一 handoff 和实测阻塞状态，容易把工程能力与实源验收混读。
> - 使用限制：本声明之后的正文逐字保留，但不再作为当前执行依据。

<!-- ORIGINAL CONTENT START -->

# A–B–C 十个自然日并行冲刺

> 生效日期：2026-08-14（Day 1）；最晚冻结日期：2026-08-23（Day 10）。
> 这是当前唯一有效的交付排期。旧文档中的“B 单包 10 天”或“总体 20 天”只保留为历史设计。

## 冻结目标

- Day 7 前形成可重复演示的 v2 主线：Murmansk–Dikson 真实 12 类数据 → 168 h
  `a.dataset-bundle.v2` → B 的 169 个逐小时 formal canonical `RiskFrame` → C 三目标
  `cd.route-plan.v2`，并完成一次 `simulation_start + 6 h` 时间触发重规划。
- Day 8–9 只在上述主线稳定后，把同一输入推广到 C 的
  `cd.four-layer-route-plan-set.v3`：四层、每层三目标，共 12 条路线。
- Day 10 只做短航区验收或阻断修复、回归、文档和制品冻结，不再增加科研功能。
- 10 天是开发期限，不是预测窗。Murmansk–Dikson 默认 168 h、上限 216 h；
  Tromsø–Isfjorden 默认 96 h、上限 144 h。

航程窗使用“保守设计航时 + 至少 48 h”并向整日取整：主航区约
`1137 nm / 10.2 kn + 48 h → 168 h`，短航区约
`555 nm / 12.56 kn + 48 h → 96 h`。这只是科研演示预算，不是实际航次保证；历史
[NSR 航次统计](https://chnl.no/wp-content/uploads/2022/12/statistics2013.pdf)显示不同冰区航次的
平均航速差异显著。

## 责任与版本

| 工程 | 本冲刺目标 | 不得越过的边界 |
|---|---|---|
| `arctic_route_contracts 0.3.0` | 两线 +48 h 政策、版本和摘要隔离；v2 transport 结构不变 | 不把 10 天开发期写入运行时域 |
| `work_package_a 0.4.2` | 恰好 12 类必需实源、doctor、replay、v2 bundle、exact resolver | 可选 bathymetry/限制区不阻塞基线 |
| `work_package_b 0.2.0` | 配置 v2、169 帧、原子 full/suffix commit；外部 CNN 仅做有门禁 shadow | 保持规则主线，不生成路线，不让模型试验阻塞 Day 7 |
| `work_package_c 0.4.0` | v2 三目标；v3 四层整组；一次 +6 h 重规划 | A*、风险采样、网格和成本核心不改 |
| `arctic_route_orchestrator 0.1.0` | 只调公共 API，输出 JSON/GeoJSON、run report、SHA-256 清单 | 不扫描任一包的私有数据库/缓存 |

正式主线只冻结 12 类必需数据：`land_sea_mask`、`ocean_current`、
`sea_ice_concentration`、`sea_ice_drift`、`sea_ice_edge`、`sea_ice_thickness`、
`sea_ice_type`、`temperature`、`visibility`、`water_level`、`wave`、`wind_field`。
`bathymetry` 和 `long_term_restricted_area` 单独报告，不得被静默升级为硬约束。

## 并行日程与闸门

| 时间 | A / 共享合同 | B / 运行器 | C |
|---|---|---|---|
| Day 1 | 冻结 +48 h；源站认证和小窗预检 | 配置 v2 和摘要门禁 | v3 合同、分层语义、端点公共接口 |
| Day 2–3 | 主航区 12 类分批采集；D3 日终实源闸门 | 数值配置迁移；夹具运行器 | codec、整组 store、四层编排测试 |
| Day 4 | 168/168 replay、doctor、bundle、RunContext、重启恢复 | 真实 169 帧 build/commit | 保持 v2 正式入口稳定，v3 隔离 |
| Day 5–6 | 只修真实来源或边界阻断 | 报告、suffix commit、失败矩阵 | v2 实源三目标及一次重规划；v3 夹具验收 |
| Day 7 | 冻结实源证据 | 两次离线彩排 | 冻结可演示 v2 主线 |
| Day 8–9 | 主线不再补采；可准备短航区 | 同一主线输入验证 v3 | v3 四层实源验收后才推广为正式输出 |
| Day 10 | 有余量才做短航区 96 h | 汇总制品和校验和 | 全回归、文档和发布冻结 |

D3 日终若主航区仍不能形成完整候选，立即尝试短航区 96 h。两条实源均失败时，保留
formal-shape 夹具链并明确标记“未完成实源验收”；旧 v1/9 类 bundle 和旧 B ZIP 永远不能
冒充正式输入。

## 完成定义

- 共享合同分别物化 168/96 h；超上限明确返回 `forecast_coverage_insufficient`；旧摘要
  不得与新上下文混用。
- A 的 12 类 coverage 全为 complete，doctor `errors=[]`，跨进程 exact resolver 成功，
  payload/source snapshot 篡改被拒绝。
- B 配置缺失或额外字段拒绝；任一数值参数变化都会改变 `model_config_digest`；缺测、未来
  信息、网格不覆盖和旧 generation 继续 fail closed。
- C v3 Python/JSON/GeoJSON round-trip，四层 × 三目标完整；锚点、身份、generation、revision
  一致；整组原子发布、取消和迟到拒绝；v2 历史解析保持。
- 主线有 1 个真实 12 类 168 h bundle、169 个 formal canonical 风险帧、v2 三目标、v3
  12 条路线、严格递增 ETA、0 个硬约束违规、可追溯 risk IDs，以及一次 +6 h 重规划。
- 两次断网复现得到相同输入摘要、三类配置摘要和内容身份；每仓 `make check` 与
  `git diff --check` 通过，根级运行器的 Markdown 链接检查通过。

## 明确延期

新训练 Transformer/CNN、Q50/Q90/概率预测、AIS/事故标签训练、真实船舶和 Ice Class 1A
校准、方向相关风浪流、净水深和法律限制区硬约束，以及 D、MPC、D* Lite 均不属于本冲刺。
2026-08-14 已交付的轻量 CNN 权重可以在不影响主线的前提下做最多 1–2 日的安全 intake 和
单步 shadow 对照；它没有明确 cadence 或独立验证，不承诺在本冲刺晋级为 formal 后端。所有
规则和模型仍为 `demo_unvalidated`/`experimental_unverified`，不得用于真实导航或安全决策。
