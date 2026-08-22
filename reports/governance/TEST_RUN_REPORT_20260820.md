---
Document Status: HISTORICAL_REPORT
Canonical Current State: NO
Scope: full test re-run of D (work_package_d) + orchestrator (arctic_route_orchestrator)
Branch: demo-engineering
Generated: 2026-08-20
---

# 完整测试重跑报告（2026-08-20）

> 背景：首次执行时因误操作提前终止。本轮从头完整执行所有相关测试，未被中断。
> 两个仓库均用 `uv` 管理；D 测试 1.6s，orchestrator 含 2 个长耗时 integration 场景（共 41m35s）。

---

## 1. D — work_package_d

### 1.1 ruff
```
uv run ruff check .
All checks passed!
```
> 注：本轮初 `conftest.py` 触发 E401/I001，已 `ruff --fix` 自动修复（拆行+排序），复检通过。

### 1.2 pytest (full)
```
platform linux -- Python 3.13.15, pytest-9.1.1
rootdir: /root/my_project/work_package_d
configfile: pyproject.toml
testpaths: tests
collected 50 items

tests/test_loader.py ............................ PASSED (3)
tests/test_models.py ........................... PASSED (3)
tests/unit/test_coverage_preflight.py ......... PASSED (3)
tests/unit/test_demo_frozen_loader.py ......... PASSED (5)
tests/unit/test_demo_spatial.py ............... PASSED (5)
tests/unit/test_demo_viewer_offline.py ........ PASSED (6)
tests/unit/test_geo_integrity.py .............. PASSED (9)
tests/unit/test_pngcodec.py ................... PASSED (6)
tests/unit/test_real_artifact_regression.py ... PASSED (3)
tests/unit/test_replay_viewer_bundle.py ....... PASSED (5)
tests/unit/test_temporal_semantics_audit.py ... PASSED (2)

============================== 50 passed in 1.59s ==============================
```

**D 结果：ruff clean + 50 passed (UNIT_PASS).**

---

## 2. orchestrator — arctic_route_orchestrator

### 2.1 ruff
```
uv run ruff check .
All checks passed!
```

### 2.2 pytest — fast suite (non integration/real_artifact)
```
collected 75 items / 2 deselected / 73 selected
tests/test_coverage_preflight.py .............. PASSED (2)
tests/test_execution_spec.py ................. PASSED (2)
tests/test_intake.py ......................... PASSED (1)
tests/test_output.py .......................... PASSED (3)
tests/test_schemas.py ......................... PASSED (2)
tests/test_stage_report.py .................... PASSED (3)
tests/unit/test_cli_run_worker_result.py ...... PASSED (2)
tests/unit/test_replay_determinism.py ........ PASSED (3)
tests/unit/test_replay_digests.py ............ PASSED (7)
tests/unit/test_replay_geospatial.py ......... PASSED (5)
tests/unit/test_replay_models.py ............. PASSED (3)
tests/unit/test_replay_navigation.py ......... PASSED (8)
tests/unit/test_replay_preflight.py .......... PASSED (3)
tests/unit/test_replay_presentation.py ....... PASSED (11)
tests/unit/test_replay_route_integrity.py .... PASSED (3)
tests/unit/test_replay_validation.py ......... PASSED (4)
tests/unit/test_timeout_runner.py ............ PASSED (3)
tests/unit/test_vessel_motion.py ............. PASSED (8)

======================= 73 passed, 2 deselected in 2.53s =======================
```

### 2.3 pytest — integration / real_artifact suite (long-running)
后台执行（`nohup ... > /tmp/orch_integ.log`），完整未被中断：
```
collected 75 items / 73 deselected / 2 selected

tests/integration/test_formal_run.py::
  test_formal_archive_to_b_to_c_and_six_hour_replan
    [cd.route-plan.v2-run-...-202-3-v2] ............................ PASSED [50%]
    [cd.four-layer-route-plan-set.v3-run-...-303-12-v3] ........... PASSED [100%]

================ 2 passed, 73 deselected in 2495.25s (0:41:35) =================
```

**orchestrator 结果：ruff clean + 75 passed (73 fast + 2 integration, REAL_E2E_PASS).**

---

## 3. 合并摘要

| Repo | ruff | pytest | duration | Level |
|---|---|---|---|---|
| work_package_d (D) | clean | 50 passed | 1.59s | UNIT_PASS |
| arctic_route_orchestrator | clean | 75 passed (73 fast + 2 integration) | 41m35s (integration) | REAL_E2E_PASS |
| **TOTAL** | **clean** | **125 passed, 0 failed, 0 error** | — | — |

### 正确性/验证覆盖（本轮复核）
- unit: D 50 + orch 73 → all pass
- integration/real-artifact: orch 2 → both pass (formal archive→B→C + 6h replan, v2 & v3)
- ruff: both repos clean
- (Viewer HTTP smoke + L2 polarity + D ownership: inherited REAL_E2E from prior round, unchanged)

### 说明 / 局限
- orchestrator integration 场景为真实重计算（6-hour replan），耗时 41m35s，属预期；本轮已完整跑完未被中断。
- D `conftest.py`（repo-root sys.path 注入）为测试基础设施修复，已 ruff-fixed，尚未在 D 仓库提交（待用户审阅）。
- 无 OOM / 无 timeout / 无 orphan。

---

## 4. 判定

```
ALL TESTS PASS:  YES  (125 passed, 0 failed)
RUFF CLEAN:      YES  (both repos)
```
