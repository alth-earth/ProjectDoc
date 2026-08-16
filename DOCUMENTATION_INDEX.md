# Documentation Index

Status: CURRENT
Last Updated: 2026-08-16

## Start Here

- [项目梳理报告.md](项目梳理报告.md) — recommended first read
- [ARCTIC_ROUTE_SYSTEM.md](ARCTIC_ROUTE_SYSTEM.md) — authoritative architecture
- [CURRENT_STATUS.md](CURRENT_STATUS.md) — today's status at a glance

## Authority Hierarchy (conflict resolution)

1. Current code/schemas/configs + producer-consumer tests;
2. `ARCTIC_ROUTE_SYSTEM.md` (architecture authority);
3. `DEMO_RC1_BASELINE_20260816.md` (RC1 identifiers authority);
4. `CURRENT_STATUS.md` / `最终交付说明.md` (current delivery state);
5. `ABC_10_DAY_SPRINT.md` / WP README / HANDOFF / docs;
6. Execution logs and archived docs (historical evidence, never edited).

## Delivery

- [最终交付说明.md](最终交付说明.md)
- [Demo RC1 Baseline](work_package_a/docs/DEMO_RC1_BASELINE_20260816.md) — authoritative RC1 identifiers

## Planning

- [ABC_10_DAY_SPRINT.md](ABC_10_DAY_SPRINT.md)
- [POST_RC1_PLAN.md](POST_RC1_PLAN.md)

## Operations

- [DEMO_RUNBOOK.md](DEMO_RUNBOOK.md)
- [RECOVERY_RUNBOOK.md](RECOVERY_RUNBOOK.md)
- [TECH_DEBT.md](TECH_DEBT.md)

## Development

- WP A: [README](work_package_a/README.md) / [HANDOFF](work_package_a/work_package_a_handoff.md)
- WP B: [README](work_package_b/README.md)
- WP C: [README](work_package_c/README.md) / [HANDOFF](work_package_c/work_package_c_handoff.md)
- WP D: [README](work_package_d/README.md) / [HANDOFF](work_package_d/HANDOFF.md)
- Orchestrator: [README](arctic_route_orchestrator/README.md) / [HANDOFF](arctic_route_orchestrator/arctic_route_orchestrator_handoff.md)
- Contracts: [README](arctic_route_contracts/README.md) / [HANDOFF](arctic_route_contracts/arctic_route_contracts_handoff.md)

## History / Archive

- Execution logs: `work_package_a/data/output/golden/EXECUTION_LOG_*.md`
- Archive mapping: [归档文件映射表与全量比对表.md](归档文件映射表与全量比对表.md)
- `_归档_*` / `.archive-*` files are historical and preserved

## Local Only

Operators may keep `local/LOCAL_OPERATOR_ENV.md` (ignored by the root
`.gitignore`, never committed). It is not a project contract.
