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

## B Risk Calibration Research Gate（2026-08-23 20:45 +08:00）

| Workstream | Current state | Evidence |
|---|---|---|
| Current B scale | DETERMINISTIC_ENGINEERING_BASELINE | 11 normalized components weighted sum；`demo_unvalidated` |
| Scientific calibration | NOT_ESTABLISHED | 无 expert/outcome/physics threshold validation |
| Winter finite distribution | REAL_ARTIFACT_AUDIT_PASS | mean `0.119016`；P95 `0.226415`；93.069778% L1 |
| Threshold change | NOT_APPROVED | `0.2/0.4/0.6/0.8` 保持 frozen baseline |
| Component attribution | NOT_IMPLEMENTED | RiskFrame 无逐格 contribution；sidecar 仍为 DRAFT |
| B/C/D runtime semantics | PRESERVED | 零代码、零 artifact 修改；C route response evidence 继承 |

当前 `risk_score` 只能解释为 weighted normalized hazard index，不是事故概率或经过实船结果
标定的严重度。等宽 level policy 对本 Winter 分布存在明显压缩，但这不足以单独批准新阈值。
下一 gate 是定义 operational target、建立跨场景 calibration dataset、发布 B-owned shadow
component contribution，并比较 expert/physics/statistical/outcome-based 方法。

Supporting evidence:

- [Risk calibration research](../reports/research-validation/RISK_CALIBRATION_RESEARCH_REPORT.md)

## Winter Combined Research Viewer（2026-08-23 20:14 +08:00）

| Workstream | Current state | Evidence |
|---|---|---|
| Winter combined presentation | REAL_E2E_PASS | one scenario/run/bundle/RiskWindow/candidate identity；145 frames；12 routes |
| D Winter Research View | REAL_E2E_PASS | Firefox；risk/hard/routes/ship/Run/Pause/layer selector |
| Browser console/network | PASS | 0 errors；0 warnings；7 required resources HTTP 200 |
| Navigation simulation | EXPERIMENTAL / REAL_E2E_PASS | 3,206 1-minute states；C selected route waypoint ETA projection |
| Winter causal replay/replanning | NOT_IMPLEMENTED | 无同 identity manifest/snapshots/events；未伪造 |
| A/B/C/contracts/frozen artifacts | PRESERVED | 本轮零修改、零重算 |

当前 Viewer 已不再混用 Summer replay 与 Winter candidates。Orchestrator fail closed 绑定
active DatasetBundle、RunContext、145-frame committed RiskWindow、C v3 plan set、12-route
candidate sidecar 与 integrity evidence；D 再次校验 combined identity，并显式显示 scenario、
DatasetBundle、RunContext、RiskWindow 与 assembly ID。航行时间线来自 C full-voyage
recommended waypoint ETA，`source_replay=null`，因此该 milestone 证明 Winter research
navigation simulation，不证明 Winter causal replay 或 dynamic replanning。

Supporting evidence:

- [Winter combined Viewer integration](../reports/research-validation/WINTER_COMBINED_VIEWER_INTEGRATION_REPORT.md)

## D Research Visualization Phase 1 历史门槛（2026-08-23 16:59 +08:00）

> 该表记录 Phase 1 结束时状态；当前 combined Browser 状态以上方最新里程碑为准。

| Workstream | Current state | Evidence |
|---|---|---|
| B→C interface | STABLE | `bc.risk-frame.v2` committed-window boundary；unknown fail closed |
| C→Orchestrator interface | STABLE | real Winter `cd.four-layer-route-plan-set.v3`；4×3 atomic publication |
| Orchestrator→D interface | STABLE | `presentation.route-candidates.v1` exact projection；no rerank/recompute |
| D Research View | IMPLEMENTED / UNIT_PASS | 4 layer selector、3 objective compare、artifact metrics、candidate geometry |
| Existing frozen Viewer fallback | BROWSER_E2E_PASS | Firefox；NOT_PUBLISHED → `SINGLE_ROUTE_FALLBACK`；console 0；required HTTP 200 |
| Winter combined Viewer | NOT_IMPLEMENTED | 尚无同一 Winter identity 的 risk/replay/candidate combined bundle |

D 现在只在完整、scenario-matched 的 12-route PUBLISHED package 下启用 Research View；
用户 route selection 是 display-only highlight，不修改 C 的 `selected_candidate_id`。缺失
sidecar、4×3 不完整、metrics/geometry 非法、hard violation 或 scenario mismatch 均 fail
closed 回到现有 authoritative route。真实 Winter sidecar 的 metrics/identity 已由 78 项 D
tests 验证；现有 48h frozen bundle 的 Operational Replay 由 Firefox 复测通过，但由于尚无
Winter combined bundle，本轮不得声明 Winter Research Browser E2E。

Supporting evidence:

- [B/C/D interface status](../reports/research-validation/B_C_D_INTERFACE_STATUS.md)

## Winter C Validation 与 D 并行接口门禁（2026-08-23 10:20 +08:00）

| Workstream | Current state | Evidence |
|---|---|---|
| A/B frozen inputs | PRESERVED | bundle、RunContext、ExecutionSpec、145-frame RiskWindow identity unchanged |
| C Winter consumer | PASS | exact committed window、formal provenance、31×11 endpoint mapping |
| C Winter validation | COMPLETED / EXPERIMENTAL | `cd.four-layer-route-plan-set.v3`；4×3=12；integrity 12/12 PASS |
| Winter route decision | OBSERVED_CHANGE | vs Summer authoritative initial：11/22 waypoint 不同，+11.658 km，+2.951 h |
| C→D candidate sidecar | INTERFACE_PASS | `presentation.route-candidates.v1` PUBLISHED；12 candidates；fail-closed fallback preserved |
| D parallel development | READY | D v3 loader 4 layers/12 plans；canonical risk metrics intake PASS |
| D Winter visualization | PHASE_1_UNIT_PASS | candidate map/compare 已实现；combined bundle 与 Winter Browser E2E 未完成 |

本轮首次完成真实 Winter C formal v3 planning。推荐线为 921.379560 km、53.405581 h，
avg/max risk 为 0.105651/0.189369。Summer Viewer 未发布 route-level risk metrics，故只对
有证据的 geometry/distance/ETA 做比较；不补造 Summer 风险数值，也不把观察性差异写成
已隔离的季节因果。

Supporting evidence:

- [Winter C smoke](../reports/research-validation/WINTER_C_SMOKE_REPORT.md)
- [Winter C route validation](../reports/research-validation/WINTER_C_ROUTE_VALIDATION_REPORT.md)
- [D interface readiness](../reports/research-validation/D_INTERFACE_READY_REPORT.md)
- [Winter data availability follow-up](../reports/research-validation/WINTER_DATA_AVAILABILITY_FOLLOWUP.md)
- [Winter C final report](../reports/research-validation/WINTER_C_VALIDATION_FINAL_REPORT.md)

## Winter B First Scientific Run（2026-08-23 02:44 +08:00）

| Workstream | Current state | Evidence |
|---|---|---|
| Winter DatasetBundle | FROZEN_ARTIFACT_READY | active `a-bundle-a2146dd0adbaa7db77a6beb7`，1,212 records，SHA/digest unchanged |
| A→B formal handoff | READY_FOR_B_VALIDATION | fixed RunContext/ExecutionSpec，exact-bundle input restore PASS |
| B Winter validation | COMPLETED / EXPERIMENTAL | medium 31×11；145 formal `bc.risk-frame.v2`；schema/store/readback PASS |
| Winter risk distribution | OBSERVED_CHANGE | Summer/Winter same realized grid comparison available；finite mean `0.045027961 → 0.119015786` |
| Unknown navigable nodes | 0 observed | Winter `unknown_navigable_nodes=0`；hard/reason consistency mismatch `0` |
| C Winter validation | NOT_STARTED | 本轮明确未运行 C planner |
| D Winter visualization | NOT_STARTED | 本轮明确未运行 D/Viewer |

当前结论：Winter B 已完成第一轮工程/研究验证，证明在相同 medium realized grid、hourly
cadence 和 B model configuration 下，Winter 输出风险分布发生变化。B 模型仍是
`demo_unvalidated`，且 Summer/Winter 数据源体系不同，因此该结果不是科学标定或仅由冬季
月份导致的因果结论。`DATA_UNAVAILABLE` 必须与有限风险分布分开解读。

Supporting evidence:

- [Winter B baseline decision](../reports/research-validation/WINTER_B_BASELINE_CONFIG_DECISION.md)
- [Winter B smoke report](../reports/research-validation/WINTER_B_SMOKE_REPORT.md)
- [Winter risk distribution audit](../reports/research-validation/WINTER_RISK_DISTRIBUTION_AUDIT.md)
- [Winter B validation report](../reports/research-validation/WINTER_B_RISK_VALIDATION_REPORT.md)

## Winter Formal Handoff Milestone（2026-08-23 01:16 +08:00；B 首轮结果见上方最新里程碑）

| Workstream | Current state | Evidence |
|---|---|---|
| Winter required coverage | 12_OF_12_COMPLETE | 1,212-record frozen A bundle |
| Winter DatasetBundle | FROZEN_ARTIFACT_READY | active `a-bundle-a2146dd0adbaa7db77a6beb7`; 144 h minimum; parse/digest/doctor pass |
| Winter RunContext | PUBLISHED / SCHEMA_PASS | `run-441b03c8-d45b-5414-b0e8-b7fd0d990c22`; official atomic generator |
| Winter ExecutionSpec | PUBLISHED / SCHEMA_PASS | strict `orchestrator.execution-spec.v1`; identity aligned |
| A→B formal handoff | READY_FOR_B_VALIDATION | exact archive intake-only PASS; B not started |
| Winter B/C/D at handoff time | NOT_STARTED | handoff 完成时的下游起点；B 首轮结果见上方最新里程碑 |

Current verdict at the handoff milestone: Winter source acquisition, corrected A immutable
bundle, matching `RunContext.v2`, strict `ExecutionSpec.v1` and Orchestrator intake-only
全部通过。该阶段只完成 intake；后续 B 首轮结果见本文件顶部最新里程碑。旧 132 小时
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
| C route candidates presentation | IMPLEMENTED | INTERFACE_PASS | real Winter 12-route sidecar PUBLISHED；既有 frozen Viewer bundle 仍保持 NOT_PUBLISHED |
| Winter scenario configuration | IMPLEMENTED | CONFIG_VALIDATED | 144 h scenario; 12/12 source rows complete |
| Winter DatasetBundle | IMPLEMENTED | FROZEN_ARTIFACT_READY | active bundle ID/digest/SHA frozen；minimum/requested horizon 均为 144 h |
| Winter A→B handoff | IMPLEMENTED | READY_FOR_B_VALIDATION | RunContext/ExecutionSpec/schema/exact intake-only PASS |
| Winter B RiskFrame / C/D artifact | B,C,D_IMPLEMENTED | B,C_FORMAL_VALIDATED / D_REAL_E2E_PASS | B 145 frames；C 12-route v3；D combined Firefox PASS |
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
2. C→D 已发布一个真实 Winter 12-route candidate set；replay 的 19 个时间修订仍不是
   19 组候选。多 decision candidate-set timeline 尚未定义。
3. 冬季场景、12 类 source rows、144 h minimum frozen bundle、matching
   RunContext/ExecutionSpec、B 145 帧 RiskFrame、C 12-route validation 与 D combined
   Browser E2E 已建立。下一缺口是正式 Winter causal replay/replanning（若研究门槛需要）；
   当前 3,206-state timeline 是 C waypoint ETA projection。
4. B 规则模型未标定；正式固定网格 build 已测，但进程 RSS 包含已加载 A window，
   独立增量内存与重复运行方差仍未测；adaptive grid 未实现。
5. C baseline/medium 联合性能已测；medium exact-sample 50k LRU 已在 default-off
   benchmark 中取得 14.77% median 收益。formal ingress/12-route promotion、共享搜索与
   incremental replanning 均未实现。
6. D 已建立基础专业导航辅助层、Research View、candidate geometry、四层三目标 compare
   与 Winter combined Browser E2E；环境 contributor / per-cell uncertainty presentation
   contract 仍待实现。

详细依据见
[RESEARCH_VALIDATION_GAP_ANALYSIS.md](RESEARCH_VALIDATION_GAP_ANALYSIS.md)。

## 当前阻塞与风险（2026-08-21 23:18）

| Risk | State | Handling |
|---|---|---|
| 多人并行前 contract 所有权不清 | CONTROLLED | registry/template/目录 ownership 已建立；breaking proposal 仍需 owner approval |
| Winter A/B/C/D gate | D_COMBINED_REAL_E2E_PASS | formal identity、B 145 frames、C 12-route v3 与 D Firefox PASS；causal replay 仍未实现 |
| B grid policy 与 C regular-grid 假设耦合 | EXPERIMENTAL EVIDENCE | formal bounded build/C comparison complete for baseline+medium; fine needs explicit budget |
| C candidate presentation | CONTROLLED / INTERFACE_PASS | proposal accepted；真实 Winter sidecar PASS；frozen bundle fallback unchanged |
| 当前 demo baseline 回退 | CONTROLLED | frozen branch/artifact 不改；研究 artifact 使用新 identity |
| B Murmansk default-grid integration expectation | OPEN FINDING | 未筛选 B suite 在 allowed-region endpoint mapping 失败；不在本轮改配置语义 |

## Formal Handoff 验证边界（2026-08-23 01:16 +08:00）

> 本节记录 Formal Handoff 当时的 intake-only 边界；B 首轮结果以本文顶部的最新里程碑为准。

Winter formal identity 双 schema、重建 identity、run/spec binding 与 exact archive
intake-only PASS。Contracts 19 PASS；Orchestrator fast 84 PASS、2 deselected；两仓库 Ruff
clean。最终三件套 intake-only wall `3:26.43`、peak RSS `978,740 KiB`。本轮没有运行 B/C/D、48h
replay、heavy integration 或新的 determinism twin-run；这些旧证据均未提升为本轮重验。
