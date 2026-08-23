---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: Winter committed RiskFrame 到 C formal ingress 的 consumer smoke
Canonical/Supporting: Supporting evidence; canonical Winter state is current/reference/WINTER_SCENARIO_STATUS.md
Branch: research-validation-system
Last Verified: 2026-08-23
---

# Winter C Consumer Smoke 报告

## 1. 结论（2026-08-23 10:20 +08:00）

```text
WINTER_C_CONSUMER_SMOKE = PASS
ALLOWED_REGION_GRID_GATE = PASS
B_ARTIFACT_MUTATION = NO
C_PLANNER_EXECUTED_IN_SMOKE = NO
```

Smoke 只执行 committed-window readback、identity、formal provenance、hourly coverage、
endpoint mapping 与 `RiskSourcePlanningIngress.prepare()`。随后正式 C run 另行执行。

## 2. 输入身份（2026-08-23 10:20 +08:00）

| 字段 | 值 |
|---|---|
| Scenario | `tromso_isfjorden_february_2026_research_v1` |
| Run | `run-441b03c8-d45b-5414-b0e8-b7fd0d990c22` |
| B schema | `bc.risk-frame.v2` |
| Commit | `risk-window-sha256-b5bed6bb48893e32620710e8c765dc60ec37a2fc384f0c49014b92f0a1c056b2` |
| Window | `2026-02-15T00Z` → `2026-02-21T00Z` |
| Cadence / count | 3600 s / 145 frames |
| Provenance | `formal` |
| Grid | medium，31×11 |

## 3. Endpoint gate（2026-08-23 10:20 +08:00）

| 项目 | Start | Goal |
|---|---|---|
| Requested lon/lat | 18.0 / 70.5 | 13.0 / 78.15 |
| Resolved lon/lat | 18.4 / 70.333333 | 12.4 / 78.033333 |
| Node | `[5, 7]` | `[26, 2]` |
| Adjustment | 23.784 km | 18.916 km |

两点均位于 allowed region、首帧非 hard，并处于同一 218-node 可航连通分量。
因此既有 Murmansk default-grid 用例中的 `allowed_region_has_no_grid_node` 不影响本次
Tromsø Winter medium grid；C fail-closed endpoint 语义无需修改。

## 4. Evidence（2026-08-23 10:20 +08:00）

- runtime：`/root/my_project/.runtime/experiments/winter-c-validation-20260823-medium/consumer-smoke.json`；
- SHA-256：`85b88e6a0e328780839260518b2988097570dde0288839d482d8ce1a271e8e7e`；
- log：`/root/my_project/.runtime/test-logs/winter-c-consumer-smoke.log`；
- wall：3.05 s；max RSS：136,424 KiB；swap：0。
