# Multi-layer TARA Report Template - Defense-in-Depth Analysis

**Purpose**: This report organizes threat analysis and risk assessment findings by domain, showing both domain-specific threats and cross-domain dependencies. Enables technical architecture review, defense-in-depth validation, and domain-owned risk accountability.

**ISO 21434 Alignment**: Clause 8.4 - System architecture and domain responsibilities

**Data Sources**:
- Asset Catalogue: [data/asset_list.md](data/asset_list.md)
- Damage Scenarios: [data/ds.md](data/ds.md)
- Threat Scenarios: [data/ts.md](data/ts.md)
- Attack Chains: [data/at.md](data/at.md)
- Risk Treatments: [data/rt.md](data/rt.md)
- Cybersecurity Goals: [data/csg.md](data/csg.md)

**Report Date**: {{REPORT_DATE}}
**Vehicle System**: {{VEHICLE_SYSTEM}}
**Reporting Period**: {{REPORTING_PERIOD}}
**Total Domains Analyzed**: {{DOMAIN_COUNT}}

---

## Defense-in-Depth Overview

This multi-layer report applies defense-in-depth principles to automotive cybersecurity threat analysis, organizing findings by domain to demonstrate layered security controls and cross-domain isolation strategies.

### Defense-in-Depth Principles Applied

1. **Domain Isolation**: Each domain (CAN, IVI, OTA, EXT, BCK, IMM, ADAS) operates with restricted privileges and network segmentation to prevent lateral movement
2. **Layered Controls**: Multiple security controls (cryptography, access control, network segmentation, secure boot) applied at different architectural layers
3. **Fail-Safe Design**: Single control failure does not compromise entire system; redundant protections at each layer
4. **Least Privilege**: Each domain granted minimum necessary access to assets and communication channels
5. **Attack Surface Reduction**: External-facing domains (EXT, OTA) isolated from safety-critical domains (CAN, ADAS)

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

- **EXT → IVI → CAN**: Physical USB access → Android compromise → hypervisor escape → QNX CAN access → Gateway bypass → safety ECU control
- **BCK → OTA → IVI**: Backend API compromise → malicious OTA delivery → firmware tampering → persistent system control
- **EXT (Bluetooth) → IVI → Backend**: Bluetooth RCE → Android exfiltration → cellular data leak

---

## Domain: CAN Bus and In-Vehicle Networking (CAN)

### Domain Summary

**Domain Risk Level**: {{CAN_DOMAIN_RISK_LEVEL}}
**Total Threat Scenarios**: {{CAN_THREAT_COUNT}}
**Total Damage Scenarios**: {{CAN_DAMAGE_COUNT}}
**Total Risk Treatments**: {{CAN_TREATMENT_COUNT}}
**Total Cybersecurity Goals**: {{CAN_CSG_COUNT}}
**Domain Assets**: {{CAN_ASSET_COUNT}}

**Top Domain Threat**: {{CAN_TOP_THREAT_ID}} (RV {{CAN_TOP_THREAT_RV}})

### Domain Description

The CAN domain encompasses the Controller Area Network (CAN-FD) bus and in-vehicle networking infrastructure, providing communication between ECUs for vehicle control, diagnostics, and infotainment integration. This domain handles safety-critical message routing via the Gateway ECU, making it a primary target for attackers seeking vehicle control.

### Domain Risk Distribution

| Risk Value | Count | Percentage |
|------------|-------|------------|
| RV 5 (Critical) | {{CAN_RV5_COUNT}} | {{CAN_RV5_PCT}}% |
| RV 4 (High) | {{CAN_RV4_COUNT}} | {{CAN_RV4_PCT}}% |
| RV 3 (Medium) | {{CAN_RV3_COUNT}} | {{CAN_RV3_PCT}}% |
| RV 2 (Low) | {{CAN_RV2_COUNT}} | {{CAN_RV2_PCT}}% |
| RV 1 (Negligible) | {{CAN_RV1_COUNT}} | {{CAN_RV1_PCT}}% |

**SFOP Impact Analysis (Domain)**:
- Safety-Critical Threats: {{CAN_SAFETY_COUNT}} (Impact ≥ 3)
- Financial Impact Threats: {{CAN_FINANCIAL_COUNT}} (Impact ≥ 3)
- Operational Impact Threats: {{CAN_OPERATIONAL_COUNT}} (Impact ≥ 3)
- Privacy Impact Threats: {{CAN_PRIVACY_COUNT}} (Impact ≥ 3)
- **Most Critical Impact Type**: {{CAN_CRITICAL_IMPACT_TYPE}}

### Domain Assets and Attack Surface

**Assets in Domain**:
{{CAN_ASSET_LIST}}

**Attack Surface / Entry Points**:
- OBD-II diagnostic port (physical access)
- Head Unit SoC → CAN-FD interface (via AST-COM-001)
- Gateway ECU routing interfaces (inter-domain bridge)
- UDS diagnostic service endpoints

**External Interfaces**: {{CAN_EXTERNAL_INTERFACE_COUNT}}
**Internal Dependencies**: {{CAN_INTERNAL_DEPENDENCY_COUNT}} (to IVI, OTA domains)
**Physical Access Required**: {{CAN_PHYSICAL_THREAT_COUNT}} threats
**Remote Attack Feasible**: {{CAN_REMOTE_THREAT_COUNT}} threats

### Domain Threat Scenarios

| TS-ID | Title | RV | AFR | Impact (S/F/O/P) | Related DS-ID | Related RT-ID | Status |
|-------|-------|-----|-----|------------------|---------------|---------------|--------|
{{CAN_THREAT_TABLE}}

### Domain Controls and Treatments

**Treatment Decision Breakdown**:
- **Reduce**: {{CAN_REDUCE_COUNT}} treatments
- **Avoid**: {{CAN_AVOID_COUNT}} treatments
- **Transfer**: {{CAN_TRANSFER_COUNT}} treatments
- **Accept**: {{CAN_ACCEPT_COUNT}} treatments

**Treatment Effectiveness**: {{CAN_TREATMENT_EFFECTIVENESS}}% (active mitigation rate)

**Primary Control Categories** (CAN domain):
1. **Cryptographic Protocols**: CAN SecOC message authentication (ISO 11898-6 MACs for safety-critical messages)
2. **Network Segmentation**: Gateway ECU firewall rules, domain isolation, CAN ID filtering
3. **Access Control**: UDS PKI authentication, diagnostic session timeout, hypervisor isolation
4. **Secure Storage**: HSM-protected MAC keys and UDS credentials
5. **Intrusion Detection**: CAN bus anomaly detection for abnormal traffic patterns

### Domain Defense Layers

**Layer 1 - Network Boundary**: Gateway ECU enforces strict CAN ID whitelisting, blocking Head Unit from sending commands to safety networks (Powertrain, Chassis, ADAS).

**Layer 2 - Cryptographic Authentication**: CAN SecOC adds message authentication codes (MACs) to all safety-critical messages, preventing spoofing/injection even if Gateway is bypassed.

**Layer 3 - Diagnostic Protection**: UDS services require PKI-based authentication with HSM-protected private keys, preventing unauthorized diagnostic access.

**Layer 4 - Physical Security**: OBD-II port requires PIN authentication when vehicle is locked, reducing physical attack window.

### Residual Risk (Domain)

**Residual Risk Level**: {{CAN_RESIDUAL_RISK_LEVEL}}
**Residual Threats (RV ≥ 4)**: {{CAN_RESIDUAL_THREAT_COUNT}}

**Remaining Risk Factors**:
- {{CAN_RESIDUAL_FACTOR_1}}
- {{CAN_RESIDUAL_FACTOR_2}}
- {{CAN_RESIDUAL_FACTOR_3}}

---

## Domain: Infotainment / Head Unit (IVI)

### Domain Summary

**Domain Risk Level**: {{IVI_DOMAIN_RISK_LEVEL}}
**Total Threat Scenarios**: {{IVI_THREAT_COUNT}}
**Total Damage Scenarios**: {{IVI_DAMAGE_COUNT}}
**Total Risk Treatments**: {{IVI_TREATMENT_COUNT}}
**Total Cybersecurity Goals**: {{IVI_CSG_COUNT}}
**Domain Assets**: {{IVI_ASSET_COUNT}}

**Top Domain Threat**: {{IVI_TOP_THREAT_ID}} (RV {{IVI_TOP_THREAT_RV}})

### Domain Description

The IVI domain encompasses the infotainment system head unit, including the Qualcomm QAM8295 SoC, QNX + Android hypervisor architecture, displays (HUD, central console, instrument cluster), sensors (GNSS, cameras, microphones), and wireless connectivity (Bluetooth, WiFi, cellular). This domain handles user interaction, navigation, media, and external connectivity, making it the primary external attack surface.

### Domain Risk Distribution

| Risk Value | Count | Percentage |
|------------|-------|------------|
| RV 5 (Critical) | {{IVI_RV5_COUNT}} | {{IVI_RV5_PCT}}% |
| RV 4 (High) | {{IVI_RV4_COUNT}} | {{IVI_RV4_PCT}}% |
| RV 3 (Medium) | {{IVI_RV3_COUNT}} | {{IVI_RV3_PCT}}% |
| RV 2 (Low) | {{IVI_RV2_COUNT}} | {{IVI_RV2_PCT}}% |
| RV 1 (Negligible) | {{IVI_RV1_COUNT}} | {{IVI_RV1_PCT}}% |

**SFOP Impact Analysis (Domain)**:
- Safety-Critical Threats: {{IVI_SAFETY_COUNT}} (Impact ≥ 3)
- Financial Impact Threats: {{IVI_FINANCIAL_COUNT}} (Impact ≥ 3)
- Operational Impact Threats: {{IVI_OPERATIONAL_COUNT}} (Impact ≥ 3)
- Privacy Impact Threats: {{IVI_PRIVACY_COUNT}} (Impact ≥ 3)
- **Most Critical Impact Type**: {{IVI_CRITICAL_IMPACT_TYPE}}

### Domain Assets and Attack Surface

**Assets in Domain**:
{{IVI_ASSET_LIST}}

**Attack Surface / Entry Points**:
- Bluetooth stack (L2CAP protocol, remote exploitable)
- WiFi (WPA3, rogue AP MITM attacks)
- USB ports (physical access, malware delivery)
- NFC reader (malicious tag injection)
- Android app framework (third-party apps)
- Media codecs (malicious audio/video file parsing)
- GNSS receiver (spoofing, jamming attacks)

**External Interfaces**: {{IVI_EXTERNAL_INTERFACE_COUNT}}
**Internal Dependencies**: {{IVI_INTERNAL_DEPENDENCY_COUNT}} (to CAN, OTA domains)
**Physical Access Required**: {{IVI_PHYSICAL_THREAT_COUNT}} threats
**Remote Attack Feasible**: {{IVI_REMOTE_THREAT_COUNT}} threats

### Domain Threat Scenarios

| TS-ID | Title | RV | AFR | Impact (S/F/O/P) | Related DS-ID | Related RT-ID | Status |
|-------|-------|-----|-----|------------------|---------------|---------------|--------|
{{IVI_THREAT_TABLE}}

### Domain Controls and Treatments

**Treatment Decision Breakdown**:
- **Reduce**: {{IVI_REDUCE_COUNT}} treatments
- **Avoid**: {{IVI_AVOID_COUNT}} treatments
- **Transfer**: {{IVI_TRANSFER_COUNT}} treatments
- **Accept**: {{IVI_ACCEPT_COUNT}} treatments

**Treatment Effectiveness**: {{IVI_TREATMENT_EFFECTIVENESS}}% (active mitigation rate)

**Primary Control Categories** (IVI domain):
1. **Code Signing**: PKI-based app signing, firmware signature verification (RSA-2048, ECDSA P-256)
2. **Access Control**: App store restrictions, hypervisor isolation (QNX ↔ Android), sandboxing (SELinux)
3. **Secure Boot**: ASLR, DEP, stack canaries for exploit mitigation, runtime integrity monitoring
4. **Cryptographic Protocols**: TLS 1.3 with certificate pinning, WPA3 WiFi encryption
5. **Input Validation**: Boundary checks on Bluetooth packets, NFC NDEF messages, media codec parsing

### Domain Defense Layers

**Layer 1 - Perimeter Defense**: Bluetooth, WiFi, USB inputs validated before processing; NFC disabled when parked.

**Layer 2 - Application Isolation**: Android apps sandboxed with SELinux; media codecs run with least privilege (no CAN access).

**Layer 3 - Hypervisor Isolation**: Android (external connectivity) isolated from QNX (CAN access) by Type-1 hypervisor; memory partitioning enforced.

**Layer 4 - Cryptographic Protection**: TLS 1.3 + cert pinning prevents MITM; OEM code signing prevents malicious apps.

**Layer 5 - Runtime Integrity**: ASLR/DEP/canaries raise exploit complexity; regular OTA security patches close vulnerabilities.

### Residual Risk (Domain)

**Residual Risk Level**: {{IVI_RESIDUAL_RISK_LEVEL}}
**Residual Threats (RV ≥ 4)**: {{IVI_RESIDUAL_THREAT_COUNT}}

**Remaining Risk Factors**:
- {{IVI_RESIDUAL_FACTOR_1}}
- {{IVI_RESIDUAL_FACTOR_2}}
- {{IVI_RESIDUAL_FACTOR_3}}

---

## Domain: Over-the-Air Updates (OTA)

### Domain Summary

**Domain Risk Level**: {{OTA_DOMAIN_RISK_LEVEL}}
**Total Threat Scenarios**: {{OTA_THREAT_COUNT}}
**Total Damage Scenarios**: {{OTA_DAMAGE_COUNT}}
**Total Risk Treatments**: {{OTA_TREATMENT_COUNT}}
**Total Cybersecurity Goals**: {{OTA_CSG_COUNT}}
**Domain Assets**: {{OTA_ASSET_COUNT}}

**Top Domain Threat**: {{OTA_TOP_THREAT_ID}} (RV {{OTA_TOP_THREAT_RV}})

### Domain Description

The OTA domain handles over-the-air firmware updates for the Head Unit SoC, hypervisor, QNX, and Android guest operating systems. OTA updates are delivered via cellular/Ethernet from the backend telematics server, verified using PKI signatures, and installed using Secure Boot mechanisms. Compromise of OTA enables persistent, fleet-wide attacks.

### Domain Risk Distribution

| Risk Value | Count | Percentage |
|------------|-------|------------|
| RV 5 (Critical) | {{OTA_RV5_COUNT}} | {{OTA_RV5_PCT}}% |
| RV 4 (High) | {{OTA_RV4_COUNT}} | {{OTA_RV4_PCT}}% |
| RV 3 (Medium) | {{OTA_RV3_COUNT}} | {{OTA_RV3_PCT}}% |
| RV 2 (Low) | {{OTA_RV2_COUNT}} | {{OTA_RV2_PCT}}% |
| RV 1 (Negligible) | {{OTA_RV1_COUNT}} | {{OTA_RV1_PCT}}% |

**SFOP Impact Analysis (Domain)**:
- Safety-Critical Threats: {{OTA_SAFETY_COUNT}} (Impact ≥ 3)
- Financial Impact Threats: {{OTA_FINANCIAL_COUNT}} (Impact ≥ 3)
- Operational Impact Threats: {{OTA_OPERATIONAL_COUNT}} (Impact ≥ 3)
- Privacy Impact Threats: {{OTA_PRIVACY_COUNT}} (Impact ≥ 3)
- **Most Critical Impact Type**: {{OTA_CRITICAL_IMPACT_TYPE}}

### Domain Assets and Attack Surface

**Assets in Domain**:
{{OTA_ASSET_LIST}}

**Attack Surface / Entry Points**:
- Cellular/Ethernet OTA update channel (TLS-encrypted)
- OTA backend API (authentication required)
- Firmware signature verification (HSM public keys)
- eFuse anti-rollback counter (SoC hardware)

**External Interfaces**: {{OTA_EXTERNAL_INTERFACE_COUNT}}
**Internal Dependencies**: {{OTA_INTERNAL_DEPENDENCY_COUNT}} (to BCK, IVI domains)
**Physical Access Required**: {{OTA_PHYSICAL_THREAT_COUNT}} threats
**Remote Attack Feasible**: {{OTA_REMOTE_THREAT_COUNT}} threats

### Domain Threat Scenarios

| TS-ID | Title | RV | AFR | Impact (S/F/O/P) | Related DS-ID | Related RT-ID | Status |
|-------|-------|-----|-----|------------------|---------------|---------------|--------|
{{OTA_THREAT_TABLE}}

### Domain Controls and Treatments

**Treatment Decision Breakdown**:
- **Reduce**: {{OTA_REDUCE_COUNT}} treatments
- **Avoid**: {{OTA_AVOID_COUNT}} treatments
- **Transfer**: {{OTA_TRANSFER_COUNT}} treatments
- **Accept**: {{OTA_ACCEPT_COUNT}} treatments

**Treatment Effectiveness**: {{OTA_TREATMENT_EFFECTIVENESS}}% (active mitigation rate)

**Primary Control Categories** (OTA domain):
1. **Code Signing**: Multi-signature firmware signing (M-of-N threshold, e.g., 3-of-5 OEM signers)
2. **Update Security**: eFuse anti-rollback counter, canary deployments (phased 1% → 10% → 50% → 100% rollout)
3. **Secure Storage**: Offline HSM for firmware signing keys, physical access control, audit logging
4. **Cryptographic Protocols**: TLS 1.3 with certificate pinning for OTA transport channel
5. **Intrusion Detection**: OTA update log audit for anomalous patterns (rollback attempts, signature failures)

### Domain Defense Layers

**Layer 1 - Transport Security**: TLS 1.3 with certificate pinning prevents MITM on cellular/Ethernet OTA channel.

**Layer 2 - Multi-Signature Verification**: M-of-N firmware signing requires compromising multiple independent OEM signing authorities (prevents single-point compromise).

**Layer 3 - Anti-Rollback Protection**: eFuse-backed counter monotonically increments with each firmware version, rejecting downgrades to vulnerable versions.

**Layer 4 - Canary Deployment**: Phased rollout detects malicious firmware before fleet-wide distribution (1% → 10% → halt if anomalies detected).

**Layer 5 - Offline Key Storage**: Firmware signing keys stored in offline HSMs with physical access control, preventing remote key theft.

### Residual Risk (Domain)

**Residual Risk Level**: {{OTA_RESIDUAL_RISK_LEVEL}}
**Residual Threats (RV ≥ 4)**: {{OTA_RESIDUAL_THREAT_COUNT}}

**Remaining Risk Factors**:
- {{OTA_RESIDUAL_FACTOR_1}}
- {{OTA_RESIDUAL_FACTOR_2}}
- {{OTA_RESIDUAL_FACTOR_3}}

---

## Domain: External Interfaces (EXT)

### Domain Summary

**Domain Risk Level**: {{EXT_DOMAIN_RISK_LEVEL}}
**Total Threat Scenarios**: {{EXT_THREAT_COUNT}}
**Total Damage Scenarios**: {{EXT_DAMAGE_COUNT}}
**Total Risk Treatments**: {{EXT_TREATMENT_COUNT}}
**Total Cybersecurity Goals**: {{EXT_CSG_COUNT}}
**Domain Assets**: {{EXT_ASSET_COUNT}}

**Top Domain Threat**: {{EXT_TOP_THREAT_ID}} (RV {{EXT_TOP_THREAT_RV}})

### Domain Description

The EXT domain encompasses external physical and wireless interfaces exposed to users and attackers, including USB ports, Bluetooth, WiFi, NFC, and cellular connectivity. These interfaces provide legitimate user functionality but also represent the primary attack surface for initial system compromise.

### Domain Risk Distribution

| Risk Value | Count | Percentage |
|------------|-------|------------|
| RV 5 (Critical) | {{EXT_RV5_COUNT}} | {{EXT_RV5_PCT}}% |
| RV 4 (High) | {{EXT_RV4_COUNT}} | {{EXT_RV4_PCT}}% |
| RV 3 (Medium) | {{EXT_RV3_COUNT}} | {{EXT_RV3_PCT}}% |
| RV 2 (Low) | {{EXT_RV2_COUNT}} | {{EXT_RV2_PCT}}% |
| RV 1 (Negligible) | {{EXT_RV1_COUNT}} | {{EXT_RV1_PCT}}% |

**SFOP Impact Analysis (Domain)**:
- Safety-Critical Threats: {{EXT_SAFETY_COUNT}} (Impact ≥ 3)
- Financial Impact Threats: {{EXT_FINANCIAL_COUNT}} (Impact ≥ 3)
- Operational Impact Threats: {{EXT_OPERATIONAL_COUNT}} (Impact ≥ 3)
- Privacy Impact Threats: {{EXT_PRIVACY_COUNT}} (Impact ≥ 3)
- **Most Critical Impact Type**: {{EXT_CRITICAL_IMPACT_TYPE}}

### Domain Assets and Attack Surface

**Assets in Domain**:
{{EXT_ASSET_LIST}}

**Attack Surface / Entry Points**:
- USB ports (physical access, malware injection, firmware updates)
- Bluetooth stack (remote RCE via L2CAP buffer overflow)
- WiFi (MITM via rogue access points)
- NFC reader (malicious tag injection)
- Physical tampering (case opening, JTAG/SWD debug interfaces)

**External Interfaces**: {{EXT_EXTERNAL_INTERFACE_COUNT}}
**Internal Dependencies**: {{EXT_INTERNAL_DEPENDENCY_COUNT}} (to IVI, BCK domains)
**Physical Access Required**: {{EXT_PHYSICAL_THREAT_COUNT}} threats
**Remote Attack Feasible**: {{EXT_REMOTE_THREAT_COUNT}} threats

### Domain Threat Scenarios

| TS-ID | Title | RV | AFR | Impact (S/F/O/P) | Related DS-ID | Related RT-ID | Status |
|-------|-------|-----|-----|------------------|---------------|---------------|--------|
{{EXT_THREAT_TABLE}}

### Domain Controls and Treatments

**Treatment Decision Breakdown**:
- **Reduce**: {{EXT_REDUCE_COUNT}} treatments
- **Avoid**: {{EXT_AVOID_COUNT}} treatments
- **Transfer**: {{EXT_TRANSFER_COUNT}} treatments
- **Accept**: {{EXT_ACCEPT_COUNT}} treatments

**Treatment Effectiveness**: {{EXT_TREATMENT_EFFECTIVENESS}}% (active mitigation rate)

**Primary Control Categories** (EXT domain):
1. **Input Validation**: Strict parsing of USB firmware files, NFC NDEF messages, Bluetooth packets
2. **Code Signing**: PKI signature verification for USB-delivered firmware (RSA-2048, ECDSA P-256)
3. **Physical Security**: USB auto-mount disabled (PIN required), Bluetooth/NFC disabled when parked
4. **Cryptographic Protocols**: TLS 1.3 for WiFi, WPA3 encryption, BT 5.2 LE Secure pairing
5. **Secure Boot**: ASLR, DEP, stack canaries for Bluetooth/WiFi stack exploit mitigation

### Domain Defense Layers

**Layer 1 - Physical Access Control**: USB/NFC require user confirmation or PIN; disable-when-parked reduces attack window.

**Layer 2 - Input Validation**: Boundary checks on all external inputs (USB files, NFC tags, Bluetooth packets) reject malformed data.

**Layer 3 - Sandboxing**: NFC/Bluetooth handlers run with least privilege (SELinux); cannot access CAN or cryptographic keys.

**Layer 4 - Cryptographic Authentication**: USB firmware signature verification, WiFi TLS cert pinning prevent malicious payloads.

**Layer 5 - Exploit Mitigation**: ASLR/DEP/canaries in Bluetooth/WiFi/NFC stacks raise RCE exploit complexity.

### Residual Risk (Domain)

**Residual Risk Level**: {{EXT_RESIDUAL_RISK_LEVEL}}
**Residual Threats (RV ≥ 4)**: {{EXT_RESIDUAL_THREAT_COUNT}}

**Remaining Risk Factors**:
- {{EXT_RESIDUAL_FACTOR_1}}
- {{EXT_RESIDUAL_FACTOR_2}}
- {{EXT_RESIDUAL_FACTOR_3}}

---

## Domain: Backend / Cloud Infrastructure (BCK)

### Domain Summary

**Domain Risk Level**: {{BCK_DOMAIN_RISK_LEVEL}}
**Total Threat Scenarios**: {{BCK_THREAT_COUNT}}
**Total Damage Scenarios**: {{BCK_DAMAGE_COUNT}}
**Total Risk Treatments**: {{BCK_TREATMENT_COUNT}}
**Total Cybersecurity Goals**: {{BCK_CSG_COUNT}}
**Domain Assets**: {{BCK_ASSET_COUNT}}

**Top Domain Threat**: {{BCK_TOP_THREAT_ID}} (RV {{BCK_TOP_THREAT_RV}})

### Domain Description

The BCK domain encompasses backend cloud infrastructure supporting telematics, OTA updates, user account management, and fleet data analytics. Backend compromise enables fleet-wide attacks by distributing malicious OTA updates or exfiltrating large-scale user data.

### Domain Risk Distribution

| Risk Value | Count | Percentage |
|------------|-------|------------|
| RV 5 (Critical) | {{BCK_RV5_COUNT}} | {{BCK_RV5_PCT}}% |
| RV 4 (High) | {{BCK_RV4_COUNT}} | {{BCK_RV4_PCT}}% |
| RV 3 (Medium) | {{BCK_RV3_COUNT}} | {{BCK_RV3_PCT}}% |
| RV 2 (Low) | {{BCK_RV2_COUNT}} | {{BCK_RV2_PCT}}% |
| RV 1 (Negligible) | {{BCK_RV1_COUNT}} | {{BCK_RV1_PCT}}% |

**SFOP Impact Analysis (Domain)**:
- Safety-Critical Threats: {{BCK_SAFETY_COUNT}} (Impact ≥ 3)
- Financial Impact Threats: {{BCK_FINANCIAL_COUNT}} (Impact ≥ 3)
- Operational Impact Threats: {{BCK_OPERATIONAL_COUNT}} (Impact ≥ 3)
- Privacy Impact Threats: {{BCK_PRIVACY_COUNT}} (Impact ≥ 3)
- **Most Critical Impact Type**: {{BCK_CRITICAL_IMPACT_TYPE}}

### Domain Assets and Attack Surface

**Assets in Domain**:
{{BCK_ASSET_LIST}}

**Attack Surface / Entry Points**:
- Backend REST APIs (OAuth 2.0 + MFA authentication)
- OTA distribution server (TLS-protected)
- Telematics database (SQL, NoSQL)
- Administrative web portals (fleet management)

**External Interfaces**: {{BCK_EXTERNAL_INTERFACE_COUNT}}
**Internal Dependencies**: {{BCK_INTERNAL_DEPENDENCY_COUNT}} (to OTA domain)
**Physical Access Required**: {{BCK_PHYSICAL_THREAT_COUNT}} threats
**Remote Attack Feasible**: {{BCK_REMOTE_THREAT_COUNT}} threats

### Domain Threat Scenarios

| TS-ID | Title | RV | AFR | Impact (S/F/O/P) | Related DS-ID | Related RT-ID | Status |
|-------|-------|-----|-----|------------------|---------------|---------------|--------|
{{BCK_THREAT_TABLE}}

### Domain Controls and Treatments

**Treatment Decision Breakdown**:
- **Reduce**: {{BCK_REDUCE_COUNT}} treatments
- **Avoid**: {{BCK_AVOID_COUNT}} treatments
- **Transfer**: {{BCK_TRANSFER_COUNT}} treatments
- **Accept**: {{BCK_ACCEPT_COUNT}} treatments

**Treatment Effectiveness**: {{BCK_TREATMENT_EFFECTIVENESS}}% (active mitigation rate)

**Primary Control Categories** (BCK domain):
1. **Authentication**: OAuth 2.0 with MFA (TOTP, hardware tokens), mTLS for vehicle-to-backend communication
2. **Access Control**: Rate limiting, account lockout, IP whitelisting for admin endpoints, RBAC
3. **Input Validation**: Parameterized SQL queries, input sanitization for API parameters
4. **Intrusion Detection**: SIEM monitoring, anomaly detection for unusual API access patterns
5. **Cryptographic Protocols**: mTLS with HSM-protected client certificates, TLS 1.3 for all connections

### Domain Defense Layers

**Layer 1 - Authentication Barrier**: OAuth 2.0 + MFA prevents credential stuffing; mTLS ensures vehicle authenticity.

**Layer 2 - Rate Limiting**: API rate limits (10 req/min per IP) and account lockout prevent brute-force attacks.

**Layer 3 - Input Validation**: Parameterized queries prevent SQL injection; input sanitization blocks XSS/SSRF.

**Layer 4 - Network Segmentation**: OTA distribution server isolated from telematics DB; admin endpoints IP-whitelisted.

**Layer 5 - Intrusion Detection**: SIEM monitoring alerts on anomalous API patterns (unusual IP, excessive requests, privilege escalation attempts).

### Residual Risk (Domain)

**Residual Risk Level**: {{BCK_RESIDUAL_RISK_LEVEL}}
**Residual Threats (RV ≥ 4)**: {{BCK_RESIDUAL_THREAT_COUNT}}

**Remaining Risk Factors**:
- {{BCK_RESIDUAL_FACTOR_1}}
- {{BCK_RESIDUAL_FACTOR_2}}
- {{BCK_RESIDUAL_FACTOR_3}}

---

## Domain: Immobilizer (IMM)

### Domain Summary

**Domain Risk Level**: {{IMM_DOMAIN_RISK_LEVEL}}
**Total Threat Scenarios**: {{IMM_THREAT_COUNT}}
**Total Damage Scenarios**: {{IMM_DAMAGE_COUNT}}
**Total Risk Treatments**: {{IMM_TREATMENT_COUNT}}
**Total Cybersecurity Goals**: {{IMM_CSG_COUNT}}
**Domain Assets**: {{IMM_ASSET_COUNT}}

**Top Domain Threat**: {{IMM_TOP_THREAT_ID}} (RV {{IMM_TOP_THREAT_RV}})

### Domain Description

The IMM domain encompasses the vehicle immobilizer system, including key fob authentication, cryptographic challenge-response protocols, and engine start authorization. Immobilizer compromise enables vehicle theft and unauthorized operation.

### Domain Risk Distribution

| Risk Value | Count | Percentage |
|------------|-------|------------|
| RV 5 (Critical) | {{IMM_RV5_COUNT}} | {{IMM_RV5_PCT}}% |
| RV 4 (High) | {{IMM_RV4_COUNT}} | {{IMM_RV4_PCT}}% |
| RV 3 (Medium) | {{IMM_RV3_COUNT}} | {{IMM_RV3_PCT}}% |
| RV 2 (Low) | {{IMM_RV2_COUNT}} | {{IMM_RV2_PCT}}% |
| RV 1 (Negligible) | {{IMM_RV1_COUNT}} | {{IMM_RV1_PCT}}% |

**SFOP Impact Analysis (Domain)**:
- Safety-Critical Threats: {{IMM_SAFETY_COUNT}} (Impact ≥ 3)
- Financial Impact Threats: {{IMM_FINANCIAL_COUNT}} (Impact ≥ 3)
- Operational Impact Threats: {{IMM_OPERATIONAL_COUNT}} (Impact ≥ 3)
- Privacy Impact Threats: {{IMM_PRIVACY_COUNT}} (Impact ≥ 3)
- **Most Critical Impact Type**: {{IMM_CRITICAL_IMPACT_TYPE}}

### Domain Assets and Attack Surface

**Assets in Domain**:
{{IMM_ASSET_LIST}}

**Attack Surface / Entry Points**:
- Key fob RF communication (relay attacks, signal replay)
- Challenge-response protocol (cryptanalysis)
- Engine start authorization logic (bypass attempts)

**External Interfaces**: {{IMM_EXTERNAL_INTERFACE_COUNT}}
**Internal Dependencies**: {{IMM_INTERNAL_DEPENDENCY_COUNT}}
**Physical Access Required**: {{IMM_PHYSICAL_THREAT_COUNT}} threats
**Remote Attack Feasible**: {{IMM_REMOTE_THREAT_COUNT}} threats

### Domain Threat Scenarios

| TS-ID | Title | RV | AFR | Impact (S/F/O/P) | Related DS-ID | Related RT-ID | Status |
|-------|-------|-----|-----|------------------|---------------|---------------|--------|
{{IMM_THREAT_TABLE}}

### Domain Controls and Treatments

**Treatment Decision Breakdown**:
- **Reduce**: {{IMM_REDUCE_COUNT}} treatments
- **Avoid**: {{IMM_AVOID_COUNT}} treatments
- **Transfer**: {{IMM_TRANSFER_COUNT}} treatments
- **Accept**: {{IMM_ACCEPT_COUNT}} treatments

**Treatment Effectiveness**: {{IMM_TREATMENT_EFFECTIVENESS}}% (active mitigation rate)

**Primary Control Categories** (IMM domain):
1. **Cryptographic Protocols**: Strong challenge-response with rolling codes
2. **Physical Security**: Key fob signal shielding, relay attack detection
3. **Access Control**: Multi-factor authentication (key fob + biometric)

---

## Domain: Advanced Driver Assistance Systems (ADAS)

### Domain Summary

**Domain Risk Level**: {{ADAS_DOMAIN_RISK_LEVEL}}
**Total Threat Scenarios**: {{ADAS_THREAT_COUNT}}
**Total Damage Scenarios**: {{ADAS_DAMAGE_COUNT}}
**Total Risk Treatments**: {{ADAS_TREATMENT_COUNT}}
**Total Cybersecurity Goals**: {{ADAS_CSG_COUNT}}
**Domain Assets**: {{ADAS_ASSET_COUNT}}

**Top Domain Threat**: {{ADAS_TOP_THREAT_ID}} (RV {{ADAS_TOP_THREAT_RV}})

### Domain Description

The ADAS domain encompasses advanced driver assistance systems including adaptive cruise control, automatic emergency braking, lane keeping assist, and sensor fusion algorithms. ADAS compromise creates direct safety risk by manipulating autonomous driving functions.

### Domain Risk Distribution

| Risk Value | Count | Percentage |
|------------|-------|------------|
| RV 5 (Critical) | {{ADAS_RV5_COUNT}} | {{ADAS_RV5_PCT}}% |
| RV 4 (High) | {{ADAS_RV4_COUNT}} | {{ADAS_RV4_PCT}}% |
| RV 3 (Medium) | {{ADAS_RV3_COUNT}} | {{ADAS_RV3_PCT}}% |
| RV 2 (Low) | {{ADAS_RV2_COUNT}} | {{ADAS_RV2_PCT}}% |
| RV 1 (Negligible) | {{ADAS_RV1_COUNT}} | {{ADAS_RV1_PCT}}% |

**SFOP Impact Analysis (Domain)**:
- Safety-Critical Threats: {{ADAS_SAFETY_COUNT}} (Impact ≥ 3)
- Financial Impact Threats: {{ADAS_FINANCIAL_COUNT}} (Impact ≥ 3)
- Operational Impact Threats: {{ADAS_OPERATIONAL_COUNT}} (Impact ≥ 3)
- Privacy Impact Threats: {{ADAS_PRIVACY_COUNT}} (Impact ≥ 3)
- **Most Critical Impact Type**: {{ADAS_CRITICAL_IMPACT_TYPE}}

### Domain Assets and Attack Surface

**Assets in Domain**:
{{ADAS_ASSET_LIST}}

**Attack Surface / Entry Points**:
- ADAS ECU (firmware updates, diagnostic access)
- Camera/radar/lidar sensors (spoofing attacks)
- FlexRay network (ADAS-specific communication bus)

**External Interfaces**: {{ADAS_EXTERNAL_INTERFACE_COUNT}}
**Internal Dependencies**: {{ADAS_INTERNAL_DEPENDENCY_COUNT}} (to CAN domain)
**Physical Access Required**: {{ADAS_PHYSICAL_THREAT_COUNT}} threats
**Remote Attack Feasible**: {{ADAS_REMOTE_THREAT_COUNT}} threats

### Domain Threat Scenarios

| TS-ID | Title | RV | AFR | Impact (S/F/O/P) | Related DS-ID | Related RT-ID | Status |
|-------|-------|-----|-----|------------------|---------------|---------------|--------|
{{ADAS_THREAT_TABLE}}

### Domain Controls and Treatments

**Treatment Decision Breakdown**:
- **Reduce**: {{ADAS_REDUCE_COUNT}} treatments
- **Avoid**: {{ADAS_AVOID_COUNT}} treatments
- **Transfer**: {{ADAS_TRANSFER_COUNT}} treatments
- **Accept**: {{ADAS_ACCEPT_COUNT}} treatments

**Treatment Effectiveness**: {{ADAS_TREATMENT_EFFECTIVENESS}}% (active mitigation rate)

**Primary Control Categories** (ADAS domain):
1. **Secure Boot**: Firmware integrity verification, Secure Boot for ADAS ECU
2. **Network Segmentation**: ADAS isolated on FlexRay network, Gateway filtering
3. **Input Validation**: Sensor data plausibility checks, redundant sensor fusion

---

## Cross-Domain Analysis

### Cross-Domain Attack Chains

This section identifies attack scenarios that span multiple domains, demonstrating where layered defenses successfully contain threats versus where additional controls are needed.

#### Attack Chain 1: EXT (USB) → IVI (Android) → IVI (Hypervisor) → CAN

**Attack Path**:
1. **EXT**: Attacker delivers USB malware via physical access (TS-IVI-003)
2. **IVI**: Malware installs on Android Guest OS (TS-IVI-001), escalates privileges
3. **IVI**: Hypervisor escape exploit breaks QNX isolation (TS-IVI-007)
4. **CAN**: Attacker gains CAN-FD access via QNX, injects malicious messages (TS-CAN-001)

**Defense-in-Depth Analysis**:
- **Layer 1 (EXT)**: USB firmware signature verification (RT-IVI-003) blocks unsigned malware → **EFFECTIVE**
- **Layer 2 (IVI)**: Android app store restrictions (RT-IVI-001) prevent malicious app installation → **EFFECTIVE**
- **Layer 3 (IVI)**: Hypervisor isolation (RT-IVI-007) prevents Android → QNX escape → **PARTIALLY EFFECTIVE** (requires zero-day exploit)
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
- **Layer 4 (BCK)**: Network anomaly detection (RT-EXT-001) alerts on unusual data volume → **PARTIALLY EFFECTIVE** (detection lag allows some exfiltration)

**Conclusion**: Defense-in-depth partially contains this attack chain. Bluetooth RCE (Layer 1) remains a risk despite hardening. However, hypervisor isolation (Layer 2) prevents escalation to CAN domain, limiting damage to user data exposure rather than vehicle control. Additional controls needed: Bluetooth disable-when-parked (RT-IVI-002), data loss prevention (DLP) for cellular exfiltration.

### Cross-Domain Dependencies

| Dependency | Description | Risk Amplification | Mitigation |
|------------|-------------|-------------------|------------|
| **IVI → CAN** | QNX Guest OS has CAN-FD access; Android compromise + hypervisor escape enables CAN manipulation | **HIGH** - Hypervisor escape converts IVI threat to CAN threat | Hypervisor isolation hardening (RT-IVI-007), CAN SecOC authentication (RT-CAN-001) |
| **BCK → OTA** | Backend API compromise enables malicious OTA distribution to entire fleet | **CRITICAL** - Single backend breach affects millions of vehicles | OAuth 2.0 + MFA (RT-EXT-001), multi-sig firmware signing (RT-OTA-001), canary deployment (RT-OTA-001) |
| **EXT → IVI** | External interfaces (USB, Bluetooth, WiFi) are primary IVI compromise vectors | **MODERATE** - External compromise limited to IVI unless hypervisor breached | Input validation (RT-IVI-003, RT-IVI-002), code signing (RT-IVI-001), sandboxing (RT-IVI-005) |
| **OTA → IVI** | OTA firmware updates modify IVI firmware; malicious OTA enables persistent compromise | **HIGH** - Persistent compromise survives reboots | Multi-sig firmware signing (RT-OTA-001), eFuse anti-rollback (RT-OTA-002), Secure Boot (RT-IVI-001) |
| **IVI → BCK** | Cellular connectivity enables IVI-to-backend communication; compromised IVI could attack backend | **LOW** - Backend authentication (OAuth 2.0 + MFA) prevents IVI compromise from backend breach | mTLS with HSM client certs (RT-EXT-001), API rate limiting, SIEM monitoring |

### Interdomain Risk Amplification

**Risk Amplification Factor**: {{CROSS_DOMAIN_RISK_AMPLIFICATION}}%

The presence of cross-domain dependencies increases aggregate system risk by {{CROSS_DOMAIN_RISK_AMPLIFICATION}}% compared to isolated domain analysis. This amplification occurs because:
1. Attacker who compromises one domain gains pivot opportunities to adjacent domains
2. Failures cascade across domain boundaries (e.g., Gateway ECU DoS disrupts both CAN and IVI)
3. Shared assets (SoC, HSM) create single points of failure affecting multiple domains

### Domain Isolation Score

**Overall Domain Isolation Score**: {{DOMAIN_ISOLATION_SCORE}} (0 = no isolation, 1 = perfect isolation)

Domain isolation effectiveness by boundary:
- **IVI ↔ CAN**: {{IVI_CAN_ISOLATION}} (Hypervisor isolation, Gateway firewall)
- **EXT ↔ IVI**: {{EXT_IVI_ISOLATION}} (Input validation, sandboxing)
- **BCK ↔ OTA**: {{BCK_OTA_ISOLATION}} (Multi-sig signing, canary deployment)
- **OTA ↔ IVI**: {{OTA_IVI_ISOLATION}} (Secure Boot, eFuse anti-rollback)

### Gateway and Controller Dependencies

The Gateway ECU (AST-ECU-006) is a critical central point affecting multiple domains:

**Gateway ECU Dependencies**:
- **Domains Affected**: CAN, IVI, ADAS (all vehicle network communication routes through Gateway)
- **Single Point of Failure Impact**: Gateway DoS disrupts inter-domain communication, disables ADAS coordination, prevents IVI from retrieving vehicle status
- **Security Boundary Function**: Gateway firewall enforces critical security boundary between infotainment (IVI, EXT) and safety-critical systems (CAN, ADAS)
- **Mitigation**: Gateway hardening (RT-CAN-004), CAN SecOC authentication (RT-CAN-001), measured boot attestation

**Other Critical Central Points**:
- **HSM/TEE (AST-ECU-005)**: Stores cryptographic keys for all domains; compromise affects OTA, IVI, CAN authentication
- **Head Unit SoC (AST-ECU-001)**: Hosts hypervisor isolating IVI guests; SoC compromise enables cross-domain attacks
- **OTA Backend**: Distributes firmware to entire fleet; backend compromise enables fleet-wide attacks

---

## Security Architecture Summary

### Overall Defense Posture

**Aggregate Defense-in-Depth Effectiveness**: {{DEFENSE_IN_DEPTH_EFFECTIVENESS}}%

The multi-layer defense architecture demonstrates:
- **Layered Controls**: Average {{AVG_LAYERS_PER_THREAT}} security controls per threat scenario
- **Domain Isolation**: {{DOMAIN_ISOLATION_SCORE}} overall isolation score (1 = perfect, 0 = no isolation)
- **Treatment Coverage**: {{OVERALL_TREATMENT_EFFECTIVENESS}}% of threats actively mitigated
- **Residual Risk**: {{OVERALL_RESIDUAL_THREAT_COUNT}} threats remain at RV ≥ 4 after treatment

### Strongest Security Layers

1. **Cryptographic Authentication** (CAN SecOC, multi-sig firmware signing, TLS 1.3 with cert pinning)
   - Applies to: CAN, OTA, BCK, EXT domains
   - Effectiveness: Prevents spoofing, injection, MITM attacks
   
2. **Hypervisor Isolation** (QNX ↔ Android separation)
   - Applies to: IVI domain
   - Effectiveness: Prevents Android compromise from escalating to CAN access
   
3. **Gateway Firewall** (CAN ID filtering, domain segmentation)
   - Applies to: CAN, IVI, ADAS domains
   - Effectiveness: Prevents infotainment from commanding safety-critical ECUs

### Weakest Security Layers / Areas for Improvement

1. **External Interface Input Validation** (Bluetooth, WiFi, USB, NFC)
   - Issue: Multiple RCE vulnerabilities (TS-IVI-002, TS-IVI-003, TS-IVI-007)
   - Recommendation: Enhanced fuzzing, stricter input validation, disable-when-parked controls
   
2. **Runtime Integrity Monitoring**
   - Issue: No post-boot firmware integrity checking (user confirmed)
   - Recommendation: Implement continuous runtime verification (measured boot attestation, kernel integrity checking)
   
3. **Backend API Authentication**
   - Issue: OAuth 2.0 + MFA vulnerable to social engineering, token theft
   - Recommendation: Hardware token requirements for admin endpoints, geo-fencing for API access

### Compliance with UN R155 and ISO 21434

**UN R155 Annex 5 Coverage**:
- All 7 threat categories mapped: ✓ Backend servers, ✓ Update procedures, ✓ Communication channels, ✓ External connectivity, ✓ Data/code, ✓ Vehicle communication interfaces, ✓ OBD port

**ISO 21434 Clause 8.4 Work Products**:
- ✓ Asset identification ({{ASSET_COUNT}} assets catalogued)
- ✓ Damage scenario definition ({{DS_COUNT}} DS with SFOP impact scores)
- ✓ Threat scenario enumeration ({{TS_COUNT}} TS with STRIDE + R155 + MITRE ATT&CK mapping)
- ✓ Attack feasibility rating (AFR calculated for all TS)
- ✓ Risk value determination (RV 1-5 for all TS)
- ✓ Treatment decisions ({{RT_COUNT}} RT with Reduce/Avoid/Transfer/Accept)
- ✓ Cybersecurity goals (CSG defined per domain)
- ✓ Traceability (Asset → DS → TS → RT → CSG chains complete)

### Recommendations for Defense-in-Depth Enhancement

1. **Add runtime integrity monitoring** to detect post-boot firmware tampering (closes gap: no runtime verification)
2. **Implement network anomaly detection** on CAN-FD to identify malicious traffic patterns (enhances RT-CAN-001, RT-CAN-004)
3. **Deploy hardware token requirements** for backend API admin endpoints (strengthens RT-EXT-001)
4. **Enable disable-when-parked** for Bluetooth, WiFi, NFC to reduce external attack window (enhances RT-IVI-002, RT-IVI-004, RT-IVI-007)
5. **Add canary deployments** for all OTA updates (already in RT-OTA-001, expand to configuration updates)

---

## Appendix: Domain Acronyms and Definitions

| Acronym | Full Name | Description |
|---------|-----------|-------------|
| **CAN** | Controller Area Network | In-vehicle networking bus for ECU communication |
| **IVI** | Infotainment / In-Vehicle Infotainment | Head unit system including displays, media, navigation, connectivity |
| **OTA** | Over-the-Air | Wireless firmware update delivery mechanism |
| **EXT** | External Interfaces | Physical and wireless interfaces exposed to users (USB, Bluetooth, WiFi, NFC) |
| **BCK** | Backend / Cloud | Cloud infrastructure supporting telematics, OTA, user accounts |
| **IMM** | Immobilizer | Vehicle theft prevention system with key fob authentication |
| **ADAS** | Advanced Driver Assistance Systems | Autonomous driving functions (ACC, AEB, LKA) |

---

**Report Generation Date**: {{REPORT_DATE}}
**Report Version**: {{REPORT_VERSION}}
**Schema Version**: 1.0 (ISO 21434:2021 Clause 8.4 Work Products)
