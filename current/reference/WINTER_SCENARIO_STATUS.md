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

## 当前判定（2026-08-23 01:16 +08:00）

```text
WINTER_DATASET_STATUS = FROZEN_ARTIFACT_READY
A_TO_B_FORMAL_HANDOFF = READY_FOR_B_VALIDATION
B_WINTER_VALIDATION = NOT_STARTED
C_WINTER_VALIDATION = NOT_STARTED
D_WINTER_VISUALIZATION = NOT_STARTED
```

| Gate | State | Evidence |
|---|---|---|
| Winter source acquisition | COMPLETE | 12 required types; CARRA + Copernicus + GEBCO |
| A immutable bundle | FROZEN_ARTIFACT_READY | active 144 h minimum `a.dataset-bundle.v2`, parse/digest/coverage/provenance/doctor pass |
| Matching `RunContext.v2` | PUBLISHED / PASS | official atomic generator; schema/rebuild identity PASS |
| `ExecutionSpec.v1` | PUBLISHED / PASS | strict existing schema; run/scenario/time aligned |
| Orchestrator intake | INTAKE_ONLY_PASS | exact archive resolution; no B/C/D execution |
| B/C/D Winter artifacts | NOT_STARTED | downstream execution remains prohibited |

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

## 接口稳定性（2026-08-22 22:24 +08:00）

```text
DatasetBundle.v2
  -> RunContext.v2
  -> RiskFrame.v2
  -> cd.route-plan.v2 / cd.four-layer-route-plan-set.v3
  -> Presentation Artifact
```

其中 `cd.route-plan.v3` 是 four-layer v3 集合内的单路线 schema，不是 ExecutionSpec 的
顶层 planning contract。当前 Replay Viewer 消费 `replay.viewer-bundle.v1`，不直接读取
four-layer aggregate；候选路线仍为 `NOT_PUBLISHED`。

现有 `orchestrator.execution-spec.v1` 是严格 schema，不包含 bundle SHA、Git commit、
B config path 或 C config path。不得为 Winter 临时追加字段：

- bundle ID/digest 由 RunContext 绑定；
- bundle file SHA 与代码版本由 experiment audit/report 记录；
- B config 由正式 CLI `--b-config` 显式选择，当前仍待批准；
- C config root 由 CLI 显式传入，默认 planner 语义不变。

## 下一门槛（2026-08-23 01:16 +08:00）

Formal handoff 已完成。下一轮才启动 Winter B Risk Validation：

1. 明确批准 B Winter grid/model config；
2. 固定本轮 RunContext 与 generation 0，不创建漂移 identity；
3. 生成并校验 `bc.risk-frame.v2`；
4. 审计 risk/hard/unknown distribution；
5. 与 Summer baseline 做同口径比较后，再开放 C/D Winter 消费。

详细证据见：

- [Winter A Freeze Audit](../../reports/research-validation/WINTER_A_FREEZE_AUDIT_REPORT.md)
- [Winter Experiment Identity Audit](../../reports/research-validation/WINTER_EXPERIMENT_IDENTITY_AUDIT.md)
- [Winter Handoff Validation](../../reports/research-validation/WINTER_HANDOFF_VALIDATION_REPORT.md)
- [Winter Bundle Reissue Audit](../../reports/research-validation/WINTER_BUNDLE_REISSUE_AUDIT.md)
- [Winter Bundle Reissue Report](../../reports/research-validation/WINTER_BUNDLE_REISSUE_REPORT.md)
- [Winter Formal Handoff Report](../../reports/research-validation/WINTER_FORMAL_HANDOFF_REPORT.md)
