# Cybersecurity Requirement Schema - ISO 21434 TARA

**Authority note**: This is the authoritative source for CSR field definitions, category names, and validation rules. `SKILL.md` and `assets/TEMPLATE.md` should point here rather than restating schema rules.

This document defines the required fields for Cybersecurity Requirement (CSR) documentation in ISO 21434 TARA (Threat Analysis and Risk Assessment) workflows, aligned with Clause 9.4 (Cybersecurity specifications).

---

## Overview

Cybersecurity Requirements (CSRs) represent specific technical controls derived from Cybersecurity Goals (CSGs). They define how to implement security objectives through concrete technologies, configurations, and validation criteria.

**Key Characteristics**:
- CSRs are formulated as **specific technical controls** with implementation details
- Each CSR implements one or more CSGs (M:N relationship)
- Each CSR is allocated to an item or component so implementation ownership is auditable
- CSRs focus on **how** to protect, not **what** to protect (inverse of CSG)
- CSRs are technology-specific and implementation-dependent
- CSRs exist in two forms: **Part A (Implemented Controls)** and **Part B (Identified Gaps)**

**Relationship to Other TARA Entities**:
```
Cybersecurity Goals (CSG) → Cybersecurity Requirements (CSR) → Security Controls Implementation
       |                              |                                     |
   What to protect?             How to protect?                   Verification evidence
```

---

## CSR Entry Types

CSR catalogue contains TWO distinct entry types:

### Part A: Implemented Controls (IMPLEMENTED status only)

**Source**: Design specifications, engineering documentation, supplier declarations

**Purpose**: Document existing security controls already implemented in the system

**Allocation Rule**: Every Part A entry must identify where the control is implemented. Use the `Source` or `Description` field to state the item, component, layer, or interface that owns the control.

**Fields** (7 total):
1. CSR-ID
2. Title (derived from Description or Section heading)
3. Status (✅ IMPLEMENTED only)
4. Category
5. Description (Chinese from design specification)
6. Source (Design specification reference)
7. (Related CSG-IDs - optional, added during traceability mapping)

**Example Count**: 56 entries in reference catalogue

---

### Part B: Identified Gaps (GAP or PARTIAL status)

**Source**: TARA analysis, threat scenario mitigation, CSG decomposition

**Purpose**: Identify missing or incomplete security controls requiring implementation

**Allocation Rule**: Every Part B entry must identify where the missing control should be implemented. The `Recommendation` field must include the component, layer, interface, or item that owns the fix.

**Fields** (9 total):
1. CSR-ID
2. Title (descriptive gap name)
3. Status (❌ GAP or ⚠️ PARTIAL)
4. Priority (CRITICAL, HIGH, MEDIUM, LOW)
5. Category
6. Description (English gap analysis with impact)
7. Identified By (TS-ID reference or "TARA Analysis")
8. Recommendation (4-element technical mitigation)
9. (Related CSG-IDs - optional, added during traceability mapping)

**Example Count**: 211 entries in reference catalogue

---

## Required Fields - Part A (Implemented Controls)

Every Part A CSR entry must include ALL 7 required fields:

### 1. CSR-ID

**Format**: `CSR-[CATEGORY]-[NN]`

**Description**: Unique identifier for the Cybersecurity Requirement following a domain-functional category naming convention. CSR-IDs use 2-digit numbers within each category for sequential tracking.

**Category Codes** (15+ valid codes):

**Cryptographic Controls**:
- `CRYPTO` - Encryption, hashing, key management
- `CERT` - Certificate handling, PKI infrastructure

**Communication Security**:
- `COMMS` - CAN, UDS, V2X communication security
- `NETWORK` - IP, TCP/UDP, DNS network layer security

**Access Control**:
- `ACCESS` - Authorization, permission management
- `AUTH` - Authentication mechanisms
- `AUDIT` - Logging, monitoring, event recording

**System Security**:
- `SYSTEM` - OS hardening, process isolation, privilege management
- `CONFIG` - Configuration management, secure defaults
- `BOOT` - Secure boot, verified boot chain

**Application Security**:
- `OTA` - Over-the-air update security
- `APP` - Application sandboxing, third-party app controls
- `DATA` - Data protection, storage encryption

**Physical Security**:
- `PHY` - Physical interface protection (USB, SD card, OBD)
- `DEBUG` - Debug interface security (JTAG, UART)

**Specialized Domains**:
- `CAMERA` - Camera security (DVR, sentinel mode, HAL)
- `CLOUD` - Cloud sync, backend API security
- `SHARE` - Data sharing, cross-domain communication
- `CHILD` - Children's data protection
- `CONNECT` - Connectivity and remote control security
- `REDUNDANCY` - High-availability and failover controls
- `STORAGE` - Secure storage mechanisms

**Example**: `CSR-CRYPTO-01`, `CSR-COMMS-15`, `CSR-ACCESS-05`

**Rules**:
- Use zero-padded 2-digit numbers (01, 02, ..., 99)
- Category code must match functional domain (not threat domain like TS-IDs)
- CSR-IDs are independent of CSG numbering (1:N relationship)
- One CSG may decompose into 3-10 CSRs across multiple categories
- Numbering should be sequential within each category

**ID Allocation Strategy**:
```
CSR-CRYPTO-01  ← First cryptographic control
CSR-CRYPTO-02  ← Second cryptographic control
CSR-COMMS-01   ← First communication control
CSR-COMMS-15   ← Fifteenth communication control (SecOC)
```

**Category Selection Rules**:
- Choose category by **primary security function**, not threat origin
- If CSR addresses multiple functions, use the **most critical** category
- Document cross-category applicability in Description field

**Validation**:
- CSR-ID format must match regex: `^CSR-[A-Z]{3,10}-\d{2}$`
- No duplicate CSR-IDs allowed in catalogue
- Category code must exist in valid category list

---

### 2. Title

**Format**: Human-readable text (maximum 100 characters)

**Description**: Concise, descriptive name for the Cybersecurity Requirement identifying the control or gap. For Part A entries, title may be implicit (derived from design specification section heading) or explicit.

**Example**: 
- "部件支持OEM证书链加载和存储" (Certificate Loading Support)
- "车辆应对内部网络进行区域划分并对区域边界进行防护" (Network Segmentation)
- "对于CAN/CANFD通信的控制器,应实施车内ECU通信校验或通信认证" (CAN Communication Authentication)

**Rules**:
- For Part A: Preserve original Chinese title from design specification
- For Part B: Create descriptive English title identifying the gap
- Keep under 100 characters for readability
- Use noun phrases describing the control mechanism
- Be specific enough to distinguish from similar CSRs
- Include key technology or standard if relevant (e.g., "SecOC", "mTLS", "RPMB")

**Naming Patterns for Part A** (Chinese):
- `[功能] + [安全机制]` - "证书 + 加载和存储"
- `[系统] + [防护措施]` - "内部网络 + 区域划分"
- `[通信协议] + [安全要求]` - "CAN/CANFD + 通信认证"

---

### Optional Allocation Target

Add this context field to every CSR when allocation is known:

```markdown
**Allocation Target**: [Item | Component | Layer | Interface | Supplier-owned subsystem]
```

Rules:
- Part A entries must identify where implemented control exists through this field, `Source`, or `Description`.
- Part B entries must identify where missing control belongs through this field or `Recommendation`.
- Use `Item` for vehicle-level allocation and `Component` for narrower supplier or subsystem allocation.
- Do not use allocation target to replace `Related CSG-IDs` or `Identified By` traceability.

---

### 3. Status

**Format**: Emoji + Text: `✅ IMPLEMENTED` (Part A only)

**Description**: Implementation status of the security control. Part A entries are ALWAYS marked as IMPLEMENTED (controls exist and are documented).

**Valid Value for Part A**:
- `✅ IMPLEMENTED` - Control is fully implemented and documented in design specification

**Example**:
```markdown
**Status**: ✅ IMPLEMENTED
```

**Rules**:
- Part A entries MUST use `✅ IMPLEMENTED` status only
- Emoji prefix (✅) is required for visual consistency
- Status must be on its own line with bold formatting
- If control is partially implemented or missing, it belongs in Part B (not Part A)

**Validation**:
- All Part A entries must have Status = `✅ IMPLEMENTED`
- No ⚠️ PARTIAL or ❌ GAP statuses allowed in Part A
- If design specification documents a control with known gaps, create TWO entries:
  - Part A: Document the implemented portion with ✅ IMPLEMENTED
  - Part B: Document the gap portion with ⚠️ PARTIAL

---

### 4. Category

**Format**: Category name string matching CSR-ID prefix

**Description**: Functional category for grouping related requirements in the catalogue output.

**Valid Categories** (must match CSR-ID prefix):

| Category Code | Category Name | Description |
|---------------|--------------|-------------|
| CRYPTO | Cryptographic Controls | Encryption, hashing, key management |
| CERT | Certificate Management | PKI, certificate handling, trust chains |
| COMMS | Communications Security | CAN, UDS, V2X message security |
| NETWORK | Network Security | IP, TCP/UDP, DNS, routing security |
| ACCESS | Access Control | Authorization, permission management |
| AUTH | Authentication | Identity verification mechanisms |
| AUDIT | Audit and Logging | Event recording, monitoring, alerting |
| SYSTEM | System Security | OS hardening, process isolation |
| CONFIG | Configuration Management | Secure defaults, policy enforcement |
| BOOT | Secure Boot | Boot chain verification, anti-rollback |
| OTA | OTA Security | Software update security |
| APP | Application Security | App sandboxing, third-party controls |
| DATA | Data Protection | Storage encryption, data lifecycle |
| PHY | Physical Security | Interface protection (USB, SD, OBD) |
| DEBUG | Debug Security | JTAG, UART, diagnostic port controls |
| CAMERA | Camera Security | DVR, sentinel mode, HAL protection |
| CLOUD | Cloud Security | Backend API, cloud sync controls |
| SHARE | Data Sharing | Cross-domain communication |
| CHILD | Child Safety | Children's data protection |
| CONNECT | Connectivity Security | Remote control, telematics |
| REDUNDANCY | High Availability | Failover, fault tolerance |
| STORAGE | Storage Security | Secure storage mechanisms |

**Example**:
```markdown
**Category**: Cryptographic Controls
**Category**: Communications Security
**Category**: Access Control
```

**Rules**:
- Category name must match the CSR-ID prefix
- Use full category name (not abbreviation) for readability
- Category groups CSRs for section organization in output document
- One CSR has exactly one category (no multi-category CSRs)

**Validation**:
- Category must exist in valid category table above
- Category must match CSR-ID prefix (CSR-CRYPTO-01 → "Cryptographic Controls")
- All CSRs with same category code must have identical category name

---

### 5. Description

**Format**: Multi-sentence Chinese text from design specification (Part A)

**Description**: Detailed description of the implemented security control, preserving original Chinese text from the source design specification for traceability.

**Example (CRYPTO)**:
```markdown
**Description**: 流程规范:证书与密钥灌装严格遵循《PKI证书灌装流程规范-v1.6》。
安全存储:所有敏感密钥及证书私钥均写入RPMB (Replay Protected Memory Block) 区域或HSM安全存储区。
RPMB具备防重放、防篡改及访问鉴权特性,确保密钥无法被普通文件系统工具读取或修改。
```

**Example (COMMS)**:
```markdown
**Description**: 实施严格的硬件绑定策略。每台ICC在产线灌装唯一的设备证书,并与云端数据库绑定。
若攻击者尝试物理替换ICC硬件,由于新硬件内无合法的预置证书,无法通过TSP平台的mTLS双向认证,从而被云端拒绝接入。
```

**Example (COMMS with technical details)**:
```markdown
**Description**: CAN/CANFD总线:建立基于CAN ID的频率监控与信号值合理性校验机制。检测到非法帧或泛洪攻击时,自动丢弃异常报文。
若触发Bus Off;具备Bus Off后的自动恢复与重试机制。
WiFi:启用动态黑名单与速率限制功能。当检测到同一源IP在短时间内发送大量连接请求(泛洪攻击)时,自动将其加入黑名单并在老化时间内丢弃其所有报文,保障正常业务可用性。
```

**Rules**:
- Preserve original Chinese text from design specification (do NOT translate)
- Length: 2-5 sentences typical (may be longer for complex controls)
- Include technical implementation details (algorithms, key sizes, storage locations)
- Include compliance or validation methods if mentioned in specification
- Use line breaks for readability (separate logical sections with Chinese punctuation)
- May include English acronyms in parentheses (RPMB, HSM, mTLS, etc.)

**Content Structure**:
1. **Control mechanism** (what is implemented)
2. **Technical details** (how it works, parameters, configurations)
3. **Security properties** (why it's secure, what attacks it prevents)
4. **Compliance/validation** (if applicable)

**Translation Note**:
- Keep original Chinese for traceability to source document
- English translation may be added in parentheses for key terms
- Do NOT replace Chinese with English (breaks traceability)

**Validation**:
- Description must be non-empty (minimum 20 characters)
- Description must be in Chinese (primary language)
- Description should reference specific technologies, standards, or mechanisms
- Vague descriptions ("系统安全", "实施保护") are insufficient

---

### 6. Source

**Format**: Reference string to design specification or source document

**Description**: Citation to the authoritative source document where this implemented control is documented. Enables traceability and verification.

**Examples**:
```markdown
**Source**: Design Specification (信息安全设计规范说明书)
**Source**: Design Specification Section 3.2.1 "Certificate Management"
**Source**: Supplier Declaration (Qualcomm QAM8295 Security Features)
**Source**: Component Datasheet (Infineon TMS-T97-111A Secure Element)
**Source**: PKI Certificate Injection Process Specification v1.6
**Source**: Design Specification Section 5.4 "CAN Gateway Filtering Rules"
```

**Rules**:
- Minimum: "Design Specification (信息安全设计规范说明书)" (generic reference)
- Preferred: Specific section reference ("Section 3.2.1")
- For supplier-provided controls: Reference supplier documentation
- For component-level controls: Reference component datasheets
- Every IMPLEMENTED control MUST have a Source reference
- Source or Description must identify the allocation target: Item, Component, layer, interface, or supplier-owned subsystem

**Source Types**:

| Source Type | Format | Use Case |
|-------------|--------|----------|
| **Generic Design Spec** | `Design Specification (信息安全设计规范说明书)` | Default for controls without specific section |
| **Specific Section** | `Design Specification Section 3.2.1 "Certificate Management"` | Precise traceability to design document |
| **Supplier Declaration** | `Supplier Declaration (Qualcomm QAM8295 Security Features)` | Third-party component security features |
| **Component Datasheet** | `Component Datasheet (Infineon TMS-T97-111A Secure Element)` | Hardware security module specifications |
| **Process Specification** | `PKI Certificate Injection Process Specification v1.6` | Operational security processes |
| **Test Report** | `Penetration Test Report 2026-Q1 Section 4.2` | Validation evidence |

**Purpose**:
- Enables audit and verification (reviewers can validate implementation)
- Supports compliance documentation (evidence for UN R155, ISO 21434)
- Traceability to authoritative source (no unverified controls)

**Validation**:
- Every Part A entry MUST have a non-empty Source field
- Source reference should be specific enough to locate the control documentation
- If Source = "Design Specification (信息安全设计规范说明书)" (generic), consider adding section reference

---

### 7. Related CSG-IDs (Optional)

**Format**: List of Cybersecurity Goal IDs from CSG catalogue (one per line)

**Description**: The Cybersecurity Goals that this CSR implements or contributes to. This field establishes the M:N mapping between CSRs and CSGs. Optional for initial CSR documentation; typically added during traceability matrix creation.

**Example**:
```markdown
**Related CSG-IDs**:
- CSG-IVI-01 (Location Data Confidentiality)
- CSG-BCK-02 (Cloud Service Authentication)
```

**Example (single CSG)**:
```markdown
**Related CSG-IDs**:
- CSG-CAN-01 (CAN Message Authentication and Integrity)
```

**Rules**:
- Optional field - may be empty during initial CSR creation
- Must reference valid CSG-IDs that exist in `data/csg.md` (when CSG catalogue exists)
- Include both the ID and the CSG title for clarity
- List all CSGs that this CSR contributes to (N:M relationship)
- Order by domain, then by ID number
- Typical range: 1-3 CSG-IDs per CSR (if more than 5, CSR may be too broad)

**CSR-to-CSG Relationship** (1:N decomposition):
```
CSG-IVI-01: Location Data Confidentiality
  ↓ (implements)
CSR-CRYPTO-01: AES-256 encryption for location data
CSR-ACCESS-01: Role-based access control for location API
CSR-AUDIT-01: Location data access logging
CSR-CLOUD-03: Encrypted cloud sync for location history
```

**When to Populate**:
- During traceability matrix creation (after both CSG and CSR catalogues exist)
- When linking TARA outputs to implementation evidence
- When preparing compliance documentation for ISO 21434 audit

**Validation**:
- Every CSG-ID listed must exist in `data/csg.md` (if CSG catalogue exists)
- Every CSG should be implemented by at least one CSR (no orphan CSGs)
- If CSG catalogue doesn't exist yet, leave field empty or mark as `[TBD]`

---

## Required Fields - Part B (Identified Gaps)

Every Part B CSR entry must include ALL 9 required fields:

### 1. CSR-ID

**Same format as Part A**: `CSR-[CATEGORY]-[NN]`

**Rules**:
- CSR-ID numbering is INDEPENDENT between Part A and Part B
- Part A and Part B may have same CSR-ID prefix (e.g., both have CSR-CRYPTO-01)
- CSR-IDs within Part B should be sequential within each category
- Choose category based on primary gap mitigation function

**Example**:
```
Part A: CSR-CRYPTO-01 (IMPLEMENTED: RPMB key storage)
Part B: CSR-CRYPTO-01 (GAP: DVR video encryption) ← Different control, same ID prefix OK
```

---

### 2. Title

**Format**: Human-readable English text (maximum 100 characters)

**Description**: Concise, descriptive name for the security gap or missing control.

**Example**: 
- "Cloud Sync Authentication"
- "DVR Video Encryption"
- "Camera HAL Behavioral Sandboxing"
- "Sentinel Mode Sensor Tampering Detection"
- "Multi-Factor Authentication (MFA) Enforcement"

**Rules**:
- Use English (Part B is for TARA analysis, international standard)
- Keep under 100 characters
- Use noun phrases describing the missing control
- Include key technology if relevant (MFA, mTLS, SecOC, etc.)
- Be specific enough to distinguish from similar gaps

**Naming Patterns for Part B** (English):
- `[Technology] + [Function]` - "MFA + Enforcement"
- `[Component] + [Security Property]` - "Camera HAL + Sandboxing"
- `[Attack] + Detection/Prevention` - "Sensor Tampering + Detection"

---

### 3. Status

**Format**: Emoji + Text: `❌ GAP` or `⚠️ PARTIAL`

**Description**: Implementation status of the security control. Part B entries indicate missing or incomplete controls.

**Valid Values for Part B**:
- `❌ GAP` - Control is not implemented at all (complete gap)
- `⚠️ PARTIAL` - Control is partially implemented (incomplete coverage)

**Example (GAP)**:
```markdown
**Status**: ❌ GAP
```

**Example (PARTIAL)**:
```markdown
**Status**: ⚠️ PARTIAL
```

**Rules**:
- Part B entries MUST use `❌ GAP` or `⚠️ PARTIAL` status (never ✅ IMPLEMENTED)
- Emoji prefix is required for visual consistency
- Status must be on its own line with bold formatting

**Decision Criteria - GAP vs PARTIAL**:

**Use ❌ GAP when**:
- Control does not exist at all (no implementation)
- No partial implementation to build upon
- Starting from scratch is required
- Example: "DVR video encryption" when no encryption exists

**Use ⚠️ PARTIAL when**:
- Some aspects of control are implemented
- Critical gaps remain in existing implementation
- Enhancement/completion required (not full rebuild)
- Example: "Cloud sync authentication" with mTLS but no MFA

**Validation**:
- All Part B entries must have Status = `❌ GAP` or `⚠️ PARTIAL`
- If control is fully implemented, it belongs in Part A (not Part B)
- Status must align with Description (GAP = no implementation mentioned, PARTIAL = existing + gap)

---

### 4. Priority

**Format**: One of: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`

**Description**: Implementation priority carried into the CSR catalogue from the originating TS/RT context. In this repository, CSR should consume upstream prioritization rather than define a separate local policy.

**Valid Values**:
- `CRITICAL`
- `HIGH`
- `MEDIUM`
- `LOW`

**Example**:
```markdown
**Priority**: CRITICAL
**Priority**: HIGH
**Priority**: MEDIUM
**Priority**: LOW
```

**Priority provenance**:
- Derive or copy the priority from the linked TS/RT analysis.
- Do not maintain a second RV-to-priority policy inside CSR.
- If upstream RT is incomplete, mark the CSR as pending RT completion rather than inventing a local priority.

**Validation**:
- Every Part B entry MUST have a Priority value.
- Priority must align with the linked TS/RT analysis.
- If upstream RT is unavailable, the entry should explicitly indicate pending RT completion rather than using an invented local priority.

---

### 5. Category

**Same format as Part A**: Category name string matching CSR-ID prefix

**See Part A Section 4 for full category table and validation rules.**

---

### 6. Description

**Format**: Multi-sentence English text with gap analysis (Part B)

**Description**: Detailed description of the security gap, including implementation status (if PARTIAL), gap description (what's missing), and impact (why it matters, which threat it enables).

**Structure** (3 elements for GAP, 4 elements for PARTIAL):

**For ❌ GAP entries**:
1. **Gap description** (what's missing entirely)
2. **Impact** (why this gap matters, which threat it enables)
3. **Regulatory/compliance context** (if applicable)

**Example (GAP - DVR Encryption)**:
```markdown
**Description**: DVR video storage lacks encryption and integrity protection. Videos stored 
in plaintext on eMMC storage enabling physical extraction attacks. No cryptographic binding 
of GPS/timestamp metadata allowing evidence tampering. Impacts evidence admissibility and 
privacy protection (GDPR Article 9 special category data).
```

**Example (GAP - MFA)**:
```markdown
**Description**: Multi-factor authentication (MFA) not enforced for cloud sync accounts. 
Current authentication relies on password-only login enabling credential theft via phishing 
attacks (TS-BCK-001). Lack of MFA violates NIST SP 800-63B Level 2 requirements for 
high-value accounts. RV 5 gap requiring immediate remediation.
```

---

**For ⚠️ PARTIAL entries**:
1. **Current implementation** (what exists already)
2. **Gap description** (what's missing or incomplete)
3. **Impact** (why the gap matters despite partial implementation)
4. **Compliance context** (if applicable)

**Example (PARTIAL - Cloud Authentication)**:
```markdown
**Description**: Cloud sync authentication implemented via mTLS and password-based login. 
Gap: Multi-factor authentication (MFA) not enforced, enabling credential theft via phishing 
attacks (TS-BCK-001). Current implementation satisfies basic authentication but insufficient 
for RV 5 credential theft scenarios. NIST SP 800-63B requires MFA for high-value accounts.
```

**Example (PARTIAL - Camera Firmware)**:
```markdown
**Description**: Camera firmware versioning tracked via metadata files but no anti-rollback 
enforcement at component level. Gap: Attacker can downgrade camera firmware to vulnerable 
version despite valid signatures (TS-CAMERA-003). Firmware version checking exists but lacks 
bootloader-level enforcement preventing rollback attacks. UN R155 requires anti-rollback 
protection for all ECU firmware.
```

**Example (PARTIAL - Camera HAL)**:
```markdown
**Description**: Camera HAL operational as standard Android Camera HAL but lacks code signing 
and behavioral sandboxing. Gap: Malicious HAL indistinguishable from legitimate HAL enabling 
unauthorized camera access and privacy violations (TS-CAMERA-002). HAL permission framework 
exists but no cryptographic authentication of HAL binaries or runtime capability restrictions.
```

---

**Rules**:
- Use English (Part B is for TARA analysis, international standard)
- Length: 2-5 sentences (be specific, avoid generic statements)
- Reference specific threat scenarios (TS-IDs) when possible
- Cite regulatory requirements (UN R155, ISO 21434, GDPR, GB 44495, NIST)
- Include technical specifics (algorithms, protocols, attack vectors)
- Explain impact (privacy, safety, financial, operational)

**Content Quality Checklist**:
- ✅ Identifies specific technical gap (not "lacks security")
- ✅ References threat scenario (TS-ID) that exploits this gap
- ✅ Explains impact on CIA properties or SFOP dimensions
- ✅ Cites relevant standards or regulations
- ✅ Uses precise technical terminology

**Bad Example**:
> "System security needs improvement for this component."

**Why Bad?**: No specifics, no threat linkage, no impact analysis, not actionable.

**Validation**:
- Description must be non-empty (minimum 50 characters for Part B)
- Description should reference at least one threat scenario or impact
- Vague descriptions without technical specifics are insufficient
- PARTIAL entries must explicitly state what exists AND what's missing

---

### 7. Identified By

**Format**: `TS-[DOMAIN]-[NNN]` or `TARA Analysis`

**Description**: Reference to the threat scenario or analysis that identified this security gap. Establishes traceability from gap → threat → damage → risk.

**Examples**:
```markdown
**Identified By**: TS-BCK-001 (Credential Theft via Phishing)
**Identified By**: TS-CAMERA-002 (Malicious Camera HAL Injection)
**Identified By**: TS-IVI-003 (Physical Storage Extraction)
**Identified By**: TARA Analysis
```

**Rules**:
- Preferred: Reference specific TS-ID when gap is identified through threat modeling
- Alternative: Use "TARA Analysis" for generic gaps not linked to specific threat
- TS-ID must exist in `data/ts.md` (if threat catalogue exists)
- Priority must align with the linked TS/RT context

**When to Use TS-ID vs "TARA Analysis"**:

**Use TS-ID** (preferred):
- Gap discovered during threat scenario enumeration
- Specific attack path requires this mitigation
- Traceability to TS/RT context needed for priority justification
- Example: "TS-BCK-001" identifies MFA gap through credential theft threat

**Use "TARA Analysis"** (fallback):
- Generic gap not tied to specific threat (e.g., hardening best practice)
- Gap identified through design review, not threat modeling
- Cross-cutting gap affecting multiple threat scenarios
- Example: "TARA Analysis" for general secure boot requirements

**Validation**:
- Every Part B entry MUST have a non-empty Identified By field
- If TS-ID reference used, TS-ID must exist in `data/ts.md`
- Priority must align with the linked TS/RT context
- If upstream RT is incomplete, mark the CSR as pending RT completion rather than inventing a local priority

**Traceability Chain**:
```
DS-BCK-001 (Credential Theft Damage)
  ↓
TS-BCK-001 (Phishing Attack)
  ↓
CSR-CLOUD-02 (MFA Enforcement Gap - priority carried from RT context)
  ↓
Recommendation: Implement TOTP-based MFA
```

**Purpose**:
- Justifies gap priority (link to TS/RT context)
- Enables threat-driven remediation planning using upstream treatment decisions
- Supports compliance audit (demonstrates threat analysis completeness)
- Links implementation requirements to risk assessment

---

### 8. Recommendation

**Format**: Multi-sentence technical mitigation with 4 required elements

**Description**: Specific, actionable, testable technical mitigation for the identified gap. Must include concrete technologies, configuration parameters, implementation locations, and verification criteria.

**Structure** (4 required elements):

1. **What to implement** (specific technology, algorithm, or mechanism)
2. **How to configure** (parameters, key sizes, timeouts, thresholds)
3. **Where to implement** (component, layer, architecture location)
4. **How to verify** (validation criteria, test cases, acceptance criteria)

**Example (CRITICAL gap - MFA)**:
```markdown
**Recommendation**: Implement mandatory TOTP-based MFA for all cloud sync accounts.
- Require MFA enrollment during account creation (no opt-out)
- Support TOTP apps (Google Authenticator, Authy) and SMS backup
- Prefer phishing-resistant MFA (WebAuthn, FIDO2) for high-value accounts
- MFA re-verification required for sensitive operations (account settings, data export)
- Estimated cost: $0.50/user for SMS OTP, $0 for TOTP app
- Validation: Penetration test confirms phishing resistance, 100% MFA adoption rate
```

**Example (CRITICAL gap - DVR Encryption)**:
```markdown
**Recommendation**: Implement AES-256-GCM encryption for DVR video storage with 
cryptographic metadata binding.
- Encrypt video files on-write to eMMC using device-unique key derived from RPMB
- Use AES-256-GCM authenticated encryption (prevents tampering)
- Bind GPS coordinates and timestamps to video via HMAC-SHA256 (integrity protection)
- Store encryption keys in RPMB or HSM (prevent physical extraction)
- Estimated cost: 5% performance overhead on video recording
- Validation: Forensic extraction test confirms encryption strength, metadata binding verification
```

**Example (HIGH gap - Session Security)**:
```markdown
**Recommendation**: Implement enhanced session security with device fingerprinting.
- Short-lived session tokens (7-day maximum lifetime)
- Device fingerprinting binding tokens to specific device (OS version, hardware ID, IP subnet)
- Session invalidation on password change (all devices logged out automatically)
- Concurrent session limits (max 5 devices per account with user-visible dashboard)
- Session activity monitoring (user sees all active sessions with manual revocation control)
- Estimated cost: $0.10/user for session state storage
- Validation: Session hijacking test confirms token binding effectiveness
```

**Example (MEDIUM gap - Sensor Tampering)**:
```markdown
**Recommendation**: Implement sensor tampering detection for Sentinel Mode.
- Monitor accelerometer baseline (detect ultrasonic interference via abnormal spectrum)
- Validate microphone health (detect jamming via noise floor analysis, <-60dBFS threshold)
- Alert driver if sensor anomalies detected (dashboard warning + cloud notification)
- Estimated cost: $5/vehicle for sensor validation firmware
- Validation: Ultrasonic/magnetic interference test confirms detection rate >95%
```

**Rules**:
- Be specific (name technologies: "AES-256-GCM", "TOTP", "WebAuthn", not "encryption")
- Include configuration parameters (key sizes: "256-bit", timeouts: "7-day", thresholds: "-60dBFS")
- Specify implementation location (component: "RPMB", layer: "bootloader", module: "Camera HAL")
- Define testable validation criteria (acceptance: "100% MFA adoption", test: "penetration test confirms")
- Consider cost/feasibility (estimate: "$0.50/user", overhead: "5% performance")
- Prioritize industry standards (NIST, OWASP, ISO) over custom solutions

**4-Element Template**:
```
1. WHAT: Implement [TECHNOLOGY] for [PURPOSE]
   - Specific algorithm, protocol, or mechanism

2. HOW: Configure with [PARAMETERS]
   - Key sizes, timeouts, thresholds, capacities

3. WHERE: Deploy in [COMPONENT/LAYER]
   - Architecture location, system boundary
   - Allocation target: Item, Component, layer, interface, or supplier-owned subsystem

4. VERIFY: Test via [VALIDATION METHOD]
   - Acceptance criteria, test cases, success metrics
```

**Quality Checklist**:
- ✅ Specific technology named (not "improve security")
- ✅ Configuration parameters included (key sizes, durations, thresholds)
- ✅ Implementation location identified (component, layer)
- ✅ Testable outcome defined (validation criteria, acceptance test)
- ✅ Cost/feasibility considered (budget estimate, performance impact)
- ✅ Industry standards referenced (NIST, OWASP, ISO, RFC)

**Bad Example**:
> "Improve security for this component by implementing best practices."

**Why Bad?**:
- No specific technology (what is "best practices"?)
- No configuration parameters (what settings?)
- No implementation location (where to deploy?)
- No validation criteria (how to test?)
- Not actionable (engineering team cannot implement this)

**Validation**:
- Recommendation must be non-empty (minimum 100 characters)
- Recommendation must include at least 2 of 4 elements (What + How, or What + Verify)
- Generic recommendations without technical specifics are insufficient
- Cost estimate or feasibility assessment recommended for CRITICAL/HIGH priorities

---

### 9. Related CSG-IDs (Optional)

**Same format as Part A Section 7**: List of Cybersecurity Goal IDs from CSG catalogue

**See Part A Section 7 for full details.**

**Additional guidance for Part B**:
- Gap CSRs typically link to CSGs via threat scenario traceability:
  - TS-BCK-001 (Credential Theft) → CSG-BCK-02 (Authentication) → CSR-CLOUD-02 (MFA Gap)
- Use Identified By TS-ID to determine Related CSG-IDs:
  - TS-ID → CSG-ID mapping exists in CSG catalogue (Related TS-IDs field)
- If CSG catalogue incomplete, leave empty until traceability matrix creation

---

## Document-Level Structure

CSR catalogue (`data/csr.md`) follows this structure:

### 1. Document Header
- Title: "BAIC B31CS ICC - Cybersecurity Requirements (CSR) Catalogue"
- Metadata: Project, Platform, Generated timestamp, Total count

### 2. Executive Summary (Bilingual EN/CN)
- Overview paragraph (English + Chinese)
- Scope definition (Part A + Part B)

### 3. Key Statistics Table
- Total CSRs count
- ✅ Implemented Controls count (Part A)
- ❌ Identified Gaps count (Part B)
- Priority breakdown (CRITICAL, HIGH, MEDIUM, LOW counts)

### 4. Part A: Implemented Controls
- Section header: "## Part A: Implemented Controls | A部分:已实施控制措施"
- Total count: "**Total: 56 CSRs from Design Specification**"
- Group by Category (### heading)
  - Certificate Management
  - Communications Security
  - Configuration Management
  - Connectivity Security
  - Cryptographic Controls
  - (etc., alphabetically sorted)
- Individual CSR entries (#### heading with CSR-ID + Title)

### 5. Part B: Identified Gaps
- Section header: "## Part B: Identified Gaps | B部分:已识别差距"
- Total count: "**Total: 211 CSRs from TARA Analysis**"
- Group by Category (### heading)
  - Access Control
  - Application Security
  - Audit and Logging
  - Authentication
  - Camera Security
  - (etc., alphabetically sorted)
- Individual CSR entries (#### heading with CSR-ID + Title)

### 6. Traceability Matrix (Optional)
- CSG → CSR mapping table
- Shows which CSRs implement each CSG
- M:N relationship visualization

### 7. Recommendations by Priority (Optional)
- Summary of CRITICAL gaps (actionable list)
- Summary of HIGH priority gaps
- Timeline for remediation

### 8. Compliance Alignment (Optional)
- UN R155 requirement coverage
- ISO 21434 clause mapping
- GDPR/GB 44495 compliance gaps

### 9. Document Control
- Version history
- Approval signatures
- Review schedule

**Heading Hierarchy**:
- `#` (H1): Document title only
- `##` (H2): Major sections (Executive Summary, Part A, Part B, Traceability)
- `###` (H3): Category groups (Certificate Management, Communications Security)
- `####` (H4): Individual CSR entries (CSR-CERT-01: Title)

---

## CSR Category Code Reference

Complete list of valid category codes with descriptions:

| Code | Category Name | Description | Typical Technologies |
|------|--------------|-------------|---------------------|
| **CRYPTO** | Cryptographic Controls | Encryption, hashing, key derivation, random number generation | AES, SHA-256, PBKDF2, TRNG |
| **CERT** | Certificate Management | PKI, certificate handling, trust chains, certificate lifecycle | X.509, OCSP, CRL, HSM |
| **COMMS** | Communications Security | CAN, UDS, V2X message security, protocol authentication | SecOC, AUTOSAR, CAN ID filtering |
| **NETWORK** | Network Security | IP, TCP/UDP, DNS, routing, firewall, IDS | TLS, IPsec, DNS-over-HTTPS |
| **ACCESS** | Access Control | Authorization, permission management, RBAC, ABAC | OAuth, RBAC policies, ACLs |
| **AUTH** | Authentication | Identity verification, MFA, SSO, biometrics | TOTP, WebAuthn, FIDO2, mTLS |
| **AUDIT** | Audit and Logging | Event recording, monitoring, alerting, SIEM | Syslog, ELK stack, log rotation |
| **SYSTEM** | System Security | OS hardening, process isolation, privilege management, SELinux | Seccomp, namespaces, cgroups |
| **CONFIG** | Configuration Management | Secure defaults, policy enforcement, configuration validation | CIS benchmarks, baselines |
| **BOOT** | Secure Boot | Boot chain verification, anti-rollback, TPM, attestation | Verified Boot, dm-verity |
| **OTA** | OTA Security | Software update security, delta updates, rollback protection | Code signing, UPTANE, A/B slots |
| **APP** | Application Security | App sandboxing, third-party app controls, permission models | Android SELinux, app signing |
| **DATA** | Data Protection | Storage encryption, data lifecycle, secure erasure, DLP | FDE, file-based encryption |
| **PHY** | Physical Security | Interface protection (USB, SD, OBD), port control | USB host disable, SD card lock |
| **DEBUG** | Debug Security | JTAG, UART, diagnostic port controls, debug disable | JTAG fuse, UART authentication |
| **CAMERA** | Camera Security | DVR, sentinel mode, Camera HAL, video encryption | Video encryption, HAL signing |
| **CLOUD** | Cloud Security | Backend API, cloud sync, server-side controls | API authentication, rate limiting |
| **SHARE** | Data Sharing | Cross-domain communication, inter-process communication | Binder, shared memory controls |
| **CHILD** | Child Safety | Children's data protection, parental controls | Age verification, COPPA compliance |
| **CONNECT** | Connectivity Security | Remote control, telematics, 4G/5G security | mTLS, SIM authentication |
| **REDUNDANCY** | High Availability | Failover, fault tolerance, redundancy, disaster recovery | Active-active, load balancing |
| **STORAGE** | Storage Security | Secure storage mechanisms, RPMB, TEE storage | RPMB, Keymaster, Gatekeeper |

**Category Selection Guidelines**:
1. Choose category by **primary security function** (not threat origin)
2. If CSR spans multiple categories, use the **most critical** category
3. Prefer specific categories (CAMERA) over generic (SYSTEM) when applicable
4. Create new categories only if no existing category fits (rare)

---

## Validation Checklist

Use this checklist when creating or reviewing CSR entries:

### Part A Entry Validation

- [ ] All 7 required fields populated (CSR-ID, Title, Status, Category, Description, Source, [Related CSG-IDs])
- [ ] CSR-ID follows format `CSR-[CATEGORY]-[NN]` with valid category code
- [ ] Status is `✅ IMPLEMENTED` (only valid value for Part A)
- [ ] Category matches CSR-ID prefix
- [ ] Description is in Chinese (from design specification)
- [ ] Description includes technical implementation details (not vague)
- [ ] Source references design specification or authoritative document
- [ ] Source is specific enough to enable verification (section reference preferred)
- [ ] Related CSG-IDs exist in `data/csg.md` (if populated)

### Part B Entry Validation

- [ ] All 9 required fields populated (CSR-ID, Title, Status, Priority, Category, Description, Identified By, Recommendation, [Related CSG-IDs])
- [ ] CSR-ID follows format `CSR-[CATEGORY]-[NN]` with valid category code
- [ ] Status is `❌ GAP` or `⚠️ PARTIAL` (never ✅ IMPLEMENTED)
- [ ] Priority is one of: CRITICAL, HIGH, MEDIUM, LOW
- [ ] Priority aligns with Identified By TS-ID Risk Value (RV → Priority mapping)
- [ ] Category matches CSR-ID prefix
- [ ] Description is in English with gap analysis (implementation status + gap + impact)
- [ ] Description references specific threats or impacts (not vague)
- [ ] Identified By references valid TS-ID from `data/ts.md` or "TARA Analysis"
- [ ] Recommendation includes at least 2 of 4 elements (What, How, Where, Verify)
- [ ] Recommendation is specific and actionable (not "improve security")
- [ ] Related CSG-IDs exist in `data/csg.md` (if populated)

### Catalogue-Level Validation

**CSR-ID Uniqueness**:
```bash
# Check for duplicate CSR-IDs within Part A
grep -E '^#### CSR-[A-Z]+-[0-9]{2}:' data/csr.md | grep -A 50 "^## Part A" | sort | uniq -d
# If output is non-empty, duplicate IDs exist (fix required)

# Check for duplicate CSR-IDs within Part B
grep -E '^#### CSR-[A-Z]+-[0-9]{2}:' data/csr.md | grep -A 1000 "^## Part B" | sort | uniq -d
# If output is non-empty, duplicate IDs exist (fix required)
```

**Priority Distribution** (expected proportions):
```bash
# Count priorities in Part B
CRITICAL=$(grep -c "Priority\*\*: CRITICAL" data/csr.md)
HIGH=$(grep -c "Priority\*\*: HIGH" data/csr.md)
MEDIUM=$(grep -c "Priority\*\*: MEDIUM" data/csr.md)
LOW=$(grep -c "Priority\*\*: LOW" data/csr.md)

echo "CRITICAL: $CRITICAL (expect ~28%)"
echo "HIGH: $HIGH (expect ~19%)"
echo "MEDIUM: $MEDIUM (expect ~45%)"
echo "LOW: $LOW (expect ~7%)"
```

**CSG Coverage** (every active-mitigation CSG implemented by at least one CSR):
```bash
# Extract all CSG-IDs from csg.md
grep -oE 'CSG-[A-Z]{2,5}-[0-9]{2}' data/csg.md | sort -u > /tmp/all_csgs.txt

# Extract CSG-IDs referenced by CSRs
grep -oE 'CSG-[A-Z]{2,5}-[0-9]{2}' data/csr.md | sort -u > /tmp/implemented_csgs.txt

# Find CSGs without CSR implementation
comm -23 /tmp/all_csgs.txt /tmp/implemented_csgs.txt
# If output is non-empty, these CSGs lack CSR implementation (orphan CSGs)
```

**TS-ID Reference Validity**:
```bash
# Extract TS-IDs referenced in Part B
grep "Identified By\*\*:" data/csr.md | grep -oE 'TS-[A-Z]{2,10}-[0-9]{3}' | sort -u > /tmp/csr_ts_refs.txt

# Extract TS-IDs defined in ts.md
grep -E '^###? TS-[A-Z]{2,10}-[0-9]{3}' data/ts.md | grep -oE 'TS-[A-Z]{2,10}-[0-9]{3}' | sort -u > /tmp/ts_defined.txt

# Check: all TS references must exist in ts.md
comm -23 /tmp/csr_ts_refs.txt /tmp/ts_defined.txt
# If output is non-empty, these TS-IDs are referenced but don't exist (fix references)
```

---

## Complete CSR Entry Examples

### Part A Example (Implemented Control)

```markdown
#### CSR-CERT-01: 部件支持OEM证书链加载和存储

- **Status**: ✅ IMPLEMENTED
- **Category**: Certificate Management
- **Description**: 流程规范:证书与密钥灌装严格遵循《PKI证书灌装流程规范-v1.6》。安全存储:所有敏感密钥及证书私钥均写入RPMB (Replay Protected Memory Block) 区域或HSM安全存储区。RPMB具备防重放、防篡改及访问鉴权特性,确保密钥无法被普通文件系统工具读取或修改。
- **Source**: Design Specification (信息安全设计规范说明书)
- **Related CSG-IDs**:
  - CSG-IVI-03 (Cryptographic Key Protection)
  - CSG-BCK-01 (Backend Authentication Infrastructure)
```

### Part B Example (GAP)

```markdown
#### CSR-CLOUD-02: Multi-Factor Authentication (MFA) Enforcement

- **Status**: ❌ GAP
- **Priority**: CRITICAL
- **Category**: Cloud Security
- **Description**: Multi-factor authentication (MFA) not enforced for cloud sync accounts. Current authentication relies on password-only login enabling credential theft via phishing attacks (TS-BCK-001). Lack of MFA violates NIST SP 800-63B Level 2 requirements for high-value accounts. RV 5 gap requiring immediate remediation.
- **Identified By**: TS-BCK-001 (Credential Theft via Phishing)
- **Recommendation**: Implement mandatory TOTP-based MFA for all cloud sync accounts. Require MFA enrollment during account creation (no opt-out). Support TOTP apps (Google Authenticator, Authy) and SMS backup. Prefer phishing-resistant MFA (WebAuthn, FIDO2) for high-value accounts. MFA re-verification required for sensitive operations (account settings, data export). Estimated cost: $0.50/user for SMS OTP, $0 for TOTP app. Validation: Penetration test confirms phishing resistance, 100% MFA adoption rate.
- **Related CSG-IDs**:
  - CSG-BCK-02 (Cloud Service Authentication)
  - CSG-IVI-01 (Location Data Confidentiality)
```

### Part B Example (PARTIAL)

```markdown
#### CSR-CLOUD-01: Cloud Sync Authentication

- **Status**: ⚠️ PARTIAL
- **Priority**: CRITICAL
- **Category**: Cloud Security
- **Description**: Cloud sync authentication implemented via mTLS and password-based login. Gap: Multi-factor authentication (MFA) not enforced, enabling credential theft via phishing attacks (TS-BCK-001). Current implementation satisfies basic authentication but insufficient for RV 5 credential theft scenarios. NIST SP 800-63B requires MFA for high-value accounts.
- **Identified By**: TS-BCK-001 (Credential Theft via Phishing)
- **Recommendation**: Add mandatory MFA layer to existing mTLS authentication. Integrate TOTP-based MFA into current OAuth2 login flow. Require MFA enrollment during first cloud sync setup. Support hardware security keys (YubiKey, Titan) for phishing-resistant authentication. Session management must validate both mTLS certificate AND MFA token. Estimated cost: $0/user for TOTP integration (app-based). Validation: Phishing simulation test confirms credential theft prevention.
- **Related CSG-IDs**:
  - CSG-BCK-02 (Cloud Service Authentication)
```

---

## References

- **ISO/SAE 21434:2021** - Road vehicles — Cybersecurity engineering
  - Clause 9.4: Cybersecurity specifications and requirements
  - Clause 8: Cybersecurity goals (CSG input for CSR derivation)
  
- **UN Regulation No. 155** - Uniform provisions concerning the approval of vehicles with regards to cyber security
  - Annex 5, Part B: Cyber security measures and controls

- **NIST Cybersecurity Framework (CSF)** - Framework for improving critical infrastructure cybersecurity
  - For control categorization and priority mapping

- **OWASP Application Security Verification Standard (ASVS)** - Security requirements for web applications
  - For application security control baselines

- **GDPR (EU 2016/679)** - General Data Protection Regulation
  - For privacy control requirements and data protection by design

- **GB 44495** - Automotive data security requirements (China)
  - For China-specific data security controls

- **AUTOSAR SecOC Specification** - Secure Onboard Communication
  - For CAN/Ethernet message authentication requirements

---

## Schema Version

- **Version**: 1.0
- **Date**: 2026-03-31
- **Status**: Active
- **Maintained By**: TARA Maker Skill / CSR Module
