---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: B to C to Orchestrator to D interface stability audit
Canonical For: NO; evidence supporting current status and contract registry
Branch: research-validation-system
Last Verified: 2026-08-23
Related Canonical Docs:
  - ../../current/CURRENT_STATUS.md
  - ../../current/reference/CONTRACT_OWNERSHIP_REGISTRY.md
---

# B/C/D Interface Stability Audit

## 审计结论（2026-08-23 16:59 +08:00）

| Boundary | Verdict | Blocking change |
|---|---|---|
| B → C | `STABLE` | NONE |
| C → Orchestrator | `STABLE` | NONE |
| Orchestrator → D | `STABLE` | NONE |

本轮不需要变更 shared contract 或 presentation schema。C 的规划采样保持
`DATA_UNAVAILABLE != SAFE`，但 `SampledRisk` 仅传播 generic `hard_mask`，不继续区分
`LAND` 与 `DATA_UNAVAILABLE` 的原始 `hard_reason`。这是 non-blocking tech debt，不影响
当前 route legality，也不构成本轮 schema 变更理由。

## B → C：`bc.risk-frame.v2`（2026-08-23 16:59 +08:00）

正式输入顶层 required fields：

```text
schema_version
risk_id
run_id
scenario_id
corridor_id
vessel_profile_id
config_digest
model_config_digest
generation_id
valid_time
as_of_time
generated_at
model_version
payload
source_summary
provenance
```

`payload` 的 grid 与变量规则：

| Domain | Contract fact |
|---|---|
| Grid | `coordinates.latitude` 与 `coordinates.longitude` 为严格递增的一维轴；CRS=`EPSG:4326` |
| Shape | 所有变量均为 `latitude × longitude` 二维数组，shape 必须一致 |
| Time | `valid_time` 是风险时间轴；`as_of_time` 是 knowledge gate；formal source 要求 `issue_time <= as_of_time` |
| Risk | required：`risk_score`、`risk_level`；unknown `risk_score` 以 JSON `null` 表达，不得转成 0 |
| Hard | required：`hard_mask`；optional semantic detail：`hard_reason`=`NONE/LAND/DATA_UNAVAILABLE/OTHER` |
| Confidence | required：`confidence`；formal frame 还必须发布 `environment_speed_factor` |
| Provenance | formal source references 保留 `data_id/issue_time/valid_time/checksum` 与 run/scenario/config/model identity |

Winter committed window 的真实证据为 145 个 hourly frames、31×11 grid、
`2026-02-15T00:00Z` 至 `2026-02-21T00:00Z`，provenance=`formal`。C ingress 要求
同一 identity 的严格闭区间 committed window，不能扫描 B 私有目录或绕过 commit。

### C 消费行为（2026-08-23 16:59 +08:00）

- C 通过 `CommittedRiskSource.get_committed_window()` 消费正式窗口，不 import 或调用 B
  业务实现。
- `RiskFrame` 是 frozen model；payload 在 codec/model 边界深拷贝并设为不可写。C 不反向
  修改 RiskFrame。
- C 的空间/时间采样采用 contract 定义的 conservative semantics：hard 以 OR 合并，
  confidence 与 environment speed factor 保守组合。
- unknown + navigable 会抛出 `RiskSamplingError`；unknown + hard 作为不可航 hard 处理，
  不会解释为低风险或安全。
- 已知限制：采样结果只保留 hard/not-hard，不继续携带原始 `hard_reason` 分类。D 仍从
  presentation risk overlay 显示 `LAND` / `DATA_UNAVAILABLE`，不得从 C route 反推原因。

主要证据：

- `work_package_c/schemas/risk-frame-v2.schema.json`
- `work_package_c/src/arctic_route_planning/contracts/models.py`
- `work_package_c/src/arctic_route_planning/contracts/sources.py`
- `work_package_c/src/arctic_route_planning/ingress.py`
- `work_package_c/src/arctic_route_planning/risk/sampler.py`

## C → Orchestrator：formal route set（2026-08-23 16:59 +08:00）

正式输入为 `cd.four-layer-route-plan-set.v3`，固定发布：

```text
full_voyage
main_corridor_24_72h
rolling_0_24h
executable_0_6h

×

fastest
low_risk
recommended

= 12 routes
```

每条 `cd.route-plan.v3` 保留：

| Field group | Published semantics |
|---|---|
| Identity | `plan_id`、run/scenario/corridor/vessel、config/model/planner digests、generation/input revision |
| Classification | `planning_layer`、`objective_mode` |
| Geometry | authoritative waypoints：longitude、latitude、ETA、recommended speed |
| Metrics | distance、arrival/travel time、average/max/integrated risk、minimum confidence、hard violations |
| Provenance | `source_risk_ids`、source identity、reference plan identity |

Orchestrator 的 `project_route_candidates()` 只执行严格投影，不 rank、不 recompute metrics、
不改变 geometry。真实 Winter artifact 的 12 条 sidecar candidate 与 C v3 的 ID、geometry、
distance、ETA、travel hours、risk metrics 逐项相等。

主要证据：

- `work_package_c/schemas/four-layer-route-plan-set-v3.schema.json`
- `work_package_c/schemas/route-plan-v3.schema.json`
- `arctic_route_orchestrator/src/arctic_route_orchestrator/route_presentation.py`
- `.runtime/experiments/winter-c-validation-20260823-medium/winter-four-layer-route-plan-set-v3.json`
- `.runtime/experiments/winter-c-validation-20260823-medium/route-candidates.json`

## Orchestrator → D：`presentation.route-candidates.v1`（2026-08-23 16:59 +08:00）

PUBLISHED package 包含：

```text
candidate_set_id
layer_set_id
decision_time
selected_candidate_id
provenance
candidates[12]
```

每个 candidate 包含：

```text
candidate_id
layer
objective
geometry: GeoJSON LineString
distance_km
arrival_eta
travel_hours
risk_metrics:
  average_risk
  maximum_risk
  integrated_risk_hours
  minimum_confidence
  hard_violation_count
provenance
```

`selected_candidate_id` 必须引用 C 的 `full_voyage/recommended`。NOT_PUBLISHED package
必须为空并携带 reason；D 保留既有 authoritative single-route fallback。

### D 消费不变量（2026-08-23 16:59 +08:00）

- 不重排：layer 内 candidate 按 sidecar source publication order 呈现，不按 metrics 排序。
- 不重算：distance、travel hours、arrival ETA 与全部 risk metrics 直接读取 artifact。
- 不改 geometry：地图读取 `LineString.coordinates`；`drawPath` 仅作共线 display
  densification，不弯曲权威折线。
- 不推断缺失：不完整 4×3、非法 identity/geometry/metrics、hard violation 或 scenario
  mismatch 均禁用 Research View，明确回到 single-route fallback。
- 不改 C selection：用户点击只更新 display-only highlight；C 的
  `selected_candidate_id` 始终单独保留并标识。
- 不混淆 availability：risk overlay 继续独立显示 hard reason；缺失 reason 默认
  `DATA_UNAVAILABLE`，不会着色为 safe。

主要证据：

- `arctic_route_orchestrator/schemas/presentation-route-candidates-v1.schema.json`
- `arctic_route_orchestrator/scripts/replay_viewer_export.py`
- `work_package_d/viewer/app.js`
- `work_package_d/tests/unit/test_route_candidate_interface.py`

## Interface Verdict（2026-08-23 16:59 +08:00）

```text
B_TO_C = STABLE
C_TO_ORCHESTRATOR = STABLE
ORCHESTRATOR_TO_D = STABLE
SHARED_CONTRACT_CHANGE = NOT_REQUIRED
```

当前稳定链已足以支持 D Research Visualization Phase 1。下一接口工作不是升级 schema，
而是由 Orchestrator 在同一 Winter experiment identity 下发布 combined Viewer bundle，
使 Winter RiskFrame、candidate sidecar、basemap/replay metadata 可被一次 Browser E2E
共同验证。

## 风险与后续动作（2026-08-23 16:59 +08:00）

| ID | Severity | Finding | Recommended action |
|---|---|---|---|
| BCD-01 | MEDIUM | C `SampledRisk` 不保留原始 hard reason 分类 | proposal first；仅在 C 科研解释确需逐点原因时评估 non-breaking sidecar |
| BCD-02 | HIGH | Winter combined Viewer bundle 尚未发布 | Orchestrator 下一轮只做 artifact assembly，不重跑 A/B/C |
| BCD-03 | MEDIUM | DatasetBundle ID 不在当前 Viewer presentation metadata | 在现有 bundle 可选 metadata owner 范围内提出 adapter 方案；D 当前显示 `not published`，不猜测 |
| BCD-04 | MEDIUM | Winter Research View 尚无 Browser E2E | combined bundle 就绪后验证 4 layers、3 objectives、map geometry、console/network |
