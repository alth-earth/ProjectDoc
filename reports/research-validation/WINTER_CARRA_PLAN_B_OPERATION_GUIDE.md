# 方案 B：CARRA 3h 完整操作指南（C3S/ECMWF，推荐但需 4 项前置）

- 生成日期：2026-08-22
- 目标源：`reanalysis-carra-single-levels`（C3S/ECMWF CARRA 单层级再分析）
- DOI：`10.24381/cds.713858f6`；许可：CC-BY-4.0
- 覆盖：1991–至今（机器目录报 temporal end = `2026-05-31T00:00:00Z`）
- 变量：10 m 风（u/v）、2 m 温度、能见度；East Arctic domain（北挪威、巴伦支海、斯瓦尔巴）；2.5 km；3 h 分析
- 关联：proposal `A-WINTER-MET-001`（**APPROVED 2026-08-22**）；`WINTER_SOURCE_VALIDATION_REPORT.md`

---

## 0. 为什么是 CARRA（一句话）

它是唯一经机器目录证明覆盖 2026-02 冬季窗口、且同时含风/2m温/能见度三变量的**单一原子源**；NCEI 直链已撤（DIRECT_BLOCKED），NOMADS 历史 403，ERA5 缺能见度。

但落地前必须跨越 4 个前置门，其中 3 个必须**人工**完成。

---

## 1. 四个前置门与责任划分

| # | 前置 | 谁来做 | 是否可脚本化 | 状态（当前） |
|---|---|---|---|---|
| G1 | CDS personal access token | **人工**（你） | 否（需登录账号生成） | 已配置（`/root/my_project/work_package_a/.cdsapirc`，权限受限，不入库） |
| G2 | 接受 CARRA dataset terms | **人工**（你） | 否（需在网页勾选同意） | 已接受（2026-08-22 单帧探测返回 200，证明 terms 已过） |
| G3 | A 的 CARRA adapter（含风矢量处理） | **AI（我）** | 是（代码） | **已实现**（`src/arctic_route_data/carra_acquisition.py`，dry-run + 单帧 smoke 通过） |
| G4 | 单帧投影 + 风 smoke 验证 | AI 实现 + 你触发 | 是（测试） | **已运行并 PASS**（2026-08-22 真实下载 2026-02-15T00Z，数值合理） |

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
5. **投影/风矢量（关键风险已排除）**：
   - **2026-08-22 单帧探测结论**：CARRA 单层级地表风 `10u`/`10v` 的
     `standard_name` 为 `eastward_wind` / `northward_wind`，即**已是真东/真北分量**，
     **无需**投影网格方向旋转。早期报告担心的旋转风险对 CARRA 单层级地表风**不适用**。
   - 因此 adapter 直接按真东/真北分量 regrid，保留了网格证据（`latitude`/`longitude`
     2D 坐标、`domain=east_domain`），不再调用 `normalization._normalize_vector_semantics`。
   - 备注：若未来扩展 CARRA **压力层/模式风**（非单层级），需重新评估是否为投影分量。
6. **source snapshot / checksum / 重启恢复**：与现有 NCEI 采集一致（`publisher.publish_dataset`、
   `.part -> sidecar` 原子发布、SHA-256）。
7. **provenance**：`source` 标签 `C3S/ECMWF CARRA Single-Levels (East domain)`，`product_id`
   区分于 NCEI，含 `analysis_cycle_id` / `nominal_interval_hours=3` / `domain`。

> 新增文件建议：`src/arctic_route_data/carra_acquisition.py` + 对应测试，
> 不改动 `forecast_acquisition.py` 现有 NCEI 函数（保护 9 类已验证路径）。

### G4：单帧 smoke 验证（已运行 2026-08-22）

- 下载 **1 个时次**（2026-02-15 00:00Z）East-domain 子集，真实跑通。
- 断言（已PASS）：风分量为真东/真北（无需旋转）；温度/能见度有限值；
  维度/坐标完整；provenance 完整。数值示例：u10 ∈ [-12.7, 14] m/s，
  t2m ∈ [235, 275] K，vis ∈ [75.8, 5e4] m。
- 单帧测试已沉淀为 `tests/unit/test_carra_acquisition.py`（离线 mock，12 项）。
- 仅 smoke 通过后才允许 49 时次全量下载。

---

## 4. 全量下载与落地序列（G3+G4 已满足，**已执行 2026-08-22**）

1. 单帧 smoke PASS（风无需旋转，结论已确认）。
2. 按 3 h 步长下载 **49 个时次**（02-15T00Z..02-21T00Z），每类独立 checkpoint。
3. 每类精确 49 时次覆盖；缺任一即 fail-closed，不静默补齐。✅ 实际 147 帧全发布。
4. 运行 `doctor` 与 12 型覆盖诊断（**不带** `--allow-incomplete`）。
5. `all_required_complete=true`（在 horizon 对齐下）时才持久化 winter bundle。
6. bundle 落地后，才允许 B/C smoke 按顺序运行。

### 执行结果与关键发现（2026-08-22）

- **route_id 修正**：首次误用 `A-winter-carra`（contracts 不存在的路由），
  导致数据进不了走廊 bundle；已删除该错误批次（168 记录 + `data/ready/A-winter-carra`），
  GRIB 缓存保留，改用正确路由 `tromso_to_isfjorden_outer` 重发。
- **doctor**：`ok: true`，5379 校验，0 errors / 0 warnings。
- **12-type 覆盖（G6，初版）**：通过（exit 0，`all_required_complete=True`），但揭示一个
  对齐问题——整套 2026-02 数据末端停在 **02-21T00Z**，而默认 `horizon_hours=144`
  的回放 `requested_end` 延伸到 02-21T12Z，造成每类 12h 末端缺口。用
  `--horizon-hours 132`（对齐 `minimum_required_end = 02-20T12Z`）后 12 类全部
  `complete`。CARRA 自身 49 周期连续无缺。
- **遗留决策（冻结 bundle 前需拍板）**：02-21T00Z..12Z 的 12h 末端缺口。选项：
  (a) 为全部 9 类非 CARRA 冬季源也补 02-21T03/06/09/12Z；或 (b) 以 `horizon=132`
  对齐冻结 winter bundle。

### 方案 (a) 执行记录（2026-08-22 下午，已收尾）

- **决策**：用户选择方案 **(a)**——为全部非 CARRA 冬季源补 02-21T03/06/09/12Z 四时次，
  消除 G6（默认 `horizon=144` → `requested_end=02-21T12Z`）的 12h 末端缺口。
- **可行性预检（非污染 smoke）**：临时 data_root 跑单源 `wave` @ 02-21T03Z
  `horizon=10h`，Copernicus 成功返回 03/06/09/12/15Z（dataset version `202411`），
  证明 2026-02-21 历史数据可达，文件名格式与正式 ready 一致 → 无阻断性问题，才正式执行。
- **校正**：用户口述"9 类非 CARRA"，但 `land_sea_mask` 是 GEBCO 派生 **static**
  （全窗口 1 份、与时间无关），不在 `COPERNICUS_FORECAST_SPECS`，无法也不需"补时次"。
  实际补的是 **8 类动态源**：`ocean_current` / `sea_ice_concentration` / `sea_ice_drift` /
  `sea_ice_thickness` / `sea_ice_type` / `sea_ice_edge` / `water_level` / `wave`。
- **实现**：`scripts/winter_non_carra_tail_acquisition.py`，逐类调用
  `acquire_copernicus(route_id, bounds, start_time=2026-02-21T03Z, horizon_hours=10,
  data_types=(dt,), mode=RETROSPECTIVE_BEST_ESTIMATE)` 指向正式 `data/`。逐类独立
  try 以避免单类失败影响其余、避免重跑触发 manifest 不可变冲突。需 `.env.copernicus`
  （`COPERNICUSMARINE_SERVICE_USERNAME/PASSWORD`）+ `LD_LIBRARY_PATH=.mamba-env/lib`。
- **结果**：8 类全部 OK（各 1 snapshot）。补采后 02-21 新增时次：1h 源到 T13Z、
  `wave`(3h) 到 T15Z，覆盖目标 03/06/09/12Z。原有数据全部保留未动。
- **doctor**：`ok: true`，checked=5461，errors=[]（无 manifest 冲突/损坏）。
- **G6（默认 `horizon=144`，`requested_end=02-21T12Z`）**：**`all_required_complete=True`**，
  12 类全部 complete（含 `land_sea_mask`）。→ 12h 末端缺口已闭合，无需再退用
  `--horizon-hours 132`。方案 (a) 圆满收尾。
- **winter_bundle 冻结（2026-08-22 20:53）**：`replay ... --horizon-hours 144`
  （不带 `--allow-incomplete`）闸门通过，`all_required_complete=True`，原子写入
  `data/tromso_to_isfjorden_outer_winter_20260215T000000Z_bundle.json`
  （generation_id 0）。随后 `doctor`：`ok: true`，5461 checked，0 errors / 0 warnings。
  全部 A 治理闸门（G5/G6）闭合。

### 已批准的代码入口

- 全量：在 `CarraAcquisition(publish=True)` 下调用 `acquire(start_time, horizon_hours)`，
  覆盖 2026-02-15T00Z..02-21T00Z（49 个 3h 时次，对齐场景 `simulation_end`）。
- 单帧预演：`acquire_carra_dry_run(cycle, data_types=...)` 或
  `acquire_frame_smoke(cycle)`，均 `publish=False`。
- 运行需：`LD_LIBRARY_PATH` 指向 `.mamba-env/lib`（eccodes），`CDSAPI_RC` 指向
  `.cdsapirc`，且 `uv run --extra acquisition`。
- 对应脚本：`scripts/carra_full_acquisition.py`。

---

## 5. 你的最小操作清单（人工部分）

- [x] G1：CDS personal access token 已生成并写入 `.cdsapirc`（权限受限，不入库）。
- [x] G2：CARRA dataset terms 已接受（单帧探测返回 200 佐证）。
- [x] 批准 `A-WINTER-MET-001`（2026-08-22）→ AI 已实现 adapter + smoke + 测试。
- [x] 全量 49 时次采集已执行并发布（route_id 已修正为走廊，doctor ok）。
- [x] **方案 (a) 已执行（2026-08-22 下午）**：为 8 类动态非 CARRA 冬季源补
  02-21T03/06/09/12Z 末尾时次（land_sea_mask 为 static 跳过），G6 在默认
  `horizon=144` 下 `all_required_complete=True`，12h 末端缺口闭合，doctor ok。
- [ ] 审查已交付的 CARRA adapter + 测试（代码评审，可选）。
- [ ] 审查 `scripts/winter_non_carra_tail_acquisition.py`（方案 a 补采脚本，可选）。

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
