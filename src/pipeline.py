"""Audit universe pipeline entry point.

Usage:
    python -m src.pipeline
    python -m src.pipeline --input data/input/dummy_audit_universe_50.csv --plan data/input/dummy_audit_plan.csv
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.stage1_filter import filter_entities  # noqa: E402
from src.stage2_nodes import build_nodes  # noqa: E402
from src.stage3_risk_map import build_risk_map  # noqa: E402
from src.stage4_relational import (  # noqa: E402
    build_entity_application,
    build_entity_model,
    build_entity_policy,
    build_entity_prsa,
    build_entity_vendor,
    build_handoffs,
)
from src.stage5_lookups import (  # noqa: E402
    build_asset_dependency_lookup,
    build_concentration_flags,
    build_entity_profile,
)
from src.stage6_edges import (  # noqa: E402
    build_master_edges,
    edge_summary,
    high_frequency_values,
)
from src.stage7_audit_cycle import build_audit_cycle  # noqa: E402
from src.stage8_coverage import (  # noqa: E402
    build_concentration_detail,
    build_coverage_flags,
    build_coverage_matrix,
    build_coverage_summary,
)
from src.utils.excel_writer import write_workbook  # noqa: E402

DEFAULT_INPUT = ROOT / "data" / "input" / "dummy_audit_universe_50.csv"
DEFAULT_PLAN = ROOT / "data" / "input" / "dummy_audit_plan.csv"
OUTPUT_DIR = ROOT / "data" / "output"
KEYWORDS = ROOT / "config" / "horizontal_keywords.json"


def _read_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in (".xlsx", ".xlsm", ".xls"):
        return pd.read_excel(path, dtype=str)
    return pd.read_csv(path, dtype=str)


def run(input_path: Path, plan_path: Path, output_dir: Path) -> dict:
    print(f"[pipeline] loading {input_path}")
    df = _read_table(input_path)
    print(f"[pipeline] {len(df)} rows, {len(df.columns)} columns")

    # Stage 1
    active, filter_stats = filter_entities(df)
    print(
        f"[stage1] removed={filter_stats['removed_total']} "
        f"(type_only={filter_stats['removed_type_only']}, "
        f"status_only={filter_stats['removed_status_only']}, "
        f"both={filter_stats['removed_both']}) "
        f"remaining={filter_stats['remaining']}"
    )

    # Stage 2
    nodes = build_nodes(active, KEYWORDS)
    print(f"[stage2] nodes={len(nodes)}")

    # Stage 3
    risk_map = build_risk_map(active)
    print(f"[stage3] risk map rows={len(risk_map)}")

    # Stage 4
    standardization_log: list = []
    node_ids = set(nodes["Audit Entity ID"])
    handoffs = build_handoffs(active, node_ids)
    entity_app, _ = build_entity_application(active, standardization_log)
    entity_vendor, _ = build_entity_vendor(active, standardization_log)
    entity_model, _ = build_entity_model(active, standardization_log)
    entity_prsa, _ = build_entity_prsa(active, standardization_log)
    entity_policy = build_entity_policy(active, standardization_log)
    print(
        f"[stage4] handoffs={len(handoffs)} app={len(entity_app)} vendor={len(entity_vendor)} "
        f"model={len(entity_model)} prsa={len(entity_prsa)} policy={len(entity_policy)}"
    )

    # Stage 5
    asset_lookup = build_asset_dependency_lookup(entity_app, entity_vendor, entity_model, nodes)
    concentration = build_concentration_flags(asset_lookup)
    profile = build_entity_profile(nodes, handoffs, entity_app, entity_vendor, entity_model, entity_prsa)
    print(f"[stage5] concentration_assets={len(concentration)}")

    # Stage 6
    edges = build_master_edges(handoffs, entity_app, entity_vendor, entity_prsa, node_ids)
    esum = edge_summary(edges)
    hf = high_frequency_values(edges)
    print(f"[stage6] edges={len(edges)}")

    # Stage 7
    audit_cycle = build_audit_cycle(active)
    overdue_counts = audit_cycle["Overdue Flag"].value_counts().to_dict()
    print(f"[stage7] overdue counts={overdue_counts}")

    # Stage 8
    plan_ids = _load_plan(plan_path)
    matrix = build_coverage_matrix(nodes, audit_cycle, edges, risk_map, entity_model, profile, plan_ids)
    flags = build_coverage_flags(
        matrix, edges, handoffs, concentration, entity_app, entity_vendor, entity_model, plan_ids
    )
    summary = build_coverage_summary(matrix, flags, concentration)
    conc_detail = build_concentration_detail(
        concentration, entity_app, entity_vendor, entity_model, matrix, plan_ids
    )
    print(f"[stage8] flags={len(flags)} (plan_ids={len(plan_ids)})")

    # --- Distribution sheets
    prsa_dist = (
        entity_prsa.groupby("PRSA Value").size().reset_index(name="Entity Count").sort_values("Entity Count", ascending=False)
        if not entity_prsa.empty
        else pd.DataFrame(columns=["PRSA Value", "Entity Count"])
    )
    policy_dist = (
        entity_policy.groupby("Policy/Standard ID").size().reset_index(name="Entity Count").sort_values("Entity Count", ascending=False)
        if not entity_policy.empty
        else pd.DataFrame(columns=["Policy/Standard ID", "Entity Count"])
    )

    filter_stats_df = pd.DataFrame(
        [
            {"Metric": "removed_type_only", "Value": filter_stats["removed_type_only"]},
            {"Metric": "removed_status_only", "Value": filter_stats["removed_status_only"]},
            {"Metric": "removed_both", "Value": filter_stats["removed_both"]},
            {"Metric": "removed_total", "Value": filter_stats["removed_total"]},
            {"Metric": "remaining", "Value": filter_stats["remaining"]},
        ]
    )
    val_log = pd.DataFrame(standardization_log) if standardization_log else pd.DataFrame(columns=["table", "original", "standardized", "reason"])

    # --- Layer 1 workbook
    layer1_path = output_dir / "layer1_output.xlsx"
    write_workbook(
        layer1_path,
        {
            "Nodes": nodes,
            "Risk Map": risk_map,
            "Handoffs": handoffs,
            "Entity-Application": entity_app,
            "Entity-Vendor": entity_vendor,
            "Entity-Model": entity_model,
            "Entity-PRSA": entity_prsa,
            "Entity-Policy": entity_policy,
            "Asset Dependency Lookup": asset_lookup,
            "Entity Dependency Profile": profile,
            "Concentration Flags": concentration,
            "PRSA & Policy Distribution": pd.concat(
                [
                    prsa_dist.assign(Kind="PRSA").rename(columns={"PRSA Value": "Value"}),
                    policy_dist.assign(Kind="Policy").rename(columns={"Policy/Standard ID": "Value"}),
                ],
                ignore_index=True,
            )
            if (len(prsa_dist) + len(policy_dist))
            else pd.DataFrame(columns=["Value", "Entity Count", "Kind"]),
            "Audit Cycle Summary": audit_cycle,
            "Filter Stats": filter_stats_df,
            "Validation & Stdzn Log": val_log,
            "Removed Entities": filter_stats["removed_log"],
        },
    )
    print(f"[pipeline] wrote {layer1_path}")

    # --- Edge derivation workbook
    edge_path = output_dir / "edge_derivation_output.xlsx"
    write_workbook(
        edge_path,
        {
            "Master Edge List": edges,
            "High Frequency Shared Values": hf if not hf.empty else pd.DataFrame(columns=["Edge Type", "Detail", "Pair Count"]),
            "Summary Statistics": esum,
        },
    )
    print(f"[pipeline] wrote {edge_path}")

    # --- Coverage workbook
    coverage_path = output_dir / "layer2_coverage_matrix.xlsx"
    write_workbook(
        coverage_path,
        {
            "Coverage Matrix": matrix,
            "Coverage Flags": flags,
            "Coverage Summary": summary,
            "Concentration Risk Detail": conc_detail,
        },
    )
    print(f"[pipeline] wrote {coverage_path}")

    return {
        "nodes": nodes,
        "risk_map": risk_map,
        "handoffs": handoffs,
        "entity_app": entity_app,
        "entity_vendor": entity_vendor,
        "entity_model": entity_model,
        "entity_prsa": entity_prsa,
        "entity_policy": entity_policy,
        "asset_lookup": asset_lookup,
        "concentration": concentration,
        "profile": profile,
        "edges": edges,
        "audit_cycle": audit_cycle,
        "coverage_matrix": matrix,
        "coverage_flags": flags,
        "filter_stats": filter_stats,
    }


def _load_plan(plan_path: Path) -> set[str]:
    if not plan_path.exists():
        return set()
    try:
        pdf = _read_table(plan_path)
    except Exception:
        return set(line.strip() for line in plan_path.read_text().splitlines() if line.strip())
    col = pdf.columns[0]
    return set(pdf[col].dropna().astype(str).str.strip()) - {""}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    run(args.input, args.plan, args.output)


if __name__ == "__main__":
    main()
