---
Overall Status: DRAFT
Content Status:
  - COMPLETED
  - PLANNED
Document Role: CANONICAL
Scope: backward-compatible publication of real C layered route candidates to D
Canonical/Supporting: Canonical proposal only; not an approved or implemented contract change
Branch: research-validation-system
Last Verified: 2026-08-22
---

# 航线展示契约提案

## 提案标识与状态（2026-08-22 01:11 +08:00）

| 字段 | 值 |
|---|---|
| 提案 | `RVS-RCP-001` |
| 状态 | `DRAFT / PLANNED` |
| 语义负责人 | 航线候选归属 C；展示投影归属 Orchestrator |
| 消费方负责人 | D |
| 目标包 | 在 `replay.viewer-bundle.v1` 内增量新增 `presentation.route-candidates.v1` |
| 既有模式版本 | 保持不变 |

本提案不授权实施。当前 Viewer 真值仍为 `status=NOT_PUBLISHED`、`candidates=[]`。

## 当前能力与缺口（2026-08-22 01:11 +08:00）

C 已验证 `cd.four-layer-route-plan-set.v3`：四层 × 三目标，原子完整，覆盖 12 条真实航线结果。D 的静态加载器可消费该结构。重放 Viewer 之所以收不到，是因为 Orchestrator 当前仅投影权威、待定与已废止的航线状态，并显式发出候选状态 `NOT_PUBLISHED`。

缺失的能力是 C→Orchestrator→D 的展示投影。这不是 C 缺少候选的证据，D 也不得臆造或排序候选。

## 拟议的可选包（2026-08-22 01:11 +08:00）

```json
{
  "schema_version": "presentation.route-candidates.v1",
  "status": "PUBLISHED",
  "candidate_set_id": "...",
  "layer_set_id": "...",
  "decision_time": "...Z",
  "selected_candidate_id": "...",
  "provenance": {"source_schema": "cd.four-layer-route-plan-set.v3"},
  "candidates": [
    {
      "candidate_id": "...",
      "layer": "full_voyage",
      "objective": "recommended",
      "geometry": {"type": "LineString", "coordinates": []},
      "distance_km": 0,
      "arrival_eta": "...Z",
      "travel_hours": 0,
      "risk_metrics": {
        "average_risk": 0,
        "maximum_risk": 0,
        "integrated_risk": 0,
        "minimum_confidence": 0,
        "hard_violation_count": 0
      },
      "provenance": {}
    }
  ]
}
```

所有数值、几何、目标与选区标识必须从已验证的 C 输出或 Orchestrator 的实际采用状态复制。示例中的零值是模式占位符，不是演示值或默认值。

## 发布不变量（2026-08-22 01:11 +08:00）

1. `PUBLISHED` 要求一个完整的同标识 `layer_set_id`、生成、修订与决策时间；部分集合失败关闭。
2. 精确投影 C 发布的层/目标基数。Orchestrator 负责校验与封装，但不重算指标或选定优胜者。
3. `selected_candidate_id` 指向 C/Orchestrator 的权威选择；D 仅高亮它。
4. 几何保持为 C 航线几何。D 可对其做样式化，但不得作为业务数据做样条插值或移动。
5. 缺失或不兼容数据保持 `NOT_PUBLISHED` 或 `UNAVAILABLE` 并附带空列表。不得臆造回退候选。
6. 候选比较不改变权威/待定/已采用航线状态。

## 向后兼容性（2026-08-22 01:11 +08:00）

该包在 `replay.viewer-bundle.v1` 中为可选。旧生产者仍有效，新 D 消费方在包缺失或 `NOT_PUBLISHED` 时显示既有的单航线 UI。旧 D 消费方可忽略该可选包。既有必填字段与 `presentation.route-candidates.v1` 的空语义不被重命名或重新解释。

若实施需要修改既有字段单位、基数、选择含义或失败行为，则此增量提案不足，需要一份带版本的破坏性变更提案。

## 验收门禁（2026-08-22 01:11 +08:00）

- C fixture 证明完整的 4×3 标识与指标；
- Orchestrator 生产者测试证明原子投影与部分集合拒绝；
- D 消费方测试覆盖缺失、NOT_PUBLISHED、PUBLISHED 与不兼容数据；
- selected/recommended 区别显式，且绝不在 D 中计算；
- 聚焦真实制品集成，将投影值与源 C JSON 比对；
- 冻结的 Viewer bundle 与当前单航线重放回归保持绿色；
- C、Orchestrator、D 负责人在状态由 DRAFT 变更前批准。
