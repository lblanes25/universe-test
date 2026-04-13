"""Stage 2: build Node table.

Output columns are canonical internal names. Raw CSV headers are looked up
through :mod:`src.utils.columns` and renamed so downstream stages never
touch source-system naming.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.utils.columns import col, resolve

# Canonical internal name -> config key for the raw CSV column.
IDENTITY_MAP: dict[str, str] = {
    "Audit Entity ID": "entity_id",
    "Audit Entity Name": "entity_name",
    "Audit Entity Type": "entity_type",
    "Audit Entity Status": "entity_status",
    "Business Unit": "business_unit",
    "Line of Defense": "line_of_defense",
    "Subsidiary Bank": "subsidiary_bank",
    "Core Audit Team": "core_audit_team",
    "Integrated Team": "integrated_team",
    "Audit Leader": "audit_leader",
    "PGA/ASL": "pga_asl",
}


def _horizontal_flag(name: str, keywords: list[str]) -> str:
    n = (name or "").lower()
    for kw in keywords:
        if kw.lower() in n:
            return "horizontal"
    return "vertical"


def build_nodes(df: pd.DataFrame, keywords_path: Path) -> pd.DataFrame:
    keywords = json.loads(Path(keywords_path).read_text(encoding="utf-8"))

    nodes = pd.DataFrame()
    for internal, key in IDENTITY_MAP.items():
        raw = col(key)
        if raw in df.columns:
            nodes[internal] = df[raw].values

    nodes["Horizontal Flag"] = nodes["Audit Entity Name"].apply(
        lambda n: _horizontal_flag(n, keywords)
    )

    inh_src = resolve(df, "overall_inherent_risk")
    nodes["Overall Inherent Risk Rating"] = df[inh_src].values if inh_src else None
    res_src = resolve(df, "overall_residual_risk")
    nodes["Overall Residual Risk Rating"] = df[res_src].values if res_src else None
    return nodes
