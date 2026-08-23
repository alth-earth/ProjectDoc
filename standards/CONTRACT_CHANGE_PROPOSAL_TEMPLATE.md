---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: CANONICAL
Scope: required template for cross-package contract changes
Canonical For: contract change proposal content and approval gate
Branch: research-validation-system
Last Verified: 2026-08-22
---

> **声明（About this template）**：本文档是 Arctic Route 项目中跨包（cross-package）合约变更的**强制模板**。
> 任何涉及生产者/消费者之间数据、Schema 或语义契约的变更，都必须复制本模板并逐项填写后才能进入审批流程。
> 本模板的作用是：1) 统一提案结构与证据要求；2) 强制完成兼容性与失败行为分析；3) 作为语义/生产者/消费者/集成四方审批门控（approval gate）的唯一依据。
> 只有状态为 `APPROVED` 且审批记录齐全的提案才被允许推进到生产环境。

# Contract Change Proposal Template

## Proposal metadata（2026-08-22 00:02）

```text
Proposal ID:
Title:
Status: DRAFT | REVIEWED | APPROVED | REJECTED | SUPERSEDED
Author:
Semantic owner:
Affected producers:
Affected consumers:
Target version:
Created:
Last updated:
```

`DRAFT` and `REVIEWED` do not authorize production use.

## Problem and evidence（2026-08-22 00:02）

- Current observed limitation:
- Code/schema/artifact evidence:
- Why configuration or an additive optional field is insufficient:
- Frozen baselines affected:

## Current and proposed semantics（2026-08-22 00:02）

| Dimension | Current | Proposed | Breaking? |
|---|---|---|---|
| Schema identity | | | |
| Field/cardinality | | | |
| Units/polarity | | | |
| Time semantics | | | |
| Missing/unavailable behavior | | | |
| Atomicity/immutability | | | |
| Content identity/digest | | | |

Include machine-readable before/after examples. Never use synthetic examples as
proof that real artifact production is complete.

## Compatibility and failure behavior（2026-08-22 00:02）

- Old producer → new consumer:
- New producer → old consumer:
- Unsupported-version behavior:
- Partial/missing/unknown behavior:
- Fail-closed behavior:
- Migration and rollback:

## Implementation ownership（2026-08-22 00:02）

| Repository / directory | Owner | Allowed change | Prohibited change |
|---|---|---|---|
| | | | |

## Verification matrix（2026-08-22 00:02）

| Gate | Required evidence | Result |
|---|---|---|
| Schema validation | old/new fixtures | NOT_RUN |
| Producer tests | deterministic output and identity | NOT_RUN |
| Consumer tests | valid/invalid/unsupported inputs | NOT_RUN |
| Compatibility | old baseline remains readable | NOT_RUN |
| Semantic equivalence | unchanged fields/digests | NOT_RUN |
| Focused integration | real or formal fixture path | NOT_RUN |
| Resource budget | wall time and peak RSS | NOT_RUN |

## Approval record（2026-08-22 00:02）

| Role | Decision | Evidence/date |
|---|---|---|
| Semantic owner | PENDING | |
| Producer owner | PENDING | |
| Consumer owner | PENDING | |
| Integration owner | PENDING | |

