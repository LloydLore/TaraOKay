---
name: tara_export
version: 1.0.0
description: Export TARA Markdown content (data/ + reports/) to professional Sphinx documentation site and audience-specific PDF reports. Converts existing TARA work products into publishable formats for stakeholder communication, compliance documentation, and technical review.
---
# TARA Export -- Skill Workflow

## 1. When to Use This Skill

**Trigger ON** when the user is:
- Exporting completed TARA work to Sphinx documentation site
- Generating PDF reports from existing TARA Markdown files
- Creating documentation site for stakeholder access to TARA analysis
- Preparing professional PDF reports for different audiences (executives, auditors, technical team)
- Publishing TARA analysis as static HTML documentation
- Converting Markdown TARA content to browseable website
- Asking about "sphinx export", "pdf export", "documentation site", "generate website", "publish TARA", "create PDF report"
- Needing audience-filtered PDF outputs (complete archive, executive summary, audit evidence, technical deep-dive)
- Completing ISO 21434 documentation delivery requirements (Clause 8.4 work product publication)
- After completing TARA reports using `tara_report` skill (reports/ directory is populated)
- Preparing TARA deliverables for external communication or compliance submission

**Trigger OFF** when the user asks:
- About generating TARA reports from data catalogues (use `tara_report` skill instead — this skill ONLY exports existing reports)
- About damage scenario creation, threat analysis, or risk assessment workflows (export is final publication step, not analysis)
- About editing TARA data files (asset_list.md, ds.md, ts.md, etc.) — export does NOT modify source data
- About creating new TARA content (use domain-specific skills: damage_scenario, threat_scenario, risk_treatment, csg)
- About CI/CD pipelines, GitHub Pages deployment, or hosting infrastructure (out of scope)
- About EPUB, DOCX, or other export formats beyond Sphinx HTML and PDF (not supported)
- General ISO 21434 theory unrelated to documentation export
- Modifying existing skills or creating custom Sphinx extensions

**CRITICAL DISTINCTION - Export vs Report Generation**:
- **tara_report skill**: Generates Markdown reports FROM data catalogues (6 input files → 3 output Markdown reports)
- **tara_export skill (this skill)**: Exports existing Markdown content TO publishable formats (8 required Markdown files + optional `data/at.md` → Sphinx HTML + 4 PDFs)

**Example Distinction**:
- ✅ tara_export: "Export reports/ to Sphinx documentation site" (publish existing content)
- ❌ tara_report: "Generate overall_report.md from data files" (create new reports)

Report generation is OUT OF SCOPE for this skill. Use this skill for export only.

---

## 2. Target Project Quick Reference

This skill is part of the **TaraOK skill set** for automotive cybersecurity TARA work.
Locate the target project root from the working directory -- do NOT hardcode any paths.

Path note: in this source repository, this skill lives at `tara_export/`. In an installed target project, it may live at `skills/tara_export/`.

**Runtime directories** (relative to the target project root):

```
data/                                  SOURCE: Input data catalogues (6 files)
  ├── asset_list.md                    Asset catalogue with CIA ratings
  ├── ds.md                            Damage scenarios with SFOP impact scores
  ├── ts.md                            Threat scenarios with AFR ratings
  ├── at.md                            Attack trees (optional, multi-step attacks)
  ├── rt.md                            Risk treatment decisions
  └── csg.md                           Cybersecurity goals
reports/                               SOURCE: Generated reports (3 files)
  ├── overall_report.md                Overall risk assessment (executive view)
  ├── traceability_report.md           Complete traceability matrix (audit view)
  └── multilayer_report.md             Domain-grouped analysis (technical view)
docs/sphinx/                           OUTPUT: Sphinx RST files (intermediate)
  ├── index.rst                        Main documentation entry point
  ├── data/                            Converted data catalogues (6 RST files)
  └── reports/                         Converted reports (3 RST files)
_build/html/                           OUTPUT: Sphinx HTML site
  ├── index.html                       Documentation site homepage
  ├── _static/                         CSS, JS, images
  └── [generated HTML files]
output/pdf/                            OUTPUT: Audience-specific PDFs
  ├── tara_complete.pdf                Complete archive (all available source files)
  ├── overall_report.pdf               Executive summary (reports/overall_report.md only)
  ├── traceability_report.pdf          Audit evidence (reports/traceability_report.md + CSG summary)
  └── multilayer_report.pdf            Technical review (reports/multilayer_report.md + threat data)
skills/tara_export/                    Installed skill files (workflow, templates, references)
  ├── SKILL.md                         This file (workflow guide)
  ├── assets/
  │   ├── CONF_PY_TEMPLATE.py          Sphinx configuration template
  │   ├── MAKEFILE_TEMPLATE            Build automation template
  │   ├── LATEX_PREAMBLE.tex           PDF styling (fonts, margins, headers)
  │   └── PDF_FILTERS/                 Audience filter definitions
  └── references/
      ├── export-guide.md              Export methodology and best practices
      └── export-schema.md             Output format specifications
```

**Workflow Overview**:
```
Source Files (8 required Markdown + optional `data/at.md`) → Sphinx Export (HTML site) → PDF Export (4 audience-specific PDFs)
                           ↓
                    docs/sphinx/ (RST intermediate)
                           ↓
                    _build/html/ (browseable site)
```

**Prerequisites** (8 required + 1 optional before export):
- **TARA Source Content** (8 required Markdown files + 1 optional file):
  - `data/asset_list.md` — From asset_analysis skill
  - `data/ds.md` — From damage_scenario skill
  - `data/ts.md` — From threat_scenario skill
  - `data/at.md` — From attack_tree skill (optional; included in exports when present)
  - `data/rt.md` — From risk_treatment skill
  - `data/csg.md` — From csg skill
  - `reports/overall_report.md` — From tara_report skill
  - `reports/traceability_report.md` — From tara_report skill
  - `reports/multilayer_report.md` — From tara_report skill
- **Tools**:
  - Pandoc 3.x — Markdown → RST and Markdown → PDF conversion
  - Python 3.x — Sphinx execution environment
  - Sphinx 7.x — Documentation generation engine
  - sphinx-book-theme — PyData ecosystem theme
  - myst-parser — Markdown support for Sphinx
  - LaTeX distribution (pdflatex or xelatex) — Professional PDF typesetting

**Tool Installation** (if missing):
```bash
# Verify Pandoc
pandoc --version  # Should show 3.x

# Recommended: install Python tooling in a virtual environment
python -m venv .venv
. .venv/bin/activate
pip install sphinx sphinx-book-theme myst-parser

# Verify xelatex (required for the PDF commands below)
xelatex --version
```

**Output counts**:
- Sphinx HTML: 1 documentation site with 8-9 content pages (5 required data files + optional attack trees + 3 reports, plus index/navigation)
- PDF Reports: EXACTLY 4 files (complete, overall, traceability, multilayer)

---

## 3. Step-by-Step Workflow

### Step 1: Validate Export Prerequisites

**Before exporting**, verify all required tools and source files exist:

**Check 1: Tool availability**
```bash
pandoc --version
sphinx-build --version
xelatex --version
```

**Check 2: Source file existence**
```bash
test -f data/asset_list.md && test -f data/ds.md && test -f data/ts.md && \
test -f data/rt.md && test -f data/csg.md && \
test -f reports/overall_report.md && test -f reports/traceability_report.md && \
test -f reports/multilayer_report.md && \
echo "✓ All 8 required source files present" || echo "⚠️ Missing required source files"

test -f data/at.md && echo "✓ Optional data/at.md present" || echo "ℹ️ Optional data/at.md absent - export will skip attack-tree appendix content"
```

**Check 3: Tool installation** (if checks fail)
```bash
python -m venv .venv
. .venv/bin/activate
pip install sphinx sphinx-book-theme myst-parser
```

**Validation criteria**:
- [ ] Pandoc 3.x available
- [ ] Sphinx 7.x installed
- [ ] LaTeX distribution available (for PDF export)
- [ ] 5 required data files exist (`asset_list.md`, `ds.md`, `ts.md`, `rt.md`, `csg.md`)
- [ ] Optional `data/at.md` handled correctly if absent
- [ ] All 3 report files exist (reports/*.md)

**If validation fails**: Install missing tools or regenerate reports via `tara_report` skill before export.

---

### Step 2: Initialize Sphinx Project

**Purpose**: Set up Sphinx directory structure and configuration for HTML site generation.

**Create output directories**:
```bash
mkdir -p docs/sphinx/data
mkdir -p docs/sphinx/reports
mkdir -p _build/html
```

**Copy Sphinx configuration template**:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cp "$REPO_ROOT/skills/tara_export/assets/CONF_PY_TEMPLATE.py" docs/sphinx/conf.py
```

**Customize conf.py placeholders** (⚠️ values below are examples — MUST be customized per project):
```bash
python - <<'PY'
from pathlib import Path

path = Path("docs/sphinx/conf.py")
text = path.read_text()
replacements = {
    "{{PROJECT_NAME}}": "TaraOK TARA Documentation",     # TODO: set actual project name
    "{{COPYRIGHT_YEAR}}": "2026",                         # TODO: set current year
    "{{COPYRIGHT_HOLDER}}": "Automotive OEM Inc.",        # TODO: set actual company
    "{{AUTHOR_NAME}}": "Security Team",                   # TODO: set actual author/team
    "{{VERSION}}": "1.0",
    "{{RELEASE}}": "1.0.0",
    "{{REPOSITORY_URL}}": "https://github.com/example/taraok",       # TODO: set actual repo URL
    "{{HTML_TITLE}}": "TARA Documentation",
    "{{HTML_SHORT_TITLE}}": "TARA",
    "{{LATEX_PREAMBLE_FILE}}": "../../skills/tara_export/assets/LATEX_PREAMBLE.tex",
    "{{PDF_FILENAME}}": "tara_complete",
    "{{PDF_TITLE}}": "TARA Complete Archive",
    "{{PDF_AUTHOR}}": "Security Team",                    # TODO: set actual author/team
    "{{PROJECT_SLUG}}": "taraok",                        # TODO: set actual slug
    "{{PROJECT_DESCRIPTION}}": "Automotive Cybersecurity TARA",
}
for old, new in replacements.items():
    text = text.replace(old, new)
path.write_text(text)
PY
```

**Copy Makefile** (optional, for build automation):
```bash
cp "$REPO_ROOT/skills/tara_export/assets/MAKEFILE_TEMPLATE" Makefile
```

**Validation**:
```bash
test -f docs/sphinx/conf.py && echo "✓ Sphinx configured"
grep -q "myst_parser" docs/sphinx/conf.py && echo "✓ myst-parser enabled"
grep -q "sphinx_book_theme" docs/sphinx/conf.py && echo "✓ Theme configured"
```

---

### Step 3: Prepare Sphinx Source Files

**Purpose**: Copy all required Markdown source files (plus optional attack trees when present) into `docs/sphinx/` for Sphinx processing.

**Option A: Direct Markdown Support** (recommended)

With `myst-parser`, Sphinx can read Markdown directly without conversion:

```bash
cp data/*.md docs/sphinx/data/
cp reports/*.md docs/sphinx/reports/
```

**Option B: Full RST Conversion** (if RST-specific features needed)

Convert each Markdown file to RST using Pandoc:

```bash
for file in data/*.md; do
    basename=$(basename "$file" .md)
    pandoc -f markdown -t rst "$file" -o "docs/sphinx/data/${basename}.rst"
done

for file in reports/*.md; do
    basename=$(basename "$file" .md)
    pandoc -f markdown -t rst "$file" -o "docs/sphinx/reports/${basename}.rst"
done
```

**Validation**:
```bash
ls docs/sphinx/data/*.md 2>/dev/null | wc -l
ls docs/sphinx/reports/*.md 2>/dev/null | wc -l
```

---

### Step 4: Create Sphinx Index (toctree)

**Purpose**: Generate index.rst with navigation structure for all available source files.

**Create index.rst**:
```bash
cat > docs/sphinx/index.rst << 'EOF'
================================
TARA Documentation
================================

Automotive Cybersecurity Threat Analysis and Risk Assessment (TARA) documentation.

.. toctree::
   :maxdepth: 2
   :caption: Data Catalogues

   data/asset_list
   data/ds
   data/ts
   data/rt
   data/csg

EOF

if test -f docs/sphinx/data/at.md || test -f docs/sphinx/data/at.rst; then
cat >> docs/sphinx/index.rst << 'EOF'
   data/at
EOF
fi

cat >> docs/sphinx/index.rst << 'EOF'

.. toctree::
   :maxdepth: 2
   :caption: Reports

   reports/overall_report
   reports/traceability_report
   reports/multilayer_report

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
EOF
```

**For Markdown index** (if using myst-parser):
```bash
cat > docs/sphinx/index.md << 'EOF'
# TARA Documentation

Automotive Cybersecurity Threat Analysis and Risk Assessment (TARA) documentation.

## Data Catalogues

```{toctree}
:maxdepth: 2

data/asset_list
data/ds
data/ts
data/rt
data/csg
```

## Reports

```{toctree}
:maxdepth: 2

reports/overall_report
reports/traceability_report
reports/multilayer_report
```
EOF

if test -f docs/sphinx/data/at.md; then
cat >> docs/sphinx/index.md << 'EOF'

## Optional Data

```{toctree}
:maxdepth: 2

data/at
```
EOF
fi
```

**Validation**:
```bash
test -f docs/sphinx/index.rst && echo "✓ Index created" || test -f docs/sphinx/index.md && echo "✓ Index created (Markdown)"
```

---

### Step 5: Build Sphinx HTML Site

**Purpose**: Generate browseable HTML documentation from Sphinx source.

**Build command**:
```bash
sphinx-build -b html docs/sphinx _build/html
```

**Using Makefile** (if copied in Step 2):
```bash
make html
```

**Build output indicators**:
- Green "build succeeded" message
- No warnings or errors
- Output written to `_build/html/`

**Validation**:
```bash
test -f _build/html/index.html && echo "✓ HTML site generated"
ls _build/html/data/*.html | wc -l
ls _build/html/reports/*.html | wc -l
```

**Expected file counts**:
- 5-6 HTML files in `_build/html/data/` (5 required data catalogues + optional `at.html`)
- 3 HTML files in `_build/html/reports/` (3 reports)
- 1 `index.html` (homepage)
- `search.html` (search interface)

---

### Step 6: Verify Sphinx Output

**Purpose**: Quality assurance checks for generated HTML site.

**Check 1: File structure**
```bash
tree _build/html -L 2
```

**Check 2: Navigation links**
```bash
grep -o 'href="[^"]*"' _build/html/index.html | head -10
```

**Check 3: Search functionality**
```bash
test -f _build/html/searchindex.js && echo "✓ Search index generated"
```

**Check 4: Theme assets**
```bash
test -d _build/html/_static/sphinx_book_theme && echo "✓ Theme assets loaded"
```

**Check 5: Manual inspection**
```bash
xdg-open _build/html/index.html 2>/dev/null || open _build/html/index.html
```

**Verification checklist**:
- [ ] Homepage loads correctly
- [ ] Sidebar navigation shows all available source files (attack trees included only if present)
- [ ] Search bar functional
- [ ] Internal links work (click between pages)
- [ ] Code blocks render with syntax highlighting
- [ ] Tables render correctly

**Common issues**:
- **Broken links**: Check toctree paths in index.rst match actual file locations
- **Missing theme**: Run `pip install sphinx-book-theme` and rebuild
- **Search broken**: Ensure `searchindex.js` exists in `_build/html/`

---

### Step 7: Validate LaTeX Prerequisites

**Purpose**: Verify PDF export tools are available before generating PDFs.

**Check LaTeX availability**:
```bash
xelatex --version
```

**Expected output**: Version information (e.g., "pdfTeX 3.14159265")

**If LaTeX missing**:
```bash
# Ubuntu/Debian
sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-latex-extra

# macOS
brew install basictex

# Or download full TeX Live distribution: https://www.tug.org/texlive/
```

**Create output directory**:
```bash
mkdir -p output/pdf
```

Pandoc PDF generation in this workflow uses the static preamble file directly from `skills/tara_export/assets/LATEX_PREAMBLE.tex`; no placeholder replacement is required.

---

### Step 8: Generate Complete PDF (tara_complete.pdf)

**Purpose**: Generate comprehensive archive PDF with all available source files for internal record-keeping.

**Target Audience**: Internal archive, legal compliance  
**Content**: All 5 required data files + all 3 reports (+ `data/at.md` if present)

**Generate PDF with Pandoc**:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
PANDOC_INPUTS="data/asset_list.md data/ds.md data/ts.md data/rt.md data/csg.md \
reports/overall_report.md reports/traceability_report.md reports/multilayer_report.md"
test -f data/at.md && PANDOC_INPUTS="$PANDOC_INPUTS data/at.md"

pandoc $PANDOC_INPUTS -o output/pdf/tara_complete.pdf \
  --pdf-engine=xelatex \
  --include-in-header="$REPO_ROOT/skills/tara_export/assets/LATEX_PREAMBLE.tex" \
  --metadata title="TARA Complete Archive" \
  --metadata author="Security Team" \
  --metadata subject="Automotive Cybersecurity TARA" \
  --metadata keywords="ISO 21434, UN R155, TARA, Threat Analysis, Risk Assessment" \
  --toc \
  --toc-depth=3 \
  --number-sections
```

**Validation**:
```bash
test -f output/pdf/tara_complete.pdf && echo "✓ tara_complete.pdf generated"
pdfinfo output/pdf/tara_complete.pdf | grep "Pages:"
```

**Expected output**: Usually 100-200 pages depending on content and PDF engine

---

### Step 9: Generate Overall PDF (overall_report.pdf)

**Purpose**: Generate executive summary PDF for high-level stakeholder communication.

**Target Audience**: Executives, customers, board members  
**Content**: `reports/overall_report.md` ONLY

**Generate PDF with Pandoc**:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
pandoc reports/overall_report.md -o output/pdf/overall_report.pdf \
  --pdf-engine=xelatex \
  --include-in-header="$REPO_ROOT/skills/tara_export/assets/LATEX_PREAMBLE.tex" \
  --metadata title="TARA Overall Risk Assessment" \
  --metadata author="Security Team" \
  --metadata subject="Executive Risk Summary" \
  --metadata keywords="ISO 21434, Risk Assessment, Executive Summary" \
  --toc \
  --toc-depth=2 \
  --number-sections
```

**Validation**:
```bash
test -f output/pdf/overall_report.pdf && echo "✓ overall_report.pdf generated"
pdfinfo output/pdf/overall_report.pdf | grep "Pages:"
```

**Expected output**: Usually 12-17 pages depending on content and PDF engine

---

### Step 10: Generate Traceability PDF (traceability_report.pdf)

**Purpose**: Generate audit evidence PDF with complete traceability matrix and cybersecurity goals.

**Target Audience**: Audit agencies, ISO 21434 / UN R155 assessors  
**Content**: `reports/traceability_report.md` + `data/csg.md`

**Generate PDF with Pandoc**:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
pandoc reports/traceability_report.md data/csg.md -o output/pdf/traceability_report.pdf \
  --pdf-engine=xelatex \
  --include-in-header="$REPO_ROOT/skills/tara_export/assets/LATEX_PREAMBLE.tex" \
  --metadata title="TARA Traceability Report - ISO 21434 Compliance" \
  --metadata author="Security Team" \
  --metadata subject="Audit Evidence and Traceability Matrix" \
  --metadata keywords="ISO 21434, UN R155, Traceability, Audit, Compliance" \
  --toc \
  --toc-depth=3 \
  --number-sections
```

**Validation**:
```bash
test -f output/pdf/traceability_report.pdf && echo "✓ traceability_report.pdf generated"
pdfinfo output/pdf/traceability_report.pdf | grep "Pages:"
```

**Expected output**: Usually 27-47 pages depending on content and PDF engine

---

### Step 11: Generate Multilayer PDF (multilayer_report.pdf)

**Purpose**: Generate technical architecture PDF with domain analysis and threat details.

**Target Audience**: Internal project team, security architects, developers  
**Content**: `reports/multilayer_report.md` + `data/ts.md` (+ `data/at.md` if present)

**Generate PDF with Pandoc**:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
PANDOC_INPUTS="reports/multilayer_report.md data/ts.md"
test -f data/at.md && PANDOC_INPUTS="$PANDOC_INPUTS data/at.md"

pandoc $PANDOC_INPUTS -o output/pdf/multilayer_report.pdf \
  --pdf-engine=xelatex \
  --include-in-header="$REPO_ROOT/skills/tara_export/assets/LATEX_PREAMBLE.tex" \
  --metadata title="TARA Multi-layer Report - Technical Architecture" \
  --metadata author="Security Team" \
  --metadata subject="Technical Risk Analysis and Attack Chains" \
  --metadata keywords="TARA, Attack Trees, Threat Scenarios, Security Architecture" \
  --toc \
  --toc-depth=3 \
  --number-sections
```

**Validation**:
```bash
test -f output/pdf/multilayer_report.pdf && echo "✓ multilayer_report.pdf generated"
pdfinfo output/pdf/multilayer_report.pdf | grep "Pages:"
```

**Expected output**: Usually 47-88 pages depending on content, PDF engine, and whether `data/at.md` is present

---

### Step 12: Verify All PDF Outputs

**Purpose**: Final quality assurance for all 4 generated PDFs.

**Check all PDFs exist**:
```bash
ls -lh output/pdf/*.pdf
```

**Expected files**:
- `tara_complete.pdf` (largest, ~100-200 pages)
- `overall_report.pdf` (smallest, ~12-17 pages)
- `traceability_report.pdf` (medium, ~27-47 pages)
- `multilayer_report.pdf` (medium, ~47-88 pages)

**Validate PDF metadata**:
```bash
for pdf in output/pdf/*.pdf; do
    echo "=== $(basename $pdf) ==="
    pdfinfo "$pdf" | grep -E "Title:|Author:|Pages:"
done
```

**Validation checklist**:
- [ ] All 4 PDFs generated successfully
- [ ] File sizes reasonable (no 0-byte files)
- [ ] Metadata populated (Title, Author, Subject)
- [ ] Page counts match expected ranges
- [ ] PDFs open without errors
- [ ] Table of contents present in each PDF
- [ ] Internal bookmarks work (PDF navigation pane)

**Manual inspection**:
```bash
xdg-open output/pdf/tara_complete.pdf 2>/dev/null || open output/pdf/tara_complete.pdf
xdg-open output/pdf/overall_report.pdf 2>/dev/null || open output/pdf/overall_report.pdf
xdg-open output/pdf/traceability_report.pdf 2>/dev/null || open output/pdf/traceability_report.pdf
xdg-open output/pdf/multilayer_report.pdf 2>/dev/null || open output/pdf/multilayer_report.pdf
```

**Common issues**:
- **LaTeX errors**: Check LATEX_PREAMBLE.tex syntax, ensure all packages installed
- **Pandoc conversion errors**: Simplify complex Markdown tables, escape special characters
- **Missing bookmarks**: Ensure `--toc` and `--number-sections` flags used
- **Empty PDFs**: Check source Markdown files exist and are not empty

---

## 4. Field-by-Field Guidance

**Note**: Export configuration involves 30+ placeholders in Sphinx conf.py, 15+ in LaTeX preamble, and 10+ filter definitions for PDF generation. Rather than duplicate field definitions here, refer to the authoritative schema document:

**Comprehensive field reference**: `skills/tara_export/references/export-schema.md` (400+ lines)

**Schema sections**:
- Sphinx HTML Output (6 categories)
  - Output Structure, HTML Metadata, Navigation Features, Styling Specifications, Accessibility, Validation
- PDF Output (8 categories)
  - PDF Types and Content Filters, PDF Metadata, Page Layout, Typography, Styling Elements, Table of Contents, PDF Bookmarks, Output Validation
- Template Variables (2 categories)
  - Sphinx conf.py Placeholders (17 variables), LaTeX Preamble Placeholders (5 variables)

**Validation rules** (from schema):
- All 4 PDFs must be generated
- Sphinx HTML must include all required source files and optional attack trees when present
- PDF page counts should be used as heuristics, not strict pass/fail gates
- PDF metadata must be populated (Title, Author, Subject)
- HTML navigation must show all required source files and optional attack trees when present
- Search functionality must work in HTML output

**Quick reference table** (most common placeholders):

| Category | Placeholder | Location | Purpose |
|----------|-------------|----------|---------|
| Project | {{PROJECT_NAME}} | conf.py, LaTeX preamble | Display name in headers |
| Project | {{AUTHOR_NAME}} | conf.py | Author field in metadata |
| Project | {{VERSION}} | conf.py | Short version (X.Y) |
| Output | docs/sphinx/ | File system | Sphinx RST intermediate |
| Output | _build/html/ | File system | HTML documentation site |
| Output | output/pdf/ | File system | PDF reports directory |
| PDF | tara_complete.pdf | output/pdf/ | Complete archive (all available source files) |
| PDF | overall_report.pdf | output/pdf/ | Executive summary only |
| PDF | traceability_report.pdf | output/pdf/ | Audit evidence (traceability + CSG) |
| PDF | multilayer_report.pdf | output/pdf/ | Technical review (multilayer + threats) |

For detailed field specifications, validation rules, and examples, consult `references/export-schema.md`.

---

## 5. Common Patterns

### Pattern 1: Full Documentation Site + All PDFs

**Scenario**: TARA project complete; publish full documentation site and generate all audience-specific PDFs for distribution.

**Use case**: Final project deliverable, comprehensive documentation package.

**Workflow**: Execute Steps 1 → 12 sequentially (all steps).

**Typical outputs**:
- Sphinx HTML: 1 site with 8-9 content pages depending on whether attack trees are present
- PDF complete: ~100-200 pages
- PDF overall: ~12-17 pages
- PDF traceability: ~27-47 pages
- PDF multilayer: ~47-88 pages

---

### Pattern 2: Executive PDF Only (Quick Export)

**Scenario**: Board meeting tomorrow, need executive summary PDF immediately.

**Use case**: Time-sensitive executive communication, high-level risk summary.

**Workflow**: Execute Step 1 (validate only `reports/overall_report.md` + LaTeX) → Step 7 (validate LaTeX) → Step 9 (generate overall PDF only) → Step 12 (verify the single PDF).

**Typical output**: 12-17 page PDF ready in <1 minute.

---

### Pattern 3: Audit Evidence Package (Traceability + Multilayer PDFs)

**Scenario**: ISO 21434 auditor requests traceability evidence and technical documentation.

**Use case**: External audit, compliance submission, UN R155 type approval.

**Workflow**: Execute Step 1 (validate required sources: `reports/traceability_report.md`, `reports/multilayer_report.md`, `data/csg.md`, `data/ts.md`, optional `data/at.md`) → Step 7 → Step 10 → Step 11 → Step 12.

**After PDFs verified**, package for auditor:
```bash
mkdir -p output/audit_package
cp output/pdf/traceability_report.pdf output/pdf/multilayer_report.pdf output/audit_package/
cp data/asset_list.md data/ds.md data/ts.md data/rt.md data/csg.md output/audit_package/
test -f data/at.md && cp data/at.md output/audit_package/

cat > output/audit_package/README.txt << 'AUDITEOF'
TARA Audit Evidence Package
============================

Included Files:
- traceability_report.pdf: Complete traceability matrix (Asset→Threat→Damage→Treatment→Goal)
- multilayer_report.pdf: Technical architecture and multi-layer defense analysis
- data/*.md: Source data catalogues (5 required files + optional attack-tree file if present)

ISO 21434 Mapping:
- Clause 15.11 (Traceability): See traceability_report.pdf
- Clause 15.5-15.9 (TARA phases): See data/*.md source files
- Clause 8.4 (Work Products): All files in this package

Contact: Security Team
AUDITEOF

cd output && zip -r audit_package.zip audit_package/
echo "✓ Audit package ready: output/audit_package.zip"
```

---

### Pattern 4: HTML Site Only (No PDFs)

**Scenario**: Internal team wants browseable documentation, PDFs not needed.

**Use case**: Internal wiki, developer documentation portal, searchable reference.

**Workflow**: Execute Steps 1 → 6 (skip Steps 7-12, which are PDF-only).

**Typical output**: Browseable HTML site with search, navigation, and cross-references.

---

## 6. Quality Checks

Before distributing exported outputs, perform these quality checks:

### Export Prerequisite Validation

**Check all tools and source files exist**:
```bash
# Create output directories if missing
mkdir -p docs/sphinx _build/html output/pdf

# Validate tool availability
pandoc --version || echo "⚠️ Pandoc missing - install from https://pandoc.org"
sphinx-build --version || echo "⚠️ Sphinx missing - create a venv and run: pip install sphinx sphinx-book-theme myst-parser"
xelatex --version || echo "⚠️ xelatex missing - install TeX Live / BasicTeX / MacTeX"

# Validate source files (8 required + optional data/at.md)
test -f data/asset_list.md && echo "✓ asset_list" || echo "⚠️ Missing data/asset_list.md"
test -f data/ds.md && echo "✓ ds" || echo "⚠️ Missing data/ds.md"
test -f data/ts.md && echo "✓ ts" || echo "⚠️ Missing data/ts.md"
test -f data/at.md && echo "✓ at (optional)" || echo "ℹ️ Missing optional data/at.md"
test -f data/rt.md && echo "✓ rt" || echo "⚠️ Missing data/rt.md"
test -f data/csg.md && echo "✓ csg" || echo "⚠️ Missing data/csg.md"
test -f reports/overall_report.md && echo "✓ overall_report" || echo "⚠️ Missing reports/overall_report.md"
test -f reports/traceability_report.md && echo "✓ traceability_report" || echo "⚠️ Missing reports/traceability_report.md"
test -f reports/multilayer_report.md && echo "✓ multilayer_report" || echo "⚠️ Missing reports/multilayer_report.md"
```

**If any source file missing**: Regenerate reports via `tara_report` skill before export.

---

### Sphinx HTML Output Validation

**Check HTML site structure**:
```bash
# Verify HTML files generated
test -f _build/html/index.html && echo "✓ index.html" || echo "⚠️ HTML build failed"

# Count data catalogue pages (expect 5 required + optional attack tree)
DATA_HTML_COUNT=$(ls _build/html/data/*.html 2>/dev/null | wc -l)
echo "Data catalogue HTML pages: $DATA_HTML_COUNT (expected: 5 or 6 depending on data/at.md)"

# Count report pages (expect 3)
REPORT_HTML_COUNT=$(ls _build/html/reports/*.html 2>/dev/null | wc -l)
echo "Report HTML pages: $REPORT_HTML_COUNT (expected: 3)"

# Verify search index
test -f _build/html/searchindex.js && echo "✓ Search index" || echo "⚠️ Search index missing"

# Verify theme assets
test -d _build/html/_static/sphinx_book_theme && echo "✓ Theme assets" || echo "⚠️ Theme missing"
```

**Expected output**:
- 5 required data catalogue HTML pages, with optional `at.html` when `data/at.md` exists
- 3 report HTML pages
- 1 index.html
- 1 search.html
- searchindex.js present
- Theme assets present

**If validation fails**: Review Sphinx build log for errors, fix source Markdown, rebuild.

---

### PDF Output Validation

**Check all 4 PDFs generated**:
```bash
# Verify PDF existence
test -f output/pdf/tara_complete.pdf && echo "✓ tara_complete.pdf" || echo "⚠️ tara_complete.pdf missing"
test -f output/pdf/overall_report.pdf && echo "✓ overall_report.pdf" || echo "⚠️ overall_report.pdf missing"
test -f output/pdf/traceability_report.pdf && echo "✓ traceability_report.pdf" || echo "⚠️ traceability_report.pdf missing"
test -f output/pdf/multilayer_report.pdf && echo "✓ multilayer_report.pdf" || echo "⚠️ multilayer_report.pdf missing"

# Check file sizes (no 0-byte PDFs)
ls -lh output/pdf/*.pdf

# Extract page counts
echo "=== PDF Page Counts ==="
for pdf in output/pdf/*.pdf; do
    echo "$(basename $pdf): $(pdfinfo "$pdf" | grep 'Pages:' | awk '{print $2}') pages"
done
```

**Expected page count ranges** (hard lower bound → soft upper guidance):
- tara_complete.pdf: **≥20 pages** (soft range: 100-200)
- overall_report.pdf: **≥5 pages** (soft range: 12-17)
- traceability_report.pdf: **≥10 pages** (soft range: 27-47)
- multilayer_report.pdf: **≥15 pages** (soft range: 47-88)

**If page count below hard lower bound**: Source file selection or Pandoc invocation error — verify each input file path and rerun the command.
**If page count outside soft range**: Treat as heuristic — check source Markdown content, verify all files concatenated correctly, then regenerate.

---

### PDF Content Integrity Validation

**Heuristic PDF smoke checks** (useful for catching obviously empty or truncated PDFs, but not authoritative for structured content):
```bash
# Requires pdftotext (from poppler-utils)
echo "=== Content Spot-Checks ==="

# tara_complete.pdf should usually contain asset IDs and threat scenario IDs
ASSET_COUNT=$(pdftotext output/pdf/tara_complete.pdf - 2>/dev/null | grep -c "^AS-" || echo 0)
TS_COUNT=$(pdftotext output/pdf/tara_complete.pdf - 2>/dev/null | grep -c "^TS-" || echo 0)
echo "tara_complete.pdf: $ASSET_COUNT asset IDs, $TS_COUNT threat scenario IDs"
[ "$ASSET_COUNT" -gt 0 ] && [ "$TS_COUNT" -gt 0 ] && echo "✓ Content likely present" || echo "⚠️ Heuristic check failed — verify source Markdown and inspect the PDF manually"

# overall_report.pdf should contain risk-related content
RISK_HITS=$(pdftotext output/pdf/overall_report.pdf - 2>/dev/null | grep -ci "risk" || echo 0)
echo "overall_report.pdf: $RISK_HITS 'risk' mentions"
[ "$RISK_HITS" -gt 5 ] && echo "✓ Content likely present" || echo "⚠️ Heuristic check failed — inspect the PDF manually"

# traceability_report.pdf should contain CSG IDs
CSG_COUNT=$(pdftotext output/pdf/traceability_report.pdf - 2>/dev/null | grep -c "^CSG-" || echo 0)
echo "traceability_report.pdf: $CSG_COUNT CSG IDs"
[ "$CSG_COUNT" -gt 0 ] && echo "✓ CSG content likely present" || echo "⚠️ Heuristic check failed — verify csg.md concatenation and inspect the PDF manually"
```

**Warning**: `pdftotext` extraction order is heuristic. Table layouts, line wraps, and font choices can produce false negatives even when the PDF is correct. Treat these checks as smoke tests only.

**If pdftotext not available**: `sudo apt-get install poppler-utils` or `brew install poppler`.

---

### PDF Metadata Validation

**Check PDF metadata completeness**:
```bash
echo "=== PDF Metadata ==="
for pdf in output/pdf/*.pdf; do
    echo "--- $(basename $pdf) ---"
    pdfinfo "$pdf" | grep -E "Title:|Author:|Subject:|Keywords:|Creator:"
done
```

**Expected metadata fields** (all must be populated):
- Title: Document title (non-empty)
- Author: "Security Team" or configured author
- Subject: Document subject description
- Keywords: "ISO 21434, UN R155, TARA" (or similar)
- Creator: "Pandoc" (tool signature)

**If metadata missing**: Check Pandoc `--metadata` flags in generation commands, regenerate with correct metadata.

---

### Cross-Export Consistency Validation

**Check content consistency between HTML and PDF**:
```bash
# Count sections in Sphinx HTML
HTML_HEADING_COUNT=$(grep -c '<h[1-6]' _build/html/data/ts.html)

# Count sections in source Markdown
MD_HEADING_COUNT=$(grep -c '^#' data/ts.md)

echo "HTML headings: $HTML_HEADING_COUNT"
echo "Markdown headings: $MD_HEADING_COUNT"
echo "Expected: counts similar (±5 due to Sphinx auto-generated headers)"
```

**Manual verification**:
- Open `_build/html/index.html` — Verify all required source files are navigable and attack trees appear only when present
- Open `output/pdf/tara_complete.pdf` — Verify table of contents includes all available source files
- Compare threat counts: HTML vs PDF should show same total threat scenarios

---

## 7. References

**Internal References** (within this skill):
- `references/export-schema.md` — Output format specifications, PDF metadata fields, HTML structure, template variables (400+ lines)
- `references/export-guide.md` — Export methodology, Sphinx setup, PDF workflow, ISO 21434 mapping (300+ lines)
- `assets/CONF_PY_TEMPLATE.py` — Sphinx configuration template with sphinx-book-theme and myst-parser
- `assets/MAKEFILE_TEMPLATE` — Build automation Makefile (html, latexpdf targets)
- `assets/LATEX_PREAMBLE.tex` — PDF styling: fonts, margins, headers, hyperlinks, booktabs tables
- `assets/PDF_FILTERS/README.md` — Audience filter definitions for 4 PDF types

**External Input Files** (from other skills):
- `data/*.md` — 6 data catalogues (from asset_analysis, damage_scenario, threat_scenario, risk_treatment, csg skills)
- `reports/*.md` — 3 reports (from tara_report skill)

**Export Tools**:
- **Pandoc 3.x**: Universal document converter — https://pandoc.org/
  - Documentation: https://pandoc.org/MANUAL.html
  - Installing: https://pandoc.org/installing.html
- **Sphinx 7.x**: Documentation generation engine — https://www.sphinx-doc.org/
  - Usage: https://www.sphinx-doc.org/en/master/usage/index.html
  - Configuration: https://www.sphinx-doc.org/en/master/usage/configuration.html
- **sphinx-book-theme**: PyData ecosystem Material Design theme — https://sphinx-book-theme.readthedocs.io/
  - Configuration options: https://sphinx-book-theme.readthedocs.io/en/stable/customize/index.html
- **myst-parser**: Markdown support for Sphinx — https://myst-parser.readthedocs.io/
  - Syntax guide: https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html
- **LaTeX (pdflatex/xelatex)**: Professional PDF typesetting — https://www.tug.org/texlive/
  - Package documentation: https://ctan.org/

**ISO 21434 Standard**:
- **Clause 8.4**: Work Products — Cybersecurity analysis documentation delivery requirements
- **Clause 8.5**: Documentation — Format and traceability requirements for work products
- **Clause 8.6**: Work Product Quality — Completeness and consistency verification

**Automotive Cybersecurity Standards**:
- **UN R155 (UNECE Regulation 155)**: Cybersecurity and Cybersecurity Management System — Annex 5 documentation requirements
- **UN R156 (UNECE Regulation 156)**: Software Update Management System — Documentation delivery

**Related Skills**:
- `tara_report` skill — Prerequisite: generates reports/*.md from data catalogues

---

## 8. Troubleshooting

### Issue 1: Pandoc Not Found

**Symptom**: Command fails with `pandoc: command not found`

**Root Cause**: Pandoc not installed or not in PATH

**Solution**:
```bash
# Check Pandoc availability
which pandoc

# If missing, install:
# Ubuntu/Debian
sudo apt-get install pandoc

# macOS
brew install pandoc

# Or download from https://pandoc.org/installing.html
```

**Verification**:
```bash
pandoc --version
```

---

### Issue 2: Sphinx Build Fails with "myst_parser not found"

**Symptom**: `sphinx-build` fails with error `Extension error: Could not import extension myst_parser`

**Root Cause**: myst-parser package not installed

**Solution**:
```bash
# Install Sphinx and dependencies
python -m venv .venv
. .venv/bin/activate
pip install sphinx sphinx-book-theme myst-parser

# Verify installation
python -c "import myst_parser; print('myst-parser installed')"
```

**Verification**:
```bash
sphinx-build --version
pip list | grep -E "myst-parser|linkify-it-py"
```

---

### Issue 3: LaTeX Errors During PDF Build

**Symptom**: Pandoc fails with errors like `! LaTeX Error: File 'booktabs.sty' not found`

**Root Cause**: Incomplete LaTeX distribution missing required packages

**Solution**:
```bash
# Install full TeX Live distribution
# Ubuntu/Debian
sudo apt-get install texlive-latex-extra texlive-fonts-recommended

# macOS
brew install --cask mactex

# Or install minimal + packages:
tlmgr install booktabs hyperref fancyhdr geometry titlesec listings xcolor
```

**Verification**:
```bash
pdflatex --version
kpsewhich booktabs.sty
```

---

### Issue 4: PDF Tables Overflow Page Width

**Symptom**: Generated PDF has tables that exceed page margins, text cut off

**Root Cause**: Markdown tables too wide for A4 paper (210mm)

**Solution**:
1. **Option A**: Simplify table (reduce columns, abbreviate headers)
   ```markdown
   # Before (too wide)
   | Threat Scenario ID | Asset | Damage Scenario | Attack Feasibility | Risk Value |
   
   # After (narrower)
   | TS-ID | Asset | Risk Value |
   ```

2. **Option B**: Use landscape orientation for wide tables (edit LATEX_PREAMBLE.tex):
   ```latex
   \usepackage{pdflscape}
   % Then wrap wide tables with \begin{landscape}...\end{landscape}
   ```

3. **Option C**: Split table into multiple sub-tables

**Verification**: Open PDF, check table columns fit within margins

---

### Issue 5: Sphinx HTML Search Not Working

**Symptom**: Search bar in HTML site returns no results

**Root Cause**: Search index not generated or JavaScript disabled

**Solution**:
```bash
# Verify search index exists
test -f _build/html/searchindex.js && echo "✓ Index present" || echo "⚠️ Index missing"

# If missing, rebuild with search enabled
sphinx-build -b html docs/sphinx _build/html

# Verify searchindex.js generated
ls -lh _build/html/searchindex.js
```

**Manual test**: Open `_build/html/index.html` in browser, type "threat" in search bar, verify results appear.

---

### Issue 6: PDF Bookmarks Not Showing

**Symptom**: PDF opens without navigation bookmarks in left pane

**Root Cause**: Missing `--toc` or `--number-sections` flags in Pandoc command

**Solution**:
```bash
# Regenerate PDF with TOC flags
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  --include-in-header=LATEX_PREAMBLE.tex \
  --metadata title="Title" \
  --toc \
  --toc-depth=3 \
  --number-sections
```

**Verification**: Open PDF in Adobe Reader or Preview, verify bookmark navigation pane shows chapter hierarchy.

---

### Issue 7: Internal Links Broken in HTML

**Symptom**: Clicking link in Sphinx HTML shows "404 Page Not Found"

**Root Cause**: Incorrect toctree paths or missing files

**Solution**:
```bash
# Check toctree in index.rst/index.md
cat docs/sphinx/index.rst

# Verify all referenced files exist
test -f docs/sphinx/data/ts.md && echo "✓ ts.md" || echo "⚠️ Missing ts.md"

# Check file extension consistency (.md vs .rst)
ls docs/sphinx/data/

# Rebuild with warnings visible
sphinx-build -W -b html docs/sphinx _build/html
```

**Fix**: Update toctree paths to match actual file locations, rebuild.

---

### Issue 8: "Can I modify exported HTML/PDF files directly?"

**Symptom**: User wants to manually edit HTML or PDF after export

**Answer**: **NO. Never manually edit exported outputs.**

**Rationale**:
- Exported outputs are **derived artifacts** generated from source Markdown (data/ + reports/)
- Manual edits are lost when exports are regenerated (which happens after any source file update)
- Manual edits break reproducibility (ISO 21434 Clause 8.4 requires traceability)
- Audit trail broken (cannot verify output matches source)

**Correct workflow**:
1. Identify what needs to change (e.g., risk values, threat descriptions, report text)
2. Update source Markdown files:
   - Risk data: Update `data/ts.md`, `data/rt.md`
   - Report content: Regenerate via `tara_report` skill
   - Styling: Update templates in `skills/tara_export/assets/`
3. Re-export from updated source
4. Distribute regenerated output (with traceability intact)

**Exception**: If you need custom styling (fonts, colors), modify templates in `assets/` directory, not the exported output.

---

*End of TARA Export Skill Workflow*
