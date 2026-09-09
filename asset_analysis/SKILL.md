---
name: asset_analysis
description: >-
  Asset Analysis and Definition for ISO 21434 TARA workflow.
  Triggers (EN): asset identification, asset analysis, identify assets,
  list assets, asset catalogue, asset inventory, TOE assets.
  Triggers (中文): 资产分析, 资产识别, 资产清单, 资产目录, 资产盘点, TOE 资产.
  Standalone TARA step producing data/asset_list.md.
---
# Asset Analysis -- Skill Workflow

## 0. Sibling Skill Routing (TARA Workflow Boundary)

This skill is **one node** in the ISO 21434 TARA pipeline. Do NOT cross into siblings' territory:

| Skill                     | Owns                                                         | Key Output           | Hand-off                       |
|---------------------------|--------------------------------------------------------------|----------------------|--------------------------------|
| **asset_analysis** (this) | What exists + intrinsic CIA sensitivity                      | `data/asset_list.md` | → damage_scenario              |
| `damage_scenario`         | What happens if compromised (SFOP severity, ISO 21434 §15.4) | `data/ds.md`         | → threat_scenario              |
| `threat_scenario`         | How it gets compromised (attack paths, AFR, §15.5–15.7)      | `data/ts.md`         | → attack_tree / risk_treatment |

**Routing rules** (re-route the user instead of doing the wrong work):
- User asks "what's the impact if X is hacked / how bad is it" → **route to `damage_scenario`**, do NOT inflate CIA here.
- User asks "how would an attacker do X / what's the attack path" → **route to `threat_scenario`**.
- User asks "what assets exist / what is in scope" → **stay here**.
- If the asset list is missing or incomplete and the user jumps to threats/damage, complete asset_analysis first as prerequisite.

### Item Definition Gate (mandatory)

Before enumerating assets, freeze the item boundary. ISO 21434 TARA starts from
item definition: an item is a component or set of components that implements a
vehicle-level function.

Record these at the top of `data/asset_list.md`:
1. **Item / TOE** — the system, subsystem, or ECU set under analysis.
2. **Vehicle-Level Function(s)** — functions delivered to road users or stakeholders.
3. **Constituent Components** — logical or technical parts that implement the item.
4. **Asset Location** — which assets live inside or across those components.

If the item cannot be described as “these components implement these
vehicle-level functions,” stop and clarify. Do not start asset enumeration.

---

## 1. When to Use This Skill

**Trigger ON** when the user is:
- Identifying assets for ISO 21434 TARA (Threat Analysis and Risk Assessment)
- Creating or updating an asset catalogue or asset inventory
- Working with files in the `input/` directory containing system specifications
- Asking about "identify assets", "asset analysis", "list assets", "asset catalogue"
- Starting ISO 21434 Clause 15.3 (Asset Identification) work
- Preparing for threat scenario development (asset list is prerequisite)
- Analyzing vehicle system architecture for security-relevant components

**Trigger OFF** when the user asks:
- About threat scenarios or attack paths (route to `threat_scenario`); about risk treatment (route to `risk_treatment`)
- General ISO 21434 theory unrelated to this specific project
- Vehicle design or engineering topics not related to cybersecurity asset identification
- Implementation of security controls (that comes after asset identification)

---

## 2. Target Project Quick Reference

This skill is part of the **TaraOK skill set** for automotive cybersecurity TARA work.
Locate the target project root from the working directory -- do NOT hardcode any paths.

Path note: in this source repository, this skill lives at `asset_analysis/`. In an installed target project, it may live at `skills/asset_analysis/`.

**Runtime directories** (relative to the target project root):

    input/              Reference documents (specs, architecture diagrams, requirements)
    data/               Output directory (asset_list.md generated here)
    skills/asset_analysis/  Installed skill files (references, templates, examples)

**Workflow**:
1. User places reference documents in `input/` (optional but recommended)
2. Skill freezes item/function/component boundary
3. Skill guides user through asset identification interview
4. Output written to `data/asset_list.md` in ISO 21434 format

### Prerequisites (before interview)

- Confirm target item scope is explicit (vehicle / subsystem / ECU boundary)
- Confirm vehicle-level function(s) implemented by the item
- Confirm constituent components, or record unknowns explicitly
- Confirm at least one evidence source exists:
  - user-provided architecture/network description, and/or
  - documents in `input/`
- Create `data/` if missing; final output path is strictly `data/asset_list.md`
- If evidence is insufficient, mark unknowns explicitly (do **not** infer/fabricate)

### TOE / Scope Definition (mandatory before asset enumeration)

Before any asset is enumerated, the **Target of Evaluation (TOE)** must be written down explicitly at the top of `data/asset_list.md`. Without a frozen TOE, asset identification has no boundary and damage/threat downstream becomes incomparable.

Record three things:

1. **In-Scope** — what is being analyzed
   - System / subsystem / ECU boundary (e.g. "T-Box + in-vehicle gateway")
   - Vehicle platform / variant / SW baseline / model year
   - Lifecycle phase covered (development / production / operation / decommission)
2. **Out-of-Scope** — what is *deliberately* excluded
   - Adjacent systems referenced only as **external entities** (e.g. cloud backend, mobile app, charging station)
   - Components owned by other TARAs (cite the other TARA if known)
3. **Assumptions on the environment** — what the TOE relies on but does not control
   - Trusted external services, physical access controls, supplier-provided components treated as black boxes
4. **Vehicle-Level Function(s)** — what the item delivers to road users or stakeholders
5. **Constituent Components** — which logical or technical parts implement the item

**Rule**: external entities (out-of-scope systems the TOE talks to) are NOT assets. They appear only in the `Interfaces` field of in-scope assets. Adding them as `AST-*` entries pollutes the asset list and double-counts in damage/threat steps.

If the user cannot answer "what is in scope vs. out of scope" in one sentence each, **stop and clarify before continuing** — do not start asset enumeration on an undefined boundary.

---

## 3. Asset Identification Workflow

Follow these steps to identify and document vehicle assets:

### Step 1: Gather Context
- Review any documents in `input/` directory (system specs, architecture diagrams, requirements)
- Understand the item and the vehicle-level function(s) it implements
- Identify the scope (whole vehicle, specific ECU, subsystem, etc.) and constituent components

### Step 2: Conduct User Interview
Use the guided questions in Section 4 to extract asset information from the user.
Take detailed notes on:
- Item boundary and vehicle-level function(s)
- System components and their functions
- Network architecture and connections
- Data flows (what data goes where)
- Security-relevant assets (what needs protection)

### Step 3: Identify Asset Categories
For each asset identified, classify it into one of below categories:
- **Hardware** - Physical components of the vehicle system, such as ECUs, sensors, and actuators. It uses `HW` to denote the category in asset IDs.
- **Software** - Programs and applications running on the vehicle system. It uses `SW` to denote the category in asset IDs.
- **Firmware** - Low-level software embedded in hardware components. It uses `FW` to denote the category in asset IDs.
- **Data-at-rest** - Information stored on the vehicle system. It uses `DAR` to denote the category in asset IDs.
- **Data-in-transit** - Information being transmitted across the vehicle network. It uses `DIT` to denote the category in asset IDs.
- **Data-in-use** - Information actively being processed by the vehicle system. It uses `DIU` to denote the category in asset IDs.

### Step 4: Document Each Asset
For each identified asset, fill in ALL 7 required fields (see `references/asset-schema.md`):
1. **Asset ID** - Format `AST-[HW]-[NNN]` (e.g., AST-HW-001)
2. **Asset Name** - Human-readable name
3. **Description** - Detailed explanation (minimum 3 sentences)
4. **Category** - One of the 7 vehicle system categories
5. **CIA Rating** - Confidentiality/Integrity/Availability on 1-4 scale
6. **Interfaces** - All connections and communication channels
7. **Related Systems** - Dependencies and relationships

#### Asset granularity
Assets should be defined at a level that is meaningful for security analysis. Avoid overly coarse or overly fine granularity. Each asset should represent a distinct component, data store, or functional unit that has security implications.

Take an example for HW assets like USB and SD-Card. Each of these should be treated as separate assets with their own unique Asset ID, rather than lumping them together under a generic "AST-HW-007: USB and SD-card interface hardware
" asset. Other similar cases should also be treated separately. The asset granularity is to ensure the atomic unit of analysis for security purposes. 


#### Asset ID assignment (collision-safe, monotonic)

Before writing a new asset header, **check the highest existing ID for that category** in `data/asset_list.md` and use `max + 1`. Never reuse retired IDs, never renumber existing IDs.

```bash
# Example: pick next free ID for category HW
LAST=$(grep -oE '^### AST-HW-[0-9]{3}:' data/asset_list.md 2>/dev/null \
       | sort -u | tail -1 | grep -oE '[0-9]{3}')
NEXT=$(printf 'AST-HW-%03d' $((10#${LAST:-000} + 1)))
echo "$NEXT"
```

If `data/asset_list.md` does not yet exist, the first ID is `AST-[HW]-001`. Repeat per category (`HW|SW|FW|DAR|DIT|DIU`). IDs are append-only and stable across revisions (see `references/asset-schema.md` §1 ID Stability rule).

Use the canonical name/code mapping (English labels are normative — do **not** localize):

| Category Name (use in `Category:` field) | Asset ID Code (use only inside `AST-*` ID) |
|------------------------------------------|--------------------------------------------|
| `Hardware`                               | `HW`                                       |
| `Software`                               | `SW`                                       |
| `Firmware`                               | `FW`                                       |
| `Data-at-rest`                           | `DAR`                                      |
| `Data-in-transit`                        | `DIT`                                      |
| `Data-in-use`                            | `DIU`                                      |

**Rule**: Put the **Category Name** (left column, e.g. `Hardware`) in the `Category:` field. Put the **Asset ID Code** (right column, e.g. `HW`) only inside the `Asset ID:` field as `AST-HW-NNN`. Do not mix them (`Category: HW` is wrong; `Asset ID: AST-Hardware-001` is wrong).

**English-only**: the `Category:` field MUST contain exactly one of the six English labels above. Localized names such as `网关`, `传感器`, `执行器`, `通信`, `数据`, `接口`, `控制器` (or any other translation) are **forbidden** in this field — they break the validation regex in `references/validation.md` and downstream tooling. Translate freely in `Description:` and prose, never in `Category:`.

Use `assets/TEMPLATE.md` as a starting point for each asset.

### Step 5: Assess CIA Ratings (Intrinsic Sensitivity)
For each asset, rate the **intrinsic security sensitivity** of the asset itself — a static property of the data/function, not a forecast of damage. Scale 1-4 (1=Negligible, 2=Moderate, 3=Major, 4=Severe):
- **Confidentiality (C)**: How sensitive is this data by nature? (public → secret credentials/keys)
- **Integrity (I)**: How trustworthy must this data/function be by nature? (informational → safety-grade)
- **Availability (A)**: How time-critical is this asset's continuous availability by nature? (optional → must-be-up)

**Important — do not double-rate**: CIA here captures the asset's *intrinsic sensitivity*. The **impact of compromise** (Safety / Financial / Operational / Privacy = SFOP, ISO 21434 §15.4) is assessed downstream in the `damage_scenario` skill. Do not pre-compute SFOP severity here, and do not let "what bad thing happens" reasoning drive the CIA number.

See `references/asset-schema.md` for detailed CIA rating guidelines.

### Step 6: Map Relationships
For each asset, identify:
- **Dependencies**: What does this asset need to function?
- **Dependents**: What relies on this asset?
- **Security relationships**: Authentication, encryption, trust boundaries
- **Safety relationships**: Impact on safety-critical functions

### Step 7: Generate Output
Write all documented assets to `data/asset_list.md` using the format specified in Section 5.
Ensure:
- Each asset has all 7 required fields
- Asset IDs are unique and stable (do not renumber existing IDs)
- CIA ratings are justified
- Cross-references to related assets use Asset IDs

### Step 8: Validate
Review the asset list for:
- Completeness (all security-relevant assets captured)
- Consistency (naming, format, categories)
- Traceability (can map back to source documents in `input/`)
- No placeholder text or TODOs remaining

Recommended command checks (optional but strongly encouraged):

```bash
# 1) Asset header format + count
grep -cE '^### AST-(HW|SW|FW|DAR|DIT|DIU)-[0-9]{3}:' data/asset_list.md

# 2) Duplicate Asset IDs (should be empty)
grep -oE 'AST-(HW|SW|FW|DAR|DIT|DIU)-[0-9]{3}' data/asset_list.md | sort | uniq -d

# 3) CIA format presence
grep -qE 'C:[1-4]\s*/\s*I:[1-4]\s*/\s*A:[1-4]' data/asset_list.md

# 4) Placeholder detection (should be empty)
grep -nE '\[(TODO|TBD)\]|\{\{[A-Z_]+\}\}' data/asset_list.md
```

For a complete validation checklist and command bundle, see `references/validation.md`.

---

## 4. Guided Questions

Use these questions to interview the user and extract asset information:

### System Overview
1. **What vehicle system or component are we analyzing?**
   - Scope: Whole vehicle, specific domain (powertrain, ADAS, infotainment), or individual ECU?
   - Purpose: What does this system do? What is its primary function?

2. **What reference documents or specifications are available?**
   - Architecture diagrams, network topology, requirements specs, design docs?
   - Are these documents in the `input/` directory?

### Components and Architecture
3. **What are the main electronic control units (ECUs) in this system?**
   - List all ECUs with their names and primary functions
   - Which ECUs are safety-critical? Which handle external communication?

4. **What network architecture connects these components?**
   - What buses or networks are used? (CAN, CAN-FD, LIN, FlexRay, Ethernet)
   - How are networks segmented? Are there gateways between segments?
   - What is the network topology? (star, bus, hierarchical)

5. **What sensors and actuators are present?**
   - Input devices: cameras, radar, lidar, speed sensors, temperature sensors, etc.
   - Output devices: motors, valves, displays, speakers, etc.
   - Which sensors/actuators are safety-critical?

### Data Flows and Interfaces
6. **What data flows through this system?**
   - What types of data are collected, processed, stored, or transmitted?
   - Where does data come from? Where does it go?
   - What data is safety-critical? What data is privacy-sensitive?

7. **What external interfaces does the system have?**
   - Physical: OBD-II port, USB, diagnostic connectors, charging port
   - Wireless: Cellular, Wi-Fi, Bluetooth, V2X, key fob
   - Cloud: OTA update server, telematics backend, mobile app

8. **What communication protocols are used?**
   - In-vehicle: CAN, Ethernet, etc.
   - External: TLS, HTTPS, cellular protocols, Bluetooth profiles
   - Are communications encrypted? Authenticated?

### Security and Safety Context
9. **Which assets are most critical from a safety perspective?**
   - What assets, if compromised, could lead to injury or loss of life?
   - Which functions are subject to safety standards (ISO 26262, ASIL ratings)?

10. **Which assets are most critical from a security perspective?**
    - What assets are exposed to external attackers? (wireless interfaces, physical ports)
    - What assets hold cryptographic keys or authentication credentials?
    - What assets can modify safety-critical functionality?

11. **What security mechanisms are currently in place?**
    - Firewalls, message authentication, encryption, secure boot, HSM?
    - This helps identify security-relevant data assets (keys, certificates)

12. **Are there any regulatory or compliance requirements?**
    - UN R155 (cybersecurity), UN R156 (OTA updates), GDPR (privacy)?
    - These may influence CIA ratings and asset criticality

---

## 5. Output Format

The output file `data/asset_list.md` should follow this structure:

```markdown
# Asset List - [System/Vehicle Name]

**Date**: [YYYY-MM-DD]  
**Scope**: [Description of system analyzed]  
**Total Assets**: [N]

## Item Definition

- **Item / TOE**: [System, subsystem, or ECU set under analysis]
- **Vehicle-Level Function(s)**: [Functions delivered to road users or stakeholders]
- **Constituent Components**: [Logical or technical parts that implement the item]
- **Out-of-Scope Components**: [Adjacent systems treated as external entities]
- **Assumptions**: [Boundary, lifecycle, supplier, or environment assumptions]

---

## Asset Summary by Category

| Category | Count | Examples                   |
|----------|-------|----------------------------|
| HW       | X     | Engine ECU, Brake ECU, ... |
| SW       | X     | Central Gateway, ...       |
| FW       | X     | Speed Sensor, Camera, ...  |
| DAR      | X     | Throttle Motor, ...        |
| DIT      | X     | CAN Bus, Ethernet, ...     |
| DIU      | X     | Cryptographic Keys, ...    |

---

## Asset Catalogue

### AST-HW-001: [Asset Name]

**Description**: [3+ sentences describing the asset, its function, and security relevance]

**Category**: HW

**CIA Rating**: C:X / I:X / A:X
- Confidentiality (Level): [Justification]
- Integrity (Level): [Justification]
- Availability (Level): [Justification]

**Interfaces**:
- [List all connections, protocols, and data flows]

**Related Systems**:
- Depends on: [List dependencies]
- Provides data to: [List dependents]
- Security relationship: [Authentication, encryption, trust]
- Safety relationship: [Impact on safety functions]

**Evidence & Confidence** (recommended):
- Sources: [Input doc name/section, or interview answer index]
- Confidence: [High | Medium | Low]
- Assumptions/Unknowns: [Explicitly list unresolved items]

---

### AST-SW-[NNN]: [Next Asset Name]

[Repeat above structure for each asset]

---

## Asset Relationships

[Optional: Include a diagram or textual description of how assets relate]

---

## Notes

[Any additional context, assumptions, or open questions]
```

**Key formatting rules**:
- Use markdown headers (##, ###) for structure
- Each asset is a level-3 header (###) with its Asset ID and name
- Maintain consistent field order for all assets
- Use bullet lists for interfaces and related systems
- Include justification for each CIA rating dimension
- Keep it human-readable and easy to navigate

---

## 6. Critical Guardrails

MUST NOT:
- **Invent or fabricate asset information** -- All asset data must come from user input, reference documents, or explicit analysis. Do not make up technical details.
- **Add asset categories beyond the 6 defined** -- Only use: ECU, Gateway, Sensor, Actuator, Communication, Data, Interface. Do not create custom categories.
- **Skip item definition** -- The item/TOE, vehicle-level function(s), and constituent components must be recorded before asset entries.
- **Assign CIA ratings without justification** -- Every CIA rating must be based on explicit impact analysis. Document the reasoning.
- **Hide uncertainty** -- If evidence is missing, explicitly record Unknown/Assumption instead of guessing.
- **Create files outside `skills/` and `data/` directories** -- Keep project structure clean. Output goes to `data/asset_list.md` only.
- **Auto-execute analysis or fabricate asset data** -- This is a runbook skill. It guides the user through interview-driven asset identification; it must not generate assets without evidence. Static validation tooling (regex/lint shell snippets, e.g. `references/validation.md`) is allowed and encouraged. LLM-driven asset fabrication is forbidden.
- **Integrate with tara-maker or generate threat scenarios** -- This skill is standalone. It produces an asset list that can be used later for threat analysis, but that's a separate workflow.
- **Use real CVE numbers, proprietary vehicle data, or sensitive information in examples** -- Use generic, anonymized examples only.
- **Skip required fields** -- ALL 7 fields must be completed for each asset. No exceptions.

---

## 7. Reference Files

| File                                           | Contents                                                                                                       |
|------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| `references/asset-schema.md`                   | Complete specification of 7 required fields, CIA rating guidelines, category definitions, validation checklist |
| `references/validation.md`                     | End-to-end validation flow for `data/asset_list.md` (format, completeness, consistency, placeholders)          |
| `references/examples/example-01-telematics.md` | Example scenario: Telematics Control Unit analysis with sample interview Q&A and expected output               |
| `references/examples/example-02-gateway.md`    | Example scenario: Central Gateway ECU analysis showing multiple related assets                                 |
| `assets/TEMPLATE.md`                           | Blank 7-field asset template ready to copy-paste for new assets                                                |

For detailed field specifications, CIA rating scales, and category definitions, see `references/asset-schema.md`.

For practical examples of how to apply this workflow, see the example scenarios in `references/examples/`.

---

## ISO 21434 Context

This skill implements the item-definition gate and **ISO/SAE 21434:2021 Clause 15.3 - Asset Identification**.

Asset identification starts after the item and vehicle-level function boundary is frozen:
1. **Item Definition + Asset Identification** ← This skill
2. Damage Scenario Definition
3. Threat Scenario Identification
4. Attack Feasibility Rating
5. Risk Determination
6. Risk Treatment Decision

The output of this skill (`data/asset_list.md`) serves as input for subsequent TARA steps, particularly threat scenario enumeration where you identify how each asset could be attacked.

**Key ISO 21434 principles applied here**:
- Assets are items of value that require protection
- Assets include hardware, software, data, and interfaces
- CIA (Confidentiality, Integrity, Availability) ratings capture the impact of asset compromise
- Asset identification considers the entire vehicle system, not just individual components
- Traceability: each asset should be traceable to system requirements or architecture documentation
