---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: GFS to CARRA transition and B intake assumptions
Canonical/Supporting: Supporting architecture audit
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Data Source Transition Audit

## 1. Executive Verdict（2026-08-22 21:56 +08:00）

```text
GFS_TO_CARRA_ADAPTER = IMPLEMENTED
A_CANONICAL_OUTPUT_COMPATIBILITY = VALIDATED_BY_BUNDLE_PARSE_AND_A_DOCTOR
B_WINTER_EXECUTION = NOT_RUN
SCIENTIFIC_COMPARABILITY = REQUIRES_WINTER_VALIDATION
```

CARRA 原始网格不会直接进入 B。A 将其转成 canonical rectilinear field，并通过
`DatasetBundle.v2` 发布；因此 B 不需要了解 CARRA projection，但必须继续验证变量、
单位、时间覆盖和 provenance。

## 2. A 侧迁移路径（2026-08-22 21:56 +08:00）

```text
C3S/ECMWF CARRA GRIB
  -> shortName / coordinate extraction
  -> longitude normalization
  -> curvilinear nearest-neighbour regrid (max 25 km)
  -> A canonical variable names and units
  -> immutable A archive records
  -> a.dataset-bundle.v2
```

当前 wind、temperature、visibility 的 49 个三小时快照覆盖冻结窗口
`2026-02-15T00Z` 至 `2026-02-21T00Z`。source issue evidence 使用 analysis cycle，
并保守标记 `authoritative=false` / `quality=suspect`，未把源身份包装为科学校准结论。

## 3. B 正式入口（2026-08-22 21:56 +08:00）

```text
B_ENTRYPOINT:
library: work_package_b/src/arctic_route_risk/service.py
class: RiskBuildService
method: build_window(RiskBuildRequest)
input: BInputEnvelope(PreparedWindow + DatasetBundle.v2 + matching RunContext.v2)
output: hourly bc.risk-frame.v2
publication: PersistentRiskStore
```

B package CLI 当前只暴露 model-intake；A→B→C 的正式命令入口位于 Orchestrator：

```text
arctic-route-orchestrator run \
  --execution-spec <path> \
  --bundle <winter-bundle.json> \
  --run-context <matching-run-context.json> \
  --a-data-root <A-root> \
  --b-config <explicit-model-config.json> \
  --c-config-root <C-config-root> \
  --contracts-config-root <contracts-config-root> \
  --risk-store-root <risk-store> \
  --output-dir <output>
```

代码链为 `arctic_route_orchestrator/service.py` 创建 `BInputEnvelope`，调用
`RiskBuildService.build_window`，随后把已提交 RiskFrame window 交给 C ingress。

## 4. B 隐含与显式假设（2026-08-22 21:56 +08:00）

| 假设 | 是否存在 | 对 CARRA 的影响 |
|---|---|---|
| 固定源网格 spacing/shape | 否 | B 会把 A canonical field 投影到显式 target grid |
| canonical 纬经轴单调、覆盖 target bbox | 是 | A 的 0.1° rectilinear 输出结构满足；未运行 B 验证 |
| 固定变量名 | 是 | 需 `wind_u10`、`wind_v10`、`air_temperature_2m`、`visibility` 等 |
| 固定单位 | 是 | wind m/s、temperature K、visibility m |
| 固定源时间步长 | 否 | 连续量可按时间插值；不得 stale extrapolation |
| B 输出时间步长 | 是 | formal MVP 固定为 60 min |
| 固定风险归一化范围 | 是 | wind 0–30 m/s、temperature 243.15–273.15 K、visibility 0–10000 m |
| unknown fail closed | 是 | 缺帧、越界、无效值不能降为低风险 |

## 5. Target Grid 与 Winter 配置缺口（2026-08-22 21:56 +08:00）

| Profile | Approx spacing | Tromsø grid |
|---|---|---|
| baseline / library default | 0.75° lat × 2.2° lon | 16×7 |
| medium | 0.375° lat × 1.25° lon | 31×11 |
| fine | 0.1875° lat × 0.625° lon | 60×21 |

Orchestrator 正式运行要求显式 `--b-config`。当前没有与 Winter bundle 匹配的
RunContext/execution spec，也没有已批准的 Winter B profile。为与既有 Tromsø 研究证据
比较，后续可评估 medium 配置，但本报告不把建议写成已选 production default。

## 6. 风险与下一门槛（2026-08-22 21:56 +08:00）

- CARRA 的更细源分辨率不会自动提高 B RiskFrame 分辨率；B target grid 才决定输出网格。
- 最近邻 regrid 可能保留边界阶跃，Winter 风险分布需要正式统计，不应预设“更高风险”。
- 固定归一化阈值对 GFS/CARRA 均一致，这保持公式不变，但不等于两个资料体系已校准等价。
- 缺少 matching RunContext 时，不能把仅有 DatasetBundle 写成正式 A→B handoff ready。

下一门槛是先生成并校验 matching RunContext/execution spec，再进行 focused B Winter
validation；本轮未运行 B。
