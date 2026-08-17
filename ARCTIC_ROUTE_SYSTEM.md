> **文档治理声明**
>
> - 本文件角色：北极航线预测驱动动态规划系统当前唯一的顶层定位、架构、运行语义与治理权威。
> - 改造时间：2026-08-15（Asia/Shanghai）。
> - 原文件去向：[ARCTIC_ROUTE_SYSTEM_归档_20260815.md](ARCTIC_ROUTE_SYSTEM_归档_20260815.md)。
> - 改造原因：落实项目负责人已定的挑战杯演示定位、D1–D7、双航区最新坐标、散货船口径和离线演示模式。
> - 事实边界：现状事实以当前代码、Schema、配置和测试为准；归档及外部附件只作来源证据。

# 北极航线预测驱动动态规划系统

## 1. 项目定位与成功标准

这是一个由 4 名学生完成的**挑战杯演示项目**，目标是稳定展示：环境数据变化后，风险图随之
变化，规划路线和指标也能合理更新。成功标准是：

- 演示流程完整、可重复、尽量可断网运行；
- 风险图和风险预测图在视觉与相对变化上基本合理；
- 航线不穿陆地、没有明显绕行或时间倒退，并大体符合现实海上航段；
- 能说明 A、B、C、D 的输入、输出和一次重规划为什么发生；
- 全部演示参数、模型和限制有明确标注，不把演示结果声称为真实导航结论。

**科学精确度、真船标定、适航认证和业务化实时运行不是挑战杯工程验收项，也不得阻塞演示。**
本系统仍禁止用于真实导航或安全决策；这一限制与“工程演示通过即成功”并不矛盾。

当前进展（2026-08-16）：**Demo RC1 Frozen Baseline 已建立**。主走廊
`murmansk_dikson_august_2026_demo_v1`（corridor 2.2.0，144 h）12 类齐全、
`complete=true`；A TOPAZ originalGrid 重建、B 风险（hard-mask=land_sea_mask_plus_unknown_v1）、
C v3 四层 + 6h 重规划、D 真实制品消费均 PASS；r6 首次完整 E2E、r7 业务级确定性复现。
精确身份见 `work_package_a/docs/DEMO_RC1_BASELINE_20260816.md`。历史基线
`tromso_isfjorden_august_2026_demo_v1` 仍保留为独立场景证据。

核心功能链固定为：

```text
arctic_route_contracts：预先准备共享走廊、场景、船型和运行身份
                              │
                              ▼
A：下载数据 → 预处理/标准化 → 持久化冻结制品
                              │
                              ▼
B：逐小时风险处理/预测 → 风险图与风险序列
                              │
                              ▼
C：按预计到达时刻采样风险 → 多目标航线 → 至少一次重规划
                              │
                              ▼
D：可视化风险图、风险预测图、候选航线和指标
```

项目负责人对 A、B、C 拥有完整决策权。文档和 AI 不再要求不存在的子项目负责人、跨专业评审组
或签字流程批准挑战杯演示。

## 2. 权威顺序与接手入口

发生冲突时按下列顺序裁决：

1. 当前公共代码、Schema、配置和生产者—消费者测试；
2. 本文件；
3. 当前 [十日计划](ABC_10_DAY_SPRINT.md)和各包 handoff；
4. [项目梳理报告](项目梳理报告.md)中的形成时点审计证据；
5. `_归档_YYYYMMDD`、`.archive-*` 归档和外部历史附件。

新成员或 AI 依次阅读：本文件 → 十日计划 → 目标包 handoff → 两侧接口文档 → 代码和测试。
若机器合同与本文件不一致，应登记并修订文档；不得自行从旧附件挑选另一套口径。

## 3. 模块边界与当前状态

| 模块 | 唯一职责 | 当前工程状态 | 挑战杯下一目标 |
|---|---|---|---|
| `arctic_route_contracts` | 共享走廊、场景、船型、时域和 RunContext | 0.3.0；corridor 2.2.0 已冻结 | 保持共享事实稳定（RC1 冻结） |
| A | 下载、留证、拆帧、标准化、QC、持久化和回放 | 0.4.2；mur RC1 数据已交付（TOPAZ originalGrid 重建） | RC1 冻结；仅 correctness/safety 修复 |
| B | 时间处理、逐小时风险、置信度、hard mask、环境速度因子 | 0.2.0；RC1 风险窗已提交（unknown-navigable=0） | RC1 冻结；hard_reason 为 POST-RC1 |
| C | 最终船速、ETA、成本、路径搜索、发布和重规划 | 0.4.0；v3 四层+6h 重规划已跑通（单目标 ≈96s） | RC1 冻结；可选性能优化 POST-RC1 |
| D | 只读展示风险、路线和指标 | 0.1.0；真实 v3 制品离线消费 + Route Geospatial Integrity gate PASS（36 tests，2026-08-17） | NEXT PHASE：GEBCO / 145-frame / Moving Ship |
| orchestrator | 只经公共 API 组织 A→B→C、报告和制品 | 阶段报告+可中断 worker 超时已实现；r6/r7 完整 E2E PASS | worker 模式全链冒烟（pre-demo） |
| experimental B | 隔离的反事实实验工程 | 工程卫生待修 | 真实主线完成后再最小修复 |

边界不变：A 不算风险，B 不生成路线，C 不下载环境数据，D 不调用 B/C 内部函数。

### 3.1 运行时身份链

一次正式运行先由共享契约物化场景，再让所有工作包传播同一身份。至少不得串线的字段包括：
`run_id`、`scenario_id`、`corridor_id`、`vessel_profile_id`、`generation`、时间窗，以及各级
内容摘要（DatasetBundle、RiskFrame、RoutePlan）。

```text
Corridor + Scenario + Vessel + HorizonPolicy
                    │
                    ▼
             冻结 simulation window
                    │
A records ──> DatasetBundle v2 ──独立复核──> RunContext v2
                    │                         │
                    └────────────┬────────────┘
                                 ▼
                    B committed RiskFrame window
                                 │
                         C execution lease
                                 │
                    RoutePlan v2 / v3 atomic set
```

任何跨包字段都要有唯一所有者和单一语义；A/B/C/D 不得通过复制 TOML 或手工拼 JSON 绕过
共享配置与公共加载器。

### 3.2 formal 与科学/校准是两条轴

`provenance`（来源/身份）与 `calibration_status`（模型/参数校准状态）必须分开表达：

| 维度 | 取值 | 含义 |
|---|---|---|
| provenance | `formal` / `synthetic` / `legacy_unverified` | 身份、时间、来源链与工程门禁是否合格 |
| calibration | `demo_unvalidated` / `experimental_unverified` / 未来的 `calibrated` | 算法与参数是否经过科学验证 |

`formal + demo_unvalidated` 是合法但受限的科研工程状态，可用于挑战杯工程验收；它绝不等于
可用于导航。`formal` 只表示运行身份、来源与工程门禁通过，不表示模型已科学校准。

### 3.3 本阶段做与不做

本阶段必须做：

- 离线复现“数据何时可见 → 风险如何变化 → 路线为何更新”；
- B 默认形成至少 24 h、并覆盖实际规划 ETA 的逐小时风险序列；
- C 按到达时刻使用对应风险，不用一张当前风险图覆盖全航程；
- D 展示最快/最短时间、低风险、综合推荐和动态重规划结果及指标；
- 保留未来接入实时源、缩短风险输出间隔和替换算法/参数的公共接口。

本阶段不做或不承诺：

- 真实业务化导航或安全决策；
- 在冰级、吃水、净空和性能模型不全时声称工程适航；
- 对所有环境变量采用统一线性外推；
- 让 D 调用 B/C 内部函数或等待持有规划锁；
- 在历史回放中提前使用模拟时刻之后才发布的数据。

## 4. 两种运行模式

| 模式 | 数据准备与时间规则 | 展示/验证目标 | 挑战杯地位 |
|---|---|---|---|
| 历史回放/验证 | 严格使用当时可见数据，要求 `issue_time <= simulation_time` | 检查未来信息泄漏、比较风险与路线变化 | 保留的工程验证模式 |
| 稳定演示 | A 预先下载、预处理并冻结到本地；运行时仍按模拟时钟、版本和代次读取 | 无网可重复展示风险变化、候选路线和至少一次重规划 | 默认比赛演示模式 |

稳定演示不要求现场下载“最新”数据。A 应提前准备与场景窗口一致的连续数据，例如为指定月份
冻结连续数日；具体长度以走廊时域为准：主走廊默认 168 h，迁移走廊默认 96 h。比赛现场
B/C/D 直接读取 A 的标准化持久化制品，不把网络可用性作为演示前提。

“数据预置”不等于把最终风险图和航线提前写死：演示运行时 B 仍生成风险序列，C 仍按模拟时钟
规划和重规划，D 展示当前代次的结果。

## 5. 时间、场景与代次语义

### 5.1 五类时间

| 字段 | 精确含义 | 不得替代 |
|---|---|---|
| `issue_time` | 从何时起系统被允许知道该数据/预报 | 不能由文件名、mtime 或 ingest 推断 |
| `valid_time` | 数据或风险描述的物理时刻 | 不是发布时间 |
| `ingest_time` | A 实际收到并登记制品的时刻 | 不决定物理有效时刻 |
| `as_of_time` | 本次 B/C 计算允许使用的信息截止时刻 | 不是算法完成时刻 |
| `generated_at` | 算法实际完成计算的墙钟时间 | 不参与模拟时间推进 |

历史回放必须保持：

```text
input.issue_time <= as_of_time <= 当前允许使用的 simulation_time
```

`valid_time` 可以晚于当前模拟时刻，因为已经发布的预报可以描述未来；关键是其 `issue_time`
在当时已经可见。稳定演示也保留这些字段，以便解释制品来源和重规划顺序。

### 5.2 `scenario_id`、`generation_id` 与版本

- `scenario_id` 标识完整演示/试验组合：走廊、船型、数据快照、时间窗和参数共同构成场景；
- `generation_id` 标识模拟时钟的一次连续代次，seek/reset 后递增；
- A、B、C、D 不得发布、消费或显示旧代次迟到结果；
- `schema_version` 描述接口结构，`model_version` 描述算法/参数，二者不能互换；
- `run_id`、corridor、vessel、各级 digest 和 generation 必须贯穿同一次演示。

### 5.3 三组缓存

| 缓存 | 内容 | 组织与保留原则 | 目的 |
|---|---|---|---|
| AB | 标准化环境帧 | 按类型/变量/时间分区；可追溯、不可变、无未来泄漏 | B 可重复读取冻结环境输入 |
| BC | 风险帧序列 | 按 `valid_time` 排序的滑动窗口，覆盖 C 实际规划窗口 | C 按 ETA 读取对应风险 |
| CD | 路线与指标 | latest 原子覆盖，并保留候选与必要历史 | D 不因 C 计算较慢而阻塞 |

## 6. A 的演示数据策略

A 的挑战杯定位是“**下载数据 + 预处理 + 标准化持久化**”：

1. 开发阶段从公开网站/API 或历史档案下载数据，保留来源和时间证据；
2. 统一变量、单位、坐标、方向、质量和时间粒度，保存为可重复读取的标准帧；
3. 按固定场景冻结 DatasetBundle/RunContext 和必要报告；
4. 比赛前完成离线复跑，比赛现场只读本地冻结制品；
5. 数据是否“刚刚发布”不重要，是否连续、匹配场景、能稳定驱动 B/C/D 才重要。

当前正式画像仍为 12 类必需环境层：陆海、海流、冰密集度、冰漂、冰缘、冰厚、冰型、温度、
能见度、水位、波浪和风场。bathymetry 与长期限制区保留为可选接口，不阻塞演示。

### 6.1 网络与下载约定（2026-08-15 起长期有效）

执行任何下载、抓取、访问任务时遵守：

1. **代理判断**：开代理不一定快，也可能直连更快。下载/访问前先判断，必要时两种方式各试
   一次，取可用且快者；明显失败时不要反复重试浪费时间。
2. **人机验证与凭证**：许多数据源有人机验证或要求登录凭证，自动化可能无法绕过。
3. **处理原则**：能自动完成的自动完成；遇到无法自动化解决的情况（验证码、凭证、封锁、
   限流等）停止重试，说明问题并给出可执行的替代方案（换数据源、换时段、手动下载的具体
   步骤），由项目负责人手动执行；需手动执行的步骤必须写清网址、点击位置、保存位置与文件
   命名。
4. **落档要求**：每次采集的网络结论、凭据使用情况与手动操作步骤写回
   [冻结演示数据集交付说明](work_package_a/docs/FROZEN_DEMO_DATASET_DELIVERY.md) 及本文件
   数据获取章节。

本批次实测：直连 NOMADS=200、CMEMS=307、GEBCO=200；本地代理 `127.0.0.1:10808` 无效，采用
直连；Copernicus 使用 `.env.copernicus` 凭据成功采集，无需人机验证。

### 6.2 冻结演示数据集（已交付）

场景 `tromso_isfjorden_august_2026_demo_v1` 已交付：12 类齐全、连续 144 h
（2026-08-11T06:00Z → 2026-08-17T06:00Z）、`complete=true`，DatasetBundle/RunContext 已生成，
并双位置备份（`frozen_demo_backup/` 与工作区内持久副本
`frozen_demo_backup_secondary/`）。交付细节、覆盖矩阵、
差距说明与恢复步骤见 [冻结演示数据集交付说明](work_package_a/docs/FROZEN_DEMO_DATASET_DELIVERY.md)。

> 2026-08-16 更正：原约定的第二位置 `/tmp/arctic_demo_backup/` 在 WSL/容器重启后被清空
> （实测 15:04 重启后消失），不能作为持久备份；第二备份改为工作区内持久路径
> `frozen_demo_backup_secondary/`（与 `frozen_demo_backup/` 同盘）。如需真正的异盘/异地
> 第二副本，需项目负责人指定持久目标路径（如外接盘挂载点），再更新本文与恢复说明。

说明：首选 168 h 因 corridor 政策上限 144 h 未达成（非数据缺失）；`ocean_current` 显式使用
detided 后备；GFS/Copernicus 部分产品为 3 h 原生步长，由 B 逐小时对齐。

### 6.3 制品生命周期与复用/失效规则

数据与中间制品按“可复用、可验证、可失效”管理：

```text
原始下载(snapshot, 不可变)
  → A ready+manifest（doctor 校验）
  → Frozen Artifact A（bundle + RunContext，哈希绑定）
  → B committed window（内容寻址）
  → C v2/v3 输出（原子发布）
  → D 只读消费
```

可长期复用：A 冻结 bundle/RunContext、已 doctor 的 source/ready、B 内容寻址 commit、C 已
校验输出。同周期开发缓存：`.uv-cache`、`.mamba-env`、`.pytest_cache`、orchestrator 阶段
临时目录。仅测试内部临时：`tmp_path` 夹具、合成 A 数据、synthetic RiskFrame。必须重新生成：
篡改/代次围栏/发布原子性测试，以及发布前干净环境全链验证。

复用必须满足失效条件，不能“目录里有文件就继续用”：

- A 冻结制品失效：A 代码/Schema、场景、走廊、船型、数据窗口或 knowledge-as-of 变化；
- B commit 失效：A bundle digest、B 模型配置 digest、B 代码、网格/时域策略变化；
- C 输出失效：B commit digest、planner/replan 配置 digest、C 算法或 Schema 变化；
- 环境缓存失效：`uv.lock`/`pyproject.toml`/`environment.yml` 变化后重新 `sync`。

所有复用以 content hash、config digest、manifest、schema version 与 provenance 为判据；
“测试产生的真实冻结制品”可以升级为正式资产，合成 fixture 永远不能。

### 6.4 项目执行时间压力原则

> 项目当前存在明显执行时间压力。在不改变功能效果、不降低正确性、不削弱可复现性和测试
> 可信度的前提下，应主动减少重复下载、重复安装、重复计算和重复执行上游工作包；优先复用
> 经过验证且带有版本、来源和有效性信息的缓存及冻结制品。任何速度优化都不得以牺牲结果
> 质量为代价。

## 7. 两条演示航线

配置真值位于 `arctic_route_contracts/configs/corridors/`，下表同时记录图中最新口径。

### 7.1 航区一：摩尔曼斯克外海—迪克森外海

| 项目 | 当前值 | 用途 |
|---|---|---|
| `corridor_id` | `offshore_murmansk_to_offshore_dikson` | 主开发与首个完整演示 |
| 配置范围 | 67.50–75.00°N，30.00–85.00°E | 数据裁剪 bbox |
| 起点建议点 | 69.15°N，33.60°E | 避开摩尔曼斯克港池内部 |
| 起点允许区域 | 68.90–69.40°N，33.00–34.50°E | 起点栅格自动修正范围 |
| 终点建议点 | 73.55°N，80.40°E | 避开迪克森港内及近岸浅水 |
| 终点允许区域 | 73.30–73.80°N，79.80–81.00°E | 终点栅格自动修正范围 |
| 默认/允许时域 | 168 h / 144–216 h | 长航线风险与规划窗口 |

端点映射只能在相应允许区域内选择同一可通航连通分量的网格点，并记录原始点、修正点、距离和
理由；不得静默吸附到区域外节点。

### 7.2 航区二：特罗姆瑟外海—伊斯峡湾外部入口

| 项目 | 当前值 | 用途 |
|---|---|---|
| `corridor_id` | `tromso_to_isfjorden_outer` | 迁移验证走廊（RC2 升 1.2.0） |
| 配置范围 | 68.50–79.50°N，10.00–22.00°E | 数据裁剪 bbox |
| 气象导航起点 | 70.50°N，18.00°E | 挪威海外海算法起点（RC2 1.2.0） |
| 起点允许区域 | 70.00–71.00°N，17.00–19.00°E | 起点匹配/栅格修正范围 |
| 气象导航终点 | 78.15°N，13.00°E | 伊斯峡湾外部入口 |
| 终点允许区域 | 77.90–78.40°N，12.00–16.50°E | 终点筛选/栅格修正范围 |
| 朗伊尔城 AIS 参考点 | 78.22°N，15.65°E | 完整航次识别，不参与优化 |
| 默认/允许时域 | 96 h / 72–144 h | 迁移与较短演示窗口 |

> 2026-08-17（RC2）数据结论：现有冻结数据在 68.5–70.4°N 全带宽（10–22°E）无可航
> 单元（多数 LAND，其余 DATA_UNAVAILABLE）；原 1.1.0 起点区域（18–20.5E/69.4–70N）
> 与 1.2.0 外海起点区域（17–19E/70–71N）均不可规划。corridor 升 1.2.0（外海起点）
> 并归档 1.1.0 事实；完成端到端迁移仍待新采集（挪威沿海带 ocean/ice/wave）或
> 起点北移（>71.5°N）的设计决策。旧 `tromso_isfjorden_august_2026_demo_v1`
> RunContext（1.1.0）与 1.2.0 配置不再兼容，回放需重新生成。

> 2026-08-17（RC2 第二轮）根因定位与解决：缺口主要来自 NEXTsim 的
> ice_type/ice_edge 在无冰水域原生全 NaN（物理语义：无冰→无冰型/冰缘），
> 而非挪威沿岸无数据（TOPAZ6 起点区域原生有限率 93%）。因此**不北移走廊、
> 不新下载**；B 新增 RC2 专属策略 `land_sea_mask_plus_unknown_ice_free_v1`
> （无冰水域将 ice_type/edge 中性化为 0，其余 unknown 仍 fail-closed）。
> 修复后 72h 第二场景：coverage gate=true、start→goal 连通、v3 四层 + 6h
> 重规划 + D 消费全部 PASS（详见 `RC2_DEVELOPMENT_STATUS.md` §3）。
>
> 2026-08-17（RC2 第二轮）：Tromsø 144h qualification PASS（145 帧 gate=true、
> v3 四层 + 6h 重规划 + D），状态为 **RC2 Second Scenario Candidate**；
> 内存 4GB vs 0.8GB 已归因（A 帧双份驻留 × bbox 差异）；2-worker 并发
> benchmark 0.95× 无收益，正式路径保持串行。

> 2026-08-17（RC2 第三轮）：RC2 Frozen Baseline ESTABLISHED（Scenario B golden，
> 权威 `work_package_a/docs/RC2_BASELINE_20260817.md`）。内存优化采用
> `StandardDataFrame.consumer_view()`（共享只读数组）+ PreparedWindow/envelope
> 生命周期释放：mur 4.18→2.81GB、Tromsø 144h 1.40→0.97GB，业务不变。
> 公平 objective 级并发 benchmark：2-worker speedup ≈1.48×、内存极低，
> 状态 EXPERIMENTAL / 正式路径串行。

### 15.2 Demo Engineering（2026-08-17，Demo Candidate 2）

```text
RC2 Frozen Artifacts (Scenario A/B)
        ↓
D / Demo Adapter (identity/checksum/digest 校验 + 冻结 risk-store 空间帧)
        ↓
demo-state.json (FROZEN_VALIDATED / LIVE_COMPUTED + spatial + phase_deltas)
        ↓
本地只读 Viewer (localhost, 无 CDN, 离线; SVG 经纬度地图)
        ↑
POST/GET /api/live/*（页面按钮 → 真实 worker → 状态轮询 → LIVE 结果）

Live 小窗重规划：frozen committed risk window → 真实 C → worker watchdog
→ d.live-result.v1 (LIVE_COMPUTED) → D/Viewer
```

- Full Validation Mode 保留（真实完整计算 17–26 min）；
- Live Demo Mode ≤2 min（实测 ≈56–58s），诚实区分 frozen/live；
- Viewer 空间图层全部来自真实风险帧坐标（frame 0/6），LAND 与
  DATA_UNAVAILABLE 独立着色、与 risk 图层分离；ice-free NOT_APPLICABLE
  以计数 + 解释呈现，不伪造逐格位置；
- Compare 模式同时绘制 initial/replanned 并显示真实 Δ 指标；
- 展示层不侵入 A/B/C 核心；离线运行无外部依赖。

> 2026-08-17（Route Geospatial Integrity 审计，Demo Candidate 2 状态修正）：
> Viewer 曾出现“航线视觉穿过 LAND 但 Hard violations=0 / Coverage Gate=PASS”。
> 独立机器审计结论：C 制品 waypoints = 完整搜索路径（无降采样），48/48 冻结
> 路线在数据空间 0 违规（waypoint/edge/LAND/DU/角切/时间映射）；根因是
> **Viewer 坐标变换 bug**——格子用独立 x/y 拉伸、路线用等比投影，非正方形
> 场景下错位，导致地理正确的路线在像素空间穿过 LAND/DU 格子（旧相交
> A=252、B=72）。已最小修复：格子与路线共用同一 `project()`，并建立正式
> **Route Geospatial Integrity Gate**（`demo geo-integrity` 机器制品 +
> `demo preflight` 硬门 + Viewer 独立 `ROUTE GEO INTEGRITY` badge）。
> 当前状态：**Demo Candidate 2 = GEOSPATIALLY VALIDATED ENGINEERING
> CHECKPOINT**；完整证据见 `ROUTE_GEOSPATIAL_INTEGRITY_AUDIT_20260817.md`。
> 展示边界：当前仅 2 张 spatial 帧（frame 0/6），145 帧动态风险播放、
> GEBCO basemap、Moving Ship、+6h Replan 动画属于 NEXT PHASE，不得写成
> 已实现能力。

## 15.1 测试层级（L0–L3，2026-08-17 正式化）

- **L0**：Ruff + targeted unit（秒级）；
- **L1**：包级测试套件（分钟级）；
- **L2**：真实数据 smoke / worker smoke / 第二场景 smoke（几分钟）；
- **L3**：完整 v2/v3、RC1 + RC2 全量 regression（几十分钟）。

规则：小改跑 L0/L1；功能完成跑 L2；milestone/跨模块大改跑 L3；不机械重复
30–40 分钟 L3。

Route Geospatial Integrity gate 属于 Demo preflight 常驻 L1/L2 检查
（`demo geo-integrity`，~0.5s，只读冻结制品与风险帧）。

AIS 可保留到朗伊尔城以识别完整航次，但伊斯峡湾内部和港内操纵轨迹不纳入气象导航算法的
航路优化评价。这样既可用 AIS 检查海上航段，又不把复杂峡湾操纵错误地归因于气象规划。

### 7.3 开发顺序与旧口径裁决

产品顺序仍以**摩尔曼斯克—迪克森为最终目标**；截至 2026-08-15，实际已交付的是特罗姆瑟—
伊斯峡湾 144 h 冻结演示数据，因此当前演示以该航区为底座，主走廊数据补齐后优先切换。

- ⚠️ 与现状不符：旧 `tromso_to_svalbard` 及朗伊尔城算法终点。依据：当前 corridor
  `tromso_to_isfjorden_outer` v1.2.0 和本轮图示口径。
- ⚠️ 与现状不符：C 归档中的 69.65°N/18.95°E、78.22°N/15.63°E，以及旧长航线端点。
  依据：当前 contracts/A 配置与本轮两幅图一致，以上旧值仅保留归档审计。

## 8. 船型与参数口径

当前统一选择倾向为**散货船**：它符合北极货运和相对固定港口航线的演示叙事，适合展示海况、
冰况、风险与航路的联合变化。

共享配置中的 `nordic_odyssey_reference_v1` 可作为明确标注的“演示散货船参数集”：公开参考为
冰区加强型 Panamax 散货船，FSICR Ice Class 1A、船长 225.0 m、船宽 32.31 m、报告吃水
14.08 m、标称航速 15.7 kn。它是 `public_reference_unvalidated`，Ice Class 1A 不能写成
Polar Class PC6，也不是完整性能校准。

演示参数集仍需逐步补齐：

| 参数组 | 对演示的影响 | 本项目处理原则 |
|---|---|---|
| 冰级及等效能力 | 冰区 hard/soft 风险和航速折减 | 优先查公开典型值并记录来源 |
| 装载、吃水、船宽、富余水深 | 浅水与端点可行性 | 未补齐前不启用净水深 hard mask |
| 经济/最大/最小航速 | ETA 与风险采样时刻 | 使用版本化演示值并显式标注 |
| 风浪流相对航向性能曲线 | 方向性速度变化 | 优先公开典型曲线，次选透明拟合 |
| 转向能力/最小转弯尺度 | 邻接与转向惩罚 | 使用可解释的演示参数 |
| 等待与减速策略 | 时间依赖路径是否允许等待 | 当前无等待；未来需显式升级 |

参数来源优先级固定为：**可追溯的网上公开典型值 > 基于现有数据的透明拟合 > 明确标注的演示
默认值**。不得把演示参数集写成真实船型校准结果。

## 9. B 风险与 C 路线口径

B 默认输出逐小时风险序列，至少覆盖 24 h，且必须覆盖 C 实际规划/ETA 所需的完整窗口；主走廊
168 h 闭区间为 169 帧，迁移走廊按其冻结窗口物化。不能用一张当前风险图覆盖全航程，也不能
把旧 CNN 单步结果复制成完整序列。

演示主输出为 **v3 四层 × 三目标（12 路线整组）+ 至少一次重规划**（2026-08-15 确认）；
v2 三目标 + 重规划保留为强制后备路径，不作为首选验收结论。

C 按候选边预计到达时刻采样对应 `valid_time` 风险，输出：

- v2：`fastest`、`low_risk`、`recommended` 三目标；
- v3：全航程、24–72 h 主通道、0–24 h 滚动、0–6 h 可执行四层，每层三目标；
- 至少一次按模拟时间推进或风险更新触发的重规划；
- ETA、距离、风险、成本、来源风险帧和重规划原因等可展示指标。

B 输出环境速度影响，C 组合船型参数得到最终船速；同一环境影响不得重复折减。D 只读 CD 的
完整发布制品，不能直接调用 B/C 内部函数或等待持有计算锁。

## 10. 科学接口与工程演示验收

### 10.1 五类专业接口仅保留

| 专业方向 | 保留接口 | 本轮处理 |
|---|---|---|
| 海洋/气象 | 风、浪、流、水位、时间策略和来源摘要 | 保留字段与替换点，不要求专家评审 |
| 冰情 | 冰密集度、冰型、冰厚、冰漂、冰缘与阈值 | 保留版本化参数接口 |
| 船舶 | 冰级、吃水、航速、操纵和性能曲线 | 使用演示散货船参数集 |
| 航运/法规 | 限制区、通航规则、航路和 hard/soft 策略 | 保留信息层，不自动升级 hard mask |
| 数据/模型 | 模型版本、训练/拟合来源、指标和替换后端 | 保留 provenance、digest 和评估接口 |

本轮及以后默认只维护上述接口。团队不具备跨专业科学校准能力，因此不要求专业人员签字，不把
`calibrated` 作为挑战杯交付前置条件。

### 10.2 工程演示验收

工程演示通过至少满足：

1. A 的冻结数据能在无网条件下重复加载，时间、走廊和变量一致；
2. B 能生成连续风险图/风险序列，风险变化可解释且没有明显全零、全满或空间错位；
3. C 路线不穿陆地，ETA 递增，候选目标和重规划可运行，结果无明显荒谬绕行；
4. D 能展示当前风险、预测风险、路线和关键指标，不读取内部私有实现；
5. 同一场景身份和 generation 贯穿全链，旧代次不覆盖当前结果；
6. 失败时有清楚错误和可恢复演示方案；
7. 所有演示参数和局限明确，不宣称真实导航能力。

`formal` 仍表示来源与工程身份合格；`demo_unvalidated` 表示参数未科学校准。挑战杯可以在
`formal + demo_unvalidated` 状态下通过工程验收。

### 10.3 已知限制的“记录即合规”口径与答辩话术

以下项目按 D7 与用户确认只记录、不修复（2026-08-15）：

- 风险规则、演示船型、hard mask、bathymetry 与法规层未完成科学/真船/法规校准；
- CNN P2/P3 冻结，不进正式 B，仅作可选展示对照；
- 实验 B 最小卫生修复按 D6 延后，比赛前不动；
- 外部数据源/凭据/产品目录变化风险由“冻结数据双备份 + 恢复说明”覆盖，不做接口改造。

答辩话术要点：

1. 明示“所有参数为演示设置、未声称适航或科学校准”，把定位放在“工程链路与可解释性”，
   不放在“科学精度”；
2. 说明数据为“来源清楚、连续、可离线复现的冻结数据”，展示来源、时间窗、覆盖与
   `navigation_use=prohibited` 警示；
3. CNN 仅作“可选展示对照”，不主动展开训练细节与科学评价；
4. 若被问“为什么未校准”，回答：挑战杯以工程演示为目标，科学/法规接口已保留，校准需
   真实船舶与法规数据，超出项目边界。

以上条目在 C 验收清单、B 总 handoff、实验 B handoff 与
[最终交付说明](最终交付说明.md) 中同步记录。

### 10.4 测试分层与“开发快路径 / 完整验证路径”

日常开发不应每次承担发布级完整验证成本，但必须保留从干净环境开始的完整验证路径。

| 层 | 内容 | 何时跑 | 网络 |
|---|---|---|---|
| L0 单元 | A/B/C/orchestrator 单元测试 | 每次改动 | 离线 |
| L1 合同/契约 | Schema、身份、digest、围栏 | 每次改动 | 离线 |
| L2 包内集成 | A 本地归档回放、B committed、C synthetic | 对应包改动 | 离线 |
| L3 orchestrator 局部 smoke | 冻结 A bundle → B → C 小窗/低节点 | orchestrator/B/C 接口改动 | 离线 |
| L4 orchestrator v2 完整 | v2 initial + replan（后备验证） | 关键改动/发布前 | 离线 |
| L5 orchestrator v3 完整 | v3 整组 + replan（主线验证） | 8/20 门槛与发布前 | 离线 |
| L6 真实源 smoke | 少量真实下载验证 | 手动、低频、数据源变动时 | 需联网 |
| L7 干净环境全链 | 冷缓存、原始输入 A→B→C→D | 发布/演示前 | 可离线（用冻结数据） |

日常默认只跑 L0–L3；改 A/B/C/orchestrator 时按上游影响选择是否重算对应冻结制品；
发布或演示前至少一次 L7。L0–L5 均不访问外网；真实下载只走 A 显式采集命令并产出冻结制品。
本原则与 6.3/6.4 的制品失效规则配套执行。

### 10.5 Demo RC1 当前实现要点（2026-08-16）

- A：TOPAZ 5 类由 `originalGrid` 原生曲网格重建（`cmems-origg-97062ef099c4`，
  20 km 最近邻阈值、水掩膜、跨陆防护、无外推；vxo/vyo 投影分量由 A 规范化旋转）。
- B：`land_sea_mask_plus_unknown_v1`：source-unknown 节点置 hard（unknown→不可规划，
  风险仍 NaN/confidence 0，fail-closed 不变）；RC2 起每格输出 `hard_reason`
  （NONE/LAND/DATA_UNAVAILABLE/OTHER）与 `missing_input_variable_counts`。
- C：state=(node, 60min bucket, heading_code)；8 邻接、无等待；RiskSampler 预计算
  numpy 数组 + bisect；heuristic 为可采纳下界；带 `C_ASTAR_PROGRESS_SECONDS` 心跳。
- D：离线本地 schema registry（`arctic-route.local` 引用本地解析）+ v3 `layers`
  数组解析；真实 initial/replanned fixtures 回归；RC2 可消费
  `planning-coverage-preflight.json`（`coverage` 子命令 / `snapshot --coverage`）。
- Orchestrator：worker 子进程 + watchdog 实现真正可中断 per-stage timeout；
  心跳、TIMEOUT 报告、无孤儿进程（单测覆盖）；RC2 新增 `coverage_preflight` 阶段，
  B full commit 后、规划前发布 `planning-coverage-preflight.json`（schema v1，
  gate=每帧 unknown_navigable_nodes==0；C fail-closed 不变）。
- 验证边界：r6/r7 完整 E2E 由旧内联路径产生；worker 路径机制已单测，
  RC2 已用真实 RC1 冻结 bundle 跑通 worker-mode full v3 E2E（成功 ×3，
  业务结果与 r6 一致），并用真实四层 A* 验证 45.2s 可中断超时（TIMEOUT 报告、
  无孤儿、无半成品）。

## 11. 历史架构蓝本的整合裁决

2026-07-15 的《北极航线预测驱动动态规划系统架构设计》继续提供设计来源，但不是现状真值。
（源自：ARCTIC_ROUTE_SYSTEM_归档_20260815.md）

保留并已落入当前架构的原则：A→B→C→D 单向依赖、UTC 时间语义、模拟时钟、未来信息隔离、
发布后不可变、generation 丢弃迟到结果，以及按数据类型区分时间策略。

以下内容必须显式标注，不得照搬：

- ⚠️ **与现状不符**：A 统一目标网格。依据：当前 A 保留源网格，B 拥有风险目标网格。
- ⚠️ **与现状不符**：固定 24 h 或 2–5.5 天窗口。依据：共享合同当前为动态 72–216 h，
  主走廊默认 168 h、迁移走廊默认 96 h。
- ⚠️ **与现状不符**：正式间隔可直接配置为 30/10 min。依据：MVP 合同固定 60 min。
- ⚠️ **与现状不符**：所有动态变量可统一短时外推。依据：当前按来源、变量、coverage 和
  knowledge cutoff 分别判断，无法证明时必须拒绝或显式降级。
- ⚠️ **与现状不符**：法律区、水深自动成为 hard mask。依据：政策、净空与船舶证据未冻结。
- ⚠️ **与现状不符**：C 对各环境因素再次做速度折减。依据：B 输出环境因子，C 只做一次最终
  船速计算。
- ⚠️ **尚未实现**：D、D* Lite、MPC 和 10/30 min 正式输出，不得写成当前能力。

旧 A/B 的 mtime 选取、部分输出、缺测补 0、稀疏帧、v1 合同和 sea-mask 广播通航掩码均为
`legacy_unverified`，只能通过兼容适配器用于审计；完整哈希与差异证据见
[项目梳理报告](项目梳理报告.md)。

## 12. 人与 AI 的继续开发协议

开始任何跨包任务前：

1. 记录涉及仓库的 commit、dirty 状态、包版本与配置摘要；不以目录名或“最新”代替身份。
2. 读取本文件、目标包 handoff、生产者与消费者两侧的接口文档和 `AGENTS.md`。
3. 明确任务属于 formal、synthetic 还是 legacy，以及期望的校准状态。
4. 先用公共 fixture 做合同门禁，再用冻结的真实制品做验收；两种证据分开报告。
5. 失败时保留原始错误、阶段、摘要和退出状态；不得以降级成功覆盖正式失败。

完成任务时至少同步：代码/Schema/配置、生产者—消费者测试、包 handoff、顶层冲刺状态；若
架构边界变化，还必须更新本文件。

## 13. 已定治理决策 D1–D7

| 编号 | 已定结论 | 文档/执行影响 |
|---|---|---|
| D1 | 科学接口保留；必需参数优先网上典型值、次选拟合 | 科学工作不阻塞；参数必须版本化和标注来源 |
| D2 | 工程演示通过即成功 | 完成定义改为风险/路线大体合理、链路稳定 |
| D3 | A 预下载、预处理、持久化；数据新鲜度非重点 | 默认稳定演示读取冻结本地数据 |
| D4 | contracts 同步问题已解决；本会话结束后由用户手动处理 Git | 不再把 ahead 1 列为阻塞，不主动要求提交/推送 |
| D5 | 建立顶层文档/治理仓库，只跟踪根级文档 | 子仓通过链接和明确版本记录引用 |
| D6 | 实验 B 在真实主线之后做 I001、lock、Mamba、`make check` | 不修改正式 B，不接入 C，当前不抢主线资源 |
| D7 | 其余风险与决策本轮只记录 | 不擅自开发 CNN P2、D 合同选择或新算法 |

## 14. 当前关键路径与保留风险

挑战杯关键路径调整为：

```text
冻结 A 演示数据
  → B 连续风险图/序列
  → C 三目标路线 + 至少一次重规划
  → D 风险/路线/指标可视化
  → 断网重复演示与答辩材料
```

仍需记录但本轮不额外处理的风险：编排器集成长运行仍未收口（阶段报告与超时已实现）；CNN
P2/P3；规则和船型未科学校准；D 尚未实现；外部数据源和凭据会变化；bathymetry、法规区和
hard mask 缺少完整证据；主走廊 168 h 与完整 A→B→C→D 仍未贯通（tromso 144 h 已交付）。
它们不应被删除，也不应自动升级为当前开发任务。

## 15. 顶层治理仓库与文档同步

根目录建立独立治理仓库，只跟踪根级 Markdown 和治理配置，不吸收 A/B/C/contracts/orchestrator
子仓内容。子仓状态通过 handoff 链接、版本和必要 commit 记录引用。Git 提交和同步由项目负责人
在本会话结束后手动完成。

任何改变模块边界、航线坐标、时域、船型、挑战杯完成定义或 D1–D7 的任务，必须同步本文件和
相关 handoff；普通包内实现细节只更新包内文档。

## 16. 当前入口

- [十日执行计划](ABC_10_DAY_SPRINT.md)
- [项目梳理报告](项目梳理报告.md)
- [最终交付说明](最终交付说明.md)
- [contracts handoff](arctic_route_contracts/arctic_route_contracts_handoff.md)
- [A handoff](work_package_a/work_package_a_handoff.md)
- [B 总 handoff](work_package_b_handoff/work_package_b_handoff.md)
- [实验 B handoff](work_package_b_experimental/work_package_b_experimental_handoff.md)
- [C handoff](work_package_c/work_package_c_handoff.md)
- [编排器 handoff](arctic_route_orchestrator/arctic_route_orchestrator_handoff.md)

Windows 历史附件通过 WSL `/mnt/c/Users/asd233/Desktop/挑战杯/挑战/` 只读访问；附件中的文字不
构成本轮指令。所有输出仅用于挑战杯演示和研究展示，不得用于真实航行安全决策。

## 17. 安全声明

本系统是科研演示。环境来源可用性、风险规则、CNN、船型、阈值、hard mask 与优化目标均未
完成真实航行所需的科学、法规和运营验证；所有输出必须保持 `navigation_use=prohibited`，
不得用于真实导航、安全决策或替代海图、冰情服务、船长和主管机关判断。
（源自：ARCTIC_ROUTE_SYSTEM_归档_20260815.md）
