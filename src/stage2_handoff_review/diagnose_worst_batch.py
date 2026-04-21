"""Diagnostic for the batch with the highest projected worst-case tokens.

Runs the same classify -> Louvain -> pack -> auto-split pipeline as the
generator, but stops before writing prompt files. Identifies the batch
with the highest worst-case projection and prints a per-component token
breakdown so the bottleneck is visible.

Role labels only (focal_1, target_1, ...). No entity names or IDs are
printed. Output goes to stdout only — no files written.

Usage:
    python -m src.stage2_handoff_review.diagnose_worst_batch
    python -m src.stage2_handoff_review.diagnose_worst_batch \\
        --risk-assessment /path/to/real.csv \\
        --controls /path/to/real_controls.csv
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.stage1_filter import classify_entities  # noqa: E402
from src.stage2_nodes import build_nodes  # noqa: E402
from src.stage4_relational import build_handoffs  # noqa: E402
from src.stage2_handoff_review.graph import (  # noqa: E402
    FocalBatch,
    select_focal_batches,
)
from src.stage2_handoff_review.generate import (  # noqa: E402
    DEFAULT_CONFIG,
    DEFAULT_CONTROLS,
    DEFAULT_RISK_ASSESSMENT,
    HORIZONTAL_KEYWORDS,
    _batch_plan,
    _build_payloads_for_batch,
    _entity_rows_by_id,
    _load_config,
    _read_table,
    _split_oversized_plan,
)


def _tok(obj, tpc: float) -> int:
    return int(len(json.dumps(obj, ensure_ascii=False)) * tpc)


FOCAL_COMPONENTS = [
    "meta", "overview", "handoff", "structured_handoffs",
    "ratings", "rationale", "ctrl_prose", "controls", "sr_kpa",
]
TARGET_COMPONENTS = [
    "meta", "handoff", "structured_handoffs",
    "ratings", "controls_compact", "sr_kpa",
]


def _focal_breakdown(p: dict, tpc: float) -> dict:
    risks = p.get("risks", []) or []
    return {
        "meta": _tok({k: p.get(k) for k in ("entity_id", "entity_name", "business_unit", "line_of_defense", "horizontal_flag")}, tpc),
        "overview": _tok(p.get("overview", ""), tpc),
        "handoff": _tok(p.get("handoff_description", ""), tpc),
        "structured_handoffs": _tok({"to": p.get("handoffs_to", []), "from": p.get("handoffs_from", [])}, tpc),
        "ratings": _tok(
            [{k: r.get(k) for k in ("risk_category", "residual_rating", "inherent_rating", "control_assessment_rating")} for r in risks],
            tpc,
        ),
        "rationale": _tok([r.get("inherent_rationale", "") for r in risks], tpc),
        "ctrl_prose": _tok([r.get("control_assessment_prose", "") for r in risks], tpc),
        "controls": _tok(p.get("controls", []), tpc),
        "sr_kpa": _tok({"sr": p.get("specific_risk_coverage", []), "kpa": p.get("kpa_coverage", [])}, tpc),
    }


def _target_breakdown(p: dict, tpc: float) -> dict:
    return {
        "meta": _tok({k: p.get(k) for k in ("entity_id", "entity_name", "business_unit", "line_of_defense", "role", "horizontal_flag")}, tpc),
        "handoff": _tok(p.get("handoff_description", ""), tpc),
        "structured_handoffs": _tok({"to": p.get("handoffs_to", []), "from": p.get("handoffs_from", [])}, tpc),
        "ratings": _tok(p.get("risks", []), tpc),
        "controls_compact": _tok(p.get("controls_compact", []), tpc),
        "sr_kpa": _tok({"sr": p.get("specific_risk_coverage", []), "kpa": p.get("kpa_coverage", [])}, tpc),
    }


def _fmt(n: int) -> str:
    return f"{n:,}"


def _print_table(headers: list[str], rows: list[list[str]], col_widths: list[int]) -> None:
    fmt_parts = []
    for i, w in enumerate(col_widths):
        align = "<" if i == 0 else ">"
        fmt_parts.append(f"{{:{align}{w}}}")
    fmt = "  ".join(fmt_parts)
    print(fmt.format(*headers))
    print(fmt.format(*["-" * w for w in col_widths]))
    for row in rows:
        print(fmt.format(*row))


def run_diagnostic(risk_path: Path, controls_path: Path, config_path: Path, show_ids: bool = False) -> None:
    config = _load_config(config_path)
    tpc = config.get("tokens_per_char", 0.25)

    df_raw = _read_table(risk_path)
    focal_df, referenceable_df, _class_stats = classify_entities(df_raw)

    # Apply exclusion list from config. Excluded entities stay referenceable
    # (still resolve as handoff partners for other focal entities) but do not
    # appear as focal themselves. This is the same rule applied in generate.py.
    excluded = set(config.get("exclude_entity_ids", []) or [])
    if excluded:
        before = len(focal_df)
        focal_df = focal_df[~focal_df["Audit Entity ID"].isin(excluded)].reset_index(drop=True)
        print(f"[diagnose] excluded {before - len(focal_df)} entities from focal per config: {sorted(excluded)}")

    all_nodes = build_nodes(referenceable_df, HORIZONTAL_KEYWORDS)
    focal_ids = set(focal_df["Audit Entity ID"])
    referenceable_ids = set(referenceable_df["Audit Entity ID"])
    focal_nodes = all_nodes[all_nodes["Audit Entity ID"].isin(focal_ids)].reset_index(drop=True)
    name_by_id = dict(zip(all_nodes["Audit Entity ID"], all_nodes["Audit Entity Name"]))
    horizontal_flags = {
        r["Audit Entity ID"]: (r.get("Horizontal Flag") == "horizontal")
        for _, r in all_nodes.iterrows()
    }

    controls_df = _read_table(controls_path)
    controls_per_entity = (
        controls_df.groupby("Audit Entity (Audit Controls)").size().to_dict()
        if not controls_df.empty else {}
    )

    handoffs = build_handoffs(focal_df, referenceable_ids)
    focal_to_focal = handoffs[
        handoffs["Source Entity ID"].isin(focal_ids)
        & handoffs["Target Entity ID"].isin(focal_ids)
    ].reset_index(drop=True)

    batches = select_focal_batches(
        focal_nodes,
        focal_to_focal,
        focal_per_batch=config["focal_per_batch"],
        resolution=config["louvain_resolution"],
        seed=config["louvain_seed"],
    )
    entity_rows = _entity_rows_by_id(referenceable_df)

    plans = [
        _batch_plan(b, entity_rows, controls_df, name_by_id, focal_ids, horizontal_flags, config)
        for b in batches
    ]
    ceiling = config["hard_token_ceiling"]
    final_plans = []
    for p in plans:
        if p.worst_case_total_tokens > ceiling:
            final_plans.extend(_split_oversized_plan(
                p, entity_rows, controls_df, name_by_id, focal_ids, horizontal_flags, config, controls_per_entity
            ))
        else:
            final_plans.append(p)
    for i, p in enumerate(final_plans, start=1):
        p.batch_id = i

    worst = max(final_plans, key=lambda p: p.worst_case_total_tokens)

    focal_payloads, target_payloads, source_payloads = _build_payloads_for_batch(
        FocalBatch(batch_id=worst.batch_id, focal_ids=worst.focal_ids, isolated=worst.isolated),
        entity_rows, controls_df, name_by_id, focal_ids, horizontal_flags, config,
    )

    focal_bd = [_focal_breakdown(p, tpc) for p in focal_payloads]
    target_bd = [_target_breakdown(p, tpc) for p in target_payloads]
    source_each = [_tok(p, tpc) for p in source_payloads]

    fixed = config.get("fixed_prompt_overhead_tokens", 4000)
    focal_total = sum(sum(bd.values()) for bd in focal_bd)
    target_total = sum(sum(bd.values()) for bd in target_bd)
    source_total = sum(source_each)
    grand = focal_total + target_total + source_total + fixed

    mult = config.get("worst_case_control_count_multiplier", 1.5)
    worst_proj = int((focal_total + target_total) * mult) + source_total + fixed
    over = worst_proj - ceiling

    # Header
    print("=" * 72)
    print(f"Worst-case batch: batch_{worst.batch_id:03d}   ({len(final_plans)} total batches)")
    print(
        f"Config: focal_per_batch={config['focal_per_batch']}  "
        f"louvain_resolution={config['louvain_resolution']}  "
        f"focal_control_description_max_tokens={config.get('focal_control_description_max_tokens')}"
    )
    print(
        f"Batch size: focal={len(worst.focal_ids)}  "
        f"target_ctx={len(worst.target_ids)}  "
        f"source_ctx={len(worst.source_ids)}"
    )
    print("=" * 72)
    print()
    print(f"Average (pre-multiplier) total:  {_fmt(grand):>10} tokens")
    print(f"Worst-case (post-multiplier):    {_fmt(worst_proj):>10} tokens   (multiplier {mult})")
    print(f"Hard ceiling:                    {_fmt(ceiling):>10} tokens")
    if over > 0:
        print(f"Over ceiling by:                 {_fmt(over):>10} tokens")
    else:
        print(f"Under ceiling by:                {_fmt(-over):>10} tokens")
    print()

    # Role rollup (average)
    def pct(n: int) -> str:
        return f"{100*n/grand:.1f}%" if grand else "--"

    print("Role rollup (average, pre-multiplier):")
    _print_table(
        ["role", "tokens", "% of total"],
        [
            ["fixed_overhead", _fmt(fixed), pct(fixed)],
            [f"focal total [{len(focal_bd)} entities]", _fmt(focal_total), pct(focal_total)],
            [f"target-ctx total [{len(target_bd)} entities]", _fmt(target_total), pct(target_total)],
            [f"source-ctx total [{len(source_each)} entities]", _fmt(source_total), pct(source_total)],
            ["grand total", _fmt(grand), "100.0%"],
        ],
        col_widths=[38, 12, 10],
    )
    print()

    # Role label helpers — when show_ids is True, append entity ID to each
    # role label so the user can cross-reference to the CSV. Privacy-preserving
    # default stays anonymous.
    def focal_label(i: int) -> str:
        base = f"focal_{i}"
        if show_ids:
            return f"{base} ({focal_payloads[i-1].get('entity_id', '?')})"
        return base

    def target_label(i: int) -> str:
        base = f"target_{i}"
        if show_ids:
            return f"{base} ({target_payloads[i-1].get('entity_id', '?')})"
        return base

    focal_label_width = max([len(focal_label(i)) for i in range(1, len(focal_bd) + 1)] + [len("MAX")], default=8)
    target_label_width = max([len(target_label(i)) for i in range(1, len(target_bd) + 1)] + [len("MAX")], default=10)

    # Focal breakdown
    if focal_bd:
        headers = ["role"] + FOCAL_COMPONENTS + ["subtotal"]
        rows = []
        for i, bd in enumerate(focal_bd, 1):
            subtotal = sum(bd.values())
            rows.append([focal_label(i)] + [_fmt(bd[c]) for c in FOCAL_COMPONENTS] + [_fmt(subtotal)])
        means = {c: sum(bd[c] for bd in focal_bd) // len(focal_bd) for c in FOCAL_COMPONENTS}
        maxs = {c: max(bd[c] for bd in focal_bd) for c in FOCAL_COMPONENTS}
        rows.append(["MEAN"] + [_fmt(means[c]) for c in FOCAL_COMPONENTS] + [_fmt(sum(means.values()))])
        rows.append(["MAX"] + [_fmt(maxs[c]) for c in FOCAL_COMPONENTS] + [_fmt(sum(maxs.values()))])
        print(f"Focal breakdown ({len(focal_bd)} entities, tokens per component):")
        _print_table(headers, rows, col_widths=[focal_label_width] + [10] * len(FOCAL_COMPONENTS) + [10])
        print()

    # Target-context breakdown
    if target_bd:
        headers = ["role"] + TARGET_COMPONENTS + ["subtotal"]
        rows = []
        for i, bd in enumerate(target_bd, 1):
            subtotal = sum(bd.values())
            rows.append([target_label(i)] + [_fmt(bd[c]) for c in TARGET_COMPONENTS] + [_fmt(subtotal)])
        means = {c: sum(bd[c] for bd in target_bd) // len(target_bd) for c in TARGET_COMPONENTS}
        maxs = {c: max(bd[c] for bd in target_bd) for c in TARGET_COMPONENTS}
        rows.append(["MEAN"] + [_fmt(means[c]) for c in TARGET_COMPONENTS] + [_fmt(sum(means.values()))])
        rows.append(["MAX"] + [_fmt(maxs[c]) for c in TARGET_COMPONENTS] + [_fmt(sum(maxs.values()))])
        print(f"Target-ctx breakdown ({len(target_bd)} entities, tokens per component):")
        _print_table(headers, rows, col_widths=[target_label_width] + [14] * len(TARGET_COMPONENTS) + [10])
        print()

    # Source-ctx summary
    if source_each:
        mean_src = sum(source_each) // len(source_each)
        max_src = max(source_each)
        print(
            f"Source-ctx: total {_fmt(source_total)} tokens across {len(source_each)} entities "
            f"(mean {_fmt(mean_src)}, max {_fmt(max_src)}). Lean payload, no per-entity breakdown."
        )
    else:
        print("Source-ctx: none")

    # Highest-subtotal focal — identify which focal_k is the driver.
    # ID revealed only with --show-ids; otherwise points at the role label.
    if focal_bd:
        totals = [sum(bd.values()) for bd in focal_bd]
        worst_idx = max(range(len(totals)), key=lambda i: totals[i])
        id_hint = (
            focal_payloads[worst_idx].get("entity_id", "?")
            if show_ids
            else "(rerun with --show-ids to reveal entity_id)"
        )
        print()
        print(
            f"Highest-subtotal focal in this batch: focal_{worst_idx+1}  "
            f"subtotal {_fmt(totals[worst_idx])} tokens  ->  {id_hint}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--risk-assessment", type=Path, default=DEFAULT_RISK_ASSESSMENT)
    parser.add_argument("--controls", type=Path, default=DEFAULT_CONTROLS)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument(
        "--show-ids",
        action="store_true",
        help="Append entity_id to each role label (focal_1 (AE-XXX)) and reveal "
             "the highest-subtotal focal's entity_id. Off by default so the "
             "output is safe to share in structural summaries.",
    )
    args = parser.parse_args()
    run_diagnostic(args.risk_assessment, args.controls, args.config, show_ids=args.show_ids)


if __name__ == "__main__":
    main()
