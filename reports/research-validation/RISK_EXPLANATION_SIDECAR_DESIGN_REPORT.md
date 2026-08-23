---
Overall Status: DRAFT
Content Status:
  - COMPLETED
  - PLANNED
Document Role: SUPPORTING
Scope: backward-compatible per-cell risk explanation sidecar design and proposal validation
Canonical For: NO; proposal evidence only, pending B, Orchestrator, and D owner approval
Branch: research-validation-system
Last Verified: 2026-08-23
Related Canonical Docs:
  - ../../current/reference/CONTRACT_OWNERSHIP_REGISTRY.md
  - ../../current/architecture/ARCTIC_ROUTE_SYSTEM.md
---

# Risk Explanation Sidecar 设计报告

## 1. Executive Summary（2026-08-23 20:01 +08:00）

本轮目标是设计可选的 `risk-explanation.v1`，为已发布 RiskWindow/RiskFrame 提供逐格风险解释，
同时保持 `bc.risk-frame.v2`、B 风险公式、C planner 和 D calculation 完全不变。

最终 verdict：**DESIGN COMPLETE / PRODUCTION NOT IMPLEMENTED**。JSON Schema、设计示例和 11 个
可执行 schema/语义测试已完成；没有真实 sidecar producer、Orchestrator 投影或 D UI 集成，因而
不得声称 Viewer 已经能够解释真实路线选择。当前没有设计阶段 blocker，生产推进仍需 B、
Orchestrator、D 负责人审阅。

### Motivation（2026-08-23 20:01 +08:00）

当前系统能够展示选中的路线和 RiskFrame 的 `risk_score`、`risk_level`、`confidence`、
`source_summary`，但 RiskFrame 不保留构成某个格点风险值的逐因子贡献。D 不能从最终
`risk_score` 反解 ice、wave、wind、current 或 water level，也不得读取 A/B 私有输入后自行重算。

Sidecar 的作用是回答“这个格点为什么是该风险值”，并为后续“路线为什么被选中”的展示提供
一类证据。它不替代 C 的 objective、航程、ETA、route-level risk aggregation 或 selection 证据。

### Key Delta Table（2026-08-23 20:01 +08:00）

| Metric / Claim | Before | After | Verdict |
|---|---|---|---|
| 逐格 explanation contract | NONE | `risk-explanation.v1` DRAFT schema | IMPROVED / DESIGN ONLY |
| Schema/example validation | NONE | 11/11 tests PASS | UNIT_PASS |
| `bc.risk-frame.v2` | FROZEN_COMPATIBLE | UNCHANGED | PASS |
| B formula | `deterministic_environment_components_v2` | UNCHANGED | PASS |
| C planner / D calculation | current production behavior | UNCHANGED | PASS |
| Real producer / Viewer panel | NOT_IMPLEMENTED | NOT_IMPLEMENTED | NO CHANGE |

### Claim Matrix（2026-08-23 20:01 +08:00）

| Claim | Status | Validation Level | Evidence | Notes / Limitation |
|---|---|---|---|---|
| v1 schema 可表达完整、部分、不可用解释 | PASS | UNIT_PASS | `tests/test_risk_explanation_v1.py` | 仅设计 fixtures |
| Sidecar 缺失不改变 Viewer 主行为 | PASS | UNIT_PASS | missing-sidecar policy test | 尚未进入 D production code |
| identity/risk mismatch 失败关闭 | PASS | UNIT_PASS | identity/risk mismatch tests | 仅 proposal semantic validator |
| 部分 sidecar 不臆造贡献 | PASS | UNIT_PASS | partial/unavailable tests | producer 尚不存在 |
| 真实格点解释已发布 | FAIL | NOT_IMPLEMENTED | N/A | 本轮明确不实施 |
| “为什么选择该路线”已完整回答 | PARTIAL | NOT_IMPLEMENTED | 本报告边界分析 | 还需 C/D route-level explanation |

## 2. Scope / Non-Scope（2026-08-23 20:01 +08:00）

本轮范围：

- 提出 `risk-explanation.v1` JSON Schema；
- 提供明确标注为 `design_example` / `synthetic` 的示例 artifact；
- 定义 identity、coverage、完整/部分/不可用、fail-closed 和 optional-consumer 规则；
- 提出 D 点击格点的 UI 概念和未来 owner 分工；
- 创建可执行 schema 与跨字段语义测试。

本轮明确不做：

- 不修改 B 公式、模型配置或正式构建路径；
- 不修改 `bc.risk-frame.v2` Schema、RiskFrame payload 或 committed window；
- 不修改 C planner、sampling、cost、route selection 或任何 C contract；
- 不修改 D calculation、Viewer runtime 或当前 bundle；
- 不生成、覆盖或重放任何正式/冻结 artifact；
- 不把示例数据描述为真实模型输出或科学解释。

## 3. Starting Baseline（2026-08-23 20:01 +08:00）

| 项目 | 起点 |
|---|---|
| Repo | `arctic_route_governance` |
| Branch | `research-validation-system` |
| Starting HEAD | `b0a10bc1fe588b2eefdb5e82c2c831048fef0ce2` |
| Working tree | clean |
| Risk contract | `bc.risk-frame.v2` |
| Window identity | `CommittedRiskWindow.commit_id = risk-window-sha256-<content_digest>` |
| Known limitation | RiskFrame 只有最终风险、等级、置信度和来源摘要，没有逐格 contributor |

当前 B 规则是 11 个归一化 component 的加权和。该事实允许未来 B research exporter 在公式求值
处生成精确加性贡献；但现有 RiskFrame 本身不包含原始 component arrays，因此不能只读
RiskFrame 后可靠重建解释。

## 4. Git Final State（2026-08-23 20:01 +08:00）

| repo | branch | start HEAD | end HEAD | origin tracking | ahead / behind | working tree | commits | push status |
|---|---|---|---|---|---|---|---|---|
| `arctic_route_governance` | `research-validation-system` | `b0a10bc` | 本报告所在 design commit | `origin/research-validation-system` | `1 / 0`（本地提交后） | clean（本地提交后） | `design: propose risk explanation sidecar` | NOT PERFORMED |

本报告不记录自引用 commit hash；最终交付回复提供精确 end HEAD 和 clean 状态。

## 5. Filesystem & Resource Safety（2026-08-23 20:01 +08:00）

| 项目 | 结果 |
|---|---|
| Allowed write root | `/root/my_project/arctic_route_governance` |
| Writes outside allowed root | NONE |
| `MemAvailable` before | 5.8 GiB |
| Lowest observed `MemAvailable` | 5.7 GiB |
| Swap before / peak / after | 34 MiB / 无重任务，峰值 N/A / 34 MiB |
| Peak RSS | N/A；仅 JSON/schema 小文件校验 |
| OOM | NO |
| Heavy-task overlap | N/A；未运行 replay、A/B/C 计算或 Browser E2E |

## 6. Code / Architecture Changes（2026-08-23 20:01 +08:00）

### Schema（2026-08-23 20:01 +08:00）

机器可读提案位于
[`risk-explanation.v1.schema.json`](../../current/proposals/risk-explanation.v1.schema.json)。
顶层结构为：

```text
risk-explanation.v1
├── publication_status: COMPLETE | PARTIAL | UNAVAILABLE
├── identity: exact committed RiskWindow identity
├── producer: formula/decomposition/provenance/maturity
└── frames[]
    ├── risk_frame_id + frame_time
    ├── grid + coverage
    └── cells[]
        ├── cell: row/column/latitude/longitude
        ├── risk: score/level/confidence
        ├── contributors[]
        ├── reason
        └── uncertainty: missing_data/explanation_gaps
```

### Schema Decision（2026-08-23 20:01 +08:00）

1. **独立 sidecar，不扩展 RiskFrame。** `risk_window_id` 必须等于
   `CommittedRiskWindow.commit_id`；每帧再绑定 `risk_frame_id`、`frame_time` 和 `grid_id`。
2. **格点使用索引与坐标双重身份。** `row_index` / `column_index` 用于确定性查找，
   `latitude` / `longitude` 必须与 RiskFrame 坐标轴交叉验证，不能近邻吸附。
3. **风险字段是只读镜像。** `risk.score`、`risk.level`、`risk.confidence` 只用于发现
   sidecar 与 RiskFrame 错配；D 永远以 RiskFrame 为权威，不用 sidecar 覆盖风险值。
4. **`contribution` 是对 `risk_score` 的加性贡献。** 它不是原始 ice concentration、wave
   height 或 wind speed，也不是百分比。`COMPLETE` 要求所有 formula component 被恰好覆盖，
   且 `sum(contribution) == risk.score`（建议容差 `1e-6`）。
5. **contributors 使用可扩展列表。** `contributor_id` 可表达 `ice`、`wave`、`wind`、
   `current`、`water_level`，同时允许当前公式实际存在的 `freezing` 与 `visibility`，避免把
   未列出的非零贡献藏起来。`component_ids` 记录分组依据。
6. **reason 由 producer 断言，D 不生成。** `reason.code` 支持稳定机器语义，`text` 与
   `locale` 支持人读展示；`main_contributor_ids` 必须引用已发布 contributors。
7. **缺失不等于零。** 未验证 contributor 必须缺席，并在 `explanation_gaps` 或
   `missing_data` 中声明；禁止发布 `null` contribution，也禁止 D 默认成 `0`。

生产集成若采用非加性模型，只有模型本身能够提供经审阅的 attribution 时才可使用
`source_provided_attribution_v1`；否则对应格点必须为 `UNAVAILABLE`，不得强行套用加性解释。

## 7. Semantic / Contract Changes（2026-08-23 20:01 +08:00）

### Compatibility（2026-08-23 20:01 +08:00）

| 情形 | 新 consumer 行为 | 主 Viewer / RiskFrame 行为 |
|---|---|---|
| Sidecar 缺失 | 不启用解释面板，或显示 explanation unavailable | 完全保持原行为 |
| `schema_version` 不支持 | 拒绝整个 sidecar | 完全保持原行为 |
| Window/frame/grid identity mismatch | 拒绝整个 sidecar | 完全保持原行为 |
| risk snapshot mismatch | 拒绝整个 sidecar | RiskFrame 仍为权威 |
| `COMPLETE` 且校验通过 | 显示 producer 发布的 contributors/reason | 不重算风险 |
| `PARTIAL` 且校验通过 | 只显示已发布项并明确 “Partial explanation” | 不补零、不补文案 |
| `UNAVAILABLE` | 不显示 contributors，只显示明确 unavailable/missing reason | 不把未知显示为安全 |
| 结构损坏、重复 cell、coverage 不一致 | 拒绝整个 sidecar | 完全保持原行为 |

这里的 fail-closed 作用域是**解释能力**：任何不可证明的解释都不展示；sidecar 是可选功能，
所以它的失败不得阻断已经通过验证的基础 RiskFrame/Viewer 展示。

正式 contract/business semantics 变化：**NONE**。`bc.risk-frame.v2` 字段、单位、极性、时间、
canonical ID、B→C 原子窗口、C route 计算和 D 当前选择语义均不改变。

## 8. Experiments / Alternatives（2026-08-23 20:01 +08:00）

| 方案 | 结果 | 决策原因 |
|---|---|---|
| 向 RiskFrame 增加 contributor arrays | REJECTED | 破坏本轮冻结边界并扩大 C 正式输入 |
| D 从 `risk_score` 或 A 数据反推 contributors | REJECTED | 数学上不可逆、跨 owner、会制造解释 |
| 固定只有五个 contributor 字段 | REJECTED | 当前公式还包含 freezing、visibility 和多个 ice component，容易遗漏非零贡献 |
| 通用 contributor list + `component_ids` | SELECTED | 可表达用户要求字段，也能完整绑定当前/未来公式 |
| D 根据最大数值生成自然语言 reason | REJECTED | 把解释业务规则放进展示层，partial 时尤其可能误导 |
| Producer 发布 reason + code + evidence binding | SELECTED | D 只校验和显示，可审计且可失败关闭 |
| 每帧强制全密集 cell array | NOT REQUIRED IN v1 | `coverage` 支持完整或显式稀疏；COMPLETE 仍要求零 omitted |

## 9. Authoritative Run / Real Validation（2026-08-23 20:01 +08:00）

`NOT RUN`。本轮没有修改生产代码，也没有 sidecar producer，因此未运行 formal B build、C
planning、Orchestrator export、D Browser E2E、12h/24h replay 或真实数据对照。设计示例是
`synthetic` / `design_example`，不能作为真实解释证据。

## 10. Performance Breakdown（2026-08-23 20:01 +08:00）

| 项目 | Before | After | Delta / Verdict |
|---|---|---|---|
| Production runtime | N/A | N/A | 未集成，无变化 |
| Viewer bundle size | N/A | N/A | 未生成真实 sidecar |
| Proposal tests | NONE | 11 tests / 0.016 s（单次记录） | 仅设计校验，不代表生产性能 |

完整逐格 sidecar 可能显著增加 artifact 体积；压缩、分帧索引、按需加载和缓存策略必须在生产
提案阶段以真实 31×11×145 或更大网格测量，不能从本示例外推。

## 11. Correctness / Validation（2026-08-23 20:01 +08:00）

运行命令：

```bash
python3 -m unittest discover -s tests -v
```

验证环境：Python `3.12.3`、`jsonschema 4.10.3`。结果：`11 tests PASS`。覆盖：

| Gate | Result | Evidence |
|---|---|---|
| JSON syntax | PASS | `python3 -m json.tool` schema + example |
| Draft 2020-12 schema validity | PASS | `Draft202012Validator.check_schema` |
| Example validation | PASS | schema + semantic reference checks |
| COMPLETE contribution sum/component coverage | PASS | positive + negative cases |
| PARTIAL no-invention behavior | PASS | only retained components + explicit gaps |
| UNAVAILABLE contributor prohibition | PASS | invalid contributor rejected |
| Unsupported version | PASS | schema rejection |
| Duplicate cell / coverage | PASS | semantic rejection |
| Window identity mismatch | PASS | explanation fallback to base view |
| Risk value mismatch | PASS | explanation fallback to base view |
| Missing sidecar | PASS | base Viewer mode retained |
| Integration / real data / Browser E2E | NOT RUN | no production integration in scope |
| Route integrity / L1 / L2 | N/A | planner and geometry unchanged |
| Manifest / snapshot | N/A | no production artifact publication |

Schema 负责结构与局部条件；跨字段语义 validator 必须负责 identity、格网、coverage、重复 cell、
risk 镜像、component coverage 和贡献和。生产方不能只说“JSON Schema PASS”。

## 12. Determinism / Reproducibility（2026-08-23 20:01 +08:00）

状态：`RUN`（proposal fixtures）。同一受控文件输入的 schema/语义测试无 wall-clock 字段，结果
确定。未实现 sidecar canonical content ID，因此本轮不声称生产 artifact byte-level
determinism；未来 producer 必须定义 canonical JSON、摘要范围和不可变发布策略。

## 13. Artifacts / Provenance（2026-08-23 20:01 +08:00）

| Artifact | SHA-256 | Tracked | Provenance / role |
|---|---|---|---|
| `current/proposals/risk-explanation.v1.schema.json` | `88eb2fc3a6d125b9d2b31daa2cfe97910f7a856fc1cac5785bc5ad6fa75978ff` | YES | DRAFT machine-readable proposal |
| `current/proposals/risk-explanation.v1.example.json` | `b1554b6fc596456ec4a8befea0231d4eaff181e98b8f41e883173f59df99053a` | YES | `synthetic` / `design_example` |
| `tests/test_risk_explanation_v1.py` | 运行时测试源 | YES | proposal-only validation |
| 本报告 | N/A（自描述文档） | YES | SUPPORTING design evidence |

示例中的 hash-like identity 是模式合法的占位值，不对应现有正式 RiskWindow/RiskFrame，也不得
写入正式 store、Viewer bundle 或验收报告作为真实来源。

### Example（2026-08-23 20:01 +08:00）

完整示例见
[`risk-explanation.v1.example.json`](../../current/proposals/risk-explanation.v1.example.json)。
核心单元为：

```json
{
  "cell": {
    "row_index": 0,
    "column_index": 0,
    "latitude": 72.25,
    "longitude": 55.75
  },
  "explanation_status": "COMPLETE",
  "risk": {"score": 0.32, "level": 2, "confidence": 0.8},
  "contributors": [
    {"contributor_id": "ice", "contribution": 0.12},
    {"contributor_id": "wave", "contribution": 0.08},
    {"contributor_id": "wind", "contribution": 0.05},
    {"contributor_id": "current", "contribution": 0.04},
    {"contributor_id": "water_level", "contribution": 0.03}
  ],
  "reason": {
    "code": "DOMINANT_CONTRIBUTOR",
    "text": "High ice concentration contribution",
    "locale": "en",
    "main_contributor_ids": ["ice"]
  }
}
```

为便于阅读，上述摘录省略了完整 `component_ids`、零贡献 formula components 和
`uncertainty`；它不是独立有效 artifact，应以链接的完整 JSON 为准。

## 14. Known Limitations / Technical Debt（2026-08-23 20:01 +08:00）

| TD-ID | Impact | Severity | Next action |
|---|---|---|---|
| REX-01 | 现有 RiskFrame 无 component arrays，不能事后可靠反解 | HIGH | 在 B 公式求值点设计只读 research exporter；不得改 RiskFrame |
| REX-02 | 无真实 producer / immutable store / manifest | HIGH | owner 审批后单独提出实现与发布协议 |
| REX-03 | 无 Orchestrator optional transport 与 D consumer | HIGH | 先 producer fixture，再 consumer fail-closed test |
| REX-04 | sidecar 只解释格点风险，不完整解释 route selection | HIGH | 与 C 已发布 objective/route metrics/selected identity 联合展示 |
| REX-05 | 当前 B formula 为 `demo_unvalidated` | HIGH | 解释只能说明该工程公式如何得到数值，不能声称科学因果或适航结论 |
| REX-06 | human-readable reason 的本地化与文案治理未定 | MEDIUM | 以 code 为稳定语义，review producer text/locale policy |
| REX-07 | 完整网格 sidecar 体积和加载成本未知 | MEDIUM | 用真实尺寸 benchmark 分帧、压缩、索引和缓存 |
| REX-08 | v1 尚未定义 sidecar 自身 canonical ID | MEDIUM | 生产提案定义 canonical JSON、digest、原子发布与 supersession |

最关键限制是：`risk-explanation.v1` 可以解释一个 cell 的风险构成，但路线选择还受 C 的
objective mode、距离、ETA、风险聚合、hard constraint、置信度和候选比较影响。只有将 sidecar
与已有 route artifact 一起展示，才能逐步回答“为什么选这条路线”。

## 15. Decision / Next Phase（2026-08-23 20:01 +08:00）

### Future Integration（2026-08-23 20:01 +08:00）

建议 owner 与数据流：

```text
B research exporter
  owns formula/component attribution + reason evidence
        |
        | optional immutable risk-explanation.v1
        v
Orchestrator presentation export
  validates identity and transports without recomputation
        |
        v
D Viewer optional consumer
  validates against displayed RiskFrame and renders only

C planner: no input, no output, no change
```

D UI 概念：用户点击已显示的 risk cell 后，面板直接读取 sidecar：

```text
Risk Level 3

Main contributors
  Ice concentration
  Wave

Confidence
  0.72

Explanation status
  COMPLETE | PARTIAL | UNAVAILABLE
```

D 不从 contributor 数值计算 Risk Level，不自行挑选 main contributors，不生成 reason，不把缺失
项补为零。Sidecar 缺失、无效或不匹配时关闭解释区域并保留当前 Viewer；`PARTIAL` 必须显式
标注并只展示 producer 已发布内容。

推荐下一阶段按以下门禁推进：

1. B 语义负责人审阅 contributor grouping、贡献和、reason policy 与 `demo_unvalidated` 标签；
2. Orchestrator/D 负责人审阅 optional transport、体积预算和 fallback UX；
3. 先实现 proposal-only producer fixture 和独立 store，不接 C、不改 RiskFrame；
4. 用同一真实 committed window 对 sidecar 与 RiskFrame 做逐格 identity/value 对照；
5. 通过 producer/consumer/fail-closed/size gates 后，再决定是否加入 Viewer bundle；
6. 最后才做 Browser E2E，并将“cell risk explanation”与“route selection explanation”分开验收。

本轮决策状态：`DRAFT / REVIEW REQUIRED / NOT AUTHORIZED FOR PRODUCTION`。明确不要修改
RiskFrame、B formula、C planner 或让 D 重算风险。
