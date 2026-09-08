# Risk Treatment Schema - ISO 21434 TARA

This document defines the required fields for risk treatment documentation in ISO 21434 TARA (Threat Analysis and Risk Assessment) workflows, aligned with Clause 15.8 (Risk Treatment Decision).

---

## Required Fields

Every risk treatment entry in the RT catalogue follows the same 14-field structure. Some fields are common to every entry, while others are required only for specific treatment types.

### 1. RT-ID

**Format**: `RT-[DOMAIN]-[NNN]`

**Description**: Unique identifier for the risk treatment entry following a structured naming convention based on the affected vehicle domain. RT-ID numbers MUST match the corresponding TS-ID numbers to maintain traceability.

**Domain Codes**:
- `CAN` - CAN bus and in-vehicle networking
- `OTA` - Over-the-air updates and remote services
- `EXT` - External interfaces and physical access points
- `BCK` - Backend/cloud services and infrastructure
- `IVI` - Infotainment and in-vehicle information systems
- `IMM` - Immobilizer and vehicle access control
- `ADAS` - Advanced driver assistance systems

**Example**: `RT-IVI-001`, `RT-CAN-012`, `RT-ADAS-005`

**Rules**:
- RT-ID MUST match the corresponding TS-ID number (e.g., RT-IVI-001 ↔ TS-IVI-001)
- Use zero-padded 3-digit numbers (001, 002, ..., 999)
- Domain code must match the threat scenario domain
- One risk treatment entry per threat scenario

**Numbering Alignment**:
```
TS-IVI-001 → RT-IVI-001 (same number)
TS-CAN-005 → RT-CAN-005 (same number)
TS-OTA-012 → RT-OTA-012 (same number)
```

---

### 2. Title

**Format**: Human-readable text (maximum 80 characters)

**Description**: Concise, descriptive name for the risk treatment that identifies the threat and treatment approach.

**Example**: 
- "Location Tracking Threat - Reduce via Encryption"
- "CAN Message Injection - Reduce via SecOC Authentication"
- "USB Malware Attack - Accept with Monitoring"
- "Backend API Bypass - Avoid via Architecture Change"

**Rules**:
- Include threat context and treatment decision type
- Use action-oriented language describing the treatment
- Keep under 80 characters for readability
- Be specific enough to distinguish from similar risk treatments

---

### 3. Related TS-ID

**Format**: Threat Scenario ID from TS catalogue

**Description**: The threat scenario that this risk treatment addresses. Links the RT entry to the specific threat being treated.

**Example**:
```
Related TS-ID: TS-IVI-001 (Unauthorized Location Tracking via GNSS Data Exfiltration)
```

**Rules**:
- Must reference a valid TS-ID that exists in `data/ts.md`
- Include both the ID and the threat scenario title for clarity
- One RT entry per TS-ID (1:1 relationship)
- If ts.md doesn't exist yet, mark as `[EXAMPLE]` during skill development

---

### 4. Related DS-ID

**Format**: Damage Scenario ID from DS catalogue

**Description**: The damage scenario that this risk treatment aims to prevent or mitigate. Links the RT entry to the potential damage.

**Example**:
```
Related DS-ID: DS-IVI-001 (Unauthorized Driver Location Tracking)
```

**Rules**:
- Must reference a valid DS-ID that exists in `data/ds.md`
- Include both the ID and the damage scenario title
- DS-ID is typically obtained from the Related TS-ID entry
- Multiple RT entries may reference the same DS-ID (many-to-one relationship)

---

### 5. Impact Score

**Format**: Integer 1-4 with SFOP dimension breakdown

**Description**: The impact level of the damage scenario being prevented, inherited from the related DS-ID. Uses SFOP (Safety, Financial, Operational, Privacy) assessment.

**Example**:
```
Impact Score: 4 (Critical)
- Safety: 1 (Negligible) - No physical harm from tracking
- Financial: 3 (Severe) - GDPR fines up to €20M/4% revenue
- Operational: 1 (Negligible) - All vehicle functions remain available
- Privacy: 4 (Critical) - Persistent tracking revealing sensitive life patterns

Overall Impact: 4 (Critical) [max of S=1, F=3, O=1, P=4]
```

**Impact Levels**:
- **1 - Negligible**: Minimal impact, no significant harm
- **2 - Moderate**: Noticeable impact, limited harm
- **3 - Severe**: Serious impact, substantial harm
- **4 - Critical**: Severe impact, catastrophic harm

**Rules**:
- Copy Impact Score directly from the related DS-ID entry in `data/ds.md`
- Include all four SFOP dimension ratings with brief justification
- Overall Impact is the MAXIMUM of the four dimensions
- Do not modify or re-assess impact at the RT stage

---

### 6. AFR Score

**Format**: Integer 0-15 with 5-factor breakdown and rating band

**Description**: The Attack Feasibility Rating from the related threat scenario, indicating how difficult the attack is for an attacker to execute.

**Example**:
```
AFR Score: 10 (AFR: Moderate Feasibility)

Factor Breakdown:
1. Elapsed Time: 2 (< 1 day with OBD-II access)
2. Specialist Expertise: 2 (Proficient - requires CAN protocol knowledge)
3. Knowledge of Item: 2 (Public - CAN frame formats documented)
4. Window of Opportunity: 2 (Moderate - requires physical vehicle access)
5. Equipment: 2 (Specialized - CAN adapter hardware required)

Total: 2+2+2+2+2 = 10 (AFR: Moderate Feasibility = more accessible to attacker)
```

**AFR Rating Bands**:
- **0-4 (AFR: Very Low Feasibility)**: Attack is very difficult → **Lower risk** for defender
- **5-9 (AFR: Low Feasibility)**: Attack requires moderate effort → **Medium risk**
- **10-13 (AFR: Moderate Feasibility)**: Attack is more accessible → **Higher risk** for defender
- **14-15 (AFR: High Feasibility)**: Attack has minimal barriers → **Very high risk**

**Rules**:
- Copy AFR Score directly from the related TS-ID entry
- Include all 5 factor scores with brief justification
- Note the rating band (Very Low / Low / Moderate / High Feasibility)
- Lower AFR scores = harder for attacker = better for defender

---

### 7. Risk Value (RV)

**Format**: Integer 1-5 calculated from Impact × AFR matrix

**Description**: The risk level calculated by combining Impact Score and AFR Score using the ISO 21434 risk value matrix. This determines the required treatment approach.

**Example**:
```
Risk Value: RV 5 (Highest Risk)

Calculation: Impact 4 (Critical) × AFR Moderate Feasibility (10-13) → RV 5
```

**Risk Value Matrix**:

| Impact Level | AFR: Very Low Feasibility (0-4) | AFR: Low Feasibility (5-9) | AFR: Moderate Feasibility (10-13) | AFR: High Feasibility (14-15) |
|--------------|----------------------------------|-----------------------------|-----------------------------------|-------------------------------|
| **4 - Critical** | RV 3 | RV 4 | RV 5 | RV 5 |
| **3 - Severe** | RV 2 | RV 3 | RV 4 | RV 5 |
| **2 - Moderate** | RV 2 | RV 3 | RV 3 | RV 4 |
| **1 - Negligible** | RV 1 | RV 2 | RV 2 | RV 3 |

**Risk Value Range**: 1 (lowest risk) to 5 (highest risk)

**Rules**:
- Calculate RV using the matrix above
- Document the calculation steps (Impact level × AFR band → RV)
- RV determines treatment guidelines (see Treatment Decision field)
- Higher RV = more stringent treatment required

---

### 8. Treatment Decision

**Format**: One of four options: Avoid / Reduce / Transfer / Accept

**Description**: The selected risk treatment approach based on Risk Value, technical feasibility, and organizational risk appetite.

**Treatment Options**:

1. **Avoid**: Eliminate the risk by removing functionality or redesigning the system
   - Used when: RV 5 and no viable Reduce option exists
   - Example: Remove OBD-II port entirely to eliminate physical CAN access risk

2. **Reduce**: Implement security controls that make the attack harder, usually lowering the numeric AFR
   - Used when: RV 3-5 (mitigation required)
   - Example: Implement CAN message authentication (SecOC) to reduce injection risk

3. **Transfer**: Shift risk responsibility to another party (supplier, insurance, OEM)
   - Used when: RV 3-4 and responsibility sits primarily with supplier, service-provider, or other transferred scope
   - Example: Transfer cloud backend security risk to telematics service provider

4. **Accept**: Consciously accept the risk without additional controls
   - Used when: RV 1-2 (low risk) or RV 3 with formal justification
   - Example: Accept USB firmware update risk with user authentication requirement

**Example**:
```
Treatment Decision: Reduce

Rationale: RV 5 mandates mitigation. CAN message injection poses safety-critical 
risk. Secure Onboard Communication (SecOC) authentication is feasible and 
industry-standard for automotive CAN networks.
```

**Rules**:
- Select ONE treatment option (Avoid/Reduce/Transfer/Accept)
- Justify the decision based on RV, feasibility, and organizational policy
- Follow treatment guidelines for each RV level (see Risk Value field)
- Document why other treatment options were not chosen (if relevant)

---

### 9. Treatment Description

**Format**: Narrative text (2-4 sentences, 100-200 words)

**Description**: Detailed explanation of what treatment is being implemented, how it addresses the threat, and what changes are required.

**Example**:
```
Treatment Description:

Implement CAN message authentication using AUTOSAR Secure Onboard Communication 
(SecOC) specification. All safety-critical CAN messages will be cryptographically 
authenticated using CMAC (Cipher-based Message Authentication Code) with AES-128 
keys provisioned during manufacturing. Gateway ECU will validate message 
authentication codes before forwarding frames to downstream CAN buses. Unauthenticated 
messages from unknown sources (e.g., OBD-II port) will be dropped and logged for 
security monitoring.
```

**Required Components**:
1. **What**: Specific controls or actions being taken
2. **How**: Technical approach or methodology
3. **Where**: Which components/assets are affected
4. **Effect**: How this reduces risk or addresses the threat

**Rules**:
- Be specific about the treatment approach at the control-category level
- Focus on WHAT is being done and why; keep algorithm/product details for downstream CSR work unless a short illustrative parenthetical helps readability
- Reference industry standards where applicable (AUTOSAR, ISO, etc.)
- Explain how the treatment reduces AFR or prevents damage
- Write 2-4 complete sentences (100-200 words)

---

### 10. Control Categories

**Format**: List of control category names (for Reduce treatments only)

**Description**: High-level categories of security controls being applied to reduce the risk. This field documents the TYPE of controls, not specific implementations.

**Control Category Taxonomy**:
- **Encryption**: Data at rest or in transit encryption
- **Authentication**: Message, device, or user authentication
- **Access Control**: Permission models, role-based access, authorization
- **Secure Boot**: Boot integrity verification, trusted boot chains
- **Code Signing**: Software authenticity verification
- **Intrusion Detection**: Anomaly detection, security monitoring
- **Network Segmentation**: Isolation, gateway filtering, firewalling
- **Input Validation**: Data sanitization, bounds checking
- **Secure Storage**: Protected key storage (HSM, TEE), encrypted storage
- **Physical Security**: Tamper detection, secure enclosures
- **Update Security**: Secure OTA, rollback protection, version control
- **Logging & Audit**: Security event logging, forensics

**Example**:
```
Control Categories:
- Authentication (message authentication for safety-critical CAN traffic)
- Secure Storage (protected key storage)
- Intrusion Detection (gateway monitoring for unauthenticated messages)
```

**Rules**:
- Required for "Reduce" treatment decisions ONLY
- List 1-5 control categories (not specific products or code-level implementations)
- Use categories from the taxonomy above
- Explain in parentheses how each category applies to this treatment
- Leave blank for Avoid/Transfer/Accept decisions

---

### 11. Residual AFR

**Format**: Re-scored AFR (0-15) with factor-by-factor justification

**Description**: The new Attack Feasibility Rating AFTER security controls are applied (for Reduce treatments). Shows how controls reduce attack feasibility by making specific factors more difficult.

**Example**:
```
Residual AFR: 7 (AFR: Low Feasibility) - DOWN FROM 10 (AFR: Moderate Feasibility)

Factor Re-Scoring:
1. Elapsed Time: 2 → 2 (Unchanged - attack duration not affected by authentication)
2. Specialist Expertise: 2 → 1 (Proficient → Expert - now requires cryptanalysis expertise)
3. Knowledge of Item: 2 → 1 (Public → Sensitive - key derivation algorithms confidential)
4. Window of Opportunity: 2 → 2 (Unchanged - physical access requirement remains)
5. Equipment: 2 → 1 (Specialized → Specialized but harder to obtain - requires HSM bypass tools, not standard CAN adapters)

Total: 2+1+1+2+1 = 7 (3-point reduction due to authentication controls)

Rationale: SecOC authentication significantly raises attacker skill requirements. 
Without knowledge of AES-128 keys stored in HSM, attacker must perform cryptanalysis 
or HSM extraction, requiring nation-state level resources.
```

**Rules**:
- Required for "Reduce" treatment decisions ONLY
- Re-score EACH of the 5 AFR factors (don't just reduce the total)
- Justify EACH factor change (or why it stayed the same)
- Controls should primarily affect: Specialist Expertise, Knowledge of Item, Equipment
- Calculate new total and rating band
- Document total AFR reduction (e.g., "5-point reduction")
- Leave blank for Avoid/Transfer/Accept decisions

---

### 12. Residual Risk Value

**Format**: Recalculated RV (1-5) after applying Residual AFR

**Description**: The new Risk Value after security controls are implemented, showing the effectiveness of the risk treatment.

**Example**:
```
Residual Risk Value: RV 4 (DOWN FROM RV 5)

Calculation: Impact 4 (Critical) × Residual AFR Low Feasibility (7) → RV 4

Risk Reduction: RV 5 → RV 4 (1-level reduction)
Treatment Effectiveness: Residual risk is still high (RV 4). Additional defense-in-depth controls may still be appropriate depending on project risk appetite and compliance expectations.
```

**Rules**:
- Required for "Reduce" treatment decisions ONLY
- Recalculate using Impact × Residual AFR matrix (same matrix as original RV)
- Impact Score does NOT change (damage potential remains the same)
- Only the AFR band changes based on Residual AFR
- Document risk reduction level (e.g., "RV 5 → RV 4")
- Comment on whether residual risk is acceptable
- Leave blank for Avoid/Transfer/Accept decisions

---

### 13. Acceptance Documentation

**Format**: Structured documentation (for Accept decisions only)

**Description**: Formal documentation required when consciously accepting a risk without additional mitigation. Records risk level, business rationale, approval authority, and review schedule.

**Example**:
```
Acceptance Documentation:

Risk Level: RV 2 (Low Risk)

Business Rationale: USB firmware update functionality is required for service center 
operations and field diagnostics. User authentication (technician login) provides 
adequate access control. Cost of implementing secure boot verification ($2M NRE + 
$15/vehicle BOM) outweighs residual risk exposure for non-safety-critical infotainment 
updates. Attack requires physical access and authenticated user credentials.

Approval Authority: Chief Information Security Officer (CISO) - Jane Smith
Approval Date: 2026-03-15
Review Date: 2026-09-15 (6-month review cycle)

Conditions for Acceptance:
- Technician authentication remains enabled
- USB update logs monitored quarterly
- Incident response plan covers firmware tampering scenarios
- Review if new USB vulnerabilities emerge (CVE monitoring)
```

**Required Components** (for Accept decisions):
1. **Risk Level**: RV score being accepted
2. **Business Rationale**: Why accepting the risk (cost/benefit, operational need)
3. **Approval Authority**: Name, title, and approval date
4. **Review Date**: When risk will be reassessed
5. **Conditions**: Compensating controls or monitoring in place

**Rules**:
- Required for "Accept" treatment decisions ONLY
- Must document formal approval by authorized decision-maker
- Must justify why risk is acceptable (business rationale)
- Must set review date (typically 6-12 months)
- Must document any compensating controls or monitoring
- Leave blank for Avoid/Reduce/Transfer decisions

---

### 14. Last Updated

**Format**: ISO 8601 date (YYYY-MM-DD)

**Description**: The date when this risk treatment entry was last modified. Maintains traceability for risk management reviews and audits.

**Example**:
```
Last Updated: 2026-03-19
```

**Rules**:
- Use ISO 8601 date format (YYYY-MM-DD)
- Update whenever ANY field in the RT entry changes
- Include in initial RT creation
- Critical for audit trails and risk management reviews

---

## Schema Validation Checklist

Use this checklist to verify RT entries are complete:

- [ ] **RT-ID**: Format `RT-[DOMAIN]-[NNN]`, matches corresponding TS-ID number
- [ ] **Title**: Present, descriptive, under 80 characters
- [ ] **Related TS-ID**: Valid reference to `data/ts.md` (or marked [EXAMPLE])
- [ ] **Related DS-ID**: Valid reference to `data/ds.md`
- [ ] **Impact Score**: Integer 1-4 with SFOP breakdown, copied from DS
- [ ] **AFR Score**: Integer 0-15 with 5-factor breakdown, copied from TS
- [ ] **Risk Value**: Integer 1-5, calculated from Impact × AFR matrix
- [ ] **Treatment Decision**: ONE of: Avoid / Reduce / Transfer / Accept
- [ ] **Treatment Description**: 2-4 sentences, 100-200 words, explains the treatment
- [ ] **Control Categories**: Present for Reduce decisions, blank otherwise
- [ ] **Residual AFR**: Present for Reduce decisions with factor re-scoring, blank otherwise
- [ ] **Residual Risk Value**: Present for Reduce decisions with RV recalculation, blank otherwise
- [ ] **Acceptance Documentation**: Present for Accept decisions with formal approval, blank otherwise
- [ ] **Last Updated**: ISO 8601 date format

---

## Field Dependencies by Treatment Type

Different treatment decisions require different fields:

### For "Reduce" Treatment:
- All 14 fields REQUIRED
- Control Categories MUST be populated (1-5 categories)
- Residual AFR MUST be re-scored with factor justifications
- Residual Risk Value MUST be recalculated

### For "Avoid" Treatment:
- Fields 1-9 REQUIRED (RT-ID through Treatment Description)
- Control Categories: LEAVE BLANK
- Residual AFR: LEAVE BLANK (risk eliminated, not reduced)
- Residual Risk Value: LEAVE BLANK
- Acceptance Documentation: LEAVE BLANK

### For "Transfer" Treatment:
- Fields 1-9 REQUIRED
- Treatment Description MUST document transfer recipient (Supplier/Insurance/OEM)
- Control Categories: LEAVE BLANK
- Residual AFR: LEAVE BLANK
- Residual Risk Value: LEAVE BLANK
- Acceptance Documentation: LEAVE BLANK

### For "Accept" Treatment:
- Fields 1-9 REQUIRED
- Control Categories: LEAVE BLANK
- Residual AFR: LEAVE BLANK
- Residual Risk Value: LEAVE BLANK
- Acceptance Documentation: REQUIRED (formal approval with authority)

---

## Cross-Reference Validation

When creating RT entries, verify:

1. **TS-ID Alignment**: RT-ID number matches TS-ID number (RT-IVI-001 ↔ TS-IVI-001)
2. **DS-ID Validity**: Related DS-ID exists in `data/ds.md`
3. **TS-ID Validity**: Related TS-ID exists in `data/ts.md` (or marked [EXAMPLE] if not yet created)
4. **Impact Score Match**: Impact Score matches the DS entry exactly
5. **AFR Score Match**: AFR Score matches the TS entry exactly
6. **RV Calculation**: Risk Value correctly calculated from Impact × AFR matrix
7. **Residual RV Calculation**: Residual Risk Value correctly calculated from Impact × Residual AFR

---

*Schema Version: 1.0*  
*Last Updated: 2026-03-20*  
*Aligned with: ISO 21434:2021 Clause 15.8*
