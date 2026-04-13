"""Stage 2: build Node table."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

IDENTITY_COLS = [
    "Audit Entity ID",
    "Audit Entity Name",
    "Audit Entity Type",
    "Audit Entity Status",
    "Business Unit",
    "Line of Defense",
    "Subsidiary Bank",
    "Core Audit Team",
    "Integrated Team",
    "Audit Leader",
    "PGA/ASL",
]

OVERALL_COLS_CANDIDATES = [
    ("Overall Inherent Risk Rating", ["Overall Inherent Risk", "Overall Inherent Risk Rating"]),
    ("Overall Residual Risk Rating", ["Overall Residual Risk", "Overall Residual Risk Rating"]),
]


def _horizontal_flag(name: str, keywords: list[str]) -> str:
    n = (name or "").lower()
    for kw in keywords:
        if kw.lower() in n:
            return "horizontal"
    return "vertical"


def build_nodes(df: pd.DataFrame, keywords_path: Path) -> pd.DataFrame:
    keywords = json.loads(Path(keywords_path).read_text(encoding="utf-8"))
    cols = [c for c in IDENTITY_COLS if c in df.columns]
    nodes = df[cols].copy()
    nodes["Horizontal Flag"] = nodes["Audit Entity Name"].apply(
        lambda n: _horizontal_flag(n, keywords)
    )
    for out_name, candidates in OVERALL_COLS_CANDIDATES:
        for c in candidates:
            if c in df.columns:
                nodes[out_name] = df[c].values
                break
        else:
            nodes[out_name] = None
    return nodes
