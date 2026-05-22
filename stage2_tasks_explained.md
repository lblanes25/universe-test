# The Five Checks — In Plain English

Stage 2 reads each audit entity's file and runs five checks on it. This page says,
in plain terms, what each check is actually asking. (The formal definitions live in
`config/stage2_prompt.yaml`; this is the translation.)

**A few words first, so the rest reads cleanly:**

- **Entity** — one audit entity (e.g. "Consumer Lending"). The one being reviewed is the **focal entity**.
- **Handoff** — when one entity says "I pass responsibility for *this risk* to *that entity*." (e.g. Credit Issuance hands AML risk to AML Monitoring.)
- **Controls** — the entity's documented control library, indexed by Specific Risk and KPA. This is the *proof* an entity actually does something about a risk.
- **Ratings** — the 14-category residual-risk ratings on the entity (High / Medium / Low / Not Applicable).
- **Overview** — the free-text description of what the entity does.

The five checks move from "does the paperwork follow our rules" up to the one that
matters most: "when a risk is handed off, does the receiver actually cover it."

---

## Check 1 — Do the files follow our own handoff rules?
*(formal name: Manual-to-file conformance)*

**The question:** We wrote down rules for how handoffs should be documented — e.g. risk
ownership must be stated explicitly, handoffs must be documented down to the attribute
level. Does each entity's file actually follow those rules?

**In short:** This is the housekeeping check. It compares the file against our own
documentation standard and flags where the entity ignored, contradicted, or stayed silent
on a rule.

**Example finding:** "Our standard requires explicit risk ownership, but this entity's
handoff is described in vague prose that never names who owns the risk afterward."

---

## Check 2 — When an entity says it handed a risk off, do its ratings agree?
*(formal name: Handoff representation in the ratings)*

**The question:** If an entity claims to have handed off a risk, its 14-category ratings
should reflect that. Do the words and the ratings tell the same story?

**In short:** Catches mismatches between the prose and the ratings. A handed-off risk
should be marked Not Applicable, or rated with a rationale that explains what was kept.
The red flag is a risk that's claimed handed off but still rated normally with no
acknowledgment — or a rating rationale that mentions another entity while the handoff
column stays blank (an undocumented handoff).

**Example finding:** "The entity says it handed off Third Party risk, but the rating is
still High with no note explaining what it retained."

---

## Check 3 — When a risk is handed off, is it covered at the same depth?
*(formal name: Coarse-handoff test)*

**The question:** A risk can be covered at two depths — **program level** (framework,
policy, training, oversight) or **embedded-process level** (the specific control inside a
business process, like ID verification at customer onboarding). When an entity hands off a
detailed, in-the-process risk, does the receiver actually cover it at that depth — or only
at the high level?

**In short:** This is the most important *pattern* the tool looks for. The classic failure:
an entity hands off "AML risk" to a team that audits the AML *program* — but the embedded
KYC check at customer onboarding isn't in that team's controls and wasn't kept by the
sender either. The handoff was too **coarse**, and the detailed risk fell through the gap.

**Example finding:** "Credit hands AML risk to AML Monitoring. AML Monitoring covers the
program (framework, training, monitoring). KYC-at-onboarding is an embedded control inside
the credit process — it's in neither library. Orphaned."

---

## Check 4 — Does the entity's own file contradict itself?
*(formal name: Overview / handoff / rationale / controls alignment)*

**The question:** Looking only inside one entity's file — do its four parts (overview,
handoff description, rating rationale, control library) tell a consistent story?

**In short:** A self-consistency check. It flags an entity whose overview describes an
activity that should generate a risk, but the rating says Not Applicable and there are no
controls — or, the opposite, an entity that claims to have handed a risk off while its own
controls still cover it.

**Example finding:** "The handoff description says this risk went to another entity, but
the rationale still describes this entity as the owner and its controls still cover the
risk. The file disagrees with itself."

---

## Check 5 — When A hands a risk to B, does B's control library actually cover it?
*(formal name: Cross-entity consistency)*

**The question:** This is the whole point of the project. For each handoff A → B: take the
risks A says it transferred, then look at B's *actual controls*. Does B cover them?

**In short:** The decisive check, judged on control-library evidence. Three outcomes:
- **Full match** → *conforms.* B genuinely covers what A handed off.
- **Partial match** → *likely coverage gap — orphaned control.* B covers the general
  category but not the specific risk that was transferred.
- **No coverage** → *likely coverage gap — no owner.* Nobody covers it. Highest-confidence
  finding.

If A's handoff prose is too vague to tell what was even transferred, that ambiguity is
itself reported as a documentation issue — the tool won't invent a transfer claim.

**Example finding:** "A's handoff transfers the onboarding-verification risk. B's library
covers monitoring and reporting for that category but has no onboarding-verification
control. Partial match — the specific transferred risk is orphaned."

---

## How they fit together

| # | Plain question | What it reads |
|---|----------------|---------------|
| 1 | Do the files follow our handoff rules? | File vs. our documentation standard |
| 2 | Do the ratings agree with the handoff claims? | Handoff prose vs. 14-category ratings |
| 3 | Is the handed-off risk covered at the same depth? | Sender's risk vs. receiver's *type* of control |
| 4 | Does the file contradict itself? | One entity's overview / handoff / rationale / controls |
| 5 | Does the receiver actually cover what was handed off? | Sender's transferred risk vs. receiver's controls |

Checks 1–2 are mostly about **documentation quality**. Checks 3 and 5 are about whether
**coverage actually lands** — they produce the likely coverage gaps. Check 4 catches files
that don't hang together internally.
