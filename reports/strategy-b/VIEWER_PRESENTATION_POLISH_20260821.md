# Viewer Presentation Polish Round

## Viewer Presentation Polish（2026-08-21 01:20 +08:00）

## 1. Key Delta

| Claim | Before | After | Evidence | Verdict |
| --- | --- | --- | --- | --- |
| Coarse grid root cause | NOT_CLASSIFIED | B target-grid realization identified | real frame inspection + grid audit | AUDITED |
| Risk presentation | Exact cells with fractional seams | Exact cells, pixel-aligned fills, softer Presentation palette | Firefox screenshots | BROWSER_E2E_PASS |
| Hard layer | Separate hard cells | Explicit LAND / DATA_UNAVAILABLE / OTHER legend | Firefox + unchanged arrays | BROWSER_E2E_PASS |
| Route presentation | Authoritative waypoint polyline | Display-only collinear densification + round joins | D source + browser | IMPLEMENTED |
| Vessel marker | White dot | Top-down ship icon with segment-bearing rotation | Firefox + exposed heading state | BROWSER_E2E_PASS |
| Viewer mode | Presentation/Debug toggle | Presentation default retained; Debug retains grid/diagnostics | Firefox mode toggle | BROWSER_E2E_PASS |
| Authoritative semantics | PASS | PASS | no replay/backend changes | PRESERVED |

## 2. Scope and non-goals

本轮只改 Viewer presentation rendering、presentation metadata 和相关文档。
没有修改 A/B/C 算法、数据采集、RiskFrame 数值、hard reason、C planning
grid、ETA、物理船位、replan adoption、causal replay 或 determinism artifact。
没有运行新的 replay。root ProjectDoc Git 未修改，PUSH 未执行。

## 3. Grid Presentation Audit

真实 `sb-viewer-baseline-12h-det` 有 13 个 formal `bc.risk-frame.v2` frames，
每个 frame 为 31×11 = 341 cells：

```text
latitude:  68.5° … 79.5°, step ≈ 0.3666666667°
longitude: 10.0° … 22.0°, step = 1.2°
```

约为南北 40.8 km；东西尺寸随纬度从约 49.0 km 降至 24.3 km。A/GEBCO
land mask 约为 0.05°×0.05°（222×242 points），显著细于风险 frame。

B 的 `demo_unvalidated_smoke_grid_v3.json` 声明 0.375° / 1.25° policy，
endpoint-cover realization 在当前 corridor bbox 上得到 0.3667° / 1.2°。
C 从同一 RiskFrame 构造 `RegularGrid`，route waypoint 也匹配这组增量。
D 只是用 canonical EPSG:4326 bbox 忠实绘制这些 cells。

结论：

```text
主要瓶颈 = B target-grid policy / realization
继承影响 = C planning waypoint grid
展示问题 = D fractional Canvas bounds 使网格接缝更明显
```

详细证据见
`[GRID_PRESENTATION_AUDIT_20260821.md](GRID_PRESENTATION_AUDIT_20260821.md)`。

## 4. Presentation implementation

### Risk / Hard

- Presentation Mode 使用较柔和的 level 1–5 颜色和较低 alpha。
- 风险 cell 按 level 分组并进行 pixel-align；没有空间插值或语义重分类。
- Engineering Debug 保留逐 cell outline。
- `LAND`、`DATA_UNAVAILABLE`、`OTHER` 仍是独立 hard reason；unknown 不会
  变成 low-risk/safe。
- 两种模式消费同一 bundle arrays。

### Route

`densifyPoints()` 只在现有 authoritative segment 上添加线性、共线点，配合
round join 改善抗锯齿。它不改变 route waypoints、ETA、ship position、active /
pending / superseded 状态、completed track 或 land/hard validation。

### Ship

白点替换为带轮廓和 cabin 的小型俯视船图标。中心位置不变；heading 来自
active authoritative route segment bearing，不来自像素速度或独立 UI timer。
当前 12h artifact 的可见 segment 都是北向，因此浏览器实际观察到 heading=0°；
rotation path 已由 segment bearing 驱动。

## 5. Real Firefox Browser E2E

```text
Firefox via Playwright CLI
http://127.0.0.1:8131/
```

| Check | Result |
| --- | --- |
| page / GEBCO / route / completed track / risk / hard | PASS |
| Presentation default / Engineering Debug toggle | PASS |
| 10:00 / 10:30 / 11:00 ship samples | PASS; latitude 70.3333 / 70.4135 / 70.4938 |
| Play movement | PASS; 300ms smoke changed latitude by ≈0.00080° |
| Pause / scrub / speed controls | PASS |
| 10:30 +6h | PASS; requested 16:30, selected 16:00, actual +5h30m |
| 10:30 +24h | PASS; explicit UNAVAILABLE, no stale fallback |
| 13:30 replan | PASS; active R1, pending R2 |
| 15:00 replan | PASS; active R2, pending R3 |
| layer toggles | PASS |
| console errors / warnings | 0 / 0 |
| required static requests | PASS; all observed HTTP 200 |

Proof images are outside Git under `/root/my_project/.runtime/viewer-proof/`,
including current, +6h, unavailable +24h, pending, adopted, Presentation Mode,
and Engineering Debug captures.

## 6. Performance and elapsed-time analysis

这是 engineering observation，不是 professional benchmark；本轮没有跑 heavy
replay 或 full integration wall-time rerun。

### Viewer/browser

| Metric | Before / baseline | After | Interpretation |
| --- | ---: | ---: | --- |
| bundle.json | 1,435,325 B | 1,435,891 B | ≈566 B presentation metadata growth |
| app.js | 17,682 B | 22,568 B | +4,886 B for display/icon/heading helpers |
| style.css | 4,023 B | 4,563 B | +540 B for polish/legend styling |
| first Firefox DOMContentLoaded | ≈174 ms | ≈176 ms | effectively unchanged |
| first Firefox load | ≈180 ms | ≈181 ms | no visible load regression |
| warmed reload | — | ≈28 ms | cache-dependent, not primary benchmark |
| resource timing | — | bundle ≈1,435,891 B; app.js ≈22,568 B; CSS ≈4,563 B; basemap ≈13,938 B encoded | remains lightweight |
| horizon switch / scrub | responsive baseline | responsive | no UI freeze observed |

Risk rendering仍只处理已有 341 presentation cells，不读取 raw NetCDF、不重算 B。
按 level 分组填充消除 seam，计算规模仍受现有 presentation payload 限制。

### Replay/integration wall time (separate from Viewer load)

```text
latest-head authoritative 12h replay / semantic-determinism baseline:
  ≈2044.9 s ≈34.1 min, inherited; not rerun
previous full integration suite:
  ≈2495.25 s ≈41:35
recent product-round integration suite:
  ≈2334.71 s ≈38:54, inherited; not rerun here
```

本轮 export-only regeneration 为 `preflight=PASS / L2=PASS / timeline=721`。

## 7. Tests and validation levels

```text
D pytest                         54 passed
D ruff                           clean
D node --check viewer/app.js     PASS
Orchestrator focused export      5 passed
Orchestrator fast suite          78 passed, 2 deselected
Orchestrator ruff                clean
Firefox Browser E2E              PASS
12h determinism twin-run         INHERITED, not rerun
```

## 8. Git and frozen-baseline impact

```text
D             feat: viewer presentation polish
Orchestrator  feat: presentation route/export improvements
Governance    docs: record viewer presentation polish
PUSH          NOT PERFORMED
```

Frozen `main` / `rc2-development` history and artifacts are not modified. All
active changes are presentation code, export metadata, tests, and docs.

## 9. Unexpected findings

1. Coarse grid is principally B output, not A/GEBCO resolution and not a D
   coordinate-transform defect.
2. Correct fractional Canvas geometry still produced visible translucent seams;
   grouped, pixel-aligned fills removed this presentation artifact.
3. The visible 12h route is northbound, so heading evidence is 0°; a non-zero
   heading needs a longer-window demo rehearsal, not a semantic fix.
4. Same-tick 15:00 ordering remains correctly represented as active R2/pending R3.

## 10. Next step

The Viewer is now at Demo Presentation Viewer foundation. Next is demo rehearsal
and operator runbook validation, followed by human-reviewed Demo Freeze. Rich
route-transition animation remains optional and must stay non-semantic.
