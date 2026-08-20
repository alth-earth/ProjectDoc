# Grid Presentation Audit

## 网格展示审计（2026-08-21 01:06 +08:00）

## 结论

当前 Viewer 中风险网格和 hard layer 看起来粗，主要瓶颈是 **B 的 RiskFrame target grid policy**，不是 A 的原始 GEBCO 数据，也不是 D 的地理坐标变换错误。

D 当前使用同一份 `bc.risk-frame.v2` 坐标和同一份 `hard_reason` 数组绘制 cell；C 也从这份 RiskFrame 构造 `RegularGrid`，因此风险网格、规划 waypoint 和 Viewer route 的粗粒度是一致的。这是一个真实的 presentation 观感问题，但不是 D 擅自改变语义的问题。

## 1. Viewer 当前使用的风险 cell 来源

当前真实 artifact：

```text
/root/my_project/work_package_a/data/output/rc2-smoke/causal-replay-mvp/
  sb-viewer-baseline-12h-det/risk-store/frames/risk-sha256-*.json
```

导出链路：

```text
B PersistentRiskStore
  bc.risk-frame.v2
    -> arctic_route_orchestrator/scripts/replay_viewer_export.py
    -> presentation.risk-overlay.v1
    -> work_package_d/viewer/bundle.json
    -> D Canvas renderer
```

Viewer 没有读取 A 的 raw weather/NetCDF，也没有重新计算 B risk。每个风险 cell 使用导出 frame 中的：

```text
coordinates.latitude
coordinates.longitude
risk_level
hard_reason
```

`risk_level` 和 `hard_reason` 没有被 D 插值或重新分类。

## 2. 实际风险 frame 几何

从当前 `sb-viewer-baseline-12h-det` 的 13 个 formal frames 抽样检查，空间形状一致：

| 项目 | 实际值 |
| --- | ---: |
| rows | 31 |
| cols | 11 |
| cells/frame | 341 |
| latitude centers | 68.5° … 79.5° |
| longitude centers | 10.0° … 22.0° |
| latitude step | 0.3666666667° |
| longitude step | 1.2° |
| valid times | 2026-08-15 10:00Z … 2026-08-15 22:00Z |
| cadence | 3600 s |

按球面近似换算，cell 尺寸随纬度变化：

| 纬度 | 南北尺寸 | 东西尺寸 |
| ---: | ---: | ---: |
| 68.5° | ≈40.8 km | ≈49.0 km |
| 74.0° | ≈40.8 km | ≈36.8 km |
| 79.5° | ≈40.8 km | ≈24.3 km |

该 frame 的 payload attributes 仍明确记录 B grid identity：

```text
grid_id = b-grid-c2bacc0bb86c70e5a59b14d4
hard_mask_policy = land_sea_mask_plus_unknown_ice_free_v1
```

## 3. 与 A / GEBCO basemap 的比较

当前 GEBCO-derived `land_sea_mask` 文件为：

```text
/root/my_project/work_package_a/data/raw/tromso_to_isfjorden_outer/
  land_sea_mask/163a3f67b391a1d90ac83cad/
  land_sea_mask_tromso_to_isfjorden_outer_valid_20260423T000000Z_
  issued_20260423T000000Z_gebco-2026-d5a7e2fe3915-7baad866_3640a87b2f5a2d15.nc
```

其实际坐标约为：

```text
222 latitude points × 242 longitude points
resolution = 0.05° × 0.05°
```

Viewer basemap 是 1024×1024 的 EPSG:4326 presentation raster，bbox 约为：

```text
longitude 9.9729167° … 22.0729167°
latitude  68.4729167° … 79.5729167°
```

因此，A/GEBCO 的源分辨率显著细于 B RiskFrame。D 只是把 31×11 的 formal cell 按 canonical bbox 映射到 1024×1024 canvas；D 没有把 0.05° basemap 降采样成 0.3667°×1.2°。

## 4. 与 C route geometry 的比较

当前 active route revision 1 有 22 个 waypoints，其他真实 revisions 为 20、19、18、17 个 waypoints。waypoint 的经纬度增量也反复出现：

```text
latitude  ≈ 0.3666666667°
longitude ≈ 1.2°
```

这与 RiskFrame 的中心坐标完全一致。C 的 `RegularGrid.from_risk_frame()` 直接从 RiskFrame 坐标建立规划 grid，故 route waypoint 粗并非 D 把一条细路线错误地折成少数点；它是当前 C planning grid 的 authoritative geometry。

## 5. Hard layer 分辨率和语义

Hard layer 与 risk layer 使用同一 frame cell index：

```text
hard_reasons[index]
risk_levels[index]
```

当前抽样 frame 的统计为：

```text
NONE             255 cells
LAND              65 cells
DATA_UNAVAILABLE  21 cells
```

因此 hard 边界粗，首先是 B frame/grid 粒度的结果；它不是 D 将 hard mask 错误平滑的结果。D 不能把 `LAND` 或 `DATA_UNAVAILABLE` 变成细化后看似安全的海域。

## 6. 根因归属

| 层 | 证据 | 判断 |
| --- | --- | --- |
| A | GEBCO land mask 为约 0.05°×0.05° | 不是主要瓶颈；A 源数据更细 |
| B | `demo_unvalidated_smoke_grid_v3.json` 使用 0.375° / 1.25° policy；cover-bbox realization 得到 0.3667° / 1.2°、31×11 | **主要根因** |
| C | `RegularGrid.from_risk_frame()` 使用 B frame 坐标；waypoints 对齐同一 grid | **继承并暴露 B 粒度** |
| D | 使用 canonical bbox，将 formal cells 逐格绘制；无 risk/hard 重算或空间插值 | 不是数据根因；存在 presentation 可读性优化空间 |

## 7. 短期 Demo 优化方案

本轮保持 authoritative semantics 不变，建议只做以下安全优化：

1. Presentation Mode 使用更低 alpha、无内部 cell 边框的风险填充，让底图和路线视觉层次更清楚。
2. Engineering Debug Mode 保留精确 cell 边界、原始 hard reason 和调试字段，便于核验。
3. Risk 与 hard 继续分层：不做 bilinear/nearest 的视觉插值，不把 unavailable 或 land 平滑成安全色。
4. Route 仅做 display-side 的逐段 densification/round join；不改 `bundle.routes`、ETA、ship position 或 C route semantics。
5. 如果未来需要真正细化风险边界，应在 B 的版本化 target-grid policy / presentation artifact 层重新生成 formal 或明确的展示数据，并重新做 contract、integrity、性能和 determinism 评估；不能在 D 中偷偷放大或插值成新的风险含义。

## 8. 本轮边界

本审计没有修改 A/B/C 核心算法、数据采集、RiskFrame 数值、hard reason、规划 grid、authoritative route 或 replay artifact。后续改动仅限 D presentation rendering，以及必要的 Orchestrator presentation metadata；不会改变 causal replay 或 frozen baseline。
