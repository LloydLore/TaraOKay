# Attack Tree Methodology Guide - ISO 21434 TARA

This guide explains the methodology for building and analyzing attack trees in ISO 21434 TARA workflows, covering gate semantics, AFR aggregation rules, ASCII visualization conventions, and analysis techniques.

---

## Attack Tree Fundamentals

### What is an Attack Tree?

An **attack tree** is a hierarchical model that represents the various paths an attacker can take to achieve a specific goal (damage scenario). The tree structure shows:

- **Root node**: The attacker's ultimate objective (damage scenario / DS-ID)
- **Leaf nodes**: Entry points or initial attack steps (threat scenarios / TS-IDs)
- **Intermediate nodes**: Sub-goals or attack stages
- **Gates**: Logical relationships between nodes (AND/OR/SEQ)

Attack trees answer the question: *"What are all the ways an attacker can achieve this damage scenario?"*

### Why Use Attack Trees?

- **Comprehensive coverage**: Enumerate ALL attack paths, not just the obvious ones
- **Risk prioritization**: Identify critical paths and high-leverage mitigation points
- **Feasibility analysis**: Calculate attack difficulty (AFR) for each path
- **Security investment**: Guide resource allocation to controls that break multiple paths
- **ISO 21434 compliance**: Clause 15.7 requires attack path analysis for TARA

---

## Gate Types and Semantics

Attack trees use three gate types to model logical relationships between attack steps:

### AND Gate `[AND]`

**Meaning**: ALL child nodes must succeed for the parent to succeed.

**Attacker Perspective**: The attacker must execute every child attack successfully—failure at any child blocks the entire path.

**Use Cases**:
- Multiple prerequisites required (e.g., network access AND valid credentials)
- Defense-in-depth layers that must all be breached
- Parallel requirements with no alternative

**Example**:
```
DS-IVI-002: Personally Identifiable Information (PII) Exposure
    |
    [AND]
    |
    +-- TS-IVI-005: Compromise IVI File System Access
    +-- TS-IVI-009: Bypass Data Encryption at Rest
```

**Interpretation**: Attacker needs BOTH file system access AND encryption bypass to exfiltrate PII. Either control alone prevents the attack.

---

### OR Gate `[OR]`

**Meaning**: ANY single child node is sufficient for the parent to succeed.

**Attacker Perspective**: The attacker chooses the easiest path from multiple alternatives—success at any child achieves the goal.

**Use Cases**:
- Multiple entry points or attack vectors
- Alternative exploitation techniques
- Different attacker capabilities (physical vs remote)

**Example**:
```
DS-CAN-001: Malicious CAN Message Injection
    |
    [OR]
    |
    +-- [Path 1] TS-IVI-012: CAN Injection via Compromised IVI
    +-- [Path 2] TS-EXT-001: CAN Injection via OBD-II Adapter
    +-- [Path 3] TS-OTA-005: CAN Injection via Malicious OTA Update
```

**Interpretation**: Attacker has three independent ways to inject CAN messages. Defending against one path still leaves two open—all paths must be mitigated.

---

### SEQ Gate `[SEQ]`

**Meaning**: Child nodes must succeed in SEQUENTIAL ORDER (top-to-bottom or left-to-right).

**Attacker Perspective**: The attacker follows a multi-stage process where each step enables the next—steps cannot be reordered.

**Use Cases**:
- Kill chains with dependent stages (access → persist → escalate → exfiltrate)
- Attacks requiring state progression
- Temporal dependencies (e.g., obtain key → decrypt data)

**Example**:
```
DS-IVI-003: Arbitrary Code Execution on IVI
    |
    [SEQ]
    |
    +-- [Step 1] TS-IVI-001: Install Malicious App on IVI
    +-- [Step 2] TS-IVI-007: Exploit App Sandbox Escape Vulnerability
    +-- [Step 3] TS-IVI-008: Escalate to Root Privileges
```

**Interpretation**: Attacker must complete steps in order. Breaking the chain at any step (e.g., preventing sandbox escape) stops the attack.

---

## AFR Aggregation Rules

Attack Feasibility Rating (AFR) scores from individual threat scenarios (TS-IDs) must be aggregated to compute path-level and tree-level AFR. The aggregation rules follow logical gate semantics:

### Rule 1: AND Gates → MINIMUM

**Formula**: `AFR_parent = MIN(AFR_child1, AFR_child2, ..., AFR_childN)`

**Rationale**: The attacker must succeed at ALL children. The HARDEST step (lowest AFR) limits the overall feasibility—this is the "weakest link" principle.

**Example**:
```
[AND] gate with children:
- TS-IVI-005 AFR: 8 (Medium)
- TS-IVI-009 AFR: 4 (High difficulty)

Aggregated AFR = MIN(8, 4) = 4 (High difficulty)
```

**Interpretation**: Even though one step is easy (AFR=8), the other step is very hard (AFR=4). The attacker's overall difficulty is 4—the attack is only as easy as its hardest step.

---

### Rule 2: OR Gates → MAXIMUM

**Formula**: `AFR_parent = MAX(AFR_child1, AFR_child2, ..., AFR_childN)`

**Rationale**: The attacker chooses the EASIEST path from alternatives. The HIGHEST AFR (easiest attack) determines overall feasibility.

**Example**:
```
[OR] gate with children:
- Path 1 (Remote): AFR = 6 (Medium)
- Path 2 (Physical): AFR = 13 (Low difficulty)
- Path 3 (OTA): AFR = 3 (High difficulty)

Aggregated AFR = MAX(6, 13, 3) = 13 (Low difficulty)
```

**Interpretation**: Attacker will choose Path 2 (physical, AFR=13) because it's the easiest option, even though remote and OTA paths are harder. The tree's feasibility is 13.

---

### Rule 3: SEQ Gates → MINIMUM (Chain Strength)

**Formula**: `AFR_path = MIN(AFR_step1, AFR_step2, ..., AFR_stepN)`

**Rationale**: Sequential chains are only as strong as their weakest link. The HARDEST step (lowest AFR) determines the chain's overall difficulty.

**Example**:
```
[SEQ] chain:
- Step 1 (Install App): AFR = 12 (Low difficulty)
- Step 2 (Sandbox Escape): AFR = 5 (Medium)
- Step 3 (Privilege Escalation): AFR = 8 (Medium)

Path AFR = MIN(12, 5, 8) = 5 (Medium)
```

**Interpretation**: Even though installation is easy (AFR=12), the sandbox escape is hard (AFR=5). The entire chain difficulty is 5—the chain is only as easy as its hardest step.

**Note**: Some methodologies use SUM for sequential paths to model cumulative difficulty. ISO 21434 TARA typically uses MIN (weakest link) to represent the limiting factor. Choose the approach that matches your organization's risk framework.

---

### Rule 4: Effective AFR → MAXIMUM Across All Paths

**Formula**: `Effective AFR = MAX(Path1_AFR, Path2_AFR, ..., PathN_AFR)`

**Rationale**: The attacker will exploit the EASIEST overall path to the root goal. The tree's effective feasibility is the maximum AFR across all complete paths.

**Scope note**: Effective AFR is a tree-level analysis metric. It helps prioritize which path is most attractive to the attacker, but downstream `risk_treatment` should still use the AFR recorded on each individual TS entry when calculating RV and treatment decisions.

**Example**:
```
Attack tree with three paths to root:
- Path 1 AFR: 5 (Medium)
- Path 2 AFR: 13 (Low difficulty)
- Path 3 AFR: 7 (Medium)

Effective AFR = MAX(5, 13, 7) = 13 (Low difficulty)
```

**Interpretation**: Despite two moderately hard paths, the attacker will choose Path 2 (AFR=13). The tree's overall feasibility is 13 (Low difficulty for attacker).

---

## AFR Aggregation Worked Example

### Scenario: Multi-Path CAN Injection Attack

**Root Goal**: DS-CAN-001 (Malicious CAN Message Injection)

**Attack Tree**:
```
DS-CAN-001: Malicious CAN Message Injection
    |
    [OR]
    |
    +-- [Path 1] [SEQ]
    |       |
    |       +-- TS-IVI-003: Malicious App Installation (AFR: 10)
    |       +-- TS-IVI-008: Privilege Escalation (AFR: 6)
    |       +-- TS-CAN-005: CAN Injection from IVI (AFR: 9)
    |
    +-- [Path 2] TS-EXT-001: Physical OBD-II CAN Injection (AFR: 13)
```

**Step 1: Calculate Path 1 AFR**
- Path 1 has a [SEQ] gate with three steps
- AFR aggregation: MIN(10, 6, 9) = 6 (weakest link in chain)
- **Path 1 AFR = 6 (Medium)**

**Step 2: Calculate Path 2 AFR**
- Path 2 is a single-step attack (no gates)
- **Path 2 AFR = 13 (Low difficulty)**

**Step 3: Calculate Effective AFR**
- Effective AFR = MAX(Path 1 AFR, Path 2 AFR)
- Effective AFR = MAX(6, 13) = 13
- **Effective AFR = 13 (Low difficulty for attacker)**

**Interpretation**:
- Path 1 (remote IVI chain) is HARDER (AFR=6, Medium difficulty)
- Path 2 (physical OBD-II) is EASIER (AFR=13, Low difficulty)
- Attacker will choose Path 2 → Overall attack feasibility is Low
- Security priority: Mitigate Path 2 first (OBD-II authentication/authorization)

---

## ASCII Art Visualization Guidelines

Attack trees are rendered as ASCII art text trees for portability and readability. Follow these conventions:

### Formatting Rules

1. **Maximum Width**: 80 characters per line (fits standard terminal/code review)
2. **Maximum Depth**: 5 levels (root + 4 child levels) for readability
3. **Indentation**: 4 spaces per level
4. **Connectors**: Use `|`, `+--`, and `    ` for tree structure
5. **Gate Labels**: Explicitly label all gates with `[AND]`, `[OR]`, or `[SEQ]`
6. **Node Format**: `TS-ID: Short Title` or `DS-ID: Short Title`

### Visual Examples

**Simple OR Gate**:
```
DS-CAN-001: CAN Message Injection
    |
    [OR]
    |
    +-- TS-IVI-012: CAN via Compromised IVI
    +-- TS-EXT-001: CAN via OBD-II Port
```

**Nested AND/OR Gates**:
```
DS-IVI-001: Location Tracking
    |
    [AND]
    |
    +-- [OR]
    |   |
    |   +-- TS-IVI-003: Malicious App Access
    |   +-- TS-EXT-004: USB Drive Malware
    |
    +-- TS-IVI-010: Exfiltrate GPS Data
```

**Sequential Chain (SEQ)**:
```
DS-IVI-003: Code Execution on IVI
    |
    [SEQ]
    |
    +-- [Step 1] TS-IVI-001: Install Malicious App
    +-- [Step 2] TS-IVI-007: Sandbox Escape
    +-- [Step 3] TS-IVI-008: Root Privilege Escalation
```

**Complex Multi-Path Tree**:
```
DS-BCK-001: Backend Data Breach
    |
    [OR]
    |
    +-- [Path 1] [SEQ]
    |       |
    |       +-- TS-BCK-003: SQL Injection in API
    |       +-- TS-BCK-008: Lateral Movement to DB
    |       +-- TS-BCK-012: Data Exfiltration
    |
    +-- [Path 2] [AND]
    |       |
    |       +-- TS-BCK-001: Compromised Admin Credentials
    |       +-- TS-BCK-005: Bypass MFA via Session Hijack
    |
    +-- [Path 3] TS-EXT-009: Physical Server Room Access
```

### Width Management Tips

If titles are too long to fit 80 characters:
- Use abbreviations (e.g., "Auth" for "Authentication")
- Reference TS-ID only: `TS-IVI-003` (full title in Leaf Nodes section)
- Break long paths across multiple lines with continuation markers

**Example**:
```
DS-CAN-001: CAN Injection
    |
    [OR]
    |
    +-- [Path 1] TS-IVI-012: CAN via IVI
    |            (Remote attack through compromised
    |             infotainment system)
    |
    +-- [Path 2] TS-EXT-001: CAN via OBD-II
```

---

## Critical Path Analysis

### What is the Critical Path?

The **critical path** is the attack path that poses the greatest practical threat, considering:
1. **Feasibility (AFR)**: How easy is the attack for the attacker?
2. **Attacker motivation**: Which paths align with real-world attacker goals?
3. **Attack surface exposure**: Which paths are accessible in operational context?
4. **Impact**: Do some paths cause more severe damage than others?

### How to Identify the Critical Path

**Step 1: Calculate AFR for all paths**
- Use aggregation rules to compute path-level AFR scores

**Step 2: Identify highest AFR path(s)**
- Highest AFR = easiest for attacker = most likely to be exploited

**Step 3: Apply contextual factors**
- **Physical vs Remote**: Remote attacks scale better (preferred by APTs)
- **Access opportunities**: Physical paths viable if valet/mechanic access common
- **Skill requirements**: Low-skill paths attract opportunistic attackers
- **Detection risk**: Stealthy paths preferred by sophisticated attackers

**Step 4: Select critical path**
- Usually highest AFR path, but context may override
- Document rationale in 2-4 sentences

### Critical Path Example

**Tree**: Three paths to DS-IVI-002 (PII Exposure)
- Path 1 (Remote): AFR = 5 (Medium) — Remote app exploit chain
- Path 2 (Physical USB): AFR = 11 (Low) — USB malware via parking lot drop
- Path 3 (Insider): AFR = 14 (Negligible) — Rogue service technician

**Critical Path**: Path 3 (Insider) despite lower sophistication

**Rationale**: AFR=14 makes this the easiest attack. Service technicians have legitimate physical access during maintenance, creating frequent windows of opportunity. While USB drop (Path 2) also has high AFR (11), it requires social engineering for driver to plug in the device. Insider path is direct and reliable. Priority: Implement service port authentication and audit logging.

---

## Mitigation Point Identification

### What are Mitigation Points?

**Mitigation points** are strategic nodes in the attack tree where implementing security controls can:
- **Block attack paths entirely** (prevent attacker from progressing)
- **Increase attack difficulty** (lower the numeric AFR for the affected path, making it less feasible)
- **Detect attacker activity** (enable incident response)

### Mitigation Strategy Framework

**1. Leaf Node Controls** (Entry Point Defense)
- **Pro**: Stops attacks early, before damage occurs
- **Pro**: Often easier to implement (existing security boundaries)
- **Con**: May require many controls if tree has numerous leaves

**2. Intermediate Node Controls** (Defense-in-Depth)
- **Pro**: Breaks chains even if earlier stages are compromised
- **Pro**: High leverage if node is shared across multiple paths
- **Con**: Attacker has already breached outer defenses

**3. Root Node Controls** (Last-Line Defense)
- **Pro**: Protects final asset directly
- **Con**: Attack has progressed far; may be too late to prevent damage
- **Con**: Root controls often expensive (e.g., data encryption at rest)

### Mitigation Prioritization

**Priority 1: Controls on Critical Path**
- Focus resources on the most likely attack vector first
- Block the easiest path to force attacker to harder alternatives

**Priority 2: High-Leverage Controls**
- Identify nodes that appear in MULTIPLE paths
- Single control can break several attack chains simultaneously

**Priority 3: Low-Cost / High-Impact**
- Prefer controls that are inexpensive to implement but significantly increase AFR
- Example: Input validation (low cost) vs hardware security module (high cost)

**Priority 4: Defense-in-Depth**
- Layer controls across multiple nodes in critical paths
- Ensure no single control failure compromises security

### Mitigation Point Example

**Tree**: DS-CAN-001 with two paths (IVI remote, OBD-II physical)

**Identified Mitigation Points**:
1. **TS-IVI-003 (Malicious App Installation)**
   - Control: App signing + allowlist enforcement
   - Impact: Blocks Path 1 entry point
   - Coverage: Stops all remote IVI-based attacks
   - Priority: HIGH (prevents entire remote chain)

2. **TS-CAN-005 (CAN Injection from Compromised IVI)**
   - Control: CAN gateway message authentication (MAC)
   - Impact: Breaks Path 1 at final stage (defense-in-depth)
   - Coverage: Protects even if IVI is compromised
   - Priority: MEDIUM (backup control for IVI compromise)

3. **TS-EXT-001 (Physical OBD-II CAN Injection)**
   - Control: OBD-II authentication + CAN firewall rules
   - Impact: Blocks Path 2 (critical path with AFR=13)
   - Coverage: Single point of failure for physical attacks
   - Priority: HIGH (critical path control)

**Recommended Approach**: Implement both TS-IVI-003 and TS-EXT-001 controls (blocks both paths). Add TS-CAN-005 control for defense-in-depth against IVI compromise scenarios.

---

## Node Classification Reference

### Root Nodes
- **Definition**: The ultimate attacker goal (what damage is achieved)
- **Source**: Damage Scenario catalogue (`data/ds.md`)
- **Format**: `DS-[DOMAIN]-[NNN]: Title`
- **Count**: Exactly ONE root per attack tree

### Leaf Nodes
- **Definition**: Entry points or initial attack steps (no child nodes)
- **Source**: Threat Scenario catalogue (`data/ts.md`)
- **Format**: `TS-[DOMAIN]-[NNN]: Title`
- **Count**: Typically 2-10 leaves per tree (depends on attack surface)

### Intermediate Nodes
- **Definition**: Sub-goals or attack stages (have both parents and children)
- **Types**: Can be threat scenarios (TS-IDs) or abstract sub-goals
- **Purpose**: Decompose complex attacks into logical stages

### Gate Nodes
- **Definition**: Logical operators that connect nodes
- **Types**: `[AND]`, `[OR]`, `[SEQ]`
- **Count**: At least ONE gate per tree (single-leaf trees are trivial)

---

## Attack Tree Analysis Workflow

**Phase 1: Define Root Goal**
1. Select target damage scenario (DS-ID) as root node
2. Clearly state attacker objective

**Phase 2: Enumerate Attack Paths**
3. Brainstorm all ways to achieve the root goal (divergent thinking)
4. Identify entry points (threat scenarios / TS-IDs)
5. Map intermediate steps between entry and goal

**Phase 3: Structure Tree with Gates**
6. Identify logical relationships (AND/OR/SEQ)
7. Place gates to model dependencies and alternatives
8. Validate gate semantics (can attacker really skip OR alternatives?)

**Phase 4: AFR Calculation**
9. Retrieve AFR scores for all leaf threat scenarios
10. Apply aggregation rules (MIN for AND/SEQ, MAX for OR)
11. Calculate path AFRs and effective AFR

**Phase 5: Critical Path & Mitigation**
12. Identify critical path (highest AFR + context)
13. Locate high-leverage mitigation points
14. Recommend security controls with priorities

**Phase 6: Documentation**
15. Render ASCII tree (max 80 chars, max 5 levels)
16. Document all fields (12 required fields per at-schema.md)
17. Set confidence level based on validation depth

---

## Common Pitfalls and Best Practices

### ❌ Pitfall 1: Confusing Gate Semantics

**Mistake**: Using AND when attacker needs only one path (should be OR)

**Example (WRONG)**:
```
DS-CAN-001
    |
    [AND]  ← WRONG: Attacker doesn't need BOTH paths
    |
    +-- TS-IVI-012: CAN via IVI
    +-- TS-EXT-001: CAN via OBD-II
```

**Correct**:
```
DS-CAN-001
    |
    [OR]  ← CORRECT: Attacker picks ONE path
    |
    +-- TS-IVI-012: CAN via IVI
    +-- TS-EXT-001: CAN via OBD-II
```

---

### ❌ Pitfall 2: Trees Too Deep or Wide

**Mistake**: Creating 8-level trees with 50 leaf nodes (unreadable, unmaintainable)

**Best Practice**:
- Keep trees focused on ONE root goal (one damage scenario)
- If tree exceeds 5 levels, decompose into sub-trees
- If >10 leaves, group similar paths or create separate trees per attack class

---

### ❌ Pitfall 3: Incorrect AFR Aggregation

**Mistake**: Using SUM for AND gates (should be MIN)

**Example (WRONG)**:
```
[AND] gate: AFR = 5 + 8 = 13 ← WRONG
```

**Correct**:
```
[AND] gate: AFR = MIN(5, 8) = 5 ← CORRECT (weakest link)
```

---

### ❌ Pitfall 4: Forgetting Defense-in-Depth

**Mistake**: Placing ALL security controls at entry points (leaf nodes)

**Best Practice**:
- Layer controls across multiple tree levels
- Implement controls at critical intermediate nodes
- Assume some controls will fail; design for resilience

---

### ✅ Best Practice 1: Validate with Red Team

- Test attack tree completeness through penetration testing
- Identify missing paths that theoretical analysis overlooked
- Update confidence level based on empirical validation

---

### ✅ Best Practice 2: Keep Trees Living Documents

- Update AFR scores as controls are implemented (AFR should decrease)
- Add new paths as threat intelligence reveals novel attack vectors
- Re-analyze critical path when security posture changes

---

### ✅ Best Practice 3: Cross-Reference Threat Intelligence

- Use real-world attack examples to validate tree paths (CVEs, NHTSA recalls)
- Incorporate automotive-specific attack research (Miller & Valasek, Checkoway)
- Review MITRE ATT&CK (Mobile, ICS) for enterprise/embedded attack patterns

---

## References and Further Reading

- **ISO 21434:2021 Clause 15.7** - Attack path analysis requirements
- **Schneier, Bruce (1999)** - "Attack Trees" - Foundational methodology for AND/OR gates
- **Miller & Valasek (2015)** - "Remote Exploitation of an Unaltered Passenger Vehicle" - Real-world automotive attack tree example (Jeep Cherokee)
- **Checkoway et al. (2011)** - "Comprehensive Experimental Analyses of Automotive Attack Surfaces" - Systematic attack surface enumeration
- **MITRE ATT&CK for Mobile** - Threat modeling framework for mobile/embedded systems
- **NHTSA Cybersecurity Best Practices** - Automotive industry security guidance
- **SAE J3061** - Cybersecurity Guidebook for Cyber-Physical Vehicle Systems (predecessor to ISO 21434)

---

## Appendix: AFR Aggregation Quick Reference

| Gate Type | Aggregation Rule | Rationale |
|-----------|------------------|-----------|
| **[AND]** | `MIN(children)` | Weakest link limits chain; attacker must succeed at all |
| **[OR]** | `MAX(children)` | Attacker picks easiest; maximum AFR determines feasibility |
| **[SEQ]** | `MIN(steps)` | Chain strength limited by hardest step |
| **Effective AFR** | `MAX(all paths)` | Attacker exploits easiest complete path to root |

**Remember**: Lower AFR = Harder for attacker | Higher AFR = Easier for attacker

---

## Document Metadata

**Version**: 1.0 (2026-03-20)  
**Status**: Active  
**Next Review**: 2027-03-20 or upon ISO 21434 revision
