"""Stage 1: filter rows to active standard audit entities."""
from __future__ import annotations

import pandas as pd

from src.utils.columns import col

SPECIAL_REVIEW_TYPES = {"Special Review", "Advisory", "Consulting", "Continuous Monitoring"}


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
