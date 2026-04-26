
### 🔴 Windows "Starting httpd at Boot" recipe — likely wrong
- [ ] The Windows service installation recipe may be incorrect for modern Windows
- [ ] No Windows machine available for verification
- [ ] Research: what is the current correct way to install httpd as a Windows service?
- [ ] Consider: is Windows coverage worth maintaining at all, or should we stub it out?

### 🔴 Ch15 Performance — likely needs major overhaul
- [ ] "Caching Frequently Viewed Files" and "Caching Dynamic Content" are dated
- [ ] Zero mod_cache/mod_cache_disk/mod_expires coverage (top ML demand topic)
- [ ] mod_dialup recipe is essentially empty stub
- [ ] Nikto recipe is misplaced — move to Ch10 Security
- [ ] Missing: HTTP/2 performance, Event MPM tuning (modern), compression
  (mod_brotli), security headers (HSTS, CSP, CORS)
- [ ] mod_ratelimit recipe may be fine but review for accuracy
- [ ] Draft caching recipes already generated (recipes_caching.rst in artifacts)
- [ ] Consider: is this chapter better split into "Performance Tuning" + "Testing"?


## Version Numbering

We use **x.y** format (not x.y.z). Bump the version in ALL THREE places:
1. `conf.py` — `release` and `version`
2. `README.md` — status line
3. `CHANGES.rst` — revision history entry (when created)

**Target**: Publish 4th edition within 1–2 weeks (by ~May 9, 2026)
**Updated**: 2026-04-25

## 🔴 Rename Git Repo (BEFORE PUBLISH)

The repo is currently `httpd-practical-guide`. "Apache Cookbook" is a trademark of
O'Reilly Media from the original editions. We need a new repo name before
going public. Candidates:
- `apache-httpd-guide`, `practical-httpd`, `httpd-practical-guide`
- Must also update `conf.py` `html_theme_options.github_repo`, README, any CI config

---

## Version Convention (IMPORTANT)

Most readers run httpd **2.4.x** (the stable release branch). Features that
only exist in trunk (future 2.6/3.0) MUST be clearly marked using the
`:version:` inline role:

- `:version:`2.4.48`` — available in 2.4 stable (rounded green pill)
- `:version:`trunk`` — trunk only, not yet released (dashed orange border)

**Rules:**
1. Every recipe/directive that is trunk-only MUST have a `:version:`trunk`` badge
2. If a directive was added in a specific 2.4.x minor, use `:version:`2.4.xx``
3. Recipes for trunk-only modules need a clear warning at the top:
   `.. warning:: This module is only available in httpd trunk (unreleased).`
4. When a trunk feature lands in a 2.4 release, update the badge
5. The module coverage audit (`module_coverage_audit.md`) flags 10 trunk-only
   modules — these need special treatment

---

## 🔴 Build Errors (153 issues as of Apr 25, 2026)

Baseline build: 75 errors, 78 warnings (HTML), 0 errors/27 warnings (LaTeX).
Three parallel fix tasks launched Apr 25 — check results and re-run build.

### Empty `.. todo::` directives (34 errors) — 🔄 FIX IN PROGRESS
- 30 in `23_puppet.rst`, 1 each in Ch10, Ch12, Ch13, Ch15
- Fix: add placeholder text to each empty directive

### AsciiDoc `+++` passthrough blocks (20 errors) — 🔄 FIX IN PROGRESS
- Raw HTML `<pre>/<strong>/<code>` blocks from AsciiDoc conversion
- Files: 10_security (2), 11_ssl_tls (8), 12_dynamic_content (2),
  13_troubleshooting (7), 14_proxies (3)
- Fix: convert to `.. code-block::` with appropriate language

### Unexpected section titles (9 errors) — 🔄 FIX IN PROGRESS
- AsciiDoc-era admonition titles (`.TitleText\n====`) inside discussions
- Files: 04_logging (4), 12_dynamic_content (4), 14_proxies (1)
- Fix: convert to bold text or `.. note::` admonitions

### Broken `:ref:` cross-references (26 warnings) — 🔄 FIX IN PROGRESS
- Labels (`.. _label:`) not followed by a heading with underline
- Files: 04_logging (3), 05_virtual_hosts (9+), 08_mod_rewrite (1),
  09_authentication (2), 10_security (1), 13_troubleshooting (2),
  14_proxies (1), 15_performance (2), 19_htaccess (2),
  21_programmable_config (2), 23_puppet (1)
- Fix: add heading underlines after labels

### Inline markup issues (23 issues) — 🔄 FIX IN PROGRESS
- [ ] Unmatched `` `` `` (9): Ch01:2105, Ch02:1406, Ch08:130+533,
  Ch16:1610+1633, Ch19:555, Ch21:192+200+239
- [ ] Unmatched `**` (4): Ch05:320, Ch23:71+79+87
- [ ] Unmatched `*` (2): Ch05:86, Ch11:1004
- [ ] Empty `.. sidebar::` (2): Ch09:91+2958
- [ ] Unreferenced footnote: Ch08:3731
- [ ] Malformed hyperlink: Ch13:397
- [ ] Inline interpreted text: Ch19:93
- [ ] Unknown target: Ch20:166
- [ ] Unexpected indentation: Ch23:96
- [ ] Code block language mismatch: Ch12:851

### Title underline issues (10 warnings)
- Short underlines: Ch04 (4), Ch12 (2), Ch13 (4)
- Fix: extend underlines to match title length

### Inconsistent title styles (6 errors)
- Wrong heading hierarchy character
- Files: Ch11 (4), Ch13 (2)

### Missing blank lines (17 warnings)
- After bullet lists (9), block quotes (4), definition lists (2),
  enumerated lists (2)

### Malformed table (1 error)
- `02_first_website.rst:1114` — Options directive reference table

### Overline too short (4 warnings)
- `13_troubleshooting.rst`: 278, 420, 874, 1191

---

## 🟡 Legacy / 3e Content (661 artifacts)

Content from the 3rd edition (2014) that needs updating or removing.
Scan ran Apr 25, 2026.

### AsciiDoc `----` horizontal rules (309 instances)
- Every chapter except the preface
- Most are section separators — review each; remove noise, keep intentional breaks

### Raw HTML in RST (140 instances)
- `<code>` (72), `<strong>` (42), `<pre>` (26)
- Worst files: Ch11 (67), Ch13 (45), Ch10 (18)
- Most are inside `+++` passthrough blocks (fix in progress above)

### AsciiDoc `_italic_` patterns (65 instances)
- Underscore-style italic from AsciiDoc
- Worst files: Ch04 (36), Ch11 (9), Ch01 (8), Ch14 (6)
- Review each — some are legit file paths, many need → `*italic*`

### AsciiDoc `++++` delimiters (48 instances)
- Being fixed by passthrough cleanup task

### AsciiDoc `//` comments (37 instances)
- Ch10 (30), Ch15 (4), Ch13 (2), Ch12 (1)
- Convert to `.. todo::` directives or delete

### 🔴 Apache 2.2 references (27 instances) — MUST FIX BEFORE PUBLISH
- [ ] Ch09 (7) — auth syntax differences
- [ ] Ch04 (3) — logging changes
- [ ] Ch05 (3) — virtual host changes
- [ ] Ch10 (3) — access control
- [ ] Ch08 (2) — mod_rewrite changes
- [ ] Ch15 (2) — performance tuning
- [ ] Scattered (7): Ch03, Ch06, Ch17, Ch19, Ch20, appendix
- Review each: update to 2.4 syntax, remove 2.2-specific content,
  or add a migration note where appropriate

### 🔴 Bitnami references (24 instances) — MUST FIX BEFORE PUBLISH
- ALL in Ch01 (installation) — Windows install recipe
- Bitnami is no longer the standard way to install on Windows
- **Decision needed**: rewrite for Apache Lounge, or stub out Windows
  with a pointer to Apache Lounge downloads

### 🔴 O'Reilly references (11 instances) — MUST FIX BEFORE PUBLISH
- [ ] `00_preface.rst` (3) — publisher references
- [ ] `01_installation.rst:155` — catalog URL
- [ ] `02_first_website.rst:352,418,1647,1660` — shop/search URLs
- [ ] `06_url_mapping.rst` (1)
- [ ] `11_ssl_tls.rst` (1)
- [ ] `15_performance.rst` (2)
- [ ] `22_mod_info_status.rst:1101` — shop URL
- [ ] `appendix.rst` (3)
- Remove dead URLs, update publisher references to "self-published"

### 🔴 modules.apache.org retired — MUST FIX BEFORE PUBLISH
- [ ] Ch03 (Common Modules) references modules.apache.org which has been retired
- [ ] Investigate: how many third-party httpd module projects exist on GitHub?
- [ ] Replace modules.apache.org references with guidance on searching GitHub
  (e.g., `topic:apache-httpd-module`, `apache httpd module` search)
- [ ] Consider: is there a successor registry, or is GitHub the de facto home now?

---

## 🟢 Module Coverage Gaps — 15 HIGH Priority

Recipe drafts generated Apr 25, 2026 (in workspace/artifacts/).
Each needs review, editing, and insertion into the target chapter.

### Ch14: Proxies (2 modules)
- [ ] `mod_proxy_fcgi` — FastCGI proxy / PHP-FPM (draft: recipe_mod_proxy_fcgi.rst)
- [ ] `mod_proxy_wstunnel` — WebSocket tunneling (draft: recipe_mod_proxy_wstunnel.rst)

### Ch15: Performance (3 modules)
- [ ] `mod_cache` — HTTP content caching (draft: recipes_caching.rst)
- [ ] `mod_cache_disk` — disk-based cache storage (draft: recipes_caching.rst)
- [ ] `mod_expires` — expiration headers (draft: recipes_caching.rst)

### Ch09: Authentication (5 modules)
- [ ] `mod_access_compat` — 2.2→2.4 migration (draft: recipes_auth_infrastructure.rst)
- [ ] `mod_authn_core` — auth provider architecture (draft: recipes_auth_infrastructure.rst)
- [ ] `mod_authz_user` — Require user/valid-user (draft: recipes_auth_infrastructure.rst)
- [ ] `mod_ldap` — LDAP connection pooling (draft: recipes_auth_infrastructure.rst)
- [ ] `mod_socache_shmcb` — shared object cache (draft: recipes_auth_infrastructure.rst)

### Ch12: Dynamic Content (2 modules)
- [ ] `mod_cgid` — CGI with threaded MPMs (draft: recipes_dynamic_content.rst)
- [ ] `mod_env` — environment variables (draft: recipes_dynamic_content.rst)

### Ch01: Installation (1 module)
- [ ] `mod_systemd` — systemd integration (draft: recipe_mod_systemd.rst)

### Ch10: Security (1 module)
- [ ] `mod_reqtimeout` — Slowloris protection (draft: recipe_mod_reqtimeout.rst)

### Ch21: Programmable Config (1 module)
- [ ] `mod_version` — version-conditional config (draft: recipe_mod_version.rst)

---

## Content Work

- [ ] Identify recipes that are in the wrong chapter, or which
  overlap/duplicate content in other chapters.

### Preface (`00_preface.rst`) — REVIEW IN PROGRESS
- [x] Opening (lines 1–70) — REWRITTEN in first-person voice (Apr 23)
- [x] "What's in This Book" — MERGED into opening, section DELETED (Apr 23)
- [x] Platform Notes — Replaced with TODO stub (Apr 23)
- [ ] "Other Books" section — the booklist is from ~2004
- [ ] "Other Sources" — review and update
- [ ] "How This Book Is Organized" — update for 4th edition structure
- [ ] Conventions section — review
- [ ] Code Examples section — review
- [ ] Contact section — update from O'Reilly to self-published
- [ ] Acknowledgments — update for 4th edition

### Chapter reviews (from embedded TODOs)
- [ ] **04_logging:1185** — "This is false. Fix." (factual error in a recipe)
- [ ] **10_security** — Multiple harsh self-reviews from 3e:
  - Move AAA recipes from old ch02 layout
  - "This recipe is probably rubbish" (line 347)
  - "This is terrible. How about a useful recipe here" (line 620)
  - "Probably all wrong now" (line 322)
  - Expand 2.2/2.4 syntax coverage (line 278)
  - Add `find` command recipe for file permissions (line 881)
  - `mod_security` rules packages recipe (line 527)
  - Testing mod_security is enabled (line 530)
- [ ] **12_dynamic_content:2000** — "Update for the modern era" (SSI/CGI content)
- [ ] **12_dynamic_content:2211** — Expression parser syntax in mod_include
- [ ] **13_troubleshooting** — "A lot of the stuff in this chapter is ancient lore"
  - Custom error response / ErrorDocument recipe (line 632)
- [ ] **15_performance** — "Review EVERY recipe carefully. Update for current."
  - Add recipe about Nikto and friends
- [ ] **18_filters_handlers:1647** — Write recipe (pending Graham Leggett)

### Chapter-level decisions
- [ ] **23_puppet.rst** — Almost entirely empty stubs. Options:
  1. Flesh out with current Puppet Apache module content
  2. Replace with a broader "Configuration Management" chapter (Ansible, Puppet, containers)
  3. Cut it entirely
- [ ] **12_dynamic_content** — Heavy CGI/SSI focus is dated. Needs:
  - PHP-FPM modernization (mod_proxy_fcgi recipe drafted)
  - Container/proxy model for dynamic content
  - Possibly split into separate CGI legacy + modern chapters

### Appendix (`appendix.rst`)
- [ ] Write 4th edition revision history entry
- [ ] Add "What's new in the 4th edition" summary

---

## Technical / Build

### Done (Apr 25, 2026)
- [x] Configure `conf.py` for KDP 6×9 format (geometry, headheight, section page breaks)
- [x] Remove "Indices and tables" from `index.rst` (was empty chapter in PDF)
- [x] Add `epub_basename` for clean ePub filenames
- [x] LaTeX build produces 0 errors (27 warnings = same cross-ref issues as HTML)

### Remaining
- [ ] Fix remaining build errors/warnings after fix tasks complete — re-run build
- [ ] Convert `// TODO` AsciiDoc comments to proper `.. todo::` directives (37 in Ch10, Ch12, Ch13, Ch15)
- [ ] Clean up `_italic_` AsciiDoc patterns (65 instances)
- [ ] Clean up `----` horizontal rules (309 instances — review which are intentional)
- [ ] Test and verify epub build
- [ ] Test and verify PDF/LaTeX build (with latexmk)
- [ ] Test Kindle (azw3) conversion via Calibre
- [ ] Rename ugly AsciiDoc-era footnote labels (e.g. `apacheckbk-PREFACE-2-FNOTE-1`)
- [ ] Audit ALL trunk-only content and add `:version:`trunk`` badges
- [ ] Audit all URLs in the book — ensure bare URLs are proper RST hyperlinks
- [ ] Run `make linkcheck` to find dead URLs
- [ ] Set up GitHub repo + CI for automated builds

---

## Publishing Setup (mirror mod_rewrite book)

Items from the mod_rewrite project that need to be replicated here:

### CHANGES.rst (revision history)
- [ ] Create `CHANGES.rst` at project root for version history
- [ ] Add initial 4.0.0 entry
- [ ] Add to `index.rst` back matter toctree (or keep separate from Sphinx build)

### KDP / Publishing
- [ ] Cover image — front cover (1600×2560 for eBook, 300dpi for print)
- [ ] KDP ebook cover (.jpg, RGB, 72+ dpi, <50MB)
- [ ] KDP paperback cover (full-wrap PDF at 300 dpi — spine width depends on page count)
- [ ] KDP category selection + 7 keywords
- [ ] ePub testing — verify on Kindle, Apple Books, Kobo
- [ ] PDF testing — verify 6×9 page layout, margins, code block overflow
- [ ] `publish.sh` — script to sync built outputs somewhere (S3, server, etc.)

### ePub / Kindle
- [ ] `fix_epub_footnotes.py` — already present, verify it works with this book
- [ ] Test footnote rendering on actual Kindle device
- [ ] Verify `epub_basename` produces clean filename
- [ ] Test azw3 conversion via Calibre

### Website / Domain
- [ ] **Pick a domain name** (low priority — no rush)
  - Suggestions: `apache-httpd-book.com`, `practical-httpd.com`, `httpd-guide.com`,
    `apachehttpd.guide`, `httpd-cookbook.com`, `httpd-practical-guide.com`
  - Check availability before deciding
  - Could also use a subdomain of `rcbowen.com` (e.g., `httpd.rcbowen.com`)
- [ ] Set up hosting (S3 + CloudFront, or `fagin.rcbowen.com` like mod-rewrite.org)
- [ ] Landing page (site_index.html equivalent)
- [ ] Publish HTML, PDF, ePub downloads on the site
- [ ] `sync-files.sh` — rsync built outputs to hosting server

---

## Nice to Have (post-publish)

### Epigraphs
- [ ] **Replace ALL placeholder rock-lyric epigraphs with real quotes**
  - Every chapter currently has a temporary classic rock song lyric as a placeholder
  - Same convention as the mod_rewrite book: each chapter opens with a quote, unique author per chapter
  - Back-matter `epigraphs.rst` collects them all with notes on why each was chosen
  - Rules: one quote per author (exceptions allowed for Terry Pratchett and Ray Bradbury),
    verse uses `| ` line blocks, attribution as `-- Author, *Source Title*`
  - These are deeply personal choices — Rich selects them himself
  - Current placeholders: AC/DC, Starship, Pink Floyd, Rolling Stones, The Police, Queen,
    The Clash, The Who, Nirvana, George Harrison, Bob Dylan, Joni Mitchell, Kenny Loggins,
    Twisted Sister, The Beatles, The Animals, Judas Priest, Madness, Kraftwerk, David Bowie, etc.

- [ ] Cover image / artwork
- [ ] Index review and cleanup (carried over from 3e, may have stale entries)
- [ ] Consistent recipe structure audit (Problem/Solution/Discussion/See Also)
- [ ] Add new recipes for httpd 2.4 features not in 3e:
  - HTTP/2 (`mod_http2`)
  - `mod_md` (ACME/Let's Encrypt)
  - Expression parser (`<If>`, `<ElseIf>`) — partially covered in Ch21
  - Event MPM tuning
- [ ] MEDIUM priority module coverage (27 modules) — see `module_coverage_audit.md`
- [ ] Replace placeholder rock-lyric epigraphs with real quotes

---

## Reference Files

| File | Description |
|------|-------------|
| `TODO.md` | This file |
| `REVIEW_BOOKMARK.md` | Current review position (preface, "Other Books") |
| `recipe_audit.md` | Full inventory of 358 recipes by chapter |
| `module_coverage_audit.md` | 142-module coverage matrix |
| `ml_research/` | 10-year mailing list research (2016–2025) |
| `build_html.log` | Latest HTML build log |
| `build_latex.log` | Latest LaTeX build log |
