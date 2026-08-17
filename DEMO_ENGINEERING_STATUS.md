# Demo Engineering 状态

状态：CURRENT（当前）
最后更新：2026-08-17
适用范围：RC2 Frozen Baseline 之上的演示工程阶段
权威基线：`work_package_a/docs/RC2_BASELINE_20260817.md`

## 1. 阶段定位

- **Demo Candidate 1 = ESTABLISHED（2026-08-17）**；
- **Demo Candidate 2 = ESTABLISHED（2026-08-17）**；
- 建立在 RC2 Frozen Baseline 之上，不修改 RC1/RC2 frozen core；
- 双模式明确区分：Full Validation Mode（真实完整计算 17–26 min）
  与 Live Demo Mode（冻结结果 + 现场 ≤2 min 真实小窗重规划）。

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
| Live Demo 操作与进度反馈（按钮 + elapsed/stage + indeterminate） | PASS（UI 触发真实计算） |
| Live Demo（真实 C 小窗重规划，≈57s，LIVE_COMPUTED） | PASS |
| Demo Preflight（冻结/校验/内存/端口） | PASS |
| 本地只读 Viewer（localhost、无 CDN、无 remote JS/CSS/fonts/tiles） | PASS |
| 失败降级（live TIMEOUT/FAIL 透明、冻结结果仍可看） | PASS（API 显式 FAIL，不冒充成功） |

## 4. 空间数据口径（Demo Candidate 2 新增）

- 来源：冻结输出 `risk/full-window-commit.json` + 对应 risk store 的真实帧
  （Scenario A = `risk-store-mur-opt`，Scenario B = `risk-store-tromso-144h-r2`）；
- 每场景 2 帧：frame 0（initial departure）与 frame 6（replan departure）；
- 每帧输出真实 lon/lat、hard_reason、risk_score、risk_level、confidence；
- ice-free NOT_APPLICABLE 仍以可信计数 + 解释呈现（帧内无逐格标记，不伪造坐标）；
- 路线 geometry 直接来自 frozen/live 制品的 waypoints，不做平滑/移动。

## 5. 技术彩排（Demo Candidate 2，2026-08-17）

| Step | Runtime | Result |
|---|---:|---|
| demo preflight | <1s | PASS（10/10，含 spatial 帧校验） |
| demo build（A+B frozen + live） | <1s | PASS（3 scenarios，demo-state ≈400KB） |
| demo serve（viewer/state/API） | <1s | PASS（HTTP 200） |
| Scenario A 加载（frozen，396 节点） | 即时 | PASS |
| Scenario B 加载（frozen，341 节点，ice-free=57） | 即时 | PASS |
| Compare initial→replanned + Risk score 图层 | 即时 | PASS（Δdistance -81.5km、ΔETA -4.55h） |
| Live 计算（浏览器按钮触发） | ≈56s | PASS（RUNNING→planning→DONE，LIVE_COMPUTED） |
| Live 结果加载进 viewer | <2s | PASS（live tab 更新，expanded=18472） |
| 合计技术演示流程 | ≈1–2 min | 冻结即时；live ≤2min |

## 6. 诚实标识

- `result_origin = FROZEN_VALIDATED / LIVE_COMPUTED`；
- viewer 顶部 badge 明确区分；live 场景 coverage 复用冻结窗口并有 note 说明；
- live TIMEOUT/FAIL 直接显示错误，不静默回退到旧结果。

## 7. 下一步

- Pre-demo final：按 `DEMO_RUNBOOK.md` 走完整答辩流程、恢复演练、独立备份；
- Demo next：已收敛；可选风险时间动画（frame selector 已支持 2 帧）；
- 不引入第三场景；不做正式并发集成。
