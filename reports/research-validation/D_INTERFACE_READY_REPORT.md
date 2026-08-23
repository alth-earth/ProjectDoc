---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - PLANNED
Document Role: SUPPORTING
Scope: Winter C route artifact 到 D 的并行开发输入就绪性
Canonical/Supporting: Supporting interface evidence; ownership registry remains canonical
Branch: research-validation-system
Last Verified: 2026-08-23
---

# D Interface Ready 报告

## 1. Verdict（2026-08-23 10:20 +08:00）

```text
C_TO_D_ROUTE_INTERFACE = STABLE
D_STATIC_V3_CONSUMER = PASS
D_ROUTE_CANDIDATE_METADATA_INTAKE = PASS
WINTER_VIEWER = NOT_IMPLEMENTED
D_PARALLEL_DEVELOPMENT = READY
```

D 可立即并行开发 Winter research visualization，但本轮没有创建 Winter Viewer bundle、
地图 candidate layer 或浏览器验证结论。

## 2. Stable inputs（2026-08-23 10:20 +08:00）

| Input | Owner | Consumer | Status |
|---|---|---|---|
| `bc.risk-frame.v2` committed window | B | C / Orchestrator presentation | frozen experiment input |
| `cd.four-layer-route-plan-set.v3` | C | Orchestrator / D static loader | PUBLISHED / 12 routes |
| `presentation.route-candidates.v1` | Orchestrator projection | D Viewer | PUBLISHED sidecar |
| `replay.viewer-bundle.v1.route_candidates` | Orchestrator | D Viewer | optional / backward compatible |

`PUBLISHED` 必须恰好包含 4×3 路线；`NOT_PUBLISHED` 必须为空并带 reason。部分候选集合
不得发布。

## 3. Field ownership（2026-08-23 10:20 +08:00）

- C owns：`candidate_id=plan_id`、layer、objective、geometry、distance、ETA、
  route risk metrics、source risk IDs、selected full-voyage recommended；
- Orchestrator owns：完整性校验、canonical `candidate_set_id`、可选 sidecar 封装与
  replay scenario identity gate；
- D owns：样式、选择高亮、面板和交互；不得重算路线、risk metrics 或 ranking。

本轮将 proposal 中含义不明确的 `integrated_risk` 固化为带单位的
`integrated_risk_hours`，数值直接复制 C `RouteMetrics.integrated_risk_hours`。

## 4. Consumer evidence（2026-08-23 10:20 +08:00）

- D `load_v3_group()` 对真实 Winter artifact：schema
  `cd.four-layer-route-plan-set.v3`、4 layers、12 plans，PASS；
- `presentation.route-candidates.v1` JSON Schema 对真实 sidecar：PASS，12 candidates；
- D Viewer 已读取 `selected_candidate_id` 与
  `risk_metrics.average_risk/maximum_risk`；
- sidecar 缺失时，既有 `NOT_PUBLISHED` 单权威路线行为保持不变；
- Orchestrator exporter 拒绝 sidecar scenario 与 replay manifest 不一致。

真实 sidecar：
`/root/my_project/.runtime/experiments/winter-c-validation-20260823-medium/route-candidates.json`，
SHA-256 `3f6ba8a53264bdcb91ea1391739c65bb30ca9de0d2e8213e9b94261bb3654f4a`。

## 5. Remaining D work（2026-08-23 10:20 +08:00）

1. 生成 Winter RiskFrame + route sidecar 的同 scenario presentation bundle；
2. 在地图中绘制可选择的 candidate geometry；当前只闭合 metadata list；
3. 明确单次 candidate set 与 replay 多 decision candidate-set timeline 的不同；
4. 运行 Winter Viewer Browser E2E 后，才能把 `D_WINTER_VISUALIZATION` 标为完成。
