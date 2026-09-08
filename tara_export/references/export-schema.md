# TARA Export Schema - Output Format Specifications

This document defines the output format specifications for Sphinx HTML documentation and audience-specific PDF reports generated from TARA Markdown content, aligned with ISO 21434:2021 Clause 8.4 (Work Products) publication requirements.

---

## Overview

The TARA export framework produces two primary output types:

1. **Sphinx HTML Documentation** - Browseable website with 8 required source files and optional attack-tree content
2. **PDF Reports** - Four audience-filtered PDFs with custom styling

---

## Sphinx HTML Output

### Purpose

The Sphinx HTML output provides a browseable, searchable documentation website for internal team access and stakeholder self-service.

**ISO 21434 Alignment**: Clause 8.4 - Communication of cybersecurity work products

### Output Structure

```
_build/html/
├── index.html                    Homepage (navigation entry point)
├── data/                         Data catalogue pages (5 required + optional attack-tree file)
│   ├── asset_list.html
│   ├── ds.html
│   ├── ts.html
│   ├── at.html                   Optional, generated only if `data/at.md` exists
│   ├── rt.html
│   └── csg.html
├── reports/                      Report pages (3 files)
│   ├── overall_report.html
│   ├── traceability_report.html
│   └── multilayer_report.html
├── _static/                      Theme assets (CSS, JS, images)
│   ├── sphinx_book_theme/        sphinx-book-theme files
│   ├── css/                      Custom stylesheets
│   └── js/                       Custom scripts
├── _sources/                     RST source files (for reference)
│   ├── data/
│   └── reports/
├── search.html                   Full-text search interface
├── genindex.html                 Generated index (if enabled)
└── objects.inv                   Intersphinx inventory (for cross-refs)
```

### HTML Metadata

| Field | Location | Format | Description |
|-------|----------|--------|-------------|
| **Page Title** | `<title>` tag | String | Document title (derived from Markdown H1) |
| **Site Title** | Header | String | Project name (from conf.py: `html_title`) |
| **Copyright** | Footer | String | Copyright year and holder |
| **Last Updated** | Footer | ISO 8601 datetime | Build timestamp |
| **Theme** | `<link>` tag | sphinx-book-theme | PyData ecosystem Material Design theme |
| **Generator** | `<meta>` tag | Sphinx version | E.g., "Sphinx 7.2.6" |

### Navigation Features

| Feature | Implementation | Description |
|---------|----------------|-------------|
| **Sidebar TOC** | Left panel | Hierarchical navigation (2 levels deep) |
| **Breadcrumbs** | Top bar | Current page path |
| **Search** | Search bar | Full-text search across all pages |
| **Previous/Next** | Bottom buttons | Sequential page navigation |
| **Repository Link** | Header button | Link to source repo (if configured) |
| **Download PDF** | Header button | Link to PDF download (if enabled) |

### Styling Specifications

| Element | Styling | Source |
|---------|---------|--------|
| **Color Scheme** | Material Design palette | sphinx-book-theme defaults |
| **Typography** | System fonts (sans-serif) | sphinx-book-theme |
| **Code Blocks** | Syntax highlighting | Pygments (via Sphinx) |
| **Tables** | Responsive, zebra striping | sphinx-book-theme CSS |
| **Links** | Blue, underline on hover | sphinx-book-theme |
| **Headers** | Hierarchical sizing (H1-H6) | sphinx-book-theme |

### Accessibility

| Feature | Standard | Implementation |
|---------|----------|----------------|
| **Semantic HTML** | WCAG 2.1 AA | Sphinx generates semantic tags |
| **Keyboard Navigation** | WCAG 2.1 AA | Tab order, focus indicators |
| **Screen Reader** | WCAG 2.1 AA | ARIA labels, alt text |
| **Color Contrast** | WCAG 2.1 AA | sphinx-book-theme compliant |

---

## PDF Output

### Purpose

The PDF outputs provide printable, archivable reports for stakeholder distribution, compliance submission, and long-term record-keeping.

**ISO 21434 Alignment**: Clause 8.4 - Cybersecurity work products in auditable format

### PDF Types and Content Filters

#### 1. tara_complete.pdf

**Target Audience**: Internal archive  
**Content**: All 8 required source files + optional `data/at.md`

| Section | Source File | Pages (est.) |
|---------|-------------|--------------|
| Title Page | Generated | 1 |
| Table of Contents | Generated | 2-3 |
| Asset Catalogue | data/asset_list.md | 5-10 |
| Damage Scenarios | data/ds.md | 10-20 |
| Threat Scenarios | data/ts.md | 20-40 |
| Attack Trees | data/at.md (optional) | 10-20 |
| Risk Treatments | data/rt.md | 10-20 |
| Cybersecurity Goals | data/csg.md | 10-20 |
| Overall Report | reports/overall_report.md | 10-15 |
| Traceability Report | reports/traceability_report.md | 15-25 |
| Multi-layer Report | reports/multilayer_report.md | 15-25 |

**Estimated Total**: Usually 100-200 pages, depending on input size and PDF engine

---

#### 2. overall_report.pdf

**Target Audience**: Executives, customers  
**Content**: Executive summary only

| Section | Source File | Pages (est.) |
|---------|-------------|--------------|
| Title Page | Generated | 1 |
| Table of Contents | Generated | 1 |
| Overall Report | reports/overall_report.md | 10-15 |

**Estimated Total**: 12-17 pages

---

#### 3. traceability_report.pdf

**Target Audience**: Audit agencies (ISO 21434, UN R155)  
**Content**: Traceability matrix + CSG summary

| Section | Source File | Pages (est.) |
|---------|-------------|--------------|
| Title Page | Generated | 1 |
| Table of Contents | Generated | 1 |
| Traceability Report | reports/traceability_report.md | 15-25 |
| Cybersecurity Goals | data/csg.md | 10-20 |

**Estimated Total**: 27-47 pages

---

#### 4. multilayer_report.pdf

**Target Audience**: Internal project team  
**Content**: Technical architecture + threat data

| Section | Source File | Pages (est.) |
|---------|-------------|--------------|
| Title Page | Generated | 1 |
| Table of Contents | Generated | 1-2 |
| Multi-layer Report | reports/multilayer_report.md | 15-25 |
| Threat Scenarios | data/ts.md | 20-40 |
| Attack Trees | data/at.md (optional) | 10-20 |

**Estimated Total**: Usually 47-88 pages, depending on input size and whether `data/at.md` is present

---

### PDF Metadata

| Field | Format | Source | Description |
|-------|--------|--------|-------------|
| **Title** | String | Template variable | Document title (e.g., "TARA Complete Archive") |
| **Author** | String | Template variable | Organization name |
| **Subject** | String | Fixed | "Automotive Cybersecurity TARA" |
| **Keywords** | CSV string | Fixed | "ISO 21434, UN R155, Threat Analysis, Risk Assessment" |
| **Creator** | String | Tool name | "Pandoc 3.x + LaTeX" |
| **Producer** | String | Tool name | "pdflatex" or "xelatex" |
| **Creation Date** | PDF Date format | Build timestamp | E.g., "D:20260325143000+00'00'" |
| **Modification Date** | PDF Date format | Build timestamp | Same as creation date |

### Page Layout

| Element | Specification | Source |
|---------|---------------|--------|
| **Paper Size** | A4 (210mm × 297mm) | LATEX_PREAMBLE.tex |
| **Margins** | Top: 30mm, Bottom: 30mm, Left: 25mm, Right: 25mm | LATEX_PREAMBLE.tex |
| **Orientation** | Portrait (default) | LATEX_PREAMBLE.tex |
| **Header** | Left: Section title, Right: Static "TARA Documentation" label | LATEX_PREAMBLE.tex (fancyhdr) |
| **Footer** | Center: Page number | LATEX_PREAMBLE.tex (fancyhdr) |
| **Line Spacing** | 1.15 (default LaTeX article) | LATEX_PREAMBLE.tex |

### Typography

| Element | Specification | Source |
|---------|---------------|--------|
| **Body Font** | Computer Modern (LaTeX default) | pdflatex |
| **Body Size** | 11pt | conf.py (latex_elements) |
| **Heading Fonts** | Builder defaults | Pandoc / LaTeX engine |
| **Code Font** | Monospace (Courier) | LATEX_PREAMBLE.tex (listings) |
| **Code Size** | 9pt (small) | LATEX_PREAMBLE.tex (listings) |

### Styling Elements

| Element | Specification | Package |
|---------|---------------|---------|
| **Hyperlinks** | Blue, clickable | hyperref (LATEX_PREAMBLE.tex) |
| **Internal Links** | Blue, cross-ref to sections | hyperref |
| **External Links** | Cyan, underlined | hyperref |
| **Code Blocks** | Gray background, line numbers | listings (LATEX_PREAMBLE.tex) |
| **Tables** | Professional booktabs formatting | booktabs (LATEX_PREAMBLE.tex) |
| **Table of Contents** | Controlled by Pandoc CLI (`--toc`, `--toc-depth`) | Pandoc command |
| **Section Numbering** | Controlled by Pandoc CLI (`--number-sections`) | Pandoc command |
| **Bookmarks** | PDF navigation pane | hyperref |

### Table of Contents

| Level | Element | Numbering |
|-------|---------|-----------|
| 1 | Section | 1, 2, 3, ... |
| 2 | Subsection | 1.1, 1.2, 1.3, ... |
| 3 | Subsubsection | 1.1.1, 1.1.2, ... |

### PDF Bookmarks

PDF bookmarks mirror the table of contents for navigation:
- Level 1: Sections (`#` in Markdown)
- Level 2: Subsections (`##` in Markdown)
- Level 3: Subsubsections (`###` in Markdown)

---

## Output Validation

### HTML Validation

| Check | Tool | Pass Criteria |
|-------|------|---------------|
| **W3C HTML5** | https://validator.w3.org/ | Zero errors |
| **Broken Links** | Sphinx linkcheck | Zero broken links |
| **Search Index** | Manual test | Search returns results |
| **Responsive Design** | Browser DevTools | Renders on mobile/tablet/desktop |

### PDF Validation

| Check | Tool | Pass Criteria |
|-------|------|---------------|
| **PDF/A Compliance** | veraPDF | PDF/A-1b or PDF/A-2b (optional) |
| **Metadata Completeness** | pdfinfo | All required fields populated |
| **Bookmarks** | PDF reader | All sections bookmarked |
| **Hyperlinks** | PDF reader | Internal/external links work |
| **Table Rendering** | Visual inspection | No overflow, aligned columns |
| **Code Block Readability** | Visual inspection | Monospace font, readable size |

---

## ISO 21434 Compliance Mapping

| ISO 21434 Clause | Export Requirement | Implementation |
|---|---|---|
| 8.4 (Work Products) | Communicate cybersecurity analysis | Sphinx HTML + 4 PDFs |
| 8.5 (Documentation) | Maintain traceability | Traceability report with cross-refs |
| 8.6 (Work Product Quality) | Ensure completeness and consistency | Validation checks, automated build |
| 15.11 (Traceability) | Document traceability matrix | traceability_report.pdf |

---

## Template Variables

### Sphinx conf.py Placeholders

| Placeholder | Example Value | Description |
|-------------|---------------|-------------|
| `{{PROJECT_NAME}}` | "TaraOK TARA Documentation" | Project display name |
| `{{COPYRIGHT_YEAR}}` | "2026" | Copyright year |
| `{{COPYRIGHT_HOLDER}}` | "Automotive OEM Inc." | Copyright holder |
| `{{AUTHOR_NAME}}` | "Security Team" | Author name |
| `{{VERSION}}` | "1.0" | Short version (X.Y) |
| `{{RELEASE}}` | "1.0.0" | Full version (X.Y.Z) |
| `{{REPOSITORY_URL}}` | "https://github.com/org/repo" | Source repo URL |
| `{{HTML_TITLE}}` | "TARA Documentation" | HTML site title |
| `{{HTML_SHORT_TITLE}}` | "TARA" | Short title for nav |
| `{{FAVICON_PATH}}` | "_static/favicon.ico" | Path to favicon |
| `{{LATEX_PREAMBLE_FILE}}` | "../../skills/tara_export/assets/LATEX_PREAMBLE.tex" | LaTeX preamble file used only by the Sphinx LaTeX builder |
| `{{PDF_FILENAME}}` | "tara_complete" | Output PDF filename (no .pdf) |
| `{{PDF_TITLE}}` | "TARA Complete Archive" | PDF document title |
| `{{PDF_AUTHOR}}` | "Security Team" | PDF author field |
| `{{PROJECT_SLUG}}` | "taraok" | URL-safe project name |
| `{{PROJECT_DESCRIPTION}}` | "Automotive Cybersecurity TARA" | Short description |

### LaTeX Preamble

`assets/LATEX_PREAMBLE.tex` is static. PDF metadata should be supplied by Pandoc CLI flags such as `--metadata title=...` and `--metadata author=...`.

---

## References

- **Sphinx HTML Output**: https://www.sphinx-doc.org/en/master/usage/builders/index.html#sphinx.builders.html.StandaloneHTMLBuilder
- **sphinx-book-theme Documentation**: https://sphinx-book-theme.readthedocs.io/en/stable/
- **PDF Metadata Standard**: ISO 32000-1:2008 (PDF 1.7)
- **LaTeX Package Documentation**:
  - geometry: https://ctan.org/pkg/geometry
  - hyperref: https://ctan.org/pkg/hyperref
  - fancyhdr: https://ctan.org/pkg/fancyhdr
  - booktabs: https://ctan.org/pkg/booktabs
- **ISO 21434:2021**: Clause 8.4 (Work Products), Clause 8.5 (Documentation)
