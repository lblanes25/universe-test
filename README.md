# Audit Universe Network Map & Handoff/Reliance Review

> **What this document is.** A plain-English overview of the project, written so anyone
> on the team can read it (or ask an AI assistant about it) and understand what we built,
> why, how it works, what it found, and — just as important — what it *can't* tell you.
> It assumes audit domain knowledge but explains the technical and AI pieces from scratch.

---

## 1. The one-sentence version

When we hand a risk off from one audit entity to another, **can we prove the receiving
entity actually covers it — at the level it was transferred?** Today, nobody can answer
that across ~427 entities and ~4,400 handoffs. This project builds the data and the AI
evaluation that gets us there.

---

## 2. Why this exists

Internal audit breaks the business into **audit entities (AEs)** — discrete slices of
business, function, or process. When scoping an AE's audit, a team can:

- **Hand off** a piece of scope to another AE — *ownership of the risk transfers.* You no
  longer test it or conclude on it. Your only residual duty is **handoff hygiene**:
  verifying the receiving entity's scope actually covers what you transferred.
- **Rely on** another AE's (or external party's) testing — *ownership stays with you.* You
  borrow their evidence toward your own conclusion.

This project is scoped to **handoffs** (reliance lives at the engagement level, out of
scope here).

**The problem:** handoff documentation lives in free-text fields. The receiving entity's
controls live in Archer, indexed by *Specific Risk* and *KPA* — not by "which entity
handed work to me." The link between "A says it handed off X" and "does B actually control
X" is implicit and never rolled up. Reading 4,400 of these by hand is a multi-quarter job,
so coverage gaps get discovered *reactively* — after an incident or a regulator asks.

**The failure mode that should make a room uncomfortable:** Credit Issuance hands "AML
risk" to AML Monitoring. AML Monitoring audits the AML *program* — framework, training,
transaction-monitoring calibration. But **KYC at customer onboarding** is an embedded
control *inside the credit process.* If that boundary isn't drawn explicitly, it's in
neither library — nobody tests it, and nobody knows nobody is testing it. This is the
**coarse-handoff failure mode**, and it's the single most important pattern the tool hunts.

**Regulatory anchor:** This maps to **IIA Global Internal Audit Standard 9.5**
(Coordination and Reliance, effective Jan 2025), which expects internal audit to produce an
**assurance map** — a view proving every risk has exactly one owner and that other coverage
is either a defined handoff or a documented reliance. We're going to be asked for that
artifact regardless. The AI is the *means* to produce it at scale; the map is the *thing*.

---

## 3. Key vocabulary

| Term | Meaning |
|------|---------|
| **Audit Entity (AE)** | A discrete auditable slice of the business. Format `AE-nnn`. |
| **Handoff** | One entity transfers ownership of a risk to another (`A → B`). |
| **Reliance** | One entity borrows another's testing as evidence; ownership stays. *(Out of scope here.)* |
| **Focal entity** | The entity currently being evaluated in a batch. |
| **Control** | A documented control in the library, indexed by Specific Risk + KPA. The *proof* an entity actually does something about a risk. |
| **Specific Risk** | The actual risk statement (e.g., "the risk that KYC is not performed at customer onboarding") — NOT one of the 14 high-level categories. |
| **KPA** | Key Process Area — a granular process decomposition. Helps tell program-level from embedded-process-level. |
| **14 risk categories** | Compliance, Country, Credit, External Fraud, Financial Reporting, Funding & Liquidity, IT, Information Security, Model, Market, Operational, Reputational, Strategic & Business, Third Party. Each carries a residual rating + rationale + control assessment. |
| **Program-level vs embedded-process-level** | A risk can be covered by a high-level program (framework/policy/training) OR by a specific control inside a business process. Coarse handoffs cover the former and miss the latter. |
| **Assurance map** | The IIA-9.5 artifact: every risk → one owner, all other coverage = defined handoff or documented reliance. |

---

## 4. The two pieces of the project

### Piece A — The deterministic pipeline (data + visualizations)

Plain Python (pandas/openpyxl), no AI. It turns the raw audit-universe CSV export into
clean relational tables, an entity-to-entity edge list, a coverage matrix with rule-based
gap flags, and interactive HTML visualizations. This is **table-stakes data prep** — it
makes the universe analyzable. It is *not* the headline value; it's the foundation the AI
piece and the visuals sit on.

### Piece B — The AI handoff evaluation (the headline)

A Gen-AI evaluation that reads, for each handoff, the **controls on both sides** plus the
handoff prose, and judges whether the transferred risk actually lands. This is the part
that answers the one-sentence question in §1. Everything else supports it.

> **Critical reframe — controls are the primary evidence.** The 14-category ratings and
> their prose are a *summary/scoring layer*, not the evidence base. The real evidence lives
> at the **control** layer: Control Description, Specific Risk, KPA. Coverage is proven or
> disproven at the control level, not by a category rating.

---

## 5. How the AI evaluation works — the five checks

The AI runs **five checks** on each entity's file. The first two are about documentation
quality; checks 3 and 5 are where the real coverage gaps come from; check 4 is internal
consistency. (Formal definitions live in `config/stage2_prompt.yaml`;
`stage2_tasks_explained.md` is the plain-English version.)

| # | Plain question | What it reads |
|---|----------------|---------------|
| **1** | Do the files follow our own handoff rules? | File vs. our documentation standard |
| **2** | Do the ratings agree with the handoff claims? | Handoff prose vs. 14-category ratings |
| **3** | Is the handed-off risk covered at the same *depth*? | Sender's risk vs. receiver's *type* of control (program vs embedded) |
| **4** | Does the entity's file contradict itself? | One entity's overview / handoff / rationale / controls |
| **5** | Does the receiver actually cover what was handed off? | Sender's transferred risk vs. receiver's **actual controls** |

**Check 5 is the whole point.** For each handoff `A → B`: take the risks A says it
transferred, then look at B's actual control library. Three outcomes:

- **Full match → conforms.** B genuinely covers what A handed off.
- **Partial match → likely coverage gap (orphaned control).** B covers the general category
  but not the specific transferred risk.
- **No coverage → likely coverage gap (no owner).** Nobody covers it. **Highest-confidence
  finding.**

If A's handoff prose is too vague to tell what was even transferred, that ambiguity is
reported as a **documentation issue** — the tool will not invent a transfer claim.

### Finding classifications

Every finding lands in one of three buckets:

- **`conforms`** — coverage lands as documented.
- **`documentation issue`** — the documentation is too coarse/contradictory to test cleanly.
  Real signal: the AI *declined* to assert a gap because the prose wasn't precise enough.
- **`likely coverage gap`** — coverage appears not to land (orphaned control or no owner).

---

## 6. Data sources

| Source | Level | Carries |
|--------|-------|---------|
| **Risk Assessment Excel** | Entity (one row per AE) | Overview prose, handoff description prose, 14-category ratings + inherent rationale + control assessment, handoff to/from AE IDs |
| **Archer Controls CSV** | Control (one row per control) | `Audit Entity ID`, `Control ID/Title/Description`, `KPA ID/Description`, `Specific Risk ID/Description`. ~10–30 controls per entity. **This is the primary evidence base.** |

**Pass 1** (a separate earlier step) classifies each handoff into a business domain
(`financial_crime`, `tech_cyber`, `privacy_data`, etc. — 16 values). Pass 1 is **excluded**
from the Stage 2 evaluation payload on purpose: feeding one model's summary into another's
evaluation would bias interpretation.

**Out of scope for the evaluation:** test procedures, prior findings, RCSA,
regulatory-to-category mapping, reliance (engagement-level).

---

## 7. How it runs (mechanics)

Because of data confidentiality, the AI evaluation is run by **manual paste into ChatGPT
Pro (web UI, extended thinking)** — not via API. The pipeline can't fit ~427 entities in
one prompt, so work is **batched**:

- **Batch unit:** focal entity + its 1-hop handoff neighbors (so both ends of a handoff sit
  in the same batch — required for check 5). Roughly ~10 focal entities per batch.
- The framework and Stage 1 findings travel with **every** batch as static context; only
  entity data varies.
- Each batch returns **structured JSON** findings, which aggregate into one dataset.
- A **quality gate** runs after the responses come back; batches that fail get flagged.

### Commands

```bash
# --- Piece A: the deterministic pipeline ---
python -m src.pipeline                         # runs all stages on dummy data
python -m src.pipeline --input <universe.csv> --plan <audit_plan.csv>

# --- Visualizations (network map, chord, heatmap, treemap, pitch map) ---
python src/generate_network_viz.py --input-dir data/output --output-dir data/output \
    --source data/input/<universe.csv>

# --- Piece B: the AI handoff review ---
python -m src.stage2_handoff_review.generate --dry-run   # preview batch plan + token estimate
python -m src.stage2_handoff_review.generate             # write batch prompts to paste into ChatGPT
# (paste each prompt into ChatGPT Pro, save the response back into runs/stage2/batches/)
python -m src.stage2_handoff_review.aggregate            # parse responses, run gate, merge findings
python -m src.stage2_handoff_review.summarize_findings   # produce the ranked summary
```

### Key outputs

| File | What it is |
|------|------------|
| `data/output/layer1_output.xlsx` | Clean relational tables (nodes, risk map, handoffs, assets, profiles) |
| `data/output/edge_derivation_output.xlsx` | Entity-to-entity edge list |
| `data/output/layer2_coverage_matrix.xlsx` | Coverage matrix + rule-based gap flags |
| `data/output/network_visualization_*.html` | Full interactive network map (grouped by Audit Leader) |
| `data/output/network_pitch_*.html` | Simplified pitch version of the map |
| `runs/stage2/aggregated/findings_rollup.xlsx` | **All AI findings**, by entity, with classification + evidence |
| `runs/stage2/aggregated/ranked_summary.md` | Findings ranked, highest-confidence coverage gaps first |

> **Data boundary:** ChatGPT response content stays on the local machine. Findings
> workbooks contain potentially sensitive entity data and are gitignored.

---

## 8. The visualization

An interactive network map (`network_visualization_*.html`), entities **grouped by Audit
Leader**:

- **Node color** = overall residual risk (red=Critical … green=Low, gray=N/A)
- **Node shape** = audit-plan status (circle = in scope, diamond = not; thick border = overdue)
- **Node size** = connectivity (number of handoff/shared-asset connections)
- **Edges** = handoffs by default (shared apps/vendors/PRSAs are toggles)
- **Likely-gap overlay** = AI findings classified `likely coverage gap` are drawn in **red**
  on the relevant nodes/edges, so the assurance gaps are visible on the canvas.
- **Portfolio + inbound-impact mode** answers: *"whose work outside my portfolio can break
  mine?"*

The map is the **hook**, not the value. The value is the ranked findings. Lead a demo with
a finding, not the graph.

---

## 9. What the tool CAN'T tell you (read this before trusting a finding)

Every finding requires **human adjudication.** The pipeline tells you *where to look*, not
what the answer is. Specific limits:

- **The evidence base is the control library — and only the control library.** The AI
  reasons over Specific Risks, KPAs, and control descriptions. It does **not** ingest
  external assurance (e.g., a **SOC 1 report**), reliance arrangements, or coverage that
  lives outside Archer. So a real "no owner" flag can be a **false positive** if coverage
  actually exists via a source the model never saw.
  - *Worked example:* AE-506 hands GNS disputes/arbitration to AE-177; AE-177's library has
    no dispute-specific control, so the model flags a high-confidence "no owner" gap — which
    is *correct about the library.* But a colleague pointed to a prior-year SOC 1 reliance
    argument. The model did its job (surfaced the right question in 30 seconds); a human then
    has to apply the SOC-1 question the model can't see. **Watch for the trap:** that SOC 1
    argument was about *transaction processing*, while the handoff was about *disputes/
    arbitration* — adjacent coverage is not the same as coverage of the transferred slice.
- **Documentation issues are not gaps.** A `documentation issue` means the prose was too
  coarse to test — it's a prompt to improve documentation, not necessarily an uncovered risk.
- **Stale handoffs exist.** A handoff sentence can be a leftover from a prior-year structure.
  "The doc is old" isn't itself evidence the risk is uncovered — confirm where it's covered today.
- **The "applicable in both entities" rule is legitimate.** The manual explicitly allows a
  risk to be applicable in two entities (owned in one, managed in another). Treat it as a
  documented design pattern, not an error.

---

## 10. Honest posture (for the pitch and for skeptics)

- This is a **prototype** using ChatGPT Pro extended thinking + a manual paste workflow.
  Productization (API/internal-LLM-driven) is roadmap, not done.
- The real run spanned the full universe across ~350 batches; **the team adjudicates** the
  top findings — the tool produces a **punch list, not a finished assurance map.**
- The framework (handoff vs reliance, controls-as-primary-evidence, the 5 checks) was
  developed iteratively with AI prototyping. It's defensible but not yet peer-reviewed.
- Audit leaders trust honesty about limits more than polished claims. State the limits.

---

## 11. Repository map

```
audit_universe_map/
├── CLAUDE.md                       # full pipeline build spec (Piece A)
├── handoff_review_context.md       # full framework + Stage 1 findings + Stage 2 prompt (Piece B)
├── stage2_tasks_explained.md       # the 5 checks in plain English
├── handoff_stage2_data_spec.md     # data requirements for the evaluation
├── handoff_stage2_batching_design.md
├── handoff_stage2_prompt_revisions.md
├── pitch_plan.md                   # the Shark-Tank-style pitch plan + 1-week sprint
├── config/
│   ├── stage2_prompt.yaml          # the 5-check prompt definitions (source of truth)
│   ├── stage2_batching.json        # batching tuning parameters
│   ├── standardization_mappings.json
│   ├── horizontal_keywords.json
│   └── column_mappings.json
├── src/
│   ├── pipeline.py                 # Piece A entry point (stages 1–8)
│   ├── stage1_filter.py … stage8_coverage.py
│   ├── generate_network_viz.py     # builds all HTML visualizations (stage 9)
│   ├── _*_template.html            # viz templates (network, pitch, chord, heatmap, treemap)
│   └── stage2_handoff_review/      # Piece B (the AI evaluation)
│       ├── generate.py             # build batch prompts (dry-run + token model)
│       ├── payload.py              # assemble per-entity payload
│       ├── graph.py                # focal + 1-hop batching over the handoff graph
│       ├── aggregate.py            # parse responses, gate, merge findings
│       ├── summarize_findings.py   # ranked summary
│       └── labels.py               # display-string mapping
├── data/
│   ├── input/                      # universe CSV + audit plan (dummy data for dev)
│   └── output/                     # xlsx + html outputs
└── runs/stage2/                    # batch prompts/responses + aggregated findings (gitignored)
```

---

## 12. Quick answers to likely questions

- **"Does this decide whether a gap is real?"** No. It flags candidates with evidence; a
  human adjudicates. See §9.
- **"Why controls and not the risk ratings?"** Ratings are a summary; controls are the proof
  coverage exists. See §4.
- **"Why ChatGPT paste and not an API?"** Data confidentiality + prototype stage. See §7.
- **"Does it look at reliance?"** No — handoffs only. Reliance is engagement-level. See §2.
- **"What's the assurance map?"** The IIA-9.5 artifact this is built to feed: every risk →
  one owner. See §2.
- **"Will it miss coverage that's in a SOC 1?"** Yes — that's its main blind spot. See §9.
```
