# RC2 开发状态

状态：CURRENT（当前）
最后更新：2026-08-17
适用范围：Demo RC1 之后的 RC2 功能完善阶段
权威基线：`work_package_a/docs/DEMO_RC1_BASELINE_20260816.md`（RC1 不可变）

## 1. 基线

- RC1 baseline commit（根仓库）：`29aa74d`（已同步 GitHub main）
- RC2 开发分支：`rc2-development`（根仓库 + contracts/B/C/D/orchestrator/A）
- RC2 起始 commit = 各仓库 RC1 提交（`8-16demo交付`）
- 原则：RC1 只作为 regression / golden 参照；新功能一律属于 RC2

## 2. 本轮完成 / 进行中 / 阻塞

| 能力 | 状态 | 说明 |
|---|---|---|
| RC2 分支建立 | PASS | 根仓库 + 6 个子仓库均建立 `rc2-development` |
| RC1 测试期望同步 | PASS | contracts 18、C 138 基线恢复；修正 corridor 2.2.0 过期断言 |
| 真实 worker 成功冒烟 | PASS | 三次完整跑通（CLI 修复后 EXIT=0）；业务结果与 r6 一致；发现并修复 CLI 结果消费 bug |
| 真实 worker 超时冒烟 | PASS | 专用真实 C worker：四层 A* 45.2s 被中断，TIMEOUT 报告、无孤儿、无半成品 |
| hard_reason 语义 | PASS（代码/测试） | B 产生；C codec/schema 消费；D 可展示 preflight 摘要 |
| coverage preflight 正式化 | PASS | orchestrator 新增阶段 + schema + gate；真实 worker 运行与 v2 集成均含该阶段 |
| RC1 golden regression | PASS | r6/r7 layer-set digest 与 checksums 校验通过 |
| 第二场景迁移 | PASS | corridor 1.2.0 + 无冰语义修复后：coverage gate、连通性、v2/v3 smoke、replan、D 全部 PASS |
| D 解释性增强 | PASS | coverage CLI/snapshot + 12 tests |
| 文档同步 | PASS | 根状态/计划/技术债/架构 + 各 WP README/CHANGELOG 已同步 |

### 集成测试说明（2026-08-17）

- 集成 fixture 使用 RC1 smoke grid v4（396 节点）后，C 搜索规模与正式链相同：
  v2 单次 c_initial≈433s、c_replanning≈398s，v2+v3 全参数 ≈36 分钟；
- 发现 run-report 内存形态 bug：`a_input.requested_data_types` 为 tuple，
  与 schema 的 array 要求不一致（落盘 JSON 为 array，仅 in-memory 校验失败）；
  已在 `_run_report` 转 list；v2 集成复验 PASS（15:24）、v3 集成复验 PASS（21:18）。

## 4. worker 成功冒烟证据（2026-08-17）

- 输入：RC1 冻结 bundle `a-bundle-32cafad4…` + RunContext `0b0005` + corridor 2.2.0
  + smoke grid v4（plus_unknown）+ v3 四层 + 6h 重规划；
- stage report：`completed`，8 阶段（含 coverage_preflight 0.008s）；
  init 538.6s / b_build 15.4s / c_initial 483.4s / suffix 3.0s / c_replanning 506.2s；
- checksums：全部一致；业务字段与 r6 完全一致（distance/ETA/risk/cost/层/转弯/
  expanded），仅 plan_id / source_risk_ids / compute_ms 不同（hard_reason 改变
  风险帧内容 ID，属预期元数据差异）；
- 发现并修复：CLI `run` 消费 worker 返回 dict 时误用属性访问（`result.output_dir`），
  修复后新增 2 项 CLI 单测；worker 运行本身未受影响。
- 第二次 worker 全链（timeout650 spec 因缓存提速未触发超时）完整跑通，
  CLI 修复后 EXIT=0；stage 耗时与 r6 相当（init 535.9s / initial 483.3s /
  replan 512.0s）。
- 超时机制实证：90/360/545/560s spec 均在真实 worker 上正确触发 TIMEOUT
  （多数落在 initialization，因 init 耗时 360–560s 波动）；
- 真实 C 超时冒烟（`scripts/real_c_timeout_worker.py` + `run_real_c_timeout_smoke.py`）：
  直接消费 worker 成功运行提交的 RC1 风险窗运行真实四层 A*；
  watchdog 45.2s 中断，stage report `TIMEOUT/c_initial_planning/45.2s`，
  无孤儿进程、无部分正式输出。

## 3. 第二场景数据结论（初步）

- 场景：`tromso_isfjorden_rc2_smoke_v1`（72h，corridor 1.2.0）
- bundle：`a-bundle-7eb08aec58dd101247157456`（612 记录，本地冻结数据）
- RunContext：`run-…0c0001/0c0002/0c0003`（同一 bundle，不同 run_id）
- intake：PASS（约 124 s）
- 端点可航性（coarse 帧证据）：68.5–70.4°N 全带宽（10–22°E）无任何可航单元；
  起点原区域（18–20.5E/69.4–70N）全为 LAND/DATA_UNAVAILABLE；1.2.0 外海起点
  （17–19E/70–71N）同样全部 DATA_UNAVAILABLE；最近可航区在 71.1°N 以西或
  71.7°N 以北。终点区域在 0.375°×1.25° 网格有 1 个可航节点。
- 结论：迁移设计本身 PASS（新场景/版本化走廊/72h 本地 bundle/intake/B/preflight
  全链路可用）；**数据覆盖 = BLOCKED**——需新采集（覆盖挪威沿海带的
  ocean/ice/wave 产品）或走廊起点重新设计（>71.5°N），属操作者设计决策。
- 走廊变更：`tromso_to_isfjorden_outer` 1.1.0 → 1.2.0（外海起点 70.5N/18E，
  起点允许区域 17–19E/70–71N），旧 1.1.0 事实归档为
  `configs/corridors/tromso_to_isfjorden_outer.1.1.0-archive.toml`；
  4 个 tromso 场景的 corridor_version 同步更新（未触碰 RC1 mur 配置）。
  旧 `tromso_isfjorden_august_2026_demo_v1` RunContext（run-…0a0001）仍为 1.1.0，
  与 1.2.0 配置不再兼容；如需回放需按新配置重新生成 RunContext。

### 3.1 根因与解决（2026-08-17 第二轮）

- 根因不是“挪威沿岸无数据”：TOPAZ6（ARCTIC 6.25km NERSC-HYCOM）在
  17–19E/70–71N 原生有限率 93%（395/425），wave 95–98%，GFS/GEBCO 100%；
  **NEXTsim ice_type/ice_edge 在无冰水域原生全 NaN（0/2244）**是唯一全区域缺口，
  物理上“无冰 → 无冰型/冰缘”是预期语义，不是缺测。
- 决策：**不北移走廊、不新下载**；保持 corridor 1.2.0（仍为 Tromsø 外海语义，
  起点 70.5N/18E 距特罗姆瑟约 85 km 挪威海），在 B 增加 RC2 专属策略
  `land_sea_mask_plus_unknown_ice_free_v1`：TOPAZ 冰浓度 ≤0.15 的单元格将
  NEXTsim ice_type/edge NaN 中性化为 0（零风险贡献）；其余 unknown 仍 fail-closed。
  RC1 策略与 digest 不变。
- 效果（73 帧网格 31×11=341 节点）：hard=86（LAND 65 + DATA_UNAVAILABLE 21）、
  navigable=255、unknown-navigable=0、finite_coverage=100%、start/goal 连通；
  端点映射 start (70.33N,18.4E) adj 23.8km、goal (78.03N,12.4E) adj 18.9km。

### 3.2 第二场景链路验证（2026-08-17）

| 阶段 | 状态 |
|---|---|
| corridor 1.2.0 / scenario 72h | PASS（RC2 配置，RC1 未动） |
| A bundle（本地冻结，无新下载） | REUSED（`a-bundle-7eb08aec…`） |
| RunContext 0c0004/0c0005 | PASS |
| intake | PASS（≈124s） |
| B（ice-free 策略） | PASS（73 帧） |
| coverage preflight | PASS（gate=true、73/73 帧） |
| connectivity | PASS（255 可航，start→goal 可达） |
| C v2 smoke（initial+replan） | PASS（909km/52h → 828km/48h，hard=0） |
| C v3 四层 smoke（initial+replan） | PASS（init 400.6s / replan 359.4s，12+12 路线） |
| D 消费（v3 + coverage） | PASS（complete，coverage 摘要正确） |

说明：第二场景为 72h smoke 窗口（非 144h 完整 RC）；`tromso_isfjorden_august_2026_demo_v1`
（144h）仍可走同一策略但未在本轮复跑。

## 4. 冻结与边界

- 不修改 RC1：corridor 2.2.0、mur 场景、risk semantics、hard-mask policy、
  C cost、RC1 artifacts 一律不动；
- RC2 新增：`tromso_isfjorden_rc2_smoke_v1` 场景、
  `demo_unvalidated_tromso_smoke_grid_v1.json` 网格配置、
  `hard_reason`（可选字段）、`planning-coverage-preflight.json`；
- 状态词：PASS / FAIL / TIMEOUT / BLOCKED / PARTIAL / NOT RUN / REUSED / DEFERRED。

## 5. 下一步

- worker 成功/超时冒烟收尾并记录证据；
- 若起点区域无解：记录第二场景数据缺口（所需产品/量）并转 PRE-DEMO 其他项；
- 全量测试（含 orchestrator integration 若时间允许）；
- 文档/状态最终同步 + checkpoint commits + 普通 push。

## 6. Git / Push 状态（2026-08-17 收尾）

- RC1 基线：根仓库 `29aa74d`（GitHub main 已同步，操作者完成）；
- RC2 分支：各仓库 `rc2-development`，checkpoint commits 已本地完成：
  contracts `54ee071`、B `bc7d830`（a1b2caa→ice-free）、C `ccd1e53`、
  D `c49a135`（28a8eda→coverage 增强）、orchestrator `1225e32`、
  根仓库 `24ce821`（7259fa7→第二场景状态）；
- 远程 push：本轮新 commit **未推送**——GitHub https 需要交互式凭据且环境无
  credential helper/gh；按项目约定不处理凭据，全部 commit 保留在本地
  `rc2-development`（上一轮 commit 已由操作者/外部环境同步至 origin）。

## 7. 长任务可靠性实测（2026-08-17）

- workspace-write sandbox 实测：>5 分钟 orchestrator 长任务两次在约 5 分钟内
  整进程树消失（无 result、无 stage report），判定为沙箱回收而非计算失败；
- 改用非沙箱/提权运行后同一任务完成（v2 全链 init 134.9s / initial 204.2s /
  replan 174.9s；v3 全链 init 124s / initial 400.6s / replan 359.4s）；
- DeepSeek stream 中断一次（用户侧报告）：先核查原进程/日志/制品，确认
  进程已退出且无有效结果后才重启，未发生重复并发执行；
- Agent-level 轮询采用 ~240s 间隔；任务心跳 `C_ASTAR_PROGRESS_SECONDS` 保留。
