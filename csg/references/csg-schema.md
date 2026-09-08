# Cybersecurity Goal Schema - ISO 21434 TARA

This document defines the required fields for Cybersecurity Goal (CSG) documentation in ISO 21434 TARA (Threat Analysis and Risk Assessment) workflows, using Clause 9 concept-phase intent and Clause 15.9 TARA workflow context.

---

## Overview

Cybersecurity Goals (CSGs) represent high-level security objectives derived from damage scenarios. They define what must be protected and form the bridge between risk assessment (damage scenarios) and implementation (cybersecurity requirements).

**Key Characteristics**:
- CSGs are formulated as **shall-statements** expressing security properties
- Each CSG addresses one or more damage scenarios (M:N relationship)
- CSGs focus on **what** must be protected, not **how** to protect it
- Each CSG carries exactly one CIA property (Confidentiality, Integrity, or Availability)
- CSGs are technology-agnostic and implementation-independent

**Relationship to Other TARA Entities**:
```
Damage Scenarios (DS) → Cybersecurity Goals (CSG) → Cybersecurity Requirements (CSR)
       |                         |                              |
    What harm?            What must be protected?        How to protect?
```

---

## Required Fields

Every Cybersecurity Goal entry in the CSG catalogue must include ALL 9 required fields:

### 1. CSG-ID

**Format**: `CSG-[DOMAIN]-[NN]`

**Description**: Unique identifier for the Cybersecurity Goal following a structured naming convention based on the affected vehicle domain. CSG-IDs use 2-digit numbers (not 3-digit like TS/RT/DS) because CSGs are higher-level abstractions with fewer entries per domain.

**Domain Codes**:
- `CAN` - CAN bus and in-vehicle networking
- `OTA` - Over-the-air updates and remote services
- `EXT` - External interfaces and physical access points
- `BCK` - Backend/cloud services and infrastructure
- `IVI` - Infotainment and in-vehicle information systems
- `IMM` - Immobilizer and vehicle access control
- `ADAS` - Advanced driver assistance systems

**Example**: `CSG-IVI-01`, `CSG-CAN-05`, `CSG-ADAS-12`

**Rules**:
- Use zero-padded 2-digit numbers (01, 02, ..., 99)
- Domain code must align with the primary affected domain
- CSG-IDs are independent of TS/RT/DS numbering (no 1:1 correspondence)
- One CSG may address multiple damage scenarios across multiple domains
- Numbering should be sequential within each domain

**ID Allocation Strategy**:
```
CSG-IVI-01  ← First infotainment CSG
CSG-IVI-02  ← Second infotainment CSG
CSG-CAN-01  ← First CAN bus CSG
CSG-CAN-02  ← Second CAN bus CSG
```

**Domain Selection Rules**:
- If CSG addresses damage scenarios from multiple domains, use the **primary affected domain**
- If CSG is cross-cutting (e.g., vehicle-wide authentication), use the **most critical domain**
- Document cross-domain applicability in Related DS-IDs field

---

### 2. Title

**Format**: Human-readable text (maximum 80 characters)

**Description**: Concise, descriptive name for the Cybersecurity Goal that identifies the protected asset or security property.

**Example**: 
- "Location Data Confidentiality"
- "CAN Message Authentication and Integrity"
- "Secure OTA Update Integrity"
- "Physical Access Control to Head Unit"
- "Driver Privacy Protection"
- "Vehicle Motion Control Integrity"

**Rules**:
- Use noun phrases describing the security property or protected asset
- Include the CIA property being protected (Confidentiality/Integrity/Availability) when relevant
- Keep under 80 characters for readability
- Avoid implementation details (e.g., "Encryption" → "Confidentiality")
- Be specific enough to distinguish from similar CSGs
- Use positive framing ("Data Confidentiality" not "Prevent Data Leakage")

**Naming Patterns**:
- `[Asset] + [CIA Property]` - "Location Data Confidentiality"
- `[System] + [Security Property]` - "CAN Bus Message Authentication"
- `[Function] + Protection` - "Driver Privacy Protection"

---

### Optional Goal Context

CSG entries may include these fields when OEM and supplier/component viewpoints
must be aligned. They do not replace any of the 9 required fields.

```markdown
**Goal Viewpoint**: OEM vehicle-level | Tier 1/component-level
**Parent Vehicle-Level Goal**: [CSG-ID or N/A for a vehicle-level goal]
```

Rules:
- Use `OEM vehicle-level` for the goal that protects a function delivered by the item.
- Use `Tier 1/component-level` only when a narrower allocation is needed.
- Component-level goals must name their parent vehicle-level goal or explain why no parent exists.
- Keep one CIA property per goal at both viewpoints.

---

### 3. Related DS-IDs

**Format**: List of Damage Scenario IDs from DS catalogue (one per line)

**Description**: The damage scenarios that this Cybersecurity Goal aims to prevent or mitigate. This field establishes the M:N mapping between CSGs and damage scenarios.

**Example**:
```
Related DS-IDs:
- DS-IVI-001 [EXAMPLE] (Unauthorized Driver Location Tracking)
- DS-IVI-002 [EXAMPLE] (Personal Information Exposure)
- DS-BCK-001 [EXAMPLE] (Telematics Backend Data Breach)
```

**Rules**:
- Must reference valid DS-IDs that exist in `data/ds.md`
- Include both the ID and the damage scenario title for clarity
- List all damage scenarios addressed by this CSG (1 to N relationship)
- Multiple CSGs may address the same DS-ID (M:N relationship allowed)
- Order by domain, then by ID number
- Minimum: 1 damage scenario per CSG
- Maximum: Typically 3-5 damage scenarios (if more, consider splitting the CSG)

**M:N Mapping Examples**:

*One CSG addressing multiple damage scenarios*:
```
CSG-IVI-01: Location Data Confidentiality
  ├─ DS-IVI-001 [EXAMPLE] (Location Tracking)
  ├─ DS-IVI-002 [EXAMPLE] (PII Exposure)
  └─ DS-BCK-001 [EXAMPLE] (Telematics Breach)
```

*Multiple CSGs addressing the same damage scenario*:
```
DS-CAN-001 [EXAMPLE]: Vehicle Motion Control via CAN Message Injection
  ├─ CSG-CAN-01: CAN Message Authentication
  ├─ CSG-CAN-02: ECU Authorization Control
  └─ CSG-ADAS-03: Critical Function Integrity
```

**Validation**:
- Every DS-ID listed must exist in `data/ds.md`
- Every DS-ID in catalogue must be addressed by at least one CSG (no orphan damage scenarios)
- If DS catalogue doesn't exist yet, mark as `[EXAMPLE]` during skill development

---

### 4. Related RT-IDs

**Format**: List of Risk Treatment IDs from RT catalogue (one per line)

**Description**: The risk treatment decisions associated with this Cybersecurity Goal. This field links CSGs to the risk treatment workflow and indicates which treatments implement this goal.

**Example**:
```
Related RT-IDs:
- RT-IVI-001 [EXAMPLE] (Location Tracking Threat - Reduce via Encryption)
- RT-IVI-002 [EXAMPLE] (PII Exposure - Reduce via Access Controls)
- RT-BCK-001 [EXAMPLE] (Backend API Bypass - Reduce via Authentication)
```

**Rules**:
- Optional field - may be empty during initial CSG formulation
- Must reference valid RT-IDs that exist in `data/rt.md` (when RT catalogue exists)
- Include both the ID and the risk treatment title
- List all risk treatments that implement or contribute to this CSG
- Order by domain, then by ID number
- Do not create a new CSG for pure `Accept` decisions; the claim stays in `data/rt.md`
- Do not create a new CSG for pure `Transfer` decisions; link RT-IDs only when that RT entry includes active mitigation
- If RT catalogue doesn't exist yet, leave blank or mark as `[TBD]`

**RT-to-CSG Relationship**:
```
CSG-IVI-01: Location Data Confidentiality
  ↓ (implements)
RT-IVI-001 [EXAMPLE]: Reduce via encryption
RT-IVI-002 [EXAMPLE]: Reduce via access controls
RT-BCK-001 [EXAMPLE]: Reduce via authentication
```

**When to Leave Blank**:
- During initial TARA cycle before risk treatment decisions are made
- When CSG is newly created and treatments are not yet defined
- When performing damage scenario analysis before threat scenarios exist

**Validation**:
- Every RT-ID listed must exist in `data/rt.md` (if RT catalogue exists)
- Every `Reduce` risk treatment should link to at least one CSG
- `Accept` and pure `Transfer` treatments should be documented in `data/rt.md` without forcing a CSG entry

---

### 5. Goal Statement

**Format**: 1-3 sentences expressing the cybersecurity objective as a shall-statement

**Description**: Clear, testable statement of what the system shall achieve to satisfy this Cybersecurity Goal. The statement must be verifiable and implementation-independent.

**Example**:
```
Goal Statement:
The vehicle system shall ensure that real-time location data and historical travel patterns are accessible only to authorized users and services. The system shall prevent unauthorized exfiltration, storage, or sharing of location information that could enable driver surveillance or movement tracking.
```

**Example**:
```
Goal Statement:
The vehicle shall ensure that CAN bus messages controlling critical driving functions (steering, braking, acceleration) can only originate from authenticated and authorized ECUs. The system shall detect and reject malicious or spoofed CAN messages that could affect vehicle motion control.
```

**Example**:
```
Goal Statement:
The OTA update system shall ensure that only cryptographically signed and verified firmware images from the authorized manufacturer can be installed on vehicle ECUs. The system shall prevent installation of modified, malicious, or unauthorized software packages.
```

**Rules**:
- Use "shall" language following ISO 26262/21434 conventions
- Express the security property to be achieved, not the implementation mechanism
- Be specific enough to enable verification (testable)
- Avoid mentioning specific technologies (AES, TLS, etc.) - focus on properties
- Length: 1-3 sentences (typically 2 sentences)
- First sentence: What shall be protected
- Second sentence: What threats shall be prevented
- Keep total length under 400 characters for readability

**Goal Statement Structure**:
```
The [system/component] shall ensure that [security property].
The system shall prevent/detect [threat action] that could [damage consequence].
```

**Technology-Agnostic Examples**:
- ✅ "ensure confidentiality of location data" (property)
- ❌ "encrypt location data using AES-256" (implementation)
- ✅ "authenticate CAN message sources" (property)
- ❌ "implement SecOC with HMAC-SHA256" (implementation)

**Verification Criteria**:
- Can you write a test case to verify this goal is met?
- Does the statement describe "what" without prescribing "how"?
- Is the statement specific enough to guide CSR (Cybersecurity Requirement) derivation?

---

### 6. CIA Property

**Format**: Exactly one of: `Confidentiality`, `Integrity`, `Availability`

**Description**: The single CIA property that this Cybersecurity Goal protects. If multiple properties apply, create separate CSG entries.

**Example**:
```
CIA Property: Integrity
```

**Example**:
```
CIA Property: Availability
```

**CIA Triad Definitions (ISO 21434 Context)**:

| Property | Definition | Vehicle Examples |
|----------|-----------|------------------|
| **Confidentiality** | Information is accessible only to authorized entities | Location data, driver profiles, vehicle credentials, diagnostic data |
| **Integrity** | Information and systems are accurate and cannot be modified without authorization | CAN messages, OTA updates, ECU firmware, sensor data, control commands |
| **Availability** | Information and systems are accessible when needed by authorized entities | Critical ECU functions, safety systems, emergency services, driver HMI |

**Rules**:
- Must select exactly one CIA property
- If a damage scenario needs multiple properties, create multiple CSGs
- Do not use primary/secondary notation inside one CSG entry

**Domain-Typical Patterns**:
```
IVI/BCK domains → Often Confidentiality (data protection)
CAN/ADAS domains → Often Integrity (control message authentication)
IMM/ADAS domains → Often Availability (safety-critical functions)
OTA domain → Often separate Integrity and Availability CSGs (secure updates + rollback)
```

**Selection Guidelines**:

*Confidentiality-focused CSGs*:
- Protect sensitive data from unauthorized disclosure
- Privacy-related goals (location, PII, driver behavior)
- Credential and key protection
- Example: "Location Data Confidentiality"

*Integrity-focused CSGs*:
- Protect data/commands from unauthorized modification
- Authentication and authorization goals
- Code signing and secure boot
- Example: "CAN Message Authentication and Integrity"

*Availability-focused CSGs*:
- Ensure critical functions remain accessible
- DoS attack prevention
- System resilience and failover
- Example: "Critical ECU Availability"

*Multiple CIA Properties Across Multiple CSGs*:
- Communication path needs confidentiality and integrity → create one Confidentiality CSG and one Integrity CSG
- Safety function needs integrity and availability → create one Integrity CSG and one Availability CSG

**Validation**:
- CIA property selection must align with Goal Statement
- CIA property must match the SFOP dimensions of Related DS-IDs
- If DS has Privacy impact → CSG should include Confidentiality
- If DS has Safety/Operational impact → CSG should include Integrity or Availability

---

### 7. Cybersecurity Claim

**Format**: Leave empty in `data/csg.md`

**Description**: Cybersecurity claims for `Accept` and `Transfer` decisions are owned by `data/rt.md`. Keep the field present for schema stability, but leave it empty in CSG entries.

**Example**:
```
Cybersecurity Claim:
```

**Rules**:
- Leave this field empty for all CSG entries
- Put `Accept` / `Transfer` justification, approval, and residual-risk text in `data/rt.md`
- If a `Transfer` RT entry includes active mitigation, create the CSG and link the RT-ID, but keep the claim in `data/rt.md`
- If a decision is pure `Accept` or pure `Transfer`, do not create a new CSG entry solely to hold the claim

**Validation**:
- `data/csg.md` must not duplicate approval or residual-risk claim text from `data/rt.md`
- If a listed RT-ID is `Transfer`, verify whether that RT entry contains active mitigation; if not, there should usually be no linked CSG
- Claim completeness is validated in the risk-treatment workflow, not in the CSG workflow

**Traceability to Risk Treatment**:
```
RT-IVI-001 [EXAMPLE]: Treatment Decision = Reduce
  → CSG-IVI-01 exists, Cybersecurity Claim field remains empty

RT-IVI-002 [EXAMPLE]: Treatment Decision = Accept
  → No new CSG; claim stays in data/rt.md

RT-OTA-004 [EXAMPLE]: Treatment Decision = Transfer + supplier-implemented mitigation
  → CSG-OTA-01 exists, Cybersecurity Claim field remains empty, claim stays in data/rt.md
```

---

### 8. Rationale

**Format**: 2-4 sentences explaining why this Cybersecurity Goal is necessary

**Description**: Justification for the CSG based on damage scenario analysis, regulatory requirements, or business context. The rationale connects the CSG back to the damage scenarios and explains the security objective.

**Example**:
```
Rationale:
Unauthorized access to real-time vehicle location data enables continuous 
driver surveillance, stalking, and privacy violations. Location tracking 
damages comply with GDPR Article 6 requirements for lawful processing of 
geolocation data. This goal ensures location data confidentiality to prevent 
privacy harm documented in DS-IVI-001 [EXAMPLE] and DS-IVI-002 [EXAMPLE].
```

**Example**:
```
Rationale:
Malicious CAN message injection can override legitimate ECU commands and 
cause unintended vehicle acceleration, braking, or steering (DS-CAN-001 [EXAMPLE], 
DS-CAN-003 [EXAMPLE]). Message authentication and integrity protection are required 
by UN R155 Annex 5 Part A (Vehicle Motion Control). This goal ensures only 
authorized ECUs can control critical driving functions.
```

**Example**:
```
Rationale:
Compromised OTA updates could install malicious firmware enabling persistent 
vehicle control or data exfiltration (DS-OTA-001 [EXAMPLE] [EXAMPLE], DS-OTA-003 [EXAMPLE] [EXAMPLE]). Code integrity 
verification is mandated by ISO 21434 Clause 11 (Software updates). This goal 
ensures only cryptographically signed updates from the authorized manufacturer 
can be installed on vehicle ECUs.
```

**Rules**:
- Length: 2-4 sentences (typically 3 sentences)
- First sentence: What damage scenarios motivate this goal
- Second sentence: Regulatory or standards context (if applicable)
- Third sentence: How this goal prevents the damage
- Reference specific DS-IDs to establish traceability
- Cite relevant regulations: UN R155, ISO 21434, GDPR, GB 44495, etc.
- Keep total length under 600 characters

**Rationale Structure Template**:
```
[Threat/damage description and consequence] ([DS-IDs]). 
[Regulatory/standards requirement if applicable]. 
This goal ensures [security property] to prevent [damage type].
```

**Regulatory References to Include**:
- **UN R155**: For vehicle cybersecurity type approval (EU regulation)
- **ISO/SAE 21434**: For automotive cybersecurity engineering processes
- **GDPR**: For privacy and personal data protection (EU)
- **GB 44495**: For automotive data security (China)
- **ISO 26262**: For functional safety interactions
- **SAE J3061**: For cybersecurity guidebook reference

**Validation**:
- Rationale must reference at least one Related DS-ID
- Rationale should explain the CIA Property selection
- Rationale must stay focused on the active security objective, not duplicate RT claim approval text
- Regulatory citations must be accurate and relevant

---

### 9. Last Updated

**Format**: ISO 8601 date (`YYYY-MM-DD`)

**Description**: Date when this CSG entry was last modified. Used for version control, audit trails, and traceability to risk assessment decisions.

**Example**: 
```
Last Updated: 2026-03-20
```

**Rules**:
- Use ISO 8601 format: `YYYY-MM-DD`
- Update whenever any field in the CSG entry changes
- Initial creation date = Last Updated date
- Date must be valid (no future dates unless planning)
- Used for audit trails and regulatory compliance documentation

**When to Update**:
- Initial CSG creation
- Changes to Goal Statement
- Addition/removal of Related DS-IDs or RT-IDs
- Changes to CIA Property
- Updates to Rationale based on new damage scenarios
- Changes to Title

**Audit Trail Usage**:
```
CSG-IVI-01: Location Data Confidentiality
Last Updated: 2026-03-20
  ← Modified to add DS-BCK-001 [EXAMPLE] (Telematics Backend Breach)
  
Previous version: 2026-02-15
  ← Initial creation with DS-IVI-001 [EXAMPLE], DS-IVI-002 [EXAMPLE]
```

**Validation**:
- Date must be in past or present (no future dates)
- Date format must be YYYY-MM-DD (ISO 8601)
- Date should be consistent with Related RT-IDs dates (CSG typically created before or during RT cycle)

---

## M:N Mapping Rules

Cybersecurity Goals have **many-to-many (M:N) relationships** with Damage Scenarios:
- **One CSG may address multiple DS-IDs** (1:N) - A single security goal can prevent multiple types of damage
- **One DS-ID may be addressed by multiple CSGs** (M:1) - Complex damage scenarios require multiple security goals

### Example: One CSG Addressing Multiple DS-IDs

```
CSG-IVI-01: Location Data Confidentiality
Related DS-IDs:
  - DS-IVI-001 [EXAMPLE] (Unauthorized Driver Location Tracking)
  - DS-IVI-002 [EXAMPLE] (Personal Information Exposure)
  - DS-BCK-001 [EXAMPLE] (Telematics Backend Data Breach)
  
Goal Statement: The vehicle system shall ensure that real-time location 
data and historical travel patterns are accessible only to authorized users 
and services.
```

**Rationale**: All three damage scenarios involve location data breaches through different attack vectors (infotainment compromise, PII leak, backend breach). A single CSG for "Location Data Confidentiality" addresses the root security property needed to prevent all three damages.

### Example: Multiple CSGs Addressing One DS-ID

```
DS-CAN-001 [EXAMPLE]: Unintended Vehicle Acceleration via CAN Message Injection

Addressed by three CSGs:

CSG-CAN-01: CAN Message Authentication and Integrity
  → Ensures CAN messages can only originate from authenticated ECUs

CSG-CAN-02: ECU Authorization Control
  → Ensures only authorized ECUs can send critical control messages

CSG-ADAS-03: Critical Function Integrity Protection
  → Ensures safety-critical functions validate all inputs before execution
```

**Rationale**: Preventing unintended vehicle acceleration requires multiple security goals: message authentication (crypto), sender authorization (access control), and input validation (defense-in-depth). Each CSG addresses a different aspect of the defense strategy.

### M:N Mapping Best Practices

**When to use 1:N (one CSG, multiple DS-IDs)**:
- Damage scenarios share the same root cause or security property
- Same CIA triad property applies across multiple damages
- Example: Data confidentiality goals addressing multiple privacy breaches

**When to use M:1 (multiple CSGs, one DS-ID)**:
- Damage scenario is complex and requires defense-in-depth
- Multiple security properties needed (create separate CSGs for each property)
- Different layers of defense (network, application, physical)
- Example: Critical safety functions requiring authentication, authorization, and input validation

**Validation Rules**:
- Every DS-ID in catalogue must be referenced by at least one CSG (no orphan damage scenarios)
- Every CSG must reference at least one DS-ID (no orphan goals)
- Typical CSG has 1-3 Related DS-IDs (if more than 5, consider splitting)
- Typical DS-ID is addressed by 1-2 CSGs (if more than 4, review for goal overlap)

### M:N Traceability Matrix Example

| CSG-ID | DS-IVI-001 [EXAMPLE] | DS-IVI-002 [EXAMPLE] | DS-CAN-001 [EXAMPLE] | DS-CAN-003 [EXAMPLE] | DS-BCK-001 [EXAMPLE] |
|--------|-----------|-----------|-----------|-----------|-----------|
| CSG-IVI-01 | ✓ | ✓ | | | ✓ |
| CSG-IVI-02 | | ✓ | | | |
| CSG-CAN-01 | | | ✓ | ✓ | |
| CSG-CAN-02 | | | ✓ | | |
| CSG-ADAS-03 | | | ✓ | ✓ | |

This matrix shows:
- DS-IVI-001 [EXAMPLE] addressed by 1 CSG
- DS-IVI-002 [EXAMPLE] addressed by 2 CSGs (privacy requires multiple security properties)
- DS-CAN-001 [EXAMPLE] addressed by 3 CSGs (critical safety function requires defense-in-depth)

---

## CSG Domain Assignment Guidelines

When creating a new CSG, select the domain code based on:

1. **Primary Affected System**: Which vehicle domain is most directly impacted?
2. **Attack Surface Origin**: Where does the security control need to be implemented?
3. **Asset Ownership**: Which system "owns" the security property?

### Domain Selection Decision Tree

```
Is CSG primarily about data confidentiality/privacy?
  └─ YES: Use IVI or BCK domain
  └─ NO: Continue to next question

Is CSG primarily about critical vehicle control or motion?
  └─ YES: Use CAN or ADAS domain
  └─ NO: Continue to next question

Is CSG primarily about software updates or remote services?
  └─ YES: Use OTA or BCK domain
  └─ NO: Continue to next question

Is CSG primarily about physical access or external interfaces?
  └─ YES: Use EXT or IMM domain
```

### Domain-Typical CSG Categories

| Domain | Typical CSG Categories | Example CSG Titles |
|--------|----------------------|-------------------|
| **IVI** | Data privacy, HMI security, multimedia protection | Location Data Confidentiality, Driver Profile Privacy |
| **CAN** | Message authentication, bus integrity, ECU authorization | CAN Message Authentication, Bus Access Control |
| **OTA** | Update integrity, remote service security, rollback protection | Secure OTA Update Integrity, Remote Service Authentication |
| **EXT** | Physical access control, connector security, tamper detection | USB Port Access Control, Physical Tamper Detection |
| **BCK** | Cloud security, API protection, data center controls | Backend API Authentication, Cloud Data Confidentiality |
| **IMM** | Vehicle access, key management, anti-theft | Immobilizer Key Confidentiality, Vehicle Access Authorization |
| **ADAS** | Safety function integrity, sensor protection, failsafe | Critical Function Integrity, Sensor Data Authenticity |

### Cross-Domain CSGs

Some CSGs span multiple domains. In these cases:
- Use the **most critical** domain (safety > privacy > convenience)
- Use the domain where the **primary security control** is implemented
- Document cross-domain applicability in Related DS-IDs and Rationale

**Example**:
```
CSG-CAN-05: Vehicle-Wide Authentication Framework
Related DS-IDs:
  - DS-CAN-001 [EXAMPLE] (CAN Message Injection)
  - DS-IVI-003 [EXAMPLE] (Malicious Code Execution)
  - DS-OTA-002 [EXAMPLE] (Unauthorized Firmware Update)
  - DS-ADAS-001 [EXAMPLE] (Sensor Spoofing)

Domain Rationale: Assigned to CAN domain because authentication framework 
is primarily implemented at the CAN gateway and central ECU level, even 
though it protects assets across IVI, OTA, and ADAS domains.
```

---

## CSG Lifecycle and Workflow

Cybersecurity Goals are created during the TARA process using Clause 9 concept-level intent and Clause 15.9 workflow context:

### CSG Creation Workflow

```
1. Damage Scenario Analysis (Clause 15.6)
   ↓
2. Threat Scenario Enumeration (Clause 15.7)
   ↓
3. Risk Assessment (Clause 15.8)
   ↓
4. Risk Treatment Decision (Clause 15.8)
   ↓
5. Cybersecurity Goal Formulation (Clause 15.9) ← CSG CREATED HERE
   ↓
6. Cybersecurity Requirements Derivation (Clause 15.9) ← CSR derived from CSG
```

### When to Create a New CSG

Create a new CSG when:
- A damage scenario requires a new security property not covered by existing CSGs
- Existing CSGs are too broad and need decomposition
- Regulatory requirements mandate a specific security objective
- Risk treatment decision (`Avoid`, `Reduce`, or mitigation-bearing `Transfer`) requires a new security goal

### When to Update an Existing CSG

Update an existing CSG when:
- New damage scenarios are identified that relate to the same security property
- Risk treatment decisions change in a way that introduces or removes active mitigation (e.g., Accept → Reduce)
- Goal Statement needs refinement based on CSR derivation experience
- Related RT-IDs are added after treatments are implemented

### When to Retire a CSG

Retire (but preserve for audit) a CSG when:
- All Related DS-IDs are eliminated (risk Avoided)
- CSG is superseded by a more comprehensive goal
- Asset or feature is removed from vehicle architecture

**Note**: Never delete CSG entries - mark as "[RETIRED]" in title and update Last Updated date for audit trail.

---

## Validation Checklist

Use this checklist when creating or reviewing a CSG entry:

### Schema Completeness
- [ ] All 9 required fields are populated (CSG-ID, Title, Related DS-IDs, Related RT-IDs, Goal Statement, CIA Property, Cybersecurity Claim, Rationale, Last Updated)
- [ ] CSG-ID follows format `CSG-[DOMAIN]-[NN]` with valid domain code
- [ ] Title is ≤80 characters and describes the security property
- [ ] Goal Statement is 1-3 sentences with "shall" language
- [ ] Last Updated is valid ISO 8601 date (YYYY-MM-DD)

### Traceability
- [ ] All Related DS-IDs exist in `data/ds.md` (or marked [EXAMPLE])
- [ ] All Related RT-IDs exist in `data/rt.md` (or marked [TBD] if RT cycle not complete)
- [ ] At least 1 Related DS-ID is listed (no orphan CSGs)
- [ ] Rationale references at least one Related DS-ID
- [ ] CIA Property aligns with SFOP dimensions of Related DS-IDs

### Content Quality
- [ ] Goal Statement is technology-agnostic (describes "what" not "how")
- [ ] Goal Statement is testable and verifiable
- [ ] CIA Property correctly reflects the security objective (Confidentiality/Integrity/Availability)
- [ ] Rationale explains why the CSG is necessary (damage prevention)
- [ ] Rationale cites relevant regulations if applicable (UN R155, ISO 21434, GDPR, etc.)
- [ ] Cybersecurity Claim field is empty and claim documentation stays in `data/rt.md`

### ISO 21434 Alignment
- [ ] CSG aligns with Clause 15.9 (Cybersecurity Goals formulation)
- [ ] CSG is derived from damage scenarios (Clause 15.6)
- [ ] CSG is linked to risk treatment decisions (Clause 15.8)
- [ ] Goal Statement uses "shall" language following ISO conventions
- [ ] CSG is technology-independent and implementation-agnostic

### M:N Mapping Validation
- [ ] If CSG addresses multiple DS-IDs, Rationale explains the commonality
- [ ] If DS-ID is addressed by multiple CSGs, Goal Statements are distinct and non-overlapping
- [ ] CSG has 1-5 Related DS-IDs (if more than 5, consider splitting)
- [ ] No circular dependencies (CSG → DS → CSG)

---

## Complete CSG Entry Example

```markdown
### CSG-IVI-01: Location Data Confidentiality

**CSG-ID**: CSG-IVI-01

**Title**: Location Data Confidentiality

**Related DS-IDs**:
- DS-IVI-001 [EXAMPLE] (Unauthorized Driver Location Tracking)
- DS-IVI-002 [EXAMPLE] (Personal Information Exposure)
- DS-BCK-001 [EXAMPLE] (Telematics Backend Data Breach)

**Related RT-IDs**:
- RT-IVI-001 [EXAMPLE] (Location Tracking Threat - Reduce via Encryption)
- RT-IVI-002 [EXAMPLE] (PII Exposure - Reduce via Access Controls)
- RT-BCK-001 [EXAMPLE] (Backend API Bypass - Reduce via Authentication)

**Goal Statement**:
The vehicle system shall ensure that real-time location data and historical travel patterns are accessible only to authorized users and services. The system shall prevent unauthorized exfiltration, storage, or sharing of location information that could enable driver surveillance or movement tracking.

**CIA Property**: Confidentiality

**Cybersecurity Claim**: 

**Rationale**:
Unauthorized access to real-time vehicle location data enables continuous driver surveillance, stalking, and privacy violations (DS-IVI-001 [EXAMPLE], DS-IVI-002 [EXAMPLE], DS-BCK-001 [EXAMPLE]). Location tracking damages comply with GDPR Article 6 requirements for lawful processing of geolocation data and China GB 44495 automotive data security regulations. This goal ensures location data confidentiality to prevent privacy harm documented in related damage scenarios.

**Last Updated**: 2026-03-20
```

---

## References

- **ISO/SAE 21434:2021** - Road vehicles — Cybersecurity engineering
  - Clause 9: Concept / cybersecurity concept phase
  - Clause 15.6: Damage scenario identification
  - Clause 15.7: Threat scenario identification  
  - Clause 15.8: Risk determination and risk treatment decisions
  - Clause 15.9: Cybersecurity goals and cybersecurity requirements
  
- **UN Regulation No. 155** - Uniform provisions concerning the approval of vehicles with regards to cyber security and cyber security management system
  - Annex 5, Part A: Threat categories and vehicle systems
  
- **ISO/IEC 27001:2022** - Information security management systems
  - For CIA triad property definitions and security objectives

- **NIST SP 800-30** - Guide for Conducting Risk Assessments
  - For risk treatment decision framework

---

## Schema Version

- **Version**: 1.0
- **Date**: 2026-03-20
- **Status**: Active
- **Maintained By**: TARA Maker Skill / CSG Module
