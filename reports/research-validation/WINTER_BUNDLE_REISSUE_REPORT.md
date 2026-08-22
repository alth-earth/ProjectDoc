---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: Winter A immutable DatasetBundle reissue evidence
Canonical/Supporting: Supporting evidence; current state is canonical in current/reference/WINTER_SCENARIO_STATUS.md
Branch: research-validation-system
Last Verified: 2026-08-23
---

# Winter A 不可变 Bundle 重发报告

## 1. 背景（2026-08-23 00:48 +08:00）

旧 Winter `a.dataset-bundle.v2` 已包含 12 类、1,212 条真实 source records，且
coverage/provenance 完整；但其 `minimum_required_end` 为
`2026-02-20T12:00:00Z`，不能覆盖结束于 `2026-02-21T00:00:00Z` 的 144 小时
scenario。官方 `create_run_context()` 因而 fail closed。本次仅由 A 使用官方生成链路和
现有验证记录发布新不可变 identity；未修改旧 bundle、schema、contract、source data
或 scenario window。

## 2. 原 bundle 问题（2026-08-23 00:48 +08:00）

| Field | Value |
|---|---|
| Path | `work_package_a/data/tromso_to_isfjorden_outer_winter_20260215T000000Z_bundle.json` |
| Bundle ID | `a-bundle-bd8957c4f10c7c73f395de23` |
| Bundle digest | `bd8957c4f10c7c73f395de2354f56e2b6bde2d0b7204b99c60e0d56284394d9b` |
| File SHA-256 | `5cf81c15162756f992bca83854e0b17cfac6be66197aed332d22ec29f8d4b795` |
| Requested end | `2026-02-21T00:00:00Z` |
| Minimum required end | `2026-02-20T12:00:00Z` |
| Formal handoff qualification | superseded；保留为历史 A acquisition evidence |

问题不是 records 缺失，也不是 contract 缺陷，而是旧发布命令没有显式传入
`--minimum-horizon-hours 144`，因而采用配置中的 132 小时 minimum horizon。

## 3. 新 bundle 信息（2026-08-23 00:48 +08:00）

| Field | Value |
|---|---|
| Path | `work_package_a/data/tromso_to_isfjorden_outer_winter_20260215T000000Z_min144_bundle.json` |
| Schema | `a.dataset-bundle.v2` |
| Bundle ID | `a-bundle-a2146dd0adbaa7db77a6beb7` |
| Bundle digest | `a2146dd0adbaa7db77a6beb7c818e975888600fb31236901fd4af2092069fb71` |
| File SHA-256 | `e28bcca682bb1047381d96d574d42c927f28bf5cd26c363f19fff1fff21c3a2f` |
| Window | `2026-02-15T00:00:00Z` → `2026-02-21T00:00:00Z` |
| Minimum required end | `2026-02-21T00:00:00Z` |
| Records | 1,212 |
| Source qualification | CARRA + Copernicus + GEBCO；12/12 complete |

生成使用 `arctic_route_data.cli replay` 的正式 producer 路径，并显式设置
`--horizon-hours 144 --minimum-horizon-hours 144`。没有下载、补采或重写 source
record。

## 4. 验证结果（2026-08-23 00:48 +08:00）

| Check | Result | Evidence |
|---|---|---|
| Schema parse | PASS | `a.dataset-bundle.v2` producer/consumer model 可解析 |
| Content digest | PASS | 重算 digest 与 bundle digest 一致 |
| File digest | PASS | SHA-256 已独立重算 |
| Coverage | PASS | 12/12 complete；`minimum_required_end == requested_end` |
| Provenance | PASS | 1,212/1,212 records provenance complete |
| Horizon | PASS | `2026-02-21T00Z >= scenario_end` |
| Official context generator compatibility | PASS_IN_MEMORY | `create_run_context()` 接受新 bundle；没有写出 RunContext 文件 |
| A doctor | PASS | 5,461 checked；0 errors；0 warnings |
| A focused tests | PASS | 188 passed |
| A core lint | PASS | `ruff check src tests` |

生成耗时 `122.49 s`，观测峰值 RSS `1,837,056 KiB`；A doctor 耗时 `27.06 s`、峰值
RSS `241,856 KiB`。这些是本机工程观测，不是完整 pipeline benchmark。未运行 B、C、
D、48h replay 或 heavy integration。

## 5. 与旧 bundle 的关系（2026-08-23 00:48 +08:00）

- 新旧 `records`、`source_snapshot_ids`、`requested_data_types`、`as_of_time` 与
  `corridor_id` 逐项一致；没有夏季替代、伪造或 silent coverage relaxation。
- 旧 bundle 文件 SHA-256 保持不变，并继续保留为历史 acquisition evidence。
- 新 bundle 是该 144 小时 Winter formal handoff 的 active frozen artifact；旧 bundle 对
  此 handoff 标记为 superseded，不删除、不覆盖。
- identity 变化来自显式 144 小时 minimum horizon 及其派生 coverage/bundle digest，符合
  content-addressed immutable publication 规则。

## 6. 风险（2026-08-23 00:48 +08:00）

1. 本轮只证明 A artifact 已满足 scenario horizon；尚未发布 matching
   `RunContext.v2` 或 `ExecutionSpec.v1`，也未运行 Orchestrator intake。
2. `formal_run_eligible=true` 不等于 B validation 已完成；A→B 状态只能提升到
   `WAITING_FOR_RUN_CONTEXT`。
3. A 的非核心脚本 `scripts/winter_non_carra_tail_acquisition.py` 仍有 47 个既有 Ruff
   diagnostics（主要为中文全角标点规则）；本轮未改该脚本，`src tests` 核心范围 clean。

## 7. 下一步（2026-08-23 00:48 +08:00）

下一轮执行 Winter Formal Handoff：用官方工具创建并持久化 matching
`RunContext.v2`，创建 strict `ExecutionSpec.v1`，再运行 intake-only。只有三项均通过后，
才能把 `A_TO_B_FORMAL_HANDOFF` 更新为 `READY_FOR_B_VALIDATION` 并开始 Winter B Risk
Validation。
