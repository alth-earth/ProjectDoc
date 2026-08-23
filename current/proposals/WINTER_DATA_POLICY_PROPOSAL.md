---
Overall Status: APPROVED
Content Status:
  - APPROVED
Document Role: CANONICAL
Scope: winter meteorological source and cadence policy (approved for execution)
Canonical/Supporting: Canonical proposal; production change authorized under gate G5/G6
Branch: research-validation-system
Last Verified: 2026-08-22
Approved: 2026-08-22
---

# Winter 数据策略提案

## 提案元数据（2026-08-22 12:58 +08:00；批准于 2026-08-22）

```text
提案 ID: A-WINTER-MET-001
标题: 2026 年 2 月冬季研究用 CARRA 3 小时回顾性气象
状态: 已批准（APPROVED）
语义负责人: 工作包 A
受影响的生产者: 工作包 A 采集/发布
受影响的消费者: B 通过现有 DatasetBundle.v2；C/D 不变
目标 Schema 版本: 不变
创建时间: 2026-08-22 12:58 +08:00
批准时间: 2026-08-22
```

`APPROVED` 状态授权在 G5/G6 门控约束下，对 2026-02-15..02-21 窗口执行 CARRA 东区单层分析的正式采集与发布。

## 问题与证据（2026-08-22 12:58 +08:00）

冬季场景所需的 12 类数据中目前只有 9 类完整。A 使用的 NOAA NCEI 2026 年 2 月 Grid 4 精确直连路径返回 404，而官方目录元数据仍描述 archive/HAS 可用性。C3S CARRA 在目标月份、区域、时间间隔以及全部三个缺失变量上均有当前的官方目录证据。

常被提及的"A 策略为 3 小时但回顾适配器为 6 小时"本身并不构成正式的 bundle 不兼容：

- `service.py` 仅在无元数据时把 3 小时作为回退值；
- 真实源记录的 `nominal_interval_hours` 优先级更高；
- `DatasetBundle.v2` 正式允许风、温度、能见度使用 3 小时或 6 小时。

当前不完整诊断显示 3 小时，是因为冬季气象记录为零。如果现有 NCEI 适配器发布了真实的 6 小时记录，覆盖率将使用其声明的 6 小时间隔。因此，生产决策关乎数据源保真度和研究分辨率，而非悄悄放宽硬编码的 bundle 门控。

## 时间间隔选项（2026-08-22 12:58 +08:00）

### 方案 A — 统一 3 小时气象（2026-08-22 12:58 +08:00）

三个缺失行均使用 CARRA 3 小时分析。

优点：

- 与当前研究回退和波浪时间间隔一致；
- 在 144 小时闭合窗口内正好有 49 个精确目标时刻；
- A 无需进行源时间插值；
- 官方 2.5 km 北极区域产品，覆盖全部三个变量。

成本/风险：

- 新增源适配器及 CDS 认证/条款工作流；
- 需按投影感知旋转网格相对风矢量；
- 需新增源身份标识，并与冻结的 GFS 夏季数据建立科学可比性说明。

### 方案 B — 统一 6 小时气象（2026-08-22 12:58 +08:00）

通过恢复直连路径或经批准的 HAS 摄取恢复 NCEI GFS。

优点：

- 复用 A 现有的回顾解析器、清单选择器、规范化字段及正式的 6 小时间隔支持；
- 与 A 之前的工作保持 NOAA/GFS 数据源家族一致。

成本/风险：

- 在 144 小时闭合窗口内仅有 25 个精确源时刻；
- B 通过在连续帧之间做确定性线性插值生成逐小时风险支撑，并应用插值置信度而非精确帧置信度；
- 直连归档当前不可用；HAS 需要外部下单及新的带检查点的摄取路径。

禁止将 6 小时记录复制为合成的 3 小时记录。

### 方案 C — 按变量区分时间间隔/数据源（2026-08-22 12:58 +08:00）

A 已支持源记录时间间隔元数据，可跨不同类型承载不同时间间隔。除非提供显式策略，否则同一类型内冲突的时间间隔声明将被拒绝。

优点：

- 允许每个变量使用可用的最佳官方数据源；
- 无需更改合约 Schema。

成本/风险：

- 使三个气象贡献项在时间与科学上异构；
- 使发布时间/溯源比较与置信度解释复杂化；
- 增加单个缺失变量阻塞完整 bundle 的可能性。

在 CARRA 提供原子化三变量产品家族的前提下，该方案仅应作为应急方案，而非首选。

## 提议语义（2026-08-22 12:58 +08:00）

| 维度 | 当前 | 提议 | 破坏性？ |
|---|---|---|---|
| Schema 身份 | `scenario.v2`, `a.dataset-bundle.v2` | 不变 | 否 |
| 必需数据类型 | 12 | 不变 | 否 |
| 数据源 | 预定 NCEI GFS 适配器 | 三个缺失行使用 CARRA 单层分析 | 仅数据源变更 |
| 时间间隔 | 记录声明的 3 小时或 6 小时 | CARRA 分析声明为 3 小时 | 否 |
| 网格 | 保留源网格 | 保留 CARRA 投影/网格证据 | 否 |
| 风语义 | 真东/真北 | 发布前将 CARRA 网格相对 u/v 旋转 | 否；必需的归一化 |
| 缺失行为 | 不完整/失败关闭 | 不变 | 否 |
| Bundle 身份 | 内容/源相关摘要 | 仅新增冬季身份标识 | 否 |
| 冻结构件 | 不可变 | 不动 | 否 |

## 对 B 和 C 的影响（2026-08-22 12:58 +08:00）

B 已在包围的有效时刻之间线性解析连续环境场，并在置信度中区分精确与插值的时间支撑。在 3 小时间隔下，每三个小时风险帧中有两个使用插值；在 6 小时间隔下，每六个中有五个。由于数据源不同，这将改变输入支撑/置信度并可能影响风险值，但不得改变风险公式或等级策略。

C 消费已发布的 B 风险帧，而非直接消费 A 的时间间隔。规划影响必须在 A 通过后，通过冬季 B 冒烟测试和路径完整性来评估。C 不得为数据源缺口做补偿，也不得自行构造气象数据。

## 实施归属与门控（2026-08-22 12:58 +08:00）

| 仓库 / 目录 | 负责人 | 批准后允许 | 禁止 |
|---|---|---|---|
| `work_package_a/src/arctic_route_data/` | A | 增量 CARRA 适配器、溯源、旋转、检查点 | Schema 变更、伪造填充、夏季替换 |
| `work_package_a/tests/` | A | 单元测试与单帧真实源冒烟 | 以 fixture 断言冒充真实采集 |
| `arctic_route_contracts` | 合约 | 预期无变更 | 版本/Schema 修改 |
| `work_package_b/c/d` | 各自负责人 | 仅在正式冬季 bundle 后进行冒烟 | 数据源侧变通 |

批准/验收门控：

1. A 负责人批准本提案及 CARRA 数据源身份标识。
2. 操作员提供 CDS 个人访问令牌（不提交入库）并通过 CDS 接受数据集条款。
3. 单帧东区冒烟测试证明变量、坐标、单位、有效时刻、投影及真矢量转换。
4. A 定向测试与 doctor 检查通过。
5. 六天采集准确发布所需源时刻，含不可变快照且无部分接收。
6. bundle 输出前，十二类覆盖率在未使用 `--allow-incomplete` 的情况下通过。

## 审批记录（2026-08-22 12:58 +08:00；更新于 2026-08-22）

| 角色 | 决策 | 证据/日期 |
|---|---|---|
| A 语义负责人 | 已批准 | 2026-08-22；适配器 `carra_acquisition.py` 实况探测 + 试运行 + 定向测试通过 |
| B 消费者负责人 | 待定 | 评审时间间隔/置信度影响（不阻塞 A 摄取） |
| 合约负责人 | 除非实现中发现 Schema 需求，否则无需 | 当前 v2 已携带时间间隔/数据源身份标识 |
| 集成负责人 | 待定 | |

批准条件（承接验收门控 5–6）：

- 门控 5：CARRA 在 `winter_bundle` 冻结前完成摄取，准确发布所需源时刻，含不可变快照且无部分接收。
- 门控 6：bundle 输出前，十二类覆盖率在未使用 `--allow-incomplete` 的情况下通过；CARRA 部分发布 ACQ-203 无效数据溯源。
- 采集使用带溯源的 `publisher.publish_dataset`。在 G5/G6 端到端可证满足之前，仅进行试运行。

## 摄取执行记录（2026-08-22）

在批准下执行了 CARRA 东区单层采集。

- **路径 / 窗口**：在 corridor `tromso_to_isfjorden_outer` 下发布（不是内部 `A-winter-carra` 标签 —— corridor `tromso_isfjorden_february_2026_research_v1` 使用 `corridor_id = tromso_to_isfjorden_outer`，窗口 2026-02-15T00Z .. 02-21T00Z，horizon 144 h）。首次尝试使用了错误的 route_id（`A-winter-carra`）；发现错误后，该错误批次（168 条记录 + `data/ready/A-winter-carra`）已被删除，GRIB 缓存保留。
- **数据量**：49 个分析周期 × 3 类数据（wind_field / temperature / visibility）= 147 个已发布帧、49 份源快照。`frames_processed = frames_published = 147`，manifest 不可变，无部分接收。
- **Doctor 检查**：`python -m arctic_route_data.cli doctor --data-root data` → `ok: true`，检查 5379 项，0 错误 / 0 警告。
- **门控 6（十二类覆盖率）**：当回放窗口与数据实际结束时间对齐时，在未使用 `--allow-incomplete` 的情况下通过。关键发现：整个 2026-02 数据集（CARRA + ocean/sea_ice/water_level/wave）在 02-21T00Z 结束，但默认 `horizon_hours=144` 的回放请求将 `requested_end` 延伸到 02-21T12Z，导致每类数据尾部出现 12 小时缺口。使用 `--horizon-hours 132`（`requested_end = minimum_required_end = 02-20T12Z`）时，全部 12 类 required 均为 `complete: true`，`all_required_complete = True`，退出码 0。这是回放窗口/数据结束时间对齐问题，而非 CARRA 采集缺陷 —— CARRA 的 49 个周期在 02-15T00Z..02-21T00Z 上连续。
- **未决项（已于 2026-08-22 下午解决）**：场景名义 144 小时视界下 02-21T00Z..12Z 处的 12 小时尾部缺口。决策：**方案 (a)** —— 为八个动态非 CARRA 冬季数据源回填 02-21T03/06/09/12Z（`land_sea_mask` 为静态 GEBCO 掩膜，不参与回填）。通过 `scripts/winter_non_carra_tail_acquisition.py` 实现；回填后数据结束时间对齐至 02-21T12Z，因此即使名义 `horizon_hours=144` 的回放也能得到 `all_required_complete = True`，无需 `--horizon-hours 132` 变通。
- **状态**：门控 5 已满足。门控 6 已满足 —— 默认 horizon=144 下十二类覆盖率在未使用 `--allow-incomplete` 的情况下通过。`winter_bundle` 于 2026-08-22 20:53 冻结为 `data/tromso_to_isfjorden_outer_winter_20260215T000000Z_bundle.json`（generation_id 0；doctor `ok: true`，检查 5461 项，0 错误）。所有门控已关闭。

## 建议（2026-08-22 12:58 +08:00）

批准方案 A：三个缺失行使用 CARRA 3 小时分析。保留 NCEI GFS 6 小时分析作为恢复性应急方案，而非前置条件。不批准从 3 小时到 6 小时的全局放宽，因为当前合约已表达按源区分的时间间隔，且 CARRA 可直接满足 3 小时。
