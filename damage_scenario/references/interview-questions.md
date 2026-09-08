# SFOP Interview Questions

Use these questions to interview the user and refine SFOP assessments. Score only after the operating context, population, duration, and recovery path are known.

## Safety (S) Dimension

**Core Question**: "What physical harm could occur to people if this damage scenario happens?"

1. **Could this damage scenario cause the vehicle to lose control?**
   - Loss of steering, braking, or acceleration control?
   - At what speeds could this occur? (parking lot vs. highway)
   - Could the driver regain control, or is it total loss of function?

2. **Could this damage scenario cause unintended vehicle behavior?**
   - Unexpected acceleration, braking, or steering inputs?
   - Could the vehicle collide with other vehicles, pedestrians, or objects?
   - Would occupants have time to react and mitigate?

3. **What is the worst-case reasonable outcome for physical safety?**
   - Minor injuries (cuts, bruises) → S=2
   - Severe injuries requiring hospitalization → S=3
   - Fatalities or permanent disability → S=4

4. **Is this a safety-critical function under ISO 26262?**
   - ASIL-D functions typically map to S=4 if compromised
   - ASIL-C functions typically map to S=3
   - Non-safety functions typically S=1-2

## Financial (F) Dimension

**Core Question**: "What monetary losses, liability, or business impact could occur?"

5. **Could this damage scenario trigger regulatory fines?**
   - GDPR violations (privacy): Up to €20M or 4% annual revenue → F=4
   - China GB 44495 violations (privacy): Up to ¥50M or 5% turnover → F=3-4
   - UN R155 violations (cybersecurity): Type approval withdrawal → F=4
   - Other regulatory penalties?

6. **What liability exposure exists?**
   - Personal injury crashes: Multi-million dollar settlements → F=3-4
   - Property damage only: Moderate liability → F=2
   - Class-action lawsuits for privacy violations: $100M+ settlements → F=4

7. **What are the recall and remediation costs?**
   - Fleet-wide recall (>100,000 vehicles): $100M+ → F=4
   - Large recall (10,000-100,000 vehicles): $10M-100M → F=3
   - Small recall (<10,000 vehicles): $1M-10M → F=2
   - OTA fix with no physical recall: Minimal cost → F=1

8. **What is the brand reputation impact?**
   - Could this damage scenario lead to loss of customer trust?
   - Would it affect future vehicle sales?
   - Could it threaten the company's viability in the market?

## Operational (O) Dimension

**Core Question**: "What vehicle functions become unavailable or degraded?"

9. **Is the affected function critical for vehicle drivability?**
   - Vehicle won't start or becomes immobilized → O=4
   - Loss of propulsion, transmission, or powertrain → O=4
   - Critical safety system disabled (ADAS, eCall) → O=3-4
   - Infotainment or comfort feature unavailable → O=1-2

10. **Can the user work around the problem?**
    - No workaround, vehicle unusable → O=4
    - Degraded mode available, can still drive → O=2-3
    - Full functionality via alternative method → O=1

11. **How long does the disruption last?**
    - Permanent (requires service center visit, ECU replacement) → +1 severity
    - Persistent (hours/days, requires OTA fix) → Normal severity
    - Temporary (seconds/minutes, auto-recovery) → -1 severity

12. **Are there legal requirements for this function?**
    - eCall (emergency calling) required in EU → O=4 if unavailable
    - Immobilizer required for type approval → O=4 if bypassed
    - Emissions monitoring required by regulation → O=3-4 if disabled

## Privacy (P) Dimension

**Core Question**: "What personal information is disclosed, and how many people are affected?"

13. **What type of personal data is exposed?**
    - Highly sensitive (location tracking, health, biometrics) → P=4
    - Moderately sensitive (PII, contact info, preferences) → P=3
    - Low sensitivity (aggregate statistics, anonymized data) → P=2
    - No personal data → P=1

14. **How many people are affected?**
    - Large population (>10,000 users) → +1 severity
    - Fleet-wide (>100,000 users) → P=4 regardless of data type
    - Small group (<100 users) → -1 severity

15. **Is the data exposure continuous or one-time?**
    - Continuous tracking/monitoring over weeks/months → P=4
    - One-time disclosure of sensitive data → P=3
    - Temporary exposure with limited duration → P=2

16. **What regulatory privacy requirements apply?**
    - GDPR Article 6 (lawful basis), Article 32 (security) → Violations = P≥3
    - China GB 44495 (personal information protection) → Violations = P≥3
    - California CCPA (consumer privacy) → Violations = P=2-3

## Fallback: No Human in the Loop

If the user is unavailable for live interview:
1. Apply the questions above as a self-checklist using only `data/asset_list.md`, asset descriptions, and architecture notes already in the repo.
2. Mark every assumed answer in the DS entry's **Assessment Context** with `(assumed: ...)` so reviewers can challenge it later.
3. Cap any score that depends on an unverified assumption at one level below the worst case (e.g., S=3 instead of S=4) and explain the cap in **Rationale**.
4. List unresolved questions in `data/ds.md` under a final `## Open Questions` section so the next reviewer can resolve them.
