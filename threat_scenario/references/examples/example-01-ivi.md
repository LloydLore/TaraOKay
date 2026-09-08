# IVI Domain - Example Threat Scenarios

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

This file demonstrates 3 complete threat scenario entries for the IVI (Infotainment) domain. Use these as reference when creating your own threat scenarios.

---

## TS-IVI-001: Malicious Android App Exfiltrating User Contacts and Location

**Threat Description**:
An attacker distributes a malicious Android application disguised as a legitimate navigation or entertainment app through a third-party app store with weak code signing verification. The user downloads and voluntarily installs the application on the vehicle's Head Unit Android partition (AST-ECU-004), granting excessive permissions including ACCESS_FINE_LOCATION, READ_CONTACTS, and INTERNET. Once installed, the malicious app silently exfiltrates user contacts, SMS history, call logs, and continuous GPS location data to an attacker-controlled server via the vehicle's cellular connection (AST-COM-005). The app operates in the background, collecting data every 30 seconds without user awareness, violating GDPR Article 6 (lawful basis for processing) and China GB 44495 personal information protection requirements.

**Target Asset**:
AST-ECU-004: Android Guest Operating System - Target due to user-facing app installation capability, access to Android APIs for location/contacts, and external network connectivity

**Attack Surface / Entry Point**:
Third-party Android app store accessible from Head Unit web browser or sideloaded via USB (AST-IFC-001). Attack requires user interaction (voluntary app installation) but no special privileges. The app store lacks Google Play Protect-equivalent malware scanning. No physical access to vehicle required - malicious APK can be distributed via phishing emails, compromised websites, or social engineering.

**STRIDE Category**:
Information Disclosure - Unauthorized exfiltration of personal data (contacts, location, communication records)

**UN R155 Annex 5 Reference**:
4.3.4 (Code execution - Unauthorized execution of code on vehicle systems)

**MITRE ATT&CK Reference**:
Collection: Data from Local System (T1005) - Malicious app reads contacts and location data from Android system APIs and local storage

**OWASP Reference**:
M2: Inadequate Supply Chain Security - Third-party app distribution without proper vetting or code signing verification

**Damage Scenario Categories**:
- DS-IVI-001: Unauthorized Driver Location Tracking - Continuous GPS exfiltration enables persistent surveillance
- DS-IVI-002: User Personal Data Exposure - Contact lists, call history, and SMS messages disclosed

**Attack Feasibility Rating (AFR)**:
AFR: 12 (Moderate)
- Elapsed Time: 3 (< 1 week) - Develop basic data-stealing app using public Android APIs
- Specialist Expertise: 2 (Proficient IT/cybersecurity professional) - Standard Android app development skills, no exploit development required
- Knowledge of Item: 3 (Publicly available / common knowledge) - Android permission model and location/contact APIs publicly documented in official Android developer docs
- Window of Opportunity: 3 (Unlimited / always accessible) - Attack works anytime after app installation; user unlikely to notice background data collection
- Equipment: 1 (Specialized but purchasable) - Requires developer account on third-party app store for distribution, ~$100 cost

**CIA Triad**:
C (Confidentiality) - Exfiltrates user contacts, location history, and communication records without authorization

**Real-world Examples / CVEs**:
- Similar to "Tesla app supply chain compromise" (2022 security bulletin) where third-party apps accessed vehicle data without proper authorization
- OWASP Mobile Top 10 M2 case study: Android automotive apps collecting excessive data (OWASP Mobile 2024 report)
- No specific CVE - attack exploits design weakness (permissive app installation policy) rather than code vulnerability

**Last Updated**:
2026-03-19

**Confidence Level**:
High - Multiple documented incidents of Android apps in automotive context collecting excessive user data; attack does not require exploits, only social engineering for app installation

**Affected Vehicle Systems**:
- Android Guest OS (AST-ECU-004) - Direct target, executes malicious code
- GNSS Receiver (AST-SNS-001) - Data source for location tracking
- Persistent Storage (AST-DAT-001) - Data source for stored contacts and call history
- Cellular/Telematics Link (AST-COM-005) - Exfiltration channel for data transmission to attacker server

**Attack Vector**: L (Local) - Requires malicious app installed on Android system, but no physical access to vehicle (installation via remote APK download)

---

## TS-IVI-002: Android Kernel Privilege Escalation via Use-After-Free Exploit

**Threat Description**:
An attacker first delivers a malicious Android application to the vehicle's Head Unit (AST-ECU-004) using the method from TS-IVI-001. This initial app appears benign and requests minimal permissions to avoid user suspicion. Once installed, the app exploits a known Android kernel use-after-free vulnerability (similar to CVE-2019-2215 affecting Pixel devices) to escalate privileges from the app sandbox to root access. With root privileges, the attacker gains unrestricted access to the Android partition including: (1) stored user data in UFS storage (AST-DAT-001), (2) cryptographic key material loaded in memory, (3) shared memory regions potentially accessible to the QNX partition (AST-ECU-003), and (4) ability to disable SELinux mandatory access controls. The attacker installs a persistent backdoor that survives reboot and enables remote command execution over the cellular connection.

**Target Asset**:
AST-ECU-004: Android Guest Operating System - Kernel vulnerability enables privilege escalation from unprivileged app to root access

**Attack Surface / Entry Point**:
Android kernel vulnerability exploited from within user-installed app. Initial entry via third-party app installation (see TS-IVI-001), then local exploit execution. Attack requires unprivileged app installation but no user interaction after initial install. Kernel exploit code can be delivered as encrypted payload to evade static analysis.

**STRIDE Category**:
Elevation of Privilege - Attacker escalates from app sandbox (unprivileged) to root access (kernel level)

**UN R155 Annex 5 Reference**:
4.3.4 (Code execution - Unauthorized execution of code on vehicle systems), combined with 4.3.7 (External connectivity - Threats via external interfaces)

**MITRE ATT&CK Reference**:
Privilege Escalation: Exploitation for Privilege Escalation (T1068) - Kernel vulnerability exploited to gain elevated privileges

**OWASP Reference**:
M7: Insufficient Binary Protections - Exploitation of Android OS kernel vulnerability (failure to apply security patches)

**Damage Scenario Categories**:
- DS-IVI-003: Malicious Code Execution on Head Unit SoC - Root access enables arbitrary code execution and system compromise
- DS-IVI-002: User Personal Data Exposure - Full access to Android partition data storage
- DS-IVI-005: Cryptographic Key Compromise from HSM/TEE - Keys loaded in memory may be accessible
- DS-CAN-001: Malicious CAN Message Injection (if attacker succeeds in hypervisor escape to QNX partition with CAN access)

**Attack Feasibility Rating (AFR)**:
AFR: 7 (Low)
- Elapsed Time: 1 (1-6 months) - Requires developing exploit for specific Android kernel version on QAM8295 platform, adapting public POC code
- Specialist Expertise: 0 (Multiple experts with rare skills) - Requires kernel exploit development skills including memory corruption techniques, ROP chain construction, and ARM64 assembly
- Knowledge of Item: 2 (Public with effort) - Android kernel source is public, but QAM8295-specific kernel customizations require firmware extraction and reverse engineering
- Window of Opportunity: 3 (Unlimited / always accessible) - Exploit can be delivered via app update after initial benign app installation; no time pressure
- Equipment: 1 (Specialized but purchasable) - Android debugging tools (ADB, Frida), kernel exploit development environment, test Head Unit hardware ~$5k

**CIA Triad**:
I+A (Integrity + Availability) - Kernel compromise enables tampering with system state (I) and potential denial of service via system crash (A)

**Real-world Examples / CVEs**:
- CVE-2019-2215: Android kernel use-after-free vulnerability in Binder driver enabling privilege escalation (Google Pixel devices)
- CVE-2020-0041: Android kernel use-after-free in Binder driver (similar attack pattern)
- Project Zero Issue 1942: Detailed write-up of Android kernel exploit techniques applicable to automotive platforms
- No automotive-specific CVE, but similar vulnerabilities demonstrated in Android Automotive OS research (Black Hat 2021)

**Last Updated**:
2026-03-19

**Confidence Level**:
High - Well-documented class of vulnerabilities (Android kernel use-after-free) with public exploits; automotive head units use standard Android kernel with minor customizations, making adaptation feasible

**Affected Vehicle Systems**:
- Android Guest OS Kernel (AST-ECU-004) - Direct exploit target
- Hypervisor (AST-ECU-002) - Potential secondary target if attacker attempts partition escape
- Persistent Storage (AST-DAT-001) - All stored data becomes accessible with root privileges
- HSM/TEE (AST-ECU-005) - Keys in memory may be vulnerable to dump attacks
- QNX Guest OS (AST-ECU-003) - At risk if hypervisor isolation is broken
- CAN-FD Bus (AST-COM-001) - Potential pivot target if QNX access achieved

**Attack Vector**: L (Local) - Exploit runs locally on Android partition after app installation, no network exploitation required for privilege escalation

---

## TS-IVI-003: WiFi Deauthentication Attack Causing Infotainment Denial of Service

**Threat Description**:
An attacker positions themselves within WiFi range (approximately 50 meters) of the target vehicle and uses a Software-Defined Radio (SDR) or commodity WiFi adapter to transmit 802.11 deauthentication frames targeting the vehicle's WiFi module (AST-COM-003). These spoofed management frames, sent on behalf of the legitimate WiFi access point, force the Head Unit to disconnect from the WiFi network repeatedly. Since the Head Unit's WiFi stack does not implement 802.11w (Protected Management Frames), it cannot distinguish legitimate deauth frames from spoofed ones. This prevents the infotainment system from maintaining WiFi connectivity for OTA updates, Internet streaming services, cloud-based navigation, and smartphone mirroring features. The attack causes user experience degradation and prevents critical OTA security patch delivery, leaving the vehicle vulnerable to other exploits.

**Threat Description (continued)**:
If executed persistently over days/weeks, the attack could delay security-critical OTA updates, violating UN R155 requirements for timely vulnerability remediation.

**Target Asset**:
AST-COM-003: Bluetooth/WiFi Module - Vulnerable due to lack of 802.11w Protected Management Frame support

**Attack Surface / Entry Point**:
802.11 wireless interface operating on 2.4 GHz / 5 GHz bands. Attack requires physical proximity (within WiFi range, typically 50-100m) but no authentication or pairing with vehicle. Attacker uses off-the-shelf WiFi hardware and freely available tools (aircrack-ng suite, Scapy). No physical access to vehicle interior required.

**STRIDE Category**:
Denial of Service - Wireless jamming prevents legitimate WiFi connectivity and service availability

**UN R155 Annex 5 Reference**:
4.3.7

**MITRE ATT&CK Reference**:
Impact: Network Denial of Service (T1498.001) - Wireless jamming disrupts network availability

**OWASP Reference**:
I5: Use of Insecure or Outdated Components - WiFi stack lacks 802.11w Protected Management Frames (security feature from 2009 WiFi standard)

**Damage Scenario Categories**:
- DS-IVI-006: Infotainment System Denial of Service - WiFi-dependent features (streaming, cloud navigation, OTA updates) become unavailable

**Attack Feasibility Rating (AFR)**:
AFR: 15 (High)
- Elapsed Time: 3 (< 1 week) - Pre-built tools like aircrack-ng can execute attack with single command
- Specialist Expertise: 3 (Layman / script kiddie) - Attack tutorials widely available online; requires no specialized knowledge
- Knowledge of Item: 3 (Publicly available / common knowledge) - 802.11 protocol specifications and deauth attack techniques documented in textbooks and online tutorials
- Window of Opportunity: 3 (Unlimited / always accessible) - Attack works whenever vehicle WiFi is enabled; attacker needs proximity but not specific timing
- Equipment: 3 (Off-the-shelf consumer electronics) - Commodity WiFi adapter ($20-50) and laptop running Kali Linux with aircrack-ng pre-installed

**CIA Triad**:
A (Availability) - Denies WiFi connectivity, preventing use of network-dependent services

**Real-world Examples / CVEs**:
- No public CVE - 802.11 deauthentication attack documented in IEEE 802.11 security analysis (academic research since 2001)
- No automotive-specific CVE, but attack applies to any WiFi-enabled vehicle without 802.11w protection
- Real-world demonstrations: DEF CON car hacking village presentations showing WiFi DoS on Tesla and other vehicles

**Last Updated**:
2026-03-19

**Confidence Level**:
High - Well-established attack vector with 20+ years of academic research and proof-of-concept tools; confirmed applicable to automotive WiFi modules lacking 802.11w

**Affected Vehicle Systems**:
- Bluetooth/WiFi Module (AST-COM-003) - Direct target of deauth frames
- Android Guest OS (AST-ECU-004) - Loses WiFi connectivity for app services
- Head Unit SoC (AST-ECU-001) - OTA update delivery via WiFi disrupted
- Infotainment displays (AST-ACT-002) - Streaming and cloud-based content unavailable

**Attack Vector**: A (Adjacent) - Requires local wireless network proximity (WiFi range, 50-100m) but no authentication or physical access

---

## Usage Notes

**Cross-Reference Validation**:
All AST-IDs in these examples reference assets from `data/asset_list.md`:
- AST-ECU-001, AST-ECU-002, AST-ECU-003, AST-ECU-004, AST-ECU-005
- AST-COM-001, AST-COM-003, AST-COM-005
- AST-SNS-001
- AST-DAT-001

All DS-IDs reference damage scenarios from `data/ds.md`:
- DS-IVI-001, DS-IVI-002, DS-IVI-003, DS-IVI-005, DS-IVI-006
- DS-CAN-001

**AFR Diversity**:
The examples demonstrate different feasibility levels:
- TS-IVI-001: AFR 12 (Moderate) - No exploits needed, only social engineering, but requires app development
- TS-IVI-002: AFR 7 (Low) - Requires expert-level exploit development
- TS-IVI-003: AFR 15 (High) - Trivial attack with commodity tools

**Framework Coverage**:
Each example maps to:
- STRIDE category (Information Disclosure, Elevation of Privilege, Denial of Service)
- MITRE ATT&CK technique (Collection, Privilege Escalation, Impact)
- OWASP category (Mobile M2, M7, IoT I5)
- UN R155 Annex 5 reference (4.3.4, 4.3.7)

**CVE Quality**:
- TS-IVI-001: No specific CVE (design weakness, not code bug)
- TS-IVI-002: Real CVEs (CVE-2019-2215, CVE-2020-0041)
- TS-IVI-003: Protocol-level attack (802.11 deauth) - no automotive-specific CVE
