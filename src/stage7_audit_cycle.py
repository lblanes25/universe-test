"""Stage 7: audit cycle summary (effective frequency, overdue)."""
from __future__ import annotations

from datetime import date, datetime

import pandas as pd

from src.utils.columns import col

FREQ_DAYS = {
    "1 Year": 365,
    "1.5 Years": 548,
    "2 Years": 730,
    "3 Years": 1095,
    "4 Years": 1460,
    "5 Years": 1825,
}
UNKNOWN_VALUES = {"", "not applicable", "n/a", "na", "nan", "none"}


def _parse_date(val) -> date | None:
    if val is None:
        return None
    s = str(val).strip()
    if not s or s.lower() in UNKNOWN_VALUES:
        return None
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%m-%d-%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def _effective_frequency(row, q_col: str, v_col: str, min_col: str) -> str:
    override_q = str(row.get(q_col, "")).strip()
    override_v = str(row.get(v_col, "")).strip()
    min_f = str(row.get(min_col, "")).strip()
    if override_q.lower() == "yes" and override_v and override_v.lower() not in UNKNOWN_VALUES:
        return override_v
    return min_f


def build_audit_cycle(df: pd.DataFrame, today: date | None = None) -> pd.DataFrame:
    today = today or date.today()
    id_col = col("entity_id")
    name_col = col("entity_name")
    q_col = col("override_question")
    v_col = col("override_value")
    min_col = col("min_audit_frequency")
    last_col = col("last_audit_date")
    rows = []
    for _, row in df.iterrows():
        eff = _effective_frequency(row, q_col, v_col, min_col)
        last = _parse_date(row.get(last_col))
        days_since = (today - last).days if last else None
        freq_days = FREQ_DAYS.get(eff)
        if freq_days is None or last is None:
            overdue = "Unknown"
        elif days_since is not None and days_since > freq_days:
            overdue = "Yes"
        else:
            overdue = "No"
        rows.append(
            {
                "Audit Entity ID": row[id_col],
                "Audit Entity Name": row.get(name_col),
                "Effective Frequency": eff,
                "Last Audit Date": last.isoformat() if last else "",
                "Days Since Last Audit": days_since if days_since is not None else "",
                "Overdue Flag": overdue,
                "Frequency Overridden": str(row.get(q_col, "")).strip() == "Yes",
            }
        )
    return pd.DataFrame(rows)
