---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: Winter and Summer medium-grid RiskFrame distribution comparison
Canonical/Supporting: Supporting scientific/engineering evidence; current state is maintained in current/CURRENT_STATUS.md
Branch: research-validation-system
Last Verified: 2026-08-23
---

# Winter / Summer 风险分布审计

## 1. 审计问题与口径（2026-08-23 02:44 +08:00）

本审计回答：在不改变 B 公式、阈值、level policy 和 hard semantics 的前提下，Winter
输入是否产生了不同的 `bc.risk-frame.v2` 风险空间分布。

对照选择：

- Winter：本轮正式生成的 145 个 hourly frame，2026-02-15 00Z → 2026-02-21 00Z。
- Summer：已有冻结 Viewer 48h risk selection 的 49 个 hourly frame，2026-08-15 10Z →
  2026-08-17 10Z；来源为 `work_package_d/viewer/bundle.json` 与其声明的
  `work_package_a/data/output/rc2-smoke/causal-replay-mvp/sb-viewer-baseline-48h/risk-store/`。
- 两者实际使用相同的 realized `31×11` 坐标、相同 `grid_id=b-grid-c2bacc0bb86c70e5a59b14d4`
  和相同 `model_config_digest=0e317a76a8d902beded2694be75b34d01390f1d460b41d7b775fe57716a8b5ce`。
- 两个窗口长度不同，因此总 cell 数只用于校验，季节比较以百分比和有限 risk score 统计为主。

## 2. Risk Level Distribution（2026-08-23 02:44 +08:00）

| Level | Summer count | Summer % | Winter count | Winter % | Winter − Summer (pp) |
|---:|---:|---:|---:|---:|---:|
| L1 | 12,495 | 74.780059% | 29,357 | 59.373041% | -15.407018 |
| L2 | 0 | 0.000000% | 2,185 | 4.419051% | +4.419051 |
| L3 | 0 | 0.000000% | 1 | 0.002022% | +0.002022 |
| L4 | 0 | 0.000000% | 0 | 0.000000% | 0.000000 |
| L5 | 4,214 | 25.219941% | 17,902 | 36.205885% | +10.985944 |
| 合计 | 16,709 | 100% | 49,445 | 100% | — |

## 3. Spatial / Availability Statistics（2026-08-23 02:44 +08:00）

| 指标 | Summer | Winter |
|---|---:|---:|
| frame 数 | 49 | 145 |
| cells/frame | 341 | 341 |
| total cells | 16,709 | 49,445 |
| finite navigable cells | 12,495 | 31,543 |
| hard mask cells | 4,214（25.219941%） | 17,902（36.205885%） |
| unknown cells | 4,214 | 17,902 |
| unknown navigable nodes | 0 | 0 |
| `LAND` | 3,185（19.062%） | 9,425（19.062%） |
| `DATA_UNAVAILABLE` | 1,029（6.158%） | 8,477（17.144%） |
| `OTHER` / `ICE` | 0 | 0 |
| `NONE` | 12,495 | 31,543 |
| hard/reason consistency mismatch | 0 | 0 |

本轮实际输出的 canonical hard reasons 只有 `LAND`、`DATA_UNAVAILABLE`、`NONE`，没有
独立的 `ICE` hard reason。冰相关变量参与风险分量，但不能把它们事后改名为 hard reason。

## 4. 有限风险分数（2026-08-23 02:44 +08:00）

| 指标 | Summer | Winter | 变化 |
|---|---:|---:|---:|
| finite min | 0.014691139 | 0.035493027 | +0.020801888 |
| finite mean | 0.045027961 | 0.119015786 | +0.073987825（2.643153×） |
| finite max | 0.162555397 | 0.400563359 | +0.238007963 |

## 5. 对 `DATA_UNAVAILABLE` 和输入缺测的解释（2026-08-23 02:44 +08:00）

Winter 的 `DATA_UNAVAILABLE` 比例比 Summer 高 10.985944 个百分点；这部分必须与
有限风险均值上升分开解释，不能直接当作“冬季环境更危险”。本轮 Winter RiskFrame 的
payload attributes 保留了逐变量缺测诊断；145 个 frame 累计非有限网格数包括：

| 输入变量 | 累计非有限 cell 数 |
|---|---:|
| `significant_wave_height` | 17,322 |
| `ice_concentration` / `ice_drift_u` / `ice_drift_v` / `ice_thickness` | 各 12,180 |
| `ice_edge` / `ice_type` | 各 11,600 |
| `ocean_current_u` / `ocean_current_v` / `sea_surface_height` | 各 12,180 |
| `air_temperature_2m` / `visibility` / `wind_u10` / `wind_v10` | 0 |

这些诊断证明 Winter hard/unavailable 区域确实存在输入支持问题；B 没有把 unknown 转成
绿色或 Level 1。`unknown_navigable_nodes=0` 且 hard/reason 一致性为 0 mismatch，满足
当前 B→C unknown fail-closed 的前置观测条件，但本轮没有运行 C，因此不构成 C 验证。

## 6. 环境解释与科学边界（2026-08-23 02:44 +08:00）

本轮可以确认的事实：

1. 在相同 medium realized grid、相同 hourly cadence 和相同 B model configuration 下，
   Winter 输出的有限风险分布发生了显著变化：L2/L3 出现，L1 减少，有限 risk mean 和
   max 均上升。
2. `LAND` 比例在两个窗口保持相同，说明本次 hard mask 总量增加主要由
   `DATA_UNAVAILABLE` 增加而不是静态 land mask 变化。
3. Winter 12 类 A 数据、CARRA/Copernicus 来源和 Summer 来源体系不同；因此不能仅凭此
   一次对照把变化因果归结为“月份”或某一个单独环境变量。

科学状态：

```text
WINTER_ENVIRONMENT_TO_RISK_DISTRIBUTION_CHANGE = OBSERVED
SCIENTIFIC_CALIBRATION = NOT_ESTABLISHED
CAUSAL_ATTRIBUTION_TO_WINTER_ONLY = NOT_ESTABLISHED
```

本轮目标“先证明风险分布变化，再进入航路验证”已达到工程/研究第一门槛；下一步应在保留
同一统计口径的前提下做变量贡献、数据支持敏感性和 C Winter consumer smoke。
