# Audit Universe Network Map — Python Pipeline Specification

## For Claude Code: This document is the complete specification for building the data pipeline. All decisions have been validated through AI prototyping with real data. Build exactly to this spec.

---

## What This Pipeline Does

Takes a CSV export of an audit universe (~427 active entities across ~800 raw rows) and produces:
1. Clean relational tables (Layer 1)
2. Entity-to-entity edge list (Edge Derivation)
3. Coverage matrix with gap flags (Layer 2)
4. Excel workbook outputs at each stage

The pipeline answers three questions:
1. Where are the coverage gaps when we account for how entities connect?
2. Where does concentration risk create uncovered exposure?
3. Where does an entity's connectivity suggest its audit frequency should be reconsidered?

---

## Input Files

### Primary: Audit Universe CSV
- For development and testing: use `dummy_audit_universe_50.csv` (50 entities, 70 columns)
- Production will use a real Archer export (~800 rows, same column structure)
- Multi-value fields use **semicolon (;)** delimiters
- Dates stored as text (MM/DD/YYYY format)

### Secondary: Audit Plan List
- Simple list of Entity IDs in scope for the current audit cycle
- Format: CSV or text, one AE ID per row
- For testing: generate a random sample of ~40% of active entity IDs from the dummy data

### Optional: Application/Vendor Name Mapping
- Maps ARA-* and TLM* IDs to human-readable names
- Not required for pipeline logic but improves readability of outputs

---

## Column Names (Exact)

### Identity / Grouping
- Audit Entity ID (primary key, format: AE-nnn)
- Audit Entity Name
- Audit Entity Type (used for filtering)
- Audit Entity Status (used for filtering)
- Business Unit
- Line of Defense
- Subsidiary Bank
- Core Audit Team
- Integrated Team
- Audit Leader
- PGA/ASL

### Audit Cycle
- Minimum Audit Frequency
- Do you want to override the Minimum Audit Frequency? (Yes/No)
- Override Minimum Audit Frequency (1 Year / 1.5 Years / 2 Years / Not Applicable / blank)
- Last AXP (Most Recent) Audit Report Issued Date (text, MM/DD/YYYY)

Effective frequency logic: if override = "Yes" AND override value is a valid frequency (not blank, not "Not Applicable"), use override value. Otherwise use Minimum Audit Frequency.

Note: 5 entities in real data have override=Yes but no usable override value. Fall back to calculated minimum for these.

### Edge Columns
- Hand-offs from Other Audit Entities (semicolon-delimited AE IDs)
- Hand-offs to Other Audit Entities (semicolon-delimited AE IDs)
- Hand-off Description (free text, not parsed programmatically)
- PRIMARY IT APPLICATIONS (MAPPED) (semicolon-delimited)
- SECONDARY IT APPLICATIONS (RELATED OR RELIED ON) (semicolon-delimited)
- PRIMARY TLM THIRD PARTY ENGAGEMENT (semicolon-delimited)
- SECONDARY TLM THIRD PARTY ENGAGEMENTS (RELATED) (semicolon-delimited)
- Models (semicolon-delimited)
- PRSA (semicolon-delimited)

### Metadata (not for edges)
- POLICIES/STANDARDS/PROCEDURES (semicolon-delimited)

### Risk Assessment (14 risks × 3 columns = 42 columns)

Each risk has three columns with these suffixes in the column headers:
- Inherent Risk (values: Not Applicable, Low, Medium, High, Critical)
- Residual Risk (same scale — this is the operative rating)
- Control Assessment (values: Well Controlled, Insufficiently Controlled; note: "Partially Controlled" does not exist in the real data)

The 14 risks:
Compliance, Country, Credit, External Fraud, Financial Reporting, Funding & Liquidity, Information Technology, Information Security, Model, Market, Operational, Reputational, Strategic & Business, Third Party

There are also "Overall" inherent and residual risk columns at the entity level. Include these in the Nodes table as metadata (useful for color-coding) but they are NOT part of the 14-risk triplets.

---

## Pipeline Stage 1: Filtering

Remove rows where:
- Audit Entity Type indicates non-recurring / special review (not a standard audit entity)
- Audit Entity Status is not "Active"

Log:
- Count removed by each filter
- Count removed by both
- Total remaining
- List all removed Entity IDs with removal reason

---

## Pipeline Stage 2: Node Table

One row per remaining entity:
- All identity/grouping columns
- Horizontal Flag: "horizontal" if entity name contains keywords suggesting cross-cutting function (AML, KYC, Sanctions, Compliance, IT, Cybersecurity, Data Governance, Vendor Management, Model Validation, Internal Controls, Business Continuity, Fraud, Operational Risk, Market Risk, Credit Risk, Anti-Money Laundering). Otherwise "vertical."
- Overall Inherent Risk Rating
- Overall Residual Risk Rating

---

## Pipeline Stage 3: Risk Map

One row per entity-risk combination where the risk is applicable.

Applicable = Residual Risk Rating is NOT "Not Applicable" and NOT blank.

Columns: Entity ID, Risk Name, Inherent Risk Rating, Residual Risk Rating, Control Assessment Rating

---

## Pipeline Stage 4: Relational Tables

Split semicolon-delimited fields. Trim whitespace from each value after splitting.

### Standardization
- Deduplicate values that differ only by whitespace, capitalization, or formatting
- For POLICIES/STANDARDS/PROCEDURES: normalize ID formats (spaces vs. underscores, e.g., "AEBC 65" → "AEBC_65")
- Log every standardization decision: original value, standardized value, table, row count affected
- In the real data run, the AI made 73 standardization decisions. The log from that run should be used as the initial mapping table. For new values not in the mapping, flag them for manual review rather than guessing.

### 4a. Handoffs
- Source Entity ID, Target Entity ID, Direction ("to" or "from")
- "to" = from Hand-offs to Other Audit Entities column
- "from" = from Hand-offs from Other Audit Entities column
- Flag unmatched: TRUE if target/source ID not in Node table
- In real data: 45 unmatched IDs, all are filtered-out entities (special reviews or inactive). 199 handoff rows reference them.

### 4b. Entity-Application
- Entity ID, Application Name, Relationship ("primary" or "secondary")
- Primary from: PRIMARY IT APPLICATIONS (MAPPED)
- Secondary from: SECONDARY IT APPLICATIONS (RELATED OR RELIED ON)
- Standardize names across both columns

### 4c. Entity-Vendor
- Entity ID, Third Party Name, Relationship ("primary" or "secondary")
- Primary from: PRIMARY TLM THIRD PARTY ENGAGEMENT
- Secondary from: SECONDARY TLM THIRD PARTY ENGAGEMENTS (RELATED)
- Standardize names across both columns

### 4d. Entity-Model
- Entity ID, Model Name
- From: Models column

### 4e. Entity-PRSA
- Entity ID, PRSA Value
- From: PRSA column
- Confirmed as edge type (~1,486 edges in real data)

### 4f. Entity-Policy (Exploratory)
- Entity ID, Policy/Standard ID
- From: POLICIES/STANDARDS/PROCEDURES column
- Normalize ID formats
- NOT used for edge construction — metadata filter only (~9,451 potential edges, too dense)

---

## Pipeline Stage 5: Dependency Lookups

### Asset Dependency Lookup
For each unique application, vendor, and model:
- Asset Name, Asset Type, Dependent Entity Count
- Primary Count, Secondary Count
- Dependent Entity IDs (list)
- Business Units represented

Sort by count descending within each type.

### Entity Dependency Profile
For each entity:
- Handoff-to count, Handoff-from count
- Primary app count, Secondary app count
- Primary vendor count, Secondary vendor count
- Model count, PRSA count
- Total connection count (simple sum, no weighting)
- Handoff partner Entity IDs

Sort by total descending.

### Concentration Flags
Flag assets with 10+ dependent entities. Include primary/secondary breakdown.

---

## Pipeline Stage 6: Edge Derivation

### CRITICAL EXCLUSION: Do NOT derive pairwise edges from shared models.

Models are excluded from edge construction. In real data, ~12 model-governance entities share nearly every model, generating ~9,900 meaningless pairwise edges (58% of all edges). Models are analyzed through concentration flags only.

### Derive entity-to-entity edges from:
- Shared applications (entities sharing the same app = one edge per shared app)
- Shared vendors (same logic)
- Shared PRSAs (same logic)

### Rules:
- Deduplicate at entity-value level before pairing
- Each pair stored once (A-B, not both A-B and B-A) for shared attributes
- Handoff edges preserve original direction (source → target)
- Flag shared values with 10+ dependent entities as "high frequency"

### Master Edge List columns:
- Entity A ID, Entity B ID, Edge Type, Detail (shared value or blank), High Frequency Flag

### Edge Types:
- handoff_to (directional — cascade/contagion risk)
- handoff_from (directional — cascade/contagion risk)
- shared_app (undirected — concentration risk)
- shared_vendor (undirected — concentration risk)
- shared_prsa (undirected — structural grouping)

Real data results: ~7,200 edges after excluding models (4,589 handoffs + 1,092 apps + 49 vendors + 1,486 PRSAs)

---

## Pipeline Stage 7: Audit Cycle Summary

For each entity:
- Effective audit frequency (apply override logic)
- Last audit date (parse from text)
- Days since last audit (from today)
- Overdue flag (Yes/No/Unknown)
- Unknown = frequency is non-cyclical or last audit date is missing

Real data: 92 overdue, 250 not overdue, 85 unknown.

---

## Pipeline Stage 8: Coverage Matrix (Layer 2)

Requires: audit plan entity list (separate input file)

### Connectivity Total
Sum of: handoff-to + handoff-from + shared_app + shared_vendor + shared_prsa edges per entity.
**Excludes shared_model.** This is the number that drives all coverage flags.

### Model Exposure
Count of models per entity from Entity-Model table. Informational only, not in Connectivity Total.

### Risk Profile
From Risk Map:
- Count of High/Critical residual risks
- Count of Insufficiently Controlled risks
- Count of both (High/Critical AND Insufficiently Controlled)
- Highest individual residual risk
- List of High/Critical risk names

### Coverage Flags

**Flag 1: COVERAGE GAP — CONNECTED CLUSTER (HIGH)**
Groups of 5+ entities connected by handoffs where NONE are in the audit plan.

**Flag 2: OVERDUE + HIGHLY CONNECTED (HIGH)**
Overdue AND top quartile Connectivity Total.

**Flag 3: CONCENTRATION ASSET — ZERO COVERAGE (HIGH)**
Apps, vendors, or models with 10+ dependent entities where no dependent entity is in the plan. (Models included here even though excluded from connectivity counts.)

**Flag 4: PRIMARY CONTROL OWNER NOT IN PLAN (HIGH)**
For concentration assets, the primary entity (control owner) is not in the plan.

**Flag 5: CONNECTIVITY SUGGESTS HIGHER FREQUENCY (MEDIUM)**
Overall residual risk = Low or Medium, BUT hands off to multiple High/Critical entities OR is primary control owner for a concentration asset.

**Flag 6: HIGH RISK + WEAK CONTROLS, NOT IN PLAN (MEDIUM)**
At least one risk rated High/Critical residual AND Insufficiently Controlled, not in plan.

**Flag 7: FREQUENCY OVERRIDE ON CONNECTED ENTITY (LOW)**
Frequency overridden AND top quartile Connectivity Total.

### Coverage Summary
- Total entities, in scope count and %, overdue count, overdue and not in plan
- Top 20/10 most connected: how many in scope
- Horizontal entities: how many in scope
- Concentration assets: total, zero coverage, primary not in plan
- Risk: entities with high risk + weak controls, average connectivity by risk level
- Flag counts by type and priority

### Concentration Risk Detail
For each concentration asset (10+ dependent entities, including models):
- Asset info, dependent count, primary entity details (risk rating, frequency, last audit, in scope), secondary coverage rate

---

## Output Format

Each pipeline stage produces an Excel workbook with formatted sheets:
- Headers: white text on blue background (#4472C4), bold
- Data: 10pt Arial
- Column widths auto-fitted
- Conditional formatting on coverage flags (red = HIGH, yellow = MEDIUM, gray = LOW)
- Coverage status cells: green fill = in scope, red fill = overdue

### Stage outputs:
1. `layer1_output.xlsx` — Nodes, Risk Map, Handoffs, Entity-Application, Entity-Vendor, Entity-Model, Entity-PRSA, Entity-Policy, Asset Dependency Lookup, Entity Dependency Profile, Concentration Flags, PRSA & Policy Distribution, Audit Cycle Summary, Validation & Standardization Log
2. `edge_derivation_output.xlsx` — Master Edge List, High Frequency Shared Values, Summary Statistics
3. `layer2_coverage_matrix.xlsx` — Coverage Matrix, Coverage Flags, Coverage Summary, Concentration Risk Detail
4. `network_visualization.html` — Interactive network graph (Stage 9)

---

## Pipeline Stage 9: Interactive HTML Visualization

Generate a single self-contained HTML file using D3.js or Plotly (embedded, no external dependencies). The file should open in any modern browser with full interactivity.

### Data Sources
Read from the pipeline's in-memory data or from the output Excel files:
- Nodes table (entity ID, name, audit leader, business unit, horizontal flag, overall residual risk)
- Coverage Matrix (in scope, overdue, connectivity total)
- Handoffs table (source, target, direction)
- Entity-Application, Entity-Vendor, Entity-PRSA tables (for toggling shared asset edges)
- Asset Dependency Lookup (for application/vendor focus mode)

### Layout
- Group entities by **Audit Leader** (not Business Unit)
- Draw a light background region or convex hull around each Audit Leader cluster with label
- Force-directed layout within each cluster
- Clear spacing between clusters
- Cross-cluster handoff edges should be visually prominent

### Node Encoding

**Color = Overall Residual Risk Rating:**
- Red (#c0392b) = Critical
- Orange (#e67e22) = High
- Yellow (#f1c40f) = Medium
- Green (#27ae60) = Low
- Gray (#95a5a6) = N/A or unknown

**Shape = Audit plan status:**
- Circle = In Scope This Year
- Diamond = Not In Scope This Year
- Thick dark border on diamonds that are also Overdue

**Size = Connectivity Total** (proportional, with min/max caps for readability)

**Labels:**
- Default zoom: Entity ID only
- Zoomed in: full Entity Name
- Full zoom out: hide labels

**Hover tooltip:** Entity ID, full Entity Name, Audit Leader, Business Unit, Connectivity Total, Overall Residual Risk Rating, In Scope (Yes/No), Overdue (Yes/No), Handoff-to count, Handoff-from count, High/Critical risks list

### Edge Encoding

**Default view: handoffs only.** All other edge types start toggled OFF.

- Handoff edges (default ON): Solid lines, medium gray (#666), thicker if bidirectional
- Shared app edges (toggle, default OFF): Thin lines, light blue (#3498db), 50% opacity
- Shared vendor edges (toggle, default OFF): Thin lines, orange (#e67e22), 50% opacity
- Shared PRSA edges (toggle, default OFF): Thin dotted lines, light purple (#9b59b6), 30% opacity
- **Never show shared_model edges**

### Interactive Controls

Control panel (sidebar or top bar):

**Edge type toggles:** Checkboxes for Handoffs (default ON), Shared Apps, Shared Vendors, Shared PRSAs

**Audit Leader filter:** Dropdown or checkboxes to show/hide specific Audit Leader clusters

**Portfolio + Inbound Impact mode:** When a user selects an Audit Leader:
- Show all entities belonging to that leader (their portfolio)
- Also show any entity from a DIFFERENT leader that has a handoff-to edge pointing into the selected leader's entities
- Color portfolio entities normally
- Color external impacting entities in blue (#2980b9) with arrows pointing into the portfolio
- This answers: "whose work outside my portfolio can break my stuff?"

**Application/Vendor Focus mode:** Searchable dropdown listing all applications and vendors from the Asset Dependency Lookup. When selected:
- Show ONLY entities that depend on that asset
- Highlight the primary entity (control owner) with a star marker or double border
- Show handoff edges between visible entities
- Panel shows: Asset Name, Asset Type, dependent entity count, primary entity, count in scope vs not, count by risk rating

**Coverage filter:** Buttons for "All", "Not In Scope Only", "Overdue Only"

**Search:** Text box to find entity by name or ID — highlights entity and its immediate connections

**Reset view** button

### Legend
- Node colors (risk rating scale)
- Node shapes (in scope / not in scope / overdue)
- Edge types with visual styles
- Node size = Connectivity Total

### Title
"Audit Universe Network — Grouped by Audit Leader"

Subtitle: "Default view: handoff edges only. Toggle shared assets in the control panel. Node size = connectivity. Color = residual risk rating. Shape = audit plan coverage."

### Performance
- Use canvas rendering if using D3 (better performance than SVG at 400+ nodes)
- Edge toggles default to handoffs-only to manage density
- Consider pre-computing cluster positions rather than simulating all nodes at once
- Only draw edges for visible/filtered nodes

---

## File Structure

```
audit-universe-map/
├── CLAUDE.md              (this spec — Claude Code reads this)
├── data/
│   ├── input/
│   │   ├── dummy_audit_universe_50.csv
│   │   └── dummy_audit_plan.csv    (generated by pipeline or setup script)
│   └── output/
│       ├── layer1_output.xlsx
│       ├── edge_derivation_output.xlsx
│       ├── layer2_coverage_matrix.xlsx
│       └── network_visualization.html
├── src/
│   ├── pipeline.py        (main entry point — runs all stages)
│   ├── stage1_filter.py
│   ├── stage2_nodes.py
│   ├── stage3_risk_map.py
│   ├── stage4_relational.py
│   ├── stage5_lookups.py
│   ├── stage6_edges.py
│   ├── stage7_audit_cycle.py
│   ├── stage8_coverage.py
│   ├── stage9_visualization.py
│   └── utils/
│       ├── excel_writer.py
│       └── standardization.py
├── config/
│   ├── standardization_mappings.json (from AI prototype log)
│   └── horizontal_keywords.json
├── tests/
│   └── test_pipeline.py
└── requirements.txt       (pandas, openpyxl)
```

---

## Testing

Build and test entirely against `dummy_audit_universe_50.csv` (50 entities, semicolon delimiters). Generate a dummy audit plan by randomly selecting ~40% of active entity IDs.

Key assertions:
- Filtering removes special reviews (Audit Entity Type) and inactive entities (Audit Entity Status) — dummy data has 3 special reviews and 2 inactive = 45 remaining
- Multi-value parsing splits on semicolons and trims whitespace
- Edge derivation excludes models
- Concentration threshold = 10 dependent entities
- Connectivity Total excludes model edges
- Coverage flags fire correctly on known test cases
- All Excel outputs open cleanly and have correct sheet names

---

## Real Data Validation Benchmarks (from AI prototype run)

When the pipeline is eventually run on real data, use these to verify output matches:
- Nodes: 427
- Risk Map: 2,881
- Handoffs: 4,589 (45 unmatched IDs, 199 unmatched rows)
- Master edges (excluding models): ~7,200
- Isolated entities: 16
- Concentration flags: 22 assets at 10+ threshold
- Overdue: 92, Not overdue: 250, Unknown: 85
