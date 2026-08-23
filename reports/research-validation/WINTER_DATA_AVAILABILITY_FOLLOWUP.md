---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - PLANNED
Document Role: SUPPORTING
Scope: Winter DATA_UNAVAILABLE 对 C planning 的影响与后续数据质量工作
Canonical/Supporting: Supporting risk/route follow-up; Winter status remains canonical elsewhere
Branch: research-validation-system
Last Verified: 2026-08-23
---

# Winter Data Availability Follow-up

## 1. Current evidence（2026-08-23 10:20 +08:00）

Winter B 145 frames × 341 cells 中：

```text
LAND = 9,425
DATA_UNAVAILABLE = 8,477
OTHER = 0
unknown_navigable_nodes = 0
hard/reason mismatch = 0
```

`DATA_UNAVAILABLE` 来源于 B 对输入变量非有限区域的既有 fail-closed 投影，主要涉及
wave、ice、current 与 water-level 的部分空间支持；不是 D 色阶或 C endpoint mapping
生成的状态。B formula、threshold、hard policy 与 frozen RiskFrame 均未修改。

## 2. Impact on C（2026-08-23 10:20 +08:00）

- start/goal 首帧均非 hard；同属 218-node 可航连通分量；
- 12 条发布路线全部 `hard_constraint_violations=0`；
- dense route integrity audit 的 waypoint、edge、corner-cut、LAND、
  `DATA_UNAVAILABLE` 违规均为 0；
- 所有路线 minimum confidence 为 `0.675000012`；
- C 正确绕过 unavailable/hard 区域，没有把它映射为低风险。

因此当前 `DATA_UNAVAILABLE` 没有阻止 medium-grid Winter route publication，但它减少了
可航搜索空间并限制结果解释。不能据此断言真实海域安全，也不能把未走过的 unavailable
区域解释为高环境风险。

## 3. Follow-up（2026-08-23 10:20 +08:00）

1. 由 A/B owners 分析 unavailable 的变量级空间 footprint 与源产品边界；
2. 保持 `unknown != safe`，不得通过插值或 Viewer 样式隐藏；
3. 未来数据改进必须重新生成新的 immutable B window identity，再由 C 独立复验；
4. 本问题是 non-blocking research quality debt，不是放宽 C hard gate 的理由。
