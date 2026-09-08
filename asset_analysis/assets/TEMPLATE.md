# Asset Template

Use this template to document each asset. Copy this structure and fill in all 7 required fields.

---

### AST-[CAT]-[NNN]: [Asset Name]
<!-- 
  Asset ID Format: AST-[CAT]-[NNN]
  Category codes: ECU | GW | SNS | ACT | COM | DAT | IFC
  Number: 3-digit zero-padded (001, 002, ..., 999)
  
  Examples:
  - AST-ECU-001: Engine Control Unit
  - AST-GW-001: Central Gateway
  - AST-SNS-005: Front Camera
  - AST-ACT-012: Brake Actuator
  - AST-COM-003: CAN Bus
  - AST-DAT-001: Cryptographic Keys
  - AST-IFC-001: OBD-II Diagnostic Port
-->

**Description**: [Write at least 3 complete sentences describing what this asset is, what it does, and why it matters from a cybersecurity perspective. Explain the asset's function, its role in the vehicle system, and its security relevance. Be specific about technical details like protocols, capabilities, and connections.]

<!-- 
  Description Guidelines:
  - Minimum 3 sentences (aim for 4-6 for complex assets)
  - First sentence: What it is
  - Second sentence: What it does (function, capabilities)
  - Third+ sentence: Security relevance, criticality, or risk context
  - Include technical details: protocols, data types, performance characteristics
  - Explain why this asset matters for security/safety
-->

**Category**: [ECU | Gateway | Sensor | Actuator | Communication | Data | Interface]

<!--
  Category → Asset ID Code mapping (the only thing this template owns):
  - ECU            → ECU
  - Gateway        → GW
  - Sensor         → SNS
  - Actuator       → ACT
  - Communication  → COM
  - Data           → DAT
  - Interface      → IFC

  IMPORTANT:
  - `Category:` field uses the English name (e.g. `Gateway`) — never localize.
  - `Asset ID:` uses the code (e.g. `AST-GW-001`).

  For category *definitions* (what counts as ECU vs Gateway vs Sensor, etc.)
  read references/asset-schema.md §5 — do NOT duplicate them here. Single
  source of truth prevents drift between template and schema.

  Borderline examples:
  - Cellular/Bluetooth/Wi-Fi as a transport path → Communication
  - User/service-accessible connector or endpoint → Interface
  - Credentials, routing tables, logs, firmware images → Data
  - Integrated modem/radio not modeled separately → include under its ECU asset
-->

**CIA Rating**: C:X / I:X / A:X
- Confidentiality ([Negligible | Moderate | Major | Severe]): [Intrinsic data sensitivity — how sensitive is this data class by nature? Do NOT reason about specific attack outcomes here; that belongs in damage_scenario / SFOP.]
- Integrity ([Negligible | Moderate | Major | Severe]): [Intrinsic trust-criticality — how tamper-proof must this asset be by nature? Informational vs operational vs important vs safety-grade.]
- Availability ([Negligible | Moderate | Major | Severe]): [Intrinsic time-criticality — optional vs convenience vs important vs continuous-required.]

<!--
  CIA is INTRINSIC SENSITIVITY only. See references/asset-schema.md §5 for the
  full 4-level scale, the C/I/A definitions, and the rule against pre-computing
  SFOP severity in this field.

  Optional extra properties (authenticity, non-repudiation) — see
  references/asset-schema.md §5 "Other security properties". Add them as
  separate bullets; never fold into the C:X / I:X / A:X line.
-->

**Interfaces**:
- [List all connections, communication channels, protocols, and data flows]
- [Include internal interfaces (e.g., SPI bus to other chips) and external interfaces (e.g., cellular network)]
- [Specify protocol names and versions (e.g., CAN-FD 2.0, Bluetooth 5.0, TLS 1.3)]
- [Identify connected systems/ECUs by name]
- [Distinguish input vs. output data flows where relevant]
- [Include physical interfaces (ports, connectors, antennas)]

<!--
  Interface Guidelines:
  - List ALL interfaces (nothing should be omitted)
  - Be specific: "CAN-FD powertrain bus", not just "CAN"
  - Include physical layer: "twisted-pair cables", "RF 2.4 GHz", "USB 2.0 Type-C"
  - Identify connected ECUs: "Connection to Engine ECU, Transmission ECU"
  - Note data direction if relevant: "Receives GPS signals", "Sends brake commands"
  - Include internal interfaces: "Internal flash storage", "SPI to modem chip"
-->

**Related Systems**:
- Depends on: [List assets or systems this asset requires to function. E.g., power supply, network connectivity, upstream data sources]
- Provides data to: [List assets or systems that rely on this asset's data or functionality. E.g., downstream ECUs, cloud services]
- Security relationship: [Describe authentication, encryption, trust boundaries. E.g., "Authenticates via TLS certificates", "Shares symmetric keys with X"]
- Safety relationship: [Describe impact on safety functions. E.g., "Provides data for emergency braking", "Controls steering actuator"]

**Evidence & Confidence** (recommended):
- Sources: [Input doc name/section, or interview answer index]
- Confidence: [High | Medium | Low]
- Assumptions/Unknowns: [Explicit unresolved items]

<!--
  Relationship Guidelines:
  - Dependencies: What must be working for this asset to function?
    Examples: Power supply, gateway routing, sensor inputs, network connectivity
  - Dependents: What breaks if this asset fails?
    Examples: Downstream ECUs waiting for data, cloud services expecting telemetry
  - Security relationships: How is trust established? What crypto is used?
    Examples: PKI certificates, symmetric MACs, firewall rules, encryption protocols
  - Safety relationships: Does this asset affect ISO 26262 safety functions?
    Examples: ASIL-rated functions, emergency systems (eCall, AEB), braking/steering
  - Reference other assets by their Asset ID when possible: "Depends on AST-ECU-001"
-->

---

## Quick Checklist

Before finalizing this asset entry, verify:
- [ ] Asset ID follows format `AST-[CAT]-[NNN]` and is unique
- [ ] Asset Name is clear and descriptive (not generic)
- [ ] Description has at least 3 complete sentences
- [ ] Category is one of the 7 defined categories
- [ ] CIA Rating has all three dimensions (C, I, A) with numeric values (1-4)
- [ ] CIA Rating includes justification for each dimension
- [ ] Interfaces lists ALL connection points (internal and external)
- [ ] Related Systems identifies both dependencies and dependents
- [ ] No placeholder text remains ([TODO], [TBD], etc.)
- [ ] Asset data is based on actual system knowledge, not fabricated
- [ ] Sources and confidence are explicitly documented

---

## Example (for reference)

### AST-ECU-003: Engine Control Unit (ECU)

**Description**: The Engine Control Unit (ECU) is a safety-related embedded computer that manages all aspects of internal combustion engine operation, including fuel injection timing, ignition timing, air-fuel ratio, turbocharger boost pressure, and emissions control. It receives sensor data (throttle position, airflow, coolant temperature, oxygen sensor readings) via the Powertrain CAN-FD bus and outputs actuator commands to fuel injectors, ignition coils, and the electronic throttle body. The Engine ECU is critical for vehicle operation - if it fails or is tampered with, the vehicle cannot start or may experience unintended acceleration, engine stall, or excessive emissions. As a component of the powertrain system, it is subject to emissions regulations (e.g., EPA, CARB) and potential cybersecurity attacks targeting fuel economy manipulation or diagnostics fraud.

**Category**: ECU

**CIA Rating**: C:2 / I:4 / A:4
- Confidentiality (Moderate): Engine ECU data includes fuel consumption, engine RPM, vehicle speed, and diagnostic codes. While not highly privacy-sensitive (no user identity data), it could reveal driving behavior for insurance or legal purposes. Impact is moderate.
- Integrity (Severe): Tampering with Engine ECU firmware or CAN messages could cause unintended acceleration (forged throttle commands), engine stall (fuel cutoff), or emissions non-compliance (disabling catalytic converter). Safety impact is severe - unintended acceleration could cause crashes and fatalities.
- Availability (Severe): If the Engine ECU becomes unavailable (crash, denial-of-service, power loss), the vehicle cannot start or the engine will immediately shut down. This disables the vehicle and could create safety hazards (stalling in traffic). Availability is critical for basic vehicle operation.

**Interfaces**:
- Powertrain CAN-FD bus (500 kbps / 2 Mbps, connection to Transmission ECU, Battery Management, Central Gateway)
- Sensor inputs: Throttle Position Sensor (TPS), Mass Airflow Sensor (MAF), Coolant Temperature Sensor, Oxygen Sensors (O2), Knock Sensors
- Actuator outputs: Fuel Injectors (8 cylinders), Ignition Coils (8 cylinders), Electronic Throttle Body, Turbocharger Wastegate, EGR Valve
- OBD-II diagnostic port (via Gateway, ISO 15765-4 protocol for reading fault codes)
- Internal flash memory (firmware, calibration tables, fault code storage)
- 12V power supply from vehicle battery

**Related Systems**:
- Depends on: Central Gateway (CAN routing), Sensors (TPS, MAF, O2, etc.), 12V Power Supply, Fuel Delivery System (pump, injectors)
- Provides data to: Transmission ECU (torque requests), Instrument Cluster (RPM, warning lights), Telematics ECU (diagnostics, fuel economy), Infotainment (engine status display)
- Security relationship: CAN messages not encrypted; some critical messages use Message Authentication Codes (MACs); firmware updates via OTA use digital signatures verified by secure boot
- Safety relationship: Controls engine power output (acceleration); if compromised, could cause unintended acceleration or engine stall; indirectly affects braking (engine braking, vacuum for brake booster on non-electric vehicles)
