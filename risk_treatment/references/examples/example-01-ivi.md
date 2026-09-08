# Risk Treatment Example 01 - IVI Domain

This example demonstrates risk treatment for a privacy-focused IVI threat scenario.

---

## RT-IVI-002: User Personal Data Exposure - Reduce via Encryption & Access Control

**Related TS-ID**:
TS-IVI-002 [EXAMPLE] (Malicious Android App Exfiltrating User Contacts via Permissions Abuse)

**Related DS-ID**:
DS-IVI-002 (User Personal Data Exposure)

**Impact Score**:
Impact: 3 (Severe)
- Safety: 1 (Negligible) - Data exposure does not directly cause physical harm
- Financial: 3 (Severe) - Regulatory fines (GDPR €20M or 4% revenue, GB 44495 ¥50M or 5% turnover), class-action lawsuits ($50M-$100M)
- Operational: 1 (Negligible) - Vehicle functions normally during data breach
- Privacy: 3 (Severe) - Exposure of contacts, call history, paired devices, WiFi credentials affecting 1,000-10,000 users

**AFR Score**:
AFR: 8 (Low Feasibility)
- Elapsed Time: 1 (1-6 months) - Malicious app development, review evasion, and staging take weeks
- Specialist Expertise: 2 (Proficient) - Android app development and reverse engineering skills (Frida, apktool)
- Knowledge of Item: 1 (Confidential / limited access) - Infotainment file layout and permission edges require substantial reverse engineering
- Window of Opportunity: 3 (Unlimited) - App store and persistent local storage remain broadly reachable
- Equipment: 1 (Specialized but purchasable) - Standard laptop plus Android reversing lab

**Risk Value**:
Risk Value: RV 3
- Calculation: Impact 3 (Severe) × AFR 8 (Low Feasibility) → RV 3 (from Risk Value Matrix)

**Treatment Decision**: Reduce

**Treatment Description**:
Implement strong data protection controls including application sandboxing with mandatory access control (MAC) enforced by the Android Security Module (SELinux), end-to-end encryption (AES-256-GCM) for all user personal data at rest in persistent storage, and granular runtime permission model requiring explicit user consent for each data category (contacts, call history, location). Deploy Trusted Execution Environment (TEE) using ARM TrustZone for secure cryptographic key storage and management. This Reduce treatment targets Knowledge of Item (encrypted data is unreadable without keys stored in TEE) and Equipment (TEE key extraction requires specialized hardware fault injection tools).

**Control Categories**:
- Encryption (data at rest with AES-256-GCM, keys managed in TEE)
- Access Control (SELinux mandatory access control, Android runtime permissions with explicit consent)
- Secure Storage (ARM TrustZone TEE for cryptographic key protection)
- Application Sandboxing (process isolation, file system permissions, principle of least privilege)

**Residual AFR**:
AFR (Before Controls): 8 (Low Feasibility)

AFR (After Controls): 5 (Low Feasibility)
- Elapsed Time: 1 (1-6 months) [UNCHANGED] - App review evasion still takes time
- Specialist Expertise: 1 (Expert) [CHANGED from 2] - Bypassing AES-256-GCM and TEE protections requires low-level hardware/firmware expertise
- Knowledge of Item: 0 (Restricted / classified) [CHANGED from 1] - Useful key handling details are isolated in TEE and no longer obtainable from normal reversing alone
- Window of Opportunity: 2 (Easy access / extended time) [CHANGED from 3] - Additional authorization and key-release checks reduce the exploitable window
- Equipment: 1 (Specialized but purchasable) [UNCHANGED from 1] - Dedicated fault-injection tooling is now required, but remains purchasable to a determined lab attacker

Justification:
- **Specialist Expertise** decreased to 1 (Expert): Encrypted user data now requires cryptanalysis or TEE exploitation. Standard Android app developers can no longer read plaintext contacts directly from the file system.
- **Knowledge of Item** decreased to 0 (Restricted / classified): TEE-isolated key handling and storage details are no longer recoverable from routine reverse engineering alone.
- **Window of Opportunity** decreased to 2: Additional authorization and key-release checks reduce the practical exploit window even though the app ecosystem remains reachable.

**Residual Risk Value**:
Residual Risk Value: RV 3
- Calculation: Impact 3 (Severe) × Residual AFR 5 (Low Feasibility) → RV 3

**Transfer Details**: N/A

**Acceptance Documentation**: N/A

**Last Updated**: 2026-03-20

---

## Key Takeaways from This Example

### 1. Privacy Data Requires Strong Protection
Even though Impact is 3 (Severe) rather than 4 (Critical), privacy violations affecting thousands of users usually justify robust Reduce treatment. For RV 3 privacy risks, Reduce or Transfer is usually easier to justify than straight Accept unless the organization can demonstrate appropriate measures, explicit rationale, and approval.

### 2. Encryption Alone Is Not Sufficient
This example demonstrates defense-in-depth:
- **Encryption** protects data confidentiality (AES-256-GCM)
- **Secure Storage** protects encryption keys (TEE/TrustZone)
- **Access Control** limits data access even before encryption (SELinux MAC, runtime permissions)
- **Application Sandboxing** isolates malicious apps from user data

### 3. Residual Risk May Remain Elevated
Despite comprehensive controls, Residual Risk Value only dropped from RV 3 → RV 3 in this example because the matrix still places Impact 3 × AFR Low Feasibility in the same RV band. This demonstrates that risk treatment does not always reduce the matrix number as much as the attacker difficulty improves.

### 4. Control Categories vs. Specific Implementations
This treatment documents **control categories** (Encryption, Access Control, Secure Storage) first, with implementation examples only used illustratively. The actual implementation details (which cryptographic library, which SELinux policies) belong in Cybersecurity Requirements (CSR), not risk treatment decisions.

### 5. Affected AFR Factors
Reduce treatments typically impact these factors:
- **Specialist Expertise**: Encryption and TEE lower the factor by raising skill requirements
- **Knowledge of Item**: Encrypted formats and proprietary key schemes lower the factor by increasing reverse engineering difficulty
- **Equipment**: TEE and HSM lower the factor by requiring specialized hardware tools

Reduce treatments rarely affect:
- **Window of Opportunity**: Attack surface timing often stays similar
- **Elapsed Time**: Initial attack staging may stay similar even if later exploitation becomes harder

### 6. Regulatory Compliance Drives Treatment Decisions
For privacy data (GDPR, GB 44495), **Accept** treatment for RV 3 usually needs explicit justification and approval. Reduce treatment with strong encryption and access control is a common baseline. Transfer treatment might apply if third-party cloud providers handle the data with contractual data processing agreements (DPAs).

---

## Cross-References

- **Related Damage Scenario**: `data/ds.md` → DS-IVI-002 (User Personal Data Exposure)
- **Related Threat Scenario**: TS-IVI-002 [EXAMPLE] (malicious app attack vector)
- **Schema Definition**: `../rt-schema.md` → 14-field structure for RT entries
- **Risk Value Matrix**: `../rt-guide.md` → Impact × AFR calculation methodology
- **Treatment Methodology**: `../rt-guide.md` → When to use Avoid/Reduce/Transfer/Accept

---

## Alternative Treatment Considerations (Not Selected)

### Why Not Avoid?
**Avoid** treatment would require removing the Android app ecosystem entirely, eliminating user-facing apps and external connectivity. This would severely degrade product functionality and user experience. The infotainment system's core value proposition includes third-party app support (navigation, music streaming, messaging), making Avoid treatment commercially unviable.

### Why Not Transfer?
**Transfer** treatment could shift some responsibility to Google (Android OS provider) or app store operators (for malware screening), but the OEM remains ultimately liable under GDPR as the data controller. User personal data stored in the vehicle is the OEM's responsibility regardless of third-party involvement. Transfer would not eliminate regulatory liability.

### Why Not Accept?
**Accept** treatment for RV 3 privacy risks under GDPR and GB 44495 requires explicit justification, approval, and evidence that appropriate technical and organizational measures were considered. Consciously accepting RV 3 privacy risk without mitigation is likely to draw regulatory scrutiny. Accept is more realistic for RV 1-2 privacy risks or with exceptional business justification and executive-level approval.

**Conclusion**: Reduce is the only viable treatment option for this scenario.
