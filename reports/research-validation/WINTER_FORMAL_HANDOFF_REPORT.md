---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: Winter formal experiment identity and A-to-B intake-only acceptance
Canonical/Supporting: Supporting evidence; canonical state is current/reference/WINTER_SCENARIO_STATUS.md
Branch: research-validation-system
Last Verified: 2026-08-23
---

# Winter Formal Handoff 报告

## 1. 当前状态（2026-08-23 01:16 +08:00）

```text
WINTER_DATASET_STATUS = FROZEN_ARTIFACT_READY
A_TO_B_FORMAL_HANDOFF = READY_FOR_B_VALIDATION
B_WINTER_VALIDATION = NOT_STARTED
C_WINTER_VALIDATION = NOT_STARTED
D_WINTER_VISUALIZATION = NOT_STARTED
```

本轮只建立正式实验身份、修正 intake 接口门禁并执行 intake-only。没有调用 B
RiskBuild、C planner、replay 或 D Viewer，也没有生成 Winter RiskFrame、route 或
presentation artifact。

## 2. RunContext 信息（2026-08-23 01:16 +08:00）

RunContext 由官方 `arctic-route-context create` 原子发布，没有手写或绕过生成器。

| Field | Value |
|---|---|
| Path | `arctic_route_orchestrator/artifacts/winter-formal-handoff/winter_run_context_20260215_v1.json` |
| Schema | `run-context.v2` |
| Run ID | `run-441b03c8-d45b-5414-b0e8-b7fd0d990c22` |
| Scenario | `tromso_isfjorden_february_2026_research_v1` v0.1.0 |
| Corridor | `tromso_to_isfjorden_outer` v1.2.0 |
| Vessel | `nordic_odyssey_reference_v1` v1.0.0 |
| Dataset bundle | `a-bundle-a2146dd0adbaa7db77a6beb7` |
| Bundle digest | `a2146dd0adbaa7db77a6beb7c818e975888600fb31236901fd4af2092069fb71` |
| Simulation window | `2026-02-15T00:00:00Z` → `2026-02-21T00:00:00Z` |
| Config digest | `0af276205eb8f22c0727a29dedefae18d72f8ccda4e816ced9142f851e463842` |
| File SHA-256 | `bea471c714422508e10bbe47a04dca60bea8ec309444a84393d8bd7bc0140717` |

Run ID 使用 UUIDv5，由 scenario ID、active bundle ID 与 formal handoff v1 seed
确定；该 seed 属 experiment report 记录，不扩展 RunContext schema。

## 3. ExecutionSpec 信息（2026-08-23 01:16 +08:00）

| Field | Value |
|---|---|
| Path | `arctic_route_orchestrator/artifacts/winter-formal-handoff/winter_execution_spec_20260215_v1.json` |
| Schema | `orchestrator.execution-spec.v1` |
| Run/scenario identity | 与 RunContext 完全一致 |
| Generation/input revision | `0 / 0` |
| Planning contract | `cd.four-layer-route-plan-set.v3` |
| Max snap | `150.0 km` |
| Replan interval | `6 h` |
| Per-stage timeout | `3600 s` |
| File SHA-256 | `b4360b760e9d3f95f71bcab2b72cc0cb01162131b509dde2420ecbb58da899f2` |

Spec 只包含 strict v1 的既有 10 个字段。Bundle SHA、Git commit、B config path 和 C
config root 未写入 Spec；它们继续由 RunContext、CLI 参数和本报告分工记录。

## 4. Intake 验证结果（2026-08-23 01:16 +08:00）

首次 intake 暴露一个 Blocking interface defect：Orchestrator 要求
`bundle.as_of_time == max(record.issue_time)`。共享 contract 与 time SSOT 的正式不变量是
`max(record.issue_time) <= as_of_time`；retrospective bundle 的 logical knowledge cutoff
允许晚于最后一条可见记录，exact records 已由 bundle digest 锁定。

本轮把 Orchestrator 门禁收敛到共享 contract 语义：仍拒绝任何
`issue_time > as_of_time`，但不再错误拒绝合法的晚 cutoff。没有改变 bundle、schema、
数据可见集合或算法。

| Check | Result |
|---|---|
| Bundle strict parse/semantic verification | PASS |
| RunContext JSON Schema | PASS |
| RunContext official rebuild identity | PASS |
| ExecutionSpec JSON Schema/model | PASS |
| RunContext/ExecutionSpec run/scenario/time binding | PASS；official intake CLI `execution_spec_validated=true` |
| Bundle exact archive resolver | PASS |
| 12-type profile / provenance / generation 0 | PASS |
| Orchestrator intake-only | PASS |
| B/C/D execution | NOT_RUN |

回归：Contracts 19 PASS + Ruff clean + shared-config validate；Orchestrator 84 fast PASS、2
deselected + Ruff clean。被 deselect 的是禁止在本轮执行的 integration/real-artifact full
pipeline 类别，不影响已单独完成的 Winter intake-only acceptance。

intake-only 最终结果：144 小时、1,212 records、12 类、bundle/run/spec identity 精确匹配；
wall time `3:26.43`，peak RSS `978,740 KiB`。这是 exact archive intake 工程观测，不是 B/C
性能基准。

## 5. Interface Freeze Audit 结果（2026-08-23 01:16 +08:00）

| Boundary | Stable interface | Verdict | Non-blocking gap |
|---|---|---|---|
| A→B | `a.dataset-bundle.v2` + `RunContext.v2` | STABLE / INTAKE_PASS | B production profile 仍需下一轮显式批准 |
| B→C | `bc.risk-frame.v2` | STABLE | adaptive grid 不在当前 regular-grid contract 内 |
| C formal output | `cd.route-plan.v2` / `cd.four-layer-route-plan-set.v3` | STABLE | 不存在名为 `cd.route-plan.v3` 的正式 schema |
| C→D | Orchestrator presentation projection → `replay.viewer-bundle.v1` | STABLE_BASELINE | candidate package 仍为 `NOT_PUBLISHED` |

详细字段、单位、missing/hard/time/provenance 和 consumer 边界分别见本轮 B/C/D interface
freeze supporting audits。没有 contract version 变化。

## 6. 修改文件列表（2026-08-23 01:16 +08:00）

- Orchestrator：两个 formal identity JSON；`intake.py` 的 knowledge cutoff 门禁；对应
  unit tests；README/CHANGELOG/handoff 状态。
- Governance：三份 interface freeze audit、本报告，以及 CURRENT_STATUS、ROADMAP、
  WINTER_SCENARIO_STATUS、registry/tech debt/decision/index 等 current SSOT。
- Work Package C/D：仅修正文档中的 nested/top-level route schema 与 Viewer consumer
  边界；代码、配置和算法未修改。
- Contracts/A/B：未修改。

## 7. Git 状态（2026-08-23 01:16 +08:00）

| Repo | Start HEAD | Result |
|---|---|---|
| Orchestrator | `89e61e3` | `efa0d96` — formal identity、intake CLI 与门禁修复 |
| C | `708047a` | `8d90695` — 仅 route schema hierarchy 文档 |
| D | `e761a1d` | `6719663` — 仅 Viewer consumer boundary 文档 |
| Governance | `3e23997` | 本报告与 current SSOT 的本地 documentation commit |
| Contracts | `c19e910` | unchanged |
| A | `b40c689` | unchanged；active/old bundle SHA 均未变化 |
| B | `a6dfa6c` | unchanged |

全部仓库保持 `research-validation-system`。本轮没有 push、merge、rebase 或 reset；Governance
最终 commit hash 由提交完成后的 Git final matrix 与交付消息记录。

## 8. 风险（2026-08-23 01:16 +08:00）

1. `READY_FOR_B_VALIDATION` 只表示正式输入身份和 intake 通过，不表示 Winter B 风险结果
   已存在或科学有效。
2. B 的 Winter production grid/model config 尚未批准；下一轮必须显式选择并记录，不能
   由 ExecutionSpec 临时承载。
3. C 的正式 v3 顶层集合是 `cd.four-layer-route-plan-set.v3`；
   `cd.route-plan.v3` 是集合内单路线 schema，不能作为 ExecutionSpec planning contract。
4. D 当前没有真实 candidate routes；`NOT_PUBLISHED` 继续是权威状态。

## 9. 下一步建议（2026-08-23 01:16 +08:00）

下一轮进入 Winter B Risk Validation：先批准显式 B profile，再只消费本轮固定的
DatasetBundle + RunContext，生成并审计 `bc.risk-frame.v2`，完成 Summer/Winter risk
distribution comparison。C 与 D 可以并行做 consumer fixture/compatibility 准备，但在
真实 Winter RiskFrame/route/presentation artifact 发布前不得宣称 Winter validation。
