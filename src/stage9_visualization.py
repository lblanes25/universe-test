"""Stage 9: emit a self-contained interactive D3 network visualization."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

RISK_COLORS = {
    "Critical": "#c0392b",
    "High": "#e67e22",
    "Medium": "#f1c40f",
    "Low": "#27ae60",
}
DEFAULT_COLOR = "#95a5a6"


def _build_payload(
    nodes: pd.DataFrame,
    coverage_matrix: pd.DataFrame,
    handoffs: pd.DataFrame,
    entity_app: pd.DataFrame,
    entity_vendor: pd.DataFrame,
    entity_prsa: pd.DataFrame,
    asset_lookup: pd.DataFrame,
    profile: pd.DataFrame,
) -> dict:
    mat = coverage_matrix.set_index("Audit Entity ID")
    prof = profile.set_index("Audit Entity ID") if not profile.empty else pd.DataFrame()

    node_records = []
    for _, n in nodes.iterrows():
        ent = n["Audit Entity ID"]
        m = mat.loc[ent] if ent in mat.index else {}
        p = prof.loc[ent] if not prof.empty and ent in prof.index else {}
        get = lambda obj, key, default="": obj.get(key, default) if isinstance(obj, (dict, pd.Series)) else default
        node_records.append(
            {
                "id": ent,
                "name": n.get("Audit Entity Name", ""),
                "leader": n.get("Audit Leader", "") or "(unassigned)",
                "businessUnit": n.get("Business Unit", ""),
                "horizontal": n.get("Horizontal Flag", ""),
                "risk": n.get("Overall Residual Risk Rating") or "",
                "inScope": str(get(m, "In Scope", "No")) == "Yes",
                "overdue": str(get(m, "Overdue Flag", "")) == "Yes",
                "connectivity": int(get(m, "Connectivity Total", 0) or 0),
                "handoffTo": int(get(p, "Handoff To Count", 0) or 0),
                "handoffFrom": int(get(p, "Handoff From Count", 0) or 0),
                "hcRisks": str(get(m, "High/Critical Risks", "")),
            }
        )

    node_ids = set(nodes["Audit Entity ID"])
    handoff_edges = []
    if not handoffs.empty:
        seen = set()
        for _, r in handoffs.iterrows():
            s, t, d = r["Source Entity ID"], r["Target Entity ID"], r["Direction"]
            if s not in node_ids or t not in node_ids:
                continue
            key = (s, t)
            if key in seen:
                continue
            seen.add(key)
            handoff_edges.append({"source": s, "target": t, "type": "handoff", "direction": d})

    def _shared(table: pd.DataFrame, attr: str, etype: str) -> list[dict]:
        if table.empty:
            return []
        out = []
        dedup = table.drop_duplicates(subset=["Audit Entity ID", attr])
        for value, grp in dedup.groupby(attr):
            ents = sorted(grp["Audit Entity ID"].unique())
            for i in range(len(ents)):
                for j in range(i + 1, len(ents)):
                    out.append({"source": ents[i], "target": ents[j], "type": etype, "detail": value})
        return out

    shared_app = _shared(entity_app, "Application Name", "shared_app")
    shared_vendor = _shared(entity_vendor, "Third Party Name", "shared_vendor")
    shared_prsa = _shared(entity_prsa, "PRSA Value", "shared_prsa")

    assets = []
    if not asset_lookup.empty:
        for _, a in asset_lookup.iterrows():
            if a["Asset Type"] == "Model":
                continue
            assets.append(
                {
                    "name": a["Asset Name"],
                    "type": a["Asset Type"],
                    "dependents": a["Dependent Entity IDs"].split(";") if a["Dependent Entity IDs"] else [],
                    "primaryCount": int(a.get("Primary Count", 0) or 0),
                    "dependentCount": int(a.get("Dependent Entity Count", 0) or 0),
                }
            )

    primary_owners: dict[str, list[str]] = {}
    for tbl, col, typ in [
        (entity_app, "Application Name", "Application"),
        (entity_vendor, "Third Party Name", "Vendor"),
    ]:
        if tbl.empty or "Relationship" not in tbl.columns:
            continue
        prim = tbl[tbl["Relationship"] == "primary"]
        for _, r in prim.iterrows():
            primary_owners.setdefault(f"{typ}::{r[col]}", []).append(r["Audit Entity ID"])

    return {
        "nodes": node_records,
        "edges": handoff_edges + shared_app + shared_vendor + shared_prsa,
        "assets": assets,
        "primaryOwners": primary_owners,
    }


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Audit Universe Network — Grouped by Audit Leader</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  :root { --bg:#fafafa; --panel:#fff; --border:#ddd; --text:#222; --muted:#666; }
  body { margin:0; font-family: "Segoe UI", Arial, sans-serif; background:var(--bg); color:var(--text); }
  #layout { display:flex; height:100vh; }
  #sidebar { width:300px; padding:14px 16px; background:var(--panel); border-right:1px solid var(--border); overflow-y:auto; }
  #sidebar h1 { font-size:16px; margin:0 0 2px; }
  #sidebar .sub { font-size:11px; color:var(--muted); margin-bottom:14px; line-height:1.4; }
  #main { flex:1; position:relative; }
  svg { width:100%; height:100%; background:var(--bg); }
  fieldset { border:1px solid var(--border); border-radius:4px; margin:0 0 12px; padding:8px 10px; }
  legend { font-size:11px; font-weight:600; color:var(--muted); text-transform:uppercase; letter-spacing:0.5px; padding:0 4px; }
  label { display:block; font-size:12px; margin:3px 0; }
  select, input[type=text] { width:100%; font-size:12px; padding:4px; box-sizing:border-box; }
  button { font-size:12px; padding:4px 8px; margin:2px 2px 2px 0; cursor:pointer; }
  button.active { background:#2c3e50; color:#fff; border-color:#2c3e50; }
  #legend { margin-top:6px; font-size:11px; }
  #legend .row { display:flex; align-items:center; gap:6px; margin:2px 0; }
  #legend .swatch { width:14px; height:14px; border:1px solid #555; }
  #tooltip { position:absolute; pointer-events:none; background:rgba(255,255,255,0.97); border:1px solid #888; border-radius:4px; padding:8px 10px; font-size:11px; max-width:280px; box-shadow:0 2px 6px rgba(0,0,0,0.15); display:none; z-index:10; }
  #tooltip strong { display:block; font-size:12px; margin-bottom:3px; }
  #assetPanel { font-size:11px; background:#f0f4f8; border:1px solid #c6d4e0; padding:8px; margin-top:8px; display:none; }
  .hull { fill-opacity:0.10; stroke-opacity:0.35; stroke-width:1.5; }
  .hull-label { font-size:11px; fill:#555; pointer-events:none; font-weight:600; }
  .edge { stroke:#666; stroke-opacity:0.55; fill:none; }
  .edge.shared_app { stroke:#3498db; stroke-opacity:0.5; stroke-width:1; }
  .edge.shared_vendor { stroke:#e67e22; stroke-opacity:0.5; stroke-width:1; }
  .edge.shared_prsa { stroke:#9b59b6; stroke-opacity:0.3; stroke-width:1; stroke-dasharray:2 3; }
  .edge.handoff { stroke:#666; stroke-width:1.5; }
  .edge.inbound { stroke:#2980b9; stroke-width:2; stroke-opacity:0.9; }
  .node { stroke:#222; stroke-width:1; cursor:pointer; }
  .node.overdue-diamond { stroke:#111; stroke-width:2.5; }
  .node.primary-owner { stroke:#c59b00; stroke-width:2.5; }
  .node.external-impact { fill:#2980b9 !important; }
  .node-label { font-size:10px; fill:#222; pointer-events:none; text-anchor:middle; }
  .dim { opacity:0.12; }
</style>
</head>
<body>
<div id="layout">
  <div id="sidebar">
    <h1>Audit Universe Network</h1>
    <div class="sub">Default view: handoff edges only. Toggle shared assets in the control panel. Node size = connectivity. Color = residual risk rating. Shape = audit plan coverage.</div>

    <fieldset><legend>Edge Types</legend>
      <label><input type="checkbox" id="tog_handoff" checked> Handoffs</label>
      <label><input type="checkbox" id="tog_shared_app"> Shared Applications</label>
      <label><input type="checkbox" id="tog_shared_vendor"> Shared Vendors</label>
      <label><input type="checkbox" id="tog_shared_prsa"> Shared PRSAs</label>
    </fieldset>

    <fieldset><legend>Audit Leader Filter</legend>
      <select id="leaderFilter"><option value="">(all leaders)</option></select>
      <label style="margin-top:6px"><input type="checkbox" id="portfolioMode"> Portfolio + Inbound Impact</label>
    </fieldset>

    <fieldset><legend>Application / Vendor Focus</legend>
      <select id="assetFocus"><option value="">(none)</option></select>
      <div id="assetPanel"></div>
    </fieldset>

    <fieldset><legend>Coverage Filter</legend>
      <button data-cov="all" class="active">All</button>
      <button data-cov="notin">Not In Scope</button>
      <button data-cov="overdue">Overdue</button>
    </fieldset>

    <fieldset><legend>Search</legend>
      <input type="text" id="searchBox" placeholder="Entity ID or name"/>
    </fieldset>

    <button id="resetView">Reset view</button>

    <fieldset style="margin-top:14px"><legend>Legend</legend>
      <div id="legend"></div>
    </fieldset>
  </div>
  <div id="main">
    <svg id="viz"></svg>
    <div id="tooltip"></div>
  </div>
</div>

<script>
const DATA = __DATA__;

const RISK_COLOR = {
  "Critical":"#c0392b","High":"#e67e22","Medium":"#f1c40f","Low":"#27ae60"
};
const DEFAULT_COLOR = "#95a5a6";

const svg = d3.select("#viz");
const tooltip = d3.select("#tooltip");
let width = document.getElementById("main").clientWidth;
let height = document.getElementById("main").clientHeight;
svg.attr("viewBox", [0, 0, width, height]);

const gRoot = svg.append("g");
const gHulls = gRoot.append("g");
const gEdges = gRoot.append("g");
const gNodes = gRoot.append("g");
const gLabels = gRoot.append("g");

const zoom = d3.zoom().scaleExtent([0.15, 5]).on("zoom", (ev) => {
  gRoot.attr("transform", ev.transform);
  updateLabelVisibility(ev.transform.k);
});
svg.call(zoom);

// --- Prepare node data with size scaling
const maxConn = d3.max(DATA.nodes, d => d.connectivity) || 1;
const sizeScale = d3.scaleSqrt().domain([0, maxConn]).range([6, 22]);
DATA.nodes.forEach(n => {
  n.r = sizeScale(n.connectivity);
  n.color = RISK_COLOR[n.risk] || DEFAULT_COLOR;
});

// --- Group by audit leader, assign cluster anchor points
const leaders = Array.from(new Set(DATA.nodes.map(n => n.leader))).sort();
const nCols = Math.ceil(Math.sqrt(leaders.length));
const cellW = width / nCols;
const cellH = height / Math.ceil(leaders.length / nCols);
const anchors = {};
leaders.forEach((lead, i) => {
  anchors[lead] = {
    x: ((i % nCols) + 0.5) * cellW,
    y: (Math.floor(i / nCols) + 0.5) * cellH,
  };
});
DATA.nodes.forEach(n => {
  const a = anchors[n.leader];
  n.x = a.x + (Math.random() - 0.5) * 40;
  n.y = a.y + (Math.random() - 0.5) * 40;
});

// --- Build edge references by lookup map
const nodeById = new Map(DATA.nodes.map(n => [n.id, n]));
DATA.edges.forEach(e => { e.s = nodeById.get(e.source); e.t = nodeById.get(e.target); });
const validEdges = DATA.edges.filter(e => e.s && e.t);

// --- Populate audit leader filter and asset focus dropdowns
const leaderSel = document.getElementById("leaderFilter");
leaders.forEach(l => { const o = document.createElement("option"); o.value = l; o.textContent = l; leaderSel.appendChild(o); });
const assetSel = document.getElementById("assetFocus");
DATA.assets.slice().sort((a,b)=>b.dependentCount-a.dependentCount).forEach(a => {
  const o = document.createElement("option");
  o.value = a.type + "::" + a.name;
  o.textContent = `[${a.type[0]}] ${a.name} (${a.dependentCount})`;
  assetSel.appendChild(o);
});

// --- Force simulation (positions only; radial cluster attraction)
const sim = d3.forceSimulation(DATA.nodes)
  .force("charge", d3.forceManyBody().strength(-70))
  .force("collide", d3.forceCollide().radius(d => d.r + 2))
  .force("x", d3.forceX(d => anchors[d.leader].x).strength(0.15))
  .force("y", d3.forceY(d => anchors[d.leader].y).strength(0.15))
  .force("link", d3.forceLink(validEdges.filter(e => e.type === "handoff")).id(d => d.id).distance(40).strength(0.2))
  .on("tick", ticked);

for (let i = 0; i < 200; i++) sim.tick();
sim.alpha(0.5).restart();

// --- Rendering
const edgeSel = gEdges.selectAll("line")
  .data(validEdges)
  .enter().append("line")
  .attr("class", d => "edge " + d.type)
  .attr("marker-end", d => d.type === "handoff" ? "url(#arrow)" : null);

// arrowhead
svg.append("defs").append("marker").attr("id","arrow")
  .attr("viewBox","0 -5 10 10").attr("refX",14).attr("refY",0)
  .attr("markerWidth",6).attr("markerHeight",6).attr("orient","auto")
  .append("path").attr("d","M0,-5L10,0L0,5").attr("fill","#666");
svg.select("defs").append("marker").attr("id","arrow-in")
  .attr("viewBox","0 -5 10 10").attr("refX",14).attr("refY",0)
  .attr("markerWidth",6).attr("markerHeight",6).attr("orient","auto")
  .append("path").attr("d","M0,-5L10,0L0,5").attr("fill","#2980b9");

const diamondPath = r => `M0,${-r} L${r},0 L0,${r} L${-r},0 Z`;

const nodeSel = gNodes.selectAll("path")
  .data(DATA.nodes)
  .enter().append("path")
  .attr("class", "node")
  .attr("fill", d => d.color)
  .on("mouseover", (ev, d) => {
    tooltip.style("display","block").html(tooltipHtml(d));
  })
  .on("mousemove", (ev) => {
    tooltip.style("left", (ev.offsetX + 18) + "px").style("top", (ev.offsetY + 12) + "px");
  })
  .on("mouseout", () => tooltip.style("display","none"))
  .call(d3.drag()
    .on("start", (ev,d) => { if (!ev.active) sim.alphaTarget(0.3).restart(); d.fx=d.x; d.fy=d.y; })
    .on("drag", (ev,d) => { d.fx=ev.x; d.fy=ev.y; })
    .on("end", (ev,d) => { if (!ev.active) sim.alphaTarget(0); d.fx=null; d.fy=null; }));

const labelSel = gLabels.selectAll("text")
  .data(DATA.nodes)
  .enter().append("text")
  .attr("class","node-label")
  .text(d => d.id);

function tooltipHtml(d) {
  return `<strong>${d.id} — ${d.name}</strong>
    Leader: ${d.leader}<br>
    Business Unit: ${d.businessUnit}<br>
    Connectivity: ${d.connectivity} (→${d.handoffTo}, ←${d.handoffFrom})<br>
    Residual Risk: ${d.risk || 'N/A'}<br>
    In Scope: ${d.inScope ? 'Yes' : 'No'}${d.overdue ? ' — <b>Overdue</b>' : ''}<br>
    ${d.hcRisks ? 'H/C Risks: ' + d.hcRisks : ''}`;
}

function ticked() {
  edgeSel
    .attr("x1", d => d.s.x).attr("y1", d => d.s.y)
    .attr("x2", d => d.t.x).attr("y2", d => d.t.y);
  nodeSel.attr("transform", d => `translate(${d.x},${d.y})`);
  labelSel.attr("x", d => d.x).attr("y", d => d.y - d.r - 3);
  drawHulls();
}

// --- Convex hulls per leader
function drawHulls() {
  const groups = d3.group(DATA.nodes.filter(n => !n.hidden), d => d.leader);
  const hullData = [];
  const labelData = [];
  groups.forEach((arr, lead) => {
    if (arr.length < 1) return;
    const pts = arr.flatMap(n => [[n.x - n.r - 6, n.y], [n.x + n.r + 6, n.y], [n.x, n.y - n.r - 6], [n.x, n.y + n.r + 6]]);
    const hull = pts.length >= 3 ? d3.polygonHull(pts) : null;
    const cx = d3.mean(arr, n => n.x);
    const cy = d3.min(arr, n => n.y) - 12;
    labelData.push({leader: lead, x: cx, y: cy});
    if (hull) hullData.push({leader: lead, hull});
  });
  const color = d3.scaleOrdinal(d3.schemeCategory10).domain(leaders);
  const hSel = gHulls.selectAll("path.hull").data(hullData, d => d.leader);
  hSel.enter().append("path").attr("class","hull")
    .merge(hSel)
    .attr("d", d => "M" + d.hull.join("L") + "Z")
    .attr("fill", d => color(d.leader)).attr("stroke", d => color(d.leader));
  hSel.exit().remove();
  const lSel = gHulls.selectAll("text.hull-label").data(labelData, d => d.leader);
  lSel.enter().append("text").attr("class","hull-label").attr("text-anchor","middle")
    .merge(lSel).attr("x", d => d.x).attr("y", d => d.y).text(d => d.leader);
  lSel.exit().remove();
}

// --- Controls state
const state = {
  show: { handoff: true, shared_app: false, shared_vendor: false, shared_prsa: false },
  leader: "",
  portfolio: false,
  asset: "",
  coverage: "all",
  search: "",
};

function applyFilters() {
  // Decide which nodes are visible.
  DATA.nodes.forEach(n => { n.hidden = false; n.external = false; n.highlight = false; });

  let portfolioIds = null;
  if (state.leader) {
    portfolioIds = new Set(DATA.nodes.filter(n => n.leader === state.leader).map(n => n.id));
    let allowed = new Set(portfolioIds);
    if (state.portfolio) {
      validEdges.forEach(e => {
        if (e.type === "handoff" && e.direction === "to" && portfolioIds.has(e.t.id) && !portfolioIds.has(e.s.id)) {
          allowed.add(e.s.id);
        }
      });
    }
    DATA.nodes.forEach(n => {
      if (!allowed.has(n.id)) n.hidden = true;
      else if (!portfolioIds.has(n.id)) n.external = true;
    });
  }

  if (state.asset) {
    const asset = DATA.assets.find(a => (a.type + "::" + a.name) === state.asset);
    if (asset) {
      const keep = new Set(asset.dependents);
      DATA.nodes.forEach(n => { if (!keep.has(n.id)) n.hidden = true; });
      const owners = new Set(DATA.primaryOwners[state.asset] || []);
      DATA.nodes.forEach(n => { if (owners.has(n.id)) n.highlight = true; });
      renderAssetPanel(asset);
    }
  } else {
    document.getElementById("assetPanel").style.display = "none";
  }

  if (state.coverage === "notin") {
    DATA.nodes.forEach(n => { if (n.inScope) n.hidden = true; });
  } else if (state.coverage === "overdue") {
    DATA.nodes.forEach(n => { if (!n.overdue) n.hidden = true; });
  }

  if (state.search) {
    const q = state.search.toLowerCase();
    const matches = new Set(DATA.nodes.filter(n => n.id.toLowerCase().includes(q) || (n.name||"").toLowerCase().includes(q)).map(n => n.id));
    const neighbors = new Set(matches);
    validEdges.forEach(e => { if (matches.has(e.s.id)) neighbors.add(e.t.id); if (matches.has(e.t.id)) neighbors.add(e.s.id); });
    DATA.nodes.forEach(n => { if (!neighbors.has(n.id)) n.hidden = true; n.highlight = n.highlight || matches.has(n.id); });
  }

  const visibleIds = new Set(DATA.nodes.filter(n => !n.hidden).map(n => n.id));

  nodeSel
    .attr("d", d => d.inScope ? `M0,0 m${-d.r},0 a${d.r},${d.r} 0 1,0 ${d.r*2},0 a${d.r},${d.r} 0 1,0 ${-d.r*2},0` : diamondPath(d.r))
    .classed("overdue-diamond", d => !d.inScope && d.overdue)
    .classed("primary-owner", d => d.highlight)
    .classed("external-impact", d => d.external)
    .style("display", d => d.hidden ? "none" : null)
    .attr("fill", d => d.external ? "#2980b9" : d.color);

  labelSel.style("display", d => d.hidden ? "none" : null);

  edgeSel
    .style("display", e => {
      if (!visibleIds.has(e.s.id) || !visibleIds.has(e.t.id)) return "none";
      if (!state.show[e.type]) return "none";
      return null;
    })
    .classed("inbound", e => e.type === "handoff" && state.leader && portfolioIds && portfolioIds.has(e.t.id) && !portfolioIds.has(e.s.id))
    .attr("marker-end", e => {
      if (e.type !== "handoff") return null;
      if (state.leader && portfolioIds && portfolioIds.has(e.t.id) && !portfolioIds.has(e.s.id)) return "url(#arrow-in)";
      return "url(#arrow)";
    });

  drawHulls();
}

function renderAssetPanel(asset) {
  const p = document.getElementById("assetPanel");
  p.style.display = "block";
  const inScope = asset.dependents.filter(id => { const n = nodeById.get(id); return n && n.inScope; }).length;
  const notIn = asset.dependents.length - inScope;
  const byRisk = {};
  asset.dependents.forEach(id => { const n = nodeById.get(id); if (!n) return; const r = n.risk || "N/A"; byRisk[r] = (byRisk[r]||0)+1; });
  const riskLines = Object.entries(byRisk).map(([k,v])=>`${k}: ${v}`).join(", ");
  const owners = (DATA.primaryOwners[asset.type+"::"+asset.name]||[]).join(", ");
  p.innerHTML = `<strong>${asset.name}</strong><br>
    Type: ${asset.type}<br>
    Dependents: ${asset.dependentCount} (in scope ${inScope}, not ${notIn})<br>
    Primary owner(s): ${owners || "—"}<br>
    Risk mix: ${riskLines || "—"}`;
}

function updateLabelVisibility(k) {
  if (k < 0.5) labelSel.style("visibility","hidden");
  else { labelSel.style("visibility","visible").text(d => k > 1.5 ? d.name : d.id); }
}

// --- Wire controls
["handoff","shared_app","shared_vendor","shared_prsa"].forEach(t => {
  document.getElementById("tog_" + t).addEventListener("change", (e) => { state.show[t] = e.target.checked; applyFilters(); });
});
leaderSel.addEventListener("change", (e) => { state.leader = e.target.value; applyFilters(); });
document.getElementById("portfolioMode").addEventListener("change", (e) => { state.portfolio = e.target.checked; applyFilters(); });
assetSel.addEventListener("change", (e) => { state.asset = e.target.value; applyFilters(); });
document.querySelectorAll("button[data-cov]").forEach(b => {
  b.addEventListener("click", () => {
    document.querySelectorAll("button[data-cov]").forEach(x => x.classList.remove("active"));
    b.classList.add("active");
    state.coverage = b.dataset.cov;
    applyFilters();
  });
});
document.getElementById("searchBox").addEventListener("input", (e) => { state.search = e.target.value; applyFilters(); });
document.getElementById("resetView").addEventListener("click", () => {
  state.show = { handoff:true, shared_app:false, shared_vendor:false, shared_prsa:false };
  state.leader = ""; state.portfolio = false; state.asset = ""; state.coverage = "all"; state.search = "";
  document.getElementById("tog_handoff").checked = true;
  ["shared_app","shared_vendor","shared_prsa"].forEach(k => document.getElementById("tog_"+k).checked = false);
  document.getElementById("portfolioMode").checked = false;
  leaderSel.value = ""; assetSel.value = ""; document.getElementById("searchBox").value = "";
  document.querySelectorAll("button[data-cov]").forEach(x => x.classList.toggle("active", x.dataset.cov === "all"));
  svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity);
  applyFilters();
});

// --- Legend
const legendEl = document.getElementById("legend");
function legendRow(swatchHtml, label) {
  const d = document.createElement("div"); d.className="row";
  d.innerHTML = swatchHtml + `<span>${label}</span>`; legendEl.appendChild(d);
}
["Critical","High","Medium","Low"].forEach(r => legendRow(`<div class="swatch" style="background:${RISK_COLOR[r]}"></div>`, `Risk: ${r}`));
legendRow(`<div class="swatch" style="background:${DEFAULT_COLOR}"></div>`, "Risk: N/A");
legendRow(`<svg width="14" height="14"><circle cx="7" cy="7" r="6" fill="#888" stroke="#222"/></svg>`, "Circle = In Scope");
legendRow(`<svg width="14" height="14"><path d="M7,1 L13,7 L7,13 L1,7 Z" fill="#888" stroke="#222"/></svg>`, "Diamond = Not In Scope");
legendRow(`<svg width="14" height="14"><path d="M7,1 L13,7 L7,13 L1,7 Z" fill="#888" stroke="#111" stroke-width="2.5"/></svg>`, "Thick border = Overdue");
legendRow(`<svg width="20" height="6"><line x1="0" y1="3" x2="20" y2="3" stroke="#666" stroke-width="2"/></svg>`, "Handoff (directional)");
legendRow(`<svg width="20" height="6"><line x1="0" y1="3" x2="20" y2="3" stroke="#3498db" stroke-width="1.5" opacity="0.6"/></svg>`, "Shared Application");
legendRow(`<svg width="20" height="6"><line x1="0" y1="3" x2="20" y2="3" stroke="#e67e22" stroke-width="1.5" opacity="0.6"/></svg>`, "Shared Vendor");
legendRow(`<svg width="20" height="6"><line x1="0" y1="3" x2="20" y2="3" stroke="#9b59b6" stroke-width="1.5" stroke-dasharray="2 3" opacity="0.6"/></svg>`, "Shared PRSA");
legendRow(`<span style="font-size:10px;color:#666">Size = connectivity</span>`, "");

window.addEventListener("resize", () => {
  width = document.getElementById("main").clientWidth;
  height = document.getElementById("main").clientHeight;
  svg.attr("viewBox", [0,0,width,height]);
});

applyFilters();
updateLabelVisibility(1);
</script>
</body>
</html>
"""


def build_visualization(
    output_path: Path,
    nodes: pd.DataFrame,
    coverage_matrix: pd.DataFrame,
    handoffs: pd.DataFrame,
    entity_app: pd.DataFrame,
    entity_vendor: pd.DataFrame,
    entity_prsa: pd.DataFrame,
    asset_lookup: pd.DataFrame,
    profile: pd.DataFrame,
) -> None:
    payload = _build_payload(
        nodes, coverage_matrix, handoffs, entity_app, entity_vendor, entity_prsa, asset_lookup, profile
    )
    html = HTML_TEMPLATE.replace("__DATA__", json.dumps(payload))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
