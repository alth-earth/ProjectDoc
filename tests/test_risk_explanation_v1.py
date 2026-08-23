"""Executable proposal tests for ``risk-explanation.v1``.

These tests validate the design artifacts only. They are not production B, C,
Orchestrator, or D integration code.
"""

from __future__ import annotations

import copy
import json
import math
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "current/proposals/risk-explanation.v1.schema.json"
EXAMPLE_PATH = ROOT / "current/proposals/risk-explanation.v1.example.json"


def _load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


SCHEMA = _load(SCHEMA_PATH)
EXAMPLE = _load(EXAMPLE_PATH)
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())


def _schema_errors(document: dict[str, Any]) -> list[str]:
    return [
        error.message
        for error in sorted(VALIDATOR.iter_errors(document), key=lambda item: list(item.path))
    ]


def _semantic_errors(
    document: dict[str, Any],
    *,
    reference: dict[str, Any] | None = None,
) -> list[str]:
    """Apply invariants that JSON Schema cannot express safely."""

    errors: list[str] = []
    formula_components = set(document["producer"]["formula_component_ids"])
    frame_ids: set[str] = set()
    frame_times: set[str] = set()
    all_statuses: list[str] = []
    total_omitted = 0

    if reference is not None:
        for field, expected in reference["identity"].items():
            if document["identity"].get(field) != expected:
                errors.append(f"identity mismatch: {field}")

    for frame in document["frames"]:
        frame_id = frame["risk_frame_id"]
        frame_time = frame["frame_time"]
        if frame_id in frame_ids:
            errors.append(f"duplicate risk_frame_id: {frame_id}")
        if frame_time in frame_times:
            errors.append(f"duplicate frame_time: {frame_time}")
        frame_ids.add(frame_id)
        frame_times.add(frame_time)

        grid = frame["grid"]
        coverage = frame["coverage"]
        cells = frame["cells"]
        expected_cells = grid["rows"] * grid["columns"]
        if coverage["expected_cell_count"] != expected_cells:
            errors.append(f"{frame_id}: expected_cell_count != rows * columns")
        if coverage["published_cell_count"] != len(cells):
            errors.append(f"{frame_id}: published_cell_count != len(cells)")
        status_counts = {
            status: sum(cell["explanation_status"] == status for cell in cells)
            for status in ("COMPLETE", "PARTIAL", "UNAVAILABLE")
        }
        for status, field in (
            ("COMPLETE", "complete_cell_count"),
            ("PARTIAL", "partial_cell_count"),
            ("UNAVAILABLE", "unavailable_cell_count"),
        ):
            if coverage[field] != status_counts[status]:
                errors.append(f"{frame_id}: {field} is inconsistent")
        if coverage["published_cell_count"] + coverage["omitted_cell_count"] != expected_cells:
            errors.append(f"{frame_id}: published + omitted != expected")
        total_omitted += coverage["omitted_cell_count"]
        all_statuses.extend(cell["explanation_status"] for cell in cells)

        reference_frame = None
        if reference is not None:
            reference_frame = reference["frames"].get(frame_id)
            if reference_frame is None:
                errors.append(f"{frame_id}: not present in referenced RiskWindow")
            else:
                if frame_time != reference_frame["frame_time"]:
                    errors.append(f"{frame_id}: frame_time mismatch")
                if grid["grid_id"] != reference_frame["grid_id"]:
                    errors.append(f"{frame_id}: grid_id mismatch")

        seen_cells: set[tuple[int, int]] = set()
        for cell in cells:
            row = cell["cell"]["row_index"]
            column = cell["cell"]["column_index"]
            key = (row, column)
            if key in seen_cells:
                errors.append(f"{frame_id}: duplicate cell {key}")
            seen_cells.add(key)
            if row >= grid["rows"] or column >= grid["columns"]:
                errors.append(f"{frame_id}: cell {key} is outside grid bounds")

            risk = cell["risk"]
            if risk["score"] is not None:
                expected_level = min(5, math.floor(risk["score"] * 5) + 1)
                if risk["level"] != expected_level:
                    errors.append(f"{frame_id}: cell {key} risk_level mismatch")

            contributor_ids: set[str] = set()
            covered_components: set[str] = set()
            for contributor in cell["contributors"]:
                contributor_id = contributor["contributor_id"]
                if contributor_id in contributor_ids:
                    errors.append(f"{frame_id}: cell {key} duplicate contributor_id")
                contributor_ids.add(contributor_id)
                component_ids = set(contributor["component_ids"])
                if covered_components & component_ids:
                    errors.append(f"{frame_id}: cell {key} component counted twice")
                covered_components |= component_ids
                dominant = contributor.get("dominant_component_id")
                if dominant is not None and dominant not in component_ids:
                    errors.append(
                        f"{frame_id}: cell {key} dominant_component_id is not covered"
                    )

            main_ids = set(cell["reason"]["main_contributor_ids"])
            if not main_ids <= contributor_ids:
                errors.append(f"{frame_id}: cell {key} reason cites absent contributor")
            if not covered_components <= formula_components:
                errors.append(f"{frame_id}: cell {key} uses unknown formula component")

            explanation_status = cell["explanation_status"]
            gaps = set(cell["uncertainty"]["explanation_gaps"])
            if explanation_status == "COMPLETE":
                if risk["score"] is None:
                    errors.append(f"{frame_id}: cell {key} complete explanation has null risk")
                else:
                    contribution_sum = math.fsum(
                        item["contribution"] for item in cell["contributors"]
                    )
                    if not math.isclose(
                        contribution_sum,
                        risk["score"],
                        rel_tol=0.0,
                        abs_tol=1e-6,
                    ):
                        errors.append(f"{frame_id}: cell {key} contributions do not sum to risk")
                if covered_components != formula_components:
                    errors.append(f"{frame_id}: cell {key} formula coverage is incomplete")
            elif explanation_status == "PARTIAL":
                if covered_components & gaps:
                    errors.append(f"{frame_id}: cell {key} covered components also marked gaps")
                if covered_components | gaps != formula_components:
                    errors.append(f"{frame_id}: cell {key} partial component accounting is incomplete")

            if reference_frame is not None:
                expected = reference_frame["cells"][key]
                if not math.isclose(cell["cell"]["latitude"], expected["latitude"], abs_tol=1e-9):
                    errors.append(f"{frame_id}: cell {key} latitude mismatch")
                if not math.isclose(cell["cell"]["longitude"], expected["longitude"], abs_tol=1e-9):
                    errors.append(f"{frame_id}: cell {key} longitude mismatch")
                if risk["score"] != expected["score"]:
                    errors.append(f"{frame_id}: cell {key} risk_score mismatch")
                if risk["level"] != expected["level"]:
                    errors.append(f"{frame_id}: cell {key} risk_level mismatch against frame")
                if not math.isclose(risk["confidence"], expected["confidence"], abs_tol=1e-6):
                    errors.append(f"{frame_id}: cell {key} confidence mismatch")

    publication_status = document["publication_status"]
    if publication_status == "COMPLETE" and (
        total_omitted != 0 or any(status != "COMPLETE" for status in all_statuses)
    ):
        errors.append("publication_status COMPLETE contradicts cell coverage")
    if publication_status == "PARTIAL" and not any(
        status in {"COMPLETE", "PARTIAL"} for status in all_statuses
    ):
        errors.append("publication_status PARTIAL has no usable explanation")
    if publication_status == "UNAVAILABLE" and any(
        status in {"COMPLETE", "PARTIAL"} for status in all_statuses
    ):
        errors.append("publication_status UNAVAILABLE contains usable explanations")
    return errors


def _reference_for_example() -> dict[str, Any]:
    identity = copy.deepcopy(EXAMPLE["identity"])
    frame = EXAMPLE["frames"][0]
    cell = frame["cells"][0]
    key = (cell["cell"]["row_index"], cell["cell"]["column_index"])
    return {
        "identity": identity,
        "frames": {
            frame["risk_frame_id"]: {
                "frame_time": frame["frame_time"],
                "grid_id": frame["grid"]["grid_id"],
                "cells": {
                    key: {
                        "latitude": cell["cell"]["latitude"],
                        "longitude": cell["cell"]["longitude"],
                        "score": cell["risk"]["score"],
                        "level": cell["risk"]["level"],
                        "confidence": cell["risk"]["confidence"],
                    }
                },
            }
        },
    }


def _optional_consumer_mode(
    sidecar: dict[str, Any] | None,
    *,
    semantic_errors: list[str] | None = None,
) -> str:
    """Model the proposed D gate without changing D production code."""

    if sidecar is None or semantic_errors:
        return "BASE_RISK_VIEW"
    if sidecar["publication_status"] == "UNAVAILABLE":
        return "BASE_RISK_VIEW"
    return "RISK_EXPLANATION_VIEW"


class RiskExplanationV1ProposalTests(unittest.TestCase):
    def test_schema_is_valid_draft_2020_12(self) -> None:
        Draft202012Validator.check_schema(SCHEMA)

    def test_example_passes_schema_and_semantic_reference_checks(self) -> None:
        self.assertEqual(_schema_errors(EXAMPLE), [])
        self.assertEqual(
            _semantic_errors(EXAMPLE, reference=_reference_for_example()),
            [],
        )

    def test_partial_cell_publishes_only_verified_components(self) -> None:
        document = copy.deepcopy(EXAMPLE)
        document["publication_status"] = "PARTIAL"
        frame = document["frames"][0]
        cell = frame["cells"][0]
        retained = cell["contributors"][0]
        covered = set(retained["component_ids"])
        cell["explanation_status"] = "PARTIAL"
        cell["contributors"] = [retained]
        cell["reason"] = {
            "code": "PARTIAL_EXPLANATION",
            "text": "Only the verified ice contribution is available",
            "locale": "en",
            "main_contributor_ids": ["ice"],
        }
        cell["uncertainty"] = {
            "status": "EXPLANATION_GAP",
            "missing_data": [],
            "explanation_gaps": sorted(
                set(document["producer"]["formula_component_ids"]) - covered
            ),
        }
        frame["coverage"]["complete_cell_count"] = 0
        frame["coverage"]["partial_cell_count"] = 1
        self.assertEqual(_schema_errors(document), [])
        self.assertEqual(_semantic_errors(document), [])

    def test_unavailable_cell_cannot_publish_contributors(self) -> None:
        document = copy.deepcopy(EXAMPLE)
        cell = document["frames"][0]["cells"][0]
        cell["explanation_status"] = "UNAVAILABLE"
        cell["contributors"] = []
        cell["reason"] = {
            "code": "EXPLANATION_UNAVAILABLE",
            "text": "Explanation metadata is unavailable",
            "locale": "en",
            "main_contributor_ids": [],
        }
        cell["uncertainty"] = {
            "status": "UNKNOWN",
            "missing_data": [],
            "explanation_gaps": [],
        }
        self.assertEqual(_schema_errors(document), [])
        cell["contributors"] = [copy.deepcopy(EXAMPLE["frames"][0]["cells"][0]["contributors"][0])]
        self.assertTrue(_schema_errors(document))

    def test_unsupported_version_fails_schema(self) -> None:
        document = copy.deepcopy(EXAMPLE)
        document["schema_version"] = "risk-explanation.v2"
        self.assertTrue(_schema_errors(document))

    def test_null_or_invented_contribution_fails_schema(self) -> None:
        document = copy.deepcopy(EXAMPLE)
        document["frames"][0]["cells"][0]["contributors"][0]["contribution"] = None
        self.assertTrue(_schema_errors(document))

    def test_complete_contributions_must_sum_to_bound_risk_score(self) -> None:
        document = copy.deepcopy(EXAMPLE)
        document["frames"][0]["cells"][0]["contributors"][0]["contribution"] = 0.11
        self.assertIn("contributions do not sum to risk", " ".join(_semantic_errors(document)))

    def test_duplicate_cell_fails_semantic_validation(self) -> None:
        document = copy.deepcopy(EXAMPLE)
        frame = document["frames"][0]
        frame["grid"]["columns"] = 2
        frame["coverage"]["expected_cell_count"] = 2
        frame["coverage"]["published_cell_count"] = 2
        frame["coverage"]["complete_cell_count"] = 2
        frame["cells"].append(copy.deepcopy(frame["cells"][0]))
        self.assertIn("duplicate cell", " ".join(_semantic_errors(document)))

    def test_identity_mismatch_fails_closed_to_base_view(self) -> None:
        reference = _reference_for_example()
        reference["identity"]["generation_id"] = 1
        errors = _semantic_errors(EXAMPLE, reference=reference)
        self.assertIn("identity mismatch: generation_id", errors)
        self.assertEqual(
            _optional_consumer_mode(EXAMPLE, semantic_errors=errors),
            "BASE_RISK_VIEW",
        )

    def test_risk_value_mismatch_fails_closed_to_base_view(self) -> None:
        reference = _reference_for_example()
        frame_id = EXAMPLE["frames"][0]["risk_frame_id"]
        reference["frames"][frame_id]["cells"][(0, 0)]["score"] = 0.31
        errors = _semantic_errors(EXAMPLE, reference=reference)
        self.assertIn("risk_score mismatch", " ".join(errors))
        self.assertEqual(
            _optional_consumer_mode(EXAMPLE, semantic_errors=errors),
            "BASE_RISK_VIEW",
        )

    def test_missing_sidecar_preserves_normal_viewer_behavior(self) -> None:
        self.assertEqual(_optional_consumer_mode(None), "BASE_RISK_VIEW")


if __name__ == "__main__":
    unittest.main()
