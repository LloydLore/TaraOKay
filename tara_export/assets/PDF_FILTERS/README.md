# PDF Filter Definitions for Audience-Specific Exports

## Filter: tara_complete.pdf
**Target Audience**: Internal archive  
**Content**: All 8 required source files + optional `data/at.md`

**Required include**:
- data/asset_list.md
- data/ds.md
- data/ts.md
- data/rt.md
- data/csg.md
- reports/overall_report.md
- reports/traceability_report.md
- reports/multilayer_report.md

**Optional include**:
- data/at.md

**Exclude**: None (complete archive)

---

## Filter: overall_report.pdf
**Target Audience**: Customers, executives  
**Content**: Executive summary only

**Include**:
- reports/overall_report.md

**Exclude**: All data/ files, other reports

---

## Filter: traceability_report.pdf
**Target Audience**: Audit agencies (ISO 21434, UN R155)  
**Content**: Traceability matrix + CSG summary

**Include**:
- reports/traceability_report.md
- data/csg.md (cybersecurity goals summary)

**Exclude**: Other data files, other reports

---

## Filter: multilayer_report.pdf
**Target Audience**: Internal project team  
**Content**: Technical architecture view + threat data (+ optional attack trees)

**Include**:
- reports/multilayer_report.md
- data/ts.md (threat scenarios for reference)

**Optional include**:
- data/at.md (attack trees for technical detail)

**Exclude**: Asset list, damage scenarios, risk treatments, CSG
