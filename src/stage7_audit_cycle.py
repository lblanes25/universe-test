"""Stage 7: audit cycle summary (effective frequency, overdue)."""
from __future__ import annotations

from datetime import date, datetime

import pandas as pd

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


def _effective_frequency(row) -> str:
    override_q = str(row.get("Do you want to override the Minimum Audit Frequency?", "")).strip()
    override_v = str(row.get("Override Minimum Audit Frequency", "")).strip()
    min_f = str(row.get("Minimum Audit Frequency", "")).strip()
    if override_q.lower() == "yes" and override_v and override_v.lower() not in UNKNOWN_VALUES:
        return override_v
    return min_f


def build_audit_cycle(df: pd.DataFrame, today: date | None = None) -> pd.DataFrame:
    today = today or date.today()
    rows = []
    for _, row in df.iterrows():
        eff = _effective_frequency(row)
        last = _parse_date(row.get("Last AXP (Most Recent) Audit Report Issued Date"))
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
                "Audit Entity ID": row["Audit Entity ID"],
                "Audit Entity Name": row.get("Audit Entity Name"),
                "Effective Frequency": eff,
                "Last Audit Date": last.isoformat() if last else "",
                "Days Since Last Audit": days_since if days_since is not None else "",
                "Overdue Flag": overdue,
                "Frequency Overridden": str(row.get("Do you want to override the Minimum Audit Frequency?", "")).strip() == "Yes",
            }
        )
    return pd.DataFrame(rows)
