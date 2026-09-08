---
name: damage_scenario
description: >-
  Damage Scenario Analysis for ISO 21434 TARA workflow.
  Triggers: damage scenario, damage analysis, SFOP assessment,
  impact analysis, what happens if compromised, harm analysis.
  Input: data/asset_list.md. Output: data/ds.md.
  ISO 21434 Clause 15.4-15.5.
---
# Damage Scenario Analysis -- Skill Workflow

**Task complete when**: `data/ds.md` exists, every `HIGH-CIA` asset (C≥3, I≥3, A≥3) in `data/asset_list.md` has been triaged into one or more DS entries, and the damage scenario validator exits 0.

## 1. When to Use

**ON**: damage scenario / SFOP / impact / harm questions tied to an existing `data/asset_list.md`; ISO 21434 Clause 15.4-15.5 work; preparing for `threat_scenario`.

**OFF**: asset cataloguing (`asset_analysis`), threat/attack/feasibility (`threat_scenario`), security control implementation, generic ISO theory.

## 2. Target Project Layout

Locate the target project root from the working directory -- never hardcode paths.

    data/
      ├── asset_list.md     INPUT  (from asset_analysis skill)
      └── ds.md             OUTPUT (this skill)
    skills/damage_scenario/ installed skill files

Path note: in this source repository, this skill lives at `damage_scenario/`. In an installed target project, it may live at `skills/damage_scenario/`.

**Prerequisites**: `data/asset_list.md` exists with ≥1 asset entry and CIA ratings.
**Fallback if missing**: stop and instruct the user to run the `asset_analysis` skill first; do not invent assets.

## 3. Core Rules (single source of truth)

These rules apply everywhere in this skill -- the workflow steps, validator, and template all enforce them.

1. **Consequence, not cause.** A damage scenario describes the HARM. How an attacker causes it is `threat_scenario` territory. Forbidden vocabulary in titles or final DS entries: attack, attacker, exploit, vulnerability, injection, spoofing, malware, ransomware, dos/ddos, denial of service, cve.
2. **SFOP scale is 1-4.** Negligible=1, Moderate=2, Severe=3, Critical=4. There is no level 0. No AFR/likelihood here.
3. **Impact Score = MAX(Safety, Financial, Operational, Privacy).** Not average, not sum.
4. **CIA ratings are triage prompts, not scores.** High C → ask Privacy/Financial. High I → ask Safety/Operational. High A → ask Operational/Safety. F is always assessed independently. Final SFOP scores must be justified from operating context, population, duration, recovery path, and regulatory scope -- never copied from CIA.
5. **DS-ID format**: `DS-[DOMAIN]-[NNN]`, unique. The 7 allowed domain codes are: `CAN, OTA, EXT, BCK, IVI, IMM, ADAS`. No custom domains.
6. **Many-to-many**: one DS may link multiple assets; one asset may appear in multiple DS entries.
7. **Worst-case reasonable**, not theoretical extreme. Anchor every score in operating conditions (parked vs. highway), scale (one vehicle vs. fleet), duration (auto-recover vs. service center), and regulation (GDPR, GB 44495, UN R155, ISO 26262).
8. **Every score > 1 needs 2-3 sentences of rationale.** Every entry needs Assessment Context that lets a reviewer reproduce the scoring.

## 4. Workflow

### Step 1 -- Read assets

Open `data/asset_list.md`. Build a working list grouped by highest CIA dimension; flag everything with C≥3, I≥3, or A≥3 as a triage candidate.

### Step 2 -- Group by domain

Assign each asset its PRIMARY domain from the 7 allowed codes (Rule 5). An asset can support multiple DS entries across domains, but the DS-ID uses its primary domain.

| Code | Domain | Typical assets |
|------|--------|----------------|
| CAN  | In-vehicle networking | CAN/LIN/FlexRay buses, gateways |
| OTA  | Over-the-air updates  | Update servers, firmware repos, diagnostic ifaces |
| EXT  | External interfaces   | OBD-II, USB, charging port, physical connectors |
| BCK  | Backend / cloud       | Telematics servers, cloud APIs, mobile apps |
| IVI  | Infotainment          | Head unit, displays, audio, connectivity |
| IMM  | Immobilizer / access  | Keyless entry, anti-theft, vehicle access |
| ADAS | ADAS / autonomous     | Cameras, radar, lidar, automated driving |

### Step 3 -- Triage candidate damages (CIA → SFOP)

For each HIGH-CIA asset, generate harm prompts using Rule 4. Patterns in `references/ds-patterns.md` (12 reusable templates) are a good seed list.

Example:
```
AST-ECU-001 (Head Unit) -- CIA C:3 / I:4 / A:3
  C=3 → DS-IVI-001 (PII Exposure)?      Ask: data type, scale, duration, regulator.
  I=4 → DS-CAN-001 (Unintended Behavior)? Ask: can bad msgs reach motion-control / warnings in this architecture?
  A=3 → DS-IVI-003 (IVI Unavailable)?    Ask: which displays, drivable-and-legal?, recovery path.
```

### Step 4 -- Refine with the user (interview)

Use the SFOP interview questions in `references/interview-questions.md` (16 questions across S/F/O/P) to pin down each candidate. Confirm realism, set scores, capture rationale, list every contributing asset.

**No-human-in-loop fallback**: see `references/interview-questions.md` § "Fallback". Mark every assumed answer in **Assessment Context** with `(assumed: ...)`, cap scores that depend on unverified assumptions one level below worst case, and add a final `## Open Questions` section to `data/ds.md`.

### Step 5 -- Assign DS-IDs

Pick the primary domain → assign the next free 3-digit number within that domain in `data/ds.md`. Check existing IDs to avoid conflicts.

### Step 6 -- Write `data/ds.md`

Copy `assets/TEMPLATE.md` per entry. The template defines all 7 required catalogue fields (DS-ID, Title, Linked Assets, SFOP Dimensions Affected, Impact Score with Overall Impact, Rationale, Assessment Context) plus the file-level summary tables and cross-reference table. Do not invent new sections. Full schema specification: `references/ds-schema.md`. SFOP scoring criteria: `references/sfop-guide.md`.

### Step 7 -- Validate

Run the validator. It is the authoritative checklist:

    python skills/damage_scenario/tools/check_ds.py data/ds.md --asset-list data/asset_list.md

From this source repository, use `python damage_scenario/tools/check_ds.py data/ds.md --asset-list data/asset_list.md`.

(From the skill directory use `python tools/check_ds.py /abs/path/data/ds.md --asset-list /abs/path/data/asset_list.md`.) The validator enforces: DS-ID format and uniqueness, required body markers from the template, no threat/attack vocabulary in titles or final DS text, no `[TODO]/[TBD]` placeholders, SFOP scores in 1-4, Impact = MAX(SFOP), Overall Impact line consistent with per-dimension scores, and AST-ID cross-references resolve in the asset list. **Any non-zero exit blocks handoff to `threat_scenario`.**

Manual checks the validator cannot perform (review by eye before handoff):

- Every HIGH-CIA asset from Step 1 is represented in at least one DS entry.
- Rationale text is consistent with the assigned scores.
- Assessment Context is detailed enough that another reviewer could reproduce the scoring.
- Similar damages have similar SFOP scores across the catalogue.

## 5. Output Format

Use `assets/TEMPLATE.md` verbatim per DS entry. The full file structure (header, summary-by-domain table, SFOP distribution table, DS entries, asset cross-reference, notes) is specified in `references/ds-schema.md`. See `references/examples/example-01-ivi.md` and `example-02-can.md` for two complete catalogues.

Inline mini-example (one entry, abbreviated -- the real entry follows the template):

```markdown
### DS-IVI-001: Continuous Driver Location Tracking

**Linked Assets**:
- AST-SNS-001: GNSS Receiver - source of precise location
- AST-ECU-001: Head Unit - aggregates and forwards location
- AST-COM-005: Cellular Modem - exfiltration channel

**SFOP Dimensions Affected**:
- Safety: No
- Financial: Yes - GDPR fines, class-action exposure
- Operational: No
- Privacy: Yes - continuous location is highly sensitive PII

**Impact Score**: 4 (Critical)
- Safety: 1 (Negligible)
- Financial: 4 (Critical)
- Operational: 1 (Negligible)
- Privacy: 4 (Critical)

Overall Impact: 4 (Critical) [max of S=1, F=4, O=1, P=4]

**Assessment Context**:
- Assumptions: production fleet, EU + China deployment.
- Operating Conditions: any drive cycle; passive collection.
- Population / Scale: fleet-wide, >100k users.
- Duration / Recoverability: continuous over weeks until OTA fix.
- Evidence / Source: data/asset_list.md (AST-SNS-001), GDPR Art. 6 + GB 44495.

**Rationale**:

Privacy (4 - Critical): continuous, fleet-wide collection of precise location is the
worst case for ISO 21434 P -- it is sensitive PII over long duration at large scale.

Financial (4 - Critical): GDPR exposure up to 4% global revenue plus probable
class-action settlements; OEM-level brand impact in two regulated markets.
```

## 6. Critical Guardrails

All Section 3 rules are MUST DO / MUST NOT. Additional guardrails:

- Do **not** create files outside `data/` and `skills/`.
- Do **not** use real CVE IDs, proprietary vehicle data, or sensitive customer information in examples.
- Do **not** invent assets -- every linked asset must exist in `data/asset_list.md`.

## 7. Reference Files

| File | Purpose |
|------|---------|
| `references/ds-schema.md` | Full schema for the 7 DS sections, DS-ID format, domain codes, validation checklist. |
| `references/sfop-guide.md` | SFOP scoring criteria for S/F/O/P with regulatory references. |
| `references/ds-patterns.md` | 12 reusable damage-scenario patterns (PII exposure, unintended braking, immobilization, ...). |
| `references/interview-questions.md` | 16 SFOP interview questions + no-human-in-loop fallback. |
| `references/iso-context.md` | ISO 21434 Clause 15.4-15.5 context, relationship to other clauses, regulatory framing. |
| `references/examples/example-01-ivi.md` | Worked IVI catalogue (privacy-driven). |
| `references/examples/example-02-can.md` | Worked CAN catalogue (safety-driven). |
| `assets/TEMPLATE.md` | Authoritative DS entry template -- copy verbatim. |
| `tools/check_ds.py` | Validator. Section 4 Step 7 is the authoritative checklist. |
