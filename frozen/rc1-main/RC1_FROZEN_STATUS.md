---
Document Status: FROZEN_RC1
Branch: main
Frozen At: 2026-08-16
Canonical Current State: NO
Scope: Demo RC1 frozen baseline (challenge-cup demo delivery)
Canonical For: what RC1 was, what passed, what was NOT completed at freeze
Related Canonical Docs: current/CURRENT_STATUS.md, current/CURRENT_ROADMAP.md
---

# RC1 冻结状态（main @ 29aa74d — "8-16demo交付"）

> **FROZEN ≠ COMPLETE（冻结 ≠ 完成）。** 本文档记录 RC1 在 2026-08-16 冻结时的真实状态。
> 冻结时 NOT RUN / NOT COMPLETED 的项被明确列出。后续的 Strategy B / RC2 / Viewer 能力
> 不会回灌进 RC1。

## 1. RC1 身份

| Field | Value |
|---|---|
| Branch | `main`（已冻结，勿修改） |
| Freeze commit | `29aa74d`（"8-16demo交付"） |
| Synced to GitHub | yes (main) |
| Project type | 挑战杯（Challenge Cup）演示 — 工程演示通过即成功 |
| Authoritative baseline doc | `work_package_a/docs/DEMO_RC1_BASELINE_20260816.md` |

## 2. RC1 版本向量（冻结时）

| Component | Version |
|---|---|
| contracts | 0.3.0 |
| corridor | 2.2.0（`murmansk_dikson_august_2026_demo_v1` v1.0.0） |
| A `arctic_route_data` | 0.4.2 |
| B `arctic_route_risk` | 0.2.0 |
| C `arctic_route_planner` | 0.4.0 |
| D `arctic_route_display` | 0.1.0 |
| orchestrator | 0.1.0 |

## 3. RC1 制品身份

| Artifact | Identity |
|---|---|
| A bundle | `a-bundle-32cafad4ee280f286d8eb049` |
| RunContext | `run-00000000-0000-4000-8000-0000000b0005` |
| Initial layer-set | `layer-set-sha256-51824e96…` |
| Replanned layer-set | `layer-set-sha256-ec74a145…` |
| Scenario | `murmansk_dikson_august_2026_demo_v1`（144 h，corridor 2.2.0） |
| Historical alternate scenario | `tromso_isfjorden_august_2026_demo_v1`（作为独立证据保留，非 RC1 main） |

## 4. RC1 冻结时通过的项

| Capability | Evidence |
|---|---|
| A TOPAZ originalGrid 重建 | unit + E2E（r6/r7） |
| 空间覆盖门禁（unknown-navigable = 0） | PASS |
| B 风险构建（`land_sea_mask_plus_unknown_v1`） | PASS |
| C 初始规划（v3 四层） | PASS |
| 6 小时重规划 | PASS |
| D 真实 v3 制品消费 | PASS |
| 业务语义确定性（r6 vs r7） | PASS |
| 分阶段的、可中断超时 | PASS（单元测试） |
| 离线运行时依赖审计 | PASS（无外部依赖） |
| 同 VHD 备份副本 | PASS（非独立灾备目标） |

## 5. RC1 冻结时未完成的项（FROZEN / NOT_COMPLETED_AT_FREEZE）

| Capability | Status at freeze | Later resolution |
|---|---|---|
| Worker 模式完整 RC1 E2E 冒烟 | **NOT RUN**（TD-1） | 在 RC2 期间完成（真实 worker 成功 + 超时冒烟，2026-08-17） |
| `hard_reason` 语义 | **NOT IN RC1**（TD-2） | 在 RC2 新增（`hard_reason` 可选字段） |
| 独立备份目标 | **NOT RUN**（TD-3） | 仍待定（操作员决策） |
| 现场演示演练 | **NOT RUN** | 后续执行（Strategy B / Viewer 时代） |
| Viewer / 移动船舶展示 | **NOT IN RC1** | 构建于 Strategy B Viewer 基础 + MVP（2026-08-19），迁移至 D |
| Strategy B causal 主线 | **NOT IN RC1** | 在 `demo-engineering` 成为活跃主线（冻结的 RC1/RC2 未触碰） |

> 明确超出 RC1 范围并冻结：数据产品、corridor 2.2.0、场景、风险语义、C 代价、A 插值、
> hard-mask 策略、规划算法、RC1 制品。RC1 必须仅作为回归 / 黄金参考。

## 6. 与后续阶段的关系

- **RC2**（`rc2-development`，冻结于 2026-08-17）：在 RC1 基础上扩展无冰语义、第二场景
  （Tromsø 144h）、`hard_reason`、覆盖预检。RC2 是独立的冻结基线 — 见
  `../rc2-rc2-development/RC2_DEVELOPMENT_STATUS.md`。
- **Strategy B / Viewer**：`demo-engineering` 活跃开发。Strategy B 是活跃的同一船舶
  causal 主线；Viewer 从 orchestrator 迁移至 `work_package_d` 并达到 MVP PASS（2026-08-19）。
  这些均不属于 RC1。

## 7. RC1 冻结不变量（不得回退）

- 不要修改 `main` 历史或 RC1 制品。
- 不要重写 RC1 digest。
- RC1 是回归检查的黄金基线（如 `rc1_golden_regression.py`）。
