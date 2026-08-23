---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
  - PLANNED
Document Role: CANONICAL
Scope: winter research scenario configuration, data readiness, identity gate, and downstream acceptance
Canonical For: current Winter capability, artifact identity, blockers, and next gate
Branch: research-validation-system
Last Verified: 2026-08-23
---

# Winter Scenario Status

## 当前判定（2026-08-23 20:14 +08:00）

```text
WINTER_DATASET_STATUS = FROZEN_ARTIFACT_READY
A_TO_B_FORMAL_HANDOFF = READY_FOR_B_VALIDATION
B_WINTER_VALIDATION = COMPLETED
C_WINTER_VALIDATION = COMPLETED
D_WINTER_VISUALIZATION = REAL_E2E_PASS
C_TO_D_ROUTE_INTERFACE = STABLE
D_PARALLEL_DEVELOPMENT = READY
WINTER_COMBINED_PRESENTATION = REAL_E2E_PASS
WINTER_CAUSAL_REPLAY = NOT_IMPLEMENTED
```

## Winter Combined Research Viewer（2026-08-23 20:14 +08:00）

```text
WINTER_COMBINED_BUNDLE = PUBLISHED_RUNTIME_ARTIFACT
WINTER_RESEARCH_BROWSER_E2E = REAL_E2E_PASS
WINTER_RISK_FRAMES = 145
WINTER_ROUTE_CANDIDATES = 12
WINTER_NAVIGATION_TIMELINE = 3206_ETA_DRIVEN_SAMPLES
WINTER_DYNAMIC_REPLANNING = NOT_IMPLEMENTED
```

combined assembly 严格绑定 active Winter DatasetBundle、RunContext、RiskWindow、C v3
plan set、candidate set 与 12/12 route integrity。D 在 Firefox 中显示 Winter risk、独立
hard availability、selected/candidate routes、ship 与 Voyage Progress；Run/Pause 和 layer
selector 通过，console errors/warnings 为 0，required HTTP resources 全部 200。

该 timeline 来自 C selected full-voyage recommended route waypoint ETA，明确标记
`source_replay=null`。因此当前状态是 Winter navigation simulation `REAL_E2E_PASS`，不是
Winter causal replay 或 replanning PASS。

Supporting evidence:

- [Winter combined Viewer integration](../../reports/research-validation/WINTER_COMBINED_VIEWER_INTEGRATION_REPORT.md)

## C First Route Validation 与 D Phase 1 历史门槛（2026-08-23 16:59 +08:00）

> 该区块记录 Phase 1 当时状态；当前 combined Browser 状态以上方最新区块为准。

```text
WINTER_ROUTE_PLAN_SCHEMA = cd.four-layer-route-plan-set.v3
WINTER_ROUTE_COUNT = 12
WINTER_ROUTE_INTEGRITY = 12_OF_12_PASS
WINTER_ROUTE_DECISION_CHANGE_VS_SUMMER = OBSERVED
ROUTE_CANDIDATE_SIDECAR = PUBLISHED
WINTER_VIEWER = RESEARCH_PHASE_1_IMPLEMENTED
WINTER_COMBINED_BUNDLE = NOT_IMPLEMENTED
WINTER_RESEARCH_BROWSER_E2E = NOT_RUN
```

Winter full-voyage recommended 为 921.379560 km / 53.405581 h；相对 Summer 48h
authoritative initial recommended，11/22 waypoint 不同、距离 +11.658308 km、ETA
+2.951089 h。Summer route-level risk metrics 未发布，因此不作无来源数值比较。

Supporting evidence:

- [Winter C smoke](../../reports/research-validation/WINTER_C_SMOKE_REPORT.md)
- [Winter C route validation](../../reports/research-validation/WINTER_C_ROUTE_VALIDATION_REPORT.md)
- [D interface readiness](../../reports/research-validation/D_INTERFACE_READY_REPORT.md)
- [Winter C final report](../../reports/research-validation/WINTER_C_VALIDATION_FINAL_REPORT.md)

## B First Scientific Run（2026-08-23 02:44 +08:00；C 结果以上方最新门禁为准）

```text
WINTER_RISKFRAME_AVAILABLE = YES
WINTER_RISKFRAME_SCHEMA = bc.risk-frame.v2
WINTER_RISKFRAME_FRAMES = 145
WINTER_B_PROFILE = medium / 31x11
SUMMER_WINTER_RISK_COMPARISON = AVAILABLE
WINTER_ENVIRONMENT_TO_RISK_DISTRIBUTION_CHANGE = OBSERVED
C_VALIDATION = COMPLETED
D_VALIDATION = NOT_STARTED
```

本轮使用固定 bundle、RunContext、ExecutionSpec generation `0`，没有修改 A artifact 或
实验 identity。Winter B 输出已写入新的 runtime experiment store，commit 为
`risk-window-sha256-b5bed6bb48893e32620710e8c765dc60ec37a2fc384f0c49014b92f0a1c056b2`。
同一 medium realized grid 的 Summer/Winter 对照显示 finite risk mean 从
`0.045027961` 上升到 `0.119015786`；同时 `DATA_UNAVAILABLE` hard 区域增加，因此需要
将环境风险上升和数据可用性变化分层解释。

Supporting evidence:

- [Winter B baseline decision](../../reports/research-validation/WINTER_B_BASELINE_CONFIG_DECISION.md)
- [Winter B smoke report](../../reports/research-validation/WINTER_B_SMOKE_REPORT.md)
- [Winter risk distribution audit](../../reports/research-validation/WINTER_RISK_DISTRIBUTION_AUDIT.md)
- [Winter B validation report](../../reports/research-validation/WINTER_B_RISK_VALIDATION_REPORT.md)

| Gate | State | Evidence |
|---|---|---|
| Winter source acquisition | COMPLETE | 12 required types; CARRA + Copernicus + GEBCO |
| A immutable bundle | FROZEN_ARTIFACT_READY | active 144 h minimum `a.dataset-bundle.v2`, parse/digest/coverage/provenance/doctor pass |
| Matching `RunContext.v2` | PUBLISHED / PASS | official atomic generator; schema/rebuild identity PASS |
| `ExecutionSpec.v1` | PUBLISHED / PASS | strict existing schema; run/scenario/time aligned |
| Orchestrator intake | INTAKE_ONLY_PASS | exact archive resolution; no B/C/D execution |
| B Winter RiskFrame | COMPLETED / AVAILABLE | 145 formal hourly `bc.risk-frame.v2`；schema/store/readback PASS |
| C Winter route artifact | COMPLETED / AVAILABLE | formal v3 4×3=12；schema/codec/integrity PASS |
| C→D route candidate interface | STABLE / AVAILABLE | real PUBLISHED sidecar；D metadata intake PASS |
| D Winter visualization | REAL_E2E_PASS | combined package；Firefox risk/hard/12 routes/ship/controls PASS |

这取代同一 current 文档中旧的 `9/12`、`READY_FOR_GENERATION`、
`DatasetBundle NOT_IMPLEMENTED` 和 `BLOCKED_WITH_DECISION` 陈述。那些状态只属于早期
Round3/Round4 supporting reports，不再是当前事实。

## Active 冻结 DatasetBundle（2026-08-23 00:48 +08:00）

| Field | Value |
|---|---|
| Artifact | `work_package_a/data/tromso_to_isfjorden_outer_winter_20260215T000000Z_min144_bundle.json` |
| Schema | `a.dataset-bundle.v2` |
| Bundle ID | `a-bundle-a2146dd0adbaa7db77a6beb7` |
| Bundle digest | `a2146dd0adbaa7db77a6beb7c818e975888600fb31236901fd4af2092069fb71` |
| File SHA-256 | `e28bcca682bb1047381d96d574d42c927f28bf5cd26c363f19fff1fff21c3a2f` |
| Corridor | `tromso_to_isfjorden_outer` v1.2.0 |
| Requested window | 2026-02-15T00:00:00Z → 2026-02-21T00:00:00Z |
| Minimum required end | 2026-02-21T00:00:00Z |
| Records | 1,212 |
| Required data profile | 12/12 coverage complete |

正式场景窗口固定为 144 小时，结束于 `2026-02-21T00Z`。`2026-02-21T12Z` 的尾部缓存
不属于该冻结 bundle，也不能作为它的窗口证据。本次没有补采 12Z。

旧 bundle `a-bundle-bd8957c4f10c7c73f395de23` 保持原 SHA-256，不删除、不覆盖；它
对 formal handoff 标记为 superseded，并作为历史 A acquisition evidence 保留。新旧
records 与 source snapshots 完全一致。

## Formal Experiment Identity（2026-08-23 01:16 +08:00）

现有生成器由 scenario、corridor、vessel 与 active bundle 创建 RunContext，禁止手写或
跳过语义校验。本轮正式发布：

```text
arctic-route-context create
  scenario = tromso_isfjorden_february_2026_research_v1
  bundle = a-bundle-a2146dd0adbaa7db77a6beb7

run_id = run-441b03c8-d45b-5414-b0e8-b7fd0d990c22
run_context_sha256 = bea471c714422508e10bbe47a04dca60bea8ec309444a84393d8bd7bc0140717
execution_spec_sha256 = b4360b760e9d3f95f71bcab2b72cc0cb01162131b509dde2420ecbb58da899f2
result = INTAKE_ONLY_PASS
```

新 bundle 的 `minimum_required_end` 与 `requested_end` 均覆盖 scenario end。RunContext、
ExecutionSpec、bundle exact resolver 和 generation 0 intake 已通过；没有调用 B/C/D。首次
intake 发现并修正 Orchestrator 额外的 cutoff equality 门禁，使其与共享不变量
`max(issue_time) <= as_of_time` 一致，同时继续拒绝 future-issued record。

## 数据源与语义边界（2026-08-22 22:24 +08:00）

| Data group | Winter source | Current qualification |
|---|---|---|
| wind / temperature / visibility | C3S/ECMWF CARRA East domain | 49 three-hourly records each through 21T00Z |
| wave | Copernicus global wave | 49 three-hourly records in frozen window |
| current / water level | Copernicus Arctic PHY | 145 hourly records each; current uses labelled detided fallback |
| sea ice concentration/drift/thickness/type/edge | Copernicus/neXtSIM-derived | 145 hourly records each |
| land/sea mask | GEBCO-derived static mask | static; `1=sea`, `0=land_or_coast` |

Winter A 数据源迁移不改变 `DatasetBundle.v2` schema、canonical variables、units 或
fail-closed 语义。B 不得扫描 A 私有 cache；D 不得读取 A/B/C 私有数据。

## 接口稳定性（2026-08-23 10:20 +08:00）

```text
DatasetBundle.v2
  -> RunContext.v2
  -> RiskFrame.v2
  -> cd.route-plan.v2 / cd.four-layer-route-plan-set.v3
  -> Presentation Artifact
```

其中 `cd.route-plan.v3` 是 four-layer v3 集合内的单路线 schema，不是 ExecutionSpec 的
顶层 planning contract。当前 Replay Viewer 消费 `replay.viewer-bundle.v1`，不直接读取
four-layer aggregate；Orchestrator 已可选投影 `presentation.route-candidates.v1`。既有
frozen Viewer bundle 仍为 `NOT_PUBLISHED`，新的 Winter sidecar 为 `PUBLISHED`，两者均
符合 fail-closed 分支。

现有 `orchestrator.execution-spec.v1` 是严格 schema，不包含 bundle SHA、Git commit、
B config path 或 C config path。不得为 Winter 临时追加字段：

- bundle ID/digest 由 RunContext 绑定；
- bundle file SHA 与代码版本由 experiment audit/report 记录；
- B config 由正式 CLI `--b-config` 显式选择，当前仍待批准；
- C config root 由 CLI 显式传入，默认 planner 语义不变。

## 下一门槛（2026-08-23 20:14 +08:00）

Winter B 风险、C 路线和 D combined research visualization 已完成。下一轮由人工在以下
两个门槛中选择，不自动启动：

1. 把当前 runtime combined package 纳入正式 artifact freeze/registry；
2. 若需航中风险变化与 adoption 证据，建立正式 Winter causal replay/snapshots/events。

任何下一轮都不得在 D 伪造 replanning、修改 C route/ETA/ranking/risk metrics，或把
`DATA_UNAVAILABLE` 显示为 safe。

详细证据见：

- [Winter A Freeze Audit](../../reports/research-validation/WINTER_A_FREEZE_AUDIT_REPORT.md)
- [Winter Experiment Identity Audit](../../reports/research-validation/WINTER_EXPERIMENT_IDENTITY_AUDIT.md)
- [Winter Handoff Validation](../../reports/research-validation/WINTER_HANDOFF_VALIDATION_REPORT.md)
- [Winter Bundle Reissue Audit](../../reports/research-validation/WINTER_BUNDLE_REISSUE_AUDIT.md)
- [Winter Bundle Reissue Report](../../reports/research-validation/WINTER_BUNDLE_REISSUE_REPORT.md)
- [Winter Formal Handoff Report](../../reports/research-validation/WINTER_FORMAL_HANDOFF_REPORT.md)
