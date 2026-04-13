"""Stage 4: relational tables from semicolon-delimited columns."""
from __future__ import annotations

import pandas as pd

from src.utils.columns import col
from src.utils.standardization import (
    normalize_policy_id,
    split_multi,
    standardize_names,
)


def _c(key: str) -> str:
    return col(key)  # raw CSV header for the given logical field


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
    src_col: str,
    mapping: dict[str, str],
    relationship: str | None,
    out_col: str,
) -> pd.DataFrame:
    if src_col not in df.columns:
        return pd.DataFrame()
    id_col = _c("entity_id")
    rows = []
    for _, row in df.iterrows():
        ent = row[id_col]
        for raw in split_multi(row.get(src_col)):
            std = mapping.get(raw, raw)
            record = {"Audit Entity ID": ent, out_col: std}
            if relationship is not None:
                record["Relationship"] = relationship
            rows.append(record)
    return pd.DataFrame(rows)


def build_handoffs(df: pd.DataFrame, node_ids: set[str]) -> pd.DataFrame:
    id_col = _c("entity_id")
    to_col = _c("handoff_to")
    from_col = _c("handoff_from")
    rows = []
    for _, row in df.iterrows():
        src = row[id_col]
        for tgt in split_multi(row.get(to_col)):
            rows.append(
                {
                    "Source Entity ID": src,
                    "Target Entity ID": tgt,
                    "Direction": "to",
                    "Unmatched": tgt not in node_ids,
                }
            )
        for origin in split_multi(row.get(from_col)):
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
    p, s = _c("primary_app"), _c("secondary_app")
    mapping = _standardize_column(df, [p, s], log, "Entity-Application")
    prim = _explode(df, p, mapping, "primary", "Application Name")
    sec = _explode(df, s, mapping, "secondary", "Application Name")
    out = pd.concat([prim, sec], ignore_index=True) if len(prim) or len(sec) else pd.DataFrame(
        columns=["Audit Entity ID", "Application Name", "Relationship"]
    )
    return out, mapping


def build_entity_vendor(df: pd.DataFrame, log: list) -> tuple[pd.DataFrame, dict]:
    p, s = _c("primary_vendor"), _c("secondary_vendor")
    mapping = _standardize_column(df, [p, s], log, "Entity-Vendor")
    prim = _explode(df, p, mapping, "primary", "Third Party Name")
    sec = _explode(df, s, mapping, "secondary", "Third Party Name")
    out = pd.concat([prim, sec], ignore_index=True) if len(prim) or len(sec) else pd.DataFrame(
        columns=["Audit Entity ID", "Third Party Name", "Relationship"]
    )
    return out, mapping


def build_entity_model(df: pd.DataFrame, log: list) -> tuple[pd.DataFrame, dict]:
    m = _c("models")
    mapping = _standardize_column(df, [m], log, "Entity-Model")
    out = _explode(df, m, mapping, None, "Model Name")
    if out.empty:
        out = pd.DataFrame(columns=["Audit Entity ID", "Model Name"])
    return out, mapping


def build_entity_prsa(df: pd.DataFrame, log: list) -> tuple[pd.DataFrame, dict]:
    p = _c("prsa")
    mapping = _standardize_column(df, [p], log, "Entity-PRSA")
    out = _explode(df, p, mapping, None, "PRSA Value")
    if out.empty:
        out = pd.DataFrame(columns=["Audit Entity ID", "PRSA Value"])
    return out, mapping


def build_entity_policy(df: pd.DataFrame, log: list) -> pd.DataFrame:
    policy_col = _c("policies")
    id_col = _c("entity_id")
    if policy_col not in df.columns:
        return pd.DataFrame(columns=["Audit Entity ID", "Policy/Standard ID"])
    rows = []
    seen: dict[str, str] = {}
    for _, row in df.iterrows():
        ent = row[id_col]
        for raw in split_multi(row.get(policy_col)):
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
