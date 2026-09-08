# Risk Treatment Methodology Guide - ISO 21434 TARA

This guide provides methodology for risk treatment decision-making in ISO 21434 TARA (Threat Analysis and Risk Assessment) workflows, aligned with Clause 15.8 (Risk Treatment Decision).

---

## Overview

Risk treatment is the process of selecting and implementing measures to modify risk. After calculating Risk Value (RV) from Impact × AFR, analysts must decide which treatment approach to apply based on risk level, technical feasibility, cost-effectiveness, and organizational risk appetite.

**Four Treatment Options (ISO 31000)**:
1. **Avoid** - Eliminate risk by removing functionality or redesigning
2. **Reduce** - Implement security controls that make the attack harder and usually lower the numeric AFR
3. **Transfer** - Shift risk responsibility to another party
4. **Accept** - Consciously accept risk without additional controls

---

## Risk Value Matrix

Risk Value (RV) is calculated by combining Impact Score (from Damage Scenarios) with AFR Score (from Threat Scenarios):

| Impact Level | AFR: Very Low Feasibility (0-4) | AFR: Low Feasibility (5-9) | AFR: Moderate Feasibility (10-13) | AFR: High Feasibility (14-15) |
|--------------|----------------------------------|-----------------------------|-----------------------------------|-------------------------------|
| **4 - Critical** | RV 3 | RV 4 | RV 5 | RV 5 |
| **3 - Severe** | RV 2 | RV 3 | RV 4 | RV 5 |
| **2 - Moderate** | RV 2 | RV 3 | RV 3 | RV 4 |
| **1 - Negligible** | RV 1 | RV 2 | RV 2 | RV 3 |

**Risk Value (RV)** ranges from 1 (lowest risk) to 5 (highest risk).

### Understanding the Matrix

**Impact Score** (1-4): Severity of damage if threat succeeds
- Derived from SFOP assessment (Safety, Financial, Operational, Privacy)
- Takes the MAXIMUM of the four dimensions
- Does NOT change during risk treatment (damage potential remains constant)

**AFR Score** (0-15): Attack Feasibility Rating
- Lower scores (0-4) = harder for attacker = better for defender
- Higher scores (10-15) = easier for attacker = worse for defender
- CAN be lowered numerically via security controls in "Reduce" treatment

**AFR Rating Bands**:
- **0-4 (AFR: Very Low Feasibility)**: Attack very difficult → Lower risk for organization
- **5-9 (AFR: Low Feasibility)**: Attack requires moderate effort → Medium risk
- **10-13 (AFR: Moderate Feasibility)**: Attack more accessible → Higher risk
- **14-15 (AFR: High Feasibility)**: Attack easily executable → Very high risk

---

## Treatment Decision Guidelines

### RV 5: Highest-Priority Treatment

**Risk Level**: Highest risk - usually unacceptable without documented treatment

**Recommended Treatment**: Avoid or Reduce

**Decision Criteria**:
- **Avoid** if functionality can be removed or redesigned to eliminate risk entirely
- **Reduce** if functionality is essential and viable security controls exist
- **Transfer** is rarely sufficient as a standalone treatment for RV 5
- **Accept** requires exceptional documented rationale and governance approval for RV 5

**Examples**:
- RV 5 from Impact 4 (Critical) × AFR Moderate Feasibility (10-13)
- RV 5 from Impact 4 (Critical) × AFR High Feasibility (14-15)
- RV 5 from Impact 3 (Severe) × AFR High Feasibility (14-15)

**Typical Scenarios**:
- Safety-critical CAN bus injection (DS-CAN-001)
- Remote code execution on safety ECU (DS-ADAS-*)
- Unauthorized vehicle immobilization (DS-IMM-*)

---

### RV 4: High-Priority Treatment

**Risk Level**: High risk - usually requires active mitigation

**Recommended Treatment**: Reduce

**Decision Criteria**:
- **Reduce** is the default approach (implement security controls)
- **Transfer** may be acceptable if supplier has better capability
- **Avoid** is preferred if functionality is non-essential
- **Accept** is usually difficult to justify and requires exceptional documentation

**Examples**:
- RV 4 from Impact 4 (Critical) × AFR Low Feasibility (5-9)
- RV 4 from Impact 3 (Severe) × AFR Moderate Feasibility (10-13)
- RV 4 from Impact 2 (Moderate) × AFR High Feasibility (14-15)

**Typical Scenarios**:
- Infotainment malware execution (DS-IVI-003)
- Backend API authentication bypass (DS-BCK-001)
- USB firmware tampering (DS-EXT-001)

---

### RV 3: Reduce or Transfer First, Accept by Exception

**Risk Level**: Medium risk - mitigation recommended

**Recommended Treatment**: Reduce or Transfer

**Decision Criteria**:
- **Reduce** if cost-effective security controls are available
- **Transfer** if risk is outside current scope (e.g., cloud services, supplier components)
- **Accept** may be acceptable with formal justification and compensating controls
- **Avoid** if functionality provides limited value

**Examples**:
- RV 3 from Impact 4 (Critical) × AFR Very Low Feasibility (0-4)
- RV 3 from Impact 3 (Severe) × AFR Low Feasibility (5-9)
- RV 3 from Impact 2 (Moderate) × AFR Low Feasibility (5-9) or Moderate Feasibility (10-13)
- RV 3 from Impact 1 (Negligible) × AFR High Feasibility (14-15)

**Typical Scenarios**:
- User personal data exposure (DS-IVI-002)
- Gateway ECU DoS via malformed messages (DS-CAN-002)
- Physical tampering detection bypass (DS-EXT-002)

---

### RV 2: Risk Accepted with Monitoring

**Risk Level**: Low risk - acceptance with documentation

**Recommended Treatment**: Accept (with documentation)

**Decision Criteria**:
- **Accept** is the typical approach (formal risk acceptance with monitoring)
- **Reduce** if very low-cost controls are available (defense-in-depth)
- **Transfer** if another party accepts responsibility for this risk
- **Avoid** is generally not cost-effective for RV 2

**Examples**:
- RV 2 from Impact 3 (Severe) × AFR Very Low Feasibility (0-4)
- RV 2 from Impact 2 (Moderate) × AFR Very Low Feasibility (0-4)
- RV 2 from Impact 1 (Negligible) × AFR Low Feasibility (5-9) or Moderate Feasibility (10-13)

**Typical Scenarios**:
- Diagnostic data exfiltration (non-PII telemetry)
- Infotainment cosmetic UI manipulation
- Non-safety sensor spoofing

---

### RV 1: Risk Accepted, No Action Required

**Risk Level**: Lowest risk - minimal concern

**Recommended Treatment**: Accept (minimal documentation)

**Decision Criteria**:
- **Accept** with minimal formal process
- **Reduce** only if controls are essentially free (already implemented)
- **Transfer** and **Avoid** are not cost-effective

**Examples**:
- RV 1 from Impact 1 (Negligible) × AFR Very Low Feasibility (0-4)

**Typical Scenarios**:
- Non-sensitive configuration changes
- Cosmetic display modifications
- Non-privileged user preference tampering

---

## Treatment Option Details

### Option 1: Avoid

**Definition**: Eliminate the risk by removing functionality, eliminating the attack surface, or redesigning the system architecture.

**When to Use**:
- RV 5 and no viable Reduce option exists
- Functionality provides limited value and can be removed
- Architectural redesign is feasible and cost-effective
- Risk elimination is required by regulation or policy

**Approach**:
- Remove vulnerable functionality entirely
- Redesign system to eliminate attack surface
- Replace risky architecture with secure alternative

**Examples**:

1. **Remove OBD-II Diagnostic Port**
   - Threat: TS-CAN-001 (CAN Message Injection via OBD-II)
   - Risk: RV 5 (Critical Impact × Low AFR)
   - Treatment: Remove physical OBD-II port from production vehicles
   - Effect: Eliminates physical CAN access attack surface entirely
   - Trade-off: Diagnostic access via wireless connection only

2. **Eliminate Internet Connectivity for Safety ECU**
   - Threat: TS-ADAS-005 (Remote Code Execution on ADAS ECU)
   - Risk: RV 5
   - Treatment: Isolate ADAS ECU from telematics network (no internet access)
   - Effect: Eliminates remote attack surface for safety-critical system
   - Trade-off: ADAS updates require USB or dealer service center

3. **Replace Cloud Storage with Local-Only Storage**
   - Threat: TS-BCK-001 (Backend Database Breach Exposing User PII)
   - Risk: RV 4
   - Treatment: Store user preferences locally only, no cloud sync
   - Effect: Eliminates cloud attack surface for user data
   - Trade-off: Users lose multi-device synchronization

**Residual Risk**: Near-zero (attack surface removed)

**Documentation Requirements**:
- RT-ID, Title, Related TS-ID/DS-ID, Impact, AFR, RV
- Treatment Decision: "Avoid"
- Treatment Description: What functionality is removed/redesigned and why
- No Control Categories, Residual AFR, or Acceptance Documentation needed

---

### Option 2: Reduce

**Definition**: Implement security controls that make the attack harder for an attacker to execute, usually lowering the numeric Attack Feasibility Rating (AFR).

**When to Use**:
- RV 3-5 (medium to high risk requiring mitigation)
- Functionality is essential and cannot be removed
- Viable security controls exist (technical feasibility)
- Cost-effective compared to risk exposure

**Approach**:
- Add security controls to increase attack barriers
- Target specific AFR factors: Specialist Expertise, Knowledge of Item, Equipment
- Raise attacker skill/resource requirements
- Calculate Residual AFR after controls applied

**Control Category Taxonomy**:

1. **Encryption** - Protect data confidentiality and integrity
   - Data at rest encryption (AES-256 storage)
   - Data in transit encryption (TLS 1.3 communications)
   - End-to-end encryption for sensitive channels

2. **Authentication** - Verify identity of users, devices, or messages
   - User authentication (multi-factor authentication)
   - Device authentication (certificate-based, TPM attestation)
   - Message authentication (HMAC, digital signatures, CAN SecOC)

3. **Access Control** - Limit permissions based on roles and policies
   - Role-based access control (RBAC)
   - Principle of least privilege
   - Permission models (file system ACLs, API authorization)

4. **Secure Boot** - Verify integrity of boot chain
   - Verified boot (signed bootloader, kernel)
   - Trusted execution environment (TEE)
   - Boot attestation and measurement

5. **Code Signing** - Verify authenticity and integrity of software
   - Firmware signature verification
   - Application code signing
   - Update package authentication

6. **Intrusion Detection** - Monitor for anomalous or malicious activity
   - Network intrusion detection (CAN bus monitoring)
   - Host-based intrusion detection (syscall monitoring)
   - Anomaly detection (ML-based behavioral analysis)

7. **Network Segmentation** - Isolate components and limit lateral movement
   - Gateway filtering (CAN domains, Ethernet VLANs)
   - Firewall rules (port restrictions, protocol filtering)
   - Air-gapped networks (safety ECU isolation)

8. **Input Validation** - Sanitize and validate external inputs
   - Bounds checking (buffer overflow prevention)
   - Type validation (schema enforcement)
   - Injection prevention (SQL, command, CAN message validation)

9. **Secure Storage** - Protect cryptographic keys and sensitive data
   - Hardware Security Module (HSM) for key storage
   - Trusted Platform Module (TPM) for attestation
   - Encrypted key storage with access control

10. **Physical Security** - Protect against physical tampering
    - Tamper detection (sensors for enclosure opening)
    - Tamper-resistant packaging (epoxy-filled chips)
    - Secure enclosures (locked ECU housings)

11. **Update Security** - Protect software update process
    - Secure OTA update channels (encrypted transport)
    - Rollback protection (version monotonicity)
    - Update verification (signature checks before installation)

12. **Logging & Audit** - Record security events for forensics
    - Security event logging (authentication failures, anomalies)
    - Immutable log storage (write-once, tamper-evident)
    - Audit trail for compliance and incident response

**Residual AFR Calculation**:

When implementing "Reduce" treatment, re-score each of the 5 AFR factors to calculate Residual AFR:

1. **Elapsed Time** - Often unchanged (controls don't affect time to develop attack)
2. **Specialist Expertise** - Often decreases numerically (controls require more specialized skills)
3. **Knowledge of Item** - Often decreases (controls obscure internal details)
4. **Window of Opportunity** - May be unchanged (access requirements remain similar)
5. **Equipment** - Often decreases numerically (controls require more sophisticated tools)

**Example**:

**Original AFR**: 10 (AFR: Moderate Feasibility)
- Elapsed Time: 2 (< 1 day)
- Specialist Expertise: 2 (Expert - CAN protocol knowledge)
- Knowledge of Item: 2 (Public - CAN frame formats documented)
- Window of Opportunity: 2 (Moderate - physical vehicle access)
- Equipment: 2 (Specialized - CAN adapter)

**Controls Applied**:
- Authentication: CAN message authentication (SecOC with AES-128 CMAC)
- Secure Storage: Keys stored in HSM (Hardware Security Module)
- Intrusion Detection: Gateway monitors for unauthenticated messages

**Residual AFR**: 6 (AFR: Medium) - lower score after controls
- Elapsed Time: 2 → 1 (Longer preparation and validation time)
- Specialist Expertise: 2 → 1 (Requires deeper cryptographic and automotive expertise)
- Knowledge of Item: 2 → 1 (Key handling details become harder to obtain)
- Window of Opportunity: 2 → 2 (Unchanged - physical access still required)
- Equipment: 2 → 1 (Requires specialized HSM bypass tools, not standard adapters)

**Residual RV**: RV 4 (down from RV 5)
- Original: Impact 4 × AFR Moderate Feasibility (10) → RV 5
- Residual: Impact 4 × AFR Low Feasibility (6) → RV 4

**Documentation Requirements**:
- All 14 fields REQUIRED
- Control Categories: 1-5 categories with brief explanations
- Residual AFR: Re-score all 5 factors with justifications
- Residual Risk Value: Recalculate using Impact × Residual AFR

---

### Option 3: Transfer

**Definition**: Shift risk responsibility to another party who has better capability, resources, or risk appetite to manage the risk.

**When to Use**:
- RV 3-4 (medium-high risk)
- Risk is outside current scope (supplier components, cloud services, insurance)
- Another party has better capability to mitigate or absorb risk
- Transfer agreement is formal and documented

**Transfer Recipients**:

1. **Supplier** - Component or subsystem provider
   - Example: Telematics service provider manages backend API security
   - Contractual: Security requirements in supply agreement, liability clauses
   - Verification: Supplier security audits, certifications (ISO 27001, SOC 2)

2. **Insurance** - Risk underwriter absorbs financial consequences
   - Example: Cyber insurance policy covers breach-related costs
   - Contractual: Insurance policy with defined coverage limits
   - Verification: Policy review, premium payments, incident reporting

3. **OEM / Parent Organization** - Higher organizational level accepts risk
   - Example: Corporate cybersecurity team manages enterprise-level threats
   - Contractual: Internal risk register, escalation procedures
   - Verification: Risk governance board approval, monitoring

**Examples**:

1. **Transfer Backend Security to Cloud Provider**
   - Threat: TS-BCK-001 (Backend API Authentication Bypass)
   - Risk: RV 4 (Severe Impact × Low AFR)
   - Treatment: Transfer backend infrastructure security to AWS/Azure with formal SLA
   - Recipient: Cloud service provider (AWS, Azure, Google Cloud)
   - Contractual: Service Level Agreement with security guarantees, indemnification
   - Residual Risk: OEM retains data handling and access control responsibilities

2. **Transfer Telematics Module Security to Supplier**
   - Threat: TS-OTA-003 (Cellular Modem Exploitation)
   - Risk: RV 3 (Moderate Impact × Medium AFR)
   - Treatment: Supplier (Qualcomm, Telit) responsible for modem firmware security
   - Recipient: Telematics hardware supplier
   - Contractual: Supply agreement with security requirements, vulnerability patching SLA
   - Residual Risk: OEM retains integration and update distribution responsibilities

3. **Cyber Insurance for Data Breach Costs**
   - Threat: TS-IVI-002 (User PII Exposure via Infotainment Breach)
   - Risk: RV 3 (Severe Impact × High AFR)
   - Treatment: Cyber insurance policy covers breach notification, legal costs, regulatory fines
   - Recipient: Insurance underwriter (AIG, Beazley, Coalition)
   - Contractual: Insurance policy with $20M coverage limit, incident reporting requirements
   - Residual Risk: OEM retains technical mitigation and breach prevention responsibilities

**Documentation Requirements**:
- RT-ID, Title, Related TS-ID/DS-ID, Impact, AFR, RV
- Treatment Decision: "Transfer"
- Treatment Description: What risk is transferred, to whom, and under what terms
- Transfer To field: Supplier name / Insurance provider / OEM division
- No Control Categories, Residual AFR, or Acceptance Documentation needed

**Important Notes**:
- Transfer does NOT eliminate risk - it shifts accountability
- OEM often retains some residual responsibilities (monitoring, integration)
- Contractual agreements must formalize the transfer (SLA, insurance policy, supply agreement)

---

### Option 4: Accept

**Definition**: Consciously accept the risk without additional mitigation, based on informed decision-making and formal approval.

**When to Use**:
- RV 1-2 (low risk acceptable to organization)
- RV 3 with exceptional justification and compensating controls
- Mitigation cost outweighs risk exposure
- Residual risk after Reduce treatment is acceptable

**Decision Criteria**:
- Risk level is within organizational risk appetite
- Business rationale justifies acceptance (operational need, cost-benefit)
- Compensating controls or monitoring are in place
- Formal approval from authorized decision-maker (CISO, risk board)
- Review schedule established (6-12 month reassessment)

**Examples**:

1. **Accept USB Firmware Update Risk with Authentication**
   - Threat: TS-EXT-002 (Malicious Firmware via USB Port)
   - Risk: RV 2 (Moderate Impact × High AFR)
   - Treatment Decision: Accept with technician authentication
   - Rationale: USB update required for service center operations. Technician authentication provides access control. Secure boot verification ($2M NRE + $15/vehicle BOM) cost outweighs RV 2 risk exposure. Attack requires physical access and authenticated credentials.
   - Approval: CISO - Jane Smith, 2026-03-15
   - Review: 2026-09-15 (6-month cycle)
   - Compensating Controls: Technician authentication, USB update logs, quarterly monitoring, incident response plan

2. **Accept Diagnostic Data Exfiltration (Non-PII Telemetry)**
   - Threat: TS-IVI-008 (Telemetry Data Exfiltration via Infotainment)
   - Risk: RV 2 (Moderate Impact × High AFR)
   - Treatment Decision: Accept with data minimization
   - Rationale: Telemetry contains only anonymized vehicle performance metrics (no PII). Data supports warranty claims analysis and quality improvements. Encryption would add significant latency to real-time telemetry. Attack requires physical vehicle access or compromised telematics account.
   - Approval: Chief Privacy Officer - John Doe, 2026-03-10
   - Review: 2026-12-10 (annual review)
   - Compensating Controls: Data minimization (no PII collection), anonymization at source, retention limits (90 days), user opt-out capability

3. **Accept Infotainment Cosmetic UI Manipulation**
   - Threat: TS-IVI-010 (UI Theme Injection via USB Media)
   - Risk: RV 1 (Negligible Impact × Medium AFR)
   - Treatment Decision: Accept (minimal documentation)
   - Rationale: Cosmetic UI changes do not affect vehicle safety, operations, or user data. Attack surface limited to USB media playback. User experience degradation is minor and reversible (factory reset).
   - Approval: Product Security Manager - Alice Brown, 2026-03-01
   - Review: None (RV 1 - accept and monitor)
   - Compensating Controls: None required for RV 1

**Formal Acceptance Documentation**:

Required for **Accept** decisions (especially RV 2-3):

1. **Risk Level**: RV score being accepted (RV 1, RV 2, or RV 3)

2. **Business Rationale**: Why accepting the risk
   - Operational necessity (required for business function)
   - Cost-benefit analysis (mitigation cost > risk exposure)
   - Technical constraints (mitigation not feasible)
   - Residual risk after Reduce treatment

3. **Approval Authority**: Name, title, and approval date
   - RV 1: Product Security Manager or equivalent
   - RV 2: CISO or Chief Risk Officer
   - RV 3: Executive Risk Board or C-level approval

4. **Review Date**: When risk will be reassessed
   - RV 1: Annual or on-demand (when new threats emerge)
   - RV 2: 6-month review cycle
   - RV 3: Quarterly review (3-month cycle)

5. **Compensating Controls**: Mitigations or monitoring in place
   - Access controls (authentication, authorization)
   - Monitoring (logging, intrusion detection)
   - Incident response plans (breach response procedures)
   - User awareness (training, notification)

**Documentation Requirements**:
- RT-ID, Title, Related TS-ID/DS-ID, Impact, AFR, RV
- Treatment Decision: "Accept"
- Treatment Description: Why risk is being accepted
- Acceptance Documentation: REQUIRED (formal approval with authority)
- No Control Categories, Residual AFR, or Residual Risk Value needed

---

## Treatment Decision Flowchart

```
Start: Calculate Risk Value (RV) from Impact × AFR
│
├─ RV 5? ─ YES ─→ [Mandatory Mitigation]
│           ├─ Can functionality be removed? ─ YES ─→ AVOID
│           └─ Can functionality be removed? ─ NO ──→ REDUCE (default)
│
├─ RV 4? ─ YES ─→ [Security Controls Required]
│           ├─ Viable security controls exist? ─ YES ─→ REDUCE
│           └─ Supplier has better capability? ─ YES ─→ TRANSFER
│
├─ RV 3? ─ YES ─→ [Controls Preferred]
│           ├─ Cost-effective controls available? ─ YES ─→ REDUCE
│           ├─ Risk outside current scope? ─ YES ─→ TRANSFER
│           └─ Exceptional justification + compensating controls? ─ YES ─→ ACCEPT (with formal approval)
│
├─ RV 2? ─ YES ─→ [Accept with Documentation]
│           ├─ Very low-cost controls available? ─ YES ─→ REDUCE (defense-in-depth)
│           └─ Within risk appetite? ─ YES ─→ ACCEPT (with monitoring)
│
└─ RV 1? ─ YES ─→ ACCEPT (minimal documentation)
```

---

## Residual Risk Assessment

After selecting a treatment, assess **residual risk** - the risk remaining after treatment is applied:

### For "Avoid" Treatment:
- **Residual Risk**: Near-zero (attack surface eliminated)
- **No residual AFR calculation** (functionality removed)
- **No residual RV** (risk eliminated, not reduced)

### For "Reduce" Treatment:
- **Residual Risk**: Reduced but not eliminated
- **Calculate Residual AFR**: Re-score 5 factors after controls applied
- **Calculate Residual RV**: Impact × Residual AFR matrix
- **Target**: Document the resulting residual RV and whether the organization accepts it

### For "Transfer" Treatment:
- **Residual Risk**: Shared between OEM and transfer recipient
- **OEM retains**: Integration responsibilities, monitoring duties
- **Recipient assumes**: Specific transferred risks per contract
- **No residual AFR/RV calculation** (accountability shifted, not mitigated)

### For "Accept" Treatment:
- **Residual Risk**: Original risk remains unchanged
- **No residual AFR/RV calculation** (risk consciously accepted as-is)
- **Compensating controls**: Monitoring and incident response readiness

---

## Treatment Combinations and Multi-Stage Approaches

Some threats may require **multiple treatment stages**:

1. **Reduce + Accept**
   - Apply cost-effective security controls to lower risk
   - Accept remaining residual risk with monitoring
   - Example: Implement SecOC authentication (Reduce AFR 10→5, RV 5→4), then Accept RV 4 residual risk with IDS monitoring

2. **Transfer + Reduce**
   - Transfer primary risk to supplier/cloud provider
   - Implement integration-level controls at OEM boundary
   - Example: Transfer backend API security to AWS (Transfer), implement API key rotation at OEM side (Reduce)

3. **Avoid + Reduce**
   - Eliminate primary attack surface (Avoid)
   - Implement defense-in-depth for residual attack vectors (Reduce)
   - Example: Remove OBD-II port (Avoid CAN injection), implement SecOC on remaining CAN gateways (Reduce)

**Documentation**: Create separate RT entries for each treatment stage if they address different threat scenarios.

---

## Cost-Benefit Considerations

When selecting treatment, consider:

1. **Implementation Cost**
   - Non-recurring engineering (NRE): Development, testing, certification
   - Bill of materials (BOM): Hardware cost per vehicle
   - Operational expenses (OPEX): Maintenance, monitoring, updates

2. **Risk Exposure**
   - Potential financial loss: Regulatory fines, litigation, brand damage
   - Safety consequences: Injury, fatality (quantified via FMEA)
   - Operational impact: Downtime, warranty claims, recalls

3. **Feasibility**
   - Technical feasibility: Can controls be implemented with current technology?
   - Certification impact: Does treatment affect safety certification (UNECE, FMVSS)?
   - Supply chain readiness: Are suppliers capable of implementing controls?

4. **Time-to-Market**
   - Development timeline: Can controls be implemented before production?
   - Retrofit requirements: Can controls be deployed to existing vehicles via OTA?

**Example Cost-Benefit Analysis**:

**Threat**: TS-CAN-001 (CAN Message Injection via OBD-II)  
**Risk**: RV 5 (Critical Impact × Low AFR)

| Treatment Option | Cost | Effectiveness | Decision |
|------------------|------|---------------|----------|
| **Avoid** (Remove OBD-II port) | $20/vehicle (connector removal), regulatory compliance issues (OBD-II required in EU/US) | 100% (eliminates attack surface) | ❌ Not viable (regulatory requirement) |
| **Reduce** (SecOC authentication) | $3M NRE + $25/vehicle (HSM/gateway upgrade) | High (reduces RV 5→4) | ✅ Selected (feasible, effective) |
| **Transfer** (Supplier responsibility) | $0 upfront, higher component cost from supplier | Depends on supplier capability | ❌ Not viable (OEM architectural decision) |
| **Accept** | $0 | 0% (risk remains RV 5) | ❌ Rarely justifiable (would need exceptional approval and rationale) |

**Decision**: Reduce via SecOC authentication (cost-effective, technically feasible, meets regulatory requirements)

---

## ISO 21434 Alignment

This risk treatment methodology aligns with ISO 21434:2021 requirements:

- **Clause 15.8**: Risk treatment decision (Avoid, Reduce, Transfer, Accept)
- **Clause 15.9**: Risk treatment implementation and verification
- **Annex E**: Risk treatment option examples
- **Annex G**: Cybersecurity goals and requirements derivation (separate skill)

**Treatment Documentation Requirements** (ISO 21434 Clause 15.8):
- [ ] Treatment option selected (Avoid/Reduce/Transfer/Accept)
- [ ] Rationale for treatment selection documented
- [ ] Residual risk assessed (for Reduce treatments)
- [ ] Approval obtained from authorized decision-maker (for Accept treatments)
- [ ] Treatment implementation plan defined (what, who, when)

---

## Common Pitfalls and Best Practices

### Pitfalls to Avoid:

1. **Treating symptoms instead of root causes**
   - ❌ Wrong: Add intrusion detection for every threat without addressing vulnerabilities
   - ✅ Right: Fix authentication weakness, THEN add detection as defense-in-depth

2. **Over-reliance on Transfer**
   - ❌ Wrong: Transfer all cloud risks to provider without any OEM-side controls
   - ✅ Right: Transfer infrastructure security, implement access controls and monitoring at OEM side

3. **Accepting high risks without formal process**
   - ❌ Wrong: Accept RV 4 with email approval from manager
   - ✅ Right: Accept RV 2 with formal CISO approval, documented rationale, and review schedule

4. **Reducing AFR without justification**
   - ❌ Wrong: Claim AFR reduces from 10→5 without explaining which factors changed
   - ✅ Right: Document factor-by-factor re-scoring with control-specific justifications

5. **Ignoring cost-effectiveness**
   - ❌ Wrong: Implement $10M solution for RV 2 risk with $100K exposure
   - ✅ Right: Accept RV 2 with monitoring, save budget for RV 5 threats

### Best Practices:

1. **Start with RV 5 threats first** (mandatory mitigation)
2. **Prefer Reduce over Transfer** for safety-critical risks (retain control)
3. **Document cost-benefit analysis** for treatment decisions
4. **Set realistic Residual RV targets** (don't expect AFR 10→0)
5. **Review accepted risks periodically** (6-12 month cycles)
6. **Align treatment with organizational risk appetite** (CISO approval for RV 2-3 Accept)
7. **Use defense-in-depth** (layer multiple control categories for RV 4-5)
8. **Verify treatment effectiveness** (penetration testing, security validation)

---

## Summary

Risk treatment is a structured decision-making process:

1. **Calculate RV** from Impact × AFR matrix
2. **Select treatment** based on RV guidelines (Avoid/Reduce/Transfer/Accept)
3. **Document rationale** for treatment selection
4. **Calculate residual risk** (for Reduce treatments)
5. **Obtain approval** (for Accept treatments)
6. **Implement and verify** treatment effectiveness

**Key Principles**:
- RV 5 requires mandatory mitigation (Avoid or Reduce)
- RV 4 requires security controls (Reduce preferred)
- RV 3 allows flexibility (Reduce, Transfer, or Accept with justification)
- RV 1-2 can be accepted with monitoring
- Impact does NOT change (damage potential constant)
- AFR CAN be reduced via security controls (Reduce treatment)
- Residual risk must be assessed and documented (especially for Reduce)

---

*Guide Version: 1.0*  
*Last Updated: 2026-03-20*  
*Aligned with: ISO 21434:2021 Clause 15.8, ISO 31000:2018*
