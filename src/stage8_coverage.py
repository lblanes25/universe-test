"""Stage 8: coverage matrix + flags (Layer 2)."""
from __future__ import annotations

import pandas as pd

HIGH_CRITICAL = {"High", "Critical"}
WEAK_CONTROLS = {"Insufficiently Controlled"}
CONCENTRATION_THRESHOLD = 10


def _connected_components(entity_ids: list[str], handoff_edges: list[tuple[str, str]]) -> list[set[str]]:
    parent = {e: e for e in entity_ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for a, b in handoff_edges:
        if a in parent and b in parent:
            union(a, b)

    groups: dict[str, set[str]] = {}
    for e in entity_ids:
        r = find(e)
        groups.setdefault(r, set()).add(e)
    return list(groups.values())


def build_coverage_matrix(
    nodes: pd.DataFrame,
    audit_cycle: pd.DataFrame,
    edges: pd.DataFrame,
    risk_map: pd.DataFrame,
    entity_model: pd.DataFrame,
    profile: pd.DataFrame,
    plan_ids: set[str],
) -> pd.DataFrame:
    # Connectivity Total: all edges except shared_model (none exist by design).
    # Count each edge incident to the entity.
    conn_counts: dict[str, int] = {e: 0 for e in nodes["Audit Entity ID"]}
    if not edges.empty:
        for _, row in edges.iterrows():
            a, b = row["Entity A ID"], row["Entity B ID"]
            if a in conn_counts:
                conn_counts[a] += 1
            if b in conn_counts:
                conn_counts[b] += 1

    model_counts = (
        entity_model.groupby("Audit Entity ID").size().to_dict() if not entity_model.empty else {}
    )

    risk_summary: dict[str, dict] = {}
    if not risk_map.empty:
        for ent, grp in risk_map.groupby("Audit Entity ID"):
            hc = grp[grp["Residual Risk Rating"].isin(HIGH_CRITICAL)]
            weak = grp[grp["Control Assessment Rating"].isin(WEAK_CONTROLS)]
            both = grp[
                grp["Residual Risk Rating"].isin(HIGH_CRITICAL)
                & grp["Control Assessment Rating"].isin(WEAK_CONTROLS)
            ]
            rank = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
            highest = grp["Residual Risk Rating"].map(rank).fillna(0).max()
            inv = {v: k for k, v in rank.items()}
            risk_summary[ent] = {
                "High/Critical Count": len(hc),
                "Insufficiently Controlled Count": len(weak),
                "High/Critical + Weak Count": len(both),
                "Highest Residual Risk": inv.get(highest, ""),
                "High/Critical Risks": ";".join(sorted(hc["Risk Name"].tolist())),
            }

    cycle_idx = audit_cycle.set_index("Audit Entity ID") if not audit_cycle.empty else pd.DataFrame()

    rows = []
    for _, n in nodes.iterrows():
        ent = n["Audit Entity ID"]
        rs = risk_summary.get(ent, {})
        in_plan = ent in plan_ids
        cycle = cycle_idx.loc[ent] if ent in cycle_idx.index else {}
        rows.append(
            {
                "Audit Entity ID": ent,
                "Audit Entity Name": n.get("Audit Entity Name"),
                "Business Unit": n.get("Business Unit"),
                "Horizontal Flag": n.get("Horizontal Flag"),
                "Overall Residual Risk": n.get("Overall Residual Risk Rating"),
                "In Scope": "Yes" if in_plan else "No",
                "Effective Frequency": cycle.get("Effective Frequency", "") if isinstance(cycle, pd.Series) else "",
                "Overdue Flag": cycle.get("Overdue Flag", "") if isinstance(cycle, pd.Series) else "",
                "Frequency Overridden": cycle.get("Frequency Overridden", False) if isinstance(cycle, pd.Series) else False,
                "Connectivity Total": conn_counts.get(ent, 0),
                "Model Exposure": model_counts.get(ent, 0),
                "High/Critical Count": rs.get("High/Critical Count", 0),
                "Insufficiently Controlled Count": rs.get("Insufficiently Controlled Count", 0),
                "High/Critical + Weak Count": rs.get("High/Critical + Weak Count", 0),
                "Highest Residual Risk": rs.get("Highest Residual Risk", ""),
                "High/Critical Risks": rs.get("High/Critical Risks", ""),
            }
        )
    return pd.DataFrame(rows)


def build_coverage_flags(
    matrix: pd.DataFrame,
    edges: pd.DataFrame,
    handoffs: pd.DataFrame,
    concentration_flags: pd.DataFrame,
    entity_app: pd.DataFrame,
    entity_vendor: pd.DataFrame,
    entity_model: pd.DataFrame,
    plan_ids: set[str],
) -> pd.DataFrame:
    flags: list[dict] = []
    in_scope = set(matrix[matrix["In Scope"] == "Yes"]["Audit Entity ID"])

    # --- Flag 1: Connected cluster (5+), none in plan
    ent_ids = matrix["Audit Entity ID"].tolist()
    ho_edges = (
        [
            (r["Source Entity ID"], r["Target Entity ID"])
            for _, r in handoffs.iterrows()
            if r["Source Entity ID"] in ent_ids and r["Target Entity ID"] in ent_ids
        ]
        if not handoffs.empty
        else []
    )
    for comp in _connected_components(ent_ids, ho_edges):
        if len(comp) >= 5 and not comp & plan_ids:
            flags.append(
                {
                    "Flag Type": "COVERAGE GAP — CONNECTED CLUSTER",
                    "Priority": "HIGH",
                    "Subject": ";".join(sorted(comp)),
                    "Detail": f"{len(comp)} connected entities, none in plan",
                }
            )

    # --- Flag 2: Overdue + top quartile connectivity
    if not matrix.empty:
        q = matrix["Connectivity Total"].quantile(0.75)
        f2 = matrix[(matrix["Overdue Flag"] == "Yes") & (matrix["Connectivity Total"] >= q)]
        for _, r in f2.iterrows():
            flags.append(
                {
                    "Flag Type": "OVERDUE + HIGHLY CONNECTED",
                    "Priority": "HIGH",
                    "Subject": r["Audit Entity ID"],
                    "Detail": f"Connectivity={r['Connectivity Total']}, overdue",
                }
            )

    # --- Flag 3: Concentration asset with zero coverage
    if not concentration_flags.empty:
        for _, asset in concentration_flags.iterrows():
            dep_ids = set(asset["Dependent Entity IDs"].split(";")) if asset["Dependent Entity IDs"] else set()
            if not dep_ids & plan_ids:
                flags.append(
                    {
                        "Flag Type": "CONCENTRATION ASSET — ZERO COVERAGE",
                        "Priority": "HIGH",
                        "Subject": f"{asset['Asset Type']}: {asset['Asset Name']}",
                        "Detail": f"{asset['Dependent Entity Count']} dependents, none in plan",
                    }
                )

    # --- Flag 4: Primary control owner for concentration asset not in plan
    if not concentration_flags.empty:
        for _, asset in concentration_flags.iterrows():
            if asset["Asset Type"] == "Application":
                tbl, col = entity_app, "Application Name"
            elif asset["Asset Type"] == "Vendor":
                tbl, col = entity_vendor, "Third Party Name"
            else:
                tbl, col = entity_model, "Model Name"
            if tbl.empty or "Relationship" not in tbl.columns:
                continue
            prim = tbl[(tbl[col] == asset["Asset Name"]) & (tbl["Relationship"] == "primary")]
            for primary_ent in prim["Audit Entity ID"].unique():
                if primary_ent not in plan_ids:
                    flags.append(
                        {
                            "Flag Type": "PRIMARY CONTROL OWNER NOT IN PLAN",
                            "Priority": "HIGH",
                            "Subject": primary_ent,
                            "Detail": f"Primary owner of {asset['Asset Type']} '{asset['Asset Name']}' ({asset['Dependent Entity Count']} dependents)",
                        }
                    )

    # --- Flag 5: Connectivity suggests higher frequency
    # Low/Medium residual risk overall, but hands off to 2+ High/Critical entities
    # OR is primary control owner for a concentration asset.
    hc_ents = set(matrix[matrix["Overall Residual Risk"].isin(HIGH_CRITICAL)]["Audit Entity ID"])
    concentration_primaries: set[str] = set()
    if not concentration_flags.empty:
        for _, asset in concentration_flags.iterrows():
            if asset["Asset Type"] == "Application":
                tbl, col = entity_app, "Application Name"
            elif asset["Asset Type"] == "Vendor":
                tbl, col = entity_vendor, "Third Party Name"
            else:
                tbl, col = entity_model, "Model Name"
            if tbl.empty or "Relationship" not in tbl.columns:
                continue
            prim = tbl[(tbl[col] == asset["Asset Name"]) & (tbl["Relationship"] == "primary")]
            concentration_primaries.update(prim["Audit Entity ID"].unique())

    for _, row in matrix.iterrows():
        ent = row["Audit Entity ID"]
        if row["Overall Residual Risk"] in HIGH_CRITICAL:
            continue
        if handoffs.empty:
            high_targets = 0
        else:
            ho_to = handoffs[(handoffs["Source Entity ID"] == ent) & (handoffs["Direction"] == "to")]
            high_targets = len(set(ho_to["Target Entity ID"]) & hc_ents)
        if high_targets >= 2 or ent in concentration_primaries:
            flags.append(
                {
                    "Flag Type": "CONNECTIVITY SUGGESTS HIGHER FREQUENCY",
                    "Priority": "MEDIUM",
                    "Subject": ent,
                    "Detail": f"{high_targets} H/C handoff targets; primary_owner={ent in concentration_primaries}",
                }
            )

    # --- Flag 6: high-risk + weak, not in plan
    f6 = matrix[(matrix["High/Critical + Weak Count"] >= 1) & (matrix["In Scope"] == "No")]
    for _, r in f6.iterrows():
        flags.append(
            {
                "Flag Type": "HIGH RISK + WEAK CONTROLS, NOT IN PLAN",
                "Priority": "MEDIUM",
                "Subject": r["Audit Entity ID"],
                "Detail": f"{r['High/Critical + Weak Count']} H/C risks with weak controls",
            }
        )

    # --- Flag 7: frequency override on top-quartile connected entity
    if not matrix.empty:
        q = matrix["Connectivity Total"].quantile(0.75)
        f7 = matrix[(matrix["Frequency Overridden"] == True) & (matrix["Connectivity Total"] >= q)]
        for _, r in f7.iterrows():
            flags.append(
                {
                    "Flag Type": "FREQUENCY OVERRIDE ON CONNECTED ENTITY",
                    "Priority": "LOW",
                    "Subject": r["Audit Entity ID"],
                    "Detail": f"Override set, connectivity={r['Connectivity Total']}",
                }
            )

    return pd.DataFrame(flags, columns=["Flag Type", "Priority", "Subject", "Detail"])


def build_coverage_summary(
    matrix: pd.DataFrame, flags: pd.DataFrame, concentration_flags: pd.DataFrame
) -> pd.DataFrame:
    total = len(matrix)
    in_scope = int((matrix["In Scope"] == "Yes").sum()) if total else 0
    overdue = int((matrix["Overdue Flag"] == "Yes").sum()) if total else 0
    overdue_not_in = int(
        ((matrix["Overdue Flag"] == "Yes") & (matrix["In Scope"] == "No")).sum()
    ) if total else 0
    top20 = matrix.sort_values("Connectivity Total", ascending=False).head(20)
    top10 = top20.head(10)
    rows = [
        ("Total entities", total),
        ("In scope", in_scope),
        ("In scope %", f"{(100 * in_scope / total):.1f}%" if total else "0%"),
        ("Overdue", overdue),
        ("Overdue & not in plan", overdue_not_in),
        ("Top 20 connected in scope", int((top20["In Scope"] == "Yes").sum())),
        ("Top 10 connected in scope", int((top10["In Scope"] == "Yes").sum())),
        ("Horizontal entities in scope", int(((matrix["Horizontal Flag"] == "horizontal") & (matrix["In Scope"] == "Yes")).sum())),
        ("Concentration assets (total)", len(concentration_flags)),
        ("HIGH flags", int((flags["Priority"] == "HIGH").sum()) if not flags.empty else 0),
        ("MEDIUM flags", int((flags["Priority"] == "MEDIUM").sum()) if not flags.empty else 0),
        ("LOW flags", int((flags["Priority"] == "LOW").sum()) if not flags.empty else 0),
    ]
    return pd.DataFrame(rows, columns=["Metric", "Value"])


def build_concentration_detail(
    concentration_flags: pd.DataFrame,
    entity_app: pd.DataFrame,
    entity_vendor: pd.DataFrame,
    entity_model: pd.DataFrame,
    matrix: pd.DataFrame,
    plan_ids: set[str],
) -> pd.DataFrame:
    if concentration_flags.empty:
        return pd.DataFrame()
    mat_idx = matrix.set_index("Audit Entity ID")
    rows = []
    for _, asset in concentration_flags.iterrows():
        if asset["Asset Type"] == "Application":
            tbl, col = entity_app, "Application Name"
        elif asset["Asset Type"] == "Vendor":
            tbl, col = entity_vendor, "Third Party Name"
        else:
            tbl, col = entity_model, "Model Name"
        primary_ents = []
        if not tbl.empty and "Relationship" in tbl.columns:
            primary_ents = (
                tbl[(tbl[col] == asset["Asset Name"]) & (tbl["Relationship"] == "primary")]["Audit Entity ID"]
                .unique()
                .tolist()
            )
        primary_id = primary_ents[0] if primary_ents else ""
        primary_in_scope = primary_id in plan_ids if primary_id else False
        primary_risk = mat_idx.loc[primary_id, "Overall Residual Risk"] if primary_id in mat_idx.index else ""
        primary_freq = mat_idx.loc[primary_id, "Effective Frequency"] if primary_id in mat_idx.index else ""
        dep_ids = set(asset["Dependent Entity IDs"].split(";")) if asset["Dependent Entity IDs"] else set()
        secondary_ids = dep_ids - set(primary_ents)
        secondary_in = len(secondary_ids & plan_ids)
        sec_rate = f"{(100 * secondary_in / len(secondary_ids)):.1f}%" if secondary_ids else "N/A"
        rows.append(
            {
                "Asset Name": asset["Asset Name"],
                "Asset Type": asset["Asset Type"],
                "Dependent Count": asset["Dependent Entity Count"],
                "Primary Entity": primary_id,
                "Primary Residual Risk": primary_risk,
                "Primary Frequency": primary_freq,
                "Primary In Scope": "Yes" if primary_in_scope else "No",
                "Secondary Coverage Rate": sec_rate,
            }
        )
    return pd.DataFrame(rows)
