# Cybersecurity Goal Template

Use this template to document Cybersecurity Goals (CSGs) for each set of related damage scenarios. Copy this structure and fill in all 9 required fields per `references/csg-schema.md`.

---

## Section 1: Blank Template

### CSG-[DOMAIN]-[NN]: [Cybersecurity Goal Title]
<!-- 
  CSG-ID Format: CSG-[DOMAIN]-[NN]
  Domain codes: CAN | OTA | EXT | BCK | IVI | IMM | ADAS
  Number: 2-digit zero-padded (01, 02, ..., 99)
  
  CSG-ID Numbering: NOT tied to TS/RT/DS numbering
  Examples:
  - CSG-IVI-01 (first infotainment CSG)
  - CSG-CAN-03 (third CAN CSG)
  - CSG-ADAS-12 (twelfth ADAS CSG)
  
  Title Guidelines:
  - Max 80 characters
  - Include the security property or protected asset
  - Example: "Location Data Confidentiality"
  - Example: "CAN Message Authentication and Integrity"
-->

**Related DS-IDs**:
<!-- 
  Damage Scenario IDs from DS catalogue (data/ds.md)
  Format: DS-[DOMAIN]-[NNN] (Damage Scenario Title)
  
  Rules:
  - List one per line with hyphen prefix
  - Include the damage scenario title for clarity
  - One CSG may address 1-5 damage scenarios (M:N mapping)
  - Multiple CSGs may address the same DS-ID
  
   Examples:
   - DS-IVI-001 [EXAMPLE] (Unauthorized Driver Location Tracking)
   - DS-IVI-002 [EXAMPLE] (Personal Information Exposure)
   - DS-BCK-001 [EXAMPLE] (Telematics Backend Data Breach)
-->

- [DS-[DOMAIN]-[NNN] (Damage Scenario Title)]
- [DS-[DOMAIN]-[NNN] (Damage Scenario Title)]

**Related RT-IDs**:
<!-- 
  Risk Treatment IDs from RT catalogue (data/rt.md)
  Format: RT-[DOMAIN]-[NNN] (Risk Treatment Title)
  
  Rules:
  - List one per line with hyphen prefix
  - Include the risk treatment title
  - Optional field - may be empty during initial CSG formulation
  - Do not use this field to represent pure Accept / pure Transfer claims
  - Pure Accept / pure Transfer claims stay in data/rt.md and do not create a new CSG entry
  - Typically added after risk treatment decisions are made
  
   Examples:
   - RT-IVI-001 [EXAMPLE] (Location Tracking Threat - Reduce via Encryption)
   - RT-IVI-002 [EXAMPLE] (PII Exposure - Reduce via Access Controls)
   - RT-BCK-001 [EXAMPLE] (Backend API Bypass - Reduce via Authentication)
-->

- [RT-[DOMAIN]-[NNN] (Risk Treatment Title)]

**Goal Viewpoint** (optional): [OEM vehicle-level | Tier 1/component-level]

**Parent Vehicle-Level Goal** (required for component-level goals): [CSG-ID | N/A for vehicle-level goal]

**Goal Statement**:
<!-- 
  1-3 sentences expressing the cybersecurity objective as a shall-statement
  
  Requirements:
  - Use "shall" language (implementation-independent, normative)
  - Express the security property to be achieved, not the mechanism
  - Be specific enough to be verifiable/testable
  - Avoid mentioning specific technologies (AES, TLS, etc.)
  - First sentence: What shall be protected
  - Second sentence: What threats shall be prevented
  
  Template:
  "The [system/component] shall ensure that [security property]. 
   The system shall prevent/detect [threat action] that could [damage consequence]."
  
  Example:
  "The vehicle system shall ensure that real-time location data and historical 
  travel patterns are accessible only to authorized users and services. The system 
  shall prevent unauthorized exfiltration, storage, or sharing of location 
  information that could enable driver surveillance or movement tracking."
-->

[1-3 sentences describing what shall be protected and what threats shall be prevented]

**CIA Property**:
<!-- 
  Exactly one of: Confidentiality | Integrity | Availability
  
  Definitions:
  - Confidentiality: Information accessible only to authorized entities
  - Integrity: Information and systems are accurate and cannot be modified without authorization
  - Availability: Information and systems are accessible when needed by authorized entities
  
  Rules:
  - Select exactly one (required)
  - If multiple properties matter, create multiple CSG entries
  - Do not use primary/secondary notation inside one CSG
  
  Typical Patterns:
  - IVI/BCK domains → Often Confidentiality (data protection)
  - CAN/ADAS domains → Often Integrity (control message authentication)
  - IMM/ADAS domains → Often Availability (safety-critical functions)
  
  Examples:
  - Confidentiality
  - Integrity
  - Integrity
-->

[Confidentiality | Integrity | Availability]

**Cybersecurity Claim**:
<!-- 
  Leave empty in CSG entries
  
  Rules:
  - Leave EMPTY for all CSG entries
  - Accept / Transfer justification and approvals belong in data/rt.md
  - If a Transfer RT entry includes active mitigation, link the RT-ID here but keep the claim in data/rt.md
  
  When to populate:
  - Empty: CSG covers active security objectives only
  
  Examples:
  - (empty)
-->

[leave empty - claims are documented in data/rt.md]

**Rationale**:
<!-- 
  2-4 sentences explaining why this Cybersecurity Goal is necessary
  
  Requirements:
  - Length: 2-4 sentences (typically 3 sentences)
  - First sentence: What damage scenarios motivate this goal
  - Second sentence: Regulatory or standards context (if applicable)
  - Third sentence: How this goal prevents the damage
  - Reference specific DS-IDs to establish traceability
  - Cite relevant regulations: UN R155, ISO 21434, GDPR, GB 44495, etc.
  - Keep total length under 600 characters
  
  Template:
  "[Threat/damage description and consequence] ([DS-IDs]). 
   [Regulatory/standards requirement if applicable]. 
   This goal ensures [security property] to prevent [damage type]."
  
  Regulatory References:
  - UN R155: Vehicle cybersecurity type approval (EU)
  - ISO/SAE 21434: Automotive cybersecurity engineering
  - GDPR: Privacy and personal data protection (EU)
  - GB 44495: Automotive data security (China)
  - ISO 26262: Functional safety interactions
-->

[2-4 sentences connecting the goal to damage scenarios, regulatory context, and prevention approach]

**Last Updated**: [YYYY-MM-DD]
<!-- ISO 8601 date format -->

---

## Section 2: Completed Example

### CSG-IVI-01: Location Data Confidentiality

**Related DS-IDs**:
- DS-IVI-001 [EXAMPLE] (Unauthorized Driver Location Tracking)
- DS-IVI-002 [EXAMPLE] (Personal Information Exposure)

**Related RT-IDs**:
- RT-IVI-001 [EXAMPLE] (Location Tracking Threat - Reduce via Encryption)
- RT-IVI-002 [EXAMPLE] (PII Exposure - Reduce via Access Controls)

**Goal Viewpoint**: OEM vehicle-level

**Parent Vehicle-Level Goal**: N/A

**Goal Statement**:
The vehicle system shall ensure that real-time location data, historical travel patterns, and personal device information are accessible only to authorized users and services. The system shall prevent unauthorized exfiltration, storage, or sharing of location and personal data that could enable driver surveillance, stalking, identity theft, or comprehensive movement tracking.

**CIA Property**: Confidentiality

**Cybersecurity Claim**:

**Rationale**:
Unauthorized access to real-time vehicle location data and personal information stored on the infotainment system enables continuous driver surveillance, stalking, and privacy violations affecting thousands of users (DS-IVI-001 [EXAMPLE], DS-IVI-002 [EXAMPLE]). Location tracking and PII exposure violate GDPR Article 6 (lawful basis for processing personal data) and China GB 44495 (personal information protection requirements). This goal ensures location and PII confidentiality to prevent privacy harms documented in related damage scenarios and meet regulatory requirements for data protection.

**Last Updated**: 2026-03-20

---

## M:N Mapping Explanation

This example demonstrates **M:N (many-to-many) mapping**: One CSG addressing multiple DS-IDs:

```
CSG-IVI-01: Location Data Confidentiality
  ├─ DS-IVI-001 [EXAMPLE] (Unauthorized Driver Location Tracking)
  │   - Impact: 4 (Critical) - Privacy dimension
  │   - Root Cause: Location data accessible to attacker
  │
  └─ DS-IVI-002 [EXAMPLE] (Personal Information Exposure)
      - Impact: 3 (Severe) - Privacy dimension
      - Root Cause: PII accessible to attacker
```

**Why one CSG addresses both DS-IDs**:
- Both damage scenarios involve confidentiality breaches of sensitive personal data
- Both violate the same regulations (GDPR, GB 44495)
- Both are prevented by the same security property (data confidentiality)
- Both require similar protective controls (encryption, access control, authentication)

**How M:N works with Risk Treatment**:
- One CSG (CSG-IVI-01) derives from multiple damage scenarios (DS-IVI-001 [EXAMPLE], DS-IVI-002 [EXAMPLE])
- Multiple Risk Treatments (RT-IVI-001 [EXAMPLE], RT-IVI-002 [EXAMPLE]) implement this single CSG
- Each RT may address a different attack vector or layer of defense
- All RTs contribute to achieving the same CSG security objective

---

## Quick Checklist

Before finalizing your Cybersecurity Goal entry, verify:

- [ ] CSG-ID follows format `CSG-[DOMAIN]-[NN]` with valid 2-digit number (01-99)
- [ ] Title is ≤80 characters and describes the security property/protected asset
- [ ] Goal Viewpoint is explicit
- [ ] Component-level goals identify a Parent Vehicle-Level Goal
- [ ] Related DS-IDs reference valid damage scenarios from data/ds.md (or marked [EXAMPLE])
- [ ] At least 1 Related DS-ID is listed (no orphan CSGs)
- [ ] Related RT-IDs reference valid risk treatments from data/rt.md (or marked [EXAMPLE] if TBD)
- [ ] Goal Statement is 1-3 sentences with "shall" language and implementation-independent
- [ ] Goal Statement is testable and describes "what" not "how"
- [ ] CIA Property is exactly one of: Confidentiality, Integrity, Availability
- [ ] CIA Property aligns with damage scenario SFOP dimensions
- [ ] Cybersecurity Claim field is empty and any Accept/Transfer claim stays in data/rt.md
- [ ] Rationale is 2-4 sentences and references at least one Related DS-ID
- [ ] Rationale explains why the CSG is necessary (damage prevention)
- [ ] Rationale cites relevant regulations if applicable (UN R155, ISO 21434, GDPR, GB 44495)
- [ ] Last Updated date is current (ISO 8601 format YYYY-MM-DD)
- [ ] If CSG addresses multiple DS-IDs, Rationale explains the commonality

For more details, see:
- `references/csg-schema.md` - Field definitions and M:N mapping rules
- `references/csg-guide.md` - Cybersecurity Goal derivation methodology
- `references/examples/` - Additional worked examples for CAN, OTA, ADAS domains
