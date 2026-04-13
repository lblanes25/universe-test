"""Stage 4: relational tables from semicolon-delimited columns."""
from __future__ import annotations

import pandas as pd

from src.utils.standardization import (
    normalize_policy_id,
    split_multi,
    standardize_names,
)

COL_HANDOFF_TO = "Hand-offs to Other Audit Entities"
COL_HANDOFF_FROM = "Hand-offs from Other Audit Entities"
COL_PRIMARY_APP = "PRIMARY IT APPLICATIONS (MAPPED)"
COL_SECONDARY_APP = "SECONDARY IT APPLICATIONS (RELATED OR RELIED ON)"
COL_PRIMARY_VENDOR = "PRIMARY TLM THIRD PARTY ENGAGEMENT"
COL_SECONDARY_VENDOR = "SECONDARY TLM THIRD PARTY ENGAGEMENTS (RELATED)"
COL_MODELS = "Models"
COL_PRSA = "PRSA"
COL_POLICY = "POLICIES/STANDARDS/PROCEDURES"


def _standardize_column(
    df: pd.DataFrame, cols: list[str], log: list, table_name: str
) -> dict[str, str]:
    raw_values: list[str] = []
    for c in cols:
        if c not in df.columns:
            continue
        for v in df[c].dropna():
            raw_values.extend(split_multi(v))
    unique = list(dict.fromkeys(raw_values))
    return standardize_names(unique, log=log, table_name=table_name)


def _explode(
    df: pd.DataFrame,
    col: str,
    mapping: dict[str, str],
    relationship: str | None,
    out_col: str,
) -> pd.DataFrame:
    if col not in df.columns:
        return pd.DataFrame()
    rows = []
    for _, row in df.iterrows():
        ent = row["Audit Entity ID"]
        for raw in split_multi(row.get(col)):
            std = mapping.get(raw, raw)
            record = {"Audit Entity ID": ent, out_col: std}
            if relationship is not None:
                record["Relationship"] = relationship
            rows.append(record)
    return pd.DataFrame(rows)


def build_handoffs(df: pd.DataFrame, node_ids: set[str]) -> pd.DataFrame:
    rows = []
    for _, row in df.iterrows():
        src = row["Audit Entity ID"]
        for tgt in split_multi(row.get(COL_HANDOFF_TO)):
            rows.append(
                {
                    "Source Entity ID": src,
                    "Target Entity ID": tgt,
                    "Direction": "to",
                    "Unmatched": tgt not in node_ids,
                }
            )
        for origin in split_multi(row.get(COL_HANDOFF_FROM)):
            rows.append(
                {
                    "Source Entity ID": origin,
                    "Target Entity ID": src,
                    "Direction": "from",
                    "Unmatched": origin not in node_ids,
                }
            )
    return pd.DataFrame(rows)


def build_entity_application(df: pd.DataFrame, log: list) -> tuple[pd.DataFrame, dict]:
    mapping = _standardize_column(df, [COL_PRIMARY_APP, COL_SECONDARY_APP], log, "Entity-Application")
    prim = _explode(df, COL_PRIMARY_APP, mapping, "primary", "Application Name")
    sec = _explode(df, COL_SECONDARY_APP, mapping, "secondary", "Application Name")
    out = pd.concat([prim, sec], ignore_index=True) if len(prim) or len(sec) else pd.DataFrame(
        columns=["Audit Entity ID", "Application Name", "Relationship"]
    )
    return out, mapping


def build_entity_vendor(df: pd.DataFrame, log: list) -> tuple[pd.DataFrame, dict]:
    mapping = _standardize_column(df, [COL_PRIMARY_VENDOR, COL_SECONDARY_VENDOR], log, "Entity-Vendor")
    prim = _explode(df, COL_PRIMARY_VENDOR, mapping, "primary", "Third Party Name")
    sec = _explode(df, COL_SECONDARY_VENDOR, mapping, "secondary", "Third Party Name")
    out = pd.concat([prim, sec], ignore_index=True) if len(prim) or len(sec) else pd.DataFrame(
        columns=["Audit Entity ID", "Third Party Name", "Relationship"]
    )
    return out, mapping


def build_entity_model(df: pd.DataFrame, log: list) -> tuple[pd.DataFrame, dict]:
    mapping = _standardize_column(df, [COL_MODELS], log, "Entity-Model")
    out = _explode(df, COL_MODELS, mapping, None, "Model Name")
    if out.empty:
        out = pd.DataFrame(columns=["Audit Entity ID", "Model Name"])
    return out, mapping


def build_entity_prsa(df: pd.DataFrame, log: list) -> tuple[pd.DataFrame, dict]:
    mapping = _standardize_column(df, [COL_PRSA], log, "Entity-PRSA")
    out = _explode(df, COL_PRSA, mapping, None, "PRSA Value")
    if out.empty:
        out = pd.DataFrame(columns=["Audit Entity ID", "PRSA Value"])
    return out, mapping


def build_entity_policy(df: pd.DataFrame, log: list) -> pd.DataFrame:
    if COL_POLICY not in df.columns:
        return pd.DataFrame(columns=["Audit Entity ID", "Policy/Standard ID"])
    rows = []
    seen: dict[str, str] = {}
    for _, row in df.iterrows():
        ent = row["Audit Entity ID"]
        for raw in split_multi(row.get(COL_POLICY)):
            norm = normalize_policy_id(raw)
            if raw != norm:
                seen_norm = seen.get(raw)
                if seen_norm != norm:
                    log.append(
                        {
                            "table": "Entity-Policy",
                            "original": raw,
                            "standardized": norm,
                            "reason": "policy ID format normalization",
                        }
                    )
                    seen[raw] = norm
            rows.append({"Audit Entity ID": ent, "Policy/Standard ID": norm})
    return pd.DataFrame(rows)
