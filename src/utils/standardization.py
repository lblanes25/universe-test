"""Multi-value parsing and name standardization."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable


def load_mappings(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"applications": {}, "vendors": {}, "models": {}, "prsa": {}, "policies": {}}


def split_multi(value) -> list[str]:
    """Split a semicolon-delimited cell into trimmed non-empty values."""
    if value is None:
        return []
    if isinstance(value, float):
        # NaN guard
        try:
            import math
            if math.isnan(value):
                return []
        except Exception:
            pass
    s = str(value).strip()
    if not s or s.lower() == "nan":
        return []
    return [piece.strip() for piece in s.split(";") if piece.strip()]


def _canonical_key(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip()).lower()


def standardize_names(
    raw_values: Iterable[str],
    mapping: dict | None = None,
    log: list | None = None,
    table_name: str = "",
) -> dict[str, str]:
    """Return {raw_value: standardized_value}. Canonical = first-seen form per key."""
    mapping = mapping or {}
    canonical: dict[str, str] = {}
    result: dict[str, str] = {}
    for raw in raw_values:
        if raw in mapping:
            result[raw] = mapping[raw]
            continue
        key = _canonical_key(raw)
        if key not in canonical:
            canonical[key] = raw.strip()
        std = canonical[key]
        if std != raw and log is not None:
            log.append(
                {
                    "table": table_name,
                    "original": raw,
                    "standardized": std,
                    "reason": "whitespace/case normalization",
                }
            )
        result[raw] = std
    return result


POLICY_ID_RE = re.compile(r"^([A-Za-z]+)[\s_]?(\d+)$")


def normalize_policy_id(pid: str) -> str:
    m = POLICY_ID_RE.match(pid.strip())
    if m:
        return f"{m.group(1).upper()}_{m.group(2)}"
    return pid.strip()
