# Engineering Run Report Standard（2026-08-19）

状态：本轮起生效的最终报告模板标准（authoritative）
范围：所有后续 Codex 轮次的最终报告，必须使用本模板，不得每轮随意
换结构；细节可以补充，固定区块不能省略。

## 1. Purpose

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

禁止只写“完成”。

## 2. Fixed Blocks（15 个固定区块）

最终报告必须按以下顺序包含全部 15 个区块；不适用时写该块名 + `N/A` 或
`NOT RUN` + 原因，不能整块删除。

### 1. Executive Summary

至少：

```text
本轮目标
最终 verdict
最重要结果
是否存在 blocker
```

顶部必须再加 **Key Delta Table**（见 §3）与 **Claim Matrix**（见 §4）。

### 2. Scope / Non-Scope

明确本轮做了什么、明确没有做什么；防止范围膨胀与错误 claim。

### 3. Starting Baseline

至少：

```text
starting HEAD
starting artifact
previous authoritative metrics
known limitations
```

### 4. Git Final State

表格字段：

```text
repo
branch
start HEAD
end HEAD
origin tracking
ahead / behind
working tree
commits
push status
```

### 5. Filesystem & Resource Safety

必须包含：

```text
writes outside allowed root
free -h before
lowest MemAvailable
swap before / peak / after
peak RSS
OOM
heavy-task overlap
```

没有 heavy task 时写 `N/A`，不能省略。

### 6. Code / Architecture Changes

不要只列文件；每项说明：

```text
changed component
old behavior
new behavior
reason
```

### 7. Semantic / Contract Changes

必须写明哪些 business semantics 变了、哪些没有变、兼容性与 fail-closed。
例如 `REPLAN_DECIDED != REPLAN_ADOPTED`、`pending route != authoritative
route`、`snapshot cadence != vessel render cadence`。

### 8. Experiments / Alternatives

记录尝试过什么、结果、采用/未采用、为什么；避免重复踩旧路。

### 9. Authoritative Run / Real Validation

如适用：

```text
replay_id
scenario
window
configuration
duration
key counters
result
```

本轮没跑则写 `NOT RUN` 并说明原因。

### 10. Performance Breakdown

即使性能不是主目标也写：

```text
before
after
delta
expected/unexpected
```

性能退步但语义更正确时必须标 `EXPECTED REGRESSION` 并说明。

### 11. Correctness / Validation

至少列出：unit / integration / smoke / real-data / route integrity / L1 / L2 /
manifest / snapshot / fail-closed。

### 12. Determinism / Reproducibility

明确 `RUN / NOT RUN / INHERITED`；哪些 digest 相同、哪些 wall-clock 字段
允许变化；不得用旧版本 determinism 冒充最新版本。

### 13. Artifacts / Provenance

至少：

```text
artifact name/path
source data identity
digest
ignored / tracked
provenance
```

### 14. Known Limitations / Technical Debt

必须写；建议格式 `TD-ID / impact / severity / next action`。功能 PASS 不能
隐藏限制。

### 15. Decision / Next Phase

写明项目状态发生了什么变化、下一里程碑、推荐下一轮、明确不要做什么。

## 3. Key Delta Table

报告顶部必须有类似表格：

```text
Metric / Claim              Before       After        Verdict
--------------------------------------------------------------
12h runtime                 21.8m        34.1m        EXPECTED REGRESSION*
Deferred real E2E           NOT PROVEN   PASS         IMPROVED
Presentation Adapter        NONE         ESTABLISHED  PASS
L2 coastline                HARNESS      PRECHECK     ...
```

要求：

- 不能只报 After；
- 必须尽量给 Before / After / Delta；
- 性能退步要明确 `EXPECTED REGRESSION` 并给原因。

## 4. Claim Matrix

报告必须包含每项核心 claim：

```text
Claim
Status
Validation Level
Evidence
Notes / Limitation
```

示例：

```text
Ship moves continuously
PASS
REAL_E2E_PASS
12h viewer baseline
-

Mid-edge deferred adoption
PASS
AUTHORITATIVE_PASS
rev2–rev5
-

Final Viewer
NOT STARTED
NOT_IMPLEMENTED
-
-
```

## 5. Validation Maturity Levels

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

## 6. Unexpected Findings / Corrections

报告固定包含 `Unexpected Findings / Corrections`；即使没有也写 `NONE`。
发现旧报告/旧假设不准确时必须写：

```text
old claim
new evidence
corrected claim
affected docs/code
```

不能在事后悄悄改掉而不再记录。

## 7. Terminology Standard

禁止含糊使用单一 `accepted`。必须尽量区分：

```text
candidate_generated
candidate_rejected
replan_decided
pending_adoption
replan_adopted
```

最终 report counters 推荐：

```text
C candidates generated
C candidates rejected
pre-gate skipped
replan decisions
replans adopted in window
pending at replay end
```

## 8. Next-Phase Optional / Forbidden Work

本轮（2026-08-19 Viewer 轮）明确不做：

```text
Planner performance optimization
Pending-Plan Gate（只记 TD，不实现）
A* / D* Lite / LPA* 重写
Numba / Cython
6/8/16 planner workers / tick parallelism
新一轮 12h / 24h / determinism replay
144h causal replay
新场景
重新生成 RC1 / RC2
修改 frozen digests
最终 UI polish / 复杂图标动画 / 粒子效果
无目的重新下载 GEBCO
架构大重写
```
