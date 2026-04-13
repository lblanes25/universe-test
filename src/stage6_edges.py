"""Stage 6: derive master edge list from handoffs and shared attributes.

Models are deliberately excluded from pairwise edge derivation.
"""
from __future__ import annotations

from itertools import combinations

import pandas as pd

HIGH_FREQ_THRESHOLD = 10


def _shared_edges(
    table: pd.DataFrame,
    attr_col: str,
    edge_type: str,
    concentration_names: set[str],
) -> list[dict]:
    if table.empty:
        return []
    rows: list[dict] = []
    # Deduplicate entity-value before pairing
    dedup = table.drop_duplicates(subset=["Audit Entity ID", attr_col])
    for value, grp in dedup.groupby(attr_col):
        ents = sorted(grp["Audit Entity ID"].unique())
        if len(ents) < 2:
            continue
        high_freq = value in concentration_names
        for a, b in combinations(ents, 2):
            rows.append(
                {
                    "Entity A ID": a,
                    "Entity B ID": b,
                    "Edge Type": edge_type,
                    "Detail": value,
                    "High Frequency Flag": high_freq,
                }
            )
    return rows


def _concentration_set(table: pd.DataFrame, attr_col: str) -> set[str]:
    if table.empty:
        return set()
    counts = table.drop_duplicates(["Audit Entity ID", attr_col]).groupby(attr_col).size()
    return set(counts[counts >= HIGH_FREQ_THRESHOLD].index)


def build_master_edges(
    handoffs: pd.DataFrame,
    entity_app: pd.DataFrame,
    entity_vendor: pd.DataFrame,
    entity_prsa: pd.DataFrame,
    node_ids: set[str],
) -> pd.DataFrame:
    rows: list[dict] = []

    if not handoffs.empty:
        valid = handoffs[
            handoffs["Source Entity ID"].isin(node_ids)
            & handoffs["Target Entity ID"].isin(node_ids)
        ]
        for _, r in valid.iterrows():
            rows.append(
                {
                    "Entity A ID": r["Source Entity ID"],
                    "Entity B ID": r["Target Entity ID"],
                    "Edge Type": f"handoff_{r['Direction']}",
                    "Detail": "",
                    "High Frequency Flag": False,
                }
            )

    app_conc = _concentration_set(entity_app, "Application Name")
    vendor_conc = _concentration_set(entity_vendor, "Third Party Name")
    prsa_conc = _concentration_set(entity_prsa, "PRSA Value")

    rows.extend(_shared_edges(entity_app, "Application Name", "shared_app", app_conc))
    rows.extend(_shared_edges(entity_vendor, "Third Party Name", "shared_vendor", vendor_conc))
    rows.extend(_shared_edges(entity_prsa, "PRSA Value", "shared_prsa", prsa_conc))

    return pd.DataFrame(
        rows,
        columns=["Entity A ID", "Entity B ID", "Edge Type", "Detail", "High Frequency Flag"],
    )


def edge_summary(edges: pd.DataFrame) -> pd.DataFrame:
    if edges.empty:
        return pd.DataFrame({"Edge Type": [], "Count": []})
    counts = edges.groupby("Edge Type").size().reset_index(name="Count")
    total = pd.DataFrame({"Edge Type": ["TOTAL"], "Count": [len(edges)]})
    return pd.concat([counts, total], ignore_index=True)


def high_frequency_values(edges: pd.DataFrame) -> pd.DataFrame:
    if edges.empty:
        return pd.DataFrame()
    hf = edges[edges["High Frequency Flag"]].copy()
    if hf.empty:
        return pd.DataFrame(columns=["Edge Type", "Detail", "Pair Count"])
    return (
        hf.groupby(["Edge Type", "Detail"])
        .size()
        .reset_index(name="Pair Count")
        .sort_values("Pair Count", ascending=False)
        .reset_index(drop=True)
    )
