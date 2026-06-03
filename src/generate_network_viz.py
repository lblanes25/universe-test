#!/usr/bin/env python3
"""
generate_network_viz.py - Audit Universe Visualization Generator (v3)

Produces two self-contained HTML visualizations from pipeline output:
  1. network_visualization.html — Interactive network graph with all filters
  2. pga_chord_sankey.html — PGA chord diagram with Sankey drill-down

Usage:
    python src/generate_network_viz.py \
        --input-dir data/output \
        --output-dir data/output \
        --source data/input/<universe.csv>

Required files in input-dir:
    layer1_output*.xlsx
    edge_derivation_output*.xlsx
    layer2_coverage_matrix*.xlsx
  (latest YYYYMMDD-suffixed file is picked automatically)

Optional:
    --source <universe.csv>     surfaces hand-off description / overview in detail panel
    handoff_categories.csv      enables category-aware 2-hop in network viz
    findings_rollup*.xlsx       enables likely-gap overlay

Dependencies:
    pip install pandas openpyxl
"""
import argparse, glob, html, json, os, re, sys
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


def _find_findings_rollup(input_dir):
    """Locate the Stage 2 findings rollup xlsx (optional gap-overlay input).

    Checks the input dir first, then the repo-default runs/stage2/aggregated
    location. Returns None when absent — the overlay is purely optional.
    """
    candidates = [
        os.path.join(input_dir, "findings_rollup.xlsx"),
        os.path.join(_TPL_DIR, "..", "runs", "stage2", "aggregated", "findings_rollup.xlsx"),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return os.path.abspath(c)
    return None


def _find_findings_csv(input_dir):
    """Locate the Stage 2 findings CSV when the reviewer workbook is absent."""
    candidates = [
        os.path.join(input_dir, "findings.csv"),
        os.path.join(_TPL_DIR, "..", "runs", "stage2", "aggregated", "findings.csv"),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return os.path.abspath(c)
    return None


def _find_source_csv(input_dir, explicit=None):
    """Locate the source universe CSV — used for entity prose (Hand-off
    Description, Audit Entity Overview) that the pipeline doesn't carry into
    the Nodes table. Returns None when not found; the prose is then omitted.
    """
    cands = []
    if explicit:
        cands.append(explicit)
    cands += sorted(glob.glob(os.path.join(input_dir, "*.csv")))
    cands += sorted(glob.glob(os.path.join(_TPL_DIR, "..", "data", "input", "*.csv")))
    for c in cands:
        if c and os.path.isfile(c):
            try:
                head = pd.read_csv(c, nrows=0)
            except Exception:
                continue
            if "Audit Entity ID" in head.columns and "Hand-off Description" in head.columns:
                return os.path.abspath(c)
    return None


def _find_controls_csv(input_dir, explicit=None):
    """Locate the Archer controls export — resolves SR/KPA IDs to descriptions
    and the receiver's covering controls for the caseboard. Detected by header
    signature; returns None when absent (the join then degrades to bare IDs).
    """
    cands = []
    if explicit:
        cands.append(explicit)
    cands += sorted(glob.glob(os.path.join(input_dir, "*.csv")))
    cands += sorted(glob.glob(os.path.join(_TPL_DIR, "..", "data", "input", "*.csv")))
    for c in cands:
        if c and os.path.isfile(c):
            try:
                head = pd.read_csv(c, nrows=0)
            except Exception:
                continue
            if "Control ID" in head.columns and "Key Risk Description" in head.columns:
                return os.path.abspath(c)
    return None


def read_pipeline(input_dir, source_csv=None, controls_csv=None):
    """Read all pipeline files and return raw DataFrames."""
    l1 = _find_latest(input_dir, "layer1_output")
    ed = _find_latest(input_dir, "edge_derivation_output")
    l2 = _find_latest(input_dir, "layer2_coverage_matrix")
    hc = os.path.join(input_dir, "handoff_categories.csv")
    fr = _find_findings_rollup(input_dir)
    fc = _find_findings_csv(input_dir)
    sc = _find_source_csv(input_dir, source_csv)
    cc = _find_controls_csv(input_dir, controls_csv)
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
    if fr is not None:
        try:
            dfs["findings"] = pd.read_excel(fr, sheet_name="All Findings (Tagged)")
            print(f"  Found findings_rollup.xlsx — enabling likely-gap overlay")
        except Exception:
            print(f"  findings_rollup.xlsx present but unreadable — gap overlay disabled")
            dfs["findings"] = None
    elif fc is not None:
        try:
            dfs["findings"] = pd.read_csv(fc)
            print(f"  Found findings.csv — enabling likely-gap overlay")
        except Exception:
            print(f"  findings.csv present but unreadable — gap overlay disabled")
            dfs["findings"] = None
    else:
        print(f"  No findings_rollup.xlsx/findings.csv — gap overlay disabled (viz unchanged)")
        dfs["findings"] = None
    if sc is not None:
        try:
            dfs["source"] = pd.read_csv(sc)
            print(f"  Found source CSV — hand-off description / overview available in detail panel")
        except Exception:
            dfs["source"] = None
    else:
        dfs["source"] = None
    if cc is not None:
        try:
            dfs["controls"] = pd.read_csv(cc)
            print(f"  Found controls CSV — resolving SR/KPA names + receiver coverage in caseboard")
        except Exception:
            print(f"  controls CSV present but unreadable — caseboard falls back to bare IDs")
            dfs["controls"] = None
    else:
        print(f"  No controls CSV — caseboard shows bare SR/KPA IDs, no covering-controls join")
        dfs["controls"] = None
    return dfs


def _split_ids(val):
    """Split a multi-id cell on ';' or ',' and trim, dropping blanks."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return []
    return [s.strip() for s in re.split(r"[;,]", str(val)) if s.strip()]


def _case_key(focal_id, partner_id, task):
    """Stable, directed key for one gap "case" — shared by the map (so a gap
    edge/node can deep-link) and the caseboard (so it can be selected). Directed
    on the finding's own focal/partner (a case is "what A handed to B"), even
    though _attach_gap_findings matches master edges undirected.
    """
    focal = _clean_value(focal_id)
    partner = _clean_value(partner_id)
    try:
        t = int(task or 0)
    except (TypeError, ValueError):
        t = 0
    return f"{focal}>{partner}|t{t}" if partner else f"{focal}|t{t}"


def _gate_passed(row):
    """Read gate_passed defensively — default True when missing or blank."""
    gp = row.get("gate_passed", True)
    if gp is None or (isinstance(gp, float) and pd.isna(gp)):
        return True
    return bool(gp)


def _attach_gap_findings(node_list, edge_list, findings):
    """Overlay Task 3/5 likely-coverage-gap findings onto nodes and edges.

    Task 5 names its partner -> aggregate onto the matching handoff edge (either
    orientation), or a synthetic dashed edge when the handoff isn't in the master
    edge list. Task 3's receiver is free-text only -> aggregate onto the focal
    node. Multiple findings per edge/node aggregate into one `gap` dict.

    Returns (gap_edges_unplaced, gap_nodes_unmatched) for honest reporting.
    """
    node_by_id = {n["id"]: n for n in node_list}
    edge_by_pair = {}
    for e in edge_list:
        if e["edgeType"] in ("handoff_to", "handoff_from"):
            edge_by_pair.setdefault(frozenset((e["source"], e["target"])), []).append(e)

    def _merge(target, row, task):
        g = target.setdefault("gap", dict(count=0, countPassed=0, countFailed=0,
                                          srIds=[], example="", items=[], task=task))
        # Stash the case key(s) so the map can deep-link into the caseboard. A
        # frozenset-matched edge can aggregate both orientations -> keep a primary
        # plus the full collected set.
        key = _case_key(row.get("focal_entity_id"), row.get("cross_entity_partner_id"), task)
        g.setdefault("caseKey", key)
        ks = g.setdefault("caseKeys", [])
        if key not in ks:
            ks.append(key)
        g["count"] += 1
        if _gate_passed(row):
            g["countPassed"] += 1
        else:
            g["countFailed"] += 1
        srs = _split_ids(row.get("specific_risk_ids"))
        seen = set(g["srIds"])
        for sr in srs:
            if sr not in seen:
                seen.add(sr)
                g["srIds"].append(sr)
        reasoning = row.get("reasoning")
        reasoning = reasoning.strip() if isinstance(reasoning, str) else ""
        if not g["example"] and reasoning:
            g["example"] = reasoning[:400]
        # Per-finding detail for the detail panel + worklist export (cap to bound size).
        if len(g["items"]) < 12:
            quote = row.get("evidence_quote")
            quote = quote.strip() if isinstance(quote, str) else ""
            g["items"].append(dict(
                srIds=srs,
                kpaIds=_split_ids(row.get("kpa_ids")),
                reasoning=reasoning[:600],
                quote=quote[:300],
            ))

    cls = findings["classification"].astype(str).str.lower()
    task_num = pd.to_numeric(findings["task"], errors="coerce")
    gaps = findings[cls.str.contains("coverage gap", na=False) & task_num.isin([3, 5])]

    unplaced = unmatched = 0
    for _, row in gaps.iterrows():
        task = int(row["task"]) if pd.notna(row["task"]) else 0
        focal = str(row["focal_entity_id"]).strip()
        if task == 5:
            partner = row.get("cross_entity_partner_id")
            partner = str(partner).strip() if partner is not None and pd.notna(partner) else ""
            matches = edge_by_pair.get(frozenset((focal, partner))) if partner else None
            if matches:
                for e in matches:
                    _merge(e, row, 5)
            elif partner and focal in node_by_id and partner in node_by_id:
                syn = dict(source=focal, target=partner, edgeType="handoff_to",
                           detail="", highFreq=False, category="", synthetic=True)
                _merge(syn, row, 5)
                edge_list.append(syn)
                edge_by_pair.setdefault(frozenset((focal, partner)), []).append(syn)
            else:
                unplaced += 1
        else:  # Task 3 — receiver unknown, anchor on the focal node
            if focal in node_by_id:
                _merge(node_by_id[focal], row, 3)
            else:
                unmatched += 1
    return unplaced, unmatched


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

    # Entity prose (hand-off description / overview) from the source CSV, keyed by entity id.
    src = dfs.get("source")
    if src is not None and "Audit Entity ID" in src.columns:
        hd_col = "Hand-off Description" if "Hand-off Description" in src.columns else None
        ov_col = "Audit Entity Overview" if "Audit Entity Overview" in src.columns else None
        pmap = {}
        for _, r in src.iterrows():
            eid = str(r["Audit Entity ID"])
            pmap[eid] = (
                str(r[hd_col]).strip() if hd_col and pd.notna(r[hd_col]) else "",
                str(r[ov_col]).strip() if ov_col and pd.notna(r[ov_col]) else "",
            )
        for n in node_list:
            hd, ov = pmap.get(n["id"], ("", ""))
            if hd:
                n["handoffDesc"] = hd
            if ov:
                n["overview"] = ov

    result = dict(nodes=node_list, edges=edge_list, assets=asset_list, entityApps=ea_list,
                  entityVendors=ev_list, concRisk=conc_list, prsaClusters=prsa_list, handoffCategories=all_cats)
    if dfs.get("findings") is not None:
        unplaced, unmatched = _attach_gap_findings(node_list, edge_list, dfs["findings"])
        result["gapEdgesUnplaced"] = unplaced
        result["gapNodesUnmatched"] = unmatched
    return result


def _clean_value(value, default=""):
    """Return a JSON-safe string without pandas/nan placeholders."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return default
    try:
        if pd.isna(value):
            return default
    except (TypeError, ValueError):
        pass
    text = str(value).strip()
    if text.lower() in ("nan", "nat", "none"):
        return default
    return text


def _int_value(value, default=0):
    try:
        if pd.isna(value):
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _bool_value(value, default=True):
    if value is None:
        return default
    try:
        if pd.isna(value):
            return default
    except (TypeError, ValueError):
        pass
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in ("true", "yes", "y", "1", "pass", "passed"):
        return True
    if text in ("false", "no", "n", "0", "fail", "failed"):
        return False
    return default


def _title_case_label(value):
    text = _clean_value(value)
    return text[:1].upper() + text[1:] if text else ""


def _recommend_action(classification, task):
    """Derive a plain-language "Now what" for a case from its classification and
    task. Returns {title, steps[]}. Kept out of the auditor-facing labels so the
    pitch never shows "Task 3/5" jargon — task only steers the wording here.
    """
    cls = (classification or "").lower()
    if "coverage gap" in cls:
        if task == 3:
            return dict(
                title="Assign an owner for this embedded control",
                steps=[
                    "Confirm whether coverage exists via external assurance (e.g. a SOC 1 report) before opening a finding.",
                    "If not, name the entity that should own and test this embedded control.",
                    "Add it to the plan or document the owner so it isn't orphaned next cycle.",
                ],
            )
        return dict(
            title="Tighten the handoff scope to the embedded layer",
            steps=[
                "Confirm what the receiving entity actually tests for this risk.",
                "Re-scope the handoff so the embedded control layer is explicitly covered.",
                "Record the control boundary between the two entities.",
            ],
        )
    if "documentation" in cls:
        return dict(
            title="Sharpen the handoff documentation",
            steps=[
                "The handoff prose is too coarse to test cleanly — name the exact risk slice transferred.",
                "Document who owns the risk after the handoff.",
            ],
        )
    if "conform" in cls:
        return dict(title="No action — coverage confirmed", steps=[])
    return dict(title="Review and triage", steps=[])


def _build_controls_lookup(controls_df):
    """One pass over the Archer controls export -> (sr_names, kpa_names,
    controls_by_entity). Risk/KPA id->description are globally 1:1, so flat maps
    are safe; controls are indexed per entity for the receiver-coverage join.
    Returns three empty dicts when the export is absent.
    """
    sr_names, kpa_names, by_entity = {}, {}, {}
    if controls_df is None or controls_df.empty:
        return sr_names, kpa_names, by_entity
    ent_col = "Audit Entity (Audit Controls)"
    for _, r in controls_df.iterrows():
        sr_id = _clean_value(r.get("Key Risk ID"))
        if sr_id and sr_id not in sr_names:
            sr_names[sr_id] = _clean_value(r.get("Key Risk Description"))
        kpa_id = _clean_value(r.get("KPA ID"))
        if kpa_id and kpa_id not in kpa_names:
            kpa_names[kpa_id] = _clean_value(r.get("KPA Description"))
        eid = _clean_value(r.get(ent_col))
        if not eid:
            continue
        by_entity.setdefault(eid, []).append(dict(
            controlId=_clean_value(r.get("Control ID")),
            title=_clean_value(r.get("Control Title")),
            description=_clean_value(r.get("Control Description"))[:240],
            kpaId=kpa_id,
            srId=sr_id,
        ))
    return sr_names, kpa_names, by_entity


def build_pitch2_data(dfs):
    """Build JSON data for the proof-first assurance caseboard."""
    cov_idx = dfs["coverage"].set_index("Audit Entity ID") if not dfs["coverage"].empty else pd.DataFrame()
    dep_idx = dfs["dep_profile"].set_index("Audit Entity ID") if not dfs["dep_profile"].empty else pd.DataFrame()
    # Resolve SR/KPA IDs to plain descriptions and index the receiver's covering
    # controls — so the caseboard reads like Archer without opening Archer.
    sr_names, kpa_names, controls_by_entity = _build_controls_lookup(dfs.get("controls"))

    prose = {}
    src = dfs.get("source")
    if src is not None and "Audit Entity ID" in src.columns:
        hd_col = "Hand-off Description" if "Hand-off Description" in src.columns else None
        ov_col = "Audit Entity Overview" if "Audit Entity Overview" in src.columns else None
        for _, r in src.iterrows():
            eid = _clean_value(r.get("Audit Entity ID"))
            if not eid:
                continue
            prose[eid] = dict(
                handoffDesc=_clean_value(r.get(hd_col)) if hd_col else "",
                overview=_clean_value(r.get(ov_col)) if ov_col else "",
            )

    entities = {}
    for _, row in dfs["nodes"].iterrows():
        eid = _clean_value(row.get("Audit Entity ID"))
        if not eid:
            continue
        c = cov_idx.loc[eid] if eid in cov_idx.index else None
        d = dep_idx.loc[eid] if eid in dep_idx.index else None
        risk = _clean_value(c.get("Overall Residual Risk") if isinstance(c, pd.Series) else "", "N/A")
        if risk == "N/A":
            risk = _clean_value(row.get("Overall Residual Risk Rating"), "N/A")
        p = prose.get(eid, {})
        entities[eid] = dict(
            id=eid,
            name=_clean_value(row.get("Audit Entity Name"), eid),
            auditLeader=_clean_value(row.get("Audit Leader"), "Unknown"),
            businessUnit=_clean_value(row.get("Business Unit"), "Unknown"),
            lineOfDefense=_clean_value(row.get("Line of Defense"), ""),
            pga=_clean_value(row.get("PGA/ASL"), ""),
            horizontalFlag=_clean_value(row.get("Horizontal Flag"), ""),
            risk=risk,
            inScope=_clean_value(c.get("In Scope") if isinstance(c, pd.Series) else "", "No"),
            overdue=_clean_value(c.get("Overdue Flag") if isinstance(c, pd.Series) else "", "No"),
            effectiveFrequency=_clean_value(c.get("Effective Frequency") if isinstance(c, pd.Series) else ""),
            connectivityTotal=_int_value(c.get("Connectivity Total") if isinstance(c, pd.Series) else 0),
            modelExposure=_int_value(c.get("Model Exposure") if isinstance(c, pd.Series) else 0),
            highCriticalRisks=_clean_value(c.get("High/Critical Risks") if isinstance(c, pd.Series) else ""),
            handoffTo=_int_value(d.get("Handoff To Count") if isinstance(d, pd.Series) else 0),
            handoffFrom=_int_value(d.get("Handoff From Count") if isinstance(d, pd.Series) else 0),
            handoffPartners=_split_ids(d.get("Handoff Partner IDs") if isinstance(d, pd.Series) else ""),
            handoffDesc=p.get("handoffDesc", ""),
            overview=p.get("overview", ""),
        )

    handoff_edges = []
    pair_lookup = {}
    for _, row in dfs["edges"].iterrows():
        etype = _clean_value(row.get("Edge Type"))
        if etype not in ("handoff_to", "handoff_from"):
            continue
        edge = dict(
            source=_clean_value(row.get("Entity A ID")),
            target=_clean_value(row.get("Entity B ID")),
            edgeType=etype,
            detail=_clean_value(row.get("Detail")),
        )
        if not edge["source"] or not edge["target"]:
            continue
        handoff_edges.append(edge)
        pair_lookup.setdefault(frozenset((edge["source"], edge["target"])), []).append(edge)

    findings_df = dfs.get("findings")
    findings = []
    if findings_df is not None and not findings_df.empty:
        for idx, row in findings_df.reset_index(drop=True).iterrows():
            source_id = _clean_value(row.get("focal_entity_id"))
            target_id = _clean_value(row.get("cross_entity_partner_id"))
            task = _int_value(row.get("task"), 0)
            classification = _clean_value(row.get("classification"), "unclassified").lower()
            source_ent = entities.get(source_id, dict(
                id=source_id, name=_clean_value(row.get("focal_entity_name"), source_id),
                auditLeader="Unknown", businessUnit="Unknown", lineOfDefense="", pga="",
                horizontalFlag="", risk="N/A", inScope="No", overdue="No",
                effectiveFrequency="", connectivityTotal=0, modelExposure=0,
                highCriticalRisks="", handoffTo=0, handoffFrom=0,
                handoffPartners=[], handoffDesc="", overview="",
            ))
            target_ent = entities.get(target_id) if target_id else None
            related = []
            if target_id:
                related = pair_lookup.get(frozenset((source_id, target_id)), [])
            if not related and source_id:
                related = [
                    e for e in handoff_edges
                    if e["source"] == source_id or e["target"] == source_id
                ][:8]
            findings.append(dict(
                id=f"F-{idx + 1:04d}",
                batchId=_int_value(row.get("batch_id"), 0),
                task=task,
                taskName=_clean_value(row.get("task_name"), f"Task {task}" if task else ""),
                classification=classification,
                classificationLabel=_title_case_label(classification),
                sourceId=source_id,
                sourceName=_clean_value(row.get("focal_entity_name"), source_ent.get("name", source_id)),
                targetId=target_id,
                targetName=target_ent.get("name", target_id) if target_ent else "",
                riskCategory=_clean_value(row.get("risk_category"), "Unspecified"),
                specificRiskIds=_split_ids(row.get("specific_risk_ids")),
                kpaIds=_split_ids(row.get("kpa_ids")),
                evidenceLayer=_clean_value(row.get("evidence_layer"), ""),
                manualRequirement=_clean_value(row.get("manual_requirement"), ""),
                evidenceQuote=_clean_value(row.get("evidence_quote"), ""),
                reasoning=_clean_value(row.get("reasoning"), ""),
                gatePassed=_bool_value(row.get("gate_passed"), True),
                source=source_ent,
                target=target_ent,
                relatedEdges=related,
            ))

    rank = {"likely coverage gap": 0, "documentation issue": 1, "conforms": 2}
    findings.sort(key=lambda f: (
        rank.get(f["classification"], 9),
        0 if f["gatePassed"] else 1,
        0 if f["task"] == 5 else 1,
        f["source"].get("auditLeader", ""),
        f["riskCategory"],
        f["id"],
    ))

    # === Group findings into cases (one gap unit) ===
    # A case = a Task-5 A->B handoff pair, or a Task-3 focal entity (no partner).
    # Aggregating here (in Python) means the map and caseboard share _case_key and
    # never drift. A single A<->B gap can carry several orphaned risks.
    def _resolve(ids, names):
        return [dict(id=i, description=names.get(i, "") or i) for i in ids]

    def _covering_controls(case_srs, case_kpas, receiver_id, cap=6):
        controls = controls_by_entity.get(receiver_id, []) if receiver_id else []
        sr_set, kpa_set = set(case_srs), set(case_kpas)
        hits = [c for c in controls if (c["srId"] and c["srId"] in sr_set)
                or (c["kpaId"] and c["kpaId"] in kpa_set)]
        return hits[:cap], len(hits)

    cases_by_key = {}
    case_order = []
    for f in findings:
        key = _case_key(f["sourceId"], f["targetId"], f["task"])
        f["caseKey"] = key
        c = cases_by_key.get(key)
        if c is None:
            c = dict(
                caseKey=key, task=f["task"],
                sourceId=f["sourceId"], sourceName=f["sourceName"],
                targetId=f["targetId"], targetName=f["targetName"],
                classification=f["classification"], classificationLabel=f["classificationLabel"],
                reasoning="", evidenceQuote="", manualRequirement="", evidenceLayer="",
                riskCategory=f["riskCategory"],
                specificRiskIds=[], kpaIds=[], riskCategories=[],
                findingIds=[], findingCount=0, gatePassed=True,
                source=f["source"], target=f["target"], relatedEdges=f["relatedEdges"],
                handoffDesc=(f["source"] or {}).get("handoffDesc", ""),
            )
            cases_by_key[key] = c
            case_order.append(key)
        # Most-severe member drives the case classification (lowest rank wins).
        if rank.get(f["classification"], 9) < rank.get(c["classification"], 9):
            c["classification"] = f["classification"]
            c["classificationLabel"] = f["classificationLabel"]
        for sr in f["specificRiskIds"]:
            if sr not in c["specificRiskIds"]:
                c["specificRiskIds"].append(sr)
        for kp in f["kpaIds"]:
            if kp not in c["kpaIds"]:
                c["kpaIds"].append(kp)
        if f["riskCategory"] and f["riskCategory"] not in c["riskCategories"]:
            c["riskCategories"].append(f["riskCategory"])
        for fld in ("reasoning", "evidenceQuote", "manualRequirement", "evidenceLayer"):
            if not c[fld] and f[fld]:
                c[fld] = f[fld]
        c["findingIds"].append(f["id"])
        c["findingCount"] += 1
        c["gatePassed"] = c["gatePassed"] and f["gatePassed"]

    cases = []
    for key in case_order:
        c = cases_by_key[key]
        # Receiver whose controls should cover the transferred slice: the partner
        # for a cross-entity handoff (Task 5), else the focal entity (Task 3).
        receiver_id = c["targetId"] if c["task"] == 5 and c["targetId"] else c["sourceId"]
        covering, covering_total = _covering_controls(c["specificRiskIds"], c["kpaIds"], receiver_id)
        c["keyRisks"] = _resolve(c["specificRiskIds"], sr_names)
        c["kpas"] = _resolve(c["kpaIds"], kpa_names)
        c["coveringControls"] = covering
        c["coveringControlsTotal"] = covering_total
        c["recommendedAction"] = _recommend_action(c["classification"], c["task"])
        cases.append(c)

    cases.sort(key=lambda c: (
        rank.get(c["classification"], 9),
        0 if c["gatePassed"] else 1,
        0 if c["task"] == 5 else 1,
        (c["source"] or {}).get("auditLeader", ""),
        c["riskCategory"],
        c["caseKey"],
    ))

    def _count_by(items, key_fn):
        counts = {}
        for item in items:
            key = key_fn(item) or "Unspecified"
            counts[key] = counts.get(key, 0) + 1
        return counts

    return dict(
        generatedAt=datetime.now().isoformat(timespec="seconds"),
        entities=entities,
        findings=findings,
        cases=cases,
        handoffEdges=handoff_edges,
        filters=dict(
            leaders=sorted(_count_by(findings, lambda f: f["source"].get("auditLeader")).keys()),
            classifications=sorted(_count_by(cases, lambda c: c["classification"]).keys()),
            riskCategories=sorted(_count_by(findings, lambda f: f["riskCategory"]).keys()),
            tasks=sorted(set(f["task"] for f in findings if f["task"])),
        ),
        summary=dict(
            totalFindings=len(findings),
            totalCases=len(cases),
            classifications=_count_by(cases, lambda c: c["classification"]),
            leaders=_count_by(findings, lambda f: f["source"].get("auditLeader")),
            riskCategories=_count_by(findings, lambda f: f["riskCategory"]),
            tasks=_count_by(findings, lambda f: f"Task {f['task']}" if f["task"] else "Unspecified"),
        ),
    )


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


def generate(input_dir, output_dir, source_csv=None, controls_csv=None):
    print(f"Reading pipeline files from: {input_dir}")
    dfs = read_pipeline(input_dir, source_csv, controls_csv)
    date_stamp = datetime.now().strftime("%Y%m%d")

    # === Network Visualization ===
    net_data = build_network_data(dfs)
    # The caseboard is a sibling file in output_dir; let map gaps deep-link to it.
    # Must be set BEFORE net_json is serialized (the pitch map reuses net_json).
    pitch2_tpl = os.path.join(_TPL_DIR, "_pitch_template2.html")
    if os.path.isfile(pitch2_tpl):
        net_data["pitch2Href"] = f"network_pitch2_{date_stamp}.html"
    cats_tagged = sum(1 for e in net_data["edges"] if e.get("category") and e["category"] not in ("","UNKNOWN"))
    print(f"  Network: {len(net_data['nodes'])} nodes, {len(net_data['edges'])} edges, {cats_tagged} categorized handoffs")
    if "gapEdgesUnplaced" in net_data:
        gap_edges = sum(1 for e in net_data["edges"] if e.get("gap"))
        gap_nodes = sum(1 for n in net_data["nodes"] if n.get("gap"))
        print(f"  Gaps: {gap_edges} edges (Task 5), {gap_nodes} nodes (Task 3); "
              f"unplaced T5={net_data['gapEdgesUnplaced']}, unmatched T3={net_data['gapNodesUnmatched']}")
        # Counters are for the console only — keep them out of the injected JSON.
        net_data.pop("gapEdgesUnplaced", None)
        net_data.pop("gapNodesUnmatched", None)
    net_json = json.dumps(net_data, separators=(",",":"))
    with open(os.path.join(_TPL_DIR, "_network_template.html"), "r", encoding="utf-8") as f:
        net_html = f.read().replace("%%DATA_INJECTION%%", "const DATA = " + net_json + ";")
    net_path = os.path.join(output_dir, f"network_visualization_{date_stamp}.html")
    with open(net_path, "w", encoding="utf-8") as f: f.write(net_html)
    print(f"  -> {net_path} ({len(net_html):,} bytes)")

    # Pitch build — same data, simplified controls (separate template, optional).
    # pitch_html / pitch2_html are also reused by the combined dashboard below.
    pitch_html = pitch2_html = None
    pitch_tpl = os.path.join(_TPL_DIR, "_pitch_template.html")
    if os.path.isfile(pitch_tpl):
        with open(pitch_tpl, "r", encoding="utf-8") as f:
            pitch_html = f.read().replace("%%DATA_INJECTION%%", "const DATA = " + net_json + ";")
        pitch_path = os.path.join(output_dir, f"network_pitch_{date_stamp}.html")
        with open(pitch_path, "w", encoding="utf-8") as f: f.write(pitch_html)
        print(f"  -> {pitch_path} ({len(pitch_html):,} bytes)")

    # Pitch build 2 — proof-first assurance caseboard (pitch2_tpl defined above).
    if os.path.isfile(pitch2_tpl):
        pitch2_data = build_pitch2_data(dfs)
        gap_cases = pitch2_data["summary"]["classifications"].get("likely coverage gap", 0)
        print(f"  Pitch2: {pitch2_data['summary']['totalCases']} cases "
              f"({len(pitch2_data['findings'])} findings), {gap_cases} likely-gap cases")
        pitch2_json = json.dumps(pitch2_data, separators=(",",":"))
        with open(pitch2_tpl, "r", encoding="utf-8") as f:
            pitch2_html = f.read().replace("%%DATA_INJECTION%%", "const DATA = " + pitch2_json + ";")
        pitch2_path = os.path.join(output_dir, f"network_pitch2_{date_stamp}.html")
        with open(pitch2_path, "w", encoding="utf-8") as f: f.write(pitch2_html)
        print(f"  -> {pitch2_path} ({len(pitch2_html):,} bytes)")

    # Combined dashboard — one self-contained file embedding the map + caseboard as
    # isolated iframes (srcdoc). The map's gap-click bridges to the caseboard drawer via
    # postMessage, so there's no sibling-file dependency. Reuses the strings built above;
    # html.escape(quote=True) is exactly right for a srcdoc attribute (the attribute parser
    # decodes the entities back into the original child document).
    dash_tpl = os.path.join(_TPL_DIR, "_dashboard_template.html")
    if os.path.isfile(dash_tpl) and pitch_html and pitch2_html:
        with open(dash_tpl, "r", encoding="utf-8") as f:
            dash_html = (f.read()
                         .replace("%%MAP_SRCDOC%%", html.escape(pitch_html, quote=True))
                         .replace("%%BOARD_SRCDOC%%", html.escape(pitch2_html, quote=True)))
        dash_path = os.path.join(output_dir, f"network_dashboard_{date_stamp}.html")
        with open(dash_path, "w", encoding="utf-8") as f: f.write(dash_html)
        print(f"  -> {dash_path} ({len(dash_html):,} bytes)")

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
    parser.add_argument("--source", default=None,
                        help="Source universe CSV for entity prose (hand-off description / overview); auto-detected if omitted")
    parser.add_argument("--controls", default=None,
                        help="Archer controls CSV — resolves SR/KPA names + receiver coverage in the caseboard; auto-detected if omitted")
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    generate(args.input_dir, args.output_dir, args.source, args.controls)
