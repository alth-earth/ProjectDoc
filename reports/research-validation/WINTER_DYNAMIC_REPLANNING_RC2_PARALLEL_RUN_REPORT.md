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
Last Verified: 2026-09-02 02:40 +08:00
Related Canonical Docs:
  - ../../current/CURRENT_STATUS.md
  - ../../current/CURRENT_ROADMAP.md
  - ../../standards/AGENT_DOCUMENTATION_RULES.md
---

# Winter 动态重规划与 C RC2 三核并行工程运行报告（2026-09-01 22:52 +08:00）

## 0. 2026-09-02 原始冻结身份最终到达态增量（取代下文 v4/v7/v13 中间数值）

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
