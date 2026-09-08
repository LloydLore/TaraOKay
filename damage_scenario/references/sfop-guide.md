# SFOP Scoring Guide - ISO 21434 Impact Assessment

This document provides detailed guidance for assessing damage scenario impacts using the SFOP (Safety, Financial, Operational, Privacy) framework defined in ISO 21434.

---

## Introduction

**SFOP** is a four-dimensional framework for assessing the impact of cybersecurity damage scenarios in automotive systems. Each dimension represents a different category of harm that can result when cybersecurity properties are violated:

- **S**afety: Physical harm to people
- **F**inancial: Monetary loss and liability
- **O**perational: Vehicle function degradation
- **P**rivacy: Personal data exposure

Under ISO 21434, each dimension is scored on a 4-level scale (1=Negligible, 2=Moderate, 3=Severe, 4=Critical). The **overall impact score** for a damage scenario is determined as the **MAXIMUM** value across all four dimensions.

---

## SFOP Scale Definition

### The 4-Level Impact Scale

| Level | Numeric | Label | General Description |
|-------|---------|-------|---------------------|
| 1 | 1 | **Negligible** | Minimal or no impact; minor inconvenience only |
| 2 | 2 | **Moderate** | Limited impact; recoverable with minor effort; no lasting harm |
| 3 | 3 | **Severe** | Significant impact; substantial recovery effort; serious harm |
| 4 | 4 | **Critical** | Catastrophic impact; irreversible harm; life-threatening |

**Important**: ISO 21434 uses a **1-4 scale** (not 0-3). Level 1 represents "Negligible" impact (not zero impact).

---

## Detailed SFOP Scoring Criteria

### Safety (S) - Physical Harm

**Question**: "What physical harm could occur to vehicle occupants, pedestrians, or other road users?"

| Score | Label | Criteria | Examples |
|-------|-------|----------|----------|
| **1** | **Negligible** | No injuries; no safety-critical function impact | Infotainment display glitch, radio malfunction, comfort feature failure |
| **2** | **Moderate** | Minor injuries possible; no hospitalization required; temporary discomfort | Hard braking (controlled), steering vibration, unexpected warning chimes |
| **3** | **Severe** | Severe or life-threatening injuries possible; hospitalization likely | Loss of braking, unintended acceleration, airbag suppression, steering failure at low speed |
| **4** | **Critical** | Fatalities or permanent disability highly likely | Loss of steering at highway speed, uncontrolled acceleration into traffic, brake failure on downhill grade |

**Safety Assessment Guidelines**:
- Consider worst-case reasonable scenarios (not theoretical extremes)
- Highway speeds (>80 km/h) generally elevate severity vs. parking lot speeds (<10 km/h)
- Safety-critical systems (steering, braking, powertrain) typically rate 3-4 when compromised
- ADAS failures may be 2-3 (driver expected to take over) unless complete automation
- ISO 26262 ASIL-D functions typically map to Safety score of 4 if compromised

---

### Financial (F) - Monetary Loss

**Question**: "What monetary losses, liability, or business impact could occur?"

| Score | Label | Criteria | Examples |
|-------|-------|----------|----------|
| **1** | **Negligible** | Minor financial loss; under $10,000; no liability | Single vehicle repair, localized service disruption, minor PR incident |
| **2** | **Moderate** | Moderate loss; $10,000-$1M; contained liability | Small-scale recall (<1,000 vehicles), regional service outage, moderate legal fees |
| **3** | **Severe** | Major financial loss; $1M-$100M; significant liability | Large recall (>10,000 vehicles), class-action lawsuit, major regulatory fine, brand damage |
| **4** | **Critical** | Catastrophic loss; >$100M; business-threatening | Fleet-wide recall, GDPR maximum penalty (4% revenue), fatal crash liability, bankruptcy risk |

**Financial Assessment Guidelines**:
- Include direct costs (repairs, recalls) + indirect costs (legal, regulatory, reputation)
- GDPR violations: Up to €20M or 4% of annual global revenue (whichever is higher)
- China GB 44495 violations: Up to ¥50M or 5% of previous year's turnover
- UN R155 violations: Type approval withdrawal (cannot sell vehicles)
- Class-action lawsuits for privacy violations can reach $100M+ settlements
- Brand reputation damage impacts future sales (quantify conservatively)

---

### Operational (O) - Function Degradation

**Question**: "What vehicle functions become unavailable or degraded?"

| Score | Label | Criteria | Examples |
|-------|-------|----------|----------|
| **1** | **Negligible** | Minor disruption; workaround readily available; no user impact | Single infotainment app crash, Bluetooth reconnection required, warning light displayed |
| **2** | **Moderate** | Significant disruption; service degraded but available; user inconvenience | Navigation loss, voice assistant offline, reduced charging speed, limited connectivity |
| **3** | **Severe** | Critical function unavailable; major user impact; vehicle usable but degraded | Complete infotainment failure, ADAS disabled, climate control inoperable, telematics offline |
| **4** | **Critical** | Complete loss of critical function; vehicle inoperable or unsafe to drive | Immobilization (vehicle won't start), loss of propulsion, transmission failure, battery drain |

**Operational Assessment Guidelines**:
- "Critical function" means required for vehicle drivability or legal compliance (e.g., eCall in EU)
- Distinguish between inconvenience (O=1-2) and inability to use vehicle (O=3-4)
- Consider duration: Temporary (seconds) vs. persistent (hours/days) vs. permanent (reflash required)
- Remote recovery (OTA fix) vs. requires service center visit affects severity
- Legal requirements: eCall, immobilizer, emissions monitoring must remain operational

---

### Privacy (P) - Personal Data Exposure

**Question**: "What personal information is disclosed, and how many people are affected?"

| Score | Label | Criteria | Examples |
|-------|-------|----------|----------|
| **1** | **Negligible** | Personal data of one individual; non-sensitive | Single user's radio presets, seat position, non-identifiable telemetry |
| **2** | **Moderate** | Personal data of a small group; limited sensitivity | Contact list of one user, recent destinations, music preferences for family vehicle |
| **3** | **Severe** | Sensitive data of many people; or highly sensitive data of few | Location history of 1,000+ users, biometric data (facial recognition), financial data, health data |
| **4** | **Critical** | Persistent tracking or sensitive data of large population (>10,000) | Real-time location tracking of entire fleet, credit card data of all users, large-scale surveillance |

**Privacy Assessment Guidelines**:
- **Sensitive data** includes: location, biometrics, health, financial, children's data, political/religious affiliation
- GDPR Article 9 "special categories" of data automatically rate P=3 or P=4
- Scale by population: 1 person (P=1), 10-100 people (P=2), 1,000+ people (P=3), 10,000+ people (P=4)
- Persistent/continuous exposure is worse than one-time exposure
- Re-identification risk: "Anonymized" data that can be de-anonymized rates higher
- Context matters: Home address alone (P=2), but home address + daily routine (P=3)

---

## Overall Impact Score Calculation

The overall impact score for a damage scenario is the **MAXIMUM** value across all four SFOP dimensions.

### Formula

```
Impact Score = MAX(Safety, Financial, Operational, Privacy)
```

### Examples

| Scenario | S | F | O | P | Overall Impact |
|----------|---|---|---|---|----------------|
| Infotainment display glitch | 1 | 1 | 1 | 1 | **1 (Negligible)** |
| Navigation data exposure (100 users) | 1 | 2 | 1 | 2 | **2 (Moderate)** |
| ADAS disabled (no crash) | 2 | 3 | 3 | 1 | **3 (Severe)** |
| Loss of steering at highway speed | 4 | 3 | 4 | 1 | **4 (Critical)** |
| Real-time location tracking (10,000 users) | 1 | 3 | 1 | 4 | **4 (Critical)** |

**Key Insight**: A damage scenario is rated by its WORST impact, not its average. Even if three dimensions are Negligible, a single Critical dimension makes the overall impact Critical.

---

## CIA → SFOP Triage Guidance

Damage scenario candidates are prompted by analyzing what happens when asset security properties (Confidentiality, Integrity, Availability) are violated. CIA is a triage input, not a scoring lookup table. Final SFOP ratings depend on the concrete harm statement, operating conditions, affected scale, duration, recoverability, stakeholder role, and regulatory market.

**Important cautions**:
- High Confidentiality does not automatically mean high Privacy; non-personal confidential data may primarily affect Financial or Operational impact.
- High Integrity does not automatically mean high Safety; the affected function must have a plausible path to physical harm in the stated operating context.
- High Availability does not automatically mean high Operational impact; function criticality, workaround availability, and recovery path determine severity.
- Use the mapping below to decide what questions to ask, then score each SFOP dimension independently.

### CIA to SFOP Triage Table

| Asset CIA Property | Violation Type | Typical SFOP Dimension(s) Affected | Rationale |
|-------------------|----------------|-----------------------------------|-----------|
| **Confidentiality (C)** | Data disclosure | **Privacy (P)** | Ask whether the data is personal, sensitive, large-scale, or continuously exposed |
| | | **Financial (F)** | Ask about regulatory fines, breach response, liability, and business impact |
| **Integrity (I)** | Data/function correctness loss | **Safety (S)** | Ask whether incorrect behavior can affect motion, warnings, ADAS, or driver decisions |
| | | **Operational (O)** | Ask which function becomes unreliable or degraded and whether a workaround exists |
| | | **Financial (F)** | Ask about recall, liability, warranty, and remediation costs |
| **Availability (A)** | Function or service unavailable | **Operational (O)** | Ask what function is unavailable, for how long, and how it recovers |
| | | **Safety (S)** | Ask whether unavailable safety-relevant functions increase crash or injury risk |
| | | **Financial (F)** | Ask about downtime, service disruption, warranty, recall, and lost revenue |

### Detailed Mapping Examples

#### High Confidentiality (C=3 or C=4) → Privacy + Financial

**Asset Example**: `AST-DAT-001` (Persistent Storage containing user data) with C=3
- **Violation**: Confidential data (location history, contacts) is disclosed
- **Primary SFOP Impact**: Privacy (P=3 or P=4) - Personal data exposure
- **Secondary SFOP Impact**: Financial (F=2 or F=3) - GDPR/GB 44495 fines

**Damage Scenario**: DS-IVI-001 "Unauthorized Driver Location Tracking"

---

#### High Integrity (I=3 or I=4) → Safety + Operational

**Asset Example**: `AST-ECU-001` (Head Unit SoC) with I=4
- **Violation**: Firmware is tampered with, installing malicious code
- **Primary SFOP Impact**: Safety (S=3 or S=4) - Could send unsafe CAN commands
- **Secondary SFOP Impact**: Operational (O=3 or O=4) - System malfunction
- **Tertiary SFOP Impact**: Financial (F=3) - Recall and liability

**Candidate Damage Scenario**: DS-CAN-001 "Unintended Vehicle Behavior During Operation"

---

#### High Availability (A=3 or A=4) → Operational + Safety

**Asset Example**: `AST-COM-001` (CAN-FD Bus) with A=3
- **Violation**: CAN bus is flooded/jammed, making it unavailable
- **Primary SFOP Impact**: Operational (O=3 or O=4) - Critical communications lost
- **Secondary SFOP Impact**: Safety (S=2 or S=3) - Safety functions may degrade
- **Tertiary SFOP Impact**: Financial (F=2) - Service disruption costs

**Candidate Damage Scenario**: DS-CAN-002 "Vehicle Network Communication Unavailable"

---

### CIA-SFOP Triage Quick Reference

| CIA Rating | Questions to Ask | Example Candidate Damage Scenario |
|------------|---------------------|------------------------|
| C=4, I=1, A=1 | Is the confidential data personal, regulated, or business-critical? | Cryptographic material disclosure |
| C=1, I=4, A=1 | Can incorrect function behavior affect motion, warnings, or ADAS? | Unintended vehicle behavior |
| C=1, I=1, A=4 | Which critical function is unavailable and how does recovery occur? | Critical vehicle service unavailable |
| C=3, I=3, A=2 | Are both data exposure and incorrect behavior plausible in this context? | Data exposure with service degradation |
| C=4, I=4, A=4 | Which concrete harms are distinct enough to document separately? | Multiple candidate DS entries requiring interview refinement |

---

## SFOP Scoring Examples

### Example 1: Infotainment Display Manipulation

**Damage Scenario**: DS-IVI-003 "False Warning Message Display"

**Assessment**:
- **Safety (1 - Negligible)**: False warning (e.g., "Low Tire Pressure") does not directly cause harm. Driver may check tires unnecessarily but no safety function is impaired.
- **Financial (1 - Negligible)**: Minimal cost impact. No recall required; software patch can fix issue remotely via OTA.
- **Operational (2 - Moderate)**: User experience degraded by false warnings. Display remains functional. Vehicle fully drivable.
- **Privacy (1 - Negligible)**: No personal data is exposed or accessed.

**Overall Impact**: **2 (Moderate)** [max of S=1, F=1, O=2, P=1]

---

### Example 2: ADAS Incorrect Environment Perception

**Damage Scenario**: DS-ADAS-001 "False Obstacle Detection Causing Emergency Braking"

**Assessment**:
- **Safety (3 - Severe)**: Unexpected emergency braking at highway speeds can cause rear-end collision from following vehicles. Occupant injury likely but modern safety systems (seatbelts, airbags) mitigate fatality risk in many cases.
- **Financial (3 - Severe)**: Liability for rear-end crashes caused by false braking. Potential recall if widespread. Legal defense costs substantial. Brand reputation damage.
- **Operational (2 - Moderate)**: ADAS function misoperates but vehicle remains drivable. Driver can disable ADAS and continue driving. Not a complete loss of function.
- **Privacy (1 - Negligible)**: No personal data involved in incorrect sensor/perception data.

**Overall Impact**: **3 (Severe)** [max of S=3, F=3, O=2, P=1]

---

### Example 3: Vehicle Immobilization

**Damage Scenario**: DS-IMM-001 "Vehicle Startup Prevented"

**Assessment**:
- **Safety (2 - Moderate)**: Vehicle cannot start, preventing driving. If immobilization occurs in dangerous location (highway, railroad crossing), occupants may be at risk. However, vehicle itself is not moving, limiting immediate crash risk.
- **Financial (3 - Severe)**: Large-scale vehicle startup prevention affecting a fleet could cost millions in recovery, service logistics, and lost productivity. OEM reputation damage significant.
- **Operational (4 - Critical)**: Complete loss of vehicle usability. Owner cannot drive until ransom paid or ECU reflashed at service center. Meets definition of Critical operational impact.
- **Privacy (1 - Negligible)**: Vehicle immobilization does not involve data disclosure by itself.

**Overall Impact**: **4 (Critical)** [max of S=2, F=3, O=4, P=1]

---

### Example 4: Continuous Location Tracking

**Damage Scenario**: DS-IVI-001 "Unauthorized Driver Location Tracking"

**Assessment**:
- **Safety (1 - Negligible)**: Location tracking is passive surveillance and does not directly cause physical harm to occupants.
- **Financial (3 - Severe)**: GDPR Article 6 violation (no lawful basis for processing). Maximum fine €20M or 4% annual revenue. Class-action lawsuit risk. Brand damage.
- **Operational (1 - Negligible)**: Vehicle functions normally. User may not even be aware of tracking. No service degradation.
- **Privacy (4 - Critical)**: Real-time, continuous location tracking of large user population (assume 10,000+ vehicles) over months reveals comprehensive life patterns. Meets definition of Critical privacy violation under GDPR Article 9 and ISO 21434.

**Overall Impact**: **4 (Critical)** [max of S=1, F=3, O=1, P=4]

---

## Assessment Workflow

### Step-by-Step Process

1. **Identify the Damage Scenario**: What is the harm that occurs (not the attack method)?

2. **Assess Each SFOP Dimension**:
   - Safety: Could this cause injury or death?
   - Financial: What are the monetary/liability consequences?
   - Operational: Does this degrade vehicle functions?
   - Privacy: Is personal data exposed?

3. **Assign Scores (1-4)** to each dimension using the criteria tables above

4. **Calculate Overall Impact**: MAX(S, F, O, P)

5. **Document Rationale**: Write 2-3 sentences justifying each score ≥ 2

6. **Review Against CIA**: Does the SFOP profile make sense given the asset's CIA ratings?

---

## Common Pitfalls

### ❌ DON'T: Confuse Damage Scenario with Threat Scenario
- **Wrong**: "Attacker injects CAN messages" (that's a threat scenario)
- **Right**: "Loss of steering control" (that's a damage scenario)

### ❌ DON'T: Include Attack Feasibility in Impact Score
- Impact score is about CONSEQUENCE (how bad is the harm)
- Attack feasibility (AFR) is separate and comes later in TARA
- Don't reduce impact score just because attack is "hard to execute"

### ❌ DON'T: Use 0-3 Scale
- ISO 21434 uses **1-4 scale** (1=Negligible, 4=Critical)
- There is no "zero impact" level

### ❌ DON'T: Average the SFOP Scores
- Overall impact = **MAX**, not average
- A single Critical dimension makes the overall impact Critical

### ✅ DO: Consider Worst-Case Reasonable Scenarios
- Not theoretical extremes ("asteroid hits vehicle")
- Not overly optimistic ("user always pays attention")
- Reasonable worst-case given the damage scenario

### ✅ DO: Reference Regulations in Rationale
- GDPR, GB 44495, UN R155, ISO 26262, eCall requirements
- Strengthens justification and shows compliance awareness

---

## Quick Reference

### SFOP Dimension Summary

| Dimension | Focus | Scale Extremes |
|-----------|-------|----------------|
| **Safety (S)** | Physical harm | 1: No injury ↔ 4: Fatalities |
| **Financial (F)** | Monetary loss | 1: <$10K ↔ 4: >$100M |
| **Operational (O)** | Function loss | 1: Minor glitch ↔ 4: Immobilized |
| **Privacy (P)** | Data exposure | 1: 1 person ↔ 4: Large population |

### Overall Impact Formula

```
Impact = MAX(Safety, Financial, Operational, Privacy)
```

### CIA → SFOP Typical Mappings

- **C** violation → **P** (Privacy) + **F** (Financial)
- **I** violation → **S** (Safety) + **O** (Operational)
- **A** violation → **O** (Operational) + **S** (Safety)

---

## References

- **ISO 21434:2021** - Road vehicles — Cybersecurity engineering (Clause 15.4-15.5: Impact rating)
- **ISO 26262** - Road vehicles — Functional safety (ASIL ratings inform safety impact)
- **GDPR** (EU 2016/679) - General Data Protection Regulation (Privacy impact, fines)
- **China GB 44495** - Personal Information Protection (Privacy requirements)
- **UN R155** - Cyber Security and Cyber Security Management System (Type approval requirements)
