# 演示手册

状态：CURRENT（当前）
最后更新：2026-08-17
适用范围：比赛/验收演示执行（Demo Candidate 2，基于 RC2 Frozen Baseline）

## 前置条件

- WSL 中 `/root/my_project` 完整存在，RC1 制品与两份同 VHD 副本齐全；
- 冻结链路不需要网络（离线审计 PASS）；
- Python 环境：`work_package_a/.venv`、`work_package_b/.venv`、
  `work_package_c/.venv`、`work_package_d/.venv`、`arctic_route_orchestrator/.venv`。

## 基线标识符

- RC1：`work_package_a/docs/DEMO_RC1_BASELINE_20260816.md`（权威）。
- RC2：`work_package_a/docs/RC2_BASELINE_20260817.md`（权威，含多仓库 SHA）。
- Demo 配置：`work_package_d/configs/demo_frozen_sources.json`。

## 演示前检查

```bash
cd /root/my_project/work_package_a && ./.venv/bin/python -m arctic_route_data.cli doctor --data-root data
cd /root/my_project/arctic_route_orchestrator && ./.venv/bin/python scripts/offline_demo_audit.py
cd /root/my_project/work_package_d && ./.venv/bin/python -m arctic_route_display.cli demo preflight
cd /root/my_project/work_package_d && ./.venv/bin/python -m arctic_route_display.cli demo geo-integrity
```

预期：doctor `ok:true`；审计输出 `外部网络依赖 = NONE`；geo-integrity 输出
`OVERALL = PASS`；preflight 输出 `READY FOR DEMO`（preflight 已内含
Route Geospatial Integrity gate，gate FAIL 时不输出 READY FOR DEMO）。

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

1. 构建冻结演示状态（A+B，即时）：
   ```bash
   cd /root/my_project/work_package_d
   ./.venv/bin/python -m arctic_route_display.cli demo build \
     --config configs/demo_frozen_sources.json \
     --output /root/my_project/work_package_a/data/output/rc2-smoke/demo-state.json
   ```
   demo-state 现在同时携带每场景 2 帧真实经纬度风险帧
   （frame 0 = initial departure，frame 6 = replan departure），
   Viewer 据此绘制 Availability / Risk 图层，不依赖任何在线地图服务；
   每个场景还携带 `geo_integrity` 摘要（PASS/FAIL/NOT_RUN），
   与 `result_origin` 分开展示。
2. 现场实时小窗重规划（真实 C，≈60s，LIVE_COMPUTED）：
   ```bash
   cd /root/my_project/work_package_d
   ./.venv/bin/python -m arctic_route_display.cli demo run-live \
     --config configs/demo_frozen_sources.json \
     --output /root/my_project/work_package_a/data/output/rc2-smoke/live-result.json
   ```
3. 合并 live 结果并启动本地 Viewer：
   ```bash
   cd /root/my_project/work_package_d
   ./.venv/bin/python -m arctic_route_display.cli demo build \
     --config configs/demo_frozen_sources.json \
     --live-result /root/my_project/work_package_a/data/output/rc2-smoke/live-result.json \
     --output /root/my_project/work_package_a/data/output/rc2-smoke/demo-state.json
   ./.venv/bin/python -m arctic_route_display.cli demo serve \
     --state /root/my_project/work_package_a/data/output/rc2-smoke/demo-state.json \
     --port 8123
   ```
   浏览器打开 `http://127.0.0.1:8123/`（仅本机，离线）。

   更常用的现场流程（无需手工合并 live）：
   ```bash
   cd /root/my_project/work_package_d
   ./.venv/bin/python -m arctic_route_display.cli demo build \
     --config configs/demo_frozen_sources.json \
     --output /root/my_project/work_package_a/data/output/rc2-smoke/demo-state.json
   ./.venv/bin/python -m arctic_route_display.cli demo serve \
     --state /root/my_project/work_package_a/data/output/rc2-smoke/demo-state.json \
     --port 8123
   ```
   在页面 Scenario B 点击 **Run Live Replanning**：
   按钮通过本地 `/api/live/start` 启动真实 worker，页面显示
   elapsed/stage 与 indeterminate 进度；完成后自动把 `LIVE COMPUTED`
   结果加载进 viewer（新标签或原位更新），失败则明确显示 TIMEOUT/FAIL。

4. 演示要点：
   - Scenario A/B 标签切换；
   - Phase = Compare initial → replanned（真实 Δ 指标表 + 双路线 overlay）；
   - Map layer = Availability / Risk score / Risk level；Frame = initial / replan；
   - 顶部双 badge：`FROZEN VALIDATED / LIVE COMPUTED`（结果来源）与
     `ROUTE GEO INTEGRITY: PASS`（路线地理完整性，独立维度）；
   - Coverage 面板解释 LAND、DATA_UNAVAILABLE、ice-free NOT_APPLICABLE；
   - 全程离线：无 CDN、无 remote JS/CSS/fonts/map tiles/schema。

诚实标识：冻结展示顶部 badge 为 `FROZEN VALIDATED`；现场计算为
`LIVE COMPUTED`；live 失败（TIMEOUT/FAIL）会明确显示，不会伪装成功。
完整 17–26 min 验证链路仍保留为 Mode A，供“系统真的会算”的证明。

## 故障恢复

- **Live 计算超时**：真实 worker watchdog 在约 110s 终止并写入 TIMEOUT 结果；
  冻结结果仍可继续展示，操作者说明“现场实时 smoke 本次未完成”。
- **Route Geospatial Integrity FAIL**：`demo preflight` 会失败并列出违规；
  不要用“看起来没穿 LAND”当作通过依据，先按
  `ROUTE_GEOSPATIAL_INTEGRITY_AUDIT_20260817.md` 的 violation type 定位
  层（waypoint/edge/角切/时间/投影），修复后重跑 geo-integrity 与 preflight。
- **D 出现 schema 错误**：使用本地 schema
  `work_package_c/schemas/four-layer-route-plan-set-v3.schema.json`；D 离线解析。
- **无网络**：演示链路不需要网络；若导入失败，检查代理环境，必要时对单条命令
  临时直连（见 `local/LOCAL_OPERATOR_ENV.md`）。
- **怀疑 bundle 错误**：与 `DEMO_RC1_BASELINE_20260816.md` 中的 digest 核对。
