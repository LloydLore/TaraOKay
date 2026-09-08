---
name: attack_tree
description: >-
  Attack Tree Analysis for ISO 21434 TARA workflow.
  Triggers: attack tree, attack path, attack chain, tree analysis,
  AND/OR gates, path analysis, multi-stage attack, kill chain.
  Input: data/asset_list.md, data/ds.md, data/ts.md. Output: data/at.md.
  ISO 21434 Clause 15.7.
---
# Attack Tree Analysis -- Skill Workflow

**Task complete when**: `data/at.md` exists, every AT entry contains all 12 required fields from `references/at-schema.md`, every Root Goal DS-ID resolves against `data/ds.md`, every non-example leaf TS-ID resolves against `data/ts.md`, every path AFR calculation follows the repository contract (`AND -> MIN`, `OR -> MAX`, `SEQ -> MIN`, `Effective AFR -> MAX(all paths)`), and no placeholder markers remain unless the document is explicitly marked as draft/practice output.

## 1. When to Use

**ON**: attack tree / attack path / attack chain / AND-OR-SEQ gate analysis / kill chain / multi-stage attack; ISO 21434 Clause 15.7 work; constructing trees from existing `data/ds.md` (root goals) and `data/ts.md` (leaf nodes).

**OFF**: asset cataloguing (`asset_analysis`), damage scenarios / SFOP (`damage_scenario`), individual threat scenarios / AFR rating (`threat_scenario`), risk treatment / security controls (`risk_treatment`), generic ISO theory, linear attack chains without branching logic.

---

## 2. Target Project Layout

Locate the target project root from the working directory -- never hardcode paths.

    data/
      ├── asset_list.md     INPUT  (from asset_analysis)
      ├── ds.md             INPUT  (from damage_scenario)
      ├── ts.md             INPUT  (from threat_scenario, if available)
      └── at.md             OUTPUT (this skill)
    skills/attack_tree/ installed skill files
      ├── references/
      │   ├── at-schema.md      Schema: 12 required fields
      │   ├── at-guide.md       Methodology: gates, AFR, patterns, pitfalls
      │   └── examples/
      │       ├── example-01-ivi.md
      │       └── example-02-can.md
      └── assets/
          └── TEMPLATE.md       Blank template + completed example

Path note: in this source repository, this skill lives at `attack_tree/`. In an installed target project, it may live at `skills/attack_tree/`.

**Prerequisites**:
- `data/asset_list.md` exists (asset context)
- `data/ds.md` exists with >= 1 damage scenario (root goals)
- `data/ts.md` should exist (leaf nodes). If unavailable, use draft mode.

**Fallback if ts.md missing**: switch to draft/practice mode (see Execution Modes below).

### Execution Modes

Use exactly one per session:

- **Validated mode** (default): `data/ts.md` exists and passed upstream checks. Use real TS-IDs, calculate AFR from those entries, remove all placeholder markers before treating output as handoff-ready.
- **Draft mode**: method rehearsal or early drafting when `data/ts.md` is missing/incomplete. Mark placeholder TS-IDs as `[EXAMPLE]`, label estimated AFR as assumptions, treat output as non-handoff until placeholders are replaced.

**Rule**: Never silently mix validated and draft data in the same AT entry.

---

## 3. Workflow

### Step 1: Gather Context and Select Root Goals

1. Read `data/ds.md` -- review all damage scenarios (potential root goals).
2. Read `data/ts.md` -- review threat scenarios (potential leaf nodes).
3. Read `data/asset_list.md` -- note attack surfaces and entry points.

**Prioritize DS for tree analysis based on**:
- Impact severity: Critical (4) and Severe (3) first
- Attack complexity: DS with multiple vectors benefit from tree visualization
- Multi-stage / branching attacks: SEQ/AND/OR gates needed

**Skip tree analysis** for single-step attacks (one TS causes one DS, no alternatives).

### Step 2: Identify Attack Paths

For the selected DS (root goal):
1. Enumerate all TS-IDs that could lead to this DS (from `data/ts.md`)
2. Separate into **entry points** (no prerequisites) vs **intermediate steps** (require earlier stages)
3. Consider multiple vectors: remote, physical, supply chain, insider

### Step 3: Structure Tree with Gates

Consult `references/at-guide.md` for gate semantics and patterns.

| Gate | Meaning | AFR Rule | When to Use |
|------|---------|----------|-------------|
| `[AND]` | ALL children must succeed | `MIN(children)` | Multiple prerequisites needed simultaneously |
| `[OR]` | ANY child sufficient | `MAX(children)` | Alternative paths to same goal |
| `[SEQ]` | Sequential order required | `MIN(steps)` | Temporal dependencies (kill chain) |

**Quick gate check**: "Does attacker need ALL these OR just ONE?" -> AND vs OR.

Build tree: DS as root -> leaf TS nodes -> intermediate nodes -> connect with gates -> validate gate semantics.

### Step 4: Calculate AFR

1. Retrieve individual TS AFR scores from `data/ts.md` (or estimate in draft mode)
2. Apply aggregation per gate type (table above)
3. Calculate each path AFR (leaf to root)
4. **Effective AFR = MAX(all path AFRs)** -- attacker picks easiest path
5. Note: effective AFR is for tree-level prioritization only; downstream `risk_treatment` uses individual TS AFR

### Step 5: Identify Critical Path

Critical path = greatest practical threat. Usually highest AFR, but apply contextual factors:
- Access opportunities (physical vs remote)
- Attacker skill distribution
- Motivation (APT vs opportunistic)
- Detection risk

Document rationale in 2-4 sentences.

### Step 6: Identify Mitigation Points (2-5 per tree)

For each point, document: TS-ID, control type, impact on paths, coverage (High/Medium/Low).

**Priority order**:
1. Controls on critical path
2. High-leverage nodes (appear in multiple paths)
3. Low-cost / high-impact controls
4. Defense-in-depth layers

### Step 7: Render ASCII Tree

Follow `references/at-guide.md` visualization rules:
- Max 80 chars width, max 5 levels depth
- 4 spaces per level indent
- Explicitly label all gates: `[AND]`, `[OR]`, `[SEQ]`
- If too complex, decompose into sub-trees

### Step 8: Document and Output

1. Consult `assets/TEMPLATE.md` for structure and quality reference
2. Fill all 12 required fields per `references/at-schema.md`:

| # | Field |
|---|-------|
| 1 | AT-ID (`AT-[DOMAIN]-[NNN]`) |
| 2 | Title (max 80 chars) |
| 3 | Root Goal (DS-ID + title) |
| 4 | Attack Tree Structure (ASCII art) |
| 5 | Attack Paths (enumerated TS-ID chains) |
| 6 | Leaf Nodes (all entry point TS-IDs) |
| 7 | Path AFR Analysis (per-path with aggregation logic) |
| 8 | Effective AFR (MAX across paths + rationale) |
| 9 | Critical Path (identified + justification) |
| 10 | Mitigation Points (2-5 with priority) |
| 11 | Last Updated (ISO 8601) |
| 12 | Confidence Level (High/Medium/Low + justification) |

3. Append to `data/at.md` (never overwrite existing entries)
4. Use `## AT-[DOMAIN]-[NNN]` heading for each entry

**AT-ID assignment**: scan `data/at.md` for existing IDs in the same domain; use next free number; never reuse.

---

## 4. Quality Checklist

Before committing output:

- [ ] All 12 fields present
- [ ] AT-ID format valid (`AT-[DOMAIN]-[NNN]`)
- [ ] Root Goal DS-ID exists in `data/ds.md`
- [ ] All leaf TS-IDs exist in `data/ts.md` (or marked `[EXAMPLE]` in draft mode)
- [ ] ASCII tree <= 80 chars width, <= 5 levels depth
- [ ] All paths enumerated (leaf to root)
- [ ] AFR aggregation logic shown for each path
- [ ] Critical path identified with rationale
- [ ] Mitigation points prioritized
- [ ] Validated output contains no `[EXAMPLE]` markers or estimated AFR placeholders

---

## 5. If Blocked

- **Missing `ts.md`?** Switch to draft mode, mark TS-IDs as `[EXAMPLE]`, estimate AFR
- **Tree too complex?** Decompose into sub-trees by attack class or domain
- **Unsure about gate type?** Consult gate decision tree in `references/at-guide.md`
- **AFR aggregation unclear?** See worked examples in `references/at-guide.md`

---

**Skill Version**: 1.0 (2026-03-20)
**ISO 21434 Clause**: 15.7 (Attack path analysis)
**Next Review**: 2027-03-20 or upon ISO 21434 revision
