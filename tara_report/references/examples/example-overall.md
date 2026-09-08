# Automotive Cybersecurity TARA - Overall Risk Assessment

**Report Date**: 2026-03-25  
**Reporting Period**: 2026-03-18 to 2026-03-25  
**Vehicle System**: Infotainment/Head Unit System  
**System Scope**: Qualcomm QAM8295 SoC with QNX+Android Hypervisor, wireless connectivity (Bluetooth, WiFi, Cellular), displays (HUD, central console, instrument cluster), CAN-FD network interface, and USB/NFC external interfaces

**Data Sources**:
- Asset Catalogue: [data/asset_list.md](data/asset_list.md)
- Damage Scenarios: [data/ds.md](data/ds.md)
- Threat Scenarios: [data/ts.md](data/ts.md)
- Attack Chains: [data/at.md](data/at.md)
- Risk Treatments: [data/rt.md](data/rt.md)
- Cybersecurity Goals: [data/csg.md](data/csg.md)

**ISO 21434 Alignment**: ISO/SAE 21434:2021 Clause 8.4 (Work Products), Clause 15 (Threat Analysis and Risk Assessment)

---

## Executive Summary

<!-- EXAMPLE: This section demonstrates executive summary with key findings from the overall risk assessment -->

The Infotainment/Head Unit system risk assessment identified **21 distinct threat scenarios** across five domains (CAN, IVI, OTA, EXT, BCK) affecting the vehicle's infotainment subsystem and its interfaces to safety-critical ECUs via the Gateway. The analysis prioritized mitigation of **4 Critical-Risk (RV-5) threats** capable of enabling remote vehicle control through hypervisor escape and CAN message injection, representing the highest safety impact. All 21 identified threats have been assigned **Reduce** treatment with active security controls targeting Attack Feasibility Reduction (AFR) factors including specialist expertise requirements, knowledge accessibility, and specialized equipment needs.

**Key Findings**:
- Overall Risk Level: **High** (4 RV-5 threats identified, 14 RV-4 threats)
- Total Threat Scenarios: 21 across 5 domains (CAN, IVI, OTA, EXT, BCK)
- Treatment Coverage: **100%** of threats under active mitigation planning
- Residual Risk Level: **High** after all treatments applied (RV-5 threats remain critical even with controls)
- Top Risk Domain: **IVI (Infotainment)** (7 threat scenarios including 3 RV-5 critical threats)

**Compliance Status**: All identified threats align with UN R155 Annex 5 threat categories and ISO 21434 threat analysis methodology. Risk treatments implement controls mapped to ISO 26262 Functional Safety ASIL-D where applicable (CAN message injection, hypervisor escape). Residual risk documentation supports Type Approval submissions under UN R155 Clause 6.2 (cybersecurity management).

---

## Summary Statistics

<!-- EXAMPLE: This section demonstrates system coverage with real counts from all data files -->

### System Coverage

| Category | Count | Source File |
|----------|-------|-------------|
| **Assets** | 28 | [data/asset_list.md](data/asset_list.md) |
| **Damage Scenarios** | 18 | [data/ds.md](data/ds.md) |
| **Threat Scenarios** | 21 | [data/ts.md](data/ts.md) |
| **Attack Chains** | 5 | [data/at.md](data/at.md) |
| **Risk Treatments** | 21 | [data/rt.md](data/rt.md) |
| **Cybersecurity Goals** | 12 | [data/csg.md](data/csg.md) |

**Asset Coverage**: 100% of 28 identified assets (SoC, hypervisor, guest OSes, gateways, sensors, actuators, communication interfaces, storage, cryptographic modules) have ≥1 identified threat  
**Treatment Coverage**: 100% of 21 threat scenarios have assigned risk treatment decisions  
**CSG Implementation**: 100% of 12 cybersecurity goals have ≥1 treatment implementation

---

## Risk Value Distribution

<!-- EXAMPLE: This section demonstrates RV breakdown with calculated percentages from rt.md -->

### Pre-Treatment Risk Landscape

| Risk Value | Count | Percentage | Description |
|------------|-------|------------|-------------|
| **RV 5** (Critical) | 4 | 19.0% | Requires immediate action (Reduce/Avoid) |
| **RV 4** (High) | 14 | 66.7% | Requires risk reduction |
| **RV 3** (Medium) | 3 | 14.3% | Requires reduction or transfer |
| **RV 2** (Low) | 0 | 0% | May accept with justification |
| **RV 1** (Negligible) | 0 | 0% | Acceptable risk |

**Total Threats**: 21

**Overall Risk Level**: **High**  
Calculation: Aggregate risk determined by highest RV present (RV 5 → High; RV 4 → High; RV 3 → Medium; RV 2 → Low; RV 1 → Negligible). Presence of 4 RV-5 critical threats escalates overall risk to High despite majority (66.7%) of threats being RV-4.

---

## Treatment Decision Breakdown

<!-- EXAMPLE: This section demonstrates treatment portfolio with counts and percentages from rt.md -->

### Treatment Portfolio (Source: [data/rt.md](data/rt.md))

| Decision | Count | Percentage | Description |
|----------|-------|------------|-------------|
| **Reduce** | 21 | 100% | Active security controls to lower AFR or Impact |
| **Avoid** | 0 | 0% | Remove threat by eliminating attack surface |
| **Transfer** | 0 | 0% | Shift risk via insurance/third-party liability |
| **Accept** | 0 | 0% | Document residual risk with stakeholder sign-off |

**Total Treatments**: 21

**Treatment Effectiveness**: **100%**  
Calculation: (Reduce + Avoid + Transfer) / Total Treatments × 100 = (21 + 0 + 0) / 21 × 100 = 100%

**Residual Risk**:
- Residual Risk Level: **High**
- Residual RV ≥ 4 Threats: 18 (after all treatments applied, 14 RV-4 + 4 RV-5 remain high-risk)
- Risk Reduction Achieved: **19.0%** (reduced from 4 RV-5 to estimated 3-4 RV-5 equivalent after residual AFR increases)

---

## Top 5 Highest Risk Scenarios (Pre-Treatment)

<!-- EXAMPLE: This section demonstrates top 5 risks with real TS data and RV ratings -->

### Most Critical Threats (Source: [data/ts.md](data/ts.md))

**1. TS-CAN-001: CAN Bus Message Injection via Compromised Head Unit**  
- **Risk Value**: RV 4  
- **Domain**: CAN  
- **Impact**: 4 (Critical) - Safety: 4, Financial: 3, Operational: 3, Privacy: 1  
- **Attack Feasibility**: AFR 8 (Medium)  
- **Treatment**: RT-CAN-001 (Reduce via SecOC and Gateway Hardening)  
- **Description**: Attacker compromises Android Guest OS via malicious app, exploits hypervisor vulnerability to escape to QNX partition with CAN-FD access, injects spoofed CAN messages to safety ECUs. Unintended acceleration, braking, or steering at highway speeds creates high fatality probability.

**2. TS-IVI-001: Malicious Android Application Installation and Privilege Escalation**  
- **Risk Value**: RV 5  
- **Domain**: IVI  
- **Impact**: 4 (Critical) - Safety: 4, Financial: 3, Operational: 4, Privacy: 3  
- **Treatment**: RT-IVI-001 (Reduce via App Store Hardening)  
- **Description**: Attacker distributes malicious app via third-party app store with weak code signing. User installs app granting permission for location access and internet connectivity. Malicious app exploits Android kernel CVE for root privilege escalation, then exploits hypervisor vulnerability for QNX escape enabling CAN access.

**3. TS-IVI-002: Bluetooth Stack Exploitation via Remote Code Execution**  
- **Risk Value**: RV 4  
- **Domain**: IVI  
- **Impact**: 4 (Critical) - Safety: 4, Financial: 3, Operational: 4, Privacy: 3  
- **Attack Feasibility**: AFR 8 (Medium)  
- **Treatment**: RT-IVI-002 (Reduce via Stack Hardening)  
- **Description**: Attacker within Bluetooth range exploits CVE-2025-32059 buffer overflow in Alps Alpine L2CAP stack, crafts malicious Bluetooth packet, hijacks control flow to execute shellcode with root privileges. Gains complete control over Android partition with potential for hypervisor escape and CAN access.

**4. TS-EXT-001: Backend API Authentication Bypass via Broken Object-Level Authorization**  
- **Risk Value**: RV 5  
- **Domain**: EXT  
- **Impact**: 4 (Critical) - Safety: 4, Financial: 4, Operational: 4, Privacy: 4  
- **Attack Feasibility**: AFR 11 (Low)  
- **Treatment**: RT-EXT-001 (Reduce via OAuth 2.0 + MFA)  
- **Description**: Attacker exploits broken object-level authorization (IDOR) in backend telematics API by manipulating VIN parameter in API requests, gains unauthorized access to fleet management functions, extracts firmware signing keys or deploys malicious OTA updates to fleet-wide vehicles.

**5. TS-OTA-001: Unsigned or Weakly Signed Firmware Update Delivery**  
- **Risk Value**: RV 4  
- **Domain**: OTA  
- **Impact**: 4 (Critical) - Safety: 4, Financial: 3, Operational: 4, Privacy: 3  
- **Treatment**: RT-OTA-001 (Reduce via Multi-Signature)  
- **Description**: Attacker intercepts OTA firmware update over WiFi or compromises backend OTA server, delivers malicious firmware signed with weak key or unsigned. Vehicles install backdoored firmware enabling persistent CAN access, location tracking, and vehicle control.

> **Note**: Only threats with RV ≥ 4 are shown. All 21 identified threats meet this criterion (4 RV-5 + 14 RV-4 + 3 RV-3, no RV ≤ 2 identified).

---

## Domain Risk Breakdown

<!-- EXAMPLE: This section demonstrates domain-specific threat distribution with real threat counts -->

### Threat Distribution by Domain (Source: [data/ts.md](data/ts.md))

| Domain | Code | Threats | RV 5 | RV 4 | RV 3-1 | Highest RV | Top Threat |
|--------|------|---------|------|------|--------|------------|------------|
| **CAN Bus** | CAN | 4 | 0 | 4 | 0 | RV 4 | TS-CAN-001 (CAN Message Injection) |
| **OTA/Update** | OTA | 2 | 1 | 1 | 0 | RV 5 | TS-OTA-001 (Unsigned Firmware) |
| **External Interface** | EXT | 4 | 1 | 3 | 0 | RV 5 | TS-EXT-001 (Backend API Bypass) |
| **Backend/Cloud** | BCK | 4 | 1 | 3 | 0 | RV 5 | TS-BCK-001 (Server Compromise) |
| **Infotainment** | IVI | 7 | 1 | 3 | 3 | RV 5 | TS-IVI-001 (Malicious App) |
| **Immobilizer** | IMM | 0 | 0 | 0 | 0 | N/A | N/A |
| **ADAS** | ADAS | 0 | 0 | 0 | 0 | N/A | N/A |

**Most Affected Asset**: AST-ECU-001 (Head Unit System-on-Chip, QAM8295) - 14 threats directly targeting SoC compromise via app execution, hypervisor escape, or firmware manipulation

---

## Impact Analysis (SFOP Dimensions)

<!-- EXAMPLE: This section demonstrates SFOP impact distribution with damage scenario coverage -->

### Damage Scenario Impact Distribution (Source: [data/ds.md](data/ds.md))

| SFOP Dimension | High Impact (≥3) Count | Most Critical DS | Residual High Risk |
|----------------|------------------------|------------------|-------------------|
| **Safety** | 6 | DS-CAN-001 (Malicious CAN Injection - Impact 4) | 5 (after treatments) |
| **Financial** | 16 | DS-IVI-005 (Cryptographic Key Compromise - Financial Impact 4) | 12 (after treatments) |
| **Operational** | 14 | DS-IVI-003 (Malicious Code Execution - Operational Impact 4) | 10 (after treatments) |
| **Privacy** | 10 | DS-IVI-001 (Location Tracking - Privacy Impact 4) | 8 (after treatments) |

**Multi-Dimensional Threats**: 8 damage scenarios affect 3+ SFOP dimensions (DS-IVI-003, DS-IVI-007, DS-CAN-001, DS-CAN-003, DS-EXT-001, DS-BCK-001)  
**Most Critical Dimension**: **Safety** (6 high-impact scenarios), driven by CAN message injection threats capable of enabling vehicle control at highway speeds  
**Safety-Critical Residual Risk**: 5 safety-related threats with RV ≥ 3 after treatment (TS-CAN-001, TS-CAN-003, TS-IVI-001 with hypervisor escape, TS-EXT-001 with OTA compromise, TS-BCK-001 with backend compromise)

---

## Cybersecurity Goals Summary

<!-- EXAMPLE: This section demonstrates CSG coverage with real counts from csg.md -->

### CSG Implementation Status (Source: [data/csg.md](data/csg.md))

| Metric | Count | Percentage |
|--------|-------|------------|
| **Total Cybersecurity Goals** | 12 | 100% |
| **Confidentiality-Focused Goals** | 4 | 33.3% |
| **Integrity-Focused Goals** | 5 | 41.7% |
| **Availability-Focused Goals** | 2 | 16.7% |
| **Multi-Property Goals** | 1 | 8.3% |
| **Goals with Treatment** | 12 | 100% |
| **Orphan Goals** | 0 | 0% |

**Data Quality Alert**: 0 orphan goals (all 12 CSG entries have ≥1 related damage scenario). CSG-IVI-03, CSG-CAN-01, CSG-CAN-03, CSG-BCK-01 address multiple damage scenarios enabling defense-in-depth.  
**Recommended Action**: All cybersecurity goals have associated risk treatments. Proceed with requirement derivation using CSG statements as basis for cybersecurity requirements specification per ISO 21434 Clause 8.4.

---

## Compliance and Standards References

<!-- EXAMPLE: This section demonstrates standards mapping with real TS/DS counts -->

### ISO 21434 and UN R155 Mapping

**ISO 21434:2021 Coverage**:
- **Clause 8.4**: Work products documented in this Overall Report (summary of cybersecurity analyses for Type Approval submission)
- **Clause 15.6**: Damage scenario analysis - 18 damage scenarios defined ([data/ds.md](data/ds.md)) covering Safety, Financial, Operational, Privacy dimensions per ISO/SAE 21434 methodology
- **Clause 15.7**: Threat scenario analysis - 21 threat scenarios identified ([data/ts.md](data/ts.md)) with AFR ratings per ISO methodology
- **Clause 15.8**: Risk assessment - 4 RV-5 + 14 RV-4 risks quantified using Impact × AFR matrix
- **Clause 15.9**: Cybersecurity goals - 12 CSG entries established ([data/csg.md](data/csg.md)) with "shall" requirements for security properties

**UN R155 Annex 5 Threat Categories**: 100% coverage  
Categories addressed: Backend server threats (BCK domain), Communication channels (CAN, OTA, EXT domains), Firmware updates (OTA domain), External interfaces (EXT domain), Vehicle data access (IVI domain), In-vehicle networks (CAN domain)

### Framework Coverage Statistics

| Framework | Mapped Threat Count | Coverage Percentage |
|-----------|---------------------|---------------------|
| **MITRE ATT&CK ICS** | 15 | 71.4% |
| **OWASP References** | 19 | 90.5% |
| **Real CVE Examples** | 18 | 85.7% |

**Traceability Assurance**: 100% of threat scenarios have complete Asset → DS → TS → RT → CSG chains documented. All damage scenarios linked to ≥1 cybersecurity goal. All cybersecurity goals have ≥1 associated risk treatment.

---

## Recommendations

<!-- EXAMPLE: This section demonstrates actionable recommendations based on risk analysis -->

### Immediate Actions Required

1. **Implement CAN SecOC (Secure Onboard Communication)** for all safety-critical CAN message IDs to prevent spoofing and injection attacks. AFR reduction from 8 (Medium) to 11 (Low) requires cryptographic message authentication using HSM-protected MAC keys per ISO 11898-6.

2. **Harden Gateway ECU Firewall Rules** with comprehensive CAN ID filtering covering all Powertrain, Chassis, ADAS message ranges. Restrict Head Unit from sending command messages to safety networks (whitelist only diagnostic queries).

3. **Restrict App Installation to OEM-Certified App Store** with mandatory PKI code signing verification (RSA-2048/ECDSA P-256). Disable third-party app stores and USB side-loading to block malicious app delivery vector (TS-IVI-001).

4. **Deploy Multi-Signature Firmware Signing** (M-of-N threshold, e.g., 3-of-5) for OTA firmware releases to prevent single-point backend compromise. Implement eFuse anti-rollback counter in SoC to prevent downgrade attacks.

5. **Implement Runtime Integrity Monitoring** on Android and QNX guest OSes using Address Space Layout Randomization (ASLR), Data Execution Prevention (DEP), and stack canaries to detect privilege escalation attempts (AFR increase targets Specialist Expertise factor).

### Strategic Priorities

**Q2 2026**: 
- Finalize CAN SecOC implementation roadmap with OEM and tier-1 suppliers
- Conduct penetration testing on Gateway firewall rules to identify bypass techniques
- Deploy PKI code signing infrastructure for OEM app store integration

**Q3 2026**:
- Deploy firmware multi-signature scheme in backend OTA infrastructure
- Implement eFuse anti-rollback counter support in QAM8295 firmware
- Establish bug bounty program for community vulnerability disclosure

**Q4 2026**:
- Roll out OTA updates for all active CVEs (CVE-2025-32059 Bluetooth, CVE-2019-2215 Android kernel, CVE-2025-21460 QNX hypervisor)
- Complete Type Approval documentation per UN R155 Clause 6.2
- Begin fleet deployment of hardened firmware with all recommended security controls

### Compliance Next Steps

1. **Type Approval Submission**: Present Overall Report and detailed risk assessment to OEM Type Approval authorities (NHTSA, NRCAN, EU Type Approval) demonstrating compliance with UN R155 Annex 5 threat categories.

2. **Cybersecurity Requirements Specification**: Derive ISO 21434 Clause 8.4 cybersecurity requirements (CSR) from 12 cybersecurity goals, map to specific security controls in risk treatments.

3. **Functional Safety Integration**: Map RV-4 and RV-5 threats with Safety impact (6 scenarios) to ISO 26262 ASIL levels (target ASIL-D for vehicle control scenarios), implement corresponding safety controls (dual-channel messaging, watchdog timers).

4. **Regulatory Reporting**: Submit evidence of threat analysis, risk assessment, and treatment planning per China GB 44495 requirements for automotive data security.

---

## Audit Trail

**Report Generated By**: TARA Automated Analysis System  
**Generation Tool**: TaraOK Risk Treatment Catalogue Report Generator v1.0
**Data Hash (MD5)**: `a1c2d3e4f5g6h7i8j9k0l1m2n3o4p5q6` (placeholder - compute from actual data files)  
**Report Version**: 1.0-example

**Data Collection Period**: 2026-03-18 to 2026-03-25  
**Next Review Date**: 2026-09-25 (6-month review cycle per ISO 21434)

---

**Appendix**: For detailed traceability chains and domain-specific analysis, refer to:
- **Traceability Report**: Complete Asset → DS → TS → RT → CSG mappings with cross-references
- **Multi-layer Report**: Domain-grouped threat analysis with cross-domain dependencies (attack trees from AT-*.md)
- **Treatment Effectiveness Report**: Residual AFR and risk reduction metrics per control implementation phase
