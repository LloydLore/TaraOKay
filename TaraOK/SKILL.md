---
name: TaraOK
description: >-
  Master orchestration skill for automotive cybersecurity TARA (Threat Analysis and Risk Assessment) 
  per ISO 21434 and UN R155. Coordinates 9 sub-skills (asset_analysis, damage_scenario, threat_scenario, 
  attack_tree, risk_treatment, csg, csr, tara_report, tara_export) into unified workflow producing compliance-ready 
  work products. Triggers: "tara assessment", "iso 21434", "threat analysis", "risk assessment", 
  "automotive cybersecurity", "un r155", "start tara", "run tara". Handles multi-format input (png, docx, 
  xlsx, pdf) and produces data catalogues, reports, and publishable documentation. For single-project 
  TARA execution only.
---
# TaraOK -- ISO 21434 TARA Master Orchestrator

## 1. When to Use This Skill

**Trigger ON** when the user is:
- Starting a new ISO 21434 TARA (Threat Analysis and Risk Assessment) project
- Running complete TARA workflow from asset identification through documentation export
- Orchestrating multiple TARA phases (asset analysis, damage scenarios, threat scenarios, risk treatment, cybersecurity goals)
- Producing ISO 21434 Clause 8.4 compliant work products
- Asking about "iso 21434 tara", "automotive cybersecurity assessment", "un r155 compliance"
- Working with vehicle system architecture requiring comprehensive threat modeling
- Needing end-to-end TARA execution with progress tracking
- Generating compliance documentation for regulatory audit (UN R155, ISO 21434)

**Trigger OFF** when the user asks:
- About threat library management or cross-project threat enumeration (use `tara-maker` skill instead)
- About individual TARA phases in isolation without full workflow context
- About general cybersecurity concepts unrelated to automotive TARA
- About software build/test processes or deployment automation (out of scope)
- About vehicle design, engineering, or non-cybersecurity topics
- About cross-project TARA aggregation or fleet-level threat management

**CRITICAL DISTINCTION - TaraOK vs tara-maker**:
- **TaraOK** (this skill): Single-project TARA execution orchestrator (runs 9 phases for ONE vehicle system)
- **tara-maker**: Cross-project threat library manager (maintains reusable threat scenarios across projects)

Use TaraOK when executing TARA for a specific vehicle or system. Use tara-maker for building shared threat libraries.

---

## 2. Skill Source vs. Target Project Layout

This repository is the **TaraOK skill set source**. It does not need to contain a
real `data/`, `reports/`, `_build/`, or `output/` directory. Those directories
belong to the **target TARA project** where the skills are executed.

**Skill source layout** (this repository):

```
TaraOK/                         # Master orchestration skill
asset_analysis/                 # Phase 1 skill source
damage_scenario/                # Phase 2 skill source
threat_scenario/                # Phase 3 skill source
attack_tree/                    # Phase 4 skill source
risk_treatment/                 # Phase 5 skill source
csg/                            # Phase 6 skill source
csr/                            # Phase 7 skill source
tara_report/                    # Phase 8 skill source
tara_export/                    # Phase 9 skill source
```

**Target project layout** (runtime working directory, auto-detected):

```
input/                          # Reference documents (optional but recommended)
  ├── architecture/             # System diagrams, network topology
  ├── requirements/             # Security requirements, specifications
  └── reference/                # ISO 21434 PDF, threat libraries
data/                           # TARA work products (exportable package uses asset_list/ds/ts/rt/csg + optional at; full-run-with-CSRs also includes csr.md)
  ├── asset_list.md             # Phase 1: Asset catalogue with CIA ratings
  ├── ds.md                     # Phase 2: Damage scenarios with SFOP impact
  ├── ts.md                     # Phase 3: Threat scenarios with AFR ratings
  ├── at.md                     # Phase 4: Attack trees (optional)
  ├── rt.md                     # Phase 5: Risk treatment decisions
  ├── csg.md                    # Phase 6: Cybersecurity goals
  └── csr.md                    # Phase 7: Cybersecurity requirements
reports/                        # Phase 8: Generated reports (3 files)
  ├── overall_report.md         # Executive summary
  ├── traceability_report.md    # Audit evidence
  └── multilayer_report.md      # Technical architecture
docs/sphinx/                    # Phase 9: Sphinx source/configuration
  ├── conf.py                   # Sphinx configuration
  └── index.rst                 # Documentation entry point
_build/html/                    # Phase 9: HTML documentation site
output/pdf/                     # Phase 9: PDF reports (4 files)
  ├── tara_complete.pdf         # Complete archive (all generated source files)
  ├── overall_report.pdf        # Executive summary only
  ├── traceability_report.pdf   # Audit evidence (traceability + CSG)
  └── multilayer_report.pdf     # Technical review (multilayer + threats)
references/                     # External standards and references
  ├── ISO-21434.pdf             # ISO 21434 standard (user-provided)
  └── workflow.md               # TARA methodology reference
```

When a command mentions `skills/<skill-name>/`, it refers to an installed skill
inside a target project. In this source repository, use the top-level skill
directory name directly, for example `damage_scenario/tools/check_ds.py`.

**Workflow Overview**:
```
Input Documents → 9-Phase TARA → Compliance Work Products
                      ↓
  Phase 1: item definition + asset_analysis (asset_list.md)
  Phase 2: damage_scenario     (ds.md)
  Phase 3: threat_scenario     (ts.md)
  Phase 4: attack_tree         (at.md, optional)
  Phase 5: risk_treatment      (rt.md)
  Phase 6: csg                 (csg.md)
  Phase 7: csr                 (csr.md)
  Phase 8: tara_report         (reports/*.md; consumes asset_list/ds/ts/rt/csg + optional at)
  Phase 9: tara_export         (docs/sphinx/, _build/html/, output/pdf/)
```

**Prerequisites**:
- Python 3.10+ with `uv` installed (repository-standard Python toolchain)
- Pandoc 3.x (for PDF export)
- Sphinx 7.x + sphinx-book-theme + myst-parser (for documentation)
- LaTeX distribution (optional, for professional PDF typesetting)
- bun (optional, for JavaScript tooling)

**Installation verification**:
```bash
python --version   # 3.10+
uv --version       # Repository-standard Python toolchain available
pandoc --version   # 3.x
sphinx-build --version  # 7.x
```

---

## 3. TARA 9-Phase Workflow

### Overview

TaraOK orchestrates 9 sequential phases aligned with ISO 21434 Clauses 15.3-15.9, 9.4, and 8.4.
The workflow starts with an Item Definition Gate inside Phase 1: define the item,
the vehicle-level function(s), the component boundary, and the assets that live
in those components before enumerating damages or threats.

**Dependencies**:
- Item Definition Gate → Phase 1 asset enumeration (item/function/component boundary required before assets)
- Phase 1 → Phase 2 (assets and vehicle-level functions required for damage scenarios)
- Phase 2 → Phase 3 (damage scenarios drive threat enumeration)
- Phase 3 → Phase 5 (threats inform risk treatment)
- Phase 2 + Phase 5 → Phase 6 (damage + treatment → goals)
- Phase 6 → Phase 7 (CSGs required for CSR derivation)
- Phase 6 → Phase 8 (reports consume `asset_list.md`, `ds.md`, `ts.md`, `rt.md`, `csg.md`, plus optional `at.md`)
- Phase 6 + Phase 8 → Phase 9 (export consumes the Phase 8 report set plus the Phase 1-6 data contract; `csr.md` is not required by `tara_export`)

**Critical Rules**:
- TARA starts from Item Definition. Do not enumerate assets, damages, or threats before the vehicle-level function boundary is explicit.
- Phases 1-3 are MANDATORY and SEQUENTIAL
- Phase 4 (attack trees) is OPTIONAL but strongly recommended for complex systems
- **Phase 7 and Phase 8 are independent of each other** — both depend on Phase 6, but neither depends on the other. Phase 8 may run as soon as Phase 6 completes; Phase 7 may run in parallel or after.
- **Exportable package** means the `tara_export` prerequisites are satisfied: `data/asset_list.md`, `data/ds.md`, `data/ts.md`, `data/rt.md`, `data/csg.md`, `reports/overall_report.md`, `reports/traceability_report.md`, `reports/multilayer_report.md`, plus optional `data/at.md`. `data/csr.md` is NOT required by `tara_export`.
- **Full TaraOK run complete** means Phases 1-7 and Phase 8 have completed and validated. Phase 9 may publish an exportable package before CSR work is finished, but the orchestrated run is not "full-run-complete" until `data/csr.md` exists and passes Phase 7 validation.
- Each phase contributes work products to the overall ISO 21434 evidence set
- Do NOT skip phases (except Phase 4); each builds on prior outputs

---

### Phase Execution Reference

Each phase delegates to a sub-skill. The orchestrator's job is to **invoke the sub-skill, pass inputs, and validate outputs** — not to replicate the sub-skill's internal process.

#### Phase 1: Item Definition + Asset Analysis (Clause 9.3 / 15.3)

**Skill**: `asset_analysis` | **Output**: `data/asset_list.md`

**Inputs**: System architecture diagrams, network topology, vehicle-level function description, software inventory, external interface specifications (from `input/`)

**Validation**:
- Item / TOE boundary is documented before asset entries
- Vehicle-level function(s) implemented by the item are explicit
- Components constituting the item are listed or explicitly unknown
- All security-relevant assets documented
- Each asset has all 7 required fields (ID, Name, Description, Category, CIA Rating, Interfaces, Related Systems)
- CIA ratings justified with impact analysis
- Asset IDs unique and follow format AST-[CODE]-[NNN], where CODE ∈ {HW, SW, FW, DAR, DIT, DIU}

---

#### Phase 2: Damage Scenario Analysis (Clause 15.4-15.5)

**Skill**: `damage_scenario` | **Output**: `data/ds.md`

**Inputs**: `data/asset_list.md`, business impact context, safety standards (ISO 26262 ASIL ratings)

**Validation**:
- All high-CIA assets have corresponding damage scenarios
- Each DS identifies the affected vehicle-level function or function cluster
- Each DS states what Function with RISK reaches the road user or stakeholder
- Each DS has all 7 required fields (DS-ID, Title, Linked Assets, SFOP Dimensions, Impact Score, Rationale, Assessment Context)
- Impact Score correctly calculated as MAX(S, F, O, P)
- SFOP scores justified with regulatory context (GDPR, UN R155, ISO 26262)

---

#### Phase 3: Threat Scenario Enumeration (Clause 15.6)

**Skill**: `threat_scenario` | **Output**: `data/ts.md`

**Inputs**: `data/asset_list.md`, `data/ds.md`, threat frameworks (STRIDE, MITRE ATT&CK, OWASP, UN R155 Annex 5)

**Validation**:
- All damage scenarios have at least one threat scenario
- Each TS contains the required core fields; extended metadata is present only where evidence or reporting needs it
- AFR calculations include all 5 factors with justifications
- Framework mappings accurate (STRIDE category, MITRE technique ID, etc.)

---

#### Phase 4: Attack Tree Analysis (Clause 15.7, OPTIONAL)

**Skill**: `attack_tree` | **Output**: `data/at.md`

**Inputs**: `data/asset_list.md`, `data/ds.md`, `data/ts.md`

**When to use**: System has multi-step attacks requiring AND/OR/SEQ logic. Skip if attacks are straightforward single-path.

**Validation**:
- All trees have valid root goal (DS-ID from ds.md)
- Leaf nodes reference real threats (TS-IDs from ts.md)
- AFR aggregation logic documented for each path
- Critical path identified with justification

---

#### Phase 5: Risk Treatment Decision (Clause 15.8)

**Skill**: `risk_treatment` | **Output**: `data/rt.md`

**Inputs**: `data/asset_list.md`, `data/ds.md`, `data/ts.md`, `data/at.md` (optional), security control database

**Validation**:
- All TS-IDs have corresponding RT-IDs (1:1 relationship)
- Each RT has all 14 required fields (RT-ID, Title, Related TS-ID, Related DS-ID, Impact, AFR, RV, Treatment Decision, etc.)
- Risk Value correctly calculated from Impact × AFR matrix
- Reduce treatments include control categories and residual AFR
- Accept treatments include formal documentation (Risk Level, Rationale, Approval Authority, Review Date)

---

#### Phase 6: Cybersecurity Goals Derivation (Clause 15.9)

**Skill**: `csg` | **Output**: `data/csg.md`

**Inputs**: `data/ds.md`, `data/rt.md`

**Validation**:
- All Avoid/Reduce/Transfer-with-active-mitigation treatments have corresponding CSG (may be M:N relationship)
- Each CSG has all 9 required fields (CSG-ID, Title, Related DS-IDs, Related RT-IDs, Goal Statement, CIA Property, Cybersecurity Claim, Rationale, Last Updated)
- Goal statements use "shall" language and are technology-agnostic
- CIA property aligns with SFOP dimensions of related DS-IDs
- Pure Accept / pure Transfer claims stay authoritative in `data/rt.md` with the required approval / rationale elements; the `Cybersecurity Claim` field in `data/csg.md` remains empty

---

#### Phase 7: Cybersecurity Requirements Derivation (Clause 9.4)

**Skill**: `csr` | **Output**: `data/csr.md`

**Inputs**: `data/csg.md`, `data/rt.md`, `data/ts.md`, `data/at.md` (optional), design specifications

**Validation**:
- All CSGs with Reduce/Avoid treatment have corresponding CSRs (1:N relationship)
- Each CSR has all required fields (CSR-ID, Title, CSR Type, Related CSG-IDs, Category, Description, Specification Reference, Implementation Status, Verification Method, Priority, Risk Reference, Last Updated)
- Each CSR identifies an allocation target: Item, Component, layer, interface, or supplier-owned subsystem
- Part A entries include specification references (source documentation)
- Part B entries include gap descriptions and CRITICAL/HIGH/MEDIUM/LOW priority
- Traceability: CSR → CSG → RT → TS → DS → Asset chain complete

---

#### Phase 8: TARA Report Generation (Clause 8.4)

**Skill**: `tara_report` | **Output**: `reports/overall_report.md`, `traceability_report.md`, `multilayer_report.md`

**Inputs**: `data/asset_list.md`, `data/ds.md`, `data/ts.md`, `data/rt.md`, `data/csg.md`, plus `data/at.md` if present. (`data/csr.md` is NOT required.)

**Validation**:
- All 3 reports generated without errors
- Count consistency across reports (total threats same in all 3)
- No placeholder text remains (all {{VARIABLES}} substituted)
- Traceability matrix shows complete required chains (AST → DS → TS → RT → CSG) and includes AT context when present
- Orphan rates within thresholds (Assets=0%, DS≤5%, TS=0%, RT=0%, CSG=0%)

---

#### Phase 9: TARA Documentation Export (Clause 8.4)

**Skill**: `tara_export` | **Output**: `_build/html/`, `output/pdf/*.pdf` (4 files)

**Inputs**: Data files from Phases 1-6, all 3 report files from Phase 8, Sphinx configuration template

**Output details**:
- `_build/html/` — browseable documentation site
- `output/pdf/tara_complete.pdf` — complete archive (all generated source files)
- `output/pdf/overall_report.pdf` — executive summary (for C-suite)
- `output/pdf/traceability_report.pdf` — traceability + CSG (for auditors)
- `output/pdf/multilayer_report.pdf` — multi-layer + threats + attack trees (for technical team)

**Validation**:
- Sphinx HTML site loads correctly (`_build/html/index.html` + all exported source pages)
- All 4 PDFs generated (no 0-byte files)
- PDF metadata populated (Title, Author, Subject, Keywords)
- Search functionality works in HTML output
- PDF bookmarks present (table of contents navigation)

---

## 4. Multi-Format Input Handling

TaraOK accepts reference documents in multiple formats:

| Format  | Tool                              | Use Case                                         |
|---------|-----------------------------------|--------------------------------------------------|
| PNG/JPG | OCR (tesseract) or `look_at` tool | System diagrams, architecture screenshots        |
| DOCX    | Read tool                         | Requirements specifications, system descriptions |
| XLSX    | Read tool                         | Asset inventories, component catalogues          |
| PDF     | Read tool                         | Standards (ISO 21434), regulations (UN R155)     |

**Note**: All extracted data must be validated and formatted into Markdown work products (`data/*.md`). Input files are reference only; TARA analysis happens in Markdown.

---

## 5. Target Project Prerequisite Validation

Before starting TARA execution, verify:

```bash
# Environment
python --version        # 3.10+
uv --version            # Repository-standard Python toolchain available
pandoc --version        # 3.x
sphinx-build --version  # 7.x

# Target project structure
mkdir -p input/{architecture,requirements,reference} data reports docs/sphinx references _build/html output/pdf
```

**Validation checklist**:
- [ ] Python 3.10+ installed
- [ ] `uv` available for the repository-standard Python workflow
- [ ] Pandoc 3.x installed
- [ ] Sphinx + sphinx-book-theme + myst-parser installed
- [ ] Project directories created (input/, data/, reports/)
- [ ] Input documents populated (architecture, requirements)
- [ ] ISO 21434 PDF available in references/ (recommended)

**If validation fails**: Install missing tools, create directories, populate input documents before starting Phase 1.

---

## 6. ISO 21434 Clause Mappings

| ISO 21434 Clause | Topic                                    | TaraOK Phase | Work Product         | Sub-Skill         |
|------------------|------------------------------------------|--------------|----------------------|-------------------|
| 9.3 / 15.3       | Item definition and asset identification | Phase 1      | `data/asset_list.md` | `asset_analysis`  |
| 15.4-15.5        | Damage scenario definition               | Phase 2      | `data/ds.md`         | `damage_scenario` |
| 15.6             | Threat scenario identification           | Phase 3      | `data/ts.md`         | `threat_scenario` |
| 15.7             | Attack path analysis                     | Phase 4      | `data/at.md`         | `attack_tree`     |
| 15.8             | Risk treatment decision                  | Phase 5      | `data/rt.md`         | `risk_treatment`  |
| 15.9             | Cybersecurity goals                      | Phase 6      | `data/csg.md`        | `csg`             |
| 9.4              | Cybersecurity specifications             | Phase 7      | `data/csr.md`        | `csr`             |
| 8.4              | Work products documentation              | Phase 8      | `reports/*.md`       | `tara_report`     |
| 8.4              | Work products publication                | Phase 9      | Sphinx docs, PDFs    | `tara_export`     |

**UN R155 Alignment**:
- Annex 5 threat categories mapped in Phase 3 (threat_scenario skill)
- Audit-supporting cybersecurity evidence is consolidated across Phases 7-9 outputs

**Compliance Verification**:
- Phase 8-9 produce the derived ISO 21434 Clause 8.4 work products for reporting and publication
- Traceability matrix in Phase 8 demonstrates complete chain (AST → DS → TS → RT → CSG), with attack-tree context when available
- Export in Phase 9 provides audit-ready documentation (HTML site + PDFs)

---

## 7. Progress Tracking and Troubleshooting

**Workflow Execution Model**:
- **Sequential phases**: Must complete Phase N before starting Phase N+1 (except Phase 4 optional, and Phase 7/8 parallel — see Critical Rules)
- **Stop on failure**: If a phase fails validation, halt workflow and report error
- **Partial run support**: Can resume from any phase if prior outputs exist

**Progress Reporting**:
```
TARA Progress: Phase N/9 - [Phase Name]
Status: [In Progress | Complete | Failed]
Output: [File path if complete]
Next: [Phase N+1 or COMPLETE]
```

**Resume support** — check which phases are complete:
```bash
for f in data/asset_list.md data/ds.md data/ts.md data/at.md data/rt.md data/csg.md data/csr.md; do
  test -f "$f" && echo "✓ $f" || echo "⚠ $f missing"
done
```

**Common Issues**:

| Issue                            | Phase | Solution                                                                                                                                                   |
|----------------------------------|-------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Missing architecture documents   | 1     | Populate `input/architecture/` before running                                                                                                              |
| Invalid CIA ratings (not 1-4)    | 1     | Fix in `data/asset_list.md`, rerun validation                                                                                                              |
| Missing `asset_list.md`          | 2     | Run Phase 1 first                                                                                                                                          |
| SFOP scores outside 1-4          | 2     | Fix scores per SFOP scale in `damage_scenario` skill                                                                                                       |
| AFR factors not summing 0-15     | 3     | Check 5-factor breakdown in `threat_scenario` skill                                                                                                        |
| TS count ≠ RT count              | 5     | Every TS needs an RT. Find orphans: `grep -oE 'TS-[A-Z]{2,5}-[0-9]{3}' data/ts.md \| sort -u` vs `grep -oE 'RT-[A-Z]{2,5}-[0-9]{3}' data/rt.md \| sort -u` |
| Missing `csg.md` for Phase 7     | 7     | Run Phase 6 first                                                                                                                                          |
| Traceability mismatch in reports | 8     | Reconcile orphan TS/RT entries before generating reports                                                                                                   |
| `myst_parser` not found          | 9     | `pip install myst-parser`                                                                                                                                  |
| Pandoc not found                 | 9     | Install Pandoc 3.x from https://pandoc.org/installing.html                                                                                                 |
| LaTeX errors                     | 9     | Install `texlive-latex-extra texlive-fonts-recommended` (Ubuntu) or MacTeX (macOS)                                                                         |
| Can I skip Phase 4?              | 4     | Yes. Attack trees are OPTIONAL. Downstream phases include AT context only when `data/at.md` exists.                                                        |

**File Update Policy**: TaraOK follows the sub-skill contract for each artifact. Derived outputs such as `reports/*.md`, `_build/html/`, and `output/pdf/*.pdf` are regenerated, while phase skills with append-only rules (for example `attack_tree` appending to `data/at.md`) keep their stricter behavior.

---

## 8. Runtime Success Criteria

These criteria apply to a **target TARA project after TaraOK runs**. They are not
requirements for this skill source repository.

**Phase-Specific Success**:

| Phase | Criterion                                                                                                                            |
|-------|--------------------------------------------------------------------------------------------------------------------------------------|
| 1     | `data/asset_list.md` exists, item/function boundary is documented, all assets have AST-ID and CIA ratings                            |
| 2     | `data/ds.md` exists, all DS have affected functions, SFOP scores, and Impact = MAX(SFOP)                                             |
| 3     | `data/ts.md` exists, all TS have AFR 0-15 and framework mappings                                                                     |
| 4     | `data/at.md` exists (if run), trees have valid root goals and AFR aggregation                                                        |
| 5     | `data/rt.md` exists, RT count = TS count (1:1), all have treatment decisions                                                         |
| 6     | `data/csg.md` exists, all Avoid/Reduce/Transfer-with-active-mitigation RT have CSG, pure Accept/Transfer claims stay in `data/rt.md` |
| 7     | `data/csr.md` exists, all CSGs for active mitigation treatments have corresponding CSRs                                              |
| 8     | All 3 reports in `reports/`, counts consistent, Phase 8 uses finalized `tara_report` contract                                        |
| 9     | Sphinx HTML site + 4 PDFs generated, all files >0 bytes                                                                              |

**Overall Success**:
- All full-run data files exist (`data/asset_list.md`, `ds.md`, `ts.md`, `rt.md`, `csg.md`, `csr.md`), with item/function boundary captured in `asset_list.md` and `at.md` present when attack trees were produced
- All 3 reports exist in `reports/`
- Traceability matrix shows complete required chains (AST → DS → TS → RT → CSG), with AT context when present
- No orphan artifacts (all TS have RT, all active-mitigation RT have CSG)
- ISO 21434 Clause 8.4 compliant work products produced
- Sphinx HTML documentation builds without errors
- 4 PDFs generated with non-zero size

**Verification**:
```bash
# Verify full-run data set
for f in data/asset_list.md data/ds.md data/ts.md data/rt.md data/csg.md data/csr.md; do
  test -f "$f" && echo "✓ $f" || echo "⚠ $f missing"
done

# Verify reports and exports
test -f reports/overall_report.md && test -f reports/traceability_report.md && \
test -f reports/multilayer_report.md && echo "✓ Reports present" || echo "⚠ Missing reports"
for f in output/pdf/tara_complete.pdf output/pdf/overall_report.pdf output/pdf/traceability_report.pdf output/pdf/multilayer_report.pdf; do
  test -f "$f" && test -s "$f" && echo "✓ $f" || echo "⚠ $f missing or empty"
done

# Verify traceability (TS count should equal RT count)
ts_count=$(grep -oE 'TS-[A-Z]{2,5}-[0-9]{3}' data/ts.md | sort -u | wc -l)
rt_count=$(grep -oE 'RT-[A-Z]{2,5}-[0-9]{3}' data/rt.md | sort -u | wc -l)
[ "$ts_count" = "$rt_count" ] && echo "✓ TS/RT count match ($ts_count)" || echo "⚠ TS=$ts_count RT=$rt_count"

# Check Sphinx build
test -f _build/html/index.html && echo "✓ Sphinx build successful"
```

---

## 9. Key References

**Workflow Methodology**:
- `references/workflow.md` — Complete 9-phase TARA workflow description

**Sub-Skill Documentation** (see each skill's SKILL.md for detailed process):
- `asset_analysis` — Phase 1 asset identification
- `damage_scenario` — Phase 2 SFOP impact assessment
- `threat_scenario` — Phase 3 AFR calculation
- `attack_tree` — Phase 4 multi-step attack modeling
- `risk_treatment` — Phase 5 control selection
- `csg` — Phase 6 goal derivation
- `csr` — Phase 7 cybersecurity requirement derivation
- `tara_report` — Phase 8 report generation
- `tara_export` — Phase 9 Sphinx/PDF export

**Standards and Regulations**:
- **ISO/SAE 21434:2021** — Cybersecurity engineering for road vehicles
- **UN R155** — Cybersecurity and software update management (EU/UN regulation)
- **ISO 26262:2018** — Functional safety (complementary to cybersecurity)
- **GDPR** — Privacy data protection (informs Privacy impact scoring)
- **China GB 44495** — Automotive data security requirements

**Security Frameworks**:
- **STRIDE** — Threat categorization (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)
- **MITRE ATT&CK** — Attack technique enumeration (ICS and Enterprise matrices)
- **OWASP** — Security best practices (IoT Top 10, API Top 10, Mobile Top 10)
- **UN R155 Annex 5** — Automotive threat categories (7 categories for type approval)

---

**End of TaraOK Master Skill**
