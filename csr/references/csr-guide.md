# Cybersecurity Requirement Derivation Methodology - ISO 21434 TARA

**Authority note**: This is the authoritative source for CSR derivation workflow, decomposition patterns, and worked methodology. `SKILL.md` should summarize and link here rather than duplicating the full method.

This guide provides methodology for deriving cybersecurity requirements (CSRs) from cybersecurity goals (CSGs) and performing gap analysis against implemented controls in ISO 21434 TARA workflows, aligned with Clause 9.4 (Cybersecurity specifications).

---

## Overview

**Cybersecurity Requirements (CSRs)** are specific, testable technical requirements that define HOW to implement cybersecurity goals. They translate high-level security objectives into concrete implementation guidance with specific technologies, algorithms, parameters, and verification criteria.

**Key Characteristics**:
- Derived FROM cybersecurity goals (not damage scenarios)
- Technology-specific and parameterized (AES-256, RSA-2048, TLS 1.3)
- Testable and verifiable (clear pass/fail criteria)
- Implementation-specific (tied to component architecture)
- Documented in two parts: IMPLEMENTED controls (Part A) and identified GAPS (Part B)

**Relationship to Other TARA Artifacts**:
```
Damage Scenario (DS-*)
    ↓ (defines impact)
Risk Treatment Decision (RT-*)
    ├─ Avoid / Reduce / Transfer + active mitigation → Cybersecurity Goal (CSG-*)
    │                                                ↓ (decomposed by this skill)
    │                                             Cybersecurity Requirement (CSR-*)
    │                                                ↓ (specifies control)
    │                                             Security Control Implementation
    └─ Pure Transfer / Accept → RT-owned claim only in `data/rt.md`
```

**Critical Distinction - CSG vs CSR**:
- **CSG**: High-level security objective (WHAT must be protected) — "protect location data confidentiality"
- **CSR**: Technical implementation requirement (HOW to protect) — "implement AES-256-GCM encryption with PBKDF2 key derivation (100,000 iterations)"

---

## The 6-Step Derivation Methodology

### Step 1: Read Cybersecurity Goals → Identify Security Properties

**Objective**: Understand WHAT security properties need technical implementation.

**Process**:
1. Locate the cybersecurity goal file (e.g., `data/csg.md`)
2. For each CSG, read the **Goal Statement**, **CIA Property**, and **Related DS-IDs**
3. Identify which security properties require implementation
4. Note the components/systems mentioned in the goal

**CIA Property to CSR Category Mapping**:

| CIA Property | Security Properties to Implement | Typical CSR Categories |
|--------------|----------------------------------|------------------------|
| **Confidentiality** | Data encryption, access control, authentication, authorization, audit logging | CRYPTO, ACCESS, AUTH, AUDIT |
| **Integrity** | Message authentication, digital signatures, code signing, input validation, tamper detection | CRYPTO, COMMS, OTA, CONFIG, SYSTEM |
| **Availability** | DoS protection, rate limiting, failover, redundancy, resource reservation | NETWORK, SYSTEM, COMMS, REDUNDANCY |

**Example**: CSG-IVI-01 "Location Data Confidentiality"
- **CIA Property**: Confidentiality
- **Goal Statement**: "The infotainment system shall protect location data to prevent unauthorized disclosure."
- **Security Properties Required**: 
  - Encryption (CRYPTO category)
  - Access control (ACCESS category)
  - Audit logging (AUDIT category)
- **Target Components**: Telematics Control Unit (TCU), Android IVI, Backend API

**Output of Step 1**: List of CSGs with their required CSR categories and target components

---

### Step 2: Read Design Specifications → Identify Implemented Controls

**Objective**: Document EXISTING security controls from design specifications, architecture documents, and component datasheets.

**Process**:
1. Collect design documentation sources
2. For each security control mentioned, extract:
   - **What** the control does (description)
   - **Where** it's documented (source reference with section number)
   - **Which CSG** it addresses (traceability)
3. Create Part A entries for implemented controls

**Common Sources of Implemented Controls**:

| Document Type | Typical Content | Example Reference |
|---------------|----------------|-------------------|
| Information Security Design Specification (信息安全设计规范说明书) | Cryptographic algorithms, secure storage, access control mechanisms | Section 3.2.1 "Certificate Management" |
| System Architecture Document | Network segmentation, gateway filtering, secure boot chain | Section 5.4 "CAN Bus Architecture" |
| Component Datasheets | Hardware security features (HSM, TEE, RPMB, eFuse) | Qualcomm QAM8295 Security Features Datasheet |
| Supplier Security Declarations | Third-party component security controls (AUTOSAR SecOC, TLS version) | AUTOSAR Classic Platform R21-11 SecOC Module |
| Previous TARA Work Products | Controls from earlier threat modeling cycles | TARA v1.0 (2024) - OTA Update Security |

**Part A Entry Creation Template**:

For each implemented control:
```
CSR-[CATEGORY]-[NN]: [Title from Design Specification]
- Status: ✅ IMPLEMENTED
- Category: [CRYPTO/ACCESS/COMMS/etc.]
- Description: [Original Chinese text from design specification - preserve exactly]
- Source: [Document name + Section reference]
- Related CSG-IDs: [CSG-XXX-NN]
```

**Example** (from design specification):
```
CSR-CERT-01: 部件支持OEM证书链加载和存储
- Status: ✅ IMPLEMENTED
- Category: Certificate Management
- Description: 流程规范：证书与密钥灌装严格遵循《PKI证书灌装流程规范-v1.6》。 
  安全存储：所有敏感密钥及证书私钥均写入RPMB (Replay Protected Memory Block) 区域
  或HSM安全存储区。RPMB具备防重放、防篡改及访问鉴权特性，确保密钥无法被普通
  文件系统工具读取或修改。
- Source: Design Specification (信息安全设计规范说明书) Section 3.2.1
- Related CSG-IDs: CSG-CERT-01
```

**Important Language Note**: Part A entries preserve **original Chinese text** from design specifications for traceability and audit purposes. Do NOT translate to English.

**Output of Step 2**: List of IMPLEMENTED controls (Part A entries) with source references

---

### Step 3: Decompose Each CSG into Technical Requirements

**Objective**: Translate high-level CSG objectives into specific, testable technical requirements (CSRs).

**CSG-to-CSR Decomposition Decision Tree**:

```
Start with CSG goal statement
    ↓
What is the CIA Property?
    ↓
┌─────────────┬─────────────┬─────────────┐
│ Confidentiality │   Integrity  │ Availability │
└─────┬──────┘     └──────┬─────┘  └──────┬─────┘
      ↓                    ↓                ↓
  CRYPTO (encryption)   CRYPTO (signing)  NETWORK (DoS protection)
  ACCESS (authorization) COMMS (authentication) SYSTEM (prioritization)
  AUDIT (logging)       CONFIG (validation) REDUNDANCY (failover)
```

**Decomposition Template**:

For each CSG, ask three questions:
1. **WHAT technical controls are needed** to achieve this goal?
2. **WHERE should these controls be implemented** (component, layer, interface)?
3. **HOW can compliance be verified** (test criteria, acceptance criteria)?

---

#### Confidentiality CSG Decomposition

**Pattern**: Encryption + Access Control + Audit

**CSG Example**: CSG-IVI-01 "Location Data Confidentiality"
- Goal: "Protect location data to prevent unauthorized disclosure"

**CSR Derivation**:

**CSR 1 - Encryption (CRYPTO category)**:
```
CSR-CRYPTO-01: Location Data Encryption
- Algorithm: AES-256-GCM for location data encryption (at-rest and in-transit)
- Key Derivation: PBKDF2 with 100,000 iterations for user password-based keys
- Key Storage: Hardware-backed secure storage (QTEE KeyStore or HSM)
- Scope: All location data (GPS coordinates, historical routes, POI search history)
- Verification: Attempt to read encrypted files without decryption key (should fail)
```

**CSR 2 - Access Control (ACCESS category)**:
```
CSR-ACCESS-01: Location Data Authorization
- Mechanism: Role-Based Access Control (RBAC) for location data access
- User Consent: Require explicit user consent before sharing location with third-party apps
- Least Privilege: Apps only access location when in foreground (background access requires additional permission)
- Verification: Test unauthorized app access attempt (should be denied)
```

**CSR 3 - Audit (AUDIT category)**:
```
CSR-AUDIT-01: Location Access Logging
- Log Events: All location data access events (timestamp, requesting app, access result)
- Storage: Tamper-resistant storage (minimum 6 months retention)
- User Visibility: Provide user dashboard showing location access history
- Verification: Trigger access event, verify log entry creation
```

**Result**: 1 CSG → 3 CSRs (Confidentiality pattern)

---

#### Integrity CSG Decomposition

**Pattern**: Authentication + Validation + Signing

**CSG Example**: CSG-CAN-01 "CAN Message Integrity"
- Goal: "Validate message authenticity to prevent injection attacks"

**CSR Derivation**:

**CSR 1 - Message Authentication (COMMS category)**:
```
CSR-COMMS-01: CAN Message Authentication
- Protocol: AUTOSAR SecOC (Secure Onboard Communication)
- Algorithm: CMAC-AES-128 with 64-bit MAC for all safety-critical CAN messages
- Freshness: Freshness Value (FV) counter preventing replay attacks (48-bit counter)
- Scope: All CAN IDs controlling braking, steering, acceleration, powertrain
- Verification: Inject unauthenticated CAN message (should be rejected)
```

**CSR 2 - Gateway Filtering (CONFIG category)**:
```
CSR-CONFIG-01: CAN Gateway Filtering Rules
- Whitelist: CAN ID whitelist filtering at gateway ECU (only allow known ECU IDs)
- Rejection: Drop unauthorized CAN IDs silently, log event to audit trail
- Rate Limiting: Max 100 messages/second per CAN ID (prevent flooding)
- Verification: Send CAN message from unauthorized ID (should be filtered)
```

**CSR 3 - Secure Boot (CRYPTO category)**:
```
CSR-CRYPTO-02: Secure Boot Chain for Gateway ECU
- Boot Chain: Bootloader → Kernel → HAL (each stage verifies next)
- Algorithm: RSA-2048 signature verification at each boot stage
- Rollback Protection: eFuse version counter preventing downgrade attacks
- Verification: Attempt to boot unsigned firmware (should fail at bootloader)
```

**Result**: 1 CSG → 3 CSRs (Integrity pattern)

---

#### Availability CSG Decomposition

**Pattern**: DoS Protection + Rate Limiting + Redundancy

**CSG Example**: CSG-COMMS-01 "eCall Availability"
- Goal: "Maintain emergency call (eCall) functionality during network attacks"

**CSR Derivation**:

**CSR 1 - DoS Detection (NETWORK category)**:
```
CSR-NETWORK-01: DoS Attack Detection and Mitigation
- Detection: Monitor network traffic for flooding patterns (threshold: 1000 packets/sec)
- SYN Flood Detection: Detect incomplete TCP handshake ratio > 50%
- Mitigation: Automatically activate rate limiting when DoS detected
- Verification: Simulate DoS attack, verify rate limiting activation
```

**CSR 2 - Resource Reservation (SYSTEM category)**:
```
CSR-SYSTEM-01: Critical Function Prioritization
- CPU Reservation: Dedicated CPU core for eCall processing (CPU affinity pinning)
- Scheduling: Real-time scheduling priority (SCHED_FIFO, priority 99) for safety-critical tasks
- Bandwidth Reservation: QoS Class Identifier (QCI) for eCall on cellular modem
- Verification: Saturate CPU with low-priority tasks, verify eCall latency < 100ms
```

**CSR 3 - Failover (REDUNDANCY category)**:
```
CSR-REDUNDANCY-01: eCall Failover Mechanism
- Backup Channel: Automatic failover to backup communication channel (LTE → 3G → SMS)
- Self-Test: Monthly automatic failover test (transparent to user)
- Recovery Time: <5 seconds recovery time for eCall restoration after failure
- Verification: Disable primary channel, verify failover to backup within 5 seconds
```

**Result**: 1 CSG → 3 CSRs (Availability pattern)

---

### CSR Quality Checklist

Before finalizing a CSR, verify:

- ✅ **Technology-specific**: Mentions concrete technology/algorithm (AES-256, RSA-2048, TLS 1.3, AUTOSAR SecOC)
- ✅ **Parameterized**: Includes specific parameters (key size, iteration count, timeout values, thresholds)
- ✅ **Testable**: Has clear verification criteria (can write test case with pass/fail criteria)
- ✅ **Component-specific**: Tied to specific component/layer (not "the vehicle")
- ✅ **Traceable**: Maps to at least one CSG (clear lineage from goal)

**Good Example** (CSR):
> "Implement AES-256-GCM encryption for location data with PBKDF2 key derivation (100,000 iterations) stored in QTEE KeyStore."

**Bad Example** (CSG-level, not CSR-level):
> "The system shall protect location data."

**Why Bad?**:
- No specific technology mentioned
- No parameters or configuration details
- Not testable (no verification criteria)
- Too abstract (belongs in CSG, not CSR)

**Output of Step 3**: Detailed technical requirements (CSRs) for each CSG, organized by category

---

### Step 4: Gap Analysis → Compare Required vs Implemented

**Objective**: Identify which required CSRs (from Step 3) are ALREADY implemented (from Step 2) and which are GAPS.

**Gap Analysis Decision Tree**:

```
For each required CSR from Step 3:
    ↓
Does an implemented control (Part A) fully satisfy this CSR?
    ↓ YES → Mark as ✅ IMPLEMENTED (already in Part A, no action needed)
    ↓ NO → Continue
       ↓
Does a partial control exist (incomplete implementation)?
    ↓ YES → Mark as ⚠️ PARTIAL (create Part B entry, document gap)
    ↓ NO → Mark as ❌ GAP (create Part B entry, full implementation required)
```

**Gap Status Definitions**:

| Status | Symbol | Meaning | Example | Part |
|--------|--------|---------|---------|------|
| **IMPLEMENTED** | ✅ | Control fully implemented and documented in design spec | CSR-CRYPTO-01: AES-256 encryption verified in design spec Section 3.2.1 | Part A |
| **PARTIAL** | ⚠️ | Control partially implemented, gaps identified | CSR-CLOUD-01: mTLS enabled but MFA missing | Part B |
| **GAP** | ❌ | Control not implemented, requirement identified through TARA | CSR-AUDIT-01: No location access logging mechanism | Part B |

**Classification Decision Matrix**:

| Implemented Control Coverage | Gap Classification | Part | Priority |
|------------------------------|-------------------|------|----------|
| 100% of CSR requirements met | ✅ IMPLEMENTED | Part A | N/A (already done) |
| 50-99% of CSR requirements met | ⚠️ PARTIAL | Part B | Based on TS-ID Risk Value |
| <50% of CSR requirements met | ❌ GAP | Part B | Based on TS-ID Risk Value |
| 0% (no control exists) | ❌ GAP | Part B | Based on TS-ID Risk Value |

**Example 1 - IMPLEMENTED Status**:

**Required CSR** (from Step 3):
```
CSR-CRYPTO-01: Location Data Encryption
- Implement AES-256-GCM for location data encryption (at-rest and in-transit)
- Use PBKDF2 key derivation (100,000 iterations) for user password-based keys
- Store encryption keys in hardware-backed secure storage (QTEE/HSM)
```

**Implemented Control** (from Step 2 - Part A):
```
CSR-CRYPTO-01: 位置数据加密
- Status: ✅ IMPLEMENTED
- Description: 位置数据使用AES-256-GCM加密存储，密钥通过PBKDF2派生(100,000次迭代)，
  存储于QTEE KeyStore中。传输中的位置数据通过TLS 1.3加密通道保护。
- Source: Design Specification Section 4.3.2 "Location Data Protection"
```

**Gap Analysis**: ✅ All requirements met → Status = IMPLEMENTED (Part A only, no Part B entry needed)

---

**Example 2 - PARTIAL Status**:

**Required CSR** (from Step 3):
```
CSR-CLOUD-01: Cloud Sync Authentication
- Implement mTLS authentication for cloud API connections
- Enforce Multi-Factor Authentication (MFA) for all user accounts
- Session timeout: 15 minutes inactivity, 8 hours absolute
```

**Implemented Control** (from Step 2 - Part A):
```
CSR-CLOUD-01: 云端同步认证
- Status: ✅ IMPLEMENTED (partial)
- Description: 云端API使用mTLS双向认证，用户登录支持密码认证。
- Source: Design Specification Section 6.1 "Cloud Services Security"
```

**Gap Analysis**: 
- ✅ mTLS authentication: IMPLEMENTED
- ❌ Multi-Factor Authentication (MFA): MISSING
- ❌ Session timeout configuration: NOT SPECIFIED
- Coverage: 33% → Status = ⚠️ PARTIAL

**Part B Entry for Gap**:
```
CSR-CLOUD-01: Cloud Sync Authentication (Gap: MFA and Session Management)
- Status: ⚠️ PARTIAL
- Category: Cloud Security
- Description: Current implementation provides mTLS authentication but lacks Multi-Factor 
  Authentication (MFA) and defined session timeout policies. Attack TS-BCK-001 (Credential 
  Theft via Phishing) can bypass password-only authentication.
- Priority: CRITICAL (RV 4)
- Identified By: TS-BCK-001 (Credential Theft)
- Recommendation: 
  WHAT: Implement TOTP-based Multi-Factor Authentication (MFA) using RFC 6238 algorithm.
  HOW: 30-second time window, 6-digit OTP codes, mandatory enrollment for all users.
  WHERE: Backend authentication service (AWS Cognito or equivalent).
  VERIFY: Test login with correct password but wrong OTP code (should fail).
- Related CSG-IDs: CSG-BCK-01
```

---

**Example 3 - GAP Status**:

**Required CSR** (from Step 3):
```
CSR-CRYPTO-04: DVR Video Encryption
- Implement AES-256-XTS encryption for all dashcam recordings
- Encrypt video files during write operation (transparent to application layer)
- Store decryption keys in QTEE KeyStore (per-file unique keys)
```

**Implemented Control** (from Step 2): NONE (no design specification entry found)

**Gap Analysis**: 
- Coverage: 0% → Status = ❌ GAP

**Part B Entry**:
```
CSR-CRYPTO-04: DVR Video Encryption
- Status: ❌ GAP
- Category: Cryptography
- Description: DVR recordings (dashcam footage) are currently stored in plaintext H.264 
  format on eMMC storage. Physical extraction attack TS-IVI-003 allows adversary with 
  physical access to extract video recordings containing sensitive location and biometric 
  data (driver face, license plates).
- Priority: HIGH (RV 3)
- Identified By: TS-IVI-003 (Physical Storage Extraction)
- Recommendation:
  WHAT: Implement file-based encryption using AES-256-XTS for all DVR video files.
  HOW: Encrypt during write operation via dm-crypt, per-file unique keys derived from 
       master key stored in QTEE KeyStore.
  WHERE: Android HAL layer (media.recorder service integration).
  VERIFY: Extract eMMC storage, attempt to decode video files without decryption key 
          (should produce undecodable binary data).
- Related CSG-IDs: CSG-IVI-01, CSG-IVI-02
```

---

**Gap Documentation Template (Part B)**:

For each gap (PARTIAL or GAP status):
```
CSR-[CATEGORY]-[NN]: [Title]
- Status: ⚠️ PARTIAL or ❌ GAP
- Category: [Category name]
- Description: [What's missing or incomplete + which TS-ID identified this + impact]
- Priority: CRITICAL | HIGH | MEDIUM | LOW
- Identified By: TS-[DOMAIN]-[NNN] or "TARA Analysis"
- Recommendation: [4-element template - WHAT/HOW/WHERE/VERIFY]
- Related CSG-IDs: [CSG-XXX-NN]
```

**Output of Step 4**: Classification of all CSRs into IMPLEMENTED (Part A), PARTIAL (Part B), or GAP (Part B) status

---

### Step 5: Carry Priority From Upstream TS/RT Context

**Objective**: Record the implementation priority already supported by the linked TS/RT analysis, without creating a second local policy inside CSR.

**Process**:

For each gap (PARTIAL or GAP status):
1. Find the originating TS-ID from `Identified By`.
2. Review the linked TS/RT context.
3. Copy the resulting priority into the CSR entry.
4. If upstream RT is incomplete, mark the CSR as pending RT completion instead of inventing a local priority.

**Important**: If a threat scenario has Treatment = Accept or pure Transfer, do NOT create CSR entries. Formal claim text, approvals, and residual-risk rationale remain in `data/rt.md`, not in `data/csg.md`.

**Output of Step 5**: Priority recorded in the CSR entry, or explicit pending-RT status noted for follow-up.

---

### Step 6: Document Traceability → Verify Completeness

**Objective**: Ensure every CSG is implemented by at least one CSR, and every gap traces back to a threat scenario.

**Traceability Matrix Format**:

Create a mapping table showing CSG → CSR relationships:

| CSG-ID | CSG Title | Related CSR-IDs | Status Summary | Completeness |
|--------|-----------|----------------|----------------|--------------|
| CSG-IVI-01 | Location Data Confidentiality | CSR-CRYPTO-01 (✅), CSR-ACCESS-01 (⚠️), CSR-AUDIT-01 (❌) | 1 Implemented, 1 Partial, 1 Gap | ✅ Covered |
| CSG-CAN-01 | CAN Message Integrity | CSR-COMMS-01 (✅), CSR-CONFIG-01 (✅), CSR-CRYPTO-02 (⚠️) | 2 Implemented, 1 Partial | ✅ Covered |
| CSG-OTA-01 | OTA Update Integrity | CSR-OTA-01 (❌), CSR-OTA-02 (❌), CSR-OTA-03 (❌) | 3 Gaps (all CRITICAL) | ⚠️ High Risk |

**Completeness Validation Rules**:

**Rule 1: Every CSG must have ≥1 CSR**
```bash
# Extract CSG-IDs from csg.md
grep -oE 'CSG-[A-Z]{2,5}-[0-9]{2}' data/csg.md | sort -u > /tmp/all_csgs.txt

# Extract CSG-IDs referenced by CSRs in csr.md
grep -oE 'CSG-[A-Z]{2,5}-[0-9]{2}' data/csr.md | sort -u > /tmp/csrs_covering.txt

# Check: all CSGs must be covered by at least one CSR
comm -23 /tmp/all_csgs.txt /tmp/csrs_covering.txt
# If output is non-empty, these CSGs lack CSR coverage (orphan goals)
```

**Rule 2: Every gap (Part B) must reference TS-ID or "TARA Analysis"**
```bash
# Extract Part B entries (gaps) from csr.md
grep -A10 'Status: ❌ GAP\|Status: ⚠️ PARTIAL' data/csr.md | grep 'Identified By' > /tmp/gap_sources.txt

# Verify all gaps have "Identified By" field
if grep -q 'Identified By:$' /tmp/gap_sources.txt; then
  echo "❌ ERROR: Some gaps missing Identified By field"
fi
```

**Rule 3: Every CRITICAL/HIGH gap must have Recommendation**
```bash
# Extract CRITICAL/HIGH gaps and verify Recommendation field exists
grep -A15 'Priority: CRITICAL\|Priority: HIGH' data/csr.md | grep -c 'Recommendation:' > /tmp/rec_count.txt
# Compare count with CRITICAL+HIGH gap count (should match)
```

**Rule 4: CSR-ID numbering is sequential within each category**
```bash
# Extract CSR-IDs and check for duplicates
grep -oE 'CSR-[A-Z]+-[0-9]{2}' data/csr.md | sort | uniq -d
# If output is non-empty, duplicate CSR-IDs exist (numbering error)
```

**Orphan CSG Detection**:

If a CSG has NO related CSRs, investigate:
1. Was the RT treatment actually pure Accept / pure Transfer? (If yes, there should be no CSG under policy A; re-check the upstream `csg` output.)
2. Was the CSG addressed by design specification controls? (Part A only, no Part B gaps)
3. Was CSG derivation incomplete? (Missing decomposition in Step 3)

**Example Orphan**:
```
CSG-IMM-03: Immobilizer Ransomware Protection
  Related CSR-IDs: [NONE]
  → Investigation: upstream RT-IMM-003 may have been classified as pure Accept / pure Transfer
  → Expected under policy A: no new CSG should exist; claim belongs in data/rt.md
  → Action: re-check Phase 6 output and retire/correct the orphan CSG if it only mirrors an RT claim
```

**Traceability Documentation Checklist**:
- [ ] CSG→CSR traceability matrix created (all CSGs covered)
- [ ] Every CSR entry has "Related CSG-IDs" field populated
- [ ] Every gap (Part B) has "Identified By" field populated with TS-ID
- [ ] Every CRITICAL/HIGH gap has detailed "Recommendation" (4 elements)
- [ ] Every IMPLEMENTED control (Part A) has "Source" reference
- [ ] No duplicate CSR-IDs (sequential numbering within category)

**Output of Step 6**: Validated traceability matrix and completeness confirmation

---

## CSR Category Taxonomy

CSRs are organized by functional domain categories (not geographical domains like CSG):

| Category Code | Category Name | Typical Technologies | Example CSRs |
|--------------|---------------|---------------------|--------------|
| **CRYPTO** | Cryptography | AES, RSA, ECC, HMAC, key management | CSR-CRYPTO-01: AES-256-GCM encryption |
| **ACCESS** | Access Control | RBAC, ABAC, ACL, OAuth, permissions | CSR-ACCESS-01: Location data authorization |
| **AUTH** | Authentication | Password, MFA, mTLS, FIDO2, biometric | CSR-AUTH-01: User authentication MFA |
| **AUDIT** | Audit and Logging | Syslog, tamper-resistant logs, SIEM | CSR-AUDIT-01: Location access logging |
| **COMMS** | Communications Security | TLS, AUTOSAR SecOC, IPsec, VPN | CSR-COMMS-01: CAN message authentication |
| **NETWORK** | Network Security | Firewall, IDS/IPS, DoS protection, segmentation | CSR-NETWORK-01: DoS attack detection |
| **OTA** | Over-the-Air Updates | Code signing, secure boot, rollback protection | CSR-OTA-01: Firmware signature verification |
| **CONFIG** | Configuration Management | Whitelisting, input validation, hardening | CSR-CONFIG-01: CAN gateway filtering |
| **SYSTEM** | System Hardening | SELinux, sandboxing, privilege separation | CSR-SYSTEM-01: CPU reservation for eCall |
| **CLOUD** | Cloud Security | API authentication, data isolation, backup | CSR-CLOUD-01: Cloud sync authentication |
| **CERT** | Certificate Management | PKI, certificate lifecycle, trust chain | CSR-CERT-01: OEM certificate chain |
| **REDUNDANCY** | Redundancy and Failover | Hot standby, automatic failover, self-test | CSR-REDUNDANCY-01: eCall failover |
| **PRIVACY** | Privacy Protection | Data minimization, anonymization, consent | CSR-PRIVACY-01: Telemetry anonymization |
| **PHYSICAL** | Physical Security | Anti-tamper, secure enclosure, debug port disable | CSR-PHYSICAL-01: JTAG port disablement |
| **CAMERA** | Camera Security | HAL signing, frame validation, lens tampering | CSR-CAMERA-01: Camera HAL verification |

**Category Selection Guidelines**:

**Primary Function**: Choose category based on the CSR's primary security function, not the affected component.
- ❌ Wrong: CSR-CAN-01 (CAN domain) → Should be CSR-COMMS-01 (communication security function)
- ✅ Right: CSR-COMMS-01 (AUTOSAR SecOC for CAN message authentication)

**Multiple Categories**: If a CSR spans multiple categories, use the MOST SPECIFIC category.
- Example: "Implement AES-256 encryption for OTA firmware updates"
  - Could be CRYPTO (encryption) OR OTA (firmware updates)
  - Choose OTA (more specific to context)

---

## Common Pitfalls and Best Practices

### ❌ DON'T: Create CSRs Without Tracing to CSG

**Wrong**: "Implement password complexity rules (8+ chars, mixed case, numbers, symbols)."

**Problem**: No link to CSG. Unclear WHICH security goal this addresses.

**Right**: 
```
CSR-AUTH-02: Password Complexity Rules
- Related CSG-IDs: CSG-BCK-01 (Backend API Authentication)
- Description: Implement password complexity requirements...
```

**Rationale**: Every CSR must trace back to at least one CSG. Orphan CSRs indicate incomplete analysis.

---

### ❌ DON'T: Specify CSG-Level Abstractions in CSR

**Wrong**: "The system shall protect location data." (CSG-level)

**Right**: "Implement AES-256-GCM encryption for location data with PBKDF2 key derivation (100,000 iterations)." (CSR-level)

**Rationale**: CSRs are implementation requirements. If it doesn't mention specific technology/parameters, it belongs in CSG.

---

### ❌ DON'T: Omit Verification Criteria

**Wrong**: "Implement encryption for sensitive data."

**Right**: "Implement AES-256-GCM encryption for location data. Verify by extracting eMMC storage and attempting to decode files without decryption key (should produce undecodable binary)."

**Rationale**: CSRs must be testable. Include verification method for each requirement.

---

### ❌ DON'T: Mix Part A (Implemented) and Part B (Gaps) in Same Entry

**Wrong**:
```
CSR-CLOUD-01: Cloud Security
- Status: ✅ IMPLEMENTED (mTLS), ❌ GAP (MFA)
```

**Right**: Create TWO entries:
```
Part A:
CSR-CLOUD-01: 云端mTLS认证
- Status: ✅ IMPLEMENTED
- Description: [Chinese design spec text]
- Source: Design Specification Section 6.1

Part B:
CSR-CLOUD-02: Cloud MFA Enforcement
- Status: ❌ GAP
- Description: [English gap analysis]
- Priority: CRITICAL
- Identified By: TS-BCK-001
```

**Rationale**: Part A and Part B have different field structures. Keep them separate for clarity.

---

### ✅ DO: Use 4-Element Recommendation Template for Gaps

**Template**:
```
Recommendation:
  WHAT: [Technology/control to implement]
  HOW: [Parameters, configuration, algorithm details]
  WHERE: [Component, layer, interface]
  VERIFY: [Test case with pass/fail criteria]
```

**Example**:
```
Recommendation:
  WHAT: Implement TOTP-based Multi-Factor Authentication (MFA) using RFC 6238.
  HOW: 30-second time window, 6-digit OTP codes, mandatory enrollment for all users.
  WHERE: Backend authentication service (AWS Cognito).
  VERIFY: Test login with correct password but wrong OTP (should fail).
```

**Rationale**: Structured recommendations ensure actionable, testable guidance for development teams.

---

### ✅ DO: Preserve Original Language in Part A

**Part A entries** (implemented controls from design specifications):
- Keep **Chinese text** exactly as written in design specification
- Do NOT translate to English
- Maintain traceability to original document

**Part B entries** (gaps identified through TARA):
- Use **English** (TARA standard language)
- Technical terminology in English for consistency with ISO 21434

**Rationale**: Part A serves as audit trail to design specification. Part B serves as TARA work product.

---

### ✅ DO: Link Gaps Back to Originating Threat Scenarios

**Every gap must reference**:
- **Identified By**: TS-ID or "TARA Analysis"
- **Priority**: Based on TS-ID Risk Value

**Example**:
```
CSR-CRYPTO-04: DVR Video Encryption
- Status: ❌ GAP
- Identified By: TS-IVI-003 (Physical Storage Extraction)
- Priority: HIGH (RV 3)
```

**Rationale**: Priority assignment requires traceability to threat scenarios. Without TS-ID, priority is arbitrary.

---

### ✅ DO: Validate Priority Traceability

- Confirm every gap priority aligns with its linked TS/RT context.
- If priority is still pending upstream RT completion, mark it explicitly.
- Do not infer quality from target percentage distributions alone.

---

## Quick Reference

### 6-Step Methodology Summary

1. **Read CSG** → Extract security properties by CIA Property (Confidentiality/Integrity/Availability)
2. **Read Design Specs** → Document implemented controls from specifications (Part A entries)
3. **Decompose CSG** → Derive technical CSRs (technology-specific, parameterized, testable)
4. **Gap Analysis** → Classify as IMPLEMENTED (Part A), PARTIAL (Part B), or GAP (Part B)
5. **Carry Priority Context** → Record CRITICAL/HIGH/MEDIUM/LOW from linked TS/RT analysis
6. **Document Traceability** → Verify every CSG has ≥1 CSR, every gap has TS-ID

### CIA Property → CSR Category Mapping

| CIA Property | Primary Categories | Secondary Categories |
|--------------|-------------------|---------------------|
| Confidentiality | CRYPTO, ACCESS, AUTH | AUDIT, PRIVACY, CLOUD |
| Integrity | CRYPTO, COMMS, CONFIG | OTA, CERT, SYSTEM |
| Availability | NETWORK, SYSTEM, REDUNDANCY | COMMS, CLOUD |

### Gap Status Classification

| Status | Coverage | Part | Action |
|--------|---------|------|--------|
| ✅ IMPLEMENTED | 100% | Part A only | Document in Part A with Source |
| ⚠️ PARTIAL | 50-99% | Part A + Part B | Document control in Part A, gap in Part B |
| ❌ GAP | 0-49% | Part B only | Document gap in Part B with Priority |

### Priority Reminder

- Copy priority from the linked TS/RT context.
- If upstream RT is incomplete, mark the CSR as pending RT completion.
- Do not recreate a separate RV-to-priority policy in CSR.

### CSR Quality Checklist

- ✅ Technology-specific (AES-256, RSA-2048, TLS 1.3)
- ✅ Parameterized (key size, iteration count, timeout)
- ✅ Testable (verification criteria with pass/fail)
- ✅ Component-specific (tied to architecture)
- ✅ Traceable (links to CSG-ID)

### Recommendation Template (Part B Gaps)

```
WHAT: [Technology/control to implement]
HOW: [Parameters, configuration details]
WHERE: [Component, layer, interface]
VERIFY: [Test case with acceptance criteria]
```

---

## References

- **ISO 21434:2021** - Road vehicles — Cybersecurity engineering
  - Clause 9.4: Cybersecurity specifications (CSR derivation)
  - Clause 9.5: Verification of cybersecurity specifications
  - Clause 15.9: Cybersecurity goals and cybersecurity requirements
- **AUTOSAR Classic Platform** - SecOC (Secure Onboard Communication) specification
- **NIST Cybersecurity Framework (CSF)** - Control catalogues and implementation guidance
- **OWASP** - Application Security Verification Standard (ASVS)
- **GDPR** (EU 2016/679) - Privacy controls and data protection requirements
- **GB 44495** - Automotive data security requirements (China)
- **UN R155** - Cyber Security Management System (CSMS) regulatory requirements

---

*End of CSR Derivation Methodology Guide*
