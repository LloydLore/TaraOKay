# Attack Tree Template

Use this template to document each attack tree. Copy this structure and fill in all 12 required fields per `references/at-schema.md`.

**Usage note -- choose one mode before writing**:
- **Validated mode**: use real TS-IDs from `data/ts.md`, use AFR values sourced from those TS entries, and remove all placeholder markers before treating the result as handoff-ready `data/at.md` content.
- **Draft / practice mode**: only when `data/ts.md` is missing or incomplete. In this mode, placeholder TS-IDs may be marked `[EXAMPLE]` and AFR values may be estimated, but the resulting entry must be treated as non-handoff output until the placeholders are replaced.

**Rule**: do not mix validated and draft data in the same AT entry. If any path depends on placeholder TS-IDs or estimated AFR values, mark the whole entry as draft/practice output.

---

## Section 1: Blank Template

### AT-[DOMAIN]-[NNN]: [Attack Tree Title]
<!-- 
  AT-ID Format: AT-[DOMAIN]-[NNN]
  Domain codes: CAN | OTA | EXT | BCK | IVI | IMM | ADAS
  Number: 3-digit zero-padded (001, 002, ..., 999)
  
  Domain Definitions (based on primary attack domain or root DS-ID domain):
  - CAN: CAN bus and in-vehicle networking attacks
  - OTA: Over-the-air update and remote service attacks
  - EXT: External interface and physical access attacks
  - BCK: Backend/cloud service and API attacks
  - IVI: Infotainment application and OS attacks
  - IMM: Immobilizer and vehicle access control attacks
  - ADAS: Advanced driver assistance system attacks
  
  Title Guidelines:
  - Max 80 characters
  - Describe the ATTACK GOAL (what attacker achieves), not individual steps
  - Be specific and include domain context when helpful
  
  Examples:
  - AT-IVI-001: Malicious App Chain to Data Exfiltration
  - AT-CAN-001: Remote CAN Injection via Multiple Entry Points
  - AT-OTA-002: Privileged Code Execution Through OTA Update
  - AT-EXT-001: Physical Access to Persistent Vehicle Tracking
  - AT-BCK-001: Backend Compromise Leading to Fleet Control
  - AT-IMM-001: Vehicle Theft via Immobilizer Bypass
  - AT-ADAS-001: Sensor Spoofing to Manipulate Vehicle Behavior
-->

**Root Goal**:
<!-- 
  The damage scenario (DS-ID) that this attack tree achieves.
  Format: DS-[DOMAIN]-[NNN]: [Title]
  
  Guidelines:
  - DS-ID MUST exist in data/ds.md
  - Only ONE root goal per attack tree
  - Root domain should typically match AT-ID domain
  
  Example:
  DS-CAN-001: Malicious CAN Message Injection
-->

DS-[DOMAIN]-[NNN]: [Damage Scenario Title]

**Attack Tree Structure**:
<!-- 
  ASCII art representation of the attack tree using gate notation.
  
  Gate Types:
  - [AND]: ALL children must succeed
  - [OR]: ANY child sufficient
  - [SEQ]: Sequential order required
  
  Formatting Rules:
  - Maximum 80 characters per line
  - Maximum 5 levels depth (including root)
  - Use consistent 4-space indentation
  - Label all gates explicitly
  
  Example Format:
  DS-XXX-NNN: Root Goal Title
      |
      [OR]
      |
      +-- [Path 1] [SEQ]
      |       |
      |       +-- TS-YYY-001: First Step
      |       +-- TS-YYY-002: Second Step
      |
      +-- [Path 2] TS-ZZZ-001: Alternative Path
-->

```
DS-[DOMAIN]-[NNN]: [Root Goal Title]
    |
    [GATE]
    |
    +-- [Child nodes or paths]
```

**Attack Paths**:
<!-- 
  Enumerate all distinct attack paths from leaf nodes to root goal.
  
  Format:
  1. **Path N (Description)**:
     - TS-XXX-NNN → TS-YYY-NNN → DS-ZZZ-NNN
     - Description: [Brief explanation of approach]
  
  Guidelines:
  - Number paths sequentially (1, 2, 3, ...)
  - Use arrow notation (→) for progression
  - Include 1-2 sentence description per path
  - Paths must start at leaf (TS-ID) and end at root (DS-ID)
  
  Example:
  1. **Path 1 (Remote via IVI)**:
     - TS-IVI-003 → TS-IVI-008 → TS-CAN-005 → DS-CAN-001
     - Description: Attacker gains IVI access remotely, escalates privileges, 
       then injects CAN messages from compromised infotainment system.
-->

1. **Path 1 ([Description])**:
   - [TS-ID] → [TS-ID] → ... → [DS-ID]
   - Description: [Approach explanation]

2. **Path 2 ([Description])**:
   - [TS-ID] → [DS-ID]
   - Description: [Approach explanation]

**Leaf Nodes**:
<!-- 
  List all threat scenarios (TS-IDs) that appear as leaf nodes in the tree.
  
  Format:
  - TS-XXX-NNN: [Short Title]
  
  Guidelines:
  - Include TS-ID and brief title for each leaf
  - Mark [EXAMPLE] if TS catalogue doesn't exist yet
  - Provide total count for verification
  - No duplicates unless same TS appears in independent paths
  
  Example:
  - TS-IVI-003: Malicious App Installation on IVI
  - TS-EXT-001: CAN Injection via OBD-II Adapter
  
  Total: 2 leaf nodes
-->

- TS-[DOMAIN]-[NNN]: [Leaf Node Title]
- TS-[DOMAIN]-[NNN]: [Leaf Node Title]

Total: [N] leaf nodes

**Path AFR Analysis**:
<!-- 
  Calculate AFR for each attack path using aggregation rules.
  
  Aggregation Rules:
  - AND gates: MIN(child AFRs) - weakest link limits chain
  - OR gates: MAX(child AFRs) - attacker picks easiest
  - SEQ gates: MIN(step AFRs) - chain strength limited by hardest step
  
  AFR Rating Bands:
  - 0-4: High (attack difficulty - hard for attacker)
  - 5-9: Medium
  - 10-13: Low (attack difficulty - easier for attacker)
  - 14-15: Negligible (very easy for attacker)
  
  Format:
  **Path N ([Description])**:
  - TS-XXX-NNN AFR: [score] ([rating])
  - TS-YYY-NNN AFR: [score] ([rating])
  - Aggregation: [Gate type] → [Formula] = [result]
  - **Path N AFR: [score] ([rating])**
  
  Example:
  **Path 1 (Remote via IVI)**:
  - TS-IVI-003 AFR: 10 (Low)
  - TS-IVI-008 AFR: 6 (Medium)
  - TS-CAN-005 AFR: 9 (Medium)
  - Aggregation: SEQ gate → MIN(10, 6, 9) = 6
  - **Path 1 AFR: 6 (Medium)**
-->

**Path 1 ([Description])**:
- TS-XXX-NNN AFR: [score] ([rating])
- Aggregation: [Gate] → [Formula] = [result]
- **Path 1 AFR: [score] ([rating])**

**Path 2 ([Description])**:
- TS-YYY-NNN AFR: [score] ([rating])
- Aggregation: [Gate] → [Formula] = [result]
- **Path 2 AFR: [score] ([rating])**

**Effective AFR**:
<!-- 
  The tree's overall attack feasibility (attacker's optimal choice).
  
  Formula: Effective AFR = MAX(all path AFRs)
  
  Rationale: Attacker will exploit easiest available path
  Use this tree-level AFR for attack-tree prioritization only. Downstream risk treatment uses the AFR on the individual TS entries, not the tree effective AFR.
  
  Format:
  **Effective AFR**: [score] ([rating])
  
  **Rationale**: [2-3 sentences explaining why this path is most likely]
  
  Example:
  **Effective AFR**: 13 (Low)
  
  **Rationale**: Attacker will choose Path 2 (physical OBD-II, AFR=13) over 
  Path 1 (remote IVI chain, AFR=6) because despite requiring physical access, 
  it has significantly fewer technical barriers and requires minimal 
  sophistication compared to the multi-stage compromise chain.
-->

**Effective AFR**: [score] ([rating])

**Rationale**: [Explanation of why maximum path is most likely]

**Critical Path**:
<!-- 
  The attack path posing the greatest practical threat.
  
  Usually the path with highest AFR (easiest for attacker), but consider:
  - Real-world access opportunities (physical vs remote)
  - Attacker motivation and skill level
  - Detection risk and stealth requirements
  
  Format:
  **Critical Path**: Path [N] ([Name])
  
  **Justification**: [2-4 sentences explaining selection and security priority]
  
  Example:
  **Critical Path**: Path 2 (Physical via OBD-II)
  
  **Justification**: While Path 1 offers remote attack capability, Path 2's 
  significantly higher AFR (13 vs 6) makes it the more accessible approach. 
  Physical access to OBD-II is trivial for opportunistic attackers (valet, 
  mechanic, parking lot scenarios). Security controls should prioritize 
  blocking this path first.
-->

**Critical Path**: Path [N] ([Name])

**Justification**: [Explanation of why this path is most threatening and should be prioritized]

**Mitigation Points**:
<!-- 
  Strategic nodes where security controls can disrupt attack paths.
  
  For each mitigation point, specify:
  1. TS-ID (node location)
  2. Control type (what security measure)
  3. Impact on paths (which paths are broken/degraded)
  4. Coverage assessment (how many paths affected)
  
  Prioritize:
  - Controls on critical path (highest threat)
  - High-leverage controls (break multiple paths)
  - Low-cost / high-impact controls (efficient security investment)
  
  Format:
  1. **TS-XXX-NNN ([Title])**
     - Control: [Security measure description]
     - Impact: [Effect on paths]
     - Coverage: [High/Medium/Low - how many paths affected]
  
  **Recommended Priority**: [Which mitigation to implement first and why]
  
  Example:
  1. **TS-EXT-001 (Physical OBD-II Access)**
     - Control: OBD-II port authentication + CAN firewall rules
     - Impact: Blocks Path 2 entirely (physical attack vector)
     - Coverage: High (eliminates critical path)
  
  2. **TS-IVI-003 (Malicious App Installation)**
     - Control: App signing enforcement + allowlist verification
     - Impact: Blocks Path 1 at entry point
     - Coverage: Medium (defense for remote chain)
  
  **Recommended Priority**: Implement TS-EXT-001 control first (blocks critical 
  path with highest AFR), then add TS-IVI-003 for defense-in-depth.
-->

1. **TS-[DOMAIN]-[NNN] ([Title])**
   - Control: [Security measure]
   - Impact: [Effect on paths]
   - Coverage: [High/Medium/Low]

2. **TS-[DOMAIN]-[NNN] ([Title])**
   - Control: [Security measure]
   - Impact: [Effect on paths]
   - Coverage: [High/Medium/Low]

**Recommended Priority**: [Priority guidance and rationale]

**Last Updated**:
<!-- 
  ISO 8601 date format (YYYY-MM-DD) or timestamp
  
  Update when:
  - Tree structure changes (new paths, revised gates)
  - AFR scores updated due to new TS analysis
  - New mitigation points identified
  
  Example: 2026-03-20 or 2026-03-20T14:30:00Z
-->

YYYY-MM-DD

**Confidence Level**:
<!-- 
  Assessment: High | Medium | Low
  
  Criteria:
  - High: Validated through pentesting/red team, all major vectors identified
  - Medium: Based on threat modeling and expert analysis, likely complete
  - Low: Preliminary/theoretical, significant unknowns, requires validation
  
  Format:
  Confidence Level: [High/Medium/Low]
  
  **Justification**: [2-3 sentences explaining confidence rating and gaps]
  
  Example:
  Confidence Level: Medium
  
  **Justification**: Tree structure validated against public automotive security 
  research. AFR scores derived from expert assessment. However, proprietary CAN 
  gateway architecture not fully analyzed—additional paths may exist through 
  undiscovered vulnerabilities.
-->

Confidence Level: [High/Medium/Low]

**Justification**: [Confidence rationale and known gaps/uncertainties]

---

## Section 2: Completed Example

### AT-CAN-001: Remote CAN Injection via Multiple Entry Points

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
    |       +-- TS-IVI-003: Malicious App Installation
    |       +-- TS-IVI-008: IVI Privilege Escalation
    |       +-- TS-CAN-005: CAN Injection from IVI
    |
    +-- [Path 2] TS-EXT-001: Physical OBD-II CAN Injection
```

**Attack Paths**:

1. **Path 1 (Remote via IVI)**:
   - TS-IVI-003 → TS-IVI-008 → TS-CAN-005 → DS-CAN-001
   - Description: Attacker remotely installs a malicious app on the IVI, 
     exploits a privilege escalation vulnerability to gain root access, 
     then injects arbitrary CAN messages from the compromised infotainment 
     system to the vehicle's CAN bus network.

2. **Path 2 (Physical via OBD-II)**:
   - TS-EXT-001 → DS-CAN-001
   - Description: Attacker with physical access connects a CAN adapter to 
     the vehicle's OBD-II diagnostic port and directly injects malicious 
     CAN frames onto the bus. Single-step attack requiring no sophistication 
     beyond basic CAN protocol knowledge.

**Leaf Nodes**:

- TS-IVI-003: Malicious App Installation on IVI [EXAMPLE]
- TS-IVI-008: IVI Privilege Escalation Exploit [EXAMPLE]
- TS-CAN-005: CAN Frame Injection from Compromised IVI [EXAMPLE]
- TS-EXT-001: CAN Injection via OBD-II Adapter [EXAMPLE]

Total: 4 leaf nodes

**Path AFR Analysis**:

**Path 1 (Remote via IVI)**:
- TS-IVI-003 AFR: 10 (Low difficulty - sideload APK via USB)
- TS-IVI-008 AFR: 6 (Medium - kernel exploit requires proficiency)
- TS-CAN-005 AFR: 9 (Medium - CAN socket access from root)
- Aggregation: SEQ gate → MIN(10, 6, 9) = 6 (weakest link)
- **Path 1 AFR: 6 (Medium)**

**Path 2 (Physical via OBD-II)**:
- TS-EXT-001 AFR: 13 (Low difficulty - $50 adapter + free tools)
- Aggregation: Single-step path (no gates)
- **Path 2 AFR: 13 (Low difficulty)**

**Effective AFR**:

**Effective AFR**: 13 (Low difficulty)

**Rationale**: Attacker will choose Path 2 (physical OBD-II access, AFR=13) 
over Path 1 (remote IVI chain, AFR=6) because it offers significantly lower 
technical barriers despite requiring physical access. Path 2 requires only 
basic CAN protocol knowledge and commodity hardware, whereas Path 1 demands 
kernel exploitation expertise and multi-stage orchestration. For opportunistic 
attackers (valet, mechanic, parking lot scenarios), physical access to OBD-II 
is trivially achievable, making this the dominant threat vector.

**Critical Path**:

**Critical Path**: Path 2 (Physical via OBD-II)

**Justification**: Path 2 represents the greatest practical threat due to its 
high AFR (13) and low skill barrier. Physical access opportunities are abundant 
in real-world scenarios: valet parking, service appointments, rental vehicles, 
and unattended vehicles in public lots. The attack requires only commodity CAN 
adapters ($50-$200) and publicly available tools (can-utils, python-can), with 
no sophisticated exploitation required. While Path 1 offers remote attack 
capability preferred by APT actors, Path 2's accessibility makes it viable for 
a much broader attacker population. Security controls must prioritize blocking 
physical CAN access vectors before addressing remote IVI chains.

**Mitigation Points**:

1. **TS-EXT-001 (Physical OBD-II CAN Injection)**
   - Control: OBD-II port authentication protocol + CAN gateway firewall rules 
     restricting diagnostic message injection
   - Impact: Blocks Path 2 entirely (eliminates critical path)
   - Coverage: High (single point of failure for physical attacks)

2. **TS-CAN-005 (CAN Injection from Compromised IVI)**
   - Control: CAN gateway message authentication code (MAC) verification for 
     IVI-originated frames + rate limiting
   - Impact: Breaks Path 1 at final stage (defense-in-depth even if IVI is 
     compromised)
   - Coverage: Medium (protects against IVI compromise scenarios)

3. **TS-IVI-003 (Malicious App Installation)**
   - Control: App signing enforcement + allowlist-only installation policy + 
     SELinux mandatory access control
   - Impact: Blocks Path 1 at entry point (prevents IVI compromise chain)
   - Coverage: Medium (defense against remote attack vector)

**Recommended Priority**: Implement TS-EXT-001 control immediately (blocks 
critical path AFR=13). Follow with TS-CAN-005 for defense-in-depth (protects 
even if IVI or other ECUs are compromised). Add TS-IVI-003 as tertiary 
control to harden remote attack surface.

**Last Updated**:

2026-03-20

**Confidence Level**:

Confidence Level: Medium

**Justification**: Tree structure validated against published automotive 
security research (Miller & Valasek 2015, Checkoway et al. 2011). AFR scores 
derived from expert assessment and industry penetration testing experience. 
However, proprietary CAN gateway filtering rules and ECU authentication 
mechanisms were not fully reverse-engineered—additional bypass paths may exist 
through undocumented diagnostic services or gateway vulnerabilities. Recommend 
red team validation and gateway firmware analysis to increase confidence to High.

---

## Quick Checklist

Before committing your attack tree to the catalogue, verify:

- [ ] AT-ID follows `AT-[DOMAIN]-[NNN]` format with valid domain code
- [ ] Root Goal references an existing DS-ID from `data/ds.md`
- [ ] Attack Tree Structure uses only [AND], [OR], [SEQ] gate notation
- [ ] ASCII tree fits within 80 characters width and 5 levels depth
- [ ] All Attack Paths enumerated from leaf nodes to root goal
- [ ] All Leaf Nodes listed with TS-IDs (or marked [EXAMPLE])
- [ ] Path AFR Analysis shows aggregation logic for each path
- [ ] Effective AFR calculated as MAX(all path AFRs)
- [ ] Critical Path identified with 2-4 sentence justification
- [ ] Mitigation Points list 2-5 strategic intervention points with priority
- [ ] Last Updated uses ISO 8601 date format
- [ ] Confidence Level includes justification and known gaps

**If all checkboxes pass → commit to `data/at.md`**
