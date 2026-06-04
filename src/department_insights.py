"""Department-wide insights — fuse the Stage 2 LLM handoff-reliance findings
with the structural Layer 1-2 coverage outputs.

The two bodies of evidence are decision-grade only when triangulated: an
LLM-flagged *likely coverage gap* on an entity that structure also says is
under-covered (not in plan / overdue / a concentration owner) is a far
stronger signal than either layer alone. This module computes that fusion and
emits two deliverables:

  - data/output/department_insights_YYYYMMDD.xlsx   (reviewer workbook)
  - data/output/department_scorecard_YYYYMMDD.html  (deck-ready one-pager)

Design rules (kept deliberately honest):
  * Rates with explicit denominators, not raw counts.
  * Two tiers kept separate: structural = defensible; LLM = candidate leads
    needing human verification. Never blurred.
  * Confidence gating up front (gate-pass rate, evidence-layer mix) plus the
    standing control-description-trim false-positive caveat.

Reuses, not duplicates:
  - summarize_findings: _parse_gate_log, _load_nodes, _classification_value,
    _by_requirement, _by_risk_category
  - labels: task/classification/requirement/evidence-layer display maps
  - utils.excel_writer.write_workbook (blue-header formatting + flag fills)

Usage:
    python -m src.department_insights
    python -m src.department_insights --input-dir data/output --out-dir data/output
"""
from __future__ import annotations

import argparse
import glob
import html
import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utils.excel_writer import write_workbook  # noqa: E402
from src.stage2_handoff_review import labels  # noqa: E402
from src.stage2_handoff_review.summarize_findings import (  # noqa: E402
    _parse_gate_log,
    _load_nodes,
    _classification_value,
    _by_requirement,
    _by_risk_category,
)

DEFAULT_INPUT_DIR = ROOT / "data" / "output"
DEFAULT_OUT_DIR = ROOT / "data" / "output"
DEFAULT_FINDINGS_CSV = ROOT / "runs" / "stage2" / "aggregated" / "findings.csv"
DEFAULT_GATE_LOG = ROOT / "runs" / "stage2" / "aggregated" / "gate_log.md"
DEFAULT_BATCHES_DIR = ROOT / "runs" / "stage2" / "batches"

# Match the network viz palette so the scorecard reads as the same tool.
RISK_COLORS = {
    "Critical": "#c0392b", "High": "#e67e22", "Medium": "#f1c40f",
    "Low": "#27ae60", "N/A": "#95a5a6",
}


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
def _latest(input_dir: Path, base: str, ext: str = ".xlsx") -> Path | None:
    """Latest base_YYYYMMDD.ext, falling back to base.ext (mirrors viz)."""
    matches = sorted(glob.glob(str(input_dir / f"{base}_*{ext}")), reverse=True)
    if matches:
        return Path(matches[0])
    fallback = input_dir / f"{base}{ext}"
    return fallback if fallback.is_file() else None


def _load_findings(input_dir: Path) -> pd.DataFrame:
    """Prefer findings_rollup.xlsx 'All Findings (Tagged)' (already carries
    gate_passed + task_name); fall back to findings.csv + gate log."""
    rollup = _latest(input_dir, "findings_rollup")
    if rollup is None and (input_dir / "findings_rollup.xlsx").is_file():
        rollup = input_dir / "findings_rollup.xlsx"
    agg_rollup = ROOT / "runs" / "stage2" / "aggregated" / "findings_rollup.xlsx"
    for cand in (rollup, agg_rollup):
        if cand and cand.is_file():
            try:
                df = pd.read_excel(cand, sheet_name="All Findings (Tagged)")
                print(f"[dept] findings: {cand}")
                return _ensure_finding_cols(df)
            except Exception:
                pass
    if DEFAULT_FINDINGS_CSV.is_file():
        df = pd.read_csv(DEFAULT_FINDINGS_CSV)
        gate = _parse_gate_log(DEFAULT_GATE_LOG)
        if gate:
            df["gate_passed"] = df["batch_id"].map(gate).fillna(False).astype(bool)
        else:
            df["gate_passed"] = True
        print(f"[dept] findings: {DEFAULT_FINDINGS_CSV} (csv fallback)")
        return _ensure_finding_cols(df)
    raise FileNotFoundError(
        "No findings_rollup.xlsx or findings.csv found. Run Stage 2 aggregation first."
    )


def _ensure_finding_cols(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["classification"] = df.get("classification", "").fillna("").astype(str)
    if "gate_passed" not in df.columns:
        df["gate_passed"] = True
    df["gate_passed"] = df["gate_passed"].fillna(True).astype(bool)
    if "task_name" not in df.columns and "task" in df.columns:
        td = labels.task_displays()
        df["task_name"] = df["task"].map(
            lambda t: td.get(int(t), "") if pd.notna(t) and str(t).strip() != "" else ""
        ).fillna("")
    return df


def _load_layer2(input_dir: Path) -> dict[str, pd.DataFrame]:
    l2 = _latest(input_dir, "layer2_coverage_matrix")
    if l2 is None:
        raise FileNotFoundError(f"layer2_coverage_matrix_*.xlsx not found in {input_dir}")
    xl = pd.ExcelFile(l2)
    print(f"[dept] coverage: {l2}")
    out = {
        "matrix": pd.read_excel(xl, "Coverage Matrix"),
        "summary": pd.read_excel(xl, "Coverage Summary"),
    }
    out["flags"] = pd.read_excel(xl, "Coverage Flags") if "Coverage Flags" in xl.sheet_names else pd.DataFrame()
    out["conc"] = (pd.read_excel(xl, "Concentration Risk Detail")
                   if "Concentration Risk Detail" in xl.sheet_names else pd.DataFrame())
    return out


def _load_ranked_summary(batches_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Roll up the per-batch ranked_summary narrative buckets across all batches.

    These live only in each batch's response.json and are never aggregated
    elsewhere. Returns (systemic_doc_issues, manual_gaps) frames.
    """
    sys_rows: dict[str, dict] = {}
    man_rows: dict[str, dict] = {}
    for resp in sorted(glob.glob(str(batches_dir / "batch_*" / "response.json"))):
        try:
            data = json.loads(Path(resp).read_text(encoding="utf-8"))
        except Exception:
            continue
        rs = data.get("ranked_summary", {}) or {}
        for it in rs.get("systemic_documentation_issues", []) or []:
            key = str(it.get("pattern", "")).strip() or "(unspecified)"
            r = sys_rows.setdefault(key, {"pattern": key, "summary": str(it.get("summary", "")).strip(),
                                          "affected_entity_count": 0, "batches_mentioning": 0})
            try:
                r["affected_entity_count"] += int(it.get("affected_entity_count", 0) or 0)
            except (TypeError, ValueError):
                pass
            r["batches_mentioning"] += 1
        for it in rs.get("manual_gaps_exposed", []) or []:
            key = str(it.get("area", "")).strip() or "(unspecified)"
            r = man_rows.setdefault(key, {"area": key, "summary": str(it.get("summary", "")).strip(),
                                          "batches_mentioning": 0})
            r["batches_mentioning"] += 1
    sys_df = pd.DataFrame(sorted(sys_rows.values(), key=lambda d: -d["affected_entity_count"]))
    man_df = pd.DataFrame(sorted(man_rows.values(), key=lambda d: -d["batches_mentioning"]))
    return sys_df, man_df


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _summary_val(summary: pd.DataFrame, metric: str, default="—"):
    hit = summary[summary["Metric"] == metric]
    return hit["Value"].iloc[0] if not hit.empty else default


def _yes(v) -> bool:
    return str(v).strip().lower() in ("yes", "true", "1")


def _gaps_only(findings: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    gap_value = _classification_value("coverage gap")
    gaps = findings[findings["classification"].str.lower().eq(gap_value.lower())].copy()
    return gaps, gap_value


def _short(text, n=160) -> str:
    s = str(text or "").strip().replace("\n", " ")
    return s[: n - 1] + "…" if len(s) > n else s


# --------------------------------------------------------------------------- #
# Section 3 — fusion
# --------------------------------------------------------------------------- #
def _build_fusion(findings: pd.DataFrame, layer2: dict, nodes: pd.DataFrame | None):
    """Join likely-gap findings to the Coverage Matrix per focal entity and
    derive the priority worklist + the cross-tab counts."""
    gaps, _ = _gaps_only(findings)
    matrix = layer2["matrix"]
    cov = matrix.set_index(matrix["Audit Entity ID"].astype(str))
    conc = layer2["conc"]
    owners = set(conc["Primary Entity"].astype(str)) if not conc.empty and "Primary Entity" in conc else set()
    leader_by = {}
    if nodes is not None and "audit_leader" in nodes.columns:
        leader_by = dict(zip(nodes["focal_entity_id"].astype(str), nodes["audit_leader"].astype(str)))

    # T5 receiving-entity exposure: A->B gap where B is not in plan.
    t5 = gaps[pd.to_numeric(gaps["task"], errors="coerce") == 5]
    partner_not_in_plan: dict[str, set] = {}
    for _, r in t5.iterrows():
        focal = str(r["focal_entity_id"]).strip()
        partner = r.get("cross_entity_partner_id")
        partner = str(partner).strip() if partner is not None and pd.notna(partner) else ""
        if partner and partner in cov.index and not _yes(cov.loc[partner, "In Scope"]):
            partner_not_in_plan.setdefault(focal, set()).add(partner)

    rows = []
    for eid, grp in gaps.groupby(gaps["focal_entity_id"].astype(str)):
        c = cov.loc[eid] if eid in cov.index else None
        in_plan = _yes(c["In Scope"]) if c is not None else None
        overdue = _yes(c["Overdue Flag"]) if c is not None else False
        # "Not rated" (not "N/A") because pandas.read_excel coerces the "N/A"
        # string back to NaN on round-trip; this also reads honestly when the
        # Overall Residual Risk column is genuinely absent/blank.
        risk = str(c["Overall Residual Risk"]).strip() if c is not None and pd.notna(c.get("Overall Residual Risk")) else "Not rated"
        conn = c["Connectivity Total"] if c is not None and pd.notna(c.get("Connectivity Total")) else ""
        is_owner = eid in owners
        bad_partners = partner_not_in_plan.get(eid, set())

        reasons = []
        if in_plan is False:
            reasons.append("Not in this year's plan")
        if overdue:
            reasons.append("Overdue")
        if is_owner:
            reasons.append("Concentration control owner")
        if bad_partners:
            reasons.append(f"Receiving entity not in plan ({', '.join(sorted(bad_partners))})")
        understates = risk in ("Low", "Medium")

        # Priority: a gap nobody is auditing, compounded by another structural
        # signal, is HIGH; an unaudited-or-otherwise-exposed gap is MEDIUM; an
        # in-plan gap (already being looked at) is LOW.
        high = (in_plan is False) and (overdue or is_owner or bool(bad_partners))
        med = (in_plan is False) or is_owner or overdue or bool(bad_partners)
        priority = "HIGH" if high else ("MEDIUM" if med else "LOW")

        sr_ids: list[str] = []
        for v in grp.get("specific_risk_ids", pd.Series(dtype=object)):
            for sr in str(v or "").replace(",", ";").split(";"):
                sr = sr.strip()
                if sr and sr.lower() != "nan" and sr not in sr_ids:
                    sr_ids.append(sr)
        tasks = sorted({int(t) for t in pd.to_numeric(grp["task"], errors="coerce").dropna()})
        example = next((str(x).strip() for x in grp.get("reasoning", []) if str(x).strip()), "")

        rows.append({
            "Priority": priority,
            "Audit Entity ID": eid,
            "Audit Entity Name": str(grp["focal_entity_name"].iloc[0]) if "focal_entity_name" in grp else "",
            "Audit Leader": leader_by.get(eid, ""),
            "Gap Findings": int(len(grp)),
            "Tasks": ", ".join(f"T{t}" for t in tasks),
            "In Plan": "—" if in_plan is None else ("Yes" if in_plan else "No"),
            "Overdue": "Yes" if overdue else "No",
            "Conc. Owner": "Yes" if is_owner else "No",
            "Residual Risk": risk,
            "Rating May Understate": "Yes" if understates else "No",
            "Connectivity": conn,
            "Structural Reasons": "; ".join(reasons) if reasons else "(in plan — verify only)",
            "Top Specific Risks": "; ".join(sr_ids[:8]),
            "Example Reasoning": _short(example, 240),
        })

    prio_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    worklist = pd.DataFrame(rows)
    if not worklist.empty:
        worklist = worklist.sort_values(
            by=["Priority", "Gap Findings"],
            key=lambda s: s.map(prio_rank) if s.name == "Priority" else s,
            ascending=[True, False],
        ).reset_index(drop=True)

    # Cross-tab counts.
    gap_entities = set(gaps["focal_entity_id"].astype(str))
    def _count(pred):
        return sum(1 for _, r in worklist.iterrows() if pred(r)) if not worklist.empty else 0
    t5_pairs = {(str(r["focal_entity_id"]).strip(),
                 str(r.get("cross_entity_partner_id") or "").strip())
                for _, r in findings[pd.to_numeric(findings["task"], errors="coerce") == 5].iterrows()
                if str(r.get("cross_entity_partner_id") or "").strip()}
    t5_gap_pairs = {(str(r["focal_entity_id"]).strip(),
                     str(r.get("cross_entity_partner_id") or "").strip())
                    for _, r in t5.iterrows()
                    if str(r.get("cross_entity_partner_id") or "").strip()}
    crosstab = pd.DataFrame([
        {"metric": "Entities with ≥1 likely coverage gap", "count": len(gap_entities)},
        {"metric": "  …not in this year's plan", "count": _count(lambda r: r["In Plan"] == "No")},
        {"metric": "  …overdue", "count": _count(lambda r: r["Overdue"] == "Yes")},
        {"metric": "  …a concentration control owner", "count": _count(lambda r: r["Conc. Owner"] == "Yes")},
        {"metric": "  …rated Low/Medium (rating may understate)", "count": _count(lambda r: r["Rating May Understate"] == "Yes")},
        {"metric": "  …already in plan (verify only)", "count": _count(lambda r: r["In Plan"] == "Yes")},
        {"metric": "HIGH-priority gap entities", "count": _count(lambda r: r["Priority"] == "HIGH")},
        {"metric": "Task-5 handoff pairs evaluated", "count": len(t5_pairs)},
        {"metric": "  …with a likely gap (A→B)", "count": len(t5_gap_pairs)},
        {"metric": "  …where receiving entity B also not in plan", "count": len(partner_not_in_plan)},
    ])
    stats = {
        "gap_entities": len(gap_entities),
        "gap_not_in_plan": _count(lambda r: r["In Plan"] == "No"),
        "gap_high": _count(lambda r: r["Priority"] == "HIGH"),
        "t5_pairs": len(t5_pairs),
        "t5_gap_pairs": len(t5_gap_pairs),
        "t5_partner_unplanned": len(partner_not_in_plan),
    }
    return worklist, crosstab, stats


# --------------------------------------------------------------------------- #
# Section 4 — org slices with normalized rates
# --------------------------------------------------------------------------- #
def _by_org_rate(findings: pd.DataFrame, nodes: pd.DataFrame, attr: str, gap_value: str) -> pd.DataFrame:
    cols = [attr, "portfolio_entities", "gap_entities", "likely_gap_rate",
            "doc_issue_findings", "total_findings"]
    if nodes is None or attr not in nodes.columns:
        return pd.DataFrame(columns=cols)
    portfolio = nodes.groupby(attr)["focal_entity_id"].nunique()
    merged = findings.merge(nodes[["focal_entity_id", attr]], on="focal_entity_id", how="left")
    merged[attr] = merged[attr].fillna("(unmapped)")
    is_gap = merged["classification"].str.lower().eq(gap_value.lower())
    doc_value = _classification_value("documentation")
    is_doc = merged["classification"].str.lower().eq(doc_value.lower())
    rows = []
    for grp_name, g in merged.groupby(attr):
        size = int(portfolio.get(grp_name, 0))
        gap_ents = g.loc[is_gap.loc[g.index], "focal_entity_id"].nunique()
        rate = round(100 * gap_ents / size, 1) if size else 0.0
        rows.append({
            attr: grp_name,
            "portfolio_entities": size,
            "gap_entities": int(gap_ents),
            "likely_gap_rate": f"{rate}%",
            "doc_issue_findings": int(is_doc.loc[g.index].sum()),
            "total_findings": int(len(g)),
        })
    return pd.DataFrame(rows).sort_values("gap_entities", ascending=False).reset_index(drop=True)


# --------------------------------------------------------------------------- #
# Scorecard assembly
# --------------------------------------------------------------------------- #
def _build_scorecard(findings, layer2, nodes, fusion_stats):
    summary = layer2["summary"]
    flags = layer2["flags"]
    gaps, gap_value = _gaps_only(findings)
    doc_value = _classification_value("documentation")
    conf_value = _classification_value("conform")

    n_total = len(findings)
    n_gap = int(findings["classification"].str.lower().eq(gap_value.lower()).sum())
    n_doc = int(findings["classification"].str.lower().eq(doc_value.lower()).sum())
    n_conf = int(findings["classification"].str.lower().eq(conf_value.lower()).sum())

    evaluated_entities = findings["focal_entity_id"].astype(str).nunique()
    gap_rate_entity = round(100 * fusion_stats["gap_entities"] / evaluated_entities, 1) if evaluated_entities else 0.0
    gap_rate_edge = round(100 * fusion_stats["t5_gap_pairs"] / fusion_stats["t5_pairs"], 1) if fusion_stats["t5_pairs"] else 0.0

    # Gate / batch confidence.
    batches = sorted({int(b) for b in pd.to_numeric(findings.get("batch_id", pd.Series(dtype=float)), errors="coerce").dropna()})
    passed_batches = sorted({int(r["batch_id"]) for _, r in findings.iterrows()
                             if r.get("gate_passed", True) and pd.notna(r.get("batch_id"))})
    n_batches = len(batches)
    n_pass = len(passed_batches)
    gate_pct = round(100 * n_pass / n_batches, 1) if n_batches else 100.0
    if "evidence_layer" in gaps.columns and len(gaps):
        ctrl = (gaps["evidence_layer"].astype(str).str.lower() == "control").sum()
        ctrl_pct = round(100 * ctrl / len(gaps), 1)
    else:
        ctrl, ctrl_pct = 0, 0.0

    overdue_connected = 0
    if not flags.empty and "Flag Type" in flags.columns:
        overdue_connected = int((flags["Flag Type"] == "OVERDUE + HIGHLY CONNECTED").sum())

    scorecard = [
        {"section": "0. Confidence", "metric": "Batches gate-passed", "value": f"{n_pass} / {n_batches} ({gate_pct}%)"},
        {"section": "0. Confidence", "metric": "Likely-gap findings cited at control layer", "value": f"{ctrl} ({ctrl_pct}%)"},
        {"section": "1. Coverage (structural)", "metric": "Total entities", "value": _summary_val(summary, "Total entities")},
        {"section": "1. Coverage (structural)", "metric": "In scope", "value": _summary_val(summary, "In scope")},
        {"section": "1. Coverage (structural)", "metric": "In scope %", "value": _summary_val(summary, "In scope %")},
        {"section": "1. Coverage (structural)", "metric": "Overdue", "value": _summary_val(summary, "Overdue")},
        {"section": "1. Coverage (structural)", "metric": "Overdue & not in plan", "value": _summary_val(summary, "Overdue & not in plan")},
        {"section": "1. Coverage (structural)", "metric": "Top 10 connected in scope", "value": _summary_val(summary, "Top 10 connected in scope")},
        {"section": "1. Coverage (structural)", "metric": "Top 20 connected in scope", "value": _summary_val(summary, "Top 20 connected in scope")},
        {"section": "1. Coverage (structural)", "metric": "Overdue + highly connected (Flag 2)", "value": overdue_connected},
        {"section": "1. Coverage (structural)", "metric": "Concentration assets", "value": _summary_val(summary, "Concentration assets (total)")},
        {"section": "2. Findings (LLM leads)", "metric": "Total findings", "value": n_total},
        {"section": "2. Findings (LLM leads)", "metric": "Conforms", "value": n_conf},
        {"section": "2. Findings (LLM leads)", "metric": "Documentation issues", "value": n_doc},
        {"section": "2. Findings (LLM leads)", "metric": "Likely coverage gaps", "value": n_gap},
        {"section": "2. Findings (LLM leads)", "metric": "Likely-gap rate (per entity evaluated)", "value": f"{gap_rate_entity}% ({fusion_stats['gap_entities']}/{evaluated_entities})"},
        {"section": "2. Findings (LLM leads)", "metric": "Likely-gap rate (per A→B handoff evaluated)", "value": f"{gap_rate_edge}% ({fusion_stats['t5_gap_pairs']}/{fusion_stats['t5_pairs']})"},
    ]
    kpis = {
        "in_scope_pct": _summary_val(summary, "In scope %"),
        "gap_rate_entity": f"{gap_rate_entity}%",
        "gap_not_in_plan": fusion_stats["gap_not_in_plan"],
        "overdue_connected": overdue_connected,
        "gate_pct": f"{gate_pct}%",
    }
    return pd.DataFrame(scorecard), kpis


# --------------------------------------------------------------------------- #
# HTML scorecard
# --------------------------------------------------------------------------- #
def _bars(pairs, color="#3a7bd5", max_n=14):
    pairs = [(str(k), int(v)) for k, v in pairs if int(v) > 0][:max_n]
    if not pairs:
        return '<div class="muted">No findings in this dimension.</div>'
    mx = max(v for _, v in pairs) or 1
    out = []
    for label, v in pairs:
        pct = int(100 * v / mx)
        out.append(
            f'<div class="bar-row"><span class="bar-label">{html.escape(label)}</span>'
            f'<span class="bar-track"><span class="bar-fill" style="width:{pct}%;background:{color}"></span></span>'
            f'<span class="bar-val">{v}</span></div>'
        )
    return "".join(out)


def _kpi_tile(label, value, accent):
    return (f'<div class="kpi"><div class="kpi-val" style="color:{accent}">{html.escape(str(value))}</div>'
            f'<div class="kpi-label">{html.escape(label)}</div></div>')


def _worklist_html(worklist: pd.DataFrame, limit=30) -> str:
    if worklist.empty:
        return '<div class="muted">No likely-gap entities to triage.</div>'
    cls = {"HIGH": "p-high", "MEDIUM": "p-med", "LOW": "p-low"}
    head = ("<tr><th>Priority</th><th>Entity</th><th>Leader</th><th>Gaps</th><th>Tasks</th>"
            "<th>In&nbsp;Plan</th><th>Risk</th><th>Why it's flagged (structural)</th></tr>")
    rows = []
    for _, r in worklist.head(limit).iterrows():
        risk = r["Residual Risk"]
        rc = RISK_COLORS.get(risk, "#95a5a6")
        rows.append(
            f'<tr class="{cls.get(r["Priority"], "")}">'
            f'<td><b>{r["Priority"]}</b></td>'
            f'<td><span class="eid">{html.escape(str(r["Audit Entity ID"]))}</span> '
            f'{html.escape(_short(r["Audit Entity Name"], 40))}</td>'
            f'<td>{html.escape(_short(r["Audit Leader"], 28))}</td>'
            f'<td style="text-align:center">{r["Gap Findings"]}</td>'
            f'<td>{html.escape(str(r["Tasks"]))}</td>'
            f'<td style="text-align:center">{r["In Plan"]}</td>'
            f'<td><span class="dot" style="background:{rc}"></span>{html.escape(str(risk))}</td>'
            f'<td>{html.escape(str(r["Structural Reasons"]))}</td></tr>'
        )
    more = "" if len(worklist) <= limit else f'<div class="muted">+ {len(worklist) - limit} more in the workbook.</div>'
    return f'<table class="worklist">{head}{"".join(rows)}</table>{more}'


def _render_html(kpis, worklist, bars, date_str) -> str:
    task_bars, req_bars, risk_bars = bars
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Audit Universe — Department Insights</title>
<style>
:root {{ --bg:#0f1419; --panel:#1b2330; --ink:#e8edf2; --muted:#8a97a8; --line:#2b3647; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink);
  font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif; font-size:13px; }}
.wrap {{ max-width:1180px; margin:0 auto; padding:24px 28px 48px; }}
h1 {{ font-size:22px; margin:0 0 2px; }}
.sub {{ color:var(--muted); margin:0 0 18px; font-size:12px; }}
.kpis {{ display:grid; grid-template-columns:repeat(5,1fr); gap:12px; margin-bottom:18px; }}
.kpi {{ background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:14px 16px; }}
.kpi-val {{ font-size:26px; font-weight:700; line-height:1.1; }}
.kpi-label {{ color:var(--muted); font-size:11px; margin-top:4px; }}
.banner {{ display:flex; gap:14px; margin-bottom:20px; }}
.tier {{ flex:1; background:var(--panel); border:1px solid var(--line); border-left:4px solid; border-radius:8px; padding:11px 14px; }}
.tier.struct {{ border-left-color:#27ae60; }}
.tier.llm {{ border-left-color:#e67e22; }}
.tier b {{ display:block; margin-bottom:2px; }}
.tier span {{ color:var(--muted); }}
.grid {{ display:grid; grid-template-columns:1.55fr 1fr; gap:20px; }}
.card {{ background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:14px 16px; margin-bottom:18px; }}
.card h2 {{ font-size:14px; margin:0 0 12px; }}
.card h3 {{ font-size:12px; color:var(--muted); text-transform:uppercase; letter-spacing:.4px; margin:14px 0 7px; }}
table.worklist {{ width:100%; border-collapse:collapse; font-size:12px; }}
table.worklist th {{ text-align:left; color:var(--muted); font-weight:600; border-bottom:1px solid var(--line); padding:6px 6px; }}
table.worklist td {{ padding:6px 6px; border-bottom:1px solid var(--line); vertical-align:top; }}
.worklist tr.p-high td:first-child b {{ color:#ff6b5e; }}
.worklist tr.p-med td:first-child b {{ color:#f1c40f; }}
.worklist tr.p-low td:first-child b {{ color:#8a97a8; }}
.eid {{ font-family:ui-monospace,Menlo,Consolas,monospace; color:#7fb2ff; }}
.dot {{ display:inline-block; width:9px; height:9px; border-radius:50%; margin-right:5px; vertical-align:middle; }}
.bar-row {{ display:flex; align-items:center; gap:8px; margin:4px 0; }}
.bar-label {{ width:140px; font-size:11px; color:var(--ink); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.bar-track {{ flex:1; background:#11181f; border-radius:4px; height:14px; overflow:hidden; }}
.bar-fill {{ display:block; height:100%; }}
.bar-val {{ width:28px; text-align:right; color:var(--muted); font-size:11px; }}
.muted {{ color:var(--muted); font-size:11px; margin-top:8px; }}
.foot {{ margin-top:22px; padding:13px 16px; background:#1a1410; border:1px solid #3a2a1a; border-radius:8px;
  color:#d8b08c; font-size:11px; line-height:1.55; }}
</style></head><body><div class="wrap">
<h1>Audit Universe — Department Insights</h1>
<p class="sub">Structural coverage (Layer 1–2) fused with the Stage 2 LLM handoff-reliance review · generated {date_str}</p>

<div class="kpis">
{_kpi_tile("In scope", kpis["in_scope_pct"], "#27ae60")}
{_kpi_tile("Likely-gap rate (per entity)", kpis["gap_rate_entity"], "#e67e22")}
{_kpi_tile("Gap entities NOT in plan", kpis["gap_not_in_plan"], "#ff6b5e")}
{_kpi_tile("Overdue + highly connected", kpis["overdue_connected"], "#f1c40f")}
{_kpi_tile("Batches gate-passed", kpis["gate_pct"], "#7fb2ff")}
</div>

<div class="banner">
<div class="tier struct"><b>Structural findings — decision-grade</b>
<span>Coverage, connectivity, concentration and overdue status are computed deterministically. Use directly for plan defense.</span></div>
<div class="tier llm"><b>LLM findings — candidate leads</b>
<span>Likely-gap findings are hypotheses for a human to confirm against the control library before they're reportable.</span></div>
</div>

<div class="grid">
<div>
<div class="card"><h2>Priority worklist — where the two layers agree</h2>
{_worklist_html(worklist)}</div>
</div>
<div>
<div class="card"><h2>Where the gaps cluster</h2>
<h3>By task</h3>{task_bars}
<h3>By requirement theme</h3>{req_bars}
<h3>By risk category</h3>{risk_bars}
</div>
</div>
</div>

<div class="foot"><b>Read with care.</b> Every likely-gap row is a lead, not a confirmed finding —
control <i>descriptions</i> were trimmed from the receiving-entity payloads to fit the token budget,
which raises false-positive risk on the Task-5 cross-entity check. Confirm each against the live control
library before acting. Structural metrics (coverage, overdue, concentration) carry no such caveat.</div>
</div></body></html>"""


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
def run(input_dir: Path = DEFAULT_INPUT_DIR, out_dir: Path = DEFAULT_OUT_DIR,
        batches_dir: Path = DEFAULT_BATCHES_DIR, date_str: str | None = None) -> dict:
    date_str = date_str or datetime.now().strftime("%Y%m%d")
    findings = _load_findings(input_dir)
    layer2 = _load_layer2(input_dir)
    nodes = _load_nodes(_latest(input_dir, "layer1_output") or (input_dir / "layer1_output.xlsx"))

    gaps, gap_value = _gaps_only(findings)
    worklist, crosstab, fusion_stats = _build_fusion(findings, layer2, nodes)
    scorecard, kpis = _build_scorecard(findings, layer2, nodes, fusion_stats)
    sys_df, man_df = _load_ranked_summary(batches_dir)

    # Org slices.
    by_leader = _by_org_rate(findings, nodes, "audit_leader", gap_value) if nodes is not None else pd.DataFrame()
    by_bu = _by_org_rate(findings, nodes, "business_unit", gap_value) if nodes is not None else pd.DataFrame()

    # Systemic & manual rollup as one stacked sheet.
    systemic_rows = []
    for _, r in sys_df.iterrows():
        systemic_rows.append({"Type": "Systemic documentation issue", "Theme": r["pattern"],
                              "Summary": r["summary"], "Affected Entities (sum)": r["affected_entity_count"],
                              "Batches Mentioning": r["batches_mentioning"]})
    for _, r in man_df.iterrows():
        systemic_rows.append({"Type": "Manual gap exposed", "Theme": r["area"], "Summary": r["summary"],
                              "Affected Entities (sum)": "", "Batches Mentioning": r["batches_mentioning"]})
    systemic_sheet = pd.DataFrame(systemic_rows)

    methodology = pd.DataFrame([
        {"Note": "Two tiers", "Detail": "Layer 1–2 structural metrics are deterministic and decision-grade. Stage 2 LLM findings are candidate leads requiring human verification."},
        {"Note": "Likely-gap rate (entity)", "Detail": "Entities with ≥1 likely coverage gap ÷ distinct focal entities evaluated."},
        {"Note": "Likely-gap rate (edge)", "Detail": "Distinct A→B handoff pairs with a Task-5 likely gap ÷ Task-5 pairs evaluated."},
        {"Note": "Priority logic", "Detail": "HIGH = likely gap AND not in plan AND (overdue OR concentration owner OR receiving entity not in plan). MEDIUM = any single structural signal. LOW = entity already in plan (verify only)."},
        {"Note": "False-positive caveat", "Detail": "Control descriptions were trimmed from target-context payloads to fit the token budget, raising false-positive risk on the Task-5 cross-entity check. Confirm gaps against the live control library."},
        {"Note": "Sources", "Detail": "findings_rollup.xlsx / findings.csv (Stage 2); layer2_coverage_matrix_*.xlsx (Coverage Matrix, Summary, Flags, Concentration Detail); layer1_output_*.xlsx (Nodes); batch response.json (ranked_summary)."},
    ])

    sheets = {
        "Executive Scorecard": scorecard,
        "Priority Worklist": worklist,
        "Fusion Cross-Tabs": crosstab,
        "Gaps by Risk Category": _by_risk_category(gaps),
        "By Requirement": _by_requirement(findings, gap_value),
    }
    if not by_leader.empty:
        sheets["By Audit Leader (rate)"] = by_leader
    if not by_bu.empty:
        sheets["By Business Unit (rate)"] = by_bu
    sheets["Systemic & Manual Gaps"] = systemic_sheet
    sheets["Methodology & Caveats"] = methodology

    out_dir.mkdir(parents=True, exist_ok=True)
    xlsx_path = out_dir / f"department_insights_{date_str}.xlsx"
    write_workbook(xlsx_path, sheets)

    # HTML bars.
    gaps_tasks = (gaps.assign(t=pd.to_numeric(gaps["task"], errors="coerce"))
                  .groupby("t").size()) if not gaps.empty else pd.Series(dtype=int)
    td = labels.task_displays()
    task_pairs = [(f"T{int(k)} {td.get(int(k), '')}", v) for k, v in gaps_tasks.items() if pd.notna(k)]
    req_df = _by_requirement(gaps, gap_value)
    req_pairs = [(r["requirement"], r["finding_count"]) for _, r in req_df.iterrows()] if not req_df.empty else []
    rc_df = _by_risk_category(gaps)
    risk_pairs = [(r["risk_category"], r["entity_count"]) for _, r in rc_df.iterrows()] if not rc_df.empty else []
    bars = (_bars(task_pairs, "#e67e22"), _bars(req_pairs, "#3a7bd5"), _bars(risk_pairs, "#9b59b6"))

    html_path = out_dir / f"department_scorecard_{date_str}.html"
    html_path.write_text(_render_html(kpis, worklist, bars, date_str), encoding="utf-8")

    print(f"[dept] wrote {xlsx_path}")
    print(f"[dept] wrote {html_path}")
    print(f"  evaluated entities: {findings['focal_entity_id'].astype(str).nunique()}")
    print(f"  likely-gap entities: {fusion_stats['gap_entities']}  (HIGH priority: {fusion_stats['gap_high']})")
    print(f"  gap & not in plan: {fusion_stats['gap_not_in_plan']}")
    print(f"  T5 gap pairs: {fusion_stats['t5_gap_pairs']}/{fusion_stats['t5_pairs']}  (receiver also unplanned: {fusion_stats['t5_partner_unplanned']})")
    return {"xlsx": xlsx_path, "html": html_path, "worklist": worklist,
            "crosstab": crosstab, "scorecard": scorecard, "stats": fusion_stats}


def main() -> None:
    p = argparse.ArgumentParser(description="Department-wide insights: fuse Layer 1-2 with Stage 2 LLM findings.")
    p.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    p.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    p.add_argument("--batches-dir", type=Path, default=DEFAULT_BATCHES_DIR)
    p.add_argument("--date", default=None, help="YYYYMMDD stamp for output filenames (default: today)")
    args = p.parse_args()
    run(args.input_dir, args.out_dir, args.batches_dir, args.date)


if __name__ == "__main__":
    main()
