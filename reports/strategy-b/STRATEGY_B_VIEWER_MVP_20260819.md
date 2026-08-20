# Strategy B Replay-driven Viewer MVP（2026-08-19）

状态：本轮随报告完成（本地 commit，未 push）
形式：按 [Engineering Run Report Standard](ENGINEERING_RUN_REPORT_STANDARD.md)
的固定区块整理（完整最终报告见对话末尾）。

## 1. Executive Summary

```text
目标  : GEBCO L2 Demo Preflight + Replay-driven Viewer MVP
verdict: PASS（代码/数据/测试/报告）；浏览器自动化受限于本沙箱
最重要 : L2 语义极性发现并修正；L2 正式并入 preflight 且真实 route PASS；
        Replay-driven Viewer（basemap/timeline/route/track/ship/pending）
        建立并有数据渲染 proof 与 bundle 单测
blocker: 无业务 blocker；sandbox 无法起 socket/browser daemon
```

## 2. Key Delta Table

```text
Metric / Claim                 Before        After                    Verdict
-----------------------------------------------------------------------------------
L2 GEBCO polarity interpretation WRONG(1=land) CORRECT(1=sea,0=land)   CORRECTED
L2 gate                        harness only   demo preflight PASS     IMPROVED
Real Scenario B L2             NOT RUN       PASS（5 rev + tracks）   IMPROVED
Presentation preflight          N/A           PASS / eligible         ESTABLISHED
Replay-driven Viewer            NONE          MVP（server+single-file+proof） IMPROVED
Ship 10:30 intermediate         API 可查       bundle 内置 + proof PNG PASS
Pending-plan gate optimization  NOT DONE      NOT DONE（TD-45）       N/A
```

## 3. Scope / Non-Scope

做了什么：Report Standard；L2 raster traversal + 极性修正 + preflight CLI；
viewer base/bundle/embed/server；bundle 契约单测；本地数据 proof PNG。

没做：不重跑 12h/24h/determinism；不做 Pending-Plan Gate；不做 Dynamic Risk
overlay；不做 hull/UI polish；不并 6/8/16 workers；不动 Strategy A。

## 4. Starting Baseline

```text
root HEAD            = daad9d9（ahead 0）
orchestrator HEAD    = 092151f（ahead 0）
artifact             = sb-viewer-baseline-12h-det（13 snapshots）
previous metrics     = 12h 2044.9s determinism PASS
known limitation     = L2 仅 harness；viewer 未实现
```

## 5. Git Final State

以最终 `git status` / `git log` 为准（commit 在报告后执行）。push 未执行。

## 6. Filesystem & Resource Safety

```text
writes outside /root/my_project = NONE
free -h before                   = available ≈ 6.2Gi，swap 0
heavy task                       = N/A（无 replay/C/pytest 长任务）
peak RSS                         ≈ 1.1Gi（系统）+ Viewer 构建 < 0.1Gi
swap peak                        = 0
OOM                              = 0
```

## 7. Code / Architecture Changes

```text
component            new/old behavior                            reason
replay/geospatial.py raster traversal replacing fixed-degree sample L2 不漏小岛
same as above        LAND polarity now 1=sea,0=land              对齐项目规范
replay/preflight.py  new L2 + viewer presentation preflight      正式门禁
scripts/replay_l2_preflight.py / replay_viewer_preflight.py      CLI 入口
replay/presentation.py active/pending revision fields            Viewer 语义明确
viewer/*             basemap/bundle/embed/server/viewer MVP      真实播放主链
```

## 8. Semantic / Contract Changes

修正一个核心 contract 误解：

```text
old: land_sea_mask value 1 interpreted as LAND
new: canonical semantics value 1 = SEA（elevation<0）；0 = land/coast
affected: geospatial.LandMaskSampler.sample / cell_status；
         previous Viewer Foundation L2 smoke 描述
```

同时 Adapter 增加显式：

```text
active_plan_revision
pending_plan_revision
pending_plan_status
```

`REPLAN_DECIDED != REPLAN_ADOPTED` 语义不变，Viewer timeline 在 pending 期间
仍以 active route 为主并单独显示 pending route。

## 9. Experiments / Alternatives

尝试过 `playwright-cli`（wrapper/npx、chromium、firefox）与本地 `http.server`
socket：均被当前受限 profile 禁止（子进程 daemon / socket bind 失败）。未采用
浏览器截图路线，改为：自包含单文件 Viewer + 数据渲染 proof PNG + bundle 契约
单测。HTTP server 脚本保留给非受限环境。

## 10. Authoritative / Real Validation

```text
replay_l2_preflight       = PASS（5 个 route revision + completed tracks，
                             0 land cell；dataset=GEBCO_2026 0.05°）
replay_viewer_preflight    = PASS，presentation_eligible=True
（snapshots/manifest PASS，projection_consistency PASS，layer coverage PASS）
bundle                     = 721 timeline entries，gates PASS
```

## 11. Correctness / Validation

```text
unit suite      = 78 passed, 2 deselected；ruff all green
preflight tests = real artifact PASS + synthetic fail-closed
bundle tests    = 10:00<10:30<11:00；max 1min delta<2km；track 不回退；
                 13:30 pending rev2 / 15:00 active rev2；
                 REPLAN_SKIPPED 生效但不改 active
proof PNG       = 10:30 / 13:30（GEBCO basemap + route/track/pending/vessel）
13 h 级全量 replay 未重跑（不必要，只动 presentation/adapter/viewer）
```

## 12. Determinism / Reproducibility

```text
latest-head 12h determinism = INHERITED（未重跑；back-end digest 未变）
bundle deterministic        = 由同一 manifest/snapshot 生成
dominant wall-clock fields  = 浏览器渲染时间（允许）
```

## 13. Artifacts / Provenance

```text
replay-l2-preflight.json           PASS, provenance=GEBCO_2026 doi
replay-viewer-preflight.json       PASS, eligible
viewer/bundle.json                 721 entries，gitignored（构建生成）
viewer/gebco_basemap.png           gitignored
viewer/index_self_contained.html   gitignored（embed 生成）
output/playwright/replay-viewer-proof-*.png（machine proof，gitignored）
```

## 14. Known Limitations / Technical Debt

```text
TD-44 统计口径（REPLAN_DECIDED 计数）   FIXED（上轮已修）
TD-45 Pending-Plan Gate                  NOT DONE（semantics-first）
TD-46 L2 极性误解                        CORRECTED THIS ROUND
TD-47 Browser smoke in sandbox           BLOCKED（operator 在非受限环境运行）
TD-48 Viewer superseded route drawing    NOT DRAWN（contract supports）
TD-49 Dynamic Risk overlay               NEXT
```

## 15. Unexpected Findings / Corrections

```text
old claim（Foundation doc）: L2 smoke 穿陆线 FAIL / 水域 PASS（按 1=land 推断）
new evidence: 项目规范变量语义 = 1 sea / 0 land；真实 12h route 全部 sea
corrected claim: L2 = PASS；Viewer Foundation §8 smoke 描述需更新
affected: STRATEGY_B_VIEWER_FOUNDATION_20260819.md、
        arctic_route_orchestrator/replay/geospatial.py
```

## 16. Claim Matrix

```text
Claim                                     Status  Validation Level    Evidence
-------------------------------------------------------------------------------
L2 real Scenario B PASS                   PASS    REAL_E2E_PASS       5 rev + tracks
Presentation eligible                     PASS    REAL_E2E_PASS       preflight
Ship moves 10:00->10:30->11:00            PASS    REAL_E2E_PASS       bundle+proof
Track append-only                         PASS    UNIT_PASS           bundle test
Pending route not early adopt             PASS    REAL_E2E_PASS       13:30 pending
Viewer page in real browser               NOT RUN NOT_IMPLEMENTED    sandbox blocked
Dynamic Risk overlay                      NOT STARTED NOT_IMPLEMENTED -
```

## 17. Decision / Next Phase

推荐下一轮：在非受限环境跑 `replay_viewer_serve.py` + 浏览器 smoke；然后
Dynamic Risk / Hard Reason overlay、superseded route drawing、replanning event
animation、最终 UI polish。明确不做：Pending-Plan Gate（仅当需要再优化 12h
性能时再议）、新 replay、新场景、Planner 重写。

## 18. Push

```text
PUSH = NOT PERFORMED
```
