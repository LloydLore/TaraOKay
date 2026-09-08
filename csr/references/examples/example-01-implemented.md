# Example 01: Part A (IMPLEMENTED Controls) - Certificate Management Domain

## About This Example

This document demonstrates **Part A CSR entries** — security controls that are **already implemented** in the system and documented in design specifications.

**Why Certificate Management?**
- Certificate Management (CERT category) has the most complete implementation documentation
- PKI infrastructure is foundational to automotive cybersecurity (mTLS, code signing, secure storage)
- Demonstrates how Chinese design specification text is preserved for traceability

**What Part A Represents**:
- ✅ **IMPLEMENTED** status only (control exists and is documented)
- Source references enable verification and audit
- Chinese descriptions preserve original design specification language
- No gaps, no recommendations — these are completed controls

**How to Use This Example**:
- Reference this when documenting existing security controls from design specs
- Copy the field structure and adapt content to your domain
- Use as a quality baseline for Part A entries

---

## Part A: Certificate Management Controls

### CSR-CERT-01: 部件支持OEM证书链加载和存储

- **Status**: ✅ IMPLEMENTED
- **Category**: Certificate Management
- **Description**: 流程规范：证书与密钥灌装严格遵循《PKI证书灌装流程规范-v1.6》。 安全存储：所有敏感密钥及证书私钥均写入RPMB (Replay Protected Memory Block) 区域或HSM安全存储区。RPMB具备防重放、防篡改及访问鉴权特性，确保密钥无法被普通文件系统工具读取或修改。
- **Source**: Design Specification (信息安全设计规范说明书)

> **Annotation**: This entry demonstrates **proper Chinese text preservation**. The Description field contains the original Chinese technical specification text, which enables:
> - Direct traceability to source document (《PKI证书灌装流程规范-v1.6》)
> - Verification by Chinese-speaking auditors
> - No translation errors or semantic drift
> 
> **CSR-ID Numbering**: CERT-01 is the first certificate management requirement. Part A CSR-IDs use 2-digit sequential numbering within each category (independent of CSG/TS/DS numbering).
> 
> **Status Field**: Part A entries are ALWAYS "✅ IMPLEMENTED" — no exceptions. If a control is incomplete, it belongs in Part B (GAP/PARTIAL).

---

### CSR-CERT-02: OEM证书链应在车端持久化存储

- **Status**: ✅ IMPLEMENTED
- **Category**: Certificate Management
- **Description**: 系统预留15KB的非易失性存储空间，支持同时加载并存储TSP云平台与华为ADS智驾系统的两套独立证书链。证书文件及对应私钥均存放于QTEE安全区域，确保在OTA升级、恢复出厂设置等操作下，证书数据不丢失、不损坏。满足《PKI证书灌装电检流程规范》要求。
- **Source**: Design Specification (信息安全设计规范说明书)

> **Annotation**: This entry demonstrates **technical implementation details in Chinese**:
> - Specific storage allocation (15KB non-volatile storage)
> - Multi-platform support (TSP cloud + Huawei ADS)
> - Storage location (QTEE secure area)
> - Persistence guarantees (survives OTA updates and factory reset)
> 
> **Why Chinese Text Matters**: Technical terms like "非易失性存储" (non-volatile storage), "证书链" (certificate chain), and "QTEE安全区域" (QTEE secure area) have precise meanings in Chinese automotive documentation. Direct preservation avoids ambiguity.

---

### CSR-CERT-03: 部件应采用物理隔离的硬件安全模块保护证书私钥

- **Status**: ✅ IMPLEMENTED
- **Category**: Certificate Management
- **Description**: 所有核心密码运算（密钥生成、加解密、签名验签）在硬件安全模块中执行： SoC (QC8295)：启用QTEE (Qualcomm Trusted Execution Environment)； MCU (TC377)：启用HSM (Hardware Security Module) 独立核。 确保密钥材料永不离开硬件安全边界，实现物理级的密钥保护。
- **Source**: Design Specification (信息安全设计规范说明书)

> **Annotation**: This entry demonstrates **hardware-level security implementation**:
> - Two distinct security modules: QTEE (SoC) and HSM (MCU)
> - Physical isolation guarantee ("密钥材料永不离开硬件安全边界")
> - Covers full cryptographic lifecycle (generation, encryption, signing)
> 
> **CSR-ID Assignment**: CSR-CERT-03 follows CSR-CERT-02 sequentially. Certificate Management entries use the CERT category code because they focus on PKI infrastructure (not general cryptographic operations, which would use CRYPTO).

---

### CSR-CERT-04: 证书验证应检查证书链完整性和有效性

- **Status**: ✅ IMPLEMENTED
- **Category**: Certificate Management
- **Description**: 系统在启动时及通信建立前，自动执行完整的证书链验证流程，包括：根证书合法性校验、中间证书未被吊销检查(CRL/OCSP)、终端证书有效期及签名验证。任一环节验证失败，系统拒绝建立通信通道或加载证书，确保证书链完整性与有效性。
- **Source**: Design Specification (信息安全设计规范说明书)

> **Annotation**: This entry demonstrates **verification process documentation**:
> - Multi-stage validation (root → intermediate → end-entity)
> - Revocation checking (CRL/OCSP)
> - Failure handling (reject communication)
> 
> **Title Derivation**: The title "证书验证应检查证书链完整性和有效性" is derived directly from the Description content. For Part A entries, titles often come from section headings in the design specification or summarize the Description.

---

### CSR-CERT-05: 证书更新应通过安全OTA通道进行

- **Status**: ✅ IMPLEMENTED
- **Category**: Certificate Management
- **Description**: 证书更新操作仅允许通过OTA安全升级通道进行。所有证书更新包必须携带TSP平台的数字签名，且在下载后立即进行签名验证。验证通过后，系统将新证书写入RPMB安全存储区，并同步更新内存中的受信根证书列表。整个流程通过mTLS加密通道传输，防止中间人攻击。
- **Source**: Design Specification (信息安全设计规范说明书)

> **Annotation**: This entry demonstrates **secure update workflow**:
> - Single authorized channel (OTA only)
> - Signature verification before installation
> - Secure storage update (RPMB)
> - Transport security (mTLS)
> 
> **Source Field**: All Part A entries reference "Design Specification (信息安全设计规范说明书)". This is the primary source document for implemented controls. Alternative sources might include:
> - Supplier declarations (e.g., "Supplier Declaration (Qualcomm QAM8295 Security Features)")
> - Component datasheets (e.g., "Infineon SLI-97 Secure Element Datasheet")
> - Industry standards (e.g., "AUTOSAR SecOC Specification v4.3.1")

---

### CSR-CERT-06: 应实施证书吊销检查机制

- **Status**: ✅ IMPLEMENTED
- **Category**: Certificate Management
- **Description**: 系统实施双模式证书吊销检查：在线模式下，通过OCSP (Online Certificate Status Protocol) 实时查询证书吊销状态；离线模式下，使用预加载的CRL (Certificate Revocation List) 进行本地校验。CRL列表定期通过OTA更新，确保即使在无网络环境下也能识别已吊销的证书。
- **Source**: Design Specification (信息安全设计规范说明书)

> **Annotation**: This entry demonstrates **dual-mode verification strategy**:
> - Online: OCSP real-time queries
> - Offline: Local CRL validation
> - Hybrid resilience (works in connected and disconnected states)
> 
> **Category Assignment**: Certificate Management (CERT) focuses on PKI operations — certificate lifecycle, validation, revocation, storage. This is distinct from:
> - Cryptographic Controls (CRYPTO) — encryption algorithms, key generation
> - Communications Security (COMMS) — protocol-level security (mTLS, TLS)
> 
> CSR-CERT-06 focuses on certificate revocation checking, which is a PKI-specific operation, hence CERT category.

---

### CSR-CERT-07: 证书私钥应在硬件安全模块内生成且不可导出

- **Status**: ✅ IMPLEMENTED
- **Category**: Certificate Management
- **Description**: 所有证书私钥在HSM (Hardware Security Module) 或QTEE内生成，密钥生成过程完全在硬件安全边界内执行，密钥材料以密文形式存储，永不以明文形式暴露给应用层或操作系统。密钥属性配置为"不可导出" (non-exportable)，确保即使攻击者获得root权限也无法提取私钥。
- **Source**: Design Specification (信息安全设计规范说明书)

> **Annotation**: This entry demonstrates **key generation and protection**:
> - Hardware-bound generation (HSM/QTEE)
> - Non-exportable key property (prevents extraction)
> - Defense against privileged attackers (root compromise does not leak keys)
> 
> **CSR-CERT vs CSR-CRYPTO Distinction**:
> - CSR-CERT-07: Private key generation **for certificates** (PKI context)
> - CSR-CRYPTO-XX: General key generation **for encryption/signing** (non-PKI context)
> 
> If the requirement is specific to certificate private keys, use CERT. If it applies to all cryptographic keys, use CRYPTO.

---

### CSR-CERT-08: 应支持多CA信任根配置

- **Status**: ✅ IMPLEMENTED
- **Category**: Certificate Management
- **Description**: 系统支持同时信任多个证书颁发机构(CA)的根证书，包括企业内部PKI根证书和公共CA根证书(如DigiCert, GlobalSign)。受信根证书列表存储于只读分区，仅允许通过签名OTA包进行更新。支持不同业务域使用不同CA根证书，实现多租户PKI架构。
- **Source**: Design Specification (信息安全设计规范说明书)

> **Annotation**: This entry demonstrates **multi-CA trust architecture**:
> - Multiple root certificate support (internal + public CAs)
> - Read-only storage (prevents unauthorized modification)
> - Multi-tenant PKI (different business domains use different CA roots)
> 
> **Why 8 Entries?**: Certificate Management domain has 8 fully-documented Part A entries in the reference catalogue (CSR-CERT-01 through CSR-CERT-08). This represents complete PKI implementation coverage for the BAIC B31CS ICC platform.

---

## Validation Checklist for Part A Entries

Before submitting Part A CSR entries, verify:

**Field Completeness** (7 required fields):
- [ ] CSR-ID in format `CSR-[CATEGORY]-[NN]` with valid 2-digit number
- [ ] Title (max 80 chars, may be Chinese or English)
- [ ] Status is "✅ IMPLEMENTED" (no exceptions for Part A)
- [ ] Category matches CSR-ID prefix (e.g., CERT → Certificate Management)
- [ ] Description contains Chinese text from design specification (preserved exactly)
- [ ] Source field populated with reference to design document

**Content Quality**:
- [ ] Chinese text is copied from source document (not invented or translated)
- [ ] Technical terms are preserved in original language (no paraphrasing)
- [ ] Description length: 2-5 sentences (typically 100-200 Chinese characters)
- [ ] Source enables traceability (document name + optional section reference)

**CSR-ID Numbering**:
- [ ] Sequential within category (CERT-01, CERT-02, CERT-03, ...)
- [ ] 2-digit zero-padded (01-99, not 001-999)
- [ ] No gaps in sequence (if you have CERT-01 and CERT-03, where is CERT-02?)

**Common Mistakes to Avoid**:
- ❌ Inventing Chinese descriptions instead of copying from design spec
- ❌ Using "⚠️ PARTIAL" or "❌ GAP" status (Part A is IMPLEMENTED only)
- ❌ Mixing Part A and Part B entries in the same document
- ❌ Omitting Source field (mandatory for traceability)
- ❌ Using 3-digit CSR-ID numbers (01 not 001)

---

## Related Files

**Schema Definition**:
- `references/csr-schema.md` — Complete field definitions and validation rules for Part A

**Template**:
- `assets/TEMPLATE.md` — Minimal output template

**Other Examples**:
- `references/examples/example-02-gap.md` — Part B example showing identified gaps and partial/incomplete controls

**Source Data**:
- `data/csr.md` — Complete CSR catalogue (56 Part A + 211 Part B entries)

---

**Example Status**: ✅ COMPLETE  
**Domain Coverage**: Certificate Management (CERT)  
**Entry Count**: 8 Part A entries  
**Line Count**: 247 lines  
**Last Updated**: 2026-03-31
