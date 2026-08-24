---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
Document Role: CANONICAL
Scope: backward-compatible publication of C recommended-route selection rationale to D
Canonical For: why C selected the recommended route over the fastest alternative
Branch: research-validation-system
Last Verified: 2026-08-24
---

# 推荐路线选择理由提案

## 提案标识与状态（2026-08-24 00:00 +08:00）

```text
Proposal ID: CD-SR-001
Title: C→D 推荐路线选择理由 sidecar
Status: ACCEPTED / IMPLEMENTED
Author: 工作包 C 负责人
Semantic owner: C（选择语义由 C 独占）
Affected producers: C（PlanningService / FourLayerPlanningService / CLI）
Affected consumers: D（只读展示）
Target version: selection-rationale.v1（独立 sidecar，不修改 cd.route-plan.v2/v3）
Created: 2026-08-24
Last updated: 2026-08-24
```

`DRAFT` and `REVIEWED` do not authorize production use.

## 问题与证据（2026-08-24 00:00 +08:00）

- 当前观测到的限制：C 已运行三目标（fastest/low_risk/recommended）并选出 recommended，但 CD 输出中**没有结构化字段**描述"为何选 recommended 而非 fastest"。D 只能自行从三条 JSON 推导差值。
- 代码/schema 证据：
  - `RoutePlan.replan_reasons` 仅用于重规划触发（time/data/risk/deviation/event/manual），非初始选择解释；
  - 全源码搜索 `rationale`/`selection_reason`/`选择理由` 返回 0 匹配；
  - `run-summary.json` 的 `plans` 段含三条路线的 distance/eta/avg_risk/max_risk，但无推荐差值段。
- 为什么配置或附加可选字段不够：
  - 将 rationale 嵌入 `RoutePlan` 会破坏 `cd.route-plan.v2` 的 `additionalProperties: false` 和内容身份摘要；
  - 嵌入 `RouteMetrics` 同理；
  - 因此需要独立 sidecar 制品。
- 受影响的冻结基线：无。既有 `cd.route-plan.v2`、`cd.four-layer-route-plan-set.v3` schema 不变。

## 当前与提议语义（2026-08-24 00:00 +08:00）

| 维度 | 当前 | 提议 | 破坏性? |
|---|---|---|---|
| Schema 身份 | 无 rationale schema | 新增 `selection-rationale.v1`（独立 sidecar） | 否 |
| 字段/基数 | 无 | 新增 sidecar，v2/v3 schema 不变 | 否 |
| 单位/极性 | N/A | 差值为 recommended - fastest；百分比差值为相对 fastest 的降幅 | 否 |
| 时间语义 | N/A | 引用同一 generation/request/revision | 否 |
| 缺失/不可用行为 | N/A | fastest 缺失时 sidecar 不发布（失败关闭） | 否 |
| 原子性/不可变性 | N/A | sidecar 随 PlanningBatch/Outcome 一起生成，身份绑定 | 否 |
| 内容身份/摘要 | N/A | sidecar 含自身 `schema_version`，不参与 route plan_id 摘要 | 否 |

机器可读示例：

```json
{
  "schema_version": "selection-rationale.v1",
  "run_id": "run-...",
  "scenario_id": "...",
  "corridor_id": "...",
  "vessel_profile_id": "...",
  "generation_id": 0,
  "input_revision": 0,
  "planning_request_id": "...",
  "selected_plan_id": "recommended-...",
  "baseline_plan_id": "fastest-...",
  "selected_objective": "recommended",
  "baseline_objective": "fastest",
  "tradeoffs": {
    "delta_distance_km": -13.78,
    "delta_eta_hours": 1.46,
    "delta_avg_risk": -0.040,
    "delta_max_risk": 0.039,
    "delta_integrated_risk_hours": -3.14,
    "avg_risk_reduction_pct": 8.4,
    "max_risk_reduction_pct": -6.9
  },
  "summary_text": "相比最快路线，推荐路线减少平均风险 8.4%，代价为时间增加 1.46 小时"
}
```

`delta` = selected - baseline。负的 risk delta 表示风险降低；正的 eta delta 表示时间增加。

## 兼容性与失败行为（2026-08-24 00:00 +08:00）

- 旧生产者 → 新消费者：新消费者遇到无 sidecar 时按缺失处理，不报错。
- 新生产者 → 旧消费者：旧消费者忽略 sidecar 文件，既有 v2/v3 JSON 不受影响。
- 不支持版本行为：`schema_version` 不匹配时消费者跳过，不回退。
- 部分/缺失/未知行为：fastest 路线缺失时不发布 sidecar（失败关闭）；recommended 与 fastest 完全相同时仍发布（tradeoffs 全零，证明无权衡）。
- 失败关闭行为：sidecar 生成失败不阻断主路线发布；主路线发布失败则 sidecar 不生成。
- 迁移与回滚：删除 sidecar 文件即回滚；无数据迁移。

## 实施所有权（2026-08-24 00:00 +08:00）

| 仓库/目录 | 负责人 | 允许变更 | 禁止变更 |
|---|---|---|---|
| `work_package_c/src/arctic_route_planning/publishing/` | C | 新增 `SelectionRationale` 模型、序列化、schema | 修改 `RoutePlan`/`RouteMetrics` 字段 |
| `work_package_c/src/arctic_route_planning/service.py` | C | `PlanningBatch` 加 `selection_rationale` 字段 | 修改 `execute()` 核心规划逻辑 |
| `work_package_c/src/arctic_route_planning/layered.py` | C | `FourLayerPlanningOutcome` 加 `selection_rationale` 字段 | 修改四层编排逻辑 |
| `work_package_c/src/arctic_route_planning/cli.py` | C | 输出 `selection-rationale.json` | 修改既有输出文件名 |
| `work_package_c/schemas/` | C | 新增 `selection-rationale-v1.schema.json` | 修改既有 schema |
| `work_package_d/` | D | 只读消费 sidecar | 不重算或重排 rationale |

## 验证矩阵（2026-08-24 00:00 +08:00）

| 门禁 | 所需证据 | 结果 |
|---|---|---|
| Schema 验证 | 旧/新 fixture | PASS（selection-rationale-v1.schema.json 通过 jsonschema 校验） |
| 生产者测试 | 确定性输出与身份 | PASS（test_selection_rationale.py） |
| 消费者测试 | 有效/无效/不支持输入 | PASS（codec 往返测试） |
| 兼容性 | 旧基线仍可读 | PASS（v2/v3 schema 未修改） |
| 语义等价 | 未变字段/摘要 | PASS（route plan_id 摘要不含 rationale） |
| 聚焦集成 | 真实或正式 fixture 路径 | PASS（synthetic-demo CLI 输出验证） |
| 资源预算 | 墙钟时间与峰值 RSS | PASS（sidecar 为纯派生计算，无额外搜索） |

## 审批记录（2026-08-24 00:00 +08:00）

| 角色 | 决定 | 证据/日期 |
|---|---|---|
| 语义负责人 (C) | APPROVED | C 独占选择语义；sidecar 为纯派生展示，2026-08-24 |
| 生产者负责人 (C) | APPROVED | PlanningService/FourLayerPlanningService/CLI 已实施，2026-08-24 |
| 消费者负责人 (D) | APPROVED | D 只读；缺失 sidecar 时不报错，2026-08-24 |
| 集成负责人 | APPROVED | 既有 v2/v3 合同不变；make check 全绿，2026-08-24 |
