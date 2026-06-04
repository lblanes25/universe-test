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

from src.utils.columns import RISK_RESIDUAL_SUFFIX, RISKS, col, resolve

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


def collapse_duplicate_entities(df: pd.DataFrame) -> tuple[pd.DataFrame, int, list[str]]:
    """Collapse multiple source rows for the same Audit Entity ID into one row.

    The real Archer export carries an entity once per Business Unit, so a single
    entity can appear as several rows that differ only in Business Unit. Left
    unfolded, that duplication double-counts edges in Stage 4, inflates coverage
    counts, and makes ``cov_idx.loc[eid]`` in the viz return a multi-row frame.

    Folding rule: Business Unit becomes the ``;``-joined set of its distinct
    non-blank values (in first-seen order); every other column takes the first
    non-null value across the duplicate rows. No-op (returns the frame unchanged)
    when there are no duplicate IDs, so single-row-per-entity data (the dummy) is
    untouched.

    Returns ``(collapsed_df, duplicate_rows_collapsed, conflict_ids)`` where
    ``conflict_ids`` lists entities whose duplicate rows held *differing* residual
    risk ratings — a genuine data conflict that "first wins" silently resolves, so
    the caller can surface it for manual review.
    """
    id_col = col("entity_id")
    if id_col not in df.columns or not df[id_col].duplicated().any():
        return df.reset_index(drop=True), 0, []

    bu_col = col("business_unit")
    cols = list(df.columns)
    residual_cols = [f"{r}{RISK_RESIDUAL_SUFFIX}" for r in RISKS
                     if f"{r}{RISK_RESIDUAL_SUFFIX}" in df.columns]
    overall_res = resolve(df, "overall_residual_risk")
    if overall_res and overall_res not in residual_cols:
        residual_cols.append(overall_res)

    def _clean(v) -> str:
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return ""
        return str(v).strip()

    rows, conflicts, dup_count = [], [], 0
    for eid, grp in df.groupby(id_col, sort=False):
        if len(grp) > 1:
            dup_count += len(grp) - 1
        # First non-blank value per column (blank "" and NaN both count as missing).
        first = grp.iloc[0].copy()
        for c in cols:
            first[c] = next((v for v in grp[c] if _clean(v)), first[c])
        if bu_col in grp.columns:
            seen: list[str] = []
            for v in grp[bu_col]:
                s = _clean(v)
                if s and s not in seen:
                    seen.append(s)
            first[bu_col] = "; ".join(seen)
        if len(grp) > 1:
            for c in residual_cols:
                if len({_clean(v) for v in grp[c] if _clean(v)}) > 1:
                    conflicts.append(str(eid))
                    break
        rows.append(first)

    collapsed = pd.DataFrame(rows, columns=cols).reset_index(drop=True)
    return collapsed, dup_count, sorted(set(conflicts))


def filter_entities(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    type_col = col("entity_type")
    status_col = col("entity_status")
    id_col = col("entity_id")
    name_col = col("entity_name")

    type_series = df[type_col].fillna("")
    type_mask = ~type_series.isin(STAGE2_FOCAL_TYPES)
    status_mask = df[status_col] != "Active"

    removed_type = df[type_mask & ~status_mask]
    removed_status = df[status_mask & ~type_mask]
    removed_both = df[type_mask & status_mask]
    removed = df[type_mask | status_mask]
    remaining = df[~(type_mask | status_mask)].reset_index(drop=True)

    # Fold multi-Business-Unit duplicate rows into one row per entity before any
    # downstream stage (nodes, risk map, relational tables, coverage) consumes
    # `remaining`. No-op on single-row-per-entity data (the dummy).
    remaining, dup_collapsed, conflict_ids = collapse_duplicate_entities(remaining)
    if dup_collapsed:
        print(f"[stage1] collapsed {dup_collapsed} duplicate entity row(s) "
              f"into {len(remaining)} unique entities")
        if conflict_ids:
            print(f"[stage1] WARNING: differing residual risk ratings across the "
                  f"duplicate rows of {len(conflict_ids)} entit(ies) — first value "
                  f"kept; verify: {', '.join(conflict_ids)}")

    log_rows = []
    for _, row in removed.iterrows():
        reasons = []
        if row[type_col] not in STAGE2_FOCAL_TYPES:
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
        "duplicate_rows_collapsed": int(dup_collapsed),
        "duplicate_conflict_ids": conflict_ids,
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
    # Fold multi-Business-Unit duplicate rows so a focal entity is never batched
    # twice and context payloads aren't duplicated. Forward-only; resume-safe
    # generation skips already-answered batches.
    df, _, _ = collapse_duplicate_entities(df)

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
