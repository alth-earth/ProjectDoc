---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
Document Role: CANONICAL
Scope: parallel development ownership and repository write boundaries
Canonical For: who may modify each research stream and integration sequence
Branch: research-validation-system
Last Verified: 2026-08-22
---

# 研究验证系统开发职责归属

## 职责矩阵（2026-08-22 00:02）

| 角色 | 主目录 | 负责 | 不得修改 |
|---|---|---|---|
| 契约负责人 | `arctic_route_contracts/configs`、契约模型/模式/测试 | 共享身份与已批准的版本提案 | A/B/C/D 业务实现 |
| A 负责人 | `work_package_a/src`、A 配置/测试/文档 | 采集、溯源、规整化、A 发布 | 风险、航线、Viewer 语义 |
| B 负责人 | `work_package_b/src`、B 配置/测试/文档 | 风险模型、固定网格实验、RiskFrame 生产 | A 私有数据、C 航线/ETA、D 渲染 |
| C 负责人 | `work_package_c/src`、C 配置/测试/文档 | 规划、最终速度/ETA、航线/重规划、性能剖析 | B 风险公式、A 采集、D 界面 |
| D 负责人 | `work_package_d/viewer`、D 测试/文档 | 可视化与验证运行时 | A/B/C 私有读取或业务重算 |
| 编排器负责人 | `arctic_route_orchestrator/replay`、`scripts`、测试 | 流水线、重放、适配器/导出 | 第二个 Viewer 运行时或臆造的 B/C 语义 |
| 治理/集成负责人 | `arctic_route_governance/current`、报告、集成 fixtures | 提案、证据等级、合并顺序、阶段门禁 | 单边语义所有权 |

## 并行工作规则（2026-08-22 00:02）

- 每个文件单一写者，每个契约单一语义负责人。
- B、C、D 的实验使用互不相交的仓库与带版本 fixtures。
- 跨包变更从已批准的提案开始；禁止消费者驱动地直接修改另一生产者。
- 不允许两个重型重放/集成任务并发运行。在内存处于记录预算内时，单元/lint 任务可独立运行。
- 实验产物使用新身份/路径，绝不覆盖冻结的 RC1、RC2、Summer 或 48h 制品。

## 集成顺序（2026-08-22 00:02）

```text
提案 + fixtures
  -> 生产者实现/测试
  -> 消费者选择性接入/测试
  -> 聚焦集成
  -> 语义摘要与资源评审
  -> 一次串行阶段退出重放
```

在声明的生产者-消费者与制品门禁通过之前，`Experimental` 实现不得提升为 `Validated`。

## Round3 交接通道（2026-08-22 02:34 +08:00）

| 负责人 | 就绪输入 | 已授权下一步 | 阻塞门禁 |
|---|---|---|---|
| A | 九条完整冬季源数据行 | 仅解决三条 GFS 行与节奏策略 | 12/12 精确覆盖前无冬季 bundle |
| B | 未变的 medium summer RiskFrame fixture | 仅 A 门禁通过后消费未来 immutable 冬季 bundle | 禁止直接读取 A cache/raw |
| C | 精确样本剖面与默认关闭的 50k LRU | 正式接入 + 三目标 + 四层相等性测试 | 尚未可生产启用 |
| D | 无新冬季展示制品 | 停留在既有 bundle | 禁止源数据绕过或臆造图层 |
| 治理 | 运行时日志与报告 | 批准 A 节奏决策与 C 提升门禁 | 证据标签仍为 EXPERIMENTAL/PARTIAL |

A 采集与 C 缓存工作互不相交。可由不同负责人开发，但重型采集、基准与重放任务在当前 7 GiB WSL 宿主上仍串行。
