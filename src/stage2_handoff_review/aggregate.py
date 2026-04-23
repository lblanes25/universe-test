"""Parse pasted ChatGPT responses, run gate checks, merge findings.

Usage:
    python -m src.stage2_handoff_review.aggregate
    python -m src.stage2_handoff_review.aggregate --override-gate
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_BATCHES_ROOT = ROOT / "runs" / "stage2" / "batches"
DEFAULT_AGGREGATED_ROOT = ROOT / "runs" / "stage2" / "aggregated"
DEFAULT_CONFIG = ROOT / "config" / "stage2_batching.json"

FINDING_REQUIRED = {
    "task", "manual_requirement", "focal_entity_id", "focal_entity_name",
    "specific_risk_ids", "kpa_ids", "evidence_layer", "evidence_quote",
    "classification", "reasoning",
}
EVIDENCE_LAYERS = {"control", "category_summary", "entity_prose", "structured_handoffs"}
CLASSIFICATIONS = {"conforms", "documentation issue", "likely coverage gap"}


@dataclass
class GateResult:
    batch_id: int
    passed: bool
    checks: dict[str, tuple[bool, str]]  # check_name -> (ok, detail)


def _load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _strip_code_fences(text: str) -> str:
    """Accept either raw JSON or JSON wrapped in ```json ... ``` fencing."""
    text = text.strip()
    if text.startswith("{") and text.endswith("}"):
        return text
    match = re.search(r"```(?:json)?\s*\n(.*?)\n```", text, flags=re.DOTALL)
    if match:
        return match.group(1).strip()
    return text


def parse_response(path: Path) -> dict | None:
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        stripped = _strip_code_fences(raw)
        try:
            return json.loads(stripped)
        except json.JSONDecodeError as e:
            raise ValueError(f"{path} is not valid JSON: {e}") from e


def _validate_schema(response: dict) -> list[str]:
    errors: list[str] = []
    if "findings" not in response or not isinstance(response["findings"], list):
        errors.append("missing top-level 'findings' array")
    if "ranked_summary" not in response or not isinstance(response["ranked_summary"], dict):
        errors.append("missing top-level 'ranked_summary' object")

    for i, f in enumerate(response.get("findings", [])):
        missing = FINDING_REQUIRED - set(f)
        if missing:
            errors.append(f"finding #{i}: missing fields {sorted(missing)}")
            continue
        if f["evidence_layer"] not in EVIDENCE_LAYERS:
            errors.append(f"finding #{i}: invalid evidence_layer={f['evidence_layer']!r}")
        if f["classification"] not in CLASSIFICATIONS:
            errors.append(f"finding #{i}: invalid classification={f['classification']!r}")
        if not isinstance(f["specific_risk_ids"], list):
            errors.append(f"finding #{i}: specific_risk_ids must be array")
        if not isinstance(f["kpa_ids"], list):
            errors.append(f"finding #{i}: kpa_ids must be array")
        if f["task"] == 5 and not f.get("cross_entity_partner_id"):
            errors.append(f"finding #{i}: Task 5 finding missing cross_entity_partner_id")

    summary = response.get("ranked_summary", {})
    for key in ("likely_coverage_gaps", "systemic_documentation_issues", "manual_gaps_exposed"):
        if key not in summary or not isinstance(summary[key], list):
            errors.append(f"ranked_summary.{key} missing or not an array")
    return errors


def _run_gate(
    batch_id: int,
    response: dict,
    manifest: dict,
    config: dict,
) -> GateResult:
    checks: dict[str, tuple[bool, str]] = {}

    schema_errors = _validate_schema(response)
    checks["valid_json_schema"] = (not schema_errors, "; ".join(schema_errors) if schema_errors else "ok")

    focal_set = set(manifest.get("focal_ids", []))
    context_set = set(manifest.get("target_ids", []) + manifest.get("source_ids", []))
    out_of_scope = []
    for f in response.get("findings", []):
        eid = f.get("focal_entity_id")
        if eid and eid in context_set and eid not in focal_set:
            out_of_scope.append(eid)
    checks["findings_scoped_to_focal"] = (
        not out_of_scope,
        f"out-of-scope findings on {sorted(set(out_of_scope))}" if out_of_scope else "ok",
    )

    handoff_partners_present = context_set | focal_set
    task5 = [f for f in response.get("findings", []) if f.get("task") == 5]
    task5_pair_hit = any(
        (f.get("focal_entity_id") in focal_set)
        and (f.get("cross_entity_partner_id") in handoff_partners_present)
        for f in task5
    )
    checks["task5_findings_present"] = (
        bool(task5_pair_hit),
        f"{len(task5)} Task 5 findings; partner-hits={task5_pair_hit}",
    )

    thresholds = config.get("gate_thresholds", {})
    t3_min = thresholds.get("task3_control_layer_min_fraction", 0.70)
    t5_min = thresholds.get("task5_control_layer_min_fraction", 0.50)

    def _control_fraction(findings_for_task: list[dict]) -> tuple[float, int]:
        if not findings_for_task:
            return (1.0, 0)  # vacuously passes (no findings to fail on)
        cited = sum(1 for f in findings_for_task if f.get("evidence_layer") == "control")
        return (cited / len(findings_for_task), len(findings_for_task))

    task3 = [f for f in response.get("findings", []) if f.get("task") == 3]
    t3_frac, t3_n = _control_fraction(task3)
    checks["task3_control_layer_threshold"] = (
        t3_frac >= t3_min if t3_n > 0 else True,
        f"{t3_frac:.0%} control-layer cited across {t3_n} Task 3 findings (min {t3_min:.0%})",
    )

    t5_frac, t5_n = _control_fraction(task5)
    checks["task5_control_layer_threshold"] = (
        t5_frac >= t5_min if t5_n > 0 else True,
        f"{t5_frac:.0%} control-layer cited across {t5_n} Task 5 findings (min {t5_min:.0%})",
    )

    summary = response.get("ranked_summary", {})
    checks["has_ranked_summary"] = (
        all(k in summary for k in ("likely_coverage_gaps", "systemic_documentation_issues", "manual_gaps_exposed")),
        "present" if summary else "missing",
    )

    passed = all(ok for ok, _ in checks.values())
    return GateResult(batch_id=batch_id, passed=passed, checks=checks)


def _findings_to_rows(batch_id: int, response: dict) -> list[dict]:
    rows = []
    for f in response.get("findings", []):
        rows.append({
            "batch_id": batch_id,
            "task": f.get("task"),
            "focal_entity_id": f.get("focal_entity_id"),
            "focal_entity_name": f.get("focal_entity_name"),
            "cross_entity_partner_id": f.get("cross_entity_partner_id"),
            "risk_category": f.get("risk_category"),
            "specific_risk_ids": "; ".join(f.get("specific_risk_ids", []) or []),
            "kpa_ids": "; ".join(f.get("kpa_ids", []) or []),
            "evidence_layer": f.get("evidence_layer"),
            "classification": f.get("classification"),
            "manual_requirement": f.get("manual_requirement"),
            "evidence_quote": f.get("evidence_quote"),
            "reasoning": f.get("reasoning"),
        })
    return rows


def run(
    batches_root: Path,
    aggregated_root: Path,
    config_path: Path,
    override_gate: bool,
) -> dict:
    config = _load_config(config_path)
    aggregated_root.mkdir(parents=True, exist_ok=True)

    batch_dirs = sorted([d for d in batches_root.glob("batch_*") if d.is_dir()])
    if not batch_dirs:
        print(f"[aggregate] no batch_* directories under {batches_root}")
        return {"processed": 0, "gated": []}

    all_rows: list[dict] = []
    gate_log: list[GateResult] = []
    missing_responses: list[str] = []
    first_batch_id: int | None = None

    for d in batch_dirs:
        batch_id = int(d.name.split("_")[1])
        manifest_path = d / "manifest.json"
        response_path = d / "response.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
        if not response_path.exists() or response_path.stat().st_size == 0:
            missing_responses.append(d.name)
            continue
        try:
            response = parse_response(response_path)
        except ValueError as e:
            gate = GateResult(batch_id=batch_id, passed=False, checks={"valid_json_schema": (False, str(e))})
            gate_log.append(gate)
            continue
        if response is None:
            missing_responses.append(d.name)
            continue
        gate = _run_gate(batch_id, response, manifest, config)
        gate_log.append(gate)

        is_first = (first_batch_id is None)
        if is_first:
            first_batch_id = batch_id

        if is_first and not gate.passed and not override_gate:
            print(f"[aggregate] batch {batch_id:03d} FAILED gate — not aggregating further batches")
            print(f"[aggregate] run with --override-gate to force aggregation")
            break

        all_rows.extend(_findings_to_rows(batch_id, response))

    findings_df = pd.DataFrame(all_rows) if all_rows else pd.DataFrame(
        columns=[
            "batch_id", "task", "focal_entity_id", "focal_entity_name", "cross_entity_partner_id",
            "risk_category", "specific_risk_ids", "kpa_ids", "evidence_layer", "classification",
            "manual_requirement", "evidence_quote", "reasoning",
        ]
    )
    findings_path = aggregated_root / "findings.csv"
    findings_df.to_csv(findings_path, index=False)
    print(f"[aggregate] wrote {len(findings_df)} findings -> {findings_path}")

    _write_gate_log(aggregated_root / "gate_log.md", gate_log, missing_responses)
    _write_ranked_summary(aggregated_root / "ranked_summary.md", batch_dirs, override_gate)

    return {
        "processed": len(gate_log),
        "missing": missing_responses,
        "gated": gate_log,
        "findings_rows": len(findings_df),
    }


def _write_gate_log(path: Path, gates: list[GateResult], missing: list[str]) -> None:
    lines = ["# Stage 2 — Gate Log", ""]
    if missing:
        lines.append(f"**Missing response.json for:** {', '.join(missing)}")
        lines.append("")
    for g in gates:
        status = "PASS" if g.passed else "FAIL"
        lines.append(f"## batch_{g.batch_id:03d} — {status}")
        for name, (ok, detail) in g.checks.items():
            mark = "OK  " if ok else "FAIL"
            lines.append(f"- [{mark}] {name}: {detail}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_ranked_summary(path: Path, batch_dirs: list[Path], allow_partial: bool) -> None:
    lines = ["# Stage 2 — Aggregated Ranked Summary", ""]
    malformed: list[str] = []
    for d in batch_dirs:
        rp = d / "response.json"
        if not rp.exists() or rp.stat().st_size == 0:
            continue
        try:
            response = parse_response(rp)
        except Exception:
            continue
        if response is None:
            continue
        s = response.get("ranked_summary") or {}
        if not isinstance(s, dict):
            malformed.append(d.name)
            continue
        gaps = s.get("likely_coverage_gaps") or []
        issues = s.get("systemic_documentation_issues") or []
        manual_gaps = s.get("manual_gaps_exposed") or []
        if not (gaps or issues or manual_gaps):
            continue
        lines.append(f"## {d.name}")
        if gaps:
            lines.append("**Likely coverage gaps:**")
            for g in gaps:
                lines.append(f"- `{g.get('focal_entity_id','?')}` ({g.get('confidence','?')}): {g.get('summary','')} "
                             f"[SRs: {', '.join(g.get('specific_risk_ids', []) or [])}]")
        if issues:
            lines.append("**Systemic documentation issues:**")
            for g in issues:
                lines.append(f"- {g.get('pattern','?')} (n={g.get('affected_entity_count','?')}): {g.get('summary','')}")
        if manual_gaps:
            lines.append("**Manual gaps exposed:**")
            for g in manual_gaps:
                lines.append(f"- {g.get('area','?')}: {g.get('summary','')}")
        lines.append("")
    if malformed:
        lines.append("---")
        lines.append("")
        lines.append(f"**Skipped {len(malformed)} batch(es) with malformed `ranked_summary` (not a dict):** "
                     f"{', '.join(malformed)}")
        print(f"[aggregate] WARNING: skipped {len(malformed)} batch(es) with malformed ranked_summary: "
              f"{', '.join(malformed)}")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batches-root", type=Path, default=DEFAULT_BATCHES_ROOT)
    parser.add_argument("--aggregated-root", type=Path, default=DEFAULT_AGGREGATED_ROOT)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--override-gate", action="store_true",
                        help="Aggregate all batches even if batch 1 fails the gate.")
    args = parser.parse_args()
    run(args.batches_root, args.aggregated_root, args.config, args.override_gate)


if __name__ == "__main__":
    main()
