# Handoff/Reliance Review — Full Context for Claude Code

This document captures everything needed to pick up the handoff/reliance review work in Claude Code. It covers the conceptual framework, the Stage 1 manual review findings, the Stage 2 prompt, the batching design considerations, and the data sufficiency evaluation needed before running Stage 2.

Work in this order:
1. Read sections 1–3 to understand the framework and findings
2. Use section 4 to evaluate data sufficiency (this is the first Claude Code task)
3. Use section 5 to design the batching approach (second Claude Code task)
4. Use section 6 as the prompt each batch will actually run

---

## 1. Background and Organizational Context

My company's internal audit function breaks the business into **audit entities (AEs)** — discrete slices of business, functions, or processes that get audited. When scoping an AE's audit, we can:

- **Hand off** pieces of the audit to another AE
- **Rely on** pieces another AE has tested

These two mechanisms serve different purposes and have different failure modes, but the procedures manual doesn't draw the distinction cleanly, which creates coverage risk.

I have two projects that both depend on understanding how handoffs and reliances work:

- **Project 1: Risk assessment transformation tool.** Transforms and surfaces the risk assessment data. Ingests the Excel file described below (as `legacy_risk_data`), resolves handoff From/To tables with name resolution, handles inactive-entity suffixes, and presents description prose alongside each entity's 23 L2 rows.
- **Project 2: Audit universe network map.** Visual network mapping of the audit universe where handoffs are the main connections between entities. Pass 1 classifications are complete; Pass 2 validation is blocked on "what does a well-formed handoff look like?" — which Stage 1 answers.

The review work below serves Project 2 primarily. Project 1 parks Stage 1 findings as reference material for post-pilot.

---

## 2. The Handoff vs. Reliance Framework

### Core distinction: who owns the risk?

**Handoff** = ownership transfers. The risk leaves your register entirely. You no longer test it, no longer conclude on it. Your only residual duty is **handoff hygiene** — verifying the receiving entity's scope actually covers what transferred. Failure mode: scope assumptions diverge, risk falls between entities.

**Reliance** = ownership stays. The risk is still on your register, you still conclude on it. You borrow another party's testing as evidence instead of redoing it. Failure mode: borrowed evidence doesn't actually address the risk angle you care about.

### Key test

"Are they concluding on my audit?" is NOT the right distinction — neither party does that in either case. The right question is: **whose register carries the risk, and who draws the conclusion about whether it's managed?**

### Analogy

- Handoff = moving a box to someone else's warehouse. Not your inventory anymore.
- Reliance = accepting someone else's inspection report on a box still in your warehouse. Your responsibility, your conclusion, just not your hands-on testing.

### Why reliance isn't double-counting

Reliance moves evidence, not ownership. SOX/compliance/external-audit testing isn't concluding on your audit — they're concluding on their own scope for their own purposes. You use their evidence toward your conclusion on your risk. Same controls may get touched, but each conclusion is drawn once, by one party. Reliance, properly used, is what *prevents* duplication.

### The coarse handoff failure mode

The most common and dangerous failure: a functional risk category (AML, sanctions, fraud, privacy, conduct, third-party, data) gets handed to a functional audit entity at the program level, but **embedded control touchpoints inside business processes** stay with the business-process auditor. If the line between program-level and embedded-process-level isn't drawn explicitly, there's a gap.

**Canonical example**: Credit issuance entity hands "AML risk" to the AML functional entity. AML entity audits the AML program. But KYC/CDD controls embedded at credit origination — are those in AML entity's scope or still with the credit entity? If "handed off" is coarse, nobody tests them.

### IIA alignment

This maps to IIA Global Internal Audit Standard 9.5 (Coordination and Reliance, effective Jan 2025). The standard is mostly written about IA↔other assurance providers, but the same logic applies to handoffs between internal audit entities. The formal mechanism the IIA expects is an **assurance map** showing which provider covers which risks.

---

## 3. Stage 1 Manual Review Findings

ChatGPT ran Stage 1 against the procedures manual with line-level citations. Overall: the manual is strongest on distinguishing handoff from reliance and on defining reliance checks. Weakest on explicit risk ownership, attribute-level handoff documentation, and a true assurance-map / one-owner coverage view.

### Risk assessment file structure

Excel file. One row per audit entity. Columns include:

- **Audit entity overview** (prose)
- **Handoff description** (prose)
- For each of **14 risk categories** (financial reporting, external fraud, AML/financial crime, etc.), three columns:
  - **Rating** (critical / high / medium / low, or marked not applicable)
  - **Inherent risk rationale**
  - **Control assessment**

Reliance is NOT in this file — reliance lives at the engagement level, not the entity/planning level. Stage 2 is scoped to handoffs only.

### Question-by-question findings

**1. Distinct concepts?** Meets. Framed as scope-transfer vs. evidence-use rather than risk-register ownership, but the distinction is real.
- "This is considered a hand-off (not a reliance)" (§5.9, 7710-7712)
- "the area scoped out is no longer considered part of the audit scope of the transferor audit and becomes part of the audit scope of the transferee audit" (§5.9, 7716-7718)
- "it may be appropriate for an audit team to leverage the testing performed and conclusions reached within the scope of another audit to help support the conclusions within their audit" (§5.9, 7782-7784)

**2. Explicit risk ownership?** Partially meets. Clear on PGA/AL entity ownership, RCO category ownership, and one-owner-per-issue — but NOT on audit-entity risk ownership in handoff/reliance decisions.
- Key ambiguity: §3.2, 2554-2558 says "When the risk resides within a given AE (AE-1) but is managed in a different AE (AE-2), the L1 risk will be applicable in both entities. In AE-1 the controls assessment at the L1 level will be marked as Not Tested. The controls will be documented and tested within AE-2."
- **This "applicable in both entities" rule directly cuts against a one-owner model.** It's the core structural tension.

**3. Specific scope documentation in handoffs?** Partially meets. Talks about processes/systems/applications and key process areas, but doesn't require the precision reliance requires.
- Reliance requires "specific processes/areas of the audit where the reliance is being placed" (§5.9, 7824-7829)
- Handoff documentation is more reference-based — doesn't explicitly require exact transferred control objective / risk angle / control slice / legal entity / period / population.

**4. Coarse handoff failure mode?** Partially meets, mostly indirectly. Recognizes residence-vs-management and embedded controls in some domains (Consumer Compliance §4.1 5041-5043; privacy §5 7150-7153) but doesn't codify the general boundary.
- "certain automated business process controls (e.g., input, processing, output, interfaces) may still be key controls within the audit entity containing the secondary mapped application" (§2.3.1, 2074-2076)
- **Does NOT use an AML/KYC example even though KYC/AML appears as a risk content area elsewhere.** This specific failure mode is partly recognized but not explicitly neutralized.

**5. Handoff hygiene?** Partially meets. Requires discussion of scope/coverage, Archer review, timing evaluation, and documented due diligence (§5.9, 7733-7758). But never says the transferor must verify the transferee's scope covers the exact risk angle being handed off. Compared to reliance sufficiency, handoff hygiene is much less granular.
- The "alternate procedures" language (§5.9, 7724-7726) muddies the model — a clean handoff should leave only hygiene, not residual risk work.

**6. Reliance sufficiency?** Largely meets. Strongest part of the manual.
- §5.9, 7799-7812: testing occurred, within frequency period, scope discussed, Archer confirms planning/documentation/review, completion/approval, test procedures and conclusions appropriate.
- Cross-cutting standard for reliance on other control functions (§5.8, 7672-7681): "work directly meets IAG's testing objectives"; "scope including testing period, population, and approach is deemed sufficient"; "performed by an individual or function that is independent."
- Only gap: the other-control-functions language isn't imported explicitly into the inter-audit reliance section.

**7. Assurance map?** Partially meets. Partial equivalents exist, no explicit map.
- Audit-universe completeness process (§3.3, 4866-4869)
- Coverage-by-risk-level analysis (§4.1, 4948-4956)
- Law/regulation-to-risk-category mapping (lines 16668-16671)
- RCO risk-category roll-up with liaison to ALs for auxiliary audits (lines 17042-17047)
- Auxiliary Audit scoping (lines 17057-17059)
- RCO accountability for monitoring category coverage (§5.12, 8241-8245)
- **Missing: an explicit single view showing each risk/control slice, its one owning audit entity, and all reliances as supporting evidence.**

**8. Silent/ambiguous/contradictory:**

- **A. Wrong primary test for handoff vs. reliance.** Manual frames around scope mechanics, not risk ownership (§5.9, 7710-7712).
- **B. "Applicable in both entities" conflicts with one-owner model.** (§3.2, 2554-2558)
- **C. Transferor may have residual risk work after handoff** — "alternate procedures" language (§5.9, 7724-7726) muddies whether risk really left the transferor.
- **D. Embedded-control boundaries not reconciled in one place.** §2.3.1 (2074-2076) says embedded controls may remain with secondary-mapped application's audit, vs. §5.9 (7764-7768) saying application controls to which an application is primarily mapped are considered a hand-off. Reconcilable but not spelled out.
- **E. Explicit one-owner accountability for issues (§7.2, 10306-10308), not for risks.** That clarity never appears as a comparable rule for handoff/reliance risk ownership.

### Prioritized gaps (Stage 1 output)

1. **Make audit-entity risk ownership explicit.** For every handoff/reliance decision, say which AE's register carries the risk and which AE concludes on whether it's managed. Today it relies too much on scope language and leaves room for "applicable in both entities."
2. **Require attribute-level handoff documentation.** Exact risk slice / control objective / embedded touchpoint / legal entity / period / population transferred — not just receiving AE or broad process category.
3. **Explicitly address the coarse handoff failure mode.** State that a functional/program audit can own the enterprise program while the business/process audit may still own embedded process-level controls, with required boundary documentation. A KYC-at-origination example would be especially useful.
4. **Strengthen handoff hygiene to match reliance sufficiency.** Import the same rigor — exact objective match, period, population, approach, geography/entity, issue impact.
5. **Create a single coverage view / assurance map.** Current audit-universe and RCO roll-up are helpful but not a clean assurance map proving every risk/control slice has one owner and all other audit work is either a handoff with defined scope or a reliance as supporting evidence.

### Key takeaways for the network map project

- The "applicable in both entities" rule (§3.2 finding) is a **documented design pattern**, not an error. Pipeline logic must treat it as legitimate.
- The manual uses "auxiliary audit" language (lines 17042-17059) that's doing some of the assurance-map work without calling it that. Practitioners will use "auxiliary audit" even if "assurance map" is the conceptual match.
- The manual recognizes embedded controls in some domains (Consumer Compliance, privacy) but doesn't generalize the principle. AML/KYC is not addressed by the manual — worth noting when interpreting handoffs in those categories.

---

## 4. Data Requirements Specification (First Claude Code Task)

**Important: Claude Code has dummy data in this project, not the real data.** The real risk assessment file lives elsewhere. This means Claude Code can't evaluate actual data sufficiency — it can only reason about what the Stage 2 review will need and tell me what the real data must contain when I bring it in.

### What the real data looks like (production state)

From the risk assessment file (`legacy_risk_data`, Excel, one row per audit entity, ~450 entities, ~4,400 handoffs):
- Audit entity overview (prose)
- Handoff description (prose)
- For each of 14 risk categories: rating, inherent risk rationale, control assessment

From the network map pipeline (already built against dummy data, will run against real data):
- Resolved handoff From/To tables with name resolution
- Inactive-entity handling
- Pass 1 handoff classifications (complete in dummy, will re-run on real)
- Connectivity scores / graph structure
- Chain analysis post-Pass-1

### What I need from Claude Code

Use the dummy data to understand the **shape and schema** of what's available, then tell me:

1. **What fields Stage 2 needs per batch.** Based on the Stage 2 tasks in section 6, what data fields does the model need to see for each entity to evaluate handoffs well? Derive this from the tasks, not from what's convenient.

2. **Gap analysis against dummy schema.** Does the dummy data's shape appear to carry everything Stage 2 needs, or are there fields Stage 2 assumes exist that aren't represented? Flag these as "real data must have X" requirements.

3. **Derived fields worth computing.** Are there fields Stage 2 would benefit from that aren't in the raw data but could be derived — e.g., "which of B's 14 risk categories does this handoff from A likely map to?" If so, should the derivation happen in the batching script before the prompt runs, or should the prompt infer it?

4. **Pass 1 classification integration.** Should Pass 1 classifications be included in the batch payload as input to the Stage 2 prompt, or would that bias the evaluation? Argue both sides and recommend.

5. **Adjacent data sources worth considering.** Based on the project structure, are there other data sources (entity metadata, RCO assignments, audit plan data, KPA mappings, prior findings) that Stage 2 would benefit from? These may not exist in dummy data but could be added to the real pipeline.

6. **Noise to exclude.** Any fields in the dummy schema that should deliberately NOT be passed to the model because they'd distract from the handoff evaluation?

### Specific questions to answer

- For Task 2 (handoff representation in ratings): does the dummy schema carry rating / rationale / control assessment in a form a batch payload can pass cleanly, or would it need joining/reshaping?
- For Task 3 (coarse-handoff test): is there any field — in dummy or worth adding to real — that signals which risk categories are functional-program-type (AML, sanctions, etc.) vs business-process-type? Or must the model infer from category name?
- For Task 5 (cross-entity consistency): given a handoff A→B, can the dummy structure support pulling B's full row into the same batch payload? Is there a clean mapping from "handoff description prose" to "which of B's 14 risk categories this lands in"?

### Output I want

- Recommended batch payload schema (field list, types, source, whether raw or derived)
- List of "real data must contain X" requirements — things the real data needs that I should verify before running Stage 2
- List of derived fields worth computing pre-prompt, with logic sketch for each
- Explicit recommendation on Pass 1 classification inclusion
- Fields to exclude from payload with reasoning

**Don't build the batching script yet. Specify the data requirements first.**

---

## 5. Batching Design (Second Claude Code Task)

Production scale: ~450 audit entities, ~4,400 handoffs. Dummy data in the project is smaller but has the same shape.

I can't run the Stage 2 prompt on the full real dataset in one shot — too much data, model will lose detail. I need a batching script that works when real data arrives.

### Design goals

- Each batch contains entities whose handoff relationships can be meaningfully evaluated together. Cross-entity consistency (Stage 2 Task 5) requires both ends of a handoff in the same batch.
- Stage 1 findings and the framework travel with every batch as static context.
- Only entity data varies per batch.
- Output is structured (JSON or similar) so findings from all batches aggregate into one dataset. Ranked summary gets produced once at the end, across everything.
- Script logs batch status, writes results as it goes, and is re-runnable on just failed batches.
- Show a per-batch cost/token estimate before committing to a full run.
- Script must work against dummy data for development/testing, then against real data when available. Don't hardcode assumptions that only hold for one.

### Questions for Claude Code to answer

1. What's the right batch unit given the graph structure? Connected components? Communities from network analysis? Something else? Reason from the dummy data's shape, but explicitly call out whether the approach will scale/adapt when real data (450 entities, 4,400 handoffs) lands.
2. What batch size balances model context limits against cross-entity signal preservation? Base this on token budgets per batch given the payload schema from section 4, not on entity count alone.
3. For entities that span multiple components or appear in multiple batches, how should duplication be handled?
4. Can Pass 1 classifications prioritize batch ordering — e.g., run high-risk multi-hop same-category chains first, so we get signal on the most likely coverage gaps before burning through the full run? (Note: dummy Pass 1 classifications exist; real ones will need to be regenerated.)
5. Are there categories of entities or handoffs to exclude or pre-filter (inactive entities, empty handoff descriptions, etc.)? Build the filtering logic against the schema; tune thresholds when real data is in.

### Validation approach given dummy data

- Develop and test the batching script against dummy data end-to-end, including a small test batch actually hitting the model.
- Document any tuning parameters (batch size, filter thresholds, prioritization weights) that will likely need re-tuning when real data lands.
- Produce a dry-run mode that prints batch composition and token estimates without calling the model, so I can inspect the plan before committing real budget.

### Budget context

Before the full run against real data, I'll provide a budget ceiling so the script can calibrate. For dummy-data testing, just keep it cheap — a few batches to validate end-to-end.

**Propose before building.** With 450 entities and 4,400 handoffs at production scale, the wrong batching choice wastes a lot of API calls. Design against the dummy schema but with an eye to production.

---

## 6. The Stage 2 Prompt (What Each Batch Will Run)

```
Using the handoff framework and the manual review findings from Prompt 1, 
evaluate whether the attached audit entity risk assessment actually follows 
what the manual requires. Focus only on handoffs. Reliance is handled at 
the engagement level and is out of scope here.

MANUAL REVIEW FINDINGS (from Prompt 1)
[PASTE HERE — use Stage 1 findings from section 3 above]

FILE STRUCTURE
Excel file. One row per audit entity. Columns:
- Audit entity overview (prose)
- Handoff description (prose)
- For each of 14 risk categories (e.g., financial reporting, external fraud, 
  AML/financial crime, etc.), three columns:
    • Rating (critical / high / medium / low, or marked not applicable)
    • Inherent risk rationale
    • Control assessment

TASK
For each requirement, expectation, or rule the manual establishes about 
handoffs, check whether the risk assessment file conforms. Treat the manual 
review findings as the standard and the file as the evidence.

EVALUATE

1. Manual-to-file conformance
   Walk through each handoff-related requirement identified in the manual 
   review. For each one:
    - Does the file demonstrate conformance? Where?
    - Does the file contradict or ignore it? Where?
    - If the manual was silent or ambiguous on something (per Prompt 1 
      findings), how is the file handling it in practice? What de facto 
      rule is the team following?

2. Handoff representation in the ratings
   The file has a handoff description column and 14 risk categories each 
   with rating + inherent rationale + control assessment. Check whether 
   handoffs described in the handoff column are reflected consistently 
   in the three rating columns for the affected risk categories. Patterns 
   to assess against what the manual requires:
    - Handed off and marked not applicable
    - Handed off but still rated, with rationale acknowledging partial 
      retention
    - Handed off but rated normally with no acknowledgment
    - Rationale or control assessment references another entity, but 
      handoff column is silent (undocumented handoff)
   Flag cases where the file's treatment diverges from what the manual 
   prescribes — or where the manual is silent and the team has adopted 
   an inconsistent approach across entities or risk categories.

3. Coarse-handoff test
   If the manual requires handoffs to specify the scope transferred 
   (program-level vs embedded-process-level controls), check each handoff 
   description against that bar. Prioritize functional risk categories 
   where embedded controls within business processes are typical (AML, 
   sanctions, fraud, privacy, conduct, data, third-party). Flag handoffs 
   that name only the category or receiving entity without specifying 
   the embedded layer.
   If the manual is silent on this, flag it as an area where the file 
   inherits the manual's gap — and note whether the file's practice 
   creates likely coverage holes regardless.

4. Overview-to-rationale alignment
   If the manual requires the overview, handoff description, and risk 
   rationales to be internally consistent, test that. Examples:
    - Overview describes activities that would generate a risk; rating 
      marks it not applicable with no handoff explanation
    - Handoff description names a receiving entity; rationale for that 
      risk contradicts the handoff (e.g., still describes this entity 
      as owner)
    - Control assessment describes controls this entity operates for a 
      risk the handoff says was transferred

5. Cross-entity consistency (if multiple rows)
   If the manual expects handoffs to be reciprocally visible — i.e., if 
   entity A hands off to entity B, entity B's row should show that risk 
   in scope and owned — check for mismatches. These are the strongest 
   indicators of real coverage gaps rather than documentation issues.

OUTPUT
For each finding:
- Manual requirement or expectation being tested (quote or paraphrase from 
  Prompt 1 findings)
- Entity and risk category in the file
- What the file shows, with quoted text from the relevant columns
- Classification: conforms / documentation issue / likely coverage gap
- Brief reasoning

End with a ranked summary:
- Likely coverage gaps (a risk appears to have no owner), highest confidence first
- Systemic documentation issues (same pattern across many entities)
- Manual gaps the file exposes (places where the manual needs to say more)
```

---

## 7. Sequencing Summary for Claude Code Session

**Reminder: Claude Code has dummy data, not real data. Design against the schema; validate end-to-end against dummy; keep tuning parameters explicit so they can be revisited when real data arrives.**

1. **Data requirements specification** (section 4). Claude Code inspects the dummy data's schema, derives what Stage 2 needs, and tells me what the real data must contain. I decide what to add to the real data pipeline before proceeding.
2. **Batching design proposal** (section 5). Claude Code looks at the dummy graph structure and Pass 1 data, proposes a batching approach, estimates token/cost cost at production scale (450 entities, 4,400 handoffs). I approve or adjust before any code gets written.
3. **Build the batching script against dummy data.** Structured output per batch, resume-able, cost-aware, with a dry-run mode.
4. **Run a small test batch against dummy data** to sanity-check output quality and end-to-end flow.
5. **When real data is available:** load it, re-tune any parameters flagged in step 2, run the full batches, aggregate results, produce the final ranked summary.
