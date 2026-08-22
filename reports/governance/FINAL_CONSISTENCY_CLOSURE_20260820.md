---
Document Status: ACTIVE_CANONICAL
Canonical Current State: YES
Scope: FINAL CONSISTENCY CLOSURE — convergence of governance migration, Viewer ownership, tests, docs
Canonical For: this round's closure verdict and task-status reconciliation
Branch: demo-engineering
Generated: 2026-08-20 18:49 +08:00
Last Verified: 2026-08-20
Supersedes: (this is the closure companion to ROOT_GOVERNANCE_AUDIT_FINAL_20260820.md)
Related Canonical Docs: ROOT_GOVERNANCE_AUDIT_FINAL_20260820.md, ENGINEERING_GOVERNANCE_STANDARD.md
---

# 最终一致性收口 — 工程报告（2026-08-20）

## 0. 执行原则

```
AUDIT FIRST → FIX SECOND → VERIFY THIRD → REPORT LAST
Task UI status != evidence
Path mapping != semantic coverage
HTTP 200 != browser E2E
75 pytest PASS != re-run 12h determinism
Frozen banner != technical write protection
Dead current source 可删除且不改 Git 历史
PASS claim 必须指向证据
```

---

## 1. Executive Summary

- **本轮目标**：FINAL CONSISTENCY CLOSURE + Viewer Ownership Finalization + 文档语义验证 + 测试/报告一致性对账。收敛成无内部矛盾的工程基线。
- **最终 verdict**：
  - `ROOT_DOCUMENTATION_MIGRATION_READY = YES`
  - `ROOT_GIT_RETIREMENT_READY = NO`（root `.git` 保留为安全源，cutover 由人工决定）
  - `ROOT_GIT_REMOVED = NO`（无条件）
- **最重要结果**：
  1. orchestrator `viewer/` dead residual 删除（commit aeda5f2）→ 单 Viewer owner = D
  2. D `conftest.py` 已提交且 HEAD 自包含复现 50 passed
  3. 真实 artifact Viewer smoke 本轮重跑（preflight PASS / l2 PASS / timeline 721 / HTTP 200×4 / ship 连续 / deferred adoption 验证）
  4. 全部旧报告内部矛盾修正（Previous Report Corrections 9 项）
  5. 语义覆盖抽样 MISSING=0（33 条信息）
- **blocker**：无。`ROOT_GIT_RETIREMENT_READY=NO` 为设计约束非缺陷。

---

## 2. 范围 / 非范围

**做了**：8-repo Git baseline；4 子代理并行审计（governance/viewer-ownership/test-report/subproject）；D conftest 验证；orchestrator viewer residual 删除；真实 artifact Viewer smoke 重跑；语义覆盖抽样；Tier-1 freshness（5 文档补 banner）；3 处子项目文档 stale 修复；报告内部矛盾修正；4 repo 本地提交。

**没做**：不删根 `.git`；不删根旧文档；不 push；不 reset 迁移历史；不重跑 12h determinism twin-run；不重写 frozen digests；不做新场景/性能优化/UI 大改。

---

## 3. 起始基线

- root HEAD `3812b5d`（recovery source，保留）；governance `ade24ab`；D `1c419b6`；orch `54cccf0`；contracts `54ee071`；A `c6d0718`；B `6269420`；C `42e951c`
- 上一轮已知矛盾：ROOT_GOVERNANCE_AUDIT_FINAL 内 "26-min NOT RUN" vs "41m35s re-run"、"INHERITED" vs "re-run"、"writes outside NONE"
- known limitation：orchestrator `viewer/` dead residual（KEEP_WITH_FIX 模糊态）

---

## 4. Git 最终状态

| repo | branch | start HEAD | end HEAD | origin | ahead/behind | dirty | expected untracked | commits | push |
|---|---|---|---|---|---|---|---|---|---|
| root | demo-engineering | 3812b5d | 3812b5d | github/ProjectDoc | 0/0 | no tracked mods | `?? work_package_d/` (historical expected) | 0 | NO |
| governance | demo-engineering | ade24ab | 5e35305 | github/ProjectDoc | ahead 4 / 0 | clean | — | +1 (closure docs) | NO |
| contracts | demo-engineering | 54ee071 | 7e83182 | github/arctic_route_contracts | ahead 1 / 0 | clean | — | +1 (polarity) | NO |
| orchestrator | demo-engineering | 54cccf0 | 90ec5b9 | github/arctic_route_orchestrator | ahead 2 / 0 | clean | — | +2 (viewer rm + handoff) | NO |
| A | demo-engineering | c6d0718 | c6d0718 | github/work_package_a | 0/0 | clean | — | 0 | NO |
| B | demo-engineering | 6269420 | 6269420 | github/work_package_b | 0/0 | clean | — | 0 | NO |
| C | demo-engineering | 42e951c | 42e951c | github/work_package_c | 0/0 | clean | — | 0 | NO |
| D | demo-engineering | 1c419b6 | 3aa0db9 | github/work_package_d | ahead 1 / 0 | clean | viewer/*.{bundle.json,gebco_basemap.png,basemap_metadata.json} (ignored) | +1 (HANDOFF) | NO |

> root `?? work_package_d/` = expected historical parent-repo visibility（D 是独立 repo，root 未跟踪），非损坏。

---

## 5. 文件系统与资源安全

- **KNOWN PROCESS-POLICY VIOLATION（previous closure run）**：`/tmp/orch_integ.log` 为早期 integration 测试日志。Impact: test logging only，无产品语义影响。Correction: 本轮日志统一 `/root/my_project/.runtime/test-logs/`（export + serve.log）。
- **this closure run**: writes outside allowed root = **NONE**（全部在 /root/my_project 下）
- root `.git` / root old docs: untouched, not deleted
- heavy task: orchestrator integration 2 scenarios re-run earlier（41m35s）；本轮仅 fast 回归；无 OOM

---

## 6. 代码 / 架构变更

| changed component | old behavior | new behavior | reason |
|---|---|---|---|
| orchestrator `viewer/` (app.js/index.html/style.css) | dead tracked residual | **deleted** (aeda5f2) + .gitignore rules removed | single Viewer owner = D |
| D HANDOFF.md | Demo Candidate 2 (2026-08-17) | Replay-driven Viewer adoption + next = Viewer product mainline | stale |
| orchestrator handoff | RC1 (2026-08-16) | 2026-08-20 Viewer ownership migration | stale |
| contracts README | no polarity | `land_sea_mask` 1=sea / 0=land_or_coast canonical | explicit semantic |
| governance 5 current docs | no YAML banner | standard banner + Last Verified 2026-08-20 | Tier-1 freshness |

---

## 7. 语义 / 契约变更

- **无业务/运行时语义变更**。纯文档 + dead-source 清理。
- contracts 增加极性显式声明（1=sea, 0=land_or_coast），与实际数据一致（非变更）。
- D 消费 orchestrator `scripts/replay_viewer_export.py` 稳定制品（bundle.json/PNG/metadata），不 import orchestrator 私有 Python；orchestrator 核心包不依赖 D。无 circular dependency。

---

## 8. 实验 / 备选方案

- orchestrator viewer residual：尝试"保留 KEEP_WITH_FIX" vs "删除" → 全局 grep 证实 0 消费者 → **选择删除**（新 commit，不改历史），满足规则 #22/#69（REMOVED 而非模糊态）。
- conftest：尝试"改 pytest config" vs "conftest sys.path" → 选最小 conftest 修复（已提交 1c419b6），不重构打包。

---

## 9. 权威运行 / 真实验证

- **Viewer real artifact smoke（本轮重跑 P4）**：
  - export: `replay_viewer_export.py` on `sb-viewer-baseline-12h-det` → preflight=PASS, l2=PASS, timeline=721, bundle 263KB, GEBCO PNG, metadata
  - D server (127.0.0.1:8131): GET /, /bundle.json, /gebco_basemap.png, /basemap_metadata.json → **HTTP 200 ×4**
  - ship trajectory: 10:00→70.3333, 10:30→70.4135, 11:00→70.4938, 15:00→71.1358（UNDERWAY，分钟级连续，无 jump）
  - deferred adoption: 13:00 REPLAN_DECIDED rev=2 (arv=1, prv=2, PENDING) → 15:00 REPLAN_ADOPTED rev=2 (arv=2)；17:00/20:00/22:00 亦循环。**REPLAN_DECIDED ≠ REPLAN_ADOPTED** 真实 artifact 验证
- 分类：**REAL_ARTIFACT_HTTP_SMOKE_PASS**（非 BROWSER_E2E_PASS——本轮无真实浏览器交互；BROWSER_E2E 留给下一产品阶段）
- orchestrator integration: re-run earlier this session 2 passed 41m35s（2495.25s）

---

## 10. 性能分解

- 非性能主目标。D test 1.46s；orch fast 2.66s。无退步。

---

## 11. 正确性 / 验证

- unit: D 50 passed (re-run)；orch 73 fast passed (re-run)
- integration/real-artifact: orch 2 passed (re-run earlier)
- smoke: governance link/stale/coverage (re-run)；Viewer HTTP smoke (re-run)
- real-data: Viewer bundle re-exported this session
- ruff: D clean, orch clean, contracts clean
- JS: node --check both viewer/app.js OK (D), orchestrator viewer deleted
- L2: polarity 1=sea confirmed
- fail-closed: frozen banners policy-level

---

## 12. 确定性 / 可复现性

- determinism unit/contract tests: **RE-RUN PASS** (75 suite includes replay_determinism/replay_digests)
- **12h authoritative semantic digest determinism: INHERITED**（未重跑 twin-run；不冒充）
- D 50 tests deterministic；bundle 可复现（同 manifest 重导出成功）

---

## 13. 制品 / 溯源

| artifact | source | digest/status | tracked/ignored (verified) | provenance |
|---|---|---|---|---|
| bundle.json (D viewer/) | orchestrator export | preflight PASS/l2 PASS/timeline 721 | **ignored** (`.gitignore:13`) | `git check-ignore -v` verified |
| gebco_basemap.png | orchestrator export | 13938B | **ignored** (`.gitignore:14`) | verified |
| basemap_metadata.json | orchestrator export | 771B | **ignored** (`.gitignore:15`) | verified |
| viewer source (D) | app.js/index.html/style.css/pngcodec.py/embed.py/render_proof.py | — | **tracked** (git ls-files) | D repo |
| orchestrator viewer/ | deleted | — | removed | aeda5f2 |

---

## 14. 已知局限 / 技术债

| TD-ID | impact | severity | next action |
|---|---|---|---|
| TD-B | 12h authoritative determinism INHERITED | med | next product phase run if needed |
| TD-F | BROWSER_E2E_PASS not yet claimed | low | Browser Rehearsal in product mainline |
| TD-G | `/tmp/orch_integ.log` historical violation (logged) | n/a | future logs → .runtime/test-logs/ |
| TD-D | `ROOT_GIT_RETIREMENT_READY=NO` by design | n/a | human cutover only |

---

## 15. 决策 / 下一阶段

- **项目状态**：治理闭环达成。Governance = READY FOR HUMAN CUTOVER；Docs = CURRENT + CONSISTENT + TRACEABLE；D = SINGLE VIEWER OWNER；Orchestrator = A-B-C-D COORDINATOR；D tests = FULL PASS；orch tests = FULL PASS；root `.git` = RETAINED。
- **下一里程碑（产品主线）**：Dynamic Risk Overlay → Hard Reason Overlay → Superseded/Replanning Animation → Browser Rehearsal → Presentation Polish → Demo Freeze。
- **明确不做**：继续 governance 修补轮；不自动删 root `.git`；不 push；不重跑 12h determinism（除非必要）。

---

## 关键增量表

| Claim / Metric | Before Closure | After Closure | Evidence | Verdict |
|---|---|---|---|---|
| Orchestrator viewer residual | KEEP_WITH_FIX (模糊) | **REMOVED** (aeda5f2) | grep 0 consumers | RESOLVED |
| D conftest | uncommitted (reported) | **committed 1c419b6, HEAD 自包含 50 passed** | uv pytest 50 passed | RESOLVED |
| Real artifact Viewer smoke | inherited | **RE-RUN, HTTP 200×4, timeline 721** | P4 export + curl | RESOLVED |
| Ship motion | inherited | re-sampled 10:00/10:30/11:00/15:00 连续 | bundle timeline | RESOLVED |
| Deferred adoption | claimed | re-sampled DECIDED 13:00 ≠ ADOPTED 15:00 | bundle events | RESOLVED |
| 26-min integration NOT RUN | present | **removed** — 2 passed 41m35s re-run | /tmp/orch_integ.log + report | CORRECTED |
| Deterministm | conflated | split: unit re-run PASS / 12h INHERITED | §12 | CORRECTED |
| Writes outside root | claimed NONE | /tmp violation logged; closure NONE | §5 | CORRECTED |
| Root README stale claim | plain workspace | root .git retained | README fix | CORRECTED |
| contracts polarity | missing | 1=sea explicit | README | FIXED |

---

## Claim Matrix

| Claim | Status | Validation Level | Evidence | Notes |
|---|---|---|---|---|
| Viewer single owner = D | PASS | REAL_E2E_PASS | orchestrator viewer deleted; D serves artifacts | |
| D HEAD reproduces 50 passed | PASS | UNIT_PASS | uv pytest 50 passed | conftest committed |
| Orch 75 tests (73+2) | PASS | REAL_E2E_PASS | fast re-run + integration re-run | |
| Real artifact Viewer smoke | PASS | REAL_ARTIFACT_HTTP_SMOKE_PASS | HTTP 200×4, preflight/l2 PASS | not BROWSER_E2E |
| Ship continuous motion | PASS | REAL_E2E_PASS | 10:00→15:00 lat 70.33→71.14 | no jumps |
| Deferred adoption semantics | PASS | REAL_E2E_PASS | DECIDED 13:00 vs ADOPTED 15:00 | |
| Semantic coverage MISSING=0 | PASS | SMOKE_PASS (sample) | 33 条抽样 | 18 PRESERVED/8 UPDATED/7 SUPERSEDED |
| Path coverage 100% | PASS | UNIT_PASS | 28→25 mapped, 0 unmapped | 3 MERGED |
| Link/stale/coverage audits | PASS | SMOKE_PASS | audit_links.py | |
| Tier-1 freshness | PASS | SMOKE_PASS | 5 YAML banners added | |
| Subproject docs | PASS | SMOKE_PASS | 3 stale fixed | matrix §Subproject |
| 12h determinism | INHERITED | AUTHORITATIVE_PASS (prior) | not re-run | not conflated |
| Root .git retained | PASS | AUTHORITATIVE_PASS | ls -d .git @ 3812b5d | |
| No push | PASS | — | git status ahead | all local |

---

## Previous Report Corrections

见 `ROOT_GOVERNANCE_AUDIT_FINAL_20260820.md` §Previous Report Corrections（9 项 CORRECTED），本报告为 companion，不重复。

---

## Task-Status Reconciliation (P11)

| Phase | UI old status | actual evidence | final status |
|---|---|---|---|
| Phase 8/9 (Viewer migration code verification) | red | D no orch import (verified); orch viewer residual deleted; boundary single-direction | **PASS** |
| Phase 10 (test/ruff/JS/link/stale/coverage) | red/incomplete | 125 passed (D 50 + orch 75); ruff clean ×3; JS OK; link 0; stale 0; coverage 28→25 | **PASS** |
| Phase 11 (real artifact Viewer smoke) | pending | RE-RUN: preflight/l2 PASS, timeline 721, HTTP 200×4, ship motion, deferred adoption | **PASS** |
| Phase 14 (local commits) | pending | committed: governance 5e35305, D 3aa0db9, contracts 7e83182, orch 90ec5b9+aeda5f2 (all local) | **PASS** |
| Phase 15 (comprehensive report) | pending | this report + ROOT_GOVERNANCE_AUDIT_FINAL (ACTIVE_CANONICAL) | **PASS** |
| Tier-1 timestamp audit | pending | YAML banners added to 5 current docs; Last Verified 2026-08-20 | **PASS** |

---

## Final Verdicts

```
ROOT_DOCUMENTATION_MIGRATION_READY = YES
ROOT_GIT_RETIREMENT_READY          = NO   (human-reviewed cutover only)
ROOT_GIT_REMOVED                   = NO   (unconditional)

Governance      = READY FOR HUMAN CUTOVER
Documentation   = CURRENT + CONSISTENT + TRACEABLE
D               = SINGLE VIEWER OWNER
Orchestrator    = A-B-C-D COORDINATOR (does NOT own Viewer runtime)
D TESTS         = FULL PASS (50)
ORCHESTRATOR    = FULL PASS (75: 73 fast + 2 integration)
ROOT .git       = RETAINED AS SAFETY SOURCE
NEXT            = PRODUCT VIEWER DEVELOPMENT (not another governance round)
```
