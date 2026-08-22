---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: B-to-C formal risk interface freeze audit
Canonical/Supporting: Supporting evidence for the contract ownership registry
Branch: research-validation-system
Last Verified: 2026-08-23
---

# C 接口冻结审计

## 1. 审计结论（2026-08-23 01:16 +08:00）

```text
B→C transport = bc.risk-frame.v2
C intake unit = committed exact hourly RiskFrame window
VERDICT = STABLE_WITH_CONDITIONAL_UNKNOWN_GATE
```

C 不直接读取 A bundle，也不接受浏览器重算数据。正式入口从 B committed source 取得完整
hourly RiskFrame window，验证 run/config/generation/time/provenance identity 后才构造
`RiskSampler`。

## 2. Grid 与时间 ownership（2026-08-23 01:16 +08:00）

B producer 决定 formal rectilinear target grid 并发布 latitude/longitude；C consumer 根据同一
坐标构造 `RegularGrid`，不得在 ingress 中暗改 resolution。Adaptive/non-uniform grid 不属于
当前 v2 兼容边界。

C 要求完整闭区间逐小时 cadence、严格排序、无重复和无时间外推。空间 risk sampling 使用
双线性插值，时间使用线性插值；hard/confidence/speed factor 采用保守组合。这些是 C consumer
语义，不授权 C 重算 B risk。

## 3. Unknown 与 Hard Reason（2026-08-23 01:16 +08:00）

正式语义保持：

```text
unknown != safe
hard_mask=false -> hard_reason=NONE
hard_mask=true  -> hard_reason in LAND/DATA_UNAVAILABLE/OTHER
```

C 在可航点遇到 unknown risk 且 `hard_mask=false` 时 fail closed。当前 B 可配置 policy 中存在
产生 `risk_score=unknown, confidence=0, hard_mask=false` 的可能，因此这是 Winter B→C 的
conditional gate：必须由 B validation 给出实际分布证据或批准 fail-closed hard policy；不能由
C/D 临时填值。

## 4. Provenance 与 publication（2026-08-23 01:16 +08:00）

正式 frame 的 `provenance=formal`，source summary 保留 source/data ID、issue/valid time、
version、quality、checksum。C 校验 canonical `risk_id`、run/scenario/corridor/vessel/config/
generation identity，并通过 committed-window protocol 原子消费；散帧不构成正式 C input。

`hard_reason` 当前进入 RiskFrame codec，但 C 的 `SampledRisk` 主要保留 hard mask，不继续传播
原因枚举。对当前不可航判定是 NON_BLOCKING；对未来按原因解释/策略则需要正式 proposal。

## 5. Findings（2026-08-23 01:16 +08:00）

| Finding | Class | Current action |
|---|---|---|
| Winter unknown policy 与 C fail-closed sampler | CONDITIONAL BLOCKING | 下一轮 B validation 先测，不在本轮改算法 |
| committed hourly window 是正式入口，不是单帧 | REQUIRED CONTROL | 既有 store/source protocol 保持 |
| adaptive grid 不兼容当前 regular-grid 假设 | NON_BLOCKING / PLANNED | proposal before implementation |
| hard_reason 未传播到 SampledRisk | NON_BLOCKING | 记录 tech debt，不临时扩字段 |

因此 B/C 接口结构可冻结；C 正式 Winter planning 仍必须等待真实 Winter RiskFrame window 通过
unknown/hard/cadence gate。

## 6. 证据位置（2026-08-23 01:16 +08:00）

- `work_package_c/schemas/risk-frame-v2.schema.json`
- `work_package_c/src/arctic_route_planning/contracts/models.py`
- `work_package_c/src/arctic_route_planning/contracts/windows.py`
- `work_package_c/src/arctic_route_planning/ingress.py`
- `work_package_c/src/arctic_route_planning/risk/sampler.py`
- `work_package_b/tests/contract/test_bc_contract.py`
- `work_package_c/tests/integration/test_formal_ingress.py`
