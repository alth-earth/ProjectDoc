> **二次文档治理归档声明**
>
> - 本文件角色：2026-08-15 改造前的十日执行计划快照，仅供历史追溯。
> - 归档时间：2026-08-15（Asia/Shanghai）。
> - 现行文件：[ABC_10_DAY_SPRINT.md](ABC_10_DAY_SPRINT.md)。
> - 归档原因：把科学/实源验收从挑战杯演示完成门槛中移出，并落实最新优先级和实验 B 顺序。
>
> <!-- ORIGINAL CONTENT START -->

> **文档治理声明**
>
> - 本文件角色：2026-08-14 至 2026-08-23 的 A–B–C 与编排器唯一执行排期。
> - 改造时间：2026-08-14（Asia/Shanghai）。
> - 原文归档：[ABC_10_DAY_SPRINT.archive-20260814-pre-governance.md](ABC_10_DAY_SPRINT.archive-20260814-pre-governance.md)。
> - 改造原因：用本轮盘点、统一 handoff 和实测门禁重排关键路径，严格区分“代码已实现”与“实源已验收”。
> - 架构依据：[ARCTIC_ROUTE_SYSTEM.md](ARCTIC_ROUTE_SYSTEM.md)。

# A–B–C 十个自然日并行冲刺

生效日为 2026-08-14（Day 1），冻结日为 2026-08-23（Day 10）。十天是开发日历，不是运行
时域；主走廊默认 168 h、允许 144–216 h，迁移走廊默认 96 h、允许 72–144 h。

## 1. 冲刺目标

本轮只承诺一条可审计的科研演示主线：

```text
主走廊真实 12 类 / 168 h
        ↓ G1
DatasetBundle v2 + RunContext v2 + doctor/exact resolver
        ↓ G2
B 169 个逐小时 formal canonical RiskFrame + committed full/suffix
        ↓ G3
C v2 三目标 + simulation_start+6h 重规划
        ↓ G4
C v3 四层 × 三目标 = 12 条路线
        ↓ G5
编排器报告、JSON/GeoJSON、SHA-256 清单、两次断网复现
```

Day 7 前冻结 v2 主线；Day 8–9 只在同一冻结输入上验收 v3；Day 10 只做阻断修复、回归、
文档与制品冻结。D、科研模型扩展和可选数据不得挤占这条关键路径。

## 2. Day 1 事实基线

| 工程 | 已具备 | 尚未满足的冲刺门禁 |
|---|---|---|
| contracts 0.3.0 | 动态窗、双走廊、bundle v2 复核、RunContext v2；18 tests passed | 本地 `main` ahead 1 的同步决策；真实 bundle 输入 |
| A 0.4.2 | 采集/归档/回放/doctor/exact resolver；172 tests passed | 主走廊真实恰好 12 类、168 h 正式制品 |
| B 0.2.0 | 规则 full/suffix committed 主线；40+8 tests passed | 同一真实 bundle 的 169 帧窗口 |
| B CNN P1 | safetensors、CPU 单步后端、10 model tests passed | P2 未授权/未实现；不进入正式主线 |
| C 0.4.0 | v2/v3、重规划与原子发布；138 passed | 真实 B 窗口的 v2、+6 h 与 v3 证据 |
| orchestrator 0.1.0 | 公共 API 编排；Python 3.13.15 + uv 0.12.4、`uv.lock`、非集成门禁通过 | 集成测试阶段遥测、性能预算、完整收口与两次复现 |
| experimental B 0.1.0 | 现有 `.venv` 中 35 tests passed | stale lock、无有效 Mamba 前缀、Ruff I001；不阻塞正式主线 |

以上测试是 2026-08-14 的实测快照；fixture 通过不等于实源或科学验收。

## 3. 范围与所有权

| 所有者 | 本冲刺必须完成 | 明确不做 |
|---|---|---|
| contracts | 保持共享身份、动态窗、12+2 类和 v2 合同稳定；协助真实上下文物化 | 不接纳 B/C 私有参数，不把十日写入运行时域 |
| A | 真实 12 类/168 h、bundle v2、RunContext、doctor、168/168 replay、exact resolver | 可选水深/法规区不阻塞；不统一目标网格 |
| B | 对同一 bundle 构建 169 帧 full/suffix committed window 与失败报告 | 不切换 CNN；不生成最终船速、ETA 或路线 |
| C | v2 三目标、+6 h 重规划；其后 v3 四层 12 路线 | 不重写 A*/成本核心；不读取 A 私有目录 |
| orchestrator | 公共 API 串联、分阶段报告、清单、断网复现 | 不扫描私有数据库/缓存；不吞掉阶段失败 |
| experimental B | 仅在不影响主线时修复工程门禁 | 不进入正式 B store/C，不占用 P0 数据与长运行预算 |

## 4. 验收闸门

| 闸门 | 通过条件 | 未通过时的动作 |
|---|---|---|
| G0 环境与身份 | 记录各仓 commit/dirty/version；标准命令可启动；同一 RunContext | 停止长运行，先修环境或版本歧义 |
| G1 A 实源 | 恰好 12 类；168 h 全窗；coverage/provenance true；doctor `errors=[]`；exact resolver 跨进程一致 | 保留来源错误；D3 日终触发短航区后备，不拼旧数据 |
| G2 B 窗口 | 60 min 闭区间 169 帧；full/suffix 原子 commit；身份/摘要一致；缺测/future/stale 均拒绝 | 回到 A/B 边界定位，不以 synthetic 或 CNN 替代 |
| G3 C v2 | 三目标齐全；ETA 严格递增；硬约束违规 0；risk IDs 可追溯；+6 h 重规划成功 | 保留 v2 失败证据，禁止进入 v3 |
| G4 C v3 | 四层各 `fastest/low_risk/recommended`；12 条完整；同一 lease/身份；整组原子发布 | 不发布部分层；保持 v2 冻结主线 |
| G5 复现冻结 | 两次断网运行输入与配置摘要一致；报告、JSON/GeoJSON、SHA-256 清单完整；各仓门禁与链接检查通过 | Day 10 只修阻断，不增加功能 |

G1–G5 的 `formal` 仅说明工程来源链通过。所有输出仍必须标注未校准与禁止导航。

## 5. 十日执行表

| 日期 / Day | A 与 contracts | B | C | orchestrator / 集成 | 当日退出条件 |
|---|---|---|---|---|---|
| 08-14 / D1 | 冻结走廊、场景、168 h、12 类与来源计划 | 冻结规则配置、目标网格与拒绝矩阵 | 冻结 v2/v3 输入、成本摘要与性能测量点 | 记录版本；建立分阶段 run report；补标准环境方案 | G0 设计与身份清单完成 |
| 08-15 / D2 | 分源小窗认证；优先动态/难源 | 准备只读真实输入预检和 169 帧资源预算 | 准备真实网格 smoke 与可取消超时 | 每阶段开始/结束/耗时/摘要落盘 | 至少一个完整采集候选，无静默降级 |
| 08-16 / D3 | 主走廊 12 类分批采集；日终判定 coverage 候选 | 对已冻结候选只做预检，不提前宣称 formal | 保持 fixture 回归，不启动全量 v3 | 汇总来源失败与剩余时间预算 | 形成主走廊候选；否则触发 96 h 后备 |
| 08-17 / D4 | 168/168 replay、doctor、bundle v2、RunContext、exact resolver | 对通过 G1 的制品执行 full build/commit | 对真实网格做受限 v2 smoke | 固化输入与内容摘要 | G1 通过；若未过，给出明确阻断报告 |
| 08-18 / D5 | 只修来源/证据链阻断 | 完成 169 帧、失败矩阵、重启恢复 | 完成 v2 三目标基线 | 生成阶段报告与制品清单 | G2 通过 |
| 08-19 / D6 | 冻结输入，不再无关补采 | 执行 +6 h suffix commit，验证旧代次拒绝 | 执行 +6 h 重规划；核对 ETA/hard mask/risk IDs | 第一次完整离线彩排 | G3 通过 |
| 08-20 / D7 | 保存实源证据与复核报告 | 冻结规则配置和 committed 窗口 | 冻结 v2 三目标与重规划输出 | 第二次断网彩排并比较摘要 | v2 主线冻结；否则明确未完成实源验收 |
| 08-21 / D8 | 主线只读支持 | 不改主线；提供同一 execution source | 在同一输入上运行 v3 四层整组 | 记录逐层耗时/内存，但只允许整组发布 | v3 可运行且没有部分发布 |
| 08-22 / D9 | 有余量才准备短航区，不影响主线 | 支持 v3 复验 | 完成 12 路线、codec、JSON/GeoJSON 与原子发布复验 | 比较两次 v3 摘要和性能 | G4、G5 通过 |
| 08-23 / D10 | 回归与证据冻结 | 回归与制品冻结 | 回归与文档冻结 | 全量链接、摘要、状态与交接验收 | 不留“完成但无证据”的任务 |

## 6. 降级与停止规则

1. **D3 实源闸门**：主走廊仍无完整候选时，可尝试迁移走廊 96 h；不得把旧 v1、9 类、
   稀疏旧 B 或 formal-shape fixture 改名成实源验收。
2. 两条走廊都失败时，保留 fixture 工程链和完整失败报告，结论必须写“实源验收未完成”。
3. G1 未通过不做正式 G2；G2 未通过不做真实 G3；G3 未通过不把 v3 作为主线成果。
4. 单阶段达到安全超时或内存预算时，先取消并落盘报告；不允许无心跳无限等待。
5. 可选数据、CNN、实验 B、第二走廊、性能算法升级不得阻塞规则 v2 主线。

## 7. CNN 与实验旁支

`22_深度学习综合风险预测模型.zip` 已在正式 B 仓库内完成 P1 可选实验后端整合，但 P2 shadow
sidecar 未完成，也未进入正式 RiskFrame/store/C。是否启动 P2 是人工决策，不是本冲刺默认任务。

若用户另行批准 P2，只允许：显式开关、fail-open、隔离输出、超时不影响正式 build、单独指标与
保留期。它不能替换规则主线，也不能把单步预测复制为 169 小时序列。

实验 B 的 lock/Mamba/Ruff 修复可以作为 P1 工程卫生任务，但只有在 G1–G3 关键路径不受影响时
执行；35 tests 的现有 `.venv` 结果不能写成 Mamba+uv 验收通过。

## 8. 风险与负责人动作

| 风险 | 当前信号 | 负责人动作 |
|---|---|---|
| 外部源覆盖/凭据/目录变化 | 新来源仅有小窗 smoke，真实 168 h 未完成 | A 保存请求、错误、发布时间与后备选择；不补造数据 |
| 网格规划耗时和内存未知 | 上次长运行约 56 分钟后未收口 | C/编排器按阶段测量，设置取消点和预算 |
| 环境不可复现 | 编排器环境已补齐；实验 B lock stale 且 Mamba 前缀无效 | 编排器固定使用自己的 Mamba+uv 与 `uv.lock`；实验 B 仍隔离修复，不借用另一 `.venv` 冒充。编排器集成测试还需性能预算 |
| 版本/工作树串线 | contracts ahead 1；多仓并行 | 每次验收记录 commit、dirty、版本与摘要 |
| 科学有效性被夸大 | 规则、船型、CNN 未校准 | 所有产物双维标注并保持 `navigation_use=prohibited` |
| D 缺失 | 当前无 D 工程 | 本冲刺只冻结 v3 消费合同与制品，不宣称展示闭环 |

## 9. 完成定义

冲刺只有在以下项目均有文件化证据时才算完成：

- G0–G5 逐项通过，或每个未通过项都有可复现的阻断报告和明确所有者；
- 一个冻结 RunContext 贯穿 bundle、169 RiskFrames、v2/v3、重规划和运行报告；
- v2 三目标与 v3 12 路线满足身份、ETA、hard mask、risk IDs 和原子发布约束；
- 两次断网复现的输入、配置和内容摘要一致；
- 各仓标准门禁、`git diff --check`、Markdown 相对链接与归档原文保护检查通过；
- 各 handoff、[系统架构](ARCTIC_ROUTE_SYSTEM.md)、本排期和[最终交付说明](最终交付说明.md)
  对同一状态使用一致措辞；
- 没有把 synthetic、legacy、fixture、P1 CNN 或未校准结果描述成真实正式成果。

## 10. 明确延期

新训练 Transformer/CNN、Q50/Q90/概率预测、AIS/事故标签训练、真实船舶和 Ice Class 1A
校准、方向相关风浪流、净水深和法律限制区硬约束、D、MPC、D* Lite/LPA*、10/30 min 正式
输出均不属于本冲刺。是否在后续推进，必须在当前主线冻结后另立目标、所有者与验收标准。

## 11. 执行入口

- [唯一系统架构权威](ARCTIC_ROUTE_SYSTEM.md)
- [阶段一项目梳理报告](项目梳理报告.md)
- [contracts handoff](arctic_route_contracts/arctic_route_contracts_handoff.md)
- [A handoff](work_package_a/work_package_a_handoff.md)
- [B 总 handoff](work_package_b_handoff/work_package_b_handoff.md)
- [C handoff](work_package_c/work_package_c_handoff.md)
- [编排器 handoff](arctic_route_orchestrator/arctic_route_orchestrator_handoff.md)
- [实验 B handoff](work_package_b_experimental/work_package_b_experimental_handoff.md)

本计划的排期变化只在本文件维护；稳定合同和架构决策留在各接口文档与
[ARCTIC_ROUTE_SYSTEM.md](ARCTIC_ROUTE_SYSTEM.md)，不得把日期复制回稳定合同。
