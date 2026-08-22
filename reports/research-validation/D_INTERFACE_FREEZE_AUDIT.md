---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: C-to-D and replay presentation interface freeze audit
Canonical/Supporting: Supporting evidence for the contract ownership registry
Branch: research-validation-system
Last Verified: 2026-08-23
---

# D 接口冻结审计

## 1. 审计结论（2026-08-23 01:16 +08:00）

当前存在两条合法但不同的 C→D 消费路径：

```text
Static display:
C cd.route-plan.v2 / cd.four-layer-route-plan-set.v3 -> D loader

Replay Viewer:
C navigation state -> Orchestrator presentation export
-> replay.viewer-bundle.v1 -> D viewer/app.js
```

`VERDICT = STABLE_BASELINE`。D 是唯一 Viewer runtime owner；Orchestrator 只投影，不重算
risk、route、ETA、adoption 或 vessel physics。

## 2. v2/v3 精确版本口径（2026-08-23 01:16 +08:00）

| Schema | Role |
|---|---|
| `cd.route-plan.v2` | v2 单路线正式顶层输出 |
| `cd.route-plan.v3` | v3 集合内的单路线对象 |
| `cd.four-layer-route-plan-set.v3` | 四层 × 三目标、12 路线的原子顶层集合 |

ExecutionSpec 的 `planning_contract` 只允许 v2 顶层或 four-layer v3 顶层；不能填写嵌套的
`cd.route-plan.v3`。当前 Winter Spec 正确选择
`cd.four-layer-route-plan-set.v3`。

## 3. Route state 与 revision（2026-08-23 01:16 +08:00）

Replay presentation 固定区分 active authoritative、pending、superseded、completed track 与
vessel timeline。`REPLAN_DECIDED` 只产生 pending；`REPLAN_ADOPTED/ROUTE_CHANGED` 才改变
active；completed track append-only。

C 的 `input_revision/generation_id/plan_id/layer_set_id` 与 Replay 的
`plan_revision/accepted_plan_revision/pending_plan_revision` 属不同 namespace，不能仅因数值
相同而合并身份。

## 4. Candidate 与 replay compatibility（2026-08-23 01:16 +08:00）

C 的 four-layer v3 已具有真实 12-route 能力，但当前 Replay Viewer package 明确发布：

```text
schema_version = presentation.route-candidates.v1
status = NOT_PUBLISHED
candidates = []
reason = candidate_geometry_and_metrics_not_published
```

D 对空候选 fail safe，不会从 revision 或 digest 推断 fastest/low-risk/recommended。C formal
12 routes 与 Replay Viewer published candidates 是两个不同验收 claim。

## 5. Findings（2026-08-23 01:16 +08:00）

| Finding | Class | Control |
|---|---|---|
| `cd.route-plan.v3` 容易被误写成 v3 顶层 | DOCUMENTATION DEFECT | 明确 nested vs aggregate |
| Replay Viewer 不直接消费 four-layer aggregate | NON_BLOCKING | 继续经 Orchestrator projection |
| Candidate geometry/metrics 未发布 | NON_BLOCKING / PLANNED | 保持 `NOT_PUBLISHED`，等待 proposal |
| C revision 与 replay revision namespace 不同 | REQUIRED CONTROL | presentation adapter 显式映射，不按数字猜测 |

这些 finding 不阻止 Winter A→B handoff，也不授权本轮修改 C/D runtime。

## 6. 证据位置（2026-08-23 01:16 +08:00）

- `work_package_c/schemas/route-plan-v3.schema.json`
- `work_package_c/schemas/four-layer-route-plan-set-v3.schema.json`
- `work_package_c/src/arctic_route_planning/contracts/layered.py`
- `work_package_d/src/arctic_route_display/loader.py`
- `arctic_route_orchestrator/src/arctic_route_orchestrator/replay/presentation.py`
- `arctic_route_orchestrator/scripts/replay_viewer_export.py`
- `work_package_d/viewer/app.js`
