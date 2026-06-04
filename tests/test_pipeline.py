"""End-to-end assertions for the pipeline against dummy data."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.pipeline import DEFAULT_INPUT, DEFAULT_PLAN, OUTPUT_DIR, run
from src.stage1_filter import collapse_duplicate_entities
from src.stage6_edges import build_master_edges
from src.stage2_handoff_review.summarize_findings import _by_requirement
from src.utils.columns import col
from src.utils.standardization import normalize_policy_id, split_multi


class FilterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = run(DEFAULT_INPUT, DEFAULT_PLAN, OUTPUT_DIR)

    def test_filter_counts(self) -> None:
        stats = self.result["filter_stats"]
        self.assertEqual(stats["remaining"], 48)
        self.assertEqual(stats["removed_type_only"], 0)
        self.assertEqual(stats["removed_status_only"], 2)

    def test_nodes_match_active(self) -> None:
        self.assertEqual(len(self.result["nodes"]), 48)

    def test_active_statuses_only(self) -> None:
        self.assertTrue((self.result["nodes"]["Audit Entity Status"] == "Active").all())


class ParsingTests(unittest.TestCase):
    def test_split_multi_trims_and_drops_empty(self) -> None:
        self.assertEqual(split_multi("a; b;c;  ;"), ["a", "b", "c"])

    def test_split_multi_handles_nan(self) -> None:
        import math
        self.assertEqual(split_multi(float("nan")), [])
        self.assertEqual(split_multi(None), [])
        self.assertEqual(split_multi(""), [])

    def test_policy_normalization(self) -> None:
        self.assertEqual(normalize_policy_id("AEBC 65"), "AEBC_65")
        self.assertEqual(normalize_policy_id("POL 009"), "POL_009")
        self.assertEqual(normalize_policy_id("STD_003"), "STD_003")


class EdgeExclusionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = run(DEFAULT_INPUT, DEFAULT_PLAN, OUTPUT_DIR)

    def test_no_model_edges(self) -> None:
        edges = self.result["edges"]
        self.assertTrue((edges["Edge Type"] != "shared_model").all())
        self.assertNotIn("shared_model", set(edges["Edge Type"].unique()))

    def test_edge_types_are_expected_set(self) -> None:
        allowed = {"handoff_to", "handoff_from", "shared_app", "shared_vendor", "shared_prsa"}
        actual = set(self.result["edges"]["Edge Type"].unique())
        self.assertTrue(actual.issubset(allowed), f"Unexpected edge types: {actual - allowed}")

    def test_shared_app_edge_dedup(self) -> None:
        # Same entity listed twice with same app should not self-pair.
        tbl = pd.DataFrame(
            [
                {"Audit Entity ID": "AE-X", "Application Name": "AppA", "Relationship": "primary"},
                {"Audit Entity ID": "AE-X", "Application Name": "AppA", "Relationship": "secondary"},
                {"Audit Entity ID": "AE-Y", "Application Name": "AppA", "Relationship": "primary"},
            ]
        )
        edges = build_master_edges(pd.DataFrame(), tbl, pd.DataFrame(), pd.DataFrame(), {"AE-X", "AE-Y"})
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges.iloc[0]["Edge Type"], "shared_app")


class CoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = run(DEFAULT_INPUT, DEFAULT_PLAN, OUTPUT_DIR)

    def test_matrix_excludes_model_from_connectivity(self) -> None:
        mat = self.result["coverage_matrix"]
        self.assertIn("Connectivity Total", mat.columns)
        self.assertIn("Model Exposure", mat.columns)
        # Sum of connectivity is twice number of edges (each edge touches 2 endpoints).
        edges = self.result["edges"]
        expected = 2 * len(edges)
        self.assertEqual(int(mat["Connectivity Total"].sum()), expected)

    def test_flag_priorities_valid(self) -> None:
        flags = self.result["coverage_flags"]
        if len(flags):
            self.assertTrue(set(flags["Priority"]).issubset({"HIGH", "MEDIUM", "LOW"}))

    def test_output_workbooks_exist(self) -> None:
        # The pipeline date-stamps every workbook (e.g. layer1_output_YYYYMMDD.xlsx),
        # so match the dated form rather than a bare name.
        import glob
        for base in (
            "layer1_output",
            "edge_derivation_output",
            "layer2_coverage_matrix",
        ):
            self.assertTrue(glob.glob(str(OUTPUT_DIR / f"{base}_*.xlsx")), f"missing {base}_*.xlsx")


class ManualRequirementRollupTests(unittest.TestCase):
    GAP = "likely coverage gap"

    def _frame(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {"manual_requirement": "Make ownership explicit",
                 "classification": "likely coverage gap", "focal_entity_id": "AE-1", "reasoning": "r1"},
                {"manual_requirement": "Make ownership explicit",
                 "classification": "conforms", "focal_entity_id": "AE-2", "reasoning": "r2"},
                {"manual_requirement": "  ",
                 "classification": "likely coverage gap", "focal_entity_id": "AE-3", "reasoning": "r3"},
                {"manual_requirement": "Attribute-level documentation",
                 "classification": "documentation issue", "focal_entity_id": "AE-1", "reasoning": "r4"},
            ]
        )

    def test_groups_and_counts(self) -> None:
        out = _by_requirement(self._frame(), self.GAP)
        self.assertEqual(len(out), 3)
        row = out[out["requirement"] == "Make ownership explicit"].iloc[0]
        self.assertEqual(int(row["finding_count"]), 2)
        self.assertEqual(int(row["gap_count"]), 1)
        self.assertEqual(int(row["entity_count"]), 2)

    def test_blank_rolls_into_none(self) -> None:
        out = _by_requirement(self._frame(), self.GAP)
        self.assertIn("(none)", set(out["requirement"]))
        self.assertNotIn("", set(out["requirement"]))

    def test_sorted_by_gap_then_finding_count(self) -> None:
        out = _by_requirement(self._frame(), self.GAP)
        # Highest gap_count first; ties broken by finding_count desc.
        self.assertEqual(out.iloc[0]["requirement"], "Make ownership explicit")

    def test_empty_input_returns_typed_columns(self) -> None:
        out = _by_requirement(pd.DataFrame(), self.GAP)
        self.assertEqual(len(out), 0)
        self.assertIn("gap_count", out.columns)


class CollapseDuplicateEntitiesTests(unittest.TestCase):
    ID = col("entity_id")
    BU = col("business_unit")

    def _frame(self) -> pd.DataFrame:
        # AE-1 spans two business units (two rows differing only by BU); AE-2 single row.
        return pd.DataFrame(
            [
                {self.ID: "AE-1", self.BU: "Retail Bank", "Audit Leader": "Chen", "Compliance Residual Risk": "High"},
                {self.ID: "AE-1", self.BU: "Commercial Bank", "Audit Leader": "Chen", "Compliance Residual Risk": "High"},
                {self.ID: "AE-2", self.BU: "Markets", "Audit Leader": "Patel", "Compliance Residual Risk": "Low"},
            ]
        )

    def test_collapses_multi_bu_into_one_row(self) -> None:
        out, dup, conflicts = collapse_duplicate_entities(self._frame())
        self.assertEqual(len(out), 2)
        self.assertEqual(dup, 1)
        self.assertEqual(conflicts, [])
        ae1 = out[out[self.ID] == "AE-1"].iloc[0]
        self.assertEqual(ae1[self.BU], "Retail Bank; Commercial Bank")
        self.assertEqual(ae1["Audit Leader"], "Chen")  # non-BU field preserved

    def test_no_duplicates_is_passthrough(self) -> None:
        df = self._frame().drop_duplicates(subset=self.ID)
        out, dup, conflicts = collapse_duplicate_entities(df)
        self.assertEqual(len(out), len(df))
        self.assertEqual(dup, 0)
        self.assertEqual(conflicts, [])

    def test_conflicting_rating_is_flagged(self) -> None:
        df = self._frame()
        df.loc[1, "Compliance Residual Risk"] = "Critical"  # AE-1's two rows now disagree
        out, dup, conflicts = collapse_duplicate_entities(df)
        self.assertEqual(conflicts, ["AE-1"])


if __name__ == "__main__":
    unittest.main()
