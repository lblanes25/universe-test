"""Direction-aware batch payload builders.

Three payload sections per batch:
  - focal: full schema (overview, handoff prose, 14-category ratings+prose, all controls, SR/KPA rollups)
  - target_context: handoff targets (B in A->B where A focal). Richer: ratings + compact controls + SR/KPA rollups.
  - source_context: handoff sources (C in C->A where A focal). Lean: ID, name, handoff prose, structured handoffs.

Focal-in-same-batch entities are not duplicated as context. The focal payload serves both roles.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
COLUMN_MAPPINGS = ROOT / "config" / "column_mappings.json"


def _load_column_mappings() -> dict:
    return json.loads(COLUMN_MAPPINGS.read_text(encoding="utf-8"))


_COLS = _load_column_mappings()


def _col(key: str):
    return _COLS[key]


def _risk_fields(risk_name: str) -> tuple[str, str, str, str, str]:
    """Return column names for rating triples + rationale prose columns.

    Real data (confirmed 2026-04-20): 11 of 14 categories carry inherent-risk
    rationale and control-assessment rationale prose; the 3 exceptions
    (Information Security, Information Technology, Third Party) carry only
    ratings. Missing prose columns are read as empty strings silently so
    Task 2's conditional-rationale handling kicks in without crashes.

    Dummy data carries only the three rating columns. Same degradation path.
    """
    residual = f"{risk_name}{_COLS['risk_residual_suffix']}"
    inherent_rating = f"{risk_name}{_COLS['risk_inherent_suffix']}"
    control_rating = f"{risk_name}{_COLS['risk_control_suffix']}"
    inherent_rationale = f"{risk_name} Inherent Risk Rationale"
    control_prose = f"{risk_name} Control Assessment Rationale"
    return residual, inherent_rating, control_rating, inherent_rationale, control_prose


def _split_ids(value) -> list[str]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    s = str(value).strip()
    if not s or s.lower() == "nan":
        return []
    return [p.strip() for p in s.split(";") if p.strip()]


def _resolve_partner_ids(ids: list[str], name_by_id: dict[str, str], active_ids: set[str]) -> list[dict]:
    """Resolve a list of AE IDs to {id, name, inactive_flag} records.

    name_by_id carries all referenceable entities (focal-eligible plus inactive
    of focal types). If a pid isn't in the map, it's a dropped-type or a
    genuinely unknown ID — surface as "(out of scope)" so the model can
    distinguish from inactive-but-named referenceable entities.

    active_ids carries focal-eligible IDs only. inactive_flag is True for any
    partner that is not focal-eligible (inactive-referenceable OR dropped).
    """
    return [
        {
            "id": pid,
            "name": name_by_id.get(pid, "(out of scope)"),
            "inactive_flag": pid not in active_ids,
        }
        for pid in ids
    ]


def _risk_rows_for_entity(
    entity_row: pd.Series,
    applicable_only: bool = True,
) -> list[dict]:
    def clean(v):
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return ""
        return str(v).strip()

    rows: list[dict] = []
    for risk in _COLS["risks"]:
        residual_c, inherent_rating_c, control_rating_c, inherent_rationale_c, control_prose_c = _risk_fields(risk)
        residual_v = clean(entity_row.get(residual_c))
        if applicable_only and (residual_v == "" or residual_v == "Not Applicable"):
            continue
        rows.append(
            {
                "risk_category": risk,
                "residual_rating": residual_v,
                "inherent_rating": clean(entity_row.get(inherent_rating_c)),
                "inherent_rationale": clean(entity_row.get(inherent_rationale_c)),  # empty in dummy
                "control_assessment_rating": clean(entity_row.get(control_rating_c)),
                "control_assessment_prose": clean(entity_row.get(control_prose_c)),  # empty in dummy
            }
        )
    return rows


_CONTROLS_ENTITY_COL = "Audit Entity (Audit Controls)"  # Archer export header
_CONTROLS_KEY_RISK_ID_COL = "Key Risk ID"               # Archer export header; maps to payload field specific_risk_id
_CONTROLS_KEY_RISK_DESC_COL = "Key Risk Description"    # Archer export header; maps to payload field specific_risk_description


def _control_records_for_entity(
    entity_id: str,
    controls_df: pd.DataFrame,
    include_description: bool,
    description_max_chars: int | None = None,
) -> list[dict]:
    """Read controls for an entity. Archer column names differ from internal
    payload field names: "Key Risk ID/Description" in the CSV maps to the
    "specific_risk_id/description" payload field we've used throughout docs
    and prompt. The conceptual name stays "Specific Risk" everywhere the
    model sees.

    If include_description is True and description_max_chars is set, the
    Control Description is hard-truncated to that many characters. KPA
    Description and Specific Risk Description are never truncated — they
    are compact and carry the primary evidence layer.
    """
    if controls_df.empty:
        return []
    sub = controls_df[controls_df[_CONTROLS_ENTITY_COL] == entity_id]
    out: list[dict] = []
    for _, r in sub.iterrows():
        rec = {
            "control_id": str(r.get("Control ID", "")).strip(),
            "control_title": str(r.get("Control Title", "")).strip(),
            "kpa_id": str(r.get("KPA ID", "")).strip(),
            "kpa_description": str(r.get("KPA Description", "")).strip(),
            "specific_risk_id": str(r.get(_CONTROLS_KEY_RISK_ID_COL, "")).strip(),
            "specific_risk_description": str(r.get(_CONTROLS_KEY_RISK_DESC_COL, "")).strip(),
        }
        if include_description:
            desc = str(r.get("Control Description", "")).strip()
            if description_max_chars is not None and len(desc) > description_max_chars:
                desc = desc[:description_max_chars]
            rec["control_description"] = desc
        out.append(rec)
    return out


def _coverage_rollup(controls: list[dict], id_key: str, desc_key: str) -> list[dict]:
    seen: dict[str, str] = {}
    for c in controls:
        cid = c.get(id_key, "")
        if not cid or cid in seen:
            continue
        seen[cid] = c.get(desc_key, "")
    return [{"id": k, "description": v} for k, v in seen.items()]


def _entity_header(row: pd.Series) -> dict:
    def clean(v):
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return ""
        return str(v).strip()
    return {
        "entity_id": clean(row.get(_col("entity_id"))),
        "entity_name": clean(row.get(_col("entity_name"))),
        "business_unit": clean(row.get(_col("business_unit"))),
        "line_of_defense": clean(row.get(_col("line_of_defense"))),
    }


def build_focal_payload(
    row: pd.Series,
    controls_df: pd.DataFrame,
    name_by_id: dict[str, str],
    active_ids: set[str],
    horizontal_flag: bool,
    include_control_description: bool = True,
    control_description_max_chars: int | None = None,
) -> dict:
    header = _entity_header(row)
    controls = _control_records_for_entity(
        header["entity_id"],
        controls_df,
        include_description=include_control_description,
        description_max_chars=control_description_max_chars,
    )
    return {
        **header,
        "horizontal_flag": horizontal_flag,
        "overview": str(row.get("Audit Entity Overview", "") or "").strip(),
        "handoff_description": str(row.get("Hand-off Description", "") or "").strip(),
        "handoffs_to": _resolve_partner_ids(_split_ids(row.get(_col("handoff_to"))), name_by_id, active_ids),
        "handoffs_from": _resolve_partner_ids(_split_ids(row.get(_col("handoff_from"))), name_by_id, active_ids),
        "risks": _risk_rows_for_entity(row, applicable_only=True),
        "controls": controls,
        "specific_risk_coverage": _coverage_rollup(controls, "specific_risk_id", "specific_risk_description"),
        "kpa_coverage": _coverage_rollup(controls, "kpa_id", "kpa_description"),
    }


def build_target_context_payload(
    row: pd.Series,
    controls_df: pd.DataFrame,
    name_by_id: dict[str, str],
    active_ids: set[str],
    horizontal_flag: bool,
    include_control_description: bool = False,
) -> dict:
    header = _entity_header(row)
    controls = _control_records_for_entity(header["entity_id"], controls_df, include_description=include_control_description)
    return {
        **header,
        "role": "target_context",
        "horizontal_flag": horizontal_flag,
        "handoff_description": str(row.get("Hand-off Description", "") or "").strip(),
        "handoffs_to": _resolve_partner_ids(_split_ids(row.get(_col("handoff_to"))), name_by_id, active_ids),
        "handoffs_from": _resolve_partner_ids(_split_ids(row.get(_col("handoff_from"))), name_by_id, active_ids),
        "risks": _risk_rows_for_entity(row, applicable_only=False),
        "controls_compact": controls,
        "specific_risk_coverage": _coverage_rollup(controls, "specific_risk_id", "specific_risk_description"),
        "kpa_coverage": _coverage_rollup(controls, "kpa_id", "kpa_description"),
    }


def build_source_context_payload(
    row: pd.Series,
    name_by_id: dict[str, str],
    active_ids: set[str],
) -> dict:
    header = _entity_header(row)
    return {
        "entity_id": header["entity_id"],
        "entity_name": header["entity_name"],
        "role": "source_context",
        "handoff_description": str(row.get("Hand-off Description", "") or "").strip(),
        "handoffs_to": _resolve_partner_ids(_split_ids(row.get(_col("handoff_to"))), name_by_id, active_ids),
    }


def partition_context(
    focal_ids: Iterable[str],
    entity_rows: dict[str, pd.Series],
) -> tuple[set[str], set[str]]:
    """Return (target_ids, source_ids) for entities outside focal_ids.

    - Target context = every entity B such that some focal A has B in handoffs_to OR some entity C has C->A meaning we also get B from A's handoffs_from? No — only A->B targets go to target context.
    - Source context = every entity C such that some focal A has C in handoffs_from (C->A).
    A bidirectional partner (both target and source) is resolved to target (richer payload wins).
    """
    focal_set = set(focal_ids)
    targets: set[str] = set()
    sources: set[str] = set()
    for eid in focal_set:
        row = entity_rows.get(eid)
        if row is None:
            continue
        for pid in _split_ids(row.get(_col("handoff_to"))):
            if pid not in focal_set:
                targets.add(pid)
        for pid in _split_ids(row.get(_col("handoff_from"))):
            if pid not in focal_set:
                sources.add(pid)
    sources = sources - targets  # target payload is a superset; avoid duplication
    return targets, sources
