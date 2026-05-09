
.. _Chapter_Contributing_to_apache:

======================================
Contributing to the Apache HTTP Server
======================================

.. epigraph::

   If you want to go fast, go alone. If you want to go far, go together.

   -- African proverb

.. index:: Contributing
.. index:: Open Source
.. index:: F/LOSS
.. index:: The Apache Way
.. index:: Apache Software Foundation

The Apache HTTP Server is open source. That means there's no **you** and
**us**. It's all just us. The software is developed by us, for us, and
you're welcome to become one of us and participate in that process.

I've been involved with this project for over twenty-five years now, and
I can tell you honestly: it's the people that keep me here. The code is
interesting, sure. But the community — the collaboration, the arguments,
the shared sense of building something that matters — that's what makes
Apache httpd special. Millions of websites run on software that we built
together, and there's room at the table for you.

If you've never worked on an open source project, navigating your way
around can be a little confusing. Every project has its own culture, its
own tools, its own unwritten rules. In this chapter, I'll give you the
lay of the land and show you all of the places where you can join in.
Some of what follows is practical how-to — step-by-step instructions for
checking out code, generating patches, and building documentation. Some of
it is the kind of tribal knowledge that you'd normally only pick up after
lurking on mailing lists for a year. I'm giving you the shortcut.

One thing I want to be upfront about: the httpd project moves at the pace
of its volunteers. Nobody is getting paid by the ASF to work on this. When
you submit a patch, it might sit for a week before someone reviews it.
That's not because people don't care — it's because everyone is juggling
this alongside their day job and their life. Patience is a virtue here.
The flip side of that is freedom. Nobody is going to assign you a ticket
or give you a deadline. You work on what interests you, at your own pace.
That's remarkably liberating once you get used to it.

Contributing doesn't require being a C programmer. Some of the most
valuable contributors I've worked with have never written a line of server
code. They write documentation, answer questions on the mailing list,
triage bug reports, translate docs into other languages, or give talks at
conferences. All of it matters. All of it makes the project better.


.. _contributing_asf:

How the Apache Software Foundation works
----------------------------------------

.. index:: Apache Software Foundation
.. index:: ASF
.. index:: Meritocracy
.. index:: PMC
.. index:: Committer
.. index:: Contributor
.. index:: Incubator
.. index:: Attic

The Apache Software Foundation — the ASF — is a non-profit organization
(a US 501(c)(3)) founded in 1999. Its mission is to provide software for
the public good. The httpd project is what started it all, but the ASF is
now home to hundreds of projects spanning every area of technology you can
imagine: big data (Hadoop, Spark), messaging (Kafka), search (Lucene,
Solr), and far more. You can browse them all at
https://projects.apache.org/.

The ASF provides infrastructure — code repositories, mailing lists,
websites, build systems — and a legal umbrella that protects both the
software and the people who write it. Everything released under the Apache
License is free to download, free to use, and free to modify, including
for commercial purposes. That's by design. The license is deliberately
permissive, which is why you'll find Apache-licensed code inside
everything from smartphones to satellites.

The organizational model
~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: Earned authority
.. index:: Community over code

The ASF operates on what we call "earned authority." You don't buy your
way in, and you don't get appointed by a corporation. You earn trust by
doing good work over time. The hierarchy looks like this:

**Contributors** are anyone who contributes to the project in any way —
patches, documentation, bug reports, mailing list help. You don't need
permission to be a contributor. Just show up and start helping.

**Committers** are contributors who have been granted direct write access
to the project's source code repository. This is offered by the existing
committers when someone has demonstrated consistent, high-quality
contributions over a sustained period. It's an invitation, not something
you apply for. When the time is right, someone will nominate you.

**PMC members** (Project Management Committee) are committers who have
been elected to the PMC. The PMC is responsible for the project's
governance — voting on releases, granting new committer access, and
ensuring the project follows ASF policies. PMC membership is a
responsibility, not just an honor.

**ASF Members** are individuals elected by the existing membership in
recognition of their contributions across the Foundation, not just to a
single project. Members elect the Board of Directors and have a voice in
Foundation-wide decisions.

This isn't a corporate ladder. Plenty of people are perfectly happy
contributing without ever becoming a committer, and that's fine. The point
is that the path is open to anyone, regardless of employer, geography, or
credentials. I've seen people go from their first patch to PMC member in
under two years. I've also seen people contribute happily for a decade
without ever wanting commit access. Both are valid paths.

One important nuance: at the ASF, we say "community over code." That
means the health of the community matters more than any individual
technical contribution. A person who is brilliant but toxic will not
advance. A person who is helpful, respectful, and consistent absolutely
will. This isn't just a slogan — I've watched it play out countless times
over the years, and it's one of the things that makes the ASF work.

The Incubator and the Attic
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: Apache Incubator
.. index:: Apache Attic

New projects entering the ASF go through the Incubator
(https://incubator.apache.org/), where they learn how to operate within
the Foundation's governance model — building a diverse community, following
the release process, understanding intellectual property requirements.
When they demonstrate that they can self-govern effectively, they graduate
to become top-level projects. Some projects spend six months in the
Incubator; others take several years. There's no rush.

On the other end of the lifecycle, projects that are no longer actively
maintained move to the Attic (https://attic.apache.org/). This isn't
shameful — some projects have simply achieved feature completeness, or the
technology has moved on. The Attic preserves the code and documentation
permanently, and provides a clear path for someone to restart the project
if that ever becomes desirable.

.. seealso::

   * The Apache Software Foundation: https://apache.org/
   * About the ASF: https://apache.org/foundation/
   * The Apache License: https://apache.org/licenses/
   * Apache Projects directory: https://projects.apache.org/
   * The Open Source Initiative: https://opensource.org/


.. _contributing_governance:

The httpd project governance
----------------------------

.. index:: Governance
.. index:: Voting
.. index:: Lazy consensus
.. index:: Release process
.. index:: Commit policies, RTC (Review Then Commit)
.. index:: Commit policies, CTR (Commit Then Review)
.. index:: RTC
.. index:: CTR

The httpd project operates within the ASF framework, but every Apache
project has its own character. Here's how httpd specifically works.

The httpd PMC currently has a few dozen members. Many of them have been
involved for ten or fifteen years; a few have been here since the
beginning in 1995. Some are employed by companies that use httpd heavily;
others contribute purely on their own time. The mix is important — it
means no single company controls the project's direction.

The PMC makes decisions by consensus on the dev@httpd.apache.org mailing
list. If consensus can't be reached through discussion, a formal vote is
called. Voting uses a simple system: +1 (yes), 0 (abstain), and -1 (veto,
but must include a technical justification). A bare -1 without explanation
carries no weight.

Most routine decisions use **lazy consensus** — if nobody objects within
72 hours, the proposal is considered approved. This keeps things moving
without requiring everyone to weigh in on every small decision.

In practice, most of the day-to-day development work happens without
formal votes. Someone proposes an idea on the list, discussion happens,
and if nobody objects, it moves forward. The formal voting mechanism is
there for when there's genuine disagreement, or for significant decisions
like releases and new committers. In twenty-five years, I've seen very few
actual vetoes. When they happen, they're serious, and they get resolved
through technical discussion rather than politics.

For code changes, httpd uses two different policies depending on the
branch:

* **Trunk** (the development branch) operates under **Commit Then Review**
  (CTR). Committers can push changes directly, and review happens after the
  fact. If someone objects, the change gets reverted and discussed.

* **Release branches** (like 2.4.x) operate under **Review Then Commit**
  (RTC). Changes must be proposed in the :file:`STATUS` file, reviewed,
  and receive at least three +1 votes from PMC members before they can be
  applied to the branch. This is more conservative, because release
  branches need to be stable.

The release process itself involves a release manager (a volunteer PMC
member) who rolls a candidate tarball, and then the PMC votes on whether
to release it. Three +1 votes from PMC members with no vetoes, and it
ships. The tarball is signed, checksums are published, and the release is
mirrored around the world. It's a well-oiled process at this point.

If this all sounds formal, it is — but in a good way. These processes
exist because they work. They've been refined over decades, and they're
what allow a globally distributed group of volunteers to produce
software that runs a significant chunk of the internet.

The httpd PMC reports to the ASF Board of Directors quarterly. This is a
lightweight report covering the project's health — new committers, release
activity, community growth, and any issues. It's a check that the project
is functioning well, not micromanagement. The Board doesn't tell projects
what to do technically; it ensures they're operating in accordance with
ASF principles.

If you want to understand the project's governance in more detail, the
best thing you can do is subscribe to dev@httpd.apache.org and read for
a few weeks. You'll see the culture in action — how decisions get made,
how disagreements get resolved, how new ideas get introduced. It's more
instructive than any description I can give you here.


.. _contributing_communication:

Communication channels
----------------------

.. index:: Mailing lists
.. index:: Slack
.. index:: Social media
.. index:: Discussion

Communication is the lifeblood of any open source project. Here's where
the httpd community talks.

Mailing lists
~~~~~~~~~~~~~

.. index:: Mailing lists, users list
.. index:: Mailing lists, dev list
.. index:: Mailing lists, docs list
.. index:: Mailing lists, commits list
.. index:: Users mailing list
.. index:: Dev mailing list
.. index:: Docs mailing list

Mailing lists are the canonical communication channel for the httpd
project. Decisions are made here. Patches are reviewed here. If it didn't
happen on the mailing list, it didn't happen — that's a core ASF principle.
The mailing list is the permanent, public, searchable record of the
project's decision-making process.

The lists you'll care about most:

**users@httpd.apache.org** — The user support list. Ask questions, report
problems, help others. Traffic is light (a few messages per day), and the
community is welcoming to newcomers. To subscribe, send an empty email to
``users-subscribe@httpd.apache.org``.

**dev@httpd.apache.org** — The developer list. If you want to contribute
code or participate in project decisions, you need to be here. This is
where patches get reviewed, releases get discussed, and technical
arguments play out. Subscribe by sending to
``dev-subscribe@httpd.apache.org``.

**docs@httpd.apache.org** — The documentation team's list. Very low
traffic, very friendly. If you want to help with docs, start here.
Subscribe via ``docs-subscribe@httpd.apache.org``.

**cvs@httpd.apache.org** — Commit notifications. Every time the source
code changes, a notification goes here. The name is a historical artifact
from when the project used CVS for version control — we migrated to SVN
ages ago, but the list name stuck. Subscribe via
``cvs-subscribe@httpd.apache.org``.

**bugs@httpd.apache.org** — Notifications from the bug tracker. When
tickets are opened, modified, or closed, the update goes here. Subscribe
via ``bugs-subscribe@httpd.apache.org``.

All of these lists have web archives at https://lists.apache.org/ where
you can read past discussions, search for topics, and participate through
a web interface if you prefer that to email. The full list of httpd
mailing lists is at https://httpd.apache.org/lists.html.

A few tips for mailing list etiquette that will serve you well:

* **Top-posting is discouraged.** Reply inline or at the bottom of the
  quoted text, not at the top. This keeps threaded conversations readable.

* **Use plain text email**, not HTML. Many of the developers read mail in
  terminal-based clients that don't render HTML well.

* **Be specific in your subject line.** "Help needed" tells nobody
  anything. "mod_rewrite RewriteRule not matching URL with query string"
  tells everyone exactly what you're asking about.

* **Do your homework first.** Before asking a question, check the
  documentation, search the list archives, and try to reproduce the
  problem with a minimal configuration. Show your work.

* **Don't email individual developers directly.** Use the list. Private
  emails bypass the community and put an unfair burden on one person.
  Plus, the answer won't help anyone else.

When you first subscribe to dev@, spend a week or two reading before you
post. Get a feel for the culture, the tone, the kinds of discussions that
happen. Then jump in. Nobody will bite.

Slack
~~~~~

.. index:: Slack
.. index:: the-asf.slack.com
.. index:: Real-time chat

The ASF has an official Slack workspace at ``the-asf.slack.com``. The
``#httpd`` channel there is where real-time conversation happens these
days. It's a good place to ask quick questions, get a sanity check on an
idea before posting it to the mailing list, or just hang out with other
httpd folks.

To join, you'll need an invitation. If you have an ``@apache.org`` email
address, you can sign up directly. Otherwise, ask on the users@ or dev@
mailing list, and someone will send you a guest invitation to the relevant
channels. See the ASF Slack guide at https://infra.apache.org/slack.html
for full details on the invitation process.

A word of caution: decisions still happen on the mailing list. Slack is
great for informal discussion, brainstorming, and quick coordination, but
if you reach a conclusion about something important in a Slack thread, it
needs to be brought back to the list for formal agreement. That's not
bureaucracy — it's how we maintain a public, searchable record that
everyone can access, including people who aren't on Slack. The ASF's
position on this is clear: "If it didn't happen on the mailing list, it
didn't happen."

.. note::

   If you've read older resources about httpd that mention IRC channels on
   Libera Chat or Freenode, those channels are essentially dead. The
   project's real-time communication moved to Slack several years ago.
   Don't waste your time waiting for a response on IRC — come to Slack
   instead.

Social media
~~~~~~~~~~~~

.. index:: Social media
.. index:: Twitter
.. index:: X (formerly Twitter)

The official account for the project on X (formerly Twitter) is
``@apache_httpd``. It's a good place to hear about new releases, security
advisories, and conference appearances. Follow it if you want a low-noise
signal of what's happening with the project.

The ASF also maintains a broader presence on social media through
``@TheASF`` on various platforms. If you're sharing something interesting
about httpd on social media, tag the project account — it helps others
find the community.


.. _contributing_source:

Getting the source code
-----------------------

.. index:: Source code
.. index:: Subversion
.. index:: SVN
.. index:: GitHub mirror
.. index:: svn checkout
.. index:: Version control

The canonical source repository for Apache httpd is Subversion (SVN),
hosted at ``svn.apache.org``. Yes, in an age of Git dominance, httpd still
uses SVN as its primary version control system. There are historical
reasons for this, and periodic discussions about migrating to Git, but for
now SVN is where the authoritative code lives. There's a read-only Git
mirror on GitHub, and I'll talk about that in a moment, but SVN is where
the real work happens.

Checking out the source
~~~~~~~~~~~~~~~~~~~~~~~

First, install Subversion if you don't already have it:

.. code-block:: bash

   # Debian/Ubuntu
   sudo apt install subversion

   # Fedora/RHEL/AlmaLinux
   sudo dnf install subversion

   # macOS (via Homebrew)
   brew install subversion

To check out the development trunk:

.. code-block:: bash

   svn checkout https://svn.apache.org/repos/asf/httpd/httpd/trunk httpd-trunk

To check out the stable 2.4.x branch:

.. code-block:: bash

   svn checkout https://svn.apache.org/repos/asf/httpd/httpd/branches/2.4.x httpd-2.4

These checkouts will give you the complete source tree, including the
documentation source in :file:`docs/manual/`.

Keeping your working copy current is straightforward:

.. code-block:: bash

   cd httpd-trunk
   svn update

Always run ``svn update`` before starting new work. You want to be working
against the latest code. If you don't, you'll generate patches that don't
apply cleanly to the current source, which creates unnecessary work for
reviewers.

A few SVN commands you'll use constantly:

.. code-block:: bash

   # See what you've changed
   svn status

   # Show your changes in diff format
   svn diff

   # Revert a file to its unmodified state
   svn revert filename.c

   # Revert everything
   svn revert -R .

The GitHub mirror
~~~~~~~~~~~~~~~~~

.. index:: GitHub
.. index:: Pull requests

There's a read-only mirror of the httpd source at
https://github.com/apache/httpd. You can browse the code there, and
GitHub's search and blame tools are useful for navigating the source tree.
The mirror is updated automatically from SVN, so it's always current.

You *can* submit pull requests on GitHub, and the project's contribute
page acknowledges this as a valid path. However, I'll be honest with you:
PRs on GitHub sometimes get overlooked. The core developers are watching
the dev@ mailing list, not GitHub notifications. If you want your
contribution to get timely attention, generate a patch with ``svn diff``
and send it to dev@httpd.apache.org with a clear explanation. That's the
path with the least friction and the fastest turnaround.

If you strongly prefer Git, you can use ``git svn`` to maintain a local
Git repository that talks to the SVN server. But for submitting patches,
the output of ``svn diff`` is what reviewers expect to see.

Browsing the repository
~~~~~~~~~~~~~~~~~~~~~~~

You can explore the repository structure without checking anything out:

.. code-block:: bash

   svn ls https://svn.apache.org/repos/asf/httpd/httpd/branches/
   svn ls https://svn.apache.org/repos/asf/httpd/httpd/tags/

There's also a web-based browser at
https://svn.apache.org/viewvc/httpd/httpd/ where you can view file
history, compare revisions, and see who changed what and when. This is
invaluable when you're trying to understand why a piece of code looks the
way it does.


.. _contributing_first_patch:

Submitting your first patch
---------------------------

.. index:: Patch
.. index:: svn diff
.. index:: Code review
.. index:: Your first patch

Here's the honest truth about submitting your first patch to any
long-established open source project: it can feel intimidating. The code
is large, the developers are experienced, and you might worry about
looking foolish. I've been there. Everyone has been there. Push through
it. The httpd community is genuinely welcoming to new contributors, and
nobody expects your first patch to be perfect.

The workflow
~~~~~~~~~~~~

The basic process looks like this:

1. Check out the source (as described above).

2. Make your change. Edit the file(s) with your favorite editor.

3. Test your change. Build the server (``./buildconf && ./configure &&
make``) and verify that it starts, runs, and does what you expect. Run
the test suite if your change is non-trivial.

4. Generate a patch:

   .. code-block:: bash

      svn diff > my_fix.patch

5. Send the patch to ``dev@httpd.apache.org`` with ``[PATCH]`` in the
subject line. Include a clear description of what you're fixing and
why. Attach the patch file — don't paste it inline, as mail clients
tend to mangle whitespace.

That's it. That's the whole process.

A realistic example
~~~~~~~~~~~~~~~~~~~

Let's say you've found a typo in an error message in
:file:`modules/http/http_filters.c`. Here's what the workflow looks like
in practice:

.. code-block:: bash

   # Get a fresh checkout (or update your existing one)
   cd httpd-trunk
   svn update

   # Make the fix
   vim modules/http/http_filters.c

   # Verify the build still works
   make

   # See what you changed
   svn diff

The diff output will look something like this:

.. code-block:: diff

   Index: modules/http/http_filters.c
   ===================================================================
   --- modules/http/http_filters.c	(revision 1920145)
   +++ modules/http/http_filters.c	(working copy)
   @@ -234,7 +234,7 @@
        if (rv != APR_SUCCESS) {
            ap_log_rerror(APLOG_MARK, APLOG_ERR, rv, r, APLOGNO(01234)
   -                      "Error rading request body");
   +                      "Error reading request body");
            return rv;
        }

Save the patch and send it:

.. code-block:: bash

   # Save the patch
   svn diff > fix_typo_http_filters.patch

Then compose an email to dev@httpd.apache.org:

.. code-block:: text

   Subject: [PATCH] Fix typo in http_filters.c error message

   Hi all,

   Attached is a one-line fix for a typo in an error message in
   http_filters.c ("rading" -> "reading").

   Tested with a full build on Ubuntu 24.04.

   Cheers,
   [Your Name]

What to expect
~~~~~~~~~~~~~~

Be patient. The httpd developers are volunteers, and reviewing patches
isn't anyone's full-time job. It might take a few days to get a response.
If a week goes by with no reply, it's perfectly acceptable to send a
polite follow-up — just reply to your original message with a brief "Any
thoughts on this?" Don't be aggressive about it, but don't let your patch
silently disappear either.

Don't be discouraged if your patch gets feedback requesting changes.
That's normal and healthy — it's how code review works. The feedback
is meant to improve the code, not to criticize you personally. Respond to
the feedback, update your patch, and resubmit. This back-and-forth is how
most patches evolve from good to great.

If your patch is accepted, a committer will apply it and credit you in the
commit message. Your name will appear in the project's change log. If you
keep submitting good patches over time, you'll eventually be offered
committer access yourself. That's how the system works — earned trust,
demonstrated through consistent contribution.

For larger changes — new features, significant refactoring, architectural
modifications — it's wise to discuss your idea on the mailing list
*before* writing the code. This saves you from investing significant time
in something that the community might not want, or that conflicts with
ongoing work you weren't aware of.


.. _contributing_what_to_work_on:

What to work on
---------------

.. index:: Bug fixing
.. index:: Bugzilla
.. index:: Test suite
.. index:: Code review
.. index:: First contribution

"I want to help, but I don't know where to start." I hear this all the
time. Here are your options, roughly in order from least to most
intimidating.

Answering questions on the mailing list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you know httpd well enough to be reading this book, you know enough to
help other people on users@httpd.apache.org. Every question you answer is
a contribution. It frees up developer time and makes the community more
welcoming. And frankly, explaining things to others is one of the best
ways to deepen your own understanding.

Triaging bug reports
~~~~~~~~~~~~~~~~~~~~

.. index:: Bug triage
.. index:: bz.apache.org

The bug tracker lives at https://bz.apache.org/bugzilla/ (select the
"Apache httpd-2" product). There are always open tickets that need
attention. Some bugs need more information from the reporter. Some are
duplicates of existing tickets. Some have been fixed but never closed.
Some are so old that the reported problem no longer exists. Helping sort
through this backlog is enormously valuable.

You can browse open bugs at:
https://bz.apache.org/bugzilla/buglist.cgi?product=Apache%20httpd-2&bug_status=NEW&bug_status=REOPENED

To help with triage, you'll need to create a Bugzilla account. Then you
can add comments to tickets — asking for reproduction steps, confirming
whether a bug still exists on the current version, or noting that a ticket
is a duplicate of another.

Fixing bugs
~~~~~~~~~~~

Once you're comfortable reading the code, pick a bug from the tracker and
try to fix it. Start with something small — a segfault with a clear
reproduction case, a logic error in a rarely-used code path, an
off-by-one error. Don't try to tackle a major architectural change as your
first contribution. Build confidence with small wins first.

The :file:`STATUS` file in the top level of the 2.4.x branch is another
great place to find work. It contains a list of proposed patches waiting
for review votes. Looking at what other people are proposing and trying to
understand their changes is excellent practice, even before you start
writing your own.

Reviewing other people's patches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When someone posts a patch to dev@, you can review it. Try applying it to
your working copy. Does it compile? Does it fix the stated problem? Does
it introduce any obvious issues? Does the code style match the surrounding
code? Posting a thoughtful review is a contribution, even if you're not a
committer. In fact, demonstrating good judgment in reviews is one of the
fastest paths to earning commit access.

Writing tests
~~~~~~~~~~~~~

.. index:: Apache::Test
.. index:: Test framework

The httpd test suite lives at https://httpd.apache.org/test/ and uses the
Perl-based ``Apache::Test`` framework. More test coverage is always
welcome. If you fix a bug, writing a test that would have caught it is an
excellent way to make your patch more likely to be accepted — and to ensure
the bug doesn't come back later.

Improving the documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

I'll cover this in more detail in the next section, but it bears
mentioning here: documentation is a first-class contribution. If you find
something confusing in the docs, fix it. If an example is wrong, correct
it. If a whole topic isn't covered, write about it. The documentation team
is perpetually understaffed, and fresh eyes catch things that we veterans
miss.

The STATUS file
~~~~~~~~~~~~~~~

.. index:: STATUS file

One resource worth mentioning specifically is the :file:`STATUS` file in
the top-level directory of each branch. This file is the project's
coordination document — it lists proposed patches that are waiting for
review votes, known bugs that need fixing, and items that are being
actively discussed. Reading the STATUS file gives you an immediate picture
of what the project is currently working on and where help is needed most.

For the 2.4.x branch, the STATUS file contains entries like this:

.. code-block:: text

   PATCHES PROPOSED TO BACKPORT FROM TRUNK:
     * mod_ssl: Fix memory leak in ssl_init_ctx_protocol
       Trunk patch: https://svn.apache.org/r1919876
       2.4.x patch: https://svn.apache.org/r1919877
       +1: covener, ylavic
       +0:
       -1:

Each entry needs three +1 votes from PMC members to be applied. If you
can test a proposed patch and provide feedback (even without a binding
vote), that's genuinely helpful and accelerates the process.

The project website also maintains a page specifically about contributing
at https://httpd.apache.org/contribute/ which provides quick links to
the source repositories, the mailing lists, and the STATUS file. It's
a good bookmark to keep handy.

.. _contributing_documentation:

Contributing to the documentation
---------------------------------

.. index:: Documentation, contributing
.. index:: XML source format
.. index:: docs-build
.. index:: Documentation project

The best software in the world doesn't do a bit of good if nobody can use
it. That's why I think the documentation is so important — arguably more
important than any individual feature. And because writing good
documentation requires a different set of skills from writing C code, the
docs project is managed as a subproject with its own mailing list, its own
review process, and a lower barrier to entry for new contributors.

The documentation project page is at https://httpd.apache.org/docs-project/
and the docs mailing list is at ``docs@httpd.apache.org``.

The source format
~~~~~~~~~~~~~~~~~

.. index:: XML, documentation format
.. index:: Documentation, build process

The httpd documentation is written in a custom XML format. It's not
DocBook, and it's not Markdown — it's an XML vocabulary specific to the
httpd docs project that was designed to produce high-quality output in
multiple formats. If you've worked with any XML-based documentation
system, you'll pick it up quickly. If you haven't, don't worry. Most
contributions start as small edits to existing files, where you can simply
follow the patterns already there.

The documentation source lives in the :file:`docs/manual/` subdirectory of
the httpd source tree. Module documentation is in
:file:`docs/manual/mod/`, how-to guides in :file:`docs/manual/howto/`, and
so on. The structure mirrors what you see on the documentation website.

Here's a small example of what the XML source looks like, from a module
documentation file:

.. code-block:: xml

   <directivesynopsis>
   <name>ServerName</name>
   <description>Hostname and port that the server uses to identify
   itself</description>
   <syntax>ServerName
   [<var>scheme</var>://]<var>domain-name</var>|<var>ip-address</var>[:<var>port</var>]</syntax>
   <contextlist><context>server config</context>
   <context>virtual host</context></contextlist>
   </directivesynopsis>

The XML vocabulary includes elements for directives, code examples,
notes, warnings, cross-references, and more. You don't need to memorize
it all — just look at existing files and follow the patterns. The format
documentation is at https://httpd.apache.org/docs-project/docsformat.html.

Building the docs locally
~~~~~~~~~~~~~~~~~~~~~~~~~

To build the HTML documentation from the XML source, you'll need the
docs-build tools. From within your source checkout:

.. code-block:: bash

   cd docs/manual
   svn checkout https://svn.apache.org/repos/asf/httpd/docs-build/trunk build

Then run the build:

.. code-block:: bash

   cd build
   ./build.sh all

This requires Java (for the XSLT transformations via Ant) and produces a
lot of output. At the end, it'll tell you whether the build succeeded. If
it did, you can open the generated HTML files in your browser to verify
your changes look correct.

If the build fails, the error messages are usually clear about what went
wrong — typically a malformed XML element or a missing closing tag. Fix the
issue, and run the build again.

.. note::

   If the build toolchain is giving you trouble, don't let it stop you.
   Send your patch to the docs list anyway. We'd rather receive a
   contribution in imperfect form than not receive it at all. Someone on
   the docs team will handle the build details. Seriously — don't let
   tooling be a barrier. The content matters more.

Common documentation tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~

Here are some things you can do right now, today, to help:

* **Fix typos and unclear wording.** Read through a page. If something is
  confusing, rewrite it. If a sentence is awkward, smooth it out.

* **Add examples.** Many directive pages lack practical examples showing
  real-world usage. If you know how to use a directive, write up a
  concrete example with explanation.

* **Update outdated information.** Some docs pages haven't been touched in
  years. Operating systems change, best practices evolve, and new versions
  of httpd add or deprecate features.

* **Improve based on user comments.** At the bottom of each docs page,
  users leave comments — questions, corrections, tips. Some of these
  should be incorporated into the docs themselves.

* **Write new howto guides.** If you've solved a problem that took you
  hours to figure out, write up the solution as a howto. Future users will
  thank you.

* **Cross-reference related content.** If you're reading a page and think
  "this would make more sense if it linked to that other page," add the
  cross-reference.

When you've made your changes, generate a patch and send it to
``docs@httpd.apache.org``:

.. code-block:: bash

   svn diff > my_docs_fix.patch

The docs team is small but responsive. Expect a faster turnaround on docs
patches than on code patches — documentation contributions are always
welcome and usually get applied quickly.


.. _contributing_translations:

Documentation translations
--------------------------

.. index:: Translation
.. index:: Documentation, translation
.. index:: Localization
.. index:: Internationalization

The httpd documentation is available in English, French, Japanese, Korean,
Turkish, German, and Spanish, with varying degrees of completeness. English
is the canonical version; other languages are translations that are
maintained alongside it.

If you're fluent in both English and another language, translation is an
incredibly valuable way to contribute. There are billions of web server
administrators who don't speak English as their first language, and
providing documentation in their native language makes a real difference
in their ability to use the software effectively.

How translation works
~~~~~~~~~~~~~~~~~~~~~

Each translated file is a copy of the English source with a language-code
file extension. For example, the Spanish translation of
:file:`mod_rewrite.xml` is :file:`mod_rewrite.xml.es`, the French version
is :file:`mod_rewrite.xml.fr`, the Japanese is :file:`mod_rewrite.xml.ja`.
You translate the prose content while leaving the XML structure intact.

Translated files are annotated with the English revision they were
translated from:

.. code-block:: xml

   <!-- English Revision: 1920145 -->

When the English source gets updated, the build system automatically flags
translations that are out of date:

.. code-block:: xml

   <!-- English Revision: 1905000:1920145 (outdated) -->

This results in a visible warning in the generated HTML, letting readers
know the translation may not reflect the latest changes. Keeping
translations in sync with the English source is an ongoing effort, and one
that always needs more hands.

Getting started with translation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before you start translating, join the docs mailing list
(``docs@httpd.apache.org``) and introduce yourself. Let the community
know which language you want to work in and which documents you plan to
tackle. This helps avoid duplicate effort and connects you with other
translators working in the same language.

You'll also want at least one other fluent speaker to review your
translations. All translated documents should be reviewed by a second
person for accuracy and natural phrasing. Machine translation is not
acceptable as a primary method — these docs need to read naturally to a
native speaker. If you're starting a translation into a language that
doesn't yet have any presence in the project, finding a review partner is
your most important first step.

The translation coordination page is at
https://httpd.apache.org/docs-project/translations.html.

Current status
~~~~~~~~~~~~~~

French and Japanese have the most complete translations — covering most
of the core documentation. Korean, German, Turkish, and Spanish have
partial translations that could use help both completing new pages and
updating existing ones that have fallen behind the English source.

There are many languages with no translation at all. If you speak
Mandarin, Hindi, Portuguese, Arabic, Russian, or any other widely-spoken
language and want to start a new translation effort, the project would be
thrilled to hear from you. Starting a new language is a significant
undertaking, but you don't have to translate everything at once — start
with the most commonly-used pages (the getting started guide, mod_rewrite,
virtual hosts) and expand from there.


.. _contributing_events:

Events and community gatherings
-------------------------------

.. index:: Community Over Code
.. index:: ApacheCon
.. index:: Conferences
.. index:: Events
.. index:: Meetups

One of the best things about open source is getting to meet the people
behind the code. I've made lifelong friends through Apache events, and
some of my most productive collaborations started with a hallway
conversation at a conference.

Community Over Code
~~~~~~~~~~~~~~~~~~~

.. index:: Community Over Code, conference

The ASF's flagship conference is **Community Over Code** (formerly known
as ApacheCon — the name changed in 2023 to better reflect what the event
is really about). It's held annually in multiple regions — typically North
America and Europe, occasionally Asia.

Community Over Code 2026 is being held in Glasgow, Scotland (October
11–14), with a hackathon, talks on Apache projects across the technology
spectrum, and plenty of unstructured time to meet people and collaborate.
There's also a Community Over Code Asia event. These conferences are where
you'll find the highest concentration of httpd developers and contributors
in one place.

You can find current information at https://communityovercode.org/ and the
ASF events page at https://events.apache.org/.

Giving a talk
~~~~~~~~~~~~~

If you've solved an interesting problem with httpd, or built something
novel, or have insights about web server architecture, consider submitting
a talk proposal. The conference has a public CFP (Call for Proposals), and
they actively seek new speakers. You don't need to be a committer or a
famous name in the community — if you have something useful to say, say
it. First-time speakers are welcome and encouraged.

Talks about Apache httpd are also welcome at other conferences:
FOSDEM, SCALE, Open Source Summit, and regional Linux/FOSS events
around the world. The httpd community is always happy to see the project
represented at these events. If you're giving a talk that mentions httpd,
drop a note on the dev@ list — people may be able to attend, or help you
refine your content.

Meetups and roadshows
~~~~~~~~~~~~~~~~~~~~~

Beyond the main conference, the ASF occasionally organizes smaller
events — community days, hackathons, or tracks co-located with other
conferences. Watch the events page and the dev@ list for announcements.

If you're in a city with a significant number of httpd users or
developers, consider organizing a local meetup. It doesn't have to be
formal — a few people in a coffee shop talking about web servers counts.
The community will support you with promotion and materials if you want
them.


.. _contributing_related:

Related Apache projects
-----------------------

.. index:: Related projects, APR
.. index:: Related projects, mod_perl
.. index:: Related projects, Tomcat
.. index:: Related projects, Traffic Server
.. index:: APR
.. index:: mod_perl
.. index:: Tomcat
.. index:: Traffic Server
.. index:: HTTPComponents

If you get involved with httpd, you'll quickly discover that the Apache
ecosystem is interconnected. Several related projects share code,
contributors, and ideas with httpd. If you're looking to expand your
involvement, here are the ones most closely linked to the web server:

**Apache Portable Runtime (APR)** — https://apr.apache.org/ — The
cross-platform C library that httpd is built on. APR provides a portable
abstraction for file I/O, networking, memory allocation, and more. If
you're working on httpd internals, you'll be working with APR constantly.
Improvements to APR directly benefit httpd.

**mod_perl** — https://perl.apache.org/ — Embeds a Perl interpreter in
the server, allowing you to write httpd modules in Perl and run Perl
applications with dramatic performance improvements over CGI. A mature
project with a dedicated community.

**Apache Tomcat** — https://tomcat.apache.org/ — The reference
implementation of Java Servlets and JSP. Frequently deployed behind httpd
as an application server, connected via ``mod_proxy_ajp`` or
``mod_proxy_http``. If you work with Java web applications, you'll likely
encounter both projects together.

**Apache Traffic Server** — https://trafficserver.apache.org/ — A
high-performance HTTP proxy and CDN cache. Originally developed at Yahoo,
now an Apache project. If you're interested in reverse proxying and
caching at massive scale, Traffic Server is worth exploring. It shares
some contributors with httpd.

**Apache HTTPComponents** — https://hc.apache.org/ — Java-based HTTP
client and server libraries. Useful if you're building tools that interact
with web servers programmatically.

All Apache projects share the same organizational philosophy and the same
license. If you become a committer on one Apache project, you'll find the
culture familiar when you visit another. The skills transfer, and the
community connections carry over. Many people are involved in multiple
Apache projects simultaneously.

You can discover more related projects by browsing
https://projects.apache.org/ and filtering by category.

The developer documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: Developer documentation
.. index:: Apache Modules Book

If you want to go deeper into httpd internals — writing modules, working
on the core, understanding the architecture — there are a few resources
worth knowing about:

The ASF's general developer documentation is at
https://www.apache.org/dev/. This covers ASF-wide policies and
procedures: how licensing works, how releases are managed, how to use the
infrastructure.

For httpd-specific development, the in-tree documentation at
:file:`docs/manual/developer/` covers module development basics. The
module development guide at
https://httpd.apache.org/docs/trunk/developer/modguide.html walks through
writing a complete module from scratch.

Nick Kew's book *The Apache Modules Book* (Prentice Hall, 2007) is
somewhat dated now, but it remains the most comprehensive book-length
treatment of httpd module development. If you can find a copy, it's worth
reading for the architectural insights alone, even where specific APIs
have evolved.

The source code itself is, of course, the ultimate documentation.
httpd is well-commented by the standards of large C projects, and reading
existing modules is the best way to learn the patterns and conventions.
Start with a simple module like :file:`modules/generators/mod_autoindex.c`
or :file:`modules/metadata/mod_env.c` to see how the pieces fit together
before diving into something complex like :file:`modules/ssl/` or
:file:`modules/proxy/`.

.. seealso::

   * ASF developer resources: https://www.apache.org/dev/
   * Module development guide: https://httpd.apache.org/docs/trunk/developer/modguide.html
   * Subversion documentation: https://subversion.apache.org/docs/


.. _contributing_summary:

Summary
-------

I've placed this chapter at the end of the book deliberately. If you've
read this far, you know httpd well enough to help. And we genuinely need
your help.

Of the original eight developers who created the Apache HTTP Server back in
1995, none are still actively involved in the project today. The project
thrives because new people keep showing up — people like you — and take
ownership of some piece of it. Maybe you'll fix a bug. Maybe you'll write
documentation. Maybe you'll become the person who answers questions on the
mailing list every day for a decade, as some of us have done. Maybe you'll
end up on the PMC, helping guide the project's direction.

Whatever form your contribution takes, you'll be part of something that
matters. Millions of websites rely on what we build together. That's
not a small thing. When you see a website served by Apache httpd — and
you will, because they're everywhere — you'll know that you helped make
it possible. That's a good feeling.

So come find us on dev@httpd.apache.org. Introduce yourself. Tell us what
you're interested in working on. Ask questions. Propose ideas. We'll help
you find your way. The community is smaller than it once was, which means
your contributions will be noticed quickly and have outsized impact. This
is a good time to get involved.

See you on the list.


.. rubric:: Key resources

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Resource
     - URL
   * - Apache Software Foundation
     - https://apache.org/
   * - httpd project home
     - https://httpd.apache.org/
   * - Contributing page
     - https://httpd.apache.org/contribute/
   * - Source code (SVN)
     - https://svn.apache.org/repos/asf/httpd/httpd/
   * - GitHub mirror
     - https://github.com/apache/httpd
   * - Bug tracker
     - https://bz.apache.org/bugzilla/
   * - Documentation project
     - https://httpd.apache.org/docs-project/
   * - Mailing lists
     - https://httpd.apache.org/lists.html
   * - ASF Slack
     - https://infra.apache.org/slack.html
   * - Community Over Code
     - https://communityovercode.org/
