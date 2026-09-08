# Part B (Gap/Partial) CSR Example - OTA Security & Camera Security

This example demonstrates Part B (Identified Gaps) CSR entries for **OTA Security** and **Camera Security** domains, showing the structure and content required for gap documentation with upstream priority traceability.

---

## Purpose

This example illustrates:
- **Part B entry format** with 9 required fields (CSR-ID, Title, Status, Priority, Category, Description, Identified By, Recommendation, [Related CSG-IDs])
- **❌ GAP vs ⚠️ PARTIAL status** classification criteria
- Priority documentation aligned to linked TS/RT context
- **4-element Recommendation** structure (What, How, Where, Verify)
- **English gap descriptions** with technical specifics
- **Traceability to threat scenarios** (TS-ID references)

**Note**: These examples are drawn from real TARA analysis for the BAIC B31CS ICC platform. CSR-IDs and content reflect actual identified gaps from `data/csr.md`.

---

## Part B Entry Structure Reminder

Every Part B entry requires **9 fields**:

1. **CSR-ID** (heading): `CSR-[CATEGORY]-[NN]` format with 2-digit number
2. **Status**: `❌ GAP` or `⚠️ PARTIAL`
3. **Priority**: `CRITICAL` | `HIGH` | `MEDIUM` | `LOW`
4. **Category**: Functional domain (OTA Security, Camera Security, etc.)
5. **Description**: English gap analysis (status + gap + impact + compliance)
6. **Identified By**: `TS-[DOMAIN]-[NNN]` reference or "TARA Analysis"
7. **Recommendation**: 4-element technical mitigation (What, How, Where, Verify)
8. **Related CSG-IDs**: (optional) Links to Cybersecurity Goals

**Key Distinction**:
- **❌ GAP** = Control does NOT exist (no implementation)
- **⚠️ PARTIAL** = Control PARTIALLY exists (implementation incomplete, critical gaps remain)

---

## Example 1: OTA Security - CRITICAL Priority (PARTIAL Status)

#### CSR-OTA-01: OTA Client Security Enhancement

- **Status**: ⚠️ PARTIAL
- **Priority**: CRITICAL
- **Category**: OTA Security
- **Description**: OTA update mechanism exists with basic signature verification and TLS transport. Gap: Certificate pinning not implemented, enabling MITM attacks via rogue access points or DNS spoofing (TS-OTA-001). Current TLS implementation accepts any CA-signed certificate, allowing attacker-controlled certificates to intercept OTA packages. Signature verification uses crypto library with unknown CVE status, risking parser vulnerabilities (CVE-2020-8539 class exploits). RV 5 gap requiring immediate remediation per UN R155 Article 8 (secure software update requirements).
- **Identified By**: TS-OTA-001 (Malicious OTA Package Distribution)
- **Recommendation**: Implement TLS certificate pinning and signature verification hardening for OTA client.
  - **What**: Hardcode OEM TSP server certificate public keys in OTA client (reject non-pinned certificates even if CA-signed)
  - **How**: Use TLS 1.3 mandatory (deprecate TLS 1.2), implement certificate rotation mechanism via signed update manifest, add redundant signature verification using independent cryptographic library (detect single-library CVE)
  - **Where**: QAM8295 OTA client application layer, integrate with existing OTA update framework
  - **Verify**: MITM penetration test using rogue AP and DNS spoofing confirms certificate pinning effectiveness, crypto library version audit confirms no known CVE >6 months old
  - **Cost**: $0 (code-only enhancement, no hardware change)

---

## Example 2: OTA Security - CRITICAL Priority (GAP Status)

#### CSR-OTA-03: RPMB Anti-Rollback Protection

- **Status**: ❌ GAP
- **Priority**: CRITICAL
- **Category**: OTA Security
- **Description**: RPMB-backed monotonic counter implementation status unclear. No hardware-enforced anti-rollback protection confirmed for firmware components (bootloader, kernel, QTEE, TC377 MCU firmware). Current firmware versioning relies on metadata files which can be manipulated by attacker with physical access or bootloader compromise. Gap enables rollback attacks to vulnerable firmware versions despite valid signatures (DS-OTA-003). UN R155 Article 8 requires anti-rollback protection for all ECU firmware.
- **Identified By**: TS-OTA-002 (Firmware Rollback Attack)
- **Recommendation**: Implement robust RPMB-backed monotonic counters for all firmware components.
  - **What**: RPMB monotonic counter per firmware component (bootloader, kernel, QTEE, TC377, camera firmware)
  - **How**: Hardware-enforced counter increment on successful update (RPMB write authentication via device-unique key), bootloader validates counter value before firmware acceptance (reject if version < counter), counter stored in RPMB partition with replay protection
  - **Where**: QAM8295 bootloader (SBL/XBL stage) for early validation, TC377 bootloader for MCU firmware, MAX96724 deserializer bootloader for camera firmware
  - **Verify**: Rollback attack test confirms bootloader refuses to boot older firmware despite valid signature, RPMB write protection test confirms counter manipulation prevention
  - **Cost**: $0 (RPMB partition already provisioned, software enhancement only)

---

## Example 3: OTA Security - CRITICAL Priority (GAP Status with Immediate Timeline)

#### CSR-OTA-07: TLS Certificate Pinning

- **Status**: ❌ GAP
- **Priority**: CRITICAL
- **Category**: OTA Security
- **Description**: TLS certificate pinning not implemented in OTA client. Current implementation accepts any CA-signed certificate enabling MITM attacks via compromised WiFi access point (rogue AP) or DNS spoofing attack (TS-OTA-001). Attacker presenting CA-signed certificate for fake TSP server can intercept OTA communication and deliver malicious rollback packages. Gap violates UN R155 Article 8 requirements for secure software update mechanisms. NIST SP 800-218 recommends certificate pinning for critical infrastructure update channels.
- **Identified By**: TS-OTA-001 (Malicious OTA Package via MITM)
- **Recommendation**: Implement TLS certificate pinning with certificate rotation mechanism.
  - **What**: Hardcode OEM TSP server certificate public keys in OTA client firmware (embedded at compile-time)
  - **How**: Reject TLS connections presenting certificates not matching pinned keys (even if CA-signed), implement certificate rotation via signed manifest update (new pinned certificates delivered through existing update channel), support 2-3 certificate slots for rotation overlap period
  - **Where**: OTA client TLS handshake layer (libcurl or Android OkHttp), integrate with existing TLS stack without breaking backward compatibility
  - **Verify**: MITM penetration test using rogue AP with CA-signed fake certificate confirms connection rejection, certificate rotation test confirms successful update to new pinned certificate
  - **Cost**: $0 (code enhancement, ~1-2 week development effort)
  - **Timeline**: IMMEDIATE (addresses RV 3 prerequisite attack for firmware tampering chain)

---

## Example 4: Camera Security - CRITICAL Priority (PARTIAL Status)

#### CSR-CAMERA-01: DMS Liveness Detection Enhancement

- **Status**: ⚠️ PARTIAL
- **Priority**: CRITICAL
- **Category**: Camera Security
- **Description**: DMS camera operational with basic liveness detection (blink detection, head pose validation). Gap: Lacks 3D depth sensing or infrared-based liveness, enabling 2D photo/video spoofing attacks (TS-CAMERA-001). Current algorithm vulnerable to printed photo attacks and video replay attacks. Biometric authentication compromise enables unauthorized vehicle access and location tracking (GDPR Article 9 special category data breach). Industry best practice (FIDO Biometric Component Certification) requires Level 2 PAD (Presentation Attack Detection) with >95% detection rate.
- **Identified By**: TS-CAMERA-001 (Biometric Spoofing Attack)
- **Recommendation**: Enhance DMS liveness detection with multi-modal verification.
  - **What**: Implement 3D liveness detection via structured light or time-of-flight depth sensing (detect photo flatness)
  - **How**: Add infrared camera for skin texture analysis (detect printed photos), implement challenge-response liveness (random blink/smile prompts), combine 3 liveness indicators with ML-based fusion (depth + IR + behavioral), require 2/3 indicators pass for authentication success
  - **Where**: DMS camera module hardware upgrade (add IR camera), QAM8295 biometric processing pipeline (integrate depth sensing SDK)
  - **Verify**: Spoofing attack test using printed photos and video replay confirms >95% detection rate per FIDO Biometric Component Certification Level 2, false rejection rate <5% for legitimate users
  - **Cost**: $15-25/vehicle for IR camera and structured light emitter (NRE ~$200K for hardware redesign)

---

## Example 5: Camera Security - CRITICAL Priority (GAP Status)

#### CSR-CAMERA-02: LVDS Feed Integrity Protection

- **Status**: ❌ GAP
- **Priority**: CRITICAL
- **Category**: Camera Security
- **Description**: LVDS video feed between MAX96724 deserializer and QAM8295 SoC lacks encryption and authentication. Gap enables video injection attacks via physical access to LVDS traces on PCB (TS-CAMERA-003). Attacker can inject fake camera feed for parking cameras (AVM) causing collision, or inject fake DMS feed defeating biometric authentication. No cryptographic protection on 1.2Gbps LVDS link. Attack requires ICC disassembly but achieves safety-critical impact (parking collision - Impact 4). ISO 21434 Clause 9.4 recommends link-layer encryption for safety-critical sensor data.
- **Identified By**: TS-CAMERA-003 (Physical LVDS Video Injection)
- **Recommendation**: Implement LVDS encryption and authentication tags on camera feed.
  - **What**: Enable MAX96724 LVDS encryption feature (AES-128-CTR mode) with frame-level authentication tags (HMAC-SHA256 truncated to 32 bits)
  - **How**: Provision shared symmetric keys between camera modules and MAX96724 during manufacturing (device-unique keys stored in camera EEPROM and QAM8295 RPMB), encrypt LVDS payload before serialization, append authentication tag to each video frame (1920x1080 frame = 1 tag per 16ms)
  - **Where**: MAX96724 deserializer firmware (enable encryption engine), camera module firmware (encrypt before LVDS output), QAM8295 Camera HAL (decrypt and verify tags)
  - **Verify**: Video injection attack test via LVDS interposer board confirms encrypted feed rejection, authentication tag validation test confirms tampered frame detection within 16ms (1 frame latency)
  - **Cost**: $0 for MAX96724 feature enable (hardware supports encryption, firmware enhancement only), ~$50K NRE for key provisioning process integration

---

## Example 6: Camera Security - HIGH Priority (GAP Status)

#### CSR-CAMERA-03: Physical Camera Tampering Detection

- **Status**: ❌ GAP
- **Priority**: HIGH
- **Category**: Camera Security
- **Description**: No tamper detection for physical camera obstruction or angle deviation attacks. Attacker can cover DMS camera with tape (defeat biometric authentication) or reposition parking camera (cause parking collision via false distance overlay). Current system does not detect sudden image darkness, blur patterns indicating lens obstruction, or camera angle deviation from factory calibration. Gap enables persistent denial-of-service attacks on camera-dependent security features (biometric auth, parking assist). Recommended by ISO 21434 Table 13 for safety-critical sensors.
- **Identified By**: TS-CAMERA-005 (Physical Camera Tampering)
- **Recommendation**: Implement computer vision-based camera tampering detection.
  - **What**: Lens obstruction detection via image brightness histogram analysis (detect sudden darkness or blur patterns)
  - **How**: Camera angle deviation detection via driver face position validation (DMS) or lane marker geometry validation (AVM), calibration reference stored in RPMB (tamper-proof baseline), trigger driver alert and disable authentication if tampering detected, log tampering events to TSP backend for fleet-wide analysis
  - **Where**: QAM8295 Camera HAL layer (pre-processing pipeline before biometric/ADAS algorithms)
  - **Verify**: Obstruction test using tape/paper covering lens confirms detection within 500ms, angle deviation test using camera repositioning confirms detection within 1 second, false positive rate <1% during normal operation
  - **Cost**: $0 (software algorithm, no hardware change), ~2-3 week development effort

---

## Example 7: Camera Security - CRITICAL Priority (PARTIAL Status with HAL Hardening)

#### CSR-CAMERA-10: Camera HAL Code Signing

- **Status**: ⚠️ PARTIAL
- **Priority**: CRITICAL
- **Category**: Camera Security
- **Description**: Camera HAL operational as standard Android Camera HAL but lacks code signing and runtime authentication. Gap: Malicious HAL indistinguishable from legitimate HAL enabling unauthorized camera access and privacy violations (TS-CAMERA-002). Android permission framework exists but no cryptographic verification of HAL binaries before loading. Compromised HAL can bypass permission checks, access camera without user consent, or exfiltrate video streams. GDPR Article 9 requires special category data (biometric templates) protection via encryption and access control. Current implementation lacks HAL binary integrity verification.
- **Identified By**: TS-CAMERA-002 (Malicious Camera HAL Injection)
- **Recommendation**: Implement cryptographic signing and runtime verification for Camera HAL modules.
  - **What**: Sign all camera HAL binaries (.so files) with OEM private key during build process
  - **How**: Android framework verifies HAL signature before loading (use Android Verified Boot key infrastructure), store HAL signing certificates in RPMB (tamper-proof trust anchor), implement HAL revocation list for compromised versions, refuse to load unsigned or revoked HAL binaries (fail-secure default)
  - **Where**: Android framework HAL loader (hardware/interfaces), integrate with existing SELinux policies for defense-in-depth
  - **Verify**: HAL injection test using unsigned malicious HAL confirms loading rejection, HAL signature verification test confirms legitimate HAL loading succeeds, revocation test confirms revoked HAL version rejected despite valid signature
  - **Cost**: $0 (code signing infrastructure already exists for APK signing, extend to HAL binaries)

---

## Example 8: Camera Security - HIGH Priority (GAP Status with Version Policy)

#### CSR-CAMERA-13: Camera Firmware Version Policy Enforcement

- **Status**: ❌ GAP
- **Priority**: HIGH
- **Category**: Camera Security
- **Description**: Camera firmware versioning tracked via metadata files but no anti-rollback enforcement at component level. Gap: Attacker can downgrade camera firmware to vulnerable version despite valid signatures (TS-CAMERA-004). Bootloader verifies signature authenticity but does not validate firmware freshness (signed-but-old firmware accepted). No minimum version policy preventing rollback below critical security thresholds. Gap enables persistent exploitation of patched vulnerabilities via firmware downgrade. UN R155 Article 8 requires anti-rollback protection for all vehicle ECUs.
- **Identified By**: TS-CAMERA-004 (Camera Firmware Downgrade Attack)
- **Recommendation**: Implement minimum firmware version policy with bootloader-level enforcement.
  - **What**: Define minimum version policy per camera component (DMS camera, AVM cameras, MAX96724 deserializer)
  - **How**: Bootloader validates firmware version against minimum version threshold before loading (reject signed-but-old firmware), store minimum version policy in RPMB monotonic counter (hardware-enforced anti-rollback), centralized version policy management in QAM8295 (distribute minimum versions via signed OTA manifest)
  - **Where**: Camera module bootloaders (before firmware execution), MAX96724 deserializer bootloader (before firmware acceptance), QAM8295 Camera HAL (attestation verification during initialization)
  - **Verify**: Firmware downgrade attack test using signed old firmware confirms bootloader rejection, version policy update test confirms successful minimum version increase via OTA, attestation test confirms QAM8295 detects non-compliant camera firmware version
  - **Cost**: $0 (software enhancement, reuse RPMB infrastructure from CSR-OTA-03)

---

## Priority Traceability Reminder

- Priority should align with the linked TS/RT context.
- If RT output is not ready, record the gap as pending RT completion rather than inventing a local priority policy.

---

## Common Mistakes to Avoid

### Mistake 1: Vague Gap Description

**Bad Example**:
> "Security controls need improvement for camera system."

**Why Bad?**: No technical specifics, no threat linkage, not actionable

**Good Example** (see CSR-CAMERA-02 above):
> "LVDS video feed lacks encryption and authentication. Attacker can inject fake camera feed via physical access to LVDS traces enabling parking collision (Impact 4)."

---

### Mistake 2: Generic Recommendation

**Bad Example**:
> "Implement best practices for camera security."

**Why Bad?**: No specific technologies, no configuration parameters, no validation criteria

**Good Example** (see CSR-CAMERA-03 above):
> "Implement lens obstruction detection via brightness histogram analysis, camera angle deviation detection via face position validation, trigger alert within 500ms."

---

### Mistake 3: Priority Not Aligned With Upstream Context

**Bad Example**:
> TS-OTA-001 / RT-OTA-001 indicates urgent treatment, but CSR-OTA-01 is marked Priority: MEDIUM

**Why Bad?**: Priority must align with the linked TS/RT context, not with ad hoc local judgment.

**Good Example**:
> TS-OTA-001 / RT-OTA-001 indicates urgent treatment, so CSR-OTA-01 carries Priority: CRITICAL

---

### Mistake 4: GAP vs PARTIAL Confusion

**Bad Example** (marked as GAP but describes existing implementation):
> "**Status**: ❌ GAP. OTA update mechanism exists but lacks certificate pinning."

**Why Bad?**: If mechanism exists, it's PARTIAL (not GAP)

**Good Example**:
> "**Status**: ⚠️ PARTIAL. OTA update mechanism exists with basic TLS. Gap: Certificate pinning not implemented."

---

## Quality Checklist

Before finalizing Part B CSR entries, verify:

- [ ] Status correctly classified (❌ GAP = no implementation, ⚠️ PARTIAL = partial implementation)
- [ ] Priority aligns with linked TS/RT context, or is explicitly marked pending RT completion
- [ ] Description includes 3+ elements (status, gap, impact, compliance context)
- [ ] Description references specific threat scenario (TS-ID) or regulatory requirement
- [ ] Recommendation includes 4 elements (What, How, Where, Verify)
- [ ] Recommendation is specific and actionable (no "improve security")
- [ ] Recommendation includes cost estimate or timeline (when feasible)
- [ ] Identified By references valid TS-ID from `data/ts.md` or uses "TARA Analysis"
- [ ] All technical terms are precise (AES-256-CTR, HMAC-SHA256, RPMB, not "encryption")

---

## References

- `references/csr-schema.md` - Part B field definitions (9 required fields)
- `references/csr-guide.md` - Gap identification methodology and priority mapping
- `data/csr.md` - Complete CSR catalogue with 211 Part B entries
- `data/ts.md` - Threat scenario catalogue with Risk Value assignments

---

**Example Version**: 1.0  
**Date**: 2026-03-31  
**Line Count**: ~250 lines
