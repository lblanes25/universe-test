"""Stage 1: filter rows to active standard audit entities.

Two public entry points:
  - filter_entities: used by the existing layer 1/2 pipeline. Returns a single
    active-entities DataFrame plus removal stats. Behavior unchanged.
  - classify_entities: used by Stage 2 handoff review. Returns two DataFrames
    (focal-eligible and referenceable) plus classification stats. Inactive
    entities of focal types remain in the referenceable set so handoff
    references to them resolve with names and inactive_flag signals.
"""
from __future__ import annotations

import pandas as pd

from src.utils.columns import col

SPECIAL_REVIEW_TYPES = {"Special Review", "Advisory", "Consulting", "Continuous Monitoring"}

# Stage 2 classification sets. Kept here (not in classify_entities body) so
# they're importable by tests or callers that want to inspect scope.
STAGE2_FOCAL_TYPES = {
    "Audit",
    "Data Driven Continuous Audit - In Cycle",
    "Data Driven Continuous Audit - New",
    "Special Review",
    "Special Review - Hybrid Assurance & Advisory",
    "Special Review - Assurance (Rated)",
    "Special Review - Advisory",
    "Special Review - Assurance (Non-Rated)",
}
STAGE2_DROPPED_TYPES = {
    "Regulatory Project",
    "Business Monitoring",
    "Investigation",
}


def filter_entities(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    type_col = col("entity_type")
    status_col = col("entity_status")
    id_col = col("entity_id")
    name_col = col("entity_name")

    type_mask = df[type_col].isin(SPECIAL_REVIEW_TYPES) | (
        df[type_col].str.lower() != "audit"
    )
    status_mask = df[status_col] != "Active"

    removed_type = df[type_mask & ~status_mask]
    removed_status = df[status_mask & ~type_mask]
    removed_both = df[type_mask & status_mask]
    removed = df[type_mask | status_mask]
    remaining = df[~(type_mask | status_mask)].reset_index(drop=True)

    log_rows = []
    for _, row in removed.iterrows():
        reasons = []
        if row[type_col] != "Audit":
            reasons.append(f"type={row[type_col]}")
        if row[status_col] != "Active":
            reasons.append(f"status={row[status_col]}")
        log_rows.append(
            {
                "Audit Entity ID": row[id_col],
                "Audit Entity Name": row[name_col],
                "Removal Reason": "; ".join(reasons),
            }
        )

    stats = {
        "removed_type_only": int(len(removed_type)),
        "removed_status_only": int(len(removed_status)),
        "removed_both": int(len(removed_both)),
        "removed_total": int(len(removed)),
        "remaining": int(len(remaining)),
        "removed_log": pd.DataFrame(log_rows),
    }
    return remaining, stats


def classify_entities(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Split entities into focal-eligible and referenceable sets for Stage 2.

    Focal-eligible: Status == "Active" AND Type in STAGE2_FOCAL_TYPES.
    Referenceable:  Type in STAGE2_FOCAL_TYPES (any status). Superset of focal.
    Dropped:        Everything else (including STAGE2_DROPPED_TYPES explicitly).

    Inactive-referenceable entities stay in the graph as context targets/sources
    so stale-handoff signals surface. Dropped entities are removed entirely;
    handoff references pointing at them become unmatched partner records.

    Returns (focal_df, referenceable_df, stats). focal_df is a subset of
    referenceable_df (by Audit Entity ID).
    """
    type_col = col("entity_type")
    status_col = col("entity_status")

    type_series = df[type_col].fillna("")
    status_series = df[status_col].fillna("")

    in_focal_types = type_series.isin(STAGE2_FOCAL_TYPES)
    is_active = status_series == "Active"

    referenceable = df[in_focal_types].reset_index(drop=True)
    focal = df[in_focal_types & is_active].reset_index(drop=True)
    dropped = df[~in_focal_types]

    stats = {
        "focal_count": int(len(focal)),
        "referenceable_count": int(len(referenceable)),
        "referenceable_only_count": int(len(referenceable) - len(focal)),
        "dropped_count": int(len(dropped)),
        "dropped_by_type": dropped[type_col].fillna("").value_counts().to_dict() if len(dropped) else {},
        "focal_by_type": focal[type_col].value_counts().to_dict() if len(focal) else {},
        "referenceable_by_status": referenceable[status_col].fillna("(blank)").value_counts().to_dict() if len(referenceable) else {},
    }
    return focal, referenceable, stats
