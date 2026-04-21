# Stage 2 Handoff Review — Batch 001

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
[
  {
    "entity_id": "AE-2",
    "entity_name": "Commercial Banking",
    "business_unit": "Global Consumer",
    "line_of_defense": "2nd Line of Defense",
    "horizontal_flag": false,
    "overview": "This entity covers the commercial banking function.",
    "handoff_description": "Processes are handed off related to commercial banking operations.",
    "handoffs_to": [
      {
        "id": "AE-36",
        "name": "Vendor Management",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [
      {
        "id": "AE-25",
        "name": "Dispute Resolution",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "Critical",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Funding & Liquidity",
        "residual_rating": "Critical",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "Critical",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "Critical",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls": [
      {
        "control_id": "CTRL-0021",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that transaction monitoring rules are not calibrated against typologies. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0022",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that audit findings are not tracked to remediation. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0023",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff",
        "control_description": "Governance control providing oversight of Training & Awareness. Mitigates the risk: Risk that annual AML training is not delivered to in-scope staff. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0024",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that Suspicious Activity Reports are not filed within regulatory deadlines. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0025",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy",
        "control_description": "Governance control providing oversight of Vendor Due Diligence. Mitigates the risk: Risk that vendors are not onboarded per Third Party Risk policy. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0026",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff",
        "control_description": "Governance control providing oversight of Training & Awareness. Mitigates the risk: Risk that annual AML training is not delivered to in-scope staff. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0027",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation",
        "control_description": "Control operated within Change Management. Mitigates the risk: Risk that emergency changes are not documented post-implementation. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0028",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff",
        "control_description": "Governance control providing oversight of Training & Awareness. Mitigates the risk: Risk that annual AML training is not delivered to in-scope staff. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0029",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy",
        "control_description": "Governance control providing oversight of Vendor Due Diligence. Mitigates the risk: Risk that vendors are not onboarded per Third Party Risk policy. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0030",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff",
        "control_description": "Governance control providing oversight of Training & Awareness. Mitigates the risk: Risk that annual AML training is not delivered to in-scope staff. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0031",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage",
        "control_description": "Governance control providing oversight of Sanctions Program Oversight. Mitigates the risk: Risk that the sanctions screening program has inadequate list coverage. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0032",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that production access is not provisioned per least-privilege policy. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0033",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that audit findings are not tracked to remediation. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0034",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage",
        "control_description": "Governance control providing oversight of Sanctions Program Oversight. Mitigates the risk: Risk that the sanctions screening program has inadequate list coverage. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0035",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that Suspicious Activity Reports are not filed within regulatory deadlines. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0036",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that production access is not provisioned per least-privilege policy. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0037",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-110",
        "specific_risk_description": "Risk that credit decisioning criteria are not applied at origination",
        "control_description": "Control operated within Credit Origination. Mitigates the risk: Risk that credit decisioning criteria are not applied at origination. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-107",
        "description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "id": "SR-124",
        "description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "id": "SR-106",
        "description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "id": "SR-108",
        "description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "id": "SR-116",
        "description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "id": "SR-121",
        "description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "id": "SR-109",
        "description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "id": "SR-118",
        "description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "id": "SR-110",
        "description": "Risk that credit decisioning criteria are not applied at origination"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-017",
        "description": "AML Transaction Monitoring Calibration"
      },
      {
        "id": "KPA-014",
        "description": "Issue Management"
      },
      {
        "id": "KPA-020",
        "description": "Training & Awareness"
      },
      {
        "id": "KPA-008",
        "description": "Vendor Due Diligence"
      },
      {
        "id": "KPA-011",
        "description": "Change Management"
      },
      {
        "id": "KPA-018",
        "description": "Sanctions Program Oversight"
      },
      {
        "id": "KPA-010",
        "description": "Access Management"
      },
      {
        "id": "KPA-002",
        "description": "Credit Origination"
      }
    ]
  },
  {
    "entity_id": "AE-22",
    "entity_name": "AML Monitoring",
    "business_unit": "Operations",
    "line_of_defense": "1st Line of Defense",
    "horizontal_flag": true,
    "overview": "This entity covers the aml monitoring function.",
    "handoff_description": "Processes are handed off related to aml monitoring operations.",
    "handoffs_to": [],
    "handoffs_from": [
      {
        "id": "AE-20",
        "name": "Customer Onboarding",
        "inactive_flag": false
      },
      {
        "id": "AE-33",
        "name": "Data Governance",
        "inactive_flag": false
      },
      {
        "id": "AE-2",
        "name": "Commercial Banking",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Country",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "Critical",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Security",
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "Medium",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls": [
      {
        "control_id": "CTRL-0398",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained",
        "control_description": "Governance control providing oversight of AML Program Framework. Mitigates the risk: Risk that the AML program framework and policies are not maintained. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0399",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained",
        "control_description": "Governance control providing oversight of AML Program Framework. Mitigates the risk: Risk that the AML program framework and policies are not maintained. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0400",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff",
        "control_description": "Governance control providing oversight of Training & Awareness. Mitigates the risk: Risk that annual AML training is not delivered to in-scope staff. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0401",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that transaction monitoring rules are not calibrated against typologies. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0402",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that transaction monitoring rules are not calibrated against typologies. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0403",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that transaction monitoring rules are not calibrated against typologies. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0404",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that Suspicious Activity Reports are not filed within regulatory deadlines. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0405",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage",
        "control_description": "Governance control providing oversight of Sanctions Program Oversight. Mitigates the risk: Risk that the sanctions screening program has inadequate list coverage. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0406",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage",
        "control_description": "Governance control providing oversight of Sanctions Program Oversight. Mitigates the risk: Risk that the sanctions screening program has inadequate list coverage. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0407",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that production access is not provisioned per least-privilege policy. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0408",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that transaction monitoring rules are not calibrated against typologies. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0409",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation",
        "control_description": "Control operated within Change Management. Mitigates the risk: Risk that emergency changes are not documented post-implementation. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0410",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that customer data is not protected in transit and at rest. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0411",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that Suspicious Activity Reports are not filed within regulatory deadlines. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-105",
        "description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "id": "SR-106",
        "description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "id": "SR-107",
        "description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "id": "SR-108",
        "description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "id": "SR-109",
        "description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "id": "SR-118",
        "description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "id": "SR-121",
        "description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "id": "SR-130",
        "description": "Risk that customer data is not protected in transit and at rest"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-016",
        "description": "AML Program Framework"
      },
      {
        "id": "KPA-020",
        "description": "Training & Awareness"
      },
      {
        "id": "KPA-017",
        "description": "AML Transaction Monitoring Calibration"
      },
      {
        "id": "KPA-018",
        "description": "Sanctions Program Oversight"
      },
      {
        "id": "KPA-010",
        "description": "Access Management"
      },
      {
        "id": "KPA-011",
        "description": "Change Management"
      }
    ]
  },
  {
    "entity_id": "AE-41",
    "entity_name": "Compliance Advisory",
    "business_unit": "Corporate Functions",
    "line_of_defense": "2nd Line of Defense",
    "horizontal_flag": true,
    "overview": "This entity covers the compliance advisory function.",
    "handoff_description": "Processes are handed off related to compliance advisory operations.",
    "handoffs_to": [
      {
        "id": "AE-20",
        "name": "Customer Onboarding",
        "inactive_flag": false
      },
      {
        "id": "AE-18",
        "name": "ATM Operations",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [
      {
        "id": "AE-2",
        "name": "Commercial Banking",
        "inactive_flag": false
      },
      {
        "id": "AE-22",
        "name": "AML Monitoring",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "Low",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "Low",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Technology",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Security",
        "residual_rating": "Critical",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "Low",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "Critical",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls": [
      {
        "control_id": "CTRL-0770",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained",
        "control_description": "Governance control providing oversight of AML Program Framework. Mitigates the risk: Risk that the AML program framework and policies are not maintained. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0771",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that periodic entity-level risk assessments are not completed. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0772",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that periodic entity-level risk assessments are not completed. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0773",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that audit findings are not tracked to remediation. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0774",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that audit findings are not tracked to remediation. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0775",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that customer data is not protected in transit and at rest. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0776",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically",
        "control_description": "Governance control providing oversight of Vendor Performance Monitoring. Mitigates the risk: Risk that vendor SLAs and performance are not monitored periodically. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0777",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff",
        "control_description": "Governance control providing oversight of Training & Awareness. Mitigates the risk: Risk that annual AML training is not delivered to in-scope staff. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0778",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that Suspicious Activity Reports are not filed within regulatory deadlines. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0779",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that audit findings are not tracked to remediation. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0780",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained",
        "control_description": "Governance control providing oversight of AML Program Framework. Mitigates the risk: Risk that the AML program framework and policies are not maintained. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0781",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that audit findings are not tracked to remediation. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0782",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage",
        "control_description": "Governance control providing oversight of Sanctions Program Oversight. Mitigates the risk: Risk that the sanctions screening program has inadequate list coverage. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0783",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage",
        "control_description": "Governance control providing oversight of Sanctions Program Oversight. Mitigates the risk: Risk that the sanctions screening program has inadequate list coverage. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0784",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy",
        "control_description": "Governance control providing oversight of Vendor Due Diligence. Mitigates the risk: Risk that vendors are not onboarded per Third Party Risk policy. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0785",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff",
        "control_description": "Governance control providing oversight of Training & Awareness. Mitigates the risk: Risk that annual AML training is not delivered to in-scope staff. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0786",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically",
        "control_description": "Governance control providing oversight of Vendor Performance Monitoring. Mitigates the risk: Risk that vendor SLAs and performance are not monitored periodically. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0787",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically",
        "control_description": "Governance control providing oversight of Vendor Performance Monitoring. Mitigates the risk: Risk that vendor SLAs and performance are not monitored periodically. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0788",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that customer data is not protected in transit and at rest. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0789",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release",
        "control_description": "Control operated within Change Management. Mitigates the risk: Risk that production changes are not approved before release. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-105",
        "description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "id": "SR-128",
        "description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "id": "SR-124",
        "description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "id": "SR-130",
        "description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "id": "SR-117",
        "description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "id": "SR-106",
        "description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "id": "SR-108",
        "description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "id": "SR-109",
        "description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "id": "SR-116",
        "description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "id": "SR-120",
        "description": "Risk that production changes are not approved before release"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-016",
        "description": "AML Program Framework"
      },
      {
        "id": "KPA-014",
        "description": "Issue Management"
      },
      {
        "id": "KPA-010",
        "description": "Access Management"
      },
      {
        "id": "KPA-009",
        "description": "Vendor Performance Monitoring"
      },
      {
        "id": "KPA-020",
        "description": "Training & Awareness"
      },
      {
        "id": "KPA-017",
        "description": "AML Transaction Monitoring Calibration"
      },
      {
        "id": "KPA-018",
        "description": "Sanctions Program Oversight"
      },
      {
        "id": "KPA-008",
        "description": "Vendor Due Diligence"
      },
      {
        "id": "KPA-011",
        "description": "Change Management"
      }
    ]
  }
]
```

## Target-context entities (handoff targets — reference for Task 5; do not produce findings about them)

```json
[
  {
    "entity_id": "AE-18",
    "entity_name": "ATM Operations",
    "business_unit": "Global Consumer",
    "line_of_defense": "2nd Line of Defense",
    "role": "target_context",
    "horizontal_flag": false,
    "handoff_description": "nan",
    "handoffs_to": [
      {
        "id": "AE-30",
        "name": "Regulatory Reporting",
        "inactive_flag": false
      },
      {
        "id": "AE-34",
        "name": "Cloud Services",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [
      {
        "id": "AE-6",
        "name": "ACH Processing",
        "inactive_flag": false
      },
      {
        "id": "AE-11",
        "name": "Trade Finance",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "Critical",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "Critical",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "Low",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Funding & Liquidity",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Technology",
        "residual_rating": "Critical",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Security",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "Low",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "Low",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0328",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-112",
        "specific_risk_description": "Risk that payment instructions are not authorized before release"
      },
      {
        "control_id": "CTRL-0329",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-112",
        "specific_risk_description": "Risk that payment instructions are not authorized before release"
      },
      {
        "control_id": "CTRL-0330",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-112",
        "specific_risk_description": "Risk that payment instructions are not authorized before release"
      },
      {
        "control_id": "CTRL-0331",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0332",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0333",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0334",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0335",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0336",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0337",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "control_id": "CTRL-0338",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "control_id": "CTRL-0339",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0340",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0341",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0342",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "control_id": "CTRL-0343",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "control_id": "CTRL-0344",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "control_id": "CTRL-0345",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "control_id": "CTRL-0346",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "control_id": "CTRL-0347",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-112",
        "description": "Risk that payment instructions are not authorized before release"
      },
      {
        "id": "SR-118",
        "description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "id": "SR-117",
        "description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "id": "SR-124",
        "description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "id": "SR-106",
        "description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "id": "SR-130",
        "description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "id": "SR-105",
        "description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "id": "SR-108",
        "description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "id": "SR-109",
        "description": "Risk that the sanctions screening program has inadequate list coverage"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-004",
        "description": "Payment Authorization"
      },
      {
        "id": "KPA-010",
        "description": "Access Management"
      },
      {
        "id": "KPA-009",
        "description": "Vendor Performance Monitoring"
      },
      {
        "id": "KPA-014",
        "description": "Issue Management"
      },
      {
        "id": "KPA-020",
        "description": "Training & Awareness"
      },
      {
        "id": "KPA-016",
        "description": "AML Program Framework"
      },
      {
        "id": "KPA-017",
        "description": "AML Transaction Monitoring Calibration"
      },
      {
        "id": "KPA-018",
        "description": "Sanctions Program Oversight"
      }
    ]
  },
  {
    "entity_id": "AE-20",
    "entity_name": "Customer Onboarding",
    "business_unit": "Global Commercial",
    "line_of_defense": "2nd Line of Defense",
    "role": "target_context",
    "horizontal_flag": false,
    "handoff_description": "Processes are handed off related to customer onboarding operations.",
    "handoffs_to": [
      {
        "id": "AE-25",
        "name": "Dispute Resolution",
        "inactive_flag": false
      },
      {
        "id": "AE-27",
        "name": "Accounts Payable",
        "inactive_flag": false
      },
      {
        "id": "AE-22",
        "name": "AML Monitoring",
        "inactive_flag": false
      },
      {
        "id": "AE-43",
        "name": "Business Continuity",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [
      {
        "id": "AE-5",
        "name": "Wire Transfers",
        "inactive_flag": false
      },
      {
        "id": "AE-38",
        "name": "Credit Risk Management",
        "inactive_flag": false
      },
      {
        "id": "AE-9",
        "name": "Mortgage Origination",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "Critical",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Funding & Liquidity",
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Technology",
        "residual_rating": "Critical",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Security",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "Critical",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "Critical",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0361",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged"
      },
      {
        "control_id": "CTRL-0362",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged"
      },
      {
        "control_id": "CTRL-0363",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged"
      },
      {
        "control_id": "CTRL-0364",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0365",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0366",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0367",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-103",
        "specific_risk_description": "Risk that sanctions screening is not performed at customer onboarding"
      },
      {
        "control_id": "CTRL-0368",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-103",
        "specific_risk_description": "Risk that sanctions screening is not performed at customer onboarding"
      },
      {
        "control_id": "CTRL-0369",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0370",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0371",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "control_id": "CTRL-0372",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged"
      },
      {
        "control_id": "CTRL-0373",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "control_id": "CTRL-0374",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0375",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "control_id": "CTRL-0376",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "control_id": "CTRL-0377",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged"
      },
      {
        "control_id": "CTRL-0378",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0379",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0380",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0381",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0382",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0383",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "control_id": "CTRL-0384",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-129",
        "description": "Risk that customer complaints are not logged and triaged"
      },
      {
        "id": "SR-130",
        "description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "id": "SR-103",
        "description": "Risk that sanctions screening is not performed at customer onboarding"
      },
      {
        "id": "SR-117",
        "description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "id": "SR-118",
        "description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "id": "SR-116",
        "description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "id": "SR-108",
        "description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "id": "SR-128",
        "description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "id": "SR-107",
        "description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "id": "SR-124",
        "description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "id": "SR-120",
        "description": "Risk that production changes are not approved before release"
      },
      {
        "id": "SR-106",
        "description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "id": "SR-119",
        "description": "Risk that user access is not recertified on the required cadence"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-005",
        "description": "Account Servicing"
      },
      {
        "id": "KPA-010",
        "description": "Access Management"
      },
      {
        "id": "KPA-001",
        "description": "Customer Onboarding"
      },
      {
        "id": "KPA-009",
        "description": "Vendor Performance Monitoring"
      },
      {
        "id": "KPA-008",
        "description": "Vendor Due Diligence"
      },
      {
        "id": "KPA-017",
        "description": "AML Transaction Monitoring Calibration"
      },
      {
        "id": "KPA-014",
        "description": "Issue Management"
      },
      {
        "id": "KPA-011",
        "description": "Change Management"
      },
      {
        "id": "KPA-020",
        "description": "Training & Awareness"
      }
    ]
  },
  {
    "entity_id": "AE-36",
    "entity_name": "Vendor Management",
    "business_unit": "Operations",
    "line_of_defense": "1st Line of Defense",
    "role": "target_context",
    "horizontal_flag": true,
    "handoff_description": "Processes are handed off related to vendor management operations.",
    "handoffs_to": [
      {
        "id": "AE-1",
        "name": "Consumer Lending",
        "inactive_flag": false
      },
      {
        "id": "AE-44",
        "name": "HR Operations",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "Low",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Funding & Liquidity",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Technology",
        "residual_rating": "Critical",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Security",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "Low",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "Medium",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0687",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "control_id": "CTRL-0688",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "control_id": "CTRL-0689",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "control_id": "CTRL-0690",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0691",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0692",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0693",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0694",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "control_id": "CTRL-0695",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0696",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0697",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-116",
        "description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "id": "SR-117",
        "description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "id": "SR-121",
        "description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "id": "SR-108",
        "description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "id": "SR-106",
        "description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "id": "SR-120",
        "description": "Risk that production changes are not approved before release"
      },
      {
        "id": "SR-107",
        "description": "Risk that transaction monitoring rules are not calibrated against typologies"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-008",
        "description": "Vendor Due Diligence"
      },
      {
        "id": "KPA-009",
        "description": "Vendor Performance Monitoring"
      },
      {
        "id": "KPA-011",
        "description": "Change Management"
      },
      {
        "id": "KPA-017",
        "description": "AML Transaction Monitoring Calibration"
      },
      {
        "id": "KPA-020",
        "description": "Training & Awareness"
      }
    ]
  }
]
```

## Source-context entities (handoff sources — reference for reciprocity checks; do not produce findings about them)

```json
[
  {
    "entity_id": "AE-25",
    "entity_name": "Dispute Resolution",
    "role": "source_context",
    "handoff_description": "Processes are handed off related to dispute resolution operations.",
    "handoffs_to": [
      {
        "id": "AE-40",
        "name": "Operational Risk",
        "inactive_flag": false
      },
      {
        "id": "AE-24",
        "name": "Fraud Detection",
        "inactive_flag": false
      },
      {
        "id": "AE-28",
        "name": "General Ledger",
        "inactive_flag": false
      },
      {
        "id": "AE-37",
        "name": "Model Validation",
        "inactive_flag": false
      },
      {
        "id": "AE-32",
        "name": "Cybersecurity",
        "inactive_flag": false
      }
    ]
  },
  {
    "entity_id": "AE-33",
    "entity_name": "Data Governance",
    "role": "source_context",
    "handoff_description": "Processes are handed off related to data governance operations.",
    "handoffs_to": [
      {
        "id": "AE-19",
        "name": "Branch Operations",
        "inactive_flag": false
      },
      {
        "id": "AE-22",
        "name": "AML Monitoring",
        "inactive_flag": false
      }
    ]
  }
]
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
