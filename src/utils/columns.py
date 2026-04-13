"""Raw CSV column name lookup.

Loads ``config/column_mappings.json`` once at import time. Pipeline stages
reference source columns through :data:`COL` so the hardcoded Archer-era
headers live in one file. When the source system changes, update the JSON.

Values may be either a string or a list of fallback candidates (first match
against the DataFrame wins — used for fields like "Overall Residual Risk"
that have historically appeared under two names).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd

_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "column_mappings.json"
_raw = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))

COL: dict[str, str | list[str]] = {k: v for k, v in _raw.items() if not k.startswith("_")}

RISKS: list[str] = list(COL.pop("risks"))  # type: ignore[arg-type]
RISK_INHERENT_SUFFIX: str = str(COL.pop("risk_inherent_suffix"))
RISK_RESIDUAL_SUFFIX: str = str(COL.pop("risk_residual_suffix"))
RISK_CONTROL_SUFFIX: str = str(COL.pop("risk_control_suffix"))


def col(key: str) -> str:
    """Return the single canonical column name for ``key``.

    If the mapping is a list (fallback candidates), return the first entry.
    Use :func:`resolve` when you need to pick from candidates against an
    actual DataFrame.
    """
    v = COL[key]
    return v[0] if isinstance(v, list) else v


def candidates(key: str) -> list[str]:
    v = COL[key]
    return list(v) if isinstance(v, list) else [v]


def resolve(df: pd.DataFrame, key: str) -> str | None:
    """Return the first candidate for ``key`` that exists in ``df.columns``."""
    for c in candidates(key):
        if c in df.columns:
            return c
    return None


def risk_cols(risk: str) -> tuple[str, str, str]:
    """Return (inherent, residual, control) column names for a given risk."""
    return (
        f"{risk}{RISK_INHERENT_SUFFIX}",
        f"{risk}{RISK_RESIDUAL_SUFFIX}",
        f"{risk}{RISK_CONTROL_SUFFIX}",
    )


def identity_columns() -> Iterable[str]:
    """Raw CSV columns pulled through to the Nodes table verbatim."""
    keys = [
        "entity_id",
        "entity_name",
        "entity_type",
        "entity_status",
        "business_unit",
        "line_of_defense",
        "subsidiary_bank",
        "core_audit_team",
        "integrated_team",
        "audit_leader",
        "pga_asl",
    ]
    return [col(k) for k in keys]
