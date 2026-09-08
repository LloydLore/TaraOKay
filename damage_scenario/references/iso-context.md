# ISO 21434 Context

This skill implements **ISO/SAE 21434:2021 Clause 15.4-15.5 - Damage Scenario Definition**.

Damage scenario identification is the second step in the TARA process:

1. Asset Identification (Clause 15.3) ← Prerequisite (`asset_analysis` skill)
2. **Damage Scenario Definition (Clause 15.4-15.5)** ← This skill
3. Threat Scenario Identification (Clause 15.6-15.7)
4. Attack Feasibility Rating (Clause 15.8-15.9)
5. Risk Determination (Clause 15.10-15.11)
6. Risk Treatment Decision (Clause 15.12-15.13)

The output of this skill (`data/ds.md`) serves as input for subsequent TARA steps, particularly threat scenario identification where `threat_scenario` maps HOW each damage scenario could be caused by cyber actions.

## Key ISO 21434 principles applied here

- **Damage scenarios represent HARM**, not attack methods.
- **SFOP framework** (Safety, Financial, Operational, Privacy) captures all cybersecurity impact dimensions.
- **Impact assessment uses 1-4 scale** aligned with ISO 21434 severity levels.
- **Damage scenarios are asset-independent** in description (multiple assets can cause the same damage).
- **Many-to-many relationship** between assets and damage scenarios reflects real-world complexity.
- **CIA → SFOP triage** provides traceability from asset security properties to candidate harm questions without turning CIA ratings into final impact scores.
- **Worst-case reasonable scenarios** guide impact assessment (not theoretical extremes).

## Relationship to other ISO 21434 clauses

- **Clause 15.3 (Asset Identification)**: Assets with HIGH CIA ratings (C≥3, I≥3, A≥3) generate candidate damage scenarios.
- **Clause 15.6 (Threat Scenario Identification)**: Damage scenarios become the "target" — threat scenarios describe how to cause each one.
- **Clause 15.10 (Risk Determination)**: Risk = Impact (from damage scenarios) × Likelihood (from threat scenarios).
- **Clause 8 (Cybersecurity Goals)**: Damage scenarios with Impact ≥3 typically require cybersecurity goals to mitigate.

## Regulatory Context

- **UN R155 (Cybersecurity)**: Requires TARA including damage scenario identification.
- **UN R156 (Software Updates)**: OTA damage scenarios (DS-OTA-XXX) inform update security requirements.
- **GDPR / GB 44495 (Privacy)**: Privacy damage scenarios (P≥3) inform data protection impact assessments (DPIA).
- **ISO 26262 (Functional Safety)**: Safety damage scenarios (S≥3) inform ASIL determination and safety requirements.
