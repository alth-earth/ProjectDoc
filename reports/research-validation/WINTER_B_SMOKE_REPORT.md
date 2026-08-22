---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: Winter B RiskBuild and RiskFrame smoke/validation evidence
Canonical/Supporting: Supporting evidence; canonical status is current/reference/WINTER_SCENARIO_STATUS.md
Branch: research-validation-system
Last Verified: 2026-08-23
---

# Winter B Smoke 与 RiskFrame 生成报告

## 1. 结论（2026-08-23 02:44 +08:00）

```text
DATASET_BUNDLE_INTAKE = PASS
B_RISK_BUILD = PASS
RISKFRAME_SCHEMA = PASS
RISKFRAME_PROVENANCE = PASS
COMMITTED_WINDOW_READBACK = PASS
WINTER_RISKFRAME_AVAILABLE = YES
```

本轮通过一个最小的 `run_winter_b_validation.py` 编排入口调用已有
`RiskBuildService.build_window()`；没有改变 B 的计算语义。由于 B 当前没有独立的
production RiskBuild CLI，runner 负责把正式 A exact-bundle resolver、B service 和
`PersistentRiskStore` 连接起来。

## 2. 输入 artifact（2026-08-23 02:44 +08:00）

| 项目 | 值 |
|---|---|
| DatasetBundle | `work_package_a/data/tromso_to_isfjorden_outer_winter_20260215T000000Z_min144_bundle.json` |
| Bundle ID | `a-bundle-a2146dd0adbaa7db77a6beb7` |
| Bundle digest | `a2146dd0adbaa7db77a6beb7c818e975888600fb31236901fd4af2092069fb71` |
| Bundle SHA-256 | `e28bcca682bb1047381d96d574d42c927f28bf5cd26c363f19fff1fff21c3a2f` |
| RunContext | `arctic_route_orchestrator/artifacts/winter-formal-handoff/winter_run_context_20260215_v1.json` |
| ExecutionSpec | `arctic_route_orchestrator/artifacts/winter-formal-handoff/winter_execution_spec_20260215_v1.json` |
| B config | `work_package_b/configs/models/demo_unvalidated_tromso_smoke_grid_v1.json` |
| Grid profile | `medium`；31×11 |

runner 先用 A 的 `resolve_dataset_bundle_for_b()` 恢复并重新验证冻结 bundle 的 1,212 条
精确记录、payload attestation 和 provenance，再构造 B `BInputEnvelope`。没有扫描 A 私有
SQLite、raw 或 ready 目录作为 B 输入。

## 3. 输出 artifact（2026-08-23 02:44 +08:00）

输出根目录：

`/root/my_project/.runtime/experiments/winter-b-validation-20260823-medium/`

| 项目 | 值 |
|---|---|
| RiskFrame schema | `bc.risk-frame.v2` |
| Valid time | `2026-02-15T00:00:00Z` → `2026-02-21T00:00:00Z` |
| Frame count | 145 |
| Cadence | 60 minutes |
| Provenance | `formal` |
| Grid | 31×11，341 cells/frame |
| Store | `.runtime/experiments/winter-b-validation-20260823-medium/risk-store/` |
| Commit ID | `risk-window-sha256-b5bed6bb48893e32620710e8c765dc60ec37a2fc384f0c49014b92f0a1c056b2` |
| Window content digest | `b5bed6bb48893e32620710e8c765dc60ec37a2fc384f0c49014b92f0a1c056b2` |

每个 RiskFrame 仍是独立的 content-addressed `risk-sha256-<64hex>.json`；`frame-index.json`
和 `distribution.json` 是本轮实验 sidecar，不是新的 B contract。

## 4. 验证结果（2026-08-23 02:44 +08:00）

| 检查 | 结果 |
|---|---|
| DatasetBundle semantic verification | PASS |
| Bundle/RunContext ID and digest binding | PASS |
| RunContext/ExecutionSpec run and generation binding | PASS |
| A exact archive restore | PASS |
| 12 required data types / coverage | PASS |
| RiskFrame JSON Schema | PASS（145/145） |
| Canonical RiskFrame ID | PASS |
| Formal provenance | PASS（145/145） |
| Persistent store publication | PASS |
| Commit readback and digest | PASS |
| B/C/D pipeline beyond B | NOT_RUN |

## 5. 性能观测（2026-08-23 02:44 +08:00）

这些数字是本次工程运行观测，不是正式 benchmark：

| 阶段 | 时间 |
|---|---:|
| A exact-bundle restore + provenance | 199.801 s |
| B RiskBuild | 7.907 s |
| store publish + readback | 2.229 s |
| runner 内部总计 | 215.546 s |
| `/usr/bin/time` wall | 3:36.12 |
| B build sampled peak RSS | 1,013,600 KiB |
| process maximum RSS | 1,024,908 KiB |
| swap | 0 |

耗时主要由 A exact archive checksum/provenance 校验构成；RiskBuild 本身约 7.9 秒。全程
只有一个长任务，没有并行 B/C/replay worker。

## 6. 告警和限制（2026-08-23 02:44 +08:00）

- 没有运行 C planner、D Viewer、Replay 或 full integration。
- B 模型仍标记 `demo_unvalidated`；本报告证明的是正式工程输入和输出链路以及风险分布
  变化，不是模型科学校准或真实航行安全结论。
- Winter C 是否可消费还需要结合本轮 unknown/hard 分析以及 C 的正式 smoke；本轮不提前
  宣称 C 验证通过。
