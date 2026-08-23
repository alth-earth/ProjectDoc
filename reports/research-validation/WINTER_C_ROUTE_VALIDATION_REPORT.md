---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: first formal Winter C four-layer route validation and Summer comparison
Canonical/Supporting: Supporting scientific/engineering evidence; canonical state is current/reference/WINTER_SCENARIO_STATUS.md
Branch: research-validation-system
Last Verified: 2026-08-23
---

# Winter C Route Validation 报告

## 1. Scientific verdict（2026-08-23 10:20 +08:00）

```text
C_WINTER_VALIDATION = COMPLETED
WINTER_ROUTE_PLAN_SET = cd.four-layer-route-plan-set.v3
ROUTES = 4 LAYERS x 3 OBJECTIVES = 12
ROUTE_INTEGRITY = PASS / 12_OF_12
WINTER_ROUTE_DECISION_CHANGE_VS_SUMMER = OBSERVED
```

Winter medium RiskFrame 使 recommended route 相对 Summer 48h 权威初始推荐线发生真实几何
变化：两者均为 22 waypoint，但 11 个对应 waypoint 坐标不同。Winter recommended
提前向西转向，距离增加 11.658 km，ETA 增加 2.951 h。该观察证明当前实验链中路线决策
发生变化；由于 Summer/Winter 数据源与实验时间不同，不能宣称已隔离季节因果。

## 2. C configuration（2026-08-23 10:20 +08:00）

- grid：B committed medium 31×11；C 不重采样、不变更网格；
- planner：`time-dependent-a-star.v1`，8-connectivity；
- objectives：`fastest`、`low_risk`、`recommended`；
- layers：`full_voyage`、`main_corridor_24_72h`、`rolling_0_24h`、
  `executable_0_6h`；
- maximum elapsed：144 h；generation/input revision：0/0；
- risk source：145-frame formal committed window；unknown/hard fail closed。

## 3. Route metrics（2026-08-23 10:20 +08:00）

| Layer | Objective | Success | Destination | Distance km | ETA h | Avg risk | Max risk | Integrated risk h | Expanded |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| full_voyage | fastest | PASS | YES | 919.821 | 53.366 | 0.107079 | 0.189369 | 5.714365 | 13,774 |
| full_voyage | low_risk | PASS | YES | 927.024 | 53.660 | 0.102996 | 0.150339 | 5.526736 | 26,775 |
| full_voyage | recommended | PASS | YES | 921.380 | 53.406 | 0.105651 | 0.189369 | 5.642363 | 18,346 |
| main_corridor_24_72h | fastest | PASS | YES | 919.821 | 53.366 | 0.107079 | 0.189369 | 5.714365 | 13,774 |
| main_corridor_24_72h | low_risk | PASS | YES | 927.024 | 53.660 | 0.102996 | 0.150339 | 5.526736 | 26,775 |
| main_corridor_24_72h | recommended | PASS | YES | 921.380 | 53.406 | 0.105651 | 0.189369 | 5.642363 | 18,346 |
| rolling_0_24h | fastest | PASS | NO | 397.438 | 22.962 | 0.096482 | 0.189369 | 2.215446 | 670 |
| rolling_0_24h | low_risk | PASS | NO | 402.055 | 23.183 | 0.090772 | 0.143020 | 2.104357 | 1,977 |
| rolling_0_24h | recommended | PASS | NO | 397.438 | 22.962 | 0.096482 | 0.189369 | 2.215446 | 980 |
| executable_0_6h | fastest | PASS | NO | 81.543 | 4.935 | 0.143772 | 0.189369 | 0.709451 | 3 |
| executable_0_6h | low_risk | PASS | NO | 81.543 | 4.935 | 0.143772 | 0.189369 | 0.709451 | 7 |
| executable_0_6h | recommended | PASS | NO | 81.543 | 4.935 | 0.143772 | 0.189369 | 0.709451 | 3 |

下层 `Destination=NO` 是正式关注窗口锚点语义，不是路线失败；12 条路线均达到各自
`layer_goal`。所有路线 `hard_constraint_violations=0`，minimum confidence 均为
`0.675000012`。

## 4. Summer / Winter comparison（2026-08-23 10:20 +08:00）

| Recommended metric | Summer authoritative initial | Winter formal v3 | Delta |
|---|---:|---:|---:|
| Route success | PASS | PASS | — |
| Waypoints | 22 | 22 | 0 |
| Distance km | 909.721253 | 921.379560 | +11.658308 |
| ETA hours | 50.454492 | 53.405581 | +2.951089 |
| Average risk | NOT_PUBLISHED | 0.105651 | 不作伪造比较 |
| Maximum risk | NOT_PUBLISHED | 0.189369 | 不作伪造比较 |
| Integrated risk hours | NOT_PUBLISHED | 5.642363 | 不作伪造比较 |
| Geometry equality | false | false | 11/22 对应点不同 |

Summer 证据来自已冻结且 browser-validated 的 `sb-viewer-baseline-48h` 初始 authoritative
route。该 Viewer bundle 没有发布 route-level risk metrics；本报告不从风险图层反推或
补造这些字段。比较是有来源差异的观察性 evidence，不是严格控制变量实验。

## 5. Artifacts 与完整性（2026-08-23 10:20 +08:00）

输出根：`/root/my_project/.runtime/experiments/winter-c-validation-20260823-medium/`。

| Artifact | SHA-256 | Result |
|---|---|---|
| `winter-four-layer-route-plan-set-v3.json` | `4353d8e4412da512b987ccd37ee5002da1e727a1487707c538f0ba10ef4032a4` | schema + codec PASS |
| `winter-four-layer-route-plan-set-v3.geojson` | `f20ff925547a6c0d9c2ddd3b073fd989ab9f552335455d434b3c295edd27fbea` | 12-route export PASS |
| `route-integrity.json` | `80bc619b47f1e6a068862ea736bd8cb6eb8e9906ddd1e61aa444f2b9d0fde03b` | 12/12 PASS |
| `validation-summary.json` | `61e1e2b6ebfb30c9243d226c3403bd6577b0f3aca4681454deb612641f8cea15` | PASS |

## 6. Performance（2026-08-23 10:20 +08:00）

| 观测 | 值 |
|---|---:|
| Planner wall | 390.894 s |
| Wrapper wall | 394.43 s（6:34.43） |
| Peak RSS | 168,088 KiB |
| CPU | 约 1 core / 100% |
| Swap | 0 |
| Routes | 12 |

这是单次工程观测，不是统计 benchmark。12 个 objective/layer search 仍为独立 A*；本轮
没有修改或优化搜索逻辑。
