"""Stage 3: risk map — one row per entity-risk where risk is applicable."""
from __future__ import annotations

import pandas as pd

RISKS = [
    "Compliance",
    "Country",
    "Credit",
    "External Fraud",
    "Financial Reporting",
    "Funding & Liquidity",
    "Information Technology",
    "Information Security",
    "Model",
    "Market",
    "Operational",
    "Reputational",
    "Strategic & Business",
    "Third Party",
]

NOT_APPLICABLE = {"not applicable", "n/a", "na", ""}


def _is_applicable(v) -> bool:
    if v is None:
        return False
    s = str(v).strip().lower()
    if s in NOT_APPLICABLE or s == "nan":
        return False
    return True


def build_risk_map(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in df.iterrows():
        ent = row["Audit Entity ID"]
        for risk in RISKS:
            inh = row.get(f"{risk} Inherent Risk")
            res = row.get(f"{risk} Residual Risk")
            ctrl = row.get(f"{risk} Control Assessment")
            if _is_applicable(res):
                rows.append(
                    {
                        "Audit Entity ID": ent,
                        "Risk Name": risk,
                        "Inherent Risk Rating": inh,
                        "Residual Risk Rating": res,
                        "Control Assessment Rating": ctrl,
                    }
                )
    return pd.DataFrame(rows)
