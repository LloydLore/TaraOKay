# TARA Export Methodology - Sphinx & PDF Publication

This guide provides methodology for exporting TARA Markdown content to professional Sphinx documentation sites and audience-specific PDF reports, aligned with ISO 21434 Clause 8.4 (Work Products) publication requirements.

---

## Overview

**TARA Export** converts completed TARA analysis (data catalogues + reports) into publishable formats for stakeholder communication, compliance documentation, and external distribution.

**Key Characteristics**:
- Input: 8 required Markdown files + optional `data/at.md`
- Output: 1 Sphinx HTML site + 4 audience-filtered PDFs
- Read-only operation — export NEVER modifies source files
- Audience-specific filtering — different PDFs for different stakeholders
- Professional typesetting — LaTeX for print-quality PDFs
- ISO 21434 compliant documentation delivery

**Export Prerequisite**:
```
TARA Content Completeness (8 required + 1 optional file):
  ├── data/asset_list.md       Asset catalogue
  ├── data/ds.md               Damage scenarios
  ├── data/ts.md               Threat scenarios
  ├── data/at.md               Attack trees (optional)
  ├── data/rt.md               Risk treatments
  ├── data/csg.md              Cybersecurity goals
  ├── reports/overall_report.md        Executive summary
  ├── reports/traceability_report.md   Audit evidence
  └── reports/multilayer_report.md     Technical architecture
```

**Export Output Locations**:
```
docs/sphinx/           Sphinx RST intermediate files
_build/html/           Sphinx HTML documentation site
output/pdf/            Audience-specific PDF reports
  ├── tara_complete.pdf          Complete archive (all available source files)
  ├── overall_report.pdf         Executive summary only
  ├── traceability_report.pdf    Audit evidence (traceability + CSG)
  └── multilayer_report.pdf      Technical review (multilayer + threats)
```

---

## When to Export

### Trigger Conditions

Export documentation at these points in the TARA lifecycle:

#### 1. After Report Generation Complete
- All 8 required source files exist; `data/at.md` is included when present
- Reports generated via `tara_report` skill
- Content ready for external distribution
- Stakeholders require browseable documentation or PDFs

**Typical Timeline**: After Phase 2 (Cybersecurity Goals) completion in ISO 21434 Clause 15

---

#### 2. For Stakeholder Delivery
- **Executive stakeholders**: Need overall_report.pdf (high-level summary)
- **Audit agencies**: Need traceability_report.pdf (ISO 21434 / UN R155 evidence)
- **Project team**: Need multilayer_report.pdf (technical architecture)
- **Internal archive**: Need tara_complete.pdf (complete record)
- **Public documentation**: Need Sphinx HTML site (browseable web access)

---

#### 3. For Compliance Submission
- ISO 21434 type approval documentation package
- UN R155 cyber security management system (CSMS) evidence
- Insurance or third-party risk assessment documentation
- Supply chain security requirements demonstration

---

### When NOT to Export

- **Source files missing**: Do not export if any required prerequisite files are missing
- **Reports outdated**: Regenerate reports via `tara_report` skill before export
- **Analysis incomplete**: Finish TARA workflow before publication
- **Content editing needed**: Fix source files first, NEVER edit export output

---

## Export Workflows

### A. Sphinx HTML Export

**Purpose**: Generate browseable documentation website from all required source files and optional attack trees when present.

**Technology Stack**:
- Pandoc 3.x — Markdown → RST conversion
- Sphinx 7.x — Documentation generation
- sphinx-book-theme — PyData ecosystem theme
- myst-parser — Markdown support for Sphinx

**Installation Prerequisites**:
```bash
python -m venv .venv
. .venv/bin/activate
pip install sphinx sphinx-book-theme myst-parser
pandoc --version
```

**Workflow Steps**:
1. Copy Markdown into `docs/sphinx/` and use MyST directly (Pandoc → RST is optional)
2. Configure Sphinx (conf.py from template)
3. Build HTML site via `sphinx-build`
4. Verify output in `_build/html/index.html`

**Output Structure**:
```
_build/html/
├── index.html              Documentation homepage
├── data/                   Converted data catalogues (5 required + optional attack-tree page)
├── reports/                Converted reports (3 pages)
├── _static/                CSS, JS, images (sphinx-book-theme assets)
└── _sources/               RST source files (for reference)
```

**Use Cases**:
- Internal team documentation portal
- Stakeholder self-service access to TARA analysis
- Searchable, cross-referenced threat scenario lookup
- Version-controlled documentation history (via git)

---

### B. PDF Export

**Purpose**: Generate audience-filtered PDF reports for stakeholder distribution.

**Technology Stack**:
- Pandoc 3.x — Markdown → PDF conversion
- LaTeX (pdflatex/xelatex) — Professional typesetting
- Custom LaTeX preamble — Fonts, margins, headers, styling

**Installation Prerequisites**:
```bash
pandoc --version
xelatex --version
```

**Audience Filtering Strategy**:

| PDF Output | Target Audience | Content Filter | Use Case |
|------------|-----------------|----------------|----------|
| `tara_complete.pdf` | Internal archive | 8 required files + optional `data/at.md` | Complete project record, legal archival |
| `overall_report.pdf` | Executives, customers | `reports/overall_report.md` only | High-level risk summary, board presentations |
| `traceability_report.pdf` | Audit agencies | `reports/traceability_report.md` + `data/csg.md` | ISO 21434 / UN R155 compliance evidence |
| `multilayer_report.pdf` | Project team | `reports/multilayer_report.md` + `data/ts.md` + `data/at.md` | Technical architecture, implementation guidance |

**Workflow Steps**:
1. Apply audience filter (select source files per PDF output)
2. Convert Markdown → PDF using Pandoc with LaTeX preamble
3. Apply custom styling (fonts, margins, headers via LATEX_PREAMBLE.tex)
4. Verify output in `output/pdf/`

**PDF Metadata** (from LaTeX preamble):
- Title: Derived from project name
- Author: Configurable via template
- Subject: "Automotive Cybersecurity TARA"
- Keywords: "ISO 21434, UN R155, Threat Analysis, Risk Assessment"

**Use Cases**:
- Executive risk review presentations (overall_report.pdf)
- ISO 21434 audit submission (traceability_report.pdf)
- Development team handoff (multilayer_report.pdf)
- Long-term project archival (tara_complete.pdf)

---

## Export Quality Standards

### Content Integrity
- **NO modification**: Export NEVER changes source files
- **Lossless conversion**: All Markdown content preserved in outputs
- **Link preservation**: Internal cross-references maintained in Sphinx HTML
- **Table formatting**: Complex tables render correctly in PDF (LaTeX booktabs)

### Professional Presentation
- **Typography**: LaTeX professional fonts and spacing
- **Navigation**: Sphinx site includes search, sidebar TOC, breadcrumbs
- **Branding**: Customizable headers, footers, logos via templates
- **Accessibility**: Sphinx HTML meets WCAG standards, PDF bookmarks for navigation

### Compliance Requirements
- **ISO 21434 Clause 8.4**: Work products delivered in auditable format
- **UN R155 Annex 5**: CSMS documentation evidence traceable
- **Version control**: Export output tracked via git (commit hash in PDF metadata)

---

## Tool Configuration

### Sphinx Configuration (conf.py)

**Required Extensions**:
```python
extensions = ['myst_parser']
```

**Theme Settings**:
```python
html_theme = 'sphinx_book_theme'
html_theme_options = {
    'show_toc_level': 2,
    'navigation_with_keys': True,
}
```

**MyST-Parser Options**:
```python
myst_enable_extensions = [
    "deflist",       
    "colon_fence",   
    "substitution",  
]
```

### Pandoc Conversion Options

**Markdown → RST**:
```bash
pandoc -f markdown -t rst input.md -o output.rst
```

**Markdown → PDF** (with LaTeX):
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  --include-in-header=LATEX_PREAMBLE.tex \
  --metadata title="<title>" \
  --metadata author="<author>"
```

### LaTeX Styling (LATEX_PREAMBLE.tex)

**Key Customizations**:
- Page geometry: A4, 25mm margins
- Headers/footers: Project name, page numbers
- Hyperlinks: Colored links, PDF bookmarks
- Code blocks: Syntax highlighting, line numbers
- Tables: Professional booktabs formatting

---

## Troubleshooting

### Common Issues

**Issue**: Pandoc not found  
**Solution**: Install Pandoc 3.x from https://pandoc.org/installing.html

**Issue**: LaTeX errors during PDF build  
**Solution**: Install full LaTeX distribution (TeX Live, MiKTeX)

**Issue**: Sphinx build fails with "myst_parser not found"  
**Solution**: `pip install myst-parser`

**Issue**: PDF tables overflow page width  
**Solution**: Simplify Markdown tables, use landscape orientation for wide tables

**Issue**: Internal links broken in Sphinx HTML  
**Solution**: Use MyST `toctree` for navigation and Sphinx document references, not raw `.md` links.

---

## Best Practices

### Before Export
1. **Verify source files complete**: All 8 required Markdown files exist and validate `data/at.md` separately if present
2. **Regenerate reports**: Run `tara_report` skill if data catalogues changed
3. **Review content**: Manually check critical sections (executive summary, RV-5 threats)

### During Export
1. **Clean build directories carefully**: Remove old output only after verifying the target path (for example `test -d _build && rm -rf -- _build/html`)
2. **Run Sphinx first**: HTML export catches Markdown formatting issues early
3. **Test PDFs individually**: Generate one PDF at a time to isolate filter errors

### After Export
1. **Visual inspection**: Open HTML site, verify navigation and search
2. **PDF validation**: Check all 4 PDFs render correctly, bookmarks work
3. **File size check**: Large PDFs (>10MB) may indicate image optimization needed
4. **Git commit**: Tag export output with version (e.g., `v1.0-export`)

---

## ISO 21434 Mapping

| ISO 21434 Clause | Export Requirement | Implementation |
|---|---|---|
| 8.4 (Work Products) | Document cybersecurity analysis results | Sphinx HTML + 4 PDFs |
| 15.3 (Asset identification) | Communicate asset catalogue | `data/asset_list.md` in exports |
| 15.5 (Impact rating) | Document damage scenarios | `data/ds.md` in exports |
| 15.6 (Threat scenario identification) | Document threat scenarios | `data/ts.md` in exports |
| 15.7 (Attack path analysis) | Document attack trees | `data/at.md` in exports |
| 15.8 (Risk determination) | Document risk treatment | `data/rt.md` in exports |
| 15.9 (Cybersecurity goals) | Document cybersecurity goals | `data/csg.md` in exports |
| 15.11 (Traceability) | Traceability matrix | `traceability_report.pdf` |

---

## References

- **Sphinx Documentation**: https://www.sphinx-doc.org/en/master/
- **sphinx-book-theme**: https://sphinx-book-theme.readthedocs.io/
- **MyST-Parser**: https://myst-parser.readthedocs.io/
- **Pandoc Manual**: https://pandoc.org/MANUAL.html
- **ISO 21434:2021**: Road vehicles - Cybersecurity engineering
- **UN R155**: Uniform provisions concerning cyber security and cyber security management system
