---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: Winter B first scientific run configuration decision
Canonical/Supporting: Supporting evidence; current state is maintained in current/CURRENT_STATUS.md and current/reference/WINTER_SCENARIO_STATUS.md
Branch: research-validation-system
Last Verified: 2026-08-23
---

# Winter B 基线配置决策

## 1. 决策结论（2026-08-23 02:44 +08:00）

本轮 Winter B First Scientific Run 采用已有 Tromsø `medium` 固定网格作为实验基线。
该选择只约束本次 B 验证，不改变 B production default、风险公式、风险等级策略或任何
冻结 artifact。

```text
WINTER_B_BASELINE_PROFILE = medium
RUN_STATUS = APPROVED_FOR_THIS_EXPERIMENT
PRODUCTION_DEFAULT = UNCHANGED
```

## 2. 实验身份与输入（2026-08-23 02:44 +08:00）

| 项目 | 值 |
|---|---|
| Scenario | `tromso_isfjorden_february_2026_research_v1` |
| Bundle | `a-bundle-a2146dd0adbaa7db77a6beb7` |
| RunContext | `run-441b03c8-d45b-5414-b0e8-b7fd0d990c22` |
| Generation | `0` |
| Window | `2026-02-15T00:00:00Z` → `2026-02-21T00:00:00Z` |
| Cadence | hourly；145 个端点包含在内的 RiskFrame |
| B model | `demo_unvalidated_rule_baseline.v2` |
| Calibration | `demo_unvalidated` |

## 3. 网格和策略（2026-08-23 02:44 +08:00）

| 项目 | 值 |
|---|---|
| 名义 profile | `medium` |
| 名义角步长 | latitude `0.375°`；longitude `1.25°` |
| 实际 realized grid | `31 × 11 = 341` cells/frame |
| 实际坐标步长 | latitude `0.3666667°`；longitude `1.2°` |
| B target bbox | `[10.0, 68.5, 22.0, 79.5]` |
| Model config | `work_package_b/configs/models/demo_unvalidated_tromso_smoke_grid_v1.json` |
| Risk formula | `deterministic_environment_components_v2` |
| Level policy | `c_equal_width_floor_v1` |
| Hard policy | `land_sea_mask_plus_unknown_ice_free_v1` |
| Unknown policy | `nan_confidence_zero_v1` |

本报告以 RiskFrame 实际坐标和 `grid_id` 为最终证据；名义 profile 仅是配置标签。

## 4. 选择依据（2026-08-23 02:44 +08:00）

1. 既有 Summer formal grid comparison 已经验证相同 Tromsø medium 口径，便于进行同网格、
   同 cadence 的季节分布比较。
2. `baseline`（16×7）过粗，不利于观察风险空间结构；`fine`（60×21）增加输出量，且本轮
   目标是先完成首轮科学分布证据，不是网格优化。
3. medium 是当前已有的 Tromsø presentation policy，避免为 Winter 首轮引入新的未审批准
   profile。

## 5. 边界和状态（2026-08-23 02:44 +08:00）

- 本轮没有修改 B 风险公式、权重、阈值、hard reason 或 `bc.risk-frame.v2`。
- 本轮没有运行 C planner、D Viewer、Replay 或 Adaptive Grid。
- 本决策不代表 medium 已成为所有场景的 production default，也不代表模型已经完成科学
  标定。
- RiskFrame 生成和 Summer/Winter 分布比较完成后，才决定是否开放 Winter C 消费。
