# Style Guide — Apache httpd: A Practical Guide

This guide defines conventions for writing and editing the book.
Derived from the official Apache httpd documentation style guide
(httpd-trunk/docs/manual/style-guide.txt) and adapted for a
Sphinx/RST book format.

---

## Product Name

- **First mention per chapter**: "Apache HTTP Server" or "Apache httpd"
- **Subsequent mentions**: "Apache httpd"
- **Further references**: just "httpd"
- **Do NOT** use bare "Apache" to mean the server. "Apache" is the
  foundation; "httpd" is the server.
- Companion book: *mod_rewrite And Friends* (italicized, full title)

## Voice and Person

- **First person singular**: "I" — never "we" (sole author)
- **Reader**: "you" — address the reader directly
- Active voice: "Use this directive to configure..." not "The directive
  is used to configure..."
- Avoid impersonal third-person: PREFER "You should configure..."
  AVOID "The administrator should configure..."
- Contractions are fine: "doesn't", "won't", "can't"
- Rich's personality belongs in the text — direct, opinionated,
  sometimes irreverent

## Things to Avoid

- **Condescending language**: no "trivial", "obvious", "simple",
  "of course", "needless to say" when describing something the reader
  is learning. OK in technical contexts ("trivially spoofed").
- **Weasel words**: no "significantly", "virtually", "almost completely",
  "deeply embedded", "widely recognized as"
- **Passive voice**: restructure to active
- **"We"**: sole author — always "I" (exception: "we" meaning the
  Apache community in Ch17 Contributing)

## Spelling and Grammar

- **American English**: behavior, customize, recognize, authorize, color
- **Oxford comma**: always ("addresses, hostnames, and ports")
- **Contractions**: acceptable and encouraged for natural tone

## RST Markup Conventions

### Inline Markup

| Content | Markup | Example |
|---------|--------|---------|
| Module names | `:module:` role | `:module:\`mod_rewrite\`` |
| File/directory paths | `:file:` role | `:file:\`/etc/httpd/conf/httpd.conf\`` |
| Directive names | Double backticks | ` ``ServerRoot`` ` |
| Literal values, CLI flags, HTTP methods, MIME types | Double backticks | ` ``GET`` `, ` ``text/html`` ` |
| Emphasis | Single asterisks | `*emphasis*` |
| Strong emphasis | Double asterisks | `**strong**` |
| URL request paths | Double backticks | ` ``/about`` `, ` ``/login`` ` |
| Placeholders (user-supplied values) | `:file:` with braces | `:file:\`/var/www/{site}\`` |

### Heading Capitalization

**Sentence case** for ALL headings — capitalize only:
- First word of the heading
- Proper nouns: Apache, HTTP, SSL, TLS, PHP, LDAP, Perl, Python, Windows,
  Linux, macOS, Debian, Ubuntu, Fedora, Red Hat
- Acronyms: MPM, URL, DNS, FQDN, SSI, IP, FTP, CGI, RPM, WebSocket
- Module names keep original case: `mod_rewrite`, `mod_ssl`
- Directive names keep CamelCase: `AllowOverride`, `ServerName`,
  `DirectoryIndex`, `ErrorDocument`, `RewriteRule`
- Auth scheme names: Basic, Digest, Bearer (these are proper names)

**Examples**:
- ✅ "Installing on RPM-based Linux distributions"
- ✅ "Understanding HTTP status codes"
- ❌ "Installing On RPM-Based Linux Distributions"

**Notes**:
- `:directive:` is **NOT** a valid Sphinx role — do not use it
- Do NOT use `:module:` inside section titles or `.. index::` directives
- Do NOT nest inline roles inside `*emphasis*` markup
- `:file:` is ONLY for filesystem paths — URL paths use plain backticks

### Headings

```
=======     Chapter title (H1) — one per file
=======

Section Title (H2) — recipe level
----------------------------------

Subsection (H3) — Problem, Solution, Discussion, See Also
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sub-subsection (H4) — rare, used for reference tables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

**Critical**: Do NOT skip levels (e.g., H2 → H4 without H3).

### Code Blocks

```rst
.. code-block:: apache

   ServerRoot "/etc/httpd"
   Listen 80

.. code-block:: bash

   $ apachectl graceful

.. code-block:: text

   [Mon Apr 25 10:00:00] [error] ...
```

Use `apache` for httpd config, `bash` for shell commands, `text` for
output/logs. Never use bare `.. code-block::` without a language.

### Index Entries

Add `.. index::` entries generously — directives, flags, modules,
tools, concepts, proper nouns. Place before the section they relate to,
with a blank line after:

```rst
.. index:: mod_rewrite
.. index:: RewriteRule
.. index:: URL rewriting

Rewriting URLs
--------------
```

### Cross-references

```rst
:ref:`Chapter_Installation`
:ref:`Recipe_canonical_hostname`
:ref:`Descriptive text <label_name>`
```

### Version Badges

```rst
:version:`2.4.48`     — available in 2.4 stable
:version:`trunk`      — trunk only (unreleased)
```

Trunk-only recipes also need a warning admonition at the top.

**Version policy**: This book covers **httpd 2.4.x only**. No content
for 2.2 or earlier. Trunk-only content should be very rare — include it
only when the feature is likely to land in a near-future 2.4.x release
or is genuinely useful for readers tracking trunk. Always mark with
`:version:\`trunk\`` AND a warning admonition:

```rst
.. warning:: This feature is only available in httpd trunk (unreleased).
```

## Recipe Structure

Every recipe follows this pattern:

```rst
.. _Recipe_name:

Recipe Title
------------

.. index:: relevant terms

Problem
~~~~~~~

One or two sentences describing what the reader wants to accomplish.

Solution
~~~~~~~~

The configuration or commands needed. Show the minimal working example.

Discussion
~~~~~~~~~~

Explanation of how it works, edge cases, common pitfalls, related
options.

See Also
~~~~~~~~

* :ref:`Related_recipe`
* `External resource <https://example.com>`_
```

## Chapter Structure

1. `.. raw:: latex` part directive (if first chapter in a Part)
2. Chapter label: `.. _Chapter_name:`
3. Epigraph (quote + attribution)
4. Chapter title with `=` overline/underline
5. `.. index::` entries
6. Brief introduction (1-3 paragraphs)
7. Recipes (H2 level)
8. Summary section

## Epigraphs

- Every chapter opens with a quote
- One unique author per chapter (exceptions: Pratchett, Bradbury)
- Format: `.. epigraph::` directive
- Verse: `| ` line blocks; prose: plain indented text
- Attribution: `-- Author, *Source Title*`
- Back matter `epigraphs.rst` collects all quotes with notes

## Version Numbering

- Format: **x.y** (not x.y.z)
- Update in THREE places: `conf.py`, `README.md`, `CHANGES.rst`

## Content Policy — Companion Book Overlap

Where content overlaps with *mod_rewrite And Friends*, keep a brief
overview (3-4 essential recipes) and point readers to the companion
book. Do NOT maintain full duplicate coverage.

Affected chapters:
- Ch08 (mod_rewrite) — condensed to essentials
- Ch21 (Programmable Config) — expression parser content removed

When removing recipes, preserve all `.. _Recipe_xxx:` labels as stubs
with a pointer note so cross-references from other chapters don't break.

## Recipe vs. Reference Material — The `refcosplay` Tag

Some "recipes" are really reference material wearing a recipe costume.
They don't answer a real Problem — they explain a concept, provide a
reference table, or introduce a topic that would be better as a chapter
introduction section.

Tag these with a comment:

```rst
.. refcosplay
```

Place this comment immediately before the recipe's `.. _Recipe_` label.
Grepable: `grep -r refcosplay chapters/`

**Future plan (v1.0)**: Each chapter gets a reference introduction
section covering basic concepts in manual/reference style, followed by
the recipes. The `refcosplay`-tagged content is the raw material for
those introductions — stuff that feels artificial as a recipe becomes
natural as reference prose.
