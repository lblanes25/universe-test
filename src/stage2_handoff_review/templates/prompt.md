# Stage 2 Handoff Review — Batch {batch_id}

You are evaluating audit entity handoffs per the framework and manual-review findings below. Produce findings **only for the focal entities**. Target-context and source-context entities are read-only reference for cross-entity checks; do not produce findings about them.

---

## Framework: handoffs vs reliance

- **Handoff** = ownership transfers. The risk leaves the transferor's register entirely. The transferor no longer tests the risk or concludes on whether it's managed. The transferor's only residual duty is **handoff hygiene** — verifying the receiving entity's scope covers what was transferred. Failure mode: scope assumptions diverge, risk falls between entities.
- **Reliance** = ownership stays with the relying auditor. Risk is still on their register; they still conclude on whether it's managed. They borrow another party's testing as evidence. Failure mode: borrowed evidence doesn't actually address the risk angle.
- **This review focuses only on handoffs.** Reliance is handled at engagement level, out of scope here.
- **Coarse-handoff failure mode:** a risk category (AML, sanctions, fraud, privacy, conduct, data, third-party) gets handed off to a functional audit at the program level, but embedded control touchpoints inside business processes stay unclaimed. Example: Consumer Lending hands AML to AML Monitoring. AML Monitoring has program-level controls (framework, training, transaction monitoring calibration). But KYC-at-origination, CDD-refresh, enhanced-DD — embedded controls — are neither in AML Monitoring's library nor retained by Consumer Lending. Orphaned.

---

## Manual review findings (Stage 1)

Prioritized gaps:
1. **Make audit-entity risk ownership explicit.** Every handoff should state which AE's register carries the risk and which AE concludes on whether it's managed. The manual relies too much on scope language; "applicable in both entities" (§3.2, 2554-2558) conflicts with one-owner accountability.
2. **Require attribute-level handoff documentation.** Exact risk slice / control objective / embedded touchpoint / legal entity / period / population — not just receiving AE or broad category.
3. **Explicitly address the coarse-handoff failure mode.** State that a program audit may own the enterprise program while a business-process audit still owns embedded process-level controls, with boundary documentation.
4. **Strengthen handoff hygiene to match reliance sufficiency.** Reliance requires exact objective match, period, population, approach, geography/entity (§5.9, 7799-7812 and §5.8, 7672-7681). Handoff hygiene (§5.9, 7733-7758) doesn't.
5. **Create a single coverage view / assurance map.** Current audit-universe completeness and RCO roll-up don't prove every risk/control slice has exactly one owner.

Silent/ambiguous:
- **A.** Manual frames handoff-vs-reliance around scope mechanics, not risk ownership (§5.9, 7710-7712).
- **B.** "Applicable in both entities" (§3.2, 2554-2558) conflicts with one-owner model.
- **C.** "Alternate procedures" language (§5.9, 7724-7726) implies residual transferor work after a handoff — muddies the model.
- **D.** Embedded-control boundaries not reconciled in one place (§2.3.1 vs §5.9, 7764-7768).
- **E.** Explicit one-owner accountability exists for issues (§7.2) but NOT for handoff/reliance risks.

---

## Evidence layers

You will be given fields from three layers. Use them in this priority for each task:

- **Primary (controls layer):** Control Description, Specific Risk ID + Description, KPA ID + Description. Per control. The actual evidence of what an entity tests.
- **Secondary (summary layer):** 14-category residual rating, inherent-risk rationale prose, control-assessment prose. Per entity × per category. Useful for rating-vs-handoff consistency checks and corroboration.
- **Entity context:** Overview prose, Hand-off Description prose (one free-text per entity), structured Hand-offs to/from AE IDs. Frames the question.

**Specific Risk is the attribute-level statement** (e.g., "the risk that KYC is not performed at customer onboarding"), NOT the high-level risk category. It's the evidence layer for attribute-level handoff documentation checks.

---

## Tasks

### Task 1 — Manual-to-file conformance

For each handoff-related requirement identified in the manual review, check whether the file conforms:
- Which evidence layer does this requirement ask about — entity-level documentation or control-level documentation?
- Does the appropriate layer demonstrate conformance? Quote or cite.
- Does it contradict or ignore the requirement? Quote or cite.
- Where the manual was silent or ambiguous, what de facto rule is the team following? Cite evidence from either layer as relevant.

For the "attribute-level handoff documentation" requirement, evaluate against the Specific Risk statements on the focal entity's controls. For the "explicit risk ownership" requirement, compare handoff description prose against who actually holds controls for the Specific Risks involved.

### Task 2 — Handoff representation in the ratings (summary-layer check)

For each focal entity, check whether handoffs described in the handoff column are reflected consistently in the 14-category rating columns. Patterns to identify:
- Handed off and marked Not Applicable.
- Handed off but still rated, with rationale acknowledging partial retention.
- Handed off but rated normally with no acknowledgment.
- Rationale or control assessment references another entity, but handoff column is silent (undocumented handoff).

Flag divergences from what the manual prescribes, and where the manual is silent, inconsistent team practice across entities.

Supplement: where a rating appears to conflict with the handoff description, cross-check the entity's control library. If the entity still carries controls for a Specific Risk it claims to have handed off, note this as a mismatch alongside the rating finding.

**Conditional handling for rationale prose:** if the payload includes inherent-risk rationale prose per risk category, evaluate the full pattern set above. If only ratings are in the payload, evaluate only rating-vs-handoff consistency and note rationale patterns as "not assessable." Do not fabricate rationale content.

### Task 3 — Coarse-handoff test (control-layer evaluation)

Program-level controls = enterprise framework, policy ownership, monitoring oversight, training, governance. Embedded-process-level controls = controls operated inside a business process (KYC verification at onboarding, transaction authorization, payment reconciliation, access provisioning at joiner-mover-leaver events).

For each handoff described or structurally present in the focal entity:
1. Identify the Specific Risks the handoff appears to transfer. Use handoff-description prose plus focal's Specific Risk coverage rollup; cross-reference receiving entity's coverage.
2. Examine receiving entity's controls (target-context payload). Are the controls that cover those Specific Risks program-level or embedded-process-level?
3. If the handoff transfers embedded-process-level risk but the receiving entity's controls are only program-level (or vice versa), flag as a coarse-handoff finding. Quote Control Descriptions or Specific Risk statements as evidence.

Use the focal entity's overview to understand what business activities it performs. Missing embedded controls represent a real gap when the overview describes activities that should generate them, not when the activity isn't performed by this entity. The overview is reasoning context for interpreting control coverage — findings must still cite Control Descriptions, Specific Risk IDs, or KPA IDs as evidence, not the overview alone.

Do not rely on handoff-description prose specificity alone; many descriptions are generic, and coarse-handoff risk is often visible only by comparing the transferor's Specific Risks to what the transferee's controls actually cover.

### Task 4 — Overview / handoff / rationale / controls alignment

Check internal consistency across the focal entity's own fields:
- Overview describes activities that would generate a risk; rating is Not Applicable with no handoff explanation; focal holds no controls for that Specific Risk (consistent omission) OR holds some (inconsistent).
- Handoff description names a receiving entity; rationale for that risk still describes focal as owner; focal's controls still cover the Specific Risks supposedly transferred (strong inconsistency).
- Rating rationale claims a risk is handed off; focal's controls contain Specific Risks that reach that category — the library contradicts the handoff claim.
- Overview describes a process that should produce specific controls; focal's library is silent on that process's KPA (potential coverage gap or undocumented handoff/reliance).

Quote the relevant prose fields and list Specific Risk IDs or Control IDs evidencing each inconsistency.

### Task 5 — Cross-entity consistency (primary control-layer check)

For each handoff A → B where A is a focal entity:

1. **Identify the Specific Risks A claims to have handed off.** Use A's handoff description prose and A's Specific Risk coverage rollup. If A's controls no longer carry a Specific Risk that the overview suggests they should, that's a signal A has transferred it. Use A's overview to sanity-check what A's handoff description likely refers to — the overview constrains which Specific Risks are plausibly being transferred. The overview is reasoning context only; findings must cite Control Descriptions, Specific Risk IDs, or KPA IDs as evidence, not the overview alone. **If A's handoff description is too generic to identify specific risks transferred, note that explicitly in the finding and classify as a documentation issue. Do not fabricate a specific transfer claim from vague prose — report the ambiguity itself as the finding.**
2. **Examine B's control library (target-context payload).** Does B's Specific Risk coverage include each risk A handed off?
   - Full coverage match: classify as **conforms**.
   - Partial match (B covers general category but not the specific risk statement): classify as **likely coverage gap — embedded control orphaned**.
   - No coverage: classify as **likely coverage gap — no owner**. Highest-confidence finding.
3. **Reciprocity check on ratings (secondary):** B's 14-category residual rating for the corresponding category should be applicable (not NA) if B owns the risk post-handoff. NA on B + A claiming transfer = another mismatch class.
4. **Reciprocity check on B's handoff description / overview (secondary):** does B mention receiving work from A, or from entities like A? Silence is not itself a failure, but mentioned conflicts are a finding.

Quote Specific Risk IDs and Descriptions as evidence in every Task 5 finding. This is the task where control-layer evidence is dispositive.

---

## Focal entities (evaluate these)

```json
{focal_json}
```

## Target-context entities (handoff targets — reference for Task 5; do not produce findings about them)

```json
{target_context_json}
```

## Source-context entities (handoff sources — reference for reciprocity checks; do not produce findings about them)

```json
{source_context_json}
```

---

## Output format

Emit exactly one top-level JSON code block matching this schema. No text outside the code block.

```json
{{
  "findings": [
    {{
      "task": 1,
      "manual_requirement": "paraphrase or quote of the Stage 1 requirement this addresses",
      "focal_entity_id": "AE-nnn",
      "focal_entity_name": "...",
      "risk_category": "one of 14, or null",
      "specific_risk_ids": ["SR-nnn"],
      "kpa_ids": ["KPA-nnn"],
      "evidence_layer": "control | category_summary | entity_prose | structured_handoffs",
      "evidence_quote": "quoted text from the relevant field(s)",
      "classification": "conforms | documentation issue | likely coverage gap",
      "reasoning": "1-3 sentences",
      "cross_entity_partner_id": "AE-nnn for Task 5, else null"
    }}
  ],
  "ranked_summary": {{
    "likely_coverage_gaps": [
      {{
        "focal_entity_id": "AE-nnn",
        "specific_risk_ids": ["SR-nnn"],
        "confidence": "high | medium | low",
        "summary": "short description"
      }}
    ],
    "systemic_documentation_issues": [
      {{
        "pattern": "name of the pattern",
        "affected_entity_count": 0,
        "summary": "short description"
      }}
    ],
    "manual_gaps_exposed": [
      {{
        "area": "short area name",
        "summary": "what the file reveals the manual doesn't say"
      }}
    ]
  }}
}}
```

Notes on filling the schema:
- `task` is integer 1–5.
- `specific_risk_ids` and `kpa_ids` are arrays. Single-element arrays are fine; Task 5 findings may contain multiple.
- `evidence_layer` must be one of: `control`, `category_summary`, `entity_prose`, `structured_handoffs`.
- `classification` must be one of: `conforms`, `documentation issue`, `likely coverage gap`.
- `cross_entity_partner_id` is required and non-null for Task 5 findings; null otherwise.
- Quote exact text in `evidence_quote` where possible. Truncate long quotes but preserve identifying phrasing.
- Produce findings only for entities listed in the focal section above.
