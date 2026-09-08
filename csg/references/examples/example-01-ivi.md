# Cybersecurity Goal Example 01 - IVI Domain (Accept Treatment, No New CSG)

This example demonstrates the policy-A boundary for an **Accept** risk treatment decision: no new CSG is created, and the formal cybersecurity claim remains in `data/rt.md`.

---

## No New CSG Entry for RT-IVI-002

**Decision**: Do not create a new CSG entry

**Reason**: `Accept` retains residual risk rather than defining a new active security objective

**Related DS-IDs**:
- DS-IVI-002 [EXAMPLE] (User Personal Data Exposure)

**Authoritative RT Entry**: RT-IVI-002 [EXAMPLE] (Treatment Decision = Accept)

**Why No CSG Is Created**:
The project is not defining a new active mitigation objective here. It is retaining residual privacy risk with formal approval, so the decision belongs in `data/rt.md` rather than `data/csg.md`.

**What Happens Instead**:
- Keep the claim, approval authority, review date, and justification in RT-IVI-002
- Do not add a `CSG-IVI-02` entry solely to mirror the claim
- If the treatment later changes to `Reduce`, create a new CSG at that time

**Traceability Note**:
DS-IVI-002 [EXAMPLE] is still covered by the risk-treatment workflow and does not become an orphan simply because it has no new CSG entry.

---

## RT-Owned Cybersecurity Claim Documentation (Accept Treatment)

This section shows the material that belongs in `data/rt.md`, not in a new CSG entry.

### Claim Element 1: Risk Statement

**Risk**: DS-IVI-002 [EXAMPLE] "User Personal Data Exposure" with Risk Value 3 (Impact 3, AFR Medium)

**Risk Details**:
- **Attack Vector**: Malicious Android application with privilege escalation accessing persistent storage
- **Affected Data**: User contacts, call history, SMS messages, paired device identifiers, WiFi network credentials
- **Scale**: Affects 1,000-10,000 users per data breach incident
- **Financial Impact**: €20M GDPR fines (or 4% annual revenue), ¥50M GB 44495 fines (or 5% turnover), $50M-$100M class-action settlement risk
- **Privacy Impact**: Severe (Privacy = 3) — Personal relationship data, communication patterns, network access information exposed
- **Safety/Operational Impact**: Negligible — Vehicle functions normally during breach, no impact on safety-critical systems

### Claim Element 2: Justification (Business Rationale)

**Justification Category**: Business/Cost-Benefit Analysis

**Technical Analysis**:
Full cryptographic protection of user personal data would require:
- Encryption controls for data at rest and in transit
- Secure key derivation and protection mechanisms
- Hardware-backed key storage capabilities
- Implementation cost per vehicle: $120-180 (hardware integration, firmware development, integration testing)
- Development timeline impact: 8-12 months for hardware integration and validation

**Cost-Benefit Analysis**:
- **Annual units affected**: 150,000 vehicles/year
- **Mitigation cost**: $18M-27M per model year (150,000 × $120-180)
- **Expected loss from DS-IVI-002 [EXAMPLE]**: Impact 3 (Severe) × AFR Medium (8) = RV 3
  - Probability of exploitation: Estimated 5-10% of fleet over 5-year lifecycle
  - Financial exposure: 150,000 × 0.075 (mid-range 5-10%) × ($50M class-action average + $15M regulatory fine) = $562.5M
  - However, actual incident frequency empirically lower (0.5-2% of automotive fleet experiences significant data breach)
  - Realistic expected loss: 150,000 × 0.01 × $65M = $97.5M per model year

**Decision Rationale**:
Given the extreme cost ($18M-27M mitigation cost annually) versus realistic expected loss ($97.5M with 1% incident probability), the cost-benefit ratio appears unfavorable. However, the organization acknowledges this calculation contains significant uncertainty due to unpredictable breach probability. The **primary business rationale** for accepting risk is:

1. **Market Timeline Pressure**: Next-generation connectivity module (featuring integrated security capabilities and hardware crypto acceleration) is scheduled for Q4 2026. Retrofitting current-generation BCM43455 module would delay model year launch by 2 quarters, causing estimated market share loss of 8-12% to competitors (financial impact: $150M-200M revenue loss).

2. **Data Classification Strategy**: The organization has adopted a data classification policy distinguishing between **critical** and **non-critical** personal data:
   - **Critical**: Payment card data, biometric data, location history → Mandatory encryption (Reduce treatment)
   - **Non-Critical**: Contact list, call history, paired device IDs → Risk accepted due to low exploitation utility (users typically don't enable Android app permissions for contacts/call history access without explicit consent)

3. **Mitigating Controls Already in Place**:
   - Android runtime permission model requires explicit user consent per data category (granular permission grants)
   - SELinux mandatory access control (MAC) enforced by Android Security Module isolates apps from other apps' data (process-level sandbox)
   - Secure boot validates bootloader and kernel integrity (prevents bootkit persistence)
   - Anti-rollback protection on firmware prevents downgrade to vulnerable versions
   
   These compensating controls reduce actual attack feasibility below calculated AFR Medium (8) rating.

4. **User Notification and Control**:
   - In-vehicle privacy control dashboard allows users to selectively disable app permissions for sensitive data categories
   - Privacy policy clearly discloses that user data is stored unencrypted (informed consent)
   - Users can factory reset head unit to wipe all personal data

**Conclusion**: Market timing constraint (launch delay risk of $150M-200M) and compensating controls justify accepting residual privacy risk of DS-IVI-002 [EXAMPLE] for current-generation head unit. Next-generation vehicle (model year 2027) will implement mandatory encryption as part of architecture upgrade.

### Claim Element 3: Residual Risk Acknowledgment

**Explicit Acceptance Statement**:

Acme Automotive Inc. accepts the residual risk of DS-IVI-002 [EXAMPLE] "User Personal Data Exposure" and acknowledges the potential impact of:
- **Financial Impact**: Regulatory fines under GDPR (up to €20M or 4% annual revenue) and GB 44495 (up to ¥50M or 5% turnover), plus class-action litigation costs ($50M-$100M settlement estimate)
- **Privacy Impact**: Exposure of personal data (contacts, call history, paired devices, WiFi credentials) affecting 1,000-10,000 users per breach incident
- **Reputational Impact**: Brand reputation damage from privacy data breach potentially reducing future vehicle market share

**Approval Authority**: 
This cybersecurity claim has been reviewed and approved by:
- **Approver Name**: Jane Chen, Chief Information Security Officer (CISO)
- **Approval Date**: 2026-03-15
- **Approval Authority Level**: Executive-level approval (Risk Value 3 = Cybersecurity Manager or equivalent with CISO notification; this claim received CISO signature as escalated business decision)
- **Claim Validity Period**: 12 months
- **Next Review Date**: 2027-03-15

**Monitoring and Re-evaluation Requirements**:
- Annual reassessment of threat landscape (new exploit techniques, real-world incident data)
- Quarterly review of Android security bulletins for vulnerabilities affecting SELinux sandbox or permission model
- Incident monitoring: If ANY data breach incident occurs at Acme Automotive involving user personal data, claim validity is suspended and emergency risk mitigation review is mandatory
- Cryptographic control retrofit will proceed per planned timeline (Q4 2026 integration with next-generation module)

**Evidence Supporting Claim**:
- `Annex A`: Cost-benefit analysis spreadsheet (150,000 units, $120-180/unit mitigation cost, 1% incident probability)
- `Annex B`: Android security architecture review (SELinux MAC effectiveness, permission model evaluation)
- `Annex C`: Next-generation module procurement contract (Q4 2026 security integration confirmed)
- `Annex D`: Privacy policy update disclosing unencrypted storage of personal data (informed user consent)
- `Annex E`: Cybersecurity insurance policy (#AUTO-2026-0315) covering data breach liability up to $100M

---

## Key Takeaways from This Example

### 1. Accept Treatment Does Not Create a New CSG

Under policy A:
- `Accept` keeps the claim in `data/rt.md`
- `csg.md` is reserved for active goals only
- If the team later introduces mitigation, that change creates a new CSG

### 2. Accept Treatment Is Rare for Privacy Data

Privacy data breaches (DS-IVI-002 [EXAMPLE]) affecting thousands of users typically trigger **Reduce** treatment under GDPR and GB 44495 regulations. **Accept** treatment is only viable when:
- Impact Score is 2 (Low) or 3 (Moderate) with special business justification, NOT 4 (Critical)
- Compensating controls already exist (not explicitly documented as failing)
- Timeline/market pressures create genuine cost-benefit dilemma
- Executive-level approval obtained
- Insurance or contractual risk transfer documented
- Clear plan for future mitigation (e.g., next-generation architecture)

### 3. Residual Risk Acknowledgment Requires Three Components

Every **Accept** claim MUST include:
1. **Risk Statement**: Clear description of DS-ID, RV, Impact dimensions, and exploitation scenario
2. **Justification**: Technical/business/legal rationale explaining WHY acceptance is necessary
3. **Residual Risk Acknowledgment**: Explicit statement that organization accepts consequences, with approver signature and review period

Without any of these three components, the claim is incomplete and unenforceable under ISO 21434.

### 4. Data Classification Strategy Guides Accept Decisions

This example demonstrates use of **data sensitivity classification**:
- **Critical Data** (payment cards, biometrics, location history) → Mandatory Reduce treatment regardless of cost
- **Non-Critical Data** (call history, contacts, device IDs) → May justify Accept treatment if proper context exists

This classification approach allows organizations to accept risk for low-sensitivity data while maintaining strong protection for high-sensitivity data.

### 5. Compensating Controls Reduce Actual Risk Below Calculated RV

Even though DS-IVI-002 [EXAMPLE] calculates to RV 3 (Severe) before controls, existing compensating controls already present in Android reduce actual risk:
- **SELinux MAC**: Prevents cross-app data access even if one app is compromised
- **Android Permission Model**: Granular consent prevents silent data exfiltration
- **Secure Boot**: Prevents bootkit persistence
- **Anti-rollback**: Prevents downgrade to vulnerable firmware

These controls shift the risk from theoretical RV 3 to more realistic RV 2-3 range, supporting Accept claim.

### 6. Market Timing Can Justify Short-Term Risk Acceptance

Deferring cryptographic protection to next-generation vehicle (Q4 2026) is only acceptable when:
- Migration plan is **concrete and time-bound** (not vague "future enhancement")
- Cost of early implementation ($150M-200M market delay) exceeds mitigation benefit
- Timeline is realistic given engineering constraints
- Business leadership explicitly approved the timeline trade-off

### 7. Cybersecurity Claim Requires Insurance or Transfer Mechanism

**Accept** claims for high-impact privacy data should include:
- Cyber liability insurance policy covering data breach (up to $100M in this example)
- Contractual liability transfer to vendors if applicable
- Clear recovery plan and incident response procedures

Without insurance or transfer mechanism, Accept treatment creates uninsurable financial risk.

### 8. CIA Property Alignment Still Matters Even Without a New CSG

DS-IVI-002 [EXAMPLE] affects Privacy dimension (P=3, Severe):
- SFOP → CIA mapping: Privacy (P) → Confidentiality (C)
- If treatment later changes to active mitigation, the resulting CSG should use **Confidentiality** ✅
- The Accept claim still documents why confidentiality protection was deferred ✅

This example demonstrates proper CIA property alignment with damage scenario dimensions.

---

## Alternative Considerations (Not Selected)

### Why Not Reduce Treatment?

**Full Encryption Implementation**:
- **Cost**: $120-180 per vehicle × 150,000 units = $18M-27M annually
- **Timeline Impact**: 8-12 month development cycle delays model year launch by 2 quarters
- **Market Loss**: Estimated 8-12% market share loss to competitors = $150M-200M revenue loss
- **Decision**: Cost of early implementation (market delay) outweighs expected loss ($97.5M with 1% incident probability)

**Partial Encryption** (encryption without hardware-backed key storage):
- **Cost**: $40-60 per vehicle (reduced hardware cost)
- **Timeline Impact**: 3-4 months development cycle (longer than Accept, shorter than full encryption)
- **Security Weakness**: Keys stored in standard memory (subject to side-channel extraction attacks), not resistant against determined adversary
- **Decision**: Partial encryption insufficient for regulatory compliance; insufficient improvement to justify timeline delay

### Why Not Avoid Treatment?

**Remove Android App Ecosystem**:
- Eliminates all app-level vulnerabilities by removing apps entirely
- **Business Impact**: Destruction of entire infotainment value proposition (navigation, music streaming, messaging apps)
- **Market Viability**: Customers demand third-party app support; removing apps would make vehicle non-competitive
- **Decision**: Avoid treatment commercially unviable

### Why Not Transfer Treatment?

**Transfer to Google (Android Provider)**:
- Android OS provider could implement system-level protection (better isolation, enhanced SELinux)
- **Reality**: OEM (Acme) remains liable under GDPR as the data controller
- **Liability**: Even if Google breaches Android security, Acme is liable to users for GDPR violations
- **Decision**: Transfer would not eliminate regulatory liability; not viable option

**Transfer to Cyber Insurance Provider**:
- Insurance covers financial loss (fines, settlements) if breach occurs
- **Reality**: Insurance covers consequences, not prevention; doesn't satisfy regulatory "appropriate measures" requirement
- **Compliance Gap**: GDPR Article 32 requires "appropriate technical and organizational measures" — insurance is financial transfer only, not technical control
- **Decision**: Insurance complements Accept claim (provides financial protection) but doesn't satisfy compliance requirements independently

### Why Confidentiality (Not Integrity or Availability)?

**Why Not Integrity**?
- DS-IVI-002 [EXAMPLE] addresses **unauthorized disclosure**, not data tampering
- Integrity goal would be: "Prevent unauthorized modification of personal data"
- This does NOT address the primary damage (unauthorized access/exfiltration)
- Privacy harm comes from **disclosure**, not modification

**Why Not Availability**?
- DS-IVI-002 [EXAMPLE] affects service continuity NOT at all (vehicle continues functioning during breach)
- Availability goal would be: "Ensure personal data system remains accessible to authorized users"
- This does NOT address the primary damage (confidentiality violation)
- Privacy harm comes from **disclosure to unauthorized parties**, not unavailability

**Why Confidentiality**?
- DS-IVI-002 [EXAMPLE] primary damage: Unauthorized access to personal data (Privacy dimension, P=3)
- Confidentiality goal: "Ensure personal data accessible only to authorized components"
- Privacy harm prevented by restricting access (confidentiality control)
- ✅ Correct CIA property for this damage scenario

---

## Cross-References

- **Related Damage Scenario**: `data/ds.md` → DS-IVI-002 [EXAMPLE] (User Personal Data Exposure)
- **Related Risk Treatment**: `data/rt.md` → RT-IVI-002 [EXAMPLE] (Treatment Decision - Accept)
- **CSG Schema Definition**: `../csg-schema.md` → claims remain empty in `data/csg.md`
- **CSG Derivation Methodology**: `../csg-guide.md` → Accept claims stay in `data/rt.md`
- **ISO 21434 References**: Clause 8.5 (Cybersecurity claims), Clause 15.9 (CSG formulation)
- **Regulatory References**: GDPR Article 32 (appropriate measures), GB 44495 (personal information protection)

---

## Relationship to CSG Skill Examples

This example demonstrates the **Accept treatment** pattern, contrasting with:
- **Reduce Treatment Pattern**: CSG with active mitigation controls
- **Transfer + Mitigation Pattern**: CSG linked to RT claim
- **Avoid Treatment Pattern**: CSG documenting feature elimination or redesign

Each treatment type produces different artifact structure and approval requirements. In this skill package, only active-mitigation treatments create new CSG entries.

---

## Last Updated

2026-03-20 — Initial example creation demonstrating Accept treatment with RT-owned claim documentation and no new CSG entry.

---

*End of RT-IVI-002 Accept Treatment Example*
