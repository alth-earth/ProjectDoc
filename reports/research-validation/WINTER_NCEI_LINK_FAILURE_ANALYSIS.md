# NCEI 链接失效根因分析、相关建议与方案

- 生成日期：2026-08-22
- 关联报告：`WINTER_SOURCE_VALIDATION_REPORT.md`、`WINTER_MET_SOURCE_COMPARISON.md`、`WINTER_DATA_RESOLUTION_ROUND4_REPORT.md`、`WINTER_DATA_POLICY_PROPOSAL.md`（proposal `A-WINTER-MET-001`）
- 背景：工作包 A 冬季三类（10 m 风 / 2 m 温度 / 能见度）数据缺口，现覆盖率 9/12；官方 NCEI 直接入口对 2026-02 返回 404。

---

## 1. 核心结论（TL;DR）

1. **不是"硬编码链接拼错"**。A 现有 9 类与冬季候选使用同一命名规则 `gfs_4_{YYYYMMDD}_{HHMM}_{step}.grb2`，该格式与 NCEI 长期路径约定一致，代码拼写正确。
2. **根因是 NCEI 整条直接访问路径在云迁移期被撤下**：archive 根目录返回 `NoSuchKey`、THREDDS 已无月份子目录、NOMADS 历史周期 403。直链层已不存在 2026-02 数据。
3. **单纯"替换/新增一个直链 URL"无法补齐冬季缺口**——直链层已无该数据，必须走离线订单（HAS）或替代源（CARRA）。
4. 报告原始状态 `DIRECT_BLOCKED / OFFLINE_ORDER_CANDIDATE` 准确，不应表述为"NOAA 从未拥有这些数据"。

---

## 2. 实测证据（2026-08-22 curl 验证）

| 入口 | 实测结果 | 解读 |
|---|---|---|
| NCEI archive `oa/prod-model/.../grid-004-0.5-degree/analysis/` 根目录 | **`NoSuchKey` XML 错误** | 整个 `analysis/` 路径已从该公开桶移除 |
| NCEI archive `.../analysis/202602/20260215/gfs_4_20260215_0000_000.grb2(.inv)` | 404 | 精确对象不可达 |
| THREDDS `model-gfs-g4-anl-files` 根 catalog | 仅根 dataset，无任何月份子目录 | DatasetScan 实际为空 / 历史月未挂出 |
| NOMADS `gfs.20260215/00/atmos` | **403** | 历史周期已被清除 |
| NOMADS `gfs.20260820/00/atmos`（近期） | **200** | 仅保留滚动窗口数据 |
| NCEI GFS 产品页 / 元数据 C00634 | 仍声明 2007–至今、HAS/HTTPS/TDS | 元数据未随实际可达性更新，产生"声明存在 vs 实际不可达"落差 |
| AWS Open Data `noaa-gfs-bdp-pds` GFS 0.5° | 本机网络超时未验证（文档称 trailing 30 天窗口） | 大概率亦不含 2026-02 |

> 注：archive 根目录 `NoSuchKey` 与 THREDDS 无子目录 + NOMADS 历史 403 为三重互相印证的铁证，排除"个别文件命名偏差"假设。

---

## 3. 根因分析（为什么直链层没了）

- **NCEI 云现代化 / 数据迁移**：NOAA 正将 NWS 模型产品从旧 `www.ncei.noaa.gov/oa/prod-model/...` 路径迁移到新基础设施（NOMADS、AWS Open Data、HAS 归档订单）。`grid-004-0.5-degree/analysis` 这类旧 archive 直链是迁移中被弃用的遗留路径。
- **THREDDS DatasetScan 惰性生成**：`model-gfs-g4-anl-files` 现在扫描路径为空，说明该 THREDDS 数据集不再主动聚合历史月，仅对近期/按需生成。
- **NOMADS 滚动保留策略**：NOMADS 仅保留近期（约 30 天滚动）周期，2026-02 已被自然淘汰。
- **元数据陈旧**：产品页与 ISO 元数据（C00634）描述的是"理论上可通过 HAS/archive order 获取"，而非"当前 HTTP 直链可达"。二者脱节是产生误判（以为直链还能用）的来源。

**结论**：你的链接遵循的是 NCEI 长期稳定路径，与 A 现有 9 类同源；其"失效"是平台侧路径移除，而非代码缺陷。因此"改一个 URL 就能修好"的假设不成立。

---

## 4. 对代码的建议（保守、fail-closed）

目标：保留历史正确性，显式表达可达性状态，不引入未验证的硬依赖。

1. **保留** `NCEI_ARCHIVE_BASE` 及其 `gfs_4_...` 命名作为 fallback（云迁移完成可能恢复；A 现有 9 类依赖它，不可破坏）。
2. **新增** `NOMADS_BASE` 候选（优先级高于 archive，对近期数据 200 可用），并加入命名转换：`gfs.t{HH}z.pgrb2.0p50.f000`（NOMADS 命名）↔ `gfs_4_{date}_{cycle}_{step}.grb2`（NCEI 命名）。
3. **显式状态机**：在 acquisition 层将 `DIRECT_BLOCKED` / `OFFLINE_ORDER_CANDIDATE` / `AVAILABLE_RECENT` 作为可达性 gate，而非仅靠文档描述；404/403/NoSuchKey 触发降级而非静默失败。
4. **注释入口**：在常量区注明 HAS 归档订单入口（冬季缺口官方直路）与 CARRA（替代源，需 token+terms+adapter+旋转）。
5. **AWS S3 端点**：本机网络不可达，暂不写死；待能连通或换出口后再验证 2026-02 是否在窗口内。
6. **不破坏既有 9 类**：所有改动以"新增候选 + fallback 降级"方式落地，绝不改动现有 9 类已验证的获取路径。

---

## 5. 可选方案（按可行性排序）

### 方案 A：NCEI HAS 离线归档订单（官方、合规、但人工/延迟）
- 来源：NCEI 产品页与元数据 C00634 明确声明历史数据走 HAS（Historical Archive System）。
- 步骤：在 NCEI 站点提交 archive order → 人工审核 → 提供下载链接。
- 优点：最直接的官方原件，provenance 最干净。
- 缺点：需线下人工提交（受"禁止跨树写/需人工"约束，我不能代下）；有审核与交付延迟；不确定 2026-02 是否仍在 HAS 库存。
- 适用：坚持 NCEI 真源、可接受等待的场景。

### 方案 B：CARRA 3h（C3S/ECMWF，推荐，但需 4 项前置）
- 来源：CARRA 机器目录覆盖至 2026-05-31，含 10 m 风 / 2 m 温度 / 能见度；DOI `10.24381/cds.713858f6`，CC-BY-4.0；3 h 分析、2.5 km、East Arctic domain。
- 前置阻塞（当前全未满足）：
  1. 本机无 CDS personal access token；
  2. 未接受 CARRA dataset terms；
  3. A 无获批的 CARRA adapter；
  4. CARRA u/v 为投影网格方向，须可验证旋转满足 A 真东/真北 contract。
- 步骤：人工审阅批准 proposal `A-WINTER-MET-001` → 提供 token/terms → 单帧投影 + 风矢量旋转 smoke → 下载完整 49 个 3 h 时次。
- 优点：机器目录明确覆盖冬季、变量齐全、分辨率高。
- 缺点：依赖外部凭证审批与新建 adapter；Copernicus Marine 用户名/密码**不能**替代 CDS token。

### 方案 C：NOMADS 近期窗口回填（仅适用于"冬季"定义可放宽）
- 若业务可接受非 2026-02 而是最近滚动窗口做"冬季气象代表性"测试，NOMADS 200 可用。
- 缺点：不解决真实 2026-02 缺口，仅用于 pipeline 联调；与 9/12 目标无关。

### 方案 D：AWS Open Data `noaa-gfs-bdp-pds`（待验证）
- 需先在本机/可连通出口验证 2026-02 是否在 trailing 窗口（大概率不在）。
- 若可达，命名亦为 NOMADS 风格，需与方案 A 的命名桥接共用。
- 当前状态：`UNVERIFIED / NETWORK_BLOCKED`。

---

## 6. 推荐决策路径

1. **短期（立即可做，不阻塞）**：按第 4 节改 `forecast_acquisition.py`，把 NCEI 直链降级为 fallback 并加状态机，使"404/403/NoSuchKey → 显式 DIRECT_BLOCKED"而非误报成功。
2. **中期（解决缺口的二选一）**：
   - 走官方：你线下提交 NCEI HAS 订单，拿到链接后由 A 拉取并归入 provenance；
   - 走替代：走 proposal `A-WINTER-MET-001` 的 CARRA 路线，先补 token/terms 与 adapter+旋转 smoke。
3. **不做**：不要寄望于"改一个硬编码 URL"修好冬季缺口——直链层已无该数据。

---

## 7. 关联约束（来自 Codex 历史记忆，已同步修正）

- 用户已**解除**"禁止 subagent/parallel"约束（2026-08-22 更正）；外-project 写入禁止、不重复下载、缓存复用、诚实状态报告等约束仍保留。
- 凭证约束：不能索要/记录新 secret；Copernicus Marine 账户 ≠ CDS token；受限网络下 Copernicus `open_dataset` 失败须用前台会话 + 心跳轮询 + manifest 校验，勿用 `ulimit -v` 限制内存（NextSIM 实测 1.6 GB+）。
- 历史原件"无一被删/覆盖"；改文档应"另存新文件 + 原文件重命名归档"；中文为主。
