---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
Document Role: SUPPORTING
Scope: Winter A immutable bundle reissue preflight
Canonical/Supporting: Supporting audit; canonical state remains current/reference/WINTER_SCENARIO_STATUS.md
Branch: research-validation-system
Last Verified: 2026-08-23
---

# Winter Bundle Reissue Audit

## 1. 当前失败原因（2026-08-23 00:48 +08:00）

当前冻结制品为：

```text
bundle_id = a-bundle-bd8957c4f10c7c73f395de23
requested_start = 2026-02-15T00:00:00Z
requested_end = 2026-02-21T00:00:00Z
minimum_required_end = 2026-02-20T12:00:00Z
```

Winter scenario 在 `2026-02-21T00Z` 结束。虽然 12 类 source records 已覆盖 requested
window，`create_run_context()` 仍要求 `minimum_required_end` 覆盖完整 scenario；
Orchestrator intake 还要求正式 bundle 的 minimum end 与 requested end 相等。因此旧 bundle
只能保留为 A acquisition/freeze evidence，不能作为该 144 h 实验的正式 handoff identity。

## 2. Bundle 生成链路（2026-08-23 00:48 +08:00）

现有正式入口无需修改代码：

```text
arctic_route_data.cli replay
  -> LocalArchiveSource
  -> WorkPackageA.prepare_window_for_b()
  -> CoverageReport / provenance verification
  -> DatasetBundle.create()
  -> atomic JSON publication
```

`--horizon-hours` 决定 `requested_end`；`--minimum-horizon-hours` 决定
`minimum_required_end`。旧命令没有显式传入后者，因此采用
`configs/work_package_a.toml` 的 `minimum_complete_horizon_hours=132`。重发只需在同一
命令中显式传入 `--minimum-horizon-hours 144`，不需要修改 schema、contract 或采集流程。

## 3. 可复用 Source Records（2026-08-23 00:48 +08:00）

| 项目 | 审计结果 |
|---|---|
| 记录总数 | 1,212 |
| 必需类型 | 12/12 |
| CARRA wind/temperature/visibility | 各 49 条，3 h cadence |
| Copernicus hourly groups | 各 145 条 |
| Wave | 49 条，3 h cadence |
| GEBCO land/sea mask | 1 条静态记录 |
| Provenance | coverage rows complete；source snapshot identity 已绑定 |

重发必须从 A archive 重新解析并重建 bundle，而不是直接编辑旧 JSON 字段。验收要求新旧
bundle 的 records、source snapshot IDs、requested window、corridor 与 as-of identity
保持一致，仅 minimum horizon 及其派生 content-addressed identity 发生变化。

## 4. 重发位置（2026-08-23 00:48 +08:00）

旧制品保持原路径不变：

```text
data/tromso_to_isfjorden_outer_winter_20260215T000000Z_bundle.json
```

新制品使用独立路径：

```text
data/tromso_to_isfjorden_outer_winter_20260215T000000Z_min144_bundle.json
```

输出前必须确认目标不存在；A 的 atomic writer 负责发布完整 JSON，不覆盖旧制品。

## 5. 风险与控制（2026-08-23 00:48 +08:00）

| 风险 | 控制 |
|---|---|
| 直接改旧 bundle 字段造成伪造 digest | 只通过正式 replay 入口重建 |
| archive 变化导致 record set 漂移 | 比较新旧全部 data IDs、checksums 与 source snapshot IDs |
| 把 21T12Z 尾部纳入新制品 | horizon 固定 144 h，结束于 21T00Z |
| 新旧 identity 混用 | current 文档明确 previous/superseded 与 current/active |
| 提前进入 RunContext/intake | 本轮只做“生成器可接受性”临时验证，不持久化 RunContext |
| B/C/D 误启动 | 不调用 Orchestrator run、RiskBuildService 或 C ingress |

## 6. 预期结果（2026-08-23 00:48 +08:00）

成功标准是新 `a.dataset-bundle.v2` 具有新的 bundle ID、bundle digest 和 file SHA-256，
同时满足：

```text
requested_end = minimum_required_end = 2026-02-21T00:00:00Z
```

本轮只验证官方 RunContext generator 能接受新 bundle；临时输出随验证结束移除，不提交
RunContext 或 ExecutionSpec。正式 handoff 留到下一轮。
