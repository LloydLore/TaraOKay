# CAN Domain - Example Threat Scenarios

> ⚠️ **PEDAGOGICAL REFERENCE EXAMPLES**
>
> These examples demonstrate evidence-rich threat scenarios using the full template from `/assets/TEMPLATE.md`. They are pedagogical references, not the minimum required output for day-to-day execution.
>
> **Production Use Guidance:**
> - These examples use realistic attack scenarios but are tailored for demonstration purposes
> - For production threat scenarios in your own TARA work, adapt the template and methodology to your specific item definition and damage scenario catalogue
> - Always cross-reference with authoritative sources:
>   - `/assets/TEMPLATE.md` — Core required fields plus optional metadata structure
>   - `/references/afr-guide.md` — AFR scoring methodology and factor definitions
>   - `/references/framework-mapping.md` — UN R155 Annex 5 and OWASP Mobile 2024 canonical definitions
>   - `/references/ts-schema.md` — Detailed field descriptions and validation rules
>
> **AFR scoring and OWASP mappings have been updated to current methodology (2026-03-19).**

This file demonstrates 3 complete threat scenario entries for the CAN (Controller Area Network) domain. Use these as reference when creating your own threat scenarios.

---

## TS-CAN-001: CAN Bus Message Injection via Compromised Head Unit

**Threat Description**:
An attacker compromises the IVI head unit (AST-ECU-001) through a malicious application or exploited vulnerability, then uses privileged access to inject crafted CAN messages onto the vehicle's internal CAN bus (AST-COM-001). The injected messages spoof legitimate ECU communications, causing unintended vehicle behavior such as:
- Disabling safety systems (ABS, ESC)
- Triggering dashboard warning lights
- Altering instrument cluster readings
- Interfering with ADAS functions

The attack exploits the lack of message authentication on traditional CAN buses, where any ECU with bus access can transmit arbitrary frames that other ECUs will process as legitimate.

Attack prerequisites:
1. Root/privileged access to IVI head unit (AST-ECU-001)
2. Knowledge of target CAN message IDs and data formats
3. Physical or persistent remote access to vehicle
4. CAN transceiver capability on compromised ECU

Attack steps:
1. Gain privileged access to IVI head unit via CVE-2019-2215 (Android kernel privilege escalation)
2. Install custom CAN frame injection tool on compromised head unit
3. Reverse engineer target CAN message formats through bus sniffing
4. Craft malicious CAN frames mimicking safety-critical ECU messages
5. Inject frames onto CAN bus (AST-COM-001) at precise timing intervals
6. Observe vehicle behavior and adjust injection parameters for desired effect

Impact chain:
TS-CAN-001 → DS-CAN-001 (CAN message spoofing) → Loss of vehicle control / Safety system malfunction → Potential collision, injury, or death

Mitigating factors:
- CAN message authentication (e.g., AUTOSAR SecOC, MACsec for Automotive Ethernet gateways)
- IVI security hardening (kernel lockdown, application sandboxing, code signing)
- Intrusion detection systems (IDS) monitoring CAN traffic for anomalous patterns
- Network segmentation isolating safety-critical CAN domains from infotainment

**Target Asset**:
AST-COM-001: CAN Bus Network - Primary target for spoofed message injection originating from a compromised head unit ECU on the in-vehicle network

**Attack Surface / Entry Point**:
Compromised IVI head unit (AST-ECU-001) via malicious app or exploited vulnerability. The attacker leverages privileged access on the head unit to transmit CAN frames through its onboard transceiver, with persistent access enabling repeated injection attempts.

**STRIDE Category**:
Spoofing, Tampering

**UN R155 Annex 5 Reference**:
4.3.2, 4.3.6

**MITRE ATT&CK Reference**:
T0855 (Unauthorized Command Message) - Injecting malicious CAN commands to actuators and ECUs

**OWASP Reference**:
N/A (hardware-focused CAN bus attack)

**Damage Scenario Categories**:
- DS-CAN-001 (Safety-critical CAN message spoofing)
- DS-IVI-003 (Unauthorized vehicle control via IVI)

**Attack Feasibility Rating (AFR)**:
AFR: 10 (Moderate)
- Elapsed Time: 3 (< 1 week) - Can be executed within hours once IVI access is gained
- Specialist Expertise: 1 (Expert in automotive cybersecurity) - Requires CAN protocol knowledge and reverse engineering skills
- Knowledge of Item: 1 (Confidential / limited access) - Needs CAN frame database obtainable via reverse engineering
- Window of Opportunity: 3 (Unlimited / always accessible) - Persistent access via compromised IVI
- Equipment: 2 (Standard automotive tools) - CAN adapter and laptop with free software

**CIA Triad**:
I (Integrity) - Spoofed messages compromise the integrity of ECU communications and vehicle state

**Real-world Examples / CVEs**:
- CVE-2019-2215 (Android kernel privilege escalation used to compromise IVI)
- Miller, C., & Valasek, C. (2015). "Remote Exploitation of an Unaltered Passenger Vehicle" (CAN injection demonstration)
- ISO 21434:2021 Clause 15.6 (Threat scenario identification)
- MITRE ATT&CK ICS T0855 (Unauthorized Command Message)

**Last Updated**:
2026-03-19

**Confidence Level**:
High - CAN message injection is well documented in academic and industry demonstrations once an ECU gains bus access

**Affected Vehicle Systems**:
- CAN Bus Network (AST-COM-001) - Injection target
- Head Unit SoC (AST-ECU-001) - Compromised source of injected traffic
- Instrument Cluster ECU (AST-ECU-003) - Spoofed status/alerts
- ADAS ECU (AST-ECU-006) - Potentially manipulated sensor/actuator messages

**Attack Vector**: L (Local) - Requires code execution on an in-vehicle ECU (compromised head unit) to inject onto CAN


---

## TS-CAN-002: CAN Bus Denial of Service via OBD-II Port Flooding

**Threat Description**:
An attacker with physical access to the OBD-II diagnostic port floods the vehicle's CAN bus (AST-COM-001) with high-priority frames, saturating the network and preventing legitimate ECU communications. The attack leverages the priority-based arbitration mechanism of CAN, where high-priority (low CAN ID) messages dominate bus access.

This creates a sustained denial-of-service condition causing:
- Loss of real-time control communications between ECUs
- ECU timeout errors and fault codes
- Degraded or disabled safety systems (ABS, ESC, airbags)
- Potential vehicle immobilization or unsafe operating states

The attack requires only physical access to the OBD-II port (accessible from inside the vehicle cabin) and inexpensive commercial CAN hardware.

Attack prerequisites:
1. Physical access to vehicle interior (OBD-II port location)
2. OBD-II to CAN adapter hardware ($20-50 commercial devices)
3. CAN flooding software (e.g., cansniffer, can-utils)

Attack steps:
1. Locate OBD-II port (typically under dashboard near driver's seat)
2. Connect CAN adapter to OBD-II port
3. Identify active CAN bus channel (usually CAN-H/CAN-L on pins 6/14)
4. Launch CAN frame flooding attack using highest priority CAN ID (0x000)
5. Sustain flood to maintain denial-of-service condition
6. Optionally: leave hardware installed for persistent remote activation

Impact chain:
TS-CAN-002 → DS-CAN-002 (CAN DoS) + DS-CAN-004 (ECU timeout) → Safety system malfunction → Loss of vehicle control, potential collision

Mitigating factors:
- Physical OBD-II port protection (locking cover, relocation to secured compartment)
- CAN traffic rate limiting and anomaly detection
- Segregated diagnostic CAN channel with gateway filtering
- OBD-II port disable/lockout when vehicle is in motion

**Target Asset**:
AST-COM-001: CAN Bus Network - Targeted by high-priority frame flooding that prevents legitimate ECU communications

**Attack Surface / Entry Point**:
OBD-II diagnostic interface (AST-IFC-001) accessible inside the vehicle cabin. Attacker connects a CAN adapter and injects high-priority frames directly onto the bus.

**STRIDE Category**:
Denial of Service

**UN R155 Annex 5 Reference**:
4.3.2, 4.3.7

**MITRE ATT&CK Reference**:
T0814 (Denial of Service) - Flooding the communication bus to prevent legitimate traffic

**OWASP Reference**:
N/A (hardware-focused CAN bus attack)

**Damage Scenario Categories**:
- DS-CAN-002 (CAN bus denial of service)
- DS-CAN-004 (ECU communication timeout)

**Attack Feasibility Rating (AFR)**:
AFR: 11 (Moderate)
- Elapsed Time: 3 (< 1 week) - Immediate effect once tool is connected
- Specialist Expertise: 2 (Proficient IT/cybersecurity professional) - Basic CAN protocol understanding
- Knowledge of Item: 3 (Publicly available / common knowledge) - OBD-II pinout and CAN bus architecture widely documented
- Window of Opportunity: 1 (Moderate access window) - Requires brief physical access to vehicle interior
- Equipment: 2 (Standard automotive tools) - Commercial OBD-II CAN adapter and open-source flooding tools

**CIA Triad**:
A (Availability) - Flooding prevents legitimate CAN traffic and ECU control messages

**Real-world Examples / CVEs**:
- No public CVE - OBD-II CAN flooding vulnerability (Security research and commodity tools demonstrate feasibility)
- Studnia, I., et al. (2020). "Survey on Security Threats and Protection Mechanisms in Embedded Automotive Networks" (CAN DoS taxonomy)
- ISO 21434:2021 Clause 15.7 (Attack path analysis)
- MITRE ATT&CK ICS T0814 (Denial of Service)

**Last Updated**:
2026-03-19

**Confidence Level**:
High - OBD-II CAN flooding is a widely demonstrated attack with commodity tools and consistent effects

**Affected Vehicle Systems**:
- CAN Bus Network (AST-COM-001) - Flooded communication channel
- OBD-II Diagnostic Interface (AST-IFC-001) - Physical entry point
- Engine Control ECU (AST-ECU-004) - Loses real-time control communications
- Instrument Cluster ECU (AST-ECU-003) - Fault codes and warning indicators triggered

**Attack Vector**: L (Local) - Requires access to vehicle cabin/OBD-II port (no hardware teardown)


---

## TS-CAN-003: CAN Frame Injection via Compromised Gateway ECU Firmware

**Threat Description**:
An attacker exploits a firmware update vulnerability in the central gateway ECU (AST-GW-001) to install malicious firmware that injects crafted CAN messages onto multiple vehicle networks. The gateway ECU is a critical asset that bridges different CAN domains (powertrain, chassis, body, infotainment), making it an ideal pivot point for cross-domain attacks.

The malicious firmware can:
- Inject spoofed messages onto safety-critical CAN buses
- Modify legitimate messages in transit (man-in-the-middle)
- Create backdoor remote access via connected interfaces
- Persist across vehicle power cycles

This attack is particularly severe because the gateway has legitimate access to all CAN domains and operates with high privilege, making injected messages difficult to distinguish from legitimate traffic.

Attack prerequisites:
1. Vulnerability in gateway ECU firmware update mechanism
2. Ability to reverse engineer and modify gateway firmware
3. Access to firmware update interface (OBD-II, OTA, or service tool)
4. Knowledge of CAN frame formats for target vehicle

Attack steps:
1. Identify vulnerability in gateway ECU firmware update process (e.g., insufficient signature validation - documented in automotive security research)
2. Extract legitimate gateway firmware via service tool or physical extraction
3. Reverse engineer firmware to locate CAN transmission routines
4. Develop malicious firmware payload with CAN injection logic
5. Bypass firmware signature validation (no public CVE - hypothetical improper signature verification)
6. Flash compromised firmware to gateway ECU via OBD-II or wireless update
7. Activate malicious CAN injection payload remotely or via trigger condition

Impact chain:
TS-CAN-003 → DS-CAN-003 (Gateway compromise) → DS-CAN-001 (Message spoofing) → Unintended braking/acceleration → Loss of vehicle control, collision

Mitigating factors:
- Secure boot with hardware root of trust
- Firmware signature validation with revocation checking
- Encrypted and authenticated firmware update channels
- Runtime integrity monitoring and watchdog timers
- Firmware rollback protection

**Target Asset**:
AST-GW-001: Central Gateway ECU - High-privilege firmware target that bridges multiple CAN domains

**Attack Surface / Entry Point**:
Gateway firmware update interface via OBD-II, OTA update pipeline, or service tool. The attacker exploits insufficient signature validation or update authentication to install malicious firmware.

**STRIDE Category**:
Spoofing, Tampering, Elevation of Privilege

**UN R155 Annex 5 Reference**:
4.3.3, 4.3.4

**MITRE ATT&CK Reference**:
T0857 (System Firmware) - Compromising gateway firmware to gain control and inject CAN messages

**OWASP Reference**:
N/A (hardware-focused CAN bus attack)

**Damage Scenario Categories**:
- DS-CAN-003 (Gateway ECU compromise)
- DS-CAN-001 (Safety-critical CAN message spoofing)

**Attack Feasibility Rating (AFR)**:
AFR: 5 (Low)
- Elapsed Time: 1 (1-6 months) - Requires vulnerability research and firmware development
- Specialist Expertise: 1 (Expert in automotive cybersecurity) - Requires firmware reverse engineering and exploit development
- Knowledge of Item: 0 (Restricted / classified) - Needs gateway firmware internals and signing keys, requires insider access or espionage
- Window of Opportunity: 2 (Easy access / extended time) - Firmware updates often accessible via OBD-II or wireless
- Equipment: 1 (Specialized but purchasable) - Firmware extraction tools, debugger, JTAG hardware

**CIA Triad**:
I+A (Integrity + Availability) - Firmware compromise enables message tampering and potential system disruption

**Real-world Examples / CVEs**:
- No public CVE - Gateway ECU firmware update vulnerability (Security research demonstrates signature bypass attacks)
- No public CVE for automotive bootloader signature bypass - hypothetical based on common firmware validation weaknesses
- Nie, S., et al. (2017). "Free-Fall: Hacking Tesla from Wireless to CAN Bus" (Gateway pivot attack demonstration)
- ISO 21434:2021 Clause 15.6 (Threat scenario identification)
- MITRE ATT&CK Enterprise T1195.002 (Compromise Software Supply Chain: Firmware)

**Last Updated**:
2026-03-19

**Confidence Level**:
High - Gateway firmware compromise and CAN injection have been demonstrated in research (e.g., Tesla gateway pivot) with real-world CVEs

**Affected Vehicle Systems**:
- Central Gateway ECU (AST-GW-001) - Compromised firmware target
- CAN Bus Network (AST-COM-001) - Multi-domain injection surface
- Engine Control ECU (AST-ECU-004) - Safety-critical powertrain effects
- Electronic Brake Actuator (AST-ACT-003) - Safety-critical chassis effects

**Attack Vector**: N (Network) - OTA firmware update channel can be compromised remotely if update authentication is weak
