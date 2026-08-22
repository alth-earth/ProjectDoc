---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
Document Role: SUPPORTING
Scope: Winter A freeze and B/C entrypoint audit
Canonical/Supporting: Supporting freeze audit; current status remains canonical
Branch: research-validation-system
Last Verified: 2026-08-22
---

# Winter A Freeze Audit Report

## 1. Executive Summary（2026-08-22 21:56 +08:00）

```text
WINTER_DATASET_STATUS = FROZEN_ARTIFACT_READY
A_TO_B_FORMAL_HANDOFF = BLOCKED_BY_MISSING_RUN_CONTEXT
B_WINTER_VALIDATION = NOT_STARTED
C_WINTER_VALIDATION = NOT_STARTED
D_WINTER_VISUALIZATION = NOT_STARTED
```

Winter A 已不再是 source-only 或仅生成未冻结状态：真实 CARRA 与 Copernicus/GEBCO
记录已形成可解析、内部 digest 一致、12/12 coverage complete 的 tracked
`a.dataset-bundle.v2`。但未找到与其身份匹配的 `RunContext.v2` 和 Winter execution spec，
所以不得把“bundle 冻结”升级为“正式 A→B handoff ready”。本轮没有运行 B/C、没有修改
算法/数据/contract/Viewer、没有 push。

## 2. Winter Dataset Status（2026-08-22 21:56 +08:00）

| Evidence | Value |
|---|---|
| Artifact | `work_package_a/data/tromso_to_isfjorden_outer_winter_20260215T000000Z_bundle.json` |
| Git state | tracked in A commit `39e9076` |
| Schema | `a.dataset-bundle.v2` |
| Bundle ID | `a-bundle-bd8957c4f10c7c73f395de23` |
| Internal bundle digest | `bd8957c4f10c7c73f395de2354f56e2b6bde2d0b7204b99c60e0d56284394d9b` |
| File SHA-256 | `5cf81c15162756f992bca83854e0b17cfac6be66197aed332d22ec29f8d4b795` |
| Size | 574,759 bytes |
| Records | 1,212 |
| Required types | 12/12 complete |
| Missing intervals | 0 in frozen requested window |
| Provenance | complete for all coverage rows |
| Requested window | 2026-02-15T00Z → 2026-02-21T00Z |
| Matching RunContext | NOT_FOUND |
| Standalone generation log | NOT_FOUND |

`DatasetBundle.from_dict` 可成功解析，并重验 bundle ID/digest 与 coverage。A doctor 检查
5,461 项，0 errors、0 warnings。bundle 中 1,211 条动态记录为保守的 `suspect` quality，
GEBCO 静态记录为 `good`；这不等于数据失败，也不应被改写成 calibrated evidence。

`generation_id` 不是 `a.dataset-bundle.v2` 字段，它属于 RunContext/执行身份。现有文档中
把 `generation_id=0` 写成 bundle 内字段的说法应修正。

## 3. Data Source Transition Audit（2026-08-22 21:56 +08:00）

Summer 的 wind/temperature/visibility 来自 NOAA GFS 0.25°；Winter 改为 C3S/ECMWF
CARRA East domain。A 将 2.5 km 曲线/投影网格以最大 25 km nearest 规则投影到 0.1°
canonical rectilinear 网格，仍发布 m/s、K、m 与 canonical 变量名。

其余动态变量保持同一 Copernicus product family；ocean current 使用既有明确标记的
detided fallback。land mask 继续使用 GEBCO，极性保持 `1=sea`、
`0=land_or_coast`。

B 不假定固定源网格，但假定 canonical 变量名、单位、规则纬经轴、充分覆盖与完整身份；
formal B 输出固定 hourly，风险归一化阈值保持不变。结构兼容不代表 GFS 与 CARRA 科学
分布已经等价，需由下一轮 B Winter validation 给出风险分布证据。

详见：

- [Winter / Summer Data Source Comparison](WINTER_SUMMER_DATA_SOURCE_COMPARISON.md)
- [Data Source Transition Audit](DATA_SOURCE_TRANSITION_AUDIT.md)

## 4. Temporal Coverage Audit（2026-08-22 21:56 +08:00）

冻结场景的正式窗口是 144 小时并在 21T00Z 结束，该窗口 12/12 complete。若按任务提出
的 21T12Z 检查，则覆盖不完整：CARRA 三变量缺 03/06/09/12；七个小时变量缺 01/02；
wave 完整到 12Z。

非 CARRA 尾部没有换供应商或产品族，但使用新 snapshot 和扩大后的请求 bbox。当前
bundle 在 00Z 截止，不包含尾部补采记录。详见
[Winter Temporal Coverage Audit](WINTER_TEMPORAL_COVERAGE_AUDIT.md)。

## 5. B Entry Point（2026-08-22 21:56 +08:00）

```text
B_ENTRYPOINT:
path: work_package_b/src/arctic_route_risk/service.py
class/method: RiskBuildService.build_window
formal command: arctic-route-orchestrator run
orchestrator path: arctic_route_orchestrator/src/arctic_route_orchestrator/cli.py
input: DatasetBundle.v2 + PreparedWindow + matching RunContext.v2
output: hourly bc.risk-frame.v2 committed window
version: bc.risk-frame.v2
```

正式运行必须显式提供 `--b-config`。library 默认 grid 为 baseline 16×7；既有 Tromsø
medium 配置为 31×11，但尚未批准为 Winter production profile。本轮未运行 B。

## 6. C Entry Point（2026-08-22 21:56 +08:00）

```text
C_ENTRYPOINT:
path: work_package_c/src/arctic_route_planning/ingress.py
class: RiskSourcePlanningIngress
methods: prepare / execute / execute_four_layer
formal command: arctic-route-orchestrator run
input: atomically committed hourly bc.risk-frame.v2 window
output: cd.route-plan.v2 or cd.four-layer-route-plan-set.v3
algorithm: TimeDependentAStar
grid profile: inherited exactly from B RiskFrame; no independent C profile
```

C 默认 planner 使用 60 分钟 time bucket、8-connectivity、3 edge samples、216 小时
搜索上限和 180 分钟最大 risk-frame gap。它不选择 baseline/medium/fine；该选择属于 B
target-grid 配置。本轮未运行 C。

## 7. Git Status（2026-08-22 21:56 +08:00）

审计开始时所有仓库均位于 `research-validation-system`。用户遗忘的修改已按仓库分开
保存为本地提交：

- Work Package A：`39e9076 wip: preserve winter A acquisition and frozen bundle`
- Governance：`696b1f0 docs: preserve winter acquisition closure evidence`

Contracts `c19e910`、Orchestrator `89e61e3`、B `a6dfa6c`、C `beae73a`、D `ec95f8c`
均未修改。`/root/my_project` 当前没有 root Git。A 的 `data/carra/` 是 376 MB 原始缓存，
保持 untracked，未提交；`.cdsapirc` 与 `.env.copernicus` 凭据未提交。最终状态以本报告
提交后的 `git status` 为准。`PUSH = NOT PERFORMED`。

## 8. Risks（2026-08-22 21:56 +08:00）

| Risk | Severity | Consequence |
|---|---|---|
| matching Winter RunContext/execution spec 缺失 | HIGH | B formal intake 不能开始 |
| current canonical docs 仍写 9/12 | HIGH | 人员可能错误判断 Winter 被阻塞 |
| 00Z 与 12Z 窗口混用 | HIGH | coverage 与实验时长被误报 |
| CARRA/GFS 科学可比性未验证 | MEDIUM | 风险分布差异不能仅归因于季节 |
| standalone bundle generation log 缺失 | MEDIUM | 生成动作复现链弱于 artifact 自证链 |
| tail 小时数据缺 01Z/02Z | MEDIUM | 156 小时扩展无法通过完整 coverage |
| `.cdsapirc` 当前权限为 0644 | HIGH / SECURITY | 本机其他用户可能读取凭据；需单独授权修复 |
| 新 A 文件 Ruff 当前 47 项 | MEDIUM | 既有“ruff clean”文档陈述不真实 |

## 9. Recommended Next Step（2026-08-22 21:56 +08:00）

1. 先同步 canonical `CURRENT_STATUS` 与 `WINTER_SCENARIO_STATUS`，统一 144 小时窗口和
   `FROZEN_ARTIFACT_READY`，保留历史报告为历史检查点。
2. 为 bundle ID/digest 创建 matching `RunContext.v2` 与 Winter execution spec，并运行
   Orchestrator intake-only 校验。
3. 明确批准 Winter B config；建议评估既有 Tromsø medium 配置以便比较，但不得默认采用。
4. intake 通过后才运行 focused B Winter validation，输出 risk distribution 与 hard reason
   证据；随后依次进入 C、D。
5. 若研究目标必须到 21T12Z，新建 scenario revision，补气象四帧与小时两帧，再生成新的
   immutable bundle；不要修改当前冻结 bundle。
6. 在获得用户明确授权后，将 `.cdsapirc` 权限收紧到 0600，并单独修复/验证 A Ruff；这些
   操作不属于本轮只读审计。

## 10. Verification Boundary（2026-08-22 21:56 +08:00）

本轮执行了 A bundle parse/digest、A doctor 与 focused CARRA unit/syntax 检查；没有运行
B、C、D、48h replay、heavy integration 或 determinism twin-run。A focused CARRA tests
为 12 passed（3 个 timezone warning）；新 A 文件 Ruff 并非 clean，当前发现 47 项。
