# Example 01: Telematics Control Unit Analysis

This example demonstrates the asset identification workflow for a Telematics Control Unit (TCU) in a connected vehicle.

---

## Input Scenario

**System**: Telematics and Connectivity System  
**Scope**: Telematics Control Unit (TCU) and related wireless communication assets  
**Reference Documents**: (Simulated - in real scenario, these would be in `input/` directory)
- System Architecture Diagram
- TCU Technical Specification
- Wireless Communication Requirements

**User's Goal**: Identify security-relevant assets for the telematics subsystem to support ISO 21434 TARA.

---

## Interview Answers (Simulated User Input)

### System Overview

**Q1: What vehicle system or component are we analyzing?**
> We're analyzing the Telematics Control Unit and the wireless connectivity subsystem. This includes the TCU hardware, the cellular modem, Bluetooth radio, Wi-Fi module, and the associated communication protocols. The scope is limited to the telematics domain - we're not covering the entire vehicle, just the external wireless communication path.

**Q2: What reference documents or specifications are available?**
> We have the TCU technical specification (version 2.3), a system architecture diagram showing how the TCU connects to the vehicle networks, and the wireless communication security requirements document. These documents are in the input/ folder.

### Components and Architecture

**Q3: What are the main electronic control units (ECUs) in this system?**
> The main ECU is the Telematics Control Unit itself. It's a safety-related ECU (not safety-critical for vehicle operation, but it provides eCall emergency services which is legally required in EU). The TCU contains several subsystems: a cellular modem (LTE/5G), a Bluetooth controller, a Wi-Fi module, and a GPS/GNSS receiver.

**Q4: What network architecture connects these components?**
> The TCU connects to the vehicle's Ethernet backbone, which links it to the Central Gateway ECU. Through the gateway, it has indirect access to CAN-FD buses for powertrain and body networks, but it does not directly connect to CAN buses. The internal architecture uses SPI and UART buses to connect the main processor to the cellular modem, Bluetooth controller, and Wi-Fi module.

**Q5: What sensors and actuators are present?**
> The GPS/GNSS receiver is the primary sensor - it provides location data. There's also a 4G/5G signal strength sensor (built into the modem). No direct actuators in this subsystem, but the TCU indirectly controls vehicle functions via remote commands (e.g., remote door unlock, remote start).

### Data Flows and Interfaces

**Q6: What data flows through this system?**
> The TCU handles several types of data:
> - **Location data**: GPS coordinates, speed, heading (privacy-sensitive)
> - **Vehicle telemetry**: Diagnostic data, fault codes, battery status (sent to OEM cloud)
> - **User personal data**: Contacts list, call history, paired mobile device IDs (privacy-sensitive)
> - **Cryptographic keys**: TLS certificates for OTA server authentication, Bluetooth pairing keys
> - **Firmware images**: OTA software updates for TCU and other ECUs
> - **Emergency call (eCall) data**: Crash sensor data, vehicle location (safety-critical, legally required)

**Q7: What external interfaces does the system have?**
> External interfaces:
> - **Cellular (LTE/5G)**: Connects to OEM backend cloud services, emergency services for eCall
> - **Bluetooth 5.0**: Pairs with user's mobile phone for hands-free calling
> - **Wi-Fi 802.11ac**: Provides in-vehicle hotspot for passenger devices
> - **GPS/GNSS antenna**: Receives satellite signals for location
>
> Physical interface: The TCU has an internal service port (USB) accessible only by removing interior panels - used during manufacturing and authorized service.

**Q8: What communication protocols are used?**
> In-vehicle: Ethernet (100BASE-T1 automotive Ethernet) to Central Gateway
> External wireless:
> - Cellular: LTE/5G with TLS 1.3 for OEM backend, unencrypted for eCall per EU regulations
> - Bluetooth: Bluetooth 5.0 with LE Secure Connections pairing
> - Wi-Fi: WPA3 encryption for the in-vehicle hotspot
>
> Application layer: HTTPS (REST API) for OTA updates, proprietary protocol over TLS for telemetry upload.

### Security and Safety Context

**Q9: Which assets are most critical from a safety perspective?**
> The eCall functionality is safety-critical and legally mandated in the EU. If the TCU cannot send an emergency call after a crash, this could delay rescue and potentially cost lives. The OTA update functionality is also safety-relevant because it's used to deploy safety-critical software patches to other ECUs (e.g., brake system updates).

**Q10: Which assets are most critical from a security perspective?**
> Most critical:
> - **Cellular modem**: This is the primary attack surface - it's exposed to the internet 24/7
> - **Cryptographic key storage**: If keys are compromised, an attacker could push malicious OTA updates
> - **OTA update mechanism**: If tampered with, attacker could install malware on safety-critical ECUs
> - **Bluetooth interface**: Nearby attackers could attempt pairing or exploit vulnerabilities
>
> The TCU is the bridge between the outside world and the internal vehicle network, making it a high-value target.

**Q11: What security mechanisms are currently in place?**
> - **Secure boot**: TCU verifies firmware signature before execution
> - **Hardware Security Module (HSM)**: Stores private keys for OTA authentication
> - **Message Authentication Codes (MAC)**: Used on Ethernet messages to Central Gateway
> - **TLS 1.3**: Encrypts communication with OEM backend
> - **Firewall rules**: Central Gateway filters messages from TCU to safety-critical buses

**Q12: Are there any regulatory or compliance requirements?**
> - **UN R155** (cybersecurity): Applies to the TCU as a connected component
> - **UN R156** (OTA updates): TCU must comply with software update management requirements
> - **EU eCall Regulation**: TCU must reliably send emergency calls
> - **GDPR**: User location and contact data must be protected

---

## Expected Output

Based on the interview above, the asset analysis would produce entries like these in `data/asset_list.md`:

```markdown
# Asset List - Telematics and Connectivity System

**Date**: 2026-03-18  
**Scope**: Telematics Control Unit (TCU) and wireless communication subsystem  
**Total Assets**: 6

---

## Asset Summary by Category

| Category | Count | Examples |
|----------|-------|----------|
| ECU | 1 | Telematics Control Unit |
| Gateway | 0 | - |
| Sensor | 1 | GPS/GNSS Receiver |
| Actuator | 0 | - |
| Communication | 3 | Cellular LTE/5G, Bluetooth, Wi-Fi |
| Data | 1 | Cryptographic Keys and Certificates |
| Interface | 0 | (Could add: Cellular Modem, if treating as interface) |

---

## Asset Catalogue

### AST-ECU-001: Telematics Control Unit (TCU)

**Description**: The Telematics Control Unit (TCU) is a connected ECU that manages all wireless communications between the vehicle and external networks, including cellular (LTE/5G), Wi-Fi, and Bluetooth connections. It handles over-the-air (OTA) software updates for the entire vehicle, remote diagnostics and telemetry upload to the OEM cloud, emergency call (eCall) services in case of a crash, stolen vehicle tracking, and infotainment connectivity features such as hands-free calling and in-vehicle Wi-Fi hotspot. The TCU is a critical gateway between the vehicle's internal Ethernet and CAN networks and the outside world, making it a high-value target for remote cyber attacks and a key component in the vehicle's external attack surface.

**Category**: ECU

**CIA Rating**: C:3 / I:4 / A:3
- Confidentiality (Major): The TCU stores and processes restricted user and vehicle data such as location history, paired-device identifiers, contact metadata, and telemetry records. These data classes are intrinsically privacy-sensitive and require controlled disclosure.
- Integrity (Severe): The TCU mediates OTA updates, remote commands, and authenticated communication toward internal vehicle systems. Its firmware, configuration, and update-validation chain are safety-grade trust anchors and must remain tamper-proof by design.
- Availability (Major): The TCU provides continuously expected connectivity services such as eCall signaling, OTA availability, telemetry upload, and remote service access. These functions are operationally important and require sustained availability, though the vehicle can still retain basic drive capability without them.

**Interfaces**:
- Ethernet backbone (100BASE-T1 to Central Gateway ECU)
- Cellular modem (LTE/5G to OEM backend cloud, emergency services)
- Bluetooth 5.0 controller (to user mobile devices for hands-free calling)
- Wi-Fi 802.11ac module (in-vehicle hotspot for passenger devices)
- GPS/GNSS receiver (location services via external antenna)
- Internal flash storage (firmware, cryptographic keys, user data cache)
- USB service port (internal, requires physical access)

**Related Systems**:
- Depends on: Central Gateway (network routing, firewall), Power Management ECU (12V power supply), GPS Antenna (satellite reception), Cellular Antenna (LTE/5G signal)
- Provides data to: OEM Cloud Backend (telemetry, diagnostics), Emergency Services (eCall), Infotainment System (connectivity status, hands-free audio), Mobile App (remote control commands)
- Security relationship: Authenticates with OTA Update Server using PKI certificates stored in HSM; sends Message Authentication Codes (MAC) to Central Gateway; enforces TLS 1.3 for all cloud communication
- Safety relationship: Provides legally required eCall crash notification; delivers OTA updates that may include safety-critical software patches for brake/steering ECUs

**Evidence & Confidence**:
- Sources: TCU Technical Specification v2.3 (Connectivity Architecture section), Wireless Communication Requirements (Security Controls section), Interview Q6-Q11
- Confidence: High
- Assumptions/Unknowns: OTA signing key rotation interval not explicitly provided in source documents

---

### AST-SNS-001: GPS/GNSS Receiver

**Description**: The GPS/GNSS receiver is a satellite navigation sensor integrated within the Telematics Control Unit hardware. It receives signals from GPS, GLONASS, Galileo, and BeiDou satellite constellations to determine the vehicle's precise geographic location, speed, and heading. This location data is used for eCall emergency services (to report crash location), stolen vehicle tracking, navigation services in the infotainment system, and usage-based insurance programs. The receiver operates continuously whenever the vehicle is powered on and communicates location data to the TCU processor via an internal SPI bus.

**Category**: Sensor

**CIA Rating**: C:3 / I:2 / A:3
- Confidentiality (Major): Location data reveals user's movements, home address, travel patterns, and can be used for surveillance. GDPR classifies location as personal data requiring protection.
- Integrity (Moderate): GNSS position data must be sufficiently trustworthy for location-based services, but the receiver is an input sensor rather than an actuator or control authority. Authenticity concerns are relevant because unauthenticated satellite signals can be spoofed.
- Availability (Major): Accurate location is an important continuously expected input for eCall, tracking, telemetry, and navigation functions. Sustained receiver unavailability materially degrades these location-dependent services.

**Interfaces**:
- GPS/GNSS satellite signals (1.2 GHz and 1.5 GHz bands, receive-only)
- SPI bus to TCU main processor (internal hardware connection)
- External GPS antenna (mounted on vehicle roof)

**Related Systems**:
- Depends on: TCU (power, processing), GPS Antenna (signal reception), Satellite Constellation (signal source)
- Provides data to: TCU (for eCall, tracking, telemetry), Infotainment System (for navigation, map display)
- Security relationship: GPS signals are unauthenticated and can be spoofed; no cryptographic protection
- Safety relationship: Critical for eCall emergency crash location reporting (legally required in EU)

---

### AST-COM-001: Cellular Communication (LTE/5G)

**Description**: The cellular communication channel is a wireless wide-area network (WWAN) connection provided by an integrated LTE/5G modem within the Telematics Control Unit. It establishes a persistent IP connection to the OEM's backend cloud infrastructure over the public cellular network, enabling bidirectional communication for over-the-air (OTA) software updates, remote diagnostics, telemetry upload, stolen vehicle tracking, and remote control commands (e.g., remote door unlock, remote engine start). The cellular link also serves as the transmission path for eCall emergency crash notifications to public safety answering points (PSAP). This communication channel operates 24/7 whenever the vehicle has battery power, even when the ignition is off, and represents the vehicle's primary external attack surface.

**Category**: Communication

**CIA Rating**: C:3 / I:4 / A:4
- Confidentiality (Major): The cellular channel carries restricted telemetry, location, diagnostic, remote-service, and emergency-call data. Even when protected by TLS for backend traffic, the channel's data classes are intrinsically privacy-sensitive.
- Integrity (Severe): The cellular channel transports OTA packages, remote commands, and diagnostic exchanges that must be authentic and protected from manipulation. Its message integrity and endpoint authenticity are safety-grade trust requirements for connected-vehicle operation.
- Availability (Severe): Cellular connectivity is designed as an always-available external communication path for eCall, OTA, telemetry, remote diagnostics, and stolen-vehicle recovery. These connected services require continuous or near-continuous availability by design.

**Interfaces**:
- Cellular modem hardware (integrated in TCU, supports LTE Cat-4 and 5G NR)
- Cellular antenna (external, mounted on vehicle roof or rear window)
- SIM card / eSIM (for cellular network authentication)
- TLS 1.3 encrypted tunnel to OEM cloud backend (IP: managed by cellular carrier NAT)
- Unencrypted eCall connection to PSAP (emergency services, per EU eCall spec)

**Related Systems**:
- Depends on: TCU (modem control, power), Cellular Network Carrier (signal, IP routing), OEM Cloud Backend (application server, OTA repository), PSAP Infrastructure (emergency call centers)
- Provides connectivity to: OTA Update Server, Telemetry Backend, Remote Command Service, Emergency Services
- Security relationship: TLS 1.3 mutual authentication with OEM backend using client certificate stored in TCU HSM; no encryption for eCall (regulatory requirement for PSAP access)
- Safety relationship: Primary transmission path for eCall crash notifications; backup path for downloading safety-critical OTA updates if in-vehicle update fails

---

### AST-COM-002: Bluetooth Communication

**Description**: The Bluetooth wireless communication protocol enables short-range (up to 10 meters) connectivity between the Telematics Control Unit and user mobile devices. It is primarily used for hands-free calling (Bluetooth Hands-Free Profile, HFP) and phone contact list synchronization (Bluetooth Phone Book Access Profile, PBAP). The Bluetooth controller supports Bluetooth 5.0 with LE (Low Energy) Secure Connections pairing to authenticate and encrypt the wireless link. Users initiate pairing via the vehicle's infotainment touchscreen, and the TCU stores paired device identifiers and pairing keys in persistent memory. Bluetooth is an external attack surface since it is discoverable and accessible to nearby attackers in physical proximity to the vehicle.

**Category**: Communication

**CIA Rating**: C:2 / I:2 / A:1
- Confidentiality (Moderate): Bluetooth carries phone contact metadata, pairing identifiers, and sometimes synchronized contact-list data. These data classes have limited but real privacy sensitivity.
- Integrity (Moderate): Bluetooth pairing state, audio routing, and profile data must remain authentic for correct hands-free and device-integration behavior. The channel is operationally important but not safety-grade.
- Availability (Negligible): Loss of Bluetooth only impacts convenience (hands-free calling). Vehicle remains fully drivable and safe without Bluetooth functionality.

**Interfaces**:
- Bluetooth 5.0 radio (2.4 GHz ISM band, integrated in TCU hardware)
- Bluetooth antenna (internal or shared with Wi-Fi)
- Pairing with user mobile devices (smartphones, typically iOS or Android)
- Audio path to Infotainment System (for hands-free call audio)
- Contact list synchronization with Infotainment System

**Related Systems**:
- Depends on: TCU (Bluetooth controller, power), Infotainment System (user interface for pairing, audio routing)
- Provides connectivity to: User Mobile Devices (phones, for hands-free calling)
- Security relationship: LE Secure Connections pairing with numeric comparison or passkey entry; AES-128 encryption of Bluetooth link; pairing keys stored in TCU flash memory (not HSM)
- Safety relationship: No direct safety impact; purely a convenience feature

---

### AST-COM-003: Wi-Fi Communication (In-Vehicle Hotspot)

**Description**: The Wi-Fi communication capability provides a wireless local area network (WLAN) hotspot inside the vehicle, allowing passengers to connect their devices (laptops, tablets, smartphones) to the internet via the TCU's cellular connection. The TCU acts as a Wi-Fi access point (AP) using the 802.11ac standard on 2.4 GHz and 5 GHz bands, with WPA3 encryption for client authentication and traffic protection. The Wi-Fi network is isolated from the vehicle's internal Ethernet and CAN networks - passenger devices have internet access only, not access to vehicle systems. Up to 8 client devices can connect simultaneously, and the Wi-Fi SSID and password are displayed on the infotainment screen or set by the user.

**Category**: Communication

**CIA Rating**: C:1 / I:1 / A:1
- Confidentiality (Negligible): Wi-Fi traffic is isolated from vehicle systems. Passenger internet traffic is not vehicle data, so confidentiality impact on the vehicle is negligible. (Passenger privacy is a separate concern.)
- Integrity (Negligible): The Wi-Fi network is strictly segregated from vehicle controls. Even if an attacker compromises the Wi-Fi, they cannot modify vehicle functions or safety-critical data.
- Availability (Negligible): Loss of in-vehicle Wi-Fi hotspot is purely a convenience issue for passengers. Vehicle operation and safety are unaffected.

**Interfaces**:
- Wi-Fi 802.11ac radio (2.4 GHz and 5 GHz, integrated in TCU)
- Wi-Fi antenna (internal or shared with Bluetooth)
- Cellular modem (for internet backhaul via LTE/5G)
- Client devices (passenger laptops, tablets, phones - up to 8 concurrent)

**Related Systems**:
- Depends on: TCU (Wi-Fi controller, power), Cellular Connection (internet backhaul)
- Provides connectivity to: Passenger Devices (internet access only, no vehicle network access)
- Security relationship: WPA3 encryption with user-configurable passphrase; network isolation ensures no routing to vehicle Ethernet/CAN
- Safety relationship: No safety impact; purely a passenger convenience feature

---

### AST-DAT-001: Cryptographic Keys and Certificates

**Description**: The cryptographic key material stored within the Telematics Control Unit is a critical security asset that enables authentication, encryption, and integrity protection for all external communications. This includes: (1) a private key and X.509 certificate for TLS mutual authentication with the OEM's OTA update server, (2) symmetric AES keys for encrypting stored user data, (3) Bluetooth pairing keys for connected mobile devices, and (4) Wi-Fi WPA3 pre-shared key. The TLS private key is stored in a dedicated Hardware Security Module (HSM) chip within the TCU to prevent extraction even if the TCU's main processor is compromised. Other keys are stored in encrypted flash memory. These keys are provisioned during vehicle manufacturing and are unique per vehicle (per-device keys, not shared across fleet).

**Category**: Data

**CIA Rating**: C:4 / I:4 / A:3
- Confidentiality (Severe): TLS private keys, OEM CA certificates, OTA signing roots, and user-data encryption keys are secret credential material by nature. They require the highest confidentiality class because their value depends on non-disclosure.
- Integrity (Severe): Cryptographic keys are trust anchors for backend authentication, encrypted storage, pairing, and update validation. Their values and provenance must remain tamper-proof by design.
- Availability (Major): The key material is required for authenticated backend communication, remote services, encrypted data access, and update validation. Loss or corruption requires re-provisioning and materially disrupts connected services.

**Interfaces**:
- Hardware Security Module (HSM) chip (isolated crypto processor within TCU hardware)
- Encrypted flash memory (for non-HSM keys)
- TLS 1.3 stack in TCU firmware (uses keys for authentication/encryption)
- Bluetooth and Wi-Fi stacks (use pairing keys)

**Related Systems**:
- Depends on: TCU Hardware (HSM chip, secure storage), Manufacturing Process (initial key provisioning), OEM PKI Infrastructure (certificate authority for TLS certs)
- Provides security to: Cellular Communication (TLS authentication), OTA Update Mechanism (code signing verification), Bluetooth/Wi-Fi (pairing/encryption)
- Security relationship: HSM enforces key non-exportability; keys are never transmitted outside TCU except during initial provisioning; OEM CA root certificate is pre-installed in TCU firmware
- Safety relationship: Integrity of OTA updates protected by these keys directly impacts safety, since OTA can update brake/steering ECU software

**Evidence & Confidence**:
- Sources: TCU Technical Specification v2.3 (HSM and key storage), Wireless Communication Requirements (TLS and OTA requirements), Interview Q10-Q11
- Confidence: Medium
- Assumptions/Unknowns: HSM vendor model and certification level are not specified in the available references

---

## Notes

**Assumptions**:
- This example assumes a modern connected vehicle with full telematics capabilities
- eCall is required by EU regulation (Regulation 2015/758)
- OTA update functionality follows UN R156 requirements
- Reference documents in `input/` would provide technical details; this example simulates user knowledge

**Open Questions** (in real scenario, these would be documented):
- What is the exact model/vendor of the HSM chip? (Affects security assessment)
- Are there any known vulnerabilities in the cellular modem firmware? (Requires vendor CVE check)
- What is the backup mechanism if cellular connection fails during an emergency? (eCall fallback)

**Next Steps**:
- This asset list would feed into threat scenario identification (tara-maker skill)
- Each asset would be analyzed for potential threats (e.g., AST-COM-001 Cellular → threat of fake base station attack)
```

---

## Lessons Learned

This example demonstrates:
- How to conduct the user interview systematically using the 12 guided questions
- How to translate user answers into structured asset entries with all 7 required fields
- How to document Evidence & Confidence for traceable, non-fabricated asset entries
- How to assess CIA ratings based on impact analysis (safety, privacy, regulatory compliance)
- How to map interfaces and relationships between assets
- How asset categories align with system architecture (ECU, Sensor, Communication, Data)

**Common patterns**:
- **Wireless interfaces** (Bluetooth, Wi-Fi, Cellular) are always Communication assets with external attack surface
- **ECUs with external connectivity** have high Integrity and Availability ratings due to safety/security criticality
- **Cryptographic keys** are always Data assets with Severe (4) CIA ratings
- **Sensors** used for safety functions (GPS for eCall) have Major+ Availability ratings
