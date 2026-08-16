# 演示手册

状态：CURRENT（当前）
最后更新：2026-08-16
适用范围：比赛/验收演示执行

## 前置条件

- WSL 中 `/root/my_project` 完整存在，RC1 制品与两份同 VHD 副本齐全；
- 冻结链路不需要网络（离线审计 PASS）；
- Python 环境：`work_package_a/.venv`、`work_package_b/.venv`、
  `work_package_c/.venv`、`work_package_d/.venv`、`arctic_route_orchestrator/.venv`。

## RC1 标识符

见 `work_package_a/docs/DEMO_RC1_BASELINE_20260816.md`（权威）。
bundle `a-bundle-32cafad4ee280f286d8eb049`；RunContext run-…0b0005；
初始 layer-set `layer-set-sha256-51824e96…`；重规划 `…ec74a145…`。

## 演示前检查

```bash
cd /root/my_project/work_package_a && ./.venv/bin/python -m arctic_route_data.cli doctor --data-root data
cd /root/my_project/arctic_route_orchestrator && ./.venv/bin/python scripts/offline_demo_audit.py
```

预期：doctor `ok:true`；审计输出 `外部网络依赖 = NONE`。

## 模式 A — 完整验证模式（约 25–30 分钟）

```bash
cd /root/my_project/arctic_route_orchestrator
C_ASTAR_PROGRESS_SECONDS=30 UV_CACHE_DIR=$PWD/.uv-cache UV_PYTHON_INSTALL_DIR=$PWD/.uv-python \
  UV_PYTHON_DOWNLOADS=never ./.mamba-env/bin/uv run --locked arctic-route-orchestrator run \
  --execution-spec /root/my_project/work_package_a/data/output/golden/mur-v3-smoke-20260816-r6.execution-spec.json \
  --bundle /root/my_project/work_package_a/data/output/bundles/murmansk_dikson_august_2026_demo_v1.bundle.json \
  --run-context /root/my_project/work_package_a/data/output/bundles/murmansk_dikson_august_2026_demo_v1.run-context.json \
  --a-data-root /root/my_project/work_package_a/data \
  --b-config /root/my_project/work_package_b/configs/models/demo_unvalidated_smoke_grid_v4.json \
  --c-config-root /root/my_project/work_package_c/configs \
  --contracts-config-root /root/my_project/arctic_route_contracts/configs \
  --risk-store-root /tmp/rc1-smoke/risk-store \
  --output-dir /tmp/rc1-smoke/output
```

预期耗时（r7 实测）：初始化 ≈9 分钟、B 构建 ≈15 秒、C 初始 ≈8 分钟、
重规划 ≈8.5 分钟，合计约 25–30 分钟。输出目录 `output/` 下的
`run-stage-report.json` 状态为 `completed`。

## 模式 B — Live Demo 模式（现场实时 ≤2 分钟）

1. 加载冻结结果：打开
   `work_package_a/data/output/golden/mur-v3-smoke-20260816-r6/output/routes/v3/initial.json`
   与 `replanned.json`（交给 D）。
2. 生成 D 快照：
   ```bash
   cd /root/my_project/work_package_d
   ./.venv/bin/arctic-route-display snapshot --v3 <initial.json> --output d-snapshot-initial.json
   ./.venv/bin/arctic-route-display snapshot --v3 <replanned.json> --output d-snapshot-replanned.json
   ```
3. 现场实时小窗（可选、需此前已验证）：只运行一个小型重规划案例，
   并明确标注为“现场实时计算”。

所有来自冻结制品的展示必须标注“预计算 RC1 结果”；现场计算必须标注“实时”。

## 故障恢复

- **C 阶段过慢**：worker 超时现在会终止该阶段并写入 TIMEOUT 阶段报告；
  用同一冻结输入重跑即可。
- **D 出现 schema 错误**：使用本地 schema
  `work_package_c/schemas/four-layer-route-plan-set-v3.schema.json`；D 离线解析。
- **无网络**：演示链路不需要网络；若导入失败，检查代理环境，必要时对单条命令
  临时直连（见 `local/LOCAL_OPERATOR_ENV.md`）。
- **怀疑 bundle 错误**：与 `DEMO_RC1_BASELINE_20260816.md` 中的 digest 核对。
