# Threat Scenario Template

Use this template to document each threat scenario. Fill in all core required fields first, then add any optional metadata your project or downstream reporting requires. See `references/ts-schema.md` for the required-vs-optional split.

---

## Section 1: Blank Template

### TS-[DOMAIN]-[NNN]: [Threat Scenario Title]
<!-- 
  TS-ID Format: TS-[DOMAIN]-[NNN]
  Domain codes: CAN | OTA | EXT | BCK | IVI | IMM | ADAS
  Number: 3-digit zero-padded (001, 002, ..., 999)
  
  Domain Definitions (based on primary attack vector):
  - CAN: CAN bus and in-vehicle networking attacks
  - OTA: Over-the-air update and remote service attacks
  - EXT: External interface and physical access attacks
  - BCK: Backend/cloud service and API attacks
  - IVI: Infotainment application and OS attacks
  - IMM: Immobilizer and vehicle access control attacks
  - ADAS: Advanced driver assistance system attacks
  
  Title Guidelines:
  - Max 80 characters
  - Describe the ATTACK (not the damage)
  - Be specific (e.g., "CAN Bus Message Injection via Compromised Head Unit" not "CAN Attack")
  
  Examples:
  - TS-IVI-001: Malicious Android App Exfiltrating User Contacts
  - TS-CAN-001: CAN Bus Message Injection via Compromised Head Unit
  - TS-OTA-001: Man-in-the-Middle Attack on Firmware Update Channel
  - TS-EXT-002: Firmware Extraction via JTAG Debug Port
  - TS-BCK-001: Backend API Object-Level Authorization Bypass
  - TS-IMM-001: Keyless Entry Relay Attack Using RF Extenders
  - TS-ADAS-001: GPS Spoofing Attack on GNSS Receiver
-->

**Threat Description**:
<!-- 
  Provide a comprehensive description (3-5 sentences) of the threat scenario.
  
  Include:
  1. What the attacker does (attack method)
  2. How they do it (technical approach)
  3. What they exploit (vulnerability or weakness)
  4. What they achieve (immediate outcome, before damage occurs)
  
  Guidelines:
  - Focus on the THREAT (attack), not the damage (that's the DS field)
  - Be specific about technical details (protocols, interfaces, vulnerabilities)
  - Avoid vague terms ("exploit a vulnerability" → specify WHICH vulnerability or class)
  - Reference real CVEs or OWASP/MITRE categories where applicable
  
  Example:
  "An attacker exploits a broken object-level authorization vulnerability (OWASP API1:2023) 
  in the OEM's backend API service. By intercepting API requests using a proxy tool and 
  modifying the VIN parameter in the GET /api/v1/vehicle/{VIN}/location endpoint, they 
  bypass ownership checks and retrieve real-time GPS coordinates for vehicles they do not own. 
  The API only validates user authentication but fails to verify that the authenticated user 
  has permission to access the requested VIN, enabling enumeration of all VINs and mass 
  surveillance of vehicle locations."
-->

[3-5 sentences describing the attack. Include what, how, what exploit, and immediate outcome.]

**Target Asset**:
<!-- 
  Identify the PRIMARY asset being attacked (the entry point or initial target).
  Format: AST-ID: Asset Name
  
  Guidelines:
  - Reference ONLY assets from data/asset_list.md (do not fabricate)
  - Choose the asset that is DIRECTLY attacked (entry point), not secondary affected assets
  - If attack affects multiple assets sequentially, list the initial target here
  - Explain briefly WHY this asset is the target (1 sentence)
  
  Example:
  AST-ECU-004: Android Guest Operating System - Target for malicious app installation due to user-facing app ecosystem and external connectivity
-->

AST-[CAT]-[NNN]: [Asset Name] - [One-sentence justification for why this is the target]

**Attack Surface / Entry Point**:
<!-- 
  Describe where and how the attacker gains initial access.
  
  Common Entry Points:
  - Network: CAN-FD bus (remote), Automotive Ethernet, backend API endpoint, cellular connection
  - Adjacent: Bluetooth pairing, WiFi association, GNSS signal (proximity required)
  - Local: USB port, OBD-II port access (physical presence in vehicle cabin, no hardware teardown)
  - Physical: JTAG/SWD debug interface, disassembled ECU, hardware manipulation
  
  Guidelines:
  - Be specific (not "wireless" → "Bluetooth SSP pairing process")
  - Include access prerequisites (e.g., "requires physical proximity <5m" or "requires user to install app")
  - Mention any authentication required (or lack thereof)
  
  Example:
  Third-party Android app store with weak code signing verification. User downloads and installs 
  malicious APK. Attack requires user interaction (app installation) but no special privileges. 
  No physical access required.
-->

[2-3 sentences describing the entry point, access prerequisites, and authentication requirements]

**STRIDE Category**:
<!-- 
  Select one or more applicable STRIDE categories (can be multiple for complex threats). Reference references/framework-mapping.md for definitions.
  
  Categories:
  - Spoofing: Attacker impersonates a legitimate user, device, or system component
  - Tampering: Attacker modifies data, code, or configuration without authorization
  - Repudiation: Attacker denies performing an action, and the system cannot prove otherwise
  - Information Disclosure: Unauthorized access to or exfiltration of confidential data
  - Denial of Service: Attacker degrades or blocks legitimate system operations
  - Elevation of Privilege: Attacker gains capabilities beyond their authorized level
  
  Format: [Category] - [One-sentence explanation of why this category applies]
  
  Example:
  Elevation of Privilege - Malicious app exploits Android kernel vulnerability to escape app sandbox and gain root access
-->

[STRIDE Category] - [Why this category applies]

**UN R155 Annex 5 Reference** (optional):
<!-- 
  Map to UN R155 Annex 5 threat categories. Reference references/framework-mapping.md.
  
  Categories:
4.3.1: Backend servers (cloud infrastructure, OTA update servers, fleet management)
4.3.2: Communication channels (vehicle internal and external communication)
4.3.3: Update procedures (software/firmware update mechanisms - OTA, dealer reflash)
4.3.4: Code execution (unauthorized execution of code on vehicle systems)
4.3.5: Data and privacy (unauthorized access to or manipulation of vehicle/user data)
4.3.6: Safety-critical compromise (compromise of systems affecting vehicle safety functions)
4.3.7: External connectivity (external interfaces - USB, Bluetooth, cellular, V2X)
  
  Format: 4.3.[X] - [Brief mapping explanation]
  
  Example:
  4.3.7 - Attack exploits wireless Bluetooth interface for malicious pairing (external connectivity)
-->

4.3.[X] - [Mapping explanation]

**MITRE ATT&CK Reference** (optional):
<!-- 
  Map to MITRE ATT&CK ICS or Enterprise tactics. Reference references/framework-mapping.md.
  
  Choose ICS (T0xxx) for vehicle-specific attacks, Enterprise (T1xxx) for IT/cloud attacks.
  Include tactic name and technique ID.
  
  Example ICS:
  T0855: Unauthorized Command Message (for CAN injection)
  T0816: Device Restart/Shutdown (for DoS)
  
  Example Enterprise:
  T1190: Exploit Public-Facing Application (for backend API exploit)
  T1552.001: Credentials In Files (for hardcoded credentials)
  
  Format: [Tactic]: [Technique Name] ([ID])
  
  Example:
  Command and Control: Ingress Tool Transfer (T1105) - Malicious app downloads additional payloads
  
  Use "N/A - No direct mapping" if no appropriate MITRE technique exists.
-->

[Tactic]: [Technique Name] ([ID]) - [Brief explanation]

**OWASP Reference** (optional):
<!-- 
  Map to OWASP Top 10 (IoT, API, or Mobile). Reference references/framework-mapping.md.
  
  Choose the most relevant OWASP list:
  - OWASP IoT Top 10: For embedded device vulnerabilities (I1-I10)
  - OWASP API Security Top 10: For backend API vulnerabilities (API1-API10)
  - OWASP Mobile Top 10: For mobile app vulnerabilities (M1-M10)
  
  Format: [Category ID]: [Category Name] - [Explanation]
  
  Examples:
  API1:2023: Broken Object Level Authorization - API fails to verify VIN ownership
  M10: Insufficient Cryptography - Using deprecated cipher (DES) for key derivation in production app
  I3: Insecure Ecosystem Interfaces - Weak authentication on diagnostic protocol
  
  Use "N/A - No direct mapping" if this threat doesn't fit OWASP categories.
-->

[Category ID]: [Category Name] - [Explanation]

**Damage Scenario Categories**:
<!-- 
  List ALL damage scenarios (DS-IDs from data/ds.md) that this threat could cause.
  
  Guidelines:
  - Include DS-IDs across multiple domains if attack has cascading effects
  - Reference ONLY DS-IDs that exist in data/ds.md
  - Explain briefly HOW each damage scenario is triggered (optional, 1 sentence each)
  - Order by likelihood/severity (most likely first)
  
  Example:
  - DS-IVI-002: User Personal Data Exposure - App exfiltrates contacts and call history
  - DS-IVI-001: Unauthorized Location Tracking - App continuously uploads GPS coordinates
  - DS-CAN-001: Malicious CAN Message Injection - If app escalates to root and accesses CAN bus
-->

- DS-[DOMAIN]-[NNN]: [Damage Scenario Title] - [Optional: How this threat triggers this damage]
- DS-[DOMAIN]-[NNN]: [Damage Scenario Title]

**Attack Feasibility Rating (AFR)**:
<!-- 
  Calculate AFR using the 5-factor scoring method from references/afr-guide.md.
  
    Factors (each 0-3 points):
    1. Elapsed Time: How long to execute attack (0 => > 6 months, 1 = 1-6 months, 2 = 1 week - 1 month, 3 = < 1 week)
    2. Specialist Expertise: Required skill level (0 = Multiple experts with rare skills, 1 = Expert in automotive cybersecurity, 2 = Proficient IT/cybersecurity professional, 3 = Layman / script kiddie)
    3. Knowledge of Item: Information needed (0 = Restricted / classified, 1 = Confidential / limited access, 2 = Public with effort, 3 = Publicly available / common knowledge)
    4. Window of Opportunity: Attack time constraints (0 = Very narrow / restricted, 1 = Moderate access window, 2 = Easy access / extended time, 3 = Unlimited / always accessible)
    5. Equipment: Tools needed (0 = Bespoke / custom-built, 1 = Specialized but purchasable, 2 = Standard automotive tools, 3 = Off-the-shelf consumer electronics)
  
  Total Score = Sum of 5 factors (0-15)
  Rating Mapping (Lower scores = harder for attacker; higher numeric AFR = easier for attacker):
  - 0-4: Very Low (very difficult to difficult for attacker)
  - 5-9: Low (moderate difficulty for attacker)
  - 10-13: Moderate (lower barriers, more accessible to attacker)
  - 14-15: High (minimal barriers, easily executable by attacker)
  
   Format: 
   AFR: [Total Score] (one of: Very Low, Low, Moderate, High)
   - Elapsed Time: [0-3] - [Justification]
   - Specialist Expertise: [0-3] - [Justification]
   - Knowledge of Item: [0-3] - [Justification]
   - Window of Opportunity: [0-3] - [Justification]
   - Equipment: [0-3] - [Justification]
  
   Example:
    AFR: 7 (Low)
    - Elapsed Time: 1 (1-6 months) - Requires developing exploit for specific Android kernel version
    - Specialist Expertise: 1 (Expert in automotive cybersecurity) - Requires reverse engineering and exploit development skills
    - Knowledge of Item: 1 (Confidential / limited access) - Firmware internals, but samples available from OTA updates
    - Window of Opportunity: 2 (Easy access / extended time) - Attack works anytime vehicle is powered on
   - Equipment: 1 (Specialized but purchasable) - Custom firmware modification tools required
-->

AFR: [0-15] (Very Low | Low | Moderate | High)
- Elapsed Time: [0-3] (> 6 months | 1-6 months | 1 week - 1 month | < 1 week) - [Justification]
- Specialist Expertise: [0-3] (Multiple experts with rare skills | Expert in automotive cybersecurity | Proficient IT/cybersecurity professional | Layman / script kiddie) - [Justification]
- Knowledge of Item: [0-3] (Restricted / classified | Confidential / limited access | Public with effort | Publicly available / common knowledge) - [Justification]
- Window of Opportunity: [0-3] (Very narrow / restricted | Moderate access window | Easy access / extended time | Unlimited / always accessible) - [Justification]
- Equipment: [0-3] (Bespoke / custom-built | Specialized but purchasable | Standard automotive tools | Off-the-shelf consumer electronics) - [Justification]

**CIA Triad**:
<!-- 
  Indicate which CIA attribute(s) this threat violates. Can be one, two, or all three.
  
  - Confidentiality (C): Unauthorized access to data (e.g., location tracking, PII exposure)
  - Integrity (I): Unauthorized modification of data/code (e.g., firmware tampering, CAN injection)
  - Availability (A): Denial of service, system shutdown (e.g., CAN DoS, ransomware)
  
  Format: [C/I/A or combinations like C+I or C+I+A] - [One-sentence explanation]
  
  Examples:
  C - Exfiltrates user contacts and location data without authorization
  I - Injects false CAN messages to manipulate vehicle behavior
  C+I - Intercepts and modifies OTA firmware update packages
  A - Floods CAN bus preventing legitimate ECU communication
-->

[C / I / A / C+I / C+A / I+A / C+I+A] - [What is violated and how]

**Real-world Examples / CVEs** (optional):
<!-- 
  Reference documented vulnerabilities, academic research, or public security advisories.
  
  Guidelines:
  - Use REAL CVE numbers (search NVD, MITRE, or automotive CVE databases)
  - Reference published security research (e.g., "Miller & Valasek 2015 Jeep Cherokee hack")
  - Cite OEM security bulletins or recalls (e.g., "Tesla 2022 Security Update SB-22-xx-xxx")
  - If no specific CVE exists, reference similar vulnerability class (use real CVE as analogy)
  - Use "No public CVE - hypothetical based on [framework/research]" for novel threats
  
  Format (bullet list):
  - Real CVE number: [Vulnerability description] ([Affected product/vendor])
  - [Research paper citation or security bulletin]
  
  Example:
  - No public CVE - Tesla Model S relay attack (Francillon et al., NDSS 2011)
  - "Relay Attacks on Passive Keyless Entry" (Francillon et al., NDSS 2011)
  - Similar to CVE-2019-2215: Android kernel use-after-free enabling privilege escalation
-->

- [Add real CVE numbers or research citations here]
- [Research citation or "No public CVE - hypothetical based on..."]

**Last Updated** (optional):
<!-- 
  ISO 8601 date format: YYYY-MM-DD
  Update this whenever threat scenario content is modified.
-->

YYYY-MM-DD

**Confidence Level** (optional):
<!-- 
  Assess confidence in this threat scenario assessment.
  
  Levels:
  - High: Threat demonstrated in lab/production, documented CVEs, OEM security bulletins
  - Medium: Threat theoretically possible, supported by academic research, no confirmed exploits
  - Low: Hypothetical threat based on analogous systems, no direct evidence for automotive context
  
  Format: (one of: High, Medium, Low) - [One-sentence justification]
  
  Example:
  High - Multiple documented CVEs for Android kernel privilege escalation in automotive head units
  Medium - No confirmed automotive incidents, but attack demonstrated on similar IoT devices
-->

[High / Medium / Low] - [Justification]

**Affected Vehicle Systems**:
<!-- 
  List ALL vehicle systems/components that could be affected if this threat is realized.
  
  Include:
  - Direct targets (e.g., "Android Guest OS")
  - Cascading effects (e.g., "CAN-FD network if privilege escalation succeeds")
  - Potential pivot targets (e.g., "Safety ECUs via Gateway")
  
  Format: Bullet list
  
  Example:
  - Android Guest OS (AST-ECU-004) - Direct target
  - Hypervisor (AST-ECU-002) - If sandbox escape exploit succeeds
  - QNX Guest OS (AST-ECU-003) - If hypervisor isolation is broken
  - CAN-FD Bus (AST-COM-001) - If attacker gains QNX access
  - Gateway ECU (AST-ECU-006) - Potential pivot to safety networks
-->

- [System/Component] ([AST-ID if applicable]) - [Role in attack: direct target / cascading effect / pivot]
- [System/Component] ([AST-ID if applicable]) - [Role]

**Attack Vector** (optional): [N / A / L / P] ([Code Name]) - [Justification]

---

## Quick Checklist

Before finalizing this threat scenario entry, verify:

- [ ] TS-ID follows format `TS-[DOMAIN]-[NNN]` and is unique
- [ ] Domain code matches the PRIMARY attack vector (not the impacted system)
- [ ] Title describes the ATTACK (not the damage) in <80 chars
- [ ] Threat Description is 3-5 sentences covering what/how/exploit/outcome
- [ ] Target Asset references a real AST-ID from `data/asset_list.md`
- [ ] Attack Surface specifies entry point and access prerequisites
- [ ] STRIDE Category is present and matches the threat mechanism
- [ ] Damage Scenarios list ONLY DS-IDs that exist in `data/ds.md`
- [ ] AFR is calculated using all 5 factors with justifications
- [ ] CIA Triad indicates C/I/A violations
- [ ] Affected Systems lists all impacted components
- [ ] Optional metadata fields are filled only when verified or explicitly marked `N/A` / `hypothetical`
- [ ] No placeholder text remains (e.g., incomplete TODO/TBD markers)
- [ ] Cross-check with `references/ts-schema.md` for field requirements
- [ ] Cross-check with `references/afr-guide.md` for AFR scoring
- [ ] Cross-check with `references/framework-mapping.md` for STRIDE/MITRE/OWASP/R155

---

## Section 2: Completed Example

### TS-CAN-001: CAN Bus Message Injection via Compromised Head Unit

**Threat Description**:
An attacker first compromises the Android Guest OS (AST-ECU-004) on the vehicle's Head Unit by exploiting a malicious Android application installed from a third-party app store. The malicious app exploits a known Android kernel vulnerability (similar to CVE-2019-2215, a use-after-free bug) to escalate privileges from the app sandbox to root access. Once the attacker has root access on Android, they exploit a hypervisor isolation weakness to break out of the Android partition and write to memory regions belonging to the QNX Guest OS (AST-ECU-003), which has legitimate access to the CAN-FD bus (AST-COM-001). Using this cross-partition access, the attacker injects crafted CAN messages with spoofed ECU identifiers onto the vehicle network. These messages, targeting safety-critical systems via the Gateway ECU (AST-ECU-006), could trigger unintended vehicle behaviors such as emergency braking, acceleration, or disabling of ADAS functions. The attack exploits the broadcast nature of CAN (no message authentication) combined with insufficient isolation between Android and QNX partitions.

**Target Asset**:
AST-ECU-004: Android Guest Operating System - Initial attack target due to user-facing app installation capability and external connectivity, serving as entry point for privilege escalation chain leading to CAN access

**Attack Surface / Entry Point**:
Third-party Android app store with weak or absent code signing verification. User downloads and installs a seemingly legitimate navigation or entertainment application that contains malicious code. The attack requires user interaction (voluntary app installation) but no special privileges are needed for initial installation. No physical access to the vehicle is required - the malicious APK can be distributed via phishing links, compromised websites, or social engineering.

**STRIDE Category**:
Spoofing + Tampering - Attacker spoofs legitimate CAN ECU identifiers (Spoofing) and injects unauthorized messages to manipulate vehicle state (Tampering)

**UN R155 Annex 5 Reference**:
4.3.2 - Attack exploits vehicle internal network (CAN-FD bus) via compromised infotainment ECU with network access

**MITRE ATT&CK Reference**:
Command and Control: Unauthorized Command Message (T0855) - Attacker sends unauthorized CAN commands to vehicle systems after gaining network access

**OWASP Reference**:
M7: Insufficient Binary Protections - Malicious app exploits Android OS vulnerabilities (kernel privilege escalation) and hypervisor weaknesses (partition escape) to gain unauthorized hardware access

**Damage Scenario Categories**:
- DS-CAN-001: Unintended Emergency Braking - Injected CAN message claims phantom obstacle ahead
- DS-CAN-002: Loss of Steering Control - Injected message disables electronic power steering assist
- DS-CAN-003: Unintended Acceleration - Injected message overrides throttle control
- DS-IVI-003: Malicious Code Execution on Head Unit SoC - Initial compromise of Android enables persistent backdoor

**Attack Feasibility Rating (AFR)**:
AFR: 8 (Low)
- Elapsed Time: 2 (1 week - 1 month) - Develop full exploit chain from app delivery to CAN injection
- Specialist Expertise: 1 (Expert in automotive cybersecurity) - Android kernel exploit dev, hypervisor reverse engineering, CAN protocol knowledge
- Knowledge of Item: 1 (Confidential / limited access) - Android/hypervisor internals available from firmware dumps; CAN DBC files often leak online
- Window of Opportunity: 3 (Unlimited / always accessible) - Attack persists as long as malicious app remains installed; no time pressure
- Equipment: 1 (Specialized but purchasable) - Custom exploit tools for hypervisor escape and CAN frame crafting required

**CIA Triad**:
I (Integrity) - Injects unauthorized CAN messages to manipulate vehicle state and safety system behavior

**Real-world Examples / CVEs**:
- CVE-2019-2215: Android kernel use-after-free vulnerability enabling privilege escalation (Pixel devices)
- Miller & Valasek (2015): "Remote Exploitation of an Unaltered Passenger Vehicle" - Demonstrated CAN message injection via compromised head unit in Jeep Cherokee
- No public CVE - TLS downgrade attacks on automotive telematics documented in security research
- No specific CVE for hypervisor escape in QAM8295, but similar attacks demonstrated on Type-1 hypervisors in academic research (e.g., "Breaking Out of the Sandbox" - Black Hat 2018)

**Last Updated**:
2026-03-19

**Confidence Level**:
High - Multiple documented CVEs for Android kernel privilege escalation, and Miller & Valasek research demonstrates feasibility of CAN injection via compromised infotainment systems in production vehicles

**Affected Vehicle Systems**:
- Android Guest OS (AST-ECU-004) - Initial compromise target
- Hypervisor (AST-ECU-002) - Exploited for partition escape
- QNX Guest OS (AST-ECU-003) - Compromised to gain CAN-FD access
- CAN-FD Bus (AST-COM-001) - Attack delivery channel for malicious messages
- Gateway ECU (AST-ECU-006) - Routes attacker's messages to safety networks
- Downstream safety ECUs (ADAS, Body Control, Powertrain) - Ultimate targets of injected messages

**Attack Vector**: L (Local) - Requires malicious app installed on Android partition (user must download and install APK, but no physical access to vehicle required)
