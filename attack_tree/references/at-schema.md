# Attack Tree Schema - ISO 21434 TARA

This document defines the required fields for attack tree analysis in ISO 21434 TARA (Threat Analysis and Risk Assessment) workflows, aligned with Clause 15.7 (Attack Path Analysis).

---

## Required Fields

Every attack tree in the AT catalogue must include ALL 12 required fields:

### 1. AT-ID

**Format**: `AT-[DOMAIN]-[NNN]`

**Description**: Unique identifier for the attack tree following a structured naming convention based on the primary attack domain.

**Domain Codes**:
- `CAN` - CAN bus and in-vehicle networking attacks
- `OTA` - Over-the-air updates and remote services attacks
- `EXT` - External interfaces and physical access point attacks
- `BCK` - Backend/cloud services and infrastructure attacks
- `IVI` - Infotainment and in-vehicle information system attacks
- `IMM` - Immobilizer and vehicle access control attacks
- `ADAS` - Advanced driver assistance system attacks

**Example**: `AT-IVI-001`, `AT-CAN-002`, `AT-ADAS-003`

**Rules**:
- Check existing IDs before assigning to avoid conflicts
- Use zero-padded 3-digit numbers (001, 002, ..., 999)
- Domain code must match the primary attack surface or root damage scenario
- If cross-domain attack paths exist, use the domain of the root goal (damage scenario)
- Maximum of 7 domains—no new domain codes allowed

---

### 2. Title

**Format**: Human-readable text (maximum 80 characters)

**Description**: Concise, descriptive name for the attack tree that identifies the attack objective or root goal.

**Example**: 
- "Malicious App Chain to Data Exfiltration"
- "Remote CAN Injection via Multiple Entry Points"
- "Privileged Code Execution Through OTA Update"
- "Vehicle Theft via Immobilizer Bypass"

**Rules**:
- Focus on the ATTACK GOAL (what the attacker achieves), not individual steps
- Use action-oriented language describing the objective
- Be specific enough to distinguish from similar attack trees
- Include domain context when helpful for clarity
- Keep under 80 characters for readability

---

### 3. Root Goal

**Format**: DS-ID from damage scenario catalogue with full title

**Description**: The damage scenario (DS-ID) that serves as the root node of the attack tree, representing what the attacker ultimately achieves.

**Example**:
```
Root Goal: DS-IVI-001 (Unauthorized Driver Location Tracking)
Root Goal: DS-CAN-001 (Malicious CAN Message Injection)
Root Goal: DS-BCK-001 (Telematics Backend Data Breach)
```

**Rules**:
- DS-ID MUST exist in `data/ds.md`
- Use full format: `DS-[DOMAIN]-[NNN] (Title)`
- Only ONE root goal per attack tree
- Root goal defines success criterion for all attack paths
- Root domain should match AT-ID domain (exceptions allowed for cross-domain attacks)

---

### 4. Attack Tree Structure

**Format**: ASCII art representation with AND/OR/SEQ gate notation

**Description**: Hierarchical visualization of attack paths from leaf nodes (threat scenarios) to the root goal (damage scenario), showing logical relationships through gates.

**Gate Notation**:
- `[AND]` - All children must succeed (conjunctive gate)
- `[OR]` - Any child is sufficient (disjunctive gate)
- `[SEQ]` - Sequential order required (ordered gate)

**Example**:
```
DS-CAN-001: Malicious CAN Message Injection
    |
    [OR]
    |
    +-- [Path 1] [SEQ]
    |       |
    |       +-- TS-IVI-003: Gain IVI Shell Access
    |       +-- TS-IVI-008: Escalate to Root Privileges
    |       +-- TS-CAN-005: Inject CAN Frames from IVI
    |
    +-- [Path 2] TS-EXT-001: Physical OBD-II CAN Injection
```

**Rules**:
- Maximum width: 80 characters per line
- Maximum depth: 5 levels (including root)
- Use consistent indentation (4 spaces per level)
- Label all gates explicitly with [AND], [OR], or [SEQ]
- Leaf nodes must reference TS-IDs (threat scenarios)
- Intermediate nodes may group sub-goals or gate outputs
- Root node must match the Root Goal DS-ID

---

### 5. Attack Paths

**Format**: Enumerated list of distinct attack paths from leaf to root

**Description**: Complete enumeration of all possible attack chains through the tree, showing the sequence of threat scenarios that achieve the root goal.

**Example**:
```
**Attack Paths**:

1. **Path 1 (Remote via IVI)**: 
   - TS-IVI-003 → TS-IVI-008 → TS-CAN-005 → DS-CAN-001
   - Description: Attacker gains IVI access, escalates privileges, then injects CAN messages

2. **Path 2 (Physical via OBD-II)**:
   - TS-EXT-001 → DS-CAN-001
   - Description: Attacker uses direct physical access to OBD-II diagnostic port
```

**Rules**:
- Number paths sequentially (1, 2, 3, ...)
- Use arrow notation (→) to show attack progression
- Include brief description of each path's approach
- Paths must start at leaf nodes (TS-IDs) and end at root goal (DS-ID)
- All paths must be viable (logically feasible attack sequences)
- Paths through AND gates must include ALL children before progressing

---

### 6. Leaf Nodes

**Format**: List of all TS-IDs at the tree's leaf positions

**Description**: Complete inventory of threat scenarios (leaf nodes) that serve as entry points or initial steps in the attack tree.

**Example**:
```
**Leaf Nodes**:
- TS-IVI-003: Malicious App Installation on IVI
- TS-IVI-008: IVI Privilege Escalation Exploit
- TS-CAN-005: CAN Frame Injection from Compromised IVI
- TS-EXT-001: CAN Injection via OBD-II Adapter

Total: 4 leaf nodes
```

**Rules**:
- List all TS-IDs that appear as leaf nodes in the tree
- TS-IDs may be marked `[EXAMPLE]` if threat scenario catalogue doesn't exist yet
- Include TS-ID and short title for each leaf node
- Provide total count for verification
- Each leaf node must have an AFR score (from threat scenario analysis)
- Leaf nodes should not repeat (unless same TS appears in multiple independent paths)

---

### 7. Path AFR Analysis

**Format**: AFR calculation for each path with aggregation logic

**Description**: Attack Feasibility Rating (AFR) for each attack path, computed by aggregating AFR scores from threat scenarios according to gate rules.

**Aggregation Rules**:
- **AND gates**: `MIN(child AFRs)` - Hardest step limits the chain (attacker must succeed at all)
- **OR gates**: `MAX(child AFRs)` - Attacker picks easiest option (highest AFR = easiest)
- **SEQ gates**: `MIN(step AFRs)` - Chain strength limited by the hardest step in sequence
- **Single-step paths**: AFR = leaf node AFR (no aggregation)

**Example**:
```
**Path AFR Analysis**:

**Path 1 (Remote via IVI)**:
- TS-IVI-003 AFR: 8 (Medium)
- TS-IVI-008 AFR: 6 (Medium)
- TS-CAN-005 AFR: 10 (Low)
- Aggregation: SEQ gate → MIN(8, 6, 10) = 6 (weakest link in chain)
- **Path 1 AFR: 6 (Medium)**

**Path 2 (Physical via OBD-II)**:
- TS-EXT-001 AFR: 13 (Low)
- Aggregation: Single-step path (no gates)
- **Path 2 AFR: 13 (Low)**
```

**Rules**:
- Calculate AFR for EVERY enumerated attack path
- Show intermediate calculations for complex trees with multiple gates
- Use AFR rating labels: Very Low (0-4), Low (5-9), Moderate (10-13), High (14-15)
- Lower AFR = harder attack; higher AFR = easier attack
- AFR scores are inherited from threat scenario catalogue (TS AFR)
- Document aggregation logic used for each path

---

### 8. Effective AFR

**Format**: Single AFR score representing the tree's overall attack feasibility

**Description**: The effective Attack Feasibility Rating for the entire attack tree, computed as the MAXIMUM AFR across all attack paths (attacker's optimal choice).

**Example**:
```
**Effective AFR**: 13 (Low)

**Rationale**: Attacker will choose Path 2 (physical OBD-II access, AFR=13) 
over Path 1 (remote IVI chain, AFR=6) because it has fewer barriers and 
higher feasibility despite requiring physical access.
```

**Rules**:
- Effective AFR = `MAX(all path AFRs)`
- Rationale: Attacker will exploit the easiest available path
- Include AFR rating label (High/Medium/Low/Negligible)
- Provide brief justification for why the maximum path is most likely
- Effective AFR is a tree-level prioritization metric only; downstream `risk_treatment` must use the AFR recorded on individual TS entries when calculating Risk Value.
- Lower effective AFR = more difficult attack overall; higher = more accessible

---

### 9. Critical Path

**Format**: Identification of the most likely attack path with justification

**Description**: The attack path that poses the greatest practical threat, considering both feasibility (AFR) and real-world attacker behavior.

**Example**:
```
**Critical Path**: Path 2 (Physical via OBD-II)

**Justification**: 
While Path 1 offers remote attack capability, Path 2's significantly higher 
AFR (13 vs 6) makes it the more accessible approach. Physical access to 
OBD-II is trivial for opportunistic attackers (valet, mechanic, parking lot 
scenarios). The single-step attack requires minimal sophistication compared 
to the multi-stage IVI compromise chain. Security controls should prioritize 
this path.
```

**Rules**:
- Typically the path with highest AFR (easiest for attacker)
- Consider real-world context: physical access opportunities, attacker motivation, skill level
- May differ from highest AFR if practical factors dominate (e.g., a remote path is harder but still preferred for scale or stealth)
- Provide 2-4 sentence justification explaining the selection
- Critical path guides prioritization of security controls and mitigation efforts

---

### 10. Mitigation Points

**Format**: List of strategic intervention points where security controls can disrupt attack paths

**Description**: Identification of nodes in the attack tree where implementing security controls would break attack chains or significantly increase attacker difficulty.

**Example**:
```
**Mitigation Points**:

1. **TS-IVI-003 (Malicious App Installation)**
   - Control: App signing enforcement + allowlist verification
   - Impact: Blocks Path 1 at entry point
   - Coverage: High (prevents entire remote attack chain)

2. **TS-CAN-005 (CAN Injection from IVI)**
   - Control: CAN gateway authentication + message authorization
   - Impact: Breaks Path 1 even if IVI is compromised
   - Coverage: Medium (defense-in-depth for IVI compromise)

3. **TS-EXT-001 (Physical OBD-II Access)**
   - Control: OBD-II port authentication + CAN firewall rules
   - Impact: Blocks Path 2 (physical attack)
   - Coverage: High (single point of failure for this path)

**Recommended Priority**: Mitigation at TS-EXT-001 (blocks critical path with single control)
```

**Rules**:
- Identify 2-5 strategic mitigation points in the tree
- For each point, specify: TS-ID, proposed control type, impact on paths, coverage assessment
- Prioritize controls that break multiple paths (high leverage)
- Prioritize controls on the critical path
- Consider cost-effectiveness: controls at leaf nodes often more practical than at root
- Note if control reduces AFR (makes attack harder) vs blocks path entirely

---

### 11. Last Updated

**Format**: ISO 8601 date (YYYY-MM-DD)

**Description**: Date when the attack tree was last modified or reviewed.

**Example**: `Last Updated: 2026-03-20`

**Rules**:
- Update whenever tree structure changes (new paths, revised gates)
- Update when AFR scores change due to new threat scenario analysis
- Update when new mitigation points are identified
- Use ISO 8601 format (YYYY-MM-DD)
- Include time if precision is needed: `2026-03-20T14:30:00Z`

---

### 12. Confidence Level

**Format**: One of three ratings: High / Medium / Low

**Description**: Assessment of confidence in the attack tree's completeness and accuracy, based on available threat intelligence and analysis depth.

**Example**:
```
Confidence Level: Medium

**Justification**: Tree structure validated against public automotive security 
research (Miller & Valasek 2015, Checkoway et al. 2011). AFR scores derived 
from expert assessment. However, proprietary CAN gateway architecture not 
fully analyzed—additional paths may exist through undiscovered gateway 
vulnerabilities.
```

**Confidence Criteria**:

| Rating | Criteria |
|--------|----------|
| **High** | Tree validated through penetration testing, red team exercises, or detailed reverse engineering. All major attack vectors identified with high certainty. AFR scores validated through empirical testing. |
| **Medium** | Tree based on threat modeling, public research, and expert analysis. Major attack vectors likely identified, but some uncertainty remains. AFR scores are expert estimates. |
| **Low** | Tree is preliminary or theoretical. Limited validation, significant unknowns about item architecture. AFR scores are rough approximations. Requires further analysis. |

**Rules**:
- Provide brief justification (2-3 sentences) for confidence rating
- Note specific gaps or uncertainties that limit confidence
- Update confidence level as additional validation is performed
- Low confidence trees should be flagged for additional research/testing
- Confidence affects risk treatment decisions (low confidence may require more conservative controls)

---

## Validation Checklist

Use this checklist to verify attack tree completeness before committing to the catalogue:

- [ ] AT-ID follows `AT-[DOMAIN]-[NNN]` format with valid domain code
- [ ] Root Goal references an existing DS-ID from `data/ds.md`
- [ ] Attack Tree Structure uses only [AND], [OR], [SEQ] gate notation
- [ ] ASCII tree fits within 80 characters width and 5 levels depth
- [ ] All Attack Paths enumerated from leaf nodes to root goal
- [ ] All Leaf Nodes listed with TS-IDs (or marked [EXAMPLE])
- [ ] Path AFR Analysis shows aggregation logic for each path
- [ ] Effective AFR calculated as MAX(all path AFRs)
- [ ] Critical Path identified with justification
- [ ] Mitigation Points list 2-5 strategic intervention points
- [ ] Last Updated uses ISO 8601 date format
- [ ] Confidence Level includes justification

---

## Schema Evolution

**Version**: 1.0 (2026-03-20)

**Change History**:
- 2026-03-20: Initial schema definition (12 fields, ASCII art trees, AFR aggregation rules)

**Future Considerations**:
- Integration with attack chain (AC) metadata when AC schema is defined
- Standardized mitigation control taxonomy for Mitigation Points field
- Quantitative risk metrics beyond AFR (e.g., expected loss, attack cost models)

---

## References

- ISO 21434:2021 Clause 15.7 - Attack Path Analysis
- `skills/threat_scenario/references/afr-guide.md` - AFR scoring methodology
- `data/ds.md` - Damage scenario catalogue (root goals)
- `data/ts.md` - Threat scenario catalogue (leaf nodes) [future]
- Schneier, Bruce - Attack Trees (foundational AND/OR gate methodology)
