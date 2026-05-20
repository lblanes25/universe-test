"""Roll up Stage 2 findings into reviewer-ready Excel views.

Reads `runs/stage2/aggregated/findings.csv` and (optionally) the Nodes
sheet from `data/output/layer1_output.xlsx` for entity attributes, then
writes `runs/stage2/aggregated/findings_rollup.xlsx`.

The roll-up pivots on the axes that actually generalize across the firm:
the 14 standardized risk categories, audit leader, business unit, and
line of defense. KPA IDs and Specific Risk IDs are entity-local in this
data — no two entities share IDs — so grouping by them produces only
single-entity rows and is intentionally not done here.

Sheets:
  - Summary                       — counts by classification, task, evidence layer
  - Gaps by Risk Category         — likely coverage gaps grouped by the 14 categories
  - Doc Issues by Risk Category   — documentation issues grouped by the 14 categories
  - Top Entities by Issue Count   — concentration: which entities have the most findings
  - Gaps by Entity                — one row per gap finding, reviewer-ready
  - Manual Requirements           — findings flagged manual_requirement = True
  - By Audit Leader               — counts per audit leader (if nodes available)
  - By Business Unit              — counts per business unit (if nodes available)
  - By Line of Defense            — counts per LoD (if nodes available)
  - All Findings (Tagged)         — full findings.csv plus gate_passed flag

Usage:
    python -m src.stage2_handoff_review.summarize_findings

Future enhancement (deferred):
  Fuzzy text-clustering of KPA *descriptions* (and SR descriptions)
  across entities to identify conceptual duplicates — e.g. "Reconciliation"
  in one entity and "Reconciliation Process" in another likely cover the
  same process. Requires NLP-style similarity (embeddings or token
  overlap) since the IDs are entity-local. Worth building only if
  leadership wants firm-wide taxonomy standardization. See
  `memory/future_kpa_fuzzy_clustering.md` for the full sketch.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utils.excel_writer import write_workbook  # noqa: E402
from src.stage2_handoff_review import labels  # noqa: E402

DEFAULT_FINDINGS = ROOT / "runs" / "stage2" / "aggregated" / "findings.csv"
DEFAULT_GATE_LOG = ROOT / "runs" / "stage2" / "aggregated" / "gate_log.md"
DEFAULT_NODES = ROOT / "data" / "output" / "layer1_output.xlsx"
DEFAULT_OUT = ROOT / "runs" / "stage2" / "aggregated" / "findings_rollup.xlsx"


def _classification_value(canonical_substring: str) -> str:
    """Look up a classification's canonical value from a stable substring.

    Used so filters in this module don't hardcode the literal string — when
    the team renames a classification in config/stage2_prompt.yaml, this still
    resolves to whatever string the corpus actually contains.
    """
    for v in labels.classification_values():
        if canonical_substring in v.lower():
            return v
    raise ValueError(
        f"No classification value contains {canonical_substring!r}; "
        "edit config/stage2_prompt.yaml or update this lookup."
    )


def _parse_gate_log(path: Path) -> dict[int, bool]:
    """Return {batch_id: passed} from the gate log markdown."""
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    result: dict[int, bool] = {}
    for m in re.finditer(r"^#{2,3}\s+batch_(\d{3})\s+\u2014\s+(PASS|FAIL|MISMATCH)\s*$",
                          text, flags=re.MULTILINE):
        bid = int(m.group(1))
        result[bid] = (m.group(2) == "PASS")
    return result


def _load_nodes(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    try:
        nodes = pd.read_excel(path, sheet_name="Nodes")
    except Exception:
        return None
    mapping_path = ROOT / "config" / "column_mappings.json"
    cols = json.loads(mapping_path.read_text(encoding="utf-8"))
    keep = {
        cols["entity_id"]: "focal_entity_id",
        cols["entity_name"]: "entity_name_node",
        cols["audit_leader"]: "audit_leader",
        cols["business_unit"]: "business_unit",
        cols["line_of_defense"]: "line_of_defense",
    }
    present = {k: v for k, v in keep.items() if k in nodes.columns}
    if cols["entity_id"] not in nodes.columns:
        return None
    nodes = nodes[list(present.keys())].rename(columns=present)
    return nodes


def _summary_sheet(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    rows.append({"metric": "Total findings", "count": len(df)})
    for col in ("classification", "task", "evidence_layer"):
        if col in df.columns:
            counts = df[col].fillna("(blank)").value_counts()
            for k, v in counts.items():
                rows.append({"metric": f"{col} = {k}", "count": int(v)})
    if "manual_requirement" in df.columns:
        manual = df["manual_requirement"].astype(str).str.lower().isin({"true", "1", "yes"}).sum()
        rows.append({"metric": "manual_requirement = True", "count": int(manual)})
    if "gate_passed" in df.columns:
        rows.append({"metric": "from gate-passing batches", "count": int(df["gate_passed"].sum())})
        rows.append({"metric": "from gate-failing batches", "count": int((~df["gate_passed"]).sum())})
    return pd.DataFrame(rows)


def _by_risk_category(df: pd.DataFrame) -> pd.DataFrame:
    """Group findings by the 14 firm-wide risk categories."""
    if df.empty or "risk_category" not in df.columns:
        return pd.DataFrame(columns=[
            "risk_category", "entity_count", "finding_count",
            "affected_entities", "example_reasoning",
        ])
    work = df.copy()
    work["risk_category"] = work["risk_category"].fillna("(unspecified)").astype(str).str.strip()
    work.loc[work["risk_category"] == "", "risk_category"] = "(unspecified)"
    grouped = (
        work.groupby("risk_category")
        .agg(
            entity_count=("focal_entity_id", "nunique"),
            finding_count=("focal_entity_id", "size"),
            affected_entities=("focal_entity_id",
                                lambda s: "; ".join(sorted(set(s.dropna().astype(str))))),
            example_reasoning=("reasoning",
                                lambda s: next((x for x in s if isinstance(x, str) and x.strip()), "")),
        )
        .reset_index()
        .sort_values("entity_count", ascending=False)
    )
    return grouped


def _top_entities(df: pd.DataFrame, nodes: pd.DataFrame | None) -> pd.DataFrame:
    """Concentration view: which entities account for the bulk of findings."""
    if df.empty:
        return pd.DataFrame()
    pivot = (
        df.assign(classification=df["classification"].fillna("").astype(str).str.lower())
        .groupby(["focal_entity_id", "focal_entity_name"])
        ["classification"]
        .value_counts()
        .unstack(fill_value=0)
        .reset_index()
    )
    pivot["total"] = pivot.drop(columns=["focal_entity_id", "focal_entity_name"]).sum(axis=1)
    pivot = pivot.sort_values("total", ascending=False)

    if nodes is not None and not nodes.empty:
        pivot = pivot.merge(
            nodes[[c for c in ["focal_entity_id", "audit_leader", "business_unit", "line_of_defense"]
                   if c in nodes.columns]],
            on="focal_entity_id",
            how="left",
        )
    return pivot


def _gaps_by_entity(df: pd.DataFrame, gap_value: str) -> pd.DataFrame:
    """One row per likely-coverage-gap finding."""
    gaps = df[df["classification"].str.lower().eq(gap_value.lower())].copy()
    if gaps.empty:
        return gaps
    keep_cols = [
        "batch_id", "task", "task_name", "focal_entity_id", "focal_entity_name",
        "cross_entity_partner_id", "risk_category", "specific_risk_ids",
        "kpa_ids", "evidence_layer", "manual_requirement",
        "evidence_quote", "reasoning", "gate_passed",
    ]
    keep_cols = [c for c in keep_cols if c in gaps.columns]
    return gaps[keep_cols].sort_values(["focal_entity_id", "task"]).reset_index(drop=True)


def _by_attribute(findings: pd.DataFrame, nodes: pd.DataFrame, attr: str) -> pd.DataFrame:
    if attr not in nodes.columns:
        return pd.DataFrame()
    merged = findings.merge(
        nodes[["focal_entity_id", attr]], on="focal_entity_id", how="left"
    )
    pivot = (
        merged.groupby([attr, "classification"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    pivot["total"] = pivot.drop(columns=[attr]).sum(axis=1)
    return pivot.sort_values("total", ascending=False)


def run(
    findings_path: Path = DEFAULT_FINDINGS,
    gate_log_path: Path = DEFAULT_GATE_LOG,
    nodes_path: Path = DEFAULT_NODES,
    out_path: Path = DEFAULT_OUT,
) -> None:
    if not findings_path.exists():
        raise FileNotFoundError(f"findings.csv not found at {findings_path}")
    findings = pd.read_csv(findings_path)
    findings["classification"] = findings["classification"].fillna("").astype(str)

    task_displays = labels.task_displays()
    if "task" in findings.columns:
        findings["task_name"] = findings["task"].map(
            lambda t: task_displays.get(int(t)) if pd.notna(t) and str(t).strip() != "" else ""
        ).fillna("")

    gate_map = _parse_gate_log(gate_log_path)
    if gate_map:
        findings["gate_passed"] = findings["batch_id"].map(gate_map).fillna(False).astype(bool)
    else:
        findings["gate_passed"] = True

    nodes = _load_nodes(nodes_path)

    doc_value = _classification_value("documentation")
    gap_value = _classification_value("coverage gap")
    docs = findings[findings["classification"].str.lower().eq(doc_value.lower())]
    gaps = findings[findings["classification"].str.lower().eq(gap_value.lower())]
    manual = (findings[findings["manual_requirement"].astype(str).str.lower().isin({"true", "1", "yes"})]
              if "manual_requirement" in findings.columns else findings.iloc[0:0])

    sheets: dict[str, pd.DataFrame] = {
        "Summary": _summary_sheet(findings),
        "Gaps by Risk Category": _by_risk_category(gaps),
        "Doc Issues by Risk Category": _by_risk_category(docs),
        "Top Entities by Issue Count": _top_entities(findings, nodes),
        "Gaps by Entity": _gaps_by_entity(findings, gap_value),
        "Manual Requirements": manual.reset_index(drop=True),
    }

    if nodes is not None and not nodes.empty:
        if "audit_leader" in nodes.columns:
            sheets["By Audit Leader"] = _by_attribute(findings, nodes, "audit_leader")
        if "business_unit" in nodes.columns:
            sheets["By Business Unit"] = _by_attribute(findings, nodes, "business_unit")
        if "line_of_defense" in nodes.columns:
            sheets["By Line of Defense"] = _by_attribute(findings, nodes, "line_of_defense")

    sheets["All Findings (Tagged)"] = findings

    write_workbook(out_path, sheets)
    print(f"[summarize] wrote {out_path}")
    print(f"  total findings:    {len(findings)}")
    print(f"  likely gaps:       {len(gaps)}")
    print(f"  documentation:     {len(docs)}")
    print(f"  manual flagged:    {len(manual)}")
    if gate_map:
        passed = int(findings["gate_passed"].sum())
        failed = len(findings) - passed
        print(f"  from passed gates: {passed}")
        print(f"  from failed gates: {failed}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--findings", type=Path, default=DEFAULT_FINDINGS)
    parser.add_argument("--gate-log", type=Path, default=DEFAULT_GATE_LOG)
    parser.add_argument("--nodes", type=Path, default=DEFAULT_NODES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    run(args.findings, args.gate_log, args.nodes, args.out)


if __name__ == "__main__":
    main()
