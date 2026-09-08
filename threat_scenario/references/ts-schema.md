# Threat Scenario Schema - ISO 21434 TARA

This document defines the field set for threat scenario identification in ISO 21434 TARA (Threat Analysis and Risk Assessment) workflows, aligned with Clause 15.6 and the repository's AFR contract.

---

## Output Modes

The repository supports two output modes:

- **Core required fields**: the minimum set every TS entry must contain for normal execution and handoff
- **Extended optional fields**: additional metadata for audit, reporting, or evidence-rich projects

**Core required fields**:
1. TS-ID
2. Title
3. Threat Description
4. Target Asset
5. Attack Surface / Entry Point
6. STRIDE Category
7. Damage Scenario Categories
8. Attack Feasibility Rating (AFR)
9. CIA Triad
10. Affected Vehicle Systems

**Extended optional fields**:
11. UN R155 Annex 5 Reference
12. MITRE ATT&CK Reference
13. OWASP Reference
14. Real-world Examples / CVEs
15. Last Updated
16. Confidence Level
17. Attack Vector (AV)

Use extended fields when evidence is available or downstream reporting explicitly requires them.

---

## Field Definitions

### 1. TS-ID

**Format**: `TS-[DOMAIN]-[NNN]`

**Description**: Unique identifier for the threat scenario following a structured naming convention based on the affected vehicle domain.

**Domain Codes**:
- `CAN` - CAN bus and in-vehicle networking
- `OTA` - Over-the-air updates and remote services
- `EXT` - External interfaces and physical access points
- `BCK` - Backend/cloud services and infrastructure
- `IVI` - Infotainment and in-vehicle information systems
- `IMM` - Immobilizer and vehicle access control
- `ADAS` - Advanced driver assistance systems

**Example**: `TS-IVI-001`, `TS-CAN-012`, `TS-ADAS-005`

**Rules**:
- Check existing IDs before assigning to avoid conflicts
- Use zero-padded 3-digit numbers (001, 002, ..., 999)
- Domain code must match the primary attack surface or entry point
- If multiple domains are affected, choose the most critical domain for the ID

---

### 2. Title

**Format**: Human-readable text (maximum 80 characters)

**Description**: Concise, descriptive name for the threat scenario that clearly identifies the attack.

**Example**: 
- "CAN Bus Message Injection via OBD-II Port"
- "Malicious OTA Update Installation"
- "Firmware Extraction via JTAG Interface"
- "Backend API Authentication Bypass"

**Rules**:
- Focus on the ATTACK METHOD (how the threat manifests), not the damage
- Use action-oriented language describing the threat
- Be specific enough to distinguish from similar threat scenarios
- Include the attack surface or entry point when relevant
- Keep under 80 characters for readability

---

### 3. Threat Description

**Format**: Narrative text (3-5 sentences, 150-300 words)

**Description**: Detailed explanation of the threat scenario, including the attacker's goal, the method used, the target asset, and the exploitation technique.

**Example**:
```
An attacker with physical access to the vehicle's OBD-II diagnostic port 
connects a malicious CAN bus adapter to inject forged CAN frames onto the 
in-vehicle network. By crafting CAN messages with spoofed source IDs, the 
attacker impersonates legitimate ECUs (e.g., Gateway, Body Control Module) 
to send unauthorized commands or manipulate sensor data. This attack exploits 
the lack of authentication and encryption on traditional CAN bus protocols, 
allowing any node with physical access to transmit arbitrary messages. The 
attacker's goal is to influence vehicle behavior, exfiltrate diagnostic data, 
or establish persistent access for subsequent attacks.
```

**Required Components**:
1. **Attacker goal**: What the attacker is trying to achieve
2. **Attack method**: How the attack is executed (technical approach)
3. **Target asset**: Which asset is being compromised
4. **Exploitation technique**: What vulnerability or weakness is exploited
5. **Attack outcome**: What happens if the attack succeeds

**Rules**:
- Write 3-5 complete sentences
- Use present tense and active voice
- Be technically specific but avoid excessive jargon
- Explain the attack from the attacker's perspective
- Paraphrase any ISO 21434 concepts; do NOT quote the standard verbatim

---

### 4. Target Asset

**Format**: Asset ID from asset catalogue with name

**Description**: The primary asset that is the target of the threat scenario.

**Example**:
```
Target Asset: AST-ECU-001 (Head Unit System-on-Chip QAM8295)
```

**Rules**:
- Reference assets by their Asset ID from `data/asset_list.md`
- Include asset name after the ID for clarity
- Choose the PRIMARY target asset if multiple assets are involved
- The target asset should align with the domain code in TS-ID

**Relationship Clarification**:
- **Threat Scenario → Asset**: "This threat targets this asset"
- **Asset → Threat Scenario**: "This asset is vulnerable to these threat scenarios"

---

### 5. Attack Surface / Entry Point

**Format**: Text description of the physical or logical interface used to initiate the attack

**Description**: Identifies where the attacker enters the vehicle's attack surface.

**Example**:
- "OBD-II diagnostic port (physical access required)"
- "Bluetooth pairing interface (adjacent network access)"
- "OTA update server endpoint (remote network access)"
- "USB Type-A port (physical media insertion)"
- "Telematics cellular modem (remote network access)"

**Attack Surface Categories**:
- **Physical interfaces**: OBD-II, USB, JTAG, Serial Console, SD Card
- **Wireless interfaces**: Bluetooth, WiFi, Cellular, NFC, Key Fob RF
- **Network services**: OTA server, Backend API, Telematics server
- **User interfaces**: Infotainment touchscreen, mobile companion app

**Rules**:
- Be specific about the exact interface (not just "network" or "wireless")
- Indicate the access level required (physical, adjacent, remote)
- Explain if special equipment or credentials are needed
- One threat scenario can have one primary entry point

---

### 6. STRIDE Category

**Format**: One or more STRIDE threat types (S / T / R / I / D / E)

**Description**: Classification of the threat using the STRIDE threat modeling framework.

**STRIDE Categories**:
- **S** - Spoofing (impersonating a user or system component)
- **T** - Tampering (modifying data or code without authorization)
- **R** - Repudiation (denying actions without traceability)
- **I** - Information Disclosure (exposing sensitive information)
- **D** - Denial of Service (making systems unavailable)
- **E** - Elevation of Privilege (gaining unauthorized permissions)

**Example**:
```
STRIDE Category: S, T
(Spoofing of CAN node identity + Tampering with CAN message data)
```

**Rules**:
- List all applicable STRIDE categories (can be multiple)
- Provide brief explanation in parentheses when using multiple categories
- If only one category applies, list it alone
- Reference the framework mapping document for detailed STRIDE definitions

---

### 7. UN R155 Annex 5 Reference (Optional Metadata)

**Format**: Section number from UN R155 Annex 5

**Description**: Maps the threat scenario to UN R155 cybersecurity regulation categories.

**UN R155 Annex 5 Threat Categories**:
- **4.3.1** - Threats to vehicle backend servers
- **4.3.2** - Threats to vehicle communication channels and data links
- **4.3.3** - Threats to update procedures
- **4.3.4** - Threats from code execution on vehicle ECUs
- **4.3.5** - Threats to vehicle data and privacy
- **4.3.6** - Threats from compromise of safety-critical systems
- **4.3.7** - External connectivity (threats via external interfaces - USB, Bluetooth, cellular, V2X)

**Example**:
```
UN R155 Annex 5 Reference: 4.3.2, 4.3.6
```

**Rules**:
- List all applicable Annex 5 sections (can be multiple)
- Use the exact section numbering from UN R155 (4.3.1 through 4.3.7)
- Prioritize sections in order of primary to secondary relevance
- See framework-mapping.md for detailed category descriptions

---

### 8. MITRE ATT&CK Reference (Optional Metadata)

**Format**: Technique ID with name

**Description**: Maps the threat scenario to MITRE ATT&CK framework techniques.

**MITRE ATT&CK Matrices**:
- **ICS (Industrial Control Systems)**: Use for CAN bus, ECU, vehicle network threats (T0xxx format)
- **Enterprise**: Use for backend, cloud, IT infrastructure threats (T1xxx format)

**Example**:
```
MITRE ATT&CK Reference: T0855 (Unauthorized Command Message) [ICS]
```

**Rules**:
- Use the technique ID format (T0xxx for ICS, T1xxx for Enterprise)
- Include the technique name in parentheses for clarity
- Indicate which matrix in square brackets [ICS] or [Enterprise]
- Only reference REAL technique IDs from the MITRE ATT&CK database
- If no exact match exists, use "N/A" rather than inventing IDs
- See framework-mapping.md for common automotive MITRE techniques

---

### 9. OWASP Reference (Optional Metadata)

**Format**: OWASP category ID with name

**Description**: Maps the threat scenario to OWASP Top 10 security risks.

**OWASP Top 10 Lists**:
- **OWASP IoT Top 10**: For ECU, embedded systems, firmware threats (I1-I10)
- **OWASP API Security Top 10**: For backend API, web service threats (API1-API10)
- **OWASP Mobile Top 10**: For companion app, mobile interface threats (M1-M10)

**Example**:
```
OWASP Reference: I5 (Use of Insecure or Outdated Components) [IoT]
```

**Rules**:
- Use the OWASP category ID (I1-I10, API1-API10, M1-M10)
- Include the category name in parentheses for clarity
- Indicate which Top 10 list in square brackets
- Only reference REAL OWASP IDs from official Top 10 lists
- If no exact match exists, use "N/A" rather than inventing IDs
- See framework-mapping.md for OWASP category definitions

---

### 10. Damage Scenario Categories

**Format**: List of DS-IDs from damage scenario catalogue

**Description**: Links the threat scenario to the damage scenarios it could realize.

**Example**:
```
Damage Scenario Categories:
- DS-CAN-001 (CAN Message Injection Leading to Vehicle Control Manipulation)
- DS-CAN-002 (CAN Bus Denial of Service)
- DS-IVI-003 (Malicious Code Execution on Head Unit)
```

**Rules**:
- Reference damage scenarios by their DS-ID from `data/ds.md`
- Include damage scenario title after the ID for clarity
- List ALL damage scenarios this threat could cause
- One threat scenario can lead to multiple damage scenarios (many-to-many)
- One damage scenario can be realized by multiple threat scenarios
- Verify that all referenced DS-IDs exist in the damage scenario catalogue

**Traceability Chain**:
```
Asset → Threat Scenario → Damage Scenario → Risk → Treatment
```

---

### 11. Attack Feasibility Rating (AFR)

**Format**: AFR score (0-15) with rating level

**Description**: Assessment of how difficult it is to successfully execute the threat scenario, based on 5 factors.

**AFR Score Calculation**:
Sum of 5 factors (each scored 0-3), total range 0-15:
1. **Elapsed Time**: How long the attack takes to execute
2. **Specialist Expertise**: Attacker skill level required
3. **Knowledge of Item**: Information needed about the vehicle system
4. **Window of Opportunity**: Access duration required
5. **Equipment**: Tools and hardware needed

**AFR Rating Levels**:
- **Very Low (0-4)**: Very difficult (0) to difficult (4) for attacker; significant barriers (lower scores = harder)
- **Low (5-9)**: Moderate difficulty for attacker; balanced effort required
- **Moderate (10-13)**: Lower barriers for attacker; accessible to skilled attackers
- **High (14-15)**: Minimal barriers for attacker; easily executable

**Example**:
```
Attack Feasibility Rating: 12 (Moderate)
- Elapsed Time: 2 (1 week - 1 month) - Attack can be executed within one week once access is gained
- Specialist Expertise: 2 (Proficient IT/cybersecurity professional) - IT security background, general cybersecurity knowledge
- Knowledge of Item: 3 (Publicly available / common knowledge) - CAN protocol specs are public ISO standards
- Window of Opportunity: 2 (Easy access / extended time) - OBD-II port accessible when vehicle is parked
- Equipment: 3 (Off-the-shelf consumer electronics) - $50 CAN adapter from Amazon
Total AFR: 12 → Moderate (lower barriers for attacker, accessible to skilled attackers)
```

**Rules**:
- Score each of the 5 factors individually (0-3 scale)
- Sum the factors to get total AFR (0-15 range)
- Map the total to the rating level (Very Low/Low/Moderate/High)
- Include brief justification for each factor score
- See afr-guide.md for detailed scoring criteria

---

### 12. CIA Triad

**Format**: One or more CIA properties affected (C / I / A)

**Description**: Identifies which security properties are violated by the threat scenario.

**CIA Properties**:
- **C** - Confidentiality (unauthorized access to information)
- **I** - Integrity (unauthorized modification of data or code)
- **A** - Availability (denial of service or system unavailability)

**Example**:
```
CIA Triad: I, A
(Integrity: CAN message tampering; Availability: Bus flooding DoS)
```

**Rules**:
- List all applicable CIA properties (can be one, two, or all three)
- Provide brief explanation in parentheses when using multiple properties
- Align CIA with STRIDE: S/T/E→I, I→C, D→A, R→I
- If only one property applies, list it alone
- CIA is asset-centric; STRIDE is threat-centric

---

### 13. Real-world Examples / CVEs (Optional Metadata)

**Format**: List of CVE IDs with brief descriptions and year

**Description**: Provides evidence of the threat scenario in real-world automotive incidents.

**Example**:
```
Real-world Examples / CVEs:
- CVE-2015-5611: Jeep Cherokee CAN bus injection via cellular modem (2015)
- No public CVE - Diagnostic CAN message spoofing attacks on vehicle networks (Security research)
- No public CVE - OBD-II CAN injection on in-vehicle networks documented in academic research
```

**Rules**:
- Use REAL CVE IDs from the NVD database (do NOT invent CVE numbers)
- Include a brief description of the vulnerability (10-15 words)
- Include the year in parentheses
- List 1-5 relevant examples (prioritize automotive CVEs)
- If no CVE exists, cite research papers or industry reports:
  - "Miller & Valasek (2015): Remote exploitation of Jeep Cherokee"
  - "Keen Security Lab (2019): Tesla Model S gateway bypass"
- If purely theoretical, use "No known real-world examples (theoretical)"

**Where to Find CVEs**:
- NVD (National Vulnerability Database): https://nvd.nist.gov/
- Automotive CVE search: Filter by "automotive", "vehicle", "CAN", "ECU"
- Security researcher publications (Miller & Valasek, Tencent Keen Lab, etc.)

---

### 14. Last Updated (Optional Metadata)

**Format**: ISO 8601 date (YYYY-MM-DD)

**Description**: The date when the threat scenario was last reviewed or updated.

**Example**:
```
Last Updated: 2026-03-19
```

**Rules**:
- Use ISO 8601 format (YYYY-MM-DD)
- Update this date whenever ANY field in the threat scenario changes
- Initialize with the creation date for new threat scenarios
- Maintain version history if using git (commit messages capture change log)

---

### 15. Confidence Level (Optional Metadata)

**Format**: Confidence rating (High / Medium / Low)

**Description**: Assessment of the quality and reliability of the threat scenario evidence.

**Confidence Levels**:
- **High**: Real CVE cited, or peer-reviewed academic paper, or demonstrated exploit
- **Medium**: Industry white paper, security research report, or conference presentation
- **Low**: Theoretical threat based on general security principles, no public evidence

**Example**:
```
Confidence Level: High
(Multiple CVEs demonstrate real-world exploitation of CAN bus injection)
```

**Rules**:
- High: Requires at least one CVE or peer-reviewed publication
- Medium: Requires credible industry report or security researcher demonstration
- Low: Theoretical threat with no public evidence (but technically plausible)
- Include brief justification in parentheses
- Lower confidence does NOT mean the threat is invalid (theoretical threats are still valid)

---

### 16. Affected Vehicle Systems

**Format**: List of vehicle subsystems impacted

**Description**: Identifies which vehicle systems could be affected if the threat is realized.

**Vehicle Subsystems**:
- Powertrain (engine, transmission, hybrid/EV systems)
- Chassis (steering, braking, suspension)
- Body (doors, lights, climate control, wipers)
- ADAS (adaptive cruise, lane keeping, emergency braking)
- Connectivity (telematics, infotainment, navigation)
- Security (immobilizer, alarm, keyless entry)

**Example**:
```
Affected Vehicle Systems:
- Connectivity (Head Unit compromise enables network access)
- ADAS (Potential pivot via CAN gateway to ADAS ECUs)
```

**Rules**:
- List all vehicle systems that could be directly or indirectly affected
- Include brief explanation in parentheses for each system
- Distinguish between direct impact (system is the target) and indirect (pivot/lateral movement)
- Use standard automotive subsystem terminology
- Consider both immediate and downstream effects

---

### 17. Attack Vector (AV) (Optional Metadata)

**Format**: CVSS 3.x Attack Vector category (N / A / L / P)

**Description**: Characterizes the network proximity required for the attacker to exploit the threat.

**Attack Vector Categories** (aligned with CVSS 3.x):
- **N - Network**: Exploitable remotely over the internet (no physical or local access required)
- **A - Adjacent**: Requires access to the same network segment (e.g., vehicle WiFi, Bluetooth range)
- **L - Local**: Requires local access (e.g., physical presence in vehicle, OBD-II port access)
- **P - Physical**: Requires physical manipulation of hardware (e.g., JTAG probe, ECU removal)

**Example**:
```
**Attack Vector**: L (Local) - Requires physical access to OBD-II port in vehicle cabin
```

**Rules**:
- Choose the LEAST restrictive access level (if both Network and Local are possible, use Network)
- Use single-line format: `**Attack Vector**: X (Code Name) - Justification`
- Align with CVSS 3.x definitions for consistency
- Consider the INITIAL access required (not subsequent pivot stages)

**CVSS 3.x Alignment**:
This field is compatible with CVSS v3.x Base Score calculation. If performing full CVSS scoring, this Attack Vector (AV) metric can be reused.

---

## Related Scenarios Section

In addition to the core required fields and any optional metadata you choose to include, each threat scenario MAY include a **Related Scenarios** subsection linking to other threat scenarios that share attack techniques, target similar assets, or enable attack chains.

**Example**:
```
### Related Scenarios

- TS-CAN-002 (CAN Bus Denial of Service via Message Flooding)
- TS-EXT-001 (Malicious Firmware Installation via OBD-II)
- TS-IVI-005 (Head Unit Privilege Escalation Enabling CAN Access)
```

**Rules**:
- List related TS-IDs with titles
- Explain the relationship if not obvious
- Use for attack chains (multi-step attacks requiring multiple TSs)
- Use for alternative exploitation paths (different attacks achieving same damage)

---

## Schema Validation Checklist

Before marking a threat scenario as complete, verify:

- [ ] All core required fields are present
- [ ] TS-ID follows format and is unique
- [ ] Target Asset references a valid AST-ID from asset_list.md
- [ ] All Damage Scenario IDs reference valid DS-IDs from ds.md
- [ ] AFR score is calculated correctly (sum of 5 factors = 0-15)
- [ ] No incomplete TODO/TBD placeholders remain
- [ ] Threat Description is 3-5 sentences and paraphrases ISO 21434 (no verbatim quotes)
- [ ] Optional metadata fields, if present, are evidence-backed or explicitly marked `N/A` / `hypothetical`

---

## Field Dependencies and Traceability

**ISO 21434 Traceability Chain**:
```
Asset (AST-ID) → Threat Scenario (TS-ID) → Damage Scenario (DS-ID) 
→ Attack Feasibility (AFR) → Risk Value (Impact × Feasibility) 
→ Cybersecurity Goal (CSG-ID) → Treatment Decision
```

**Key Relationships**:
- **TS → Asset**: Every threat targets at least one asset
- **TS → DS**: Every threat can realize one or more damage scenarios
- **DS → Impact**: Impact remains owned by linked damage scenarios; TS references DS-IDs instead of duplicating impact
- **TS → AFR**: Attack feasibility is independently assessed per threat scenario
- **TS → Risk**: Risk = f(Impact, AFR) calculated in risk assessment phase

---

**End of Threat Scenario Schema**
