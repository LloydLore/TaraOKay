# Damage Scenario Patterns - Reusable Templates

This document provides reusable damage scenario patterns for common automotive cybersecurity harm events. Use these patterns as starting points when creating damage scenario entries in `data/ds.md`.

---

## How to Use This Document

Each pattern includes:
- **Pattern Name**: Descriptive title for the damage category
- **Damage Description**: What harm occurs (focus on consequence, not attack method)
- **Typical SFOP Dimensions Affected**: Which of S/F/O/P are impacted and why
- **Typical Impact Score Range**: Expected severity (1-4)
- **Example Assets**: Which assets from `data/asset_list.md` could lead to this damage
- **Template Description**: Reusable text you can adapt for specific DS entries

**Language rule**: Pattern titles and DS titles should describe the observable harm state. Avoid attack-method words such as "injection", "spoofing", "malware", "exploit", "attacker", or "vulnerability" in DS titles and final damage descriptions; save those details for `threat_scenario`.

**Usage**: 
1. Identify which pattern(s) match your damage scenario
2. Copy the template description
3. Customize with specifics from your asset analysis
4. Adjust SFOP scores based on your vehicle system context

---

## Pattern 1: Vehicle Immobilization

**Damage Description**: Vehicle cannot be started or operated, rendering it completely unusable until recovery action is taken (ransom payment, ECU reflash, or service center visit).

**Typical SFOP Dimensions Affected**:
- **Safety**: Moderate (2-3) - Vehicle stranded, occupants may be in unsafe location
- **Financial**: Severe (3) - Recovery costs, lost productivity, potential ransom demands
- **Operational**: Critical (4) - Complete loss of vehicle function
- **Privacy**: Negligible (1) - No data exposure in pure immobilization

**Typical Impact Score Range**: 3-4 (Severe to Critical)

**Example Assets** (from asset_list.md):
- AST-ECU-001: Head Unit System-on-Chip (QAM8295) - Loss of correct system behavior could prevent startup
- AST-ECU-006: Gateway ECU - Loss of network availability could isolate powertrain communication
- AST-DAT-004: Firmware Images - Corrupted firmware prevents boot
- AST-COM-001: CAN-FD Bus - Communication unavailability prevents ECU coordination

**Template Description**:
```
The vehicle cannot be started or operated under [context: parked, roadside stop, charging, service mode]. 
The engine control system refuses to start, displaying [error message or behavior]. This renders the vehicle 
completely unusable, requiring [recovery method: OTA recovery, ECU reflashing at service center, towing, 
hardware replacement]. Operational impact is Critical (4) as the vehicle cannot 
fulfill its primary function. Financial impact is Severe (3) due to recovery costs and potential fleet-wide 
implications if scaled.
```

---

## Pattern 2: Unintended Acceleration or Braking

**Damage Description**: Vehicle accelerates or brakes without driver input, or fails to respond to driver commands, potentially causing collisions.

**Typical SFOP Dimensions Affected**:
- **Safety**: Critical (4) - High probability of collision, injury, or fatality
- **Financial**: Severe (3) - Major liability exposure, recall costs
- **Operational**: Critical (4) - Loss of critical vehicle control function
- **Privacy**: Negligible (1) - No personal data involved

**Typical Impact Score Range**: 4 (Critical)

**Example Assets** (from asset_list.md):
- AST-ECU-001: Head Unit System-on-Chip - Incorrect output could influence vehicle behavior if accepted by downstream systems
- AST-COM-001: CAN-FD Bus - Incorrect or unavailable network communication could affect powertrain coordination
- AST-ECU-006: Gateway ECU - Incorrect routing or filtering could allow unsafe vehicle state changes

**Template Description**:
```
The vehicle [accelerates/brakes] without driver input or fails to respond to driver [acceleration/braking] 
commands in [operating condition: low speed, highway, ADAS active, parking]. 
At highway speeds (>80 km/h), unintended [acceleration/braking] creates high probability of collision with 
fatality or severe injury to occupants and other road users. Safety impact is Critical (4) as this directly 
causes loss of vehicle control. Operational impact is Critical (4) as a critical safety function is compromised. 
Financial impact is Severe (3) due to crash liability, potential recalls, and brand reputation damage.
```

---

## Pattern 3: Loss of Steering Control

**Damage Description**: Driver loses ability to steer the vehicle, making it uncontrollable and likely to leave the intended path.

**Typical SFOP Dimensions Affected**:
- **Safety**: Critical (4) - Extremely high crash risk, likely fatalities at speed
- **Financial**: Severe (3) - Catastrophic liability, recall, regulatory action
- **Operational**: Critical (4) - Complete loss of essential vehicle function
- **Privacy**: Negligible (1) - No data exposure

**Typical Impact Score Range**: 4 (Critical)

**Example Assets** (from asset_list.md):
- AST-ECU-001: Head Unit System-on-Chip - Incorrect vehicle data could contribute to steering assist degradation if accepted downstream
- AST-COM-001: CAN-FD Bus - Communication loss or incorrect state propagation could affect steering-related coordination
- AST-ECU-006: Gateway ECU - Network isolation could degrade steering support communication

**Template Description**:
```
The driver loses the ability to steer the vehicle in [operating condition: highway, low speed, automated lane keeping]. 
At highway speeds above 80 km/h, loss of steering 
control makes the vehicle uncontrollable, with extremely high probability of collision resulting in fatalities 
or severe injuries. Safety impact is Critical (4), representing the highest severity category. Operational impact 
is Critical (4) as steering is an absolutely essential vehicle function. Financial impact is Severe (3) due to 
multi-million dollar liability, regulatory fines, and mandatory recall costs.
```

---

## Pattern 4: Personal Information (PII) Exposure

**Damage Description**: Driver or passenger personal information is disclosed to unauthorized parties, violating privacy and data protection regulations.

**Typical SFOP Dimensions Affected**:
- **Safety**: Negligible (1) - No physical harm from data exposure alone
- **Financial**: Moderate to Severe (2-3) - GDPR/GB 44495 fines, lawsuits
- **Operational**: Negligible (1) - Vehicle functions normally
- **Privacy**: Moderate to Critical (2-4) - Depends on data sensitivity and population size

**Typical Impact Score Range**: 2-4 (Moderate to Critical, driven by Privacy score)

**Example Assets** (from asset_list.md):
- AST-ECU-001: Head Unit System-on-Chip - Processes user contacts, call logs
- AST-DAT-001: Persistent Storage (UFS) - Stores personal data
- AST-SNS-003: Driver Monitoring Camera - Captures biometric (facial) data
- AST-COM-005: Cellular/Telematics Link - Transmits user data

**Template Description**:
```
Personal information including [specify data types: contacts, location history, biometric data, etc.] is disclosed 
to unauthorized parties affecting [specify population: one user, 100 users, 10,000+ users]. This violates GDPR 
Article [specify article] and China GB 44495 personal information protection requirements. Privacy impact is 
[2-4 based on sensitivity and scale]. Financial impact is [2-3] due to regulatory fines up to €20M/4% annual revenue 
(GDPR) or ¥50M/5% turnover (GB 44495), plus class-action lawsuit risk. Safety and Operational impacts are Negligible (1) 
as no physical systems are affected.
```

---

## Pattern 5: Continuous Location Tracking

**Damage Description**: Vehicle location is continuously monitored and recorded without user consent, enabling comprehensive surveillance of driver movements and behavior.

**Typical SFOP Dimensions Affected**:
- **Safety**: Negligible (1) - No direct physical harm from tracking
- **Financial**: Severe (3) - Major GDPR/GB 44495 violations, class-action lawsuits
- **Operational**: Negligible (1) - Vehicle functions normally
- **Privacy**: Severe to Critical (3-4) - Persistent tracking reveals comprehensive life patterns

**Typical Impact Score Range**: 3-4 (Severe to Critical, driven by Privacy)

**Example Assets** (from asset_list.md):
- AST-SNS-001: GNSS Receiver - Provides location data
- AST-ECU-001: Head Unit System-on-Chip - Processes and stores location
- AST-DAT-001: Persistent Storage (UFS) - Stores location history
- AST-COM-005: Cellular/Telematics Link - Transmits location data outside the vehicle boundary

**Template Description**:
```
The vehicle's real-time location is continuously monitored and recorded over [timeframe: days, months, years] 
affecting [population size] users. Continuous tracking reveals comprehensive movement patterns including home/work 
addresses, daily routines, visited locations, and associations with other individuals. This enables surveillance of 
personal life, health (hospital visits), religion (places of worship), and political activities. Privacy impact is 
Critical (4) under ISO 21434 and GDPR Article 9 special categories. Financial impact is Severe (3) due to maximum 
GDPR penalties and class-action lawsuit exposure. Location data is considered highly sensitive personal information 
under both GDPR and China GB 44495.
```

---

## Pattern 6: Financial Theft via Unauthorized Transactions

**Damage Description**: Unauthorized financial transactions are initiated from the vehicle's payment systems, resulting in monetary theft from vehicle owner or users.

**Typical SFOP Dimensions Affected**:
- **Safety**: Negligible (1) - No physical harm
- **Financial**: Moderate to Severe (2-3) - Direct monetary theft, liability for unauthorized charges
- **Operational**: Negligible to Moderate (1-2) - Payment features may be disabled, vehicle functions normally
- **Privacy**: Moderate (2) - Financial data may be exposed

**Typical Impact Score Range**: 2-3 (Moderate to Severe, driven by Financial)

**Example Assets** (from asset_list.md):
- AST-ECU-001: Head Unit System-on-Chip - Processes payment transactions
- AST-DAT-001: Persistent Storage (UFS) - Stores payment credentials
- AST-COM-005: Cellular/Telematics Link - Transmits payment data

**Template Description**:
```
Unauthorized financial transactions totaling [amount range] are initiated from the vehicle's [payment system: 
toll payment, charging station, in-car commerce, etc.] affecting [population size] users. Financial impact is 
[2-3 based on total theft amount and liability exposure]. Individual losses may be $[amount] but scaled across 
fleet could reach $[larger amount]. OEM may be liable for inadequate security controls. Privacy impact is Moderate (2) 
as payment credentials and transaction history are exposed. Operational impact is Negligible (1) as core vehicle 
functions remain available.
```

---

## Pattern 7: Vehicle System Unavailable with Extortion Demand

**Damage Description**: Vehicle systems are unavailable and recovery is blocked by an extortion demand, or sensitive data has been disclosed with a publication threat.

**Typical SFOP Dimensions Affected**:
- **Safety**: Moderate (2) - Vehicle may be stranded in unsafe location
- **Financial**: Severe (3) - Extortion payments, recovery costs, scaled across fleet
- **Operational**: Critical (4) - Vehicle completely unusable until recovery
- **Privacy**: Moderate to Severe (2-3) - If sensitive data disclosure is combined with system unavailability

**Typical Impact Score Range**: 3-4 (Severe to Critical)

**Example Assets** (from asset_list.md):
- AST-ECU-001: Head Unit System-on-Chip - Could be encrypted/disabled
- AST-DAT-001: Persistent Storage (UFS) - Files encrypted
- AST-DAT-004: Firmware Images - Encrypted boot prevents startup

**Template Description**:
```
Vehicle systems are unavailable and the user or OEM is presented with an extortion demand of [amount] to restore functionality. 
The vehicle cannot be operated until [recovery method]. If scaled across fleet of [size], total extortion exposure is $[amount]. 
Operational impact is Critical (4) as vehicle is completely unusable. Financial impact is Severe (3) accounting for extortion payments, recovery costs, service center visits, and brand damage. 
If sensitive data was also disclosed with publication threat, Privacy impact increases to Severe (3).
```

---

## Pattern 8: Display / HUD Misinformation

**Damage Description**: False or misleading information is displayed to the driver via instrument cluster, HUD, or infotainment screen, potentially causing driver confusion or unsafe decisions.

**Typical SFOP Dimensions Affected**:
- **Safety**: Negligible to Moderate (1-2) - Driver confusion could lead to unsafe decisions
- **Financial**: Negligible to Moderate (1-2) - OTA patch costs, potential liability
- **Operational**: Moderate (2) - Display information unreliable, user experience degraded
- **Privacy**: Negligible (1) - No data exposure

**Typical Impact Score Range**: 2 (Moderate)

**Example Assets** (from asset_list.md):
- AST-ECU-001: Head Unit System-on-Chip - Controls all displays
- AST-ACT-001: HUD (Head-Up Display)
- AST-ACT-002: Central Display (Infotainment)
- AST-ACT-003: Instrument Cluster Display

**Template Description**:
```
False or misleading information is displayed via [specify display: HUD, instrument cluster, infotainment] showing 
[example: false speed reading, fake warning messages, incorrect navigation, manipulated camera feed]. Driver may make 
unsafe decisions based on false information (e.g., accelerating believing speed is lower than actual). Safety impact is 
Moderate (2) as driver confusion increases crash risk but modern vehicles have redundant safety systems. Operational 
impact is Moderate (2) as display functions are degraded but vehicle remains drivable. Financial impact is Moderate (2) 
for OTA patch deployment and potential liability for crashes caused by misinformation.
```

---

## Pattern 9: Regulatory Non-Compliance (Fines, Type Approval Loss)

**Damage Description**: Vehicle violates regulatory requirements (emissions, safety reporting, data protection, cybersecurity) resulting in fines, type approval withdrawal, or inability to sell vehicles.

**Typical SFOP Dimensions Affected**:
- **Safety**: Negligible to Moderate (1-2) - Depends on which regulation is violated
- **Financial**: Severe to Critical (3-4) - Major regulatory fines, type approval loss is business-threatening
- **Operational**: Negligible to Moderate (1-2) - Vehicle may function but be illegal to operate
- **Privacy**: Variable - Depends on regulation (GDPR → Privacy impact)

**Typical Impact Score Range**: 3-4 (Severe to Critical, driven by Financial)

**Example Assets** (from asset_list.md):
- AST-ECU-001: Head Unit System-on-Chip - Must comply with UN R155 cybersecurity requirements
- AST-COM-005: Cellular/Telematics Link - eCall compliance (EU mandate)
- AST-DAT-003: Cryptographic Keys & Certificates - Must meet security standards

**Template Description**:
```
Vehicle violates [specify regulation: UN R155 cybersecurity, eCall emergency call, GDPR data protection, emissions 
monitoring] due to [specify failure: inadequate security controls, disabled safety feature, improper data handling]. 
Financial impact is [3-4] due to [specify penalty: GDPR fine up to €20M/4% revenue, UN R155 type approval withdrawal 
preventing vehicle sales, eCall non-compliance fines]. Type approval withdrawal is business-threatening, rating Financial 
impact as Critical (4). Regulatory violations also cause severe brand reputation damage affecting consumer trust and 
future sales.
```

---

## Pattern 10: Reputational Damage / Brand Harm

**Damage Description**: Widely publicized cybersecurity incident damages OEM brand reputation, erodes customer trust, and impacts future vehicle sales and market valuation.

**Typical SFOP Dimensions Affected**:
- **Safety**: Variable (1-4) - Depends on underlying incident
- **Financial**: Severe to Critical (3-4) - Lost sales, stock price impact, long-term brand damage
- **Operational**: Negligible (1) - Vehicles continue to function
- **Privacy**: Variable - Depends on incident (data breach → high Privacy)

**Typical Impact Score Range**: 3-4 (Severe to Critical, driven by Financial)

**Example Assets** (from asset_list.md):
- Any asset - Reputational damage is a secondary effect of any major cybersecurity incident

**Template Description**:
```
A widely publicized cybersecurity incident involving [specify underlying harm: safety failure, data breach, vehicle unavailability] 
severely damages OEM brand reputation. Media coverage ([specify scale: regional, national, international]) 
erodes customer trust in vehicle security and safety. Financial impact is [3-4] due to: (1) lost vehicle sales over [timeframe], 
(2) stock price decline affecting market valuation, (3) increased customer acquisition costs to rebuild trust, (4) competitive 
disadvantage vs. competitors with stronger security reputation. Brand damage persists for years after the incident, making this 
a Critical (4) financial impact for major incidents (e.g., large-scale safety failure or massive data breach).
```

---

## Pattern 11: Incorrect Environment Perception

**Damage Description**: Vehicle sensor inputs or derived perception state are incorrect, causing ADAS or automated systems to misinterpret the environment and make unsafe decisions.

**Typical SFOP Dimensions Affected**:
- **Safety**: Moderate to Critical (2-4) - Depends on ADAS response and driving context
- **Financial**: Moderate to Severe (2-3) - Liability for crashes, potential recall
- **Operational**: Moderate (2) - ADAS may disable or degrade, but manual driving available
- **Privacy**: Negligible (1) - No data exposure

**Typical Impact Score Range**: 2-4 (Moderate to Critical, depends on ADAS level)

**Example Assets** (from asset_list.md):
- AST-SNS-001: GNSS Receiver - Incorrect position or timing information
- AST-SNS-003: Driver Monitoring Camera - Incorrect driver state or image information
- AST-ECU-001: Head Unit System-on-Chip - Processes sensor data

**Template Description**:
```
Vehicle [specify sensor/perception input: camera, radar, lidar, GNSS, fused object list] receives or derives incorrect data causing [specify ADAS function: adaptive cruise control, 
lane keeping, emergency braking, navigation] to [specify unsafe behavior: brake unexpectedly, fail to brake, steer incorrectly, 
provide wrong directions]. Safety impact is [2-4 based on automation level and speed]. For Level 2 ADAS with driver supervision, 
Safety = Moderate (2-3) as driver can intervene. For higher automation levels, Safety = Severe to Critical (3-4). Financial impact 
is Moderate to Severe (2-3) due to crash liability and potential recall if vulnerability is widespread.
```

---

## Pattern 12: Cryptographic Key Disclosure

**Damage Description**: Vehicle cryptographic keys (firmware signing, TLS certificates, immobilizer keys) are disclosed or no longer trustworthy, enabling unauthorized future use.

**Typical SFOP Dimensions Affected**:
- **Safety**: Negligible to Moderate (1-2) - Enabler for future safety-impacting harm
- **Financial**: Severe (3) - Recall to replace keys, certificate revocation costs
- **Operational**: Moderate (2) - Key rotation may temporarily disrupt services
- **Privacy**: Severe (3) - Keys may protect user data; disclosure enables decryption

**Typical Impact Score Range**: 3 (Severe)

**Example Assets** (from asset_list.md):
- AST-DAT-003: Cryptographic Keys & Certificates
- AST-ECU-005: HSM/TEE Security Module

**Template Description**:
```
Cryptographic keys used for [specify purpose: firmware signing, TLS connections, immobilizer authentication, data encryption] 
are disclosed or no longer trustworthy. This enables future unauthorized use such as: (1) accepting untrusted firmware as legitimate, 
(2) decryption of encrypted user data, (3) unauthorized vehicle access, (4) impersonation of secure communications. 
Financial impact is Severe (3) due to mandatory key rotation across entire vehicle fleet, certificate revocation costs, and 
potential recall to replace hardware security modules. Privacy impact is Severe (3) if keys protect user data, as past encrypted 
data can now be decrypted. This is an "enabler" damage scenario that facilitates other, potentially more severe scenarios.
```

---

## Using Patterns in Combination

**Note**: A single asset CIA violation may trigger MULTIPLE damage scenarios. For example:

**Asset**: AST-ECU-001 (Head Unit SoC) with CIA rating C:3 / I:4 / A:3

**Potential Damage Scenarios**:
1. **Pattern 4** (PII Exposure) - From C=3: User data disclosure → DS-IVI-001
2. **Pattern 5** (Location Tracking) - From C=3: GPS history tracking → DS-IVI-002
3. **Pattern 2** (Unintended Braking) - From I=4: Unintended braking behavior → DS-CAN-001
4. **Pattern 1** (Immobilization) - From A=3: Vehicle startup prevented → DS-IVI-003

**Best Practice**: Create separate DS entries for each distinct harm event, even if they originate from the same asset CIA violation.

---

## Pattern Selection Guide

| If the damage involves... | Use Pattern |
|---------------------------|-------------|
| Vehicle won't start | #1 (Immobilization) |
| Loss of vehicle control | #2 (Accel/Brake), #3 (Steering) |
| Personal data exposed | #4 (PII Exposure) |
| Location surveillance | #5 (Location Tracking) |
| Unauthorized charges | #6 (Financial Theft) |
| Extortion-linked vehicle unavailability | #7 (System Unavailable with Extortion Demand) |
| False driver information | #8 (Display Misinformation) |
| Regulatory penalties | #9 (Non-Compliance) |
| Media coverage of hack | #10 (Reputational Damage) |
| ADAS malfunctions | #11 (Incorrect Environment Perception) |
| Disclosed security credentials | #12 (Key Disclosure) |

---

## Customization Checklist

When adapting a pattern:

- [ ] Replace generic asset references with specific AST-IDs from your asset_list.md
- [ ] Adjust SFOP scores based on your vehicle's specific capabilities and architecture
- [ ] Add system-specific details (protocols, ECU names, data types)
- [ ] Update regulatory references to match target markets (EU, China, US)
- [ ] Customize impact justifications with quantitative estimates where possible
- [ ] Ensure DS-ID domain code matches the primary affected system
- [ ] Verify all linked assets are documented in asset_list.md
