---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - EXPERIMENTAL
Document Role: SUPPORTING
Applicability: CURRENT
Scope: Winter 真实动态回放、Viewer revision 传输与 C RC2 三核并行恢复
Canonical For: 本轮工程变更、验证证据、限制与下一阶段门禁
Branch: research-validation-system
Last Verified: 2026-09-04 19:59 +08:00
Related Canonical Docs:
  - ../../current/CURRENT_STATUS.md
  - ../../current/CURRENT_ROADMAP.md
  - ../../standards/AGENT_DOCUMENTATION_RULES.md
---

# Winter 动态重规划与 C RC2 三核并行工程运行报告（2026-09-01 22:52 +08:00）

## 0. 2026-09-02 原始冻结身份最终到达态增量（取代下文 v4/v7/v13 中间数值）

### 2026-09-04 22:17 +08:00 v4 连续性修正与最终 Viewer 交付

本节是 v3 发现严重路线/船位不一致后的更正记录；下方 v3 及更早内容保留为历史证据，
不代表当前 ready 默认制品。

#### 1. 执行摘要

Verdict：`v4 PUBLISHED / REAL_BROWSER_REGRESSION_PASS / CAUSAL_PENDING`。C 修正了 AnyAngle
跳过权威航点和 adaptive trust 距离方向，D 修正了候选 overlay、formal/timeline 连续性和
adoption 精确时刻。v4 的运行路线为身份绑定 `CURVE`；R2–R6 的采用事件真实消费，未观察到
超过 25 km 的瞬移。不存在把 Winter 经纬度写死在 D 平滑代码中的做法。

| 指标 / 声明 | Before（v3） | After（v4） | Delta | Verdict / 原因 |
| --- | --- | --- | --- | --- |
| R1 初始拓扑 | AnyAngle 可跳过中间航点，首段视觉偏离 | 保留全部 raw waypoint anchor，首段同经度北向 | 修正 | `C AUTHORITATIVE PASS` |
| active route 绘制 | 候选比较线可能覆盖正式线 | 候选永不替换 formal motion | 修正 | `D SEMANTIC PASS` |
| formal curve 连续性 | 失配曲线可能造成大跳跃 | 超过 25 km 回退权威 timeline | 新增门禁 | `FAIL-CLOSED PASS` |
| 动态采用 | 稀疏 timeline 可能晚一帧切换 | 按真实 `REPLAN_ADOPTED.t` 切换 | 修正 | `REAL_E2E PASS` |

#### 2. 范围 / 非范围

范围是本地现有 Winter A/B 数据上的 C 重新规划、正式 motion、Orchestrator replay、D Viewer
导出与浏览器回归。不重新下载数据、不改变 B 风险公式、不放宽海陆/unknown/走廊/操纵性/ETA/
风险非劣化门禁，不声明 causal replay、实时预测、导航级或实船资格。

#### 3. 起始基线

起始制品为外部 ready 中的 v3；其首段 R1 geometry 的前八个航点为
`(18.4,70.3333) → … → (18.4,72.9)`，原始拓扑本身是向北的。v3 的偏差来自 C AnyAngle
和 D 展示/连续性边界，不是纬经度互换。C 起始 HEAD `9a57289`，D 起始 HEAD `e2428c7`；
当前控制中心 AppImage 为包含修正后的二进制。

#### 4. Git 最终状态

| 仓库 | HEAD | 工作树 / 提交 / 推送 |
| --- | --- | --- |
| C `work_package_c` | `680e085`（起始 `9a57289`） | 已本地提交 `fix: preserve formal motion waypoint topology`；未 push |
| Orchestrator | `c0cbc92` | clean；本轮无代码修改、未新增提交 |
| D `work_package_d` | `53a7f3c`（起始 `e2428c7`） | 已本地提交 `fix: keep viewer motion and display layers aligned`；未 push |
| Governance | `current HEAD`（本报告随最终提交更新） | 已本地提交 v4 治理与交付记录；未 push |
| Control Center | `91687eb` | 已本地提交 `docs: update winter v4 release handoff`；release 二进制为外部构件，未 push |

#### 5. 文件系统与资源安全

重型 replay 串行执行；Orchestrator 全量测试 wall time 263.37 s，未与其他重型任务重叠。
本次最终 AppImage 解包扫描目录和临时构建目录均在验证后清理；凭据、原始 GRIB/NC 和缓存
未进入包。清理前 `/` 可用空间约 850 GB，`MemAvailable` 约 4.2 GiB；无 OOM。

#### 6. 代码 / 架构变更

- C `motion/producer.py` 增加向后兼容 `allow_any_angle_shortcuts=False`，默认过滤到完整
  raw waypoint 序列；局部窗口曲线平滑只在 producer 侧生成并保留 anchor。
- D `route_motion.js` 将每个 formal motion 与所有 waypoint 绑定误差限制为 2 km；`app.js`
  排除 operational candidate overlay，formal/timeline 偏差超过 25 km 时切回线性 timeline，
  并在真实 adoption event 时间更新 active revision。
- D `route_visual_smoothing.js` 未写入路线数据；它读取当前 candidate 的 `geometry`，把已投影
  点变成 display-only Canvas quadratic commands。20 CSS px、40% trim 等是可测试显示策略，
  不是航线、船位、ETA 或 route ID。

#### 7. 语义 / 合约变更

正式 vessel position、heading、trail、ETA 和 active route 继续由 C `motion_samples` 与
authoritative timeline 驱动；候选平滑不改变 geometry、metrics、ranking、adoption 或合同。
`REPLAN_DECIDED` 仍不等于 `REPLAN_ADOPTED`；事件切换不跳船位。v4 标签仍为
`retrospective_post_hoc_dynamic_projection`。

#### 8. 实验 / 备选方案

历史 AnyAngle shortcut、`route_smoothing.js` B-spline 和 research sidecar 未进入默认生产
绘制链；它们保留为历史/隔离实验。未用“放宽门禁”伪造曲线；未采用的比较候选仍保留真实
RAW/失败原因。

#### 9. 权威运行 / 真实验证

窗口 `2026-02-15T00:00:00Z → 2026-02-21T00:00:00Z`，v4 replay 复用同一 Winter A/B 身份，
25 snapshots、6 revisions、5 adopted chains、终态 `ARRIVED`。R2–R6 adoption 均为 formal
`CURVE`，一秒前到 adoption 的最大位置差为 0.710 km；大于 25 km 的 teleport 为 false。

#### 10. 性能分解

未改变时间窗口和 tick 预算。新增 waypoint binding、连续性计算和候选过滤属于预期小额展示/
校验开销；未重新运行性能基准，性能增量记为 `NOT BENCHMARKED`，不以旧数据冒充新结果。

#### 11. 正确性 / 验证

C `761 passed`；D `125 passed`；控制中心 `28 passed`；Orchestrator `191 passed`（退出码 0，
仅有 host `cfgrib` 找不到 ecCodes 的 warning）；AppImage 自检内置 ecCodes `2.48.0`，解包
扫描 `27047` 文件 `PASS`。最终 Chromium console errors/warnings 均为 0，重新扫描发现 v4，
运行后 route layer、目标筛选和候选高亮均可操作。

#### 12. 确定性 / 可复现性

v4 publisher 的包内 JSON/checksum 校验通过；完整 replay 第二次确定性重型运行本轮记为
`NOT RUN`，不得继承 v3 证据冒充 v4。截图与 evidence 文件绑定本轮 v4 assembly、bundle、
checksums 和 AppImage SHA-256。

#### 13. 构件 / 溯源

v4 source：`work_package_d/output/winter-rebuilt-20260215-viewer-package-v4/`；外部 ready：
`/root/.local/share/arctic-route-control-center/artifacts/ready/winter-rebuilt-20260215-viewer-package-v4/`。
assembly `winter-viewer-sha256-f3113a19243bce88f712717ad91bddd9d3c76d93c6d84ac3c57e930496dff1ad`；
bundle SHA `f993ac113ac7280e9378710fdc84a825338ebd6ea4b5193ce8679aeb5c3b114a`；checksums SHA
`92ca583e52d41d277d22750631f083b0de798cb5ce8f9b105ef7a1d0123f7d33`；AppImage SHA
`9fca146f0e8f57219724562d07488999d78862ddf34b10b7002160584ef7934d`。v3 移至 invalid withdrawn
目录但源码、历史摘要和交付 archive 保留。

#### 14. 已知限制 / 技术债

`TD-WINTER-CAUSAL-001 / high`：issue-time 可追溯 causal window 仍未建立；继续标记 post-hoc。
`TD-APPIMAGE-GLIBC-001 / medium`：本构建机 glibc 2.39，广泛旧 Linux 兼容性需在 Ubuntu 22.04
基线复建。`TD-V4-DETERMINISM-001 / medium`：完整第二次 v4 replay 未运行，保留为下一轮门禁。

#### 15. 决策 / 下一阶段

当前默认外部制品切换为 v4；v3 不可选但不删除历史证据。后续只在 C producer 审计、formal
motion identity 和真实 browser regression 均通过后发布新制品；不得用 D 平滑层掩盖规划几何，
不得放宽硬门禁来制造动态事件。下一阶段是 causal data feasibility 审计或按授权执行 Git 本地提交，
仍不 push、不修改冻结 RC1/RC2。

### 2026-09-04 19:17 +08:00 v3 Winter 重建与 Viewer 动态回放收口

本小节是本报告当前最新结论；下方原有 2026-09-02 原始冻结身份表格及第 1–15 节保留为
前一轮工程证据，不被静默改写。目标是修复 v2 的 `RAW_PASSTHROUGH` 运行路线和缺失的
动态 replay/revision/motion 身份绑定，同时保留正式 producer、Switch Gate 与失败关闭边界。

#### Before / After（2026-09-04 19:17 +08:00）

| 指标 / 声明 | Before（v2/旧回放） | After（v3） | Delta | Verdict / 原因 |
|---|---|---|---|---|
| Viewer 动态 replay | 运行路线可落到 `RAW_PASSTHROUGH`；动态采用资源不完整 | 真实 replay manifest、snapshots、revision 和采用事件均可消费 | 补齐 | `REAL_RETROSPECTIVE_E2E_PASS` |
| C plan revision | 旧资源无法与采用 motion 完整绑定 | 6 个不可变 revision，每版四层×三目标=12 条 | +6 revisions | `AUTHORITATIVE_PASS`（C 生产者范围） |
| replan adoption | 无法证明多次真实采用 | 5 组 `DECIDED → ADOPTED → ROUTE_CHANGED`，均有 revision 身份 | +5 chains | `REAL_E2E_PASS`（事后动态投影） |
| replay 时间线 | 旧包缺动态时间线或为静态 fallback | 6h tick、25 snapshots，最终 `ARRIVED`、`pending_route=null` | +25 snapshots | `REAL_E2E_PASS` |
| 初始/采用 motion | 初始运行路线可显示 raw fallback | 三个初始 full-voyage 候选和所有实际采用路线为 `CURVE` | 回退消除（采用路径） | `FORMAL_MOTION_PASS`；未采用 RAW 仍如实保留 |
| AppImage | 当前 Linux x86_64 二进制可运行 | 二进制保持不变，仅外部导入 v3 | 无重建 | `UNCHANGED / COMPATIBLE` |

#### 运行与配置事实（2026-09-04 19:17 +08:00）

- 输入身份未重新下载：DatasetBundle 为
  `a-bundle-fbbbfbb6e14bec5162408046`（digest
  `fbbbfbb6e14bec5162408046781cd64eb6659f22b0b07d6005b0acf70e473bba`），RiskWindow 为
  `risk-window-sha256-86bdb614c5137ba9ef9129713b5575423e97bac3522bea9ff89f45f879a03ecb`，
  scenario 为 `tromso_isfjorden_february_2026_research_v1`。
- 回放根为
  `.runtime/replays/winter-rebuilt-20260215-retro-dynamic-v3/`，窗口为
  `2026-02-15T00:00:00Z → 2026-02-21T00:00:00Z`，模式为
  `retrospective_dynamic_replay`，对外能力标签为
  `retrospective_post_hoc_dynamic_projection`。共 25 snapshots、6 revisions、113 个
  manifest events；终态 `ship_state.status=ARRIVED`，`pending_route=null`，无待采用路线。
- C 使用 `winter_motion_reserve_5pct`，`operational_speed_reserve_fraction=0.05` 只用于
  规划 ETA；replanning 使用 `winter_dynamic_replay`：最小间隔 6h、route gain 1%、hysteresis
  1%、最大风险回退容差 0%。Orchestrator replay CLI 增加显式
  `--planner-name`/`--replanning-name`，命名 profile、摘要和 worker 传播写入 manifest，
  worker 不加载默认配置。
- 3 个持久 worker 的真实 summary 为 `requested/effective/max=3/3/3`、36 planning calls、
  108 objective tasks；tick、四层 barrier、B、Switch/Adoption Gate 仍串行。R1–R6 六套
  candidate-motion transport 均已绑定；R3 的 executable/fastest `RAW` 只作为未采用比较层
  和真实 `minimum_radius_exceeded` 证据，不伪装为 `CURVE`。

#### 制品、发布与浏览器证据（2026-09-04 19:17 +08:00）

- v3 包路径为
  `work_package_d/output/winter-rebuilt-20260215-viewer-package-v3/`，assembly 为
  `winter-viewer-sha256-1a50c77c012285404d96d3de1cdb0cd563214371911c6ae0c066c3280f5e8afd`；
  `bundle.json` SHA-256 为
  `3772a5d621bd058ef58d6b8aadc0254a15f3bd44cc027b7e10c4c63ceacf58ed`，
  `checksums.json` SHA-256 为
  `a96c61138f089a962e21dbaa481521db3213376f2bcbcb90aafe8ce2cb2627ff`。发布器输出只保留
  包内相对引用/摘要，20 个白名单文件中 `publish-summary.json` 及其余 18 个文件均由
  checksum 覆盖（不含 checksums 自身）；严格 JSON、allowlist、确定性逐文件比对与解包扫描
  通过，包不含 D HTML/CSS/JS、凭据、原始 GRIB/NC、缓存或绝对路径。
- v3 已复制到当前 AppImage 外部数据根的 `artifacts/inbox/`，经“重新扫描”及校验后原子
  提升到 `/root/.local/share/arctic-route-control-center/artifacts/ready/`；v2 已退役到
  `artifacts/invalid/winter-rebuilt-20260215-viewer-package-v2-retired-20260904/`，v2 原始
  输出和历史摘要保留。现有 AppImage
  `arctic_route_control_center/release/Arctic_Route_Control_Center-x86_64.AppImage` 未重建，
  当前 SHA-256 仍为 `cc9fd06f100e777cc43d7e0aac69b6de2662530eeba3946a6d23a7ad49e4acbf`。
- 浏览器截图在最终 R1–R6 完整 v3 包上重新生成，目录为
  `output/playwright/winter-rebuilt-20260215-current-standard-v3/`，不复用旧二进制证据：
  `viewer-v3-r2-adopted.png`（SHA-256
  `72650104cb6e3c613d1b092d8cfe0e1713862a6d81cb516aa812b51b1ffd5f29`）、
  `viewer-v3-r6-active.png`（SHA-256
  `9dd3e749148e2f17904ca01cfeba000a96a6b0ce9d1be0648e686490c605ff6a`）和
  `control-center-ready-v3.png`（SHA-256
  `f4610122030e150783e2fa832f4edef40c122706fd1453de9b09f9babf3b16ce`）。回归确认路线层、
  三目标筛选和候选卡片高亮在运行锁定后仍可操作；运行锁只保护运行 candidate/motion/ETA，
  控制台错误/警告为 0。

#### 验证成熟度与边界（2026-09-04 19:17 +08:00）

| 能力 | 本轮成熟度 | 证据边界 |
|---|---|---|
| C formal motion / Switch Gate | `PASS` | 初始及实际采用路线为 CURVE；R3/R4 未采用 RAW 保留真实状态 |
| Orchestrator replay | `REAL_E2E_PASS` | 25 snapshots、6 revisions、5 adopted chains；不证明 causal 可得性 |
| Viewer package | `PUBLISHED / CHECKSUM_PASS` | v3 可导入当前 AppImage 外部 ready；不重建 AppImage |
| Risk Explanation | `PARTIAL`（逐格仍可 COMPLETE/UNAVAILABLE） | 继续消费 producer 字段，不由 D 反推 reason |
| 科学标定、实时预测、导航/实船资格 | `NOT ESTABLISHED / PROHIBITED` | `demo_unvalidated` 与 retrospective post-hoc 限制仍有效 |

#### Unexpected Findings / Corrections（2026-09-04 19:17 +08:00）

- 首次 v3 exporter 输出漏带 Risk Explanation；该失败包已隔离，随后补入同身份 explanation
  transport，重新计算 assembly/manifest/summary/checksum，并对最终包做确定性逐文件比对。
- 第二次发布前审计发现初始修正版只携带 R1 candidate-motion set；该 exporter-only 包也已
  隔离，随后用同一 replay 的 R2–R6 C motion 产物补齐六版 candidate-motion，并重新完成
  发布器校验。最终 v3 才是当前 ready 制品。
- v3 最终包中的 `adoption_status=DEFERRED` 只描述最后一次 deferred 模式；正式终态依据是
  `status=ARRIVED` 且 `pending_route=null`，不能把该字段误读为残留待采用。
- 截图哈希已在最终 R1–R6 完整 v3 二进制上重新绑定；旧截图不作为本轮证据。严格 causal Winter 仍因
  issue-time 覆盖不足保持 fail-closed。

下文 3 snapshots、17 events、3 revisions 和 Viewer v7 是排障过程中的可审计中间基线；
最终发布链已恢复 2026-08-31 原始冻结身份并继续运行至到达，不应再把那些计数或后续
holdout 的风险覆盖/路线选择当作当前默认状态。

| 项目 | 最终证据 | Verdict |
|---|---|---|
| Replay | `winter-original-frozen-dynamic-v1`；25 snapshots、9 revisions、119 events；8 组 DECIDED/ADOPTED/ROUTE_CHANGED；终态 `ARRIVED` | `REAL_RETROSPECTIVE_E2E_PASS` |
| 四层路线 | 每个 revision 4 layers × 3 objectives = 12；9 个不可变 candidate set | `AUTHORITATIVE_PASS` |
| 正式 motion | 9 个 `cd.route-motion-set.v1`；R1–R4 `CURVE`，R5–R7 风险回退，R8–R9 几何回退 | `ENGINEERING_PASS / FAIL_CLOSED` |
| C 三核 | requested/effective/max `3/3/3`；36 planning calls、108 objective tasks | `REAL_RUN_PASS` |
| Viewer | assembly `a375b4…94e7`；8,641 minute samples；到达后 completed track 保留、current segment 清空 | `BROWSER_E2E_PASS` |
| 风险时域 | 344/528 px；145 ticks；8 px tick；绿/黄；横向滚动 | `BROWSER_LAYOUT_PASS` |
| B explanation | 当前 identity 无 sidecar；精确 A source trace 已退役，不跨身份复用、不伪造 | `OPTIONAL_UNAVAILABLE / BASE_CHAIN_UNAFFECTED` |
| 测试 | C 736；O 145 + formal integration `2 passed, 1 warning`/exit 0/1009.42s；D unit 107；定向 Ruff PASS；浏览器 console 0、344/528 layout PASS | `PASS` |

“6:00 snapshot 仍显示旧 revision”的根因是采用事件发生于稀疏 snapshot 之间，而不是局部
B 样条缺失。PresentationAdapter 现按 event time 覆盖 active/pending；D 对 motion adoption
offset 的跨语言校验只容忍 JavaScript 丢失的亚毫秒，2 ms 错配仍失败关闭。completed-track
ETA 同步应用 adopted route 的 time offset，避免重规划后已走航迹被改写或消失。

局部 B 样条的基函数不是性能瓶颈；主要成本来自连续走廊、风险和操纵性资格门。当前正式
参数为 trim `0.49`、采样间距 `250 m`；R1 full-voyage 最小半径约 7,464 m、最大偏离约
723 m，曲线约缩短 2.17 km。R5–R7 在五档 trim 下均触发同一积分风险回退，证明不能靠放大
曲率窗口绕过门禁。优化仅复用同一调用内 raw 风险采样并前置廉价门禁，不跨 identity 缓存，
也不减少安全检查。

## 1. holdout 排障中间摘要（2026-09-01 22:52 +08:00，非当前默认）

本节记录当时 3-revision holdout 排障包，供审计重现；当前 verdict 必须读取第 0 节，以下
计数和 explanation 状态均不得作为当前默认：

```text
INTERMEDIATE_VIEWER_DYNAMIC_REPLANNING = PUBLISHED_RETROSPECTIVE_DYNAMIC_REPLAY
INTERMEDIATE_WINTER_STRICT_CAUSAL_REPLAY = PENDING / FAIL_CLOSED
INTERMEDIATE_WINTER_ROUTE_CARDINALITY = 4 layers × 3 objectives × 3 revisions
INTERMEDIATE_C_RC2_OBJECTIVE_PARALLELISM = REAL_RUN_PASS (effective/max concurrent = 3)
INTERMEDIATE_B_RISK_EXPLANATION = PUBLISHED_PARTIAL / ENGINEERING_CHAIN_PASS
```

**关键增量表**

| 指标 / 声明 | Before | After | Delta | Verdict / 原因 |
|---|---|---|---|---|
| 默认 Winter replay | 静态/单路线 fallback，无真实 replay event | 同身份真实 holdout 回放，17 events、3 snapshots | 新增 | `IMPROVED`；明确为事后动态投影 |
| revision 资源 | 没有可消费的多 revision plan-set | rev1 superseded、rev2 current、rev3 pending；每版 4×3=12 | 新增 | `PASS`；content-addressed index |
| Viewer 候选路线 | 入口呈现 1 项或空 package | `PUBLISHED`，12 candidates，12/12 integrity | +11 项 | `PASS`；D 不重排/不重算 |
| C 并行证据 | 3-worker 只在历史基线/配置中可见 | 正式 initial/replan path；3 workers、36 tasks、max=3 | 可审计 | `REAL_RUN_PASS`；tick/layer/B 串行 |
| 风险时域 | 窄侧栏 tick/bar 被 flex 压缩，颜色不可见 | 145 ticks、横向滚动、8px/3.35px、绿/黄 | 恢复可见性 | `BROWSER_E2E_PASS` |
| risk explanation（中间 holdout） | 缺 sidecar 时用户只能看到不可用 | 当时同 RiskWindow sidecar 已传输 | 当时从整包缺失到逐格可解释 | `HISTORICAL_ENGINEERING_CHAIN_PASS`；不可跨身份用于当前包 |

**声明矩阵（Claim Matrix）**

| 声明 | 状态 | 验证等级 | 证据 | 备注 / 限制 |
|---|---|---|---|---|
| 真实 Winter 动态事件 | `PASS` | `REAL_E2E_PASS` | `winter-retro-holdout-resource-v4` manifest；17 events | `retrospective_post_hoc_dynamic_projection`，不是 causal |
| 待采用 / 已替代 / 当前路段 | `PASS` | `REAL_E2E_PASS` | revision index + DOM：R2 pending/adopted、R3 pending | current segment 由正式 motion/ETA 驱动 |
| 完整四层 12 路线 | `PASS` | `AUTHORITATIVE_PASS`（继承 C artifact） | 每 revision 4 layers × 3 objectives；12/12 integrity | D 只投影 C 资源 |
| C RC2 三核并行 | `PASS` | `REAL_E2E_PASS` | `requested=3/effective=3/max=3/tasks=36` | PID 是 provenance，不是 9 核同时运行 |
| 风险时域颜色与宽度 | `PASS` | `REAL_E2E_PASS` | Firefox 344px/528px | 145 个 risk frames，颜色来自真实摘要 |
| B 风险解释（中间 holdout） | `UNAVAILABLE` | `PUBLISHED_PARTIAL` | 当时 B artifact/manifest 同 RiskWindow | 历史证据；当前恢复身份无 sidecar，不可复用 |
| 严格 Winter causal replay | `PENDING` | `NOT_IMPLEMENTED` | issue-time 晚于 2026-02-22 起点 | 数据真实但历史可得性不足 |
| 导航级/实船资格 | `PROHIBITED` | `NOT_APPLICABLE` | B `demo_unvalidated`、工程 motion | 本轮不提升资格 |

## 2. 范围 / 非范围（2026-09-01 22:52 +08:00）

本轮范围：Orchestrator replay/resource/index、正式 C objective-level 并行接入与遥测、D
combined exporter 的 revision 消费、Viewer 风险时域布局、B 默认网格测试语义、默认 Winter
runtime 制品和治理文档。

非范围：不修改 B 风险公式/等级/阈值，不修改 C 搜索目标或路线语义，不把 B-spline 平滑幅度
放大，不绕过安全门，不重写 A frozen data、共享 contract 或 RC1/RC2 frozen artifacts，
不把 retrospective 事件重标成 causal，不执行 push/merge/rebase/reset。

## 3. 起始基线（2026-09-01 22:52 +08:00）

| 项目 | 起始事实 |
|---|---|
| Orchestrator HEAD | `3c6a7f7fe6018793fcd46f9c3d886509806a948b`；working tree 含本轮前后续改动 |
| B HEAD | `853bba020c265c4212f17eec020761bcc2d3fed5`；已有 risk-explanation dirty work |
| C HEAD | `c438dd86babc0889599cccfb5afe10a205c7db7f`；未跟踪 docs 由用户保留 |
| D HEAD | `14a29cc150d53c4679562d2c0bbdc8d8e0fc2224`；已有 Viewer test dirty work |
| Governance HEAD | `1f83d01ea467e572e398c3969671638f2c753a8b` |
| 旧 Viewer | 无同身份 Winter replay resource；候选入口可能落到单路线/空 fallback |
| Winter 输入 | `a-bundle-0ffa8463fa7e05cfd14fa0f8`；真实 3,707-record holdout；145 帧 |
| 已知限制 | issue-time 多数在 2026-08-25，不能假定 2026-02-22 当时可见 |

## 4. Git 最终状态（2026-09-01 22:52 +08:00）

| 仓库 | 分支 | 起始/结束 HEAD | origin tracking / 领先·落后 | Working tree | Commit / Push |
|---|---|---|---|---|---|
| governance | `research-validation-system` | `1f83d01e` / 未提交 | `origin/research-validation-system` / 0 ahead, 0 behind | 本轮 current docs、index、report 修改 | `NOT COMMITTED` / `NOT PERFORMED` |
| orchestrator | `research-validation-system` | `3c6a7f7f` / 未提交 | `origin/research-validation-system` / 0 ahead, 0 behind | 本轮代码、schema、tests、README/CHANGELOG 修改 | `NOT COMMITTED` / `NOT PERFORMED` |
| B | `research-validation-system` | `853bba02` / 未提交 | `origin/research-validation-system` / 0 ahead, 0 behind | 保留用户既有 risk-explanation 修改；本轮只改集成测试 | `NOT COMMITTED` / `NOT PERFORMED` |
| C | `research-validation-system` | `c438dd86` / 未提交 | `origin/research-validation-system` / 0 ahead, 0 behind | 用户未跟踪 docs 保留；无本轮 C 源码修改 | `NOT COMMITTED` / `NOT PERFORMED` |
| D | `research-validation-system` | `14a29cc1` / 未提交 | `origin/research-validation-system` / 0 ahead, 0 behind | 本轮 D README 与既有 test 修改；viewer runtime 为 ignored | `NOT COMMITTED` / `NOT PERFORMED` |

没有执行 reset、clean、rebase、merge 或 push；没有覆盖并发工作树中的无关文件。

## 5. 文件系统与资源安全（2026-09-01 22:52 +08:00）

| 项目 | 结果 |
|---|---|
| 工作树外写入 | `/tmp/winter-retro-resource-v2/v3/v4`、`/tmp/winter-dynamic-viewer-v5/v6`；均为 runtime 生成物 |
| 冻结构件 | 未修改；A/C/D 默认数据源只读消费 |
| `free -h` 连续采样 | `NOT RUN`；本轮未将其作为容量证据 |
| Replay peak RSS | `1750.8 MB`（v4 summary）；无 OOM |
| 重型任务重叠 | `N/A`；三次真实重跑均串行，失败旧目录未删除 |
| 非致命环境告警 | xarray `cfgrib` 缺 ecCodes；不影响输出/schema/Viewer |
| 不可变冲突 | 复用旧 runtime store 时触发 `PublicationConflictError`；改用隔离目录，未绕过 `_write_once` |

## 6. 代码 / 架构变更（2026-09-01 22:52 +08:00）

| 组件 | 旧行为 | 新行为 | 原因 |
|---|---|---|---|
| `ExecutionSpec` | v1 没有可审计 worker profile | v1 保持固定 RC2 `3/persistent` 兼容默认；v2 显式保存 profile | 兼容旧 wire shape，同时可审计 |
| `replay/parallel.py` | ProcessPool 只在历史局部调用，缺少 profile/恢复/遥测 | install 受控替换 C private planner，三目标 ProcessPool、worker PID/任务计数、选项 fail-closed，退出恢复 | 把 RC2 并行接回正式路径 |
| `service.py` | formal initial/replan 没有统一并行包装 | `_execute_with_parallel` 同时包装 initial 与 replan，report 发布 `c_objective_parallelism` | 不分叉 C coordinator/switch gate |
| `replay/runner.py` | plan revision 只有内存/快照引用；遥测可能丢失 | 写不可变 plan-set/index、checkpoint 恢复、上下文内捕获遥测、revision 状态迁移 | Viewer 必须能追踪 pending/superseded/current |
| `replay_viewer_export.py` | 没有真实同身份 replay 时静态 fallback；hard reason 形状不兼容 | 明确允许且标记 retrospective dynamic source；校验 index/digest/cardinality；hard mask 缺 B reason 时显示 unavailable，不推断 | 真实展示与失败关闭并存 |
| D risk timeline | flex 子项可压至不可见，颜色/满度误导 | tick/bar 最小宽度、横向滚动、344/528 回归 | 修复展示层，不改变 risk 数据 |

## 7. 语义 / 合约变更（2026-09-01 22:52 +08:00）

- `retrospective_dynamic_replay` 只改变知识投影方式：原始 `issue_time`、scenario、bundle、
  RiskWindow 和 C plan identity 保留；不改变事实时间，也不声明 causal 可得性。
- `REPLAN_DECIDED` 表示候选已决定/待采用，`REPLAN_ADOPTED` 表示到达 planner-origin 后真正
  采用，`ROUTE_CHANGED` 记录显示变化；三者不合并成一个 `accepted`。
- revision index 的生命周期状态为 `pending/current/superseded`；当前最终包有 8 个
  superseded、R9 current、到达态无 pending。pending route 不替换 current route，当前路段
  来自正式 motion/ETA，独立于 routePolyline 图层开关。
- C 并行边界保持不变：一个 C request 内只并行 fastest、low_risk、recommended；tick、四层
  barrier、B build、switch/adoption gate 严格串行。`effective_workers=3` 是最大同时容量，
  9 个 PID 是三次调用的累计 provenance。
- B-spline 仍是 D display-only 绘制；waypoint、ETA、risk、route metrics、adoption、hard gate
  和 authoritative motion 不变。局部放大、曲率半径与最大偏离用于解释，不用于“肉眼更弯”。
- B `risk-explanation.v1` 是 optional sidecar；transport 曾在中间 holdout 身份闭合，但当前
  原始冻结 RiskWindow 的精确 A source trace 已退役，默认包不携带 sidecar。D 显示
  `Explanation unavailable`，不计算 contributor、不填 reason、不改变 risk layer/route/
  simulation。

## 8. 实验 / 备选方案（2026-09-01 22:52 +08:00）

| 方案 | 结果 | 决策 |
|---|---|---|
| 复用 Summer causal replay 补 Winter 事件 | identity、时间窗和 route 不一致 | `REJECTED` |
| 手工制造 `PLAN_COMPUTED/REPLAN_*` | 违反真实事件来源门禁 | `REJECTED` |
| 同一 runtime store 重跑 | B immutable query pointer 冲突 | `REJECTED`；改用隔离输出根 |
| 真实 holdout retrospective dynamic replay | 145 RiskFrame、3 snapshots、17 events、3 revisions、无 blocker | `ADOPTED`，明确 post-hoc |
| strict causal Winter window | issue-time 晚于 simulation start | `PENDING / FAIL_CLOSED`，不改标签 |
| C 3-worker ProcessPool | 真实三次 planning call，每次 3 tasks，max simultaneous=3 | `ADOPTED`；池生命周期为单次 C invocation |
| 放大 B-spline 平滑幅度 | 会改变几何/安全解释 | `REJECTED` |

## 9. 权威运行 / 真实验证（2026-09-01 22:52 +08:00）

本轮真实运行使用：

```text
replay_id       = winter-retro-holdout-resource-v4
scenario        = tromso_isfjorden_winter_holdout_20260222_v1
mode            = retrospective_dynamic_replay
simulation      = 2026-02-22T00:00Z → 2026-02-22T12:00Z (6h ticks)
risk window     = 2026-02-22T00:00Z → 2026-02-28T00:00Z / 145 frames
snapshots       = 3
events          = 17
C candidates    = 3 computations / 3 accepted / 0 rejected
C parallel      = requested 3 / effective 3 / max 3 / 12 calls / 36 tasks
planning wall   = 382.1 s; total wall = 532.6 s; blockers = []
```

导出最终 `winter-viewer-sha256-311952dbe42f8d01e9f29fa974d2d53a96f9de823cdca32af18100a20bf78098`
后，Firefox 真实 DOM 检查得到 route status
`权威路线运行中`，事件文本包含 `R2 待采用`、`R2 已采用`、`R3 待采用`。这证明 Viewer
消费了真实事件/资源，不证明历史当时 causal 可得性或实船资格。

B 同次公式求值生成的 explanation transport 也通过了真实 readback：manifest
`risk-window-sha256-6ebe9d4560d04dc01b27bba2239af7f0f9a96dc779aaaad0d2ad17619700ee7c`
（manifest SHA `9f25d90b372190c36f40f6121821f89f8c1b6ff3afed3fd41ef34489607b37b6`）绑定该
RiskWindow，artifact 为
`risk-explanation-sha256-28a2329d38e98540be23e8756d6314874dcb13d4e482c70876cfabb7e31ef39c`。
145 帧逐格统计为 `COMPLETE=29,433`、`PARTIAL=17,402`、`UNAVAILABLE=2,610`；选中
77.3°N/17.2°E 格点在 Firefox 中显示 `PARTIAL/MISSING_DATA` 及 B producer 提供的缺测项。

验证等级与结果：

- O：Ruff 全通过；核心单测 24 passed。
- B：默认网格语义 2 passed；risk explanation/store + 集成定向 9 passed。
- C：端点、四层、重规划、formal ingress 44 passed。
- D：unit 105 passed / 1 causal-only skipped；Firefox 344px/528px layout PASS；动态事件
  DOM PASS；risk 145 帧、候选 12、formal motion 4 records；真实 v7 sidecar 格点解释
  `PARTIAL/MISSING_DATA` PASS。
- O formal integration：最终工作树已重新执行 v2/v3 两个参数用例，结果
  `2 passed, 1 warning`、exit code `0`、1009.42 秒；warning 仅为缺少可选 ecCodes。

## 10. 性能分解（2026-09-01 22:52 +08:00）

| 指标 | Before | After | Delta / 判断 |
|---|---:|---:|---|
| C objective 并发可观测性 | 配置/历史基线，formal report 不稳定 | requested/effective/max = 3；36 tasks | `IMPROVED`；语义证据完整 |
| v3→v4 同输入 replay wall | 539.0 s | 532.6 s | −6.4 s；机器噪声，`NOT BENCHMARKED` |
| C planning wall（v4） | N/A | 382.1 s | 真实运行观察，不作 speedup 声明 |
| Viewer export | N/A | 约 2.1 s | presentation assembly 工程观察 |
| Risk timeline | 窄侧栏压缩到不可见 | 145×8px ticks、3.35px bars | `EXPECTED FIX`，未改变数值 |
| RSS | 无本轮可比基线 | 1750.8 MB peak | 未越过本轮观察范围；无 OOM |

并行优化的目标是恢复 RC2 三目标并行和可审计性，不是改变路线结果；serial/parallel 语义
逐位一致的历史 benchmark 仍作为继承证据，最新补丁后未做 twin-run。

## 11. 正确性 / 验证（2026-09-01 22:52 +08:00）

| 验证项 | 结果 | 等级 |
|---|---|---|
| ExecutionSpec v1/v2 + schema | 通过 | `UNIT_PASS` |
| ProcessPool install/restore/profile | 5 passed | `UNIT_PASS` |
| Replay navigation/schema/coverage | 24 项定向通过 | `UNIT_PASS` |
| B grid fail-closed semantics | 2 passed（含预期 `allowed_region_has_no_grid_node`） | `INTEGRATION_PASS` |
| B risk-explanation/store integration | 9 passed | `INTEGRATION_PASS` |
| C endpoint/layer/replan/formal ingress | 44 passed | `INTEGRATION_PASS` |
| D Viewer unit | 105 passed / 1 skip（缺 replay events 的旧 fixture） | `UNIT_PASS` |
| Real Winter replay | 3 snapshots、17 events、3 revision resources；blockers=[] | `REAL_E2E_PASS`（retro scope） |
| Route integrity | 12/12 per revision；formal motion 4 records | `AUTHORITATIVE_PASS`（C artifact scope） |
| Browser layout | 344px 与 528px 均 PASS；green/yellow visible | `REAL_E2E_PASS` |
| Browser dynamic event text | pending/adopted/pending 与 authoritative status 可见 | `REAL_E2E_PASS` |
| Strict causal Winter | 未运行/不可满足 issue-time gate | `NOT RUN / FAIL_CLOSED` |
| B/C/D scientific calibration | 未建立 | `NOT APPLICABLE / PROHIBITED` |

## 12. 确定性 / 可复现性（2026-09-01 22:52 +08:00）

本轮同输入 v3/v4 的 C route semantic digest、candidate cardinality 和业务事件序列保持一致；
RiskFrame semantic digest 为 `5f5350cec8a01cb00e32d39b634daef5d7a2f8ce0091a9046d5194c165f2f250`。
v4 每个输出仍以 canonical content digest 命名，index digest 为
`c6f83183e5a90adee7d6994ebc3500909b8de12c8023e2f3e5974796bed444bf`。

状态：`PARTIAL / INHERITED`。历史 serial/parallel equivalence 与旧 replay determinism 继承；
本轮没有在最终 state-telemetry patch 后执行独立双跑。允许变化的字段是 wall-clock、created_at
和 worker PID；route/risk/content identity 不应随这些字段变化。

## 13. 构件 / 溯源（2026-09-01 22:52 +08:00）

| 构件 | 路径 / digest | Tracking | 溯源 |
|---|---|---|---|
| Replay manifest | `/tmp/winter-retro-resource-v4/winter-retro-holdout-resource-v4/causal-replay-manifest.json`; SHA `440e69c6...` | runtime / ignored | 3,707 real A records；B/C replay |
| Plan revision index | `planning-revisions/index-c6f831...444bf.json` | runtime / ignored | C 3 revision resources；rev1 superseded/rev2 current/rev3 pending |
| Default Viewer bundle | `work_package_d/viewer/bundle.json`; 74,700,038 bytes；SHA `558731d2a6485bf2ea403838e00e92e3daf776992d712d1eb8ffc60567b0833a` | ignored runtime | assembly `winter-viewer-sha256-311952dbe42f8d01e9f29fa974d2d53a96f9de823cdca32af18100a20bf78098` |
| Combined manifest | `work_package_d/viewer/winter-combined-viewer-manifest.json` | ignored runtime | identity/checksum transport；含真实 B explanation transport |
| B explanation manifest | `/tmp/winter-b-explanation-v4-exact/risk-explanation/manifests/risk-window-sha256-6ebe9d4560d04dc01b27bba2239af7f0f9a96dc779aaaad0d2ad17619700ee7c.json`; SHA `9f25d90b...b37b6` | B runtime / ignored | 同 RiskWindow identity；Orchestrator readback PASS |
| B explanation artifact | `/tmp/winter-b-explanation-v4-exact/risk-explanation/artifacts/risk-explanation-sha256-28a2329d38e98540be23e8756d6314874dcb13d4e482c70876cfabb7e31ef39c.json` | B runtime / ignored | content-addressed；145 frames；逐格状态由 B 生产 |
| RiskWindow | `risk-window-sha256-6ebe9d4560d04dc01b27bba2239af7f0f9a96dc779aaaad0d2ad17619700ee7c` | runtime | 145 formal `bc.risk-frame.v2` frames |
| DatasetBundle | `a-bundle-0ffa8463fa7e05cfd14fa0f8` | real source/runtime copy | Winter holdout, 12 required types |
| Formal motion | `route-motion-set-sha256-940ed349...` / 4 records | runtime / ignored | C `cd.route-motion-set.v1`; GEBCO declaration |
| Browser proof | `/tmp` logs + default Viewer | ignored/runtime | Firefox 344/528 layout + dynamic DOM |

默认 `viewer/index_self_contained.html` 已由当前 bundle 重新嵌入；这些二进制/JSON runtime
输出没有提交到 Git，也没有替换 frozen artifacts。

## 14. 已知限制 / 技术债（2026-09-01 22:52 +08:00）

| TD-ID | Impact | Severity | Next action |
|---|---|---|---|
| TD-DYN-01 | Winter 是真实数据但非历史 causal 可得性；不能作 navigation-grade claim | High | 取得 issue-time 可追溯的 causal window，再单独跑 strict replay |
| TD-DYN-02 | 当前原始冻结身份缺 B explanation sidecar；consumer/transport 在其他身份已验证 | Open / Low | 只有恢复精确 A source trace 或重新形成同次 B trace 才能发布；不得跨身份复用或反推 |
| TD-DYN-03 | `persistent` pool 目前是单次 C planning invocation 生命周期，不跨所有 ticks 常驻 | Low/Medium | 若需 run-lifetime pool，先评估 commit identity、cache、内存和取消契约 |
| TD-DYN-04 | 最终工作树 O formal integration | Resolved | 2 个参数用例均 PASS；exit 0；1009.42 秒；仅缺可选 ecCodes warning |
| TD-DYN-05 | B `demo_unvalidated`，C motion 为工程参考模型 | High | 保持 `navigation_use=prohibited`，建立 calibration/qualification evidence |

**Unexpected Findings / Corrections**

```text
旧声明：Winter 缺少动态事件只是 Viewer 没有指向正确 replay。
新证据：旧默认 package 没有同身份 replay source；Summer source 不能混用。
修正声明：先发布明确标注的 retrospective dynamic replay；strict causal 继续 fail closed。

旧实现假设：累计 worker PID 数可以直接作为 effective_workers。
新证据：三次调用产生 9 个不同 PID，但每次同时只有 3 个目标 worker。
修正声明：effective_workers=max simultaneous pool=3，PID 只作 provenance。

旧制品状态：rev1/rev2/rev3 index entries 都是 pending。
新证据：真实 REPLAN_ADOPTED 后旧 current 未转 superseded。
修正声明：runner 在 adoption 时迁移 superseded/current/pending，并重新生成 index。

断线重跑：复用旧风险 store 触发 immutable query pointer conflict。
修正声明：保留旧目录，使用新的隔离 runtime root；没有删除或覆盖旧不可变构件。
```

## 15. 决策 / 下一阶段（2026-09-01 22:52 +08:00）

本轮状态从“默认 Viewer 无真实重规划资源、C 并行证据不完整”推进到：

```text
ENGINEERING_DYNAMIC_VIEWER = COMPLETED / REAL_E2E_PASS
C_RC2_3_WORKER_FORMAL_PATH = RESTORED / REAL_RUN_PASS
WINTER_CAUSAL_QUALIFICATION = BLOCKED_BY_ISSUE_TIME / FAIL_CLOSED
```

下一阶段按以下顺序推进：

1. 获取 issue-time、publication-time 和完整 12 类覆盖均可审计的 Winter causal window；
   仅在门禁通过后发布 causal replay，不改变 retrospective 包的标签。
2. 维持 B 真实、不可变、同 RiskWindow identity 的 `risk-explanation.v1` sidecar 发布链；
   如需减少 `PARTIAL/UNAVAILABLE`，由 B/A 先补充可审计输入覆盖，D 继续只消费 producer 字段。
3. 在资源允许时重跑 O full integration/twin-run，核对最终返回码、serial/parallel
   semantic digest、RSS 和取消恢复。
4. 若要把并行池扩展到 run-lifetime，先提交 lifecycle/backpressure/memory/determinism
   方案；本轮不擅自改变边界。

明确不要做：把 post-hoc replay 改名 causal、把缺 explanation 填成 reason、为了视觉更弯
而放大 B-spline、修改风险公式/阈值/C 路线语义、覆盖 frozen artifact，或以本工程证据宣称
实船/导航资格。
