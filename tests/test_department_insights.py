"""Assertions for the department-wide insights fusion against dummy outputs.

Requires the dummy pipeline + Stage 2 aggregation artifacts to be present
(layer2_coverage_matrix_*.xlsx in data/output and findings_rollup.xlsx /
findings.csv under runs/stage2/aggregated). Writes its outputs to a temp
dir so it never clobbers data/output.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import department_insights as di

EXPECTED_SHEETS = {
    "Executive Scorecard", "Priority Worklist", "Fusion Cross-Tabs",
    "Gaps by Risk Category", "By Requirement", "Methodology & Caveats",
    "Systemic & Manual Gaps",
}


class DepartmentInsightsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = Path(tempfile.mkdtemp(prefix="dept_insights_"))
        cls.result = di.run(out_dir=cls.tmp, date_str="testrun")
        cls.worklist = cls.result["worklist"]
        cls.stats = cls.result["stats"]

    def test_outputs_written(self) -> None:
        self.assertTrue(self.result["xlsx"].is_file())
        self.assertTrue(self.result["html"].is_file())

    def test_workbook_has_expected_sheets(self) -> None:
        names = set(pd.ExcelFile(self.result["xlsx"]).sheet_names)
        self.assertTrue(EXPECTED_SHEETS.issubset(names),
                        f"missing sheets: {EXPECTED_SHEETS - names}")

    def test_gap_entities_within_evaluated(self) -> None:
        # The likely-gap-rate denominator is distinct focal entities; the
        # numerator can never exceed it.
        findings = di._load_findings(di.DEFAULT_INPUT_DIR)
        evaluated = findings["focal_entity_id"].astype(str).nunique()
        self.assertLessEqual(self.stats["gap_entities"], evaluated)
        self.assertGreater(evaluated, 0)

    def test_worklist_rows_carry_structural_signal(self) -> None:
        # Every row is either flagged with ≥1 structural reason or explicitly
        # labelled in-plan/verify-only — never blank.
        self.assertFalse(self.worklist.empty)
        for reasons in self.worklist["Structural Reasons"]:
            self.assertTrue(str(reasons).strip(), "worklist row has no reason text")

    def test_high_priority_implies_not_in_plan(self) -> None:
        high = self.worklist[self.worklist["Priority"] == "HIGH"]
        self.assertTrue((high["In Plan"] == "No").all(),
                        "HIGH priority must mean the gap entity is not in plan")

    def test_fusion_counts_bounded(self) -> None:
        n = self.stats["gap_entities"]
        self.assertLessEqual(self.stats["gap_not_in_plan"], n)
        self.assertLessEqual(self.stats["gap_high"], n)
        self.assertLessEqual(self.stats["t5_gap_pairs"], self.stats["t5_pairs"])

    def test_html_has_caveat_and_tiers(self) -> None:
        text = self.result["html"].read_text(encoding="utf-8")
        self.assertIn("candidate leads", text)
        self.assertIn("decision-grade", text)
        self.assertIn("false-positive", text.lower())


if __name__ == "__main__":
    unittest.main()
