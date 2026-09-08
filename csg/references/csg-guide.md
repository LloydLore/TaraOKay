# Cybersecurity Goal Derivation Methodology - ISO 21434 TARA

This guide provides methodology for deriving cybersecurity goals in ISO 21434 TARA (Threat Analysis and Risk Assessment) workflows, using Clause 9 concept-phase context and Clause 15.9 TARA workflow context. RT-owned cybersecurity claims remain in `data/rt.md`.

---

## Overview

**Cybersecurity Goals (CSGs)** are high-level requirements that define WHAT must be protected to prevent or mitigate damage scenarios. They bridge the gap between risk analysis (damage scenarios, threats) and technical implementation (cybersecurity requirements, controls).

**Key Characteristics**:
- Derived FROM damage scenarios (not threat scenarios)
- Expressed as SHALL statements (normative requirements)
- Anchored to the vehicle-level function and item boundary captured during item definition
- Assigned exactly one CIA property per CSG (Confidentiality, Integrity, or Availability)
- Technology-agnostic (HOW is defined later in cybersecurity requirements)
- Must be verifiable at integration/validation stage

**Relationship to Other TARA Artifacts**:
```
Damage Scenario (DS-*)
    ↓ (defines impact)
Risk Treatment Decision (RT-*)
    ├─ Avoid / Reduce / Transfer + active mitigation → Cybersecurity Goal (CSG-*)
    │                                                ↓ (drives requirements)
    │                                             Cybersecurity Requirement (CSR-*)
    │                                                ↓ (specifies control)
    │                                             Security Control Implementation
    └─ Pure Transfer / Accept → RT-owned claim only in `data/rt.md`
```

---

## Goal Granularity Policy

Cybersecurity goals are not the center of the concept model. They are derived
objectives created after damage and treatment context is known.

- **Vehicle-level goal**: use when the goal protects a function delivered by the item to road users or stakeholders.
- **Component-level goal**: use only when a supplier/component boundary needs a more local objective.
- **Parent alignment**: every component-level goal must state which vehicle-level goal or affected function it supports.
- **One CIA property per goal**: split goals when integrity, availability, and confidentiality need separate verification.
- **No implementation detail**: algorithms, key sizes, products, and test procedures belong in CSR.

When OEM and Tier 1 viewpoints differ, keep the vehicle-level goal as the parent
and express the component-level goal as a narrower child objective. Do not create
parallel goals with no parent relationship.

---

## The 5-Step Derivation Methodology

### Step 1: Read Damage Scenario → Identify Impact Dimensions

**Objective**: Understand WHAT harm occurs and WHICH SFOP dimension(s) are affected.

**Process**:
1. Locate the damage scenario file (e.g., `data/ds.md`)
2. Read the **SFOP Dimensions Affected** section
3. Read the affected function and Function with RISK in **Assessment Context**
4. Identify which dimension(s) have scores ≥ 2 (Moderate or higher)
5. Note the **rationale** explaining WHY each dimension is affected

**Example**: DS-IVI-001 [EXAMPLE] "Unauthorized Driver Location Tracking"
- **Safety**: 1 (Negligible) - ❌ Not a goal driver
- **Financial**: 3 (Severe) - ✅ GDPR/GB 44495 violations
- **Operational**: 1 (Negligible) - ❌ Not a goal driver
- **Privacy**: 4 (Critical) - ✅ Continuous surveillance

**Key Impact Dimensions**: Financial (F=3) + Privacy (P=4)

**Output of Step 1**: List of SFOP dimensions with score ≥ 2 that need protection

---

### Step 2: Read Risk Treatment Decision → Identify Treatment Approach

**Objective**: Determine IF a cybersecurity goal is needed based on the chosen treatment.

**Process**:
1. Locate the risk treatment file (e.g., `data/rt.md`)
2. Find the RT-* entry corresponding to the damage scenario
3. Read the **Treatment Decision** field
4. Apply the CSG derivation rules based on treatment type

**CSG Derivation Rules by Treatment Type**:

| Treatment Shape | CSG Required? | Rationale |
|----------------|---------------|-----------|
| **Avoid** | ✅ Yes | Goal describes WHAT must be eliminated/redesigned |
| **Reduce** | ✅ Yes | Goal describes WHAT controls must achieve |
| **Transfer + active mitigation** | ✅ Yes | Goal describes WHAT the transferred/implemented mitigation must achieve |
| **Pure Transfer** | ❌ No | No new active goal; keep the claim in `data/rt.md` |
| **Accept** | ❌ No | Risk consciously accepted without mitigation; keep the claim in `data/rt.md` |

**Example**: RT-IVI-001 [EXAMPLE] for DS-IVI-001 [EXAMPLE]
- **Treatment Decision**: Reduce
- **Justification**: Implement access control, data minimization, encryption
- **CSG Required?**: ✅ Yes (need goal defining WHAT protection is required)

**Special Case - Transfer/Accept**: Separate pure claims from active mitigation. If treatment is pure Transfer or Accept, do NOT create a CSG. If a Transfer entry includes implemented/planned mitigation, derive a CSG and link it back to the RT-ID.

**Output of Step 2**: Decision whether CSG is required (Yes → continue to Step 3; No → jump to Step 5)

---

### Step 3: Formulate Goal Statement → Address Impact

**Objective**: Write a clear, verifiable SHALL statement that addresses the identified impact dimensions.

**Goal Statement Template**:
```
The [COMPONENT/SYSTEM] shall [PROTECTION ACTION] to [PREVENT/MITIGATE] [DAMAGE SCENARIO].
```

**Protection Action Patterns by Impact Type**:

#### Safety Impact (S ≥ 2) → Integrity/Availability Goals

**Pattern**: "maintain correct operation", "detect and respond to anomalies", "ensure availability"

**Examples**:
- S=3 (Severe): "The CAN gateway shall validate message authenticity to prevent injection of malicious commands."
- S=4 (Critical): "The steering ECU shall maintain functional safety integrity to prevent loss of vehicle control."

**Rationale**: Safety harm typically results from compromised data integrity (corrupted safety functions) or loss of availability (safety function unavailable).

---

#### Financial Impact (F ≥ 2) → Confidentiality/Integrity Goals

**Pattern**: "protect against unauthorized access", "prevent tampering", "maintain audit trail"

**Examples**:
- F=3 (Severe): "The backend API shall authenticate all requests to prevent unauthorized vehicle commands."
- F=3 (Severe): "The infotainment system shall protect stored payment credentials to prevent financial fraud."

**Rationale**: Financial harm results from data breaches (confidentiality), unauthorized transactions (integrity), or liability from compromised systems.

---

#### Operational Impact (O ≥ 2) → Availability Goals

**Pattern**: "ensure continuous operation", "recover from failures", "maintain service availability"

**Examples**:
- O=3 (Severe): "The telematics control unit shall resist denial-of-service attacks to maintain connectivity."
- O=4 (Critical): "The immobilizer system shall remain operational to prevent unauthorized vehicle startup."

**Rationale**: Operational harm results from service degradation or complete loss of function (availability violation).

---

#### Privacy Impact (P ≥ 2) → Confidentiality Goals

**Pattern**: "protect personal data", "limit data collection", "control data access"

**Examples**:
- P=3 (Severe): "The connected services platform shall protect location data from unauthorized disclosure."
- P=4 (Critical): "The head unit shall minimize collection of personally identifiable information to prevent privacy violations."

**Rationale**: Privacy harm results from unauthorized disclosure of personal data (confidentiality violation).

---

### Impact-to-Goal Mapping Table

This table provides quick guidance for mapping SFOP dimensions to CIA properties:

| SFOP Dimension | Score | Primary CIA Property | Typical Goal Pattern | Example Damage Scenario |
|----------------|-------|---------------------|---------------------|------------------------|
| **Safety (S)** | 3-4 | **Integrity (I)** | Validate/authenticate safety functions | Loss of steering control |
| | | **Availability (A)** | Ensure safety function remains operational | ADAS emergency braking disabled |
| **Financial (F)** | 2-3 | **Confidentiality (C)** | Protect payment/business data | Payment credential theft |
| | 3-4 | **Integrity (I)** | Prevent unauthorized transactions | Fraudulent vehicle unlock |
| **Operational (O)** | 2-4 | **Availability (A)** | Maintain service/function availability | Infotainment DoS attack |
| | 3-4 | **Integrity (I)** | Preserve operational functionality | Firmware corruption |
| **Privacy (P)** | 2-4 | **Confidentiality (C)** | Protect personal data | Unauthorized location tracking |

**Important**: A single damage scenario may map to MULTIPLE CIA properties if multiple SFOP dimensions are affected.

---

### Goal Statement Quality Checklist

Before finalizing a goal statement, verify:

- ✅ **Uses "shall" (normative requirement)**: "The system shall..." not "The system should..."
- ✅ **Identifies specific component/system**: "The head unit" not "The vehicle"
- ✅ **Names the protected function or asset**: goal links back to affected function or DS context
- ✅ **States WHAT, not HOW**: "authenticate requests" not "use OAuth 2.0"
- ✅ **Addresses the damage scenario**: Clear link between goal and harm being prevented
- ✅ **Verifiable**: Can test whether goal is achieved (measurable)
- ✅ **Technology-agnostic**: Doesn't mandate specific implementation (AES-256, RSA-4096, etc.)

**Example - Good Goal**:
> "The infotainment system shall protect user location data to prevent unauthorized tracking."

**Example - Bad Goal**:
> "The system should probably use encryption for privacy."

**Why Bad?**:
- Uses "should" (not normative)
- No specific component identified
- Prescribes HOW (encryption) instead of WHAT (protection)
- Vague (no clear verification criteria)

---

### Step 4: Assign CIA Property

**Objective**: Classify the goal according to CIA triad for traceability and requirement derivation.

**CIA Property Definitions**:

#### Confidentiality (C)
**Definition**: Prevention of unauthorized disclosure of information.

**When to Assign**: Goal addresses data protection, access control, privacy, or information leakage.

**Keywords**: protect, restrict access, authorize, encrypt, anonymize, limit disclosure

**Examples**:
- "The connected services platform shall restrict access to user location data." → **Confidentiality**
- "The backend API shall authenticate all requests before granting vehicle control." → **Confidentiality**

---

#### Integrity (I)
**Definition**: Prevention of unauthorized modification of data or functionality.

**When to Assign**: Goal addresses data validation, authentication, tamper protection, or correctness of operation.

**Keywords**: validate, authenticate, verify, detect tampering, maintain correctness, prevent modification

**Examples**:
- "The CAN gateway shall validate message authenticity to prevent injection attacks." → **Integrity**
- "The ADAS ECU shall verify sensor data integrity to prevent spoofing." → **Integrity**

---

#### Availability (A)
**Definition**: Ensuring timely and reliable access to services and data.

**When to Assign**: Goal addresses service continuity, DoS resistance, failover, or recovery.

**Keywords**: ensure availability, maintain operation, resist denial-of-service, recover from failure, remain operational

**Examples**:
- "The telematics control unit shall resist denial-of-service attacks." → **Availability**
- "The immobilizer system shall remain operational during attempted unauthorized access." → **Availability**

---

### CIA Assignment Decision Tree

```
┌─────────────────────────────────────────┐
│ Does goal address DATA DISCLOSURE?      │
│ (unauthorized access, privacy, leakage) │
└────────┬────────────────────────────────┘
         │ Yes → Confidentiality (C)
         │ No ↓
┌─────────────────────────────────────────┐
│ Does goal address DATA/FUNCTION TAMPERING? │
│ (validation, authentication, corruption)│
└────────┬────────────────────────────────┘
         │ Yes → Integrity (I)
         │ No ↓
┌─────────────────────────────────────────┐
│ Does goal address SERVICE AVAILABILITY? │
│ (continuity, DoS, failover, recovery)   │
└────────┬────────────────────────────────┘
         │ Yes → Availability (A)
         │
         └→ If multiple CIA properties apply, create SEPARATE goals
```

**Important - Multiple CIA Properties**: If a damage scenario affects multiple SFOP dimensions that map to different CIA properties, create MULTIPLE goals (one CIA property per CSG).

**Example**: DS-IVI-002 [EXAMPLE] "Malicious Firmware Execution"
- Impact: S=3, O=3, F=3, P=1
- Goal 1 (Integrity): "The head unit shall verify firmware authenticity to prevent malicious code execution."
- Goal 2 (Availability): "The head unit shall maintain operational availability during firmware update failures."

**Output of Step 4**: CIA property assignment for each goal (C, I, or A)

---

### Step 5: Review RT-Owned Claims (if Risk Retained)

**Objective**: Keep cybersecurity-goal scope narrow. Accept / pure Transfer claims belong in `data/rt.md`, not in `data/csg.md`.

**When Claims Are Required**:

| Treatment Shape | Claim Required? | Where it lives |
|----------------|-----------------|----------------|
| **Avoid** | ❌ No | N/A |
| **Reduce** | ❌ No | N/A |
| **Transfer + active mitigation** | ✅ Yes | `data/rt.md` |
| **Pure Transfer** | ✅ Yes | `data/rt.md` |
| **Accept** | ✅ Yes | `data/rt.md` |

**Key Distinction**: 
- **Cybersecurity Goal (CSG)** = Active mitigation (`Avoid`, `Reduce`, and mitigation-bearing `Transfer` treatments)
- **Cybersecurity Claim** = Residual-risk or responsibility documentation owned by `data/rt.md`
- **CSR allocation** = Item or component location where the goal becomes implementable

---

### What to Verify in `data/rt.md`

When a related RT entry is `Accept` or pure `Transfer`, confirm that `data/rt.md` contains:
- a clear risk statement tied to DS/TS context
- justification for the decision
- approval / review metadata required by the risk-treatment workflow

Do not restate that material in `data/csg.md`.

---

### Claim vs. Goal Decision Matrix

| Treatment Shape | Output Artifact | Purpose | Example |
|----------------|----------------|---------|---------|
| **Avoid** | CSG (Goal) | Define WHAT must be eliminated/redesigned | "The system shall remove deprecated TLS 1.0 support." |
| **Reduce** | CSG (Goal) | Define WHAT controls must achieve | "The API shall authenticate all requests." |
| **Transfer + active mitigation** | CSG + RT claim | Define the active goal while RT records the transfer | "The update service shall verify supplier-signed firmware before install." |
| **Pure Transfer** | RT claim | Document responsibility transfer | "Risk transferred to supplier per MSA-2023-001." |
| **Accept** | RT claim | Document justification for retaining risk | "Attack requires physical access during 2-minute window." |

**Key Rule**: If you are DOING something to change the system or lower risk → Create CSG. If you are only retaining risk or assigning responsibility → Keep the claim in `data/rt.md`.

---

## M:N Mapping Scenarios

### Scenario 1: One Damage Scenario → Multiple Cybersecurity Goals

**Situation**: A single damage scenario affects multiple SFOP dimensions mapping to different CIA properties.

**Example**: DS-CAN-001 [EXAMPLE] "CAN Bus Message Injection"
- **Impact**: S=4 (steering compromise), O=3 (communication disruption)
- **SFOP → CIA**: S=4 → Integrity, O=3 → Availability

**Goals Derived**:
1. **CSG-CAN-001** (Integrity): "The CAN gateway shall validate message authenticity to prevent injection of unauthorized commands."
2. **CSG-CAN-002** (Availability): "The CAN gateway shall detect and mitigate message flooding to maintain bus availability."

**Rationale**: Integrity goal addresses safety impact (corrupted commands), Availability goal addresses operational impact (DoS on communication).

---

### Scenario 2: Multiple Damage Scenarios → One Cybersecurity Goal

**Situation**: Several damage scenarios can be prevented by a single, broadly-scoped goal.

**Example**: DS-IVI-001 [EXAMPLE] (Location Tracking) + DS-IVI-002 [EXAMPLE] (Personal Data Exposure)
- Both address **Privacy (P)** via **Confidentiality (C)**
- Both involve unauthorized access to user data

**Goal Derived**:
- **CSG-IVI-001** (Confidentiality): "The infotainment system shall protect personal data from unauthorized disclosure."

**Rationale**: Single access control goal addresses multiple data exposure scenarios.

**Important**: Only consolidate goals when they share the SAME CIA property and the SAME mitigation approach. Do NOT over-generalize ("The vehicle shall be secure").

---

### Scenario 3: Chain of Damage Scenarios → Layered Goals

**Situation**: Attack chain progresses through multiple damage scenarios with escalating impact.

**Example**: 
- DS-IVI-003 [EXAMPLE] (Infotainment compromise, Impact=2) → 
- DS-CAN-002 [EXAMPLE] (CAN gateway breach, Impact=3) → 
- DS-CAN-001 [EXAMPLE] (Safety ECU control, Impact=4)

**Goals Derived** (defense-in-depth):
1. **CSG-IVI-002** (Integrity): "The head unit shall verify firmware authenticity to prevent malicious code execution."
2. **CSG-CAN-003** (Integrity): "The CAN gateway shall isolate infotainment domain from safety-critical CAN buses."
3. **CSG-CAN-001** (Integrity): "The steering ECU shall validate CAN message authenticity to prevent unauthorized commands."

**Rationale**: Layered goals provide defense-in-depth. If one control fails, subsequent layers still protect.

---

### Scenario 4: Damage Scenario + Mixed Treatments → Goal + RT Claim

**Situation**: High-impact damage scenario with partial mitigation (Reduce) but some residual risk accepted.

**Example**: DS-ADAS-001 [EXAMPLE] "Camera Sensor Spoofing"
- **Impact**: S=3, O=2 (RV 4)
- **Treatment**: Reduce (implement sensor fusion) + partial Accept (cannot eliminate all spoofing vectors)

**Outputs**:
1. **CSG-ADAS-001** (Integrity): "The ADAS ECU shall validate sensor data consistency across multiple sources to detect spoofing attempts."
2. **RT-owned Claim**: "Acme Automotive accepts residual risk of advanced adversarial spoofing using projected images undetectable by current sensor fusion algorithms. Mitigation requires next-generation lidar sensors planned for 2026 model year. CISO approval: 2024-10-01."

**Rationale**: Goal addresses what CAN be mitigated (basic spoofing via sensor fusion). Claim documents what CANNOT be mitigated with current technology.

---

## Goal Statement Templates by CIA Property

### Confidentiality Goal Templates

**Data Protection Pattern**:
```
The [COMPONENT] shall protect [DATA TYPE] to prevent unauthorized disclosure.
```

**Access Control Pattern**:
```
The [COMPONENT] shall restrict [DATA/FUNCTION] access to authorized [USERS/SYSTEMS].
```

**Privacy-Specific Pattern**:
```
The [COMPONENT] shall minimize collection of [PII TYPE] to prevent privacy violations.
```

**Examples**:
- "The connected services platform shall protect location data in transit and at rest from unauthorized tracking."
- "The backend API shall authenticate all user requests to prevent unauthorized vehicle access."
- "The head unit shall anonymize diagnostic telemetry to prevent driver identification."

---

### Integrity Goal Templates

**Validation Pattern**:
```
The [COMPONENT] shall validate [DATA/MESSAGE] authenticity to prevent [ATTACK TYPE].
```

**Tamper Detection Pattern**:
```
The [COMPONENT] shall detect unauthorized modifications to [FIRMWARE/DATA] to maintain system integrity.
```

**Functional Correctness Pattern**:
```
The [COMPONENT] shall maintain [FUNCTION] correctness to prevent [SAFETY/OPERATIONAL IMPACT].
```

**Examples**:
- "The CAN gateway shall validate message authenticity to prevent injection of malicious commands."
- "The boot loader shall verify firmware signatures to prevent installation of unauthorized software."
- "The ADAS ECU shall detect sensor data manipulation to prevent false obstacle detection."

---

### Availability Goal Templates

**Service Continuity Pattern**:
```
The [COMPONENT] shall maintain [SERVICE/FUNCTION] availability during [ATTACK/FAILURE CONDITION].
```

**DoS Resistance Pattern**:
```
The [COMPONENT] shall resist denial-of-service attacks to ensure [CRITICAL FUNCTION] remains operational.
```

**Recovery Pattern**:
```
The [COMPONENT] shall recover from [FAILURE TYPE] within [TIME CONSTRAINT] to maintain [SERVICE LEVEL].
```

**Examples**:
- "The telematics control unit shall resist network flooding attacks to maintain emergency call (eCall) availability."
- "The immobilizer system shall remain operational during unauthorized access attempts to prevent vehicle theft."
- "The ADAS ECU shall detect sensor failures and transition to safe degraded mode within 100ms to maintain operational safety."

---

## Common Pitfalls and Best Practices

### ❌ DON'T: Specify Implementation Details in Goals

**Wrong**: "The system shall use AES-256-GCM encryption with PBKDF2 key derivation (100,000 iterations)."

**Right**: "The system shall protect stored credentials to prevent unauthorized access."

**Rationale**: Goals define WHAT, not HOW. Implementation details belong in Cybersecurity Requirements (CSR).

---

### ❌ DON'T: Create Overly Generic Goals

**Wrong**: "The vehicle shall be secure against all cyber attacks."

**Right**: "The CAN gateway shall validate message authenticity to prevent unauthorized command injection."

**Rationale**: Goals must be specific, testable, and traceable to damage scenarios.

---

### ❌ DON'T: Derive Goals from Threat Scenarios

**Wrong**: "The system shall prevent SQL injection attacks." (threat-centric)

**Right**: "The backend database shall validate input parameters to prevent unauthorized data access." (damage-centric)

**Rationale**: Goals address DAMAGE (harm that occurs), not THREATS (attack methods). Multiple threats may cause the same damage.

---

### ❌ DON'T: Conflate Goals and Requirements

**Goal (High-Level, WHAT)**: "The infotainment system shall authenticate user requests to prevent unauthorized vehicle control."

**Requirement (Low-Level, HOW)**: "The infotainment API shall implement OAuth 2.0 authorization with JWT tokens having maximum 1-hour validity."

**Rationale**: Goals are technology-agnostic and stable across product generations. Requirements are specific and may change as technology evolves.

---

### ✅ DO: Create Separate Goals for Each CIA Property

**Example**: DS-IMM-001 [EXAMPLE] "Ransomware Immobilization"
- Impact: S=2, F=3, O=4 → Multiple SFOP dimensions affected

**Separate Goals**:
1. **CSG-IMM-001** (Availability): "The immobilizer system shall maintain startup functionality during software failures."
2. **CSG-IMM-002** (Integrity): "The immobilizer system shall detect unauthorized firmware modifications."

**Rationale**: Different CIA properties require different verification methods and may have different implementation priorities.

---

### ✅ DO: Link Goals to Specific Components

**Wrong**: "The vehicle shall protect location data." (too broad)

**Right**: "The telematics control unit shall protect location data." (specific component)

**Rationale**: Goals must be assignable to development teams and testable at component integration. "The vehicle" is not a verifiable test scope.

---

### ✅ DO: Use Active Voice with "Shall"

**Wrong**: "Location data should be protected." (passive, non-normative)

**Right**: "The telematics control unit shall protect location data." (active, normative)

**Rationale**: ISO standards require normative language. "Shall" indicates mandatory requirement; "should" indicates recommendation.

---

### ✅ DO: Verify Goal Against Damage Scenario

**Checklist**:
- ✅ Does the goal, if achieved, prevent or mitigate the damage scenario?
- ✅ Is the CIA property consistent with the SFOP dimensions affected?
- ✅ Would verification of this goal provide evidence that the risk is reduced?

**Example Verification**:
- **DS-IVI-001 [EXAMPLE]**: Unauthorized location tracking (P=4)
- **CSG-IVI-001**: "The telematics control unit shall restrict access to location data."
- ✅ If access is restricted → tracking is prevented → goal addresses damage

---

## Quick Reference

### 5-Step Methodology Summary

1. **Read DS** → Identify SFOP dimensions with score ≥ 2
2. **Read RT** → If Avoid/Reduce → Continue; if Transfer includes mitigation → Continue; if pure Accept/pure Transfer → keep claim in `data/rt.md`
3. **Formulate Goal** → Write SHALL statement addressing impact
4. **Assign CIA** → Classify as Confidentiality, Integrity, or Availability
5. **Review RT claim** (if needed) → Ensure `data/rt.md` contains risk statement + justification + residual risk acknowledgment

### SFOP → CIA Mapping

| SFOP | CIA | Typical Goal Focus |
|------|-----|-------------------|
| Safety (S) | I or A | Maintain correct/available safety functions |
| Financial (F) | C or I | Protect data/prevent unauthorized transactions |
| Operational (O) | A or I | Ensure service availability/functional correctness |
| Privacy (P) | C | Protect personal data from disclosure |

### Treatment → Output Artifact

| Treatment | Output | When to Create |
|-----------|--------|---------------|
| Avoid | CSG (Goal) | Define WHAT to eliminate |
| Reduce | CSG (Goal) | Define WHAT to protect |
| Transfer + mitigation | CSG + RT claim | Define WHAT to protect and keep responsibility in RT |
| Pure Transfer | RT claim | Document responsibility transfer |
| Accept | RT claim | Justify retained risk |

### Goal Quality Checklist

- ✅ Uses "shall" (normative)
- ✅ Identifies specific component
- ✅ States WHAT, not HOW
- ✅ Verifiable and testable
- ✅ Addresses damage scenario
- ✅ Technology-agnostic

### RT Claim Review Checklist

1. **Risk Statement** present in `data/rt.md`
2. **Justification** present in `data/rt.md`
3. **Approval / review metadata** present in `data/rt.md`

---

## References

- **ISO 21434:2021** - Road vehicles — Cybersecurity engineering
  - Clause 9: Concept / cybersecurity concept phase
  - Clause 8.5: Cybersecurity claims
  - Clause 15.9: Cybersecurity goals and cybersecurity requirements
- **ISO 31000:2018** - Risk management guidelines (treatment options)
- **ISO 26262** - Functional safety (safety goal patterns)
- **GDPR** (EU 2016/679) - Privacy impact considerations
- **UN R155** - Cyber Security Management System (regulatory requirements)

---

## Appendix: CIA Property Examples

### Confidentiality Examples

| Asset | Goal | Damage Prevented |
|-------|------|------------------|
| Location Data | "The telematics system shall protect location data confidentiality." | DS-IVI-001 [EXAMPLE] Location tracking |
| Payment Credentials | "The head unit shall protect stored payment data." | DS-IVI-004 [EXAMPLE] Payment card theft |
| Cryptographic Keys | "The secure element shall prevent extraction of private keys." | DS-EXT-003 [EXAMPLE] Key compromise |

### Integrity Examples

| Asset | Goal | Damage Prevented |
|-------|------|------------------|
| CAN Messages | "The gateway shall validate message authenticity." | DS-CAN-001 [EXAMPLE] Command injection |
| Firmware | "The bootloader shall verify firmware signatures." | DS-IVI-002 [EXAMPLE] Malicious code execution |
| Sensor Data | "The ADAS ECU shall detect sensor data manipulation." | DS-ADAS-001 [EXAMPLE] False obstacle detection |

### Availability Examples

| Asset | Goal | Damage Prevented |
|-------|------|------------------|
| Telematics | "The TCU shall resist DoS attacks." | DS-BCK-002 [EXAMPLE] Service outage |
| Immobilizer | "The immobilizer shall remain operational." | DS-IMM-001 [EXAMPLE] Ransomware |
| ADAS | "The ADAS shall maintain safe degraded mode." | DS-ADAS-002 [EXAMPLE] Sensor failure |

---

*End of CSG Derivation Methodology Guide*
