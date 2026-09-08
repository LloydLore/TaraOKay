# Damage Scenario Template

Use this template to document each damage scenario. Copy this structure and fill in all 7 required sections.

---

### DS-[DOMAIN]-[NNN]: [Damage Scenario Title]
<!-- 
  DS-ID Format: DS-[DOMAIN]-[NNN]
  Domain codes: CAN | OTA | EXT | BCK | IVI | IMM | ADAS
  Number: 3-digit zero-padded (001, 002, ..., 999)
  
  Domain Definitions:
  - CAN: CAN bus and in-vehicle networking
  - OTA: Over-the-air updates and remote services  
  - EXT: External interfaces and physical access points
  - BCK: Backend/cloud services and infrastructure
  - IVI: Infotainment and in-vehicle information systems
  - IMM: Immobilizer and vehicle access control
  - ADAS: Advanced driver assistance systems
  
  Examples:
  - DS-IVI-001: Unauthorized Driver Location Tracking
  - DS-CAN-001: Vehicle Network Communication Unavailable
  - DS-ADAS-001: False Obstacle Detection Causing Emergency Braking
  - DS-IMM-001: Vehicle Startup Prevented
  - DS-EXT-001: Unsafe Vehicle Configuration Change
  - DS-BCK-001: Unauthorized Remote Command Availability
  - DS-OTA-001: Firmware Integrity Loss During Update
-->

**Linked Assets**:
<!-- 
  List all assets from data/asset_list.md whose CIA violation could lead to this damage scenario.
  Format: AST-ID: Asset Name (one per line)
  
  Example:
  - AST-ECU-001: Head Unit System-on-Chip (QAM8295)
  - AST-COM-001: CAN-FD Bus
  - AST-SNS-001: GNSS Receiver
  
  Guidelines:
  - Reference actual AST-IDs from your asset_list.md (do not fabricate)
  - Include asset name after ID for clarity
  - Explain WHY compromising each asset enables this damage scenario
  - Many-to-many relationship: One DS can link to multiple assets, one asset can contribute to multiple DSs
-->

- AST-[CAT]-[NNN]: [Asset Name]
- AST-[CAT]-[NNN]: [Asset Name]

<!--
  Relationship clarification:
  Asset → DS: "If this asset's CIA properties are violated, these damage scenarios become possible"
  DS → Asset: "This damage scenario can occur if any of these assets' CIA properties are violated"
-->

**SFOP Dimensions Affected**:
<!-- 
  Assess each of the four SFOP dimensions independently.
  For each dimension, indicate Yes/No and provide brief justification (1-2 sentences).
  
  SFOP Categories:
  - Safety (S): Physical harm to vehicle occupants, pedestrians, or other road users
  - Financial (F): Monetary loss, liability, regulatory fines, or business impact
  - Operational (O): Vehicle function degradation, service disruption, or availability loss
  - Privacy (P): Unauthorized access to or disclosure of personal information
  
  Guidelines:
  - Focus on DIRECT impacts of this specific damage scenario
  - Don't include secondary/indirect effects (save for Rationale section)
  - See references/sfop-guide.md for detailed scoring criteria
-->

- **Safety**: [Yes/No] - [Brief explanation of physical harm potential. Does this cause injury/death?]
- **Financial**: [Yes/No] - [Brief explanation of monetary loss. Regulatory fines? Liability? Recall?]
- **Operational**: [Yes/No] - [Brief explanation of function degradation. Does vehicle remain drivable?]
- **Privacy**: [Yes/No] - [Brief explanation of data exposure. What personal data? How many people?]

**Impact Score**: [1-4] ([Negligible | Moderate | Severe | Critical])
<!-- 
  Overall impact is the MAXIMUM score across all four SFOP dimensions.
  
  Impact Scale:
  1 = Negligible: Minimal or no harm; minor inconvenience
  2 = Moderate: Limited harm; recoverable with minor effort
  3 = Severe: Significant harm; substantial recovery effort; serious injury possible
  4 = Critical: Catastrophic harm; fatalities, permanent disability, or business-threatening loss
  
  Format: Document individual scores for each SFOP dimension, then state overall impact
  
  Example:
  Impact Score: 4 (Critical)
  - Safety: 4 (Critical) - Potential fatalities from loss of vehicle control
  - Financial: 3 (Severe) - Major liability exposure and recall costs
  - Operational: 4 (Critical) - Complete loss of critical safety function
  - Privacy: 1 (Negligible) - No personal data involved
  
  Overall Impact: 4 (Critical) [max of S=4, F=3, O=4, P=1]
-->

- Safety: [1-4] ([Label]) - [One-line summary]
- Financial: [1-4] ([Label]) - [One-line summary]
- Operational: [1-4] ([Label]) - [One-line summary]
- Privacy: [1-4] ([Label]) - [One-line summary]

Overall Impact: [1-4] ([Label]) [max of S=X, F=X, O=X, P=X]

**Rationale**:
<!-- 
  Provide detailed justification (minimum 2-3 sentences) for EACH affected SFOP dimension (score ≥ 2).
  Explain WHY this damage scenario has the assessed severity.
  
  Guidelines:
  - Write a separate paragraph for each affected dimension
  - Reference specific consequences: injuries, costs, disruptions, data exposure
  - Consider worst-case REASONABLE outcomes (not theoretical extremes)
  - Cite regulatory requirements where relevant (ISO 26262, GDPR, GB 44495, UN R155, etc.)
  - Explain why this scenario rates at the assigned level vs. one level higher/lower
  - Quantify impacts where possible (monetary amounts, population affected, timeframes)
  
  Example structure:
  
  Safety (4 - Critical): [Explain physical harm potential. At what speed? What injuries? Why Critical vs. Severe?]
  
  Financial (3 - Severe): [Explain monetary impact. Regulatory fines? Liability? Recall costs? Brand damage? Why Severe vs. Critical?]
  
  Operational (2 - Moderate): [Explain function degradation. What stops working? Can vehicle still drive? Workarounds? Why Moderate vs. Severe?]
  
  Privacy (4 - Critical): [Explain data exposure. What data? How many people? Duration? Sensitivity? Regulatory violations? Why Critical?]
-->

**Safety ([1-4] - [Label])**: [Detailed explanation. Minimum 2-3 sentences. Explain physical harm potential, injury/fatality likelihood, driving context (highway vs parking lot), and why this severity level is appropriate.]

**Financial ([1-4] - [Label])**: [Detailed explanation. Minimum 2-3 sentences. Explain monetary losses including regulatory fines (GDPR up to €20M/4% revenue, GB 44495 up to ¥50M/5% turnover), liability for crashes, recall costs, legal fees, brand reputation damage, and lost sales.]

**Operational ([1-4] - [Label])**: [Detailed explanation. Minimum 2-3 sentences. Explain which vehicle functions are affected, whether vehicle remains drivable, duration of impact, recovery method (OTA vs service center), and legal compliance requirements (eCall, immobilizer, etc.).]

**Privacy ([1-4] - [Label])**: [Detailed explanation. Minimum 2-3 sentences. Explain what personal data is exposed (location, contacts, biometrics, financial, health), how many people affected (1, 100, 10,000+), duration of exposure (one-time vs continuous), data sensitivity under GDPR Article 9, and regulatory violations.]

**Assessment Context**:
<!--
  Record the assumptions that make the SFOP score reproducible.
  Do not include attack paths or feasibility; capture only the context needed to understand the harm.
-->

- **Affected Function / Function Cluster**: [Vehicle-level function affected by this damage scenario]
- **Function Risk Statement**: [What risky, unavailable, malformed, or privacy-invasive function reaches the road user or stakeholder]
- **Assumptions**: [Architecture, dependency, or stakeholder assumptions used in this score]
- **Operating Conditions**: [Parked / low speed / highway / ADAS mode / charging / service mode / other]
- **Population / Scale**: [One vehicle, targeted group, region, fleet-wide, estimated users]
- **Duration / Recoverability**: [Temporary auto-recovery, OTA fix, service center visit, towing, hardware replacement]
- **Evidence / Source**: [Asset list line, stakeholder interview, regulation, architecture note, or analysis source]

---

## Quick Checklist

Before finalizing this damage scenario entry, verify:

- [ ] DS-ID follows format `DS-[DOMAIN]-[NNN]` and is unique
- [ ] Domain code is one of the 7 defined (CAN, OTA, EXT, BCK, IVI, IMM, ADAS)
- [ ] Title is clear, concise, and under 80 characters
- [ ] Title describes the HARM (not the attack method)
- [ ] Linked Assets lists actual AST-IDs from `data/asset_list.md`
- [ ] Affected Function / Function Cluster is explicit
- [ ] Function Risk Statement explains how function reaches road user or stakeholder with risk
- [ ] Assessment Context records assumptions, operating conditions, scale, duration/recoverability, and evidence/source
- [ ] All four SFOP dimensions are assessed (Yes/No with justification)
- [ ] Impact Score is 1-4 and equals the MAX of individual SFOP scores
- [ ] Overall Impact line shows the MAX calculation explicitly
- [ ] Rationale provides 2-3 sentences for EACH affected SFOP dimension (score ≥ 2)
- [ ] No threat scenario or attack method details (that's TS, not DS)
- [ ] No attack feasibility rating (AFR) included (that's a later TARA step)
- [ ] No placeholder text remains ([TODO], [TBD], etc.)
- [ ] Cross-check with references/ds-schema.md for field requirements
- [ ] Cross-check with references/sfop-guide.md for scoring criteria

---

## Example (for reference)

### DS-IVI-001: Unauthorized Driver Location Tracking

**Linked Assets**:
- AST-ECU-001: Head Unit System-on-Chip (QAM8295)
- AST-SNS-001: GNSS Receiver
- AST-DAT-001: Persistent Storage (UFS)
- AST-COM-005: Cellular/Telematics Link

**SFOP Dimensions Affected**:
- **Safety**: No - Location tracking is passive surveillance and does not directly cause physical harm to vehicle occupants or other road users
- **Financial**: Yes - Violates GDPR Article 6 (lawful basis for processing) and China GB 44495 personal information protection requirements, resulting in major regulatory fines
- **Operational**: No - Vehicle operational functions (driving, navigation, infotainment) remain fully available and unaffected
- **Privacy**: Yes - Continuous real-time tracking reveals comprehensive movement patterns, visited locations, daily routines, and associations with other individuals

**Impact Score**: 4 (Critical)
- Safety: 1 (Negligible) - No physical harm from tracking
- Financial: 3 (Severe) - GDPR fines up to €20M/4% revenue, class-action lawsuits
- Operational: 1 (Negligible) - All vehicle functions remain available
- Privacy: 4 (Critical) - Persistent tracking of large user population revealing sensitive life patterns

Overall Impact: 4 (Critical) [max of S=1, F=3, O=1, P=4]

**Rationale**:

**Safety (1 - Negligible)**: Real-time location tracking is a passive surveillance activity that does not directly cause physical harm to vehicle occupants, pedestrians, or other road users. No safety-critical vehicle functions are impacted - the steering, braking, powertrain, and ADAS systems continue to operate normally. There is no mechanism by which location tracking alone would cause a crash, injury, or fatality. Therefore, safety impact is rated as Negligible.

**Financial (3 - Severe)**: Unauthorized location tracking without user consent violates GDPR Article 6 (lawful basis for processing personal data) and China GB 44495 personal information protection requirements. GDPR enforcement can result in fines up to €20 million or 4% of annual global revenue, whichever is higher. For a major automotive OEM with €50B annual revenue, this represents a potential €2B penalty. Additionally, class-action lawsuits from affected users could result in significant settlement costs ($100M+ based on comparable privacy litigation). Brand reputation damage from a high-profile privacy scandal would impact customer trust and future vehicle sales. The financial impact is rated Severe due to these combined regulatory, legal, and reputational costs, though it does not reach Critical level (which would be business-threatening).

**Operational (1 - Negligible)**: Vehicle operational functions including driving controls (steering, braking, acceleration), infotainment features, navigation, and connectivity remain fully available and unaffected during location tracking. The damage scenario does not degrade vehicle performance or user experience from an operational perspective. The driver may not even be aware that tracking is occurring. All systems continue to function normally. Therefore, operational impact is rated as Negligible.

**Privacy (4 - Critical)**: Continuous real-time tracking of driver location over extended periods (months to years) enables comprehensive surveillance of movement patterns including home and work addresses, daily commute routes, frequented locations, and associations with other individuals through location proximity. Location data reveals highly sensitive personal information about an individual's life including health information (hospital visits, pharmacy trips), religious practices (places of worship), political activities (rallies, campaign offices), and intimate relationships (overnight stays at residential addresses). Under ISO 21434 and GDPR Article 9 special categories of personal data, location tracking that reveals these sensitive attributes is considered a Critical privacy violation. If this affects a large user population (10,000+ vehicles) over long duration, it represents the highest category of privacy harm. China GB 44495 also classifies precise location data as sensitive personal information requiring enhanced protection.

**Assessment Context**:

- **Affected Function / Function Cluster**: Location-based services and driver travel history
- **Function Risk Statement**: The vehicle delivers location services with privacy risk because movement patterns can be exposed without authorization
- **Assumptions**: Location data is stored or transmitted with identifiers that can be linked to a driver or account.
- **Operating Conditions**: Normal driving and parked states over an extended ownership period.
- **Population / Scale**: Fleet-scale exposure, potentially 10,000+ users.
- **Duration / Recoverability**: Continuous or repeated tracking over months; remediation requires software and data-handling changes.
- **Evidence / Source**: GNSS receiver, persistent storage, and telematics assets in `data/asset_list.md`; GDPR/GB 44495 privacy rationale.
