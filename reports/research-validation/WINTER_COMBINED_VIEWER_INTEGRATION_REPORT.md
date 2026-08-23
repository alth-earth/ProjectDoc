---
Overall Status: ACTIVE
Content Status:
  - COMPLETED
  - EXPERIMENTAL
Document Role: SUPPORTING
Scope: Winter combined presentation assembly 与 D Firefox E2E
Canonical For: 本轮实现、验证证据、限制与交接
Branch: research-validation-system
Last Verified: 2026-08-23
Related Canonical Docs:
  - ../../current/CURRENT_STATUS.md
  - ../../current/CURRENT_ROADMAP.md
  - ../../current/reference/WINTER_SCENARIO_STATUS.md
---

# Winter Combined Viewer Integration Report

## 1. Executive Summary（2026-08-23 20:14 +08:00）

本轮把同一 Winter experiment identity 下已冻结/已验证的 A、B、C artifacts 组装为一个
D 可消费的 combined presentation package，并完成 Firefox Browser E2E。最终 verdict：

```text
WINTER_COMBINED_PRESENTATION = REAL_E2E_PASS
WINTER_RESEARCH_BROWSER_E2E = REAL_E2E_PASS
WINTER_CAUSAL_REPLAY = NOT_IMPLEMENTED
```

combined package 包含 145 个 hourly RiskFrame、31×11 risk/hard grid、四层 × 三目标的
12 条真实 C candidates、full-voyage recommended route，以及由该路线 waypoint ETA
投影出的 3,206 个 1-minute navigation simulation samples。不存在当前 blocker，但没有
Winter causal replay snapshots，因此不得把本轮 ETA-driven simulation 写成 replay 或
dynamic-replanning evidence。

**Key Delta Table**

| Metric / Claim | Before | After | Delta | Verdict |
|---|---|---|---|---|
| 当前 Viewer identity | Summer August 2026 | Winter February 2026 | scenario/run/bundle/risk-window 全绑定 | IMPROVED |
| Winter combined package | NOT_IMPLEMENTED | 7.9 MiB package / 145 frames / 12 routes | 新增 | PASS |
| Winter Research Browser | NOT_RUN | Firefox REAL_E2E_PASS | page/map/risk/hard/routes/simulation | PASS |
| Browser console/network | NOT_VERIFIED_FOR_WINTER | 0 errors / 0 warnings / 7 required HTTP 200 | 新增证据 | PASS |
| 航行 timeline | MISSING | C waypoint ETA projection / 3,206 samples | 非 replay | EXPERIMENTAL |
| Summer frozen fallback | BROWSER_E2E_PASS | 兼容路径与测试保留 | 无语义变化 | PRESERVED |

**Claim Matrix**

| Claim | Status | Validation Level | Evidence | Notes / Limitation |
|---|---|---|---|---|
| Winter artifact identity 单一且一致 | PASS | REAL_E2E_PASS | preflight + D identity guard + Firefox | 不允许 Summer/Winter 混装 |
| Winter risk/hard layer 可见 | PASS | REAL_E2E_PASS | Firefox screenshot；145 formal frames | `DATA_UNAVAILABLE` 独立于 risk color |
| 12 条候选路线来自 C | PASS | REAL_E2E_PASS | candidate set + 12/12 integrity + layer selector | D 不排序、不重算 |
| 船按 C ETA 持续移动 | PASS | REAL_E2E_PASS | Run 后 0.0 km → 1.3 km | 不是 causal replay |
| Winter dynamic replanning | NOT IMPLEMENTED | NOT_IMPLEMENTED | 无 Winter snapshots/events | 本轮不伪造 |
| A/B/C frozen semantics | PRESERVED | AUTHORITATIVE_PASS（继承） | source artifact SHA/identity unchanged | 本轮未重跑 A/B/C |

## 2. Scope / Non-Scope（2026-08-23 20:14 +08:00）

本轮修改 Orchestrator presentation assembly、D artifact identity consumption、相关测试与
current documentation。未修改 A pipeline、B risk model、C planner、shared contracts、
任何 frozen artifact；未生成 RiskFrame、RoutePlan 或 causal Replay；未运行 B/C、full
integration 或 heavy replay。

## 3. Starting Baseline（2026-08-23 20:14 +08:00）

| Item | Baseline |
|---|---|
| Orchestrator start HEAD | `6888830cc613c4c26019b647b5073ca494d48086` |
| D start HEAD | `e5488f4d832ddc1b85cb40f035f77697bd53088d` |
| Governance start HEAD | `b0a10bc1fe588b2eefdb5e82c2c831048fef0ce2` |
| Current D bundle | Summer `tromso_isfjorden_august_2026_demo_v1` |
| Winter B | 145 formal `bc.risk-frame.v2` / 31×11 / committed RiskWindow |
| Winter C | `cd.four-layer-route-plan-set.v3` / 4×3=12 / integrity 12/12 PASS |
| Known limitation | 无 Winter causal replay manifest/snapshots/timeline |

## 4. Git Final State（2026-08-23 20:14 +08:00）

| Repo | Branch | Start HEAD | End HEAD | Origin tracking | Ahead / Behind | Working tree | Commits | Push |
|---|---|---|---|---|---|---|---|---|
| root | N/A | no root Git | no root Git | N/A | N/A | N/A | 0 | NOT PERFORMED |
| governance | `research-validation-system` | `b0a10bc1` | 本报告提交后见最终回执 | `origin/research-validation-system` | 提交前 0/0 | report commit 前 dirty | 1 planned | NOT PERFORMED |
| contracts | `research-validation-system` | `c19e910f` | `c19e910f` | origin | 0/0 | clean | 0 | NOT PERFORMED |
| orchestrator | `research-validation-system` | `6888830c` | `9d29ad5` | origin | 1/0 | clean | 1 | NOT PERFORMED |
| A | `research-validation-system` | `b40c689f` | `b40c689f` | origin | 0/0 | clean | 0 | NOT PERFORMED |
| B | `research-validation-system` | `2d034bf5` | `2d034bf5` | origin | 0/0 | clean | 0 | NOT PERFORMED |
| C | `research-validation-system` | `8d906950` | `8d906950` | origin | 0/0 | clean | 0 | NOT PERFORMED |
| D | `research-validation-system` | `e5488f4d` | `69e8485` | origin | 1/0 | clean | 1 | NOT PERFORMED |

## 5. Filesystem & Resource Safety（2026-08-23 20:14 +08:00）

| Observation | Result |
|---|---|
| Writes outside `/root/my_project/**` | 0 |
| `free -h` before | 7.4 GiB total / 5.8 GiB available / 34 MiB swap used |
| Lowest `MemAvailable` | 未连续采样；结束时 5.4 GiB available |
| Swap before / peak / after | 34 MiB / 未连续采样 / 34 MiB |
| Assembly peak RSS | 163,484 KiB（约 159.7 MiB） |
| OOM | 0 |
| Heavy-task overlap | N/A；未运行 heavy task |

Browser session metadata 已从 D working tree 移入 `.runtime/browser-session-artifacts/`；截图、
package 与 test logs 均保存于 `.runtime/`，未提交 Git。Windows 宿主物理剩余空间未核验，
状态保持 `UNKNOWN`。

## 6. Code / Architecture Changes（2026-08-23 20:14 +08:00）

| Component | Old behavior | New behavior | Reason |
|---|---|---|---|
| `replay_viewer_export.py` | 只从 causal replay manifest/snapshots 组装 | 新增独立 Winter combined assembly 路径 | 不混用 Summer replay，复用冻结 Winter artifacts |
| Orchestrator identity gate | candidate 只检查 replay scenario | 同时绑定 dataset/run/risk-window/plan/candidate/integrity | 防止跨实验拼装 |
| Navigation timeline | Winter 缺失 | 从 C selected full-voyage waypoint ETA 投影 1-minute states | 支持研究航行仿真且不伪造 pixel speed |
| D `app.js` | Research View 只校验 candidate package | combined identity 跨 risk/research/candidate fail closed | 页面与 artifact identity 一致 |
| D metadata panel | run/scenario/risk schema 为主 | 增加 scenario ID、RunContext、DatasetBundle、RiskWindow、assembly | 让研究证据链可见 |

Orchestrator 仍只拥有 projection/preflight/export；D 仍是唯一 HTML/CSS/JS Viewer runtime
owner。A/B/C 不被浏览器导入或调用。

## 7. Semantic / Contract Changes（2026-08-23 20:14 +08:00）

未修改 shared contract version，也未改变 risk、route、ETA 或 selection semantics。
`replay.viewer-bundle.v1` 维持既有 D input shape，并通过可选
`combined_presentation`/`research_validation` metadata 向后兼容扩展。

```text
DATA_UNAVAILABLE != SAFE
route candidate highlight != route reranking
ETA projection != causal replay
ship position = C waypoint ETA + Simulation Clock
pixel speed = NO
```

Legacy bundle 不包含 combined metadata 时仍进入原有路径；combined bundle 任一 identity
不一致则 fail closed。

## 8. Experiments / Alternatives（2026-08-23 20:14 +08:00）

| Alternative | Result | Decision |
|---|---|---|
| Summer replay + Winter risk/candidates | identity 与时间窗不一致 | REJECTED |
| 人工伪造 Winter replay/events | 无 source snapshots | REJECTED |
| 只显示静态候选，不提供仿真 | 可行但不能覆盖任务 Simulation 要求 | 未采用 |
| C waypoint ETA presentation projection | geometry/speed/time 均来自 C artifact | ADOPTED / EXPERIMENTAL |

## 9. Authoritative Run / Real Validation（2026-08-23 20:14 +08:00）

未运行 authoritative replay、B RiskBuild 或 C planner（`NOT RUN`，用户明确禁止重新生成）。
本轮运行的 real-artifact presentation assembly：

```text
scenario = tromso_isfjorden_february_2026_research_v1
run = run-441b03c8-d45b-5414-b0e8-b7fd0d990c22
RiskWindow = risk-window-sha256-b5bed6bb...
risk frames = 145
route candidates = 12
timeline samples = 3206
preflight = PASS
L2 route integrity = 12/12 PASS
```

Firefox Browser E2E 使用 `playwright-cli` + Firefox，访问
`http://127.0.0.1:8131/index.html`。页面、GEBCO、risk、hard layer、routes、ship 均可见；
`Run` 后进度从 0.0 km 增至 1.3 km，`Pause` 生效；切到 `executable_0_6h` 显示 3 条真实
candidates；console errors/warnings 均为 0，7 个 required resources 均 HTTP 200。

## 10. Performance Breakdown（2026-08-23 20:14 +08:00）

| Metric | Before | After | Delta / Verdict |
|---|---|---|---|
| Winter assembly | N/A | 1.51 s wall | 新路径；工程观察 |
| Assembly peak RSS | N/A | 163,484 KiB | 无内存压力 |
| Bundle size | Summer bundle 未用于可比基准 | 7.9 MiB | 145 frames + 3,206 states；NOT BENCHMARKED |
| Browser required requests | Summer baseline 7 resources | Winter 7 resources / all 200 | 无新增网络依赖 |
| Run/Pause responsiveness | Summer PASS | Winter visually immediate | 无可见冻结；工程观察 |

未进行专业浏览器 benchmark；Firefox CLI 总时长包含浏览器启动，不能作为 initial-load
benchmark。bundle 增大主要来自完整 145-frame risk window 与 minute timeline，后续若优化
应先做 compact/lazy presentation，不得把计算移入 D。

## 11. Correctness / Validation（2026-08-23 20:14 +08:00）

| Validation | Result | Level |
|---|---|---|
| Orchestrator focused export/projection | 15 passed | UNIT_PASS |
| Orchestrator fast suite | 93 passed / 2 deselected / 1 nonfatal warning | UNIT_PASS |
| Orchestrator Ruff / `py_compile` | PASS | UNIT_PASS |
| D full pytest | 77 passed / 3 causal-replay-only skipped | UNIT_PASS |
| D Ruff / `node --check viewer/app.js` | PASS | UNIT_PASS |
| Manifest/preflight/identity/digest | PASS | REAL_E2E_PASS |
| Route integrity / L2 | 12/12 PASS | AUTHORITATIVE_PASS（继承 artifact evidence） |
| Firefox page/risk/hard/route/ship/controls | PASS | REAL_E2E_PASS |
| Browser console/network | 0 errors / 0 warnings / all required HTTP 200 | REAL_E2E_PASS |

Orchestrator fast suite 的唯一 warning 是 xarray 探测 `cfgrib` 时本机无 ecCodes library；
本轮 GEBCO basemap 仍成功输出，warning 未导致请求、schema 或 rendering failure。

## 12. Determinism / Reproducibility（2026-08-23 20:14 +08:00）

Winter causal replay/twin-run determinism：`NOT RUN`。本轮 assembly 使用 immutable source
SHA 与 canonical JSON digest，manifest 固定记录全部 source identities。输出 bundle SHA 为
`ec8653b65ff0c5de6bb498c80ce25570f310c5ea9e650986bf6443e67b6e10fd`，但未执行独立
twin-run，因此不得升级为 authoritative determinism claim。

## 13. Artifacts / Provenance（2026-08-23 20:14 +08:00）

| Artifact | Identity / SHA | Tracking | Provenance |
|---|---|---|---|
| Winter combined manifest | `winter-viewer-sha256-2fa396f...` | `.runtime`, ignored | exact source SHA map |
| Viewer `bundle.json` | SHA `ec8653b65...` | `.runtime`, ignored | combined presentation assembly |
| GEBCO basemap | SHA `924e8eea...` | `.runtime`, ignored | A cached GEBCO source |
| DatasetBundle | `a-bundle-a2146dd0adbaa7db77a6beb7` | frozen source, unchanged | A formal |
| RiskWindow | `risk-window-sha256-b5bed6bb...` | runtime experiment, unchanged | B formal / experimental model |
| Candidate set | `route-candidates-sha256-46baf020...` | runtime experiment, unchanged | C formal route projection |
| Firefox proof | `firefox-winter-e2e-final.png` | `.runtime`, ignored | real browser screenshot |

完整 package 位于：
`/root/my_project/.runtime/viewer-proof/winter-combined/package/`。

## 14. Known Limitations / Technical Debt（2026-08-23 20:14 +08:00）

| TD-ID | Impact | Severity | Next action |
|---|---|---|---|
| TD-WCV-01 | 无 Winter replan events，不能展示 dynamic adoption | Medium | 未来发布正式 Winter causal replay/snapshots |
| TD-WCV-02 | 7.9 MiB bundle 一次加载完整 145 frames | Low | 先量测，再考虑 compact/lazy presentation |
| TD-WCV-03 | xarray 环境缺 ecCodes，产生非致命 plugin warning | Low | 仅在需要 GRIB runtime 时配置，不为 Viewer 引入依赖 |
| TD-WCV-04 | package 为 runtime artifact，尚未进入 frozen lifecycle | Medium | 审阅后决定 freeze/registry，不自动提交二进制 |

**Unexpected Findings / Corrections**

- 旧假设：Winter combined Viewer 的主要缺口只是把现有 replay exporter 指向 Winter。
- 新证据：没有同 identity 的 Winter replay manifest/snapshots；Summer replay 不能复用。
- 修正：本轮发布明确的 ETA-driven `research_navigation_simulation`，并设置
  `source_replay=null`；不声明 Winter replay/replanning PASS。
- 另发现 `uv run` 曾机械刷新无关 `uv.lock`；已恢复到 starting HEAD 内容，未提交。

## 15. Decision / Next Phase（2026-08-23 20:14 +08:00）

项目状态从 `Winter combined Viewer = NOT_IMPLEMENTED` 推进到
`WINTER_RESEARCH_BROWSER_E2E = REAL_E2E_PASS`。本轮可接受为 Winter Research
Visualization 的 first combined baseline，但尚不是 frozen artifact，也不包含 dynamic
replanning。

下一阶段建议：先由人工审阅 identity、截图和 7.9 MiB package；如研究目标要求航中风险
变化驱动的重规划，再单独建立 Winter causal replay，而不是在 D 添加事件。明确不要做：
修改 B risk formula、C planner、shared contracts、冻结 artifacts，或把 ETA projection
升级成 replay claim。
