# Stage 2 Handoff Review — Batch 003

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
    "entity_id": "AE-20",
    "entity_name": "Customer Onboarding",
    "business_unit": "Global Commercial",
    "line_of_defense": "2nd Line of Defense",
    "horizontal_flag": false,
    "overview": "This entity covers the customer onboarding function.",
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
    "controls": [
      {
        "control_id": "CTRL-0361",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged",
        "control_description": "Control operated within Account Servicing. Mitigates the risk: Risk that customer complaints are not logged and triaged. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0362",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged",
        "control_description": "Control operated within Account Servicing. Mitigates the risk: Risk that customer complaints are not logged and triaged. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0363",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged",
        "control_description": "Control operated within Account Servicing. Mitigates the risk: Risk that customer complaints are not logged and triaged. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0364",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that customer data is not protected in transit and at rest. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0365",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that customer data is not protected in transit and at rest. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0366",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that customer data is not protected in transit and at rest. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0367",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-103",
        "specific_risk_description": "Risk that sanctions screening is not performed at customer onboarding",
        "control_description": "Control operated within Customer Onboarding. Mitigates the risk: Risk that sanctions screening is not performed at customer onboarding. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0368",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-103",
        "specific_risk_description": "Risk that sanctions screening is not performed at customer onboarding",
        "control_description": "Control operated within Customer Onboarding. Mitigates the risk: Risk that sanctions screening is not performed at customer onboarding. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0369",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically",
        "control_description": "Governance control providing oversight of Vendor Performance Monitoring. Mitigates the risk: Risk that vendor SLAs and performance are not monitored periodically. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0370",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that production access is not provisioned per least-privilege policy. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0371",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy",
        "control_description": "Governance control providing oversight of Vendor Due Diligence. Mitigates the risk: Risk that vendors are not onboarded per Third Party Risk policy. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0372",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged",
        "control_description": "Control operated within Account Servicing. Mitigates the risk: Risk that customer complaints are not logged and triaged. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0373",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that Suspicious Activity Reports are not filed within regulatory deadlines. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0374",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that periodic entity-level risk assessments are not completed. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0375",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that transaction monitoring rules are not calibrated against typologies. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0376",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that audit findings are not tracked to remediation. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0377",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged",
        "control_description": "Control operated within Account Servicing. Mitigates the risk: Risk that customer complaints are not logged and triaged. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0378",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release",
        "control_description": "Control operated within Change Management. Mitigates the risk: Risk that production changes are not approved before release. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0379",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff",
        "control_description": "Governance control providing oversight of Training & Awareness. Mitigates the risk: Risk that annual AML training is not delivered to in-scope staff. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0380",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically",
        "control_description": "Governance control providing oversight of Vendor Performance Monitoring. Mitigates the risk: Risk that vendor SLAs and performance are not monitored periodically. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0381",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that periodic entity-level risk assessments are not completed. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0382",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff",
        "control_description": "Governance control providing oversight of Training & Awareness. Mitigates the risk: Risk that annual AML training is not delivered to in-scope staff. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0383",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy",
        "control_description": "Governance control providing oversight of Vendor Due Diligence. Mitigates the risk: Risk that vendors are not onboarded per Third Party Risk policy. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0384",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that user access is not recertified on the required cadence. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
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
    "entity_id": "AE-23",
    "entity_name": "Sanctions Screening",
    "business_unit": "Technology",
    "line_of_defense": "1st Line of Defense",
    "horizontal_flag": true,
    "overview": "This entity covers the sanctions screening function.",
    "handoff_description": "Processes are handed off related to sanctions screening operations.",
    "handoffs_to": [
      {
        "id": "AE-15",
        "name": "Asset Management",
        "inactive_flag": false
      },
      {
        "id": "AE-4",
        "name": "Treasury Operations",
        "inactive_flag": false
      },
      {
        "id": "AE-39",
        "name": "Market Risk Management",
        "inactive_flag": false
      },
      {
        "id": "AE-32",
        "name": "Cybersecurity",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [
      {
        "id": "AE-43",
        "name": "Business Continuity",
        "inactive_flag": false
      },
      {
        "id": "AE-39",
        "name": "Market Risk Management",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "Critical",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Security",
        "residual_rating": "Critical",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "Critical",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "Low",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
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
        "risk_category": "Strategic & Business",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "Critical",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls": [
      {
        "control_id": "CTRL-0412",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage",
        "control_description": "Governance control providing oversight of Sanctions Program Oversight. Mitigates the risk: Risk that the sanctions screening program has inadequate list coverage. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0413",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage",
        "control_description": "Governance control providing oversight of Sanctions Program Oversight. Mitigates the risk: Risk that the sanctions screening program has inadequate list coverage. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0414",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage",
        "control_description": "Governance control providing oversight of Sanctions Program Oversight. Mitigates the risk: Risk that the sanctions screening program has inadequate list coverage. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0415",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically",
        "control_description": "Governance control providing oversight of Vendor Performance Monitoring. Mitigates the risk: Risk that vendor SLAs and performance are not monitored periodically. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0416",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that user access is not recertified on the required cadence. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0417",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically",
        "control_description": "Governance control providing oversight of Vendor Performance Monitoring. Mitigates the risk: Risk that vendor SLAs and performance are not monitored periodically. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0418",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy",
        "control_description": "Governance control providing oversight of Vendor Due Diligence. Mitigates the risk: Risk that vendors are not onboarded per Third Party Risk policy. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0419",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically",
        "control_description": "Governance control providing oversight of Vendor Performance Monitoring. Mitigates the risk: Risk that vendor SLAs and performance are not monitored periodically. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0420",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that Suspicious Activity Reports are not filed within regulatory deadlines. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0421",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy",
        "control_description": "Governance control providing oversight of Vendor Due Diligence. Mitigates the risk: Risk that vendors are not onboarded per Third Party Risk policy. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0422",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy",
        "control_description": "Governance control providing oversight of Vendor Due Diligence. Mitigates the risk: Risk that vendors are not onboarded per Third Party Risk policy. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0423",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff",
        "control_description": "Governance control providing oversight of Training & Awareness. Mitigates the risk: Risk that annual AML training is not delivered to in-scope staff. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0424",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that audit findings are not tracked to remediation. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0425",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy",
        "control_description": "Governance control providing oversight of Vendor Due Diligence. Mitigates the risk: Risk that vendors are not onboarded per Third Party Risk policy. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0426",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained",
        "control_description": "Governance control providing oversight of AML Program Framework. Mitigates the risk: Risk that the AML program framework and policies are not maintained. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-109",
        "description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "id": "SR-117",
        "description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "id": "SR-119",
        "description": "Risk that user access is not recertified on the required cadence"
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
        "id": "SR-106",
        "description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "id": "SR-124",
        "description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "id": "SR-105",
        "description": "Risk that the AML program framework and policies are not maintained"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-018",
        "description": "Sanctions Program Oversight"
      },
      {
        "id": "KPA-009",
        "description": "Vendor Performance Monitoring"
      },
      {
        "id": "KPA-010",
        "description": "Access Management"
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
        "id": "KPA-020",
        "description": "Training & Awareness"
      },
      {
        "id": "KPA-014",
        "description": "Issue Management"
      },
      {
        "id": "KPA-016",
        "description": "AML Program Framework"
      }
    ]
  },
  {
    "entity_id": "AE-35",
    "entity_name": "Application Development",
    "business_unit": "Technology",
    "line_of_defense": "1st Line of Defense",
    "horizontal_flag": false,
    "overview": "This entity covers the application development function.",
    "handoff_description": "Processes are handed off related to application development operations.",
    "handoffs_to": [
      {
        "id": "AE-9",
        "name": "Mortgage Origination",
        "inactive_flag": false
      },
      {
        "id": "AE-1",
        "name": "Consumer Lending",
        "inactive_flag": false
      },
      {
        "id": "AE-11",
        "name": "Trade Finance",
        "inactive_flag": false
      },
      {
        "id": "AE-32",
        "name": "Cybersecurity",
        "inactive_flag": false
      },
      {
        "id": "AE-23",
        "name": "Sanctions Screening",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "Critical",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "Medium",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Funding & Liquidity",
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Technology",
        "residual_rating": "Low",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
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
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls": [
      {
        "control_id": "CTRL-0661",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release",
        "control_description": "Control operated within Change Management. Mitigates the risk: Risk that production changes are not approved before release. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0662",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation",
        "control_description": "Control operated within Change Management. Mitigates the risk: Risk that emergency changes are not documented post-implementation. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0663",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation",
        "control_description": "Control operated within Change Management. Mitigates the risk: Risk that emergency changes are not documented post-implementation. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0664",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation",
        "control_description": "Control operated within Change Management. Mitigates the risk: Risk that emergency changes are not documented post-implementation. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0665",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that audit findings are not tracked to remediation. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0666",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that production access is not provisioned per least-privilege policy. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0667",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage",
        "control_description": "Governance control providing oversight of Sanctions Program Oversight. Mitigates the risk: Risk that the sanctions screening program has inadequate list coverage. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0668",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that periodic entity-level risk assessments are not completed. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0669",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff",
        "control_description": "Governance control providing oversight of Training & Awareness. Mitigates the risk: Risk that annual AML training is not delivered to in-scope staff. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0670",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that customer data is not protected in transit and at rest. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0671",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage",
        "control_description": "Governance control providing oversight of Sanctions Program Oversight. Mitigates the risk: Risk that the sanctions screening program has inadequate list coverage. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0672",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that Suspicious Activity Reports are not filed within regulatory deadlines. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0673",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that audit findings are not tracked to remediation. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0674",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that periodic entity-level risk assessments are not completed. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0675",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that Suspicious Activity Reports are not filed within regulatory deadlines. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0676",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that Suspicious Activity Reports are not filed within regulatory deadlines. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0677",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that audit findings are not tracked to remediation. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0678",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation",
        "control_description": "Control operated within Change Management. Mitigates the risk: Risk that emergency changes are not documented post-implementation. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0679",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that production access is not provisioned per least-privilege policy. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0680",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that production access is not provisioned per least-privilege policy. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0681",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that customer data is not protected in transit and at rest. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0682",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically",
        "control_description": "Governance control providing oversight of Vendor Performance Monitoring. Mitigates the risk: Risk that vendor SLAs and performance are not monitored periodically. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0683",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff",
        "control_description": "Governance control providing oversight of Training & Awareness. Mitigates the risk: Risk that annual AML training is not delivered to in-scope staff. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0684",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that production access is not provisioned per least-privilege policy. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0685",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation",
        "control_description": "Control operated within Change Management. Mitigates the risk: Risk that emergency changes are not documented post-implementation. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0686",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage",
        "control_description": "Governance control providing oversight of Sanctions Program Oversight. Mitigates the risk: Risk that the sanctions screening program has inadequate list coverage. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-120",
        "description": "Risk that production changes are not approved before release"
      },
      {
        "id": "SR-121",
        "description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "id": "SR-124",
        "description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "id": "SR-118",
        "description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "id": "SR-109",
        "description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "id": "SR-128",
        "description": "Risk that periodic entity-level risk assessments are not completed"
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
        "id": "SR-108",
        "description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "id": "SR-117",
        "description": "Risk that vendor SLAs and performance are not monitored periodically"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-011",
        "description": "Change Management"
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
        "id": "KPA-018",
        "description": "Sanctions Program Oversight"
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
        "id": "KPA-009",
        "description": "Vendor Performance Monitoring"
      }
    ]
  },
  {
    "entity_id": "AE-38",
    "entity_name": "Credit Risk Management",
    "business_unit": "Global Commercial",
    "line_of_defense": "1st Line of Defense",
    "horizontal_flag": true,
    "overview": "This entity covers the credit risk management function.",
    "handoff_description": "Processes are handed off related to credit risk management operations.",
    "handoffs_to": [
      {
        "id": "AE-21",
        "name": "KYC/CDD",
        "inactive_flag": false
      },
      {
        "id": "AE-23",
        "name": "Sanctions Screening",
        "inactive_flag": false
      },
      {
        "id": "AE-39",
        "name": "Market Risk Management",
        "inactive_flag": false
      },
      {
        "id": "AE-2",
        "name": "Commercial Banking",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [
      {
        "id": "AE-25",
        "name": "Dispute Resolution",
        "inactive_flag": false
      },
      {
        "id": "AE-23",
        "name": "Sanctions Screening",
        "inactive_flag": false
      },
      {
        "id": "AE-12",
        "name": "Foreign Exchange",
        "inactive_flag": false
      },
      {
        "id": "AE-16",
        "name": "Retail Banking",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Country",
        "residual_rating": "Critical",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "Critical",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
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
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Security",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "High",
        "inherent_rating": "High",
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
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls": [
      {
        "control_id": "CTRL-0718",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-110",
        "specific_risk_description": "Risk that credit decisioning criteria are not applied at origination",
        "control_description": "Control operated within Credit Origination. Mitigates the risk: Risk that credit decisioning criteria are not applied at origination. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0719",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-110",
        "specific_risk_description": "Risk that credit decisioning criteria are not applied at origination",
        "control_description": "Control operated within Credit Origination. Mitigates the risk: Risk that credit decisioning criteria are not applied at origination. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0720",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-110",
        "specific_risk_description": "Risk that credit decisioning criteria are not applied at origination",
        "control_description": "Control operated within Credit Origination. Mitigates the risk: Risk that credit decisioning criteria are not applied at origination. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0721",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-111",
        "specific_risk_description": "Risk that credit limits are not approved per delegated authority",
        "control_description": "Control operated within Credit Origination. Mitigates the risk: Risk that credit limits are not approved per delegated authority. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0722",
        "control_title": "Program-level oversight of Model Validation",
        "kpa_id": "KPA-013",
        "kpa_description": "Model Validation",
        "specific_risk_id": "SR-123",
        "specific_risk_description": "Risk that model performance is not monitored against thresholds",
        "control_description": "Governance control providing oversight of Model Validation. Mitigates the risk: Risk that model performance is not monitored against thresholds. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0723",
        "control_title": "Program-level oversight of Model Validation",
        "kpa_id": "KPA-013",
        "kpa_description": "Model Validation",
        "specific_risk_id": "SR-123",
        "specific_risk_description": "Risk that model performance is not monitored against thresholds",
        "control_description": "Governance control providing oversight of Model Validation. Mitigates the risk: Risk that model performance is not monitored against thresholds. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0724",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that audit findings are not tracked to remediation. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0725",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that customer data is not protected in transit and at rest. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0726",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained",
        "control_description": "Governance control providing oversight of AML Program Framework. Mitigates the risk: Risk that the AML program framework and policies are not maintained. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0727",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that production access is not provisioned per least-privilege policy. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0728",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that periodic entity-level risk assessments are not completed. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0729",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that transaction monitoring rules are not calibrated against typologies. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0730",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that periodic entity-level risk assessments are not completed. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-110",
        "description": "Risk that credit decisioning criteria are not applied at origination"
      },
      {
        "id": "SR-111",
        "description": "Risk that credit limits are not approved per delegated authority"
      },
      {
        "id": "SR-123",
        "description": "Risk that model performance is not monitored against thresholds"
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
        "id": "SR-105",
        "description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "id": "SR-118",
        "description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "id": "SR-128",
        "description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "id": "SR-107",
        "description": "Risk that transaction monitoring rules are not calibrated against typologies"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-002",
        "description": "Credit Origination"
      },
      {
        "id": "KPA-013",
        "description": "Model Validation"
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
        "id": "KPA-016",
        "description": "AML Program Framework"
      },
      {
        "id": "KPA-017",
        "description": "AML Transaction Monitoring Calibration"
      }
    ]
  },
  {
    "entity_id": "AE-43",
    "entity_name": "Business Continuity",
    "business_unit": "Corporate Functions",
    "line_of_defense": "1st Line of Defense",
    "horizontal_flag": true,
    "overview": "This entity covers the business continuity function.",
    "handoff_description": "Processes are handed off related to business continuity operations.",
    "handoffs_to": [
      {
        "id": "AE-37",
        "name": "Model Validation",
        "inactive_flag": false
      },
      {
        "id": "AE-30",
        "name": "Regulatory Reporting",
        "inactive_flag": false
      },
      {
        "id": "AE-10",
        "name": "Mortgage Servicing",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [
      {
        "id": "AE-22",
        "name": "AML Monitoring",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "Low",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
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
        "residual_rating": "Critical",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "Critical",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls": [
      {
        "control_id": "CTRL-0802",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that production access is not provisioned per least-privilege policy. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0803",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that production access is not provisioned per least-privilege policy. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0804",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that production access is not provisioned per least-privilege policy. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0805",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that user access is not recertified on the required cadence. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0806",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release",
        "control_description": "Control operated within Change Management. Mitigates the risk: Risk that production changes are not approved before release. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0807",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation",
        "control_description": "Control operated within Change Management. Mitigates the risk: Risk that emergency changes are not documented post-implementation. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0808",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation",
        "control_description": "Control operated within Change Management. Mitigates the risk: Risk that emergency changes are not documented post-implementation. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0809",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that periodic entity-level risk assessments are not completed. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0810",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that periodic entity-level risk assessments are not completed. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0811",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that audit findings are not tracked to remediation. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0812",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that audit findings are not tracked to remediation. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0813",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that audit findings are not tracked to remediation. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0814",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy",
        "control_description": "Governance control providing oversight of Vendor Due Diligence. Mitigates the risk: Risk that vendors are not onboarded per Third Party Risk policy. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0815",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that Suspicious Activity Reports are not filed within regulatory deadlines. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0816",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that periodic entity-level risk assessments are not completed. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0817",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy",
        "control_description": "Governance control providing oversight of Vendor Due Diligence. Mitigates the risk: Risk that vendors are not onboarded per Third Party Risk policy. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0818",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that periodic entity-level risk assessments are not completed. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0819",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically",
        "control_description": "Governance control providing oversight of Vendor Performance Monitoring. Mitigates the risk: Risk that vendor SLAs and performance are not monitored periodically. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0820",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained",
        "control_description": "Governance control providing oversight of AML Program Framework. Mitigates the risk: Risk that the AML program framework and policies are not maintained. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-118",
        "description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "id": "SR-119",
        "description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "id": "SR-120",
        "description": "Risk that production changes are not approved before release"
      },
      {
        "id": "SR-121",
        "description": "Risk that emergency changes are not documented post-implementation"
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
        "id": "SR-116",
        "description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "id": "SR-108",
        "description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "id": "SR-117",
        "description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "id": "SR-105",
        "description": "Risk that the AML program framework and policies are not maintained"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-010",
        "description": "Access Management"
      },
      {
        "id": "KPA-011",
        "description": "Change Management"
      },
      {
        "id": "KPA-014",
        "description": "Issue Management"
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
        "id": "KPA-009",
        "description": "Vendor Performance Monitoring"
      },
      {
        "id": "KPA-016",
        "description": "AML Program Framework"
      }
    ]
  },
  {
    "entity_id": "AE-5",
    "entity_name": "Wire Transfers",
    "business_unit": "Risk & Compliance",
    "line_of_defense": "1st Line of Defense",
    "horizontal_flag": false,
    "overview": "This entity covers the wire transfers function.",
    "handoff_description": "Processes are handed off related to wire transfers operations.",
    "handoffs_to": [],
    "handoffs_from": [],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Technology",
        "residual_rating": "Medium",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
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
        "residual_rating": "Low",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "Medium",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "Low",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls": [
      {
        "control_id": "CTRL-0071",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-112",
        "specific_risk_description": "Risk that payment instructions are not authorized before release",
        "control_description": "Control operated within Payment Authorization. Mitigates the risk: Risk that payment instructions are not authorized before release. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0072",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-112",
        "specific_risk_description": "Risk that payment instructions are not authorized before release",
        "control_description": "Control operated within Payment Authorization. Mitigates the risk: Risk that payment instructions are not authorized before release. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0073",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-112",
        "specific_risk_description": "Risk that payment instructions are not authorized before release",
        "control_description": "Control operated within Payment Authorization. Mitigates the risk: Risk that payment instructions are not authorized before release. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0074",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-113",
        "specific_risk_description": "Risk that daily payment reconciliations are not completed and reviewed",
        "control_description": "Control operated within Payment Authorization. Mitigates the risk: Risk that daily payment reconciliations are not completed and reviewed. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0075",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-113",
        "specific_risk_description": "Risk that daily payment reconciliations are not completed and reviewed",
        "control_description": "Control operated within Payment Authorization. Mitigates the risk: Risk that daily payment reconciliations are not completed and reviewed. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0076",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-112",
        "specific_risk_description": "Risk that payment instructions are not authorized before release",
        "control_description": "Control operated within Payment Authorization. Mitigates the risk: Risk that payment instructions are not authorized before release. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0077",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that user access is not recertified on the required cadence. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0078",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage",
        "control_description": "Governance control providing oversight of Sanctions Program Oversight. Mitigates the risk: Risk that the sanctions screening program has inadequate list coverage. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0079",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that customer data is not protected in transit and at rest. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0080",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that audit findings are not tracked to remediation. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0081",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff",
        "control_description": "Governance control providing oversight of Training & Awareness. Mitigates the risk: Risk that annual AML training is not delivered to in-scope staff. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0082",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that transaction monitoring rules are not calibrated against typologies. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0083",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that user access is not recertified on the required cadence. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-112",
        "description": "Risk that payment instructions are not authorized before release"
      },
      {
        "id": "SR-113",
        "description": "Risk that daily payment reconciliations are not completed and reviewed"
      },
      {
        "id": "SR-119",
        "description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "id": "SR-109",
        "description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "id": "SR-130",
        "description": "Risk that customer data is not protected in transit and at rest"
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
        "id": "SR-107",
        "description": "Risk that transaction monitoring rules are not calibrated against typologies"
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
        "id": "KPA-018",
        "description": "Sanctions Program Oversight"
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
        "id": "KPA-017",
        "description": "AML Transaction Monitoring Calibration"
      }
    ]
  },
  {
    "entity_id": "AE-9",
    "entity_name": "Mortgage Origination",
    "business_unit": "Technology",
    "line_of_defense": "2nd Line of Defense",
    "horizontal_flag": false,
    "overview": "This entity covers the mortgage origination function.",
    "handoff_description": "Processes are handed off related to mortgage origination operations.",
    "handoffs_to": [
      {
        "id": "AE-33",
        "name": "Data Governance",
        "inactive_flag": false
      },
      {
        "id": "AE-5",
        "name": "Wire Transfers",
        "inactive_flag": false
      },
      {
        "id": "AE-38",
        "name": "Credit Risk Management",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "Critical",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
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
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Funding & Liquidity",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Technology",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Security",
        "residual_rating": "Low",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "Critical",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "Low",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "Critical",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "Critical",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls": [
      {
        "control_id": "CTRL-0152",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-110",
        "specific_risk_description": "Risk that credit decisioning criteria are not applied at origination",
        "control_description": "Control operated within Credit Origination. Mitigates the risk: Risk that credit decisioning criteria are not applied at origination. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0153",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-110",
        "specific_risk_description": "Risk that credit decisioning criteria are not applied at origination",
        "control_description": "Control operated within Credit Origination. Mitigates the risk: Risk that credit decisioning criteria are not applied at origination. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0154",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-111",
        "specific_risk_description": "Risk that credit limits are not approved per delegated authority",
        "control_description": "Control operated within Credit Origination. Mitigates the risk: Risk that credit limits are not approved per delegated authority. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0155",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-111",
        "specific_risk_description": "Risk that credit limits are not approved per delegated authority",
        "control_description": "Control operated within Credit Origination. Mitigates the risk: Risk that credit limits are not approved per delegated authority. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0156",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that production access is not provisioned per least-privilege policy. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0157",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that production access is not provisioned per least-privilege policy. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0158",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained",
        "control_description": "Governance control providing oversight of AML Program Framework. Mitigates the risk: Risk that the AML program framework and policies are not maintained. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0159",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation",
        "control_description": "Control operated within Change Management. Mitigates the risk: Risk that emergency changes are not documented post-implementation. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0160",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that production access is not provisioned per least-privilege policy. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0161",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-102",
        "specific_risk_description": "Risk that Customer Due Diligence is not refreshed per policy cadence",
        "control_description": "Control operated within Customer Onboarding. Mitigates the risk: Risk that Customer Due Diligence is not refreshed per policy cadence. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0162",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that Suspicious Activity Reports are not filed within regulatory deadlines. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0163",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-103",
        "specific_risk_description": "Risk that sanctions screening is not performed at customer onboarding",
        "control_description": "Control operated within Customer Onboarding. Mitigates the risk: Risk that sanctions screening is not performed at customer onboarding. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0164",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that Suspicious Activity Reports are not filed within regulatory deadlines. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0165",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release",
        "control_description": "Control operated within Change Management. Mitigates the risk: Risk that production changes are not approved before release. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0166",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies",
        "control_description": "Governance control providing oversight of AML Transaction Monitoring Calibration. Mitigates the risk: Risk that transaction monitoring rules are not calibrated against typologies. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0167",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained",
        "control_description": "Governance control providing oversight of AML Program Framework. Mitigates the risk: Risk that the AML program framework and policies are not maintained. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0168",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy",
        "control_description": "Governance control providing oversight of Vendor Due Diligence. Mitigates the risk: Risk that vendors are not onboarded per Third Party Risk policy. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0169",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-102",
        "specific_risk_description": "Risk that Customer Due Diligence is not refreshed per policy cadence",
        "control_description": "Control operated within Customer Onboarding. Mitigates the risk: Risk that Customer Due Diligence is not refreshed per policy cadence. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0170",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained",
        "control_description": "Governance control providing oversight of AML Program Framework. Mitigates the risk: Risk that the AML program framework and policies are not maintained. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0171",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-101",
        "specific_risk_description": "Risk that KYC identity verification is not performed at customer onboarding",
        "control_description": "Control operated within Customer Onboarding. Mitigates the risk: Risk that KYC identity verification is not performed at customer onboarding. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0172",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest",
        "control_description": "Control operated within Access Management. Mitigates the risk: Risk that customer data is not protected in transit and at rest. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0173",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff",
        "control_description": "Governance control providing oversight of Training & Awareness. Mitigates the risk: Risk that annual AML training is not delivered to in-scope staff. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0174",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed",
        "control_description": "Governance control providing oversight of Issue Management. Mitigates the risk: Risk that periodic entity-level risk assessments are not completed. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0175",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained",
        "control_description": "Governance control providing oversight of AML Program Framework. Mitigates the risk: Risk that the AML program framework and policies are not maintained. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0176",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically",
        "control_description": "Governance control providing oversight of Vendor Performance Monitoring. Mitigates the risk: Risk that vendor SLAs and performance are not monitored periodically. Evidence is produced at the program or framework level and is reviewed by second-line governance on a defined cadence."
      },
      {
        "control_id": "CTRL-0177",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-101",
        "specific_risk_description": "Risk that KYC identity verification is not performed at customer onboarding",
        "control_description": "Control operated within Customer Onboarding. Mitigates the risk: Risk that KYC identity verification is not performed at customer onboarding. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      },
      {
        "control_id": "CTRL-0178",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-103",
        "specific_risk_description": "Risk that sanctions screening is not performed at customer onboarding",
        "control_description": "Control operated within Customer Onboarding. Mitigates the risk: Risk that sanctions screening is not performed at customer onboarding. Evidence is retained per the control operator's workpapers and is executed at the transaction or event level."
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-110",
        "description": "Risk that credit decisioning criteria are not applied at origination"
      },
      {
        "id": "SR-111",
        "description": "Risk that credit limits are not approved per delegated authority"
      },
      {
        "id": "SR-118",
        "description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "id": "SR-105",
        "description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "id": "SR-121",
        "description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "id": "SR-102",
        "description": "Risk that Customer Due Diligence is not refreshed per policy cadence"
      },
      {
        "id": "SR-108",
        "description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "id": "SR-103",
        "description": "Risk that sanctions screening is not performed at customer onboarding"
      },
      {
        "id": "SR-120",
        "description": "Risk that production changes are not approved before release"
      },
      {
        "id": "SR-107",
        "description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "id": "SR-116",
        "description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "id": "SR-101",
        "description": "Risk that KYC identity verification is not performed at customer onboarding"
      },
      {
        "id": "SR-130",
        "description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "id": "SR-106",
        "description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "id": "SR-128",
        "description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "id": "SR-117",
        "description": "Risk that vendor SLAs and performance are not monitored periodically"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-002",
        "description": "Credit Origination"
      },
      {
        "id": "KPA-010",
        "description": "Access Management"
      },
      {
        "id": "KPA-016",
        "description": "AML Program Framework"
      },
      {
        "id": "KPA-011",
        "description": "Change Management"
      },
      {
        "id": "KPA-001",
        "description": "Customer Onboarding"
      },
      {
        "id": "KPA-017",
        "description": "AML Transaction Monitoring Calibration"
      },
      {
        "id": "KPA-008",
        "description": "Vendor Due Diligence"
      },
      {
        "id": "KPA-020",
        "description": "Training & Awareness"
      },
      {
        "id": "KPA-014",
        "description": "Issue Management"
      },
      {
        "id": "KPA-009",
        "description": "Vendor Performance Monitoring"
      }
    ]
  }
]
```

## Target-context entities (handoff targets — reference for Task 5; do not produce findings about them)

```json
[
  {
    "entity_id": "AE-1",
    "entity_name": "Consumer Lending",
    "business_unit": "Global Consumer",
    "line_of_defense": "1st Line of Defense",
    "role": "target_context",
    "horizontal_flag": false,
    "handoff_description": "Processes are handed off related to consumer lending operations.",
    "handoffs_to": [
      {
        "id": "AE-19",
        "name": "Branch Operations",
        "inactive_flag": false
      },
      {
        "id": "AE-45",
        "name": "Facilities Management",
        "inactive_flag": false
      },
      {
        "id": "AE-43",
        "name": "Business Continuity",
        "inactive_flag": false
      },
      {
        "id": "AE-6",
        "name": "ACH Processing",
        "inactive_flag": false
      },
      {
        "id": "AE-40",
        "name": "Operational Risk",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [
      {
        "id": "AE-24",
        "name": "Fraud Detection",
        "inactive_flag": false
      },
      {
        "id": "AE-15",
        "name": "Asset Management",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "Critical",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "Critical",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
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
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Security",
        "residual_rating": "Medium",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
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
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
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
        "control_id": "CTRL-0001",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-110",
        "specific_risk_description": "Risk that credit decisioning criteria are not applied at origination"
      },
      {
        "control_id": "CTRL-0002",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-111",
        "specific_risk_description": "Risk that credit limits are not approved per delegated authority"
      },
      {
        "control_id": "CTRL-0003",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-111",
        "specific_risk_description": "Risk that credit limits are not approved per delegated authority"
      },
      {
        "control_id": "CTRL-0004",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged"
      },
      {
        "control_id": "CTRL-0005",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged"
      },
      {
        "control_id": "CTRL-0006",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged"
      },
      {
        "control_id": "CTRL-0007",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-102",
        "specific_risk_description": "Risk that Customer Due Diligence is not refreshed per policy cadence"
      },
      {
        "control_id": "CTRL-0008",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-103",
        "specific_risk_description": "Risk that sanctions screening is not performed at customer onboarding"
      },
      {
        "control_id": "CTRL-0009",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0010",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "control_id": "CTRL-0011",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0012",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged"
      },
      {
        "control_id": "CTRL-0013",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-102",
        "specific_risk_description": "Risk that Customer Due Diligence is not refreshed per policy cadence"
      },
      {
        "control_id": "CTRL-0014",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "control_id": "CTRL-0015",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "control_id": "CTRL-0016",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-102",
        "specific_risk_description": "Risk that Customer Due Diligence is not refreshed per policy cadence"
      },
      {
        "control_id": "CTRL-0017",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-103",
        "specific_risk_description": "Risk that sanctions screening is not performed at customer onboarding"
      },
      {
        "control_id": "CTRL-0018",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0019",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0020",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-103",
        "specific_risk_description": "Risk that sanctions screening is not performed at customer onboarding"
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-110",
        "description": "Risk that credit decisioning criteria are not applied at origination"
      },
      {
        "id": "SR-111",
        "description": "Risk that credit limits are not approved per delegated authority"
      },
      {
        "id": "SR-129",
        "description": "Risk that customer complaints are not logged and triaged"
      },
      {
        "id": "SR-102",
        "description": "Risk that Customer Due Diligence is not refreshed per policy cadence"
      },
      {
        "id": "SR-103",
        "description": "Risk that sanctions screening is not performed at customer onboarding"
      },
      {
        "id": "SR-128",
        "description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "id": "SR-105",
        "description": "Risk that the AML program framework and policies are not maintained"
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
        "id": "SR-108",
        "description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "id": "SR-119",
        "description": "Risk that user access is not recertified on the required cadence"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-002",
        "description": "Credit Origination"
      },
      {
        "id": "KPA-005",
        "description": "Account Servicing"
      },
      {
        "id": "KPA-001",
        "description": "Customer Onboarding"
      },
      {
        "id": "KPA-014",
        "description": "Issue Management"
      },
      {
        "id": "KPA-016",
        "description": "AML Program Framework"
      },
      {
        "id": "KPA-009",
        "description": "Vendor Performance Monitoring"
      },
      {
        "id": "KPA-017",
        "description": "AML Transaction Monitoring Calibration"
      },
      {
        "id": "KPA-010",
        "description": "Access Management"
      }
    ]
  },
  {
    "entity_id": "AE-10",
    "entity_name": "Mortgage Servicing",
    "business_unit": "Global Consumer",
    "line_of_defense": "1st Line of Defense",
    "role": "target_context",
    "horizontal_flag": false,
    "handoff_description": "Processes are handed off related to mortgage servicing operations.",
    "handoffs_to": [
      {
        "id": "AE-42",
        "name": "Internal Controls",
        "inactive_flag": false
      },
      {
        "id": "AE-33",
        "name": "Data Governance",
        "inactive_flag": false
      },
      {
        "id": "AE-6",
        "name": "ACH Processing",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [
      {
        "id": "AE-39",
        "name": "Market Risk Management",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "High",
        "inherent_rating": "Medium",
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
        "residual_rating": "Low",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
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
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Technology",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Security",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "Low",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "Critical",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "Critical",
        "inherent_rating": "Critical",
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
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0179",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged"
      },
      {
        "control_id": "CTRL-0180",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged"
      },
      {
        "control_id": "CTRL-0181",
        "control_title": "Operating control over Account Servicing",
        "kpa_id": "KPA-005",
        "kpa_description": "Account Servicing",
        "specific_risk_id": "SR-129",
        "specific_risk_description": "Risk that customer complaints are not logged and triaged"
      },
      {
        "control_id": "CTRL-0182",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0183",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0184",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-110",
        "specific_risk_description": "Risk that credit decisioning criteria are not applied at origination"
      },
      {
        "control_id": "CTRL-0185",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0186",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0187",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0188",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0189",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "control_id": "CTRL-0190",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "control_id": "CTRL-0191",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0192",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0193",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0194",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-129",
        "description": "Risk that customer complaints are not logged and triaged"
      },
      {
        "id": "SR-118",
        "description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "id": "SR-106",
        "description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "id": "SR-110",
        "description": "Risk that credit decisioning criteria are not applied at origination"
      },
      {
        "id": "SR-117",
        "description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "id": "SR-130",
        "description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "id": "SR-121",
        "description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "id": "SR-105",
        "description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "id": "SR-120",
        "description": "Risk that production changes are not approved before release"
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
        "id": "KPA-020",
        "description": "Training & Awareness"
      },
      {
        "id": "KPA-002",
        "description": "Credit Origination"
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
        "id": "KPA-016",
        "description": "AML Program Framework"
      }
    ]
  },
  {
    "entity_id": "AE-11",
    "entity_name": "Trade Finance",
    "business_unit": "Operations",
    "line_of_defense": "1st Line of Defense",
    "role": "target_context",
    "horizontal_flag": false,
    "handoff_description": "Processes are handed off related to trade finance operations.",
    "handoffs_to": [
      {
        "id": "AE-26",
        "name": "Payroll Processing",
        "inactive_flag": false
      },
      {
        "id": "AE-31",
        "name": "IT Infrastructure",
        "inactive_flag": false
      },
      {
        "id": "AE-22",
        "name": "AML Monitoring",
        "inactive_flag": false
      },
      {
        "id": "AE-14",
        "name": "Investment Banking",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [
      {
        "id": "AE-23",
        "name": "Sanctions Screening",
        "inactive_flag": false
      },
      {
        "id": "AE-37",
        "name": "Model Validation",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "Critical",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "Critical",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "Critical",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "Critical",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Funding & Liquidity",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Technology",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
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
        "risk_category": "Model",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
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
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
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
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0195",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "control_id": "CTRL-0196",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "control_id": "CTRL-0197",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "control_id": "CTRL-0198",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0199",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0200",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0201",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-110",
        "specific_risk_description": "Risk that credit decisioning criteria are not applied at origination"
      },
      {
        "control_id": "CTRL-0202",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "control_id": "CTRL-0203",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-111",
        "specific_risk_description": "Risk that credit limits are not approved per delegated authority"
      },
      {
        "control_id": "CTRL-0204",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0205",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "control_id": "CTRL-0206",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "control_id": "CTRL-0207",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0208",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "control_id": "CTRL-0209",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0210",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0211",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-110",
        "specific_risk_description": "Risk that credit decisioning criteria are not applied at origination"
      },
      {
        "control_id": "CTRL-0212",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0213",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy"
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-109",
        "description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "id": "SR-108",
        "description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "id": "SR-119",
        "description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "id": "SR-117",
        "description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "id": "SR-130",
        "description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "id": "SR-110",
        "description": "Risk that credit decisioning criteria are not applied at origination"
      },
      {
        "id": "SR-105",
        "description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "id": "SR-111",
        "description": "Risk that credit limits are not approved per delegated authority"
      },
      {
        "id": "SR-120",
        "description": "Risk that production changes are not approved before release"
      },
      {
        "id": "SR-118",
        "description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "id": "SR-107",
        "description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "id": "SR-116",
        "description": "Risk that vendors are not onboarded per Third Party Risk policy"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-018",
        "description": "Sanctions Program Oversight"
      },
      {
        "id": "KPA-017",
        "description": "AML Transaction Monitoring Calibration"
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
        "id": "KPA-002",
        "description": "Credit Origination"
      },
      {
        "id": "KPA-016",
        "description": "AML Program Framework"
      },
      {
        "id": "KPA-011",
        "description": "Change Management"
      },
      {
        "id": "KPA-008",
        "description": "Vendor Due Diligence"
      }
    ]
  },
  {
    "entity_id": "AE-15",
    "entity_name": "Asset Management",
    "business_unit": "Global Consumer",
    "line_of_defense": "2nd Line of Defense",
    "role": "target_context",
    "horizontal_flag": false,
    "handoff_description": "Processes are handed off related to asset management operations.",
    "handoffs_to": [
      {
        "id": "AE-21",
        "name": "KYC/CDD",
        "inactive_flag": false
      },
      {
        "id": "AE-23",
        "name": "Sanctions Screening",
        "inactive_flag": false
      },
      {
        "id": "AE-24",
        "name": "Fraud Detection",
        "inactive_flag": false
      },
      {
        "id": "AE-1",
        "name": "Consumer Lending",
        "inactive_flag": false
      },
      {
        "id": "AE-12",
        "name": "Foreign Exchange",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [
      {
        "id": "AE-19",
        "name": "Branch Operations",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "Low",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
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
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Funding & Liquidity",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Technology",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Security",
        "residual_rating": "Low",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "Medium",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "Low",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0279",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0280",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "control_id": "CTRL-0281",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0282",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0283",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "control_id": "CTRL-0284",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0285",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0286",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0287",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0288",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy"
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-117",
        "description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "id": "SR-124",
        "description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "id": "SR-121",
        "description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "id": "SR-120",
        "description": "Risk that production changes are not approved before release"
      },
      {
        "id": "SR-105",
        "description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "id": "SR-118",
        "description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "id": "SR-130",
        "description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "id": "SR-106",
        "description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "id": "SR-116",
        "description": "Risk that vendors are not onboarded per Third Party Risk policy"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-009",
        "description": "Vendor Performance Monitoring"
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
        "id": "KPA-016",
        "description": "AML Program Framework"
      },
      {
        "id": "KPA-010",
        "description": "Access Management"
      },
      {
        "id": "KPA-020",
        "description": "Training & Awareness"
      },
      {
        "id": "KPA-008",
        "description": "Vendor Due Diligence"
      }
    ]
  },
  {
    "entity_id": "AE-2",
    "entity_name": "Commercial Banking",
    "business_unit": "Global Consumer",
    "line_of_defense": "2nd Line of Defense",
    "role": "target_context",
    "horizontal_flag": false,
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
        "risk_category": "Country",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
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
        "risk_category": "Information Technology",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
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
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
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
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0021",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "control_id": "CTRL-0022",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "control_id": "CTRL-0023",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0024",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "control_id": "CTRL-0025",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "control_id": "CTRL-0026",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0027",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0028",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0029",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "control_id": "CTRL-0030",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0031",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "control_id": "CTRL-0032",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0033",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "control_id": "CTRL-0034",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "control_id": "CTRL-0035",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "control_id": "CTRL-0036",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0037",
        "control_title": "Operating control over Credit Origination",
        "kpa_id": "KPA-002",
        "kpa_description": "Credit Origination",
        "specific_risk_id": "SR-110",
        "specific_risk_description": "Risk that credit decisioning criteria are not applied at origination"
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
    "entity_id": "AE-21",
    "entity_name": "KYC/CDD",
    "business_unit": "Technology",
    "line_of_defense": "1st Line of Defense",
    "role": "target_context",
    "horizontal_flag": true,
    "handoff_description": "Processes are handed off related to kyc/cdd operations.",
    "handoffs_to": [
      {
        "id": "AE-19",
        "name": "Branch Operations",
        "inactive_flag": false
      },
      {
        "id": "AE-6",
        "name": "ACH Processing",
        "inactive_flag": false
      },
      {
        "id": "AE-17",
        "name": "Digital Banking",
        "inactive_flag": false
      },
      {
        "id": "AE-13",
        "name": "Capital Markets",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [
      {
        "id": "AE-24",
        "name": "Fraud Detection",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "Low",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "Critical",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Funding & Liquidity",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Technology",
        "residual_rating": "Low",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Security",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "Medium",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
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
        "residual_rating": "Medium",
        "inherent_rating": "Low",
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
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0385",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-101",
        "specific_risk_description": "Risk that KYC identity verification is not performed at customer onboarding"
      },
      {
        "control_id": "CTRL-0386",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-102",
        "specific_risk_description": "Risk that Customer Due Diligence is not refreshed per policy cadence"
      },
      {
        "control_id": "CTRL-0387",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-102",
        "specific_risk_description": "Risk that Customer Due Diligence is not refreshed per policy cadence"
      },
      {
        "control_id": "CTRL-0388",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-102",
        "specific_risk_description": "Risk that Customer Due Diligence is not refreshed per policy cadence"
      },
      {
        "control_id": "CTRL-0389",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-103",
        "specific_risk_description": "Risk that sanctions screening is not performed at customer onboarding"
      },
      {
        "control_id": "CTRL-0390",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-103",
        "specific_risk_description": "Risk that sanctions screening is not performed at customer onboarding"
      },
      {
        "control_id": "CTRL-0391",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-103",
        "specific_risk_description": "Risk that sanctions screening is not performed at customer onboarding"
      },
      {
        "control_id": "CTRL-0392",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-104",
        "specific_risk_description": "Risk that enhanced due diligence is not completed for high-risk customers"
      },
      {
        "control_id": "CTRL-0393",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-104",
        "specific_risk_description": "Risk that enhanced due diligence is not completed for high-risk customers"
      },
      {
        "control_id": "CTRL-0394",
        "control_title": "Operating control over Customer Onboarding",
        "kpa_id": "KPA-001",
        "kpa_description": "Customer Onboarding",
        "specific_risk_id": "SR-104",
        "specific_risk_description": "Risk that enhanced due diligence is not completed for high-risk customers"
      },
      {
        "control_id": "CTRL-0395",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0396",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "control_id": "CTRL-0397",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage"
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-101",
        "description": "Risk that KYC identity verification is not performed at customer onboarding"
      },
      {
        "id": "SR-102",
        "description": "Risk that Customer Due Diligence is not refreshed per policy cadence"
      },
      {
        "id": "SR-103",
        "description": "Risk that sanctions screening is not performed at customer onboarding"
      },
      {
        "id": "SR-104",
        "description": "Risk that enhanced due diligence is not completed for high-risk customers"
      },
      {
        "id": "SR-118",
        "description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "id": "SR-105",
        "description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "id": "SR-109",
        "description": "Risk that the sanctions screening program has inadequate list coverage"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-001",
        "description": "Customer Onboarding"
      },
      {
        "id": "KPA-010",
        "description": "Access Management"
      },
      {
        "id": "KPA-016",
        "description": "AML Program Framework"
      },
      {
        "id": "KPA-018",
        "description": "Sanctions Program Oversight"
      }
    ]
  },
  {
    "entity_id": "AE-22",
    "entity_name": "AML Monitoring",
    "business_unit": "Operations",
    "line_of_defense": "1st Line of Defense",
    "role": "target_context",
    "horizontal_flag": true,
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
        "risk_category": "Compliance",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
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
        "risk_category": "Funding & Liquidity",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Technology",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
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
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0398",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "control_id": "CTRL-0399",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "control_id": "CTRL-0400",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0401",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "control_id": "CTRL-0402",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "control_id": "CTRL-0403",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "control_id": "CTRL-0404",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "control_id": "CTRL-0405",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "control_id": "CTRL-0406",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "control_id": "CTRL-0407",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0408",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "control_id": "CTRL-0409",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0410",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0411",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
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
    "entity_id": "AE-25",
    "entity_name": "Dispute Resolution",
    "business_unit": "Technology",
    "line_of_defense": "2nd Line of Defense",
    "role": "target_context",
    "horizontal_flag": false,
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
    ],
    "handoffs_from": [
      {
        "id": "AE-31",
        "name": "IT Infrastructure",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "Low",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "Medium",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Funding & Liquidity",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Technology",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Security",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0447",
        "control_title": "Operating control over Fraud Case Management",
        "kpa_id": "KPA-019",
        "kpa_description": "Fraud Case Management",
        "specific_risk_id": "SR-126",
        "specific_risk_description": "Risk that fraud cases are not investigated and closed"
      },
      {
        "control_id": "CTRL-0448",
        "control_title": "Operating control over Fraud Case Management",
        "kpa_id": "KPA-019",
        "kpa_description": "Fraud Case Management",
        "specific_risk_id": "SR-126",
        "specific_risk_description": "Risk that fraud cases are not investigated and closed"
      },
      {
        "control_id": "CTRL-0449",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0450",
        "control_title": "Operating control over Fraud Case Management",
        "kpa_id": "KPA-019",
        "kpa_description": "Fraud Case Management",
        "specific_risk_id": "SR-126",
        "specific_risk_description": "Risk that fraud cases are not investigated and closed"
      },
      {
        "control_id": "CTRL-0451",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "control_id": "CTRL-0452",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0453",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0454",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "control_id": "CTRL-0455",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0456",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0457",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "control_id": "CTRL-0458",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0459",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "control_id": "CTRL-0460",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-126",
        "description": "Risk that fraud cases are not investigated and closed"
      },
      {
        "id": "SR-119",
        "description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "id": "SR-109",
        "description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "id": "SR-130",
        "description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "id": "SR-121",
        "description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "id": "SR-107",
        "description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "id": "SR-106",
        "description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "id": "SR-116",
        "description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "id": "SR-128",
        "description": "Risk that periodic entity-level risk assessments are not completed"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-019",
        "description": "Fraud Case Management"
      },
      {
        "id": "KPA-010",
        "description": "Access Management"
      },
      {
        "id": "KPA-018",
        "description": "Sanctions Program Oversight"
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
      },
      {
        "id": "KPA-008",
        "description": "Vendor Due Diligence"
      },
      {
        "id": "KPA-014",
        "description": "Issue Management"
      }
    ]
  },
  {
    "entity_id": "AE-27",
    "entity_name": "Accounts Payable",
    "business_unit": "Operations",
    "line_of_defense": "1st Line of Defense",
    "role": "target_context",
    "horizontal_flag": false,
    "handoff_description": "Processes are handed off related to accounts payable operations.",
    "handoffs_to": [
      {
        "id": "AE-16",
        "name": "Retail Banking",
        "inactive_flag": false
      },
      {
        "id": "AE-37",
        "name": "Model Validation",
        "inactive_flag": false
      },
      {
        "id": "AE-21",
        "name": "KYC/CDD",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [
      {
        "id": "AE-16",
        "name": "Retail Banking",
        "inactive_flag": false
      },
      {
        "id": "AE-40",
        "name": "Operational Risk",
        "inactive_flag": false
      },
      {
        "id": "AE-14",
        "name": "Investment Banking",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "Low",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
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
        "residual_rating": "Critical",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Funding & Liquidity",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Technology",
        "residual_rating": "Critical",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Security",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "Low",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0471",
        "control_title": "Operating control over Financial Reporting — Period Close",
        "kpa_id": "KPA-006",
        "kpa_description": "Financial Reporting — Period Close",
        "specific_risk_id": "SR-114",
        "specific_risk_description": "Risk that period-end financial statements contain material misstatement"
      },
      {
        "control_id": "CTRL-0472",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0473",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0474",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "control_id": "CTRL-0475",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "control_id": "CTRL-0476",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0477",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0478",
        "control_title": "Operating control over Financial Reporting — Period Close",
        "kpa_id": "KPA-006",
        "kpa_description": "Financial Reporting — Period Close",
        "specific_risk_id": "SR-114",
        "specific_risk_description": "Risk that period-end financial statements contain material misstatement"
      },
      {
        "control_id": "CTRL-0479",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "control_id": "CTRL-0480",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-112",
        "specific_risk_description": "Risk that payment instructions are not authorized before release"
      },
      {
        "control_id": "CTRL-0481",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "control_id": "CTRL-0482",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0483",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-112",
        "specific_risk_description": "Risk that payment instructions are not authorized before release"
      },
      {
        "control_id": "CTRL-0484",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-113",
        "specific_risk_description": "Risk that daily payment reconciliations are not completed and reviewed"
      },
      {
        "control_id": "CTRL-0485",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0486",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0487",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0488",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-113",
        "specific_risk_description": "Risk that daily payment reconciliations are not completed and reviewed"
      },
      {
        "control_id": "CTRL-0489",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0490",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "control_id": "CTRL-0491",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0492",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-112",
        "specific_risk_description": "Risk that payment instructions are not authorized before release"
      },
      {
        "control_id": "CTRL-0493",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "control_id": "CTRL-0494",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-114",
        "description": "Risk that period-end financial statements contain material misstatement"
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
        "id": "SR-116",
        "description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "id": "SR-109",
        "description": "Risk that the sanctions screening program has inadequate list coverage"
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
        "id": "SR-108",
        "description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "id": "SR-112",
        "description": "Risk that payment instructions are not authorized before release"
      },
      {
        "id": "SR-113",
        "description": "Risk that daily payment reconciliations are not completed and reviewed"
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
        "id": "SR-119",
        "description": "Risk that user access is not recertified on the required cadence"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-006",
        "description": "Financial Reporting — Period Close"
      },
      {
        "id": "KPA-010",
        "description": "Access Management"
      },
      {
        "id": "KPA-011",
        "description": "Change Management"
      },
      {
        "id": "KPA-008",
        "description": "Vendor Due Diligence"
      },
      {
        "id": "KPA-018",
        "description": "Sanctions Program Oversight"
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
        "id": "KPA-004",
        "description": "Payment Authorization"
      },
      {
        "id": "KPA-009",
        "description": "Vendor Performance Monitoring"
      },
      {
        "id": "KPA-014",
        "description": "Issue Management"
      }
    ]
  },
  {
    "entity_id": "AE-30",
    "entity_name": "Regulatory Reporting",
    "business_unit": "Technology",
    "line_of_defense": "2nd Line of Defense",
    "role": "target_context",
    "horizontal_flag": false,
    "handoff_description": "Processes are handed off related to regulatory reporting operations.",
    "handoffs_to": [
      {
        "id": "AE-5",
        "name": "Wire Transfers",
        "inactive_flag": false
      },
      {
        "id": "AE-27",
        "name": "Accounts Payable",
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
        "id": "AE-31",
        "name": "IT Infrastructure",
        "inactive_flag": false
      },
      {
        "id": "AE-14",
        "name": "Investment Banking",
        "inactive_flag": false
      },
      {
        "id": "AE-29",
        "name": "Financial Reporting",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "Low",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "Critical",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "Medium",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Funding & Liquidity",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
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
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0535",
        "control_title": "Operating control over Regulatory Reporting",
        "kpa_id": "KPA-015",
        "kpa_description": "Regulatory Reporting",
        "specific_risk_id": "SR-125",
        "specific_risk_description": "Risk that regulatory reports are not filed by required deadlines"
      },
      {
        "control_id": "CTRL-0536",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0537",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0538",
        "control_title": "Operating control over Financial Reporting — Period Close",
        "kpa_id": "KPA-006",
        "kpa_description": "Financial Reporting — Period Close",
        "specific_risk_id": "SR-114",
        "specific_risk_description": "Risk that period-end financial statements contain material misstatement"
      },
      {
        "control_id": "CTRL-0539",
        "control_title": "Operating control over Financial Reporting — Period Close",
        "kpa_id": "KPA-006",
        "kpa_description": "Financial Reporting — Period Close",
        "specific_risk_id": "SR-114",
        "specific_risk_description": "Risk that period-end financial statements contain material misstatement"
      },
      {
        "control_id": "CTRL-0540",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0541",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0542",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "control_id": "CTRL-0543",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0544",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0545",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0546",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0547",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0548",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0549",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0550",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "control_id": "CTRL-0551",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0552",
        "control_title": "Operating control over Financial Reporting — Period Close",
        "kpa_id": "KPA-006",
        "kpa_description": "Financial Reporting — Period Close",
        "specific_risk_id": "SR-114",
        "specific_risk_description": "Risk that period-end financial statements contain material misstatement"
      },
      {
        "control_id": "CTRL-0553",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained"
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-125",
        "description": "Risk that regulatory reports are not filed by required deadlines"
      },
      {
        "id": "SR-128",
        "description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "id": "SR-114",
        "description": "Risk that period-end financial statements contain material misstatement"
      },
      {
        "id": "SR-118",
        "description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "id": "SR-105",
        "description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "id": "SR-121",
        "description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "id": "SR-120",
        "description": "Risk that production changes are not approved before release"
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
        "id": "SR-119",
        "description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "id": "SR-116",
        "description": "Risk that vendors are not onboarded per Third Party Risk policy"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-015",
        "description": "Regulatory Reporting"
      },
      {
        "id": "KPA-014",
        "description": "Issue Management"
      },
      {
        "id": "KPA-006",
        "description": "Financial Reporting — Period Close"
      },
      {
        "id": "KPA-010",
        "description": "Access Management"
      },
      {
        "id": "KPA-016",
        "description": "AML Program Framework"
      },
      {
        "id": "KPA-011",
        "description": "Change Management"
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
        "id": "KPA-008",
        "description": "Vendor Due Diligence"
      }
    ]
  },
  {
    "entity_id": "AE-32",
    "entity_name": "Cybersecurity",
    "business_unit": "Wealth & Investment",
    "line_of_defense": "2nd Line of Defense",
    "role": "target_context",
    "horizontal_flag": true,
    "handoff_description": "Processes are handed off related to cybersecurity operations.",
    "handoffs_to": [
      {
        "id": "AE-15",
        "name": "Asset Management",
        "inactive_flag": false
      },
      {
        "id": "AE-36",
        "name": "Vendor Management",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "Critical",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Funding & Liquidity",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Technology",
        "residual_rating": "Low",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Security",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "Medium",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0574",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0575",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0576",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0577",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0578",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0579",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0580",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0581",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0582",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0583",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "control_id": "CTRL-0584",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0585",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0586",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0587",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0588",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0589",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "control_id": "CTRL-0590",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0591",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "control_id": "CTRL-0592",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0593",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0594",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0595",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0596",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "control_id": "CTRL-0597",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "control_id": "CTRL-0598",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0599",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "control_id": "CTRL-0600",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "control_id": "CTRL-0601",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-118",
        "description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "id": "SR-119",
        "description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "id": "SR-130",
        "description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "id": "SR-120",
        "description": "Risk that production changes are not approved before release"
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
        "id": "SR-117",
        "description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "id": "SR-116",
        "description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "id": "SR-109",
        "description": "Risk that the sanctions screening program has inadequate list coverage"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-010",
        "description": "Access Management"
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
      },
      {
        "id": "KPA-014",
        "description": "Issue Management"
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
        "id": "KPA-018",
        "description": "Sanctions Program Oversight"
      }
    ]
  },
  {
    "entity_id": "AE-33",
    "entity_name": "Data Governance",
    "business_unit": "Corporate Functions",
    "line_of_defense": "1st Line of Defense",
    "role": "target_context",
    "horizontal_flag": true,
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
    ],
    "handoffs_from": [
      {
        "id": "AE-14",
        "name": "Investment Banking",
        "inactive_flag": false
      },
      {
        "id": "AE-32",
        "name": "Cybersecurity",
        "inactive_flag": false
      },
      {
        "id": "AE-18",
        "name": "ATM Operations",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "Medium",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "Medium",
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
        "residual_rating": "High",
        "inherent_rating": "High",
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
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "Critical",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "Critical",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0602",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0603",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0604",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0605",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0606",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "control_id": "CTRL-0607",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0608",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0609",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "control_id": "CTRL-0610",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0611",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0612",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0613",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "control_id": "CTRL-0614",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "control_id": "CTRL-0615",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0616",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0617",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "control_id": "CTRL-0618",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0619",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0620",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0621",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0622",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0623",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0624",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0625",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "control_id": "CTRL-0626",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0627",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0628",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0629",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0630",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-130",
        "description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "id": "SR-128",
        "description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "id": "SR-105",
        "description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "id": "SR-124",
        "description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "id": "SR-119",
        "description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "id": "SR-121",
        "description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "id": "SR-117",
        "description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "id": "SR-107",
        "description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "id": "SR-120",
        "description": "Risk that production changes are not approved before release"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-010",
        "description": "Access Management"
      },
      {
        "id": "KPA-014",
        "description": "Issue Management"
      },
      {
        "id": "KPA-016",
        "description": "AML Program Framework"
      },
      {
        "id": "KPA-011",
        "description": "Change Management"
      },
      {
        "id": "KPA-009",
        "description": "Vendor Performance Monitoring"
      },
      {
        "id": "KPA-017",
        "description": "AML Transaction Monitoring Calibration"
      }
    ]
  },
  {
    "entity_id": "AE-37",
    "entity_name": "Model Validation",
    "business_unit": "Operations",
    "line_of_defense": "1st Line of Defense",
    "role": "target_context",
    "horizontal_flag": true,
    "handoff_description": "Processes are handed off related to model validation operations.",
    "handoffs_to": [
      {
        "id": "AE-45",
        "name": "Facilities Management",
        "inactive_flag": false
      },
      {
        "id": "AE-42",
        "name": "Internal Controls",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [
      {
        "id": "AE-26",
        "name": "Payroll Processing",
        "inactive_flag": false
      }
    ],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "Low",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
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
        "residual_rating": "Low",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
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
        "residual_rating": "High",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
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
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "Low",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "Medium",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "Low",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0698",
        "control_title": "Operating control over Model Validation",
        "kpa_id": "KPA-013",
        "kpa_description": "Model Validation",
        "specific_risk_id": "SR-122",
        "specific_risk_description": "Risk that models are not validated before production deployment"
      },
      {
        "control_id": "CTRL-0699",
        "control_title": "Operating control over Model Validation",
        "kpa_id": "KPA-013",
        "kpa_description": "Model Validation",
        "specific_risk_id": "SR-122",
        "specific_risk_description": "Risk that models are not validated before production deployment"
      },
      {
        "control_id": "CTRL-0700",
        "control_title": "Program-level oversight of Model Validation",
        "kpa_id": "KPA-013",
        "kpa_description": "Model Validation",
        "specific_risk_id": "SR-123",
        "specific_risk_description": "Risk that model performance is not monitored against thresholds"
      },
      {
        "control_id": "CTRL-0701",
        "control_title": "Program-level oversight of Model Validation",
        "kpa_id": "KPA-013",
        "kpa_description": "Model Validation",
        "specific_risk_id": "SR-123",
        "specific_risk_description": "Risk that model performance is not monitored against thresholds"
      },
      {
        "control_id": "CTRL-0702",
        "control_title": "Program-level oversight of Model Validation",
        "kpa_id": "KPA-013",
        "kpa_description": "Model Validation",
        "specific_risk_id": "SR-123",
        "specific_risk_description": "Risk that model performance is not monitored against thresholds"
      },
      {
        "control_id": "CTRL-0703",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0704",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "control_id": "CTRL-0705",
        "control_title": "Program-level oversight of AML Program Framework",
        "kpa_id": "KPA-016",
        "kpa_description": "AML Program Framework",
        "specific_risk_id": "SR-105",
        "specific_risk_description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "control_id": "CTRL-0706",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0707",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0708",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0709",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0710",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "control_id": "CTRL-0711",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0712",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0713",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0714",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0715",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0716",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0717",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-122",
        "description": "Risk that models are not validated before production deployment"
      },
      {
        "id": "SR-123",
        "description": "Risk that model performance is not monitored against thresholds"
      },
      {
        "id": "SR-120",
        "description": "Risk that production changes are not approved before release"
      },
      {
        "id": "SR-109",
        "description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "id": "SR-105",
        "description": "Risk that the AML program framework and policies are not maintained"
      },
      {
        "id": "SR-130",
        "description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "id": "SR-106",
        "description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "id": "SR-119",
        "description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "id": "SR-108",
        "description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "id": "SR-117",
        "description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "id": "SR-128",
        "description": "Risk that periodic entity-level risk assessments are not completed"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-013",
        "description": "Model Validation"
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
        "id": "KPA-016",
        "description": "AML Program Framework"
      },
      {
        "id": "KPA-010",
        "description": "Access Management"
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
        "id": "KPA-009",
        "description": "Vendor Performance Monitoring"
      },
      {
        "id": "KPA-014",
        "description": "Issue Management"
      }
    ]
  },
  {
    "entity_id": "AE-39",
    "entity_name": "Market Risk Management",
    "business_unit": "Risk & Compliance",
    "line_of_defense": "1st Line of Defense",
    "role": "target_context",
    "horizontal_flag": true,
    "handoff_description": "Processes are handed off related to market risk management operations.",
    "handoffs_to": [
      {
        "id": "AE-1",
        "name": "Consumer Lending",
        "inactive_flag": false
      },
      {
        "id": "AE-4",
        "name": "Treasury Operations",
        "inactive_flag": false
      },
      {
        "id": "AE-25",
        "name": "Dispute Resolution",
        "inactive_flag": false
      },
      {
        "id": "AE-29",
        "name": "Financial Reporting",
        "inactive_flag": false
      },
      {
        "id": "AE-27",
        "name": "Accounts Payable",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [
      {
        "id": "AE-17",
        "name": "Digital Banking",
        "inactive_flag": false
      },
      {
        "id": "AE-7",
        "name": "Card Operations",
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
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Financial Reporting",
        "residual_rating": "Critical",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Funding & Liquidity",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Technology",
        "residual_rating": "Not Applicable",
        "inherent_rating": "Not Applicable",
        "inherent_rationale": "",
        "control_assessment_rating": "Not Applicable",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Information Security",
        "residual_rating": "Critical",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Model",
        "residual_rating": "Critical",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
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
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "High",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
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
        "residual_rating": "Medium",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0731",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0732",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "control_id": "CTRL-0733",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-108",
        "specific_risk_description": "Risk that Suspicious Activity Reports are not filed within regulatory deadlines"
      },
      {
        "control_id": "CTRL-0734",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0735",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0736",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      },
      {
        "control_id": "CTRL-0737",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "control_id": "CTRL-0738",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "control_id": "CTRL-0739",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0740",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "control_id": "CTRL-0741",
        "control_title": "Program-level oversight of Vendor Due Diligence",
        "kpa_id": "KPA-008",
        "kpa_description": "Vendor Due Diligence",
        "specific_risk_id": "SR-116",
        "specific_risk_description": "Risk that vendors are not onboarded per Third Party Risk policy"
      },
      {
        "control_id": "CTRL-0742",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "control_id": "CTRL-0743",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-120",
        "specific_risk_description": "Risk that production changes are not approved before release"
      },
      {
        "control_id": "CTRL-0744",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0745",
        "control_title": "Operating control over Change Management",
        "kpa_id": "KPA-011",
        "kpa_description": "Change Management",
        "specific_risk_id": "SR-121",
        "specific_risk_description": "Risk that emergency changes are not documented post-implementation"
      },
      {
        "control_id": "CTRL-0746",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0747",
        "control_title": "Program-level oversight of Sanctions Program Oversight",
        "kpa_id": "KPA-018",
        "kpa_description": "Sanctions Program Oversight",
        "specific_risk_id": "SR-109",
        "specific_risk_description": "Risk that the sanctions screening program has inadequate list coverage"
      },
      {
        "control_id": "CTRL-0748",
        "control_title": "Program-level oversight of Training & Awareness",
        "kpa_id": "KPA-020",
        "kpa_description": "Training & Awareness",
        "specific_risk_id": "SR-106",
        "specific_risk_description": "Risk that annual AML training is not delivered to in-scope staff"
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-117",
        "description": "Risk that vendor SLAs and performance are not monitored periodically"
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
      },
      {
        "id": "SR-124",
        "description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "id": "SR-119",
        "description": "Risk that user access is not recertified on the required cadence"
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
        "id": "SR-130",
        "description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "id": "SR-121",
        "description": "Risk that emergency changes are not documented post-implementation"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-009",
        "description": "Vendor Performance Monitoring"
      },
      {
        "id": "KPA-017",
        "description": "AML Transaction Monitoring Calibration"
      },
      {
        "id": "KPA-020",
        "description": "Training & Awareness"
      },
      {
        "id": "KPA-011",
        "description": "Change Management"
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
        "id": "KPA-018",
        "description": "Sanctions Program Oversight"
      },
      {
        "id": "KPA-008",
        "description": "Vendor Due Diligence"
      }
    ]
  },
  {
    "entity_id": "AE-4",
    "entity_name": "Treasury Operations",
    "business_unit": "Global Commercial",
    "line_of_defense": "2nd Line of Defense",
    "role": "target_context",
    "horizontal_flag": false,
    "handoff_description": "nan",
    "handoffs_to": [
      {
        "id": "AE-18",
        "name": "ATM Operations",
        "inactive_flag": false
      }
    ],
    "handoffs_from": [],
    "risks": [
      {
        "risk_category": "Compliance",
        "residual_rating": "High",
        "inherent_rating": "High",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Country",
        "residual_rating": "Low",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Credit",
        "residual_rating": "High",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "External Fraud",
        "residual_rating": "Medium",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
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
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
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
        "residual_rating": "Critical",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Market",
        "residual_rating": "Critical",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Insufficiently Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Operational",
        "residual_rating": "Medium",
        "inherent_rating": "Critical",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Reputational",
        "residual_rating": "Medium",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Strategic & Business",
        "residual_rating": "Low",
        "inherent_rating": "Low",
        "inherent_rationale": "",
        "control_assessment_rating": "Well Controlled",
        "control_assessment_prose": ""
      },
      {
        "risk_category": "Third Party",
        "residual_rating": "Medium",
        "inherent_rating": "Medium",
        "inherent_rationale": "",
        "control_assessment_rating": "Partially Controlled",
        "control_assessment_prose": ""
      }
    ],
    "controls_compact": [
      {
        "control_id": "CTRL-0051",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-112",
        "specific_risk_description": "Risk that payment instructions are not authorized before release"
      },
      {
        "control_id": "CTRL-0052",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-112",
        "specific_risk_description": "Risk that payment instructions are not authorized before release"
      },
      {
        "control_id": "CTRL-0053",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-113",
        "specific_risk_description": "Risk that daily payment reconciliations are not completed and reviewed"
      },
      {
        "control_id": "CTRL-0054",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-113",
        "specific_risk_description": "Risk that daily payment reconciliations are not completed and reviewed"
      },
      {
        "control_id": "CTRL-0055",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-113",
        "specific_risk_description": "Risk that daily payment reconciliations are not completed and reviewed"
      },
      {
        "control_id": "CTRL-0056",
        "control_title": "Operating control over Financial Reporting — Consolidation",
        "kpa_id": "KPA-007",
        "kpa_description": "Financial Reporting — Consolidation",
        "specific_risk_id": "SR-115",
        "specific_risk_description": "Risk that intercompany eliminations are not applied during consolidation"
      },
      {
        "control_id": "CTRL-0057",
        "control_title": "Operating control over Financial Reporting — Consolidation",
        "kpa_id": "KPA-007",
        "kpa_description": "Financial Reporting — Consolidation",
        "specific_risk_id": "SR-115",
        "specific_risk_description": "Risk that intercompany eliminations are not applied during consolidation"
      },
      {
        "control_id": "CTRL-0058",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-119",
        "specific_risk_description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "control_id": "CTRL-0059",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0060",
        "control_title": "Operating control over Financial Reporting — Consolidation",
        "kpa_id": "KPA-007",
        "kpa_description": "Financial Reporting — Consolidation",
        "specific_risk_id": "SR-115",
        "specific_risk_description": "Risk that intercompany eliminations are not applied during consolidation"
      },
      {
        "control_id": "CTRL-0061",
        "control_title": "Operating control over Payment Authorization",
        "kpa_id": "KPA-004",
        "kpa_description": "Payment Authorization",
        "specific_risk_id": "SR-112",
        "specific_risk_description": "Risk that payment instructions are not authorized before release"
      },
      {
        "control_id": "CTRL-0062",
        "control_title": "Operating control over Financial Reporting — Consolidation",
        "kpa_id": "KPA-007",
        "kpa_description": "Financial Reporting — Consolidation",
        "specific_risk_id": "SR-115",
        "specific_risk_description": "Risk that intercompany eliminations are not applied during consolidation"
      },
      {
        "control_id": "CTRL-0063",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "control_id": "CTRL-0064",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0065",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-130",
        "specific_risk_description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "control_id": "CTRL-0066",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-128",
        "specific_risk_description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "control_id": "CTRL-0067",
        "control_title": "Operating control over Access Management",
        "kpa_id": "KPA-010",
        "kpa_description": "Access Management",
        "specific_risk_id": "SR-118",
        "specific_risk_description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "control_id": "CTRL-0068",
        "control_title": "Program-level oversight of Issue Management",
        "kpa_id": "KPA-014",
        "kpa_description": "Issue Management",
        "specific_risk_id": "SR-124",
        "specific_risk_description": "Risk that audit findings are not tracked to remediation"
      },
      {
        "control_id": "CTRL-0069",
        "control_title": "Program-level oversight of Vendor Performance Monitoring",
        "kpa_id": "KPA-009",
        "kpa_description": "Vendor Performance Monitoring",
        "specific_risk_id": "SR-117",
        "specific_risk_description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "control_id": "CTRL-0070",
        "control_title": "Program-level oversight of AML Transaction Monitoring Calibration",
        "kpa_id": "KPA-017",
        "kpa_description": "AML Transaction Monitoring Calibration",
        "specific_risk_id": "SR-107",
        "specific_risk_description": "Risk that transaction monitoring rules are not calibrated against typologies"
      }
    ],
    "specific_risk_coverage": [
      {
        "id": "SR-112",
        "description": "Risk that payment instructions are not authorized before release"
      },
      {
        "id": "SR-113",
        "description": "Risk that daily payment reconciliations are not completed and reviewed"
      },
      {
        "id": "SR-115",
        "description": "Risk that intercompany eliminations are not applied during consolidation"
      },
      {
        "id": "SR-119",
        "description": "Risk that user access is not recertified on the required cadence"
      },
      {
        "id": "SR-117",
        "description": "Risk that vendor SLAs and performance are not monitored periodically"
      },
      {
        "id": "SR-107",
        "description": "Risk that transaction monitoring rules are not calibrated against typologies"
      },
      {
        "id": "SR-130",
        "description": "Risk that customer data is not protected in transit and at rest"
      },
      {
        "id": "SR-128",
        "description": "Risk that periodic entity-level risk assessments are not completed"
      },
      {
        "id": "SR-118",
        "description": "Risk that production access is not provisioned per least-privilege policy"
      },
      {
        "id": "SR-124",
        "description": "Risk that audit findings are not tracked to remediation"
      }
    ],
    "kpa_coverage": [
      {
        "id": "KPA-004",
        "description": "Payment Authorization"
      },
      {
        "id": "KPA-007",
        "description": "Financial Reporting — Consolidation"
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
        "id": "KPA-017",
        "description": "AML Transaction Monitoring Calibration"
      },
      {
        "id": "KPA-014",
        "description": "Issue Management"
      }
    ]
  }
]
```

## Source-context entities (handoff sources — reference for reciprocity checks; do not produce findings about them)

```json
[
  {
    "entity_id": "AE-12",
    "entity_name": "Foreign Exchange",
    "role": "source_context",
    "handoff_description": "Processes are handed off related to foreign exchange operations.",
    "handoffs_to": [
      {
        "id": "AE-5",
        "name": "Wire Transfers",
        "inactive_flag": false
      }
    ]
  },
  {
    "entity_id": "AE-16",
    "entity_name": "Retail Banking",
    "role": "source_context",
    "handoff_description": "Processes are handed off related to retail banking operations.",
    "handoffs_to": []
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
