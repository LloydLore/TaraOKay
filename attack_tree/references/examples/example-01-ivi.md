# Attack Tree Example: IVI Domain

## AT-IVI-001: Malicious App Chain to User Data Exfiltration

**Root Goal**:

DS-IVI-002: User Personal Data Exposure

**Attack Tree Structure**:

```
DS-IVI-002: User Personal Data Exposure
    |
    [OR]
    |
    +-- [Path 1] [SEQ]
    |       |
    |       +-- [Step 1] TS-IVI-001: Malicious App Installation
    |       +-- [Step 2] TS-IVI-007: App Sandbox Escape Exploit
    |       +-- [Step 3] TS-IVI-010: File System Access to PII
    |       +-- [Step 4] TS-IVI-015: Data Exfiltration via Network
    |
    +-- [Path 2] [AND]
    |       |
    |       +-- TS-EXT-003: Physical USB Drive with Malware
    |       +-- TS-IVI-009: Bypass Data Encryption at Rest
    |
    +-- [Path 3] TS-BCK-005: Backend API Authorization Bypass
```

**Attack Paths**:

1. **Path 1 (Remote Multi-Stage App Compromise)**:
   - TS-IVI-001 → TS-IVI-007 → TS-IVI-010 → TS-IVI-015 → DS-IVI-002
   - Description: Attacker remotely distributes a malicious Android app 
     disguised as a legitimate utility (e.g., car customization tool). After 
     user installation, the app exploits a kernel vulnerability to escape the 
     Android sandbox, gains root privileges to access file system locations 
     containing user PII (contacts, call logs, SMS), then exfiltrates data 
     via cellular/WiFi connection to attacker-controlled server.

2. **Path 2 (Physical USB Malware with Encryption Bypass)**:
   - TS-EXT-003 ∧ TS-IVI-009 → DS-IVI-002
   - Description: Attacker leaves malicious USB drive in parking lot or uses 
     social engineering to convince driver to plug it in (BadUSB attack). USB 
     malware exploits autorun or file manager vulnerabilities to execute code. 
     Simultaneously, attacker exploits weak encryption implementation or 
     extracts keys from TEE to decrypt persistent storage, accessing user PII 
     stored on UFS flash.

3. **Path 3 (Backend API Remote Access)**:
   - TS-BCK-005 → DS-IVI-002
   - Description: Attacker exploits broken object-level authorization (OWASP 
     API1:2023) in OEM's backend API. By manipulating VIN or user ID parameters 
     in API requests, attacker bypasses ownership checks and retrieves user PII 
     synced to cloud (profile data, location history, contact lists, voice 
     recordings) without needing physical or IVI-level access.

**Leaf Nodes**:

- TS-IVI-001: Malicious App Installation via Sideloading [EXAMPLE]
- TS-IVI-007: Android Kernel Privilege Escalation Exploit [EXAMPLE]
- TS-IVI-010: Unauthorized File System Access to PII Storage [EXAMPLE]
- TS-IVI-015: Cellular/WiFi Data Exfiltration to C2 Server [EXAMPLE]
- TS-EXT-003: BadUSB Attack via Physical USB Port [EXAMPLE]
- TS-IVI-009: Bypass TEE/HSM-Based Data Encryption [EXAMPLE]
- TS-BCK-005: Backend API Broken Object-Level Authorization [EXAMPLE]

Total: 7 leaf nodes

**Path AFR Analysis**:

**Path 1 (Remote Multi-Stage App Compromise)**:
- TS-IVI-001 AFR: 11 (Low) - USB sideloading or third-party store
- TS-IVI-007 AFR: 5 (Medium) - Kernel exploit requires expertise
- TS-IVI-010 AFR: 9 (Medium) - File system navigation with root
- TS-IVI-015 AFR: 12 (Low) - HTTP POST with stolen data
- Aggregation: SEQ gate → MIN(11, 5, 9, 12) = 5 (weakest link)
- **Path 1 AFR: 5 (Medium)**

**Path 2 (Physical USB Malware with Encryption Bypass)**:
- TS-EXT-003 AFR: 10 (Low) - BadUSB hardware available ($100)
- TS-IVI-009 AFR: 3 (High) - TEE key extraction requires expert
- Aggregation: AND gate → MIN(10, 3) = 3 (both required, hardest limits)
- **Path 2 AFR: 3 (High difficulty)**

**Path 3 (Backend API Remote Access)**:
- TS-BCK-005 AFR: 8 (Medium) - API testing with Burp Suite, moderate skill
- Aggregation: Single-step path (no gates)
- **Path 3 AFR: 8 (Medium)**

**Effective AFR**:

**Effective AFR**: 8 (Medium)

**Rationale**: Attacker will choose Path 3 (backend API, AFR=8) over Path 1 
(remote app chain, AFR=5) and Path 2 (physical + encryption, AFR=3). While 
Path 3 requires moderate web security skills, it avoids the kernel exploitation 
expertise needed in Path 1 and the TEE key extraction complexity in Path 2. 
Path 3 is also fully remote with no physical access required, and the backend 
API attack surface is continuously accessible. The API vulnerability (broken 
authorization) is a common weakness (OWASP Top 10) that mid-level attackers can 
exploit using standard web testing tools.

**Critical Path**:

**Critical Path**: Path 3 (Backend API Remote Access)

**Justification**: Path 3 represents the highest practical threat despite not 
having the highest AFR. It combines moderate feasibility (AFR=8) with remote 
accessibility, scalability (can attack entire fleet), and stealth (backend 
logs may not correlate API access to individual vehicles). The attack requires 
only web application security skills (OWASP API testing), which are more common 
than automotive-specific exploitation knowledge. Path 1's kernel exploit 
barrier (AFR=5) and Path 2's TEE complexity (AFR=3) limit their attacker pool 
to advanced adversaries. Security priority: Implement robust API authorization 
with per-VIN ownership validation and rate limiting to block bulk enumeration.

**Mitigation Points**:

1. **TS-BCK-005 (Backend API Authorization Bypass)**
   - Control: Object-level authorization enforcement (verify user owns VIN 
     before data access) + API request rate limiting + anomaly detection for 
     VIN enumeration patterns
   - Impact: Blocks Path 3 entirely (eliminates critical path)
   - Coverage: High (single point of failure for remote API attacks)

2. **TS-IVI-007 (Android Kernel Privilege Escalation)**
   - Control: Kernel exploit mitigations (KASLR, SMEP/SMAP, PXN, seccomp-bpf) 
     + timely security patching for Android kernel CVEs
   - Impact: Breaks Path 1 at escalation stage (prevents root access even if 
     malicious app is installed)
   - Coverage: High (blocks entire remote app compromise chain)

3. **TS-IVI-001 (Malicious App Installation)**
   - Control: APK signing verification + allowlist-only installation policy + 
     user education against sideloading
   - Impact: Blocks Path 1 at entry point (first-line defense)
   - Coverage: Medium (defense-in-depth for remote vector)

4. **TS-IVI-009 (Bypass Data Encryption at Rest)**
   - Control: Hardware-backed encryption with HSM/TEE key storage + secure 
     boot chain + key derivation tied to device attestation
   - Impact: Blocks Path 2 even if USB malware executes (defense-in-depth)
   - Coverage: Medium (protects PII at rest across multiple attack scenarios)

5. **TS-EXT-003 (BadUSB Physical Attack)**
   - Control: USB port authentication + disable USB mass storage autorun + 
     restricted USB device classes (allowlist input devices only)
   - Impact: Blocks Path 2 at entry point
   - Coverage: Medium (physical attack surface hardening)

**Recommended Priority**: 
1. **Immediate**: TS-BCK-005 (API authorization) - blocks critical path AFR=8
2. **High**: TS-IVI-007 (kernel hardening) - blocks Path 1 AFR=5, high impact
3. **Medium**: TS-IVI-009 (encryption) - defense-in-depth for data at rest
4. **Low**: TS-IVI-001 + TS-EXT-003 (entry point controls) - tertiary defenses

**Last Updated**:

2026-03-20

**Confidence Level**:

Confidence Level: Medium

**Justification**: Tree structure validated against Android security best 
practices, OWASP API Top 10, and published automotive IVI research (IOActive 
2017, Keen Security Lab 2018). AFR scores derived from industry penetration 
testing experience and public CVE analysis. However, proprietary TEE 
implementation details for QAM8295 SoC were not reverse-engineered—actual key 
extraction difficulty (TS-IVI-009 AFR) may be higher or lower than estimated. 
Backend API architecture assumed based on common automotive OEM patterns but 
not validated against actual implementation. Recommend backend API security 
audit and TEE security assessment to increase confidence to High.

---

## Analysis Notes

### Why OR Gate at Root?

The three attack paths are INDEPENDENT alternatives—attacker needs only ONE to 
succeed. Path 1 (app chain), Path 2 (USB + encryption), and Path 3 (API bypass) 
do not depend on each other and represent distinct attack surfaces (IVI, 
physical, backend). Thus, OR gate models the attacker's choice of approach.

### Why SEQ Gate for Path 1?

Path 1 requires a specific ORDER of operations: (1) install app, (2) escape 
sandbox, (3) access files, (4) exfiltrate. Each step ENABLES the next—you 
cannot exfiltrate data before gaining file access, and you cannot access 
protected files before privilege escalation. Thus, SEQ gate enforces temporal 
dependency.

### Why AND Gate for Path 2?

Path 2 requires BOTH conditions simultaneously: (1) malware execution AND (2) 
encryption bypass. USB malware alone cannot read encrypted PII, and encryption 
bypass alone provides no mechanism to exfiltrate data. Both must succeed—thus 
AND gate models the conjunctive requirement.

### AFR Aggregation Logic

- **Path 1 (SEQ)**: MIN(11, 5, 9, 12) = 5 — Kernel exploit is the bottleneck
- **Path 2 (AND)**: MIN(10, 3) = 3 — TEE attack is the hardest requirement
- **Path 3 (single)**: 8 — No aggregation needed for single-step path
- **Effective**: MAX(5, 8, 3) = 8 — Attacker chooses easiest complete path

### Mitigation Strategy Rationale

**Priority 1 (API)**: Highest ROI—blocks remote scalable attack with single 
control. API authorization fix is software-only (no hardware changes), deployable 
via backend update, and immediately effective across entire fleet.

**Priority 2 (Kernel)**: High impact but longer timeline—requires Android 
kernel security patches, may need SoC vendor involvement, and update deployment 
via OTA (customer acceptance risk).

**Priority 3 (Encryption)**: Defense-in-depth control—protects even if USB 
malware runs. Hardware-backed encryption already partially implemented on 
QAM8295; focus on key management improvements (lower marginal cost).

**Priority 4 (Entry points)**: Defense-in-depth but lower ROI—user behavior 
hard to control (sideloading), physical access prevention difficult (valet, 
mechanic scenarios). Still valuable as layered defense but not primary focus.

### Real-World Attack Precedent

- **Path 1 analogy**: Similar to iOS/Android privilege escalation chains used 
  in mobile spyware (Pegasus, Chrysaor). Multi-stage exploitation targeting 
  personal data is well-established attack pattern.
  
- **Path 2 analogy**: BadUSB attacks demonstrated at Black Hat (Karsten Nohl 
  2014). Automotive context adds encryption complexity but core USB exploit 
  technique is proven.
  
- **Path 3 analogy**: OWASP API1:2023 (Broken Object-Level Authorization) is 
  #1 API vulnerability. Automotive backend APIs have shown similar weaknesses 
  (e.g., Nissan Leaf API bypass allowing remote vehicle control, 2016).

**Conclusion**: All three paths have real-world precedent. Path 3 (API) is 
most likely due to common vulnerability class and remote accessibility. Path 1 
(app chain) requires sophistication but aligns with APT tactics. Path 2 (USB) 
is opportunistic physical attack suitable for insider threats.
