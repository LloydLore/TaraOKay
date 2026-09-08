# Asset Schema - ISO 21434 Asset Identification

This document defines the required fields for asset identification in ISO 21434 TARA (Threat Analysis and Risk Assessment) workflows.

---

## Required Fields

Every asset in the asset catalogue must include ALL 7 required fields:

### 1. Asset ID

**Format**: `AST-[CAT]-[NNN]`

**Description**: Unique identifier for the asset following a structured naming convention.

**Category Codes**:
- `ECU` - Electronic Control Unit
- `GW` - Gateway
- `SNS` - Sensor
- `ACT` - Actuator
- `COM` - Communication
- `DAT` - Data
- `IFC` - Interface

**Example**: `AST-ECU-001`, `AST-GW-012`, `AST-SNS-005`

**Rules**:
- Check existing IDs before assigning to avoid conflicts
- Use zero-padded 3-digit numbers (001, 002, ..., 999)
- Category code must match the asset's primary classification
- Keep IDs stable once published (do not renumber existing IDs)

---

### 2. Asset Name

**Format**: Human-readable text (max 100 characters)

**Description**: Clear, descriptive name for the asset that identifies its function or role.

**Example**: 
- "Telematics Control Unit (TCU)"
- "Central Gateway ECU"
- "Vehicle Speed Sensor"
- "CAN Bus Communication Protocol"

**Rules**:
- Use official product names when available
- Include abbreviations in parentheses on first use
- Be specific enough to distinguish from similar assets

---

### 3. Description

**Format**: Detailed text (minimum 3 sentences)

**Description**: Comprehensive explanation of what the asset is, what it does, and why it matters for vehicle security.

**Example**:
```
The Telematics Control Unit (TCU) manages all wireless communications between 
the vehicle and external networks, including cellular, Wi-Fi, and Bluetooth 
connections. It handles over-the-air (OTA) software updates, remote diagnostics, 
emergency call (eCall) services, and infotainment connectivity. The TCU is a 
critical gateway between the vehicle's internal networks and the outside world, 
making it a high-value target for cyber attacks.
```

**Rules**:
- Minimum 3 complete sentences
- Cover: what it is, what it does, security relevance
- Include technical details (protocols, capabilities, connections)
- Explain criticality from a cybersecurity perspective

---

### 4. Category

**Format**: One of 7 predefined vehicle system categories

**Categories**:

| Category | Code | Description |
|----------|------|-------------|
| Electronic Control Unit | ECU | Embedded computers that control vehicle functions (engine, brakes, steering, etc.) |
| Gateway | GW | Network bridges that connect different vehicle buses (CAN, LIN, FlexRay, Ethernet) |
| Sensor | SNS | Input devices that measure physical properties (speed, temperature, distance, camera, radar, lidar) |
| Actuator | ACT | Output devices that perform physical actions (motors, valves, displays, speakers) |
| Communication | COM | Protocols and channels for data exchange (CAN, Ethernet, Bluetooth, cellular, Wi-Fi) |
| Data | DAT | Stored or transmitted information (calibration data, logs, user data, cryptographic keys) |
| Interface | IFC | External connection points (OBD-II port, USB, diagnostic connectors, charging port) |

**Category name ↔ Asset ID code mapping (canonical)**:

| Category Name | Asset ID Code |
|---|---|
| ECU | ECU |
| Gateway | GW |
| Sensor | SNS |
| Actuator | ACT |
| Communication | COM |
| Data | DAT |
| Interface | IFC |

**Example**: `ECU`, `Gateway`, `Sensor`

**Rules**:
- Must select exactly ONE category from the 7 defined
- Choose the category that best represents the asset's primary function
- If an asset spans multiple categories, classify by its most security-critical aspect
- Use the **Category Name** in the `Category` field, and use the **Asset ID Code** only in `Asset ID`

**Borderline classification rules**:
- Integrated radios/modems inside an ECU are usually part of the ECU asset unless modeled separately for TARA scope.
- A protocol or transport channel (cellular, Bluetooth, Wi-Fi, CAN, Ethernet) is `Communication`.
- A physical or logical access point exposed to users, service tools, chargers, or external actors is `Interface`.
- Configuration, credentials, routing tables, firmware images, logs, and key material are `Data` even when stored inside an ECU.
- If two categories seem plausible, choose one canonical category and document the rationale in `Evidence & Confidence` / assumptions.

---

### 5. CIA Rating (Intrinsic Sensitivity)

**Purpose**: Captures the asset's **intrinsic security sensitivity** — a static property of the asset itself (how sensitive / how trust-critical / how time-critical the data or function is *by nature*). This is **not** a forecast of the damage a compromise causes; that belongs to the downstream `damage_scenario` skill (SFOP — Safety / Financial / Operational / Privacy, ISO 21434 §15.4). Do not pre-compute SFOP severity here.

**Format**: Confidentiality / Integrity / Availability ratings using a 4-level scale

**Scale**:

| Level | Numeric | Confidentiality (data sensitivity class) | Integrity (trust-criticality) | Availability (time-criticality) |
|-------|---------|------------------------------------------|-------------------------------|---------------------------------|
| Negligible | 1 | Public / freely shareable | Informational; tampering is harmless | Optional; can be offline indefinitely |
| Moderate | 2 | Internal-use; limited sensitivity | Operational; tampering causes degraded UX | Convenience; brief outage tolerable |
| Major | 3 | Restricted; PII / proprietary | Important; must be authentic for correct function | Important; sustained outage disrupts function |
| Severe | 4 | Secret; keys / credentials / regulated data | Safety-grade / legally-binding; must be tamper-proof | Continuous-required; must always be up |

**Format**: `C:X / I:X / A:X` where X is the numeric rating (1-4)

**Example**:
- `C:3 / I:4 / A:2` - PII data, integrity must be tamper-proof, brief outage tolerable
- `C:1 / I:3 / A:4` - Public data, integrity must be authentic, must be continuously available

**Rules**:
- Rate each dimension (C, I, A) independently based on the asset's **intrinsic** property, not on any specific attack outcome
- **Confidentiality**: How sensitive is this data by nature?
- **Integrity**: How trust-critical must this data/function be by nature?
- **Availability**: How time-critical is continuous availability by nature?
- Do **not** reason "if attacker does X, then Y people die" here — that is SFOP/damage analysis
- Two assets with identical CIA can have very different SFOP downstream depending on context

#### Other security properties (optional, not part of the C/I/A field)

ISO/SAE 21434 explicitly allows additional cybersecurity properties beyond C/I/A when the asset's nature requires them. They are **optional** and, if used, MUST be recorded as a separate annotation under CIA — never folded into the `C:X / I:X / A:X` numbers.

| Property | When to record it | How to record |
|----------|-------------------|---------------|
| **Authenticity** | Asset's value depends on proving *who* produced/sent the data (e.g. signed firmware, signed CAN messages, signed OTA manifests) | Add bullet `- Authenticity: [Negligible \| Moderate \| Major \| Severe] — [why]` under the CIA bullets |
| **Non-repudiation** | A party must not be able to plausibly deny an action (e.g. diagnostic session logs, tachograph records, regulated event logs) | Add bullet `- Non-repudiation: [Negligible \| Moderate \| Major \| Severe] — [why]` under the CIA bullets |
| **Authorization / Accountability** | Distinct from integrity (e.g. role-based access enforcement on diagnostic services UDS 0x27/0x29) | Same pattern; one bullet per property |

**Rules**:
- Do NOT mutate the `C:X / I:X / A:X` line — the validation regex (`references/validation.md` step [5/7]) only matches three dimensions and downstream tools depend on it.
- These extra properties are **descriptive**, not part of the canonical CIA score. Downstream `damage_scenario` reads CIA + free-text justification, so put authenticity/non-repudiation reasoning in the justification bullets where it will be picked up.
- If you find yourself repeatedly needing a 4th dimension across many assets, raise it as a project-level decision instead of silently extending the schema.

---

### 6. Interfaces

**Format**: Bullet list (preferred) of connected systems, protocols, and data flows

**Description**: All communication channels, network connections, and integration points with other vehicle systems or external entities.

**Example**:
```
Interfaces:
- CAN-FD powertrain bus (connection to Engine ECU, Transmission ECU)
- Ethernet backbone (connection to Central Gateway)
- Cellular modem (LTE/5G connection to OEM backend)
- Bluetooth 5.0 (connection to mobile devices)
- USB 2.0 diagnostic port (internal service interface)
```

**Rules**:
- List ALL interfaces (internal and external)
- Specify protocols used (CAN, Ethernet, Bluetooth, etc.)
- Identify connected systems/ECUs
- Distinguish between input and output data flows where relevant
- Include physical interfaces (ports, connectors)
- If compact representation is needed, a comma-separated summary line may be added in addition to bullets

---

### 7. Related Systems

**Format**: List of dependencies, upstream/downstream assets, and relationships

**Description**: Other assets that this asset depends on, interacts with, or affects. Maps the asset's position in the vehicle system architecture.

**Example**:
```
Related Systems:
- Depends on: Central Gateway (for network routing), Power Management ECU (for power supply)
- Provides data to: Infotainment System, OEM Cloud Services, Mobile App
- Security relationship: Shares cryptographic key material with OTA Update Server
- Safety relationship: Impacts eCall Emergency Service functionality
```

**Rules**:
- Identify dependencies (what this asset needs to function)
- Identify dependents (what depends on this asset)
- Note security relationships (authentication, encryption, trust boundaries)
- Note safety relationships (impact on safety functions)
- Reference other assets by their Asset ID when possible

---

## Asset Categories - Detailed Definitions

### Electronic Control Unit (ECU)
Embedded computers with microprocessors that control specific vehicle functions. Examples: Engine Control Module (ECM), Brake Control Module (BCM), Airbag Control Unit (ACU), Body Control Module (BCM).

**Security Considerations**: ECUs often run safety-critical functions. Compromise can lead to loss of vehicle control, injury, or death.

### Gateway (GW)
Network bridges that connect different vehicle communication buses (CAN, LIN, FlexRay, Ethernet). Gateways route messages between network segments and often implement firewall rules.

**Security Considerations**: Gateways are critical chokepoints. A compromised gateway can enable lateral movement across vehicle networks.

### Sensor (SNS)
Input devices that measure physical properties and convert them to electrical signals. Examples: Speed sensors, cameras, radar, lidar, temperature sensors, pressure sensors.

**Security Considerations**: Sensor spoofing can mislead automated driving systems or safety functions.

### Actuator (ACT)
Output devices that convert electrical signals into physical actions. Examples: Motors (steering, throttle), valves (fuel injection, brakes), displays, speakers.

**Security Considerations**: Unauthorized actuator control can directly cause unsafe vehicle behavior.

### Communication (COM)
Protocols and channels for data exchange within the vehicle or between vehicle and external systems. Examples: CAN bus, Ethernet, Bluetooth, cellular (LTE/5G), Wi-Fi, V2X.

**Security Considerations**: Communication channels are attack surfaces. Unencrypted or unauthenticated channels enable eavesdropping and injection attacks.

### Data (DAT)
Information stored or transmitted by vehicle systems. Examples: Calibration data, firmware, user profiles, location history, cryptographic keys, diagnostic logs.

**Security Considerations**: Data theft can violate privacy. Data tampering can disable security controls or alter vehicle behavior.

### Interface (IFC)
Physical or logical connection points that provide external access to vehicle systems. Examples: OBD-II port, USB ports, diagnostic connectors, charging port, infotainment inputs.

**Security Considerations**: Interfaces are entry points for attackers. Unsecured interfaces enable unauthorized access to internal networks.

---

## CIA Rating Guidelines

> **Reminder**: CIA here = **intrinsic sensitivity** of the asset. Damage-of-compromise (SFOP) is downstream in `damage_scenario`. Frame each question as "what kind of asset is this", not "what bad thing happens".

### Confidentiality Assessment

Ask: "How sensitive is this data **by its nature**?"

- **Negligible (1)**: Public information or non-sensitive operational data
- **Moderate (2)**: Internal vehicle data; limited sensitivity
- **Major (3)**: Personal user data, location history, or proprietary calibration data (PII / restricted)
- **Severe (4)**: Cryptographic keys, authentication credentials, or regulated highly-sensitive data

### Integrity Assessment

Ask: "How trust-critical must this data/function be **by its nature** — what level of authenticity does it inherently demand?"

- **Negligible (1)**: Informational only; tampering is harmless
- **Moderate (2)**: Operational data; tampering causes degraded UX
- **Major (3)**: Important functions that must be authentic to behave correctly
- **Severe (4)**: Safety-grade or legally-binding data/function; must be tamper-proof by design

### Availability Assessment

Ask: "How time-critical is continuous availability **by its nature**?"

- **Negligible (1)**: Optional; can be offline indefinitely
- **Moderate (2)**: Convenience features; brief outage tolerable
- **Major (3)**: Important functions; sustained outage disrupts the system
- **Severe (4)**: Continuous-required by design or by regulation (e.g., eCall)

---

## Example Asset Entry

```markdown
**Asset ID**: AST-ECU-015

**Asset Name**: Telematics Control Unit (TCU)

**Description**: The Telematics Control Unit (TCU) manages all wireless communications between the vehicle and external networks, including cellular (LTE/5G), Wi-Fi, and Bluetooth connections. It handles over-the-air (OTA) software updates, remote diagnostics, emergency call (eCall) services, stolen vehicle tracking, and infotainment connectivity features. The TCU is a critical gateway between the vehicle's internal CAN/Ethernet networks and the outside world, making it a high-value target for remote cyber attacks and a key component in the vehicle's attack surface.

**Category**: ECU

**CIA Rating**: C:3 / I:4 / A:3
- Confidentiality (Major): Contains user location data, personal contacts, and vehicle usage patterns
- Integrity (Severe): Tampering could enable unauthorized OTA updates or disable security features
- Availability (Major): Loss of eCall functionality impacts legal compliance; loss of OTA impacts security patch delivery

**Interfaces**:
- CAN-FD powertrain bus (connection to Engine ECU, Transmission ECU, Gateway)
- Ethernet backbone (connection to Central Gateway, Infotainment System)
- Cellular modem (LTE/5G to OEM backend server, emergency services)
- Bluetooth 5.0 (connection to user mobile devices for hands-free calling)
- Wi-Fi 802.11ac (hotspot for passenger devices)
- GPS/GNSS receiver (location services)
- Internal flash storage (firmware, keys, user data)

**Related Systems**:
- Depends on: Central Gateway (network routing), Power Management ECU (12V power), GNSS Antenna (location)
- Provides data to: Infotainment System (connectivity status), Cloud Services (telemetry, diagnostics), Mobile App (remote commands)
- Security relationship: Authenticates with OTA Update Server using embedded PKI certificates; shares session keys with Infotainment System for Bluetooth pairing
- Safety relationship: Provides eCall emergency crash notification (legally required in EU); impacts safety through OTA update integrity
```

---

## Quick Reference Table

| Field | Format | Example |
|-------|--------|---------|
| Asset ID | `AST-[CAT]-[NNN]` | AST-ECU-015 |
| Asset Name | Human-readable text | Telematics Control Unit (TCU) |
| Description | 3+ sentences | The TCU manages all wireless... |
| Category | ECU \| Gateway \| Sensor \| Actuator \| Communication \| Data \| Interface | ECU |
| CIA Rating | C:X / I:X / A:X (1-4 scale) | C:3 / I:4 / A:3 |
| Interfaces | List of connections | CAN-FD bus, Cellular LTE, Bluetooth... |
| Related Systems | Dependencies & relationships | Depends on Central Gateway... |

---

## Validation Checklist

Before finalizing an asset entry, verify:

- [ ] Asset ID follows `AST-[CAT]-[NNN]` format
- [ ] Asset ID is unique (no duplicates)
- [ ] Asset Name is clear and descriptive
- [ ] Description has at least 3 complete sentences
- [ ] Category is one of the 7 defined categories
- [ ] CIA Rating has all three dimensions (C, I, A) with values 1-4
- [ ] CIA Rating justification is documented
- [ ] Interfaces lists ALL connection points (internal and external)
- [ ] Related Systems identifies dependencies and dependents
- [ ] No placeholder text remains (e.g., [TODO], [TBD])
