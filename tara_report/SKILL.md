---
name: tara_report
version: 1.0.0
description: Generate three comprehensive TARA reports (Overall, Traceability, Multi-layer) from consolidated data catalogues. Enables stakeholder communication, compliance audit, and technical architecture review aligned with ISO 21434 Clause 8.4 (Work Products).
---
# TARA Report Generation -- Skill Workflow

## 1. When to Use This Skill

**Trigger ON** when the user is:
- Generating TARA (Threat Analysis and Risk Assessment) reports from completed data catalogues
- Creating executive summaries for risk review and stakeholder communication
- Preparing compliance evidence for ISO 21434 audit or UN R155 type approval
- Documenting complete traceability chains (Asset → DS → TS → AT → RT → CSG)
- Producing domain-specific risk analysis for security architecture review
- Asking about "generate report", "create TARA report", "export analysis", "audit evidence", "traceability matrix"
- Completing ISO 21434 Clause 8.4 (Work Products) documentation requirements
- After completing all TARA phases (damage scenarios, threat scenarios, risk treatment, cybersecurity goals)
- Updating reports after data catalogue changes (new threats, treatment decisions, goals)

**Trigger OFF** when the user asks:
- About individual damage scenario creation (use `damage_scenario` skill instead)
- About individual threat scenario creation (use `threat_scenario` skill instead)
- About individual risk treatment decisions (use `risk_treatment` skill instead)
- About individual cybersecurity goal derivation (use `csg` skill instead)
- About attack tree analysis (use `attack_tree` skill, if available)
- About editing reports directly (reports are DERIVED artifacts, never manually edited)
- About data entry or TARA analysis workflows (report generation is final output step)
- General ISO 21434 theory unrelated to report generation

---

## 2. Repository Quick Reference

This skill applies to the **TaraAgent** project for automotive cybersecurity TARA work.
Locate the repo root from the working directory -- do NOT hardcode any paths.

**Key directories** (relative to repo root):

```
data/                                Input data catalogues (prerequisite)
  ├── asset_list.md                  INPUT: Asset catalogue with CIA ratings
  ├── ds.md                          INPUT: Damage scenarios with SFOP impact scores
  ├── ts.md                          INPUT: Threat scenarios with AFR ratings
  ├── at.md                          INPUT: Attack trees (optional, multi-step attacks)
  ├── rt.md                          INPUT: Risk treatment decisions
  └── csg.md                         INPUT: Cybersecurity goals
reports/                             Output directory for generated reports (Markdown only)
  ├── overall_report.md              Overall risk assessment (executive view)
  ├── traceability_report.md         Complete traceability matrix (audit view)
  └── multilayer_report.md           Domain-grouped analysis (technical view)
skills/tara_report/                  This skill's files (references, templates)
  ├── SKILL.md                       This file (workflow guide)
  ├── assets/
  │   ├── OVERALL_REPORT_TEMPLATE.md          Template for Overall Report
  │   ├── TRACEABILITY_REPORT_TEMPLATE.md     Template for Traceability Report
  │   └── MULTILAYER_REPORT_TEMPLATE.md       Template for Multi-layer Report
  └── references/
      ├── tara-report-schema.md      Field definitions and validation rules
      └── tara-report-guide.md       Methodology and ISO 21434 mapping
```

**Workflow Overview**:
```
Data Files (5 required + 1 optional) → Validation → Report Generation → Output (3 Markdown reports)
```

**Prerequisites** (5 required + 1 optional):
- `data/asset_list.md` — Asset catalogue from asset_analysis skill **(required)**
- `data/ds.md` — Damage scenario catalogue from damage_scenario skill **(required)**
- `data/ts.md` — Threat scenario catalogue from threat_scenario skill **(required)**
- `data/at.md` — Attack tree catalogue from attack_tree skill **(optional, skip cross-domain chain analysis if absent)**
- `data/rt.md` — Risk treatment catalogue from risk_treatment skill **(required)**
- `data/csg.md` — Cybersecurity goal catalogue from csg skill **(required)**

**Data counts** (vary by project):
- Counts depend on the input data files in `data/` directory

---

## 3. Step-by-Step Workflow

### Success Criteria

Report generation is **complete** when ALL conditions are met:
1. All 3 report files exist in `reports/` (overall, traceability, multilayer)
2. Zero `{{PLACEHOLDER}}` text remains in any report
3. Counts are consistent across all 3 reports (TS, DS, RT, CSG totals match)
4. Generation timestamp recorded in `reports/GENERATION_LOG.txt`

### Step 1: Validate Data Prerequisites

**Before generating any report**, verify the 5 required data files exist (at.md is optional):

**Check 1: File existence**
```bash
# Verify 5 required files exist
test -f data/asset_list.md && test -f data/ds.md && test -f data/ts.md && \
test -f data/rt.md && test -f data/csg.md && \
echo "✓ All 5 required data files present" || echo "⚠️ Missing required data files"

# Check optional file
test -f data/at.md && echo "✓ at.md present (cross-domain chains enabled)" || echo "ℹ️ at.md absent (cross-domain chain analysis skipped)"
```

**Check 2: Data completeness**
```bash
# Check for critical sections in each file
grep -q "## Asset Catalogue" data/asset_list.md && echo "✓ asset_list.md valid"
grep -q "## Damage Scenario Catalogue" data/ds.md && echo "✓ ds.md valid"
grep -q "## Threat Scenario Catalogue" data/ts.md && echo "✓ ts.md valid"
grep -q "## Risk Treatment Catalogue" data/rt.md && echo "✓ rt.md valid"
grep -q "## Cybersecurity Goal Catalogue" data/csg.md && echo "✓ csg.md valid"
```

**Check 3: Traceability validation**
```bash
# Count TS entries
TS_COUNT=$(grep -oE 'TS-[A-Z]{2,5}-[0-9]{3}' data/ts.md | sort -u | wc -l)

# Count RT entries
RT_COUNT=$(grep -oE 'RT-[A-Z]{2,5}-[0-9]{3}' data/rt.md | sort -u | wc -l)

# Verify 1:1 TS-RT mapping by identifier parity
echo "TS: $TS_COUNT, RT: $RT_COUNT"
comm -3 \
  <(grep -oE 'TS-[A-Z]{2,5}-[0-9]{3}' data/ts.md | sed 's/^TS-/RT-/' | sort -u) \
  <(grep -oE 'RT-[A-Z]{2,5}-[0-9]{3}' data/rt.md | sort -u)
# Expect no output; RT-ID numbers must match the corresponding TS-ID numbers
```

**Validation criteria** (see `references/tara-report-guide.md` for full checklist):
- [ ] All 5 required data files exist with required sections (at.md optional)
- [ ] All TS-IDs have corresponding RT-IDs (1:1 treatment coverage)
- [ ] All DS-IDs referenced in TS exist in ds.md
- [ ] All AST-IDs referenced in DS exist in asset_list.md
- [ ] No orphan scenarios (< 5% orphan rate acceptable for DS only)

**If validation fails**: Fix source data files first, then regenerate reports. Do NOT generate reports from incomplete required data.

---

### Step 2: Generate Overall Report (Executive View)

**Purpose**: High-level risk summary for stakeholder communication and compliance status.

**Audience**:
- C-level executives (CEO, Chief Risk Officer)
- Regulatory compliance officers
- Board-level risk committees
- Insurance and risk transfer partners

**Contents** (11 sections):
- Executive summary with key findings
- Summary statistics (total threats, assets, treatments, goals)
- Risk value distribution (RV 1-5 breakdown with percentages)
- Treatment portfolio (Reduce/Avoid/Transfer/Accept breakdown)
- Top 5 highest-risk scenarios (RV ≥ 4 only)
- Domain risk breakdown (7 default domains: CAN/OTA/EXT/BCK/IVI/IMM/ADAS — project may define fewer or different domains; adapt domain list from `data/ts.md` TS-ID prefixes)
- SFOP impact analysis (Safety/Financial/Operational/Privacy dimensions)
- Cybersecurity goals summary (CIA property distribution)
- Compliance and standards references (ISO 21434, UN R155)
- Recommendations (immediate actions, strategic priorities)
- Audit trail (generation metadata, review date)

**Template reference**: `skills/tara_report/assets/OVERALL_REPORT_TEMPLATE.md`

**Key metrics**:
- Overall Risk Level (Critical/High/Medium/Low based on max RV present)
- Treatment Effectiveness % = (Reduce + Avoid + Transfer) / Total Treatments × 100
- Residual Risk Level (after all treatments applied)
- Asset Coverage % (% of assets with ≥1 identified threat)
- CSG Implementation % (% of CSG with ≥1 treatment implementation)

**Generation approach**:
1. Read template from `skills/tara_report/assets/OVERALL_REPORT_TEMPLATE.md`
2. Extract data from all data files (data/asset_list.md, ds.md, ts.md, at.md if present, rt.md, csg.md)
3. Calculate aggregate metrics:
   - Count totals per domain (CAN_THREAT_COUNT, IVI_THREAT_COUNT, etc.)
   - Calculate RV distribution (RV5_COUNT, RV5_PERCENT, RV4_COUNT, etc.)
   - Calculate treatment breakdown (REDUCE_COUNT, AVOID_COUNT, etc.)
   - Identify top 5 risks (sort by RV descending, filter RV ≥ 4)
   - Calculate SFOP high-impact counts (Safety ≥ 3, Financial ≥ 3, etc.)
   - Calculate CSG CIA property distribution
4. Substitute placeholders in template ({{UPPERCASE_SNAKE_CASE}} format)
5. Write output to `reports/overall_report.md`

**Validation after generation**:
```bash
# Verify output file exists
test -f reports/overall_report.md && echo "✓ Overall Report generated"

# Check for key sections
grep -q "## Executive Summary" reports/overall_report.md && echo "✓ Executive summary present"
grep -q "## Top 5 Highest Risk" reports/overall_report.md && echo "✓ Top risks documented"
grep -q "## Domain Risk Breakdown" reports/overall_report.md && echo "✓ Domain analysis present"
```

---

### Step 3: Generate Traceability Report (Audit View)

**Purpose**: Comprehensive bidirectional traceability (Asset → DS → TS → AT → RT → CSG) for development and audit.

**Audience**:
- Development teams (who implements CSGs?)
- QA/Verification teams (how to test CSGs?)
- ISO 21434 auditors
- Cybersecurity requirement writers

**Contents** (10 sections):
- Asset catalogue summary (total assets, orphan count)
- Complete traceability matrix (AST → DS → TS, TS → AT → RT, DS → RT → CSG)
- Complete end-to-end chains (example 6-element chain with all mappings)
- Orphan analysis (5 subsections: AST/DS/TS/RT/CSG orphans with recommendations)
- Coverage statistics (4 subsections: overall, domain-specific, risk value, CIA triad)
- Cross-reference index (6 subsections: AST/DS/TS/AT/RT/CSG with bidirectional links)
- Multi-domain dependencies (cross-domain threats, domain isolation score)
- Compliance and audit evidence (ISO 21434, UN R155 mapping)
- Traceability quality assessment (grade A-D with recommended actions)
- Report metadata (data sources, schema version, generation timestamp)

**Template reference**: `skills/tara_report/assets/TRACEABILITY_REPORT_TEMPLATE.md`

**Key metrics**:
- Complete Chains % (% of chains with all required elements: AST → DS → TS → RT → CSG; include AT context when `data/at.md` exists)
- Asset Coverage % (% of AST with ≥1 identified threat)
- DS Coverage % (% of DS with ≥1 threat scenario)
- TS Treatment Rate % (% of TS with documented RT decision)
- CSG Implementation % (% of CSG with ≥1 RT implementation)
- Orphan Artifacts count (AST/DS/TS/RT/CSG with broken traceability)

**Generation approach**:
1. Read template from `skills/tara_report/assets/TRACEABILITY_REPORT_TEMPLATE.md`
2. Build traceability matrices:
   - **AST → DS → TS**: For each AST, find DS-IDs from ds.md, then TS-IDs from ts.md
   - **TS → AT → RT**: For each TS, include related AT-IDs from `at.md` when present, then resolve the matching RT-ID from `rt.md`
   - **DS → RT → CSG**: For each DS, find RT-IDs via TS, then CSG-IDs from csg.md (M:N mapping)
3. Detect orphans:
   - AST with 0 DS/TS references (expect 0% orphan rate)
   - DS with 0 TS references (≤5% orphan rate acceptable)
   - TS with 0 RT references (expect 0% orphan rate)
   - RT with 0 CSG references (expect 0% orphan rate for Reduce/Avoid treatments)
   - CSG with 0 DS references or 0 RT implementations (expect 0% orphan rate)
4. Calculate coverage percentages
5. Build cross-reference index (bidirectional links for each artifact type)
6. Substitute placeholders in template
7. Write output to `reports/traceability_report.md`

**Orphan notation pattern** (12 occurrences in template):
```markdown
⚠️ ORPHAN: {{ARTIFACT_ID}} - {{ARTIFACT_TITLE}}
- **Issue**: [Description of broken traceability]
- **Impact**: [Consequence for TARA completeness]
- **Recommendation**: [Actionable fix]
```

**Validation after generation**:
```bash
# Verify output file exists
test -f reports/traceability_report.md && echo "✓ Traceability Report generated"

# Check for traceability chains
grep -q "Complete Traceability Chains" reports/traceability_report.md && echo "✓ Chain analysis present"

# Check for orphan detection
grep -q "Orphan Analysis" reports/traceability_report.md && echo "✓ Orphan detection included"

# Verify coverage statistics
grep -q "Coverage Statistics" reports/traceability_report.md && echo "✓ Coverage metrics present"
```

---

### Step 4: Generate Multi-Layer Report (Technical Architecture View)

**Purpose**: Domain-grouped analysis with cross-domain dependencies for security architecture review.

**Audience**:
- Security architects (system-level design review)
- Penetration testers (multi-step attack understanding)
- Threat modeling teams (attack chain validation)

**Contents** (per-domain sections + cross-domain analysis):
- **Per-domain analysis** (repeat for each domain discovered from `data/ts.md` TS-ID prefixes):
  - Domain summary (threat count, RV distribution, risk level)
  - Domain description (purpose, architecture, external interfaces)
  - Risk distribution (RV 5/4/3-1 counts)
  - Assets and attack surface (entry points, physical vs. remote access)
  - Threat scenarios (table: TS-ID | Title | RV | Treatment | CSG | Status)
  - Defense layers (controls at each architectural layer)
  - Residual risk (post-treatment RV distribution)
- **Cross-domain dependencies**:
  - Attack chains spanning multiple domains (EXT→IVI→CAN, BCK→OTA→IVI, etc.)
  - Domain isolation score (0=no isolation, 1=perfect isolation)
  - Gateway/controller dependencies (central points affecting multiple domains)
- **Security architecture summary**:
  - Defense-in-depth narrative (how layered controls prevent attacks)
  - Treatment effectiveness per domain
  - Cross-domain risk amplification

**Template reference**: `skills/tara_report/assets/MULTILAYER_REPORT_TEMPLATE.md`

**Key metrics per domain**:
- Domain Threats (count of TS-[DOMAIN]-* entries)
- Domain Risk Level (Critical/High/Medium/Low based on max RV in domain)
- Domain Treatment Effectiveness % (% of domain threats actively mitigated)
- Defense Layers (average number of CSGs per domain threat)
- Cross-Domain Threats (count of TS affecting multiple domains)

**Generation approach**:
1. Read template from `skills/tara_report/assets/MULTILAYER_REPORT_TEMPLATE.md`
2. Group data by domain:
   - Extract TS-CAN-* from ts.md, RT-CAN-* from rt.md, CSG-CAN-* from csg.md
   - Repeat for each domain present in `data/ts.md`
3. Calculate per-domain metrics (threat count, RV distribution, treatment effectiveness)
4. Identify cross-domain attack chains:
   - Extract AT-* entries from at.md where TS-IDs span multiple domains
   - Example: AT-EXT-001 uses TS-EXT-001 → TS-IVI-003 → TS-CAN-001
5. Calculate domain isolation score (measure of domain separation)
6. Substitute placeholders in template (domain-specific placeholders repeated 7 times)
7. Write output to `reports/multilayer_report.md`

**Validation after generation**:
```bash
# Verify output file exists
test -f reports/multilayer_report.md && echo "✓ Multi-layer Report generated"

# Check for discovered domain sections
grep -cE '^## (DOMAIN|Domain):' reports/multilayer_report.md
# Expected: count of generated domain sections

# Check for cross-domain analysis
grep -q "Cross-Domain Dependencies" reports/multilayer_report.md && echo "✓ Cross-domain analysis present"

# Verify defense-in-depth content
grep -q "Defense Layers" reports/multilayer_report.md && echo "✓ Defense layer analysis present"
```

---

### Step 5: Verify Report Outputs

**After generating all 3 reports**, perform final validation:

**Output file verification**:
```bash
# Verify all 3 reports exist (Markdown format)
test -f reports/overall_report.md && echo "✓ overall_report.md"
test -f reports/traceability_report.md && echo "✓ traceability_report.md"
test -f reports/multilayer_report.md && echo "✓ multilayer_report.md"
```

**Cross-report consistency checks**:

**Check 1: Count consistency** (total threat counts must match across all reports)
```bash
# Extract threat count from Overall Report
OVERALL_TS_COUNT=$(grep "Total Threat Scenarios:" reports/overall_report.md | grep -oE '[0-9]+')

# Extract threat count from Traceability Report
TRACE_TS_COUNT=$(grep "Total Threat Scenarios" reports/traceability_report.md | grep -oE '[0-9]+' | head -1)

# Compare
if [ "$OVERALL_TS_COUNT" -eq "$TRACE_TS_COUNT" ]; then
    echo "✓ Threat counts match across reports"
else
    echo "⚠️ Threat count mismatch: Overall=$OVERALL_TS_COUNT, Trace=$TRACE_TS_COUNT"
fi
```

**Check 2: RV distribution consistency** (RV breakdown must match)
- Overall Report RV counts = Sum of domain RV counts in Multi-layer Report
- Manual review: Compare RV 5/4/3/2/1 counts across reports

**Check 3: Treatment decision consistency** (RT-ID → Treatment Decision must be identical)
- Manual review: Check that same RT-ID shows same treatment in all reports
- No RT-ID should have conflicting treatment decisions

**Record generation timestamp**:
```bash
# Log report generation date
echo "Reports generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)" > reports/GENERATION_LOG.txt
```

**Quality assessment**:
- [ ] All 3 output files exist (3 Markdown reports)
- [ ] No placeholder text remains (all {{VARIABLES}} substituted)
- [ ] Counts are consistent across reports
- [ ] No broken internal links (all AST-ID/DS-ID/TS-ID references are valid)
- [ ] Generation log recorded

**If any check fails**: Review report generation logic, fix data inconsistencies, regenerate affected report(s).

---

## 4. Field-by-Field Guidance

**Note**: Report generation involves a large number of template placeholders across all three report types. Rather than duplicate field definitions here, refer to the authoritative schema document:

**Comprehensive field reference**: `skills/tara_report/references/tara-report-schema.md` (598 lines)

**Schema sections**:
- Overall Report Fields (8 categories)
  - Report Header, Risk Summary Statistics, Treatment Portfolio, Domain Breakdown, Impact Analysis (SFOP), Top Risk Scenarios, CSG Summary, Compliance References
- Traceability Report Fields (7 categories)
  - Asset Catalogue Summary, Asset-to-Threat Mapping, Damage Scenario Traceability, Attack Chain Documentation, Treatment-to-Goal Mapping, Complete Traceability Chain, Domain Traceability
- Multi-Layer Report Fields (7 categories)
  - Domain Summary (per domain), Domain Risk Distribution, Domain Assets and Attack Surface, Domain Treatment Strategy, Cross-Domain Dependencies, Domain Compliance, Domain Threat Scenarios Listing

**Validation rules** (from schema):
- All counts must be non-negative integers
- Sum of domain counts = Total Threat Scenarios
- All percentages sum to 100.0 ± 0.1
- Residual Risk Level ≤ Overall Risk Level
- Coverage percentages between 0-100
- Chain Completeness ≥ 90% indicates good coverage
- Orphan rates: Assets=0%, DS≤5%, TS=0%, RT=0%, CSG=0%

**Quick reference table** (most common placeholders):

| Category | Placeholder | Source | Calculation |
|----------|-------------|--------|-------------|
| Counts | {{TS_COUNT}} | data/ts.md | Count of TS-* entries |
| Counts | {{DS_COUNT}} | data/ds.md | Count of DS-* entries |
| Counts | {{RT_COUNT}} | data/rt.md | Count of RT-* entries |
| Counts | {{CSG_COUNT}} | data/csg.md | Count of CSG-* entries |
| Risk | {{RV5_COUNT}} | data/ts.md + ds.md | Count of TS with RV=5 |
| Risk | {{RV5_PERCENT}} | Calculated | (RV5_COUNT / TS_COUNT) × 100 |
| Treatment | {{REDUCE_COUNT}} | data/rt.md | Count of RT with Decision=Reduce |
| Treatment | {{TREATMENT_EFFECTIVENESS}} | Calculated | (Reduce+Avoid+Transfer) / RT_COUNT × 100 |
| Coverage | {{ASSET_COVERAGE}} | data/asset_list.md + ts.md | (Assets with ≥1 TS / Total Assets) × 100 |
| Coverage | {{CSG_IMPLEMENTATION}} | data/csg.md + rt.md | (CSG with ≥1 RT / Total CSG) × 100 |

For detailed field specifications, validation rules, and examples, consult `references/tara-report-schema.md`.

---

## 5. Common Patterns

See `references/common-patterns.md` for 5 stakeholder-specific usage patterns (executive review, audit prep, dev handoff, domain deep-dive, annual refresh).

---

## 6. Quality Checks

Before finalizing reports, run the validations from **Step 1** (data prerequisites) and **Step 5** (output verification). Then perform these additional checks:

### Placeholder Substitution Validation

**Check that all placeholders were substituted** (no {{VARIABLES}} remain):
```bash
for f in reports/overall_report.md reports/traceability_report.md reports/multilayer_report.md; do
  COUNT=$(grep -oE '\{\{[A-Z0-9_]+\}\}|\{[A-Z0-9_]+\}' "$f" 2>/dev/null | wc -l)
  echo "$f: $COUNT placeholders remaining (expect 0)"
done
```

**If placeholders remain**: Review template substitution logic, verify data extraction for missing placeholders, regenerate report.

---

### ISO 21434 Compliance Validation

**Verify ISO 21434 Clause 8.4 requirements met**:

| Clause Element | Report Location | Validation |
|----------------|-----------------|------------|
| Risk Analysis Results | Traceability Report (Section 2) | ✓ DS → TS → RT chain documented |
| Cybersecurity Goals | Overall Report (Section 7) + Traceability Report (Section 6.6) | ✓ CSG count, CIA property distribution |
| Goal Derivation | Traceability Report (Section 5) | ✓ RT → CSG mapping with M:N relationships |
| CIA Properties | Traceability Report (Section 5.4) | ✓ CSG CIA breakdown (C/I/A percentages) |
| Goal Verification | Multi-layer Report (Defense Layers) | ✓ CSG defense-in-depth narrative |

**Manual review checklist**:
- [ ] Overall Report includes ISO 21434 Clause 8.4 reference (Compliance section)
- [ ] Traceability Report documents complete AST → DS → TS → RT → CSG chains
- [ ] Multi-layer Report includes defense-in-depth analysis per domain
- [ ] All reports reference UN R155 Annex 5 threat categories
- [ ] Audit trail metadata includes generation date, data hash, schema version

---

## 7. References

**Internal References** (within this skill):
- `references/tara-report-schema.md` — Field definitions, validation rules, orphan detection thresholds
- `references/tara-report-guide.md` — Methodology, ISO 21434 Clause 8.4 compliance mapping, stakeholder distribution guide
- `references/common-patterns.md` — 5 stakeholder usage patterns (executive review, audit, dev handoff, domain review, annual refresh)
- `assets/OVERALL_REPORT_TEMPLATE.md` — Overall Report template
- `assets/TRACEABILITY_REPORT_TEMPLATE.md` — Traceability Report template
- `assets/MULTILAYER_REPORT_TEMPLATE.md` — Multi-layer Report template

**External Input Files** (from other skills):
- `data/asset_list.md` — Asset catalogue (output from `asset_analysis` skill, if available)
- `data/ds.md` — Damage scenario catalogue with Impact scores (output from `damage_scenario` skill)
- `data/ts.md` — Threat scenario catalogue with AFR scores (output from `threat_scenario` skill)
- `data/at.md` — Attack tree catalogue (output from `attack_tree` skill, optional)
- `data/rt.md` — Risk treatment catalogue (output from `risk_treatment` skill)
- `data/csg.md` — Cybersecurity goal catalogue (output from `csg` skill)

**ISO 21434 Standard**:
- **Clause 8.4**: Work Products — defines cybersecurity goals documentation requirements and traceability verification
- **Clause 8.5**: Cybersecurity Claims — defines claim structure for Accept/Transfer treatments
- **Clause 15**: Threat Analysis and Risk Assessment (TARA) — overall TARA process context
  - Clause 15.4-15.5: Damage scenario identification and impact assessment
  - Clause 15.6: Threat scenario identification
  - Clause 15.7: Attack path / attack tree analysis (if performed)
  - Clause 15.8: Risk assessment and treatment decision
  - Clause 15.9: Cybersecurity goals and requirements

**Related ISO Standards**:
- **ISO 31000:2018**: Risk management principles — provides general risk management framework
- **ISO 26262:2018**: Functional safety — ASIL ratings and safety risk management (complementary to cybersecurity)

**Automotive Cybersecurity Standards**:
- **UN R155 (UNECE Regulation 155)**: Cybersecurity and Cybersecurity Management System — mandatory for vehicle type approval
  - Annex 5: Threat categories (7 categories mapped in reports)
- **UN R156 (UNECE Regulation 156)**: Software Update and Software Update Management System

**Industry References**:
- **NIST SP 800-53**: Security and Privacy Controls for Information Systems — control reporting and compliance documentation patterns

---

## 8. Troubleshooting

### Issue 1: Missing Data Files Error

**Symptom**: Report generation fails with `FileNotFoundError: data/csg.md not found`

**Root Cause**: One or more required data files are missing (`asset_list.md`, `ds.md`, `ts.md`, `rt.md`, `csg.md`)

**Solution**:
1. Check which files are missing: `ls -la data/`
2. Complete missing TARA phase:
   - If `asset_list.md` missing → use `asset_analysis` skill (if available)
   - If `ds.md` missing → use `damage_scenario` skill
   - If `ts.md` missing → use `threat_scenario` skill
   - If `at.md` missing → optional (attack tree skill), may skip if not using attack chains
   - If `rt.md` missing → use `risk_treatment` skill
   - If `csg.md` missing → use `csg` skill
3. Retry report generation after all 5 required files exist (`at.md` remains optional)

**Prevention**: Always validate data prerequisites (Step 1 in workflow) before attempting report generation.

---

### Issue 2: Orphaned Threat Scenarios

**Symptom**: Traceability Report shows orphaned TS (threat scenario not linked to any DS)

**Root Cause**: Threat scenario enumerated but damage scenario impact not documented

**Solution**:
1. Review TS in `data/ts.md` with no DS references:
   ```bash
   # Find TS entries without DS references
   grep -E '^###? TS-' data/ts.md | while read ts; do
       TS_ID=$(echo "$ts" | grep -oE 'TS-[A-Z]{2,5}-[0-9]{3}')
       DS_COUNT=$(grep -c "$TS_ID" data/ds.md)
       if [ "$DS_COUNT" -eq 0 ]; then
           echo "⚠️ Orphan: $TS_ID (not referenced in any DS)"
       fi
   done
   ```
2. For each orphan TS:
   - **Option A**: Document what damage this threat causes (add DS entry with reference to TS-ID)
   - **Option B**: Remove TS if it's a false positive or non-material threat
3. Regenerate Traceability Report
4. Verify orphan count reduced to acceptable level (≤5% for DS, 0% for TS)

---

### Issue 3: Missing Cybersecurity Goals

**Symptom**: Reduce/Avoid risk treatment exists but no corresponding CSG in Traceability Report

**Root Cause**: CSG not created for some Reduce/Avoid treatments

**Solution**:
1. Review `data/rt.md` for Reduce/Avoid entries:
   ```bash
   # Find RT entries with Reduce/Avoid treatment but no CSG reference
   grep -E 'Treatment Decision.*Reduce|Treatment Decision.*Avoid' data/rt.md
   ```
2. For each Reduce/Avoid RT entry, verify corresponding CSG in `data/csg.md`:
   ```bash
   # Check if RT-IVI-001 has corresponding CSG
   grep -q "RT-IVI-001" data/csg.md && echo "✓ CSG exists" || echo "⚠️ CSG missing"
   ```
3. Create missing CSGs using `csg` skill (reference CSG derivation guide)
4. Update RT entries to reference new CSG-IDs
5. Regenerate Traceability Report
6. Verify CSG Implementation % ≥ 80% in Overall Report

**Note**: Accept/Transfer treatments do NOT require CSG (they use cybersecurity claims instead). Only Reduce/Avoid treatments require CSG.

---

### Issue 4: Risk Value Inconsistency

**Symptom**: Overall Report shows contradictory risk values for same scenario (RV 5 in one section, RV 4 in another)

**Root Cause**: Data file was manually edited; pre-mitigation and post-mitigation RV not recalculated

**Solution**:
1. **Never manually edit reports** — always fix source data and regenerate
2. Re-read `data/ds.md` and `data/ts.md` to verify Impact and AFR scores:
   - Impact Score (1-4) must match DS entry
   - AFR Score (0-15) must match TS entry
3. Recalculate Risk Value (RV) in `data/rt.md` if inputs changed:
   - Use Risk Value Matrix: Impact × AFR → RV (1-5)
   - See `references/rt-guide.md` for matrix
4. Verify Residual RV ≤ Original RV (treatments should improve or maintain risk)
5. Regenerate all 3 reports (Overall, Traceability, Multi-layer)
6. Compare RV values across reports to verify consistency

**Prevention**: Use `risk_treatment` skill workflow to calculate RV correctly. Do NOT manually edit RV values in data files.

---

### Issue 5: Count Mismatch Across Reports

**Symptom**: Overall Report shows "Total Threats: 21", but Multi-layer Report domain totals sum to 23

**Root Cause**: Placeholder substitution error or double-counting of cross-domain threats

**Solution**:
1. Verify actual threat count from source data:
   ```bash
   TS_COUNT=$(grep -cE '^###? TS-[A-Z]{2,5}-[0-9]{3}' data/ts.md)
   echo "Actual TS count: $TS_COUNT"
   ```
2. Check domain-specific counts:
   ```bash
   # Count per domain
   CAN_COUNT=$(grep -cE '^###? TS-CAN-[0-9]{3}' data/ts.md)
   IVI_COUNT=$(grep -cE '^###? TS-IVI-[0-9]{3}' data/ts.md)
   # ... (repeat for all 7 domains)
   
   # Sum domain counts
   DOMAIN_SUM=$((CAN_COUNT + IVI_COUNT + OTA_COUNT + EXT_COUNT + BCK_COUNT + IMM_COUNT + ADAS_COUNT))
   echo "Domain sum: $DOMAIN_SUM (should equal $TS_COUNT)"
   ```
3. If domain sum ≠ total count:
   - Check for TS-IDs with invalid domain codes (typos in ts.md)
   - Check for cross-domain threats counted twice (TS-ID should appear in only ONE domain)
4. Fix data inconsistencies in `data/ts.md`
5. Regenerate all 3 reports
6. Re-verify count consistency

**Note**: Cross-domain threats (TS affecting multiple domains) should still have only ONE primary domain in TS-ID. Cross-domain impacts are documented in "Affected Vehicle Systems" field, not in duplicate TS-IDs.

---

### Issue 6: Placeholder {{VARIABLE}} Remains in Generated Report

**Symptom**: Generated report Markdown contains `{{EXECUTIVE_SUMMARY_TEXT}}` instead of actual summary text

**Root Cause**: Placeholder substitution logic didn't populate this variable

**Solution**:
1. Identify which placeholder was not substituted:
   ```bash
   # Find all remaining placeholders in Overall Report
   grep -oE '\{\{[A-Z_]+\}\}' reports/overall_report.md | sort -u
   ```
2. For each missing placeholder, determine data source:
   - Review `assets/OVERALL_REPORT_TEMPLATE.md` to see where placeholder is used
   - Check `references/tara-report-schema.md` for placeholder definition
3. Common causes:
   - **Missing data**: If `{{RANK5_TS_ID}}` empty, verify that 5th-highest RV threat exists (may have fewer than 5 RV ≥ 4 threats)
   - **Calculation error**: If `{{TREATMENT_EFFECTIVENESS}}` empty, verify (Reduce+Avoid+Transfer) / RT_COUNT calculation
   - **Text placeholder**: If `{{EXECUTIVE_SUMMARY_TEXT}}` empty, generate 2-3 sentence summary from key findings
4. Populate missing placeholders with correct data
5. Regenerate report
6. Re-verify all placeholders substituted (0 remaining)

**Prevention**: Use template validation script to check all placeholders before distribution:
```bash
# Count placeholders (should be 0 after generation)
grep -c '{{' reports/overall_report.md
```

---

*End of TARA Report Generation Skill Workflow*
