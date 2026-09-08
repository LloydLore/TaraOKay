# Cybersecurity Requirement Template

**Canonical references**:
- Field definitions and validation rules: `references/csr-schema.md`
- Derivation method and patterns: `references/csr-guide.md`
- This file is the output template only. If guidance here conflicts with the references, fix the references first.

Use this file as the shape for `data/csr.md`.

---

## Part A: Implemented Controls

#### CSR-[CATEGORY]-[NN]: [Requirement Title]

- **Status**: ✅ IMPLEMENTED
- **Category**: [Category Name]
- **Allocation Target**: [Item | Component | Layer | Interface | Supplier-owned subsystem]
- **Description**: [Original source-language or source-faithful implemented-control description]
- **Source**: [Design specification / supplier declaration / datasheet reference]
- **Related CSG-IDs**:
  - [CSG-ID] [Optional title]

---

## Part B: Identified Gaps

#### CSR-[CATEGORY]-[NN]: [Requirement Title]

- **Status**: ❌ GAP | ⚠️ PARTIAL
- **Priority**: CRITICAL | HIGH | MEDIUM | LOW
- **Category**: [Category Name]
- **Allocation Target**: [Item | Component | Layer | Interface | Supplier-owned subsystem]
- **Description**: [Gap analysis: what exists, what is missing, why it matters]
- **Identified By**: TS-[DOMAIN]-[NNN] ([Threat Scenario Title]) | TARA Analysis
- **Recommendation**:
  - **What**: [Specific control or mechanism]
  - **How**: [Parameters / configuration]
  - **Where**: [Component / layer / interface]
  - **Verify**: [Test or acceptance criteria]
- **Related CSG-IDs**:
  - [CSG-ID] [Optional title]

---

## Optional Document Skeleton

```markdown
# Cybersecurity Requirement Catalogue - [System Name]

**Date**: YYYY-MM-DD
**Scope**: [Brief scope statement]

## Part A: Implemented Controls

[Part A entries]

## Part B: Identified Gaps

[Part B entries]

## Optional Traceability Matrix

[CSG -> CSR mapping table if needed]
```

---

## Notes

- For field definitions, category names, and validation rules, see `references/csr-schema.md`.
- For derivation workflow and decomposition patterns, see `references/csr-guide.md`.
- For worked examples, see `references/examples/example-01-implemented.md` and `references/examples/example-02-gap.md`.
