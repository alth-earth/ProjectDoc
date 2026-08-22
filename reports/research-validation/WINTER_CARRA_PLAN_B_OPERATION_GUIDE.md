# 方案 B：CARRA 3h 完整操作指南（C3S/ECMWF，推荐但需 4 项前置）

- 生成日期：2026-08-22
- 目标源：`reanalysis-carra-single-levels`（C3S/ECMWF CARRA 单层级再分析）
- DOI：`10.24381/cds.713858f6`；许可：CC-BY-4.0
- 覆盖：1991–至今（机器目录报 temporal end = `2026-05-31T00:00:00Z`）
- 变量：10 m 风（u/v）、2 m 温度、能见度；East Arctic domain（北挪威、巴伦支海、斯瓦尔巴）；2.5 km；3 h 分析
- 关联：proposal `A-WINTER-MET-001`（DRAFT / PENDING_APPROVAL）；`WINTER_SOURCE_VALIDATION_REPORT.md`

---

## 0. 为什么是 CARRA（一句话）

它是唯一经机器目录证明覆盖 2026-02 冬季窗口、且同时含风/2m温/能见度三变量的**单一原子源**；NCEI 直链已撤（DIRECT_BLOCKED），NOMADS 历史 403，ERA5 缺能见度。

但落地前必须跨越 4 个前置门，其中 3 个必须**人工**完成。

---

## 1. 四个前置门与责任划分

| # | 前置 | 谁来做 | 是否可脚本化 | 状态（当前） |
|---|---|---|---|---|
| G1 | CDS personal access token | **人工**（你） | 否（需登录账号生成） | 未配置（`/root/.cdsapirc` 缺失） |
| G2 | 接受 CARRA dataset terms | **人工**（你） | 否（需在网页勾选同意） | 未记录 |
| G3 | A 的 CARRA adapter（含风矢量旋转） | **AI（我）**，需你批准后实现 | 是（代码） | 未实现 |
| G4 | 单帧投影 + 风旋转 smoke 验证 | AI 实现 + 你触发 | 是（测试） | 未运行 |

> G1/G2 是硬凭证门，AI 无法代为申请或代为"接受条款"——这涉及你的账户身份与法律同意。
> Copernicus Marine 用户名/密码 **不能** 替代 CDS token（两套独立服务）。

---

## 2. 人工步骤（G1 + G2）具体怎么做

### G1：获取 CDS personal access token

1. 打开 CDS 账户页（需已有 Copernicus Climate/ECMWF 账号；没有则先注册）：
   `https://cds.climate.copernicus.eu/`
2. 进入 **User profile / API key** 页面（或直接访问
   `https://cds.climate.copernicus.eu/api-how-to` 的 "How to use the API" 小节）。
3. 复制页面上显示的 **personal access token**（一长串 `xxxx:yyyy...` 形如
   `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx:abcdef...`）。
4. **不要**把 token 提交进任何 git 仓库或日志。放置到本机两处之一：
   - 推荐：`/root/.cdsapirc`（文件权限 `600`），内容：
     ```
     url: https://cds.climate.copernicus.eu/api
     key: <你的 personal access token>
     ```
   - 或仅导出环境变量（不落盘）：
     ```
     export CDS_API_KEY="<你的 personal access token>"
     ```
5. 本仓库约定：token 与 terms 接受状态**不入库、不打印**。A 的采集层应从
   `~/.cdsapirc` 或 `CDS_API_KEY` 读取，绝不硬编码。

### G2：接受 CARRA dataset terms

1. 打开数据集页：
   `https://cds.climate.copernicus.eu/datasets/reanalysis-carra-single-levels`
2. 点击 **"Download data" / "Submit"** 或 terms 面板，阅读并勾选同意
   **dataset terms**（含 CC-BY-4.0 署名要求）。
3. 接受后 CDS 才会允许该 dataset 的 API 检索（否则返回 403/terms-not-accepted）。
4. 在 A 侧记录"terms 已接受"这一事实（仅记状态，不记 token 值），作为
   `A-WINTER-MET-001` 批准的证据链路一环。

> 完成 G1+G2 后，可让我执行一次**最小化连通性探测**（仅 `cdsapi` 元数据请求，
> 不下载数据）来确认凭证与条款门已通过，再进入 G3。

---

## 3. AI 步骤（G3 + G4）做什么、你如何触发

### G3：实现 CARRA adapter（待你批准 `A-WINTER-MET-001` 后由我写）

新增一个**附加的、不破坏现有 NCEI 路径**的采集分支，至少包含：

1. **East-domain 空间子集**：按冬季窗口 bbox（北挪威/巴伦支海/斯瓦尔巴）裁剪。
2. **时间选择**：2026-02-15 00:00Z 起，3 h 步长，至 2026-02-21 00:00Z，共 49 个时次。
3. **变量映射**：`10m_u_component_of_wind`、`10m_v_component_of_wind`、
   `2m_temperature`、`visibility`（CARRA 变量名以 CDS 实际暴露为准）。
4. **issue-time 证据**：保留 CDS 返回的可信发布时间，而非仅检索时间。
5. **投影/风矢量旋转（关键风险）**：
   - CARRA u/v 是**投影网格方向**（Lambert conformal / polar-stereographic 局部 x/y），
     不是真东/真北。
   - A 的 contract（`AB_INTERFACE.md`）要求真东/真北分量。
   - adapter 必须读取 CARRA 网格映射（grid mapping / projection parameters），
     对每格点做可验证旋转：`true_east = u*cosθ + v*sinθ` 之类的局部角变换，
     **保留旋转证据**（投影参数、旋转矩阵、验证样本），禁止直接重命名 u/v。
   - 已有先例：`curvilinear.py` 与 `normalization._normalize_vector_semantics`
     处理 TOPAZ 投影分量 → 真东/真北，可复用其旋转框架。
6. **source snapshot / checksum / 重启恢复**：与现有 NCEI 采集一致。
7. **provenance**：`source_uri` 指向 CARRA dataset，`product_id` 区分于 NCEI。

> 新增文件建议：`src/arctic_route_data/carra_acquisition.py` + 对应测试，
> 不改动 `forecast_acquisition.py` 现有 NCEI 函数（保护 9 类已验证路径）。

### G4：单帧 smoke 验证（你批准后由我写测试并运行）

- 下载 **1 个时次**（如 2026-02-15 00:00Z）East-domain 子集。
- 断言：风分量旋转后为真东/真北（与已知站点/邻近格点交叉验证）；温度/能见度有限值；
  维度/坐标完整；provenance 完整。
- 仅 smoke 通过后才允许 49 时次全量下载。

---

## 4. 全量下载与落地序列（G3+G4 之后）

1. 单帧 smoke PASS（含风旋转验证）。
2. 按 3 h 步长下载 49 个时次，每类（风/温/能见度）独立 checkpoint，断点续传。
3. 每类精确 49 时次覆盖；缺任一即 fail-closed，不静默补齐。
4. 运行 `make doctor` 与 12 型覆盖诊断（**不带** `--allow-incomplete`）。
5. `all_required_complete=true` 时才持久化 winter bundle。
6. bundle 落地后，才允许 B/C smoke 按顺序运行。

---

## 5. 你的最小操作清单（人工部分）

- [ ] G1：生成 CDS personal access token → 写入 `~/.cdsapirc`（权限 600）或 `CDS_API_KEY` 环境变量。
- [ ] G2：打开 CARRA dataset 页，接受 dataset terms。
- [ ] 回复"批准 `A-WINTER-MET-001` 并已完成 G1/G2"，触发我做连通性探测。
- [ ] 审查我交付的 CARRA adapter + 旋转 smoke 测试（代码评审）。
- [ ] 触发全量 49 时次下载与 doctor/覆盖校验。

---

## 6. 风险与回退

- **凭证/条款门不过**：adapter 无法运行；此时唯一官方直路退回 NCEI HAS 离线订单（方案 A）。
- **风旋转错误**：若旋转证据不足或验证样本偏差，须回退重写，不得带着错误分量发布（违反 A 真东/真北 contract）。
- **CARRA 目录撤回 2026-02**：机器目录当前报覆盖至 2026-05-31，但下载前须再次确认该窗口仍在；若被裁剪，退回方案 A。
- **网络受限**：Copernicus 下载应在前台联网会话执行（`timeout ... | tee ...` + 心跳/输出/manifest 校验），勿信 sandbox `ps`；勿用 `ulimit -v` 限制内存。

---

## 7. 关联约束（来自 Codex 历史记忆，已同步修正）

- 用户已**解除**"禁止 subagent/parallel"约束；外-project 写入禁止、不重复下载、缓存复用、诚实状态报告仍保留。
- 文档治理以 `/root/my_project/arctic_route_governance/standards/AGENT_DOCUMENTATION_RULES.md` 为准（取代旧的"原件不得删/覆盖 + 另存新文件归档"规则）；中文为主保留。
