"""Generate fictional Stage 2 batch responses for end-to-end dummy runs.

The real Stage 2 corpus (pasted ChatGPT responses) lives only on local
machines. This module fabricates a *plausible, gate-passing* `response.json`
for every `runs/stage2/batches/batch_*/` directory so the whole downstream
chain can be exercised against dummy data alone:

    python -m src.stage2_handoff_review.make_dummy_responses
    python -m src.stage2_handoff_review.aggregate
    python -m src.stage2_handoff_review.summarize_findings
    python src/generate_network_viz.py --input-dir data/output --output-dir data/output

Findings are grounded in each batch's manifest (focal_ids / target_ids) and,
when the Layer 1 / edge outputs are present, in the real entity names and
handoff edges — so Task 5 gap findings land on actual handoff edges in the
network viz rather than synthetic ones.

The output is deterministic (seeded per batch). It is NOT real audit content;
it exists purely to make the pipeline runnable and the viz overlay reviewable.
One batch is deliberately failed (see --fail-batch) so the gate log, the
rollup's failed-gate split, and the viz "include failed-gate" toggle all have
something to show.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_BATCHES = ROOT / "runs" / "stage2" / "batches"
DEFAULT_PIPELINE = ROOT / "data" / "output"

# Exact enum values — must match config/stage2_prompt.yaml (validated by aggregate).
CLASSIFICATIONS = ["conforms", "documentation issue", "likely coverage gap"]
RISK_CATEGORIES = [
    "Compliance", "Country", "Credit", "External Fraud", "Financial Reporting",
    "Funding & Liquidity", "Information Technology", "Information Security", "Model",
    "Market", "Operational", "Reputational", "Strategic & Business", "Third Party",
]
# Paraphrases of the 5 Stage 1 manual requirements (see batch prompt §"Manual review").
MANUAL_REQS = [
    "Make audit-entity risk ownership explicit",
    "Require attribute-level handoff documentation",
    "Explicitly address the coarse-handoff failure mode",
    "Strengthen handoff hygiene to match reliance sufficiency",
    "Create a single coverage view / assurance map",
]


def _load_entity_context(pipeline_dir: Path):
    """Return (id->name, handoff_partners: id->[ids]) from Layer 1 / edge output.

    Degrades to empty maps when the workbooks are absent — the generator then
    falls back to manifest target_ids and bare entity IDs.
    """
    names: dict[str, str] = {}
    partners: dict[str, list[str]] = {}
    l1 = pipeline_dir / "layer1_output.xlsx"
    ed = pipeline_dir / "edge_derivation_output.xlsx"
    if l1.is_file():
        try:
            nodes = pd.read_excel(l1, sheet_name="Nodes")
            names = {str(r["Audit Entity ID"]): str(r["Audit Entity Name"])
                     for _, r in nodes.iterrows()}
        except Exception:
            pass
    if ed.is_file():
        try:
            edges = pd.read_excel(ed, sheet_name="Master Edge List")
            ho = edges[edges["Edge Type"].astype(str) == "handoff_to"]
            for _, r in ho.iterrows():
                partners.setdefault(str(r["Entity A ID"]), []).append(str(r["Entity B ID"]))
        except Exception:
            pass
    return names, partners


def _name(eid: str, names: dict[str, str]) -> str:
    return names.get(eid, eid)


def _srs(rng: random.Random, n: int = 2) -> list[str]:
    return [f"SR-{rng.randint(100, 999)}" for _ in range(n)]


def _kpas(rng: random.Random, n: int = 1) -> list[str]:
    return [f"KPA-{rng.randint(100, 999)}" for _ in range(n)]


def _pick_classification(rng: random.Random, gap_weight: float) -> str:
    """Weighted pick: `gap_weight` chance of a gap, rest split doc-issue/conforms."""
    if rng.random() < gap_weight:
        return "likely coverage gap"
    return "documentation issue" if rng.random() < 0.6 else "conforms"


def _finding(task, focal, focal_name, classification, evidence_layer, rng,
             partner=None, partner_name=None):
    risk = rng.choice(RISK_CATEGORIES)
    f = {
        "task": task,
        "manual_requirement": rng.choice(MANUAL_REQS),
        "focal_entity_id": focal,
        "focal_entity_name": focal_name,
        "cross_entity_partner_id": partner,
        "risk_category": risk,
        "specific_risk_ids": _srs(rng),
        "kpa_ids": _kpas(rng),
        "evidence_layer": evidence_layer,
        "evidence_quote": f"“{risk} risk is monitored at the program level.”",
        "classification": classification,
        "reasoning": _reasoning(task, focal_name, partner_name, risk, classification),
    }
    return f


def _reasoning(task, focal_name, partner_name, risk, classification):
    gap = classification == "likely coverage gap"
    if task == 5:
        if gap:
            return (f"{focal_name} transfers the {risk.lower()} slice to {partner_name}; "
                    f"{partner_name}'s control library covers the category but not the "
                    f"specific risk statement, leaving it without an owner.")
        return f"{partner_name}'s controls cover the {risk.lower()} risk {focal_name} handed off."
    if task == 3:
        if gap:
            return (f"{focal_name} hands off {risk.lower()} at the program level; the receiving "
                    f"controls are framework/oversight only, not the embedded-process control.")
        return f"{focal_name}'s embedded {risk.lower()} controls align with the program-level handoff."
    if task == 1:
        return (f"Manual requires explicit ownership; {focal_name} documents the handoff in prose "
                f"but does not state which register carries {risk.lower()} risk.")
    if task == 2:
        return (f"{focal_name} describes a {risk.lower()} handoff, but the residual rating is still "
                f"applied with no acknowledgment of partial retention.")
    return (f"{focal_name}'s overview describes activity that should generate {risk.lower()} "
            f"controls; the library is silent on that process's KPA.")


def build_response(manifest, names, partners, seed, fail=False):
    rng = random.Random(seed)
    focal_ids = [str(x) for x in manifest.get("focal_ids", []) or []]
    target_ids = [str(x) for x in manifest.get("target_ids", []) or []]
    source_ids = [str(x) for x in manifest.get("source_ids", []) or []]
    context = target_ids + source_ids
    if not focal_ids:
        return {"findings": [], "ranked_summary": {
            "likely_coverage_gaps": [], "systemic_documentation_issues": [], "manual_gaps_exposed": []}}

    findings = []
    gap_focals = []  # focal entities that got a gap finding (for ranked_summary)

    def _partner_for(focal):
        """Prefer a real handoff partner of `focal` (-> real edge in the viz),
        else a manifest target, else another focal."""
        real = [p for p in partners.get(focal, []) if p in (context + focal_ids)]
        if real:
            return rng.choice(real)
        if target_ids:
            return rng.choice(target_ids)
        if source_ids:
            return rng.choice(source_ids)
        others = [f for f in focal_ids if f != focal] or focal_ids
        return rng.choice(others)

    for focal in focal_ids:
        fname = _name(focal, names)
        # Task 5 — cross-entity (drives red edges). Control layer unless this is
        # the deliberately-failed batch (then non-control -> fails the t5 gate).
        partner = _partner_for(focal)
        t5_layer = "entity_prose" if fail else "control"
        t5_cls = _pick_classification(rng, gap_weight=0.45)
        findings.append(_finding(5, focal, fname, t5_cls, t5_layer, rng,
                                  partner=partner, partner_name=_name(partner, names)))
        if t5_cls == "likely coverage gap":
            gap_focals.append((focal, fname))

        # Task 3 — coarse-handoff (drives node rings). Always control layer.
        t3_cls = _pick_classification(rng, gap_weight=0.40)
        findings.append(_finding(3, focal, fname, t3_cls, "control", rng))
        if t3_cls == "likely coverage gap":
            gap_focals.append((focal, fname))

        # Tasks 1/2/4 — documentation-quality texture for the rollup.
        findings.append(_finding(1, focal, fname, _pick_classification(rng, 0.10),
                                 rng.choice(["entity_prose", "control"]), rng))
        findings.append(_finding(2, focal, fname, _pick_classification(rng, 0.10),
                                 "category_summary", rng))
        findings.append(_finding(4, focal, fname, _pick_classification(rng, 0.15),
                                 rng.choice(["control", "entity_prose"]), rng))

    ranked = {
        "likely_coverage_gaps": [
            {"focal_entity_id": fid, "confidence": rng.choice(["high", "medium"]),
             "summary": f"{fn} hands off a risk slice that the receiver does not fully cover.",
             "specific_risk_ids": _srs(rng)}
            for fid, fn in gap_focals[:3]
        ],
        "systemic_documentation_issues": [
            {"pattern": "Handoff described in prose but not reflected in residual ratings",
             "affected_entity_count": len(focal_ids),
             "summary": "Ratings applied without acknowledging partial retention after a handoff."}
        ],
        "manual_gaps_exposed": (
            [{"area": "Attribute-level handoff documentation",
              "summary": "Manual does not require the exact risk slice / embedded touchpoint to be named."}]
            if rng.random() < 0.5 else []
        ),
    }
    return {"findings": findings, "ranked_summary": ranked}


def run(batches_root: Path, pipeline_dir: Path, fail_batch: int) -> None:
    names, partners = _load_entity_context(pipeline_dir)
    if names:
        print(f"[dummy] grounded in {len(names)} entity names, "
              f"{sum(len(v) for v in partners.values())} handoff_to edges")
    else:
        print(f"[dummy] no Layer 1 output found — using manifest IDs only")

    batch_dirs = sorted(d for d in batches_root.glob("batch_*") if d.is_dir())
    if not batch_dirs:
        sys.exit(f"[dummy] no batch_* directories under {batches_root}")

    written = 0
    for d in batch_dirs:
        manifest_path = d / "manifest.json"
        if not manifest_path.exists():
            print(f"[dummy] {d.name}: no manifest.json — skipped")
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        bid = int(manifest.get("batch_id", d.name.split("_")[1]))
        fail = (bid == fail_batch)
        response = build_response(manifest, names, partners, seed=bid, fail=fail)
        (d / "response.json").write_text(json.dumps(response, indent=2), encoding="utf-8")
        flag = "  (deliberately fails gate)" if fail else ""
        print(f"[dummy] {d.name}: {len(response['findings'])} findings{flag}")
        written += 1
    print(f"[dummy] wrote {written} response.json files")


def main() -> None:
    p = argparse.ArgumentParser(description="Generate fictional Stage 2 batch responses.")
    p.add_argument("--batches", type=Path, default=DEFAULT_BATCHES)
    p.add_argument("--pipeline", type=Path, default=DEFAULT_PIPELINE,
                   help="dir with layer1_output.xlsx / edge_derivation_output.xlsx for grounding")
    p.add_argument("--fail-batch", type=int, default=7,
                   help="batch_id to deliberately fail the gate (must not be the first batch)")
    args = p.parse_args()
    run(args.batches, args.pipeline, args.fail_batch)


if __name__ == "__main__":
    main()
