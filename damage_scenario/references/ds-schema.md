# Damage Scenario Schema - ISO 21434 TARA

This document defines the required fields for damage scenario identification in ISO 21434 TARA (Threat Analysis and Risk Assessment) workflows.

---

## Required Fields

Every damage scenario in the DS catalogue must include ALL 7 required sections:

### 1. DS-ID

**Format**: `DS-[DOMAIN]-[NNN]`

**Description**: Unique identifier for the damage scenario following a structured naming convention based on the affected vehicle domain.

**Domain Codes**:
- `CAN` - CAN bus and in-vehicle networking
- `OTA` - Over-the-air updates and remote services
- `EXT` - External interfaces and physical access points
- `BCK` - Backend/cloud services and infrastructure
- `IVI` - Infotainment and in-vehicle information systems
- `IMM` - Immobilizer and vehicle access control
- `ADAS` - Advanced driver assistance systems

**Example**: `DS-IVI-001`, `DS-CAN-012`, `DS-ADAS-005`

**Rules**:
- Check existing IDs before assigning to avoid conflicts
- Use zero-padded 3-digit numbers (001, 002, ..., 999)
- Domain code must match the primary vehicle domain affected by the damage scenario
- If multiple domains are affected, choose the most critical domain for the ID

---

### 2. Title

**Format**: Human-readable text (maximum 80 characters)

**Description**: Concise, descriptive name for the damage scenario that clearly identifies the harm event.

**Example**: 
- "Unauthorized Vehicle Location Tracking"
- "Loss of Steering Control During Operation"
- "Driver Personal Data Exposure"
- "Unintended Emergency Braking Activation"

**Rules**:
- Focus on the HARM (what bad thing happens), not the attack method (how it happens)
- Use action-oriented language describing the damage
- Be specific enough to distinguish from similar damage scenarios
- Avoid technical jargon where possible; prioritize clarity
- Keep under 80 characters for readability

---

### 3. Linked Assets

**Format**: List of Asset IDs (AST-ID format) from the asset catalogue

**Description**: Identifies which assets, when their CIA properties are violated, could lead to this damage scenario. This establishes the many-to-many relationship between assets and damage scenarios.

**Example**:
```
Linked Assets:
- AST-ECU-001: Head Unit System-on-Chip (QAM8295)
- AST-DAT-001: Persistent Storage (UFS)
- AST-COM-003: Bluetooth/WiFi Module
```

**Rules**:
- Reference assets by their Asset ID from `data/asset_list.md`
- Include asset name after the ID for clarity
- List ALL assets whose CIA-property violation could cause this damage scenario
- One damage scenario can link to multiple assets (many-to-many relationship)
- One asset can contribute to multiple damage scenarios
- Explain the linkage: why does compromising this asset enable this damage?

**Relationship Clarification**:
- **Asset → Damage Scenario**: "If this asset's CIA properties are violated, these damage scenarios could occur"
- **Damage Scenario → Asset**: "This damage scenario can be realized by compromising these assets"

---

### 4. SFOP Dimensions

**Format**: List indicating which SFOP dimensions are affected

**Description**: Identifies which of the four damage categories (Safety, Financial, Operational, Privacy) are impacted by this damage scenario.

**SFOP Categories**:
- **Safety (S)**: Physical harm to vehicle occupants, pedestrians, or other road users
- **Financial (F)**: Monetary loss, liability, regulatory fines, or business impact
- **Operational (O)**: Vehicle function degradation, service disruption, or availability loss
- **Privacy (P)**: Unauthorized access to or disclosure of personal information

**Example**:
```
SFOP Dimensions Affected:
- Safety: Yes - Loss of steering control can lead to crashes
- Financial: Yes - Potential liability for injuries and property damage
- Operational: Yes - Vehicle becomes unsafe to operate
- Privacy: No - No personal data exposure in this scenario
```

**Rules**:
- Assess each dimension (S, F, O, P) independently
- Indicate "Yes" or "No" for each dimension with brief justification
- A damage scenario can affect one, multiple, or all four dimensions
- Focus on DIRECT impacts of the damage scenario (not secondary effects)
- See `references/sfop-guide.md` for detailed scoring criteria

---

### 5. Impact Score

**Format**: Numeric value from 1-4 using ISO 21434 impact scale

**Description**: The overall impact severity of this damage scenario, determined as the MAXIMUM score across all SFOP dimensions.

**Scale**:

| Level | Numeric | Description |
|-------|---------|-------------|
| Negligible | 1 | Minimal or no harm; minor inconvenience |
| Moderate | 2 | Limited harm; recoverable with minor effort |
| Severe | 3 | Significant harm; substantial recovery effort or injury |
| Critical | 4 | Catastrophic harm; fatalities, permanent disability, or business-threatening loss |

**Example**:
```
Impact Score: 4 (Critical)
- Safety: 4 (Critical) - Potential fatalities from loss of vehicle control
- Financial: 3 (Severe) - Major liability exposure
- Operational: 4 (Critical) - Complete loss of critical safety function
- Privacy: 1 (Negligible) - No personal data involved

Overall Impact: 4 (Critical) [max of S=4, F=3, O=4, P=1]
```

**Rules**:
- Overall impact score = MAX(Safety, Financial, Operational, Privacy)
- Document individual scores for each affected SFOP dimension
- Justify the score for each dimension in the Rationale field
- Use worst-case reasonable scenarios (not theoretical extremes)
- Safety impacts typically rate highest (3-4) due to potential for injury/death

---

### 6. Rationale

**Format**: Detailed text explanation (minimum 2-3 sentences per affected SFOP dimension)

**Description**: Comprehensive justification for the impact scores assigned to each SFOP dimension. Explains WHY this damage scenario has the assessed severity.

**Example**:
```
Rationale:

Safety (4 - Critical): Loss of steering control during highway driving at speeds above 80 km/h 
would make the vehicle uncontrollable, with high probability of collision resulting in fatalities 
or severe injuries to occupants and potentially other road users. This represents the highest 
safety impact category under ISO 21434.

Financial (3 - Severe): Liability exposure from injury crashes could result in multi-million 
dollar settlements and legal costs. Additionally, regulatory fines for safety violations and 
potential recall costs would impose major financial burden. Brand reputation damage would 
impact future sales.

Operational (4 - Critical): Steering is a critical vehicle function required for safe operation. 
Complete loss of steering renders the vehicle inoperable and unsafe, meeting the definition of 
Critical operational impact.

Privacy (1 - Negligible): This damage scenario does not involve access to or disclosure of 
personal information, so privacy impact is negligible.
```

**Rules**:
- Provide justification for EACH affected SFOP dimension (where score > 1)
- Minimum 2-3 sentences per dimension explaining the reasoning
- Reference specific consequences: injuries, costs, disruptions, data exposure
- Consider worst-case reasonable outcomes (not theoretical extremes)
- Cite regulatory requirements where relevant (ISO 26262, GDPR, GB 44495, etc.)
- Explain why the scenario rates at the assigned level vs. one level higher/lower

---

### 7. Assessment Context

**Format**: Structured bullet list capturing assumptions and evidence used to score SFOP.

**Description**: Records the context needed to reproduce and audit the impact assessment without introducing threat-path details. Assessment Context explains the conditions under which the harm is evaluated.

**Example**:
```
Assessment Context:
- Affected Function / Function Cluster: Navigation route guidance and location services
- Function Risk Statement: The vehicle continues to deliver navigation with privacy risk because location history can be observed by unauthorized parties
- Assumptions: Location data is linked to driver accounts and stored for 90 days
- Operating Conditions: Normal driving and parked states
- Population / Scale: Fleet-scale exposure, 10,000+ users
- Duration / Recoverability: Continuous exposure until software/data-handling remediation
- Evidence / Source: AST-SNS-001, AST-DAT-001, stakeholder interview, GDPR/GB 44495 rationale
```

**Rules**:
- Record the affected vehicle-level function or function cluster. If no function is affected, reconsider whether the DS is in scope.
- Record the Function with RISK statement: what risky, unavailable, malformed, or privacy-invasive function reaches the road user or stakeholder.
- Include architecture or stakeholder assumptions that materially affect scoring
- Record operating conditions such as parked, low speed, highway, ADAS mode, charging, or service mode
- Record affected population or fleet scale when Privacy or Financial scores depend on scale
- Record duration and recovery path when Operational or Financial scores depend on recoverability
- Record evidence/source references such as asset IDs, interview notes, regulations, or architecture notes
- Do not include attack paths, vulnerabilities, exploit steps, or AFR details

---

## Damage Scenario vs. Threat Scenario

**Important Distinction**:

| Damage Scenario (DS) | Threat Scenario (TS) |
|---------------------|---------------------|
| Describes the HARM that occurs | Describes the ATTACK that causes harm |
| "What bad thing happens?" | "How does the attacker make it happen?" |
| Focused on consequences and impact | Focused on attack path and feasibility |
| Example: "Loss of steering control" | Example: "Attacker injects CAN messages to disable steering ECU" |
| Assessed with SFOP (impact) | Assessed with AFR (attack feasibility) |
| ISO 21434 Clause 15.4-15.5 | ISO 21434 Clause 15.6-15.8 |

**This skill (damage_scenario) focuses ONLY on DS**. Per-project threat scenarios (TS) and attack feasibility (AFR) are handled by the separate `threat_scenario` skill. If `tara-maker` is used as a reusable threat library, treat it as a reference source rather than the owner of `data/ts.md`.

---

## Domain Definitions

| Domain Code | Domain Name | Description | Example Damage Scenarios |
|-------------|-------------|-------------|-------------------------|
| **CAN** | CAN Bus & Networking | In-vehicle networks (CAN, LIN, FlexRay, Ethernet) | Unintended vehicle behavior, network communication unavailable, ECU isolation |
| **OTA** | Over-The-Air Updates | Remote software updates and diagnostics | Firmware integrity loss, update failure |
| **EXT** | External Interfaces | Physical access points (USB, OBD-II, charging) | Unsafe vehicle configuration change, unauthorized service mode |
| **BCK** | Backend/Cloud | Remote services, cloud infrastructure, APIs | Account takeover, service denial, data breach |
| **IVI** | Infotainment | Head unit, displays, entertainment, connectivity | Privacy violation, display manipulation |
| **IMM** | Immobilizer | Vehicle access control, keyless entry, anti-theft | Unauthorized vehicle access, theft |
| **ADAS** | ADAS/Autonomous | Automated driving, ADAS features, sensors | Incorrect environment perception, unintended acceleration/braking |

---

## CIA → SFOP Relationship

Damage scenario candidates are prompted by analyzing what happens when an asset's CIA (Confidentiality, Integrity, Availability) properties are violated. CIA ratings are triage signals, not final SFOP scores: the final Safety, Financial, Operational, and Privacy scores must be based on the concrete harm context, assumptions, operating conditions, affected scale, and recovery path.

| Asset CIA Property | Typical SFOP Impact |
|-------------------|---------------------|
| **High Confidentiality** (C=3 or C=4) | → Privacy (P) damage: Data exposure, tracking |
| **High Integrity** (I=3 or I=4) | → Safety (S) + Operational (O) damage: Function corruption, unsafe behavior |
| **High Availability** (A=3 or A=4) | → Operational (O) + Safety (S) damage: Service denial, function loss |

**Example Mapping**:
- Asset: `AST-ECU-001` with CIA rating `C:3 / I:4 / A:3`
  - High Confidentiality (C=3) → Damage scenario involving Privacy (P): User data exposure
  - High Integrity (I=4) → Candidate damage scenario involving Safety (S): Unintended vehicle behavior
  - High Availability (A=3) → Candidate damage scenario involving Operational (O): System unavailability or degraded service

---

## Example Damage Scenario Entry

```markdown
### DS-IVI-001: Unauthorized Driver Location Tracking

**Linked Assets**:
- AST-ECU-001: Head Unit System-on-Chip (QAM8295)
- AST-SNS-001: GNSS Receiver
- AST-DAT-001: Persistent Storage (UFS)
- AST-COM-005: Cellular/Telematics Link

**SFOP Dimensions Affected**:
- Safety: No - Location tracking does not cause physical harm
- Financial: Yes - GDPR/GB 44495 violation fines (up to 4% annual revenue)
- Operational: No - Vehicle functions remain available
- Privacy: Yes - Continuous monitoring of driver location and movement patterns

**Impact Score**: 4 (Critical)
- Safety: 1 (Negligible)
- Financial: 3 (Severe) - Major regulatory fines, class-action lawsuit risk
- Operational: 1 (Negligible)
- Privacy: 4 (Critical) - Persistent tracking of large user population

Overall Impact: 4 (Critical) [max of S=1, F=3, O=1, P=4]

**Assessment Context**:
- Affected Function / Function Cluster: Navigation and location-based services
- Function Risk Statement: The vehicle delivers location services with privacy risk because movement patterns can be exposed without authorization
- Assumptions: Location data is linked to driver accounts and retained long enough to reveal movement patterns
- Operating Conditions: Normal driving and parked states over an extended ownership period
- Population / Scale: Fleet-scale exposure, potentially 10,000+ users
- Duration / Recoverability: Continuous or repeated tracking until software and data-handling remediation
- Evidence / Source: AST-SNS-001, AST-DAT-001, AST-COM-005, stakeholder privacy assessment, GDPR/GB 44495 rationale

**Rationale**:

Safety (1 - Negligible): Real-time location tracking does not directly cause physical harm 
to vehicle occupants or other road users. There is no safety-critical function impact.

Financial (3 - Severe): Unauthorized location tracking violates GDPR Article 6 (lawful basis 
for processing) and China GB 44495 personal information protection requirements. Regulatory 
fines can reach 4% of annual global revenue for GDPR violations. Class-action lawsuits from 
affected users could result in significant settlement costs. Brand reputation damage would 
impact customer trust and future sales.

Operational (1 - Negligible): Vehicle operational functions (driving, navigation, infotainment) 
remain fully available. The damage scenario does not degrade vehicle performance or user experience 
from an operational perspective.

Privacy (4 - Critical): Continuous real-time tracking of driver location enables comprehensive 
surveillance of movement patterns, visited locations, daily routines, and associations with other 
individuals. This represents the highest privacy violation category, affecting potentially large 
user populations over extended time periods. Location data reveals highly sensitive information 
about personal life, work, health (hospital visits), religion (places of worship), and political 
activities.
```

---

## Quick Reference Table

| Field | Format | Example |
|-------|--------|---------|
| DS-ID | `DS-[DOMAIN]-[NNN]` | DS-IVI-001 |
| Title | Short harm description (max 80 chars) | Unauthorized Driver Location Tracking |
| Linked Assets | List of AST-IDs | AST-ECU-001, AST-SNS-001, AST-DAT-001 |
| SFOP Dimensions | S/F/O/P with Yes/No and brief explanation | Safety: No, Financial: Yes, Operational: No, Privacy: Yes |
| Impact Score | 1-4 (Negligible, Moderate, Severe, Critical) | 4 (Critical) |
| Assessment Context | Affected function, Function with RISK, assumptions, operating context, scale, duration, evidence | Navigation/location services delivered with privacy risk; fleet-scale tracking |
| Rationale | Detailed justification (2-3 sentences per dimension) | Privacy (4 - Critical): Continuous tracking... |

---

## Validation Checklist

Before finalizing a damage scenario entry, verify:

- [ ] DS-ID follows `DS-[DOMAIN]-[NNN]` format
- [ ] DS-ID is unique (no duplicates in the catalogue)
- [ ] Domain code is one of the 7 defined codes (CAN, OTA, EXT, BCK, IVI, IMM, ADAS)
- [ ] Title is clear, concise, and under 80 characters
- [ ] Title describes the HARM (not the attack method)
- [ ] Linked Assets lists all relevant AST-IDs from `data/asset_list.md`
- [ ] Assessment Context records affected function, Function with RISK, assumptions, operating conditions, scale, duration/recoverability, and evidence/source
- [ ] All four SFOP dimensions are assessed (Yes/No with justification)
- [ ] Impact Score is 1-4 and equals the MAX of individual SFOP scores
- [ ] Rationale provides 2-3 sentences for EACH affected SFOP dimension
- [ ] No threat scenario or attack method details (that's TS, not DS)
- [ ] No attack feasibility rating (that's AFR, later TARA step)
- [ ] No placeholder text remains (e.g., [TODO], [TBD])
