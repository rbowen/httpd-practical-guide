# Apache Cookbook

Solutions and examples for Apache HTTP Server administrators, by [Rich Bowen](https://github.com/rbowen) and Ken Coar.

This book covers the full range of Apache httpd administration — installation, virtual hosts, URL mapping, mod_rewrite, authentication, SSL/TLS, proxying, performance tuning, logging, security, dynamic content, and much more — in a practical recipe-based format.

## Status

This is a **work in progress** (v4.0.0). See the appendix for revision history and the TODO list.

Found a bug, typo, or have a suggestion? [File an issue](https://github.com/rbowen/apache_cookbook/issues).

## Building

The book is written in [reStructuredText](https://docutils.sourceforge.io/rst.html) and built with [Sphinx](https://www.sphinx-doc.org/). No global install required — use [uv](https://docs.astral.sh/uv/) to run in an ephemeral environment:

### Prerequisites

**Required (for HTML and ePub):**

- **Python 3.8+**
- **[uv](https://docs.astral.sh/uv/)** (recommended) — or install Sphinx globally with `pip install sphinx`

**Optional (for PDF output only):**

- A **LaTeX distribution** with `latexmk` and `pdflatex`:

  | OS | Install command |
  |---|---|
  | macOS | `brew install mactex-no-gui` |
  | Debian / Ubuntu | `sudo apt install texlive-full latexmk` |
  | Fedora / RHEL | `sudo dnf install texlive-scheme-full latexmk` |
  | Arch | `sudo pacman -S texlive-most latexmk` |
  | Windows | Install [MiKTeX](https://miktex.org/) or [TeX Live](https://tug.org/texlive/) |

**Optional (for Kindle output):**

- **[Calibre](https://calibre-ebook.com/)** — provides `ebook-convert` for ePub → azw3 conversion:
  - macOS: `brew install calibre`
  - Other platforms: [download from calibre-ebook.com](https://calibre-ebook.com/download)

If LaTeX is not installed, `build.sh` will still generate HTML and ePub successfully and skip the PDF step.

**Installing uv:**

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### HTML

```bash
uv run --with sphinx -- sphinx-build -b html -d _build/doctrees . _build/html
```

Open `_build/html/index.html` in your browser to view.

### ePub

```bash
uv run --with sphinx -- sphinx-build -b epub -d _build/doctrees . _build/epub
```

The ePub file will be at `_build/epub/Apache Cookbook.epub`.

### PDF (via LaTeX)

```bash
uv run --with sphinx -- sphinx-build -b latex -d _build/doctrees . _build/latex
cd _build/latex && make
```

The PDF will be at `_build/latex/apache_cookbook.pdf`.

### Using Make

If you have Sphinx installed globally (or in a virtualenv), you can use the Makefile shortcuts:

```bash
make html
make epub
make latexpdf
make linkcheck   # verify external links
make clean       # remove all build output
```

### All formats

```bash
./build.sh
```

This cleans the output directory and builds HTML, ePub, and PDF in one go.

## Structure

```
├── conf.py                 — Sphinx configuration
├── index.rst               — Master table of contents
├── build.sh                — Build all formats (HTML, ePub, PDF)
├── Makefile                — Build targets
├── images/                 — Figures and screenshots
└── chapters/
    ├── 00_preface.rst
    ├── 01_installation.rst     — Getting Started
    ├── 02_first_website.rst    — Your First Website
    ├── 03_common_modules.rst   — Common Modules
    ├── 04_logging.rst          — Logging
    ├── 05_virtual_hosts.rst    — Virtual Hosts
    ├── 06_url_mapping.rst      — URL Mapping
    ├── 07_regex.rst            — Regular Expressions
    ├── 08_mod_rewrite.rst      — mod_rewrite
    ├── 09_authentication.rst   — Authentication
    ├── 10_security.rst         — Security
    ├── 11_ssl_tls.rst          — SSL/TLS
    ├── 12_dynamic_content.rst  — Dynamic Content (CGI, SSI, etc.)
    ├── 13_troubleshooting.rst  — Troubleshooting
    ├── 14_proxies.rst          — Proxies and Gatewaying
    ├── 15_performance.rst      — Performance
    ├── 16_directory_listing.rst— Directory Listing
    ├── 17_contributing.rst     — Contributing to Apache httpd
    ├── 18_filters_handlers.rst — Filters and Handlers
    ├── 19_htaccess.rst         — .htaccess Files
    ├── 20_user_directories.rst — User Directories
    ├── 21_programmable_config.rst — Programmable Configuration
    ├── 22_mod_info_status.rst  — mod_info and mod_status
    ├── 23_puppet.rst           — Puppet
    ├── appendix.rst            — Revision History / TODO
    ├── appendix_b.rst          — Additional Resources
    └── glossary.rst
```

## Edition History

- **1st Edition** (2003) — Originally published by O'Reilly Media, covering Apache 2.0
- **2nd Edition** (2004) — O'Reilly Media, covering Apache 2.2
- **3rd Edition** (2014) — O'Reilly Media (AsciiDoc), covering Apache 2.4
- **4th Edition** (2026) — Self-published (Sphinx/RST), covering Apache 2.4+
- **4th Edition** (2026) — reStructuredText / Sphinx, covering Apache 2.4.x / 2.5+

## License

Copyright © 2004–2026 Rich Bowen and Ken Coar.

All rights reverted to the author. Licensed under the [Apache License, Version 2.0](LICENSE). See the LICENSE file for details.
