---
name: threat_scenario
description: >-
  Threat Scenario Analysis for ISO 21434 TARA workflow.
  Triggers: threat scenario, attack path, attack feasibility,
  AFR rating, threat enumeration, cybersecurity attack analysis.
  Input: data/asset_list.md, data/ds.md. Output: data/ts.md.
  ISO 21434 Clause 15.6 threat scenario identification and
  attack feasibility scoring input for downstream analysis.
---
# Threat Scenario Analysis -- Skill Workflow

**Task complete when**: `data/ts.md` exists, every TS entry contains the required core fields, all AST-ID and DS-ID references resolve against `data/asset_list.md` and `data/ds.md`, every AFR includes all 5 factor scores whose sum matches the total, and `python skills/threat_scenario/tools/check_ts.py data/ts.md --asset-list data/asset_list.md --ds data/ds.md` exits 0.

## 1. When to Use This Skill

**Trigger ON** when the user is:
- Conducting threat scenario identification for ISO 21434 TARA
- Creating or updating `data/ts.md`
- Working from an existing asset catalogue (`data/asset_list.md`) and damage scenario catalogue (`data/ds.md`)
- Asking "how could this be attacked", "what attack path is realistic", or "what is the AFR for this threat"
- Preparing threat-scenario inputs for downstream `attack_tree` or `risk_treatment`

**Trigger OFF** when the user asks:
- About asset identification or asset cataloguing (use `asset_analysis`)
- About damage scenarios, SFOP assessment, or impact analysis (use `damage_scenario`)
- About Risk Value (RV), treatment choice, or security control implementation (use `risk_treatment`)
- About generic ISO 21434 theory unrelated to the current project

---

## 2. Repository Quick Reference

Locate the repo root from the working directory -- do NOT hardcode paths.

    data/
      ├── asset_list.md     INPUT: asset catalogue from `asset_analysis`
      ├── ds.md             INPUT: damage scenario catalogue from `damage_scenario`
      └── ts.md             OUTPUT: threat scenario catalogue
    skills/threat_scenario/
      ├── SKILL.md
      ├── assets/
      ├── references/
      └── tools/

**Prerequisites**:
- `data/asset_list.md` exists with at least one valid AST entry and CIA ratings
- `data/ds.md` exists with at least one valid DS entry and impact ratings

**Fallback if missing**:
- Stop and route to the prerequisite skill
- Do not invent assets, damage scenarios, or hidden system context
- If evidence is incomplete, carry assumptions forward explicitly in `data/ts.md`

---

## 3. Core Rules

These rules apply everywhere in this skill -- the workflow steps, validator, and template all assume them.

1. **This skill owns threat scenario identification, not risk treatment.** Do not calculate RV or recommend Avoid / Reduce / Transfer / Accept here.
2. **Threats describe cause, not consequence.** Consequence severity already belongs to `damage_scenario`; threat entries explain how an attacker reaches that consequence.
3. **Use evidence first, assumptions second.** If you do not know a control, interface, or constraint, mark it as an assumption instead of presenting it as verified fact.
4. **Core required fields come first.** Extended metadata is useful but optional unless the user or downstream reporting explicitly requires it.
5. **Do not invent identifiers.** AST-IDs must come from `data/asset_list.md`; DS-IDs must come from `data/ds.md`.
6. **The AFR contract is fixed for this repository.** Use 5 factors, each scored 0-3, total 0-15. Higher numeric AFR means easier for the attacker and worse for the defender.
7. **`data/ts.md` is not complete until the validator exits 0.** Manual review supplements the validator; it does not replace it.

---

## 4. Threat Scenario Workflow

### Step 1 -- Gather Context

Read `data/asset_list.md` and `data/ds.md`.

Build a working list of:
- exposed interfaces / entry points from the asset catalogue
- linked assets per damage scenario
- missing facts that must remain assumptions

Do not infer hidden architecture, threat actors, controls, or attacker capabilities unless the project evidence states them.

### Step 2 -- Enumerate Candidate Threats

Use `references/ts-patterns.md` as a seed list, not as a mandatory checklist.

For each relevant asset / entry point / linked damage scenario:
1. Identify plausible attack paths
2. Link each candidate threat to one or more DS-IDs
3. Note unknowns and assumptions explicitly
4. Carry only realistic, evidence-grounded threats into `data/ts.md`

If a threat does not match an existing pattern, document it anyway. Patterns are starting points, not a completeness requirement.

### Step 3 -- Map Assets -> Damage Scenarios -> Threats

For each DS in `data/ds.md`:
1. Read the linked assets
2. Ask how an attacker could compromise one or more linked assets to realize that damage
3. Document the attack path as one or more TS entries

Rules:
- one TS can lead to multiple DS entries
- one DS can be realized by multiple TS entries
- do not create synthetic TS entries solely to force one-to-one coverage

### Step 4 -- Score Attack Feasibility (AFR)

Use the authoritative scoring rules in `references/afr-guide.md`.

**Repository AFR contract**:
- factors: Elapsed Time, Specialist Expertise, Knowledge of Item, Window of Opportunity, Equipment
- each factor scored 0-3
- total AFR = 0-15
- rating bands use `Very Low / Low / Moderate / High` attacker feasibility
- map scores as follows: `0-4 = Very Low`, `5-9 = Low`, `10-13 = Moderate`, `14-15 = High`
- higher numeric AFR = easier for attacker / worse for defender

Required output per TS:
- total AFR
- all 5 factor scores
- one-sentence justification per factor

Only adjust factor scores based on documented controls or explicitly stated assumptions. Do not invent hidden controls or attacker constraints.

### Step 5 -- Add Classification Metadata

Required:
- STRIDE

Optional when evidence is available or downstream reporting requires it:
- MITRE ATT&CK
- OWASP
- UN R155 Annex 5
- CVE / research examples
- Confidence Level
- Attack Vector

Use `references/framework-mapping.md` for lookup rules.
If no reliable mapping is available, use `N/A` or `hypothetical` with a short reason.

### Step 6 -- Write `data/ts.md`

Use `assets/TEMPLATE.md`.

**Core required fields for every TS**:
1. TS-ID
2. Title
3. Threat Description
4. Target Asset
5. Attack Surface / Entry Point
6. STRIDE Category
7. Damage Scenario Categories
8. Attack Feasibility Rating (AFR)
9. CIA Triad
10. Affected Vehicle Systems

**Extended fields** (fill when evidence is available or audit/reporting needs them):
- UN R155 Annex 5 Reference
- MITRE ATT&CK Reference
- OWASP Reference
- Real-world Examples / CVEs
- Last Updated
- Confidence Level
- Attack Vector

Rules:
- use the template structure; do not invent new required sections
- do not invent AST-ID or DS-ID references
- do not duplicate DS impact inside TS; linked damage scenarios remain the impact source of truth
- if external references cannot be verified, use `N/A` or `hypothetical` with reason
- no placeholder text remains in final output

### Step 7 -- Handoff

`data/ts.md` is an input to `attack_tree` and `risk_treatment`.

Do not calculate Risk Value (RV) or recommend treatment decisions here. Those decisions are owned by `risk_treatment`.

---

## 5. Output Format

Mirror the catalogue shape used by `data/ds.md`:

```markdown
# Threat Scenario Catalogue - [System Name]

**Date**: YYYY-MM-DD
**Scope**: [Brief description]
**Total Threat Scenarios**: [Count]

---

## Summary by Domain (optional convenience — not checked by validator)

| Domain | Count | Examples |
|--------|-------|----------|
| IVI | X | TS-IVI-001, TS-IVI-002 |
| CAN | X | TS-CAN-001 |

## AFR Distribution (optional convenience — not checked by validator)

| AFR Rating | Count | TS-IDs |
|------------|-------|--------|
| Very Low (0-4) | X | ... |
| Low (5-9) | X | ... |
| Moderate (10-13) | X | ... |
| High (14-15) | X | ... |

---

## Threat Scenario Catalogue

[TS entries]
```

The template and schema reference define the exact field formatting.

---

## 6. Validation

Run the validator. It is the authoritative checklist:

    python skills/threat_scenario/tools/check_ts.py data/ts.md --asset-list data/asset_list.md --ds data/ds.md

(From the skill directory use `python tools/check_ts.py /abs/path/data/ts.md --asset-list /abs/path/data/asset_list.md --ds /abs/path/data/ds.md`.) Any non-zero exit blocks handoff to `attack_tree` or `risk_treatment`.

The validator enforces:
- TS-ID format and uniqueness
- required core sections present
- target asset contains a valid AST-ID
- linked DS-IDs resolve when `--ds` is supplied
- AFR includes all 5 factors and the sum matches the total
- no `[TODO]` / `[TBD]` / placeholder text remains

Manual checks the validator cannot perform:
- threat descriptions are technically specific and evidence-grounded
- assumptions are labeled as assumptions
- optional mappings and CVE references are either verified or explicitly marked `N/A` / `hypothetical`
- similar threats are scored consistently across the catalogue

---

## 7. References

**Schema and Template**:
- `references/ts-schema.md` - field definitions, required vs optional metadata, and traceability rules
- `assets/TEMPLATE.md` - blank template plus completed example

**Scoring and Classification**:
- `references/afr-guide.md` - authoritative AFR scoring rules for this repository
- `references/framework-mapping.md` - STRIDE / MITRE / OWASP / UN R155 lookup guidance

**Reusable Seed Content**:
- `references/ts-patterns.md` - reusable threat-pattern seed library
- `references/examples/example-01-ivi.md` - pedagogical full-schema examples for IVI threats
- `references/examples/example-02-can.md` - pedagogical full-schema examples for CAN threats

**Validator**:
- `tools/check_ts.py` - authoritative validation gate for `data/ts.md`

---

## 8. Troubleshooting

**"I don't know where to start"**:
→ Begin with `references/ts-patterns.md`, then walk from linked assets in `data/ds.md` back to realistic attack paths.

**"AFR scores seem arbitrary"**:
→ Re-read `references/afr-guide.md` and ensure every factor score has one evidence-grounded justification sentence.

**"I have incomplete evidence"**:
→ Write the TS with explicit assumptions, avoid unverifiable mappings, and lower `Confidence Level` accordingly.

**"All my AFR scores are Very Low (0-4)"**:
→ Re-check `Specialist Expertise` and `Knowledge of Item`; most practical automotive attacks require at least some public knowledge or professional skill.

**"My threat doesn't fit any pattern"**:
→ Document it anyway. Patterns are a seed list, not a completeness rule.

**"No CVE exists for my threat"**:
→ Use `No public CVE - hypothetical based on [reason]` or cite security research instead.

---

**End of Skill Workflow**

---
