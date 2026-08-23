---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - PLANNED
Document Role: SUPPORTING
Scope: A→B→C→D risk identity, Winter data coverage, risk distribution, mapping, and route-impact audit
Canonical For: NO; current phase remains in current/CURRENT_STATUS.md
Branch: research-validation-system
Last Verified: 2026-08-23
Related Canonical Docs:
  - ../../current/CURRENT_STATUS.md
  - ../../current/reference/WINTER_SCENARIO_STATUS.md
---

# Risk Pipeline Audit 与 Winter Data Validation 报告

## 1. Executive Summary（2026-08-23 19:19 +08:00）

本轮回答“为什么当前 Viewer 看起来几乎都是低风险”。最终判定：**现象已确认，但不是单一
Viewer 渲染 bug**。首要原因是当前 D frozen Viewer 明确消费 Summer 48h artifact，而不是
已验证的 Winter RiskFrame；其次，即使查看 Winter finite ocean cells，当前
`demo_unvalidated` B 基线经等宽 level policy 映射后仍有 `93.069778%` 为 L1、
`6.927052%` 为 L2，仅 1 个 finite cell 进入 L3，没有 finite L4/L5。

Winter A 不是“缺少 12 类输入”：冻结 bundle 的 12/12 record-level coverage 和 provenance
全部完整。但不同 source footprint 在 raw cell 和 B target grid 上确有非有限区域；B 把这些
单元 fail closed 为 `DATA_UNAVAILABLE`/hard/NaN，而不是衰减成低风险。C 已消费相同 Winter
RiskWindow，并产生可测的 risk-time tradeoff；D 的 level 色阶和 hard layer 分离逻辑与 artifact
一致。当前 blocker 是科学解释与同 identity Winter combined Viewer artifact，而不是 C/D 重算。

### Key Delta Table（2026-08-23 19:19 +08:00）

| Metric / Claim | Before | Audit evidence | Verdict |
|---|---|---|---|
| 当前 Viewer season identity | 未明确 | Summer Aug-2026 / 49 frames | CONFIRMED |
| Winter 12-type coverage | 可能缺变量 | 12/12 complete；1,212 records | CONFIRMED COMPLETE |
| Winter finite risk mean | 旧报告 `0.119016` | 独立 frame scan `0.119016` | CONFIRMED |
| Winter finite L1 ratio | 被 total L1 `59.37%` 掩盖 | finite-only `93.07%` | CORRECTED INTERPRETATION |
| Winter L5 environmental risk | 旧 total 表为 `36.21%` | finite L5=0；17,902 全为 hard unknown | CORRECTED INTERPRETATION |
| C risk sensitivity | 定性 | low-risk avg -3.81%、max -20.61% | CONFIRMED |
| Viewer mapping defect | 怀疑 | exact level colors；hard separate | NOT CONFIRMED |

### Claim Matrix（2026-08-23 19:19 +08:00）

| Claim | Status | Validation Level | Evidence | Limitation |
|---|---|---|---|---|
| Winter A exact bundle 可恢复 | PASS | REAL_E2E_PASS | public exact resolver；1,212 records | read-only，未重发 bundle |
| Winter B formal RiskFrame 可用 | PASS | AUTHORITATIVE_PASS | committed 145-frame window | model `demo_unvalidated` |
| Winter 风险高于 Summer output | OBSERVED | REAL_E2E_PASS | same realized grid comparison | 非受控季节因果 |
| 当前 Viewer 展示 Winter risk | FAIL | NOT_IMPLEMENTED | Viewer scenario 是 Summer | combined Winter bundle 缺失 |
| unknown 没有变成 safe | PASS | AUTHORITATIVE_PASS | hard/reason mismatch=0 | source footprint 仍有缺口 |
| C 对 risk variation 有响应 | PASS | REAL_E2E_PASS | 12 routes + integrity | 未做消融实验 |
| per-cell risk explanation | ABSENT | NOT_IMPLEMENTED | schema/artifact audit | 只有全局 component config |

## 2. Scope / Non-Scope（2026-08-23 19:19 +08:00）

Scope：只读恢复 Winter A frozen bundle、统计 raw/source values、核验 Winter B committed
RiskFrame、score/level/hard mapping、Winter C route metrics、当前 D bundle identity 与
render mapping，并运行现有 B/C/D tests。

Non-scope：未修改 A pipeline、B 公式/权重/阈值、C planner、D renderer、shared contracts
或 frozen artifacts；未重新生成 RiskFrame、route、replay 或 Viewer bundle；未混装 Summer
replay 与 Winter candidates。

## 3. Starting Baseline / Experiment Identity（2026-08-23 19:19 +08:00）

| Identity | Winter formal value |
|---|---|
| DatasetBundle | `a-bundle-a2146dd0adbaa7db77a6beb7` |
| bundle digest | `a2146dd0adbaa7db77a6beb7c818e975888600fb31236901fd4af2092069fb71` |
| bundle SHA-256 | `e28bcca682bb1047381d96d574d42c927f28bf5cd26c363f19fff1fff21c3a2f` |
| RunContext | `run-441b03c8-d45b-5414-b0e8-b7fd0d990c22` |
| scenario | `tromso_isfjorden_february_2026_research_v1` |
| ExecutionSpec | `orchestrator.execution-spec.v1` |
| window | `2026-02-15T00Z` → `2026-02-21T00Z` |
| B RiskWindow | `risk-window-sha256-b5bed6bb48893e32620710e8c765dc60ec37a2fc384f0c49014b92f0a1c056b2` |
| B schema / grid | `bc.risk-frame.v2`；145 hourly；31×11 |
| C artifact | `cd.four-layer-route-plan-set.v3`；4×3=12 routes |

当前实际显示身份：

| Surface | Actual identity |
|---|---|
| Viewer replay | `sb-viewer-baseline-48h` |
| scenario | `tromso_isfjorden_august_2026_demo_v1` |
| time | `2026-08-15T10Z` → `2026-08-17T10Z` |
| risk | Summer `bc.risk-frame.v2` projection；49 frames |
| DatasetBundle ID | Viewer bundle 未发布该字段 |
| route | embedded 19 authoritative revisions；`full_voyage/recommended` |
| route candidates | `NOT_PUBLISHED` / empty |

因此当前页面不是 Winter visualization，也没有把 Winter candidate sidecar 混入 Summer
bundle；它诚实进入 `SINGLE_ROUTE_FALLBACK`。

## 4. Git Final State（2026-08-23 19:19 +08:00）

| Repo | Branch | Start HEAD | End HEAD | Tracking | Tree before report | Planned commit | Push |
|---|---|---|---|---|---|---|---|
| governance | research-validation-system | `9db7bee` | 本报告 commit | origin/research-validation-system | clean | audit report only | NO |
| contracts | research-validation-system | `c19e910` | unchanged | origin | clean | none | NO |
| orchestrator | research-validation-system | `6888830` | unchanged | origin | clean | none | NO |
| A | research-validation-system | `b40c689` | unchanged | origin | clean | none | NO |
| B | research-validation-system | `2d034bf` | unchanged | origin | clean | none | NO |
| C | research-validation-system | `8d90695` | unchanged | origin | clean | none | NO |
| D | research-validation-system | `e5488f4` | unchanged | origin | clean | none | NO |

## 5. Filesystem & Resource Safety（2026-08-23 19:19 +08:00）

- 主动写入仅 `/root/my_project/**`；报告在 governance，分析输出和 logs 在 `.runtime/**`。
- 初始 `MemAvailable`：约 5.9 GiB；最低观测约 5.4 GiB；分析后约 5.9 GiB。
- Swap used：初始约 3.7 MiB；峰值/最终约 34 MiB；分析进程自身 swaps=0。
- A exact restore：peak RSS `974,252 KiB`；wall `3:36.75`。
- B/C/D pytest peak RSS：398,876 / 102,232 / 70,640 KiB。
- OOM：0。
- 重复 heavy overlap：发现 A 子代理启动 raw scan 后立即中止；权威 exact restore 保持单任务。
- `/` 的 880 GiB 是 WSL VHD 逻辑可用空间；Windows 宿主物理空间为 `UNKNOWN`。

## 6. A Dataset Validation（2026-08-23 19:19 +08:00）

### Record-level coverage（2026-08-23 19:19 +08:00）

| Data type | Records | Cadence | Coverage | Source / quality |
|---|---:|---|---|---|
| land_sea_mask | 1 | static | complete | GEBCO；good |
| ocean_current | 145 | 1h | complete | Copernicus；suspect |
| sea_ice_concentration | 145 | 1h | complete | Copernicus；suspect |
| sea_ice_drift | 145 | 1h | complete | Copernicus；suspect |
| sea_ice_edge | 145 | 1h | complete | Copernicus；suspect |
| sea_ice_thickness | 145 | 1h | complete | Copernicus；suspect |
| sea_ice_type | 145 | 1h | complete | Copernicus；suspect |
| water_level | 145 | 1h | complete | Copernicus；suspect |
| wave | 49 | 3h | complete | Copernicus；suspect |
| wind_field | 49 | 3h | complete | CARRA；suspect |
| temperature | 49 | 3h | complete | CARRA；suspect |
| visibility | 49 | 3h | complete | CARRA；suspect |

### Raw/source variable statistics（2026-08-23 19:19 +08:00）

下表来自 frozen bundle public exact restore，统计原 source arrays；missing ratio 表示 source
footprint 内非有限 cells，不等同于最终 B navigable coverage。向量保留 u/v 分量，未事后发明
vector contributor。

| Variable | Exists | Raw missing | Min | Max | Mean | Unit |
|---|---|---:|---:|---:|---:|---|
| air_temperature_2m | YES | 0% | 233.876 | 279.683 | 264.910 | K |
| visibility | YES | 0% | 46.383 | 50,000 | 36,480.362 | m |
| wind_u10 | YES | 0% | -21.026 | 14.045 | -3.147 | m/s |
| wind_v10 | YES | 0% | -23.665 | 20.723 | -4.754 | m/s |
| significant_wave_height | YES | 31.956% | 0 | 8.090 | 2.803 | m |
| ice_concentration | YES | 22.339% | 0 | 1.000 | 0.144 | 1 |
| ice_thickness | YES | 22.339% | 0 | 0.817 | 0.053 | m |
| ice_drift_u | YES | 22.339% | -0.432 | 0.227 | -0.054 | m/s |
| ice_drift_v | YES | 22.339% | -0.245 | 0.246 | ~0 | m/s |
| ice_edge | YES | 39.441% | 0 | 1 | 0.023 | 1 |
| ice_type | YES | 39.441% | 0 | 2 | 0.448 | 1 |
| ocean_current_u | YES | 22.339% | -0.671 | 1.445 | -0.071 | m/s |
| ocean_current_v | YES | 22.339% | -0.505 | 1.329 | 0.084 | m/s |
| sea_surface_height | YES | 22.339% | -0.821 | -0.053 | -0.588 | m |
| land_sea_mask | YES | 0% | 0 | 1 | 0.825 | 1 |

B 31×11 target grid 上，temperature/visibility/wind/land mask 的累计 missing 为 0；wave 为
35.033%，冰/海流/水位约 23.46–24.63%。这些 footprint 相互重叠，最终
`DATA_UNAVAILABLE` 是 8,477/49,445 cells（17.144%），不能相加。

## 7. B Risk Distribution / Mapping Validation（2026-08-23 19:19 +08:00）

### Score statistics（2026-08-23 19:19 +08:00）

| Statistic | Summer displayed | Winter formal |
|---|---:|---:|
| finite count | 12,495 | 31,543 |
| min | 0.014691 | 0.035493 |
| mean | 0.045028 | 0.119016 |
| P50 | 0.043758 | 0.106969 |
| P90 | 0.060523 | 0.179519 |
| P95 | 0.064754 | 0.226415 |
| P99 | 0.073932 | 0.335272 |
| max | 0.162555 | 0.400563 |

| Score bin | Summer finite | Winter finite |
|---|---:|---:|
| `[0, 0.1)` | 99.711885% | 41.644739% |
| `[0.1, 0.3)` | 0.288115% | 56.291412% |
| `[0.3, 0.5)` | 0% | 2.063849% |
| `[0.5, 1.0]` | 0% | 0% |

### score → level → color（2026-08-23 19:19 +08:00）

实现是 `clip(floor(risk_score*5)+1, 1, 5)`：`[0,.2)→L1`、`[.2,.4)→L2`、
`[.4,.6)→L3`、`[.6,.8)→L4`、`[.8,1]→L5`。NaN 使用保守 level 5，但同时必须 hard。

| Finite level | Summer | Winter |
|---|---:|---:|
| L1 | 100% | 93.069778% |
| L2 | 0% | 6.927052% |
| L3 | 0% | 0.003170%（1 cell） |
| L4 | 0% | 0% |
| L5 | 0% | 0% |

D 直接把 level 1–5 映射为 green/blue/yellow/orange/red；presentation opacity 只影响视觉，
不改变 level。`LAND` 和 `DATA_UNAVAILABLE` 在独立 hard 分支绘制，不使用 risk color。因此
没有发现 threshold、clipping 或 Viewer color lookup 实现错误；但离散 level 会隐藏同一 L1
内部从 0.035 到 0.199 的变化，这是 presentation information loss，不是数值篡改。

### Availability and explanation（2026-08-23 19:19 +08:00）

Winter hard reasons：`LAND=9,425`、`DATA_UNAVAILABLE=8,477`、`NONE=31,543`；
`unknown_navigable_nodes=0`、hard/reason mismatch=0。缺测不会衰减 risk：任一必需 component
非有限时，risk 为 NaN、confidence=0、hard=true。open-water 规则只在可信
`ice_concentration<0.15` 时把缺失 ice_type/edge 中性化为 0，并记录计数。

RiskFrame 发布 confidence、source_summary、formula/policy 和 missing counters，但没有 per-cell
`contributors`、component contribution、feature importance 或 explanation。当前只能审计全局
11-component weights，不能从 artifact 直接回答“某 cell 为什么是 0.12”。

## 8. Experiments / Alternatives（2026-08-23 19:19 +08:00）

| 方法 | 结果 | 决定 |
|---|---|---|
| 只信旧 Markdown 分布 | 数值可用但 total L5 易误读 | 未采用；回读 frames |
| 重跑 Winter RiskBuild | 会生成新 artifact，越界 | 未运行 |
| public exact-bundle restore | 12/12 identity/coverage + raw stats | 采用，只读 |
| raw scan 子代理并发 | 与 resolver 重复 | 发现后立即中止 |
| 把 missing 当 0 风险 | 违反 fail-closed | 拒绝 |
| 将 Summer replay 与 Winter candidates 混装 | identity 虚假 | 拒绝 |

## 9. Authoritative Run / C Route Impact（2026-08-23 19:19 +08:00）

本轮没有重新运行 B/C authoritative pipeline；检查的是现有正式 Winter artifacts。C input
commit 与 B commit 精确相同，145 frames、formal provenance、hard mask endpoint mapping PASS。

Full-voyage objective 对比：

| Metric | Fastest | Low risk | Delta low-risk vs fastest |
|---|---:|---:|---:|
| distance | 919.821 km | 927.024 km | +7.203 km / +0.783% |
| ETA duration | 53.366 h | 53.660 h | +0.294 h / +0.551% |
| average risk | 0.107079 | 0.102996 | -3.813% |
| maximum risk | 0.189369 | 0.150339 | -20.611% |
| integrated risk | 5.714365 | 5.526736 | -3.283% |
| expanded nodes | 13,774 | 26,775 | +94.388% |

12/12 route integrity 均 PASS，`data_unavailable_violations=0`。结论：C 收到的 finite risk
variation 足以产生可测的 objective tradeoff，并严格避开 hard unavailable；但没有 component
ablation，不能把 route difference 因果归属到某一个环境变量。

## 10. Performance Breakdown（2026-08-23 19:19 +08:00）

| Task | Before | This audit | Verdict |
|---|---:|---:|---|
| A exact restore | prior 199.801 s resolve | 215.702 s total / 216.75 s wrapper | observation |
| A process peak RSS | prior 1,024,908 KiB whole runner | 974,252 KiB read-only | observation |
| B tests | prior 53.22 s | 61.12 s pytest / 62.20 s wrapper | expected variance |
| C tests | prior 3.05 s | 2.97 s | PASS |
| D tests | prior 1.76 s | 1.70 s | PASS |

本轮保留 wall time 与 peak RSS 作为工程观测，不使用固定内存或运行时长上限作为
验收门槛。没有引入 dependency 或 benchmark harness。数据读取产生 page cache，但没有写回
frozen artifact。

## 11. Correctness / Validation（2026-08-23 19:19 +08:00）

| Check | Result | Classification |
|---|---|---|
| A exact frozen bundle restore/statistics | PASS；1,212 records | REAL_E2E_PASS |
| Winter RiskFrame schema/store/readback | inspected existing PASS | AUTHORITATIVE_PASS |
| B full pytest | 68 passed，1 failed，1 warning | PARTIAL |
| B failure | existing `allowed_region_has_no_grid_node` integration endpoint mapping | unrelated/open |
| B Ruff | PASS | UNIT_PASS |
| C full pytest / Ruff | 152 passed / PASS | UNIT_PASS |
| D full pytest / Ruff | 78 passed / PASS | UNIT_PASS |
| `node --check viewer/app.js` | PASS | UNIT_PASS |
| C route integrity | 12/12；hard/unavailable violations 0 | REAL_E2E_PASS |
| Current Viewer identity | Summer confirmed | ARTIFACT_AUDIT |
| Browser | NOT RUN；render code/artifact only audit | NOT RUN |

## 12. Determinism / Reproducibility（2026-08-23 19:19 +08:00）

状态：`INHERITED / NOT RUN`。本轮没有生成 RiskFrame/route/replay，也未进行 twin-run。
Bundle、RiskWindow、C artifact 和 Viewer SHA-256 均只读记录；A statistics 的 `generated_at`
和 wall/RSS 是允许变化的观测字段，不构成 artifact identity。

## 13. Artifacts / Provenance（2026-08-23 19:19 +08:00）

| Artifact | Identity / SHA-256 | Tracking |
|---|---|---|
| Winter DatasetBundle | `a-bundle-a2146...` / `e28bcca6...` | tracked frozen A artifact；unchanged |
| RunContext | `run-441b03...` / `bea471c7...` | tracked Orchestrator artifact；unchanged |
| ExecutionSpec | v1 / `b4360b76...` | tracked Orchestrator artifact；unchanged |
| Winter frame index | `bc19e22b...` | `.runtime` existing evidence |
| Winter distribution | `153d53a2...` | `.runtime` existing evidence |
| Winter C summary | `61e1e2b6...` | `.runtime` existing evidence |
| Winter candidates | `3f6ba8a5...` | `.runtime` existing evidence |
| Current Viewer bundle | `7a9111ee...` | D frozen Summer artifact；unchanged |
| A variable audit | `.runtime/risk-pipeline-audit/a-variable-statistics.json` | new read-only derived evidence；untracked |

## 14. Root Cause / Known Limitations / Corrections（2026-08-23 19:19 +08:00）

| Rank | Finding | Classification | Consequence |
|---|---|---|---|
| P0 | 当前 Viewer 使用 Summer，不是 Winter | CONFIRMED | 页面有限海域 100% L1 |
| P1 | Winter finite scores 在等宽阈值下 93.07% L1 | CONFIRMED | Winter 仍显得偏低，L4/L5 不出现 |
| P2 | B 是未标定 weighted-average baseline | CONFIRMED LIMITATION | 不能证明极端环境风险尺度科学有效 |
| P3 | Winter source footprint 有缺测 | CONFIRMED | 17.144% 以 DATA_UNAVAILABLE fail closed，不是低风险 |
| P4 | 当前 corridor/window 多数 finite cell 可能是开水或中等环境 | SUSPECTED | 缺 per-cell contributor，尚不能定量归因 |
| P5 | Viewer level/color mapping 错误 | NOT VERIFIED / EVIDENCE AGAINST | code/artifact mapping 一致 |

Unexpected correction：既有 total level 表把 NaN/hard 的保守占位 L5 计为 36.21%；这不是
finite high environmental risk。正确口径必须同时报告 finite-only level 与 hard reason。

Technical debt：

| ID | Severity | Limitation | Next action |
|---|---|---|---|
| RISK-AUDIT-01 | HIGH | 没有同 identity Winter combined Viewer | Orchestrator projection + D Browser E2E |
| RISK-AUDIT-02 | HIGH | B calibration=`demo_unvalidated` | 建立独立验证集与 calibration proposal |
| RISK-AUDIT-03 | MEDIUM | 无 per-cell component contribution | 先做 contract proposal，不直接扩 schema |
| RISK-AUDIT-04 | MEDIUM | wave/ice/current source footprint 不完整 | A source-footprint/target-grid spatial audit |
| RISK-AUDIT-05 | LOW | D 只显示 discrete level | 评估 research-only score legend，保持 hard 独立 |

## 15. Decision / Recommended Next Actions（2026-08-23 19:19 +08:00）

```text
RISK_VISUALIZATION_CONCERN = CONFIRMED
PRIMARY_ROOT_CAUSE = CURRENT_VIEWER_IS_SUMMER
WINTER_A_REQUIRED_TYPES = COMPLETE
WINTER_B_OUTPUT_CHANGE = OBSERVED
B_SCIENTIFIC_CALIBRATION = NOT_ESTABLISHED
C_RISK_SENSITIVITY = CONFIRMED
D_RENDERING_BUG = NOT_CONFIRMED
```

分层行动：

1. **Artifact/presentation（优先）**：由 Orchestrator 组装同一 Winter identity 的 RiskFrame、
   route candidates 与 simulation presentation bundle；D 只消费并做 Browser E2E。
2. **Data**：对 wave、ice、current、水位的 source footprint→target-grid missing spatial pattern
   做独立审计；不放宽 `DATA_UNAVAILABLE`。
3. **Model**：B owner 建立 calibration/threshold proposal，使用观测、专家标签或独立验证集评估
   11-component weights 与 equal-width bins；本报告不批准直接调权重。
4. **Explanation**：提出 backward-compatible explanation sidecar/contract proposal，发布 per-cell
   component contributions 和 uncertainty；不要让 D 重新计算。
5. **C**：当前不需要修 planner；保留 hard avoidance，并在解释 sidecar 可用后做 component
   ablation/route sensitivity research。
6. **D**：当前不需要改 color mapping；可在 Winter combined bundle 到位后评估 continuous score
   research overlay，但必须与 canonical level 和 hard layer并列。

明确不要做：不要把 Summer/Winter 混装、不要把 unknown 变低风险、不要为了比赛视觉直接降低
阈值或夸大颜色、不要在 Viewer 计算 risk contribution。
