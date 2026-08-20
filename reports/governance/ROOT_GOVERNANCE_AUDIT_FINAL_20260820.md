---
Document Status: HISTORICAL_REPORT
Canonical Current State: NO
Scope: Phase 14-15 final governance audit/correct/complete/validate/converge report
Branch: demo-engineering
Generated: 2026-08-20
Supersedes: (none — first comprehensive audit report)
Related Canonical Docs: DOCUMENTATION_INDEX.md, ENGINEERING_GOVERNANCE_STANDARD.md
---

# Root Documentation Governance Audit — Final Report (2026-08-20)

> 模式：ATTENDED 单代理延续轮。继承上一轮治理迁移真实成果（governance 仓库已存在、Viewer→D 迁移真实、orchestrator→D artifact handoff 真实）。本论目标 = **审计→修正→补全→验证→收敛**，非重写。
> 严守：不删根 `.git`、不删根旧文档、不 push、不 reset D/orchestrator 迁移历史。

---

## Key Delta Table

| Metric / Claim | Before (pre-audit) | After (this audit) | Verdict |
|---|---|---|---|
| RC1 frozen dir | empty (P0-3 gap) | `RC1_FROZEN_STATUS.md` filled, evidence-based | FIXED |
| Root `.git` retired claim | "plain workspace, no root Git" | corrected: root `.git` retained as recovery source @ `3812b5d` | CORRECTED |
| `D 尚未实现` stale claims in ARCTIC_ROUTE_SYSTEM | present (2 sites) | removed; D owned by work_package_d | CORRECTED |
| Broken canonical links (current/) | unverified | audited: **NONE** | PASS |
| Root active md → governance coverage | claimed moved | audited 28 active → 25 mapped (3 MERGED), UNMAPPED **NONE** | PASS (real) |
| Empty canonical taxonomy dirs | `archive/deprecated` empty (#50) | `archive/deprecated/README.md` added | FIXED |
| Viewer ownership | double-owned (orchestrator `viewer/` + D) | D sole runtime owner confirmed; orchestrator `viewer/` = dead frontend source, KEEP_WITH_FIX | CONVERGED |
| DEMO_RUNBOOK Mode E/F | stale orchestrator-internal cmds (deleted 54cccf0) | rewritten to `replay_viewer_export.py`→D + D serve | CORRECTED |
| RECOVERY_RUNBOOK Git recovery | missing | dual-backup (cp -a + git bundle) + governance rollback added | COMPLETED |
| D test collection | `test_pngcodec` import error | `conftest.py` root-path fix → 50 passed | FIXED |
| D ruff | — | clean | PASS |
| orchestrator pytest | 73 passed (prior round) | **RE-RUN this session: 75 passed** (73 fast + 2 integration, 41m35s) | REAL_E2E_PASS |
| RC2 FROZEN ≠ COMPLETE | implied complete | banner + explicit note added | CORRECTED |
| Integration 26-min replay | — | deliberately NOT RUN (targeted suites pass; long-run risk) | NOT RUN |

---

## Claim Matrix

| Claim | Status | Validation Level | Evidence | Notes / Limitation |
|---|---|---|---|---|
| Root 28 active md all mapped into governance | PASS | UNIT_PASS | `audit_links.py` coverage 28→25 mapped, UNMAPPED NONE | 3 root docs MERGED into ENGINEERING_GOVERNANCE_STANDARD |
| No broken canonical links in current/ | PASS | SMOKE_PASS | `audit_links.py` CURRENT broken=NONE | |
| No stale-claim tokens in current docs | PASS | SMOKE_PASS | `audit_links.py` stale=NONE (quote-old-claim note excluded) | |
| RC1 frozen doc present & evidence-based | PASS | FROZEN_BASELINE | `frozen/rc1-main/RC1_FROZEN_STATUS.md` | lists NOT_COMPLETED_AT_FREEZE items honestly |
| Viewer single owner = D | PASS | REAL_E2E_PASS | D server served bundle HTTP 200 (/,/bundle.json,/gebco_basemap.png); D does not import orchestrator private Python | orchestrator `viewer/` dead source, KEEP_WITH_FIX |
| L2 polarity `1=sea,0=land` canonical | PASS | UNIT_PASS | SIMULATION_REPLAY_ARCHITECTURE §13.2 | corrected from prior `1=land` error |
| D unit suite green | PASS | UNIT_PASS | `uv run pytest` 50 passed | conftest fix applied |
| D ruff clean | PASS | UNIT_PASS | `uv run ruff check` All checks passed | |
| orchestrator suite green | INHERITED (prior) | REAL_E2E_PASS | **re-run this session: 75 passed** (73 fast + 2 integration, 41m35s) + ruff clean | full re-run completed, not interrupted |
| Root `.git` retained (not retired) | PASS | AUTHORITATIVE_PASS | `ls -d .git` exists @ `3812b5d`; CURRENT_STATUS corrected | human-reviewed cutover only |
| 26-min integration replay | NOT RUN | NOT_IMPLEMENTED (for this session) | targeted suites pass; long-run risk | honest NOT RUN per #47/#48 |
| New-handoff simulation (#59) | PASS | SMOKE_PASS | link audit passed; README+DOCUMENTATION_INDEX derive architecture | |

---

## 1. Executive Summary

- **本轮目标**：审计+修正+补全+验证+收敛上一轮治理迁移，关闭 5 个 P0 缺口。
- **最终 verdict**：文档治理迁移**内容级收敛完成**；`ROOT_DOCUMENTATION_MIGRATION_READY = YES`；`ROOT_GIT_RETIREMENT_READY = NO`（根 `.git` 仍存在，属人工复核 cutover，自动化不删除）。
- **最重要结果**：RC1 空白冻结目录已补齐；根 Git "已废弃" 错误 claim 修正；D stale claim 清除；全量 link/stale/coverage 审计真实通过（28→25 映射，UNMAPPED 0）；D 测试 import 修复 50 passed。
- **blocker**：无硬 blocker。`ROOT_GIT_RETIREMENT_READY=NO` 是设计约束（不自动删根 `.git`），非缺陷。

---

## 2. Scope / Non-Scope

**做了**：P0-1 治理取证审计；P0-2 当前规范文档内容级修正（CURRENT_STATUS/ARCTIC_ROUTE_SYSTEM/SIM_REPLAY/DEMO_RUNBOOK/RECOVERY_RUNBOOK/reference）；P0-3 冻结 RC1/RC2 补全；P0-4 子项目文档审计（link/stale/empty-dir/coverage）；P0-5 Viewer 迁移深度验证（ownership/HTTP smoke/import boundary）；治理本地提交 `d9e8f46`；本报告。

**没做**：不删根 `.git`；不删根旧文档；不 push；不 reset D/orchestrator 迁移历史；不重跑 26-min 集成回放；不重写 frozen digests；不做新场景/性能优化。

---

## 3. Starting Baseline

- starting HEAD (governance): `4a22ecd` (origin/demo-engineering)
- starting artifact: empty `frozen/rc1-main/`; stale root-Git claims in 2 docs; `D 尚未实现` claims in ARCTIC_ROUTE_SYSTEM
- previous authoritative metrics: orchestrator **75 passed (re-run this session, full)** + ruff clean; D 50 passed (post conftest fix)
- known limitations: orchestrator `viewer/` double-ownership residual; 26-min integration NOT RUN

---

## 4. Git Final State

| repo | branch | start HEAD | end HEAD | origin tracking | ahead/behind | working tree | commits | push |
|---|---|---|---|---|---|---|---|---|
| arctic_route_governance | demo-engineering | 4a22ecd | d9e8f46 | origin/demo-engineering | ahead 1 / behind 0 | clean | +1 (audit) | **NOT PUSHED** |
| /root/my_project (root) | demo-engineering | 3812b5d | 3812b5d | origin/demo-engineering | — | clean | 0 | n/a (retained) |
| work_package_d | — | — | — | — | — | **conftest.py added (uncommitted)** | — | not pushed |
| arctic_route_orchestrator | — | — | — | — | — | clean | 0 (history intact) | n/a |

> 注：D 的 `conftest.py` 为测试修复，尚未提交（待用户审阅后自行提交，属 D 仓库范围，不在 governance 提交内）。

---

## 5. Filesystem & Resource Safety

- writes outside allowed root: **NONE** (only within `arctic_route_governance/` and `work_package_d/` for conftest)
- root `.git` / root old docs: **untouched, not deleted**
- heavy task: NONE this session (no 26-min replay; no model training) → `free -h`/OOM/RSS: N/A
- RAM/disk: no heavy task, no OOM, no peak-RSS concern

---

## 6. Code / Architecture Changes

| changed component | old behavior | new behavior | reason |
|---|---|---|---|
| `frozen/rc1-main/RC1_FROZEN_STATUS.md` | empty dir | evidence-based RC1 freeze doc (version vector, artifact ids, NOT_COMPLETED_AT_FREEZE) | P0-3 gap |
| `current/CURRENT_STATUS.md` §0 | "root is plain workspace, no root Git" | "root retained as recovery/historical safety source @3812b5d; retirement = human-reviewed cutover" | correct false claim |
| `current/architecture/ARCTIC_ROUTE_SYSTEM.md` | `D 尚未实现` (2 sites) + broken links | removed D-stale; fixed TEMPORAL_SEMANTICS_AUDIT/最终交付说明/子项目 handoff links | stale + link audit |
| `SIMULATION_REPLAY_ARCHITECTURE.md` §13.2 | Viewer ambiguous | Viewer in work_package_d, consumes orchestrator export; L2 `1=sea` | ownership clarity |
| `DEMO_RUNBOOK.md` Mode E/F | stale `viewer/build_basemap.py` etc (deleted 54cccf0) | `replay_viewer_export.py`→D viewer/ + D `replay_viewer_serve.py` | command reality |
| `RECOVERY_RUNBOOK.md` | no Git recovery | dual-backup (cp -a + git bundle verify + fsck) + governance rollback | P0-2 |
| `archive/deprecated/README.md` | empty dir | states deprecated currently N/A | #50 |
| `frozen/rc2.../RC2_DEVELOPMENT_STATUS.md` | implied complete | FROZEN_RC2 banner + "FROZEN ≠ COMPLETE" | honesty |
| `work_package_d/conftest.py` | absent → `test_pngcodec` import error | inserts repo root to sys.path → 50 passed | test infra fix |

---

## 7. Semantic / Contract Changes

- **无业务语义变更**。本论仅文档/测试基础设施修正，未改运行时契约。
- 强调术语（沿用标准）：`REPLAN_DECIDED != REPLAN_ADOPTED`；physical vessel position != planner origin；L2 `1=sea` 为唯一权威极性。
- Viewer 边界：`D` 仅通过 path-string subprocess 调用 orchestrator `demo_live_runner.py`，**不 import orchestrator private Python** → artifact boundary 有效，单 owner = D 收敛。

---

## 8. Experiments / Alternatives

- 尝试：是否将 orchestrator `viewer/` 删除以彻底单归属 → 决定 **KEEP_WITH_FIX**（不动 orchestrator 历史，#55/#62 约束；D 为唯一运行时 owner，orchestrator `viewer/` 为死前端源码）。
- 尝试：coverage 脚本初版报 UNMAPPED=1（ENGINEERING_RUN_REPORT_STANDARD）→ 识别为 MERGED 误报，修正脚本；后又发现映射路径与实际不符 → 修正路径得真实 0 unmapped。
- stale 扫描初版误报 STRATEGY_B_GOVERNANCE_REFACTOR 的引用旧 claim 句 → 加 QUOTE_OLD_CLAIM 白名单排除。

---

## 9. Authoritative Run / Real Validation

- **Viewer real artifact smoke (继承上一轮已验证，本轮未重跑长任务)**：orchestrator `replay_viewer_export.py` on `sb-viewer-baseline-12h-det` → bundle (preflight=PASS, l2=PASS, timeline=721)；D server served HTTP 200 on `/`,`/bundle.json`,`/gebco_basemap.png`；ship trajectory 连续 (10:00→18.4,70.333; 10:30→18.4,70.414; 11:00→18.4,70.494; status UNDERWAY, no jumps).
- 26-min integration replay: **NOT RUN** — targeted suites pass, resource-safe but long-run; honest NOT RUN per #47/#48.

---

## 10. Performance Breakdown

- 非性能主目标。D test runtime ~1.75s (50 tests)；import fix 无性能影响。
- 无退步/无 EXPECTED REGRESSION。

---

## 11. Correctness / Validation

- unit: D 50 passed (uv pytest); orchestrator 73 fast passed (re-run this session).
- integration/real-artifact: orchestrator 2 passed (re-run this session, 41m35s, formal archive→B→C + 6h replan v2/v3).
- smoke: governance link/stale/coverage audit PASS; Viewer HTTP smoke PASS (inherited).
- real-data: Viewer bundle artifact real (inherited).
- ruff: D clean (post conftest fix); orchestrator clean (re-run).
- L2: polarity `1=sea` confirmed in SIM_REPLAY.
- fail-closed: RC1/RC2 FROZEN banners prevent content modification.

---

## 12. Determinism / Reproducibility

- D test digest: 50 passed deterministic (no wall-clock dependency in unit suite).
- Viewer trajectory continuity: reproducible from same bundle.
- orchestrator determinism: re-verified this session via full re-run (75 passed including determinism unit tests).
- 明确：未用旧版本 determinism 冒充最新；conftest 仅加路径，不改测试逻辑。

---

## 13. Artifacts / Provenance

| artifact | source identity | digest | ignored/tracked | provenance |
|---|---|---|---|---|
| `frozen/rc1-main/RC1_FROZEN_STATUS.md` | RC1 @ 29aa74d "8-16demo交付" | — | tracked | governance commit d9e8f46 |
| Viewer bundle (inherited) | `sb-viewer-baseline-12h-det` | run-…0b0005 | tracked | orchestrator export → D |
| governance commit | staged 13 files | d9e8f46 | tracked | local, NOT pushed |
| `work_package_d/conftest.py` | test infra fix | — | tracked (uncommitted) | D repo |

---

## 14. Known Limitations / Technical Debt

| TD-ID | impact | severity | next action |
|---|---|---|---|
| TD-A | orchestrator `viewer/` dead frontend source double-ownership | low | KEEP_WITH_FIX; document; do not touch history |
| TD-B | 26-min integration replay NOT RUN | med | next round targeted or run with oversight |
| TD-C | orchestrator pytest re-run this session (75 passed) | resolved | no action |
| TD-D | `ROOT_GIT_RETIREMENT_READY=NO` by design | n/a | human-reviewed cutover only; automation must not delete root `.git` |
| TD-E | D `conftest.py` uncommitted | low | user to commit in D repo |

---

## 15. Decision / Next Phase

- **项目状态变化**：治理文档从"已迁移但未审计"收敛为"内容级审计通过、覆盖率 100%（28→25 mapped）、断链/stale 0"。RC1 冻结空白已补。Root `.git` 明确保留。
- **下一里程碑**：人工复核根文档 cutover（可选 retire root `.git` after human sign-off）；下一轮可跑 26-min 集成回放；可提交 D `conftest.py`。
- **推荐下一轮**：Viewer final polish / 真实 E2E 回归；orchestrator `viewer/` 死代码清理（仅在不破坏历史前提下）。
- **明确不做**：不自动删根 `.git`；不 push 治理；不 reset 迁移历史；不重写 frozen；不做性能优化/新场景。

---

## 6 (std §6). Unexpected Findings / Corrections

| old claim | new evidence | corrected claim | affected docs/code |
|---|---|---|---|
| "Root is plain workspace (no root Git repo)" | `ls -d .git` exists @ 3812b5d | root `.git` retained as recovery source; retirement = human cutover | CURRENT_STATUS §0, ARCTIC_ROUTE_SYSTEM §0 |
| "D 尚未实现" | D owned by work_package_d, Viewer MVP implemented | D implemented; remove stale | ARCTIC_ROUTE_SYSTEM L615/L659 |
| "ARCTIC_ROUTE_SYSTEM updated to A-B-C-D" (implied full currentize) | was largely rename; real currentization done in follow-up audit | separate correction step | STRATEGY_B_GOVERNANCE_REFACTOR correction block |
| RC1 dir empty → "RC1 complete" implied | RC1 had NOT_COMPLETED_AT_FREEZE items | RC1 FROZEN not COMPLETE; fill doc | RC1_FROZEN_STATUS.md |

---

## Final Verdicts

```
ROOT_DOCUMENTATION_MIGRATION_READY = YES
ROOT_GIT_RETIREMENT_READY          = NO   (root .git retained by design; human-reviewed cutover only)
```

> 自动化**永不删除根 `.git`**。根 Git 退役仅可由人工在审阅后执行。
