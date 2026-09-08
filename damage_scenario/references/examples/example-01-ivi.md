# Example: IVI/Infotainment Damage Scenarios

This example demonstrates how to derive damage scenarios from IVI (In-Vehicle Infotainment) assets using the damage_scenario skill workflow.

---

## Context

**Source Assets**: From `data/asset_list.md`, we focus on Infotainment/Head Unit system assets with high CIA ratings that could lead to privacy and operational damage scenarios.

**Key IVI Assets**:
- AST-ECU-001: Head Unit System-on-Chip (QAM8295) - C:3 / I:4 / A:3
- AST-ECU-004: Android Guest Operating System - C:3 / I:3 / A:2
- AST-DAT-001: Persistent Storage (UFS) - C:3 / I:3 / A:3
- AST-SNS-001: GNSS Receiver - C:2 / I:2 / A:2
- AST-COM-005: Cellular/Telematics Link - C:2 / I:3 / A:2

**CIA Triage Process**:
1. Identify assets with high Confidentiality (C=3 or C=4) → ask privacy and financial impact questions
2. Identify assets with high Integrity (I=3 or I=4) → ask safety and operational impact questions only when the architecture supports those harms
3. Identify assets with high Availability (A=3 or A=4) → ask operational and safety impact questions based on function criticality and recovery path

---

## Damage Scenario 1: Location Privacy Violation

### Derivation

**Asset**: AST-SNS-001 (GNSS Receiver) with C:2 / I:2 / A:2  
**Asset**: AST-DAT-001 (Persistent Storage) with C:3 / I:3 / A:3

**CIA Analysis**:
- GNSS Receiver provides location data (Confidentiality concern)
- Persistent Storage stores location history (Confidentiality = 3)
- Combined: High Confidentiality → **Privacy (P) damage scenario**

**Interview Questions Used**:
- Q: "What harm occurs if GNSS location history is disclosed without authorization?"
- A: Continuous location tracking reveals driver movements, home/work addresses, visited locations
- Q: "How many users could be affected?"
- A: Potentially 10,000+ vehicles if fleet-wide exposure occurs
- Q: "What are the regulatory implications?"
- A: GDPR Article 6 violation (no lawful basis), GB 44495 sensitive personal information violation

**SFOP Assessment**:
- Safety: 1 (No physical harm from tracking)
- Financial: 3 (GDPR fines up to €20M/4% revenue)
- Operational: 1 (Vehicle functions normally)
- Privacy: 4 (Persistent tracking of large population)

**Overall Impact**: 4 (Critical) [driven by Privacy]

---

### DS-IVI-001: Unauthorized Driver Location Tracking

**Linked Assets**:
- AST-ECU-001: Head Unit System-on-Chip (QAM8295)
- AST-SNS-001: GNSS Receiver
- AST-DAT-001: Persistent Storage (UFS)
- AST-COM-005: Cellular/Telematics Link

**SFOP Dimensions Affected**:
- **Safety**: No - Location tracking is passive surveillance and does not directly cause physical harm to vehicle occupants or other road users
- **Financial**: Yes - Violates GDPR Article 6 (lawful basis for processing) and China GB 44495 personal information protection requirements, resulting in major regulatory fines up to €20M or 4% annual revenue
- **Operational**: No - Vehicle operational functions (driving, navigation, infotainment) remain fully available and unaffected by location tracking
- **Privacy**: Yes - Continuous real-time tracking reveals comprehensive movement patterns, visited locations, daily routines, and associations with other individuals over extended periods

**Impact Score**: 4 (Critical)
- Safety: 1 (Negligible) - No physical harm from tracking
- Financial: 3 (Severe) - GDPR fines up to €20M/4% revenue, class-action lawsuits
- Operational: 1 (Negligible) - All vehicle functions remain available
- Privacy: 4 (Critical) - Persistent tracking of large user population revealing sensitive life patterns

Overall Impact: 4 (Critical) [max of S=1, F=3, O=1, P=4]

**Assessment Context**:
- **Assumptions**: GNSS and stored location history can be linked to driver accounts or vehicle identifiers.
- **Operating Conditions**: Normal driving and parked states over an extended ownership period.
- **Population / Scale**: Fleet-scale exposure, potentially 10,000+ users.
- **Duration / Recoverability**: Continuous or repeated tracking over months; remediation requires software and data-handling changes.
- **Evidence / Source**: AST-SNS-001, AST-DAT-001, AST-COM-005, privacy interview responses, GDPR/GB 44495 rationale.

**Rationale**:

**Safety (1 - Negligible)**: Real-time location tracking is a passive surveillance activity that does not directly cause physical harm to vehicle occupants, pedestrians, or other road users. No safety-critical vehicle functions are impacted - the steering, braking, powertrain, and ADAS systems continue to operate normally. There is no mechanism by which location tracking alone would cause a crash, injury, or fatality. Therefore, safety impact is rated as Negligible.

**Financial (3 - Severe)**: Unauthorized location tracking without user consent violates GDPR Article 6 (lawful basis for processing personal data) and China GB 44495 personal information protection requirements. GDPR enforcement can result in fines up to €20 million or 4% of annual global revenue, whichever is higher. For a major automotive OEM with €50B annual revenue, this represents a potential €2B penalty. Additionally, class-action lawsuits from affected users could result in significant settlement costs ($100M+ based on comparable privacy litigation in the automotive and mobile device sectors). Brand reputation damage from a high-profile privacy scandal would impact customer trust and future vehicle sales, with potential loss of market share to competitors with stronger privacy reputations. The financial impact is rated Severe due to these combined regulatory, legal, and reputational costs, though it does not reach Critical level (which would be business-threatening bankruptcy risk).

**Operational (1 - Negligible)**: Vehicle operational functions including driving controls (steering, braking, acceleration), infotainment features, navigation services, and wireless connectivity remain fully available and unaffected during location tracking. The damage scenario does not degrade vehicle performance or user experience from an operational perspective. The driver may not even be aware that unauthorized tracking is occurring, as navigation and location services continue to work normally. All systems continue to function as designed. Therefore, operational impact is rated as Negligible.

**Privacy (4 - Critical)**: Continuous real-time tracking of driver location over extended periods (months to years) enables comprehensive surveillance of movement patterns including precise home and work addresses, daily commute routes, frequented locations (shopping, dining, recreation), and associations with other individuals through location proximity analysis. Location data is recognized as highly sensitive under ISO 21434 and GDPR because it reveals information about an individual's private life, health (hospital visits, pharmacy trips, doctor appointments), religious practices (places of worship, religious events), political activities (rallies, campaign offices, government buildings), intimate relationships (overnight stays at residential addresses), and social networks (locations visited with others). Under GDPR Article 9, location data that reveals special categories of personal data (health, religion, political opinions) receives the highest level of privacy protection. China GB 44495 also classifies precise location data as sensitive personal information requiring user consent and enhanced security controls. If this tracking affects a large user population (10,000+ vehicles) over long duration, it represents the highest category of privacy harm under ISO 21434 (Critical level). The persistent, comprehensive nature of the tracking - capturing every trip, every destination, every pattern over years - constitutes a Critical privacy violation.

---

## Damage Scenario 2: PII Exposure via Infotainment

### Derivation

**Asset**: AST-ECU-004 (Android Guest OS) with C:3 / I:3 / A:2  
**Asset**: AST-DAT-001 (Persistent Storage) with C:3 / I:3 / A:3

**CIA Analysis**:
- Android processes user contacts, call history, paired devices (Confidentiality = 3)
- Persistent Storage stores user data (Confidentiality = 3)
- Combined: High Confidentiality → **Privacy (P) + Financial (F) damage scenario**

**Interview Questions Used**:
- Q: "What user data is stored in Android and UFS storage?"
- A: Contacts, call history, SMS, paired mobile device IDs, WiFi credentials, app data
- Q: "What is the regulatory classification of this data?"
- A: Personal data under GDPR Article 6, personal information under GB 44495
- Q: "How many users affected?"
- A: 100-1,000 users for targeted exposure, 10,000+ for fleet-wide breach

**SFOP Assessment**:
- Safety: 1 (No physical harm)
- Financial: 3 (GDPR fines, class-action lawsuits)
- Operational: 1 (Vehicle functions normally)
- Privacy: 3-4 (Depends on scale: 3 for thousands, 4 for tens of thousands)

**Overall Impact**: 3-4 (Severe to Critical)

---

### DS-IVI-002: User Personal Data Exposure

**Linked Assets**:
- AST-ECU-004: Android Guest Operating System
- AST-DAT-001: Persistent Storage (UFS)
- AST-ECU-001: Head Unit System-on-Chip (QAM8295)
- AST-COM-003: Bluetooth/WiFi Module

**SFOP Dimensions Affected**:
- **Safety**: No - Data exposure does not cause physical harm to vehicle occupants or other road users
- **Financial**: Yes - GDPR Article 5 (data security) and China GB 44495 violations result in regulatory fines and potential class-action lawsuits from affected users
- **Operational**: No - Vehicle infotainment and driving functions continue to operate normally after data disclosure
- **Privacy**: Yes - User personal data including contacts, call history, paired device identifiers, and app data is exposed to unauthorized parties

**Impact Score**: 3 (Severe)
- Safety: 1 (Negligible) - No physical harm
- Financial: 3 (Severe) - GDPR fines up to €20M/4% revenue, lawsuit settlements
- Operational: 1 (Negligible) - All functions remain available
- Privacy: 3 (Severe) - Personal data of thousands of users exposed

Overall Impact: 3 (Severe) [max of S=1, F=3, O=1, P=3]

**Assessment Context**:
- **Assumptions**: Contacts, call history, paired device identifiers, and stored app data are linkable to identifiable users.
- **Operating Conditions**: Normal infotainment operation before disclosure; vehicle functions remain available after disclosure.
- **Population / Scale**: Regional or model-specific exposure affecting approximately 1,000-5,000 users.
- **Duration / Recoverability**: One-time or bounded data disclosure; remediation requires notification, credential rotation guidance, and data-handling fixes.
- **Evidence / Source**: AST-ECU-004, AST-DAT-001, AST-COM-003, user-data inventory interview, GDPR Article 5/32 rationale.

**Rationale**:

**Safety (1 - Negligible)**: The exposure of personal data stored in the infotainment system does not directly cause physical harm to vehicle occupants, pedestrians, or other road users. No safety-critical vehicle functions (steering, braking, powertrain, ADAS) are affected by data disclosure. The vehicle remains fully operational and safe to drive. Therefore, safety impact is Negligible.

**Financial (3 - Severe)**: Unauthorized access and disclosure of user personal data violates GDPR Article 5(1)(f) (security of processing) and Article 32 (security of personal data), which require appropriate technical measures to protect personal data. For a data breach affecting thousands of users, GDPR fines under Article 83 can reach up to €20 million or 4% of annual global turnover. Notification requirements under GDPR Article 33 (notify supervisory authority within 72 hours) and Article 34 (notify affected individuals) create additional compliance costs. Class-action lawsuits from affected users could result in settlements ranging from $10M to $100M based on precedents in automotive and technology data breach litigation. Brand reputation damage from the data breach would impact customer trust, requiring investment in PR campaigns and potentially causing loss of market share. The combined regulatory fines, legal settlements, notification costs, and reputation damage rate this as Severe financial impact, though not Critical (which would threaten business viability).

**Operational (1 - Negligible)**: Vehicle operational functions remain completely unaffected by data disclosure. The infotainment system continues to provide navigation, media playback, Bluetooth connectivity, and other features normally. Driving controls (steering, braking, acceleration, powertrain) are unaffected. No service disruption occurs from the user's perspective - they may not even be aware that data has been disclosed. Therefore, operational impact is Negligible.

**Privacy (3 - Severe)**: User personal data exposed includes contacts (names, phone numbers, email addresses), call history and SMS logs, paired mobile device identifiers (Bluetooth MAC addresses), WiFi network credentials (SSIDs and passwords), third-party app data, and voice command history. This data is classified as "personal data" under GDPR and "personal information" under China GB 44495. The exposure affects approximately 1,000-5,000 users (assuming targeted exposure for a specific vehicle model or region). Contact information can be used for identity theft, phishing, and social engineering harms. WiFi credentials enable unauthorized network access. Device identifiers enable tracking across different systems. The impact is rated Severe (3) based on the sensitivity of the data and the scale of affected population. If the breach affected 10,000+ users or included special categories of data (biometric, health, financial), the privacy rating would escalate to Critical (4).

---

## Damage Scenario 3: Infotainment System Unavailable

### Derivation

**Asset**: AST-ECU-001 (Head Unit SoC) with C:3 / I:4 / A:3  
**Asset**: AST-DAT-001 (Persistent Storage) with C:3 / I:3 / A:3

**CIA Analysis**:
- Head Unit SoC availability loss (A=3) → Vehicle infotainment inoperable
- Persistent Storage encrypted (A=3) → Data inaccessible
- Combined: High Availability → **Operational (O) + Financial (F) damage scenario**

**Interview Questions Used**:
- Q: "What happens if the Head Unit SoC becomes unavailable?"
- A: Entire infotainment system becomes inoperable - no displays, navigation, audio
- Q: "Can the vehicle still be driven?"
- A: Yes, vehicle drivability is not affected (user confirmed HUD not safety-critical)
- Q: "What is the recovery method?"
- A: Visit service center for ECU reflash or equivalent recovery action
- Q: "What is the financial impact if scaled?"
- A: Recovery costs across fleet could reach millions if service-center reflashing is required

**SFOP Assessment**:
- Safety: 2 (Vehicle stranded, but drivable if already running)
- Financial: 3 (Recovery costs and brand damage if fleet-wide)
- Operational: 4 (Complete loss of infotainment - all displays, navigation, audio inoperable)
- Privacy: 1 (No data disclosure in this availability-only scenario)

**Overall Impact**: 4 (Critical) [driven by Operational]

---

### DS-IVI-003: Infotainment System Unavailable

**Linked Assets**:
- AST-ECU-001: Head Unit System-on-Chip (QAM8295)
- AST-DAT-001: Persistent Storage (UFS)
- AST-DAT-004: Firmware Images

**SFOP Dimensions Affected**:
- **Safety**: Yes - Vehicle infotainment system disabled, driver loses all visual displays including instrument cluster (showing speed, fuel, warnings), creating safety risk from loss of situational awareness
- **Financial**: Yes - Recovery requires service center visit for ECU reflash, fleet-scale service costs, and brand reputation damage from widespread vehicle service unavailability
- **Operational**: Yes - Complete loss of infotainment functionality including all displays (HUD, central console, instrument cluster), navigation, audio, wireless connectivity, rendering system unusable
- **Privacy**: No - This availability-only scenario does not expose personal data; data disclosure would be a separate damage scenario

**Impact Score**: 4 (Critical)
- Safety: 2 (Moderate) - Loss of instrument cluster degrades driver awareness
- Financial: 3 (Severe) - Fleet-wide recovery costs and brand damage
- Operational: 4 (Critical) - Complete system inoperability
- Privacy: 1 (Negligible) - No data exposure (encryption only)

Overall Impact: 4 (Critical) [max of S=2, F=3, O=4, P=1]

**Assessment Context**:
- **Assumptions**: Head Unit SoC controls central display, HUD, instrument cluster, navigation, audio, and wireless connectivity in this architecture.
- **Operating Conditions**: Vehicle remains physically drivable but the integrated display/infotainment subsystem is unavailable.
- **Population / Scale**: Fleet-scale condition affecting up to 10,000 vehicles in the financial rationale.
- **Duration / Recoverability**: Persistent until service-center ECU reflash or equivalent recovery.
- **Evidence / Source**: AST-ECU-001, AST-DAT-001, AST-DAT-004, recovery interview responses, service-cost assumptions.

**Rationale**:

**Safety (2 - Moderate)**: Head Unit SoC unavailability renders all displays inoperable, including the instrument cluster (AST-ACT-003) which typically shows vehicle speed, fuel level, and warning lights. While the user confirmed that displays are not safety-critical and the vehicle remains drivable, the loss of speed indication and warning lights degrades driver situational awareness. A driver who cannot see their current speed may unintentionally violate speed limits or drive unsafely for conditions. Loss of warning lights (check engine, low fuel, brake system warnings) prevents the driver from being alerted to vehicle malfunctions that could escalate to safety issues. However, the core driving controls (steering, braking, acceleration) remain functional, and the driver can still operate the vehicle safely with caution. This rates as Moderate (2) safety impact - not Negligible because there is some safety degradation, but not Severe because the vehicle remains controllable.

**Financial (3 - Severe)**: Recovery from widespread infotainment unavailability requires service center ECU reflashing at approximately $200-500 per vehicle for labor and logistics, plus customer support and goodwill costs. If this condition affects a fleet of 10,000 vehicles, total recovery costs could reach $2M-$5M before indirect brand and customer-retention costs. Beyond direct costs, the OEM faces reputation damage from a high-profile vehicle service outage, potentially impacting customer confidence and future sales. The combination of recovery costs, customer disruption, and brand damage rates this as Severe (3) financial impact. It does not reach Critical (4) because while expensive, this does not threaten business viability or constitute a catastrophic financial loss (>$100M).

**Operational (4 - Critical)**: The Head Unit SoC controls all infotainment functions and displays. Complete unavailability of the SoC results in loss of: (1) All displays - HUD, central console touchscreen, instrument cluster - go blank, (2) Navigation system inoperable, (3) Audio system inoperable - no radio, media, or phone calls, (4) Wireless connectivity lost - Bluetooth, WiFi, cellular all unavailable, (5) Voice assistant disabled. The vehicle owner cannot use the infotainment system at all until recovery action is taken. This represents complete loss of a critical vehicle subsystem, meeting the definition of Critical (4) operational impact for this assumed integrated display architecture. While the vehicle remains physically drivable, the infotainment and display subsystem is completely non-functional and requires service center intervention to restore.

**Privacy (1 - Negligible)**: This damage scenario assumes availability loss only, with no disclosure of user personal information to unauthorized parties. If personal data is also disclosed or threatened for publication, that would be a separate privacy damage scenario (DS-IVI-002 or a variant) with a higher Privacy impact. For this availability-only scenario, privacy impact is Negligible.

---

## Summary

**IVI Damage Scenarios Created**: 3  
**Asset Coverage**: 6 unique assets referenced (AST-ECU-001, AST-ECU-004, AST-DAT-001, AST-SNS-001, AST-COM-003, AST-COM-005, AST-DAT-004)

**Key Learnings**:
1. High Confidentiality assets (C=3) → Privacy damage scenarios
2. High Availability assets (A=3) → Operational damage scenarios
3. IVI domain typically has lower Safety scores (1-2) because infotainment doesn't control vehicle motion
4. Financial and Privacy scores drive IVI impact ratings (3-4 common)
5. Many-to-many relationship: One asset (AST-ECU-001) appears in multiple DSs

**Next Step**: Use these DS entries as input to `threat_scenario` to identify attack paths and attack feasibility without changing the consequence-focused DS wording.
