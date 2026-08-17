# Route Geospatial Integrity Audit（2026-08-17）

> 状态：**OVERALL = PASS（机器可验证）**
> 机器可读制品：`work_package_a/data/output/rc2-smoke/route-geospatial-integrity.json`
> 本文记录对“Viewer 显示航线穿过 LAND，但页面显示 Hard violations = 0 /
> Coverage Gate = PASS”这一矛盾的独立审计与修复。

## 1. Problem statement

Demo Candidate 2 的 Viewer 运行截图显示航线 polyline 明显经过 LAND（棕色）区域，
但页面同时显示：

- `Hard violations = 0`（来自 C 制品的 `metrics.hard_constraint_violations`）；
- `Coverage Gate = PASS`（来自 orchestrator 的 `planning-coverage-preflight.json`）。

这两个指标分别只回答“C 搜索是否遇到过 hard 边”和“可航节点上是否有 unknown 风险”，
**均不是对路线地理完整性的验证**。上一轮“Demo Candidate 2 = ESTABLISHED /
Pre-Demo Finalization”的结论因此不能直接信任，需要独立、机器可验证的
Route Geospatial Integrity Gate。

## 2. Scope

- 冻结制品：Scenario A（Murmansk → Dikson，RC1 golden 重跑）与
  Scenario B（Tromsø → Isfjorden，RC2 golden r2）；
- 全部真实 frozen routes：两场景 × initial/replanned × 4 层 × 3 目标 =
  **48 条路线**（以制品动态枚举为准，非 hard-code）；
- 数据链：C 制品 `routes/v3/{initial,replanned}.json` → D frozen loader →
  `demo-state.json` → Viewer SVG；
- 风险数据：两场景各 145 帧 committed risk store（含 hard_mask/hard_reason）；
- Live route：不在本轮 frozen gate 范围（`status = NOT_RUN`，单独检查）。

## 3. Data sources

| 项 | Scenario A | Scenario B |
|---|---|---|
| scenario_id | `murmansk_dikson_august_2026_demo_v1` | `tromso_isfjorden_august_2026_demo_v1` |
| output_dir | `rc2-smoke/output-mur-opt` | `rc2-smoke/output-tromso-144h-r2` |
| risk_store | `rc2-smoke/risk-store-mur-opt` | `rc2-smoke/risk-store-tromso-144h-r2` |
| risk commit | `risk-window-sha256-25de23bc…` | `risk-window-sha256-e2a92582…` |
| frames | 145（2026-08-11T06Z → 2026-08-17T06Z，逐小时） | 同左 |
| layer-set（initial/replanned） | `3f9a8f7b…` / `29eba0ac…` | `e135e32d…` / `6e101345…` |

## 4. Route representation

结论：**Viewer 画出的 polyline 就是 C 实际搜索得到的完整路径，不存在降采样、
锚点抽取、插值或直线伪连。**

证据：

1. C 发布代码 `layered.py::_to_v3_plan` / `service.py::_to_route_plan` 把
   `PlanningResult.steps` 逐点写入 `waypoints`（未去重、未抽稀）；
2. 制品 waypoint 坐标全部精确等于风险帧网格节点（容差 1e-9）；
3. 相邻 waypoint 全部是 8-neighbor 网格邻点（无跳格）；
4. 逐段大圆距离之和 = 制品 `metrics.distance_km`（容差 0.5 km），
   逐段 ETA 差之和 = 制品 `metrics.eta_hours`（容差 0.01 h）——若曾抽稀，
   距离/时间不可能逐条一致；
5. D `frozen_loader.py` 原样复制全部 waypoint；`demo-state.json` 与制品
   waypoint 完全一致（逐点 lon/lat/eta 相等）。

实际节点数（audited）：

| 场景/阶段 | full_voyage | main_corridor_24_72h | rolling_0_24h | executable_0_6h |
|---|---|---|---|---|
| A initial | 29 | 18 | 7 | 2 |
| A replanned | 28 | 19 | 7 | 2 |
| B initial | 22 | 22 | 11 | 3 |
| B replanned | 20 | 20 | 11 | 3 |

## 5. Grid / coordinate semantics

- C 网格是**规则 rectilinear 经纬网格**（1-D 严格单调 lat/lon），
  节点即格心；`RegularGrid.from_risk_frame` 直接采用 RiskFrame 坐标；
- Scenario A：12 × 33（lat 67.5–75.0，步长 0.6818°；lon 30.0–85.0，
  步长 1.71875°），396 节点；
- Scenario B：31 × 11（lat 68.5–79.5，步长 0.3667°；lon 10.0–22.0，
  步长 1.2°），341 节点；
- flatten 顺序（D spatial）：row-major（lat 外循环、lon 内循环），
  Viewer 的 grid 绘制与 D 的 flatten 顺序一致；
- C `RiskSampler` 空间采样为双线性插值（lat/lon 各取 ≤2 个 contributor），
  `hard_mask` 对所有 contributor 做 OR——因此对角边中点（格点交叉角）会
  同时看到 2×2 邻域 4 格，任一 hard 都会拒绝该边；
- Viewer SVG 变换：`x = ox + (lon-minLon)*scale`，`y = oy + (maxLat-lat)*scale`
  （y 轴反转），`scale = min(可用宽/经度跨度, 可用高/纬度跨度)`。

## 6. Temporal mapping

- C 对每条边按 `departure_time + travel_hours * fraction` 采样，等价地把
  ETA 映射到 risk frame 时间轴（逐小时帧，`max_frame_gap=180min`）；
- 本审计对每个 waypoint 用其精确 ETA 采样，对每条边用 C 同款 3 采样 +
  约 10 km 密集采样，并做逐小时 bracketing（两帧 OR）；
- 两场景 hard_reason 在全部 145 帧中**恒定**（A：LAND=144、DU=31；
  B：LAND=65、DU=21；available=221/255），因此 LAND 穿越不能用“时间帧
  不一致”解释——时间映射用于排除 DATA_UNAVAILABLE 类动态解释，且证明
  LAND 本身静态；
- 当前 Viewer 只展示 frame 0（initial departure）与 frame 6（replan
  departure）两张静态风险帧——这是**下一阶段 145-frame 播放的已知边界**，
  不是本轮 LAND 矛盾的成因。

## 7. Audit method

`work_package_d/src/arctic_route_display/demo/geo_integrity.py`：

1. `load_frozen_scenario()` 先做身份/checksum/语义 digest/coverage gate 校验；
2. 逐路线检查：waypoint 网格身份、8-neighbor 邻接、距离/ETA 可复算；
3. waypoint hard（精确 ETA）；edge hard（C 3 采样 + ≤10 km 密集采样）；
4. diagonal corner-cut：对角边两个正交侧格在边中时刻是否 hard；
5. temporal mapping：ETA 在窗内、逐小时帧 bracketing、ETA 严格递增；
6. Viewer 投影一致性：按修复后 Viewer 的同一等比投影，统计全部路线 ×
   全部 spatial 帧的 polyline 与 LAND/DATA_UNAVAILABLE/OTHER 格子的
   像素空间相交数；
7. 回归 oracle：同时保留历史“混合投影”计算器，证明旧 Viewer 确实会产生
   视觉相交（A=252、B=72），而修复后为 0。

## 8. Results

```text
Route Geospatial Integrity

Scenario A（murmansk_dikson_august_2026_demo_v1）
Initial
  routes audited: 12    PASS: 12    FAIL: 0
Replanned
  routes audited: 12    PASS: 12    FAIL: 0

Scenario B（tromso_isfjorden_august_2026_demo_v1）
Initial
  routes audited: 12    PASS: 12    FAIL: 0
Replanned
  routes audited: 12    PASS: 12    FAIL: 0

Waypoint hard violations      = 0
Edge hard violations          = 0
LAND intersections            = 0
DATA_UNAVAILABLE violations   = 0
OTHER violations              = 0
Corner-cutting violations     = 0

Temporal mapping              = PASS
C → artifact consistency      = PASS（waypoint 完整、邻接、距离/ETA 可复算）
Artifact → D consistency      = PASS（逐点相等）
D → Viewer consistency        = PASS（修复后 viewer_px = 0）

OVERALL = PASS
```

抽样追踪（frame 0 身份核对）：

| 场景 | 节点 | lon/lat | node (row, col) | hard | reason |
|---|---|---|---|---|---|
| A | start | 33.4375 / 69.5455 | (3, 2) | False | NONE |
| A | goal | 79.8438 / 73.6364 | (9, 29) | False | NONE |
| A | LAND 样本 | 30.0000 / 67.5000 | (0, 0) | True | LAND |
| A | DU 样本 | 43.7500 / 67.5000 | (0, 8) | True | DATA_UNAVAILABLE |
| B | start | 18.4000 / 70.3333 | (5, 7) | False | NONE |
| B | goal | 12.4000 / 78.0333 | (26, 2) | False | NONE |
| B | LAND 样本 | 16.0000 / 68.5000 | (0, 5) | True | LAND |
| B | DU 样本 | 14.8000 / 68.5000 | (0, 4) | True | DATA_UNAVAILABLE |

## 9. Root cause

**Case C：Viewer 渲染器坐标变换不一致（COORDINATE_TRANSFORM_MISMATCH）。**

修复前的 `demo_viewer.html` 同时使用两套投影：

- 路线 polyline：等比（aspect-preserving）`scale = min(...)`；
- 风险格子：独立拉伸 `lonScale = (W-2PAD)/spanLon`、
  `latScale = (H-2PAD)/spanLat`，且格子尺寸按节点数等分而非真实经纬步长。

由于两个场景都不是正方形（A 经度跨度 55° vs 纬度 7.5°；B 经度 12° vs
纬度 11°），格子与路线在像素空间错位：A 在 y 方向错位约一格多、B 在 x
方向错位约一格，导致**地理上正确的路线在屏幕上穿过 LAND/DATA_UNAVAILABLE
格子**。旧 Viewer 像素空间相交：A = 252（LAND 228 + DU 24）、B = 72（LAND 72）。

这不是 Planner correctness bug、不是 artifact/waypoint 丢失、不是 temporal
mapping bug：

- 数据空间（网格身份 + C 同款采样 + 密集采样 + 角切检查）：48/48 路线 0 违规；
- 修正投影后像素空间相交 = 0（两种一致投影方案均验证）。

## 10. Corrective action

最小修复（不伪造路径、不改 Planner、不触碰 frozen baseline）：

- `web/demo_viewer.html`：格子中心改用与路线相同的 `project(lon, lat)`；
  格子尺寸改为真实经纬步长 × 统一 scale × 0.9；删除独立 `lonScale`/
  `latScale`；
- `demo preflight` 新增 **Route Geospatial Integrity** 检查（48 路线 + 投影
  一致性），FAIL 时 preflight 不再输出 READY FOR DEMO；
- `demo build` 的 demo-state 每个场景新增独立维度
  `geo_integrity`（PASS/FAIL/NOT_RUN），与 `result_origin`
  （FROZEN_VALIDATED / LIVE_COMPUTED）分开；
- Viewer 顶部新增独立 badge `ROUTE GEO INTEGRITY: PASS/FAIL/NOT RUN`，
  Coverage 面板新增对应行；
- 新增 `demo geo-integrity` 子命令，输出机器可读审计制品
  `route-geospatial-integrity.json`。

## 11. Regression coverage

新增/更新测试（`work_package_d/tests/unit/`）：

- `test_geo_integrity.py`：合成 3×3 网格覆盖 waypoint LAND、edge
  DATA_UNAVAILABLE、对角角切、时间窗越界、非网格 waypoint、投影回归
  oracle、真实冻结制品 48 路线 PASS；
- `test_demo_viewer_offline.py`：单一投影断言（不再存在独立 lon/lat scale）、
  JS 语法 `node --check`、新增 DOM id；
- 真实制品回归：旧混合投影必然相交（A>0、B>0），修复投影 = 0。

## 12. Remaining limitations

- 本 gate 验证的是**冻结 v3 制品 + committed risk frames** 的几何与时序完整性，
  不等同于科学/适航验证（仍 `demo_unvalidated`）；
- C 内部原始 `PlanningResult.steps` 不落盘，完整性由 waypoint 邻接 +
  距离/ETA 可复算 + 发布代码路径证明；
- Viewer 目前仅展示 2 张 spatial 帧（frame 0/6），145 帧动态播放是下一阶段；
- Live route 不在本轮 frozen gate 内（单独检查）；
- 投影使用等距圆柱近似（equirectangular），高纬度横向比例不精确；未来
  GEBCO 底图阶段应引入正式 CRS/投影。

## 13. Final gate status

```text
Route Geospatial Integrity = PASS（2026-08-17）
Demo Candidate 2 = GEOSPATIALLY VALIDATED ENGINEERING CHECKPOINT
```

在此之前，上一轮“Demo Candidate 2 = ESTABLISHED / Pre-Demo Finalization”
仅为历史结论；本轮以机器审计为准。
