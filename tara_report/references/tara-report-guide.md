# TARA Report Generation Methodology - ISO 21434 Compliance

This guide provides methodology for generating three complementary TARA reports in ISO 21434 compliance context, aligned with Clause 8.4 (Work Products) and the overall TARA deliverables framework.

---

## Overview

**TARA Reports** are derived views of the threat analysis and risk assessment data that communicate risk findings, traceability, and multi-layer attack dependencies to different stakeholders (technical teams, management, regulators).

**Key Characteristics**:
- Generated from 5 required data files plus optional `data/at.md` in `data/`
- Always regenerated (never manually edited) — reports are derived artifacts
- Fixed naming convention — overwrite on regeneration
- Three complementary report types with distinct purposes
- Markdown format for stakeholder distribution
- ISO 21434 compliant traceability and evidence

**Report Generation Prerequisite**:
```
TARA Data Completeness (5 Required Files + Optional Attack Trees):
  ├── data/asset_list.md       Asset catalogue with system boundaries
  ├── data/ds.md               Damage scenarios with SFOP impact scores
  ├── data/ts.md               Threat scenarios with AFR (Attack Feasibility Rating)
  ├── data/at.md               Attack trees (optional attack path chains)
  ├── data/rt.md               Risk treatment decisions (Avoid/Reduce/Transfer/Accept)
  └── data/csg.md              Cybersecurity goals derived from risk treatment
```

**Report Output Location**: `reports/` at project root (Markdown format)
```
reports/
  ├── overall_report.md
  ├── traceability_report.md
  └── multilayer_report.md
```

---

## When to Generate

### Trigger Conditions

Generate reports at these points in the TARA lifecycle:

#### 1. After TARA Completion
- All 5 required data files exist and are complete (`data/at.md` optional)
- All threat scenarios have been analyzed and rated
- All risk treatment decisions have been approved
- All cybersecurity goals have been derived
- External auditors or regulators request risk documentation

**Typical Timeline**: End of Phase 2 (Cybersecurity Goals) in ISO 21434 Clause 15 (Threat analysis and risk assessment)

---

#### 2. After Data Catalogue Updates
- New threat scenarios added to `data/ts.md`
- New damage scenarios added to `data/ds.md`
- Risk treatment decisions changed in `data/rt.md`
- Cybersecurity goals updated in `data/csg.md`
- Asset catalogue expanded in `data/asset_list.md`
- Attack tree dependencies modified in `data/at.md`

**Typical Scenario**: Mid-cycle threat modeling update (e.g., after security conference reveals new attack vector) or TARA re-analysis for model year refresh

---

#### 3. For Stakeholder Communication
- Executive summaries for management risk review
- Technical traceability for development teams
- Regulatory evidence for ISO 21434 audit
- Insurance or risk transfer documentation
- Supply chain or third-party risk assessment

---

### When NOT to Generate

- **Incomplete data**: Do not generate if any required data files are missing or incomplete
- **In-progress analysis**: Do not generate during TARA iteration unless snapshot is explicitly requested
- **Data validation failure**: Resolve validation errors (orphaned scenarios, broken references) before generation
- **Manual edits needed**: Never generate, then manually edit reports. Instead, fix source data and regenerate.

---

## Prerequisites

### Data Validation Checklist

Before generating any report, verify all data files pass validation:

**1. Asset Completeness** (`data/asset_list.md`):
- ✅ All vehicle domains identified (CAN, OTA, EXT, BCK, ADAS, IMM, IVI)
- ✅ Each asset has unique ID (A-[DOMAIN]-[NNN])
- ✅ Each asset has classification (safety-critical, connected, data-processing)
- ✅ No orphaned assets (every asset referenced in damage scenarios)

**2. Damage Scenario Completeness** (`data/ds.md`):
- ✅ All damage scenarios have unique ID (DS-[DOMAIN]-[NNN])
- ✅ SFOP impact scores assigned (Safety, Financial, Operational, Privacy)
- ✅ At least one domain-specific asset referenced for each DS
- ✅ Every DS severity ≥ 1 (skip negligible-only scenarios)
- ✅ No orphaned damage scenarios

**3. Threat Scenario Completeness** (`data/ts.md`):
- ✅ All threat scenarios have unique ID (TS-[DOMAIN]-[NNN])
- ✅ Attack Feasibility Rating (AFR) calculated (0-15 scale or High/Medium/Low)
- ✅ Each TS linked to one or more Damage Scenarios (what harm occurs if successful?)
- ✅ STRIDE and MITRE ATT&CK references valid
- ✅ No orphaned threat scenarios

**4. Attack Tree Completeness** (`data/at.md`, if present):
- ✅ Attack trees map multi-step attack chains
- ✅ Each AT-[DOMAIN]-[NNN] linked to constituent threat scenarios
- ✅ Attack tree provides context (doesn't replace per-TS risk treatment)

**5. Risk Treatment Completeness** (`data/rt.md`):
- ✅ Every threat scenario (TS-*) has corresponding treatment decision (RT-*)
- ✅ Treatment type assigned: Avoid, Reduce, Transfer, or Accept
- ✅ For Reduce treatments: control categories specified
- ✅ For Accept/Transfer: justification and approval documented
- ✅ Residual risk acknowledged (post-mitigation risk level)

**6. Cybersecurity Goal Completeness** (`data/csg.md`):
- ✅ Every Reduce/Avoid treatment has corresponding CSG (CSG-[DOMAIN]-[NN])
- ✅ Each CSG links to one or more Damage Scenarios
- ✅ CIA property assigned (Confidentiality, Integrity, or Availability)
- ✅ Goal statements are technology-agnostic SHALL statements
- ✅ No orphaned cybersecurity goals

**Validation Command**:
```bash
# Check for missing prerequisite files
test -f data/asset_list.md && test -f data/ds.md && test -f data/ts.md && \
test -f data/rt.md && test -f data/csg.md && echo "PASS: All required data files exist"

# Optional attack-tree context
test -f data/at.md && echo "PASS: Optional at.md present" || echo "INFO: Optional at.md absent"

# Check for critical sections in each file
grep -q "## Asset Catalogue" data/asset_list.md && echo "PASS: asset_list.md valid"
grep -q "## Damage Scenario Catalogue" data/ds.md && echo "PASS: ds.md valid"
grep -q "## Threat Scenario Catalogue" data/ts.md && echo "PASS: ts.md valid"
grep -q "## Risk Treatment Catalogue" data/rt.md && echo "PASS: rt.md valid"
grep -q "## Cybersecurity Goal Catalogue" data/csg.md && echo "PASS: csg.md valid"
```

---

## Report Generation Sequence

### Overview: Three-Report Strategy

The three reports address different audiences and use cases:

| Report | Audience | Purpose | Depth | Update Frequency |
|--------|----------|---------|-------|------------------|
| **Overall Report** | Management, Regulators | Executive summary of risk profile | High-level | After major changes |
| **Traceability Report** | Development teams, Auditors | Complete traceability matrix | Detailed | Per TARA cycle |
| **Multi-layer Report** | Security architects | Attack chains and defense-in-depth | Technical | When attack trees updated |

---

### Step 1: Generate Overall Report

**Purpose**: High-level risk summary and compliance status for executive stakeholders.

**Audience**:
- C-level executives (CEO, Chief Risk Officer)
- Regulatory compliance officers
- Board-level risk committees
- Insurance and risk transfer partners

**Contents**:
- Executive summary (TARA scope, compliance status)
- Risk distribution by domain (pie charts, heatmaps)
- Risk value histogram (RV 1-5 distribution)
- Treatment summary (% Reduce vs. Accept vs. Transfer)
- Top 10 highest-risk scenarios
- CSG count and CIA property distribution
- Key metrics (78 TS analyzed, X% mitigated, Y residual risk)

**Generation Method**:
Reports are generated manually using the templates in `skills/tara_report/assets/` by reading data from `/data/` files and replacing placeholders with actual values.

**Output Files**:
- `reports/overall_report.md` (comprehensive risk assessment)

**Validation**:
- ✅ Report contains risk distribution summary
- ✅ Treatment options enumerated (Reduce: X%, Accept: Y%, Transfer: Z%)
- ✅ No broken links to data files
- ✅ Markdown renders correctly

---

### Step 2: Generate Traceability Report

**Purpose**: Comprehensive bidirectional traceability (Asset → DS → TS → RT → CSG, with AT context when present) for development and audit.

**Audience**:
- Development teams (who implements CSGs?)
- QA/Verification teams (how to test CSGs?)
- ISO 21434 auditors
- Cybersecurity requirement writers

**Contents**:
- Full traceability matrix (Asset → DS ↔ TS → RT → CSG, plus AT context when available)
- Per-domain TS summary (CAN: 12 TS, OTA: 15 TS, ...)
- Risk treatment breakdown by domain
- Damage scenario → CSG mapping
- Threat scenario → Control category mapping
- Data lineage (which TS influenced which CSG?)
- Cross-reference indices (by domain, by risk value, by CIA property)

**Generation Method**:
Reports are generated manually using the templates in `skills/tara_report/assets/` by reading data from `/data/` files and replacing placeholders with actual values.

**Output Files**:
- `reports/traceability_report.md` (comprehensive bidirectional traceability matrix)

**Validation**:
- ✅ Every TS appears exactly once with treatment decision
- ✅ Every DS linked to at least one TS
- ✅ Every Reduce/Avoid TS has corresponding CSG row
- ✅ Accept/Transfer TS shows justification (not CSG)
- ✅ No missing cross-references

---

### Step 3: Generate Multi-Layer Report

**Purpose**: Defense-in-depth and attack chain analysis for security architects.

**Audience**:
- Security architects (system-level design review)
- Penetration testers (multi-step attack understanding)
- Threat modeling teams (attack chain validation)

**Contents**:
- Attack tree diagrams (if `data/at.md` exists)
- Multi-step attack dependencies (TS-A → TS-B → TS-C chains)
- Layered defense visualization (E-E-E-E model: Expose, Engage, Exploit, Execute)
- Per-layer risk residuals (after each mitigation layer)
- Attack feasibility by layer (how many steps required?)
- Defense gap analysis (which domains lack multi-layer defense?)

**Generation Method**:
Reports are generated manually using the templates in `skills/tara_report/assets/` by reading data from `/data/` files and replacing placeholders with actual values.

**Output Files**:
- `reports/multilayer_report.md` (domain-grouped attack chain analysis)

**Validation**:
- ✅ Attack trees match threat scenario IDs
- ✅ Multi-step chains show cumulative feasibility
- ✅ Each layer references corresponding CSG defense
- ✅ No dangling threat references in chains

---

## Report Generation Workflow

### Full Workflow: End-to-End

```bash
# 1. Validate data completeness
test -f data/asset_list.md && echo "✓ asset_list"
test -f data/ds.md && echo "✓ ds"
test -f data/ts.md && echo "✓ ts"
test -f data/rt.md && echo "✓ rt"
test -f data/csg.md && echo "✓ csg"
test -f data/at.md && echo "✓ optional at" || echo "ℹ️ optional at absent"

# 2. Create reports/ output directory if missing
mkdir -p reports/

# 3. Generate all three reports manually
# Use the TRACEABILITY_REPORT_TEMPLATE.md, MULTILAYER_REPORT_TEMPLATE.md, and OVERALL_REPORT_TEMPLATE.md
# from skills/tara_report/assets/ and replace {{PLACEHOLDERS}} with actual data from /data/ files

# 4. Verify output files exist
test -f reports/overall_report.md && echo "✓ overall_report"
test -f reports/traceability_report.md && echo "✓ traceability_report"
test -f reports/multilayer_report.md && echo "✓ multilayer_report"

# 5. Record generation timestamp
echo "Reports generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)" > reports/GENERATION_LOG.txt
```

---

## Decision Trees for Report Customization

### Decision Tree 1: Should I Generate Now?

```
START
  ├─ Are all 5 required data files present?
  │  ├─ NO  → STOP: Add missing required files first
  │  └─ YES ↓
  ├─ Does data pass validation checks?
  │  ├─ NO  → STOP: Fix validation errors, then regenerate
  │  └─ YES ↓
  ├─ Is generation triggered by:
  │  ├─ Scheduled (end of TARA phase)? → Generate all 3 reports
  │  ├─ Data update (single file changed)? → Generate affected report(s) only
  │  ├─ Stakeholder request (executive)? → Generate overall + traceability
  │  └─ Audit preparation? → Generate traceability + multilayer
  └─ END: Proceed to generation
```

### Decision Tree 2: Which Report Types to Generate?

```
What is the primary use case?
  ├─ Executive risk review / Board meeting
  │  └─ Generate: OVERALL + TRACEABILITY (show compliance status + risk distribution)
  ├─ Development team kickoff / CSG allocation
  │  └─ Generate: TRACEABILITY + MULTILAYER (show TS→CSG mapping + attack chains)
  ├─ ISO 21434 audit preparation
  │  └─ Generate: TRACEABILITY + MULTILAYER (complete traceability evidence)
  ├─ Penetration testing scoping
  │  └─ Generate: MULTILAYER (attack chains + feasibility)
  ├─ Insurance risk transfer negotiation
  │  └─ Generate: OVERALL + TRACEABILITY (executive summary + evidence)
  └─ Threat model refresh / model year update
     └─ Generate: ALL THREE (comprehensive new baseline)
```

### Decision Tree 3: Report Filtering and Customization

```
Do you need domain-specific filtering?
  ├─ YES → Specify --domains flag
  │  Example: --domains CAN,ADAS (generate reports for only these domains)
  └─ NO  → Generate for all domains (default)

Do you need risk-level filtering?
  ├─ YES → Specify --min-risk-value flag
  │  Example: --min-risk-value 3 (show only RV 3-5, hide RV 1-2)
  └─ NO  → Generate for all risk levels (default)

Do you need treatment-type filtering?
  ├─ YES → Specify --treatment-types flag
  │  Example: --treatment-types Reduce,Accept (show only active mitigation + accepted risks)
  └─ NO  → Generate for all treatments (default)

Do you need CIA property focus?
  ├─ YES → Specify --cia-focus flag
  │  Example: --cia-focus Integrity (show only Integrity CSGs and related threats)
  └─ NO  → Generate for all CIA properties (default)
```

---

## ISO 21434 Clause 8.4 Compliance Mapping

### Clause 8.4 Work Products

**Normative Requirement** (ISO 21434:2021, Section 8.4):
> "Cybersecurity goals shall be determined based on the risk analysis results."

**Traceability in TARA Reports**:

| Clause Element | Source Data | Report Location | Evidence |
|----------------|-------------|-----------------|----------|
| **Risk Analysis Results** | `data/ds.md`, `data/ts.md`, `data/rt.md` | Traceability Report (full matrix) | Damage scenario → Threat scenario → Risk treatment chain |
| **Cybersecurity Goals** | `data/csg.md` | Traceability Report (CSG section) + Multilayer Report (defense layer) | CSG-[DOMAIN]-[NN] with SHALL statement |
| **Goal Derivation** | Risk treatment decisions | Traceability Report (RT → CSG mapping) | Each CSG row shows source RT entry |
| **CIA Properties** | CSG definitions | Traceability Report (CSG CIA column) | Confidentiality, Integrity, or Availability classification |
| **Goal Verification** | CSG quality checks | Multilayer Report (defense-in-depth) | Goal addresses specific damage scenario |

---

### Clause 8.5 Compliance: Cybersecurity Claims

**Normative Requirement** (ISO 21434:2021, Section 8.5):
> "Cybersecurity claims shall be documented and justified for consciously accepted or transferred risks."

**Traceability in TARA Reports**:

| Clause Element | Source Data | Report Location | Evidence |
|----------------|-------------|-----------------|----------|
| **Risk Statement** | `data/rt.md` treatment rationale | Overall Report (risk summary) + Traceability Report (claim section) | DS-ID + RV + impact statement |
| **Justification** | RT approval notes + business case | Traceability Report (detailed claim) | Technical/business/legal rationale with specifics |
| **Approval Authority** | RT approval date/signature | Traceability Report (claim metadata) | Approver role + date + authorization level |
| **Residual Risk Acknowledgment** | Post-mitigation residual RV | Overall Report (risk residuals) + Traceability Report (residual column) | Explicit acknowledgment of remaining risk |

---

### Clause 15 Alignment: Overall TARA Process

**TARA Phases Covered by Reports**:

| ISO Phase | Data Source | Report Coverage | Verification |
|-----------|-------------|-----------------|--------------|
| **15.1 - Item Definition** | `data/asset_list.md` | Overall Report (scope statement) | Assets and system boundaries identified |
| **15.2 - Threat Analysis** | `data/ts.md` | Multilayer Report (threat chains) | TS enumerated with STRIDE/MITRE mapping |
| **15.3 - Vulnerability Analysis** | Implicit in TS AFR | Traceability Report (AFR column) | Attack feasibility rated (AFR 0-15) |
| **15.4 - Risk Analysis** | `data/ds.md` + `data/ts.md` | Overall Report (risk profile) | Impact × AFR = Risk Value (1-5) |
| **15.5 - Risk Evaluation** | Risk treatment decisions | Traceability Report (treatment column) | RV vs. acceptance criteria compared |
| **15.6-15.8 - Risk Treatment** | `data/rt.md` + `data/csg.md` | Traceability Report (full matrix) | Mitigation decisions + CSGs for Reduce/Avoid |

---

## Report Data Consistency Guarantees

### Invariants Maintained by Report Generation

The report generator enforces these consistency rules:

**Invariant 1: Damage Scenario Coverage**
- Every damage scenario (DS-*) in `data/ds.md` appears in reports
- No DS is orphaned (not linked to any TS or CSG)

**Invariant 2: Threat Scenario Traceability**
- Every threat scenario (TS-*) has exactly one risk treatment (RT-*)
- Every RT points back to its source TS

**Invariant 3: Goal Derivation**
- Every Reduce/Avoid treatment (RT-*) has corresponding CSG (CSG-*)
- Every Accept/Transfer treatment has corresponding claim (documented in RT)
- No CSG without backing RT

**Invariant 4: Risk Value Monotonicity**
- Residual risk ≤ Initial risk (mitigation does not increase risk)
- Pre-mitigation RV (from Impact × AFR) ≥ Post-mitigation RV

**Invariant 5: CIA Completeness**
- For each damage scenario, at least one CSG assigned (for Reduce/Avoid treatment)
- CIA properties cover all SFOP dimensions with score ≥ 2

**Validation Command** (verify invariants):
```bash
# Check for orphaned damage scenarios
grep "^## DS-" data/ds.md | wc -l > /tmp/ds_count.txt
grep "DS-[A-Z].*-[0-9]" data/ts.md | grep -o "DS-[A-Z]*-[0-9]*" | sort | uniq | wc -l > /tmp/ds_referenced.txt
diff /tmp/ds_count.txt /tmp/ds_referenced.txt && echo "PASS: No orphaned DS"

# Check for orphaned threat scenarios
grep "^## TS-" data/ts.md | wc -l > /tmp/ts_count.txt
grep "TS-[A-Z].*-[0-9]" data/rt.md | grep -o "TS-[A-Z]*-[0-9]*" | sort | uniq | wc -l > /tmp/ts_referenced.txt
diff /tmp/ts_count.txt /tmp/ts_referenced.txt && echo "PASS: No orphaned TS"
```

---

## Stakeholder Distribution Guide

### Who Gets Which Report?

| Stakeholder | Report(s) | Format | Update Cadence |
|---|---|---|---|
| **C-Level Executives** | Overall + Traceability (executive summary) | Markdown | Quarterly |
| **Board/Risk Committee** | Overall (1-page summary) | Markdown | Annually + ad-hoc |
| **ISO 21434 Auditors** | Traceability + Multilayer (complete evidence) | Markdown | On-demand |
| **Development Teams** | Traceability (TS→CSG mapping section) | Markdown | Per sprint |
| **Security Architects** | Multilayer (attack chains) + Traceability | Markdown | Bi-weekly |
| **Compliance Officers** | Overall (compliance status) + Traceability (audit trail) | Markdown | Monthly |
| **Insurance/Risk Partners** | Overall (risk profile) + Traceability (detailed breakdown) | Markdown | Annual renewal |

---

## Common Report Generation Scenarios

### Scenario 1: TARA Completion Handoff to Development

**Situation**: TARA analysis complete; team is transitioning to cybersecurity requirement writing.

**Reports to Generate**:
- Traceability Report (so dev teams can see TS→CSG mapping)
- Multilayer Report (so architects understand attack chains)

**Customization**: Filter to show only Reduce/Avoid CSGs (not Accept/Transfer)

**Distribution**: Development team shared folder + wiki

**Generation Method**: Use templates from `skills/tara_report/assets/` to manually generate reports by filtering to Reduce/Avoid treatments only.

---

### Scenario 2: Quarterly Executive Risk Review

**Situation**: Quarterly board meeting; risk committee needs high-level summary.

**Reports to Generate**:
- Overall Report (executive summary with key metrics)

**Customization**: Focus on top 10 highest-risk scenarios + risk distribution by domain

**Format**: Markdown (executive summary view)

**Generation Method**: Manually generate Overall Report using template from `skills/tara_report/assets/OVERALL_REPORT_TEMPLATE.md`, focusing on high-level metrics and top risks.

---

### Scenario 3: ISO 21434 Audit Preparation

**Situation**: External auditor requests evidence of cybersecurity goals and risk treatment.

**Reports to Generate**:
- Traceability Report (complete TS→DS→RT→CSG matrix)
- Multilayer Report (defense-in-depth evidence)

**Customization**: None (generate full data)

**Format**: Markdown (complete traceability matrix)

**Generation Method**: Reports are generated manually using templates in `skills/tara_report/assets/` by reading data from `/data/` files and replacing {{PLACEHOLDERS}} with actual values.

---

### Scenario 4: CAN Domain Deep Dive

**Situation**: Security team investigating CAN bus vulnerabilities after new threat intelligence.

**Reports to Generate**:
- Traceability Report (CAN domain only)
- Multilayer Report (CAN domain attack chains)

**Customization**: Domain filter for CAN

**Format**: Markdown (domain-specific view)

**Generation Method**: Reports are generated manually using templates in `skills/tara_report/assets/` by reading data from `/data/` files and replacing {{PLACEHOLDERS}} with actual values. Apply domain filter (e.g., CAN) by selecting only relevant threat scenarios and damage scenarios from the source data files.

---

## Troubleshooting Guide

### Issue 1: "Missing data file" Error

**Symptoms**: Report generation fails with `FileNotFoundError: data/csg.md not found`

**Root Cause**: Not all 5 required prerequisite data files exist

**Resolution**:
1. Check which files are missing: `ls -la data/`
2. Complete missing TARA phase (e.g., if `csg.md` missing, generate cybersecurity goals first)
3. Retry report generation

---

### Issue 2: Orphaned Threat Scenarios

**Symptoms**: Report shows orphaned TS (threat scenario not linked to any DS)

**Root Cause**: Threat scenario enumerated but damage scenario impact not documented

**Resolution**:
1. Review TS in `data/ts.md` with no DS references
2. Either: (a) Document what damage this threat causes (add DS entry), or (b) Remove TS if false positive
3. Regenerate Traceability Report

---

### Issue 3: Missing Cybersecurity Goals

**Symptoms**: Reduce/Avoid risk treatment exists but no corresponding CSG in report

**Root Cause**: CSG not created for some Reduce/Avoid treatments

**Resolution**:
1. Review `data/rt.md` for Reduce/Avoid entries
2. For each Reduce/Avoid RT, verify corresponding CSG in `data/csg.md`
3. Create missing CSGs (reference CSG derivation guide)
4. Regenerate Traceability Report

---

### Issue 4: Risk Value Inconsistency

**Symptoms**: Report shows contradictory risk values for same scenario

**Root Cause**: Data file was manually edited; pre-mitigation and post-mitigation RV not recalculated

**Resolution**:
1. Never manually edit reports; always fix source data
2. Re-read `data/ds.md` and `data/ts.md` impact/AFR scores
3. Recalculate Risk Value (RV) in `data/rt.md` if inputs changed
4. Regenerate all reports

---

## References

- **ISO/SAE 21434:2021** - Road vehicles — Cybersecurity engineering
  - Clause 8.4: Work products
  - Clause 8.5: Cybersecurity claims
  - Clause 15: Threat analysis and risk assessment
- **UN R155** - Cyber Security Management System (regulatory framework alignment)
- **Report Generation Schema**: `skills/tara_report/references/tara-report-schema.md` (if exists)
- **CSG Derivation Methodology**: `skills/csg/references/csg-guide.md`
- **Risk Treatment Methodology**: `skills/risk_treatment/references/rt-guide.md`

---

*End of TARA Report Generation Methodology Guide*
