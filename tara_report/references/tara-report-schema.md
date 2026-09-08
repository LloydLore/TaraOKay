# TARA Report Schema - ISO 21434 Work Products

This document defines the required fields for all three TARA (Threat Analysis and Risk Assessment) report types generated from the automotive threat scenario library, aligned with ISO 21434:2021 Clause 8.4 (Work Products).

---

## Overview

The TARA reporting framework produces three complementary report types from the unified threat-damage-treatment data:

1. **Overall Report** - Summary risk landscape and treatment portfolio (executive view)
2. **Traceability Report** - Complete asset→threat→damage→treatment chains (audit/compliance view)
3. **Multi-layer Report** - Domain-grouped analysis with cross-domain dependencies (technical architecture view)

---

## Overall Report Fields

### Purpose

The Overall Report provides a high-level summary of the TARA findings for stakeholder communication, risk portfolio management, and executive decision-making.

**ISO 21434 Alignment**: Clause 8.4 - Summary of cybersecurity analyses and findings

### Required Fields

#### 1. Report Header

| Field | Format | Description |
|-------|--------|-------------|
| **Report Title** | String | Fixed: "Automotive Cybersecurity TARA - Overall Risk Assessment" |
| **Report Date** | ISO 8601 (YYYY-MM-DD) | Date report was generated |
| **Reporting Period** | ISO 8601 range | Data collection period (e.g., "2026-01-01 to 2026-03-31") |
| **Vehicle System** | String | E.g., "Infotainment/Head Unit System" |
| **Scope** | String (1-2 sentences) | System description and boundaries |
| **Total Threat Scenarios** | Integer | Count of all TS-* entries analyzed |
| **Total Damage Scenarios** | Integer | Count of all DS-* entries analyzed |
| **Total Risk Treatments** | Integer | Count of all RT-* entries |
| **Total Cybersecurity Goals** | Integer | Count of all CSG-* entries |
| **Total Attack Chains** | Integer | Count of documented attack sequences |

**Validation Rules**:
- All counts must be non-negative integers
- Total TS count ≥ 0 (may be 0 during early phases)
- Report Date ≤ today's date
- Scope must be concise (under 300 characters)

---

#### 2. Risk Summary Statistics

| Field | Format | Description |
|-------|--------|-------------|
| **Overall Risk Level** | Enum: Critical / High / Medium / Low / Negligible | Aggregate risk of all TS scenarios |
| **Total Threats (RV 5)** | Integer | Count of highest-risk scenarios (RV 5) |
| **Total Threats (RV 4)** | Integer | Count of high-risk scenarios (RV 4) |
| **Total Threats (RV 3)** | Integer | Count of medium-risk scenarios (RV 3) |
| **Total Threats (RV 2)** | Integer | Count of low-risk scenarios (RV 2) |
| **Total Threats (RV 1)** | Integer | Count of negligible-risk scenarios (RV 1) |
| **Risk Distribution Percentage** | Decimal (0-100) per RV level | % breakdown: e.g., "38% RV5, 42% RV4, 15% RV3, 5% RV2, 0% RV1" |

**Validation Rules**:
- Sum of all RV counts = Total Threat Scenarios
- Overall Risk Level = highest RV present in portfolio (RV 5 → Critical; RV 4 → High; etc.)
- All percentages sum to 100.0 ± 0.1

---

#### 3. Treatment Portfolio

| Field | Format | Description |
|-------|--------|-------------|
| **Reduce Treatments** | Integer | Count of RT entries with Decision = "Reduce" |
| **Avoid Treatments** | Integer | Count of RT entries with Decision = "Avoid" |
| **Transfer Treatments** | Integer | Count of RT entries with Decision = "Transfer" |
| **Accept Treatments** | Integer | Count of RT entries with Decision = "Accept" |
| **Treatment Effectiveness** | Percentage (0-100) | (Sum Reduce + Avoid + Transfer) / Total Treatments × 100 |
| **Residual Risk Level** | Enum (Critical/High/Medium/Low) | Aggregate risk after all treatments applied |
| **Residual Threats (RV ≥ 4)** | Integer | Count of RV 4-5 scenarios remaining after treatment |

**Validation Rules**:
- Sum of all treatment counts = Total Risk Treatments
- Treatment Effectiveness ≥ 0 and ≤ 100
- Residual Risk Level ≤ Overall Risk Level (treatments improve or maintain risk posture)
- Residual Threats ≤ Original Threats at same RV level

---

#### 4. Domain Breakdown

| Field | Format | Description |
|-------|--------|-------------|
| **CAN Bus Threats** | Integer | Count of TS-CAN-* entries |
| **OTA/Update Threats** | Integer | Count of TS-OTA-* entries |
| **External Interface Threats** | Integer | Count of TS-EXT-* entries |
| **Backend/Cloud Threats** | Integer | Count of TS-BCK-* entries |
| **Infotainment Threats** | Integer | Count of TS-IVI-* entries |
| **Immobilizer Threats** | Integer | Count of TS-IMM-* entries |
| **ADAS Threats** | Integer | Count of TS-ADAS-* entries |
| **Highest-Risk Domain** | String | Domain with greatest RV 5 concentration |
| **Most-Affected Asset** | String (ID + Name) | AST-* with highest threat count |

**Validation Rules**:
- All counts ≥ 0
- Sum of domain counts = Total Threat Scenarios
- Highest-Risk Domain must correspond to a domain with TS entries

---

#### 5. Impact Analysis (SFOP Dimensions)

| Field | Format | Description |
|-------|--------|-------------|
| **Safety-Critical Threats** | Integer | Count of DS with Safety dimension ≥ 3 |
| **Financial Impact Threats** | Integer | Count of DS with Financial dimension ≥ 3 |
| **Operational Impact Threats** | Integer | Count of DS with Operational dimension ≥ 3 |
| **Privacy Impact Threats** | Integer | Count of DS with Privacy dimension ≥ 3 |
| **Multi-Dimensional Threats** | Integer | Count of DS affecting 3+ SFOP dimensions |
| **Most Critical SFOP Dimension** | String | Enum: Safety / Financial / Operational / Privacy |
| **Safety-Critical Residual Risk** | Integer | Count of safety-related threats with RV ≥ 3 after treatment |

**Validation Rules**:
- All counts ≥ 0
- Safety-Critical Residual Risk ≤ Safety-Critical Threats
- Most Critical SFOP Dimension = dimension with highest threat count

---

#### 6. Top Risk Scenarios

| Field | Format | Description |
|-------|--------|-------------|
| **Rank 1 Risk** | String (TS-ID + Title + RV) | Highest-risk threat scenario |
| **Rank 2 Risk** | String (TS-ID + Title + RV) | Second-highest-risk scenario |
| **Rank 3 Risk** | String (TS-ID + Title + RV) | Third-highest-risk scenario |
| **Rank 4 Risk** | String (TS-ID + Title + RV) | Fourth-highest-risk scenario |
| **Rank 5 Risk** | String (TS-ID + Title + RV) | Fifth-highest-risk scenario |
| **Top Risk Scenario Description** | String (2-3 sentences) | Brief threat narrative of Rank 1 |

**Validation Rules**:
- All Rank fields must have RV ≥ 4 (only show material risks)
- Ranks must be ordered: RV(Rank1) ≥ RV(Rank2) ≥ RV(Rank3) ≥ ... ≥ RV(Rank5)
- If fewer than 5 RV ≥ 4 threats exist, list only those present
- Rank 1 Risk Title and Description must match the TS-ID entry

---

#### 7. Cybersecurity Goals Summary

| Field | Format | Description |
|-------|--------|-------------|
| **Total Cybersecurity Goals (CSG)** | Integer | Count of all CSG-* entries |
| **Confidentiality-Focused Goals** | Integer | Count of CSG with CIA Property = Confidentiality |
| **Integrity-Focused Goals** | Integer | Count of CSG with CIA Property = Integrity |
| **Availability-Focused Goals** | Integer | Count of CSG with CIA Property = Availability |
| **Multi-Property Goals** | Integer | Count of CSG addressing 2+ CIA properties |
| **Goals with Treatment** | Integer | Count of CSG with ≥1 Related RT-ID |
| **Orphan Goals** | Integer | Count of CSG with 0 Related DS-IDs (data quality issue) |

**Validation Rules**:
- Sum of CIA property counts ≤ Total CSG (goals may span multiple properties)
- Goals with Treatment ≤ Total CSG
- Orphan Goals should be 0 (indicates data completeness issue if > 0)

---

#### 8. Compliance and Standards References

| Field | Format | Description |
|-------|--------|-------------|
| **ISO 21434 Alignment** | String | Clauses covered: "15.6 (Damage), 15.7 (Threat), 15.8 (Risk), 15.9 (CSG)" |
| **UN R155 Coverage** | String | Annex 5 threat categories mapped in report |
| **MITRE ATT&CK ICS References** | Integer | Count of threat scenarios mapped to MITRE |
| **OWASP References** | Integer | Count of scenarios mapped to OWASP frameworks |
| **CVE Examples** | Integer | Count of real CVEs cited as evidence |

**Validation Rules**:
- ISO 21434 Alignment must reference valid clause numbers
- MITRE/OWASP/CVE counts ≥ 0
- If any count > 0, supporting evidence must exist in underlying TS/DS entries

---

### Overall Report Example Structure

```
# AUTOMOTIVE CYBERSECURITY TARA - OVERALL RISK ASSESSMENT

## Report Information
- Report Date: 2026-03-25
- Vehicle System: Infotainment/Head Unit System (QAM8295)
- Total Threat Scenarios: 21
- Total Risk Treatments: 21

## Risk Summary
- Overall Risk Level: **Critical** (3 RV-5 threats identified)
- RV Distribution: 14% RV5 (3), 67% RV4 (14), 19% RV3 (4), 0% RV2, 0% RV1

## Treatment Portfolio
- Reduce: 21/21 (100%)
- Avoid: 0
- Transfer: 0
- Accept: 0
- **Residual Risk: HIGH** (RV 4 average after treatment)

## Top 5 Risks (Pre-Treatment)
1. TS-CAN-001: CAN Bus Message Injection - **RV 5**
2. TS-IVI-001: GNSS Location Data Exfiltration - **RV 5**
3. TS-OTA-001: Unauthorized Firmware Update - **RV 5**
...
```

---

## Traceability Report Fields

### Purpose

The Traceability Report documents the complete M:N mappings between assets, damage scenarios, threat scenarios, attack chains, risk treatments, and cybersecurity goals. Used for compliance audits, regulatory submissions, and verification of coverage.

**ISO 21434 Alignment**: Clause 8.4 - Traceability and completeness verification

### Required Fields

#### 1. Asset Catalogue Summary

| Field | Format | Description |
|-------|--------|-------------|
| **Total Assets** | Integer | Count of all AST-* entries |
| **Asset IDs** | List (AST-XXX-NNN) | All unique asset identifiers |
| **Asset Names** | List (String) | Human-readable names corresponding to each AST-ID |
| **Threats per Asset** | Table (AST-ID → Count) | Number of threat scenarios per asset |
| **Orphan Assets** | Integer | Count of AST-* with 0 related TS/DS entries |

**Validation Rules**:
- Total Assets = count of unique AST-IDs
- Orphan Assets should be 0 (indicates missing threat analysis)
- Threats per Asset ≥ 0

---

#### 2. Asset-to-Threat Mapping

| Field | Format | Description |
|-------|--------|-------------|
| **Traceability Matrix (Asset × Threat)** | Table (AST-ID rows × TS-ID columns) | ✓/✗ matrix showing which assets are affected by which threats |
| **Asset Coverage (%)** | Decimal (0-100) | % of assets with ≥1 identified threat |
| **Threat Coverage (%)** | Decimal (0-100) | % of threats that affect ≥1 asset |
| **High-Impact Assets** | List (AST-ID + Max RV) | Assets affected by RV 4-5 threats |

**Validation Rules**:
- Coverage percentages between 0-100
- Matrix cells = ✓ if AST-ID appears in any threat scenario
- High-Impact Assets list ≥ 0 entries

---

#### 3. Damage Scenario Traceability

| Field | Format | Description |
|-------|--------|-------------|
| **Damage Scenario IDs** | List (DS-XXX-NNN) | All unique DS identifiers |
| **DS-to-Threat Mapping** | Table (DS-ID rows × TS-ID columns) | Which threats lead to which damages |
| **DS Coverage (%)** | Decimal (0-100) | % of damage scenarios with ≥1 threat scenario |
| **Orphan Damage Scenarios** | Integer | Count of DS-* with 0 related TS entries |
| **DS with Multiple Threats** | Integer | Count of DS addressed by 2+ TS entries |

**Validation Rules**:
- Orphan Damage Scenarios should be ≤ 5% of total DS (acceptable for low-likelihood scenarios)
- DS with Multiple Threats ≥ 0
- Coverage % reflects defense-in-depth threat analysis

---

#### 4. Attack Chain Documentation

| Field | Format | Description |
|-------|--------|-------------|
| **Total Attack Chains** | Integer | Count of documented multi-step attack sequences |
| **Chain IDs** | List (AT-[DOMAIN]-NNN) | All unique attack chain identifiers |
| **Attack Chain Descriptions** | List (String, 2-3 sentences each) | Narrative of each multi-stage attack |
| **Stages per Chain** | Integer | Average number of stages per chain (min/max) |
| **Most Complex Chain** | String (AT-ID + Stage Count) | Chain with most stages |

**Validation Rules**:
- Total Attack Chains ≥ 0
- Stages per Chain typically 2-5
- Complex chains have explicit TS-linkage documentation

---

#### 5. Treatment-to-Goal Mapping

| Field | Format | Description |
|-------|--------|-------------|
| **RT-to-CSG Mapping** | Table (RT-ID rows × CSG-ID columns) | Which risk treatments implement which cybersecurity goals |
| **CSG Implementation (%)** | Decimal (0-100) | % of CSGs with ≥1 RT implementation |
| **Unimplemented Goals** | Integer | Count of CSG-* with 0 Related RT-IDs |
| **Goals with Multiple Treatments** | Integer | Count of CSG addressed by 2+ RT entries |

**Validation Rules**:
- CSG Implementation % ≥ 80 (most goals should have implementation)
- Unimplemented Goals should be minimal (indicates work-in-progress)
- Mappings must be consistent with CSG schema

---

#### 6. Complete Traceability Chain

| Field | Format | Description |
|-------|--------|-------------|
| **Traceability Chains** | List (AST → DS → TS → AT → RT → CSG) | Multi-step mappings showing complete threat→treatment→goal flow |
| **Chain Completeness (%)** | Decimal (0-100) | % of chains with all 6 elements present |
| **Broken Chains** | Integer | Count of chains missing required elements |
| **Example Complete Chain** | String (formatted path) | Sample traced scenario from asset to cybersecurity goal |

**Validation Rules**:
- Chain Completeness ≥ 90% indicates good coverage
- Broken Chains ≤ 10% acceptable (may indicate accepted risks)
- Example must be traceable through all data files

---

#### 7. Domain Traceability

| Field | Format | Description |
|-------|--------|-------------|
| **Domain Coverage** | Table (Domain × Completeness %) | Per-domain traceability completeness |
| **Cross-Domain Threats** | Integer | Count of TS affecting multiple domains |
| **Domain-Specific Goals** | Table (Domain × CSG Count) | Number of CSGs per domain |
| **Interdomain Dependencies** | Integer | Count of RT decisions depending on multiple domains |

**Validation Rules**:
- Domain Coverage ≥ 75% per domain (comprehensive analysis)
- Cross-Domain Threats ≥ 0
- All 7 domains (CAN, IVI, OTA, EXT, BCK, IMM, ADAS) should be represented

---

### Traceability Report Example

```
# TRACEABILITY REPORT - THREAT ANALYSIS COVERAGE

## Asset-to-Threat Coverage
| Asset | Threats | Max RV | Coverage |
|-------|---------|--------|----------|
| AST-ECU-001 | 12 | RV 5 | 100% |
| AST-SNS-001 | 8 | RV 4 | 95% |

## Complete Chain Example
AST-ECU-001 (Head Unit) 
  → DS-IVI-001 (Location Tracking)
  → TS-IVI-001 (GNSS Data Exfiltration)
  → AT-IVI-001 (Multi-stage location breach)
  → RT-IVI-001 (Reduce via Encryption)
  → CSG-IVI-01 (Location Confidentiality)

**Status**: ✓ Complete chain with all mappings present

## Domain Coverage
- CAN: 85% traceability completeness
- IVI: 92% traceability completeness
- OTA: 78% traceability completeness
- [...]
```

---

## Multi-layer Report Fields

### Purpose

The Multi-layer Report organizes all findings by domain, showing both domain-specific threats and cross-domain dependencies. Enables technical architecture review and domain-owned risk accountability.

**ISO 21434 Alignment**: Clause 8.4 - System architecture and domain responsibilities

### Required Fields

#### 1. Domain Summary (per Domain)

For each of the 7 domains (CAN, OTA, EXT, BCK, IVI, IMM, ADAS), include:

| Field | Format | Description |
|-------|--------|-------------|
| **Domain Name** | String | Full domain title (e.g., "CAN Bus and In-Vehicle Networking") |
| **Domain Threats** | Integer | Count of TS-[DOMAIN]-* entries |
| **Domain Damage Scenarios** | Integer | Count of DS-[DOMAIN]-* entries |
| **Domain Risk Treatments** | Integer | Count of RT-[DOMAIN]-* entries |
| **Domain CSGs** | Integer | Count of CSG-[DOMAIN]-* entries |
| **Domain Assets** | Integer | Count of AST-* assigned to this domain |
| **Domain Risk Level** | Enum (Critical/High/Medium/Low) | Highest RV in domain |
| **Top Domain Threat** | String (TS-ID + RV) | Highest-RV threat in domain |

**Validation Rules**:
- All counts ≥ 0
- Top Domain Threat must have RV in domain (typically RV ≥ 3)
- Domain Risk Level = highest RV present in domain threats

---

#### 2. Domain Risk Distribution

| Field | Format | Description |
|-------|--------|-------------|
| **RV 5 Threats (Domain)** | Integer | Count of TS with RV 5 in domain |
| **RV 4 Threats (Domain)** | Integer | Count of TS with RV 4 in domain |
| **RV 3-1 Threats (Domain)** | Integer | Count of TS with RV ≤ 3 in domain |
| **Domain SFOP Impact** | Table (S/F/O/P × Threat Count) | Safety/Financial/Operational/Privacy impact per domain |
| **Most Critical Impact Type** | Enum (Safety/Financial/Operational/Privacy) | Highest-severity SFOP dimension in domain |

**Validation Rules**:
- Sum of RV counts = Domain Threats
- SFOP threat counts may overlap (one threat affects multiple dimensions)
- Most Critical Impact Type corresponds to highest threat count

---

#### 3. Domain Assets and Attack Surface

| Field | Format | Description |
|-------|--------|-------------|
| **Entry Points** | List (String) | Attack surfaces / interfaces for domain |
| **Assets at Risk** | List (AST-ID + Name) | All assets in domain with ≥1 threat |
| **External Interfaces** | Integer | Count of external attack entry points |
| **Internal Dependencies** | Integer | Count of interdomain dependencies |
| **Physical Access Required** | Integer | Count of threats requiring physical access |
| **Remote Attack Feasible** | Integer | Count of threats executable remotely |

**Validation Rules**:
- All counts ≥ 0
- External Interfaces ≤ 10 (architectural constraint)
- Physical + Remote threats ≤ Domain Threats (overlap acceptable)

---

#### 4. Domain Treatment Strategy

| Field | Format | Description |
|-------|--------|-------------|
| **Domain Treatment Decisions** | Table (Reduce/Avoid/Transfer/Accept counts) | Treatment breakdown for domain |
| **Treatment Effectiveness (Domain)** | Percentage (0-100) | % of domain risks being actively mitigated |
| **Residual Risk (Domain)** | Integer | Count of RV ≥ 4 threats remaining after treatment |
| **High-Risk CSGs (Domain)** | Integer | Count of CSGs addressing RV 5 threats |
| **Defense Layers (Domain)** | Integer | Average number of CSGs per domain threat |

**Validation Rules**:
- Treatment Effectiveness ≥ 70% (most threats should have treatment)
- Residual Risk ≤ Original Domain Threats
- Defense Layers typically 1-3 (defense-in-depth)

---

#### 5. Cross-Domain Dependencies

| Field | Format | Description |
|-------|--------|-------------|
| **Threats Affecting Multiple Domains** | Integer | Count of TS with cross-domain impact |
| **Cross-Domain Attack Chains** | List (AT-ID + Description) | Multi-stage attacks spanning domains |
| **Interdomain Risk Amplification** | String (% increase) | Risk increase due to cross-domain dependencies |
| **Domain Isolation Score** | Decimal (0-1) | Measure of domain separation (1 = fully isolated) |
| **Gateway/Controller Dependencies** | List (Component + Dependency) | Central points affecting multiple domains |

**Validation Rules**:
- Cross-Domain Threats ≥ 0
- Risk Amplification ≥ 0% (interdependencies can increase aggregate risk)
- Domain Isolation 0-1 range (architectural design metric)

---

#### 6. Domain Compliance and Standards

| Field | Format | Description |
|-------|--------|-------------|
| **Applicable UN R155 Categories (Domain)** | List (String) | R155 Annex 5 threat categories per domain |
| **Domain-Specific Regulations** | List (String) | Regional requirements affecting domain |
| **Safety-Critical Functions (Domain)** | Integer | Count of threats affecting ISO 26262 functions |
| **Data Protection Constraints (Domain)** | String | GDPR/GB44495 applicability notes |

**Validation Rules**:
- Applicable standards must be relevant to domain function
- Safety-Critical count ≥ 0

---

#### 7. Domain Threat Scenarios Listing

| Field | Format | Description |
|-------|--------|-------------|
| **Threat Scenario Table** | Table (TS-ID | Title | RV | Treatment | CSG | Status) | All threats in domain with key attributes |
| **TS-ID** | String | Threat scenario identifier |
| **Title** | String | Brief threat description |
| **RV** | Integer (1-5) | Risk value (1=low, 5=critical) |
| **Related Treatment** | String (RT-ID) | Associated risk treatment entry |
| **Related CSG** | String (CSG-ID) | Cybersecurity goal addressing threat |
| **Status** | Enum (Open/In-Progress/Treated/Residual) | Treatment status |

**Validation Rules**:
- Status progression: Open → In-Progress → Treated (or Residual)
- All TS entries must be present (no gaps)
- RT/CSG references must be valid identifiers

---

### Multi-layer Report Example

```
# MULTI-LAYER THREAT ANALYSIS REPORT

## DOMAIN: CAN Bus and In-Vehicle Networking (CAN)

### Domain Summary
- Threats: 4 scenarios
- Risk Level: **CRITICAL** (1 RV-5 threat)
- Treatment: 100% under Reduce strategy

### Risk Distribution
- RV 5: 1 threat (CAN Message Injection)
- RV 4: 3 threats
- RV ≤ 3: 0 threats

### Threat Scenarios

| TS-ID | Title | RV | Treatment | CSG | Status |
|-------|-------|-----|-----------|-----|--------|
| TS-CAN-001 | Message Injection | 5 | RT-CAN-001 | CSG-CAN-01 | In-Progress |
| TS-CAN-002 | Bus DoS | 4 | RT-CAN-002 | CSG-CAN-02 | Treated |

### Cross-Domain Dependencies
- **Gateway Control**: TS-CAN-001 affects IVI messages (cascading failure risk)
- **OTA Updates**: RT-CAN-001 interacts with OTA secure boot (RT-OTA-001)

---

## DOMAIN: Infotainment/Head Unit (IVI)

### Domain Summary
- Threats: 10 scenarios
- Risk Level: **HIGH** (0 RV-5, 6 RV-4 threats)
- Treatment: 100% under Reduce strategy

[Domain details continue...]
```

---

## Report Generation and Validation

### Cross-Report Consistency Rules

When generating all three report types from unified data, maintain consistency:

1. **Count Consistency**: Total threat counts must match across all reports
   - Overall Report: "Total Threat Scenarios = X"
   - Sum of domain threat counts (Multi-layer) = X
   - TS entries in Traceability Report = X

2. **RV Consistency**: Risk value distributions must align
   - Overall Report RV breakdown = Sum of domain RV breakdowns
   - Residual Risk calculations must use same AFR methodology

3. **Treatment Consistency**: Treatment decisions must be identical across reports
   - RT-ID → Treatment Decision must be consistent
   - Residual Risk calculations deterministic

### Validation Checklist

- [ ] Overall Report totals match source data files (ts.md, ds.md, rt.md, csg.md)
- [ ] Traceability Report chains trace successfully through all data files
- [ ] Multi-layer Report domain totals sum to overall totals
- [ ] All TS-IDs, DS-IDs, RT-IDs, CSG-IDs are valid identifiers
- [ ] Risk values (RV, AFR, Impact) are calculated correctly
- [ ] No orphan scenarios (all DS linked to ≥1 TS, all TS linked to ≥1 RT)
- [ ] Cross-domain dependencies explicitly documented
- [ ] ISO 21434 Clause 8.4 work product requirements met

---

## References

- **ISO/SAE 21434:2021** - Road vehicles — Cybersecurity engineering
  - Clause 8.4: Work products for security engineering (documentation requirements)
  - Clause 15: Threat analysis and risk assessment (TARA)
  
- **UN Regulation No. 155** - Cyber security and cyber security management system
  - Annex 5: Threat categories and vehicle systems
  
- **NIST SP 800-53** - Security and Privacy Controls for Information Systems
  - Control reporting and compliance documentation patterns

---

## Schema Version

- **Version**: 1.0
- **Date**: 2026-03-25
- **Status**: Active
- **Aligned With**: ISO 21434:2021 Clause 8.4 Work Products
