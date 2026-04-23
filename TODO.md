# Apache httpd: A Practical Guide — TODO

## Build Health

### Cross-reference labels (41 warnings)
These labels exist but Sphinx can't auto-generate link text because
they're not followed by a section heading. Two options per label:
either add a heading underline, or change the `:ref:` usage to include
explicit text (e.g., `:ref:`Title <label>``).

- **23 chapter-level labels** (line 2 of each chapter) — e.g., `.. _Chapter_Installation:`.
  These need the chapter title line below them to have an RST underline.
- **18 recipe/section labels** — scattered in 04_logging, 05_virtual_hosts,
  09_authentication, 12_dynamic_content, 15_performance, 23_puppet.

### Empty `.. todo::` directives (34)
Mostly in `23_puppet.rst` (28 of them). The Puppet chapter was barely
started in the 3e — it's essentially an outline with empty recipe stubs.
Decision: either flesh it out or cut it.

---

## Content Work

- [ ] Identify recipes that are in the wrong chapter, or which
  overlap/duplicate content in other chapters.

### Preface (`00_preface.rst`)
- [ ] Update "Other Books" section — the booklist is from ~2004
- [ ] Review and update "How This Book Is Organized" for 4th edition structure
- [ ] Write 4th edition author preface / introduction

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
  - PHP-FPM modernization
  - Container/proxy model for dynamic content
  - Possibly split into separate CGI legacy + modern chapters

### Stale URLs
- [ ] `01_installation.rst:155` — O'Reilly catalog URL → update or remove
- [ ] `02_first_website.rst:352,418` — O'Reilly search URLs → update or remove
- [ ] `02_first_website.rst:1647,1660` — O'Reilly shop URLs → update or remove
- [ ] `22_mod_info_status.rst:1101` — O'Reilly shop URL → update or remove
- [ ] General: audit all external URLs for link rot

### Appendix (`appendix.rst`)
- [ ] Write 4th edition revision history entry
- [ ] Add "What's new in the 4th edition" summary

---

## Technical / Build

- [ ] Fix remaining 41 cross-ref labels (add heading underlines)
- [ ] Fix remaining Sphinx warnings (~100+ from inline markup, lists, etc.)
- [ ] Convert `// TODO` AsciiDoc comments to proper `.. todo::` directives (13 instances)
- [ ] Clean up remaining AsciiDoc artifacts (stray `pass:[]` HTML, `_italic_` patterns)
- [ ] Test and fix epub build
- [ ] Test and fix PDF/LaTeX build
- [ ] Set up GitHub repo + CI for automated builds

---

## Nice to Have

- [ ] Cover image / artwork
- [ ] Index review and cleanup (carried over from 3e, may have stale entries)
- [ ] Consistent recipe structure audit (Problem/Solution/Discussion/See Also)
- [ ] Add new recipes for httpd 2.4 features not in 3e:
  - HTTP/2 (`mod_http2`)
  - `mod_md` (ACME/Let's Encrypt)
  - Expression parser (`<If>`, `<ElseIf>`)
  - Event MPM tuning
  - Systemd integration
