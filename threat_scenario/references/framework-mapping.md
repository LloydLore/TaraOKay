# Security Framework Mapping for Automotive Threat Scenarios

This reference provides mapping tables for standard security frameworks used in automotive threat modeling. In this repository, only STRIDE is required by default for `threat_scenario`; the rest are optional metadata when evidence or downstream reporting needs them.

---

## 1. STRIDE Threat Model

STRIDE is a mnemonic for six threat categories widely used during threat modeling. Each category represents a different class of security violation.

| ID | Category | Violated Property | Automotive Example |
|----|----------|-------------------|---------------------|
| **S** | Spoofing | Authenticity | Fake ECU impersonating legitimate gateway on CAN bus |
| **T** | Tampering | Integrity | Attacker modifying OTA firmware package during download |
| **R** | Repudiation | Non-repudiation | Malicious actor erasing diagnostic logs to hide attack traces |
| **I** | Information Disclosure | Confidentiality | Extracting cryptographic keys via OBD-II diagnostic interface |
| **D** | Denial of Service | Availability | CAN bus flooding attack blocking safety-critical messages |
| **E** | Elevation of Privilege | Authorization | Exploiting IVI vulnerability to gain gateway ECU access |

### STRIDE to UN R155 Annex 5 Mapping

| STRIDE Category | Primary UN R155 Threat Categories |
|----------------|-----------------------------------|
| Spoofing | 4.3.2 (Communication Channels), 4.3.7 (External Connectivity) |
| Tampering | 4.3.3 (Update Procedures), 4.3.4 (Code Execution) |
| Repudiation | 4.3.5 (Data and Privacy), 4.3.1 (Backend Servers) |
| Information Disclosure | 4.3.5 (Data and Privacy), 4.3.7 (External Connectivity) |
| Denial of Service | 4.3.2 (Communication Channels), 4.3.7 (External Connectivity) |
| Elevation of Privilege | 4.3.7 (External Connectivity) |

---

## 2. MITRE ATT&CK for ICS

Key techniques from the MITRE ATT&CK for Industrial Control Systems framework relevant to automotive embedded systems and connected vehicles.

| Technique ID | Name | Automotive Relevance |
|-------------|------|----------------------|
| **T0855** | Unauthorized Command Message | Injecting malicious CAN/LIN commands to actuators (brakes, steering) |
| **T0856** | Spoof Reporting Message | Falsifying sensor data such as speed, GPS coordinates, or temperature |
| **T0860** | Wireless Compromise | Attacking Bluetooth, WiFi, V2X (Vehicle-to-Everything), or cellular links |
| **T0839** | Module Firmware | Flashing malicious firmware to individual ECUs |
| **T0857** | System Firmware | Compromising base firmware of gateway ECU or telematics control unit |
| **T0836** | Modify Parameter | Altering ECU calibration data or configuration parameters |
| **T0878** | Alarm Suppression | Suppressing diagnostic trouble codes (DTCs) or warning indicators |
| **T0814** | Denial of Service | Overloading communication bus or ECU to deny service |
| **T0827** | Loss of Control | Disrupting normal control of critical vehicle functions |
| **T0880** | Loss of Safety | Causing unsafe state in safety-critical system (ASIL-C/D functions) |
| **T0847** | Replication Through Removable Media | USB-based malware delivery to infotainment or diagnostic port |
| **T0842** | Network Sniffing | Passive capture of in-vehicle network or V2X traffic |
| **T0862** | Supply Chain Compromise | Malicious hardware or software component from supplier |
| **T0883** | Internet Accessible Device | Exploiting internet-facing telematics unit or cloud API |

---

## 3. MITRE ATT&CK Enterprise

Enterprise ATT&CK techniques applicable when backend servers, cloud APIs, mobile apps, or OEM corporate infrastructure are in scope for the TARA.

| Technique ID | Name | Backend/Cloud Relevance |
|-------------|------|------------------------|
| **T1190** | Exploit Public-Facing Application | Attacking OTA update server or fleet management web portal |
| **T1195** | Supply Chain Compromise | Malicious library injected into vehicle software build pipeline |
| **T1078** | Valid Accounts | Using stolen credentials for backend admin or engineer access |
| **T1566** | Phishing | Targeting OEM engineers to gain access to internal systems |
| **T1552** | Unsecured Credentials | Hardcoded API keys in firmware or configuration files |
| **T1486** | Data Encrypted for Impact | Ransomware attack against OTA infrastructure or fleet services |
| **T1041** | Exfiltration Over C2 Channel | Data exfiltration from vehicle via telematics connection |
| **T1133** | External Remote Services | Unauthorized access to VPN or remote vehicle diagnostics |
| **T1071** | Application Layer Protocol | Covert C2 communication via HTTPS or DNS to backend |
| **T1110** | Brute Force | Password attack against vehicle owner portal or mobile app |

---

## 4. OWASP IoT Security Top 10 (2018)

Applicable to automotive ECUs, sensors, actuators, and embedded systems with IoT characteristics.

| ID | Vulnerability | Automotive ECU Relevance |
|----|--------------|--------------------------|
| **I1** | Weak, Guessable, or Hardcoded Passwords | Default credentials on diagnostic interfaces or debug ports |
| **I2** | Insecure Network Services | Exposed CAN-to-Ethernet bridge or unprotected diagnostic services |
| **I3** | Insecure Ecosystem Interfaces | Unsecured mobile app API or cloud service for vehicle control |
| **I4** | Lack of Secure Update Mechanism | OTA updates without cryptographic signature verification |
| **I5** | Use of Insecure or Outdated Components | Unpatched open-source libraries in infotainment OS (Android, QNX) |
| **I6** | Insufficient Privacy Protection | PII logging without encryption or access controls |
| **I7** | Insecure Data Transfer and Storage | Unencrypted diagnostic data stored on ECU flash memory |
| **I8** | Lack of Device Management | No mechanism to revoke compromised ECU credentials or certificates |
| **I9** | Insecure Default Settings | Debug ports (JTAG, UART) enabled in production firmware build |
| **I10** | Lack of Physical Hardening | No tamper detection on ECU housing or physical attack countermeasures |

---

## 5. OWASP API Security Top 10 (2023)

Relevant when vehicle backend APIs, mobile companion apps, or fleet management portals are in scope.

| ID | Vulnerability | Automotive API Relevance |
|----|--------------|--------------------------|
| **API1** | Broken Object Level Authorization | Accessing another user's vehicle data via API without authorization check |
| **API2** | Broken Authentication | Weak token validation on telematics or remote control API |
| **API3** | Broken Object Property Level Authorization | API returning sensitive vehicle fields (VIN, GPS) to unauthorized clients |
| **API4** | Unrestricted Resource Consumption | Denial-of-service via API flooding without rate limiting |
| **API5** | Broken Function Level Authorization | Vehicle user accessing admin-only API endpoints (fleet management) |
| **API6** | Unrestricted Access to Sensitive Business Flows | Bulk querying of vehicle location history without throttling |
| **API7** | Server-Side Request Forgery | Backend server fetching internal resources via manipulated API parameter |
| **API8** | Security Misconfiguration | Exposed debug endpoints or verbose error messages in production API |
| **API9** | Improper Inventory Management | Shadow APIs from legacy vehicle models not properly secured |
| **API10** | Unsafe Consumption of APIs | Trusting third-party V2X or mapping data without validation |

---

## 6. OWASP Mobile Security Top 10 (2024)

Applicable when vehicle companion mobile apps (iOS, Android) are in scope for the TARA.

| ID | Vulnerability | Automotive App Relevance |
|----|--------------|--------------------------|
| **M1** | Improper Credential Usage | Hardcoded API keys or OAuth tokens in OEM companion app |
| **M2** | Inadequate Supply Chain Security | Malicious third-party SDK integrated into vehicle mobile app |
| **M3** | Insecure Authentication/Authorization | Bypassing PIN or biometric authentication to unlock vehicle remotely |
| **M4** | Insufficient Input/Output Validation | SQL injection or command injection via app UI to backend API |
| **M5** | Insecure Communication | Unencrypted Bluetooth Low Energy (BLE) pairing for digital key |
| **M6** | Inadequate Privacy Controls | App collecting precise location data without user consent disclosure |
| **M7** | Insufficient Binary Protections | Reverse engineering app binary to extract API secrets or encryption keys |
| **M8** | Security Misconfiguration | Debug flags or logging left enabled in production app release |
| **M9** | Insecure Data Storage | Storing vehicle access tokens in plaintext in app local storage |
| **M10** | Insufficient Cryptography | Using deprecated cipher (DES, MD5) for key derivation or signing |

---

## 7. UN R155 Annex 5 Threat Categories

The seven threat categories mandated by UN Regulation No. 155 (Cybersecurity and Cybersecurity Management System). All automotive TARA activities must address these categories.

| Category | UN R155 Reference | Description | Example Threat |
|----------|-------------------|-------------|----------------|
| **Backend Servers** | Annex 5, Para 4.3.1 | Threats to backend servers, cloud infrastructure, OTA update servers | Backend database breach exposing VINs and user accounts |
| **Communication Channels** | Annex 5, Para 4.3.2 | Threats to vehicle internal and external communication channels | Man-in-the-middle attack on Ethernet or CAN bus |
| **Update Procedures** | Annex 5, Para 4.3.3 | Threats to software/firmware update mechanisms (OTA, dealer reflash) | Malicious firmware installation via compromised OTA package |
| **Code Execution** | Annex 5, Para 4.3.4 | Unauthorized execution of code on vehicle systems | Remote code execution on infotainment via WiFi exploit |
| **Data and Privacy** | Annex 5, Para 4.3.5 | Unauthorized access to or manipulation of vehicle/user data | Extraction of user PII (contacts, location history) |
| **Safety-Critical Compromise** | Annex 5, Para 4.3.6 | Compromise of systems affecting vehicle safety functions | CAN message injection causing unintended braking |
| **External Connectivity** | Annex 5, Para 4.3.7 | Threats via external interfaces (USB, Bluetooth, cellular, V2X) | USB malware injection via infotainment port |

---

## Usage Guidance

### When to Use Each Framework

| Framework | Use When... | Example Scenario |
|-----------|------------|------------------|
| **STRIDE** | Conducting structured threat brainstorming sessions; need universal threat categories | Identifying all threat types for a new ECU architecture |
| **MITRE ATT&CK ICS** | Analyzing vehicle-specific embedded attacks; need real-world technique references | Documenting CAN bus injection attack based on published research |
| **MITRE ATT&CK Enterprise** | Backend or cloud systems in scope; aligning with IT security team | Threat modeling OTA infrastructure or fleet management portal |
| **OWASP IoT** | Embedded ECUs with network connectivity; IoT-like characteristics | Assessing infotainment head unit or telematics control unit |
| **OWASP API** | Vehicle exposes APIs (REST, GraphQL) to mobile apps or web portals | Threat modeling companion app backend or dealer diagnostic API |
| **OWASP Mobile** | Companion mobile app (iOS/Android) in scope | Assessing security of OEM vehicle control app |
| **UN R155 Annex 5** | Regulatory compliance required; type approval submission | Demonstrating TARA coverage for all seven mandated categories |

### Multi-Framework Mapping

Many threat scenarios map to **multiple** frameworks simultaneously. Document multiple mappings only when they add value and you can justify them. `N/A` is acceptable when a framework does not fit cleanly.

**Example**: CAN Bus Message Injection Attack

| Framework | Classification |
|-----------|---------------|
| STRIDE | **T** (Tampering) + **I** (Information Disclosure if sniffing precedes injection) |
| MITRE ATT&CK ICS | **T0855** (Unauthorized Command Message) |
| OWASP IoT | **I2** (Insecure Network Services - exposed CAN interface) |
| UN R155 | **4.3.2** (Communication Channels) + **4.3.6** (Safety-Critical Compromise) |

---

## Framework Selection Matrix

| Threat Scenario Type | Recommended Frameworks |
|---------------------|------------------------|
| CAN bus attacks | STRIDE (T, S, D), MITRE ICS (T0855, T0856), UN R155 (4.3.2, 4.3.6) |
| OTA firmware tampering | STRIDE (T), MITRE ICS (T0839, T0857), OWASP IoT (I4), UN R155 (4.3.3) |
| Backend API exploitation | STRIDE (E, I), MITRE Enterprise (T1190), OWASP API (API1-10), UN R155 (4.3.1) |
| Mobile app vulnerabilities | STRIDE (S, I), OWASP Mobile (M1-10), UN R155 (4.3.7) |
| USB malware injection | STRIDE (T, E), MITRE ICS (T0847), OWASP IoT (I9, I10), UN R155 (4.3.7) |
| Wireless attacks (BLE, WiFi, V2X) | STRIDE (S, D), MITRE ICS (T0860), OWASP IoT (I2, I3), UN R155 (4.3.7) |
| Privacy violations (data exposure) | STRIDE (I), MITRE Enterprise (T1041), OWASP IoT (I6, I7), UN R155 (4.3.5) |
| Supply chain compromise | STRIDE (T), MITRE ICS/Enterprise (T0862, T1195), OWASP Mobile (M2), UN R155 (4.3.3) |

---

**Note**: Framework mappings are based on publicly available MITRE ATT&CK and OWASP documentation. Always verify technique IDs and categories against the latest framework releases:
- MITRE ATT&CK: https://attack.mitre.org/
- OWASP IoT Top 10: https://owasp.org/www-project-internet-of-things/
- OWASP API Security: https://owasp.org/www-project-api-security/
- OWASP Mobile Security: https://owasp.org/www-project-mobile-top-10/
- UN R155: https://unece.org/transport/documents/2021/03/standards/un-regulation-no-155-cyber-security-and-cyber-security
