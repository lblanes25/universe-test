"""Single-source-of-truth loader for Stage 2 prompt content + finding labels.

Reads `config/stage2_prompt.yaml`. Provides:
  - Value sets (for validation in aggregate.py)
  - value -> display maps (for human-readable output)
  - Key list (for ranked_summary structural checks)
  - Markdown renderers for the framework section and the tasks section
    (consumed by generate.py when assembling each batch's prompt.md)

Edit `config/stage2_prompt.yaml` to rename labels or rework task / framework
content in one place.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
LABELS_PATH = ROOT / "config" / "stage2_prompt.yaml"


@lru_cache(maxsize=1)
def _load() -> dict:
    return yaml.safe_load(LABELS_PATH.read_text(encoding="utf-8"))


# ---------- task display + body ----------

def task_displays() -> dict[int, str]:
    return {int(t["id"]): t["display"] for t in _load()["tasks"]}


def render_tasks_section() -> str:
    """Render the full `## Tasks` body — 5 task blocks, separated by one blank line.

    Each block is `### Task {id} — {display}` then a blank line then `body`.
    No trailing newline; the template supplies the surrounding spacing.
    """
    parts = []
    for t in _load()["tasks"]:
        parts.append(f"### Task {t['id']} — {t['display']}\n\n{t['body'].rstrip()}")
    return "\n\n".join(parts)


# ---------- framework definitions ----------

def render_framework_section() -> str:
    """Render the 4 framework bullets as a single markdown list, no trailing newline."""
    f = _load()["framework"]
    bullets = [
        f["handoff_definition"],
        f["reliance_definition"],
        f["scope_statement"],
        f["coarse_handoff_failure_mode"],
    ]
    return "\n".join(f"- {b.strip()}" for b in bullets)


# ---------- classification labels ----------

def classification_values() -> set[str]:
    return {c["value"] for c in _load()["classifications"]}


def classification_displays() -> dict[str, str]:
    return {c["value"]: c["display"] for c in _load()["classifications"]}


# ---------- evidence layer labels ----------

def evidence_layer_values() -> set[str]:
    return {e["value"] for e in _load()["evidence_layers"]}


def evidence_layer_displays() -> dict[str, str]:
    return {e["value"]: e["display"] for e in _load()["evidence_layers"]}


# ---------- ranked summary buckets ----------

def ranked_summary_keys() -> list[str]:
    return [b["key"] for b in _load()["ranked_summary_buckets"]]


def ranked_summary_displays() -> dict[str, str]:
    return {b["key"]: b["display"] for b in _load()["ranked_summary_buckets"]}
