---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - PLANNED
Document Role: SUPPORTING
Scope: Winter C validation and parallel C/D interface enablement milestone
Canonical/Supporting: Supporting final round report; canonical state is current/CURRENT_STATUS.md
Branch: research-validation-system
Last Verified: 2026-08-23
---

# Winter C Validation Final Report

## 1. Executive Summary（2026-08-23 10:20 +08:00）

| Claim | Before | After | Evidence | Verdict |
|---|---|---|---|---|
| Winter C consumer | NOT_STARTED | formal 145-frame intake | smoke artifact | PASS |
| Winter C planning | NOT_STARTED | 4 layers × 3 objectives | v3 JSON/GeoJSON | COMPLETED |
| Route integrity | unknown | 12/12 | exact C sampler audit | PASS |
| Summer/Winter decision | not tested | geometry/distance/ETA differ | frozen Summer route + Winter v3 | OBSERVED_CHANGE |
| Route candidates | NOT_PUBLISHED | real 12-route sidecar available | schema/projector | INTERFACE_PASS |
| D Winter Viewer | NOT_STARTED | metadata intake ready | D loader/test | NOT_IMPLEMENTED |

最终状态：

```text
B_WINTER_VALIDATION = COMPLETED / EXPERIMENTAL
C_WINTER_VALIDATION = COMPLETED / EXPERIMENTAL
C_TO_D_INTERFACE = STABLE
D_PARALLEL_DEVELOPMENT = READY
D_WINTER_VISUALIZATION = NOT_STARTED
```

## 2. Experiment Identity（2026-08-23 10:20 +08:00）

固定使用现有 A/B identity：bundle `a-bundle-a2146dd0adbaa7db77a6beb7`、run
`run-441b03c8-d45b-5414-b0e8-b7fd0d990c22`、RiskWindow commit
`risk-window-sha256-b5bed6bb48893e32620710e8c765dc60ec37a2fc384f0c49014b92f0a1c056b2`。
A bundle、RunContext、ExecutionSpec 与 B RiskFrame 内容均未改写。

## 3. B RiskFrame Input 与 C configuration（2026-08-23 10:20 +08:00）

- schema/provenance：`bc.risk-frame.v2` / formal；
- window/cadence：2026-02-15T00Z → 2026-02-21T00Z，145 hourly frames；
- grid：medium 31×11，341 cells；
- C：`time-dependent-a-star.v1`，默认 frozen objective weights，12 次独立 search；
- endpoint：`[5,7] → [26,2]`，218-node connected component；
- output：`cd.four-layer-route-plan-set.v3`，layer set
  `layer-set-sha256-4f70866a4a1532c21101a378c63e643563459da7864dd2b93c1d457b4c97d404`。

## 4. Route Results 与 Summer comparison（2026-08-23 10:20 +08:00）

Winter full-voyage recommended：921.379560 km、53.405581 h、avg risk 0.105651、
max risk 0.189369、integrated risk 5.642363 h。low-risk objective 以 7.203 km 与
0.294 h 的代价，把 avg/max risk 降至 0.102996/0.150339，证明三个 objective 不是
Viewer 伪造标签。

相对 Summer authoritative initial recommended，Winter 几何有 11/22 对应 waypoint
变化，距离 +11.658308 km、ETA +2.951089 h。Summer route-level risk metrics 没有发布，
因此只报告 `NOT_PUBLISHED`，不进行无来源数值比较。详见
[Winter C route validation](WINTER_C_ROUTE_VALIDATION_REPORT.md)。

## 5. Interface Changes（2026-08-23 10:20 +08:00）

Orchestrator 新增：

- formal committed-window C runner；
- `presentation.route-candidates.v1` schema，明确 `PUBLISHED` 12-route 与
  `NOT_PUBLISHED` empty 两个 fail-closed 分支；
- C v3 → presentation strict projector 和 canonical candidate-set identity；
- replay exporter 可选 sidecar 与 scenario mismatch rejection。

D 新增 canonical candidate risk metrics 与 selected identity 消费。未新增核心 contract
版本，也未把 presentation schema 移入 shared contracts；C owns route semantics，
Orchestrator owns projection，D owns rendering。

## 6. D Parallel Development Readiness（2026-08-23 10:20 +08:00）

D static loader 对真实 Winter v3 artifact 得到 4 layers / 12 plans；candidate sidecar
schema PASS，Viewer 在 sidecar 缺失时仍保持既有 single-route fallback。因此
`D_PARALLEL_DEVELOPMENT=READY`。但 candidate geometry map、Winter combined bundle 与
Browser E2E 未执行，`D_WINTER_VISUALIZATION` 仍为 `NOT_STARTED`。

## 7. Performance（2026-08-23 10:20 +08:00）

- C planner wall 390.894 s；wrapper 394.43 s；
- peak RSS 168,088 KiB；swap 0；约 1 CPU core；
- artifact 总量 281,006 bytes，其中 C JSON 104,081、GeoJSON 92,728、candidate sidecar
  68,339 bytes；
- 不宣称 benchmark，未做 C optimization、shared search 或 parallel worker 改造。

## 8. Validation（2026-08-23 10:20 +08:00）

| Repository / check | Result |
|---|---|
| Winter consumer smoke | PASS；3.05 s；136,424 KiB |
| C formal v3 run | PASS；12 routes；integrity 12/12 |
| C full pytest | 152 passed；3.05 s |
| C Ruff | PASS |
| B focused regression | 51 passed；5.59 s |
| B Ruff | PASS |
| Contracts full pytest | 19 passed；0.35 s |
| Contracts Ruff | PASS |
| Orchestrator fast pytest | 90 passed，2 deselected；2.39 s |
| Orchestrator Ruff | PASS |
| D full pytest | 64 passed；1.20 s |
| D Ruff / `node --check viewer/app.js` | PASS / PASS |

没有运行 A/B rebuild、full integration、replay、Firefox 或 determinism twin-run；这些不是
本轮 C/interface 门禁所需，也避免污染冻结输入与资源浪费。

## 9. Code / Artifact / Git（2026-08-23 10:20 +08:00）

- Orchestrator commit：`6888830 feat: validate winter routes and publish candidates`；
- D commit：`c8a9750 feat: consume winter route candidate metadata`；
- A/B/C/contracts：零代码修改；
- runtime artifacts 位于 `.runtime/experiments/winter-c-validation-20260823-medium/`，不纳入 Git；
- push/merge/rebase：未执行。

## 10. Known Issues 与 Next Steps（2026-08-23 10:20 +08:00）

1. B calibration 仍为 `demo_unvalidated`，结果是 research evidence，不是导航安全认证；
2. Summer route metrics publication 不完整，季节对照不是完全对称的 controlled experiment；
3. `DATA_UNAVAILABLE` 仍需 A/B variable-footprint follow-up，但 C 已 fail-closed 避开；
4. proposal v1 只表达一个 decision 的 candidate set；replay 多 decision sets 尚未设计；
5. 下一阶段由 D 生成 Winter combined presentation artifact、绘制候选并执行 Browser E2E；
6. C 可并行继续 profiling，但不得为展示修改本轮冻结 route artifacts。
