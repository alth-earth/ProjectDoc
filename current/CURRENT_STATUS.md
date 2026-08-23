---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
  - PLANNED
Document Role: CANONICAL
Scope: whole-project current state
Canonical For: current phase, capability evidence, blockers, and ownership
Branch: research-validation-system
Last Verified: 2026-08-23
---

# 研究验证系统当前状态

## D 风险解释消费者门禁（2026-08-23 21:51 +08:00）

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| D 可选消费者 | BROWSER_E2E_PASS | 合成 sidecar + 真实 Winter base；missing/invalid/PARTIAL/COMPLETE；Firefox 点击格点面板 |
| RiskFrame 权威性 | PRESERVED | level/score/confidence 只读 `bc.risk-frame.v2`；risk/route/simulation 不变 |
| 身份失败关闭 | PASS | schema、RiskWindow、RiskFrame、网格/坐标不匹配时拒绝 sidecar |
| 浏览器控制台/网络 | PASS | 0 错误；0 警告；8 个必需资源 HTTP 200 |
| D 回归 | PASS | `91 passed / 3 causal-replay-only skipped`；Ruff/JS 语法 PASS |
| B 生产者构件 | NOT_IMPLEMENTED | 仅合成/设计示例 fixture；无真实贡献者声明 |
| Orchestrator 不可变传输 | NOT_IMPLEMENTED | D 已接受可选字段；正式发布链尚未闭合 |

D 的 `risk-explanation.v1` 支持是可选、增量且 explanation-scope 失败关闭。sidecar 缺失或
不匹配时，Viewer 显示 `Explanation unavailable`，基础 Winter RiskFrame、route candidates
与 ETA simulation 继续工作。`PARTIAL` 不补零或自动生成 reason；`COMPLETE` 仅展示生产者
字段。浏览器 E2E 的 PARTIAL/COMPLETE 内容是明确标记的合成 B fixture，因此成熟度只
证明 D 消费者，不证明真实 B 解释已发布或经过科学验证。

## B 风险标定研究门禁（2026-08-23 20:45 +08:00）

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| 当前 B 标尺 | DETERMINISTIC_ENGINEERING_BASELINE | 11 个归一化分量的加权和；`demo_unvalidated` |
| 科学标定 | NOT_ESTABLISHED | 无专家/结果/物理阈值验证 |
| 冬季有限分布 | REAL_ARTIFACT_AUDIT_PASS | 均值 `0.119016`；P95 `0.226415`；93.069778% L1 |
| 阈值变更 | NOT_APPROVED | `0.2/0.4/0.6/0.8` 保持冻结基线 |
| 分量归因 | PRODUCER NOT_IMPLEMENTED | RiskFrame 无逐格贡献；D 可选消费者已 BROWSER_E2E_PASS（合成 fixture），sidecar 合约仍为 DRAFT |
| B/C/D 运行时语义 | PRESERVED | 零代码、零构件修改；C 路线响应证据继承 |

当前 `risk_score` 只能解释为加权归一化风险指数，不是事故概率或经过实船结果
标定的严重度。等宽 level 策略对本冬季分布存在明显压缩，但这不足以单独批准新阈值。
下一门禁是定义 operational target、建立跨场景 calibration dataset、发布 B-owned shadow
component contribution，并比较 expert/physics/statistical/outcome-based 方法。

支持证据：

- [风险标定研究](../reports/research-validation/RISK_CALIBRATION_RESEARCH_REPORT.md)

## 冬季组合研究查看器（2026-08-23 20:14 +08:00）

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| 冬季组合展示 | REAL_E2E_PASS | 单一 scenario/run/bundle/RiskWindow/candidate 身份；145 帧；12 条路线 |
| D 冬季研究视图 | REAL_E2E_PASS | Firefox；风险/硬约束/路线/船舶/运行/暂停/图层选择器 |
| 浏览器控制台/网络 | PASS | 0 错误；0 警告；8 个必需资源 HTTP 200（含可选消费者验证器） |
| 航行仿真 | EXPERIMENTAL / REAL_E2E_PASS | 3,206 个 1 分钟状态；C 所选路线航路点 ETA 投影 |
| 冬季因果回放/重规划 | NOT_IMPLEMENTED | 无同身份 manifest/快照/事件；未伪造 |
| A/B/C/合约/冻结构件 | PRESERVED | 本轮零修改、零重算 |

当前 Viewer 已不再混用 Summer replay 与 Winter candidates。Orchestrator 失败关闭绑定
active DatasetBundle、RunContext、145 帧提交态 RiskWindow、C v3 方案集、12 条路线
candidate sidecar 与完整性证据；D 再次校验组合身份，并显式显示 scenario、
DatasetBundle、RunContext、RiskWindow 与 assembly ID。航行时间线来自 C 全航程
recommended waypoint ETA，`source_replay=null`，因此该里程碑证明冬季研究
航行仿真，不证明冬季因果回放或动态重规划。

支持证据：

- [冬季组合 Viewer 集成](../reports/research-validation/WINTER_COMBINED_VIEWER_INTEGRATION_REPORT.md)

## D 研究可视化第一阶段历史门槛（2026-08-23 16:59 +08:00）

> 该表记录第一阶段结束时的状态；当前组合 Browser 状态以上方最新里程碑为准。

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| B→C 接口 | STABLE | `bc.risk-frame.v2` 提交窗口边界；unknown 失败关闭 |
| C→Orchestrator 接口 | STABLE | 真实 Winter `cd.four-layer-route-plan-set.v3`；4×3 原子发布 |
| Orchestrator→D 接口 | STABLE | `presentation.route-candidates.v1` 精确投影；不重排/不重算 |
| D 研究视图 | IMPLEMENTED / UNIT_PASS | 4 层选择器、3 目标对比、构件指标、候选几何 |
| 既有冻结 Viewer 回退 | BROWSER_E2E_PASS | Firefox；NOT_PUBLISHED → `SINGLE_ROUTE_FALLBACK`；控制台 0；必需资源 HTTP 200 |
| 冬季组合 Viewer | NOT_IMPLEMENTED | 尚无同一 Winter 身份的 risk/replay/candidate 组合 bundle |

D 现在只在完整、scenario 匹配的 12 路线 PUBLISHED 包下启用研究视图；
用户路线选择是 display-only 高亮，不修改 C 的 `selected_candidate_id`。缺失
sidecar、4×3 不完整、metrics/geometry 非法、硬约束违规或 scenario 不匹配均失败
关闭回到现有权威路线。真实 Winter sidecar 的 metrics/identity 已由 78 项 D
测试验证；现有 48h 冻结 bundle 的 Operational Replay 由 Firefox 复测通过，但由于尚无
冬季组合 bundle，本轮不得声明 Winter Research Browser E2E。

支持证据：

- [B/C/D 接口状态](../reports/research-validation/B_C_D_INTERFACE_STATUS.md)

## 冬季 C 验证与 D 并行接口门禁（2026-08-23 10:20 +08:00）

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| A/B 冻结输入 | PRESERVED | bundle、RunContext、ExecutionSpec、145 帧 RiskWindow 身份不变 |
| C 冬季消费者 | PASS | 精确提交窗口、正式溯源、31×11 端点映射 |
| C 冬季验证 | COMPLETED / EXPERIMENTAL | `cd.four-layer-route-plan-set.v3`；4×3=12；完整性 12/12 PASS |
| 冬季路线决策 | OBSERVED_CHANGE | 对比夏季权威初始：11/22 航路点不同，+11.658 km，+2.951 h |
| C→D 候选 sidecar | INTERFACE_PASS | `presentation.route-candidates.v1` 已发布；12 个候选；失败关闭回退保留 |
| D 并行开发 | READY | D v3 加载器 4 层/12 方案；规范风险指标摄取 PASS |
| D 冬季可视化 | PHASE_1_UNIT_PASS | 候选地图/对比已实现；组合 bundle 与 Winter Browser E2E 未完成 |

本轮首次完成真实 Winter C 正式 v3 规划。推荐线为 921.379560 km、53.405581 h，
avg/max 风险为 0.105651/0.189369。Summer Viewer 未发布路线级风险指标，故只对
有证据的 geometry/distance/ETA 做比较；不补造 Summer 风险数值，也不把观察性差异写成
已隔离的季节因果。

支持证据：

- [冬季 C 冒烟](../reports/research-validation/WINTER_C_SMOKE_REPORT.md)
- [冬季 C 路线验证](../reports/research-validation/WINTER_C_ROUTE_VALIDATION_REPORT.md)
- [D 接口就绪](../reports/research-validation/D_INTERFACE_READY_REPORT.md)
- [冬季数据可用性跟进](../reports/research-validation/WINTER_DATA_AVAILABILITY_FOLLOWUP.md)
- [冬季 C 最终报告](../reports/research-validation/WINTER_C_VALIDATION_FINAL_REPORT.md)

## 冬季 B 首次科学运行（2026-08-23 02:44 +08:00）

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| 冬季 DatasetBundle | FROZEN_ARTIFACT_READY | active `a-bundle-a2146dd0adbaa7db77a6beb7`，1,212 条记录，SHA/摘要不变 |
| A→B 正式交接 | READY_FOR_B_VALIDATION | 固定 RunContext/ExecutionSpec，精确 bundle 输入恢复 PASS |
| B 冬季验证 | COMPLETED / EXPERIMENTAL | medium 31×11；145 个正式 `bc.risk-frame.v2`；schema/存储/回读 PASS |
| 冬季风险分布 | OBSERVED_CHANGE | 夏季/冬季相同 realized 网格对比可用；有限均值 `0.045027961 → 0.119015786` |
| 未知可航行节点 | 观察到 0 | Winter `unknown_navigable_nodes=0`；硬约束/原因一致性不匹配 `0` |
| C 冬季验证 | NOT_STARTED | 本轮明确未运行 C 规划器 |
| D 冬季可视化 | NOT_STARTED | 本轮明确未运行 D/Viewer |

当前结论：冬季 B 已完成第一轮工程/研究验证，证明在相同 medium realized 网格、逐小时
时间间隔和 B 模型配置下，冬季输出风险分布发生变化。B 模型仍是
`demo_unvalidated`，且夏季/冬季数据源体系不同，因此该结果不是科学标定或仅由冬季
月份导致的因果结论。`DATA_UNAVAILABLE` 必须与有限风险分布分开解读。

支持证据：

- [冬季 B 基线决策](../reports/research-validation/WINTER_B_BASELINE_CONFIG_DECISION.md)
- [冬季 B 冒烟报告](../reports/research-validation/WINTER_B_SMOKE_REPORT.md)
- [冬季风险分布审计](../reports/research-validation/WINTER_RISK_DISTRIBUTION_AUDIT.md)
- [冬季 B 验证报告](../reports/research-validation/WINTER_B_RISK_VALIDATION_REPORT.md)

## 冬季正式交接里程碑（2026-08-23 01:16 +08:00；B 首轮结果见上方最新里程碑）

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| 冬季必需覆盖率 | 12_OF_12_COMPLETE | 1,212 条记录的冻结 A bundle |
| 冬季 DatasetBundle | FROZEN_ARTIFACT_READY | active `a-bundle-a2146dd0adbaa7db77a6beb7`；144 h 最小；解析/摘要/doctor 通过 |
| 冬季 RunContext | PUBLISHED / SCHEMA_PASS | `run-441b03c8-d45b-5414-b0e8-b7fd0d990c22`；官方原子生成器 |
| 冬季 ExecutionSpec | PUBLISHED / SCHEMA_PASS | 严格 `orchestrator.execution-spec.v1`；身份对齐 |
| A→B 正式交接 | READY_FOR_B_VALIDATION | 精确归档仅摄取 PASS；B 未开始 |
| 交接时的冬季 B/C/D | NOT_STARTED | 交接完成时的下游起点；B 首轮结果见上方最新里程碑 |

当前交接里程碑结论：冬季数据源采集、修正后的 A 不可变 bundle、匹配的 `RunContext.v2`、
严格的 `ExecutionSpec.v1` 以及 Orchestrator 仅摄取全部通过。该阶段只完成摄取；
后续 B 首轮结果见本文件顶部最新里程碑。旧的 132 小时最小 bundle 继续作为被取代的
历史证据保留。

支持证据：

- [冬季数据源验证](../reports/research-validation/WINTER_SOURCE_VALIDATION_REPORT.md)
- [气象数据源对比](../reports/research-validation/WINTER_MET_SOURCE_COMPARISON.md)
- [冬季身份审计](../reports/research-validation/WINTER_EXPERIMENT_IDENTITY_AUDIT.md)
- [冬季交接验证](../reports/research-validation/WINTER_HANDOFF_VALIDATION_REPORT.md)
- [冬季不可变 bundle 重新发布](../reports/research-validation/WINTER_BUNDLE_REISSUE_REPORT.md)
- [冬季正式交接](../reports/research-validation/WINTER_FORMAL_HANDOFF_REPORT.md)

接口稳定化结论：A→B `DatasetBundle.v2 + RunContext.v2`、B→C
`bc.risk-frame.v2 + committed hourly window`、C 正式 v2/v3 与 Orchestrator→D
展示基线均可保持现有版本。冬季 B 验证必须先审计 unknown 是否被
正确硬掩膜；C route candidates 在 Replay Viewer 仍为 `NOT_PUBLISHED`。

## 第三阶段真实实验结果（2026-08-22 02:34 +08:00）

> 历史第三阶段检查点；上方的冬季身份门禁才是当前状态。

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| 冬季 Copernicus 采集 | PARTIAL / 8_TYPES_DOWNLOADED | 1,064 条目标窗口记录、八个不可变源快照、精确端点 |
| 冬季 12 类 A 覆盖率 | PARTIAL / 9_OF_12_COMPLETE | 八个 Copernicus 行 + 缓存的 GEBCO 掩膜完整；bundle 未持久化 |
| 冬季 GFS | BLOCKED_BY_SOURCE_AND_CADENCE | NCEI 202602 object/THREDDS 路径缺失；直接清单 404；6 h 适配器 vs 3 h 覆盖率门控 |
| A 归档完整性 | VALIDATED | doctor 检查 5,232 项，0 错误，0 警告 |
| C 精确采样画像 | EXPERIMENTAL / REAL_B_FRAME_PASS | 705,469 请求；242,992 次精确重复；34.444% 复用上限 |
| C 有界 LRU | IMPLEMENTED / EXPERIMENTAL_DEFAULT_OFF | 5 万上限；中位数 76.281 s → 65.012 s；完整路线摘要不变 |
| B-C 优化 medium 路径 | EXPERIMENTAL / VALIDATED | 固定 B 输入与端点；每模式 3 次独立运行；无合约/发布变更 |

在此历史检查点，尚无冬季 DatasetBundle、RiskFrame、路线或 Viewer 构件。C LRU
仅通过实验基准可用，不用于正式入口。未运行完整 48 小时回放、重型集成与
确定性双跑。

## 第二阶段真实实验结果（2026-08-22 01:11 +08:00）

> 历史第二阶段检查点；上方第三阶段表格才是当前状态。

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| 冬季 12 类可行性 | BLOCKED_BY_DATASET | 全部 12 个本地目标走廊行均无 2026 年 2 月记录；未下载/未伪造 |
| B 正式固定网格对比 | EXPERIMENTAL / REAL_DATA_PIPELINE_PASS | 16×7、31×11、60×21 各 78 个正式帧；B 构建 4.03/3.86/3.91 s |
| B→C 耦合基线 | EXPERIMENTAL / REAL_B_FRAMES + REAL_C_SEARCH_PASS | 推荐路线在 112 节点时 10.51 s，341 节点时 75.00 s |
| C 缓存可观测性 | IMPLEMENTED / UNIT_PASS | 既有边几何缓存报告命中/未命中/条目；行为不变 |
| 路线候选展示 | DRAFT / PLANNED | 向后兼容提案；当前 bundle 仍为 NOT_PUBLISHED |

正式 B 对比因冬季数据受阻而使用既有夏季归档，其输出未发布到 B 存储。
C 基准解码公共 `bc.risk-frame.v2` 文档并运行真实 C 组件，但未经过提交窗口的正式入口；
它是实验性耦合证据，而非完整集成声明。

## 第二阶段加速结果（2026-08-22 00:24）

> 历史准备阶段检查点；上方第三阶段表格取代其冬季与缓存就绪行。

| 工作流 | 当前状态 | 证据 |
|---|---|---|
| P0 合约登记 | IMPLEMENTED / DOCUMENT_VALIDATED | 归属/版本/状态登记、提案模板、开发归属矩阵 |
| P1 冬季配置 | IMPLEMENTED / UNIT_VALIDATED | 新 `scenario.v2` 身份；合约 19 PASS |
| P1 冬季数据/构件 | BLOCKED_BY_DATASET | 无匹配的 12 类源 bundle；未伪造冬季构件 |
| P2 B 固定网格实验 | EXPERIMENTAL / UNIT_VALIDATED | 合成核 + 正式 78 帧对比；B 61 项非集成 PASS |
| P3 C 组件画像 | EXPERIMENTAL / UNIT_VALIDATED | 组件画像 + 真实帧 BC 基准；C 146 项非集成 PASS |
| P3 边几何缓存身份 | IMPLEMENTED / UNIT_VALIDATED | 缓存键现包含样本数；含定向回归 |
| P4 专业导航辅助 | IMPLEMENTED / BROWSER_E2E_PASS | Firefox：经纬网格、坐标标签、比例尺、格北、独立开关 |

本轮未改动任何核心合约版本、A 采集实现、B 风险公式/等级策略、C 搜索算法/路线语义、
Orchestrator 导出、冻结构件或 48 小时回放。

## 当前阶段（2026-08-21 23:18）

项目已从 Competition Demo Freeze 转入 **研究验证系统增强阶段**。冻结演示基线保留在
`demo-engineering`，当前开发只在 `research-validation-system` 进行。这个阶段先冻结接口
事实和验证口径，再开展 B/C/D 并行研究；不把规划中的冬季场景、自适应网格或候选路线
展示写成已有能力。

| 分支 | 含义 | 状态 |
|---|---|---|
| `main` | RC1 基线 | FROZEN |
| `rc2-development` | RC2 基线 | FROZEN |
| `demo-engineering` | 竞赛演示基线 | FROZEN |
| `research-validation-system` | 研究验证增强 | ACTIVE |

`/root/my_project` 是多个仓库的工作区，当前没有 root Git。各子仓库分别维护自己的
`research-validation-system` 分支。

## 当前真实架构（2026-08-21 23:18）

| 模块 | 研究阶段角色 | 运行时边界 |
|---|---|---|
| A | 环境数据采集 | 发布 `PreparedWindow` / `a.dataset-bundle.v2` 与溯源 |
| B | 风险评估与预报 | 消费 A 公共 bundle，发布 `bc.risk-frame.v2` |
| C | 风险感知导航决策 | 消费 B risk frame，发布 route plan / layered route set |
| D | 可视化与验证平台 | 只消费已发布 presentation artifact；唯一 Viewer 运行时 owner |
| Orchestrator | 流水线 / 构件 / 展示适配器 | 编排 A→B→C，执行 replay，验证并投影展示 bundle |

```text
A PreparedWindow / DatasetBundle.v2
  -> B BInputEnvelope / bc.risk-frame.v2
  -> C RiskSourcePlanningIngress
  -> cd.route-plan.v2 or cd.four-layer-route-plan-set.v3
  -> Orchestrator replay/presentation export
  -> replay.viewer-bundle.v1
  -> D Viewer
```

`cd.route-plan.v3` 是 four-layer v3 集合内的单路线 schema，不是顶层
ExecutionSpec planning contract。当前 Replay Viewer 消费 `replay.viewer-bundle.v1`，
不直接消费 four-layer aggregate。

## 能力与证据等级（2026-08-21 23:18）

| 能力 | 实现 | 验证 | 当前资格 |
|---|---|---|---|
| A 12 类公共数据 bundle | IMPLEMENTED | ARTIFACT_PASS | 夏季 RC1/RC2 + active Winter 144 h 最小冻结 bundle |
| B 逐小时确定性风险帧 | IMPLEMENTED | AUTHORITATIVE_PASS | 模型仍为 `demo_unvalidated`，不是科学标定结论 |
| B 固定目标网格 | IMPLEMENTED | UNIT/ARTIFACT_PASS | RC2 显式 31×11；代码默认配置可为 16×7 |
| B 自适应网格 | NOT_IMPLEMENTED | NOT_RUN | 研究计划，不得隐式改变 C regular-grid contract |
| C 三目标 | IMPLEMENTED | AUTHORITATIVE_PASS | fastest / low_risk / recommended |
| C 四层 × 三目标 | IMPLEMENTED | AUTHORITATIVE_PASS | `FourLayerRoutePlanSet.v3` 明确验证 12 路线 |
| C 因果回放规划 | IMPLEMENTED | AUTHORITATIVE_PASS | 12h 确定性继承；48h 产品构件已验证 |
| D 展示 Viewer | IMPLEMENTED | BROWSER_E2E_PASS | Firefox；单一 Simulation Clock；artifact driven |
| 48h 回放 Viewer | IMPLEMENTED | BROWSER_E2E_PASS | 49 快照、2881 分钟状态、49 风险帧 |
| C 路线候选展示 | IMPLEMENTED | INTERFACE_PASS | 真实 Winter 12 路线 sidecar 已发布；既有冻结 Viewer bundle 仍保持 NOT_PUBLISHED |
| 冬季场景配置 | IMPLEMENTED | CONFIG_VALIDATED | 144 h scenario；12/12 源行完整 |
| 冬季 DatasetBundle | IMPLEMENTED | FROZEN_ARTIFACT_READY | active bundle ID/digest/SHA 已冻结；最小/请求视界均为 144 h |
| 冬季 A→B 交接 | IMPLEMENTED | READY_FOR_B_VALIDATION | RunContext/ExecutionSpec/schema/精确仅摄取 PASS |
| 冬季 B RiskFrame / C/D 构件 | B,C,D_IMPLEMENTED | B,C_FORMAL_VALIDATED / D_REAL_E2E_PASS | B 145 帧；C 12 路线 v3；D 组合 Firefox PASS |
| B 固定网格实验平台 | IMPLEMENTED | UNIT_PASS / EXPERIMENTAL_REAL_DATA | 正式 builder 对比已完成；输出仍未发布 |
| C 组件画像 / BC 基准 | IMPLEMENTED | UNIT_PASS / EXPERIMENTAL_REAL_DATA | 真实 B 帧与真实 C 搜索；提交态入口未演练 |
| D 专业导航辅助 | IMPLEMENTED | BROWSER_E2E_PASS | 仅 bundle 元数据；规范变换/纵横比保留 |

## 冻结语义（2026-08-21 23:18）

- A→B 只通过公共 `PreparedWindow` / `DatasetBundle.v2` 和匹配的
  `RunContext`；B 不扫描 A 私有 cache、SQLite 或 raw 目录。
- B→C 以 `bc.risk-frame.v2` 为正式边界；unknown 失败关闭，
  `DATA_UNAVAILABLE != safe`。
- C 拥有最终路线、速度、ETA 和重规划决策；D 不重新计算。
- `REPLAN_DECIDED != REPLAN_ADOPTED`，pending route 不提前替换权威
  route，completed track 追加写。
- D 是唯一 Viewer 运行时 owner；Orchestrator 只拥有 replay 与展示
  adapter/export。
- 当前正规网格是 rectilinear regular grid。Adaptive Grid 在 contract proposal
  通过前只能作为隔离实验。

## 当前事实缺口（2026-08-21 23:18）

1. Contract ownership registry 已建立；尚待各 owner 对未来 candidate/adaptive
   proposal 逐项审批，registry 本身不等于提案批准。
2. C→D 已发布一个真实 Winter 12 路线候选集；replay 的 19 个时间修订仍不是
   19 组候选。多决策候选集时间线尚未定义。
3. 冬季场景、12 类源行、144 h 最小冻结 bundle、匹配的
   RunContext/ExecutionSpec、B 145 帧 RiskFrame、C 12 路线验证与 D 组合
   Browser E2E 已建立。下一缺口是正式 Winter causal replay/replanning（若研究门槛需要）；
   当前 3,206 状态时间线是 C waypoint ETA projection。
4. B 规则模型未标定；正式固定网格 build 已测，但进程 RSS 包含已加载 A window，
   独立增量内存与重复运行方差仍未测；adaptive grid 未实现。
5. C baseline/medium 联合性能已测；medium exact-sample 50k LRU 已在 default-off
   基准中取得 14.77% 中位数收益。正式入口/12 路线提升、共享搜索与
   增量重规划均未实现。
6. D 已建立基础专业导航辅助层、研究视图、候选几何、四层三目标对比、
   冬季组合 Browser E2E 与可选逐格风险解释消费者。真实 B 贡献者
   生产者、Orchestrator 不可变传输和独立环境因子层合约仍待实现。

详细依据见
[RESEARCH_VALIDATION_GAP_ANALYSIS.md](RESEARCH_VALIDATION_GAP_ANALYSIS.md)。

## 当前阻塞与风险（2026-08-21 23:18）

| 风险 | 状态 | 处理 |
|---|---|---|
| 多人并行前合约所有权不清 | CONTROLLED | registry/模板/目录所有权已建立；breaking 提案仍需 owner 批准 |
| Winter A/B/C/D 门禁 | D_COMBINED_REAL_E2E_PASS | 正式身份、B 145 帧、C 12 路线 v3 与 D Firefox PASS；causal replay 仍未实现 |
| B 网格策略与 C regular-grid 假设耦合 | EXPERIMENTAL EVIDENCE | baseline+medium 的正式有界 build/C 对比已完成；fine 需要显式预算 |
| C 候选展示 | CONTROLLED / INTERFACE_PASS | 提案已接受；真实 Winter sidecar PASS；冻结 bundle 回退不变 |
| 当前演示基线回退 | CONTROLLED | 冻结分支/构件不改；研究构件使用新身份 |
| B Murmansk 默认网格集成预期 | OPEN FINDING | 未筛选 B 套件在 allowed-region 端点映射失败；本轮不改配置语义 |

## 正式交接验证边界（2026-08-23 01:16 +08:00）

> 本节记录正式交接当时的仅摄取边界；B 首轮结果以本文顶部的最新里程碑为准。

冬季正式身份双 schema、重建身份、run/spec 绑定与精确归档仅摄取 PASS。Contracts 19 PASS；
Orchestrator fast 84 PASS、2 deselected；两仓库 Ruff clean。最终三件套仅摄取 wall
`3:26.43`、peak RSS `978,740 KiB`。本轮没有运行 B/C/D、48h 回放、重型集成或新的
确定性双跑；这些旧证据均未提升为本轮重验。
