# Stage 2 Prompt — Proposed Revisions

Task-by-task diff against §6 of `handoff_review_context.md`. The current prompt language leans on 14-category fields (rating + rationale + control assessment prose) as the evidence base. After the controls-as-primary-evidence reframe, three of five tasks need substantive language changes and two need lighter touch-ups. This memo lays out proposed new wording per task; the final prompt file inherits these revisions.

Evidence layer reminder:
- **Primary:** Control Description, Specific Risk ID + Description, KPA ID + Description (per control; from Archer CSV pull).
- **Secondary:** 14-category residual rating, inherent-risk rationale prose, control-assessment prose (per entity × per category; from risk-assessment Excel).
- **Entity context:** Overview prose, Hand-off Description prose, structured Hand-offs to/from IDs (per entity).

---

## Task 1 — Manual-to-file conformance

**What the current prompt says:**
> Walk through each handoff-related requirement identified in the manual review. For each one: does the file demonstrate conformance? Where? Does the file contradict or ignore it? Where? [...]

**What changes:**
Requirement #2 in the Stage 1 prioritized gaps is "attribute-level handoff documentation — exact risk slice / control objective / embedded touchpoint / legal entity / period / population." This evidence lives in control descriptions and Specific Risk statements, **not** the entity-level handoff description. The current language implicitly treats "the file" as the risk-assessment Excel; it needs to be widened to include the control-layer payload.

**Proposed revised wording:**
> For each handoff-related requirement identified in the manual review, check whether the file conforms. For each requirement:
> - Which evidence layer does this requirement ask about — entity-level documentation (overview, handoff description, 14-category ratings/rationale) or control-level documentation (Control Description, Specific Risk, KPA)?
> - Does the appropriate layer demonstrate conformance? Quote or cite.
> - Does it contradict or ignore the requirement? Quote or cite.
> - Where the manual was silent or ambiguous, what de facto rule is the team following? Cite evidence from either layer as relevant.
>
> Note specifically: for the "attribute-level handoff documentation" requirement, evaluate against the Specific Risk statements on the focal entity's controls. For the "explicit risk ownership" requirement, compare handoff description prose against who actually holds controls for the Specific Risks involved.

---

## Task 2 — Handoff representation in the ratings

**What the current prompt says:**
> The file has a handoff description column and 14 risk categories each with rating + inherent rationale + control assessment. Check whether handoffs described in the handoff column are reflected consistently in the three rating columns for the affected risk categories. [...]

**What changes:**
This task is explicitly about the summary layer — does the rating reflect the handoff? Primary evidence stays category-level. Control-layer evidence is supplementary corroboration for pattern 4 ("rationale or control assessment references another entity, but handoff column is silent"). Minimal changes; just add one line.

**Proposed revised wording:**
> [Current language preserved verbatim — this task is specifically a summary-layer check. Add two paragraphs at the end:]
>
> Supplement: where a rating appears to conflict with the handoff description, cross-check against the entity's control library. If the entity still carries controls for a Specific Risk it claims to have handed off, note this as a mismatch alongside the rating finding.
>
> Conditional handling for rationale prose: if the payload includes inherent-risk rationale prose per risk category, evaluate the full pattern set (prose-referenced entities, partial-retention language, etc.) as described above. If the payload does not include rationale prose — only ratings — evaluate only rating-vs-handoff consistency and note that rationale patterns could not be assessed. Do not fabricate rationale content or infer what the rationale would have said.

---

## Task 3 — Coarse-handoff test

**What the current prompt says:**
> If the manual requires handoffs to specify the scope transferred (program-level vs embedded-process-level controls), check each handoff description against that bar. Prioritize functional risk categories where embedded controls within business processes are typical (AML, sanctions, fraud, privacy, conduct, data, third-party). Flag handoffs that name only the category or receiving entity without specifying the embedded layer.

**What changes:**
This is where the reframe bites hardest. "Program-level vs embedded-process-level" is **literally** the Specific Risk / KPA layer on controls. The handoff description prose is often too vague to judge (user confirmed this). The real test: does the receiving entity's control library actually contain embedded-process-level controls for the Specific Risks in question, or only program-level framework controls? The test pivots from prose-specificity scoring to control-library evaluation.

**Proposed revised wording:**
> The manual requires handoffs to specify the scope transferred — program-level controls (enterprise framework, policy ownership, monitoring oversight) vs embedded-process-level controls (controls operated inside a business process, like KYC verification at customer onboarding, transaction monitoring review, SAR filing oversight). For each handoff described or structurally present in the focal entity:
>
> 1. Identify the Specific Risks the handoff appears to transfer. Use the handoff description prose plus the focal entity's Specific Risk coverage rollup; cross-reference receiving entity's Specific Risk coverage.
> 2. Examine the receiving entity's controls (target-context payload). Are the controls that cover those Specific Risks **program-level** (framework, governance, oversight language) or **embedded-process-level** (specific process touchpoints)?
> 3. If the handoff transfers embedded-process-level risk but the receiving entity's controls are only program-level (or vice versa), flag as a coarse-handoff finding. Quote Control Descriptions or Specific Risk statements as evidence.
>
> Use the focal entity's overview to understand what business activities it performs. Missing embedded controls represent a real gap when the overview describes activities that should generate them, not when the activity isn't performed by this entity. The overview is reasoning context for interpreting control coverage — findings must still cite Control Descriptions, Specific Risk IDs, or KPA IDs as evidence, not the overview alone.
>
> Where the manual is silent on this distinction, flag it as an area where the file inherits the manual's gap — and note that the file's practice creates likely coverage holes regardless.
>
> Do not rely on the handoff description's prose specificity alone; many descriptions are variable or generic, and the coarse-handoff risk is often visible only by comparing the transferor's Specific Risks to what the transferee's controls actually cover.

---

## Task 4 — Overview-to-rationale alignment

**What the current prompt says:**
> If the manual requires the overview, handoff description, and risk rationales to be internally consistent, test that. [Examples follow: overview describes activities → rating NA with no handoff explanation; handoff names receiver → rationale still describes this entity as owner; control assessment describes controls this entity operates for a risk the handoff says was transferred.]

**What changes:**
Add a fourth consistency point: the focal entity's control library. The third example above ("control assessment describes controls this entity operates for a risk the handoff says was transferred") is implicitly reaching for control-layer evidence — make it explicit.

**Proposed revised wording:**
> If the manual requires the overview, handoff description, risk rationales, and control library to be internally consistent, test that. Examples:
>
> - Overview describes activities that would generate a risk; rating marks it not applicable with no handoff explanation; focal entity holds no controls for that Specific Risk (consistent omission) — or holds some (inconsistent).
> - Handoff description names a receiving entity; rationale for that risk contradicts the handoff (still describes focal as owner); focal's controls still cover the Specific Risks supposedly transferred (strong inconsistency).
> - Rating rationale claims a risk is handed off; focal's controls contain Specific Risks that reach that category — the control library contradicts the handoff claim.
> - Overview describes a process that should produce specific controls; focal's control library is silent on that process's KPA (potential coverage gap or a reliance/handoff not documented).
>
> Quote the relevant prose fields and, where applicable, list the Specific Risk IDs or Control IDs evidencing the inconsistency.

---

## Task 5 — Cross-entity consistency

**What the current prompt says:**
> If the manual expects handoffs to be reciprocally visible — i.e., if entity A hands off to entity B, entity B's row should show that risk in scope and owned — check for mismatches. These are the strongest indicators of real coverage gaps rather than documentation issues.

**What changes:**
"Risk in scope and owned" currently reads as "B's 14-category ratings aren't NA." That's the weak test. The strong test is: B's control library covers the Specific Risks A claims to have transferred. Rewrite around Specific Risk coverage matching, with ratings as supporting signal.

**Proposed revised wording:**
> For each handoff A → B where A is a focal entity:
>
> 1. **Identify the Specific Risks A claims to have handed off.** Use A's handoff description prose and A's Specific Risk coverage rollup. If A's controls no longer carry a Specific Risk that the overview suggests they should, that's a signal A has transferred it. Use A's overview to sanity-check what A's handoff description likely refers to — the overview constrains which Specific Risks are plausibly being transferred. The overview is reasoning context only; findings must cite Control Descriptions, Specific Risk IDs, or KPA IDs as evidence, not the overview alone. **If A's handoff description is too generic to identify specific risks transferred, note that explicitly in the finding and classify as a documentation issue. Do not fabricate a specific transfer claim from vague prose — report the ambiguity itself as the finding.**
> 2. **Examine B's control library (target-context payload).** Does B's Specific Risk coverage include each risk A handed off?
>    - **Full coverage match:** B's controls explicitly cover the Specific Risks A transferred. Classify as **conforms**.
>    - **Partial match:** B covers the general category (e.g., "AML governance") but not the specific risk statement A transferred ("KYC at customer onboarding"). Classify as **likely coverage gap — embedded control orphaned**.
>    - **No coverage:** B's controls don't carry the Specific Risk at all. Classify as **likely coverage gap — no owner**. Highest-confidence finding.
> 3. **Reciprocity check on ratings (secondary signal):** B's 14-category residual rating for the corresponding category should be applicable (not NA) if B genuinely owns the risk post-handoff. An NA rating on B combined with A claiming transfer is another mismatch class.
> 4. **Reciprocity check on B's handoff description (secondary):** does B's handoff description or overview reference receiving work from A, or from entities like A? Silence is not itself a failure, but mentioning conflicts with B's ratings/controls is a finding.
>
> Quote Specific Risk IDs and Descriptions as evidence in every Task 5 finding. This is the task where control-layer evidence is dispositive.

---

## OUTPUT format — revision

**What changes:**
Each finding should carry a new field: `evidence_layer` ∈ `{control, category_summary, entity_prose, structured_handoffs}`. This is what the quality gate in the batching design checks to verify the model is operating at the right evidence layer.

**Proposed revised output schema:**

`specific_risk_ids` is an array on every finding (uniform across tasks). A Task 5 finding may legitimately span multiple SRs — A transferred SR-101, SR-102, SR-103 and B covers only one — so the array is required there. Tasks 1–4 usually emit one-element arrays but keep the same shape so aggregation is uniform.

```json
{
  "findings": [
    {
      "task": 1 | 2 | 3 | 4 | 5,
      "manual_requirement": "paraphrase or quote from Stage 1 findings",
      "focal_entity_id": "AE-nnn",
      "focal_entity_name": "...",
      "risk_category": "one of 14 | null if not category-keyed",
      "specific_risk_ids": ["SR-nnn", ...],
      "kpa_ids": ["KPA-nnn", ...],
      "evidence_layer": "control | category_summary | entity_prose | structured_handoffs",
      "evidence_quote": "quoted text from the relevant field(s)",
      "classification": "conforms | documentation issue | likely coverage gap",
      "reasoning": "1-3 sentences",
      "cross_entity_partner_id": "AE-nnn | null — filled for Task 5"
    }
  ],
  "ranked_summary": {
    "likely_coverage_gaps": [ { "focal_entity_id": "...", "specific_risk_ids": ["SR-nnn", ...], "confidence": "high|medium|low", "summary": "..." } ],
    "systemic_documentation_issues": [ { "pattern": "...", "affected_entity_count": N, "summary": "..." } ],
    "manual_gaps_exposed": [ { "area": "...", "summary": "..." } ]
  }
}
```

---

## Summary of which tasks changed how

| Task | Change level | What changed |
|---|---|---|
| 1 | Moderate | Widened to include control-layer evidence; requirement 2 (attribute-level documentation) explicitly pivots to Specific Risk |
| 2 | Light | Added optional control-layer corroboration; core of task unchanged |
| 3 | **Major** | Pivots from prose-specificity scoring to control-library evaluation (program-level vs embedded-process-level) |
| 4 | Moderate | Added control library as a fourth consistency point |
| 5 | **Major** | Primary test is Specific Risk coverage match between A and B; ratings demoted to secondary signal |
| Output schema | Addition | New `evidence_layer` field to enable gate-checking and later analysis |

---

## Resolved: Task 2 stays as-is

Decision (2026-04-20): Task 2 keeps distinct-task status for the first real-data run. Two reasons:
1. Low cost — operates on structured ratings, not prose, so it doesn't compete for token budget.
2. Task 2 findings volume relative to Tasks 1/3/5 is itself diagnostic — it tells us where documentation issues actually concentrate in the 14-category summary layer.

Revisit after the first real-data run based on what Task 2 actually produces.
