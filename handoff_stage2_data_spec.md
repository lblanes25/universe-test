# Stage 2 Data Requirements Specification (v2)

Fresh rewrite after the controls-as-primary-evidence reframe. Supersedes v1 in its entirety. Output of the first Claude Code task defined in `handoff_review_context.md` section 4.

---

## 1. The reframe in one paragraph

The 14 risk-category fields on the risk-assessment Excel (residual rating, inherent-risk rationale, control-assessment prose) are a **summary and scoring layer**, not the evidence that answers Stage 2's questions. The real evidence lives at the **control** layer — each audit entity's individual controls, each tagged with a **Specific Risk** (actual risk statement like "the risk that KYC is not performed at customer onboarding") and a **KPA** (key process area). Stage 2 reasons primarily over the control layer; the 14-category fields are kept as secondary signal and for Task 2, which is specifically a summary-layer check. This rewrite adjusts the payload schema, data sources, and must-have checklist to match.

---

## 2. Data sources

### Source A — Risk Assessment Excel (entity-level)
One row per active audit entity. Columns the payload actually uses:
- `Audit Entity ID`, `Audit Entity Name`
- `Audit Entity Overview` (prose)
- `Business Unit`, `Line of Defense`, `Audit Leader` (context only)
- `Hand-offs to Other Audit Entities`, `Hand-offs from Other Audit Entities` (semicolon-delimited AE IDs)
- `Hand-off Description` (prose, one free-text box per entity; often doesn't name the receiving entity)
- For each of 14 risk categories: `<Risk> Residual Risk` (rating), `<Risk> Inherent Risk` rationale prose, `<Risk> Control Assessment` prose. Ratings confirmed present in dummy; prose confirmed present in real data.

### Source B — Archer Controls CSV (control-level, NEW in v2)
Manual export from Archer. Static file, user-provided. One row per control. Columns:
- `Audit Entity ID` (join key to Source A)
- `Control ID`, `Control Title`, `Control Description`
- `KPA ID`, `KPA Description`
- `Specific Risk ID`, `Specific Risk Description`
- 14-category risk tagging available but **deprioritized** — KPA and Specific Risk are richer and primary.

Typical volume: **10–30 controls per entity**, distribution roughly uniform (not heavily skewed).

### Source C — Network map pipeline outputs
Existing `layer1_output.xlsx` / `layer2_coverage_matrix.xlsx`. Used for:
- Nodes table — authoritative active-entity list and names
- Handoffs table — directional edge list with `Unmatched` flag
- Removed entities log — identifies the 45 filtered IDs referenced by 199 handoff rows

### Explicitly out of scope for Stage 2 (user-confirmed)
- Test procedures / test plans
- Prior audit findings / issues
- RCSA (1LOD self-assessment)
- Regulatory-to-risk-category mapping
- Pass 1 classification file — excluded from evaluation payload (kept for potential post-hoc use only; not driving Stage 2 here)

---

## 3. Evidence layer hierarchy

Every Stage 2 reasoning step should start with **primary** evidence; **secondary** evidence is corroboration or mismatch-detection; **entity context** frames the question.

| Layer | Fields |
|---|---|
| **Primary evidence** (control layer) | Control Description, **Specific Risk ID + Description**, KPA ID + Description |
| **Secondary evidence** (summary layer) | 14-category residual rating, inherent-risk rationale prose, control-assessment prose |
| **Entity context** | Overview prose, Hand-off Description prose, structured `Hand-offs to/from` IDs |

**Specific Risk is the single most important field for Tasks 3 and 5.** It carries the attribute-level documentation needed to judge whether a handoff's scope is specified, and whether a receiving entity's controls actually cover the risk slice that was transferred. Surface it prominently in the payload, not as an afterthought.

---

## 4. Batch payload schema (direction-aware)

Each batch contains three distinct payload sections. Each entity appears in exactly one role per batch. Fields the prompt will see:

| Field | Source | Focal | Target ctx (B in A→B) | Source ctx (C in C→A) |
|---|---|---|---|---|
| `entity_id`, `entity_name` | A | ✓ | ✓ | ✓ |
| `overview` | A | ✓ | — | — |
| `business_unit`, `line_of_defense`, `horizontal_flag` | A / derived | ✓ | ✓ | — |
| `handoff_description` (prose) | A | ✓ | ✓ | ✓ |
| `handoffs_to`, `handoffs_from` (list of `{id, name, inactive_flag}`) | A + derived | ✓ | ✓ | — |
| **`controls`** (list of `{control_id, title, description, kpa_id, kpa_description, specific_risk_id, specific_risk_description}`) | B | ✓ full | ✓ compact† | — |
| `specific_risk_coverage` (deduplicated unique SR IDs + descs) | derived from B | ✓ | ✓ | — |
| `kpa_coverage` (deduplicated unique KPA IDs + descs) | derived from B | ✓ | ✓ | — |
| `risks` (14 categories × {residual rating, inherent rationale, control-assessment prose}) | A | ✓ applicable only | ratings only | — |

† Target-context `controls` list: drop the Control Description to save tokens; keep Control Title + Specific Risk ID+Desc + KPA ID. That's enough for Task 5's "does B's library cover what A transferred" without carrying every control's full narrative.

### Role assignment rules
- **Focal:** evaluated for all 5 Stage 2 tasks. Each active entity is focal in exactly one batch.
- **Target context (B):** included when some focal A has a `handoff_to` pointing at B. Purpose: Task 5 "receiving-entity coverage" check. Richer payload because it's the answer to the coverage question.
- **Source context (C):** included when some focal A has a `handoff_from` from C (or equivalently C has a `handoff_to` pointing at A). Purpose: check whether C's handoff description matches how A describes what it received. Lean payload because the interesting evidence is C's description prose, not C's controls.
- **Bidirectional partner (both A→B and B→A):** use target-context treatment (richer); source-context content is a subset.
- **Focal-in-same-batch:** if B is already focal in this batch, don't duplicate it as context. The focal payload serves both roles.

### Excluded from all payloads
Apps, vendors, models, PRSAs, policies, Pass 1 classifications, audit cycle fields (frequency, override, last audit date), coverage flags, connectivity breakdown. These feed other pipeline stages and don't inform handoff evaluation.

### Carried as batching-script metadata only (not in prompt)
`audit_leader`, `pga_asl`, `connectivity_total`, `in_scope`, `overdue_flag`, Pass 1 category. Used for batch composition and post-hoc keying, not evaluation.

---

## 5. Derived fields (computed pre-prompt by the batching script)

1. **Handoff partner resolution.** For each AE ID in `handoffs_to/from`, look up `entity_name` from Nodes; set `inactive_flag = True` if ID is in the filtered-entities log. 45 such IDs in real data; they appear legitimately in the prose but aren't active.
2. **Applicable-risk filter.** Per focal, drop risk categories whose residual rating is `Not Applicable` or blank. Reduces payload ~30–50%. Target context gets all 14 rating values (abbreviated) regardless — the model may need to see an "NA" to catch Task 5 mismatches.
3. **Specific Risk coverage rollup.** Per entity, deduplicate Specific Risks across that entity's controls. Emit `specific_risk_coverage: [{id, description}, ...]`. Enables the model to scan "which risks does this entity's library cover" without reading all 20 control descriptions. Used heavily by Task 5.
4. **KPA coverage rollup.** Same logic for KPAs. Gives the model a process-map view of the entity.
5. **Direction tagging.** Each context entity labeled `role: "target"` or `role: "source"` so the prompt explains what check to run against which context.
6. **Bidirectional flag.** If entity X is both in A's `handoffs_to` and `handoffs_from`, mark once with `bidirectional: true`; prevent duplicate context entries.

---

## 6. Real-data must-have checklist

Confirm before running Stage 2 on real data.

- [x] Risk assessment Excel carries inherent rationale prose and control-assessment prose (confirmed 2026-04-20).
- [x] Hand-off Description is entity-level free text, variable detail, may not name receiving entity (confirmed 2026-04-20).
- [ ] **Archer controls CSV export available** with all 8 required fields: Audit Entity ID, Control ID, Control Title, Control Description, KPA ID, KPA Description, Specific Risk ID, Specific Risk Description.
- [ ] Specific Risk ID + Description populated (not blank) for every row.
- [ ] KPA ID + Description populated for every row.
- [ ] Audit Entity ID join key matches between risk-assessment Excel and controls CSV; no orphans on either side.
- [ ] Every active audit entity (~427) has at least one control record. Entities with zero controls may be legitimately empty (new entity, entity whose audit is done entirely through reliance) or a data-pull defect; either way, flag them — don't silently drop.
- [ ] Exact column headers in risk-assessment Excel for the prose fields (`<Risk> Inherent Risk` rationale column and `<Risk> Control Assessment` prose column) — confirm header names so `config/column_mappings.json` can be updated.

**Graceful degradation contract:** If at payload-build time the rationale-prose columns are missing or empty for some or all entities, the batching script emits the focal `risks` entries with rating only (rationale prose = empty string) rather than failing. Task 2 evaluates only rating-vs-handoff consistency in that case and flags rationale patterns as "not assessable" rather than producing empty findings. This is the conditional handling in the Task 2 prompt revision; the spec codifies it so the payload schema tolerates the real-data variability.

---

## 7. Answers to the five original section-4 questions (revised)

**Q1: What fields Stage 2 needs per batch.**
Derived from the task-by-task evidence mapping in the companion memo `handoff_stage2_prompt_revisions.md`. Headline: control-layer fields (description, Specific Risk, KPA) are primary for Tasks 1/3/4/5; 14-category ratings are primary for Task 2 and corroborating secondary for the others; overview and handoff-description prose frame the questions.

**Q2: Gap analysis against dummy schema.**
Dummy has entity-level fields (overview, handoff description, 14-category ratings). Dummy does **not** have the Archer controls CSV — that's an additional data source the real run needs. Dummy testing exercises the batching script mechanics and the focal-payload envelope for the fields it does carry; it cannot exercise Task 5's control-coverage check or Task 3's embedded-vs-program assessment meaningfully.

**Q3: Derived fields worth computing.**
Five, listed in §5. Specific Risk and KPA coverage rollups are the highest leverage — they let the model reason about "what does this entity cover" without iterating through every control.

**Q4: Pass 1 classification integration.**
Excluded from evaluation payload. This call hasn't changed: Pass 1's `Handoff Description` is an AI-generated summary, and its `Handoff Category` is a business-domain tag, not program-vs-embedded. Both would bias evaluation. Optional post-hoc diff (skipped for now per user decision).

**Q5: Adjacent data sources.**
KPA mapping now in scope via control-level tagging (Source B). Test procedures, findings, RCSA, regulatory-to-risk mapping confirmed out of scope.

**Q6: Noise to exclude.**
As listed in §4 "Excluded from all payloads."

---

## 8. Still open

- Exact column header confirmation for risk-assessment Excel's rationale-prose columns (must-have checklist item).
- Policy on controls with blank Specific Risk or KPA: include with a `(no specific risk)` placeholder, or exclude from the coverage rollup? Recommendation: include but flag, so the model sees tagging gaps as themselves a finding.
- Whether to carry Archer's 14-category risk tagging on the control record as tertiary evidence. Recommendation: no — it duplicates what's already in Source A at the entity level and bloats tokens. Revisit if calibration shows the model needs it.
