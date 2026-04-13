"""Stage 5: dependency lookups, entity profile, concentration flags."""
from __future__ import annotations

import pandas as pd

CONCENTRATION_THRESHOLD = 10


def _asset_lookup(
    table: pd.DataFrame,
    asset_col: str,
    asset_type: str,
    nodes: pd.DataFrame,
) -> pd.DataFrame:
    if table.empty:
        return pd.DataFrame(
            columns=[
                "Asset Name",
                "Asset Type",
                "Dependent Entity Count",
                "Primary Count",
                "Secondary Count",
                "Dependent Entity IDs",
                "Business Units",
            ]
        )
    has_rel = "Relationship" in table.columns
    bu_map = dict(zip(nodes["Audit Entity ID"], nodes.get("Business Unit", pd.Series(dtype=object))))
    rows = []
    for name, grp in table.groupby(asset_col):
        ents = sorted(grp["Audit Entity ID"].unique())
        primary = int((grp["Relationship"] == "primary").sum()) if has_rel else 0
        secondary = int((grp["Relationship"] == "secondary").sum()) if has_rel else 0
        bus = sorted({bu_map.get(e) for e in ents if bu_map.get(e)})
        rows.append(
            {
                "Asset Name": name,
                "Asset Type": asset_type,
                "Dependent Entity Count": len(ents),
                "Primary Count": primary,
                "Secondary Count": secondary,
                "Dependent Entity IDs": ";".join(ents),
                "Business Units": ";".join(bus),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["Dependent Entity Count"], ascending=False
    ).reset_index(drop=True)


def build_asset_dependency_lookup(
    entity_app: pd.DataFrame,
    entity_vendor: pd.DataFrame,
    entity_model: pd.DataFrame,
    nodes: pd.DataFrame,
) -> pd.DataFrame:
    app = _asset_lookup(entity_app, "Application Name", "Application", nodes)
    vendor = _asset_lookup(entity_vendor, "Third Party Name", "Vendor", nodes)
    model = _asset_lookup(entity_model, "Model Name", "Model", nodes)
    return pd.concat([app, vendor, model], ignore_index=True)


def build_entity_profile(
    nodes: pd.DataFrame,
    handoffs: pd.DataFrame,
    entity_app: pd.DataFrame,
    entity_vendor: pd.DataFrame,
    entity_model: pd.DataFrame,
    entity_prsa: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    for ent in nodes["Audit Entity ID"]:
        ho_to = handoffs[(handoffs["Direction"] == "to") & (handoffs["Source Entity ID"] == ent)]
        ho_from = handoffs[(handoffs["Direction"] == "from") & (handoffs["Target Entity ID"] == ent)]
        partners = sorted(
            set(ho_to["Target Entity ID"]).union(ho_from["Source Entity ID"])
        )
        prim_app = int(
            ((entity_app["Audit Entity ID"] == ent) & (entity_app.get("Relationship") == "primary")).sum()
        ) if not entity_app.empty else 0
        sec_app = int(
            ((entity_app["Audit Entity ID"] == ent) & (entity_app.get("Relationship") == "secondary")).sum()
        ) if not entity_app.empty else 0
        prim_v = int(
            ((entity_vendor["Audit Entity ID"] == ent) & (entity_vendor.get("Relationship") == "primary")).sum()
        ) if not entity_vendor.empty else 0
        sec_v = int(
            ((entity_vendor["Audit Entity ID"] == ent) & (entity_vendor.get("Relationship") == "secondary")).sum()
        ) if not entity_vendor.empty else 0
        model_c = int((entity_model["Audit Entity ID"] == ent).sum()) if not entity_model.empty else 0
        prsa_c = int((entity_prsa["Audit Entity ID"] == ent).sum()) if not entity_prsa.empty else 0
        handoff_to_c = len(ho_to)
        handoff_from_c = len(ho_from)
        total = handoff_to_c + handoff_from_c + prim_app + sec_app + prim_v + sec_v + model_c + prsa_c
        rows.append(
            {
                "Audit Entity ID": ent,
                "Handoff To Count": handoff_to_c,
                "Handoff From Count": handoff_from_c,
                "Primary App Count": prim_app,
                "Secondary App Count": sec_app,
                "Primary Vendor Count": prim_v,
                "Secondary Vendor Count": sec_v,
                "Model Count": model_c,
                "PRSA Count": prsa_c,
                "Total Connection Count": total,
                "Handoff Partner IDs": ";".join(partners),
            }
        )
    return pd.DataFrame(rows).sort_values("Total Connection Count", ascending=False).reset_index(drop=True)


def build_concentration_flags(lookup: pd.DataFrame) -> pd.DataFrame:
    if lookup.empty:
        return lookup.copy()
    return lookup[lookup["Dependent Entity Count"] >= CONCENTRATION_THRESHOLD].copy().reset_index(drop=True)
