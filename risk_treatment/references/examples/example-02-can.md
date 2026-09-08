# Risk Treatment Example 02 - CAN Domain

This example demonstrates risk treatment for a safety-critical CAN bus threat scenario.

---

## RT-CAN-001: CAN Message Injection - Reduce via SecOC & Gateway Filtering

**Related TS-ID**:
TS-CAN-001 [EXAMPLE] (CAN Bus Message Injection via Compromised Head Unit Firmware)

**Related DS-ID**:
DS-CAN-001 (Malicious CAN Message Injection Enabling Unintended Vehicle Behavior)

**Impact Score**:
Impact: 4 (Critical)
- Safety: 4 (Critical) - Loss of vehicle control, high fatality risk at highway speeds (unintended acceleration, sudden braking, steering angle changes)
- Financial: 3 (Severe) - Major liability for crashes ($10M-$50M per incident), mandatory recall ($50M-$100M for 100K vehicles), UN R155 regulatory fines
- Operational: 3 (Severe) - Critical safety functions compromised, vehicle cannot be safely operated until remediated
- Privacy: 1 (Negligible) - CAN messages are operational data, not personal information

**AFR Score**:
AFR: 11 (Moderate Feasibility)
- Elapsed Time: 2 (1 week - 1 month) - Firmware compromise plus validation take days to weeks
- Specialist Expertise: 1 (Expert in automotive cybersecurity) - Requires firmware reverse engineering, CAN protocol knowledge, and embedded exploit development
- Knowledge of Item: 2 (Public with effort) - Head Unit firmware architecture and CAN paths require reverse engineering effort
- Window of Opportunity: 3 (Unlimited / always accessible) - Once the compromised head unit is in place, the in-vehicle path stays available
- Equipment: 3 (Off-the-shelf consumer electronics) - CAN adapters and firmware tooling are broadly purchasable to a determined attacker

**Risk Value**:
Risk Value: RV 5
- Calculation: Impact 4 (Critical) × AFR 11 (Moderate Feasibility) → RV 5 (from Risk Value Matrix)

**Treatment Decision**: Reduce

**Treatment Description**:
Implement multi-layered CAN security controls including AUTOSAR Secure Onboard Communication (SecOC) for message authentication codes (MACs) on all safety-critical CAN messages, strengthened Gateway ECU filtering with allowlist-based message validation (only explicitly permitted message IDs forwarded to safety-critical networks), and CAN intrusion detection system (IDS) monitoring for anomalous message patterns (frequency, sequence, payload bounds). Deploy Hardware Security Module (HSM) in Head Unit SoC for secure storage of SecOC cryptographic keys (CMAC-AES-128) with access controlled by Trusted Execution Environment (TEE). This Reduce treatment targets Specialist Expertise (cryptographic protocol expertise required to forge valid MACs), Knowledge of Item (SecOC key derivation scheme is proprietary), and Equipment (HSM key extraction requires hardware fault injection tools).

**Control Categories**:
- Message Authentication (AUTOSAR SecOC with CMAC-AES-128 for safety-critical CAN messages)
- Network Segmentation (Gateway ECU with allowlist-based filtering, separation of safety-critical and infotainment networks)
- Intrusion Detection (CAN IDS monitoring for anomalous message frequency, sequence violations, out-of-bounds payloads)
- Secure Storage (HSM for SecOC cryptographic key protection, TEE-controlled access)
- Input Validation (Gateway message ID validation, payload bounds checking at receiving ECUs)

**Residual AFR**:
AFR (Before Controls): 11 (Moderate Feasibility)

AFR (After Controls): 6 (Low Feasibility)
- Elapsed Time: 1 (1-6 months) [CHANGED from 2] - SecOC bypass and key extraction extend preparation substantially
- Specialist Expertise: 0 (Multiple experts with rare skills) [CHANGED from 1] - Forging valid SecOC MACs plus firmware compromise now requires combined hardware and cryptographic expertise
- Knowledge of Item: 1 (Confidential / limited access) [CHANGED from 2] - Key derivation and HSM integration details are proprietary and significantly harder to recover
- Window of Opportunity: 3 (Unlimited / always accessible) [UNCHANGED] - The compromised in-vehicle path still exists once established
- Equipment: 1 (Specialized but purchasable) [CHANGED from 3] - HSM fault-injection and timing gear are required instead of commodity CAN tooling alone

Justification:
- **Elapsed Time** decreased to 1: SecOC bypass and HSM key extraction extend preparation from weeks into months.
- **Specialist Expertise** decreased to 0: Valid SecOC forgery now requires combined automotive, hardware security, and cryptographic expertise.
- **Knowledge of Item** decreased to 1: Proprietary key derivation and HSM integration details are much harder to obtain than the original CAN injection path.
- **Equipment** decreased to 1: HSM fault-injection and timing gear replace the original commodity CAN toolkit.

**Residual Risk Value**:
Residual Risk Value: RV 4
- Calculation: Impact 4 (Critical) × Residual AFR 6 (Low Feasibility) → RV 4

**Transfer Details**: N/A
*(Note: See "Alternative Treatment Considerations" section below for discussion of Transfer treatment with Tier 1 suppliers)*

**Acceptance Documentation**: N/A

**Last Updated**: 2026-03-20

---

## Key Takeaways from This Example

### 1. Safety-Critical Risks Usually Need Active Treatment
RV 5 with Impact 4 (Critical) from Safety dimension usually leads to **Reduce** treatment. Accept treatment for safety-critical risks usually needs exceptional justification, formal approval, and a strong argument for why active mitigation is not feasible. Regulatory and product-liability scrutiny is highest for serious threats affecting loss of life.

### 2. Defense-in-Depth for CAN Security
This example demonstrates multi-layered CAN protection:
- **Message Authentication (SecOC)**: Cryptographic MACs prevent message forgery
- **Gateway Filtering**: Allowlist-based filtering blocks unauthorized message IDs
- **Intrusion Detection**: Anomaly monitoring detects attack attempts
- **Secure Storage (HSM)**: Hardware-backed key protection prevents key extraction
- **Input Validation**: Receiving ECUs validate message payloads

No single control is sufficient; layers provide redundancy if one control fails.

### 3. Residual Risk May Not Collapse to Low Values
Despite AFR improvement from 11 (Moderate Feasibility) to 6 (Low Feasibility), Residual Risk Value only drops from RV 5 to RV 4 because Impact 4 remains critical. This illustrates that high-impact safety scenarios still need layered controls even after the attack becomes materially harder.

### 4. SecOC as Automotive Standard
AUTOSAR SecOC (Secure Onboard Communication) is the industry-standard message authentication mechanism for CAN bus security. It provides:
- Message authentication codes (MACs) using CMAC-AES-128
- Freshness values to prevent replay attacks
- Standardized integration with AUTOSAR Classic Platform and Adaptive Platform

SecOC is widely used as an accepted mitigation pattern for vehicle network security and aligns well with UN R155 expectations around protecting vehicle communication networks.

### 5. HSM Lowers the Equipment Score
Hardware Security Modules (HSMs) significantly lower the Equipment score (3 → 1) because key extraction now requires:
- Side-channel analysis equipment (ChipWhisperer, oscilloscopes, $50K+)
- Electromagnetic probes and Faraday cages ($100K+)
- Laser fault injection systems ($200K+)
- Expertise in differential power analysis (DPA) and fault injection techniques

This raises the attacker profile from a commodity-tool attacker to a well-funded lab or highly specialized team.

### 6. Gateway as Critical Choke Point
The Gateway ECU provides network segmentation between:
- **Infotainment Network**: Head Unit, Android OS, external connectivity (high attack surface)
- **Safety-Critical Network**: ADAS ECUs, Body Control, Powertrain (must be isolated)

Gateway filtering with allowlists ensures only explicitly authorized messages cross this boundary. Without Gateway protection, any Head Unit compromise would grant direct access to safety-critical ECUs.

---

## Cross-References

- **Related Damage Scenario**: `data/ds.md` → DS-CAN-001 (Malicious CAN Message Injection Enabling Unintended Vehicle Behavior)
- **Related Threat Scenario**: TS-CAN-001 [EXAMPLE] (firmware compromise attack vector)
- **Schema Definition**: `../rt-schema.md` → 14-field structure for RT entries
- **Risk Value Matrix**: `../rt-guide.md` → Impact × AFR calculation methodology
- **Treatment Methodology**: `../rt-guide.md` → When to use Avoid/Reduce/Transfer/Accept

---

## Alternative Treatment Considerations

### Why Not Avoid?
**Avoid** treatment would require removing CAN bus connectivity entirely, eliminating Head Unit access to vehicle network for data queries (speed, fuel level, diagnostic codes). This would break core infotainment functionality:
- No vehicle status display (speedometer, fuel gauge in instrument cluster)
- No diagnostic trouble codes (check engine light details)
- No integration with ADAS for navigation guidance (next turn, speed limit warnings)
- No climate control integration (cabin temperature display)

The CAN bus is essential for modern vehicle architecture. Avoid treatment is **commercially unviable** and would require fundamental vehicle redesign. The user confirmed that Head Unit access to CAN is required for product functionality.

### Why Not Transfer?
**Transfer** treatment has **partial applicability**:
- **Tier 1 Supplier Responsibility**: SecOC implementation may be contracted to a Tier 1 supplier (Bosch, Continental, Vector) who provides the AUTOSAR stack and cryptographic libraries. Supply contracts can include liability clauses requiring the supplier to provide secure SecOC implementation.
- **OEM Retains Ultimate Liability**: Under UN R155 and product liability law, the OEM (vehicle manufacturer) is the responsible party for vehicle safety regardless of supplier involvement. Transfer can shift **implementation responsibility** but not **regulatory liability**.

**Conclusion**: Transfer is a **complementary mechanism** (supplier contracts) but **not a standalone treatment**. Reduce controls must still be implemented; Transfer only determines who implements them.

### Why Not Accept?
**Accept** treatment is generally a poor fit for RV 5 safety-critical risks:
- ISO 26262 requires hazard mitigation for ASIL-D scenarios (life-threatening risks)
- UN R155 and vehicle approval practice expect documented treatment and effective controls for threats affecting safety-critical functions
- Product liability law holds OEMs responsible for foreseeable safety risks

Consciously accepting RV 5 safety risk without mitigation would constitute **negligence** and result in:
- Regulatory enforcement (type approval suspension, mandatory recalls)
- Criminal liability if crashes result from known, unmitigated vulnerabilities
- Massive tort liability in injury/fatality litigation

**Accept is rarely a viable option for safety-critical threats.** Reduce is usually the default treatment unless there is exceptional documented rationale for another path.

---

## Real-World Context

### Miller & Valasek CAN Injection Research (2015)
Security researchers Charlie Miller and Chris Valasek demonstrated remote vehicle control via CAN message injection in a 2014 Jeep Cherokee, leading to a 1.4 million vehicle recall. Their research showed:
- Compromised telematics unit (cellular modem) provided remote access to vehicle network
- Injected CAN messages caused unintended acceleration, braking, and transmission shifts
- Gateway filtering was insufficient to block safety-critical messages

This research motivated UN R155 requirements and widespread SecOC adoption. Modern Head Units face similar threat vectors (compromised Android OS → QNX hypervisor escape → CAN access).

### AUTOSAR SecOC Adoption
AUTOSAR SecOC has been deployed in production vehicles since 2018:
- **BMW**: SecOC on CAN-FD for drivetrain and chassis networks
- **Volkswagen Group**: MQB platform Gateway with SecOC filtering
- **Tesla**: Proprietary CAN authentication (non-AUTOSAR but similar concept)

SecOC adds ~2-8 bytes overhead per CAN message (MAC + freshness) and requires HSM or secure element in each ECU for key management. Cost is $5-$15 per ECU for HSM integration, totaling $50-$150 per vehicle for fleet-wide deployment.

### UN R155 Compliance
UN R155 (Cybersecurity and Software Updates) requires:
- **Clause 7.2.4.1**: "Protection against manipulation of vehicle communication networks"
- **Clause 7.3.1**: "Risk treatment for identified threats"

SecOC-based message authentication is the accepted industry practice for UN R155 compliance in CAN-based vehicle architectures. Regulatory audits verify that security controls are implemented, not just documented.

---

## Control Implementation Notes

### SecOC Deployment Strategy
1. **Identify Safety-Critical Messages**: Apply SecOC to messages affecting ISO 26262 ASIL-C/D functions (brake commands, steering angle, throttle position, gear selection)
2. **Key Management Architecture**: Use HSM in each ECU with unique per-ECU keys derived from master secret, rotated annually
3. **Freshness Values**: Implement freshness counters to prevent replay attacks (increment per message, synchronized via secure time source)
4. **Performance Constraints**: Ensure MAC computation latency < 10ms to meet real-time constraints (100 Hz CAN message rates)

### Gateway Filtering Rules
1. **Allowlist by Message ID**: Only permit explicitly authorized CAN IDs to cross from Infotainment Network to Safety-Critical Network
2. **Direction Enforcement**: Head Unit can query (read) vehicle data but cannot send commands (write) to safety-critical ECUs
3. **Rate Limiting**: Enforce maximum message frequency per ID to prevent DoS attacks
4. **Payload Validation**: Check message payload length and value ranges at Gateway before forwarding

### CAN IDS Monitoring
1. **Message Frequency Anomalies**: Alert if message rate exceeds 2x normal baseline (e.g., door lock commands suddenly sent at 100 Hz)
2. **Sequence Violations**: Detect out-of-order messages or unexpected message combinations (e.g., parking brake engaged while vehicle speed > 0)
3. **Payload Bounds Checking**: Flag messages with payloads outside valid ranges (e.g., throttle position > 100%)
4. **Logging and Alerting**: Store IDS events for post-incident forensics, alert telematics backend for fleet-wide threat intelligence

**Implementation Timeline**: 18-24 months for full SecOC deployment across vehicle platform, including ECU firmware updates, key provisioning infrastructure, and validation testing.
