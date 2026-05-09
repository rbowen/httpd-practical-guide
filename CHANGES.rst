Changes


0.3 — 2026-05-09
-----------------

Major content overhaul.

* Full rewrite of Chapter 04 (Logging): JSON/structured logging,
  mod_journald, piped logging, systemd journal, mod_log_debug,
  request timing. First 3 recipes reframed as reference prose.
* Full rewrite of Chapter 15 (Performance): Event MPM tuning, HTTP/2,
  mod_brotli, mod_cache/mod_expires, h2load benchmarking. Removed
  dated content (mod_perl, mod_dialup, Nikto).
* Full rewrite of Chapter 17 (Contributing): Reframed from recipes to
  flowing narrative. Updated IRC→Slack, ApacheCon→Community Over Code.
* New Chapter 23: Automated Deployment (Ansible, Puppet, Chef,
  Docker/Podman, Terraform/OpenTofu)
* New Chapter 24: Module Reference (63 modules cataloged by category)
* Inserted Windows "Starting httpd at boot" recipe into Chapter 01
* Fixed section header hierarchy in Chapter 09 (Authentication)
* Removed orphan Chapter 13 (Troubleshooting) — already excluded from toctree
* Deleted old Chapter 23 (Puppet) stub
* Fixed 18 broken cross-references across 10 files
* Fixed Unicode U+2212 minus sign causing LaTeX build failure
* Updated "How This Book Is Organized" in preface
* All http:// links in Contributing chapter converted to https://
* Clean build: 0 errors, 0 warnings (HTML + LaTeX), 780 pages PDF


0.1 — 2026-04-25
-----------------

First working draft of the 4th edition.

* Converted from AsciiDoc (3rd edition) to reStructuredText/Sphinx
* Restructured into 7 Parts (Getting Started, Core Configuration,
  URL Rewriting, Security and Access Control, Dynamic Content and
  Proxying, Performance and Operations, Advanced Topics)
* Removed Puppet chapter (Ch23)
* Condensed mod_rewrite chapter to essentials — full coverage in
  companion book *mod_rewrite And Friends*
* Trimmed Programmable Configuration chapter — expression parser
  content moved to companion book
* Removed Bitnami Windows install recipes (Bitnami discontinued)
* Updated all Freenode references to Libera Chat
* Updated SVN references to Git
* Fixed 200+ Sphinx build errors/warnings
* Cleaned up AsciiDoc conversion artifacts (raw HTML, passthrough blocks)
* Configured for KDP 6×9 paperback format
* Added 15 new module coverage recipe drafts
* Single author (Rich Bowen) — Ken Coar credited for earlier editions
