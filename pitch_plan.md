# Pitch Plan — Audit Universe / Handoff Review as a Gen AI Solution

Working doc for the Shark-Tank-style pitch to audit leadership. Captures the framing, demo plan, 1-week execution sprint, and the templates needed to run the week. Adjust freely; this is a starting frame, not a finished script.

---

## 1. The frame

One question, not a tour:

> When we hand off a risk to another audit entity, can we prove the receiving entity actually covers it — at the level it was transferred? Today, no one can answer that across ~427 entities and ~4,400 handoffs. This solution gets us there.

Anchor the whole pitch on the **assurance map** as the deliverable. IIA Global Internal Audit Standard 9.5 (Coordination and Reliance, effective Jan 2025) expects internal audit to produce a view proving every risk has exactly one owner and that other coverage is either a defined handoff or a documented reliance. The function is going to be asked for that artifact regardless. The Gen AI piece is the *means* to produce it at scale; the map is the *thing*.

Reframing "AI solution" as "the artifact you're already going to be asked to produce" converts curiosity into urgency. Don't pitch a vitamin; pitch alignment to a standard.

---

## 2. The story beats (in order)

1. **The question we cannot answer today.** State plainly: we have 4,400 handoffs documented in prose form across 427 entities. There is no rolled-up view that demonstrates each handed-off risk lands somewhere. We discover gaps reactively — after an incident or after a regulator asks.
2. **Why it's hard.** Handoff documentation lives in free-text fields. The receiving entity's controls are in Archer, indexed by Specific Risk and KPA — not by which transferor pointed at them. The connection is implicit. Reading 4,400 of these manually is a multi-quarter undertaking.
3. **The failure mode that should make the room uncomfortable.** Credit Issuance hands "AML risk" to AML Monitoring. AML Monitoring audits the AML program — framework, training, transaction-monitoring calibration. But KYC at customer onboarding is an embedded control inside the credit process. If that boundary isn't drawn explicitly, nobody tests it, and nobody knows nobody is testing it.
4. **What we built.** A deterministic pipeline produces the relational view (entities, handoffs, shared apps/vendors/PRSAs, concentration assets, coverage flags) plus an interactive network map grouped by Audit Leader. On top of that, a Gen AI evaluation reads each entity's controls (Specific Risk + KPA), reads the handoff description, reads the receiving entity's controls, and flags where coverage doesn't actually land.
5. **What we found.** [Insert the 3–5 adjudicated findings the team picks during the working session. This is the proof.]
6. **What this becomes.** Annual planning input, mid-year coverage attestation, RCO-level assurance map. Pick one for the pitch and park the others as roadmap.

---

## 3. Audience and demo scope (decided)

- **Audience:** audit leadership / domain.
- **Demo:** real data, end-to-end. Stage 2 has been executed across 350 batches; the corpus exists.
- **Posture:** prototype using ChatGPT Pro extended thinking with a 5-task evaluation prompt. Productization is roadmap, not done. State this plainly; audit leaders are skeptical-by-training and over-claiming loses them.

Tailoring for this audience:
- Use domain language: handoff hygiene, embedded controls, attribute-level documentation, assurance map.
- Anchor on IIA 9.5 explicitly.
- Lead with the KYC-at-credit-origination example. It's the most viscerally familiar embedded-control failure for any audit leader.
- Do not lead with the network visualization. It's the hook, not the value. The value is the ranked findings.

---

## 4. The live demo (≤5 minutes)

Three altitudes, each ~90 seconds:

1. **The map** — Open the network viz. Switch to one Audit Leader's portfolio + inbound-impact mode. "Here's whose work outside my portfolio can break mine. This is the assurance-map view we don't currently have."
2. **The tactical view** — Open the coverage matrix. Walk one HIGH flag: a concentration asset (10+ dependent entities) with zero coverage in this year's plan, or an overdue + highly-connected entity. "This is what the rules find deterministically. Mechanical. Cheap to run quarterly."
3. **The finding** — Show one adjudicated Stage 2 finding. "Entity A's handoff description claims AML risk transferred to Entity B. B's control library covers the program layer. The embedded KYC controls at A's process touchpoints are not in B's library. This is the kind of gap manual review would not catch at scale. We ran 350 batches and surfaced N likely coverage gaps; our team adjudicated M as real."

Honest captioning under each: "Prototype. Run via ChatGPT Pro web UI. Findings adjudicated by the team."

---

## 5. One-week sprint plan

Timeline is one week. You are the critical path, not the team. Their contribution is high-leverage and time-bounded; everything else gets cut.

### Day 1 — Make the artifact and bound the ask

- Generate the rollup:
  ```
  python -m src.stage2_handoff_review.aggregate
  python -m src.stage2_handoff_review.summarize_findings
  ```
- Open `runs/stage2/aggregated/findings_rollup.xlsx`. Skim every sheet. Note totals (total findings, classification breakdown, top entities by issue count, gate pass rate).
- Open `runs/stage2/aggregated/ranked_summary.md`. Identify 10–15 candidate "likely real coverage gap" findings for the working session. Bias selection toward:
  - High confidence (`confidence: high` in the ranked summary).
  - Gate-passed batch (the `gate_passed` column on the findings sheet).
  - Classic coarse-handoff pattern (program-level vs embedded-process control mismatch).
  - Spread across audit leaders so multiple teammates can each recognize one of theirs in the working session.
- Send the team the kickoff message (see §12). Lock the working session time.

### Day 2 — The working session (60–90 min)

- Walk through the 10–15 candidates on screen share.
- For each: 60 seconds of context, then group calls "real / noise / partial." Capture notes in the workbook.
- Land on 3–5 findings that will be the demo's proof. Each teammate "owns" at least one — meaning they can speak to it if a shark asks.
- Decide on the demo entity (whose Audit Leader portfolio the network viz opens to).
- Decide on the use case framing (annual planning input vs mid-year attestation vs RCO assurance map). Pick ONE.
- See §13 for full agenda.

### Day 3 — Build the deck

- 5–7 slides max. Beats from §2 are the spine.
- Slot the 3–5 adjudicated findings into the proof slide(s).
- Decide who presents which beat by end of day. If any teammate is presenting, they need to know now.

### Day 4 — Dry-run with one teammate

- Stand-and-deliver, full demo path, time it.
- Cut anything that doesn't earn its slot.
- Fix any rough edges in the live demo: font sizes in the workbook, sheet visibility order, which Audit Leader the viz opens to, network viz performance.

### Day 5 — Final polish + present

- Last sanity check of the demo path. Don't introduce new content the day of.
- Present.

---

## 6. What the team commits to

Total ask per teammate: ~2 hours across the week. Anything more and someone under-delivers and slows the sprint.

1. **A 60–90 minute working session with you, mid-week.** The ownership moment. You walk them through the rollup, they react in real time, you co-decide which findings make the demo. Without this they're spectators; with it they're co-authors.
2. **30–60 minutes of pre-work before that session.** Each teammate skims the slice of findings tied to entities in their portfolio (filter by `audit_leader` or `business_unit` in the rollup workbook). They come with 1–2 reactions: "this one is real," "this one is noise," "this is interesting but partial."
3. **A name on a slide.** Each teammate's name appears as a contributor on the deck. Doesn't cost them anything; matters.

Pre-registration of expected gaps, full adjudication of 50 findings, framework reworking, label retitling — all the things that were on the long-timeline roadmap — get cut. They're post-pitch work.

---

## 7. Post-pitch roadmap (NOT this week)

Captured for the working session's "park-it" list. Don't do these now:

- **Relabel display strings in `config/stage2_prompt.yaml`** to match the team's plain-English vocabulary. (Refactor is done; team can edit later.)
- **Plain-English second pass over finding prose.** A short LLM cleanup pass over `findings.csv` so the `reasoning` and `evidence_quote` fields read more like an auditor wrote them.
- **Pre-register expected findings on 10+ entities** to quantify "of N expected gaps, we found M, plus K we didn't expect."
- **Full adjudication of the top 50 findings.** This week we adjudicate 10–15; the rest is later.
- **Productize the manual ChatGPT Pro paste workflow** (API-driven or internal-LLM-driven runs).
- **Rework task definitions or framework definitions** in the YAML. Deliberate-edit operation; requires re-run of affected batches.
- **Generate the second LLM pass to plain-English-ify findings.**
- **Build the actual assurance map artifact** beyond the demo views.

---

## 8. What to be honest about with the sharks

Audit leaders will smell over-claiming. State plainly:

- This is a prototype using ChatGPT Pro extended thinking and a manual paste workflow. Productization is roadmap.
- We ran 350 batches. Our team adjudicated N findings.
- Findings require human adjudication — the pipeline tells you *where to look*, not what the answer is.
- We've identified [N] real coverage gaps and [M] systemic documentation patterns. We have NOT yet remediated any of them. The tool produces a punch list, not a finished assurance map.
- The framework (handoff vs reliance, controls-as-primary-evidence, the 5 tasks) was developed iteratively with AI prototyping. It's defensible but not yet peer-reviewed.

That posture is the credibility play. Audit leaders trust honesty about limits more than they trust polished claims.

---

## 9. What to cut from the pitch

- The Layer 1 / Layer 2 pipeline as "the product." It's table-stakes data prep. Mentioning every stage will make the Gen AI piece feel like 10% of a 90% project.
- The full feature set of the network viz. Show the one mode that lands (portfolio + inbound impact); don't tour the rest.
- The IIA 9.5 quote at length. One sentence linking to the standard is enough; auditors know the standard exists.
- Raw token counts, batch sizes, prompt architecture. Sharks aren't asking about plumbing.

---

## 10. What to NOT do this week

- Don't relabel anything in the YAML. The refactor enables it for later; this week, ship with the labels you have.
- Don't try to plain-English-ify finding prose with a second LLM pass. Use the cleanest 3–5 findings; don't rewrite the others.
- Don't re-run any Stage 2 batches. The corpus is what it is.
- Don't try to get audit leadership feedback before the pitch. That *is* the pitch.
- Don't get drawn into prompt revision discussions during the working session. Capture them on a parking-lot list (§7) and move on.
- Don't try to adjudicate everything. Cap yourself at the top of the ranked summary.
- Don't re-introduce cut scope on Day 4 or 5. Stop adding content after Day 3.

---

## 11. Two failure modes to watch

1. **You go down the rabbit hole on findings.** With 350 batches of findings, it's tempting to read everything. Cap yourself at the top of the ranked summary on Day 1. Use the workbook's filters; don't try to adjudicate everything. If you find yourself reading findings for more than ~2 hours on Day 1, stop and curate.
2. **A teammate misses the working session.** If anyone can't make the time, they don't get an ownership slot. Don't try to re-run the session for one person — give them an async role like deck reviewer instead, so they still appear on the slide. Lock the session time on Day 1.

---

## 12. Team kickoff message (template)

Adapt and send Day 1. Keep it short — long emails get skimmed.

> **Subject: Shark Tank pitch — your input needed before [day, time]**
>
> Team — we're pitching the audit universe / handoff review work to leadership on **[pitch date]**. Thanks for the vote of confidence. Here's what I need from each of you between now and then. It's small but it matters.
>
> **Working session:** **[day, time, 90 min, link/room]**
> This is the only sync meeting required. We'll go through the Stage 2 findings together, decide which 3–5 make the demo, and split up who speaks to what.
>
> **Before the session (~30–60 min of your time):**
> 1. Open the rollup: `[path or shared link to findings_rollup.xlsx]`
> 2. Go to the **"Gaps by Entity"** sheet. Filter the `audit_leader` column to your portfolio (or `business_unit` if you cover multiple).
> 3. Pick 1–2 findings to come prepared to react to. Reactions can be:
>    - "This is a real gap"
>    - "This is noise / the model misread something"
>    - "This is interesting but the framing is off — here's what's actually going on"
>
> **Background reading (optional but useful):**
> - Pitch framing: `pitch_plan.md` §1–2 in the repo
> - How the findings were produced: `runs/stage2/README.md`
>
> **What I'm NOT asking:**
> - Don't try to adjudicate everything — just your portfolio.
> - Don't try to rework the prompt or labels — those decisions are post-pitch.
> - Don't try to fix the methodology — it shipped, we work with what's there.
>
> If you can't make the working session, ping me. We'll find you an async role so your name still goes on the deck.
>
> [Your name]

---

## 13. Working session agenda (90 min)

| Time | Item | Who |
|------|------|-----|
| 00:00–05:00 | **Why we're here.** Confirm the pitch frame (IIA 9.5, KYC-at-credit-origination, assurance map). 30 seconds each: what is the demo path. | You |
| 05:00–15:00 | **The numbers.** Show the rollup's Summary tab. Total findings, classification breakdown, top entities by issue count, gate pass rate. Set context. | You |
| 15:00–60:00 | **Adjudicate candidates.** Walk through the 10–15 pre-selected findings. For each: 60 seconds context, then group calls "real / noise / partial." Capture notes inline in the workbook. | Team |
| 60:00–75:00 | **Pick the demo set.** Land on 3–5 findings. Each teammate owns at least one — they'll speak to it if a shark asks. | Team |
| 75:00–85:00 | **Roles for pitch day.** Who presents what beat. Who is on standby for questions. Who covers if someone is out. | You + team |
| 85:00–90:00 | **Action items.** Confirm demo entity (whose Audit Leader portfolio shows in the viz). Confirm use case framing pick. Assign deck-review owner. | You |

**Rules of the session:**
- One person speaks at a time. If multiple people want to react to a finding, take them in order.
- "Park it" rule: any methodology, labeling, or framework discussion goes into the post-pitch list (§7), not the session. You'll need someone to keep the parking lot.
- No agenda padding. If the adjudication block runs long, cut the roles block to 5 minutes — those can be decided in a follow-up message.
- Take rough notes; clean up after.

**Artifacts at end of session:**
- The 3–5 adjudicated demo findings (in the rollup or a shared doc).
- The demo entity (one named Audit Leader's portfolio).
- The use case framing pick (one of: annual planning input / mid-year attestation / RCO assurance map / something else surfaced by the team).
- Speaker assignments for the pitch.
- A list of "things we wanted to discuss but parked" for post-pitch.

---

## 14. Open decisions for the working session

- Demo entity selection — which Audit Leader's portfolio shows in the network viz?
- Which 3–5 findings carry the proof load?
- Use case framing — single sentence the pitch hinges on.
- Speaker assignments per pitch beat.
- Deck review owner (one teammate other than you).
