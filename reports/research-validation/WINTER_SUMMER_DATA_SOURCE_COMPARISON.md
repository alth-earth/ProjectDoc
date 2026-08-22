---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: Summer and Winter A source comparison
Canonical/Supporting: Supporting data-source audit
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Winter / Summer Data Source Comparison

## 1. 比较范围（2026-08-22 21:56 +08:00）

Summer 基准为 `tromso_isfjorden_august_2026_demo_v1.bundle.json`；Winter 基准为
`tromso_to_isfjorden_outer_winter_20260215T000000Z_bundle.json`。表中分辨率区分源产品
分辨率与 A 发布后的 canonical 网格，避免把下载产品分辨率误写为 B/C 网格。

## 2. 数据源矩阵（2026-08-22 21:56 +08:00）

| Variable | Summer Source | Winter Source | Resolution / A output | Temporal Resolution | Unit | Risk |
|---|---|---|---|---|---|---|
| wind | NOAA GFS 0.25° | C3S/ECMWF CARRA East domain | 2.5 km curvilinear → A 0.1° rectilinear | 3 h | m/s | source/grid/projection changed |
| temperature | NOAA GFS 0.25° | C3S/ECMWF CARRA East domain | 2.5 km curvilinear → A 0.1° rectilinear | 3 h | K | source/grid/projection changed |
| visibility | NOAA GFS 0.25° | C3S/ECMWF CARRA East domain | 2.5 km curvilinear → A 0.1° rectilinear | 3 h | m | source/grid/projection changed |
| wave | Copernicus global wave | same Copernicus product family | 0.0833° rectilinear | 3 h | m / degree / s | snapshot changed only |
| current | Copernicus Arctic PHY detided fallback | same Copernicus product family | source ~6 km; A sample about 0.0625°×0.08° | 1 h | m/s | detided, not total/tidal current |
| ice concentration | Copernicus Arctic PHY | same product family | source ~6 km; A sample about 177×152 | 1 h | 1 | snapshot changed only |
| ice drift | Copernicus Arctic PHY | same product family | source ~6 km; A sample about 177×152 | 1 h | m/s | snapshot changed only |
| ice thickness | Copernicus Arctic PHY | same product family | source ~6 km; A sample about 177×152 | 1 h | m | snapshot changed only |
| ice type | Copernicus/neXtSIM-derived | same product family | A sample about 369×402, ~0.03° | 1 h | 1 | categorical handling required |
| ice edge | Copernicus/neXtSIM-derived | same product family | A sample about 369×402, ~0.03° | 1 h | 1 | categorical handling required |
| water level | Copernicus Arctic PHY | same product family | source ~6 km; A sample about 177×152 | 1 h | m | snapshot changed only |
| land mask | GEBCO 2026 / CEDA | same static mask | A-normalized about 0.05° | static | 1 | `1=sea`, `0=land_or_coast` |

## 3. CARRA 替换 GFS 的变化（2026-08-22 21:56 +08:00）

- **分辨率**：GFS 0.25° 规则网格变为 CARRA 2.5 km 投影/曲线网格；A 先最近邻投影到
  0.1° 规则经纬网格后发布。
- **时间步长**：两者在当前 A 记录中均以 3 小时 cadence 发布，没有把 6 小时记录
  静默冒充 3 小时。
- **坐标**：CARRA 经度在适配器中统一到 `[-180, 180]`，再按 canonical 纬经轴发布。
- **单位**：A 输出仍为 B 所需的 `wind m/s`、`temperature K`、`visibility m`。
- **预处理**：CARRA 增加 GRIB shortName 解析、曲线/投影网格识别以及最大 25 km 的
  nearest regrid；B 不接触原始 CARRA GRIB。
- **覆盖范围**：当前 CARRA 获取脚本使用 `lon 10–30 / lat 68–80`，大于 scenario config
  的 `lon 10–22 / lat 68.5–79.5`。覆盖充分，但范围未由场景配置驱动。

## 4. 比较结论（2026-08-22 21:56 +08:00）

CARRA 迁移不改变 A→B canonical 变量名和单位，结构上可进入 B；它会改变空间采样、
资料同化体系与局部数值分布，因此 Winter 与 Summer 风险分布不可被视为只改变月份的
同源对照。该差异必须在 B Winter Validation 中作为科学可比性变量记录，而不能由
Viewer 或 B 公式做隐式补偿。
