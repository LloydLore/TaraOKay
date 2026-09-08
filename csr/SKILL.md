---
name: csr
version: 1.0.0
description: Cybersecurity Requirement (CSR) derivation skill for ISO 21434 TARA workflow. Derives technical requirements from cybersecurity goals and design specifications. Performs gap analysis between implemented controls and required controls. Aligns with Clause 9.4 (Cybersecurity specifications).
---
# Cybersecurity Requirement (CSR) -- Skill Workflow

## 1. When to Use This Skill

**Trigger ON** when the user is:
- Deriving cybersecurity requirements from cybersecurity goals (CSG catalogue)
- Specifying technical security controls and implementation requirements
- Performing gap analysis between implemented controls and required controls
- Working with existing cybersecurity goals (`data/csg.md`) and design specifications
- Asking about "cybersecurity requirement", "CSR", "security control", "implementation requirement", "technical requirement"
- Starting ISO 21434 Clause 9.4 (Cybersecurity specifications) work
- Documenting implemented security controls (Part A) or identified gaps (Part B)
- Prioritizing security gaps based on risk treatment decisions
- Preparing inputs for cybersecurity validation testing
- Creating traceability matrix linking CSRs back to CSGs, threat scenarios, and risk treatments

**Trigger OFF** when the user asks:
- About cybersecurity goals or security objectives (use `csg` skill instead)
- About high-level "WHAT must be protected" questions (CSG domain, not CSR)
- About damage scenarios, impact analysis, or SFOP assessment (use `damage_scenario` skill instead)
- About threat scenarios, attack paths, or AFR rating (use `threat_scenario` skill instead)
- About risk treatment decisions or control selection (use `risk_treatment` skill instead)
- General ISO 21434 theory unrelated to technical requirement specification
- Vehicle design or engineering topics not related to security controls

**CRITICAL DISTINCTION - CSR vs CSG**:
- **CSG (separate skill)**: High-level security objectives defining WHAT must be protected (technology-agnostic, normative "shall" statements)
- **CSR (this skill)**: Low-level technical requirements defining HOW to protect (specific algorithms, protocols, configurations)

**Example Distinction**:
- ❌ CSG: "The system shall protect location data confidentiality" (WHAT)
- ✅ CSR: "Implement AES-256-GCM encryption with PBKDF2 key derivation" (HOW)

CSG derivation is OUT OF SCOPE for this skill. Use this skill for technical requirements only.

---

## 2. Target Project Quick Reference

This skill is part of the **TaraOK skill set** for automotive cybersecurity TARA work.
Locate the target project root from the working directory -- do NOT hardcode any paths.

Path note: in this source repository, this skill lives at `csr/`. In an installed target project, it may live at `skills/csr/`.

**Runtime directories** (relative to the target project root):

```
data/                          Input and output directory
  ├── asset_list.md            INPUT: Asset catalogue
  ├── ds.md                    INPUT: Damage scenario catalogue
  ├── ts.md                    INPUT: Threat scenario catalogue
  ├── at.md                    INPUT: Attack tree catalogue
  ├── rt.md                    INPUT: Risk treatment catalogue
  ├── csg.md                   INPUT: Cybersecurity goal catalogue
  └── csr.md                   OUTPUT: Cybersecurity requirement catalogue
skills/csr/                    Installed skill files
  ├── SKILL.md                 This file (skill entry point)
  ├── assets/
  │   └── TEMPLATE.md          Minimal output template
  └── references/
      ├── csr-schema.md        Authoritative field definitions and validation rules
      ├── csr-guide.md         Authoritative derivation methodology and patterns
      └── examples/
          ├── example-01-implemented.md   Part A example
          └── example-02-gap.md           Part B example
```

**Canonical source-of-truth rules**:
- `references/csr-schema.md` is the authority for field definitions, category names, and validation rules.
- `references/csr-guide.md` is the authority for the derivation method and decomposition patterns.
- `assets/TEMPLATE.md` is the fill-in template only.
- If these files disagree, fix the references first. Do not invent a fourth rule set inside `SKILL.md`.

**Prerequisites**:
- `data/csg.md` exists and contains cybersecurity goals.
- `data/rt.md` exists and contains treatment decisions.
- `data/ts.md` exists and contains threat scenarios.
- Design specifications or existing security documentation are available for Part A.

---

## 3. Done Criteria

This skill is complete when all of the following are true:
- `data/csr.md` exists.
- Every CSR entry follows the schema in `references/csr-schema.md`.
- Every implemented control (Part A) has a traceable source reference.
- Every gap (Part B) links back to a threat scenario or clearly states `TARA Analysis`.
- Every CSG in scope is covered by at least one CSR, or the omission is explained by upstream RT policy.
- Priority values are copied from the upstream `risk_treatment` output, not re-invented locally.

---

## 4. Workflow

Follow this workflow. Keep `SKILL.md` short; use the referenced files for details.

### Step 1: Gather Inputs

Read these inputs before deriving anything:
- `data/csg.md` for the goal set that needs implementation detail.
- `data/rt.md` for authoritative treatment decisions and downstream priority context.
- `data/ts.md` for threat traceability.
- Relevant design specifications, supplier declarations, or architecture docs for implemented controls.

Do not derive CSRs from damage scenarios directly. CSRs implement CSGs.

→ verify: all four input sources are loaded. For CSGs that require implementation per upstream treatment decisions, confirm RT context exists or mark the affected CSR work as pending RT completion.

### Step 2: Capture Implemented Controls (Part A)

Document existing security controls already evidenced by design documentation.

For each implemented control, capture:
- what is implemented,
- where it is documented,
- which CSG(s) it supports.

Use the Part A structure from `assets/TEMPLATE.md`.
Use the exact field requirements from `references/csr-schema.md`.

→ verify: every Part A entry has a source reference. Related CSG-IDs are recommended, but may be added later during traceability mapping per `references/csr-schema.md`.

### Step 3: Derive Required Technical Controls

Translate each CSG into one or more specific, testable CSRs.

Use `references/csr-guide.md` for:
- the 6-step derivation method,
- CIA-to-CSR decomposition patterns,
- compact examples by confidentiality / integrity / availability.

Working rule:
- CSG answers **WHAT must be protected**.
- CSR answers **HOW this implementation will protect it**.

One CSG commonly produces multiple CSRs across different functional categories.

→ verify: every in-scope CSG that requires implementation has at least one derived CSR; each CSR is specific and testable.

### Step 4: Classify Each CSR Outcome

Compare the required control against the implemented evidence.

Allowed states are defined in `references/csr-schema.md`:
- `✅ IMPLEMENTED` for Part A only
- `⚠️ PARTIAL` for incomplete implementation
- `❌ GAP` for missing implementation

Do not use private heuristics like percentage thresholds unless the user explicitly asks for one. If the distinction is unclear, describe what exists and what is missing, then choose the status that matches the schema definitions.

→ verify: no CSR is left without a status; every `⚠️ PARTIAL` entry describes what is missing.

### Step 5: Assign Priority From Upstream RT

This skill does **not** own risk scoring.

Use `risk_treatment` output as the authority for priority context:
- read the related `RT-ID` / `TS-ID`,
- carry the resulting priority into the CSR entry,
- do not create a separate RV-to-priority policy here.

If upstream RT does not yet provide enough information, mark the CSR draft as needing RT completion rather than inventing local priority logic.

→ verify: every CSR priority aligns with the originating TS/RT context. If RT output is not ready, mark the CSR as pending RT completion rather than inventing local priority logic.

### Step 6: Write and Validate `data/csr.md`

Build `data/csr.md` with:
- Part A: implemented controls
- Part B: partial controls and gaps
- traceability back to CSGs and threat scenarios

Before handoff:
- validate field completeness against `references/csr-schema.md`,
- verify the derivation logic against `references/csr-guide.md`,
- use `assets/TEMPLATE.md` as the output shape,
- review `references/examples/` if a compact example is needed.

---

## 5. Practical Rules

- Keep Part A close to the source text for auditability.
- Keep Part B specific, technical, and testable.
- Prefer traceable evidence over plausible invention.
- Put long examples, parameter tables, and worked patterns in `references/`, not in `SKILL.md`.
- Avoid duplicating schema rules here; fix the authoritative references instead.

---

## 6. References

**Internal references**:
- `references/csr-schema.md` — authoritative schema and validation rules
- `references/csr-guide.md` — authoritative derivation method
- `assets/TEMPLATE.md` — minimal template for `data/csr.md`
- `references/examples/example-01-implemented.md` — implemented-control example
- `references/examples/example-02-gap.md` — gap example

**Upstream inputs**:
- `data/asset_list.md` — asset catalogue
- `data/ds.md` — damage scenarios
- `data/ts.md` — threat scenarios
- `data/at.md` — attack tree catalogue
- `data/rt.md` — risk treatment catalogue
- `data/csg.md` — cybersecurity goals

---

## 7. Troubleshooting

**"I am not sure how many CSRs a CSG should create"**:
→ Use `references/csr-guide.md`. One CSG often expands into multiple CSRs.

**"I found a control in the design spec, but it is incomplete"**:
→ Record the implemented portion in Part A only if it truly stands alone as an implemented control; otherwise document the missing or incomplete outcome in Part B using schema definitions.

**"I cannot find a TS-ID for a gap"**:
→ Use `TARA Analysis` only when no specific TS linkage is available. Prefer explicit TS traceability when possible.

**"Priority feels wrong"**:
→ Re-check `data/rt.md` and `data/ts.md`. This skill does not override upstream risk treatment.

**"A design-spec control is marked N/A"**:
→ Do not create a CSR entry for a non-applicable control. Keep that note in design-review material instead.

**"The docs disagree"**:
→ Treat `references/csr-schema.md` and `references/csr-guide.md` as the source of truth. Fix those files instead of adding another interpretation here.

---

*End of CSR Skill Workflow*
