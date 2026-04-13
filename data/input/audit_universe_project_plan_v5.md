# Audit Universe Network Map — Detailed Project Plan (v5)

## Purpose
Build a layered tool that helps internal audit plan and demonstrate coverage of the audit universe in a way that accounts for how entities connect — through operational handoffs, shared applications, shared vendors, shared models, and PRSAs. The tool should answer: *"Does our audit plan cover the universe in a way that accounts for clusters, bridge entities, and concentration nodes — and can we demonstrate that visually to the board and regulators?"*

**[ADDED] Regulatory positioning:** All outputs should be structured and documented with the assumption that they will eventually support regulatory responses on audit plan coverage. The specific regulatory citation doesn't need to be identified now, but deliverables should be designed to withstand scrutiny — clear methodology, documented data sources, reproducible logic.

## Audiences
- **Primary:** Internal audit team and audit leadership
- **Secondary (deferred):** Risk & Control Owners — revisit only if the tool reveals insights they actively want

---

## Reference: Edge Philosophy

**Cascade/contagion risk (handoffs):** Directional. A failure in Entity A propagates operationally to Entity B through work, data, or decision handoffs.

**Concentration risk (shared assets):** Entities depend on the same vendor, application, or model. Failure radiates from the shared asset outward, not between entities. Primary entities own the controls; secondary entities are dependent without direct oversight — the true blast radius.

**Structural grouping (PRSA):** Management's grouping of the universe. Produces meaningful cluster signals (~1,390 potential edges).

**Excluded from edges:** Shared policies/standards/procedures (~9,451 potential edges, too noisy). Retained as metadata filters only. Policy subset inclusion TBD pending distribution review.

---

## Phase 1: Data Exploration & Prototyping (AI-Assisted)
*Status: In Progress*

This phase uses AI (ChatGPT) for rapid iteration. All outputs are exploratory — they validate the approach and serve as specifications for the production Python code later.

### Milestone 1.1: Column Inventory ✅ COMPLETE
- [x] Export full Archer Data Set to CSV
- [x] Run column inventory prompt — classify all 383 columns by relationship potential
- [x] Identify usable edge columns, grouping columns, and metadata
- [x] Document known data quality issues

### Milestone 1.2: Layer 1 Tables (AI Draft) ✅ IN PROGRESS
- [x] Export trimmed CSV (~30 columns + 42 risk columns)
- [x] Run Layer 1 prompt — parse into relational tables
- [x] Review output: 373 nodes, 4,043 handoffs, 3,156 entity-app rows, 1,384 entity-vendor rows, 3,955 entity-model rows, 1,208 entity-PRSA rows
- [ ] Review the 13 output sheets for accuracy and completeness
- [ ] Spot-check standardization log (73 decisions) — are the merges correct?
- [ ] Investigate 33 unmatched handoff references — cross-check against 28 removed special review entities
- [ ] Review 7 isolated entities — genuinely standalone or data gaps?
- [ ] Review PRSA distribution — confirm grouping sizes are meaningful
- [ ] Review policy distribution — decide whether any subset is worth including as edges
- [ ] Review 23 concentration flags — do they make sense?

### Milestone 1.3: Edge Derivation (AI Draft)
- [ ] Run Part 2 prompt on validated Layer 1 output — derive entity-to-entity edges from shared attributes
- [ ] Review master edge list — total size, edge type breakdown
- [ ] Review high-frequency shared values — decide on exclusion thresholds
- [ ] Check: do the most connected entities make intuitive sense?
- [ ] Check: do the concentration flags align with known risk areas?

### [ADDED] Milestone 1.3b: Early Visualization Signal Check
- [ ] After edge derivation, produce a rough exploratory visualization of the AI prototype output (quick Plotly, Gephi, or similar render)
- [ ] Show informally to one audit leader — gauge reaction
- [ ] Purpose: calibrate how much to invest in full visualization later. This is not a deliverable; it's a signal check.
- [ ] Note what resonated and what confused them — this informs Phase 4 design

### Milestone 1.4: Layer 2 Exploration (AI Draft)
- [ ] Add audit cycle columns to CSV (minimum frequency, override, last audit date)
- [ ] Add current audit plan data (in-scope entities for this cycle)
- [ ] **[CHANGED]** Run Layer 2 prompt — compute unweighted connection counts by edge type + coverage analysis
- [ ] Review coverage gaps — does this surface anything the team didn't already know?
- [ ] **[CHANGED]** Review overdue + highly connected entities (by raw counts, not composite score) — are these real priority gaps?
- [ ] Present preliminary findings to audit leadership for feedback

**Phase 1 Exit Criteria:** Audit leadership confirms the approach produces useful planning insights. The AI outputs are validated and stable enough to serve as a specification.

---

## Phase 2: Python Production Build

This phase recreates everything from Phase 1 in deterministic, auditable, rerunnable Python code. Start this once Phase 1 outputs are validated — not before. The AI prompts, outputs, and this project plan are the specification.

### Milestone 2.1: Data Pipeline Script
- [ ] Python script: read Archer CSV, filter out special reviews and inactive entities
- [ ] Parse multi-value cells (newline-delimited) into relational tables
- [ ] Preserve primary/secondary distinction for applications and third parties
- [ ] Standardize naming — port the standardization rules from the AI's log into deterministic code (exact match mappings, not AI judgment)
- [ ] Output: Node table, Risk Map, Handoff table, Entity-Application, Entity-Vendor, Entity-Model, Entity-PRSA tables
- [ ] Validation checks built in: row counts, unmatched handoff refs, isolated entities

### Milestone 2.2: Edge Derivation Script
- [ ] Derive entity-to-entity edges from shared attributes (applications, vendors, models, PRSAs)
- [ ] Apply exclusion thresholds for high-frequency shared values (decided in Phase 1)
- [ ] Preserve edge type distinction (cascade vs. concentration vs. structural grouping)
- [ ] Preserve primary/secondary on concentration edges
- [ ] **[ADDED]** Tag edges with display threshold flags — assets shared by 10+ entities flagged for concentration callout treatment rather than individual edge rendering (supports Phase 4 density management)
- [ ] Output: Master edge list with edge type and display flags

### Milestone 2.3: Dependency Lookups
- [ ] Asset → Entity lookup (given a vendor/app/model, list all dependent entities)
- [ ] Entity → Assets + Handoffs lookup (given an entity, list all its dependencies)
- [ ] Concentration flags (assets with 10+ dependent entities)
- [ ] **[CHANGED]** Entity Dependency Profile — unweighted connection counts per edge type:
  - Handoff-to count
  - Handoff-from count
  - Primary application count
  - Secondary application count
  - Primary vendor count
  - Secondary vendor count
  - Model count
  - PRSA group count
  - Total connection count (simple sum)
- [ ] **[ADDED]** Note: weighting can be revisited later if a specific planning question demands it. For now, raw counts by type let leadership apply their own judgment.
- [ ] Output: Excel workbook or queryable data store

### Milestone 2.4: Coverage Matrix Script
- [ ] Import audit plan data
- [ ] Compute effective audit frequency (override if Y, otherwise calculated)
- [ ] Compute overdue status per entity
- [ ] **[CHANGED]** Attach unweighted connection counts by edge type to each entity (no composite score)
- [ ] Generate coverage flags:
  - Overdue AND high total connection count
  - High/Critical residual risk AND Insufficiently/Partially Controlled AND not in plan
  - Concentration assets (10+ dependent entities) where no dependent entity is in the plan
  - Concentration assets where the primary entity (control owner) is not in the plan
  - Clusters of connected entities where coverage is sparse
- [ ] **[ADDED]** Build filtering logic to support Phase 4 density management views:
  - Filter by edge type (handoff-only view, vendor-only view, etc.)
  - Filter by coverage status (uncovered/overdue only)
  - Filter by PRSA group
- [ ] Output: Coverage matrix table with all flags + filter-ready data structure

### Milestone 2.5: Testing & Validation
- [ ] Compare Python outputs against AI outputs — they should match (minus any corrections from review)
- [ ] Run on a fresh CSV export to confirm the pipeline works end-to-end
- [ ] Document the script: what it does, what it expects, how to run it
- [ ] Peer review by another team member

**Phase 2 Exit Criteria:** A single Python script (or small set of scripts) that takes a raw Archer CSV export and produces all Layer 1 + Layer 2 outputs. Deterministic, documented, peer-reviewed.

---

## Phase 3: Layer 2 Delivery & Adoption

**[ADDED] Regulatory framing:** The coverage matrix and its supporting methodology should be documented to a standard that could support a regulatory response. This means: clear data lineage (Archer → CSV → parsed tables → edges → flags), documented decisions (why certain edge types were included/excluded, what thresholds were used), and reproducible outputs.

### Milestone 3.1: Coverage Matrix Delivery
- [ ] Run production pipeline against current audit plan
- [ ] Present coverage matrix to audit leadership
- [ ] Walk through key flags: overdue + connected, uncovered concentration assets, primary entity gaps
- [ ] Collect feedback — what's useful, what's noise, what's missing?

### Milestone 3.2: Integration into Audit Planning Process
- [ ] Define when in the annual planning cycle this tool gets run
- [ ] Define who runs it and who reviews the output
- [ ] Decide: does this supplement the existing planning process or replace parts of it?
- [ ] Document the process

### Milestone 3.3: First Refresh Cycle
- [ ] Run pipeline on next Archer export
- [ ] Compare results to prior run — what changed?
- [ ] Validate that the pipeline handles changes cleanly (new entities, retired entities, renamed assets)

**Phase 3 Exit Criteria:** The coverage matrix is used in at least one real audit planning decision. The pipeline has been run more than once successfully.

---

## Phase 4: Layer 3 — Network Visualization

Only pursue this after Phase 3 confirms Layer 2 is useful. This is the board/regulator communication layer.

### [ADDED] Network Density Management Principles

373 nodes with multiple edge types will be too dense to visualize as a single graph. Density control is a design requirement, not an afterthought.

1. **Filter by edge type.** Every view shows one edge type at a time by default. The handoff network, the shared vendor network, the shared app network, and the PRSA network are separate views. Only layer edge types when answering a specific question.

2. **Set display thresholds.** Assets shared by 10+ entities (aligned with existing concentration flag threshold) are shown as concentration callouts, not as edges drawn to every connected entity. The concentration flag threshold is the density control boundary.

3. **Filter by coverage status.** Build a view that strips out recently audited, well-covered entities and shows only the uncovered or overdue portion of the network. This is the action map for leadership.

4. **Collapse clusters.** If PRSA groupings prove meaningful, support a view where each PRSA group is a single node. Board-level view shows ~30 cluster nodes, not 373 entities. Expand on demand.

5. **Use tables where graphs don't add value.** Some findings are better delivered as adjacency tables than network visuals. Example: "These 8 entities share a critical vendor and none have been audited in 3 years." Design table-based outputs alongside graph-based outputs. Save the visual for when it genuinely adds insight.

*Note: The filtering and threshold logic supporting these views is built into Phase 2's edge derivation and coverage matrix scripts (Milestones 2.2 and 2.4).*

### Milestone 4.1: Tooling Decision
- [ ] Evaluate options: Python (NetworkX + matplotlib/plotly), Gephi, D3, Power BI, Claude-built artifact
- [ ] Key criteria: can it handle 373 nodes legibly? Does it support filtering by edge type and coverage status? Can it collapse PRSA clusters? Can it produce static exports for board decks?
- [ ] Build proof-of-concept in chosen tool

### Milestone 4.2: Graph Construction
- [ ] Load nodes and master edge list
- [ ] **[CHANGED]** Build separate views per edge type — handoff network, vendor network, app network, model network, PRSA network
- [ ] Apply concentration callout treatment for assets above display threshold
- [ ] Run community detection (Louvain or similar) on handoff-only network and on combined network — compare
- [ ] Handle horizontal entities — exclude from clustering, overlay as cross-cutting connectors
- [ ] **[ADDED]** Build collapsed PRSA cluster view for board-level presentation
- [ ] Validate: do the clusters make sense? Do bridge entities surface correctly?

### Milestone 4.3: Audit Plan Overlay
- [ ] Color-code entities by coverage status (in-scope, recently audited, overdue, not covered)
- [ ] Show coverage density per cluster
- [ ] Highlight bridge entities and their coverage status
- [ ] Concentration risk callouts on the map
- [ ] **[ADDED]** Build "action map" view: uncovered/overdue entities only, with their connections

### Milestone 4.4: Board/Regulator Deliverable
- [ ] Design high-level cluster map with coverage percentages (collapsed PRSA view)
- [ ] Prepare static/simplified version for board presentations
- [ ] **[ADDED]** Prepare table-based companion outputs for findings that don't benefit from visualization
- [ ] Write the narrative that accompanies the visual — the map supports the story, doesn't replace it
- [ ] Present to audit leadership for sign-off before board delivery

**Phase 4 Exit Criteria:** A visual deliverable that audit leadership is comfortable presenting to the board or regulators.

---

## Phase 5: Maintenance & Evolution

### Milestone 5.1: Operational Cadence
- [ ] Define refresh schedule (quarterly recommended, aligned with audit planning cycle)
- [ ] Automate CSV export from Archer if possible
- [ ] Build comparison logic: flag what changed between runs (new entities, new edges, shifted clusters)

### Milestone 5.2: Risk Framework Migration
- [ ] When the 14 risks migrate to 23, update the Risk Map parsing logic
- [ ] Re-run the pipeline and compare — does the expanded framework change any coverage conclusions?
- [ ] Update all documentation

### Milestone 5.3: RCO Views (If Warranted)
- [ ] Only if Phases 3-4 reveal insights RCOs actively request
- [ ] Add risk-based filtering to the visualization (select a risk, see affected entities and their connections)
- [ ] Pilot with 2-3 RCOs
- [ ] Design for non-auditor audience — no audit jargon, plain language

---

## Reproducibility & Auditability

The initial data parsing and exploration is done using AI (ChatGPT) for speed and iteration. Once the approach is validated, the entire pipeline is rebuilt in Python (pandas + NetworkX) for production use. This is important because:

- **Deterministic:** A Python script produces identical output every time on the same input. AI prompts don't guarantee this.
- **Auditable:** Reviewers, regulators, or successors can read the code and verify the logic. No black box.
- **Repeatable:** Quarterly or annual refreshes run the same script against a fresh CSV export. No re-prompting required.
- **Defensible:** "We built a script that parses our Archer data and computes connectivity" is easier to defend than "we asked an AI to do it."

The AI is the prototyping tool. Python is the production tool. The project plan, prompts, and AI outputs serve as the specification for the Python rewrite.

---

## Reference: Data Source Details

### CSV Columns

**Identity/grouping:** Entity ID, Entity Name, Entity Type, Entity Status, Business Unit, Line of Defense, Subsidiary Bank, Tab IV: Subsidiary, Audit Leader, PGA/ASL

**Audit cycle:** Minimum Audit Frequency, Override Minimum Audit Frequency (Y/N), Override Minimum Audit Frequency (value), Last AXP (Most Recent) Audit Report Issued Date

*Effective audit frequency = override value if override = Y, otherwise calculated minimum.*

**Edge columns:** Hand-offs from Other Audit Entities, Hand-offs to Other Audit Entities, Hand-off Description, PRIMARY IT APPLICATIONS, SECONDARY IT APPLICATIONS, PRIMARY TLM THIRD PARTY ENGAGEMENT(S), SECONDARY TLM THIRD PARTY ENGAGEMENT(S), Models, PRSA

**Metadata filters (not for edges):** POLICIES/STANDARDS/PROCEDURES

**Risk assessment (14 risks × 3 ratings = 42 columns):**
- Inherent Risk Rating (Not Applicable, Low, Medium, High, Critical)
- Residual Risk Rating (same scale — operative rating driving frequency and planning)
- Control Assessment Rating (Well Controlled, Partially Controlled, Insufficiently Controlled)

Migrating to 23 risks in the future — redo when transition is complete.

### Primary/Secondary Distinction (Applications & Third Parties)
- **Primary:** Entity owns and tests controls for this asset
- **Secondary:** Entity's key controls depend on this asset without owning control testing

### Data Interpretation
- Blanks in vendor, application, and model fields = no relationship of that type (real data, not a gap)
- **[CHANGED]** Teams validate their audit entities annually through the entity refresh process. This plan treats validated data as accurate. If blanks are wrong, the data quality problem is upstream in the entity refresh process and broader than this project — it doesn't block this work.

### Known Data Issues
- [ ] Inconsistent naming in application, vendor, and model fields
- [ ] 33 unmatched handoff references (some likely map to the 28 removed special review entities)
- [ ] 7 isolated entities to investigate

### Layer 1 Results (from AI prototype)
- 373 active entities (28 special reviews removed, 0 inactive)
- 4,043 handoff rows
- 3,156 entity-application rows
- 1,384 entity-vendor rows
- 3,955 entity-model rows
- 1,208 entity-PRSA rows
- 1,849 entity-policy rows (exploratory)
- 2,617 risk map rows
- 23 concentration flags
- 73 standardization decisions
- PRSA: ~1,390 potential edges (confirmed as edge type)
- Policies: ~9,451 potential edges (excluded pending subset review)

---

## Change Log (v4 → v5)

| Change | Where | What |
|--------|-------|------|
| Removed | Throughout | Composite connectivity score weighting. Replaced with unweighted connection counts by edge type. |
| Removed | Open Questions | "Composite connectivity score weighting for Layer 2" |
| Added | Purpose | Regulatory positioning note |
| Added | Phase 1, after 1.3 | Milestone 1.3b: Early Visualization Signal Check |
| Added | Phase 2, Milestone 2.2 | Display threshold flags on edges for density management |
| Added | Phase 2, Milestone 2.4 | Filtering logic for edge type, coverage status, PRSA group |
| Added | Phase 3 | Regulatory framing note on documentation standards |
| Added | Phase 4 | Network Density Management Principles (5 principles) |
| Changed | Phase 4, Milestone 4.2 | Separate views per edge type, collapsed PRSA cluster view |
| Changed | Phase 4, Milestone 4.3 | Added "action map" view (uncovered/overdue only) |
| Added | Phase 4, Milestone 4.4 | Table-based companion outputs |
| Changed | Data Interpretation | Updated data quality stance — validated through entity refresh, upstream problem if wrong |

---

## Open Questions
- [ ] Policy edge decision: review distribution detail for subset inclusion (policies with <20-30 entities)
- [ ] Board deliverable format: interactive dashboard vs. static slides
- [ ] Does audit plan data exist in a structured format, or does it need to be built?
- [ ] Visualization tooling decision (Phase 4)
