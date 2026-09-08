# Example: CAN Bus Damage Scenarios

This example demonstrates how to derive safety-critical damage scenarios from CAN bus and vehicle network assets using the damage_scenario skill workflow.

---

## Context

**Source Assets**: From `data/asset_list.md`, we focus on CAN bus and network-related assets that could lead to safety-critical damage scenarios.

**Key CAN/Network Assets**:
- AST-COM-001: CAN-FD Bus - C:2 / I:4 / A:3
- AST-ECU-006: Gateway ECU (Automotive Ethernet Switch) - C:2 / I:4 / A:4
- AST-ECU-001: Head Unit System-on-Chip (QAM8295) - C:3 / I:4 / A:3

**CIA Triage Process**:
1. Identify assets with high Integrity (I=4) and CAN/vehicle network access → ask whether incorrect vehicle states can create Safety damage scenarios
2. Identify assets with high Availability (A=3 or A=4) for critical communications → ask Operational + Safety questions based on redundancy and affected functions
3. CAN domain typically has high Safety scores (3-4) due to safety-critical ECU connectivity

---

## Damage Scenario 1: Unintended Vehicle Behavior

### Derivation

**Asset**: AST-ECU-001 (Head Unit SoC) with C:3 / I:4 / A:3  
**Asset**: AST-COM-001 (CAN-FD Bus) with C:2 / I:4 / A:3

**CIA Analysis**:
- Head Unit has CAN-FD interface (per asset_list.md: "CAN-FD Bus Interface (AST-COM-001) via CAIF1043/1044 transceivers")
- High Integrity (I=4) - Tampering with CAN messages could affect vehicle behavior
- User confirmed: "Does not send commands to safety ECUs, only data queries and status updates"
- Boundary question: if design constraints fail, could incorrect vehicle states be accepted by downstream ECUs?

**Interview Questions Used**:
- Q: "If the Head Unit SoC outputs incorrect vehicle network states, can downstream ECUs accept them?"
- A: Hardware interface exists; the impact depends on gateway filtering and receiving ECU acceptance rules
- Q: "What vehicle ECUs are connected via CAN-FD through the Gateway?"
- A: ADAS, Body Control, Powertrain (per user context about gateway connectivity)
- Q: "What is the worst-case reasonable impact of incorrect vehicle-control states?"
- A: Unintended braking, acceleration, or steering depending on gateway filtering

**SFOP Assessment**:
- Safety: 3-4 (Depends on what commands are accepted by downstream ECUs)
- Financial: 3 (Major liability, potential recall)
- Operational: 3-4 (Critical functions could be disrupted)
- Privacy: 1 (No data exposure)

**Overall Impact**: 4 (Critical) [driven by Safety]

---

### DS-CAN-001: Unintended Vehicle Behavior During Operation

**Linked Assets**:
- AST-ECU-001: Head Unit System-on-Chip (QAM8295)
- AST-COM-001: CAN-FD Bus
- AST-ECU-006: Gateway ECU (Automotive Ethernet Switch)

**SFOP Dimensions Affected**:
- **Safety**: Yes - Incorrect vehicle-control states accepted by safety-critical ECUs (via Gateway) could cause unintended acceleration, braking, or steering behavior, resulting in loss of vehicle control and high probability of collision with injury or fatality
- **Financial**: Yes - Liability for injuries and property damage, mandatory safety recall, regulatory investigation under UN R155, substantial legal defense costs, and severe brand reputation damage
- **Operational**: Yes - Safety-critical vehicle functions could be disrupted or disabled, making the vehicle unsafe to operate until ECUs are reflashed with hardened firmware
- **Privacy**: No - Incorrect vehicle-control states do not involve personal data exposure

**Impact Score**: 4 (Critical)
- Safety: 4 (Critical) - Loss of vehicle control, high fatality risk
- Financial: 3 (Severe) - Major liability, recall, regulatory fines
- Operational: 3 (Severe) - Safety functions disrupted
- Privacy: 1 (Negligible) - No data exposure

Overall Impact: 4 (Critical) [max of S=4, F=3, O=3, P=1]

**Assessment Context**:
- **Assumptions**: Gateway filtering or downstream ECU acceptance rules allow incorrect vehicle-control states to affect safety-relevant behavior.
- **Operating Conditions**: Highway operation above 80 km/h is used as the worst-case reasonable safety context.
- **Population / Scale**: Potential fleet-scale design condition; financial rationale assumes up to 100,000 affected vehicles.
- **Duration / Recoverability**: Persistent until ECU firmware, gateway filtering, or message-validation remediation is deployed.
- **Evidence / Source**: AST-ECU-001, AST-COM-001, AST-ECU-006, gateway connectivity interview, ISO 26262 safety context.

**Rationale**:

**Safety (4 - Critical)**: Incorrect vehicle-control states reaching safety-critical ECUs via the physical CAN interface (AST-COM-001) could create unintended acceleration, sudden braking, steering angle changes, or disabling of safety functions. While the user confirmed that the Head Unit normally sends only data queries and status updates, this damage scenario records the harm if architecture assumptions or filtering fail and downstream ECUs accept incorrect states through the Gateway ECU (AST-ECU-006). At highway speeds above 80 km/h, any of these behaviors creates extremely high probability of collision resulting in severe injuries or fatalities to vehicle occupants and potentially other road users. This represents the highest safety impact category under ISO 21434 and ISO 26262 ASIL-D failure modes. The rating is Critical (4) because the accepted incorrect vehicle-control state can directly affect safety-critical vehicle functions with life-threatening consequences.

**Financial (3 - Severe)**: Unintended vehicle behavior resulting in crashes would create major liability exposure for the OEM. Tort liability for injuries and fatalities could reach tens of millions of dollars per incident, with potential for multiple affected vehicles if the condition is systematic. A mandatory safety recall under NHTSA (US) or Type Approval authorities (EU, China) would be required to reflash or replace affected ECUs with hardened firmware, costing $500-$1,000 per vehicle in service center labor and logistics. For a fleet of 100,000 affected vehicles, recall costs alone could reach $50M-$100M. Regulatory investigation under UN R155 (Cybersecurity and CSMS) could result in fines or suspension of type approval, preventing future vehicle sales until remediation. Legal defense costs for injury litigation would be substantial ($10M-$50M). Brand reputation damage from a high-profile safety failure would be severe, potentially causing years of lost sales and market share decline as customers lose trust in vehicle safety. The combined liability, recall, regulatory, legal, and reputation costs rate this as Severe (3) financial impact, approaching but not quite reaching Critical (4) which would represent business-threatening losses (>$500M or bankruptcy risk).

**Operational (3 - Severe)**: Accepted incorrect vehicle-control states create unreliable and unsafe vehicle operation. Safety-critical functions including braking, steering, acceleration control, and ADAS features become untrustworthy because vehicle behavior may diverge from driver intent. The vehicle cannot be safely operated until the condition is remediated through ECU firmware updates, filtering changes, message authentication, or input validation. While the vehicle may remain physically drivable in the short term, it represents an unacceptable safety risk. Operational impact is rated Severe (3) because critical vehicle functions are unreliable, requiring mandatory service intervention to restore safe operation. The rating is not Critical (4) because the vehicle is not completely immobilized - it can still physically move - but it cannot be safely used, which is nearly equivalent.

**Privacy (1 - Negligible)**: Incorrect vehicle-control states and diagnostic data do not involve access to or disclosure of user personal information. The CAN bus carries operational data (vehicle speed, engine RPM, brake pressure) but not PII such as contacts, location history, or user identities in this example. No personal data is exposed to unauthorized parties through this harm. Therefore, privacy impact is Negligible. If vehicle network data includes linkable location or user data, that would be documented as a separate privacy damage scenario.

---

## Damage Scenario 2: Vehicle Network Communication Unavailable

### Derivation

**Asset**: AST-COM-001 (CAN-FD Bus) with C:2 / I:4 / A:3

**CIA Analysis**:
- High Availability (A=3) - CAN bus unavailability disrupts critical vehicle communications
- CAN bus connects infotainment to Gateway (AST-ECU-006)
- Gateway connects to safety-critical ECUs (per user context)
- Loss of CAN availability → Loss of vehicle network communication

**Interview Questions Used**:
- Q: "What happens if the CAN-FD bus becomes unavailable?"
- A: ECUs cannot communicate; diagnostic messages fail; displays may lose data
- Q: "Are safety functions affected by CAN-FD bus unavailability?"
- A: Depends on redundancy; some vehicles have separate CAN buses for safety vs infotainment
- Q: "Can the vehicle be driven if CAN-FD to infotainment is disabled?"
- A: Yes, but with degraded functionality (no displays, warnings, diagnostics)

**SFOP Assessment**:
- Safety: 2-3 (Driver loses warning lights, displays; safety systems may degrade)
- Financial: 2 (Recovery costs, service disruption)
- Operational: 3-4 (Critical communications lost, vehicle function degraded)
- Privacy: 1 (No data exposure)

**Overall Impact**: 3-4 (Severe to Critical)

---

### DS-CAN-002: Vehicle Network Communication Unavailable

**Linked Assets**:
- AST-COM-001: CAN-FD Bus
- AST-ECU-001: Head Unit System-on-Chip (QAM8295) - connected to CAN-FD
- AST-ECU-006: Gateway ECU (Automotive Ethernet Switch) - routes CAN traffic

**SFOP Dimensions Affected**:
- **Safety**: Yes - CAN bus unavailability prevents critical diagnostic warnings from reaching instrument cluster displays, and may degrade ADAS or safety functions if CAN is used for safety-critical inter-ECU communication
- **Financial**: Yes - Service center visits required to diagnose and recover from persistent CAN communication unavailability, potential warranty claims, and customer dissatisfaction costs
- **Operational**: Yes - Vehicle network communication disrupted, causing loss of instrument cluster displays (speed, fuel, warnings), diagnostic failures, and potential degradation of vehicle functions that rely on CAN messaging
- **Privacy**: No - Communication unavailability blocks communication but does not expose personal data

**Impact Score**: 4 (Critical)
- Safety: 3 (Severe) - Loss of warnings and potential safety function degradation
- Financial: 2 (Moderate) - Service costs, warranty claims
- Operational: 4 (Critical) - Critical communication channel blocked
- Privacy: 1 (Negligible) - No data exposure

Overall Impact: 4 (Critical) [max of S=3, F=2, O=4, P=1]

**Assessment Context**:
- **Assumptions**: CAN-FD bus unavailability affects instrument cluster data, diagnostics, and potentially ADAS-related communication in this architecture.
- **Operating Conditions**: Vehicle remains physically drivable but loses displays, warnings, diagnostics, and some integrated functions.
- **Population / Scale**: Service-disruption example assumes approximately 1,000 vehicles.
- **Duration / Recoverability**: Persistent until service diagnosis and ECU/transceiver/network remediation.
- **Evidence / Source**: AST-COM-001, AST-ECU-001, AST-ECU-006, interview responses on redundancy and drivability.

**Rationale**:

**Safety (3 - Severe)**: If the CAN-FD bus (AST-COM-001) connecting the Head Unit to the Gateway ECU (AST-ECU-006) is unavailable, several safety-relevant impacts occur: (1) Instrument cluster displays (AST-ACT-003) lose vehicle data from the CAN bus, preventing display of speed, fuel level, and warning lights (check engine, brake system, ABS), (2) Driver loses situational awareness - not knowing current speed creates crash risk, (3) Critical fault warnings (e.g., brake system failure, low tire pressure) cannot be communicated to the driver, delaying response to vehicle malfunctions. While the core driving controls (steering, braking, acceleration via direct mechanical/hydraulic linkages) may continue to function, the loss of feedback and warnings degrades safety. If safety-critical ECUs also use the same CAN bus for inter-ECU communication (not clear from asset list, but common in some architectures), then ADAS and safety functions could be directly disrupted. Safety impact is rated Severe (3) because the loss of warnings and displays creates significant crash risk, though not as directly life-threatening as loss of steering/braking control itself (which would be Critical 4).

**Financial (2 - Moderate)**: Vehicle network communication unavailability causes service disruption costs but not catastrophic financial losses in this example. Affected vehicles require diagnosis at service centers to identify and remediate the communication failure source, whether through ECU reflash, CAN transceiver replacement, or network reconfiguration. Service costs are approximately $200-$500 per vehicle. If the condition affects 1,000 vehicles, total service costs could reach $500K. Customer dissatisfaction from loss of vehicle functionality may trigger warranty claims or goodwill compensations ($100-$1,000 per customer). There is no major regulatory fine exposure in this example because the condition is treated as a service disruption rather than confirmed safety defect or data breach. Brand reputation impact is moderate. The financial impact is rated Moderate (2), representing manageable costs in the $1M-$10M range for remediation and customer compensation.

**Operational (4 - Critical)**: CAN bus is a critical vehicle network that enables communication between ECUs, sensors, actuators, and displays. CAN-FD bus unavailability results in complete loss of network functionality for all connected systems. Specific operational impacts include: (1) Instrument cluster displays go blank or freeze, showing no speed, fuel, warnings, or telltale lights, (2) Navigation system cannot receive vehicle data (speed, odometer, turn signals), (3) Infotainment system loses integration with vehicle functions, (4) Diagnostic systems (OBD-II) cannot query ECUs for fault codes, (5) Advanced features (adaptive cruise control, lane keeping) may disable if they rely on CAN messaging. The vehicle remains physically drivable (engine runs, steering and braking work via direct control paths), but the loss of critical communication infrastructure severely degrades vehicle functionality and makes the vehicle unsuitable for normal use. This meets the definition of Critical (4) operational impact under ISO 21434 - a critical subsystem is completely non-functional. The rating is not reduced despite physical drivability because the CAN bus is an essential component for modern vehicle operation, and its complete unavailability represents a critical system failure.

**Privacy (1 - Negligible)**: Vehicle network communication unavailability blocks communication, preventing legitimate messages from being transmitted or received. This is an availability harm, not a confidentiality harm. No personal data is disclosed or exfiltrated. The CAN bus carries vehicle operational data (speed, RPM, diagnostics) but not user PII in this example. Therefore, privacy impact is Negligible for this communication-unavailability scenario.

---

## Damage Scenario 3: Vehicle Network Isolation

### Derivation

**Asset**: AST-ECU-006 (Gateway ECU / Automotive Ethernet Switch) with C:2 / I:4 / A:4

**CIA Analysis**:
- Gateway ECU is critical network chokepoint connecting infotainment to vehicle networks
- High Availability (A=4) - Gateway failure isolates networks
- High Integrity (I=4) - Incorrect gateway behavior could cause unauthorized routing or blocking

**Interview Questions Used**:
- Q: "What happens if the Gateway ECU routes or blocks vehicle network traffic incorrectly?"
- A: Infotainment or safety networks can become isolated from required communication
- Q: "What vehicle networks are connected through the Gateway?"
- A: CAN-FD (infotainment), Automotive Ethernet, and potentially other CAN buses to ADAS/Body Control
- Q: "Can the vehicle operate if Gateway ECU fails?"
- A: Partial operation - some ECUs may be isolated and unable to communicate

**SFOP Assessment**:
- Safety: 2-3 (Network isolation could disable warnings or ADAS features)
- Financial: 3 (Recall to fix gateway security, liability if safety impact)
- Operational: 4 (Critical network infrastructure unavailable or incorrectly isolating domains)
- Privacy: 1 (No direct data exposure, though eavesdropping is possible)

**Overall Impact**: 4 (Critical)

---

### DS-CAN-003: Vehicle Network Isolation

**Linked Assets**:
- AST-ECU-006: Gateway ECU (Automotive Ethernet Switch)
- AST-COM-001: CAN-FD Bus
- AST-ECU-001: Head Unit System-on-Chip (QAM8295) - connected via Gateway

**SFOP Dimensions Affected**:
- **Safety**: Yes - Incorrect Gateway routing or blocking can isolate safety-critical ECUs from receiving necessary data (sensor inputs, diagnostic information), potentially degrading ADAS or safety function performance
- **Financial**: Yes - Gateway remediation requires fleet-wide firmware update or ECU replacement, potential recall under UN R155, and liability if isolation causes safety incidents
- **Operational**: Yes - Gateway is critical network infrastructure connecting multiple vehicle networks; isolation disrupts essential inter-ECU communication
- **Privacy**: No - Network isolation does not directly expose user personal data; data disclosure would be a separate scenario

**Impact Score**: 4 (Critical)
- Safety: 3 (Severe) - Network isolation degrades safety functions
- Financial: 3 (Severe) - Fleet-wide gateway remediation, potential recall
- Operational: 4 (Critical) - Critical network infrastructure unavailable or incorrectly isolating domains
- Privacy: 1 (Negligible) - No direct PII exposure

Overall Impact: 4 (Critical) [max of S=3, F=3, O=4, P=1]

**Assessment Context**:
- **Assumptions**: Gateway ECU is the central routing point between infotainment, CAN-FD, Automotive Ethernet, and safety-relevant vehicle networks.
- **Operating Conditions**: Vehicle may remain locally drivable, but integrated cross-domain functions and diagnostics are disrupted.
- **Population / Scale**: Fleet-scale remediation example assumes up to 100,000 affected vehicles.
- **Duration / Recoverability**: Persistent until gateway firmware update, configuration fix, or ECU replacement.
- **Evidence / Source**: AST-ECU-006, AST-COM-001, AST-ECU-001, network topology interview, UN R155 remediation rationale.

**Rationale**:

**Safety (3 - Severe)**: The Gateway ECU (AST-ECU-006) is the central routing device connecting the infotainment subsystem (via CAN-FD and Automotive Ethernet) to other vehicle networks that reach ADAS, Body Control, and potentially Powertrain ECUs. Incorrect Gateway routing or blocking can selectively drop critical network messages, creating network isolation. Specific safety impacts include: (1) ADAS ECUs may be isolated from receiving sensor data (camera, radar feeds from infotainment-side sensors), degrading automated braking or lane keeping functionality, (2) Diagnostic warning messages from safety ECUs (brake system faults, ABS malfunctions) could be blocked from reaching the infotainment displays, preventing driver awareness of safety issues, (3) Vehicle-to-X (V2X) safety messages (if routed through Gateway) could be dropped, reducing cooperative safety features. The safety impact is rated Severe (3) because network isolation creates conditions for safety function degradation, increasing crash risk. However, it does not rate Critical (4) because the isolation is indirect - core mechanical controls (steering, braking) typically have redundant direct pathways that do not rely on the Gateway, and isolation does not directly cause loss of vehicle control.

**Financial (3 - Severe)**: Vehicle network isolation affecting safety or network integrity would trigger a mandatory security recall under UN R155 Cybersecurity regulations, which require OEMs to remediate cybersecurity vulnerabilities that affect vehicle safety or data protection. Recall costs to reflash or replace Gateway ECUs across the affected vehicle fleet would be substantial - approximately $300-$800 per vehicle for service center labor and logistics. For a fleet of 100,000 vehicles, this represents $30M-$80M in direct recall costs. If network isolation facilitated a safety incident (crash due to ADAS degradation), liability exposure could add tens of millions in settlements. Regulatory investigation costs under UN R155 Type Approval authorities and potential fines for cybersecurity non-compliance would add $1M-$10M. Brand reputation damage from a safety-adjacent cybersecurity failure would impact customer trust and future sales. The combined recall costs, liability exposure, regulatory response, and reputation impact rate this as Severe (3) financial impact, in the range of $50M-$150M. This approaches Critical (4) but does not quite reach business-threatening levels (which would require >$500M impact).

**Operational (4 - Critical)**: The Gateway ECU is the most critical piece of network infrastructure in the vehicle architecture, serving as the central routing point for inter-ECU communication across multiple network segments (CAN-FD, Automotive Ethernet, potentially LIN, FlexRay). Gateway network isolation determines which ECUs can communicate with each other. Operational impacts include: (1) Infotainment system (Head Unit) can be completely isolated from vehicle data, losing all connectivity to sensors, actuators, and other ECUs, (2) Diagnostic systems cannot reach ECUs for fault code reading or updates, (3) OTA update delivery may be blocked if routed through Gateway, preventing security patches, (4) Cross-domain features (e.g., ADAS data displayed on infotainment screen) fail due to blocked communication. Network isolation represents a complete failure of critical network infrastructure, meeting the definition of Critical (4) operational impact. The vehicle may still be physically drivable, but the integrated vehicle system is fundamentally broken, making it unsuitable for modern vehicle operation that depends on inter-ECU coordination.

**Privacy (1 - Negligible)**: Vehicle network isolation does not directly expose user personal data. The Gateway routes CAN and Ethernet messages between ECUs but does not typically store or process user PII (contacts, location, credentials). If network traffic containing personal information is disclosed, that would be a separate privacy damage scenario (DS-IVI or DS-CAN related to privacy). This damage scenario specifically addresses network isolation/blocking, not data disclosure. Therefore, the direct privacy impact is Negligible.

---

## Summary

**CAN Domain Damage Scenarios Created**: 3  
**Asset Coverage**: 4 unique assets referenced (AST-ECU-001, AST-COM-001, AST-ECU-006)

**Key Learnings**:
1. High Integrity (I=4) assets with vehicle network access → Safety-critical damage scenarios
2. CAN domain typically has high Safety scores (3-4) due to potential impact on vehicle control
3. Gateway ECU is critical chokepoint - network isolation has cascading operational impact
4. Financial scores driven by recall costs, liability, UN R155 regulatory compliance
5. Privacy scores remain low (1) for CAN-domain availability/integrity harms unless personal data is specifically disclosed

**Comparison with IVI Domain**:
| Dimension | IVI Domain (Example 01) | CAN Domain (Example 02) |
|-----------|------------------------|------------------------|
| Safety | Low (1-2) | High (3-4) |
| Financial | High (3) | High (3) |
| Operational | Moderate (2-4) | High (3-4) |
| Privacy | High (3-4) | Low (1) |
| Overall Impact | Privacy-driven | Safety-driven |

**Next Step**: Use these DS entries as input to `threat_scenario` to identify attack paths and assess attack feasibility (AFR).
