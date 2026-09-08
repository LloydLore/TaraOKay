# Threat Scenario Patterns - Reusable Templates

This document provides reusable threat scenario patterns for common automotive cybersecurity attack vectors. Use these patterns as starting points when creating threat scenario entries in `data/ts.md`.

---

## How to Use This Document

Each pattern includes:
- **Pattern Name**: Descriptive title for the threat category
- **Domain**: Which of the 7 domains this threat applies to (CAN/OTA/EXT/BCK/IVI/IMM/ADAS)
- **Attack Description**: What the attacker does (focus on attack method and entry point)
- **Typical Attack Surface**: Where the attack originates from
- **STRIDE Category**: Which STRIDE threat type(s) apply
- **Typical AFR Range**: Expected Attack Feasibility Rating (0-15 scale → Very Low/Low/Moderate/High)
- **Example Scenario**: Concrete instance of this pattern
- **Mitigation Approaches**: Common countermeasures to reduce feasibility or impact

**Usage**: 
1. Identify which pattern(s) match your threat scenario
2. Copy the template description
3. Customize with specifics from your asset and damage scenario analysis
4. Adjust AFR scores based on implemented security controls
5. Link to specific damage scenarios (DS-IDs) this threat could cause

---

## Pattern 1: CAN Bus Message Injection

**Domain**: CAN

**Attack Description**: Attacker gains access to the vehicle CAN bus network (via compromised ECU or physical diagnostic port) and injects crafted CAN messages to trigger unintended vehicle behavior. By spoofing legitimate ECU identifiers and exploiting the broadcast nature of CAN (lack of authentication), the attacker sends commands that safety-critical ECUs execute as if from a trusted source.

**Typical Attack Surface**:
- Compromised Infotainment/Head Unit ECU with CAN-FD access (AST-ECU-001, AST-ECU-003)
- OBD-II diagnostic port (physical access)
- Compromised Gateway ECU (AST-ECU-006)
- Aftermarket devices connected to CAN bus (dashcams, telematics dongles)

**STRIDE Category**: Spoofing (attacker impersonates legitimate ECU), Tampering (manipulates vehicle state)

**Typical AFR Range**: 
- With physical access: 6-9 (Medium) - Elapsed Time: 1 day, Specialist Expertise: Proficient, Knowledge of Item: Public, Window of Opportunity: Unlimited, Equipment: Specialized
- Without physical access (remote via compromised Head Unit): 9-12 (Medium to Low) - Requires chaining multiple exploits

**Example Scenario**: 
Attacker compromises the Android partition of the Head Unit (AST-ECU-004) via a malicious app. They exploit a hypervisor vulnerability to escape into QNX (AST-ECU-003), which has direct CAN-FD access. Using publicly available CAN database files (DBC format), the attacker identifies the CAN message ID for "target vehicle speed" (used by adaptive cruise control). They inject CAN frames claiming the vehicle ahead has suddenly stopped, triggering emergency automatic braking at highway speeds, potentially causing rear-end collision.

**Mitigation Approaches**:
- CAN message authentication (CMAC per ISO 11898-1, SecOC per AUTOSAR)
- Network segmentation with authenticated gateways (isolate infotainment from safety CAN buses)
- Hypervisor hardening to prevent Android → QNX escape
- CAN intrusion detection systems (IDS) monitoring for anomalous message patterns
- Rate limiting and sequence number validation on safety-critical CAN messages

**Related Damage Scenarios**: DS-CAN-001 (Unintended Braking), DS-CAN-002 (Loss of Steering), DS-CAN-003 (Unintended Acceleration)

---

## Pattern 2: CAN Bus Denial of Service

**Domain**: CAN

**Attack Description**: Attacker floods the CAN bus with high-priority frames, consuming all available bus bandwidth and preventing legitimate ECU communication. Due to CAN's priority-based arbitration, low-priority messages (often from safety-critical systems like ADAS) are starved, causing system malfunctions or failsafe mode activation.

**Typical Attack Surface**:
- Compromised ECU with CAN transmit capability (AST-ECU-001 Head Unit)
- Physical access to OBD-II port with CAN transceiver device
- Compromised aftermarket telematics device

**STRIDE Category**: Denial of Service

**Typical AFR Range**: 4-7 (High to Medium) - Elapsed Time: <1 day, Specialist Expertise: Proficient, Knowledge of Item: Public, Window of Opportunity: Moderate, Equipment: Standard

**Example Scenario**: 
Attacker connects a rogue device to the OBD-II diagnostic port and transmits CAN frames with the highest priority identifier (CAN ID 0x000) at maximum bus rate (500 kbps for CAN, 2 Mbps for CAN-FD). All other ECUs are starved of bus access. The Gateway ECU (AST-ECU-006) cannot forward critical messages between network segments. ADAS systems enter failsafe mode and disable adaptive cruise control, lane keeping assist, and collision warning. Driver loses advanced safety features mid-journey.

**Mitigation Approaches**:
- CAN bus monitoring and rate limiting at Gateway ECU
- Anomaly detection for sustained high-priority traffic
- Physical security for OBD-II port (cover, lockable door in cabin)
- Segmented CAN architecture (separate buses for safety vs. infotainment)
- CAN-FD with flexible data rate (allows burst communication for critical messages)

**Related Damage Scenarios**: DS-CAN-004 (ADAS Degradation), DS-IVI-003 (Infotainment Denial of Service)

---

## Pattern 3: OTA Update Manipulation (Malicious Firmware)

**Domain**: OTA

**Attack Description**: Attacker compromises the OTA update mechanism to deliver malicious or tampered firmware to vehicle ECUs. This could involve man-in-the-middle attacks on the update channel, compromising the backend OTA server, or bypassing signature verification on the vehicle side. Successful firmware manipulation provides persistent attacker control over the ECU even after reboot.

**Typical Attack Surface**:
- Cellular/Telematics communication link (AST-COM-005) between vehicle and OTA backend
- Compromised OTA backend server or CDN infrastructure
- Weak or broken signature verification on vehicle side (AST-ECU-001, AST-ECU-005)
- Stolen or leaked firmware signing keys (AST-DAT-003)

**STRIDE Category**: Tampering (firmware modification), Spoofing (attacker impersonates legitimate OTA server), Elevation of Privilege (attacker gains ECU control)

**Typical AFR Range**: 4-7 (High to Medium) - Elapsed Time: Months, Specialist Expertise: Expert, Knowledge of Item: Restricted, Window of Opportunity: Moderate, Equipment: Specialized  
(Note: ISO band naming is counterintuitive. Higher AFR numeric scores mean lower barriers for the attacker; strong PKI/Secure Boot typically LOWER the numeric AFR by increasing attacker effort.)

**Example Scenario**: 
Attacker compromises the OEM's OTA backend server by exploiting an unpatched vulnerability (OWASP API2:2023 Broken Authentication). They replace the legitimate firmware image for the Head Unit (AST-DAT-004) with a modified version containing a backdoor. The malicious firmware is signed using the stolen signing key (AST-DAT-003) obtained via a previous supply chain attack. Vehicles download and install the malicious update, believing it to be authentic. The backdoor allows the attacker remote command execution on the Head Unit, enabling data exfiltration (contacts, location history) and potential pivot to CAN bus for message injection.

**Mitigation Approaches**:
- Strong PKI with Hardware Security Module (HSM) protection for signing keys (AST-ECU-005)
- Multi-signature or dual-authorization for firmware releases (prevents single compromised developer)
- Secure Boot with rollback protection (AST-ECU-001 verified by user)
- End-to-end encryption of OTA channel (TLS 1.3 with certificate pinning)
- Backend server hardening (OWASP API security controls, regular penetration testing)
- Delta updates with cryptographic hash verification

**Related Damage Scenarios**: DS-BCK-001 (Backend Server Compromise), DS-IVI-001 (PII Exposure via backdoor)

---

## Pattern 4: Firmware Extraction & Reverse Engineering

**Domain**: EXT

**Attack Description**: Attacker extracts firmware images from vehicle ECUs (via JTAG/SWD debug ports, UART boot modes, or removable storage) and reverse-engineers the binaries to discover vulnerabilities, hardcoded credentials, or cryptographic keys. This is typically a reconnaissance step enabling subsequent attacks.

**Typical Attack Surface**:
- Physical debug interfaces (JTAG, SWD) on ECU circuit boards
- UART boot mode pins exposed on PCB
- UFS/eMMC flash storage (AST-DAT-001) removable for offline reading
- Firmware update packages downloaded from OTA server (AST-DAT-004)

**STRIDE Category**: Information Disclosure (firmware contains intellectual property, keys, vulnerabilities)

**Typical AFR Range**: 5-8 (High to Medium) - Elapsed Time: Days to weeks, Specialist Expertise: Expert, Knowledge of Item: Restricted, Window of Opportunity: Unlimited (if physical access), Equipment: Specialized

**Example Scenario**: 
Security researcher obtains a Head Unit module from a salvage yard. They desolder the UFS flash chip (AST-DAT-001) and use a flash programmer to dump the raw storage contents. The extracted firmware image is loaded into Ghidra or IDA Pro for reverse engineering. Analysis reveals:
1. Hardcoded WiFi credentials for factory test network in Android partition
2. Debug symbols left in QNX binary, aiding exploit development
3. Vulnerable version of OpenSSL library (no specific CVE; class of TLS vulnerabilities requiring up-to-date patching)
4. Firmware signing public key (AST-DAT-003) stored in plaintext, enabling verification bypass research

This information is published online, lowering the expertise required for future attackers to exploit these vehicles.

**Mitigation Approaches**:
- Firmware encryption with SoC-fused keys (prevents plaintext extraction)
- Debug interface protection (fuse JTAG/SWD in production builds, or require authenticated debug)
- Secure storage of cryptographic keys in HSM/TEE (AST-ECU-005), never in plaintext flash
- Code obfuscation and symbol stripping (increases reverse engineering effort)
- Regular third-party security audits of firmware before release

**Related Damage Scenarios**: DS-EXT-001 (Hardcoded Credential Exposure), DS-EXT-002 (Cryptographic Key Compromise)

---

## Pattern 5: Backend API Exploitation

**Domain**: BCK

**Attack Description**: Attacker exploits vulnerabilities in the vehicle manufacturer's backend API services (used for telematics, mobile app integration, cloud services) to gain unauthorized access to vehicle data or control functions. Common vulnerabilities include broken authentication (OWASP API2), broken object-level authorization (OWASP API1), and excessive data exposure (OWASP API3).

**Typical Attack Surface**:
- RESTful APIs exposed to mobile apps and web portals
- GraphQL endpoints with insufficient access control
- Legacy SOAP/XML services with known vulnerabilities
- Third-party integrations (payment gateways, insurance telematics)

**STRIDE Category**: Spoofing (attacker impersonates legitimate user), Elevation of Privilege (horizontal/vertical privilege escalation), Information Disclosure

**Typical AFR Range**: 6-9 (Medium) - Elapsed Time: Days, Specialist Expertise: Proficient, Knowledge of Item: Public, Window of Opportunity: Unlimited, Equipment: Standard

**Example Scenario**: 
Attacker analyzes the OEM's mobile app using a proxy tool (Burp Suite) to intercept API traffic. They discover the "GET /api/v1/vehicle/{VIN}/location" endpoint used to retrieve vehicle GPS position. The endpoint only checks if the user is authenticated but does not verify if the user *owns* that VIN (OWASP API1:2023 Broken Object Level Authorization). The attacker writes a script to enumerate VINs (format is predictable: manufacturer code + year + serial number) and retrieves location data for 50,000 vehicles. This constitutes mass surveillance and GDPR/GB 44495 violation.

**Mitigation Approaches**:
- Object-level authorization checks (verify user owns the resource before returning data)
- Rate limiting and API throttling (prevent enumeration attacks)
- Strong authentication (OAuth 2.1 with PKCE, short-lived tokens, refresh token rotation)
- Input validation and parameterized queries (prevent injection attacks)
- API gateway with centralized logging and anomaly detection
- Regular OWASP API Security Top 10 assessments

**Related Damage Scenarios**: DS-BCK-001 (Backend API Exploitation), DS-IVI-002 (Location Tracking), DS-IVI-001 (PII Exposure)

---

## Pattern 6: Telematics Data Exfiltration

**Domain**: BCK

**Attack Description**: Attacker intercepts or exfiltrates sensitive vehicle data transmitted via the telematics channel (cellular connection between vehicle and backend). This could involve network sniffing (if encryption is weak), compromising the telematics ECU, or exploiting backend data storage.

**Typical Attack Surface**:
- Cellular/Telematics Link (AST-COM-005) with weak or no encryption
- Compromised Telematics ECU (external to Head Unit but connected via Ethernet)
- Backend database with insufficient access controls
- Third-party data analytics platforms receiving telemetry feeds

**STRIDE Category**: Information Disclosure

**Typical AFR Range**: 7-10 (Medium to Low) - Elapsed Time: Weeks, Specialist Expertise: Proficient to Expert, Knowledge of Item: Restricted, Window of Opportunity: Moderate, Equipment: Specialized

**Example Scenario**: 
Attacker discovers that the telematics link (AST-COM-005) uses TLS 1.2 with weak cipher suite (CBC mode vulnerable to BEAST/POODLE attacks). They set up a rogue cellular base station (IMSI catcher) near a highway to intercept vehicle-to-backend traffic. Using known TLS downgrade attacks, they decrypt the telematics stream and extract:
1. GPS coordinates (sent every 30 seconds) - enabling continuous location tracking
2. Diagnostic trouble codes (DTCs) - revealing vehicle faults and maintenance history
3. Driver behavior data - acceleration, braking, cornering patterns (used for insurance scoring)

This data is sold on dark web marketplaces for stalking, industrial espionage, or insurance fraud.

**Mitigation Approaches**:
- TLS 1.3 with strong cipher suites and certificate pinning (AST-DAT-003)
- Mutual TLS (mTLS) authentication (vehicle authenticates backend, backend authenticates vehicle)
- Data minimization (only transmit necessary telemetry, anonymize where possible)
- End-to-end encryption (encrypt payload before TLS layer for defense-in-depth)
- Cellular network security (reject suspicious base stations, SIM card authentication)

**Related Damage Scenarios**: DS-IVI-002 (Continuous Location Tracking), DS-IVI-001 (PII Exposure)

---

## Pattern 7: IVI Application Compromise (Malicious App)

**Domain**: IVI

**Attack Description**: Attacker distributes a malicious Android application (via third-party app store, phishing, or supply chain compromise) that, when installed on the vehicle's Head Unit, exploits OS vulnerabilities or misuses granted permissions to access sensitive data or escape sandboxing.

**Typical Attack Surface**:
- Android Guest OS (AST-ECU-004) running user-installed apps
- Third-party app stores with weak or no code signing verification
- Side-loaded APK files from USB storage (AST-IFC-001)
- Compromised legitimate app via supply chain attack

**STRIDE Category**: Elevation of Privilege (sandbox escape), Information Disclosure, Tampering

**Typical AFR Range**: 5-8 (High to Medium) - Elapsed Time: Days to weeks, Specialist Expertise: Proficient, Knowledge of Item: Public, Window of Opportunity: Moderate to Unlimited, Equipment: Standard

**Example Scenario**: 
User downloads a "free navigation app" from a third-party Android app store (not Google Play). The app requests excessive permissions: ACCESS_FINE_LOCATION, READ_CONTACTS, RECORD_AUDIO, and INTERNET. Once installed on the Head Unit's Android partition (AST-ECU-004), the malicious app:
1. Exfiltrates user contacts, SMS history, and call logs to attacker's server (STRIDE: Information Disclosure)
2. Records GPS location every 10 seconds and uploads to tracking server (violating GDPR)
3. Exploits a known Android kernel vulnerability (e.g., CVE-2019-2215 for similar privilege escalation) to escape the app sandbox and gain root access
4. With root access, writes to shared memory regions accessible by QNX, attempting a hypervisor (AST-ECU-002) escape to access CAN-FD bus

**Mitigation Approaches**:
- Restrict app installation to trusted sources only (whitelist Google Play or OEM app store)
- Android permission hardening (principle of least privilege, runtime permission prompts)
- Regular Android security patch updates via OTA (AST-DAT-004)
- Hypervisor hardening to prevent Android → QNX memory access (AST-ECU-002)
- App sandboxing with SELinux mandatory access controls
- User education on phishing and malicious app risks

**Related Damage Scenarios**: DS-IVI-001 (PII Exposure), DS-IVI-002 (Location Tracking), DS-CAN-001 (if hypervisor escape succeeds)

---

## Pattern 8: Diagnostic Interface Abuse (OBD-II / UDS)

**Domain**: EXT

**Attack Description**: Attacker exploits vehicle diagnostic protocols (OBD-II, UDS per ISO 14229) accessed via physical diagnostic port or remote telematics channel to read sensitive data, reprogram ECUs, or disable security controls. Diagnostic interfaces often have elevated privileges and weak authentication.

**Typical Attack Surface**:
- OBD-II port (physical access in cabin)
- UDS protocol over CAN-FD (AST-COM-001)
- Remote diagnostic sessions via telematics (if enabled)
- Aftermarket diagnostic tools with default/hardcoded authentication

**STRIDE Category**: Elevation of Privilege (diagnostic mode grants ECU reprogramming), Information Disclosure (read DTC, VIN, calibration data)

**Typical AFR Range**: 4-7 (High to Medium) - Elapsed Time: <1 day, Specialist Expertise: Proficient, Knowledge of Item: Public, Window of Opportunity: Moderate, Equipment: Specialized

**Example Scenario**: 
Attacker gains physical access to vehicle (valet attack, rental car, car sharing) and connects an automotive diagnostic tool (e.g., Autel MaxiSys, open-source EOBD tools) to the OBD-II port. Using UDS commands over CAN:
1. Read Diagnostic Trouble Codes (DTCs) to identify disabled safety features or tampered odometer
2. Use "Read Data by Identifier" (0x22) to extract calibration data, VIN, and ECU serial numbers
3. Enter "Programming Session" (0x10 0x02) and reflash the Gateway ECU (AST-ECU-006) with modified firmware that disables immobilizer authentication
4. Exit diagnostic mode, disconnect tool, and steal vehicle using a cloned key fob

**Mitigation Approaches**:
- Seed-key authentication for diagnostic sessions (ISO 14229-1 Security Access service)
- Cryptographic challenge-response using HSM-stored keys (AST-ECU-005)
- Physical security for OBD-II port (lockable cover, tamper detection)
- Disable remote diagnostic access in production vehicles (only enable at service centers)
- Logging and auditing of all diagnostic sessions (sent to backend for anomaly detection)

**Related Damage Scenarios**: DS-EXT-001 (Hardcoded Credential Exposure), DS-IMM-001 (Immobilizer Bypass), DS-CAN-001 (if ECU reprogrammed for malicious CAN injection)

---

## Pattern 9: Key Fob Relay Attack (Passive Entry)

**Domain**: IMM

**Attack Description**: Attacker uses two radio relay devices to extend the range of the vehicle's passive keyless entry system. One device is placed near the legitimate key fob (e.g., inside owner's house), and the other near the vehicle. The system believes the key is present, allowing door unlock and engine start without the owner's knowledge.

**Typical Attack Surface**:
- Passive Keyless Entry & Start (PKES) system using low-frequency (LF) challenge and high-frequency (HF) response
- Key fob with always-on radio receiver (not motion-sensing sleep mode)
- Vehicle Body Control Module (BCM) that unlocks/starts based on proximity alone

**STRIDE Category**: Spoofing (attacker relays legitimate key fob signal to impersonate authorized user)

**Typical AFR Range**: 2-5 (High) - Elapsed Time: Minutes, Specialist Expertise: Layman, Knowledge of Item: Public, Window of Opportunity: Short (minutes), Equipment: Standard (relay devices $50-300)

**Example Scenario**: 
Two attackers target a vehicle parked in the driveway. Attacker 1 stands near the front door (where the owner left the key fob on a table) with a relay device. Attacker 2 stands next to the vehicle with a second relay device. The vehicle sends a low-frequency (125 kHz) challenge signal asking "Is key present?". Attacker 2's device receives this and relays it to Attacker 1's device, which retransmits it near the real key fob. The key fob responds with a high-frequency (434 MHz) encrypted response. This is relayed back to the vehicle, which unlocks the doors and allows engine start. The attackers drive away in under 60 seconds. No alarm is triggered because the vehicle believes the legitimate key is present.

**Mitigation Approaches**:
- Motion-sensing key fobs (sleep mode when stationary for >5 minutes)
- Ultra-wideband (UWB) ranging to measure true distance (prevents relay)
- Time-of-flight measurement (if relay adds >10ms latency, reject)
- Owner education (store key in Faraday pouch/RFID-blocking container)
- Multi-factor authentication (require PIN entry on touchscreen before engine start)

**Related Damage Scenarios**: DS-IMM-001 (Keyless Entry Relay Attack → Vehicle Theft), DS-FIN-001 (Financial loss from stolen vehicle)

---

## Pattern 10: Sensor Spoofing (ADAS Camera/Radar)

**Domain**: ADAS

**Attack Description**: Attacker manipulates sensor inputs to Advanced Driver Assistance Systems (ADAS) by projecting false images onto cameras, emitting radar signals to create phantom objects, or using GPS spoofing to mislead navigation. This causes the ADAS to make incorrect decisions (e.g., emergency braking for non-existent obstacle, failing to detect real pedestrian).

**Typical Attack Surface**:
- Front/rear-facing cameras (AST-SNS-003 Driver Monitoring Camera used as example; actual ADAS cameras are external)
- GNSS Receiver (AST-SNS-001) vulnerable to GPS spoofing
- Radar sensors (not listed in current asset_list.md, but typical in ADAS)
- Lidar sensors (if equipped)

**STRIDE Category**: Tampering (sensor data integrity compromised), Spoofing (fake objects presented to ADAS)

**Typical AFR Range**: 6-9 (Medium) - Elapsed Time: Days, Specialist Expertise: Proficient, Knowledge of Item: Public, Window of Opportunity: Short to Moderate, Equipment: Specialized

**Example Scenario**: 
Researchers demonstrate an attack where they project carefully crafted laser patterns onto a vehicle's front camera sensor. The patterns are designed to fool the ADAS object detection neural network into misclassifying a real pedestrian as a "non-obstacle" (adversarial machine learning attack). When tested at 50 km/h in a closed track, the vehicle's automatic emergency braking (AEB) fails to engage, and the test dummy is struck. In a separate attack, GPS spoofing hardware (Software-Defined Radio transmitting fake GPS signals) is used to convince the navigation system (AST-SNS-001) that the vehicle is on a highway when it is actually in a 30 km/h school zone, leading to inappropriate speed recommendations.

**Mitigation Approaches**:
- Sensor fusion (cross-validate camera with radar and lidar; reject if inconsistent)
- GNSS spoofing detection (check signal strength, multi-constellation validation, inertial measurement unit cross-check)
- Machine learning model hardening (adversarial training, input sanitization)
- Physical sensor protection (anti-reflective coatings, tamper detection)
- Cryptographic authentication for sensor data (if sensors support SecOC)

**Related Damage Scenarios**: DS-ADAS-001 (ADAS Emergency Braking Failure → Collision), DS-ADAS-002 (GPS Spoofing → Navigation Error)

---

## Using Patterns in Combination

**Note**: A single attack campaign may combine MULTIPLE threat patterns in sequence (attack chain). For example:

**Attack Chain Example**: Vehicle Theft via Multi-Stage Attack
1. **Pattern 4** (Firmware Extraction) - Extract Head Unit firmware from salvage vehicle, discover hardcoded diagnostic key
2. **Pattern 8** (Diagnostic Interface Abuse) - Use extracted key to unlock UDS programming mode on target vehicle
3. **Pattern 3** (OTA Manipulation) - Reprogram Gateway ECU firmware to disable immobilizer authentication
4. **Pattern 9** (Key Fob Relay) - Use relay attack to unlock and start vehicle with cloned/bypassed key

**Best Practice**: Document each step of the attack chain as a separate threat scenario (TS-EXT-001, TS-EXT-002, TS-IMM-001) and cross-reference them in the "Attack Prerequisites" or "Chaining" section.

---

## Pattern Selection Guide

| If the attack involves... | Use Pattern | STRIDE | Typical Domain |
|---------------------------|-------------|--------|----------------|
| Injecting malicious CAN messages | #1 (CAN Injection) | Spoofing, Tampering | CAN |
| Flooding CAN bus bandwidth | #2 (CAN DoS) | Denial of Service | CAN |
| Installing malicious firmware | #3 (OTA Manipulation) | Tampering, Elevation of Privilege | OTA |
| Extracting/reverse engineering firmware | #4 (Firmware Extraction) | Information Disclosure | EXT |
| Exploiting backend REST/GraphQL APIs | #5 (Backend API) | Spoofing, Elevation of Privilege | BCK |
| Intercepting telematics data | #6 (Telematics Exfiltration) | Information Disclosure | BCK |
| Malicious Android app on Head Unit | #7 (IVI App Compromise) | Elevation of Privilege | IVI |
| Abusing OBD-II/UDS diagnostic commands | #8 (Diagnostic Abuse) | Elevation of Privilege | EXT |
| Relay attack on keyless entry | #9 (Key Fob Relay) | Spoofing | IMM |
| Spoofing camera/radar/GPS sensors | #10 (Sensor Spoofing) | Tampering, Spoofing | ADAS |

---

## Customization Checklist

When adapting a pattern:

- [ ] Replace generic asset references with specific AST-IDs from your `data/asset_list.md`
- [ ] Adjust AFR scores based on your vehicle's implemented security controls (Secure Boot, HSM, network segmentation, etc.)
- [ ] Link to specific damage scenarios (DS-IDs from `data/ds.md`) this threat could cause
- [ ] Add vehicle-specific details (ECU names, protocol versions, architecture)
- [ ] Update framework mappings (STRIDE, MITRE ATT&CK, OWASP, UN R155 Annex 5)
- [ ] Include real-world CVE numbers if applicable (e.g., CVE-2019-2215 for known exploits)
- [ ] Ensure TS-ID domain code matches the primary attack vector (not the impacted system)
- [ ] Verify all linked assets and damage scenarios are documented

---

## Attack Feasibility Rating (AFR) Quick Reference

Use the detailed AFR scoring guide in `references/afr-guide.md`. Quick estimates:

| AFR Score | Rating | Typical Profile |
|-----------|--------|----------------|
| 0-4 | Very Low | Multiple experts, restricted/classified knowledge, >6 months, bespoke/custom-built equipment, very narrow window |
| 5-9 | Low | Expert, confidential/limited access knowledge, weeks-months, specialized but purchasable equipment, moderate window |
| 10-13 | Moderate | Proficient, public with effort knowledge, days-weeks, standard automotive tools, easy access window |
| 14-15 | High | Layman, publicly available/common knowledge, <1 week, off-the-shelf consumer electronics, unlimited window |

**Remember**: AFR is context-dependent. Implementing security controls (Secure Boot, HSM, network segmentation, IDS) typically reduces the numeric AFR (harder for attacker), potentially shifting a pattern toward more difficult bands.
