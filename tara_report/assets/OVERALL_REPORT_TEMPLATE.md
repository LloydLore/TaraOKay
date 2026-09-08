# Automotive Cybersecurity TARA - Overall Risk Assessment

**Report Date**: {{REPORT_DATE}}  
**Reporting Period**: {{DATA_START_DATE}} to {{DATA_END_DATE}}  
**Vehicle System**: {{VEHICLE_SYSTEM}}  
**System Scope**: {{SYSTEM_SCOPE}}

**Data Sources**:
- Asset Catalogue: [data/asset_list.md](data/asset_list.md)
- Damage Scenarios: [data/ds.md](data/ds.md)
- Threat Scenarios: [data/ts.md](data/ts.md)
- Attack Chains: [data/at.md](data/at.md)
- Risk Treatments: [data/rt.md](data/rt.md)
- Cybersecurity Goals: [data/csg.md](data/csg.md)

**ISO 21434 Alignment**: ISO/SAE 21434:2021 Clause 8.4 (Work Products), Clause 15 (Threat Analysis and Risk Assessment)

---

## Executive Summary

{{EXECUTIVE_SUMMARY_TEXT}}

**Key Findings**:
- Overall Risk Level: **{{OVERALL_RISK_LEVEL}}** ({{RV5_COUNT}} RV-5 threats identified)
- Total Threat Scenarios: {{TS_COUNT}} across {{DOMAIN_COUNT}} domains
- Treatment Coverage: {{TREATMENT_EFFECTIVENESS}}% of threats under active mitigation
- Residual Risk Level: **{{RESIDUAL_RISK_LEVEL}}** after all treatments applied
- Top Risk Domain: **{{HIGHEST_RISK_DOMAIN}}** ({{HIGHEST_RISK_DOMAIN_RV5_COUNT}} RV-5 threats)

**Compliance Status**: {{COMPLIANCE_STATUS_TEXT}}

---

## Summary Statistics

### System Coverage

| Category | Count | Source File |
|----------|-------|-------------|
| **Assets** | {{ASSET_COUNT}} | [data/asset_list.md](data/asset_list.md) |
| **Damage Scenarios** | {{DS_COUNT}} | [data/ds.md](data/ds.md) |
| **Threat Scenarios** | {{TS_COUNT}} | [data/ts.md](data/ts.md) |
| **Attack Chains** | {{AT_COUNT}} | [data/at.md](data/at.md) |
| **Risk Treatments** | {{RT_COUNT}} | [data/rt.md](data/rt.md) |
| **Cybersecurity Goals** | {{CSG_COUNT}} | [data/csg.md](data/csg.md) |

**Asset Coverage**: {{ASSET_COVERAGE}}% of assets have ≥1 identified threat  
**Treatment Coverage**: {{TREATMENT_COVERAGE}}% of threats have assigned risk treatment  
**CSG Implementation**: {{CSG_IMPLEMENTATION}}% of cybersecurity goals have ≥1 treatment implementation

---

## Risk Value Distribution

### Pre-Treatment Risk Landscape

| Risk Value | Count | Percentage | Description |
|------------|-------|------------|-------------|
| **RV 5** (Critical) | {{RV5_COUNT}} | {{RV5_PERCENT}}% | Requires immediate action (Reduce/Avoid) |
| **RV 4** (High) | {{RV4_COUNT}} | {{RV4_PERCENT}}% | Requires risk reduction |
| **RV 3** (Medium) | {{RV3_COUNT}} | {{RV3_PERCENT}}% | Requires reduction or transfer |
| **RV 2** (Low) | {{RV2_COUNT}} | {{RV2_PERCENT}}% | May accept with justification |
| **RV 1** (Negligible) | {{RV1_COUNT}} | {{RV1_PERCENT}}% | Acceptable risk |

**Total Threats**: {{TS_COUNT}}

**Overall Risk Level**: {{OVERALL_RISK_LEVEL}}  
Calculation: Aggregate risk determined by highest RV present (RV 5 → Critical; RV 4 → High; RV 3 → Medium; RV 2 → Low; RV 1 → Negligible)

---

## Treatment Decision Breakdown

### Treatment Portfolio (Source: [data/rt.md](data/rt.md))

| Decision | Count | Percentage | Description |
|----------|-------|------------|-------------|
| **Reduce** | {{REDUCE_COUNT}} | {{REDUCE_PERCENT}}% | Active security controls to lower AFR or Impact |
| **Avoid** | {{AVOID_COUNT}} | {{AVOID_PERCENT}}% | Remove threat by eliminating attack surface |
| **Transfer** | {{TRANSFER_COUNT}} | {{TRANSFER_PERCENT}}% | Shift risk via insurance/third-party liability |
| **Accept** | {{ACCEPT_COUNT}} | {{ACCEPT_PERCENT}}% | Document residual risk with stakeholder sign-off |

**Total Treatments**: {{RT_COUNT}}

**Treatment Effectiveness**: {{TREATMENT_EFFECTIVENESS}}%  
Calculation: (Reduce + Avoid + Transfer) / Total Treatments × 100

**Residual Risk**:
- Residual Risk Level: **{{RESIDUAL_RISK_LEVEL}}**
- Residual RV ≥ 4 Threats: {{RESIDUAL_HIGH_RISK_COUNT}} (after all treatments applied)
- Risk Reduction Achieved: {{RISK_REDUCTION_PERCENT}}%

---

## Top 5 Highest Risk Scenarios (Pre-Treatment)

### Most Critical Threats (Source: [data/ts.md](data/ts.md))

**1. {{RANK1_TS_ID}}: {{RANK1_TS_TITLE}}**  
- **Risk Value**: RV {{RANK1_RV}}  
- **Domain**: {{RANK1_DOMAIN}}  
- **Impact**: {{RANK1_IMPACT}} (Safety: {{RANK1_SAFETY}}, Financial: {{RANK1_FINANCIAL}}, Operational: {{RANK1_OPERATIONAL}}, Privacy: {{RANK1_PRIVACY}})  
- **Attack Feasibility**: AFR {{RANK1_AFR}}  
- **Treatment**: {{RANK1_RT_ID}} ({{RANK1_TREATMENT_DECISION}})  
- **Description**: {{RANK1_THREAT_DESCRIPTION}}

**2. {{RANK2_TS_ID}}: {{RANK2_TS_TITLE}}**  
- **Risk Value**: RV {{RANK2_RV}}  
- **Domain**: {{RANK2_DOMAIN}}  
- **Impact**: {{RANK2_IMPACT}}  
- **Treatment**: {{RANK2_RT_ID}} ({{RANK2_TREATMENT_DECISION}})

**3. {{RANK3_TS_ID}}: {{RANK3_TS_TITLE}}**  
- **Risk Value**: RV {{RANK3_RV}}  
- **Domain**: {{RANK3_DOMAIN}}  
- **Impact**: {{RANK3_IMPACT}}  
- **Treatment**: {{RANK3_RT_ID}} ({{RANK3_TREATMENT_DECISION}})

**4. {{RANK4_TS_ID}}: {{RANK4_TS_TITLE}}**  
- **Risk Value**: RV {{RANK4_RV}}  
- **Domain**: {{RANK4_DOMAIN}}  
- **Impact**: {{RANK4_IMPACT}}  
- **Treatment**: {{RANK4_RT_ID}} ({{RANK4_TREATMENT_DECISION}})

**5. {{RANK5_TS_ID}}: {{RANK5_TS_TITLE}}**  
- **Risk Value**: RV {{RANK5_RV}}  
- **Domain**: {{RANK5_DOMAIN}}  
- **Impact**: {{RANK5_IMPACT}}  
- **Treatment**: {{RANK5_RT_ID}} ({{RANK5_TREATMENT_DECISION}})

> **Note**: Only threats with RV ≥ 4 are shown. If fewer than 5 threats meet this criterion, fewer entries are listed.

---

## Domain Risk Breakdown

### Threat Distribution by Domain (Source: [data/ts.md](data/ts.md))

| Domain | Code | Threats | RV 5 | RV 4 | RV 3-1 | Highest RV | Top Threat |
|--------|------|---------|------|------|--------|------------|------------|
| **CAN Bus** | CAN | {{CAN_THREAT_COUNT}} | {{CAN_RV5_COUNT}} | {{CAN_RV4_COUNT}} | {{CAN_RV3_COUNT}} | RV {{CAN_MAX_RV}} | {{CAN_TOP_THREAT}} |
| **OTA/Update** | OTA | {{OTA_THREAT_COUNT}} | {{OTA_RV5_COUNT}} | {{OTA_RV4_COUNT}} | {{OTA_RV3_COUNT}} | RV {{OTA_MAX_RV}} | {{OTA_TOP_THREAT}} |
| **External Interface** | EXT | {{EXT_THREAT_COUNT}} | {{EXT_RV5_COUNT}} | {{EXT_RV4_COUNT}} | {{EXT_RV3_COUNT}} | RV {{EXT_MAX_RV}} | {{EXT_TOP_THREAT}} |
| **Backend/Cloud** | BCK | {{BCK_THREAT_COUNT}} | {{BCK_RV5_COUNT}} | {{BCK_RV4_COUNT}} | {{BCK_RV3_COUNT}} | RV {{BCK_MAX_RV}} | {{BCK_TOP_THREAT}} |
| **Infotainment** | IVI | {{IVI_THREAT_COUNT}} | {{IVI_RV5_COUNT}} | {{IVI_RV4_COUNT}} | {{IVI_RV3_COUNT}} | RV {{IVI_MAX_RV}} | {{IVI_TOP_THREAT}} |
| **Immobilizer** | IMM | {{IMM_THREAT_COUNT}} | {{IMM_RV5_COUNT}} | {{IMM_RV4_COUNT}} | {{IMM_RV3_COUNT}} | RV {{IMM_MAX_RV}} | {{IMM_TOP_THREAT}} |
| **ADAS** | ADAS | {{ADAS_THREAT_COUNT}} | {{ADAS_RV5_COUNT}} | {{ADAS_RV4_COUNT}} | {{ADAS_RV3_COUNT}} | RV {{ADAS_MAX_RV}} | {{ADAS_TOP_THREAT}} |

**Most Affected Asset**: {{MOST_AFFECTED_ASSET_ID}} ({{MOST_AFFECTED_ASSET_NAME}}) - {{MOST_AFFECTED_ASSET_THREAT_COUNT}} threats

---

## Impact Analysis (SFOP Dimensions)

### Damage Scenario Impact Distribution (Source: [data/ds.md](data/ds.md))

| SFOP Dimension | High Impact (≥3) Count | Most Critical DS | Residual High Risk |
|----------------|------------------------|------------------|-------------------|
| **Safety** | {{SAFETY_HIGH_COUNT}} | {{SAFETY_CRITICAL_DS}} | {{SAFETY_RESIDUAL_COUNT}} |
| **Financial** | {{FINANCIAL_HIGH_COUNT}} | {{FINANCIAL_CRITICAL_DS}} | {{FINANCIAL_RESIDUAL_COUNT}} |
| **Operational** | {{OPERATIONAL_HIGH_COUNT}} | {{OPERATIONAL_CRITICAL_DS}} | {{OPERATIONAL_RESIDUAL_COUNT}} |
| **Privacy** | {{PRIVACY_HIGH_COUNT}} | {{PRIVACY_CRITICAL_DS}} | {{PRIVACY_RESIDUAL_COUNT}} |

**Multi-Dimensional Threats**: {{MULTI_DIM_THREAT_COUNT}} damage scenarios affect 3+ SFOP dimensions  
**Most Critical Dimension**: {{MOST_CRITICAL_SFOP}} ({{MOST_CRITICAL_SFOP_COUNT}} high-impact scenarios)  
**Safety-Critical Residual Risk**: {{SAFETY_RESIDUAL_HIGH_RV_COUNT}} safety-related threats with RV ≥ 3 after treatment

---

## Cybersecurity Goals Summary

### CSG Implementation Status (Source: [data/csg.md](data/csg.md))

| Metric | Count | Percentage |
|--------|-------|------------|
| **Total Cybersecurity Goals** | {{CSG_COUNT}} | 100% |
| **Confidentiality-Focused Goals** | {{CSG_CONFIDENTIALITY_COUNT}} | {{CSG_CONFIDENTIALITY_PERCENT}}% |
| **Integrity-Focused Goals** | {{CSG_INTEGRITY_COUNT}} | {{CSG_INTEGRITY_PERCENT}}% |
| **Availability-Focused Goals** | {{CSG_AVAILABILITY_COUNT}} | {{CSG_AVAILABILITY_PERCENT}}% |
| **Multi-Property Goals** | {{CSG_MULTI_PROPERTY_COUNT}} | {{CSG_MULTI_PROPERTY_PERCENT}}% |
| **Goals with Treatment** | {{CSG_WITH_TREATMENT_COUNT}} | {{CSG_IMPLEMENTATION}}% |
| **Orphan Goals** | {{CSG_ORPHAN_COUNT}} | {{CSG_ORPHAN_PERCENT}}% |

**Data Quality Alert**: {{CSG_ORPHAN_COUNT}} orphan goals (CSG entries with 0 related DS-IDs) indicate potential traceability gaps.  
**Recommended Action**: {{CSG_ORPHAN_ACTION}}

---

## Compliance and Standards References

### ISO 21434 and UN R155 Mapping

**ISO 21434:2021 Coverage**:
- **Clause 8.4**: Work products documented in this Overall Report (summary of cybersecurity analyses)
- **Clause 15.4-15.5**: Damage scenario analysis - {{DS_COUNT}} damage scenarios defined ([data/ds.md](data/ds.md))
- **Clause 15.6**: Threat scenario analysis - {{TS_COUNT}} threat scenarios identified ([data/ts.md](data/ts.md))
- **Clause 15.8**: Risk assessment and treatment status - {{RV5_COUNT}} RV-5 + {{RV4_COUNT}} RV-4 risks quantified
- **Clause 15.9**: Cybersecurity goals - {{CSG_COUNT}} CSG entries established ([data/csg.md](data/csg.md))

**UN R155 Annex 5 Threat Categories**: {{R155_CATEGORY_COVERAGE}}  
(Backend server threats, Communication channels, Firmware updates, External interfaces, Vehicle data/code, In-vehicle networks)

### Framework Coverage Statistics

| Framework | Mapped Threat Count | Coverage Percentage |
|-----------|---------------------|---------------------|
| **MITRE ATT&CK ICS** | {{MITRE_COUNT}} | {{MITRE_COVERAGE}}% |
| **OWASP References** | {{OWASP_COUNT}} | {{OWASP_COVERAGE}}% |
| **Real CVE Examples** | {{CVE_COUNT}} | {{CVE_COVERAGE}}% |

**Traceability Assurance**: {{TRACEABILITY_COMPLETENESS}}% of threat scenarios have complete Asset → DS → TS → RT → CSG chains

---

## Recommendations

### Immediate Actions Required

{{IMMEDIATE_ACTIONS_TEXT}}

### Strategic Priorities

{{STRATEGIC_PRIORITIES_TEXT}}

### Compliance Next Steps

{{COMPLIANCE_NEXT_STEPS_TEXT}}

---

## Audit Trail

**Report Generated By**: {{GENERATED_BY}}  
**Generation Tool**: {{GENERATION_TOOL}}  
**Data Hash (MD5)**: {{DATA_HASH}}  
**Report Version**: {{REPORT_VERSION}}

**Data Collection Period**: {{DATA_START_DATE}} to {{DATA_END_DATE}}  
**Next Review Date**: {{NEXT_REVIEW_DATE}}

---

**Appendix**: For detailed traceability chains and domain-specific analysis, refer to:
- **Traceability Report**: Complete Asset → DS → TS → RT → CSG mappings
- **Multi-layer Report**: Domain-grouped threat analysis with cross-domain dependencies
