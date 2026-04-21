# Stage 2 Batching Design Proposal (v2)

Fresh rewrite after the controls-as-primary-evidence reframe. Supersedes v1 in its entirety. Companion to `handoff_stage2_data_spec.md` v2 and `handoff_stage2_prompt_revisions.md`.

---

## 1. What changed from v1

- Control-layer payloads (10–30 controls per entity with Specific Risk + KPA tags + full description on focal) dominate token budget. Focal and target-context payloads are roughly 3–5× bigger than v1 assumed.
- Token budget per batch raised from 60k to **~85k** prompt target, leaving 30–40k for the model's reasoning and response within ChatGPT Pro's context window.
- Focal-per-batch dropped from 15 to **10**, projecting ~43 batches at real-data scale (vs. 29 in v1). Still under the user's 50-batch ceiling.
- Context payload is **direction-aware** (target vs. source), not uniform.
- Added a **quality gate** after calibration batch 1 that must pass before batch 2 is written.
- Generated prompts and pasted responses live under `runs/stage2/` (gitignored), not `data/output/`.

---

## 2. Locked-in design decisions (user-confirmed)

- **Delivery:** manual paste into ChatGPT Pro web UI with extended thinking. One prompt per batch, one pasted response per batch.
- **Batch count ceiling:** up to 50 batches.
- **Ordering:** doesn't matter; strict graph-derived order is fine.
- **Approach:** focal + 1-hop context over disjoint partitions (approved).
- **Pass 1 disagreement report:** out of scope for now.
- **Prompt format:** Markdown with fenced JSON code blocks.
- **Repo layout:** `src/stage2_handoff_review/` for code, `runs/stage2/batches/` and `runs/stage2/aggregated/` for artifacts (gitignored), `config/stage2_batching.json` for tuning parameters.

---

## 3. Batch unit: focal + direction-aware context

Each batch has three sections:

1. **Focal entities (K ≈ 10).** Fully evaluated for all 5 Stage 2 tasks. Each active entity is focal in exactly one batch.
2. **Target-context entities.** Every entity B such that some focal A has `handoff_to` → B. Richer payload: controls list (compact form), Specific Risk + KPA coverage rollups, 14-category ratings, entity context. Purpose: Task 5 receiving-entity coverage check.
3. **Source-context entities.** Every entity C such that some focal A has `handoff_from` ← C (C→A). Lean payload: ID, name, handoff-description prose, structured handoffs only. Purpose: cross-check that C's description of what it handed off matches what A describes receiving.

Deduplication:
- If B is focal in this batch, don't include it as target-context — focal payload serves both.
- If B handed off to A and A handed off to B (bidirectional), include once as target-context.
- An entity that's focal in a *different* batch still appears as context here (we're not coordinating cross-batch visibility — every batch self-contained).

---

## 4. Token math

### Per-role estimates (real data)

| Role | Fields | Tokens / entity |
|---|---|---|
| Focal | overview + handoff prose + structured handoffs + 14-cat ratings (applicable only) + 20 controls with full descriptions + Specific Risk + KPA | ~6,500 |
| Target context | name + BU + handoff prose + 14-cat ratings + 20 controls **without description** (title + SR + KPA only) + SR/KPA coverage rollups | ~1,500 |
| Source context | name + handoff prose + structured handoffs | ~300 |
| Fixed overhead per batch | framework, Stage 1 findings table, task instructions, output schema | ~4,000 |

### Projected batch size (K=10 focal)

- Focal: 10 × 6,500 = 65,000
- Target context (estimate 10 unique per batch): 10 × 1,500 = 15,000
- Source context (estimate 8 unique per batch): 8 × 300 = 2,400
- Fixed: 4,000
- **Total ≈ 86,400 tokens prompt**

Leaves 30–40k for the model's extended-thinking reasoning and response at ChatGPT Pro's context ceiling. Tight but workable. Calibration batch will confirm.

### Sensitivity and worst-case modeling

The estimate varies most with control count per entity (10 → 30 makes focal payload swing by ±3,000 tokens per entity, ±30k per batch at K=10) and with handoff-description prose length. Averages hide the risk: a batch loaded with high-control-count focal entities can blow the target before context or overhead is even considered.

**Dry-run must project worst-case per batch, not just average:**
- For each proposed batch, compute token estimate assuming every focal + context entity hits the upper-bound control count observed in its source data (or a configurable 90th-percentile bound).
- Any batch whose worst-case projection exceeds `hard_token_ceiling` (default 110k) is **auto-split** by the generator into two smaller batches before prompt files are written, not just flagged for inspection. Splitting picks the highest-control-count focal(s) and peels them into a new batch, preserving Louvain clustering as much as possible.
- Batches auto-split for token reasons are noted in the dry-run summary so the user can see where the binding constraint hit.

Fallback levers if auto-splitting produces too many batches (blows the 50 cap):
- Reduce K proactively (e.g., K=8 → 34 base batches with headroom for splits).
- Compact focal control payloads (truncate `Control Description` to first 200 tokens, full SR + KPA).
- Target-context already lean; no further compaction available without losing SR/KPA coverage rollups needed for Task 5.

---

## 5. Focal selection algorithm

1. Build undirected handoff graph over active entities.
2. Run Louvain modularity (resolution=1.0, seed=42) → candidate communities.
3. For each community:
   - If `size ≤ K`: it becomes one batch.
   - If `size > K`: subdivide by repeated Louvain calls at higher resolution, or by edge-weighted k-way partitioning targeting K.
   - If `size < K/2`: mark mergeable; merge with the smallest neighboring community whose combined size stays ≤ K.
4. Isolated entities (no handoffs): one dedicated "isolated" batch at the end, evaluated for Tasks 1, 2, 3, 4 only (Task 5 is N/A).
5. Log for each batch: focal IDs, severed-edge count (A→B with A focal here and B focal elsewhere — B still appears as context so check remains possible, but it's useful telemetry).

Dummy smoke test for this algorithm: 45 entities, one giant component, Louvain at default finds 5 communities of 14/12/8/6/5 → produces batches of sizes 10, 10 (split from 14), 8, 6, 5 (the 12 splits to 10+2, the 2 merges into the 5-community → 7). Final: 5 batches. Fine for dummy testing.

---

## 6. Pre-filters (before focal assignment)

1. Drop entities already filtered by Stage 1 (inactive, special-review). Honor `Nodes` table.
2. Keep entities with empty `Hand-off Description` — absence is itself a finding for Task 1.
3. Keep entities with all 14 risks = NA — evaluated only for Tasks 1 and 5 (appearing as handoff target).
4. Keep entities with zero controls — flag in payload (`controls: []`, `specific_risk_coverage: []`). If this is common in real data, it indicates a data-pull gap worth surfacing before burning API calls.
5. Unmatched handoff IDs stay inline as `{id, name: "(inactive or filtered)", inactive_flag: true}`; don't pull them as context entities.

---

## 7. Prompt file structure (Markdown, ready to paste)

```
# Stage 2 Handoff Review — Batch NN

[Header and role instructions]

## Framework
[Handoff vs reliance, risk ownership, coarse-handoff failure mode — from context doc §1–2]

## Manual review findings (Stage 1)
[Prioritized gaps + silent/ambiguous items — from context doc §3]

## Evaluation tasks
[5 revised tasks — see handoff_stage2_prompt_revisions.md]

## Focal entities (evaluate these)
```json
[ {focal entity 1}, {focal entity 2}, ... ]
```

## Target-context entities (handoff targets — reference for Task 5 coverage checks; do not evaluate)
```json
[ {target 1}, {target 2}, ... ]
```

## Source-context entities (handoff sources — reference for reciprocity checks; do not evaluate)
```json
[ {source 1}, {source 2}, ... ]
```

## Output format
[Strict JSON schema with per-finding fields (including `specific_risk_ids` as an array, `evidence_layer` enum, task-numbered findings) and ranked-summary schema. Full schema defined in `handoff_stage2_prompt_revisions.md` under "OUTPUT format — revision." Instruct model to emit one top-level ```json code block.]
```

Each batch's `prompt.md` is self-contained. The header/framework/findings/tasks/output-format blocks are identical across batches; only the three JSON payloads vary.

---

## 8. Quality gate (NEW — must pass before batch 2)

After you paste batch 1 into ChatGPT and paste the response back into `runs/stage2/batches/batch_01/response.json`, the aggregator runs **gate checks** and refuses to generate batch 2's prompt file until all pass:

1. **Response is valid JSON** matching the declared output schema.
2. **Findings are scoped to focal entities only.** Any finding keyed to an entity listed in target-context or source-context sections fails the gate.
3. **Task 5 findings exist for at least one handoff pair present in the batch.** (If none of the batch's handoffs generated a finding, the prompt or the payload is probably not letting the model reach cross-entity reasoning.)
4. **Control-layer grounding — split thresholds by task:**
   - **Task 3 findings: ≥70% must cite a Control Description, Specific Risk, or KPA by ID or quoted text.** Task 3 is literally a control-layer evaluation (program-level vs embedded-process-level); near-100% control-layer citation is expected. 70% is the floor.
   - **Task 5 findings: ≥50% must cite control-layer evidence.** Task 5 step 4 (reciprocity check against B's handoff description and overview prose) legitimately cites entity-level prose, so the threshold is relaxed.
   - **Either task falling below its threshold fails the gate.** A single combined threshold would let Task 5 carry the average while Task 3 operates at the wrong layer — the split catches that.
5. **Response includes a ranked summary section** as the prompt requires.

A failed gate prints the specific check(s) that failed and the corrective action (revise prompt wording, revise payload field emphasis, re-run batch 1). The batch generator won't write batch_02+ until the gate passes or you pass an explicit `--override-gate` flag for debugging.

---

## 9. Dry-run mode

`python -m src.stage2_handoff_review.generate --dry-run` outputs `runs/stage2/batches/_dry_run_summary.md`:

- Per batch: focal IDs, target-context count, source-context count, token estimates (focal total, context total, fixed, grand total)
- Totals: batch count, min/max/avg tokens/batch, total focal coverage (should equal active-entity count), severed-edge metric
- Any batches estimated over a configurable ceiling (default 110k) flagged as "likely to exceed ChatGPT context"
- No prompt files written

You inspect, approve, and re-run without `--dry-run` to generate actual prompt files.

---

## 10. Calibration against dummy

Two dummy runs before real data:

1. **Dry run** against `dummy_audit_universe_50.csv` + a stub controls CSV (I'll generate a ~150-row dummy controls file with plausible Specific Risks / KPAs for testing mechanics). Confirm batch composition and token math plausible.
2. **Live batch 1** against dummy. Paste into ChatGPT Pro. Run gate checks. Iterate on prompt or payload until gate passes. Document final parameters.

Explicitly acknowledge: dummy will produce weak findings because dummy's handoff-description prose is boilerplate and the stub controls won't mirror real coverage patterns. The goal of dummy testing is **mechanics**, not findings quality.

---

## 11. Parameterization (`config/stage2_batching.json`)

Tuning surface exposed as config so real-data calibration doesn't require code edits:

- `focal_per_batch` (default 10)
- `target_token_budget` (default 85000)
- `hard_token_ceiling` (default 110000; batches over this flagged in dry-run)
- `louvain_resolution` (default 1.0)
- `louvain_seed` (default 42)
- `target_context_include_control_description` (default false — descriptions dropped from target context to save tokens)
- `focal_control_description_max_tokens` (default unlimited; set to e.g. 200 if calibration shows we need truncation)

---

## 12. Repo layout (confirmed)

```
src/stage2_handoff_review/
  __init__.py
  generate.py            # batch prompt generator + dry-run
  aggregate.py           # parse pasted responses, run gate, merge findings
  graph.py               # Louvain focal selection
  payload.py             # builds focal / target / source payloads
  templates/
    prompt.md            # Markdown skeleton with placeholders
    output_schema.json   # the JSON schema the model is asked to fill
config/
  stage2_batching.json
runs/stage2/              # GITIGNORED — contains generated prompts + pasted responses + aggregated findings
  batches/
    batch_01/
      prompt.md
      manifest.json
      response.json       # user pastes ChatGPT output here
    batch_02/
      ...
  aggregated/
    findings.csv
    ranked_summary.md
    gate_log.md
```

Add to `.gitignore`:
```
runs/
```

---

## 13. Build order (once this proposal is approved)

1. Stub controls CSV generator for dummy data (~150 rows across 45 entities with plausible Specific Risks and KPAs).
2. `src/stage2_handoff_review/graph.py` — Louvain focal selection + severed-edge metric.
3. `src/stage2_handoff_review/payload.py` — direction-aware payload builders with the derived fields from §5 of the data spec.
4. `src/stage2_handoff_review/generate.py` — orchestration + dry-run mode.
5. `src/stage2_handoff_review/aggregate.py` — gate + findings merge.
6. Dry-run against dummy, inspect summary, adjust parameters.
7. Live batch 1 against dummy, run gate, iterate.

---

## 14. Open questions — resolved (2026-04-20)

1. **Stub controls CSV:** synthesize with deliberately seeded coarse-handoff patterns so the calibration batch can test whether Task 3 actually fires when the pattern is present. Random plausible tagging alone is insufficient for calibration.
2. **Target-context control descriptions:** dropped. Keep Title + SR + KPA only.
3. **Severed-edge escalation:** dropped. SR + KPA is the evidence layer. If that's true, B with more controls doesn't need richer representation. Revisit only if Task 5 findings are weak after calibration.
4. **Gate threshold:** split by task — Task 3 ≥70%, Task 5 ≥50%. See §8 check #4.
