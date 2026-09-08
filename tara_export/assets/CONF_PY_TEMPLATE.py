# Configuration file for Sphinx documentation builder
# For full list of options: https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

from pathlib import Path

project = "{{PROJECT_NAME}}"
copyright = "{{COPYRIGHT_YEAR}}, {{COPYRIGHT_HOLDER}}"
author = "{{AUTHOR_NAME}}"
version = "{{VERSION}}"
release = "{{RELEASE}}"

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",  # Markdown support
]

# MyST-Parser configuration
myst_enable_extensions = [
    "deflist",  # Definition lists
    "colon_fence",  # Colon-fenced code blocks
    "substitution",  # Variable substitution
]

# Source file suffixes
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# The master doc (entry point)
master_doc = "index"

# Language for content autogeneration
language = "en"

# List of patterns to exclude from source files
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_book_theme"

html_theme_options = {
    "show_toc_level": 2,
    "navigation_with_keys": True,
}

repository_url = "{{REPOSITORY_URL}}"
if not repository_url.startswith("{{"):
    html_theme_options["repository_url"] = repository_url

html_title = project if "{{HTML_TITLE}}".startswith("{{") else "{{HTML_TITLE}}"
html_short_title = project if "{{HTML_SHORT_TITLE}}".startswith("{{") else "{{HTML_SHORT_TITLE}}"

favicon_path = "{{FAVICON_PATH}}"
if not favicon_path.startswith("{{") and Path(favicon_path).exists():
    html_favicon = favicon_path

# Static files (CSS, JS, images)
html_static_path = ["_static"] if Path("_static").exists() else []

# Custom CSS files
html_css_files = [
    # Add custom CSS here if needed
]

# -- Options for LaTeX output ------------------------------------------------

latex_engine = "xelatex"

latex_preamble_file = "{{LATEX_PREAMBLE_FILE}}"
latex_preamble = ""
if not latex_preamble_file.startswith("{{"):
    preamble_path = Path(latex_preamble_file)
    if not preamble_path.is_absolute():
        preamble_path = (Path(__file__).parent / preamble_path).resolve()
    if preamble_path.exists():
        latex_preamble = preamble_path.read_text()
    else:
        latex_preamble = f"\n\\input{{{latex_preamble_file}}}\n"

latex_elements = {
    "papersize": "a4paper",
    "pointsize": "11pt",
    "preamble": latex_preamble,
    "figure_align": "htbp",
}

# LaTeX document structure
latex_documents = [
    (master_doc, "{{PDF_FILENAME}}.tex", "{{PDF_TITLE}}", "{{PDF_AUTHOR}}", "manual"),
]

# -- Options for manual page output ------------------------------------------

man_pages = [
    (master_doc, "{{PROJECT_SLUG}}", "{{PROJECT_NAME}} Documentation", [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------

texinfo_documents = [
    (
        master_doc,
        "{{PROJECT_SLUG}}",
        "{{PROJECT_NAME}} Documentation",
        author,
        "{{PROJECT_SLUG}}",
        "{{PROJECT_DESCRIPTION}}",
        "Miscellaneous",
    ),
]
