"""Stage 1: filter rows to active standard audit entities."""
from __future__ import annotations

import pandas as pd

SPECIAL_REVIEW_TYPES = {"Special Review", "Advisory", "Consulting", "Continuous Monitoring"}


def filter_entities(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    type_mask = df["Audit Entity Type"].isin(SPECIAL_REVIEW_TYPES) | (
        df["Audit Entity Type"].str.lower() != "audit"
    )
    status_mask = df["Audit Entity Status"] != "Active"

    removed_type = df[type_mask & ~status_mask]
    removed_status = df[status_mask & ~type_mask]
    removed_both = df[type_mask & status_mask]
    removed = df[type_mask | status_mask]
    remaining = df[~(type_mask | status_mask)].reset_index(drop=True)

    log_rows = []
    for _, row in removed.iterrows():
        reasons = []
        if row["Audit Entity Type"] != "Audit":
            reasons.append(f"type={row['Audit Entity Type']}")
        if row["Audit Entity Status"] != "Active":
            reasons.append(f"status={row['Audit Entity Status']}")
        log_rows.append(
            {
                "Audit Entity ID": row["Audit Entity ID"],
                "Audit Entity Name": row["Audit Entity Name"],
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
