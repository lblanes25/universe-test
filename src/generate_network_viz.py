#!/usr/bin/env python3
"""
generate_network_viz.py - Audit Universe Visualization Generator (v3)

Produces two self-contained HTML visualizations from pipeline output:
  1. network_visualization.html — Interactive network graph with all filters
  2. pga_chord_sankey.html — PGA chord diagram with Sankey drill-down

Usage:
    python generate_network_viz.py [--input-dir DIR] [--output-dir DIR]

Required files in input-dir:
    layer1_output.xlsx
    edge_derivation_output.xlsx
    layer2_coverage_matrix.xlsx

Optional:
    handoff_categories.csv  (enables category-aware 2-hop in network viz)

Dependencies:
    pip install pandas openpyxl
"""
import argparse, glob, json, os, sys
from datetime import datetime
import pandas as pd

_TPL_DIR = os.path.dirname(os.path.abspath(__file__))

def _find_latest(input_dir, base_name, ext=".xlsx"):
    """Find the latest timestamped file matching base_name_YYYYMMDD.ext, or fall back to base_name.ext."""
    pattern = os.path.join(input_dir, f"{base_name}_*{ext}")
    matches = sorted(glob.glob(pattern), reverse=True)
    if matches:
        return matches[0]
    fallback = os.path.join(input_dir, f"{base_name}{ext}")
    if os.path.isfile(fallback):
        return fallback
    return None


def read_pipeline(input_dir):
    """Read all pipeline files and return raw DataFrames."""
    l1 = _find_latest(input_dir, "layer1_output")
    ed = _find_latest(input_dir, "edge_derivation_output")
    l2 = _find_latest(input_dir, "layer2_coverage_matrix")
    hc = os.path.join(input_dir, "handoff_categories.csv")
    for name, p in [("layer1_output", l1), ("edge_derivation_output", ed), ("layer2_coverage_matrix", l2)]:
        if p is None:
            sys.exit(f"ERROR: Missing file: {name}*.xlsx in {input_dir}")

    dfs = dict(
        nodes = pd.read_excel(l1, sheet_name="Nodes"),
        edges = pd.read_excel(ed, sheet_name="Master Edge List"),
        coverage = pd.read_excel(l2, sheet_name="Coverage Matrix"),
        assets = pd.read_excel(l1, sheet_name="Asset Dependency Lookup"),
        entity_app = pd.read_excel(l1, sheet_name="Entity-Application"),
        entity_vendor = pd.read_excel(l1, sheet_name="Entity-Vendor"),
        dep_profile = pd.read_excel(l1, sheet_name="Entity Dependency Profile"),
        conc_risk = pd.read_excel(l2, sheet_name="Concentration Risk Detail"),
        prsa = pd.read_excel(l1, sheet_name="Entity-PRSA"),
    )
    if os.path.isfile(hc):
        print(f"  Found handoff_categories.csv — enabling category-aware 2-hop")
        dfs["categories"] = pd.read_csv(hc)
    else:
        print(f"  No handoff_categories.csv — 2-hop will use structural tracing")
        dfs["categories"] = None
    return dfs


def build_network_data(dfs):
    """Build JSON data for the network visualization."""
    cat_lookup = {}
    all_cats = []
    if dfs["categories"] is not None:
        for _, r in dfs["categories"].iterrows():
            key = (str(r["Source Entity ID"]), str(r["Target Entity ID"]), str(r["Direction"]))
            cat_lookup[key] = str(r["Handoff Category"])
        all_cats = sorted(set(cat_lookup.values()))

    cov_idx = dfs["coverage"].set_index("Audit Entity ID")
    dep_idx = dfs["dep_profile"].set_index("Audit Entity ID")

    node_list = []
    for _, row in dfs["nodes"].iterrows():
        eid = str(row["Audit Entity ID"])
        c = cov_idx.loc[eid] if eid in cov_idx.index else None
        d = dep_idx.loc[eid] if eid in dep_idx.index else None
        risk_val = c["Overall Residual Risk"] if c is not None and pd.notna(c.get("Overall Residual Risk")) else None
        risk = str(risk_val) if risk_val else "N/A"
        hr = c["Highest Residual Risk"] if c is not None and pd.notna(c.get("Highest Residual Risk")) else None
        highest_risk = str(hr) if hr else "N/A"
        display_risk = highest_risk if risk == "N/A" else risk
        node_list.append(dict(id=eid, name=str(row["Audit Entity Name"]), businessUnit=str(row["Business Unit"]),
            auditLeader=str(row["Audit Leader"]), horizontalFlag=str(row["Horizontal Flag"]),
            pga=str(row.get("PGA/ASL","")) if pd.notna(row.get("PGA/ASL")) else "",
            riskRating=display_risk, inScope=str(c["In Scope"]) if c is not None else "No",
            overdue=str(c["Overdue Flag"]) if c is not None else "No",
            connectivityTotal=int(c["Connectivity Total"]) if c is not None and pd.notna(c["Connectivity Total"]) else 0,
            highestRisk=highest_risk,
            hcRisks=str(c["High/Critical Risks"]) if c is not None and pd.notna(c.get("High/Critical Risks")) else "",
            handoffTo=int(d["Handoff To Count"]) if d is not None and pd.notna(d["Handoff To Count"]) else 0,
            handoffFrom=int(d["Handoff From Count"]) if d is not None and pd.notna(d["Handoff From Count"]) else 0))

    # Merge small audit leaders into "Other" bucket
    MIN_LEADER_ENTITIES = 6
    leader_counts = {}
    for n in node_list:
        leader_counts[n["auditLeader"]] = leader_counts.get(n["auditLeader"], 0) + 1
    small_leaders = {l for l, c in leader_counts.items() if c < MIN_LEADER_ENTITIES}
    if small_leaders:
        other_count = sum(leader_counts[l] for l in small_leaders)
        for n in node_list:
            if n["auditLeader"] in small_leaders:
                n["auditLeader"] = "Other"
        print(f"  Merged {len(small_leaders)} small audit leaders into Other ({other_count} entities)")

    edge_list = []
    for _, row in dfs["edges"].iterrows():
        etype = str(row["Edge Type"])
        if "model" in etype.lower(): continue
        e = dict(source=str(row["Entity A ID"]), target=str(row["Entity B ID"]), edgeType=etype,
            detail=str(row["Detail"]) if pd.notna(row["Detail"]) else "", highFreq=bool(row["High Frequency Flag"]))
        if etype in ("handoff_to","handoff_from"):
            direction = "to" if etype == "handoff_to" else "from"
            e["category"] = cat_lookup.get((e["source"], e["target"], direction), "UNKNOWN")
        else:
            e["category"] = ""
        edge_list.append(e)

    asset_list = []
    for _, row in dfs["assets"].iterrows():
        if str(row["Asset Type"]).lower() == "model": continue
        dep_ids = str(row["Dependent Entity IDs"]).split(";") if pd.notna(row["Dependent Entity IDs"]) else []
        asset_list.append(dict(name=str(row["Asset Name"]), type=str(row["Asset Type"]),
            depCount=int(row["Dependent Entity Count"]), primaryCount=int(row["Primary Count"]),
            secondaryCount=int(row["Secondary Count"]), depIds=dep_ids))

    ea_list = [dict(entityId=str(r["Audit Entity ID"]), appName=str(r["Application Name"]),
        relationship=str(r["Relationship"])) for _, r in dfs["entity_app"].iterrows()]
    ev_list = [dict(entityId=str(r["Audit Entity ID"]), vendorName=str(r["Third Party Name"]),
        relationship=str(r["Relationship"])) for _, r in dfs["entity_vendor"].iterrows()]
    conc_list = [dict(assetName=str(r["Asset Name"]), assetType=str(r["Asset Type"]),
        depCount=int(r["Dependent Count"]), primaryEntity=str(r["Primary Entity"]),
        primaryInScope=str(r["Primary In Scope"]), secCovRate=str(r["Secondary Coverage Rate"]))
        for _, r in dfs["conc_risk"].iterrows()]
    prsa_map = {}
    for _, r in dfs["prsa"].iterrows():
        pv, eid = str(r["PRSA Value"]), str(r["Audit Entity ID"])
        prsa_map.setdefault(pv, []).append(eid)
    prsa_list = [dict(value=k, entityIds=v) for k,v in sorted(prsa_map.items(), key=lambda x: -len(x[1]))]

    return dict(nodes=node_list, edges=edge_list, assets=asset_list, entityApps=ea_list,
                entityVendors=ev_list, concRisk=conc_list, prsaClusters=prsa_list, handoffCategories=all_cats)


def build_chord_data(dfs):
    """Build JSON data for the PGA chord/sankey visualization."""
    nodes_df = dfs["nodes"]
    edges_df = dfs["edges"]
    cov_idx = dfs["coverage"].set_index("Audit Entity ID")

    entities = {}
    for _, r in nodes_df.iterrows():
        eid = str(r["Audit Entity ID"])
        pga = str(r["PGA/ASL"]).strip() if pd.notna(r["PGA/ASL"]) and str(r["PGA/ASL"]).strip() else "Unassigned"
        c = cov_idx.loc[eid] if eid in cov_idx.index else None
        entities[eid] = dict(id=eid, name=str(r["Audit Entity Name"]), pga=pga,
            leader=str(r["Audit Leader"]), bu=str(r["Business Unit"]),
            risk=str(c["Overall Residual Risk"]) if c is not None and pd.notna(c.get("Overall Residual Risk")) else "N/A",
            inScope=str(c["In Scope"]) if c is not None else "No")

    handoffs = []
    for _, e in edges_df.iterrows():
        etype = str(e["Edge Type"])
        if etype not in ("handoff_to","handoff_from"): continue
        src, tgt = str(e["Entity A ID"]), str(e["Entity B ID"])
        if src not in entities or tgt not in entities: continue
        handoffs.append(dict(source=src, target=tgt, type=etype))

    pgas = sorted(set(e["pga"] for e in entities.values()))
    leaders = sorted(set(e["leader"] for e in entities.values()))
    pga_idx = {p:i for i,p in enumerate(pgas)}
    n = len(pgas)
    matrix = [[0]*n for _ in range(n)]
    for h in handoffs:
        sp, tp = entities[h["source"]]["pga"], entities[h["target"]]["pga"]
        matrix[pga_idx[sp]][pga_idx[tp]] += 1

    pga_summaries = {}
    for p in pgas:
        ents = [e for e in entities.values() if e["pga"]==p]
        pga_summaries[p] = dict(count=len(ents), inScope=sum(1 for e in ents if e["inScope"]=="Yes"),
            leaders=list(set(e["leader"] for e in ents)), entities=[e["id"] for e in ents])

    return dict(pgas=pgas, leaders=leaders, matrix=matrix, entities=entities,
                handoffs=handoffs, pgaSummaries=pga_summaries)



def _group_small(values, counts, threshold=3, label="Other"):
    """Group values with <= threshold entities into a single 'Other' bucket."""
    keep = [v for v in values if counts.get(v, 0) > threshold]
    small = [v for v in values if counts.get(v, 0) <= threshold]
    mapping = {v: v for v in keep}
    for v in small:
        mapping[v] = label
    result = sorted(keep)
    if small:
        result.append(label)
    return result, mapping


def build_heatmap_data(dfs):
    """Build JSON data for the PGA x Audit Leader coverage heatmap."""
    cov_idx = dfs["coverage"].set_index("Audit Entity ID")

    # Count entities per PGA and per leader for grouping
    pga_counts = {}
    leader_counts = {}
    for _, r in dfs["nodes"].iterrows():
        pga = str(r["PGA/ASL"]).strip() if pd.notna(r.get("PGA/ASL")) and str(r["PGA/ASL"]).strip() else "Unassigned"
        leader = str(r["Audit Leader"]).strip() if pd.notna(r.get("Audit Leader")) else "Unknown"
        pga_counts[pga] = pga_counts.get(pga, 0) + 1
        leader_counts[leader] = leader_counts.get(leader, 0) + 1

    pgas_ordered, pga_map = _group_small(list(pga_counts.keys()), pga_counts)
    leaders_ordered, leader_map = _group_small(list(leader_counts.keys()), leader_counts)

    cells = {}
    for _, r in dfs["nodes"].iterrows():
        eid = str(r["Audit Entity ID"])
        raw_pga = str(r["PGA/ASL"]).strip() if pd.notna(r.get("PGA/ASL")) and str(r["PGA/ASL"]).strip() else "Unassigned"
        raw_leader = str(r["Audit Leader"]).strip() if pd.notna(r.get("Audit Leader")) else "Unknown"
        pga = pga_map.get(raw_pga, "Other")
        leader = leader_map.get(raw_leader, "Other")
        c = cov_idx.loc[eid] if eid in cov_idx.index else None
        inScope = str(c["In Scope"]) == "Yes" if c is not None else False
        overdue = str(c["Overdue Flag"]) == "Yes" if c is not None else False
        risk = str(c["Overall Residual Risk"]) if c is not None and pd.notna(c.get("Overall Residual Risk")) else "N/A"
        key = (pga, leader)
        if key not in cells:
            cells[key] = dict(pga=pga, leader=leader, total=0, inScope=0, overdue=0, notInScope=0, entities=[])
        cells[key]["total"] += 1
        if inScope:
            cells[key]["inScope"] += 1
        else:
            cells[key]["notInScope"] += 1
        if overdue:
            cells[key]["overdue"] += 1
        cells[key]["entities"].append(dict(id=eid, name=str(r["Audit Entity Name"]), risk=risk, inScope=inScope, overdue=overdue))

    cell_list = list(cells.values())
    pga_totals, leader_totals = {}, {}
    for c in cell_list:
        for d, k in [(pga_totals, c["pga"]), (leader_totals, c["leader"])]:
            if k not in d:
                d[k] = dict(total=0, inScope=0, overdue=0, notInScope=0)
            d[k]["total"] += c["total"]
            d[k]["inScope"] += c["inScope"]
            d[k]["overdue"] += c["overdue"]
            d[k]["notInScope"] += c["notInScope"]
    gt = dict(total=sum(t["total"] for t in pga_totals.values()),
              inScope=sum(t["inScope"] for t in pga_totals.values()),
              overdue=sum(t["overdue"] for t in pga_totals.values()),
              notInScope=sum(t["notInScope"] for t in pga_totals.values()))
    return dict(pgas=pgas_ordered, leaders=leaders_ordered, cells=cell_list,
                pgaTotals=pga_totals, leaderTotals=leader_totals, grandTotal=gt)


def build_treemap_data(dfs):
    """Build JSON data for the coverage treemap (PGA > Audit Leader > Entity)."""
    cov_idx = dfs["coverage"].set_index("Audit Entity ID")

    pga_counts = {}
    leader_counts = {}
    for _, r in dfs["nodes"].iterrows():
        pga = str(r["PGA/ASL"]).strip() if pd.notna(r.get("PGA/ASL")) and str(r["PGA/ASL"]).strip() else "Unassigned"
        leader = str(r["Audit Leader"]).strip() if pd.notna(r.get("Audit Leader")) else "Unknown"
        pga_counts[pga] = pga_counts.get(pga, 0) + 1
        leader_counts[leader] = leader_counts.get(leader, 0) + 1

    _, pga_map = _group_small(list(pga_counts.keys()), pga_counts)
    _, leader_map = _group_small(list(leader_counts.keys()), leader_counts)

    # Build hierarchy: PGA -> Leader -> entities
    tree = {}
    for _, r in dfs["nodes"].iterrows():
        eid = str(r["Audit Entity ID"])
        raw_pga = str(r["PGA/ASL"]).strip() if pd.notna(r.get("PGA/ASL")) and str(r["PGA/ASL"]).strip() else "Unassigned"
        raw_leader = str(r["Audit Leader"]).strip() if pd.notna(r.get("Audit Leader")) else "Unknown"
        pga = pga_map.get(raw_pga, "Other")
        leader = leader_map.get(raw_leader, "Other")
        c = cov_idx.loc[eid] if eid in cov_idx.index else None
        inScope = str(c["In Scope"]) == "Yes" if c is not None else False
        overdue = str(c["Overdue Flag"]) == "Yes" if c is not None else False
        risk = str(c["Overall Residual Risk"]) if c is not None and pd.notna(c.get("Overall Residual Risk")) else "N/A"
        conn = int(c["Connectivity Total"]) if c is not None and pd.notna(c.get("Connectivity Total")) else 0

        if pga not in tree:
            tree[pga] = {}
        if leader not in tree[pga]:
            tree[pga][leader] = []
        tree[pga][leader].append(dict(id=eid, name=str(r["Audit Entity Name"]),
                                       risk=risk, inScope=inScope, overdue=overdue, connectivity=conn))

    # Convert to nested children format for D3 treemap
    children = []
    for pga in sorted(tree.keys()):
        pga_children = []
        for leader in sorted(tree[pga].keys()):
            entities = tree[pga][leader]
            total = len(entities)
            in_scope = sum(1 for e in entities if e["inScope"])
            pga_children.append(dict(
                name=leader, children=entities,
                total=total, inScope=in_scope,
                coverageRate=round(in_scope / total * 100) if total else 0
            ))
        pga_total = sum(c["total"] for c in pga_children)
        pga_in_scope = sum(c["inScope"] for c in pga_children)
        children.append(dict(
            name=pga, children=pga_children,
            total=pga_total, inScope=pga_in_scope,
            coverageRate=round(pga_in_scope / pga_total * 100) if pga_total else 0
        ))
    return dict(name="Audit Universe", children=children)


def nodeTotal_py(node):
    """Count total entities in a treemap node (Python-side helper)."""
    if "total" in node:
        return node["total"]
    if "children" not in node:
        return 1
    return sum(nodeTotal_py(c) for c in node["children"])


def generate(input_dir, output_dir):
    print(f"Reading pipeline files from: {input_dir}")
    dfs = read_pipeline(input_dir)
    date_stamp = datetime.now().strftime("%Y%m%d")

    # === Network Visualization ===
    net_data = build_network_data(dfs)
    cats_tagged = sum(1 for e in net_data["edges"] if e.get("category") and e["category"] not in ("","UNKNOWN"))
    print(f"  Network: {len(net_data['nodes'])} nodes, {len(net_data['edges'])} edges, {cats_tagged} categorized handoffs")
    net_json = json.dumps(net_data, separators=(",",":"))
    with open(os.path.join(_TPL_DIR, "_network_template.html"), "r", encoding="utf-8") as f:
        net_html = f.read().replace("%%DATA_INJECTION%%", "const DATA = " + net_json + ";")
    net_path = os.path.join(output_dir, f"network_visualization_{date_stamp}.html")
    with open(net_path, "w", encoding="utf-8") as f: f.write(net_html)
    print(f"  -> {net_path} ({len(net_html):,} bytes)")

    # === PGA Chord + Sankey ===
    chord_data = build_chord_data(dfs)
    print(f"  Chord: {len(chord_data['pgas'])} PGAs, {len(chord_data['handoffs'])} handoffs")
    chord_json = json.dumps(chord_data, separators=(",",":"))
    with open(os.path.join(_TPL_DIR, "_chord_sankey_template.html"), "r", encoding="utf-8") as f:
        chord_html = f.read().replace("%%DATA_INJECTION%%", "const DATA = " + chord_json + ";")
    chord_path = os.path.join(output_dir, f"pga_chord_sankey_{date_stamp}.html")
    with open(chord_path, "w", encoding="utf-8") as f: f.write(chord_html)
    print(f"  -> {chord_path} ({len(chord_html):,} bytes)")


    # === Coverage Heatmap (PGA x Audit Leader) ===
    hm_data = build_heatmap_data(dfs)
    print(f"  Heatmap: {len(hm_data['pgas'])} PGAs x {len(hm_data['leaders'])} leaders, {hm_data['grandTotal']['total']} entities")
    hm_json = json.dumps(hm_data, separators=(",",":"))
    with open(os.path.join(_TPL_DIR, "_heatmap_template.html"), "r", encoding="utf-8") as f:
        hm_html = f.read().replace("%%DATA_INJECTION%%", "const DATA = " + hm_json + ";")
    hm_path = os.path.join(output_dir, f"coverage_heatmap_{date_stamp}.html")
    with open(hm_path, "w", encoding="utf-8") as f: f.write(hm_html)
    print(f"  -> {hm_path} ({len(hm_html):,} bytes)")

    # === Coverage Treemap ===
    tm_data = build_treemap_data(dfs)
    tm_total = sum(nodeTotal_py(c) for c in tm_data["children"])
    print(f"  Treemap: {len(tm_data['children'])} PGA groups, {tm_total} entities")
    tm_json = json.dumps(tm_data, separators=(",",":"))
    with open(os.path.join(_TPL_DIR, "_treemap_template.html"), "r", encoding="utf-8") as f:
        tm_html = f.read().replace("%%DATA_INJECTION%%", "const DATA = " + tm_json + ";")
    tm_path = os.path.join(output_dir, f"coverage_treemap_{date_stamp}.html")
    with open(tm_path, "w", encoding="utf-8") as f: f.write(tm_html)
    print(f"  -> {tm_path} ({len(tm_html):,} bytes)")

    print(f"Done. All visualizations written to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Audit Universe Visualizations (v3)")
    parser.add_argument("--input-dir", default=".", help="Directory containing pipeline outputs")
    parser.add_argument("--output-dir", default=".", help="Directory for output HTML files")
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    generate(args.input_dir, args.output_dir)
