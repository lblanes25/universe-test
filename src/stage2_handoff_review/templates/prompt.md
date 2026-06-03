# Stage 2 Handoff Review — Batch {batch_id}

You are evaluating audit entity handoffs per the framework and manual-review findings below. Produce findings **only for the focal entities**. Target-context and source-context entities are read-only reference for cross-entity checks; do not produce findings about them.

---

## Framework: handoffs vs reliance

{framework_section}

---

## Manual review findings (Stage 1)

Prioritized gaps (the `requirement_id` value in **bold-italic** is the controlled key — set each finding's `requirement_id` to one of these):
1. ***risk_ownership*** — **Make audit-entity risk ownership explicit.** Every handoff should state which AE's register carries the risk and which AE concludes on whether it's managed. The manual relies too much on scope language; "applicable in both entities" (§3.2, 2554-2558) conflicts with one-owner accountability.
2. ***attribute_documentation*** — **Require attribute-level handoff documentation.** Exact risk slice / control objective / embedded touchpoint / legal entity / period / population — not just receiving AE or broad category.
3. ***coarse_handoff*** — **Explicitly address the coarse-handoff failure mode.** State that a program audit may own the enterprise program while a business-process audit still owns embedded process-level controls, with boundary documentation.
4. ***handoff_hygiene*** — **Strengthen handoff hygiene to match reliance sufficiency.** Reliance requires exact objective match, period, population, approach, geography/entity (§5.9, 7799-7812 and §5.8, 7672-7681). Handoff hygiene (§5.9, 7733-7758) doesn't.
5. ***assurance_map*** — **Create a single coverage view / assurance map.** Current audit-universe completeness and RCO roll-up don't prove every risk/control slice has exactly one owner.

Use `requirement_id: other` only when a finding fits none of the five above (e.g. one of the silent/ambiguous items below).

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

{tasks_section}

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
      "requirement_id": "risk_ownership | attribute_documentation | coarse_handoff | handoff_hygiene | assurance_map | other",
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
      "cross_entity_partner_id": "AE-nnn for Task 5, else null",
      "case_headline": "one plain sentence stating this entity's specific gap (Task 3 & 5)",
      "transferred_summary": "1-2 sentences: what this entity actually handed off, in its own terms (Task 3 & 5)",
      "coverage_summary": "1-2 sentences: what the receiving/program side actually does for it, and why that is not the embedded control needed (Task 3 & 5)",
      "pointing_at": "1 sentence naming the specific embedded control / risk slice left unowned (Task 3 & 5)"
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
- `requirement_id` is the **controlled key** for the Stage 1 requirement the finding addresses — exactly one of: `risk_ownership`, `attribute_documentation`, `coarse_handoff`, `handoff_hygiene`, `assurance_map`, `other`. This is what findings are grouped/themed on, so pick the closest fit; use `other` only when none apply. `manual_requirement` stays the free-text paraphrase/specifics — do not put theming weight on its wording.
- `specific_risk_ids` and `kpa_ids` are arrays. Single-element arrays are fine; Task 5 findings may contain multiple.
- `evidence_layer` must be one of: `control`, `category_summary`, `entity_prose`, `structured_handoffs`.
- `classification` must be one of: `conforms`, `documentation issue`, `likely coverage gap`.
- `cross_entity_partner_id` is required and non-null for Task 5 findings; null otherwise.
- Quote exact text in `evidence_quote` where possible. Truncate long quotes but preserve identifying phrasing.
- Produce findings only for entities listed in the focal section above.
- **Narrative fields (`case_headline`, `transferred_summary`, `coverage_summary`, `pointing_at`)** are required for **Task 3 and Task 5** findings and may be empty strings for Tasks 1/2/4. Write them as plain prose **specific to this entity and its handoff** — name the actual entities, channels, and risk slice from the evidence; do **not** restate the risk category generically. These are read by non-technical auditors as the headline story; `evidence_quote`, `specific_risk_ids`, and `kpa_ids` remain the supporting evidence behind them. Ground every narrative claim in the same evidence you cite (handoff description, control/quote, risk statements) — do not introduce facts not present in the payload.
