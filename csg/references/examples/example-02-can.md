# Cybersecurity Goal Example 02 - CAN Domain

This example demonstrates cybersecurity goal derivation for a safety-critical CAN bus threat scenario, following the CSG methodology used in the ISO 21434 TARA workflow.

---

## CSG-CAN-01: CAN Bus Message Integrity Goal

**CSG-ID**: CSG-CAN-01

**Title**: CAN Bus Message Integrity and Authenticity Goal

**Related DS-IDs**:
- DS-CAN-001 [EXAMPLE] (Malicious CAN Message Injection Enabling Unintended Vehicle Behavior)

**Related RT-IDs**: 
- [TBD] Risk treatment to be determined in risk treatment cycle

**Goal Statement**:
The vehicle CAN bus architecture shall ensure that messages controlling critical driving functions (steering, braking, acceleration, suspension) can only originate from authenticated and authorized ECUs. The system shall detect and reject malicious, spoofed, or tampered CAN messages that could affect vehicle motion control or safety-critical operations.

**CIA Property**: Integrity

**Cybersecurity Claim**: 

**Rationale**:
Malicious CAN message injection could override legitimate ECU commands and cause unintended vehicle acceleration, braking, steering angle changes, or disabling of safety functions, creating risk of collision and vehicle occupant fatalities (DS-CAN-001 [EXAMPLE] with Safety Impact=4 Critical). Message authentication and validation are mandatory under ISO 26262 functional safety requirements for ASIL-D failure modes and UN R155 Annex 5 Part A vehicle network protection. This cybersecurity goal ensures CAN message integrity to prevent safety harm documented in DS-CAN-001 [EXAMPLE].

**Last Updated**: 2026-03-20

---

## Derivation Methodology Walkthrough

### Step 1: Read Damage Scenario → Identify SFOP Dimensions

**Damage Scenario**: DS-CAN-001 [EXAMPLE] (Malicious CAN Message Injection)

**SFOP Analysis**:
- **Safety**: 4 (Critical) ✅ → Loss of vehicle control at highway speeds, ASIL-D failure
- **Financial**: 3 (Severe) ✅ → Liability for crashes, mandatory recall, UN R155 regulatory fines
- **Operational**: 3 (Severe) ✅ → Critical safety functions compromised
- **Privacy**: 1 (Negligible) ❌ → CAN messages contain operational data, not PII

**Impact Drivers**: Safety, Financial, Operational (scores ≥ 2)

---

### Step 2: Read Risk Treatment → Determine CSG Requirement

**Risk Treatment Decision** (from risk assessment): Reduce (mandatory for safety-critical risks)

**CSG Required?**: ✅ **Yes**

**Rationale**: Reduce treatment means implementing security controls to lower risk below acceptable threshold. Cybersecurity goals define WHAT these controls must achieve. For safety-critical risks with Impact=4, the treatment decision is mandatory mitigation (Reduce), not acceptance or transfer. Therefore, a CSG is required to specify the security objective.

---

### Step 3: Formulate Goal Statement → Address Impact Dimensions

**Impact-to-Goal Mapping**:

From csg-guide.md SFOP-CIA mapping:
- **Safety (S=4)** → **Integrity** - Prevent corruption of safety-critical CAN messages
- **Operational (O=3)** may also justify a separate **Availability** CSG if bus continuity is in scope

**Goal Statement Template Applied**:
```
The [COMPONENT] shall [PROTECTION ACTION] to [PREVENT/MITIGATE] [DAMAGE SCENARIO].
```

**Filled Template**:
```
The vehicle CAN bus architecture shall ensure that messages controlling critical driving functions 
can only originate from authenticated and authorized ECUs. The system shall detect and reject malicious 
or tampered CAN messages that could affect vehicle motion control.
```

**Quality Verification**:
- ✅ Uses "shall" (normative, ISO-compliant)
- ✅ Identifies specific component (CAN bus, ECUs)
- ✅ States WHAT (message authentication), not HOW (technology-agnostic, not implementation-specific protocols)
- ✅ Addresses damage scenario (injection attack prevention)
- ✅ Verifiable (can test whether only authenticated ECUs send critical messages)
- ✅ Flexible implementation (applies to any industry-standard authentication mechanism)

---

### Step 4: Assign CIA Property

**CIA Decision Tree Applied**:

```
Q1: Does goal address DATA DISCLOSURE?
    └─ No, message injection is about tampering, not disclosure

Q2: Does goal address DATA/FUNCTION TAMPERING?
    └─ YES → Integrity
    └─ CAN messages are data structures
    └─ Injection attempts unauthorized modification
    └─ Goal requires validation and authentication

Q3: Does goal also expose a separate SERVICE AVAILABILITY concern?
    └─ YES → Capture that in a separate Availability CSG if bus continuity is in scope
```

**CIA Assignment**: **Integrity**

**Why Integrity Gets Its Own CSG**:
- The root security property is message authenticity and tamper detection
- Without integrity, injected messages are accepted as legitimate
- Availability concerns should be represented by a separate CSG if the project needs one

---

### Step 5: Confirm No RT Claim Is Needed for Reduce

**Treatment Decision**: Reduce

**RT Claim Required?**: ❌ **No**

**Rationale**: Reduce treatments implement security controls to mitigate risk. Cybersecurity claims are only required for Accept treatments (residual risk) or Transfer treatments (third-party responsibility). For Reduce treatments, the CSG itself documents the security objective. No claim is needed.

**Cybersecurity Claim Field**: [EMPTY]

---

## Real-World Context and Standards

### UN R155 Compliance

UN Regulation No. 155 (Cybersecurity and Software Updates) mandates:

**Clause 7.2.4.1**: "Protection against manipulation of vehicle communication networks"
- Vehicles must implement protection mechanisms to ensure CAN bus messages are not tampered with
- Industry-standard authentication mechanisms are required

**Clause 7.3.1**: "Risk treatment for identified threats"
- Cybersecurity goals must be formulated for all threats requiring mitigation
- Security controls implementing these goals must be documented and validated

### Industry Standards

Various industry standards exist for CAN message authentication. CSG goals remain technology-agnostic to allow selection based on system requirements.

### ISO 26262 Functional Safety Alignment

This CSG aligns with ISO 26262 (Functional Safety) requirements:

**ASIL-D Failures**:
- Malicious CAN message injection maps to ASIL-D (highest severity) failures
- Loss of vehicle control due to safety function corruption = life-threatening risk
- Functional safety standards mandate hazard mitigation for ASIL-D

**Integrity Analysis**:
- ISO 26262 Part 5 requires analysis of ECU communication integrity
- Message authentication is a standard control for CAN communication
- Goal Statement provides the verifiable objective for integrity controls

---

## Key Takeaways

### 1. Safety-Critical Risks Require Integrity Goals

For damages affecting safety (SFOP-S ≥ 2), the corresponding cybersecurity goal often starts with an **Integrity** CSG. Malicious CAN message injection is a classic integrity threat because the attacker modifies messages rather than merely disclosing them.

**Why Integrity Gets Its Own CSG**:
- Safety depends on correct execution of control commands
- Injected (modified) messages produce incorrect vehicle behavior
- Message authentication prevents unauthorized modification

### 2. Why Reduce Treatment is Mandatory (Not Accept)

For RV 5 safety-critical risks:
- **Accept** treatment (ignoring the risk) is prohibited under ISO 26262 and UN R155
- **Transfer** treatment (delegating to suppliers) is complementary but does not eliminate OEM liability
- **Reduce** treatment (implementing security controls) is mandatory

**Business Implication**: You cannot ignore RV 5 safety risks through insurance or supplier contracts alone. Security controls must be implemented and validated.

### 3. Availability Requires a Separate Goal When Needed

Availability can matter here because:
- Message flooding DoS attacks disrupt CAN bus availability
- Jamming attacks prevent legitimate messages from being transmitted
- Defense-in-depth must address both tampering and denial of service

Under policy A, that availability concern becomes a separate CSG with `CIA Property: Availability` rather than a secondary property inside this entry.

### 4. No Cybersecurity Claim for Reduce Treatment

The Cybersecurity Claim field is left **empty** because:
- Claim records live in `data/rt.md`
- Reduce treatment means implementing controls (not accepting residual risk)
- The CSG itself documents the active security objective
- If the project later accepts or transfers residual risk, that approval stays with the RT entry

**If this later gained an Accept or pure Transfer decision**, the claim would be documented in `data/rt.md` rather than added to this CSG entry.

### 5. Goal Statement Remains Technology-Agnostic

This CSG does NOT mandate specific implementation technologies:
- Goal: "messages can only originate from authenticated and authorized ECUs"
- Implementation options are flexible and can be selected based on system architecture
- Different vehicle manufacturers can use different authentication approaches

**Why Technology-Agnostic?**:
- Goals are stable across product generations
- Implementation technology evolves and should not be locked by CSG
- Different vehicle architectures may require different approaches
- CSG provides traceability to CSR (cybersecurity requirements) which specifies implementation

---

## M:N Mapping Context

This CSG demonstrates a **1:1 mapping** in this example (one CSG ↔ one DS):

```
DS-CAN-001 [EXAMPLE] (Malicious CAN Message Injection)
     ↓
CSG-CAN-01 [EXAMPLE] (CAN Bus Message Integrity Goal)
     ↓
RT-CAN-001 [TBD] (Reduce via Gateway Filtering)
     ↓
[CSR derivation is a separate skill - out of scope for CSG]
```

However, in complex scenarios:
- **Multiple DS per CSG**: If DS-CAN-002 [EXAMPLE] (DoS) and DS-CAN-003 [EXAMPLE] (Gateway Bypass) also require integrity protection, CSG-CAN-01 might address all three
- **Multiple CSG per DS**: If DS-CAN-001 [EXAMPLE] requires both integrity AND availability controls, CSG-CAN-01 (Integrity) and CSG-CAN-02 (Availability) would both address the same DS

---

## Note on Cybersecurity Requirements (CSR)

Once this CSG is approved, cybersecurity requirements (CSR) are derived to specify HOW to achieve the goal. **CSR derivation is a separate skill** (out of scope for this CSG skill).

**Key Distinction**:
- **CSG (this skill)**: Defines WHAT must be protected (e.g., "messages can only originate from authenticated ECUs")
- **CSR (separate skill)**: Specifies HOW to protect (e.g., specific algorithms, protocols, performance requirements)

This skill focuses ONLY on the goal layer. Requirements derivation will be covered in a dedicated CSR skill.

---

## Cross-References

**Related Documentation**:
- **CSG Schema**: `skills/csg/references/csg-schema.md` (9-field definition)
- **CSG Methodology**: `skills/csg/references/csg-guide.md` (5-step derivation process)
- **Damage Scenario**: `data/ds.md` → DS-CAN-001 [EXAMPLE] (Impact=4 Critical)
- **Risk Treatment Example**: `skills/risk_treatment/references/examples/example-02-can.md` (RT-CAN-001 details)
- **UN R155**: Regulation on cybersecurity type approval (Clause 7.2.4.1)
- **ISO 26262**: Functional safety standard (ASIL-D requirements)

---

**Document Version**: 1.0  
**Created**: 2026-03-20  
**Status**: Example (For CSG Skill Training)
