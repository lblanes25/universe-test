"""Batch prompt generator with dry-run, worst-case token modeling, and auto-split.

Usage:
    python -m src.stage2_handoff_review.generate --dry-run
    python -m src.stage2_handoff_review.generate
    python -m src.stage2_handoff_review.generate --risk-assessment data/input/real.xlsx --controls data/input/real_controls.csv
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.stage1_filter import classify_entities  # noqa: E402
from src.stage2_nodes import build_nodes  # noqa: E402
from src.stage4_relational import build_handoffs  # noqa: E402
from src.stage2_handoff_review.graph import (  # noqa: E402
    FocalBatch,
    build_undirected_handoff_graph,
    select_focal_batches,
    severed_edge_count,
)
from src.stage2_handoff_review.payload import (  # noqa: E402
    build_focal_payload,
    build_source_context_payload,
    build_target_context_payload,
    partition_context,
)

DEFAULT_CONFIG = ROOT / "config" / "stage2_batching.json"
DEFAULT_RISK_ASSESSMENT = ROOT / "data" / "input" / "dummy_audit_universe_50.csv"
DEFAULT_CONTROLS = ROOT / "data" / "input" / "dummy_controls.csv"
HORIZONTAL_KEYWORDS = ROOT / "config" / "horizontal_keywords.json"
PROMPT_TEMPLATE = ROOT / "src" / "stage2_handoff_review" / "templates" / "prompt.md"
OUTPUT_ROOT = ROOT / "runs" / "stage2" / "batches"


@dataclass
class BatchPlan:
    batch_id: int
    focal_ids: list[str]
    target_ids: list[str]
    source_ids: list[str]
    isolated: bool
    focal_tokens: int
    target_tokens: int
    source_tokens: int
    fixed_tokens: int
    avg_total_tokens: int
    worst_case_total_tokens: int
    split_from: int | None = None


def _read_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in (".xlsx", ".xlsm", ".xls"):
        return pd.read_excel(path, dtype=str)
    # Try UTF-8-with-BOM first (handles UTF-8 and UTF-8-BOM both); fall back
    # to CP1252, which is the common Windows/Excel export encoding for CSVs
    # from Archer and similar tools.
    try:
        return pd.read_csv(path, dtype=str, encoding="utf-8-sig")
    except UnicodeDecodeError:
        return pd.read_csv(path, dtype=str, encoding="cp1252")


def _estimate_tokens(obj, tokens_per_char: float) -> int:
    # JSON-ified payload char count as a proxy; rough but consistent.
    s = json.dumps(obj, ensure_ascii=False)
    return int(len(s) * tokens_per_char)


def _scale_tokens(base_tokens: int, multiplier: float) -> int:
    return int(base_tokens * multiplier)


def _load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _entity_rows_by_id(df: pd.DataFrame) -> dict[str, pd.Series]:
    return {row["Audit Entity ID"]: row for _, row in df.iterrows()}


def _build_payloads_for_batch(
    batch: FocalBatch,
    entity_rows: dict[str, pd.Series],
    controls_df: pd.DataFrame,
    name_by_id: dict[str, str],
    active_ids: set[str],
    horizontal_flags: dict[str, bool],
    config: dict,
) -> tuple[list[dict], list[dict], list[dict]]:
    target_ids, source_ids = partition_context(batch.focal_ids, entity_rows)

    # Convert focal_control_description_max_tokens (config) to max_chars using
    # the same tokens_per_char heuristic the token estimator uses. None = no
    # truncation (keep existing behavior).
    max_tokens = config.get("focal_control_description_max_tokens")
    tpc = config.get("tokens_per_char", 0.25)
    max_chars = int(max_tokens / tpc) if max_tokens else None

    focal_payloads = []
    for eid in batch.focal_ids:
        row = entity_rows.get(eid)
        if row is None:
            continue
        focal_payloads.append(
            build_focal_payload(
                row,
                controls_df,
                name_by_id,
                active_ids,
                horizontal_flags.get(eid, False),
                include_control_description=True,
                control_description_max_chars=max_chars,
            )
        )

    include_ctrl_desc_target = bool(config.get("target_context_include_control_description", False))
    target_payloads = []
    for eid in sorted(target_ids):
        row = entity_rows.get(eid)
        if row is None:
            continue
        target_payloads.append(
            build_target_context_payload(
                row,
                controls_df,
                name_by_id,
                active_ids,
                horizontal_flags.get(eid, False),
                include_control_description=include_ctrl_desc_target,
            )
        )

    source_payloads = []
    for eid in sorted(source_ids):
        row = entity_rows.get(eid)
        if row is None:
            continue
        source_payloads.append(
            build_source_context_payload(row, name_by_id, active_ids)
        )

    return focal_payloads, target_payloads, source_payloads


def _tokens_for_payloads(
    focal: list[dict],
    target: list[dict],
    source: list[dict],
    config: dict,
) -> tuple[int, int, int, int]:
    tpc = config["tokens_per_char"]
    focal_tokens = sum(_estimate_tokens(p, tpc) for p in focal)
    target_tokens = sum(_estimate_tokens(p, tpc) for p in target)
    source_tokens = sum(_estimate_tokens(p, tpc) for p in source)
    fixed = config["fixed_prompt_overhead_tokens"]
    return focal_tokens, target_tokens, source_tokens, fixed


def _batch_plan(
    batch: FocalBatch,
    entity_rows: dict[str, pd.Series],
    controls_df: pd.DataFrame,
    name_by_id: dict[str, str],
    active_ids: set[str],
    horizontal_flags: dict[str, bool],
    config: dict,
) -> BatchPlan:
    focal, target, source = _build_payloads_for_batch(
        batch, entity_rows, controls_df, name_by_id, active_ids, horizontal_flags, config
    )
    ft, tt, st, fixed = _tokens_for_payloads(focal, target, source, config)
    mult = config.get("worst_case_control_count_multiplier", 1.5)
    # Worst case: assume focal + target control payloads scale by multiplier (source carries no controls, so unchanged).
    worst = int((ft + tt) * mult) + st + fixed
    avg = ft + tt + st + fixed
    target_ids, source_ids = partition_context(batch.focal_ids, entity_rows)
    return BatchPlan(
        batch_id=batch.batch_id,
        focal_ids=batch.focal_ids,
        target_ids=sorted(target_ids),
        source_ids=sorted(source_ids),
        isolated=batch.isolated,
        focal_tokens=ft,
        target_tokens=tt,
        source_tokens=st,
        fixed_tokens=fixed,
        avg_total_tokens=avg,
        worst_case_total_tokens=worst,
    )


def _split_oversized_plan(
    plan: BatchPlan,
    entity_rows: dict[str, pd.Series],
    controls_df: pd.DataFrame,
    name_by_id: dict[str, str],
    active_ids: set[str],
    horizontal_flags: dict[str, bool],
    config: dict,
    controls_per_entity: dict[str, int],
) -> list[BatchPlan]:
    """Peel the highest-control-count focal(s) into a new batch until worst-case fits."""
    if plan.worst_case_total_tokens <= config["hard_token_ceiling"]:
        return [plan]

    remaining = list(plan.focal_ids)
    # Sort focal by descending control count so we peel the biggest first.
    remaining.sort(key=lambda e: -controls_per_entity.get(e, 0))
    split_batches: list[list[str]] = []
    current_group: list[str] = []

    def try_group_plan(group: list[str]) -> BatchPlan:
        temp = FocalBatch(batch_id=-1, focal_ids=sorted(group), isolated=plan.isolated)
        return _batch_plan(temp, entity_rows, controls_df, name_by_id, active_ids, horizontal_flags, config)

    for eid in remaining:
        trial = current_group + [eid]
        trial_plan = try_group_plan(trial)
        if trial_plan.worst_case_total_tokens <= config["hard_token_ceiling"] or not current_group:
            current_group = trial
        else:
            split_batches.append(current_group)
            current_group = [eid]
    if current_group:
        split_batches.append(current_group)

    out: list[BatchPlan] = []
    for i, group in enumerate(split_batches):
        p = try_group_plan(group)
        p.batch_id = plan.batch_id if i == 0 else plan.batch_id + i * 1000  # temp; renumbered later
        p.split_from = plan.batch_id
        out.append(p)
    return out


def _render_prompt(template: str, batch_id: int, focal: list[dict], target: list[dict], source: list[dict]) -> str:
    def dump(payload):
        return json.dumps(payload, ensure_ascii=False, indent=2)
    return (
        template.replace("{batch_id}", f"{batch_id:03d}")
        .replace("{focal_json}", dump(focal))
        .replace("{target_context_json}", dump(target))
        .replace("{source_context_json}", dump(source))
    )


def _write_batch(
    output_root: Path,
    plan: BatchPlan,
    entity_rows: dict[str, pd.Series],
    controls_df: pd.DataFrame,
    name_by_id: dict[str, str],
    active_ids: set[str],
    horizontal_flags: dict[str, bool],
    config: dict,
    template: str,
    skip_if_response_exists: bool = True,
) -> Path:
    batch_dir = output_root / f"batch_{plan.batch_id:03d}"
    response_path = batch_dir / "response.json"
    if skip_if_response_exists and response_path.exists() and response_path.stat().st_size > 0:
        return batch_dir
    batch_dir.mkdir(parents=True, exist_ok=True)
    focal, target, source = _build_payloads_for_batch(
        FocalBatch(batch_id=plan.batch_id, focal_ids=plan.focal_ids, isolated=plan.isolated),
        entity_rows,
        controls_df,
        name_by_id,
        active_ids,
        horizontal_flags,
        config,
    )
    prompt_text = _render_prompt(template, plan.batch_id, focal, target, source)
    (batch_dir / "prompt.md").write_text(prompt_text, encoding="utf-8")
    manifest = asdict(plan)
    manifest["focal_count"] = len(plan.focal_ids)
    manifest["target_count"] = len(plan.target_ids)
    manifest["source_count"] = len(plan.source_ids)
    (batch_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return batch_dir


def run(
    risk_assessment_path: Path,
    controls_path: Path,
    output_root: Path,
    config_path: Path,
    dry_run: bool,
) -> dict:
    config = _load_config(config_path)
    template = PROMPT_TEMPLATE.read_text(encoding="utf-8")

    print(f"[generate] reading {risk_assessment_path}")
    df_raw = _read_table(risk_assessment_path)
    focal_df, referenceable_df, class_stats = classify_entities(df_raw)
    print(
        f"[generate] classified: focal={class_stats['focal_count']} "
        f"referenceable={class_stats['referenceable_count']} "
        f"(referenceable-only={class_stats['referenceable_only_count']}) "
        f"dropped={class_stats['dropped_count']}"
    )

    # Nodes / horizontal flags / name lookup span all referenceable entities so that
    # inactive-referenceable partners resolve to real names and the graph-construction
    # helpers can reason about them. Focal assignment uses only focal_ids.
    all_nodes = build_nodes(referenceable_df, HORIZONTAL_KEYWORDS)
    focal_nodes = all_nodes[all_nodes["Audit Entity ID"].isin(set(focal_df["Audit Entity ID"]))].reset_index(drop=True)

    focal_ids = set(focal_df["Audit Entity ID"])
    referenceable_ids = set(referenceable_df["Audit Entity ID"])
    name_by_id = dict(zip(all_nodes["Audit Entity ID"], all_nodes["Audit Entity Name"]))
    horizontal_flags = {
        r["Audit Entity ID"]: (r.get("Horizontal Flag") == "horizontal")
        for _, r in all_nodes.iterrows()
    }

    print(f"[generate] reading {controls_path}")
    controls_df = _read_table(controls_path)
    controls_per_entity = (
        controls_df.groupby("Audit Entity (Audit Controls)").size().to_dict()
        if not controls_df.empty
        else {}
    )

    # Handoffs built from focal entities' rows; unmatched check against the full
    # referenceable universe so inactive-referenceable partners don't get flagged
    # as unmatched. Dropped-type partner IDs remain unmatched (correct behavior).
    handoffs = build_handoffs(focal_df, referenceable_ids)

    # Focal-to-focal subgraph drives Louvain community detection. Handoffs between
    # focal and inactive-referenceable entities are preserved in the full handoffs
    # table for payload context but don't influence focal clustering.
    focal_to_focal_handoffs = handoffs[
        handoffs["Source Entity ID"].isin(focal_ids)
        & handoffs["Target Entity ID"].isin(focal_ids)
    ].reset_index(drop=True)
    print(
        f"[generate] handoff rows: total={len(handoffs)} focal-to-focal={len(focal_to_focal_handoffs)}"
    )

    batches = select_focal_batches(
        focal_nodes,
        focal_to_focal_handoffs,
        focal_per_batch=config["focal_per_batch"],
        resolution=config["louvain_resolution"],
        seed=config["louvain_seed"],
    )
    G = build_undirected_handoff_graph(focal_nodes, focal_to_focal_handoffs)
    severed = severed_edge_count(G, batches)
    print(f"[generate] initial batches={len(batches)} severed_edges={severed}/{G.number_of_edges()}")

    # Entity rows cover all referenceable entities so target/source context
    # payloads can render for inactive-referenceable partners too.
    entity_rows = _entity_rows_by_id(referenceable_df)

    # Pass focal_ids as the "active_ids" arg to payload builders: inactive_flag on
    # a handoff partner is True iff the partner is not focal-eligible (covers both
    # inactive-referenceable and dropped partners).
    plans = [
        _batch_plan(b, entity_rows, controls_df, name_by_id, focal_ids, horizontal_flags, config)
        for b in batches
    ]

    # Auto-split plans over hard_token_ceiling (worst case).
    ceiling = config["hard_token_ceiling"]
    final_plans: list[BatchPlan] = []
    for p in plans:
        if p.worst_case_total_tokens > ceiling:
            pieces = _split_oversized_plan(
                p, entity_rows, controls_df, name_by_id, focal_ids, horizontal_flags, config, controls_per_entity
            )
            final_plans.extend(pieces)
        else:
            final_plans.append(p)
    # Renumber batches sequentially.
    for i, p in enumerate(final_plans, start=1):
        p.batch_id = i

    over_ceiling = [p for p in final_plans if p.worst_case_total_tokens > ceiling]
    if over_ceiling:
        print(
            f"[generate] WARNING {len(over_ceiling)} batches still over worst-case ceiling "
            f"after split — inspect dry-run summary"
        )

    # Write dry-run summary always.
    output_root.mkdir(parents=True, exist_ok=True)
    summary_path = output_root.parent / "_dry_run_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    _write_dry_run_summary(summary_path, final_plans, config, severed, G.number_of_edges())
    print(f"[generate] dry-run summary -> {summary_path}")

    if dry_run:
        return {"plans": final_plans, "summary_path": summary_path, "dry_run": True}

    for p in final_plans:
        _write_batch(
            output_root, p, entity_rows, controls_df, name_by_id, focal_ids,
            horizontal_flags, config, template, skip_if_response_exists=True,
        )
    print(f"[generate] wrote {len(final_plans)} batches -> {output_root}")

    return {"plans": final_plans, "summary_path": summary_path, "dry_run": False}


def _write_dry_run_summary(
    path: Path,
    plans: list[BatchPlan],
    config: dict,
    severed: int,
    total_edges: int,
) -> None:
    lines = ["# Stage 2 Batching — Dry Run Summary", ""]
    lines.append(f"Batches: **{len(plans)}**")
    lines.append(f"Target budget: {config['target_token_budget']:,} tokens")
    lines.append(f"Hard ceiling: {config['hard_token_ceiling']:,} tokens")
    lines.append(f"Worst-case multiplier: {config.get('worst_case_control_count_multiplier', 1.5)}")
    lines.append(f"Severed handoff edges: {severed} / {total_edges} "
                 f"(coverage remains via target/source context)")
    lines.append("")
    lines.append("| # | Focal | Target ctx | Source ctx | Avg tokens | Worst-case tokens | Isolated | Split from |")
    lines.append("|---|-------|------------|------------|------------|-------------------|----------|------------|")
    for p in plans:
        lines.append(
            f"| {p.batch_id:03d} | {len(p.focal_ids)} | {len(p.target_ids)} | {len(p.source_ids)} | "
            f"{p.avg_total_tokens:,} | {p.worst_case_total_tokens:,} | "
            f"{'Y' if p.isolated else ''} | {p.split_from if p.split_from else ''} |"
        )
    lines.append("")
    avg_tokens = [p.avg_total_tokens for p in plans]
    worst_tokens = [p.worst_case_total_tokens for p in plans]
    lines.append(f"Avg batch (mean/max): {int(sum(avg_tokens)/len(avg_tokens)):,} / {max(avg_tokens):,}")
    lines.append(f"Worst-case batch (mean/max): {int(sum(worst_tokens)/len(worst_tokens)):,} / {max(worst_tokens):,}")
    lines.append("")
    lines.append("## Focal composition per batch")
    for p in plans:
        lines.append(f"- **batch_{p.batch_id:03d}:** focal={p.focal_ids}")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--risk-assessment", type=Path, default=DEFAULT_RISK_ASSESSMENT)
    parser.add_argument("--controls", type=Path, default=DEFAULT_CONTROLS)
    parser.add_argument("--output", type=Path, default=OUTPUT_ROOT)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(args.risk_assessment, args.controls, args.output, args.config, args.dry_run)


if __name__ == "__main__":
    main()
