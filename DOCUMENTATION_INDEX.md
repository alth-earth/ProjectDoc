# 文档索引

状态：CURRENT（当前）
最后更新：2026-08-16

## 从这里开始

- [项目梳理报告.md](项目梳理报告.md) — 推荐首先阅读
- [ARCTIC_ROUTE_SYSTEM.md](ARCTIC_ROUTE_SYSTEM.md) — 权威架构
- [CURRENT_STATUS.md](CURRENT_STATUS.md) — 今日状态速览

## 权威层级（冲突裁决）

1. 当前代码/Schema/配置 + 生产者—消费者测试；
2. `ARCTIC_ROUTE_SYSTEM.md`（架构权威）；
3. `DEMO_RC1_BASELINE_20260816.md`（RC1 标识符权威）；
4. `CURRENT_STATUS.md` / `最终交付说明.md`（当前交付状态）；
5. `ABC_10_DAY_SPRINT.md` / 各 WP README / HANDOFF / docs；
6. 执行日志与归档文档（历史证据，不改写）。

## 交付

- [最终交付说明.md](最终交付说明.md)
- [Demo RC1 基线](work_package_a/docs/DEMO_RC1_BASELINE_20260816.md) — RC1 精确标识符权威

## 规划

- [ABC_10_DAY_SPRINT.md](ABC_10_DAY_SPRINT.md)
- [POST_RC1_PLAN.md](POST_RC1_PLAN.md)

## 运维

- [DEMO_RUNBOOK.md](DEMO_RUNBOOK.md)
- [RECOVERY_RUNBOOK.md](RECOVERY_RUNBOOK.md)
- [TECH_DEBT.md](TECH_DEBT.md)

## 开发

- WP A：[README](work_package_a/README.md) / [HANDOFF](work_package_a/work_package_a_handoff.md)
- WP B：[README](work_package_b/README.md)
- WP C：[README](work_package_c/README.md) / [HANDOFF](work_package_c/work_package_c_handoff.md)
- WP D：[README](work_package_d/README.md) / [HANDOFF](work_package_d/HANDOFF.md)
- Orchestrator：[README](arctic_route_orchestrator/README.md) / [HANDOFF](arctic_route_orchestrator/arctic_route_orchestrator_handoff.md)
- Contracts：[README](arctic_route_contracts/README.md) / [HANDOFF](arctic_route_contracts/arctic_route_contracts_handoff.md)

## 历史 / 归档

- 执行日志：`work_package_a/data/output/golden/EXECUTION_LOG_*.md`
- 归档映射：[归档文件映射表与全量比对表.md](归档文件映射表与全量比对表.md)
- `_归档_*` / `.archive-*` 文件为历史证据，保留不改写

## 仅本机

操作者可保留 `local/LOCAL_OPERATOR_ENV.md`（被根 `.gitignore` 忽略，不会提交）。
它不是项目契约。
