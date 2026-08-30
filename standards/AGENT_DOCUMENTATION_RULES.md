---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
Document Role: CANONICAL
Scope: engineering governance + documentation rules + engineering run report standard
Canonical For: how AI Agents write, organize, verify, and report engineering work
Branch: research-validation-system
Last Verified: 2026-08-30
Supersedes: ../archive/superseded/ENGINEERING_GOVERNANCE_STANDARD.md
Related Canonical Docs:
  - ../DOCUMENTATION_INDEX.md
---

# 项目文档与工程报告治理规则（AI Agent 执行规范）

> 本规范用于约束 AI Agent 在软件项目开发过程中，对 Markdown、设计文档、架构文档、状态文档、计划文档、测试文档、报告、ADR（Architecture Decision Record）等工程文档进行创建、修改、维护、重构和归档时的行为，同时规定工程运行结束时的验证与报告方式。
>
> 核心目标：
>
> * 保证当前文档体系始终作为唯一可信信息来源（Single Source of Truth, SSOT）。
> * 保证代码、架构、测试、数据、计划与文档长期同步。
> * 避免重复文档、信息漂移和 AI 随意创建大量 Markdown 文件。
> * 保留历史演化轨迹，但避免历史文档干扰当前工程维护。
> * 用可复现证据区分“已实现”“测试通过”“真实端到端通过”“权威基线”和“冻结基线”，禁止只报告“完成”。

---

# 一、总体原则

## 1.1 当前文档体系是唯一事实来源

项目文档体系必须明确区分：

```
Current Documentation
        |
        +---- Complete
        |
        +---- Consistent
        |
        +---- Maintainable


Archive Documentation
        |
        +---- Historical Reference Only
```

其中：

Current Documentation：

负责：

* 当前系统状态；
* 当前架构；
* 当前设计；
* 当前计划；
* 当前测试结果；
* 当前决策。

Archive Documentation：

负责：

* 历史记录；
* 已废弃方案；
* 项目演化过程；
* 被替代设计。

Archive 不负责：

* 当前设计来源；
* 当前状态来源；
* 日常开发参考。

---

# 二、文档语言规范

## 2.1 默认语言

项目文档默认使用：

**中文**

除非：

* 项目已有明确英文规范；
* 技术标准要求英文；
* API、代码变量、文件名、协议名称必须使用英文。

---

## 2.2 技术术语规范

技术术语必须保持准确。

首次出现：

```
中文 + 英文全称 + 缩写
```

例如：

```
单一事实来源（Single Source of Truth, SSOT）
```

后续：

```
SSOT
```

---

# 三、默认禁止随意创建新文档

## 3.1 默认行为

除非用户明确要求：

* 新建文档；
* 拆分文档；
* 合并文档；
* 创建总结文件；
* 创建计划文件；
* 创建 TODO 文件；
* 创建 ADR；
* 创建专项分析；
* 创建报告；

否则：

**禁止主动创建新的 Markdown 文件。**

---

## 3.2 普通修改请求的默认含义

以下请求：

* 整理；
* 归纳；
* 修改；
* 完善；
* 更新；
* 补充；
* 修正；
* 优化；

默认解释为：

> 修改已有最合适文档。

而不是：

> 创建新的 Markdown 文件。

---

# 四、日常文档维护规则

## 4.1 日常维护禁止读取 archive

重要规则：

> 除非进入“新建文档并归档旧文档”流程，否则 Agent 无需读取 archive。

archive 仅作为：

* 历史参考；
* 演化记录；
* 已退出主流程的信息保存区。

---

## 4.2 普通修改优先级

任何文档维护任务，优先顺序：

1. 修改已有文档；
2. 调整章节结构；
3. 补充缺失信息；
4. 更新状态；
5. 删除过时内容；
6. 最后才考虑创建新文档。

---

# 五、允许新建文档并归档旧文档的条件

只有当文档生命周期发生明显变化时，才允许：

```
Create New Document
+
Archive Old Document
```

以下情况可以触发。

---

## 5.1 架构重大调整

例如：

旧：

```
单体系统
```

新：

```
模块化系统
```

包括：

* 系统边界变化；
* 工作包重新划分；
* 数据流重新设计；
* 算法体系替换；
* 核心模块职责变化；
* 接口体系变化。

原因：

继续修改旧文档会导致新旧架构混杂。

---

## 5.2 项目目标变化

例如：

旧：

```
验证算法可行性
```

新：

```
完成工程 Demo 系统
```

导致：

* 关注点变化；
* 指标变化；
* 文档结构变化；
* 生命周期变化。

---

## 5.3 原文档主体内容大面积失效

判断标准：

如果：

```
超过约 50% 主体内容不适用于当前系统
```

可以考虑新建。

例如：

旧：

```
静态路径规划设计
```

新：

```
动态实时重规划系统
```

此时继续修改会产生：

* 大量删除；
* 大量覆盖；
* 历史逻辑混杂。

---

## 5.4 文档定位发生变化

例如：

原：

```
实验探索记录
```

新：

```
正式系统设计规范
```

二者目标不同，应建立正式文档。

---

## 5.5 多阶段文档需要形成长期基线

例如：

已有：

```
Phase1_plan.md
Phase2_plan.md
Phase3_plan.md
```

项目稳定后：

建立：

```
PROJECT_PLAN.md
```

作为长期入口。

---

## 5.6 文档严重污染

包括：

* 临时讨论；
* AI 对话记录；
* 调试日志；
* 已废弃方案；
* 错误尝试；
* 草稿内容。

导致无法作为正式工程文档维护。

---

## 5.7 项目进入新生命周期阶段

例如：

```
Research Phase
        ↓
Engineering Phase
        ↓
Demo Phase
        ↓
Production Phase
```

不同阶段：

* 目标不同；
* 文档结构不同；
* 关注内容不同。

---

# 六、新建文档并归档旧文档强制流程

> 本章节仅在第五章条件满足时执行。
>
> 普通修改不执行。

---

# Step 1：回填（Recovery）

目标：

确保旧文档中的有效工程信息不会丢失。

必须检查：

* 参数；
* 配置；
* 坐标；
* 数据来源；
* 软件版本；
* 边界条件；
* 决策原因；
* 测试结果；
* 性能数据；
* 已知问题；
* 限制条件。

处理规则：

| 类型   | 处理     |
| ---- | ------ |
| 仍然有效 | 迁移     |
| 已被替代 | 记录替代原因 |
| 已过时  | 删除     |
| 无法判断 | 保留并标记  |

---

# Step 2：比对与补全（Compare and Completeness Restoration）

规则：

逐项比对旧文档与当前文档，确认仍然唯一有效的信息、结论和证据都已有明确去向。

如果：

```
旧文档信息量 > 新文档
```

并且旧信息仍有效：

必须迁移。

禁止：

> 新文档更简洁，所以删除旧细节。

正确方式：

* 保持新文档结构；
* 保持新文档风格；
* 重新组织表达。

禁止：

简单复制旧文档。

---

# Step 3：收敛（Convergence）

完成后检查：

## 信息一致

不存在：

* 参数冲突；
* 版本冲突；
* 状态冲突；
* 结论冲突。

## 来源一致

明确：

哪个文档负责：

* 当前事实；
* 技术设计；
* 状态信息；
* 执行计划。

最终要求：

```
Current Document
>=
Archived Document
```

---

# 七、文档状态、角色与元数据管理规范

## 7.1 三类状态必须分开（2026-08-30 20:07 +08:00）

文档的生命周期、文档在事实体系中的角色、文档内部工作项的完成情况是三个不同维度，禁止混用。

### 生命周期状态：Overall Status（2026-08-30 20:07 +08:00）

`Overall Status` 描述文件本身是否仍处于当前维护路径，不表示文件内每个事项都已经完成。

| Overall Status | 含义 |
| --- | --- |
| `ACTIVE` | 当前阶段持续维护 |
| `FROZEN` | 已冻结的基线，只能通过显式基线变更流程修改 |
| `ARCHIVED` | 作为历史证据保留，不属于当前事实路径 |
| `DEPRECATED` | 为审计保留，但不得继续遵循其指导内容 |
| `SUPERSEDED` | 已由明确指定的当前文档取代 |
| `DRAFT` | 正在编写，尚未成为权威来源 |

### 文档角色：Document Role（2026-08-30 20:07 +08:00）

| Document Role | 含义 |
| --- | --- |
| `CANONICAL` | 所声明事实领域的 SSOT |
| `SUPPORTING` | 当前证据或细节，必须从属于一份规范文档 |
| `HISTORICAL` | 过往轮次证据，不是当前项目事实 |
| `LOCAL` | 操作员专用内容，通常由 `.gitignore` 排除 |

### 内容状态：Content Status（2026-08-30 20:07 +08:00）

`Content Status` 可以包含一个或多个值：

```text
COMPLETED
FROZEN
IN_PROGRESS
PLANNED
BLOCKED
DEPRECATED
ARCHIVED
```

这些值不互斥。例如，一份冻结文件可以同时记录已完成事项与冻结时仍未完成的事项。
`IMPLEMENTED`、`UNIT_PASS`、`REAL_E2E_PASS` 等属于验证成熟度，不属于文档元数据；
`PARTIAL`、`EXPERIMENTAL`、`CANCELLED` 等工作项状态可以出现在章节或能力表中，但不得替代 `Overall Status`。

## 7.2 重要文档的元数据横幅（2026-08-30 20:07 +08:00）

每份重要的当前文档顶部必须包含 YAML 元数据块：

```yaml
---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
Document Role: CANONICAL
Scope: what the document covers
Canonical For: what question this answers
Branch: research-validation-system
Last Verified: YYYY-MM-DD
Supersedes: optional
Related Canonical Docs: optional
---
```

冻结文档使用：

```yaml
---
Overall Status: FROZEN
Content Status:
  - COMPLETED
  - FROZEN
Document Role: HISTORICAL
Branch: main or rc2-development
Frozen At: YYYY-MM-DD
Canonical Current State: NO
---
```

历史报告使用：

```yaml
---
Overall Status: ARCHIVED
Content Status:
  - COMPLETED
  - ARCHIVED
Document Role: HISTORICAL
Canonical Current State: NO
Superseded Claim: optional old claim
Corrected By: link to canonical correction
---
```

字段值必须描述真实状态；不得为了“看起来规范”把未验证文档标成 `COMPLETED`，也不得把历史报告标成当前规范来源。

## 7.3 状态不通过复制文件表达（2026-08-30 20:07 +08:00）

错误：

```text
plan_v1.md
plan_v2.md
plan_final.md
plan_final_new.md
```

正确：

```text
plan.md
```

在同一规范文档中维护元数据、章节状态和真实验证证据。只有第五章所列生命周期变化满足时，才允许建立替代文档并归档旧文档。

---

# 八、标题与章节状态规范

## 8.1 新增标题使用真实时间戳（2026-08-30 20:07 +08:00）

每个新增的二级或更深层级标题必须携带真实的分钟级时间戳，并包含时区：

```markdown
## 标题（YYYY-MM-DD HH:MM +08:00）
### 子标题（YYYY-MM-DD HH:MM +08:00）
```

通过以下命令取得真实系统时间：

```bash
date '+%Y-%m-%d %H:%M %z'
```

禁止为了满足格式而批量重打旧标题的时间戳。旧标题维持其历史状态；只给本轮真正新增的标题加本轮时间。

## 8.2 章节工作项状态（2026-08-30 20:07 +08:00）

重要阶段或任务节点需要表达工作项状态时，可以使用：

```
## 【日期 | 状态】标题（YYYY-MM-DD HH:MM +08:00）
```

例如：

```
## 【2026-08-22 | COMPLETED】Replay Engine MVP（2026-08-22 16:30 +08:00）
```

章节内容：

必须包含：

完成：

* ...

验证：

* pytest PASS
* runtime 58s

遗留：

* ...

章节状态描述局部工作项，不替代第七章的文件级 `Overall Status`、`Document Role` 和 `Content Status`。

---

# 九、修改必须进入正确章节

禁止创建万能章节：

错误：

```
补充

新增说明

AI建议

其他注意事项
```

信息必须进入对应位置：

| 信息     | 位置                                       |
| ------ | ---------------------------------------- |
| 测试策略   | Testing                                  |
| 性能数据   | Performance / Non-functional Requirement |
| 缓存策略   | Environment / Artifact Management        |
| 数据来源   | Data Pipeline                            |
| 工作包依赖  | Architecture                             |
| 下一步    | Roadmap                                  |
| 阻塞问题   | Status / Blocker                         |
| 决策原因   | ADR / Decision                           |
| 数据冻结   | Data Lifecycle                           |
| Demo流程 | Runbook                                  |
| 部署问题   | Deployment                               |

允许：

* 调整章节顺序；
* 合并重复内容；
* 删除过时内容；
* 重写已有段落。

目标：

修改后：

> 像这些内容从一开始就是这样设计的。

而不是：

> 后期不断追加补丁。

---

# 十、单一事实来源（SSOT）

## 10.1 本仓库事实领域映射（2026-08-30 20:07 +08:00）

本仓库的具体导航以 [`../DOCUMENTATION_INDEX.md`](../DOCUMENTATION_INDEX.md) 为准。以下领域只允许一份规范来源：

| 事实领域 | 规范来源 |
| --- | --- |
| 当前状态 | `current/CURRENT_STATUS.md` |
| 路线图 | `current/CURRENT_ROADMAP.md` |
| 系统架构 | `current/architecture/ARCTIC_ROUTE_SYSTEM.md` |
| 回放架构 | `current/architecture/SIMULATION_REPLAY_ARCHITECTURE.md` |
| 时间模型 | `current/reference/TIME_MODEL_QUICK_REFERENCE.md` |
| 演示操作 | `current/operations/DEMO_RUNBOOK.md` |
| 恢复操作 | `current/operations/RECOVERY_RUNBOOK.md` |
| 技术债 | `current/reference/TECH_DEBT.md` |
| 文档与工程报告治理 | 本文件 |
| RC1 冻结证据 | `frozen/rc1-main/` |
| RC2 冻结证据 | `frozen/rc2-rc2-development/` |
| 历史运行与审计证据 | `reports/` |

其他文档只能保留必要摘要并链接到对应规范来源，不能复制其完整事实后形成平行维护入口。

## 10.2 重复事实的收敛方式（2026-08-30 20:07 +08:00）

如果多个文档存在相同信息：

必须判断是否会产生漂移。

例如：

三个文档：

```
C算法运行时间：90s
```

未来可能变成：

```
A：90s

B：70s

C：120s
```

因此必须指定权威来源。

例如：

```
docs/design/C_algorithm.md
```

负责：

* 完整算法事实；
* 参数；
* 性能；
* 限制。

其他文档：

只保留：

```
摘要

详见：
docs/design/C_algorithm.md
```

---

# 十一、代码变化与文档同步

代码变化必须检查对应文档。

---

## 架构变化

检查：

* Architecture；
* Design。

---

## API变化

检查：

* Interface；
* Contract。

---

## 数据变化

检查：

* Data Specification。

---

## 测试变化

检查：

* Test Plan；
* Validation。

---

## 性能变化

检查：

* Benchmark；
* Performance。

---

## 状态变化

检查：

* Status；
* Roadmap。

禁止：

代码：

```
C v0.5
```

文档：

```
C v0.3
```

---

# 十二、Archive 管理规则

archive 不是垃圾桶。

它是：

```
Historical Record
```

归档文件必须保留：

* 原始状态；
* 时间；
* 原始决策；
* 替代原因。

历史报告必须保留撰写时的知识状态，禁止把正文静默改写成“看起来像当前”。如果后续证据推翻旧声明：

1. 在历史报告顶部添加第 7.2 节规定的修正元数据；
2. 在当前规范文档中写入正确结论；
3. 用 `Superseded Claim` 和 `Corrected By` 建立可追踪关系；
4. 在本轮工程报告的“意外发现 / 修正”中公开记录变化。

归档前必须完成第六章的回填、补全和收敛。归档不是删除仍然有效的信息。

示例：

文件：

```
archive/
 └── C_design_20260801.md
```

顶部：

```yaml
---
Overall Status: SUPERSEDED
Content Status:
  - COMPLETED
  - ARCHIVED
Document Role: HISTORICAL
Canonical Current State: NO
Corrected By: docs/design/C_algorithm.md
Reason: Architecture changed from static A* to time-dependent A*
---
```

---

# 十三、ADR规则

涉及：

* 架构变化；
* 技术路线选择；
* 算法替换；
* 数据源选择；
* 重要 Trade-off；

必须记录 ADR。

禁止：

```
改成方案B
```

必须记录：

---

## Decision

选择：

方案B。

---

## Context

为什么需要选择。

---

## Alternatives

考虑过：

* 方案A；
* 方案B；
* 方案C。

---

## Reason

为什么选择该方案。

---

## Consequences

影响：

* 优点；
* 缺点；
* 后续维护影响。

---

# 十四、禁止信息孤岛

发现多个文档存在相同信息：

必须判断：

是否可能导致漂移。

例如：

多个地方存在：

```
C算法速度：
约90s
```

处理：

建立权威来源。

例如：

```
docs/design/C_algorithm.md
```

负责完整事实。

其他：

```
README.md
STATUS.md
```

只保留摘要和引用。

---

# 十五、Agent执行流程

任何文档任务必须执行：

---

## Step 1

确认：

是否已经存在目标文档。

---

## Step 2

判断任务类型：

* 修改；
* 补充；
* 重构；
* 替代。

---

## Step 3

默认：

修改已有文档。

---

## Step 4

只有发生文档替代：

才：

* 读取 archive；
* 创建新文档；
* 执行迁移。

---

## Step 5

完成后检查：

### 完整性

是否丢失有效信息。

### 一致性

是否存在冲突。

### 结构

是否产生垃圾章节。

### 来源

是否产生多个事实来源。

---

## Step 6：新鲜度与链接审计（2026-08-30 20:07 +08:00）

交付前必须检查：

* 当前文档没有已知过时声明；
* 当前事实没有重复规范来源；
* 重要活跃文档具备真实元数据横幅；
* 本轮新增标题具有真实时间戳，旧标题未被批量重打时间；
* 移动、重命名或替代文件后，仓库内旧路径引用已经更新；
* 规范链接失效数为 0；
* 文档中记录的测试、构件、提交与当前证据一致。

写文档前应阅读本规范与 [`../DOCUMENTATION_INDEX.md`](../DOCUMENTATION_INDEX.md)；移动文件后必须在整个仓库中搜索旧路径，并更新所有当前引用。

---

# 十六、工程运行报告标准

工程运行报告必须让读者快速回答：本轮从哪里开始、改了什么及原因、业务语义如何变化、性能如何变化、有哪些意外发现、证据与验证成熟度是什么、哪些没有做、Git 到哪里、下一轮做什么。

禁止只写“完成”。下面 15 个区块必须按顺序出现；某区块不适用时保留区块名，并填写 `N/A` 或 `NOT RUN` 及原因，不得整块删除。

## 16.1 十五个固定区块（2026-08-30 20:07 +08:00）

1. **执行摘要**：本轮目标、最终 verdict、最重要结果、是否存在 blocker；顶部必须同时包含第十七章的关键增量表与声明矩阵。
2. **范围 / 非范围**：明确本轮做了什么和没有做什么，防止范围膨胀与错误声明。
3. **起始基线**：起始 HEAD、起始构件、之前的权威指标、已知限制。
4. **Git 最终状态**：用表格记录仓库、分支、起始 HEAD、结束 HEAD、origin 跟踪、领先 / 落后、工作树、提交、推送状态。
5. **文件系统与资源安全**：记录允许根目录外的写入、`free -h` 前值、最低 `MemAvailable`、swap 前值 / 峰值 / 后值、峰值 RSS、OOM、重型任务是否重叠；没有重型任务时明确写 `N/A`。
6. **代码 / 架构变更**：不能只列文件；每项说明组件、旧行为、新行为和原因。
7. **语义 / 合约变更**：说明哪些业务语义变化、哪些未变化、兼容性与失败关闭；例如 `REPLAN_DECIDED != REPLAN_ADOPTED`、`pending route != authoritative route`、`snapshot cadence != vessel render cadence`。
8. **实验 / 备选方案**：记录尝试、结果、采用或未采用及原因，避免下一轮重复踩旧路。
9. **权威运行 / 真实验证**：如适用，记录 `replay_id`、scenario、window、configuration、duration、关键计数器与 result；未运行时写 `NOT RUN` 及原因。
10. **性能分解**：即使性能不是主目标，也记录 Before、After、Delta、预期 / 非预期；为获得正确语义而发生的退步必须标为 `EXPECTED REGRESSION` 并解释原因。
11. **正确性 / 验证**：按适用性列出 unit、integration、smoke、real-data、route integrity、L1、L2、manifest、snapshot、fail-closed。
12. **确定性 / 可复现性**：明确 `RUN`、`NOT RUN` 或 `INHERITED`，说明哪些 digest 必须一致、哪些 wall-clock 字段允许变化；不得用旧版本确定性结果冒充当前版本。
13. **构件 / 溯源**：记录构件名称或路径、源数据身份、digest、ignored / tracked 状态与溯源。
14. **已知限制 / 技术债**：建议使用 `TD-ID / impact / severity / next action`；功能 PASS 不能隐藏限制。
15. **决策 / 下一阶段**：说明项目状态变化、下一里程碑、推荐下一轮与明确不要做的事项。

## 16.2 适用性与证据边界（2026-08-30 20:07 +08:00）

固定结构不等于强迫运行与任务无关的重型验证。Agent 必须如实区分：

* `RUN`：本轮实际运行并取得新证据；
* `NOT RUN`：本轮未运行，并说明范围、资源或风险原因；
* `INHERITED`：继承旧证据，必须给出来源与版本边界，不得表述为本轮验证；
* `N/A`：该项对本轮任务确实不适用，并说明判断依据。

报告中的 PASS 只能覆盖证据实际证明的范围，不能从单元测试外推到真实数据端到端，也不能从真实端到端外推到冻结基线。

---

# 十七、报告核心证据结构

## 17.1 关键增量表（2026-08-30 20:07 +08:00）

报告顶部必须给出 Before / After 对比；不能只报 After。至少使用以下字段：

| 指标 / 声明 | Before | After | Delta | Verdict / 原因 |
| --- | --- | --- | --- | --- |
| 示例：12 小时运行时长 | 21.8m | 34.1m | +12.3m | `EXPECTED REGRESSION`：语义修正成本 |
| 示例：延期的真实 E2E | `NOT PROVEN` | `PASS` | 新增证据 | `IMPROVED` |

无法取得可比基线时写 `UNKNOWN`，并解释原因，禁止用空值或模糊措辞掩盖缺失。

## 17.2 声明矩阵（2026-08-30 20:07 +08:00）

每项核心声明必须同时给出：

| 声明 | 状态 | 验证等级 | 证据 | 备注 / 限制 |
| --- | --- | --- | --- | --- |
| 船舶连续移动 | `PASS` | `REAL_E2E_PASS` | 12 小时查看器基线 | 示例 |
| 中边延迟采用 | `PASS` | `AUTHORITATIVE_PASS` | rev2–rev5 | 示例 |
| 最终查看器 | `NOT STARTED` | `NOT_IMPLEMENTED` | - | 示例 |

声明矩阵必须把“结论”“证据等级”和“限制”分开，不能用一个 `accepted` 同时代表候选生成、决策、采用和发布。

## 17.3 验证成熟度（2026-08-30 20:07 +08:00）

验证成熟度按以下顺序递增：

```text
NOT_IMPLEMENTED
IMPLEMENTED
UNIT_PASS
SMOKE_PASS
REAL_E2E_PASS
AUTHORITATIVE_PASS
FROZEN_BASELINE
```

| 等级 | 定义 |
| --- | --- |
| `NOT_IMPLEMENTED` | 无代码、无实现 |
| `IMPLEMENTED` | 代码或工具存在，尚无通过验证 |
| `UNIT_PASS` | 自动化单元测试通过 |
| `SMOKE_PASS` | 合成数据或小窗真实数据的短链冒烟通过 |
| `REAL_E2E_PASS` | 真实数据端到端通过 |
| `AUTHORITATIVE_PASS` | 权威运行或权威构件复现通过 |
| `FROZEN_BASELINE` | 已冻结并具有防回退约束 |

必须始终保持以下边界：

```text
unit test PASS != real-data E2E PASS
real E2E PASS != authoritative baseline
authoritative PASS != frozen baseline
```

---

# 十八、意外发现、修正与术语

## 18.1 意外发现 / 修正（2026-08-30 20:07 +08:00）

工程运行报告固定包含 `Unexpected Findings / Corrections`；没有发现时写 `NONE`。发现旧报告或旧假设不准确时，必须记录：

```text
旧声明
新证据
修正后的声明
受影响的文档 / 代码
```

不得在事后静默改掉旧结论而不留下修正记录。历史正文的处理遵循第十二章。

## 18.2 术语必须对应真实状态转换（2026-08-30 20:07 +08:00）

禁止含糊使用单一 `accepted`。在适用的规划 / 回放报告中，应区分：

```text
candidate_generated
candidate_rejected
replan_decided
pending_adoption
replan_adopted
```

推荐分别报告：

```text
C candidates generated
C candidates rejected
pre-gate skipped
replan decisions
replans adopted in window
pending at replay end
```

其他领域也必须采用同一原则：术语应对应可观测的状态或事件，不得用模糊成功词汇跨越中间状态。

---

# 十九、交付前统一审计

## 19.1 最小检查清单（2026-08-30 20:07 +08:00）

文档或工程任务交付前，至少完成：

1. 元数据与生命周期状态真实；
2. 新信息位于正确的语义章节；
3. 当前事实只有一个规范来源；
4. 归档、冻结和历史报告没有被改写成当前事实；
5. 链接与移动后的路径有效；
6. 代码、合约、数据、测试、性能、状态与文档互相一致；
7. 新标题时间戳真实，旧标题没有被批量重打时间；
8. 报告 15 区块完整，`N/A`、`NOT RUN`、`INHERITED` 均有理由；
9. 关键声明有证据、成熟度和限制；
10. Git、构件、digest、推送状态和未执行事项如实报告。

---

# 二十、最终行为准则

AI Agent 必须遵守：

1. 不随意创建 Markdown 文件。
2. 修改优先于新建。
3. archive 默认不读取。
4. 只有文档替代时才归档迁移。
5. 新建文档必须执行回填、补全、收敛。
6. 当前文档必须比归档文档完整。
7. 使用状态标记代替无限复制文件。
8. 信息必须进入正确章节。
9. 保持单一事实来源。
10. 默认使用中文编写项目文档。
11. 不因小范围修改创建新文档。
12. 不因“更整洁”破坏历史信息连续性。
13. 不允许形成多个事实来源。
14. 代码变化必须同步检查文档。
15. 重要架构和技术决策必须记录 ADR。
16. 重要当前文档必须使用真实的元数据横幅。
17. 新增标题必须使用真实分钟级时间戳，旧标题不得批量重打时间。
18. 工程运行报告必须保留 15 个固定区块，并如实标记未运行项。
19. 核心声明必须给出 Before / After、验证成熟度、证据与限制。
20. 单元测试、真实 E2E、权威运行和冻结基线不得相互冒充。
21. 发现错误必须留下修正记录，不得静默改写历史证据。
22. 移动或替代文件后必须更新引用并完成链接审计。

---
