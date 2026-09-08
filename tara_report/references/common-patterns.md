# TARA Report — Common Usage Patterns

These patterns describe typical stakeholder scenarios for report generation. They are **reference material**, not agent workflow steps. For the actual generation workflow, see `SKILL.md` §3.

---

## Pattern 1: Quarterly Executive Risk Review

**Scenario**: Board meeting requires high-level risk summary for stakeholder communication.

**Reports to Generate**:
- **Overall Report** (executive summary with key metrics)
- Optional: Traceability Report (if compliance questions expected)

**Customization**: Focus on top 5 highest-risk scenarios (RV ≥ 4) + risk distribution by domain

**Example workflow**:
1. Validate data prerequisites (Step 1)
2. Generate Overall Report
3. Extract key findings: Overall Risk Level, Treatment Effectiveness %, Top 5 Risks
4. Share Markdown report or convert to presentation slides externally

---

## Pattern 2: ISO 21434 Audit Preparation

**Scenario**: External auditor requests evidence of cybersecurity goals and risk treatment traceability.

**Reports to Generate**:
- **Traceability Report** (complete TS→DS→RT→CSG matrix)
- **Multi-layer Report** (defense-in-depth evidence)

**Example workflow**:
1. Validate data prerequisites (Step 1)
2. Run orphan detection: Verify orphan rates meet targets (Assets=0%, DS≤5%, TS=0%, RT=0%, CSG=0%)
3. Generate Traceability Report with full cross-reference index
4. Generate Multi-layer Report with per-domain compliance mapping
5. Provide auditor with Markdown reports and all data files

---

## Pattern 3: TARA Completion Handoff to Development

**Scenario**: TARA analysis complete; transitioning to cybersecurity requirement writing.

**Reports to Generate**:
- **Traceability Report** (so dev teams can see TS→CSG mapping)
- **Multi-layer Report** (so architects understand attack chains and defense layers)

**Example workflow**:
1. Validate data prerequisites (Step 1)
2. Generate Traceability Report with focus on RT-to-CSG mapping section
3. Generate Multi-layer Report with focus on defense layer analysis per domain
4. Publish to internal wiki or shared folder

---

## Pattern 4: Domain-Specific Security Review

**Scenario**: Security team investigating a specific domain (e.g., CAN bus) after new threat intelligence.

**Reports to Generate**:
- **Traceability Report** (filtered to target domain)
- **Multi-layer Report** (target domain section only)

**Example workflow**:
1. Validate data prerequisites (Step 1)
2. Extract domain-specific data (filter ts.md/rt.md/csg.md by domain prefix)
3. Generate domain-specific sections from both reports
4. Review with domain security architects

---

## Pattern 5: Annual TARA Refresh for Model Year Update

**Scenario**: New model year requires TARA re-analysis and updated risk documentation.

**Reports to Generate**: All three reports (comprehensive new baseline)

**Example workflow**:
1. Update all data files with new threats, treatments, goals for new model year
2. Archive previous year's reports: `mv reports/ reports-YYYY/`
3. Validate updated data prerequisites
4. Generate all 3 reports
5. Compare key metrics year-over-year (TS_COUNT, Overall Risk Level, Treatment Effectiveness %)
6. Document delta in executive summary
