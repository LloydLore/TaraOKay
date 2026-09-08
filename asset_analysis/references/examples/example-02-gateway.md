# Example 02: Central Gateway ECU Analysis

This example demonstrates the asset identification workflow for a Central Gateway ECU in a vehicle's network architecture.

---

## Input Scenario

**System**: Vehicle Network Architecture  
**Scope**: Central Gateway ECU and interconnected network segments  
**Reference Documents**: (Simulated - in real scenario, these would be in `input/` directory)
- Network Topology Diagram
- Central Gateway Functional Specification
- Network Security Requirements

**User's Goal**: Identify assets related to the Central Gateway to understand the vehicle's network security architecture for ISO 21434 TARA.

---

## Interview Answers (Simulated User Input)

### System Overview

**Q1: What vehicle system or component are we analyzing?**
> We're analyzing the Central Gateway ECU, which is the main network router and firewall in our vehicle architecture. It connects five different network segments: the powertrain CAN-FD bus, the chassis CAN bus, the body/comfort LIN network, the infotainment Ethernet backbone, and the ADAS (Advanced Driver Assistance Systems) FlexRay network. The scope includes the Gateway hardware, the network segments it manages, and the routing/filtering rules it enforces.

**Q2: What reference documents or specifications are available?**
> We have the network topology diagram showing all five network segments and which ECUs are on each segment, the Central Gateway functional spec (version 4.1), and the network security requirements document that defines the firewall rules and message filtering policies.

### Components and Architecture

**Q3: What are the main electronic control units (ECUs) in this system?**
> The Central Gateway is the main ECU in scope. It's a safety-related component because it routes messages from ADAS sensors to the brake ECU, and it enforces firewall rules that protect safety-critical networks from non-critical networks. The Gateway has five separate network controllers (two CAN-FD, one LIN, one Ethernet, one FlexRay) and a main processor running an AUTOSAR-based embedded OS.

**Q4: What network architecture connects these components?**
> Five network segments connect to the Gateway:
> 1. **Powertrain CAN-FD** (500 kbps → 2 Mbps): Engine ECU, Transmission ECU, Battery Management System
> 2. **Chassis CAN** (500 kbps): Brake ECU, ABS, Electronic Stability Control (ESC), Steering ECU
> 3. **Body/Comfort LIN** (19.2 kbps): Door modules, window motors, seat controllers, lighting
> 4. **Infotainment Ethernet** (100BASE-T1): Infotainment Head Unit, Telematics Control Unit, rear-seat displays
> 5. **ADAS FlexRay** (10 Mbps): Camera ECUs, radar sensors, lidar, ADAS domain controller
>
> The Gateway routes messages between these segments and enforces firewall rules to block unauthorized messages.

**Q5: What sensors and actuators are present?**
> The Gateway itself has no sensors or actuators - it's a pure network device. However, it routes messages from ADAS sensors (cameras, radar) to actuators (brakes, steering), so it's in the critical path for autonomous emergency braking and lane-keeping assist.

### Data Flows and Interfaces

**Q6: What data flows through this system?**
> The Gateway routes several types of messages:
> - **Safety-critical**: ADAS → Brake ECU (emergency braking commands), Camera → ADAS Controller (object detection)
> - **Powertrain**: Engine → Transmission (torque requests), Battery → Engine (power limits)
> - **Telemetry**: All ECUs → Telematics (diagnostic data upload to cloud)
> - **Infotainment**: Telematics → Infotainment (connectivity status), Powertrain → Infotainment (vehicle speed for display)
> - **Body/Comfort**: User commands from infotainment to door locks, windows, climate control
>
> The Gateway also logs all routed messages to internal flash storage for diagnostics.

**Q7: What external interfaces does the system have?**
> The Gateway has no direct external interfaces (no wireless, no physical ports accessible to users). However, it indirectly connects external interfaces to internal networks:
> - The Telematics Control Unit (on Ethernet segment) has cellular/Bluetooth/Wi-Fi
> - The Infotainment (on Ethernet segment) has USB ports accessible in the cabin
>
> So the Gateway is the chokepoint between external attack surface (via Telematics/Infotainment) and safety-critical networks (Chassis CAN, ADAS FlexRay).

**Q8: What communication protocols are used?**
> - **CAN-FD**: Powertrain network (Classical CAN + Flexible Data-Rate)
> - **CAN 2.0B**: Chassis network (traditional 500 kbps CAN)
> - **LIN 2.1**: Body/Comfort network (low-speed, single-master)
> - **FlexRay**: ADAS network (deterministic, time-triggered)
> - **Ethernet (100BASE-T1)**: Infotainment network (switched Ethernet with VLANs)
>
> The Gateway translates between these protocols and enforces message filtering at each boundary.

### Security and Safety Context

**Q9: Which assets are most critical from a safety perspective?**
> The Central Gateway is safety-critical because:
> 1. It routes emergency braking commands from ADAS to the Brake ECU - if this routing fails or is delayed, autonomous emergency braking (AEB) could fail, leading to crashes.
> 2. It enforces firewall rules that prevent the Infotainment (which has USB ports and could be compromised) from sending unauthorized commands to the Brake or Steering ECUs.
> 3. ASIL-B rated (Automotive Safety Integrity Level B per ISO 26262) for its message routing function.

**Q10: Which assets are most critical from a security perspective?**
> The Gateway is the single most critical security asset in the vehicle network. If an attacker compromises the Gateway, they can:
> - Bypass all firewall rules and send malicious messages to any ECU
> - Eavesdrop on all vehicle communications (engine data, brake data, location from GPS)
> - Disable safety functions by blocking critical messages (e.g., drop AEB commands)
> - Pivot from a compromised non-critical ECU (e.g., Infotainment) to safety-critical ECUs
>
> The Gateway is also a single point of failure - if it crashes or is DoS'd, the entire vehicle network becomes partitioned.

**Q11: What security mechanisms are currently in place?**
> - **Firewall rules**: The Gateway maintains a whitelist of allowed CAN IDs and Ethernet MAC addresses for each network segment. Messages not on the whitelist are dropped.
> - **Message Authentication Codes (MACs)**: Critical messages (e.g., ADAS → Brake) include a MAC computed using a shared symmetric key. The Gateway verifies MACs before routing.
> - **Secure boot**: The Gateway verifies a digital signature on its firmware before booting.
> - **Network segmentation**: Safety-critical networks (Chassis CAN, ADAS FlexRay) are physically separated from non-critical networks (Infotainment Ethernet). The Gateway is the only connection point.
> - **Logging**: All routed messages are logged with timestamps for forensic analysis.

**Q12: Are there any regulatory or compliance requirements?**
> - **UN R155**: The Gateway's firewall function is required to comply with UN R155 cybersecurity regulation.
> - **ISO 26262 ASIL-B**: The message routing function is safety-rated and must meet functional safety requirements.
> - **ISO 21434**: The Gateway is a critical component in the vehicle's cybersecurity architecture and must undergo TARA.

---

## Expected Output

Based on the interview above, the asset analysis would produce entries like these in `data/asset_list.md`:

```markdown
# Asset List - Central Gateway and Vehicle Network Architecture

**Date**: 2026-03-18  
**Scope**: Central Gateway ECU and five interconnected network segments  
**Total Assets**: 7

---

## Asset Summary by Category

| Category | Count | Examples |
|----------|-------|----------|
| ECU | 0 | - |
| Gateway | 1 | Central Gateway |
| Sensor | 0 | - |
| Actuator | 0 | - |
| Communication | 5 | Powertrain CAN-FD, Chassis CAN, Body LIN, Infotainment Ethernet, ADAS FlexRay |
| Data | 1 | Firewall Rules and Routing Tables |
| Interface | 0 | - |

---

## Asset Catalogue

### AST-GW-002: Central Gateway ECU

**Description**: The Central Gateway ECU is the primary network router and security firewall for the vehicle's electrical/electronic architecture. It interconnects five heterogeneous network segments - Powertrain CAN-FD, Chassis CAN, Body/Comfort LIN, Infotainment Ethernet, and ADAS FlexRay - and routes messages between them according to configurable routing tables. The Gateway enforces network security policies by filtering messages based on whitelists of allowed CAN IDs, Ethernet MAC addresses, and FlexRay slots, effectively acting as an in-vehicle firewall. It also performs protocol translation (e.g., CAN to Ethernet) and verifies Message Authentication Codes (MACs) on safety-critical messages. The Gateway is rated ASIL-B (Automotive Safety Integrity Level B) under ISO 26262 for its role in routing autonomous emergency braking commands from ADAS sensors to the Brake ECU. As the central chokepoint between external attack surfaces (Telematics, Infotainment with USB ports) and safety-critical networks (brakes, steering), the Gateway is the single most critical cybersecurity asset in the vehicle.

**Category**: Gateway

**CIA Rating**: C:4 / I:4 / A:4
- Confidentiality (Severe): The Gateway can observe cross-domain vehicle traffic, including safety-related messages, powertrain state, diagnostic records, and user-related telemetry routed from connected domains. This breadth of visibility makes its data exposure class highly sensitive by nature.
- Integrity (Severe): The Gateway enforces firewall rules and routes messages between safety-critical and non-safety networks. Its firmware, routing tables, and filtering policy are safety-grade trust anchors and must remain tamper-proof by design.
- Availability (Severe): The Gateway is a continuously required network coordination point for multiple in-vehicle domains. Its routing and isolation functions must remain available for normal cross-domain communication and network segmentation.

**Interfaces**:
- Powertrain CAN-FD bus (500 kbps/2 Mbps, connection to Engine ECU, Transmission ECU, Battery Management System)
- Chassis CAN bus (500 kbps, connection to Brake ECU, ABS, ESC, Steering ECU)
- Body/Comfort LIN network (19.2 kbps, connection to Door Modules, Window Motors, Seat Controllers, Lighting)
- Infotainment Ethernet backbone (100BASE-T1, connection to Infotainment Head Unit, Telematics Control Unit, Rear-Seat Displays)
- ADAS FlexRay network (10 Mbps, connection to Camera ECUs, Radar Sensors, Lidar, ADAS Domain Controller)
- Internal flash storage (for firmware, routing tables, firewall rules, message logs)
- Power supply from vehicle 12V battery via Power Management ECU

**Related Systems**:
- Depends on: Power Management ECU (12V power supply), Network Segments (physical buses must be operational)
- Provides routing to: All ECUs in the vehicle (Engine, Brake, Steering, Infotainment, Telematics, ADAS, Body modules)
- Security relationship: Enforces firewall rules (whitelist-based message filtering), verifies Message Authentication Codes (MACs) on safety-critical messages, isolates Infotainment/Telematics networks from Chassis/ADAS networks, logs all routed messages for forensic analysis
- Safety relationship: Routes autonomous emergency braking commands from ADAS to Brake ECU (ASIL-B function), prevents non-safety networks from disrupting safety-critical ECUs

**Evidence & Confidence**:
- Sources: Network Topology Diagram, Central Gateway Functional Specification v4.1, Network Security Requirements, Interview Q4-Q11
- Confidence: High
- Assumptions/Unknowns: Gateway fail-safe behavior under flash corruption not explicitly specified

---

### AST-COM-004: Powertrain CAN-FD Bus

**Description**: The Powertrain CAN-FD (Controller Area Network with Flexible Data-Rate) bus is a high-speed in-vehicle network segment that connects the Engine Control Unit (ECU), Transmission ECU, Battery Management System, and Central Gateway. It operates at two data rates: Classical CAN at 500 kbps for arbitration and CAN-FD at 2 Mbps for payload transmission, allowing larger message payloads and faster data transfer compared to traditional CAN. The Powertrain bus carries time-critical messages for engine control (fuel injection timing, ignition timing), torque coordination between engine and transmission, battery state-of-charge and power limits, and diagnostic requests. All messages are broadcast (multi-master bus), and there is no built-in encryption or authentication at the CAN protocol level, so message integrity relies on higher-layer MACs or physical network segmentation via the Gateway firewall.

**Category**: Communication

**CIA Rating**: C:2 / I:4 / A:4
- Confidentiality (Moderate): Powertrain CAN messages include vehicle speed, engine RPM, battery charge level, fuel-consumption, and driving-behavior signals. These are internal operational data with limited privacy sensitivity compared with location history or credentials.
- Integrity (Severe): The Powertrain CAN bus carries powertrain coordination messages such as throttle, fuel, torque, and battery-management signals. These are safety-grade operational signals whose authenticity and ordering must be preserved.
- Availability (Severe): The Powertrain CAN bus is a continuously required communication channel for propulsion and energy-management coordination. Its availability is intrinsic to normal powertrain operation.

**Interfaces**:
- Central Gateway (CAN-FD transceiver, routes messages to/from other network segments)
- Engine Control Unit (ECU on Powertrain bus)
- Transmission Control Unit (ECU on Powertrain bus)
- Battery Management System (ECU on Powertrain bus, for electric/hybrid vehicles)
- Physical CAN bus wiring (twisted-pair cables, CAN High and CAN Low lines)

**Related Systems**:
- Depends on: Central Gateway (network access), Physical CAN Transceivers (bus drivers in each ECU), 12V Power (for transceiver power)
- Provides communication to: Engine ECU, Transmission ECU, Battery Management System
- Security relationship: No encryption or authentication at CAN protocol level; relies on Gateway firewall to prevent injection from non-Powertrain networks; MACs may be used at application layer for critical messages
- Safety relationship: Carries safety-relevant messages for powertrain coordination; bus failure could disable vehicle propulsion

---

### AST-COM-005: Chassis CAN Bus

**Description**: The Chassis CAN bus is a traditional CAN 2.0B network segment operating at 500 kbps that connects safety-critical vehicle dynamics and braking systems including the Brake ECU, Anti-lock Braking System (ABS), Electronic Stability Control (ESC), Steering ECU, and Central Gateway. This bus carries real-time commands and sensor data for active safety functions such as autonomous emergency braking (AEB), electronic stability control (preventing skids), anti-lock braking (preventing wheel lockup), and electric power steering assistance. The Chassis CAN bus is physically isolated from non-safety networks (Infotainment, Body/Comfort) and can only be accessed via the Central Gateway, which enforces strict firewall rules to prevent unauthorized messages from reaching brake or steering actuators. Due to the safety-critical nature of the systems on this bus, any compromise of message integrity or availability could lead to loss of vehicle control, crashes, injuries, or fatalities.

**Category**: Communication

**CIA Rating**: C:2 / I:4 / A:4
- Confidentiality (Moderate): Chassis CAN messages include vehicle speed, steering angle, brake pressure, wheel speeds, and yaw-rate data. These operational signals have limited privacy sensitivity and are primarily internal vehicle data.
- Integrity (Severe): The Chassis CAN bus carries braking, steering, ABS, and stability-control messages. These are safety-grade vehicle-dynamics signals whose authenticity and ordering must be preserved end-to-end.
- Availability (Severe): The Chassis CAN bus is a continuously required communication channel for active safety and vehicle-dynamics coordination. Its availability is intrinsic to normal chassis-domain operation.

**Interfaces**:
- Central Gateway (CAN transceiver, routes messages to/from other network segments, enforces firewall rules)
- Brake ECU (controls hydraulic brake pressure, receives AEB commands from ADAS via Gateway)
- Anti-lock Braking System (ABS) (prevents wheel lockup during hard braking)
- Electronic Stability Control (ESC) (prevents skidding by applying individual wheel braking)
- Steering ECU (provides electric power steering assistance)
- Physical CAN bus wiring (twisted-pair cables)

**Related Systems**:
- Depends on: Central Gateway (network access, firewall protection), Physical CAN Transceivers, 12V Power
- Provides communication to: Brake ECU, ABS, ESC, Steering ECU
- Security relationship: Isolated from non-safety networks by Gateway firewall; critical messages (e.g., AEB commands from ADAS) use Message Authentication Codes (MACs); no direct access from Infotainment or Telematics networks
- Safety relationship: Carries safety-critical messages for braking and steering; ASIL-D rated functions (AEB, ESC) rely on this bus; message integrity and availability are essential for safe vehicle operation

---

### AST-COM-006: Body/Comfort LIN Network

**Description**: The Body/Comfort LIN (Local Interconnect Network) is a low-speed (19.2 kbps), low-cost serial network segment that connects non-critical body electronics such as door lock actuators, window motor controllers, seat adjustment motors, interior lighting modules, and climate control actuators to the Central Gateway. LIN is a single-master bus where the Gateway acts as the master node, polling slave nodes (door modules, etc.) for status and sending commands. The Body/Comfort network handles user convenience functions such as locking/unlocking doors, raising/lowering windows, adjusting seats and mirrors, and controlling interior lights. These functions are not safety-critical (vehicle can drive safely without them), but they do interact with user commands from the Infotainment system, which could be an attack vector if the Infotainment is compromised via USB or other external interfaces.

**Category**: Communication

**CIA Rating**: C:1 / I:2 / A:1
- Confidentiality (Negligible): Body/Comfort LIN messages contain only door lock status, window positions, seat positions, and light states. This information is not privacy-sensitive and has negligible value to attackers.
- Integrity (Moderate): Body/Comfort LIN carries convenience-control commands and status signals for doors, windows, seats, lighting, and climate actuators. These signals require operational integrity but are not safety-grade.
- Availability (Negligible): Body/Comfort LIN supports convenience features whose continuous availability is not required for core vehicle operation. Temporary or sustained outage is tolerable from the asset's intrinsic time-criticality perspective.

**Interfaces**:
- Central Gateway (LIN master node, sends commands and polls slave nodes)
- Door Lock Modules (LIN slaves, control door lock actuators)
- Window Motor Controllers (LIN slaves, control window up/down)
- Seat Adjustment Controllers (LIN slaves, control seat motors)
- Interior Lighting Modules (LIN slaves, control cabin lights, ambient lighting)
- Climate Control Actuators (LIN slaves, control HVAC flaps and fans)
- Physical LIN bus wiring (single-wire plus ground)

**Related Systems**:
- Depends on: Central Gateway (LIN master function), 12V Power
- Provides communication to: Door modules, Window motors, Seat controllers, Lighting, Climate actuators
- Security relationship: Low-priority network; Gateway firewall prevents LIN messages from routing to safety-critical networks (Chassis, ADAS); user commands from Infotainment are filtered by Gateway before reaching LIN
- Safety relationship: No direct safety impact; purely convenience/comfort functions

---

### AST-COM-007: Infotainment Ethernet Backbone

**Description**: The Infotainment Ethernet backbone is a switched 100BASE-T1 automotive Ethernet network segment that connects the Infotainment Head Unit, Telematics Control Unit (TCU), rear-seat entertainment displays, and Central Gateway. This Ethernet segment uses VLANs (Virtual LANs) to logically separate traffic types (e.g., video streaming for rear displays, telemetry upload to cloud, user app data). Unlike CAN or LIN, Ethernet supports TCP/IP protocols, enabling internet connectivity via the TCU's cellular modem, software updates, and multimedia streaming. The Infotainment Ethernet segment is the highest-risk network from a cybersecurity perspective because it directly connects to external attack surfaces: the TCU has cellular/Bluetooth/Wi-Fi interfaces, and the Infotainment has USB ports and user-installable apps. The Central Gateway enforces strict firewall rules to prevent messages from the Infotainment Ethernet from reaching safety-critical networks (Chassis CAN, ADAS FlexRay) without authorization.

**Category**: Communication

**CIA Rating**: C:3 / I:3 / A:2
- Confidentiality (Major): The Infotainment Ethernet carries restricted user and vehicle data such as contacts, call history, location-derived data, multimedia traffic, and telemetry. The data class is privacy-sensitive by nature.
- Integrity (Major): The Infotainment Ethernet carries user-facing application traffic, telemetry, update-support traffic, and gateway-routed messages. Its data should be authentic and correctly segmented, but the network itself is not the final authority for safety-grade vehicle control.
- Availability (Moderate): The Infotainment Ethernet supports connectivity, media, navigation, rear-seat display, and update-support paths. These services are important but not continuously required for basic vehicle operation.

**Interfaces**:
- Central Gateway (Ethernet switch port, routes packets to/from other network segments, enforces firewall rules)
- Infotainment Head Unit (multimedia, navigation, user interface)
- Telematics Control Unit (TCU) (cellular/Bluetooth/Wi-Fi connectivity, OTA updates, cloud telemetry)
- Rear-Seat Displays (video streaming from Infotainment)
- Physical Ethernet wiring (100BASE-T1 twisted-pair cables)

**Related Systems**:
- Depends on: Central Gateway (Ethernet routing, firewall), Telematics Control Unit (internet backhaul), 12V Power
- Provides communication to: Infotainment Head Unit, TCU, Rear-Seat Displays
- Security relationship: Highest-risk network segment (external attack surface via TCU wireless and Infotainment USB); Gateway enforces firewall to prevent Infotainment/TCU from sending unauthorized messages to Chassis/ADAS networks; VLANs logically segment traffic; TLS encryption used for TCU-to-cloud communication
- Safety relationship: No direct safety impact (purely infotainment/connectivity), but serves as OTA update path for safety-critical software patches to other ECUs

---

### AST-COM-008: ADAS FlexRay Network

**Description**: The ADAS FlexRay network is a deterministic, time-triggered, high-speed (10 Mbps) communication bus that connects Advanced Driver Assistance Systems (ADAS) components including camera ECUs, radar sensors, lidar sensors, the ADAS Domain Controller, and the Central Gateway. FlexRay is designed for safety-critical, real-time applications where message timing must be guaranteed. The ADAS network carries time-sensitive sensor data (camera images, radar point clouds, lidar scans) to the ADAS controller for processing, and the controller outputs safety-critical commands (e.g., autonomous emergency braking requests) that are routed via the Gateway to the Brake ECU on the Chassis CAN bus. The ADAS FlexRay network is isolated from non-safety networks and can only communicate with other segments (e.g., Chassis CAN for brake commands) through the Gateway's controlled routing and firewall. ADAS functions such as Automatic Emergency Braking (AEB) and Lane Keeping Assist (LKA) are ASIL-B or ASIL-D rated under ISO 26262.

**Category**: Communication

**CIA Rating**: C:2 / I:4 / A:4
- Confidentiality (Moderate): ADAS FlexRay messages include camera image data (potentially capturing faces of pedestrians or license plates), radar/lidar point clouds (revealing surroundings), and vehicle trajectory predictions. While not directly user-identifiable data, privacy concerns exist. Confidentiality impact is moderate since the network is isolated and requires Gateway compromise to eavesdrop.
- Integrity (Severe): The ADAS FlexRay bus carries object-detection, trajectory, timing, and control-request messages. These are safety-grade ADAS signals whose authenticity, ordering, and timing must be guaranteed.
- Availability (Severe): The ADAS FlexRay network is a continuously required deterministic communication channel for ADAS sensing and control coordination. Its availability is intrinsic to the ADAS domain's real-time function.

**Interfaces**:
- Central Gateway (FlexRay communication controller, routes ADAS commands to Chassis CAN, enforces firewall rules)
- Camera ECUs (front camera, surround-view cameras, send processed image data)
- Radar Sensors (front long-range radar, corner radars, send object detection data)
- Lidar Sensors (if equipped, send 3D point cloud data)
- ADAS Domain Controller (processes sensor data, generates AEB/LKA commands)
- Physical FlexRay bus wiring (dual-channel twisted-pair for redundancy)

**Related Systems**:
- Depends on: Central Gateway (FlexRay routing, isolation from non-safety networks), ADAS Sensors (camera, radar, lidar), 12V Power
- Provides communication to: Camera ECUs, Radar Sensors, Lidar, ADAS Controller
- Security relationship: Isolated from Infotainment/Telematics by Gateway firewall; critical AEB commands use Message Authentication Codes (MACs) verified by Gateway before routing to Brake ECU; no direct external access
- Safety relationship: Carries ASIL-B/ASIL-D rated safety functions (AEB, LKA); message integrity and availability are critical for safe operation of automated driving features

---

### AST-DAT-002: Firewall Rules and Routing Tables

**Description**: The firewall rules and routing tables are critical configuration data stored in the Central Gateway ECU's non-volatile memory (flash storage). These data structures define which messages are allowed to traverse between the five network segments (Powertrain CAN-FD, Chassis CAN, Body/Comfort LIN, Infotainment Ethernet, ADAS FlexRay) and which are blocked. The firewall rules are implemented as whitelists of allowed CAN IDs, Ethernet MAC addresses, and FlexRay slots for each network-to-network boundary. For example, a rule might allow the ADAS controller to send brake commands (CAN ID 0x123) from FlexRay to Chassis CAN via the Gateway, but block all other FlexRay-to-Chassis traffic. The routing tables specify how messages are translated and forwarded between different protocols (e.g., how a CAN message from Powertrain is encapsulated in Ethernet for transmission to Infotainment for display). These rules are configured during vehicle manufacturing and updated via OTA (Over-The-Air) software updates signed by the OEM. Unauthorized modification of firewall rules would allow an attacker to bypass all network segmentation controls, enabling attacks from low-security networks (Infotainment) to high-security networks (Brakes, Steering).

**Category**: Data

**CIA Rating**: C:3 / I:4 / A:4
- Confidentiality (Major): The firewall rules reveal security-boundary design, allowed message identifiers, routing policy, and segmentation assumptions. This configuration data is restricted architecture information by nature.
- Integrity (Severe): The firewall ruleset is the Gateway's primary security-control configuration. It must remain tamper-proof because its correctness defines the network segmentation boundary.
- Availability (Severe): The firewall rules and routing tables are required at runtime for deterministic message filtering and forwarding. They are continuously required configuration data for the Gateway's normal operation.

**Interfaces**:
- Central Gateway non-volatile flash memory (stores firewall rules and routing tables)
- Gateway firmware (reads rules at boot, enforces them during message routing)
- OTA Update Mechanism (delivers signed updates to firewall rules via Telematics → Gateway path)
- Manufacturing/Diagnostic Tool (initial provisioning of rules during vehicle production)

**Related Systems**:
- Depends on: Central Gateway Hardware (flash storage), OEM Firewall Configuration Process (defines allowed rules), OTA Update Server (signs and delivers rule updates)
- Provides security to: All network segments (Powertrain, Chassis, Body, Infotainment, ADAS) by enforcing isolation boundaries
- Security relationship: Rules are digitally signed by OEM private key; Gateway verifies signature before applying rule updates; rules are write-protected (cannot be modified at runtime without signed update)
- Safety relationship: Firewall rules protect safety-critical networks (Chassis, ADAS) from unauthorized access, ensuring that only authenticated, safety-rated ECUs can command brakes/steering; rule integrity is essential for functional safety

**Evidence & Confidence**:
- Sources: Network Security Requirements (firewall policy and signing flow), Central Gateway Functional Specification v4.1 (routing table behavior), Interview Q10-Q11
- Confidence: Medium
- Assumptions/Unknowns: Cryptographic algorithm suite and key rotation cadence for rule signing are not specified in available references

---

## Notes

**Assumptions**:
- This example assumes a modern vehicle with multiple network technologies (CAN, Ethernet, LIN, FlexRay)
- The Central Gateway is a single ECU, not distributed gateway architecture
- Firewall rules are enforced in hardware/firmware at the Gateway (not software on a general-purpose OS)

**Open Questions** (in real scenario, these would be documented):
- What is the Gateway's behavior if flash memory corruption is detected? (Fail-safe mode?)
- Are firewall rules redundantly stored (e.g., dual flash banks) for fault tolerance?
- How are firewall rule updates authenticated? (Specific cryptographic algorithm and key management)

**Next Steps**:
- This asset list would feed into threat scenario identification for the Gateway and network segments
- Threat scenarios would include: Gateway firmware exploit, firewall rule tampering, bus-off DoS attacks on CAN segments, ADAS sensor spoofing via FlexRay injection, etc.

---

## Lessons Learned

This example demonstrates:
- How to handle a **Gateway ECU** that connects multiple network segments
- How to categorize **network segments** (CAN, Ethernet, LIN, FlexRay) as **Communication** assets
- How to assess CIA ratings for **network assets** based on the criticality of the systems they connect
- How to document **security mechanisms** (firewall rules, MACs) as separate **Data** assets
- How to document **Evidence & Confidence** to keep asset entries traceable and non-fabricated
- How multiple assets relate to each other in a networked system (Gateway + 5 networks + firewall rules)

**Key insights**:
- **Gateways** have severe CIA ratings (4/4/4) because they are single points of failure and control network isolation
- **Safety-critical networks** (Chassis, ADAS) have Integrity=4 and Availability=4 regardless of confidentiality
- **Convenience networks** (Body/Comfort) have low CIA ratings (1/2/1) even though they connect to user commands
- **Firewall rules** are Data assets with CIA ratings as critical as the Gateway itself (integrity compromise bypasses all network security)
