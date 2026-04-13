"""Stage 3: risk map — one row per entity-risk where risk is applicable."""
from __future__ import annotations

import pandas as pd

from src.utils.columns import RISKS, col, risk_cols

NOT_APPLICABLE = {"not applicable", "n/a", "na", ""}


def _is_applicable(v) -> bool:
    if v is None:
        return False
    s = str(v).strip().lower()
    if s in NOT_APPLICABLE or s == "nan":
        return False
    return True


def build_risk_map(df: pd.DataFrame) -> pd.DataFrame:
    id_col = col("entity_id")
    rows = []
    for _, row in df.iterrows():
        ent = row[id_col]
        for risk in RISKS:
            inh_c, res_c, ctrl_c = risk_cols(risk)
            inh = row.get(inh_c)
            res = row.get(res_c)
            ctrl = row.get(ctrl_c)
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
