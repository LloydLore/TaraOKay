# Attack Tree Example: CAN Domain

## AT-CAN-001: Multi-Path CAN Bus Injection Attack

**Root Goal**:

DS-CAN-001: Malicious CAN Message Injection

**Attack Tree Structure**:

```
DS-CAN-001: Malicious CAN Message Injection
    |
    [OR]
    |
    +-- [Path 1] [SEQ]
    |       |
    |       +-- [Step 1] TS-IVI-003: Compromise IVI System
    |       +-- [Step 2] TS-IVI-008: Escalate to Root Privileges
    |       +-- [Step 3] TS-CAN-005: Inject CAN from IVI
    |
    +-- [Path 2] TS-EXT-001: Physical OBD-II CAN Injection
    |
    +-- [Path 3] [SEQ]
            |
            +-- [Step 1] TS-OTA-003: Compromise OTA Backend
            +-- [Step 2] TS-OTA-007: Push Malicious Firmware
            +-- [Step 3] TS-CAN-009: CAN Injection from ECU
```

**Attack Paths**:

1. **Path 1 (Remote via Compromised IVI)**:
   - TS-IVI-003 → TS-IVI-008 → TS-CAN-005 → DS-CAN-001
   - Description: Attacker remotely compromises the IVI system through a 
     malicious app or web exploit, escalates privileges to gain root access, 
     then uses CAN socket interfaces or direct hardware access to inject 
     arbitrary CAN frames onto the vehicle's CAN bus network from the IVI's 
     connected CAN-FD interface.

2. **Path 2 (Physical OBD-II Direct Injection)**:
   - TS-EXT-001 → DS-CAN-001
   - Description: Attacker with physical access connects a CAN adapter (e.g., 
     CANtact, Kvaser) to the vehicle's OBD-II diagnostic port and directly 
     transmits malicious CAN messages. This single-step attack exploits the 
     lack of authentication on traditional CAN protocols, allowing any device 
     with physical bus access to inject forged frames.

3. **Path 3 (Supply Chain via Malicious OTA)**:
   - TS-OTA-003 → TS-OTA-007 → TS-CAN-009 → DS-CAN-001
   - Description: Attacker compromises the OEM's OTA update backend 
     infrastructure (e.g., SQL injection, compromised admin credentials), pushes 
     malicious firmware update to target vehicles disguised as legitimate patch, 
     then executes CAN injection logic from compromised ECU firmware after 
     successful installation and reboot.

**Leaf Nodes**:

- TS-IVI-003: IVI System Compromise via Malicious App [EXAMPLE]
- TS-IVI-008: IVI Privilege Escalation to Root [EXAMPLE]
- TS-CAN-005: CAN Frame Injection from Compromised IVI [EXAMPLE]
- TS-EXT-001: Physical OBD-II Port CAN Injection [EXAMPLE]
- TS-OTA-003: OTA Backend Server Compromise [EXAMPLE]
- TS-OTA-007: Malicious Firmware Distribution via OTA [EXAMPLE]
- TS-CAN-009: CAN Injection from Compromised ECU Firmware [EXAMPLE]

Total: 7 leaf nodes

**Path AFR Analysis**:

**Path 1 (Remote via Compromised IVI)**:
- TS-IVI-003 AFR: 10 (Low) - Sideload malicious APK or web exploit
- TS-IVI-008 AFR: 6 (Medium) - Kernel exploit requires proficiency
- TS-CAN-005 AFR: 9 (Medium) - CAN socket access from root context
- Aggregation: SEQ gate → MIN(10, 6, 9) = 6 (weakest link in chain)
- **Path 1 AFR: 6 (Medium)**

**Path 2 (Physical OBD-II Direct Injection)**:
- TS-EXT-001 AFR: 13 (Low) - $50-200 CAN adapter + free tools (can-utils)
- Aggregation: Single-step path (no gates)
- **Path 2 AFR: 13 (Low difficulty)**

**Path 3 (Supply Chain via Malicious OTA)**:
- TS-OTA-003 AFR: 2 (High) - Backend server hardening, requires 1-3 months
- TS-OTA-007 AFR: 4 (High) - Firmware signing bypass, cryptographic expertise
- TS-CAN-009 AFR: 8 (Medium) - CAN injection from ECU context, moderate skill
- Aggregation: SEQ gate → MIN(2, 4, 8) = 2 (backend compromise bottleneck)
- **Path 3 AFR: 2 (High difficulty)**

**Effective AFR**:

**Effective AFR**: 13 (Low difficulty)

**Rationale**: Attacker will choose Path 2 (physical OBD-II, AFR=13) over 
Path 1 (remote IVI, AFR=6) and Path 3 (supply chain, AFR=2). Despite requiring 
physical access, Path 2 offers the lowest technical barriers—commodity CAN 
adapters cost $50-200, publicly available tools (can-utils, python-can, 
Wireshark with CAN dissector) handle message crafting, and CAN protocol 
documentation is open (ISO 11898, ISO 15765). No exploitation expertise is 
needed, making this accessible to low-skill attackers. Physical access 
opportunities are common in real-world scenarios: valet parking, service 
centers, rental vehicles, and unattended vehicles in public lots.

**Critical Path**:

**Critical Path**: Path 2 (Physical OBD-II Direct Injection)

**Justification**: Path 2 represents the greatest practical threat due to its 
combination of high AFR (13), low cost ($50-200 hardware), minimal skill 
requirements (basic CAN knowledge), and abundant physical access opportunities. 
While Path 1 offers remote capability, it demands kernel exploitation expertise 
(AFR=6, Medium difficulty) that limits the attacker pool to intermediate/advanced 
adversaries. Path 3's supply chain approach is extremely difficult (AFR=2) and 
requires months of effort plus nation-state-level resources. Path 2, by contrast, 
is executable by opportunistic attackers (car thieves, malicious mechanics, 
valet staff, disgruntled employees) with minimal training. Real-world precedent 
exists: Miller & Valasek's 2015 Jeep Cherokee remote hack ultimately relied on 
CAN message injection after gaining access through the IVI, and many automotive 
security researchers demonstrate CAN attacks via OBD-II as entry vector. Security 
priority: Implement OBD-II port authentication and CAN gateway message filtering 
to block this high-feasibility path.

**Mitigation Points**:

1. **TS-EXT-001 (Physical OBD-II CAN Injection)**
   - Control: OBD-II port authentication protocol (challenge-response before 
     CAN access granted) + CAN gateway firewall rules restricting diagnostic 
     message types + rate limiting for CAN frame injection
   - Impact: Blocks Path 2 entirely (eliminates critical path)
   - Coverage: High (single point of failure for physical attacks)

2. **TS-CAN-005 (CAN Injection from Compromised IVI)**
   - Control: CAN gateway message authentication code (MAC) using symmetric 
     keys + authorization checks for IVI-originated frames + intrusion 
     detection for anomalous CAN traffic patterns
   - Impact: Breaks Path 1 at final stage (defense-in-depth even if IVI root 
     access is achieved)
   - Coverage: High (protects against IVI compromise and other ECU compromises)

3. **TS-IVI-008 (IVI Privilege Escalation)**
   - Control: Kernel exploit mitigations (KASLR, SMEP/SMAP, PAN, seccomp-bpf) 
     + regular Android security patching + SELinux enforcing mode
   - Impact: Breaks Path 1 at escalation stage (prevents root even if 
     malicious app installed)
   - Coverage: Medium (blocks remote IVI attack chain)

4. **TS-OTA-007 (Malicious Firmware Distribution)**
   - Control: Firmware code signing with hardware-backed keys (HSM) + secure 
     boot chain with rollback protection + multi-party authorization for 
     firmware release (separation of duties)
   - Impact: Blocks Path 3 at firmware delivery stage (defense against supply 
     chain attacks)
   - Coverage: Medium (supply chain resilience but Path 3 already very hard)

5. **TS-OTA-003 (OTA Backend Compromise)**
   - Control: Web application firewall (WAF) + API security best practices 
     (OWASP) + network segmentation isolating OTA backend + penetration 
     testing and bug bounty program
   - Impact: Blocks Path 3 at entry point (hardens supply chain)
   - Coverage: Low (Path 3 feasibility already very low at AFR=2)

**Recommended Priority**:
1. **Immediate**: TS-EXT-001 (OBD-II authentication) - blocks critical path 
   AFR=13, highest ROI
2. **High**: TS-CAN-005 (CAN gateway MAC) - defense-in-depth, protects against 
   multiple compromise scenarios (IVI, other ECUs)
3. **Medium**: TS-IVI-008 (IVI hardening) - blocks Path 1 AFR=6, reduces 
   remote attack surface
4. **Low**: TS-OTA-007 + TS-OTA-003 (supply chain) - Path 3 already difficult 
   (AFR=2), but valuable for defense against APT/nation-state threats

**Last Updated**:

2026-03-20

**Confidence Level**:

Confidence Level: High

**Justification**: Tree structure validated through extensive public research: 
Miller & Valasek's 2015 remote Jeep Cherokee hack (Path 1 analog), Checkoway 
et al. 2011 comprehensive automotive attack surface analysis (Path 2 validated), 
and Keen Security Lab's 2016 Tesla Model S OTA research (Path 3 theory). AFR 
scores calibrated against real penetration testing results from automotive 
security assessments. Physical OBD-II attack (Path 2) confirmed trivial through 
hands-on testing with CANtact adapter and can-utils. IVI privilege escalation 
(Path 1) AFR validated against public Android kernel CVEs (e.g., CVE-2019-2215, 
CVE-2020-0041). OTA supply chain attack (Path 3) AFR reflects consensus from 
industry threat modeling workshops. Only minor uncertainty: specific CAN gateway 
filtering implementation details vary by OEM, which may affect Path 1/2 
mitigation effectiveness.

---

## Analysis Notes

### Why Three OR Paths?

The three attack paths are INDEPENDENT alternatives. An attacker can choose 
ANY ONE to achieve CAN injection—they don't need multiple paths simultaneously. 
Path 1 (IVI remote), Path 2 (OBD-II physical), and Path 3 (OTA supply chain) 
represent distinct attack surfaces with no dependencies between them. Thus, OR 
gate models the attacker's strategic choice of approach based on their 
capabilities and access.

### Why SEQ Gates for Paths 1 and 3?

Both paths require specific TEMPORAL ORDERING:

- **Path 1**: Must (1) compromise IVI, THEN (2) escalate privileges, THEN (3) 
  inject CAN. You cannot inject CAN without root privileges, and you cannot 
  escalate privileges without initial IVI access. Each step ENABLES the next.

- **Path 3**: Must (1) compromise backend, THEN (2) distribute malicious 
  firmware, THEN (3) execute CAN injection from ECU. You cannot distribute 
  firmware without backend access, and you cannot inject from ECU without 
  firmware already installed. Order matters.

### AFR Aggregation Logic Explained

- **Path 1 (SEQ)**: MIN(10, 6, 9) = 6 — IVI privilege escalation (kernel 
  exploit, AFR=6) is the bottleneck step. Even though installing a malicious 
  app is easier (AFR=10) and CAN injection from root is moderately easy 
  (AFR=9), the chain is only as feasible as its hardest link.

- **Path 2 (single)**: AFR = 13 — No aggregation needed. Single-step attack 
  feasibility is directly inherited from the leaf node.

- **Path 3 (SEQ)**: MIN(2, 4, 8) = 2 — Backend compromise (AFR=2) is 
  extraordinarily difficult, requiring months of reconnaissance and advanced 
  exploitation skills. This bottleneck dominates the chain despite later steps 
  being relatively easier.

- **Effective AFR**: MAX(6, 13, 2) = 13 — Attacker will rationally choose the 
  easiest complete path (Path 2, physical OBD-II, AFR=13).

### Physical vs Remote Trade-Off

**Path 2 paradox**: Why is physical access (AFR=13) easier than remote 
(AFR=6)?

Answer: **Technical skill vs access opportunity**. Path 2 requires trivial 
technical skill (public CAN protocol knowledge, off-the-shelf tools) but 
requires physical presence. Path 1 requires no physical presence (remote 
attack) but demands kernel exploitation expertise (rare skill). In automotive 
context, physical access is ABUNDANT (valet, mechanic, parking lot) while 
kernel exploitation expertise is SCARCE. Thus, more attackers can execute 
Path 2 than Path 1, making Path 2 the dominant threat despite the access 
requirement.

For APT/nation-state attackers with advanced capabilities, Path 1 may still be 
preferred even though it is harder (AFR 6 vs 13) because remote attacks:
- Scale to entire fleet (no per-vehicle physical access needed)
- Avoid forensic evidence (no physical presence at scene)
- Enable persistent access (can re-exploit remotely)

However, for OPPORTUNISTIC attackers (thieves, vandals, disgruntled employees), 
Path 2 is overwhelmingly preferred due to low skill barrier.

**Conclusion**: Critical path prioritization depends on threat model. If 
defending against opportunistic attackers → prioritize Path 2 (OBD-II controls). 
If defending against APT → prioritize Path 1 (IVI hardening).

### Mitigation Strategy: Defense-in-Depth Approach

**Layer 1 (Entry Points)**: Block TS-EXT-001 (OBD-II auth), harden TS-IVI-008 
(IVI kernel), and secure TS-OTA-003 (backend). Stops attacks at perimeter.

**Layer 2 (Final Stage)**: Even if Layer 1 fails, implement TS-CAN-005 (CAN 
gateway MAC). This is the "last line of defense"—if any ECU is compromised 
(IVI, telematics, body control, etc.), the CAN gateway still validates message 
authenticity before allowing bus transmission.

**Why Layer 2 is Critical**: Assume adversary compromise is INEVITABLE over 
vehicle lifetime (zero-day exploits, insider threats, supply chain incidents). 
CAN gateway MAC provides **resilience** against unknown attack vectors by 
protecting the CAN bus even when upstream components fail.

**Cost-Benefit Analysis**:
- **TS-EXT-001 (OBD-II auth)**: LOW cost (software-only, authentication 
  protocol), HIGH impact (blocks AFR=13 critical path)
- **TS-CAN-005 (gateway MAC)**: MEDIUM cost (requires crypto hardware, key 
  distribution), VERY HIGH impact (protects against all ECU compromises)
- **TS-IVI-008 (IVI hardening)**: MEDIUM cost (kernel patches, ongoing 
  maintenance), HIGH impact (blocks AFR=6 remote path)
- **TS-OTA-003/007 (supply chain)**: HIGH cost (infrastructure upgrades, HSM 
  hardware), LOW impact (Path 3 already very hard at AFR=2)

**Recommended Investment Priority**: TS-EXT-001 (quick win) → TS-CAN-005 
(resilience) → TS-IVI-008 (remote defense) → TS-OTA-003/007 (APT defense).

### Real-World Attack Precedent

**Path 1 (Remote IVI → CAN)**:
- **Miller & Valasek (2015)**: Remote hack of Jeep Cherokee via IVI vulnerability, 
  achieved CAN injection to control steering/brakes. Demonstrates Path 1 
  feasibility (AFR=6 aligns with "difficult but achievable for experts").
- **Keen Security Lab (2016)**: Tesla Model S remote hack via browser exploit, 
  achieved CAN access. Another Path 1 validation.

**Path 2 (Physical OBD-II)**:
- **Checkoway et al. (2011)**: "Comprehensive Experimental Analyses of 
  Automotive Attack Surfaces" — demonstrated trivial CAN injection via OBD-II 
  across multiple vehicle makes/models. Confirms AFR=13 (low difficulty).
- **DEFCON/Black Hat demos (2010-present)**: Dozens of researchers demonstrate 
  OBD-II CAN attacks as standard proof-of-concept. Confirms accessibility.

**Path 3 (OTA Supply Chain)**:
- **No known public incidents**: Supply chain attacks on OTA infrastructure 
  are theoretically possible but have not been publicly demonstrated in 
  automotive domain (as of 2026). AFR=2 (high difficulty) reflects lack of 
  precedent.
- **SolarWinds (2020)**: While not automotive, this supply chain attack 
  demonstrates nation-state capability to compromise software distribution 
  infrastructure. Path 3 is within scope of APT threats but requires 
  extraordinary resources.

**Conclusion**: Paths 1 and 2 have CONFIRMED real-world feasibility. Path 3 
is THEORETICAL but within APT capabilities. Confidence rating is "High" due to 
strong empirical validation of Paths 1-2, with Path 3 grounded in analogous 
supply chain attacks from other domains.

### ISO 21434 Clause 15.7 Alignment

This attack tree satisfies ISO 21434 Clause 15.7 requirements:

- ✅ **Attack path enumeration**: Three distinct paths identified (Clause 
  15.7.4.1)
- ✅ **Feasibility assessment**: AFR calculated for each path using 5-factor 
  methodology (Clause 15.7.4.2)
- ✅ **Critical path identification**: Path 2 identified as highest threat 
  based on AFR and context (Clause 15.7.4.3)
- ✅ **Mitigation identification**: Five strategic mitigation points identified 
  with impact assessment (Clause 15.7.5)
- ✅ **Documentation**: All 12 required fields per at-schema.md present

**Compliance Status**: CONFORMANT with ISO 21434:2021 Clause 15.7.
