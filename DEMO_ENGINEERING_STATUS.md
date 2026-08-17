# Demo Engineering 状态

状态：CURRENT（当前）
最后更新：2026-08-17
适用范围：RC2 Frozen Baseline 之上的演示工程阶段
权威基线：`work_package_a/docs/RC2_BASELINE_20260817.md`

## 1. 阶段定位

- **Demo Candidate = ESTABLISHED（2026-08-17）**；
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
| Coverage / LAND / DATA_UNAVAILABLE / ice-free 解释 | PASS |
| Live Demo（真实 C 小窗重规划，57.6s，LIVE_COMPUTED） | PASS |
| Demo Preflight（冻结/校验/内存/端口） | PASS |
| 本地只读 Viewer（localhost、无 CDN、离线） | PASS |
| 失败降级（live TIMEOUT/FAIL 透明、冻结结果仍可看） | PASS（loader 显式抛错） |

## 4. 技术彩排（2026-08-17）

| Step | Runtime | Result |
|---|---:|---|
| demo preflight | <2s | PASS（8/8） |
| demo build（A+B frozen） | <1s | PASS（2 scenarios） |
| demo run-live（真实重规划） | 57.6s | PASS（LIVE_COMPUTED，distance 909.2km） |
| demo build（含 live） | <1s | PASS（3 scenarios） |
| demo serve + viewer/state 访问 | <3s | PASS（HTTP 200） |
| 合计技术演示流程 | ≈62s | 冻结加载即时；live ≤2min |

## 5. 诚实标识

- `result_origin = FROZEN_VALIDATED / LIVE_COMPUTED`；
- viewer 顶部 badge 明确区分；live 场景 coverage 复用冻结窗口并有 note 说明；
- live TIMEOUT/FAIL 直接显示错误，不静默回退到旧结果。

## 6. 下一步

- Pre-demo final：按 `DEMO_RUNBOOK.md` 走完整答辩流程、恢复演练、独立备份；
- Demo next：可选 viewer 交互打磨（风险图例、数据质量着色）；
- 不引入第三场景；不做正式并发集成。
