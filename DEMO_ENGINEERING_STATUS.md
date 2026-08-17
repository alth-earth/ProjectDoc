# Demo Engineering 状态

状态：CURRENT（当前）
最后更新：2026-08-17
适用范围：RC2 Frozen Baseline 之上的演示工程阶段
权威基线：`work_package_a/docs/RC2_BASELINE_20260817.md`

## 1. 阶段定位

- **Demo Candidate 1 = ESTABLISHED（2026-08-17）**；
- **Demo Candidate 2 = GEOSPATIALLY VALIDATED ENGINEERING CHECKPOINT
  （2026-08-17，Route Geospatial Integrity 审计后）**；
- 建立在 RC2 Frozen Baseline 之上，不修改 RC1/RC2 frozen core；
- 双模式明确区分：Full Validation Mode（真实完整计算 17–26 min）
  与 Live Demo Mode（冻结结果 + 现场 ≤2 min 真实小窗重规划）。

> 历史事实：2026-08-17 较早轮次曾把 Candidate 2 记为 `ESTABLISHED`。
> 在 Viewer 出现“航线视觉穿过 LAND 但 Hard violations=0”后，该结论被
> 独立 Route Geospatial Integrity 审计取代（见
> [`ROUTE_GEOSPATIAL_INTEGRITY_AUDIT_20260817.md`](ROUTE_GEOSPATIAL_INTEGRITY_AUDIT_20260817.md)）。

## 2. 分支与来源

- Demo 分支：`demo-engineering`（由 RC2 Frozen commits 派生）；
- Frozen 来源：Scenario A `output-mur-opt`（业务与 RC1 golden r6 一致）、
  Scenario B `output-tromso-144h-r2`（RC2 golden r2）；
- 配置：`work_package_d/configs/demo_frozen_sources.json`。

## 3. 能力矩阵

| 能力 | 状态 |
|---|---|
| Demo Data Model（scenario/route/layer/coverage/hard reason/origin） | PASS |
| Frozen Result Loader（identity/checksum/digest 校验 + RC1 golden 对照） | PASS |
| Scenario A 冻结展示（12 路线/阶段，gate=True） | PASS |
| Scenario B 冻结展示（12 路线/阶段，ice-free=57） | PASS |
| Initial/Replanned 切换与指标差异 | PASS |
| Initial vs Replanned 真实 delta 表（Δdistance/ETA/risk、route_changed） | PASS（Compare 模式） |
| Coverage / LAND / DATA_UNAVAILABLE / ice-free 解释 | PASS |
| 离线经纬度地图（真实风险帧坐标，非伪造） | PASS（SVG，A/B 自动 fit bounds） |
| 空间图层：Availability / Risk score / Risk level | PASS（frame 0=initial、frame 6=replan） |
| LAND / DATA_UNAVAILABLE / OTHER 图例与说明 | PASS（与 risk 分开） |
| Scenario A/B 交互切换 | PASS（地图/指标/coverage 同步更新） |
| Route Layer/Objective 选择（4 层 × 3 目标） | PASS |
| **Route Geospatial Integrity gate（机器审计 48/48）** | **PASS**（2026-08-17 新增；waypoint/edge/LAND/DU/角切/时间映射/投影一致性 0 违规） |
| Live Demo 操作与进度反馈（按钮 + elapsed/stage + indeterminate） | PASS（UI 触发真实计算） |
| Live Demo（真实 C 小窗重规划，≈57s，LIVE_COMPUTED） | PASS |
| Demo Preflight（冻结/校验/Route Geospatial Integrity/内存/端口） | PASS（11 项；gate FAIL 则 READY FOR DEMO 不输出） |
| 本地只读 Viewer（localhost、无 CDN、无 remote JS/CSS/fonts/tiles） | PASS |
| 失败降级（live TIMEOUT/FAIL 透明、冻结结果仍可看） | PASS（API 显式 FAIL，不冒充成功） |

## 4. 空间数据口径（Demo Candidate 2 新增）

- 来源：冻结输出 `risk/full-window-commit.json` + 对应 risk store 的真实帧
  （Scenario A = `risk-store-mur-opt`，Scenario B = `risk-store-tromso-144h-r2`）；
- 每场景 2 帧：frame 0（initial departure）与 frame 6（replan departure）；
- 每帧输出真实 lon/lat、hard_reason、risk_score、risk_level、confidence；
- ice-free NOT_APPLICABLE 仍以可信计数 + 解释呈现（帧内无逐格标记，不伪造坐标）；
- 路线 geometry 直接来自 frozen/live 制品的 waypoints，不做平滑/移动。

### 4.1 Route Geospatial Integrity（2026-08-17 审计后）

- 审计链：C 制品 waypoints（= 完整搜索路径，无降采样）→ D loader →
  demo-state → Viewer；
- 检查项：waypoint 网格身份与邻接、距离/ETA 可复算、waypoint hard（ETA）、
  edge hard（C 同款 3 采样 + ≤10 km 密集采样）、对角角切（正交侧格）、
  ETA→frame 时间映射、Viewer 投影一致性（像素空间相交=0）；
- 结果：Scenario A/B 各 24 路线（initial 12 + replanned 12），48/48 PASS，
  机器制品 `route-geospatial-integrity.json`；
- 上一轮“Hard violations=0”只说明 C 搜索未接受 hard 边；“Coverage Gate
  PASS”只说明可航节点无 unknown 风险；二者都不是路线地理完整性结论。

### 4.2 Viewer 修复（Case C：坐标变换 bug）

- 根因：旧 Viewer 路线用等比投影、格子用独立 x/y 拉伸投影，两套变换在
  非正方形场景下错位（A 纵向、B 横向），使地理正确的路线在屏幕上穿过
  LAND/DU 格子（旧像素相交 A=252、B=72）；
- 修复：格子中心与路线共用同一 `project(lon, lat)`，格子尺寸改用真实
  经纬步长 × 统一 scale；不修改路线坐标、不伪造任何路径；
- 回归：旧混合投影必然相交（测试 oracle），修复后像素相交 = 0。

### 4.3 Temporal Semantics（2026-08-17 审计后）

- Viewer 的 `Frame initial / Frame replan` 标签是 **risk 帧的 valid_time**
  （06:00Z / 12:00Z），不是 simulation snapshot；
- demo-state spatial 帧当前**不保存** `as_of_time` 与 `scenario_mode`
  （结构性 gap，下一阶段 SimulationSnapshot 补齐）；
- 两场景都是 `retrospective_best_estimate`：`knowledge_as_of`
  （08-16 / 08-15）晚于 `simulation_start`（08-11 06:00Z）；
- 完整语义见
  [`TEMPORAL_SEMANTICS_AUDIT_20260817.md`](TEMPORAL_SEMANTICS_AUDIT_20260817.md)
  与 [`TIME_MODEL_QUICK_REFERENCE.md`](TIME_MODEL_QUICK_REFERENCE.md)。

### 4.4 Causal Replay Feasibility 与模式诚实展示（2026-08-17）

- 机器审计：A ready 20/145（first 08-16T11:00Z，longest 19h）、
  B ready 45/145（first 08-15T10:00Z，longest 44h）；严格 144h
  tick-by-tick causal replay 不被历史证据支持（见
  `CAUSAL_REPLAY_FEASIBILITY_AUDIT_20260817.md`）；
- demo-state 与 Viewer 现在显式展示 `scenario_mode`（
  RETROSPECTIVE BEST ESTIMATE）、`simulation_start/end` 与
  `knowledge_as_of`，避免把事后数据理解为当时预测；
- 架构设计见 `SIMULATION_REPLAY_ARCHITECTURE.md`（DESIGN ONLY）。

## 5. 技术彩排（Demo Candidate 2，2026-08-17）

| Step | Runtime | Result |
|---|---:|---|
| demo preflight | <1s | PASS（11/11，含 Route Geospatial Integrity gate） |
| demo geo-integrity | <1s | PASS（48/48 routes，viewer_px=0；机器制品 route-geospatial-integrity.json） |
| demo build（A+B frozen + live） | <1s | PASS（3 scenarios，demo-state ≈400KB，每场景含 geo_integrity 摘要） |
| demo serve（viewer/state/API） | <1s | PASS（HTTP 200） |
| Scenario A 加载（frozen，396 节点） | 即时 | PASS |
| Scenario B 加载（frozen，341 节点，ice-free=57） | 即时 | PASS |
| Compare initial→replanned + Risk score 图层 | 即时 | PASS（Δdistance -81.5km、ΔETA -4.55h） |
| Live 计算（浏览器按钮触发） | ≈56s | PASS（RUNNING→planning→DONE，LIVE_COMPUTED） |
| Live 结果加载进 viewer | <2s | PASS（live tab 更新，expanded=18472） |
| 合计技术演示流程 | ≈1–2 min | 冻结即时；live ≤2min |

## 6. 诚实标识

- `result_origin = FROZEN_VALIDATED / LIVE_COMPUTED`；
- `geo_integrity = PASS / FAIL / NOT_RUN` 是**独立维度**，与
  `result_origin` 分开展示（Viewer 顶部双 badge）；
- viewer 顶部 badge 明确区分；live 场景 coverage 复用冻结窗口并有 note 说明；
- live TIMEOUT/FAIL 直接显示错误，不静默回退到旧结果。

## 7. 下一步

- 当前能力边界：空间图层只有 2 张 presentation 帧（frame 0 = initial
  departure、frame 6 = replan departure；= risk valid_time 帧），**不是
  145 帧动态风险动画，也不是 simulation snapshot**；
- NEXT PHASE（仅 integrity PASS 后，本轮不实施）：
  P0 Simulation Snapshot schema（simulation_time × knowledge_as_of ×
  scenario_mode × B horizon × C layers）→ P1 short-window rolling replay
  MVP（Scenario B 08-15T10:00Z 起 12–24h）→ P2 全窗需 causal-ready 采集 →
  P2 GEBCO georeferenced basemap → P3 Simulation-clock Viewer + Timeline
  （play/pause/scrub/1×/2×/4×/8×，主控 = simulation_time）→
  P4 动态 B forecast（current/+6h/+12h/+24h）→ P5 动态 C routes +
  Moving Ship → P6 +6h Replanning Event（old route faded/dashed、new route
  highlighted）→ P7 overlays（hard/ice/edge/grid）→ P8 Scenario/Objective/
  Mode UI（CAUSAL / RETROSPECTIVE 区分）→ P9 Pre-Demo Finalization；
- 不引入第三场景；不做正式并发集成。
