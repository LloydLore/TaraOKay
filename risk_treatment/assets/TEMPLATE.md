# Risk Treatment Template

Use this template to document risk treatment decisions for each threat scenario. Copy this structure and fill in all 14 required fields per `references/rt-schema.md`.

---

## Section 1: Blank Template

### RT-[DOMAIN]-[NNN]: [Risk Treatment Title]
<!-- 
  RT-ID Format: RT-[DOMAIN]-[NNN]
  Domain codes: CAN | OTA | EXT | BCK | IVI | IMM | ADAS
  Number: 3-digit zero-padded (001, 002, ..., 999)
  
  RT-ID Numbering: MUST match corresponding TS-ID number
  Examples:
  - TS-IVI-001 → RT-IVI-001 (same number)
  - TS-CAN-005 → RT-CAN-005 (same number)
  
  Title Guidelines:
  - Max 80 characters
  - Include threat context and treatment decision type
  - Example: "Location Tracking Threat - Reduce via Encryption"
-->

**Related TS-ID**:
<!-- 
  Threat Scenario ID from TS catalogue (data/ts.md)
  Format: TS-[DOMAIN]-[NNN] (Threat Scenario Title)
  
  Example:
  TS-IVI-001 (Unauthorized Location Tracking via GNSS Data Exfiltration)
  
  Note: If ts.md doesn't exist yet, mark as [EXAMPLE]
-->

[TS-[DOMAIN]-[NNN] (Threat Scenario Title)]

**Related DS-ID**:
<!-- 
  Damage Scenario ID from DS catalogue (data/ds.md)
  Format: DS-[DOMAIN]-[NNN] (Damage Scenario Title)
  
  Obtained from the Related TS-ID entry
  Must be a valid DS-ID that exists in data/ds.md
  
  Example:
  DS-IVI-001 (Unauthorized Driver Location Tracking)
-->

[DS-[DOMAIN]-[NNN] (Damage Scenario Title)]

**Impact Score**:
<!-- 
  Impact score (1-4) from the related DS-ID entry
  Include SFOP breakdown showing which dimensions contribute
  
  Format:
  Impact: [1-4] ([Negligible/Moderate/Severe/Critical])
  - Safety: [1-4] ([category])
  - Financial: [1-4] ([category])
  - Operational: [1-4] ([category])
  - Privacy: [1-4] ([category])
  
  Impact Level = MAX(Safety, Financial, Operational, Privacy)
  
  Example:
  Impact: 4 (Critical)
  - Safety: 1 (Negligible) - No physical harm
  - Financial: 3 (Severe) - GDPR fines up to €20M
  - Operational: 1 (Negligible) - Vehicle functions normally
  - Privacy: 4 (Critical) - Continuous location tracking
-->

Impact: [1-4] ([Level])
- Safety: [1-4] ([category])
- Financial: [1-4] ([category])
- Operational: [1-4] ([category])
- Privacy: [1-4] ([category])

**AFR Score**:
<!-- 
  Attack Feasibility Rating (0-15) from the related TS-ID entry
  Include 5-factor breakdown
  
  Format:
  AFR: [0-15] ([Very Low/Low/Moderate/High])
  - Elapsed Time: [0-3] ([level])
  - Specialist Expertise: [0-3] ([level])
  - Knowledge of Item: [0-3] ([level])
  - Window of Opportunity: [0-3] ([level])
  - Equipment: [0-3] ([level])
  
  AFR Bands:
  - 0-4: Very Low (hardest for attacker)
  - 5-9: Low
  - 10-13: Moderate (more accessible to attacker)
  - 14-15: High (easiest for attacker)
  
  Example:
  AFR: 10 (Moderate)
  - Elapsed Time: 1 (1-6 months) - Reconnaissance and abuse setup take weeks
  - Specialist Expertise: 2 (Proficient) - Requires mobile app development skills
  - Knowledge of Item: 2 (Public with effort) - API behavior inferred from client traffic
  - Window of Opportunity: 3 (Unlimited) - API always accessible
  - Equipment: 2 (Standard automotive / test equipment) - Laptop, proxy, and device lab
-->

AFR: [0-15] ([Band])
- Elapsed Time: [0-3] ([level])
- Specialist Expertise: [0-3] ([level])
- Knowledge of Item: [0-3] ([level])
- Window of Opportunity: [0-3] ([level])
- Equipment: [0-3] ([level])

**Risk Value**:
<!-- 
  Risk Value (RV 1-5) calculated from Impact × AFR using the Risk Value Matrix
  
  Risk Value Matrix (from rt-guide.md):
  
  | Impact Level | AFR: Very Low Feasibility (0-4) | AFR: Low Feasibility (5-9) | AFR: Moderate Feasibility (10-13) | AFR: High Feasibility (14-15) |
  |--------------|----------------------------------|-----------------------------|-----------------------------------|-------------------------------|
  | 4 - Critical | RV 3            | RV 4              | RV 5             | RV 5                    |
  | 3 - Severe   | RV 2            | RV 3              | RV 4             | RV 5                    |
  | 2 - Moderate | RV 2            | RV 3              | RV 3             | RV 4                    |
  | 1 - Negligible| RV 1           | RV 2              | RV 2             | RV 3                    |
  
  Example:
  Impact 4 (Critical) × AFR 10 (Moderate Feasibility) → RV 5
-->

Risk Value: RV [1-5]
- Calculation: Impact [1-4] × AFR [Band] → RV [1-5] (from Risk Value Matrix)

**Treatment Decision**:
<!-- 
  Select ONE of the 4 treatment options:
  
  1. **Avoid**: Remove functionality or redesign to eliminate risk
     - When: RV 5 with no viable Reduce options, unacceptable risk
     - Result: Attack surface eliminated
  
  2. **Reduce**: Implement security controls that make the attack harder and usually lower the numeric AFR
     - When: RV 3-5, functionality essential, viable controls exist
     - Result: Lowered AFR, reduced residual risk
  
  3. **Transfer**: Shift risk to supplier, insurance, or OEM
     - When: RV 3-4, controls not OEM responsibility
     - Result: Risk liability transferred to third party
  
  4. **Accept**: Consciously accept risk with formal documentation
     - When: RV 1-2, or RV 3 with formal justification
     - Result: No action, risk accepted
  
  Example:
  Treatment Decision: Reduce
-->

Treatment Decision: [Avoid | Reduce | Transfer | Accept]

**Treatment Description**:
<!-- 
  Describe the treatment approach in 2-4 sentences
  
  Include:
  - What action is taken
  - How it addresses the risk
  - Why this treatment was selected
  
  For Reduce: List which AFR factors are targeted
  For Transfer: Identify the third party and transfer mechanism
  For Accept: State the rationale for acceptance
  For Avoid: Describe what functionality is removed/redesigned
  
  Example:
  "Implement end-to-end encryption (AES-256) for all location data at rest and in transit, 
  combined with role-based access control limiting location access to authorized services only. 
  Deploy Hardware Security Module (HSM) for secure key storage. This Reduce treatment targets 
  Knowledge of Item (encrypted data useless without keys) and Equipment (HSM raises barrier)."
-->

[2-4 sentences describing the treatment approach and rationale]

**Control Categories** (for Reduce treatments):
<!-- 
  List applicable control categories (NOT specific implementations)
  
  Available Categories:
  1. Encryption - Data at rest, data in transit, end-to-end
  2. Authentication - User, device, message authentication
  3. Access Control - RBAC, least privilege, permissions
  4. Secure Boot - Verified boot, TEE, attestation
  5. Code Signing - Firmware signing, app signing, package signing
  6. Intrusion Detection - Anomaly detection, logging, monitoring
  7. Network Segmentation - Firewalls, gateways, isolation
  8. Secure Storage - HSM, TPM, secure enclaves
  9. Input Validation - Sanitization, bounds checking, type validation
  10. Update Security - Signed updates, rollback protection, version checks
  11. Physical Security - Tamper detection, secure enclosures, port disabling
  12. Cryptographic Protocols - TLS, IPsec, CAN SecOC
  
  Example:
  - Encryption (data at rest and in transit)
  - Secure Storage (HSM for key management)
  - Access Control (RBAC for location data)
  
  Leave blank for Avoid, Transfer, or Accept treatments
-->

[List of applicable control categories, or "N/A" for non-Reduce treatments]

**Residual AFR** (for Reduce treatments):
<!-- 
  Re-score the AFR after controls are applied
  Show BEFORE and AFTER for each affected factor
  
  Methodology:
  - Review each AFR factor (0-3)
  - Determine which factors become harder for the attacker after controls
  - Re-score those factors downward when controls increase attacker difficulty
  - Factors typically affected:
    * Specialist Expertise: Lower if specialized skills are needed to bypass controls
    * Knowledge of Item: Lower if encryption/obfuscation makes internals harder to understand
    * Equipment: Lower if HSM, TPM, or specialized tools are needed
  
  Format:
  AFR (Before Controls): [0-15] ([Band])
  
  AFR (After Controls): [0-15] ([Band])
  - Elapsed Time: [0-3] ([level]) [CHANGED/UNCHANGED]
  - Specialist Expertise: [0-3] ([level]) [CHANGED/UNCHANGED]
  - Knowledge of Item: [0-3] ([level]) [CHANGED/UNCHANGED]
  - Window of Opportunity: [0-3] ([level]) [CHANGED/UNCHANGED]
  - Equipment: [0-3] ([level]) [CHANGED/UNCHANGED]
  
  Justification:
  - [Explain why each changed factor was re-scored]
  
  Example:
  AFR (Before Controls): 10 (Moderate Feasibility)
  
  AFR (After Controls): 6 (Low Feasibility)
  - Elapsed Time: 1 (1-6 months) [UNCHANGED] - Reconnaissance cadence stays similar
  - Specialist Expertise: 1 (Expert) [CHANGED from 2] - Requires advanced specialist skills to bypass strong encryption
  - Knowledge of Item: 1 (Confidential / limited access) [CHANGED from 2] - Key handling details are no longer public enough for direct abuse
  - Window of Opportunity: 2 (Easy access / extended time) [CHANGED from 3] - Extra control steps reduce the exploitable window
  - Equipment: 1 (Specialized but purchasable) [CHANGED from 2] - Requires protected-key-storage bypass tooling
  
  Justification:
  - Specialist Expertise decreased to 1 (Expert) because bypassing strong encryption and protected key handling requires advanced specialist skills
  - Equipment decreased to 1 (Specialized but purchasable) because protected key storage can require dedicated lab tooling to bypass
  
  Leave blank for Avoid, Transfer, or Accept treatments
-->

[Re-scored AFR with BEFORE/AFTER comparison and justification, or "N/A" for non-Reduce treatments]

**Residual Risk Value** (for Reduce treatments):
<!-- 
  Recalculate Risk Value using Impact × Residual AFR
  
  Format:
  Residual Risk Value: RV [1-5]
  - Calculation: Impact [1-4] × Residual AFR [Band] → RV [1-5]
  
  Example:
  Residual Risk Value: RV 5
  - Calculation: Impact 4 (Critical) × Residual AFR 10 (Moderate Feasibility) → RV 5
  
  Note: Residual risk may remain the same if AFR band doesn't change enough to cross matrix threshold
  
  Leave blank for Avoid (near-zero risk), Transfer, or Accept treatments
-->

Residual Risk Value: RV [1-5]
- Calculation: Impact [1-4] × Residual AFR [Band] → RV [1-5]

**Transfer Details** (for Transfer treatments):
<!-- 
  Document the transfer mechanism
  
  Include:
  - Transfer To: [Supplier | Insurance | OEM | Third Party]
  - Transfer Mechanism: [Contract clause | SLA | Insurance policy | Indemnification]
  - Rationale: Why risk is being transferred
  
  Example:
  Transfer To: Tier 1 Supplier (SecOC provider)
  Transfer Mechanism: Supply contract requires CAN SecOC implementation with liability clause
  Rationale: CAN message authentication is supplier responsibility per contract
  
  Leave blank for Avoid, Reduce, or Accept treatments
-->

[Transfer details, or "N/A" for non-Transfer treatments]

**Acceptance Documentation** (for Accept treatments):
<!-- 
  Formal documentation of risk acceptance decision
  
  Required Fields:
  - Risk Level: RV [1-5]
  - Business Rationale: Why accepting this risk (2-3 sentences)
  - Approval Authority: [Role/Name] who authorized acceptance
  - Review Date: [ISO 8601 date] when risk will be reassessed
  
  Example:
  Risk Level: RV 2
  Business Rationale: USB debugging interface is disabled in production builds and only enabled 
  for engineering development vehicles. Production fleet has debug ports physically removed during 
  manufacturing. Residual risk from engineering vehicles (< 0.01% of fleet) is acceptable.
  Approval Authority: Chief Information Security Officer (CISO)
  Review Date: 2027-03-15 (annual review)
  
  Leave blank for Avoid, Reduce, or Transfer treatments
-->

[Acceptance documentation, or "N/A" for non-Accept treatments]

**Last Updated**: [YYYY-MM-DD]
<!-- ISO 8601 date format -->

---

## Section 2: Completed Example

### RT-IVI-001: Location Tracking Threat - Reduce via Encryption

**Related TS-ID**:
TS-IVI-001 [EXAMPLE] (Unauthorized Location Tracking via GNSS Data Exfiltration)

**Related DS-ID**:
DS-IVI-001 (Unauthorized Driver Location Tracking)

**Impact Score**:
Impact: 4 (Critical)
- Safety: 1 (Negligible) - Location tracking is passive surveillance, no physical harm
- Financial: 3 (Severe) - GDPR fines up to €20M/4% annual revenue, class-action lawsuits
- Operational: 1 (Negligible) - All vehicle functions remain available
- Privacy: 4 (Critical) - Continuous real-time tracking reveals comprehensive movement patterns

**AFR Score**:
AFR: 10 (Moderate Feasibility)
- Elapsed Time: 1 (1-6 months) - Reconnaissance and abuse setup take weeks
- Specialist Expertise: 2 (Proficient) - Requires mobile app development and API knowledge
- Knowledge of Item: 2 (Public with effort) - Backend API behavior learned by reversing client traffic
- Window of Opportunity: 3 (Unlimited) - Cloud API accessible 24/7 from internet
- Equipment: 2 (Standard automotive / test equipment) - Laptop with proxy tool and device lab

**Risk Value**:
Risk Value: RV 5
- Calculation: Impact 4 (Critical) × AFR 10 (Moderate Feasibility) → RV 5 (from Risk Value Matrix)

**Treatment Decision**: Reduce

**Treatment Description**:
Implement strong encryption for all location data at rest and in transit, combined with role-based access control limiting location data access to authorized services only (navigation, emergency services). Deploy protected cryptographic key storage in the backend. This Reduce treatment targets Knowledge of Item (encrypted location data is useless without decryption keys) and Equipment (protected key storage raises the barrier for key extraction).

**Control Categories**:
- Encryption (data at rest and in transit)
- Secure Storage (protected cryptographic key management)
- Access Control (role-based access, principle of least privilege)

**Residual AFR**:
AFR (Before Controls): 10 (Moderate Feasibility)

AFR (After Controls): 6 (Low Feasibility)
- Elapsed Time: 1 (1-6 months) [UNCHANGED] - Reconnaissance cadence stays similar
- Specialist Expertise: 1 (Expert) [CHANGED from 2] - Bypassing strong encryption and protected key handling requires advanced specialist skills beyond a typical app developer
- Knowledge of Item: 1 (Confidential / limited access) [CHANGED from 2] - Useful internals are now protected by key isolation and harder to obtain
- Window of Opportunity: 2 (Easy access / extended time) [CHANGED from 3] - Additional authorization steps narrow the practical exploit window
- Equipment: 1 (Specialized but purchasable) [CHANGED from 2] - Extracting keys from protected storage requires dedicated lab equipment

Justification:
- **Specialist Expertise** decreased to 1 (Expert): Encrypted location data now requires advanced specialist skills to bypass protected storage and encryption barriers. Standard app developers can no longer trivially read location values from intercepted API responses.
- **Equipment** decreased to 1 (Specialized but purchasable): Protected key storage raises the barrier beyond a standard laptop-and-proxy setup and can require dedicated lab tooling.

**Residual Risk Value**:
Residual Risk Value: RV 4
- Calculation: Impact 4 (Critical) × Residual AFR 6 (Low Feasibility) → RV 4

**Transfer Details**: N/A

**Acceptance Documentation**: N/A

**Last Updated**: 2026-03-20

---

## Quick Checklist

Before finalizing your risk treatment entry, verify:

- [ ] RT-ID matches corresponding TS-ID number (RT-IVI-001 ↔ TS-IVI-001)
- [ ] Related TS-ID references a valid threat scenario from ts.md (or marked [EXAMPLE])
- [ ] Related DS-ID references a valid damage scenario from ds.md
- [ ] Impact Score copied from DS-ID entry with SFOP breakdown
- [ ] AFR Score copied from TS-ID entry with 5-factor breakdown
- [ ] Risk Value calculated correctly using Impact × AFR matrix
- [ ] Treatment Decision is one of: Avoid | Reduce | Transfer | Accept
- [ ] Treatment Description explains what, how, and why (2-4 sentences)
- [ ] Control Categories listed if treatment is Reduce
- [ ] Residual AFR re-scored with BEFORE/AFTER and justification if treatment is Reduce
- [ ] Residual Risk Value recalculated if treatment is Reduce
- [ ] Transfer Details documented if treatment is Transfer
- [ ] Acceptance Documentation completed if treatment is Accept
- [ ] Last Updated date is current (ISO 8601 format YYYY-MM-DD)

For more details, see:
- `references/rt-schema.md` - Field definitions and validation rules
- `references/rt-guide.md` - Risk Value matrix and treatment decision methodology
- `references/examples/` - Additional worked examples for IVI and CAN domains
