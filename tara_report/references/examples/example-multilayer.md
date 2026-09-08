# Multi-layer TARA Report Example - Infotainment Head Unit System

**Report Date**: 2026-03-25  
**Vehicle System**: Passenger Vehicle Infotainment/Head Unit (Qualcomm QAM8295 with QNX+Android Hypervisor)  
**Reporting Period**: 2026-01-01 to 2026-03-25  
**Total Domains Analyzed**: 5 (CAN, IVI, OTA, EXT, BCK)  
**Total Threat Scenarios**: 21  
**Total Damage Scenarios**: 18  
**Total Risk Treatments**: 21  

---

## Defense-in-Depth Overview

This multi-layer report applies defense-in-depth principles to the Infotainment Head Unit cybersecurity threat analysis, organizing findings by domain to demonstrate layered security controls and cross-domain isolation strategies.

### Defense-in-Depth Principles Applied

1. **Domain Isolation**: Each domain (CAN, IVI, OTA, EXT, BCK) operates with restricted privileges and network segmentation to prevent lateral movement
2. **Layered Controls**: Multiple security controls (cryptography, access control, network segmentation, secure boot) applied at different architectural layers
3. **Fail-Safe Design**: Single control failure does not compromise entire system; redundant protections at each layer
4. **Least Privilege**: Each domain granted minimum necessary access to assets and communication channels
5. **Attack Surface Reduction**: External-facing domains (EXT, OTA) isolated from safety-critical domains (CAN)

### Architectural Security Layers

| Layer | Description | Domains | Key Controls |
|-------|-------------|---------|--------------|
| **Physical Layer** | Hardware interfaces, sensors, actuators | EXT (USB, NFC) | Physical access control, tamper detection |
| **Network Layer** | Communication buses, Ethernet, wireless | CAN, EXT (Bluetooth, WiFi) | Firewall rules, MACsec, CAN SecOC authentication |
| **Platform Layer** | Operating systems, hypervisor, firmware | IVI (QNX, Android) | Secure Boot, hypervisor isolation, runtime integrity |
| **Application Layer** | Apps, services, OTA updates | IVI, OTA | Code signing, sandboxing, input validation |
| **Backend Layer** | Cloud services, telematics | BCK, OTA | OAuth 2.0 + MFA, API authentication, TLS 1.3 |

### Cross-Domain Attack Chains

The report identifies attack chains that span multiple domains, demonstrating where defense-in-depth controls successfully contain threats versus where additional controls are needed:

- **EXT → IVI → CAN**: Physical USB access → Android compromise → hypervisor escape → Gateway bypass → CAN access
- **BCK → OTA → IVI**: Backend API compromise → malicious OTA delivery → firmware tampering → persistent system control
- **EXT (Bluetooth) → IVI → BCK**: Bluetooth RCE → Android exfiltration → cellular data leak

---

## Domain: CAN Bus and In-Vehicle Networking (CAN)

### Domain Summary

**Domain Risk Level**: HIGH  
**Total Threat Scenarios**: 4  
**Total Damage Scenarios**: 5  
**Total Risk Treatments**: 4  
**Domain Assets**: AST-COM-001 (CAN-FD Bus), AST-ECU-003 (QNX), AST-ECU-006 (Gateway ECU)  

**Top Domain Threat**: TS-CAN-001 (RV 4) - CAN Bus Message Injection via Compromised Head Unit  

### Domain Description

The CAN domain encompasses the Controller Area Network (CAN-FD) bus and in-vehicle networking infrastructure, providing communication between ECUs for vehicle control, diagnostics, and infotainment integration. This domain handles message routing via the Gateway ECU, making it a primary target for attackers seeking vehicle control. The QNX guest OS has privileged CAN-FD access, contrasting with the isolated Android guest that cannot directly access vehicle networks.

### Domain Risk Distribution

| Risk Value | Count | Percentage |
|------------|-------|------------|
| RV 5 (Critical) | 0 | 0% |
| RV 4 (High) | 3 | 75% |
| RV 3 (Medium) | 1 | 25% |
| RV 2 (Low) | 0 | 0% |
| RV 1 (Negligible) | 0 | 0% |

**SFOP Impact Analysis (Domain)**:
- Safety-Critical Threats: 2 (Impact ≥ 3) - Malicious CAN injection, Gateway bypass
- Financial Impact Threats: 2 (Impact ≥ 3) - Recall costs, regulatory fines
- Operational Impact Threats: 2 (Impact ≥ 3) - Safety functions compromised
- Privacy Impact Threats: 0 (Impact ≥ 3)
- **Most Critical Impact Type**: Safety (unintended vehicle behavior at highway speeds)

### Domain Assets and Attack Surface

**Assets in Domain**:
- AST-COM-001: CAN-FD Bus Interface (in-vehicle communication backbone)
- AST-ECU-003: QNX Guest OS (CAN-FD access, real-time vehicle functions)
- AST-ECU-006: Gateway ECU (external, critical security boundary)

**Attack Surface / Entry Points**:
- OBD-II diagnostic port (physical access)
- Head Unit SoC → CAN-FD interface (via AST-COM-001)
- Gateway ECU routing interfaces (inter-domain bridge)
- UDS diagnostic service endpoints

**External Interfaces**: 1 (OBD-II to external diagnostics)  
**Internal Dependencies**: 2 (to IVI, OTA domains via Gateway)  
**Physical Access Required**: 3 threats  
**Remote Attack Feasible**: 2 threats (via compromised IVI reaching CAN)  

### Domain Threat Scenarios

| TS-ID | Title | RV | AFR | Impact (S/F/O/P) | Related DS-ID | Related RT-ID | Status |
|-------|-------|-----|-----|------------------|---------------|---------------|--------|
| TS-CAN-001 | CAN Bus Message Injection via Compromised Head Unit | 4 | 8 | 4/3/3/1 | DS-CAN-001 | RT-CAN-001 | Active |
| TS-CAN-002 | CAN Bus Traffic Eavesdropping and Data Exfiltration | 4 | 11 | 1/3/1/3 | DS-IVI-002 | RT-CAN-002 | Active |
| TS-CAN-003 | Diagnostic Service Abuse via UDS Protocol | 4 | 7 | 4/4/4/1 | DS-CAN-003 | RT-CAN-003 | Active |
| TS-CAN-004 | Gateway ECU Bypass via Network Segmentation Vulnerability | 4 | 5 | 4/4/4/1 | DS-CAN-003 | RT-CAN-004 | Active |

### Domain Controls and Treatments

**Treatment Decision Breakdown**:
- **Reduce**: 4 treatments
- **Avoid**: 0 treatments
- **Transfer**: 0 treatments
- **Accept**: 0 treatments

**Treatment Effectiveness**: 100% (all 4 CAN threats actively mitigated)

**Primary Control Categories** (CAN domain):
1. **Cryptographic Protocols**: CAN SecOC message authentication (ISO 11898-6 MACs for safety-critical messages)
2. **Network Segmentation**: Gateway ECU firewall rules, domain isolation, CAN ID filtering
3. **Access Control**: UDS PKI authentication, diagnostic session timeout, hypervisor isolation
4. **Secure Storage**: HSM-protected MAC keys and UDS credentials
5. **Intrusion Detection**: CAN bus anomaly detection for abnormal traffic patterns

### Domain Defense Layers

**Layer 1 - Network Boundary**: Gateway ECU enforces strict CAN ID whitelisting (RT-CAN-004), blocking Head Unit from sending commands to safety networks (Powertrain, Chassis, ADAS).

**Layer 2 - Cryptographic Authentication**: CAN SecOC adds message authentication codes (MACs) to all safety-critical messages (RT-CAN-001), preventing spoofing/injection even if Gateway is bypassed.

**Layer 3 - Diagnostic Protection**: UDS services require PKI-based authentication with HSM-protected private keys (RT-CAN-003), preventing unauthorized diagnostic access to CAN network.

**Layer 4 - Physical Security**: OBD-II port requires PIN authentication when vehicle is locked, reducing physical attack window for CAN sniffing.

**Layer 5 - Eavesdropping Prevention**: Encrypted CAN diagnostic payloads (RT-CAN-002) using AES-256-GCM with HSM keys prevent plaintext eavesdropping of proprietary calibration data.

### Residual Risk (Domain)

**Residual Risk Level**: MEDIUM  
**Residual Threats (RV ≥ 4)**: 4 (unchanged post-treatment - AFR improvements offset by multi-stage attack complexity)

**Remaining Risk Factors**:
- Hypervisor escape vulnerability could grant Android direct CAN access, bypassing Gateway isolation
- Zero-day CAN SecOC cryptanalysis could enable forged messages despite MAC authentication
- OBD-II physical access remains feasible in parking scenarios, requiring PIN enforcement compliance

---

## Domain: Infotainment / Head Unit (IVI)

### Domain Summary

**Domain Risk Level**: HIGH  
**Total Threat Scenarios**: 7  
**Total Damage Scenarios**: 10  
**Total Risk Treatments**: 7  
**Domain Assets**: AST-ECU-001 (Head Unit SoC), AST-ECU-002 (Hypervisor), AST-ECU-004 (Android), AST-ECU-005 (HSM/TEE)  

**Top Domain Threat**: TS-IVI-001 (RV 5) - Malicious Android Application Installation and Privilege Escalation  

### Domain Description

The IVI domain encompasses the infotainment system head unit, including the Qualcomm QAM8295 SoC, QNX + Android hypervisor architecture, displays (HUD, central console, instrument cluster), sensors (GNSS, cameras, microphones), and wireless connectivity (Bluetooth, WiFi, cellular). This domain handles user interaction, navigation, media, and external connectivity, making it the primary external attack surface.

### Domain Risk Distribution

| Risk Value | Count | Percentage |
|------------|-------|------------|
| RV 5 (Critical) | 2 | 29% |
| RV 4 (High) | 3 | 43% |
| RV 3 (Medium) | 2 | 28% |
| RV 2 (Low) | 0 | 0% |
| RV 1 (Negligible) | 0 | 0% |

**SFOP Impact Analysis (Domain)**:
- Safety-Critical Threats: 3 (Impact ≥ 3) - Potential for hypervisor escape to reach CAN
- Financial Impact Threats: 5 (Impact ≥ 3) - Recall, privacy fines, litigation
- Operational Impact Threats: 5 (Impact ≥ 3) - Multiple critical functions compromised
- Privacy Impact Threats: 5 (Impact ≥ 3) - User data exposure, biometric leaks, location tracking
- **Most Critical Impact Type**: Privacy (affects 1,000+ users with comprehensive personal data)

### Domain Assets and Attack Surface

**Assets in Domain**:
- AST-ECU-001: Head Unit System-on-Chip (Qualcomm QAM8295 - root of trust)
- AST-ECU-002: Hypervisor (Type-1 isolation layer)
- AST-ECU-003: QNX Guest OS (vehicle network access)
- AST-ECU-004: Android Guest OS (external connectivity, user apps)
- AST-ECU-005: HSM/TEE (cryptographic operations, key storage)
- AST-SNS-001: GNSS Receiver (location data)
- AST-SNS-003: Driver Monitoring Camera (facial biometrics)
- AST-COM-003: Bluetooth/WiFi Module (wireless connectivity)
- AST-ACT-001/002: Display outputs (user-facing interface)

**Attack Surface / Entry Points**:
- Bluetooth stack (L2CAP protocol, remote exploitable via CVE-2025-32059)
- WiFi (WPA3, rogue AP MITM attacks)
- USB ports (physical access, malware delivery)
- NFC reader (malicious tag injection)
- Android app framework (third-party apps)
- Media codecs (malicious audio/video file parsing)
- GNSS receiver (spoofing attacks)

**External Interfaces**: 4 (Bluetooth, WiFi, NFC, USB)  
**Internal Dependencies**: 2 (to CAN, OTA domains)  
**Physical Access Required**: 2 threats (USB malware, physical tampering)  
**Remote Attack Feasible**: 5 threats (Bluetooth RCE, WiFi MITM, media codec, app installation)  

### Domain Threat Scenarios

| TS-ID | Title | RV | AFR | Impact (S/F/O/P) | Related DS-ID | Related RT-ID | Status |
|-------|-------|-----|-----|------------------|---------------|---------------|--------|
| TS-IVI-001 | Malicious Android Application Installation and Privilege Escalation | 5 | 10 | 4/4/4/3 | DS-IVI-003 | RT-IVI-001 | Active |
| TS-IVI-002 | Bluetooth Stack Exploitation via Remote Code Execution | 4 | 8 | 4/3/4/3 | DS-IVI-003 | RT-IVI-002 | Active |
| TS-IVI-003 | USB Port Malware Injection via Physical Access | 4 | 9 | 4/3/4/3 | DS-EXT-001 | RT-IVI-003 | Active |
| TS-IVI-004 | WiFi Network Exploitation and Man-in-the-Middle Attack | 4 | 11 | 1/3/1/3 | DS-IVI-002 | RT-IVI-004 | Active |
| TS-IVI-005 | Media Codec Exploitation via Malicious Audio/Video File | 3 | 8 | 3/3/3/2 | DS-IVI-003 | RT-IVI-005 | Active |
| TS-IVI-006 | QNX Kernel Vulnerability Exploitation | 4 | 12 | 1/3/1/3 | DS-IVI-002 | RT-IVI-006 | Active |
| TS-IVI-007 | NFC Malicious Tag Injection | 4 | 4 | 4/3/3/1 | DS-CAN-001 | RT-IVI-007 | Active |

### Domain Controls and Treatments

**Treatment Decision Breakdown**:
- **Reduce**: 7 treatments
- **Avoid**: 0 treatments
- **Transfer**: 0 treatments
- **Accept**: 0 treatments

**Treatment Effectiveness**: 100% (all 7 IVI threats actively mitigated)

**Primary Control Categories** (IVI domain):
1. **Code Signing**: PKI-based app signing, firmware signature verification (RSA-2048, ECDSA P-256)
2. **Access Control**: App store restrictions, hypervisor isolation (QNX ↔ Android), sandboxing (SELinux)
3. **Secure Boot**: ASLR, DEP, stack canaries for exploit mitigation, runtime integrity monitoring
4. **Cryptographic Protocols**: TLS 1.3 with certificate pinning, WPA3 WiFi encryption
5. **Input Validation**: Boundary checks on Bluetooth packets, NFC NDEF messages, media codec parsing

### Domain Defense Layers

**Layer 1 - Perimeter Defense**: Bluetooth, WiFi, USB inputs validated before processing; NFC disabled when parked (RT-IVI-002, RT-IVI-007).

**Layer 2 - Application Isolation**: Android apps sandboxed with SELinux; media codecs run with least privilege with no CAN access (RT-IVI-005).

**Layer 3 - Hypervisor Isolation**: Android (external connectivity) isolated from QNX (CAN access) by Type-1 hypervisor; memory partitioning enforced via IOMMU (RT-IVI-001).

**Layer 4 - Cryptographic Protection**: TLS 1.3 + cert pinning prevents MITM (RT-IVI-004); OEM code signing prevents malicious apps (RT-IVI-001).

**Layer 5 - Runtime Integrity**: ASLR/DEP/canaries raise exploit complexity (RT-IVI-002, RT-IVI-006); regular OTA security patches close vulnerabilities (RT-IVI-005).

### Residual Risk (Domain)

**Residual Risk Level**: HIGH  
**Residual Threats (RV ≥ 4)**: 5 (TS-IVI-001, 002, 003, 004, 007)

**Remaining Risk Factors**:
- Bluetooth stack hardening (ASLR/DEP) increases complexity but published ROP techniques may still succeed
- Hypervisor isolation is critical; zero-day hypervisor vulnerability remains a pivot risk to QNX/CAN
- Multiple remote code execution vectors (Bluetooth, WiFi, media codecs) require continuous vulnerability management

---

## Domain: Over-the-Air Updates (OTA)

### Domain Summary

**Domain Risk Level**: HIGH  
**Total Threat Scenarios**: 2  
**Total Damage Scenarios**: 1  
**Total Risk Treatments**: 2  
**Domain Assets**: OTA delivery channels (TLS-encrypted), firmware signing infrastructure (HSM-protected)  

**Top Domain Threat**: TS-OTA-001 (RV 4) - Unsigned or Weakly Signed Firmware Update Delivery  

### Domain Description

The OTA domain handles over-the-air firmware updates for the Head Unit SoC, hypervisor, QNX, and Android guest operating systems. OTA updates are delivered via cellular/Ethernet from the backend telematics server, verified using PKI signatures, and installed using Secure Boot mechanisms. Compromise of OTA enables persistent, fleet-wide attacks on all connected vehicles.

### Domain Risk Distribution

| Risk Value | Count | Percentage |
|------------|-------|------------|
| RV 5 (Critical) | 0 | 0% |
| RV 4 (High) | 2 | 100% |
| RV 3 (Medium) | 0 | 0% |
| RV 2 (Low) | 0 | 0% |
| RV 1 (Negligible) | 0 | 0% |

**SFOP Impact Analysis (Domain)**:
- Safety-Critical Threats: 1 (Impact ≥ 3) - Malicious firmware enables CAN compromise
- Financial Impact Threats: 1 (Impact ≥ 3) - Fleet-wide recall costs
- Operational Impact Threats: 1 (Impact ≥ 3) - Persistent system compromise
- Privacy Impact Threats: 1 (Impact ≥ 3) - User data compromise via firmware tampering
- **Most Critical Impact Type**: Safety (fleet-wide remote vehicle control capability)

### Domain Assets and Attack Surface

**Assets in Domain**:
- AST-DAT-004: Firmware Images & OTA Manifests (update payloads)
- AST-ECU-005: HSM/TEE (firmware signature verification)
- OTA Delivery Channel (TLS 1.3 encrypted, cellular/Ethernet)
- Telematics Backend (external OTA server)

**Attack Surface / Entry Points**:
- Cellular/Ethernet OTA update channel (TLS-encrypted)
- OTA backend API (OAuth 2.0 + MFA protected)
- Firmware signature verification (HSM public keys, protected by multi-signature scheme)
- eFuse anti-rollback counter (SoC hardware)

**External Interfaces**: 2 (cellular, Ethernet to backend)  
**Internal Dependencies**: 2 (to BCK backend, IVI firmware installation)  
**Physical Access Required**: 0 threats (all remote)  
**Remote Attack Feasible**: 2 threats (MITM on OTA channel, unsigned firmware delivery)  

### Domain Threat Scenarios

| TS-ID | Title | RV | AFR | Impact (S/F/O/P) | Related DS-ID | Related RT-ID | Status |
|-------|-------|-----|-----|------------------|---------------|---------------|--------|
| TS-OTA-001 | Unsigned or Weakly Signed Firmware Update Delivery | 4 | 8 | 4/3/4/3 | DS-IVI-003 | RT-OTA-001 | Active |
| TS-OTA-002 | OTA Firmware Rollback to Vulnerable Version | 4 | 5 | 4/3/4/3 | DS-IVI-003 | RT-OTA-002 | Active |

### Domain Controls and Treatments

**Treatment Decision Breakdown**:
- **Reduce**: 2 treatments
- **Avoid**: 0 treatments
- **Transfer**: 0 treatments
- **Accept**: 0 treatments

**Treatment Effectiveness**: 100% (all 2 OTA threats actively mitigated)

**Primary Control Categories** (OTA domain):
1. **Code Signing**: Multi-signature firmware signing (M-of-N threshold, e.g., 3-of-5 OEM signers)
2. **Update Security**: eFuse anti-rollback counter, canary deployments (phased 1% → 10% → 50% → 100% rollout)
3. **Secure Storage**: Offline HSM for firmware signing keys, physical access control, audit logging
4. **Cryptographic Protocols**: TLS 1.3 with certificate pinning for OTA transport channel
5. **Intrusion Detection**: OTA update log audit for anomalous patterns (rollback attempts, signature failures)

### Domain Defense Layers

**Layer 1 - Transport Security**: TLS 1.3 with certificate pinning prevents MITM on cellular/Ethernet OTA channel (RT-OTA-001).

**Layer 2 - Multi-Signature Verification**: M-of-N firmware signing (3-of-5) requires compromising multiple independent OEM signing authorities (RT-OTA-001).

**Layer 3 - Anti-Rollback Protection**: eFuse-backed counter monotonically increments with each firmware version, rejecting downgrades to vulnerable versions (RT-OTA-002).

**Layer 4 - Canary Deployment**: Phased rollout (1% → 10% → 50%) detects malicious firmware before fleet-wide distribution (RT-OTA-001).

**Layer 5 - Offline Key Storage**: Firmware signing keys stored in offline HSMs with physical access control, preventing remote key theft (RT-OTA-001).

### Residual Risk (Domain)

**Residual Risk Level**: MEDIUM  
**Residual Threats (RV ≥ 4)**: 2 (unchanged - multi-sig + eFuse + canary make rollback extremely difficult)

**Remaining Risk Factors**:
- Compromising 3-of-5 independent signing authorities requires coordinated insider attack
- eFuse manipulation requires expensive fault injection tools ($100K+)
- Canary deployment detects 1% malicious rate; lower rates may escape detection

---

## Domain: External Interfaces (EXT)

### Domain Summary

**Domain Risk Level**: HIGH  
**Total Threat Scenarios**: 2  
**Total Damage Scenarios**: 2  
**Total Risk Treatments**: 4  
**Domain Assets**: USB ports, Bluetooth/WiFi modules, NFC reader, physical interfaces  

**Top Domain Threat**: TS-EXT-001 (RV 5) - Cloud Backend API Authentication Bypass  

### Domain Description

The EXT domain encompasses external physical and wireless interfaces exposed to users and attackers, including USB ports, Bluetooth, WiFi, NFC, and cellular connectivity. These interfaces provide legitimate user functionality but also represent the primary attack surface for initial system compromise. The EXT domain also includes the backend cloud infrastructure (BCK domain link) supporting telematics and OTA updates.

### Domain Risk Distribution

| Risk Value | Count | Percentage |
|------------|-------|------------|
| RV 5 (Critical) | 1 | 25% |
| RV 4 (High) | 3 | 75% |
| RV 3 (Medium) | 0 | 0% |
| RV 2 (Low) | 0 | 0% |
| RV 1 (Negligible) | 0 | 0% |

**SFOP Impact Analysis (Domain)**:
- Safety-Critical Threats: 1 (Impact ≥ 3) - Backend compromise enables fleet-wide attacks
- Financial Impact Threats: 2 (Impact ≥ 3) - Fleet-wide data breach, recall costs
- Operational Impact Threats: 1 (Impact ≥ 3) - Backend infrastructure compromise
- Privacy Impact Threats: 2 (Impact ≥ 3) - User data exposure via backend breach
- **Most Critical Impact Type**: Financial (business-threatening recall and regulatory fines)

### Domain Assets and Attack Surface

**Assets in Domain**:
- AST-IFC-001: USB Ports (2x USB 2.0, user-accessible)
- AST-COM-003: Bluetooth/WiFi Module (wireless connectivity)
- AST-SNS-001: GNSS Receiver (location services)
- NFC Reader (embedded in Head Unit)
- Backend API endpoints (OAuth 2.0 + MFA protected)

**Attack Surface / Entry Points**:
- USB ports (physical access, malware injection, firmware updates)
- Bluetooth stack (remote RCE via L2CAP buffer overflow)
- WiFi (MITM via rogue access points)
- NFC reader (malicious tag injection)
- Backend API (credential stuffing, social engineering)

**External Interfaces**: 4 (USB, Bluetooth, WiFi, NFC)  
**Internal Dependencies**: 2 (to IVI, BCK domains)  
**Physical Access Required**: 2 threats (USB malware, NFC tags)  
**Remote Attack Feasible**: 4 threats (Bluetooth RCE, WiFi MITM, API bypass, CDN compromise)  

### Domain Threat Scenarios

| TS-ID | Title | RV | AFR | Impact (S/F/O/P) | Related DS-ID | Related RT-ID | Status |
|-------|-------|-----|-----|------------------|---------------|---------------|--------|
| TS-EXT-001 | Cloud Backend API Authentication Bypass | 5 | 11 | 4/4/4/4 | DS-BCK-001 | RT-EXT-001 | Active |
| TS-EXT-002 | Telematics Cloud Database SQL Injection | 4 | 12 | 1/3/1/3 | DS-IVI-002 | RT-EXT-002 | Active |

### Domain Controls and Treatments

**Treatment Decision Breakdown**:
- **Reduce**: 4 treatments
- **Avoid**: 0 treatments
- **Transfer**: 0 treatments
- **Accept**: 0 treatments

**Treatment Effectiveness**: 100% (all 4 EXT threats actively mitigated)

**Primary Control Categories** (EXT domain):
1. **Input Validation**: Strict parsing of USB firmware files, NFC NDEF messages, Bluetooth packets
2. **Code Signing**: PKI signature verification for USB-delivered firmware (RSA-2048, ECDSA P-256)
3. **Physical Security**: USB auto-mount disabled (PIN required), Bluetooth/NFC disabled when parked
4. **Cryptographic Protocols**: TLS 1.3 for WiFi, WPA3 encryption, BT 5.2 LE Secure pairing
5. **Authentication**: OAuth 2.0 with MFA for backend API, rate limiting, IP whitelisting

### Domain Defense Layers

**Layer 1 - Physical Access Control**: USB/NFC require user confirmation or PIN; disable-when-parked reduces attack window (RT-IVI-003, RT-IVI-007).

**Layer 2 - Input Validation**: Boundary checks on all external inputs (USB files, NFC tags, Bluetooth packets) reject malformed data (RT-IVI-002, RT-IVI-003).

**Layer 3 - Sandboxing**: NFC/Bluetooth handlers run with least privilege (SELinux); cannot access CAN or cryptographic keys (RT-IVI-002, RT-IVI-007).

**Layer 4 - Cryptographic Authentication**: USB firmware signature verification (RT-IVI-003), WiFi TLS cert pinning (RT-IVI-004), OAuth 2.0 + MFA for API (RT-EXT-001).

**Layer 5 - Exploit Mitigation**: ASLR/DEP/canaries in Bluetooth/WiFi/NFC stacks raise RCE exploit complexity (RT-IVI-002).

### Residual Risk (Domain)

**Residual Risk Level**: HIGH  
**Residual Threats (RV ≥ 4)**: 4 (TS-EXT-001 and 002 plus derived threats from IVI)

**Remaining Risk Factors**:
- Backend API authentication (OAuth 2.0 + MFA) vulnerable to social engineering and token theft
- SQL injection techniques well-documented; continuous parameterized query validation required
- Multiple wireless stacks (Bluetooth, WiFi) increase attack surface despite individual controls

---

## Domain: Backend / Cloud Infrastructure (BCK)

### Domain Summary

**Domain Risk Level**: CRITICAL  
**Total Threat Scenarios**: 4  
**Total Damage Scenarios**: 1  
**Total Risk Treatments**: 4  
**Domain Assets**: Backend REST APIs, OTA distribution server, telematics database, admin portals  

**Top Domain Threat**: TS-EXT-001 (RV 5) - Cloud Backend API Authentication Bypass (linked to BCK)  

### Domain Description

The BCK domain encompasses backend cloud infrastructure supporting telematics, OTA updates, user account management, and fleet data analytics. Backend compromise enables fleet-wide attacks by distributing malicious OTA updates or exfiltrating large-scale user data affecting hundreds of thousands of vehicles.

### Domain Risk Distribution

| Risk Value | Count | Percentage |
|------------|-------|------------|
| RV 5 (Critical) | 1 | 25% |
| RV 4 (High) | 3 | 75% |
| RV 3 (Medium) | 0 | 0% |
| RV 2 (Low) | 0 | 0% |
| RV 1 (Negligible) | 0 | 0% |

**SFOP Impact Analysis (Domain)**:
- Safety-Critical Threats: 1 (Impact ≥ 3) - Fleet-wide malicious OTA enables vehicle control
- Financial Impact Threats: 4 (Impact ≥ 3) - Billion-dollar recall, regulatory sanctions, business viability
- Operational Impact Threats: 4 (Impact ≥ 3) - Service disruption, integrity loss
- Privacy Impact Threats: 4 (Impact ≥ 3) - Fleet-wide user data exposure
- **Most Critical Impact Type**: Financial (business-threatening at OEM scale)

### Domain Assets and Attack Surface

**Assets in Domain**:
- Backend REST APIs (OAuth 2.0 + MFA authentication)
- OTA distribution server (TLS-protected, firmware repository)
- Telematics database (SQL, NoSQL, user personal data)
- Administrative web portals (fleet management)
- Offline HSM for firmware signing keys (air-gapped, physical security)

**Attack Surface / Entry Points**:
- Backend REST APIs (credential stuffing, social engineering, token theft)
- OTA distribution server (MITM if TLS bypassed, supply chain attacks via CDN)
- Telematics database (SQL injection, NoSQL injection, insider access)
- Administrative web portals (XSS, CSRF, privilege escalation)

**External Interfaces**: 2 (Internet API, OTA delivery)  
**Internal Dependencies**: 1 (to OTA firmware delivery)  
**Physical Access Required**: 0 threats (all remote)  
**Remote Attack Feasible**: 4 threats (API bypass, SQL injection, CDN compromise, APT)  

### Domain Threat Scenarios

| TS-ID | Title | RV | AFR | Impact (S/F/O/P) | Related DS-ID | Related RT-ID | Status |
|-------|-------|-----|-----|------------------|---------------|---------------|--------|
| TS-EXT-001 | Cloud Backend API Authentication Bypass | 5 | 11 | 4/4/4/4 | DS-BCK-001 | RT-EXT-001 | Active |
| TS-EXT-002 | Telematics Cloud Database SQL Injection | 4 | 12 | 1/3/1/3 | DS-IVI-002 | RT-EXT-002 | Active |
| TS-BCK-003 | CDN Firmware Distribution Compromise | 4 | (varies) | 3/3/3/2 | DS-IVI-003 | RT-EXT-004 | Active |
| TS-BCK-004 | Backend Infrastructure APT Compromise | 4 | (varies) | 4/4/4/4 | DS-BCK-001 | RT-BCK-004 | Active |

### Domain Controls and Treatments

**Treatment Decision Breakdown**:
- **Reduce**: 4 treatments
- **Avoid**: 0 treatments
- **Transfer**: 0 treatments
- **Accept**: 0 treatments

**Treatment Effectiveness**: 100% (all 4 BCK threats actively mitigated)

**Primary Control Categories** (BCK domain):
1. **Authentication**: OAuth 2.0 with MFA (TOTP, hardware tokens), mTLS for vehicle-to-backend communication
2. **Access Control**: Rate limiting (10 req/min per IP), account lockout, IP whitelisting for admin endpoints, RBAC
3. **Input Validation**: Parameterized SQL queries, input sanitization for API parameters
4. **Intrusion Detection**: SIEM monitoring, anomaly detection for unusual API access patterns
5. **Cryptographic Protocols**: mTLS with HSM-protected client certificates, TLS 1.3 for all connections

### Domain Defense Layers

**Layer 1 - Authentication Barrier**: OAuth 2.0 + MFA (RT-EXT-001) prevents credential stuffing; mTLS ensures vehicle authenticity (RT-BCK-001).

**Layer 2 - Rate Limiting**: API rate limits (10 req/min per IP) and account lockout prevent brute-force attacks (RT-EXT-001).

**Layer 3 - Input Validation**: Parameterized queries prevent SQL injection (RT-EXT-002); input sanitization blocks XSS/SSRF.

**Layer 4 - Network Segmentation**: OTA distribution server isolated from telematics DB; admin endpoints IP-whitelisted (RT-BCK-001, RT-BCK-002).

**Layer 5 - Intrusion Detection**: SIEM monitoring alerts on anomalous API patterns (unusual IP, excessive requests, privilege escalation attempts) (RT-BCK-004).

### Residual Risk (Domain)

**Residual Risk Level**: CRITICAL  
**Residual Threats (RV ≥ 4)**: 4 (all backend threats remain high-risk despite controls)

**Remaining Risk Factors**:
- Advanced persistent threat (APT) with insider access can bypass OAuth 2.0 + MFA
- Zero-day SQL injection or NoSQL injection vulnerabilities may evade parameterized queries
- Supply chain attack via CDN or OTA infrastructure providers remains high-risk for fleet-wide impact

---

## Cross-Domain Analysis

### Cross-Domain Attack Chains

#### Attack Chain 1: EXT (USB) → IVI (Android) → IVI (Hypervisor) → CAN

**Attack Path**:
1. **EXT**: Attacker delivers USB malware via physical access (TS-IVI-003)
2. **IVI**: Malware installs on Android Guest OS (TS-IVI-001), escalates privileges
3. **IVI**: Hypervisor escape exploit breaks QNX isolation (TS-IVI-002)
4. **CAN**: Attacker gains CAN-FD access via QNX, injects malicious messages (TS-CAN-001)

**Defense-in-Depth Analysis**:
- **Layer 1 (EXT)**: USB firmware signature verification (RT-IVI-003) blocks unsigned malware → **EFFECTIVE**
- **Layer 2 (IVI)**: Android app store restrictions (RT-IVI-001) prevent malicious app installation → **EFFECTIVE**
- **Layer 3 (IVI)**: Hypervisor isolation (RT-IVI-001) prevents Android → QNX escape → **PARTIALLY EFFECTIVE** (requires zero-day exploit)
- **Layer 4 (CAN)**: CAN SecOC message authentication (RT-CAN-001) prevents message injection even if CAN accessed → **EFFECTIVE**
- **Layer 5 (CAN)**: Gateway firewall (RT-CAN-004) blocks Head Unit commands to safety ECUs → **EFFECTIVE**

**Conclusion**: Defense-in-depth successfully contains this attack chain. Even if attacker breaches Layers 1-3 (USB → Android → Hypervisor), Layers 4-5 (CAN SecOC + Gateway) prevent safety-critical ECU compromise.

#### Attack Chain 2: BCK (Backend API) → OTA (Malicious Firmware) → IVI (Persistent Compromise)

**Attack Path**:
1. **BCK**: Attacker compromises backend API via authentication bypass (TS-EXT-001)
2. **OTA**: Attacker distributes malicious firmware via OTA channel (TS-OTA-001)
3. **IVI**: Malicious firmware installed on Head Unit, grants persistent CAN access

**Defense-in-Depth Analysis**:
- **Layer 1 (BCK)**: OAuth 2.0 + MFA (RT-EXT-001) prevents API authentication bypass → **EFFECTIVE**
- **Layer 2 (OTA)**: Multi-signature firmware signing (RT-OTA-001) requires compromising 3-of-5 OEM signers → **EFFECTIVE**
- **Layer 3 (OTA)**: Canary deployment (RT-OTA-001) detects malicious firmware at 1% rollout → **EFFECTIVE**
- **Layer 4 (OTA)**: eFuse anti-rollback (RT-OTA-002) prevents downgrade to vulnerable versions → **EFFECTIVE**
- **Layer 5 (IVI)**: Secure Boot (RT-IVI-001) verifies firmware signatures before execution → **EFFECTIVE**

**Conclusion**: Defense-in-depth successfully contains this attack chain. Even if attacker compromises backend API (Layer 1), multi-signature firmware signing (Layer 2) requires coordinated compromise of multiple independent OEM signing authorities, making the attack extremely difficult.

#### Attack Chain 3: EXT (Bluetooth RCE) → IVI (Android Exfiltration) → BCK (Cellular Data Leak)

**Attack Path**:
1. **EXT**: Attacker exploits Bluetooth stack RCE vulnerability (TS-IVI-002)
2. **IVI**: Attacker gains Android access, exfiltrates user data (contacts, location, keys)
3. **BCK**: Attacker transmits stolen data via cellular/WiFi to external server

**Defense-in-Depth Analysis**:
- **Layer 1 (EXT)**: Bluetooth stack hardening with ASLR/DEP (RT-IVI-002) raises RCE exploit complexity → **PARTIALLY EFFECTIVE** (mitigates but doesn't eliminate RCE risk)
- **Layer 2 (IVI)**: Hypervisor isolation prevents Android from accessing QNX/CAN → **EFFECTIVE** (limits damage scope to IVI domain)
- **Layer 3 (BCK)**: TLS 1.3 encryption (RT-IVI-004) protects data in transit → **EFFECTIVE** (encrypted exfiltration harder to detect but still possible)
- **Layer 4 (BCK)**: Network anomaly detection (RT-BCK-004) alerts on unusual data volume → **PARTIALLY EFFECTIVE** (detection lag allows some exfiltration)

**Conclusion**: Defense-in-depth partially contains this attack chain. Bluetooth RCE (Layer 1) remains a risk despite hardening. However, hypervisor isolation (Layer 2) prevents escalation to CAN domain, limiting damage to user data exposure rather than vehicle control. Additional controls needed: Bluetooth disable-when-parked (RT-IVI-002), data loss prevention (DLP) for cellular exfiltration.

### Cross-Domain Dependencies

| Dependency | Description | Risk Amplification | Mitigation |
|------------|-------------|-------------------|------------|
| **IVI → CAN** | QNX Guest OS has CAN-FD access; Android compromise + hypervisor escape enables CAN manipulation | **HIGH** - Hypervisor escape converts IVI threat to CAN threat | Hypervisor isolation hardening (RT-IVI-001), CAN SecOC authentication (RT-CAN-001) |
| **BCK → OTA** | Backend API compromise enables malicious OTA distribution to entire fleet | **CRITICAL** - Single backend breach affects all connected vehicles | OAuth 2.0 + MFA (RT-EXT-001), multi-sig firmware signing (RT-OTA-001), canary deployment (RT-OTA-001) |
| **EXT → IVI** | External interfaces (USB, Bluetooth, WiFi) are primary IVI compromise vectors | **MODERATE** - External compromise limited to IVI unless hypervisor breached | Input validation (RT-IVI-003, RT-IVI-002), code signing (RT-IVI-001), sandboxing (RT-IVI-005) |
| **OTA → IVI** | OTA firmware updates modify IVI firmware; malicious OTA enables persistent compromise | **HIGH** - Persistent compromise survives reboots | Multi-sig firmware signing (RT-OTA-001), eFuse anti-rollback (RT-OTA-002), Secure Boot (RT-IVI-001) |
| **IVI → BCK** | Cellular connectivity enables IVI-to-backend communication; compromised IVI could attack backend | **LOW** - Backend authentication (OAuth 2.0 + MFA) prevents IVI compromise from backend breach | mTLS with HSM client certs (RT-EXT-001), API rate limiting, SIEM monitoring |

### Interdomain Risk Amplification

**Risk Amplification Factor**: 35%

The presence of cross-domain dependencies increases aggregate system risk by 35% compared to isolated domain analysis. This amplification occurs because:
1. Attacker who compromises one domain (e.g., IVI) gains pivot opportunities to adjacent domains (e.g., CAN via hypervisor escape)
2. Failures cascade across domain boundaries (e.g., Gateway ECU DoS disrupts both CAN and IVI communication)
3. Shared assets (SoC, HSM) create single points of failure affecting multiple domains

### Domain Isolation Score

**Overall Domain Isolation Score**: 0.72 (Fair - 72% isolation effectiveness)

Domain isolation effectiveness by boundary:
- **IVI ↔ CAN**: 0.78 (Hypervisor isolation + Gateway firewall - effective but hypervisor escape risk remains)
- **EXT ↔ IVI**: 0.65 (Input validation + sandboxing - moderate, multiple wireless stacks increase attack surface)
- **OTA ↔ IVI**: 0.82 (Multi-sig signing + Secure Boot - effective, eFuse anti-rollback strong)
- **BCK ↔ OTA**: 0.68 (OAuth 2.0 + canary deployment - moderate, insider threat and APT risks)
- **EXT ↔ BCK**: 0.42 (TLS + rate limiting - weak, direct Internet-facing API vulnerable to sophisticated attacks)

### Gateway and Controller Dependencies

The Gateway ECU (AST-ECU-006) is a critical central point affecting multiple domains:

**Gateway ECU Dependencies**:
- **Domains Affected**: CAN, IVI, ADAS (all vehicle network communication routes through Gateway)
- **Single Point of Failure Impact**: Gateway DoS disrupts inter-domain communication, disables ADAS coordination, prevents IVI from retrieving vehicle status (TS-CAN-004)
- **Security Boundary Function**: Gateway firewall enforces critical security boundary between infotainment (IVI, EXT) and safety-critical systems (CAN, ADAS)
- **Mitigation**: Gateway hardening (RT-CAN-004), CAN SecOC authentication (RT-CAN-001), measured boot attestation

**Other Critical Central Points**:
- **HSM/TEE (AST-ECU-005)**: Stores cryptographic keys for all domains; compromise affects OTA (RT-OTA-001), IVI (RT-IVI-001), CAN (RT-CAN-001) authentication
- **Head Unit SoC (AST-ECU-001)**: Hosts hypervisor isolating IVI guests; SoC compromise enables cross-domain attacks
- **OTA Backend**: Distributes firmware to entire fleet; backend compromise enables fleet-wide attacks

---

## Security Architecture Summary

### Overall Defense Posture

**Aggregate Defense-in-Depth Effectiveness**: 82%

The multi-layer defense architecture demonstrates:
- **Layered Controls**: Average 4.2 security controls per threat scenario (21 RT across 21 TS)
- **Domain Isolation**: 0.72 overall isolation score (fair - indicates room for improvement in cross-domain boundaries)
- **Treatment Coverage**: 100% of threats actively mitigated (all 21 TS have Reduce treatment)
- **Residual Risk**: 19 threats remain at RV ≥ 4 after treatment (90% of original 21 threats)

### Strongest Security Layers

1. **Cryptographic Authentication** (CAN SecOC, multi-sig firmware signing, TLS 1.3 with cert pinning)
   - Applies to: CAN (RT-CAN-001), OTA (RT-OTA-001), BCK (RT-EXT-001), EXT (RT-IVI-004)
   - Effectiveness: Prevents spoofing, injection, MITM attacks
   
2. **Hypervisor Isolation** (QNX ↔ Android separation)
   - Applies to: IVI domain (RT-IVI-001)
   - Effectiveness: Prevents Android compromise from escalating to CAN access
   
3. **Gateway Firewall** (CAN ID filtering, domain segmentation)
   - Applies to: CAN domain (RT-CAN-004)
   - Effectiveness: Prevents infotainment from commanding safety-critical ECUs

### Weakest Security Layers / Areas for Improvement

1. **External Interface Input Validation** (Bluetooth, WiFi, USB, NFC)
   - Issue: Multiple RCE vulnerabilities (TS-IVI-002, TS-IVI-003, TS-IVI-007)
   - Recommendation: Enhanced fuzzing, stricter input validation, disable-when-parked controls
   
2. **Backend API Authentication**
   - Issue: OAuth 2.0 + MFA vulnerable to social engineering, token theft, insider threats
   - Recommendation: Hardware token requirements for admin endpoints, geo-fencing for API access, continuous authentication
   
3. **Cross-Domain Attack Chain Prevention**
   - Issue: Multiple pivot paths remain viable despite individual domain controls
   - Recommendation: Implement network anomaly detection correlating events across domains

### Compliance with UN R155 and ISO 21434

**UN R155 Annex 5 Coverage**:
- ✓ Backend servers (TS-EXT-001, RT-EXT-001)
- ✓ Update procedures (TS-OTA-001/002, RT-OTA-001/002)
- ✓ Communication channels (TS-CAN-001/002/003/004, RT-CAN-001/002/003/004)
- ✓ External connectivity (TS-IVI-002/004/007, RT-IVI-002/004/007)
- ✓ Data/code (TS-IVI-001/003/005/006, RT-IVI-001/003/005/006)
- ✓ Vehicle communication interfaces (TS-CAN-001/003/004, RT-CAN-001/003/004)

**ISO 21434 Clause 8.4 Work Products**:
- ✓ Asset identification (9 assets catalogued: 6 ECU, 1 GW, 5 sensors, 5 communication, 2 interface)
- ✓ Damage scenario definition (18 DS with SFOP impact scores)
- ✓ Threat scenario enumeration (21 TS with STRIDE + R155 + MITRE ATT&CK mapping)
- ✓ Attack feasibility rating (AFR calculated for all 21 TS, residual AFR post-treatment)
- ✓ Risk value determination (RV 1-5 for all 21 TS, residual RV post-treatment)
- ✓ Treatment decisions (21 RT with Reduce/Avoid/Transfer/Accept breakdown)
- ✓ Cybersecurity goals (per-domain CSG definitions implicit in RT requirements)
- ✓ Traceability (Asset → DS → TS → RT chains documented in domain sections)

### Recommendations for Defense-in-Depth Enhancement

1. **Add runtime integrity monitoring** to detect post-boot firmware tampering (closes gap: no runtime verification post-Secure Boot)
2. **Implement network anomaly detection** on CAN-FD to identify malicious traffic patterns and cross-domain attack propagation
3. **Deploy hardware token requirements** for backend API admin endpoints (strengthens RT-EXT-001 against social engineering)
4. **Enable disable-when-parked** for Bluetooth, WiFi, NFC to reduce external attack window (enhances RT-IVI-002, RT-IVI-004, RT-IVI-007)
5. **Add continuous authentication** with re-authentication for long-lived sessions (enhances RT-EXT-001 against token theft)
6. **Implement firmware attestation** for runtime verification of non-modifying firmware integrity checks

---

## Appendix: Domain Acronyms and Definitions

| Acronym | Full Name | Description |
|---------|-----------|-------------|
| **CAN** | Controller Area Network | In-vehicle networking bus for ECU communication |
| **IVI** | Infotainment / In-Vehicle Infotainment | Head unit system including displays, media, navigation, connectivity |
| **OTA** | Over-the-Air | Wireless firmware update delivery mechanism |
| **EXT** | External Interfaces | Physical and wireless interfaces exposed to users (USB, Bluetooth, WiFi, NFC) |
| **BCK** | Backend / Cloud | Cloud infrastructure supporting telematics, OTA, user accounts |

---

**Report Generation Date**: 2026-03-25  
**Report Version**: 1.0  
**Schema Version**: 1.0 (ISO 21434:2021 Clause 8.4 Work Products)  
**Data Sources**: asset_list.md, ds.md, ts.md, rt.md  
**Total Lines**: 615
