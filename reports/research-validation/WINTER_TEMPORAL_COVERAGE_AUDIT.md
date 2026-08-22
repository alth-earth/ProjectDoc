---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: Winter 2026-02-15T00Z to 2026-02-21T12Z temporal coverage
Canonical/Supporting: Supporting temporal coverage audit
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Winter Temporal Coverage Audit

## 1. 两个时间窗口必须分离（2026-08-22 21:56 +08:00）

| Window | Definition | Verdict |
|---|---|---|
| Frozen scenario | 2026-02-15T00Z → 2026-02-21T00Z (144 h) | 12/12 COMPLETE |
| Requested audit extension | 2026-02-15T00Z → 2026-02-21T12Z (156 h) | INCOMPLETE |

scenario TOML 与当前 bundle 均以 21T00Z 为 `requested_end`。因此当前 bundle 对自身
144 小时窗口完整且可冻结；它不是 156 小时 bundle，不能被文档描述成已覆盖 21T12Z。

## 2. 156 小时窗口实际覆盖（2026-08-22 21:56 +08:00）

| Variable group | Cadence | Expected | Found | Last/Gap | Status |
|---|---:|---:|---:|---|---|
| wind / temperature / visibility | 3 h | 53 each | 49 each | ends 21T00; missing 03/06/09/12 | INCOMPLETE |
| wave | 3 h | 53 | 53 | complete through 12Z | COMPLETE |
| current / ice concentration / drift / thickness / type / edge / water level | 1 h | 157 each | 155 each | missing 21T01 and 21T02 | INCOMPLETE |
| land/sea mask | static | 1 | 1 | static | COMPLETE |

## 3. 尾部补采与来源连续性（2026-08-22 21:56 +08:00）

`scripts/winter_non_carra_tail_acquisition.py` 从 21T03Z 开始、持续 10 小时，因此对小时
变量天然遗漏 01Z 与 02Z。它补齐 wave 的 03/06/09/12，但不负责 CARRA 气象变量。

| Group | Before tail | Tail | Source transition | Continuity risk |
|---|---|---|---|---|
| wave | Copernicus global wave | same dataset/product family | new source snapshot | low; verify boundary values |
| current | Arctic PHY detided fallback | same dataset/product family | new snapshot and larger request bbox | medium |
| sea ice / water level | same Copernicus family | same family | new snapshot and larger request bbox | medium |
| CARRA meteorology | CARRA through 00Z | no tail acquisition | no replacement source | hard gap after 00Z |

没有发现前段 TOPAZ/NEXTSIM/CARRA、后段改用另一供应商产品来补值的行为。存在的是同一
Copernicus product family 的新 snapshot，以及空间请求从 corridor 附近扩大到
`lon 10–30 / lat 68–80`。例如 ocean snapshot shape 从约 `145×177×152` 变为尾段
`11×193×252`；发布前仍需由 A canonical normalization 保证一致坐标语义。

## 4. 冻结 bundle 的关系（2026-08-22 21:56 +08:00）

冻结 bundle 的 `requested_end=21T00Z`，因此不包含任何 21T03Z–12Z 尾部记录，也不受
上述 01Z/02Z 缺口影响。这个事实同时意味着：

- `FROZEN_ARTIFACT_READY` 只适用于 144 小时场景；
- 尾部缓存不能作为当前 bundle 已覆盖 12Z 的证据；
- 若 12Z 是新研究需求，应先修订 scenario identity/window，然后补 CARRA 四帧与小时
  变量两帧，再生成新的 immutable bundle；禁止原地扩写当前冻结 bundle。

## 5. 日志证据与限制（2026-08-22 21:56 +08:00）

- `work_package_a/carra_run2.log`：CARRA 15T00–21T00，147 processed/published，
  49 snapshots。
- `work_package_a/logs/winter_tail_acq.log`：八类非 CARRA 尾部补采结果。
- 未发现与 20:53 bundle 生成动作一一对应的 standalone generation log；交付文档、
  bundle 内部 digest、外部 SHA-256 与 A doctor 构成当前冻结证据，但日志链仍有缺口。
