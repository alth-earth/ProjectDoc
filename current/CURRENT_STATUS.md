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

# Research Validation System Current Status

## Winter Formal Handoff Milestone（2026-08-23 01:16 +08:00）

| Workstream | Current state | Evidence |
|---|---|---|
| Winter required coverage | 12_OF_12_COMPLETE | 1,212-record frozen A bundle |
| Winter DatasetBundle | FROZEN_ARTIFACT_READY | active `a-bundle-a2146dd0adbaa7db77a6beb7`; 144 h minimum; parse/digest/doctor pass |
| Winter RunContext | PUBLISHED / SCHEMA_PASS | `run-441b03c8-d45b-5414-b0e8-b7fd0d990c22`; official atomic generator |
| Winter ExecutionSpec | PUBLISHED / SCHEMA_PASS | strict `orchestrator.execution-spec.v1`; identity aligned |
| A→B formal handoff | READY_FOR_B_VALIDATION | exact archive intake-only PASS; B not started |
| Winter B/C/D | NOT_STARTED | downstream execution remains prohibited |

Current verdict: Winter source acquisition, corrected A immutable bundle,
matching `RunContext.v2`, strict `ExecutionSpec.v1` and Orchestrator intake-only
全部通过。intake 使用 exact archive resolver 复现 1,212 records；B/C/D 未执行，因此
handoff 是 `READY_FOR_B_VALIDATION`，不是 `B_WINTER_VALIDATION=PASS`。旧 132 小时
minimum bundle 继续作为 superseded historical evidence 保留。

Supporting evidence:

- [Winter source validation](../reports/research-validation/WINTER_SOURCE_VALIDATION_REPORT.md)
- [Meteorological source comparison](../reports/research-validation/WINTER_MET_SOURCE_COMPARISON.md)
- [Winter identity audit](../reports/research-validation/WINTER_EXPERIMENT_IDENTITY_AUDIT.md)
- [Winter handoff validation](../reports/research-validation/WINTER_HANDOFF_VALIDATION_REPORT.md)
- [Winter immutable bundle reissue](../reports/research-validation/WINTER_BUNDLE_REISSUE_REPORT.md)
- [Winter formal handoff](../reports/research-validation/WINTER_FORMAL_HANDOFF_REPORT.md)

Interface stabilization verdict：A→B `DatasetBundle.v2 + RunContext.v2`、B→C
`bc.risk-frame.v2 + committed hourly window`、C formal v2/v3 与 Orchestrator→D
presentation baseline 均可保持现有版本。Winter B validation 必须先审计 unknown 是否被
正确 hard-mask；C route candidates 在 Replay Viewer 仍为 `NOT_PUBLISHED`。

## 第三阶段真实实验结果（2026-08-22 02:34 +08:00）

> Historical Round3 checkpoint; the Winter identity gate above is the current state.

| Workstream | Current state | Evidence |
|---|---|---|
| Winter Copernicus acquisition | PARTIAL / 8_TYPES_DOWNLOADED | 1,064 target-window records, eight immutable source snapshots, exact endpoints |
| Winter 12-type A coverage | PARTIAL / 9_OF_12_COMPLETE | eight Copernicus rows + cached GEBCO mask complete; bundle not persisted |
| Winter GFS | BLOCKED_BY_SOURCE_AND_CADENCE | NCEI 202602 object/THREDDS paths absent; direct inventory 404; 6 h adapter vs 3 h coverage gate |
| A archive integrity | VALIDATED | doctor 5,232 checked, 0 errors, 0 warnings |
| C exact sample profile | EXPERIMENTAL / REAL_B_FRAME_PASS | 705,469 requests; 242,992 exact repeats; 34.444% reuse ceiling |
| C bounded LRU | IMPLEMENTED / EXPERIMENTAL_DEFAULT_OFF | 50k cap; median 76.281 s → 65.012 s; complete route digest unchanged |
| B-C optimized medium path | EXPERIMENTAL / VALIDATED | fixed B input and endpoint; 3 independent runs per mode; no contract/publication change |

At this historical checkpoint no winter DatasetBundle, RiskFrame, route or Viewer artifact existed. The C LRU
is available only through the experiment benchmark and is not used by formal
ingress. Full 48h replay, heavy integration and determinism twin-run were not
run.

## 第二阶段真实实验结果（2026-08-22 01:11 +08:00）

> Historical Round2 checkpoint; the Round3 table above is the current state.

| Workstream | Current state | Evidence |
|---|---|---|
| Winter 12-type feasibility | BLOCKED_BY_DATASET | all 12 local target-corridor rows have zero February 2026 records; no download/fabrication |
| B formal fixed-grid comparison | EXPERIMENTAL / REAL_DATA_PIPELINE_PASS | 78 formal frames each at 16×7, 31×11, 60×21; B build 4.03/3.86/3.91 s |
| B→C coupling baseline | EXPERIMENTAL / REAL_B_FRAMES + REAL_C_SEARCH_PASS | recommended route 10.51 s at 112 nodes and 75.00 s at 341 nodes |
| C cache observability | IMPLEMENTED / UNIT_PASS | existing edge-geometry cache reports hit/miss/entries; behavior unchanged |
| Route candidate presentation | DRAFT / PLANNED | backward-compatible proposal; current bundle remains NOT_PUBLISHED |

The formal B comparison used the existing summer archive because winter data is
blocked. Its outputs were not published to the B store. The C benchmark decoded
public `bc.risk-frame.v2` documents and ran real C components, but did not pass
through committed-window formal ingress; it is experimental coupling evidence,
not a full integration claim.

## 第二阶段加速结果（2026-08-22 00:24）

> Historical preparation checkpoint; the Round3 table above supersedes its
> winter and cache readiness rows.

| Workstream | Current state | Evidence |
|---|---|---|
| P0 Contract Registry | IMPLEMENTED / DOCUMENT_VALIDATED | ownership/version/status registry, proposal template, development ownership matrix |
| P1 Winter configuration | IMPLEMENTED / UNIT_VALIDATED | new `scenario.v2` identity; contracts 19 PASS |
| P1 Winter data/artifact | BLOCKED_BY_DATASET | no matching 12-type source bundle; no winter artifact fabricated |
| P2 B fixed-grid experiment | EXPERIMENTAL / UNIT_VALIDATED | synthetic kernel plus formal 78-frame comparison; B 61 non-integration PASS |
| P3 C component profiling | EXPERIMENTAL / UNIT_VALIDATED | component profile plus real-frame BC benchmark; C 146 non-integration PASS |
| P3 edge geometry cache identity | IMPLEMENTED / UNIT_VALIDATED | cache key now includes sample count; focused regression included |
| P4 professional navigation aids | IMPLEMENTED / BROWSER_E2E_PASS | Firefox: graticule, coordinate labels, scale bar, grid north, independent toggle |

No core contract version, A acquisition implementation, B risk formula/level
policy, C search algorithm/route semantics, Orchestrator export, frozen artifact,
or 48h replay was changed.

## 当前阶段（2026-08-21 23:18）

项目已从 Competition Demo Freeze 转入 **Research Validation System
Enhancement Phase**。冻结演示基线保留在 `demo-engineering`，当前开发只在
`research-validation-system` 进行。这个阶段先冻结接口事实和验证口径，再开展
B/C/D 并行研究；不把规划中的冬季场景、自适应网格或候选路线展示写成已有能力。

| Branch | Meaning | Status |
|---|---|---|
| `main` | RC1 baseline | FROZEN |
| `rc2-development` | RC2 baseline | FROZEN |
| `demo-engineering` | competition demo baseline | FROZEN |
| `research-validation-system` | research validation enhancement | ACTIVE |

`/root/my_project` 是多个仓库的工作区，当前没有 root Git。各子仓库分别维护自己的
`research-validation-system` 分支。

## 当前真实架构（2026-08-21 23:18）

| Module | Research-stage role | Runtime boundary |
|---|---|---|
| A | Environmental Data Acquisition | 发布 `PreparedWindow` / `a.dataset-bundle.v2` 与 provenance |
| B | Risk Assessment and Forecast | 消费 A 公共 bundle，发布 `bc.risk-frame.v2` |
| C | Risk-aware Navigation Decision | 消费 B risk frame，发布 route plan / layered route set |
| D | Visualization and Validation Platform | 只消费已发布 presentation artifact；唯一 Viewer runtime owner |
| Orchestrator | Pipeline / Artifact / Presentation Adapter | 编排 A→B→C，执行 replay，验证并投影 presentation bundle |

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

| Capability | Implementation | Validation | Current qualification |
|---|---|---|---|
| A 12-type public data bundle | IMPLEMENTED | ARTIFACT_PASS | 夏季 RC1/RC2 + active Winter 144 h minimum frozen bundle |
| B hourly deterministic risk frame | IMPLEMENTED | AUTHORITATIVE_PASS | 模型仍为 `demo_unvalidated`，不是科学标定结论 |
| B fixed target grid | IMPLEMENTED | UNIT/ARTIFACT_PASS | RC2 显式 31×11；代码默认配置可为 16×7 |
| B adaptive grid | NOT_IMPLEMENTED | NOT_RUN | 研究计划，不得隐式改变 C regular-grid contract |
| C three objectives | IMPLEMENTED | AUTHORITATIVE_PASS | fastest / low_risk / recommended |
| C four layers × three objectives | IMPLEMENTED | AUTHORITATIVE_PASS | `FourLayerRoutePlanSet.v3` 明确验证 12 路线 |
| C causal replay planning | IMPLEMENTED | AUTHORITATIVE_PASS | 12h determinism inherited；48h product artifact verified |
| D presentation Viewer | IMPLEMENTED | BROWSER_E2E_PASS | Firefox；单 Simulation Clock；artifact driven |
| 48h replay Viewer | IMPLEMENTED | BROWSER_E2E_PASS | 49 snapshots、2881 minute states、49 risk frames |
| C route candidates in replay Viewer | NOT_IMPLEMENTED | NOT_PUBLISHED | bundle 明确 `status=NOT_PUBLISHED`, `candidates=[]` |
| Winter scenario configuration | IMPLEMENTED | CONFIG_VALIDATED | 144 h scenario; 12/12 source rows complete |
| Winter DatasetBundle | IMPLEMENTED | FROZEN_ARTIFACT_READY | active bundle ID/digest/SHA frozen；minimum/requested horizon 均为 144 h |
| Winter A→B handoff | IMPLEMENTED | READY_FOR_B_VALIDATION | RunContext/ExecutionSpec/schema/exact intake-only PASS |
| Winter B/C/D artifact | NOT_IMPLEMENTED | NOT_STARTED | 合法 experiment identity 已就绪；等待下一轮 |
| B fixed-grid experiment harness | IMPLEMENTED | UNIT_PASS / EXPERIMENTAL_REAL_DATA | formal builder comparison completed; output remains unpublished |
| C component profiler / BC benchmark | IMPLEMENTED | UNIT_PASS / EXPERIMENTAL_REAL_DATA | real B frames and real C search; committed ingress not exercised |
| D professional navigation aids | IMPLEMENTED | BROWSER_E2E_PASS | bundle metadata only; canonical transform/aspect preserved |

## 冻结语义（2026-08-21 23:18）

- A→B 只通过公共 `PreparedWindow` / `DatasetBundle.v2` 和匹配的
  `RunContext`；B 不扫描 A 私有 cache、SQLite 或 raw 目录。
- B→C 以 `bc.risk-frame.v2` 为正式边界；unknown fail closed，
  `DATA_UNAVAILABLE != safe`。
- C 拥有最终路线、速度、ETA 和重规划决策；D 不重新计算。
- `REPLAN_DECIDED != REPLAN_ADOPTED`，pending route 不提前替换 authoritative
  route，completed track append-only。
- D 是唯一 Viewer runtime owner；Orchestrator 只拥有 replay 与 presentation
  adapter/export。
- 当前正规网格是 rectilinear regular grid。Adaptive Grid 在 contract proposal
  通过前只能作为隔离实验。

## 当前事实缺口（2026-08-21 23:18）

1. Contract ownership registry 已建立；尚待各 owner 对未来 candidate/adaptive
   proposal 逐项审批，registry 本身不等于 proposal 批准。
2. C 已有 12-route 输出，但 replay export 没有发布候选 geometry/metrics；不能把
   19 个时间修订版误称为 19 个候选。
3. 冬季场景、12 类 source rows、144 h minimum frozen bundle、matching
   RunContext/ExecutionSpec 与 intake-only 已建立。B/C/D 冬季验证链尚未开始；下一缺口是
   批准显式 B Winter profile 并生成第一批正式 RiskFrame。
4. B 规则模型未标定；正式固定网格 build 已测，但进程 RSS 包含已加载 A window，
   独立增量内存与重复运行方差仍未测；adaptive grid 未实现。
5. C baseline/medium 联合性能已测；medium exact-sample 50k LRU 已在 default-off
   benchmark 中取得 14.77% median 收益。formal ingress/12-route promotion、共享搜索与
   incremental replanning 均未实现。
6. D 已建立基础专业导航辅助层；route candidate compare 与研究 provenance/
   uncertainty 交互仍取决于真实 presentation contract。

详细依据见
[RESEARCH_VALIDATION_GAP_ANALYSIS.md](RESEARCH_VALIDATION_GAP_ANALYSIS.md)。

## 当前阻塞与风险（2026-08-21 23:18）

| Risk | State | Handling |
|---|---|---|
| 多人并行前 contract 所有权不清 | CONTROLLED | registry/template/目录 ownership 已建立；breaking proposal 仍需 owner approval |
| Winter identity gate | READY_FOR_B_VALIDATION | formal identity + exact intake PASS；B 尚未运行 |
| B grid policy 与 C regular-grid 假设耦合 | EXPERIMENTAL EVIDENCE | formal bounded build/C comparison complete for baseline+medium; fine needs explicit budget |
| C candidate 未投影到 replay bundle | DRAFT / PLANNED | proposal exists; current NOT_PUBLISHED semantics unchanged |
| 当前 demo baseline 回退 | CONTROLLED | frozen branch/artifact 不改；研究 artifact 使用新 identity |
| B Murmansk default-grid integration expectation | OPEN FINDING | 未筛选 B suite 在 allowed-region endpoint mapping 失败；不在本轮改配置语义 |

## 本轮验证边界（2026-08-23 01:16 +08:00）

Winter formal identity 双 schema、重建 identity、run/spec binding 与 exact archive
intake-only PASS。Contracts 19 PASS；Orchestrator fast 84 PASS、2 deselected；两仓库 Ruff
clean。最终三件套 intake-only wall `3:26.43`、peak RSS `978,740 KiB`。本轮没有运行 B/C/D、48h
replay、heavy integration 或新的 determinism twin-run；这些旧证据均未提升为本轮重验。
