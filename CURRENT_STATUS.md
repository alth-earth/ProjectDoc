# 当前状态

状态：CURRENT（当前）
最后更新：2026-08-16
适用范围：整个北极航线项目
权威字段：当前里程碑与状态矩阵

## 当前里程碑

**Demo RC1 冻结基线已建立（2026-08-16）。**

精确标识符以
[`work_package_a/docs/DEMO_RC1_BASELINE_20260816.md`](work_package_a/docs/DEMO_RC1_BASELINE_20260816.md)
为权威。

**RC2 功能完善阶段进行中（2026-08-17，分支 `rc2-development`）。**
RC1 保持冻结；RC2 状态见 [`RC2_DEVELOPMENT_STATUS.md`](RC2_DEVELOPMENT_STATUS.md)。

## 当前版本

- contracts 0.3.0 / corridor 2.2.0 / 场景 murmansk_dikson_august_2026_demo_v1 v1.0.0
- A 0.4.2、B 0.2.0、C 0.4.0、D 0.1.0、orchestrator 0.1.0
- bundle：`a-bundle-32cafad4ee280f286d8eb049`
- RunContext：`run-00000000-0000-4000-8000-0000000b0005`

## 状态矩阵

| 领域 | 状态 |
|---|---|
| A 数据 / TOPAZ originalGrid 重建 | PASS |
| 空间覆盖 gate（unknown-navigable = 0） | PASS |
| B 风险构建（hard_mask=land_sea_mask_plus_unknown_v1） | PASS |
| C 初始规划（v3 四层） | PASS |
| 6 小时重规划 | PASS |
| D 真实 v3 制品消费 | PASS |
| 业务语义确定性可复现（r6 与 r7） | PASS |
| 可中断 per-stage 超时机制 | PASS（单元测试） |
| worker 模式完整 RC1 E2E | NOT RUN |
| 离线运行时依赖审计 | PASS（无外部依赖） |
| 同 VHD 备份副本 | PASS（非独立灾备） |

## RC2 状态速览（2026-08-17）

| 领域 | 状态 |
|---|---|
| hard_reason（LAND/DATA_UNAVAILABLE） | PASS（B 产生、C codec/schema、D 消费） |
| coverage preflight 正式化 | PASS（orchestrator 阶段 + schema + gate，单测通过） |
| RC1 golden regression | PASS（r6/r7 digest/checksums） |
| D 解释性增强（coverage 命令） | PASS |
| worker 真实冒烟（成功/超时） | PASS（成功 ×3；真实 C 45.2s 超时中断） |
| 第二场景迁移 | PARTIAL（迁移链 PASS；数据覆盖 BLOCKED，见 RC2 状态） |

## 当前非阻塞技术债

见 [`TECH_DEBT.md`](TECH_DEBT.md)，要点：TD-1 worker 模式全链冒烟；
TD-2 hard_reason 语义；TD-3 独立备份目标；TD-4 可选规划优化。

## 下一步（按优先级）

1. RC2 checkpoint commits（普通 push）；
2. Pre-demo：Live Demo 彩排、恢复演练、独立备份。

详见 [`POST_RC1_PLAN.md`](POST_RC1_PLAN.md)。

## RC2 之前冻结

无 correctness/safety bug 或操作者明确决定，不得修改：数据产品、corridor 2.2.0、
场景、风险语义、C 成本、A 插值、hard-mask 策略、规划算法、RC1 制品。
