# ISO 21434 TARA 9-Phase Workflow Reference

## Overview

This document outlines the complete **Threat Analysis and Risk Assessment (TARA)** workflow aligned with **ISO/SAE 21434** cybersecurity standards and **UN R155** automotive regulations. The workflow comprises 9 interdependent phases that transform raw asset inventories into actionable cybersecurity goals and control recommendations.

**Key Standards**: 
- ISO 21434 Clauses 15.3-15.9 (Threat Analysis & Risk Assessment cycle)
- Clause 8.4 (Work Products documentation requirements)
- UN R155 Annex 5 (Attack vector enumeration framework)

---

## 9-Phase Workflow Architecture

```
Phase 1: Item Definition + Asset Analysis    [Clause 9.3 / 15.3]
         ↓ (freezes item/function/component boundary, produces data/asset_list.md)
Phase 2: Damage Scenario Analysis            [Clause 15.4-15.5]
         ↓ (produces data/ds.md with SFOP Impact scores)
Phase 3: Threat Scenario Enumeration         [Clause 15.6]
         ↓ (produces data/ts.md with AFR scores)
Phase 4: Attack Tree Analysis (Optional)     [Clause 15.7]
         ↓ (produces data/at.md, multi-step attack paths)
Phase 5: Risk Treatment Decision             [Clause 15.8]
         ↓ (produces data/rt.md with treatment decisions, controls, and RT-owned claims)
Phase 6: Cybersecurity Goals Derivation      [Clause 15.9]
         ↓ (produces data/csg.md with active-mitigation cybersecurity goals)
Phase 7: Cybersecurity Requirements Derivation [Clause 9.4]
         ↓ (produces data/csr.md with technical requirements)
Phase 8: TARA Report Generation              [Clause 8.4]
         ↓ (produces reports/ with compliance documentation)
Phase 9: TARA Documentation Export           [Clause 8.4]
         ↓ (produces publishable Sphinx docs + PDF reports)
         FINAL: ISO 21434 COMPLIANT WORK PRODUCTS
```

---

## Phase Details

### Phase 1: Item Definition + Asset Analysis (Clause 9.3 / 15.3)
**Skill**: `asset_analysis`  
**Input**: Vehicle system architecture, network diagrams, software inventory  
**Output**: `data/asset_list.md` — Item/function boundary plus comprehensive inventory of all security-relevant assets

**Methodology**:
- Define the item / TOE and the vehicle-level function(s) it implements
- Record constituent components and item boundary assumptions
- Identify hardware assets (ECUs, sensors, infotainment systems, communication bus, connectors)
- Identify software assets (firmware, applications, libraries, protocols)
- Identify data assets (vehicle telemetry, user PII, diagnostic information)
- Document asset boundaries, communication interfaces, and trust levels
- Assign unique asset identifiers (AST-DOMAIN-NNN)

**ISO 21434 Requirement**: Define the item and its vehicle-level function before documenting components and assets subject to threats. Record sufficient technical detail for threat modelers to reason about attack surfaces.

---

### Phase 2: Damage Scenario Analysis (Clauses 15.4-15.5)
**Skill**: `damage_scenario`  
**Input**: `data/asset_list.md` (asset inventory)  
**Output**: `data/ds.md` — Damage scenarios with SFOP Impact ratings

**Methodology**:
Damage scenarios describe adverse outcomes if assets are compromised. Each damage scenario receives an **Impact Score (1-4)** derived from **SFOP scale**:
- Each damage scenario identifies the affected vehicle-level function or function cluster
- Each damage scenario states the Function with RISK delivered to the road user or stakeholder

**SFOP Scale**:
- **Safety (S)**: Impacts vehicle occupants/pedestrians (injury, death)
  - Impact 4: Fatal or critical injury
  - Impact 3: Severe injury requiring hospitalization
  - Impact 2: Minor injury or near-miss
  - Impact 1: No safety impact

- **Financial (F)**: Economic consequences to OEM or user
  - Impact 4: >$1M total damage or >$100k per vehicle
  - Impact 3: $100k-$1M total damage or $10k-$100k per vehicle
  - Impact 2: $10k-$100k total damage or $1k-$10k per vehicle
  - Impact 1: <$1k total damage

- **Operational (O)**: Service availability and functionality
  - Impact 4: Complete system unavailability, mass fleet immobilization
  - Impact 3: Significant functionality loss, multiple subsystems affected
  - Impact 2: Degraded performance or non-critical features unavailable
  - Impact 1: No operational impact or easily recoverable

- **Privacy (P)**: Personal data exposure
  - Impact 4: Exposure of critical PII (location history, biometric data)
  - Impact 3: Exposure of significant PII (payment info, communication logs)
  - Impact 2: Exposure of moderate PII (vehicle settings, preferences)
  - Impact 1: No privacy impact or public data

**Impact Determination**: The final Impact Score = **MAX(S, F, O, P)** for the damage scenario.

**ISO 21434 Requirement**: Damage scenarios must be defined before threat identification to ensure comprehensive threat enumeration aligned with business harm.

---

### Phase 3: Threat Scenario Enumeration (Clause 15.6)
**Skill**: `threat_scenario`  
**Input**: `data/asset_list.md` (assets), `data/ds.md` (damage scenarios)  
**Output**: `data/ts.md` — Threat scenarios with Attack Feasibility Rating (AFR)

**Methodology**:
For each asset-damage scenario pair, enumerate credible threat scenarios describing HOW an attacker could achieve that damage outcome. Assign each threat an **Attack Feasibility Rating (AFR)**.

**AFR Calculation** (5-factor model):
Evaluate each threat scenario across five dimensions:

| Factor | Value | Points |
|--------|-------|--------|
| **Elapsed Time** | <30 sec \| 1-30 min \| 1-4 hrs \| 1-7 days \| >1 week | 0 \| 1 \| 2 \| 3 \| 4 |
| **Expertise** | Master \| Proficient \| Expert \| Novice | 0 \| 1 \| 2 \| 3 |
| **Knowledge** | Public \| Open-source \| Restricted \| Confidential | 0 \| 1 \| 2 \| 3 |
| **Opportunity** | Public \| Physical proximity \| Network access \| Insider | 0 \| 1 \| 2 \| 3 |
| **Equipment** | Standard tools \| Custom \| Specialized \| Banned | 0 \| 1 \| 2 \| 3 |

**AFR Scoring**:
- Sum the five factors: Total = 0-15 points
- Repository contract: higher numeric AFR = easier for attacker / worse for defender
- AFR Classification:
  - 0-4 points = **Very Low** feasibility (hardest for attacker)
  - 5-9 points = **Low** feasibility
  - 10-13 points = **Moderate** feasibility
  - 14-15 points = **High** feasibility (easiest for attacker)

**Threat Mapping**:
- Each threat scenario links to: one or more assets (attack target)
- Each threat scenario links to: one or more damage scenarios (attack outcome)
- Include reference to applicable frameworks: STRIDE, UN R155 Annex 5, MITRE ATT&CK, OWASP

**ISO 21434 Requirement**: Threat scenarios must enumerate feasible attack paths using recognized methodologies (Clause 15.6). AFR assessment ensures distinction between theoretical and practical threats.

---

### Phase 4: Attack Tree Analysis (Optional, Clause 15.7)
**Skill**: `attack_tree`  
**Input**: `data/asset_list.md`, `data/ds.md`, `data/ts.md` (threat scenarios)  
**Output**: `data/at.md` — Multi-step attack chains with logical gates

**Methodology**:
Attack trees model complex multi-stage attacks that require sequential compromises. Each tree shows:
- **Root goal**: The final damage outcome (e.g., "achieve remote vehicle control")
- **Sub-goals**: Intermediate objectives that enable the root goal
- **Leaf nodes**: Individual threat scenarios (attack steps)
- **Logical gates**: AND (all steps required) or OR (alternative paths)

**Example Attack Tree**:
```
Goal: Unauthorized Remote Engine Kill
├─ AND
│  ├─ Compromise CAN Bus Access
│  │  └─ OR
│  │     ├─ Obtain OBD-II Dongle
│  │     ├─ Physical CAN Access via Bench/Lab
│  │     └─ Exploit Diagnostic Port (TS-DIA-001)
│  └─ Craft Malicious CAN Messages
│     └─ Reverse Engineer Message Specs (TS-REV-002)
```

**Attack Feasibility in Trees**:
- Individual threat nodes use AFR from Phase 3
- Tree-level AFR = Effective AFR of the entire attack sequence
- AND gates typically INCREASE difficulty; OR gates offer alternatives

**ISO 21434 Note**: Attack trees are OPTIONAL for TARA compliance. They provide qualitative insight into complex attack chains but do NOT replace per-threat-scenario risk treatment (which uses individual TS AFR scores).

---

### Phase 5: Risk Treatment Decision (Clause 15.8)
**Skill**: `risk_treatment`  
**Input**: `data/asset_list.md`, `data/ds.md`, `data/ts.md`, optionally `data/at.md`  
**Output**: `data/rt.md` — Risk treatment decisions and security controls

**Methodology**:

**Step 1: Calculate Risk Value (RV)**
For each threat scenario:
- Impact Score from linked DS (1-4)
- AFR Score from TS (Very Low=0-4, Low=5-9, Moderate=10-13, High=14-15)
- Risk Value = f(Impact, AFR) using Risk Matrix

**Risk Value Matrix**:

| Impact Level | AFR: Very Low (0-4) | AFR: Low (5-9) | AFR: Moderate (10-13) | AFR: High (14-15) |
|--------------|---------------------|-----------------|------------------------|-------------------|
| 4 - Critical | RV 3            | RV 4              | RV 5             | RV 5                    |
| 3 - Severe   | RV 2            | RV 3              | RV 4             | RV 5                    |
| 2 - Moderate | RV 2            | RV 3              | RV 3             | RV 4                    |
| 1 - Negligible| RV 1           | RV 2              | RV 2             | RV 3                    |

**Risk Value Interpretation**:
- **RV 5 (Very High Risk)**: Requires Avoid or Reduce treatment; unacceptable without controls
- **RV 4 (High Risk)**: Requires Reduce or Transfer treatment; significant controls needed
- **RV 3 (Medium Risk)**: Requires treatment evaluation; controls recommended
- **RV 2 (Low Risk)**: May Accept with documented justification
- **RV 1 (Very Low Risk)**: Typically acceptable; document risk acceptance

**Step 2: Select Treatment Strategy**
For each threat, choose ONE primary strategy:
- **Avoid**: Eliminate the threat by removing the asset/functionality or architectural change
- **Reduce**: Implement security controls to decrease Impact or AFR
- **Transfer**: Shift risk to third party (e.g., insurance, contract terms, supplier responsibility)
- **Accept**: Explicitly document acceptance of residual risk with business justification

**Step 3: Design Security Controls**
For "Reduce" treatments, identify specific controls:
- **Preventive controls**: Decrease AFR (harder to exploit) — firewalls, encryption, access control
- **Detective controls**: Enable rapid incident response — logging, monitoring, anomaly detection
- **Corrective controls**: Mitigate harm — safety shutoffs, failsafes, recovery procedures

**Step 4: Re-Assess Residual Risk**
After control implementation:
- Re-estimate AFR considering new controls
- Recalculate Risk Value with residual AFR
- Document residual risk acceptance or additional control needs

**ISO 21434 Requirement**: Risk treatment decisions must be documented (Clause 15.8) with clear linkage between threats, controls, and residual risk levels. Business decision-makers must explicitly accept any residual risk.

---

### Phase 6: Cybersecurity Goals Derivation (Clause 15.9)
**Skill**: `csg`  
**Input**: `data/ds.md` (damage scenarios), `data/rt.md` (risk treatments)  
**Output**: `data/csg.md` — Cybersecurity goals for active mitigation treatments

**Methodology**:
Cybersecurity goals translate active mitigation treatment decisions into technology-agnostic security objectives. Each goal links to:
- One or more damage scenarios (what harm to prevent)
- One or more risk treatment entries requiring active mitigation

Pure `Accept` / pure `Transfer` decisions do **not** create new CSG entries; their formal claim text remains in `data/rt.md`.

**Goal Structure**:
```
CSG-[DOMAIN]-[NN]: [Goal Name]
  Prevents: DS-XXX-NNN (specific damage scenario)
  Associated Controls: RT-XXX-001, RT-XXX-002, ...
  Goal Statement: The [component/system] shall [protect/prevent/maintain] ...
  CIA Property: [Confidentiality | Integrity | Availability]
  Linked to ISO 21434: Clause 15.9 (Cybersecurity goals)
  Linked to UN R155: [Specific annex reference if applicable]
```

**Example Goals**:
- CSG-CAN-001: Prevent unauthorized CAN message injection
  - Goal Statement: The CAN gateway shall validate message authenticity to prevent unauthorized command injection
  - CIA Property: Integrity
  
- CSG-OTA-001: Prevent malicious firmware updates
  - Goal Statement: The OTA update system shall ensure only authorized firmware is installed
  - CIA Property: Integrity

**ISO 21434 Alignment**: Cybersecurity goals (Clause 15.9 workflow context, Clause 9 concept intent) bridge treatment decisions and later cybersecurity requirements. Each goal must be traceable to one or more damage scenarios and active mitigation RT entries.

---

### Phase 7: Cybersecurity Requirements Derivation (Clause 9.4)
**Skill**: `csr`  
**Input**: `data/csg.md` (cybersecurity goals), `data/rt.md` (risk treatments), `data/ts.md` (threat scenarios), `data/at.md` (attack trees), design specifications  
**Output**: `data/csr.md` — Cybersecurity requirements with Part A (implemented) and Part B (gaps)

**Methodology**:
Cybersecurity requirements translate cybersecurity goals into specific, testable technical controls. Each CSR specifies HOW to implement a security objective, with concrete algorithms, protocols, and configurations. Requirements are classified into:
- **Part A (Implemented)**: Controls already present in the system design, verified against design specifications
- **Part B (Gaps)**: Missing or incomplete controls identified through TARA analysis, prioritized by risk value

**Derivation Process**:
1. Read cybersecurity goals from `data/csg.md` — understand WHAT must be protected
2. Read design specifications — identify existing security controls (Part A candidates)
3. Decompose each CSG into technical requirements using CIA-to-CSR decomposition matrix
4. Perform gap analysis — compare required CSRs against implemented controls
5. Prioritize gaps by Risk Value (CRITICAL/HIGH/MEDIUM/LOW) using `data/rt.md`
6. Document traceability: CSR → CSG → RT → TS → DS → Asset
7. Document allocation target: Item, Component, layer, interface, or supplier-owned subsystem

**CSR Structure**:
```
CSR-[CATEGORY]-[NN]: [Requirement Name]
  Status: ✅ IMPLEMENTED | ⚠️ PARTIAL | ❌ GAP
  Category: [Functional domain]
  Description: [Technical implementation details]
  Related CSG-IDs: [Traceability to cybersecurity goals]
  Source: [Design specification reference] (Part A only)
  Priority: [CRITICAL|HIGH|MEDIUM|LOW] (Part B only)
  Identified By: [TS-ID] (Part B only)
  Recommendation: [Specific mitigation] (Part B only)
```

**ISO 21434 Alignment**: Cybersecurity requirements (Clause 9.4) are the bridge between cybersecurity goals (Clause 15.9) and cybersecurity validation (Clause 10). Each requirement must be traceable to its parent CSG and testable through defined verification methods.

---

### Phase 8: TARA Report Generation (Clause 8.4)
**Skill**: `tara_report`  
**Input**: `data/asset_list.md`, `data/ds.md`, `data/ts.md`, `data/rt.md`, `data/csg.md`, plus optional `data/at.md`  
**Output**: `reports/overall_report.md`, `reports/traceability_report.md`, `reports/multilayer_report.md`

**Report Types**:

1. **TARA Overall Report** (`reports/overall_report.md`)
   - Executive summary of threat landscape
   - Risk statistics and distributions
   - High-level treatment decisions and residual risk
   - Audience: Management, compliance officers

2. **TARA Traceability Report** (`reports/traceability_report.md`)
   - Complete traceability matrix: Assets → Damages → Threats → Controls → Goals
   - Verification that all threats have treatment decisions
   - Gap analysis and control effectiveness
   - Audience: Architects, security engineers, auditors

3. **TARA Multi-Layer Report** (`reports/multilayer_report.md`)
   - Threat landscape organized by attack vector and entry point
   - Defense-in-depth analysis across system layers
   - Control overlap and redundancy analysis
   - Audience: System architects, integration engineers

**ISO 21434 Compliance**: These reports fulfill Clause 8.4 requirements for TARA work products documentation. They enable compliance demonstration to regulators (UN R155) and OEM auditors.

---

### Phase 9: TARA Documentation Export (Clause 8.4)
**Skill**: `tara_export`  
**Input**: `data/asset_list.md`, `data/ds.md`, `data/ts.md`, `data/rt.md`, `data/csg.md`, all three report files, plus optional `data/at.md`  
**Output**: `_build/html/` + `output/pdf/tara_complete.pdf`, `overall_report.pdf`, `traceability_report.pdf`, `multilayer_report.pdf`

**Export Formats**:

1. **Sphinx Documentation Site** (HTML)
   - Professional presentation of TARA methodology and findings
   - Searchable threat catalogue
   - Interactive risk matrices
   - Control effectiveness dashboard
   - Audience: Technical teams, auditors, regulators

2. **Stakeholder PDF Reports**
   - `overall_report.pdf` — executive summary
   - `traceability_report.pdf` — audit evidence
   - `multilayer_report.pdf` — technical deep-dive
   - `tara_complete.pdf` — complete archive

**ISO 21434 Documentation Requirements**: Clause 8.4 mandates clear, accessible TARA documentation. The export skill transforms raw markdown into polished work products suitable for regulatory submission, internal approvals, and supplier collaboration.

---

## Workflow Interdependencies

```
TARA Workflow Dependency Graph
================================

 ┌─ Phase 1: Item Definition + Asset Analysis
 │  └─ Prerequisite: Vehicle architecture, system specs, vehicle-level functions
 │
 └─→ Phase 2: Damage Scenario Analysis
    │  Needs: Item boundary, vehicle-level functions, asset inventory (Phase 1 output)
    │  Prerequisite: Business impact assessment, safety standards
    │
    └─→ Phase 3: Threat Scenario Enumeration
       │  Needs: Assets (Phase 1), Damage scenarios (Phase 2)
       │  Prerequisite: Threat frameworks (STRIDE, R155, MITRE, OWASP)
       │
       ├─→ Phase 4: Attack Tree Analysis (OPTIONAL)
       │  │  Needs: Asset list, damage scenarios, threat scenarios
       │  │
       │  └─→ [branches here if needed for complex attacks]
       │
       └─→ Phase 5: Risk Treatment Decision
          │  Needs: All above (Assets, Damages, Threats, optionally Trees)
          │  Prerequisite: Security control database, business risk appetite
          │
           └─→ Phase 6: Cybersecurity Goals Derivation
              │  Needs: Damage scenarios, treatment decisions (Phases 2, 5)
              │  Output: Security requirements for system design
              │
               ├─→ Phase 7: Cybersecurity Requirements Derivation
               │  │  Needs: CSG goals, treatment decisions, threat scenarios (Phases 5, 6, plus TS and optional AT context)
               │  │  Output: Technical security requirements for implementation
               │
               ├─→ Phase 8: TARA Report Generation
               │  │  Needs: asset_list, ds, ts, rt, csg, optionally at
               │  │  Output: reports/*.md
               │  │
               │  └─→ Phase 9: TARA Documentation Export
               │     │  Needs: Phase 8 reports + Phase 1-6 export data contract (optional at)
               │     │  Output: `_build/html/` + `output/pdf/*.pdf`
               │     │
               │     └─ FINAL: ISO 21434 EXPORTABLE TARA PACKAGE
               │
               └─ Regulatory Compliance Check (UN R155, OEM standards)
```

**Critical Rules**:
- **Must-Do-First**: Phases 1 → 2 → 3 are mandatory sequential steps
- **Optional-But-Valuable**: Phase 4 (Attack Trees) enhances threat modeling for complex systems
- **Integration Points**: Phase 7 and Phase 8 both consume Phase 6 outputs independently; Phase 9 consumes the export contract plus Phase 8 reports
- **No Skipping**: Each phase produces work products that feed the overall ISO 21434 evidence set

---

## ISO 21434 Clause Mappings

| Clause | Topic | TARA Phase | Work Product |
|--------|-------|-----------|--------------|
| 9.3 / 15.3 | Item definition and asset identification | Phase 1 | `data/asset_list.md` |
| 15.4-15.5 | Damage scenario analysis | Phase 2 | `data/ds.md` |
| 15.6 | Threat scenario identification | Phase 3 | `data/ts.md` |
| 15.7 | Attack tree analysis | Phase 4 | `data/at.md` |
| 15.8 | Risk treatment decisions | Phase 5 | `data/rt.md` |
| 15.9 | Cybersecurity goals | Phase 6 | `data/csg.md` |
| 9.4 | Cybersecurity specifications | Phase 7 | `data/csr.md` |
| 8.4 | TARA work product documentation | Phases 8-9 | `reports/`, `_build/html/`, `output/pdf/` |

---

## Framework Cross-Reference

The TARA workflow integrates multiple security frameworks:

- **ISO 21434**: Core automotive cybersecurity process (Clauses 15.3-15.9)
- **UN R155**: Regulatory framework for automotive cybersecurity
- **STRIDE**: Threat categorization (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)
- **MITRE ATT&CK**: Attack tactic/technique enumeration
- **OWASP**: Software security best practices
- **CVSS v3.1**: Vulnerability severity scoring (optional, for supplier vulnerabilities)

---

## Quality Assurance Checklist

Use this checklist to verify TARA workflow completeness:

- [ ] Phase 1: Item/function/component boundary documented; all vehicle assets inventoried with identifiers (AST-DOMAIN-NNN)
- [ ] Phase 2: All damage scenarios identify affected functions, link to assets, and include SFOP impact scores
- [ ] Phase 3: All threat scenarios enumerated with AFR calculations (0-15 points)
- [ ] Phase 4: Attack trees (if applicable) show multi-step attack chains
- [ ] Phase 5: Every threat scenario has a risk treatment decision (Avoid/Reduce/Transfer/Accept)
- [ ] Phase 6: Every active-mitigation RT entry (Avoid/Reduce/Transfer with active mitigation) has at least one cybersecurity goal; pure Accept / pure Transfer claims stay in `data/rt.md`
- [ ] Phase 7: All cybersecurity goals have derived technical requirements (CSRs)
- [ ] Phase 8: All three TARA reports generated without errors
- [ ] Phase 9: `_build/html/index.html` exists and all four PDF exports are present
- [ ] Traceability: Can trace any threat → damage → control → security goal → requirement
- [ ] No orphan work products (every item links to upstream/downstream items)

---

## References

- **ISO/SAE 21434:2021** — Road vehicles — Cybersecurity engineering
- **UN R155** — Cybersecurity and software update management
- **NIST Cybersecurity Framework** — General cybersecurity governance
- **SAE J3061** — Cybersecurity Guidebook for Cyber-Physical Vehicles
- **MITRE ATT&CK Framework** — Attack technique enumeration
- **OWASP Top 10** — Web/API security risks
- **CVSS v3.1** — Common Vulnerability Scoring System

---

**Document Version**: 1.0  
**Last Updated**: 2026-03-31  
**Status**: Reference documentation for TaraOK skill workflow
