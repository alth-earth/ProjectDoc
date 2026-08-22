---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: A-to-B formal input and B formal output interface freeze audit
Canonical/Supporting: Supporting evidence for the contract ownership registry
Branch: research-validation-system
Last Verified: 2026-08-23
---

# B 接口冻结审计

## 1. 审计结论（2026-08-23 01:16 +08:00）

```text
A→B input = a.dataset-bundle.v2 + RunContext.v2
B output = bc.risk-frame.v2 + committed hourly window
VERDICT = STABLE_WITH_NEXT_GATE_CONTROLS
```

A 负责 DatasetBundle 领域生成，shared contracts 负责独立结构/identity 校验，B 只消费 A
公共 `PreparedWindow`/bundle，不读取 A 私有 SQLite、raw 或 ready 目录。B 拥有风险计算与
发布语义；`bc.risk-frame.v2` transport model/codec 当前位于 C repository，C 是强制兼容性
审阅者。这种 split ownership 已有 producer-consumer tests，不需要本轮改 schema。

## 2. DatasetBundle.v2 冻结字段（2026-08-23 01:16 +08:00）

顶层冻结字段包括 schema/bundle identity、corridor、`as_of_time`、requested/minimum
window、requested data types、source snapshots、records 与 coverage。Record 固定表达：

```text
data_id, data_type, issue_time, valid_time, source, version,
quality_flag, checksum, source_snapshot_id
```

Coverage 固定表达 cadence、available range、missing intervals、minimum/requested coverage、
provenance completeness 与 content digests。缺失不能伪装为 `quality_flag=missing` 的完整
payload；正式 bundle 必须 coverage/provenance complete。

## 3. 单位、时间与 provenance（2026-08-23 01:16 +08:00）

Bundle JSON 不重复携带 payload variable units、CRS 或分辨率；当前正式路径由 A normalized
xarray payload、manifest metadata、semantic payload digest 和 exact resolver 共同 attestation。
规范示例包括 wind/current/drift `m s-1`、temperature `K`、visibility `m`、wave/thickness/
water level `m`、direction `degree`、land mask/concentration dimensionless。

时间不变量为 UTC，且 `record.issue_time <= bundle.as_of_time`。`as_of_time` 是 logical
knowledge cutoff，不要求等于 max issue time；`valid_time` 不参与可见性判断。RunContext 绑定
scenario/corridor/vessel/bundle ID 与 digest，ExecutionSpec 不重复这些字段。

## 4. B 输出冻结语义（2026-08-23 01:16 +08:00）

`bc.risk-frame.v2` 固定携带 run/scenario/corridor/vessel/config/model/generation identity，
`valid_time/as_of_time/generated_at`，payload、source summary 与 provenance。Payload 固定包含：

```text
latitude, longitude, risk_score, risk_level, hard_mask,
confidence, environment_speed_factor, optional hard_reason
```

- 经纬度严格递增，CRS 为 `EPSG:4326`；
- `risk_score` 为 `[0,1]` dimensionless 或 unknown；`risk_level` 为 1–5；
- `confidence` 为 `[0,1]`，`environment_speed_factor` 为 `(0,1]`；
- `hard_reason` canonical values 为 `NONE/LAND/DATA_UNAVAILABLE/OTHER`；
- unknown/hard/availability 独立，unknown 绝不等于 safe；
- 正式 B window 为完整、无重复、无缺帧的 hourly closed interval，原子 commit 后供 C 消费。

## 5. Findings（2026-08-23 01:16 +08:00）

| Finding | Class | Control |
|---|---|---|
| DatasetBundle transport 不内嵌 units/resolution | NON_BLOCKING | 当前 exact resolver + payload attestation 补足；未来需 proposal，不改 v2 |
| B formal model 仍为 `demo_unvalidated` | NON_BLOCKING / SCIENTIFIC | contract-valid 不等于科学校准完成 |
| unknown 若为非 hard，C 会拒绝导航采样 | CONDITIONAL BLOCKING FOR C | Winter B validation 必须证明无此状态或显式采用 `DATA_UNAVAILABLE` hard policy |
| 只发布散帧而无 committed hourly window | BLOCKING IF VIOLATED | 使用既有 `PersistentRiskStore` 原子窗口协议 |

本轮 A→B formal intake 已通过，以上 conditional finding 不阻止
`READY_FOR_B_VALIDATION`，但会阻止未经验证的 Winter C planning。

## 6. 证据位置（2026-08-23 01:16 +08:00）

- `arctic_route_contracts/schemas/dataset-bundle-v2.schema.json`
- `work_package_a/src/arctic_route_data/bundle.py`
- `work_package_a/src/arctic_route_data/service.py`
- `work_package_b/src/arctic_route_risk/context.py`
- `work_package_b/src/arctic_route_risk/service.py`
- `work_package_b/src/arctic_route_risk/publishing/store.py`
- `work_package_c/schemas/risk-frame-v2.schema.json`
