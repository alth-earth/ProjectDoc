---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - IN_PROGRESS
Document Role: CANONICAL
Scope: engineering governance + documentation rules + report standard
Canonical For: how to write, organize, and report documentation
Branch: research-validation-system
Last Verified: 2026-08-21
---

# 工程治理标准

本文档定义：
1. 文档治理规则（状态分类、元数据、语义化放置、归档规则）
2. 工程运行报告标准（15 个固定区块、关键增量表、声明矩阵、成熟度等级）

---

## 第一部分：文档治理

### 文档生命周期分类（2026-08-21 23:18）

`Overall Status` 描述的是文件的生命周期状态，而非文件内每一项是否完成。

| Overall Status | 含义 |
|----------------|---------|
| ACTIVE | 为当前阶段维护 |
| FROZEN | 冻结的基线；只能通过显式基线流程变更 |
| ARCHIVED | 作为历史证据保留，不在当前真相路径内 |
| DEPRECATED | 为审计而保留，但其指导内容不得再遵循 |
| SUPERSEDED | 已被指定的当前文档取代 |
| DRAFT | 进行中的工作，尚未成为权威 |

`Document Role` 是另一个独立字段：

| Document Role | 含义 |
|---------------|---------|
| CANONICAL | 所声明事实领域的单一事实来源 |
| SUPPORTING | 从属于某个规范文档的当前证据或细节 |
| HISTORICAL | 过往轮次证据；本身永远不是当前项目真相 |
| LOCAL | 操作员专用，通常被 gitignore |

### 内容状态分类（2026-08-21 23:18）

`Content Status` 可包含以下一个或多个值：`COMPLETED`、`FROZEN`、
`IN_PROGRESS`、`PLANNED`、`BLOCKED`、`DEPRECATED`、`ARCHIVED`。

这些值并非互斥。一个冻结文件可以同时记录已完成的工作和冻结时刻尚未完成的项目。
能力表仍可使用诸如 `IMPLEMENTED`、`UNIT_PASS`、`BROWSER_E2E_PASS`、
`NOT_IMPLEMENTED` 等证据等级；这些不是文档元数据。

### 元数据横幅（2026-08-21 23:18）

每份重要的当前文档顶部必须有 YAML 元数据块：

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
Supersedes: (optional)
Related Canonical Docs: (optional)
---
```

冻结文档使用：
```yaml
Overall Status: FROZEN
Content Status:
  - COMPLETED
  - FROZEN
Document Role: HISTORICAL
Branch: main or rc2-development
Frozen At: YYYY-MM-DD
Canonical Current State: NO
```

历史报告使用：
```yaml
Overall Status: ARCHIVED
Content Status:
  - COMPLETED
  - ARCHIVED
Document Role: HISTORICAL
Canonical Current State: NO
Superseded Claim: (if applicable)
Corrected By: (link to correction)
```

禁止批量重打旧标题的时间戳。每个新增的二级或更深层级标题必须包含分钟级时间戳，
格式为 `## 标题（YYYY-MM-DD HH:MM）`。变更必须整合进正确的语义小节；诸如"补充"、
"新增说明"、"AI 建议"或"其他注意事项"之类的标题一律禁止。

### 语义化放置

信息必须放在正确的小节：
- 测试 -> 测试文档
- 缓存 -> 环境/缓存/构件文档
- 依赖 -> 架构/依赖
- 下一步 -> 路线图
- 阻塞 -> 状态/阻塞
- 决策 -> 决策/架构
- 数据冻结 -> 构件生命周期
- 性能 -> 性能/非功能

禁止在文档末尾追加信息，应改写相关小节。

### 单一事实来源（SSOT）

每个事实领域只有一份规范文档：
- 当前状态 -> CURRENT_STATUS.md
- 路线图 -> CURRENT_ROADMAP.md
- 系统架构 -> ARCTIC_ROUTE_SYSTEM.md
- 回放架构 -> SIMULATION_REPLAY_ARCHITECTURE.md
- 时间模型 -> TIME_MODEL_QUICK_REFERENCE.md
- 演示操作 -> DEMO_RUNBOOK.md
- 恢复 -> RECOVERY_RUNBOOK.md
- 技术债 -> TECH_DEBT.md
- 治理标准 -> 本文件
- RC1 -> frozen/rc1-main/
- RC2 -> frozen/rc2-rc2-development/
- 历史报告 -> reports/

其他文档应链接到规范来源，而非复制完整内容。

### 归档三步法

归档文档前：
1. 回填（Back-fill）：把旧文档中仍然有效的信息迁移到当前规范文档。
2. 比对（Compare）：对照新旧内容，检查是否遗漏了仍唯一有效的信息。
3. 收敛（Converge）：确保当前有效信息覆盖 >= 归档覆盖，且无过时冲突。
然后才能归档。归档不是删除有效信息。

### 历史报告规则

历史报告不得被改写为"看起来像当前"。它们保留撰写时的知识状态。如有需要，
在顶部添加修正说明：

```yaml
Overall Status: ARCHIVED
Content Status:
  - COMPLETED
  - ARCHIVED
Document Role: HISTORICAL
Canonical Current State: NO
Superseded Claim: (old claim that was wrong)
Corrected By: (link to canonical correction)
```

### 修正规则

在历史报告中发现错误时：
- 不得静默修改历史报告正文。
- 在顶部添加修正说明。
- 修改当前规范文档以反映正确理解。

### 带时间戳的新标题

所有新增标题必须携带真实时间戳：
```markdown
### X.Y Title (YYYY-MM-DD HH:MM +08:00)
```
使用 `date '+%Y-%m-%d %H:%M %z'` 获取真实系统时间。
禁止用新时间戳批量更新旧标题。

### AI 文档工作流

1. 写文档前先阅读本标准与 DOCUMENTATION_INDEX.md。
2. 将信息放入正确小节（语义化放置）。
3. 不在文档末尾追加补丁。
4. 不创建重复的规范文档。
5. 移动文件时更新链接。
6. 报告完成前运行一次新鲜度审计。

### 链接更新规则

移动文件后，搜索所有仓库中的旧路径并更新链接。
目标：规范链接失效数 = 0。

### 新鲜度审计

报告完成前验证：
- 当前文档中没有过时声明。
- 没有失效链接。
- 没有重复的规范来源。
- 所有新标题都有时间戳。
- 活跃文档都有元数据横幅。

---

## 第二部分：工程运行报告标准

## 1. 目的

最终报告必须能快速回答：

```text
这一轮从哪里开始？
改了什么？为什么改？
哪些业务语义变化？
性能变好还是变差？
有没有意外发现？
证据是什么？
达到哪一级成熟度？
哪些没做？
Git 到哪里？
下一轮做什么？
```

禁止只写"完成"。

## 2. 固定区块（15 个固定区块）

最终报告必须按以下顺序包含全部 15 个区块；不适用时写该块名 + `N/A` 或
`NOT RUN` + 原因，不能整块删除。

### 1. 执行摘要

至少：

```text
本轮目标
最终 verdict
最重要结果
是否存在 blocker
```

顶部必须再加 **关键增量表**（见 §3）与 **声明矩阵**（见 §4）。

### 2. 范围 / 非范围

明确本轮做了什么、明确没有做什么；防止范围膨胀与错误声明。

### 3. 起始基线

至少：

```text
起始 HEAD
起始构件
之前的权威指标
已知限制
```

### 4. Git 最终状态

表格字段：

```text
仓库
分支
起始 HEAD
结束 HEAD
origin 跟踪
领先 / 落后
工作树
提交
推送状态
```

### 5. 文件系统与资源安全

必须包含：

```text
允许根目录外的写入
free -h 之前
最低 MemAvailable
swap 之前 / 峰值 / 之后
峰值 RSS
OOM
重型任务重叠
```

没有重型任务时写 `N/A`，不能省略。

### 6. 代码 / 架构变更

不要只列文件；每项说明：

```text
变更的组件
旧行为
新行为
原因
```

### 7. 语义 / 合约变更

必须写明哪些业务语义变了、哪些没有变、兼容性与失败关闭。
例如 `REPLAN_DECIDED != REPLAN_ADOPTED`、`pending route != authoritative
route`、`snapshot cadence != vessel render cadence`。

### 8. 实验 / 备选方案

记录尝试过什么、结果、采用/未采用、为什么；避免重复踩旧路。

### 9. 权威运行 / 真实验证

如适用：

```text
replay_id
scenario
window
configuration
duration
关键计数器
result
```

本轮没跑则写 `NOT RUN` 并说明原因。

### 10. 性能分解

即使性能不是主目标也写：

```text
之前
之后
增量
预期 / 非预期
```

性能退步但语义更正确时必须标 `EXPECTED REGRESSION` 并说明。

### 11. 正确性 / 验证

至少列出：unit / integration / smoke / real-data / route integrity / L1 / L2 /
manifest / snapshot / fail-closed。

### 12. 确定性 / 可复现性

明确 `RUN / NOT RUN / INHERITED`；哪些 digest 相同、哪些 wall-clock 字段
允许变化；不得用旧版本确定性冒充最新版本。

### 13. 构件 / 溯源

至少：

```text
构件名称/路径
源数据身份
digest
ignored / tracked
溯源
```

### 14. 已知限制 / 技术债

必须写；建议格式 `TD-ID / impact / severity / next action`。功能 PASS 不能
隐藏限制。

### 15. 决策 / 下一阶段

写明项目状态发生了什么变化、下一里程碑、推荐下一轮、明确不要做什么。

## 3. 关键增量表

报告顶部必须有类似表格：

```text
指标 / 声明                  Before       After        Verdict
--------------------------------------------------------------
12 小时运行时长               21.8m        34.1m        EXPECTED REGRESSION*
延期的真实 E2E               NOT PROVEN   PASS         IMPROVED
展示适配器                   NONE         ESTABLISHED  PASS
L2 海岸线                    HARNESS      PRECHECK     ...
```

要求：

- 不能只报 After；
- 必须尽量给 Before / After / Delta；
- 性能退步要明确 `EXPECTED REGRESSION` 并给原因。

## 4. 声明矩阵

报告必须包含每项核心声明：

```text
声明
状态
验证等级
证据
备注 / 限制
```

示例：

```text
船舶连续移动
PASS
REAL_E2E_PASS
12 小时查看器基线
-

中边延迟采用
PASS
AUTHORITATIVE_PASS
rev2–rev5
-

最终查看器
NOT STARTED
NOT_IMPLEMENTED
-
-
```

## 5. 验证成熟度等级

固定成熟度，级别递增：

```text
NOT_IMPLEMENTED
IMPLEMENTED
UNIT_PASS
SMOKE_PASS
REAL_E2E_PASS
AUTHORITATIVE_PASS
FROZEN_BASELINE
```

定义：

```text
NOT_IMPLEMENTED   : 无代码、无实现
IMPLEMENTED       : 代码/工具存在，尚无通过验证
UNIT_PASS         : 自动化单元测试通过
SMOKE_PASS        : 短链冒烟通过（合成或小窗真实数据）
REAL_E2E_PASS     : 真实数据端到端通过
AUTHORITATIVE_PASS: 权威/权威 artifact 复现通过
FROZEN_BASELINE   : 已被冻结并防回退
```

特别强调等级不能等同：

```text
unit test PASS != real-data E2E PASS
real E2E PASS   != authoritative baseline
authoritative PASS != frozen baseline
```

## 6. 意外发现 / 修正

报告固定包含 `Unexpected Findings / Corrections`；即使没有也写 `NONE`。
发现旧报告/旧假设不准确时必须写：

```text
旧声明
新证据
修正后的声明
受影响的文档/代码
```

不能在事后悄悄改掉而不再记录。

## 7. 术语标准

禁止含糊使用单一 `accepted`。必须尽量区分：

```text
candidate_generated
candidate_rejected
replan_decided
pending_adoption
replan_adopted
```

最终报告计数器推荐：

```text
C candidates generated
C candidates rejected
pre-gate skipped
replan decisions
replans adopted in window
pending at replay end
```
