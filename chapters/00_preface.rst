
.. _Preface:

=======
Preface
=======

.. index:: Preface

.. index:: open source

.. index:: F/LOSS

The Apache Web server is a remarkable piece of software. The basic
package distributed by the Apache Software Foundation is quite
complete and very powerful, and a lot of effort has gone into keeping
it from suffering software bloat. One facet of the package makes it
especially remarkable: it includes extensibility by design. In short,
if the Apache package right out of the box does not do what you want,
you can generally extend it so that it does. This is a fundamental
feature of the way the software is created, using what is called an
'open source' development model.  (See
:ref:`Chapter_Contributing_to_apache`, **Contributing to the Apache HTTP Server**,
for more information.)  Dozens of extensions (called modules) are
included as part of the package distributed by the Apache Software
Foundation. And if one of these doesn't meet your needs, with several
million users out there, there is an excellent chance someone else has
already done your work for you, someone who has concocted a recipe of
changes or enhancements to the server that will satisfy your
requirements.

This book is a collection of these recipes. These are sourced primarily
from conversations on IRC, but also include questions asked on the
httpd users mailing list (See :ref:`Chapter_Contributing_to_apache`,
**Contributing to the Apache HTTP Server**),
various third party forum websites like Stack Overflow,
questions asked in the documentation feedback mechanism, and
personal encounters at conferences and meetups.

All of the items in this book come from real-life situations,
encountered either by us or by other people who have asked for our help.
The topics range from basic compilation of the source code to complex
problems involving the treatment of URLs that require SSL
encryption.

We've collected more than two hundred different problems and their
solutions, largely based on how often they occurred, and have grouped them
roughly by subject as shown in :ref:`Whats_in_This_Book`.

Primarily, these recipes are useful to webmasters who are
responsible for the entire server; however, many are equally applicable to
users who want to customize the behavior in their own Web directories
through the use of **.htaccess** files.

We've written the Apache Cookbook to be a practical reference,
rather than a theoretical discourse: reading it recipe by recipe, chapter
by chapter, isn't going to reveal a plot ("Roy Fielding in the Library
with an RFC!" [#apacheckbk-PREFACE-2-FNOTE-1]_ ). It's intended to provide point solutions to specific
problems, located through the table of contents or the index.


.. _Whats_in_This_Book:

What's in This Book
-------------------

.. index:: What's in this book


Because much of the material in this book is drawn from
question-and-answer discussions and consultations, we have tried to make
it as complete as possible. Of course, this means that we have included
"recipes" for some questions to which there are currently no
satisfactory answers (at least to our knowledge). This has not been done
to tease, annoy, or frustrate you; such recipes are included to provide
completeness, so that you will know those problems have been considered
rather than ignored.

Very few problems remain insoluble forever, and these incomplete
recipes are the ones that will receive immediate attention on the book's
Web site and in revisions of the book. If a reader has figured out a way
to do something the book mentions but doesn't explain, or omits
mentioning entirely, our research team can be notified, and that 
solution will go on the Web site and in the next revision.

Who knows, you may be the one to provide such a solution!


.. _Platform_Notes:

Platform Notes
--------------

.. index:: Platform notes


The recipes in this book are geared toward two major platforms:
Unixish (such as Linux, Solaris, or BSD) and Microsoft Windows. There are
many that have no platform-specific aspects, and for those, any mention
of the underlying operating system or hardware is gratefully omitted.
Because of the authors' personal preferences and experiences, Unixish
coverage is more complete than that for the Windows platforms. However,
contributions, suggestions, and corrections for Windows-specific recipes
will be gladly considered for future revisions and inclusion on the Web
site.


.. _Other_Books:


Other Books
-----------

.. index:: Other books


.. todo:: It would be good to update this to reflect the many excellent books that are probably out there in the market that I'm not aware of.


There are a number of books currently in print that deal with the
      Apache Web server and its operation. Among them are:


* Apache: The Definitive Guide, Third
          Edition, by Ben and Peter Laurie (O'Reilly)

        
* Apache Administrator's Handbook by Rich
          Bowen, et al. (Macmillan)


* The Definitive Guide to Apache mod_rewrite, by Rich Bowen (Apress)


.. _Other_Sources:

Other Sources
-------------

.. index:: Other sources


In addition to books, there is a wealth of information available
online. There are Web sites, mailing lists, and Usenet newsgroups
devoted to the use and management of the Apache Web server. The Web
sites are limitless, but here are some active and useful sources of
information:

* The most important resource is the reference documentation, which can
be found at https://httpd.apache.org/docs/. Always check
here first, as we've worked hard to make sure that it is accurate,
comprehensive, and full of useful working examples.

* The pass:[<a class="email" href="mailto:users@httpd.apache.org"><em>users@httpd.apache.org</em></a>] mailing list is
populated with people who have varying degrees of experience with
the Apache software, and some of the Apache developers can be found
there, too. Posting is only permitted to subscribed participants. To
join the list, visit
https://httpd.apache.org/userslist.html, the mailing list
page in the httpd documentation.

* The pass:[<a class="email" href="mailto:dev@httpd.apache.org"><em>dev@httpd.apache.org</em></a>] mailing list is for
those of a more technical bent. If you're interested in
participating in the development of the server, or if you want
to discuss bugs or features in the server, the dev list is
probably the place to go. You'll get in-depth conversations
about how things work, but you'll be expected to know
something about C programming. To join the list, visit 
https://httpd.apache.org/userslist.html.

* The #httpd IRC channel on the
**irc.freenode.net** network—or on many other IRC
networks, for that matter. However, your chances of encountering us
are most likely on the freenode network.

* StackOverflow is a site where questions can be asked on a wide variety
of technical topics, and Apache httpd is one that gets quite a bit
of traffic. There's also a large archive of previously-answered
questions that you can search, as it's safe to assume that most of
the problems you'll encounter have been discussed already.

We must point out that all of these support forums are "staffed"
by volunteers. While we strive to help, it's on a "best effort"
basis - that is, we do the best we can, but there's no formal terms
of service, or expectation that your problems will necessarily be
fixed for you, like you'd get with a support contract.


.. _How_This_Book_Is_Organized:

How This Book Is Organized
--------------------------

.. index:: How this book is organized


This book is broken up into 22 chapters, as follows:

:ref:`Chapter_Installation`, **Installation**, covers the basics of installing the
Apache web server software, whether you're building from source,
or installing from packages, and whether it's on Microsoft
Windows, Linux, OSX, or something else. We'll cover the most basic
install, and also dig a little into how you might do a more
advanced installation.

:ref:`Chapter_My_First_Website`, **My First Website**, talks about putting 
up your very first website.
This includes some of the basics, such as editing a configuration
file, registering a domain name, and where to put your website
content files. While some of our audience can skip this chapter, we
had quite a bit of feedback from the previous editions asking for
this kind of recipes.

:ref:`Chapter_Common_modules`, **Adding Common Modules**,
describes the details of installing,
configuring, and using, several popular third-party modules,
including mod_php, mod_security, and several others. The chapter
also includes generic instructions that apply to many other
third-party modules that have less complex installation needs.

:ref:`Chapter_Logging`, **Logging**, discusses the Apache web server's many logging
modules, from basic access logging, to error logging and detailed
debug logging.

:ref:`Chapter_Virtual_hosts`, **Virtual Hosts**,
tells you how to run multiple Web sites
using a single Apache http server and set of configuration files.

:ref:`Chapter_URL_Mapping`, **URL Mapping**,
discusses the process - called URL Mapping, by which Apache httpd
maps a URL - the string that appears in the address bar of your
browser - into actual content that is sent back to the client. Because
this is a large topic, this chapter covers the main concepts, while
specific sub-topics, like directory listings and mod_rewrite, are
covered in their own chapters.

:ref:`Chapter_Directory_listing`, **Directory Listing**, is 
about mod_dir, which is the module
that can display a directory listing for a particular directory. In
this chapter, you'll learn how to customize that directory listing in
various ways.

:ref:`Chapter_regex`, **Introduction to regular expressions**, is not like
the other chapters in this book. It's a digression from the usual
Question and Answer format of the book, to provide an introduction to
regular expressions. This is done in order that chapters that
follow, especially  :ref:`Chapter_mod_rewrite`, **URL Rewriting with mod_rewrite**,
and :ref:`Chapter_per_request`, **Programmable Configuration**, may proceed
without spending time on these topics. If you're already familiar with
regular expressions, you can probably skip this chapter entirely.

:ref:`Chapter_mod_rewrite`, **URL Rewriting with mod_rewrite**,
talks about URL rewriting using mod_rewrite.
This is a complex module, and the source of a large percentage of the
questions that appear on Apache httpd question-and-answer forums, so
merits its own chapter.

:ref:`Chapter_userdir`, **User Directories**, is for 
recipes about allowing system users to
serve content out of their home directories, rather than having to
give them access to the main content tree.

:ref:`Chapter_per_request`, **Programmable Configuration**,
covers the **per**-request configuration syntax
that is new in Apache httpd 2.4, and allows for request-time
conditional configuration. Also, it covers mod_macro, which gives the
ability to script your configuration files.

:ref:`Chapter_htaccess`, **.htaccess Files**, 
discusses .htaccess files - the **per**-directory
configuration files which give users the ability to modify the
configuration of the server on a **per**-directory basis, without having
access to the main server configuration file.

:ref:`Chapter_AAA`, **Authentication, Authorization, and Access Control**,
covers selectively granting or denying access to
various portions of your web site content based on various conditions,
including, but not limited to, usernames and passwords. 

:ref:`Chapter_Security`, **Security**, covers some security precautions that 
you need to take to prevent common security attacks against your website.
Security is an enormous topic, and this doesn't attempt to cover it
comprehensively, but, rather, to show you what you need to do
specifically on your Apache http server as part of an overall security
posture.

:ref:`Chapter_SSL_and_TLS`, **SSL and TLS**,
addresses the issues of making your Apache Web server capable of
handling secure transactions with SSL-capable browsers—a must if you're
going to be handling sensitive data such as money transfers or medical
records.

:ref:`Chapter_Dynamic_content`, **Dynamic Content**, talks about generating content "on the
fly" using a variety of technologies including CGI, PHP, Server Side
Includes, and so on.

:ref:`Chapter_Filters_And_Handlers`, **Filters and Handlers**, covers the
various handlers and filters that come as part of the Apache http
server, and how you can use them. This includes content compression
with mod_deflate, imagemap handling with mod_imagemap, and others.

:ref:`Chapter_Proxies`, **Proxies**,
describes how to configure your Apache server to act as a proxy between
users and Web pages and make the processes as transparent and seamless
as possible.

:ref:`Chapter_info_and_status`, **mod_info and mod_status**, covers the
incredibly useful modules mod_info and mod_status, which give you, as
the server administrator, a glimpse into the condition of your
servers, and what they're doing.

:ref:`Chapter_Troubleshooting_and_error_handling`, *Troubleshooting and
Error Handling*, describes how to customize the Web
server's error messages to give your site its own unique flavor, and
also how to deal with commonly-occurring error conditions.

:ref:`Chapter_Performance_and_testing`, **Performance and Testing**,
includes a number of recipes for
addressing performance bottlenecks and improving the overall function of
your Apache server. It also covers several tools for testing your
server's performance, and other functionality.

:ref:`Chapter_Contributing_to_apache`, **Contributing to the Apache HTTP Server**,
covers what's involved in contributing to the Apache http server
project. Apache httpd is open source, which means that it is built by
the volunteer effort of the people that rely on the server. That is,
people like you and me. If there's some change you want to make to the
code, the documentation, the website, or any other aspect of the
project, this chapter will help you find your way into the community.


.. _Conventions_Used_in_This_Book:

Conventions Used in This Book
-----------------------------

.. index:: Conventions used in this book


Throughout this book certain stylistic conventions are followed.
Once you are accustomed to them, you can easily distinguish between
comments, commands you need to type, values you need to supply, and so
forth.

In some cases, the typeface of terms in the main text will be
different and likewise in code examples. The details of what the
different styles (italic, boldface, etc.) mean are described in the
following sections.


.. _Programming_Conventions:

Programming Conventions
~~~~~~~~~~~~~~~~~~~~~~~


In this book, most case examples of code will be in the form of
excerpts from scripts, rather than actual application code. When
commands need to be issued at a command-line prompt (such as an xterm
for a Unixish system or a DOS command prompt for Windows), they will
look something like this:


.. code-block:: text

   % find /usr/local -name apachectl -print
   # /usr/local/apache/bin/apachectl graceful
   C:> cd "\Program Files\Apache Group\Apache\bin"
   C:\Program Files\Apache Group\Apache\bin> apache -k stop


On Unixish systems, command prompts that begin with ``#`` indicate that 
you need to be logged in as the superuser (root username); if the 
prompt begins with ``%``, then the command can be used by any user. In
this book, we tend to prefer the use of ``sudo`` to execute commands
that need root privileges, which is considered best security practice.


.. _Typesetting_Conventions:

Typesetting Conventions
~~~~~~~~~~~~~~~~~~~~~~~


The following typographic conventions are used in this book:

**Italic**:: 
              Used for commands, filenames, abbreviations, citations of
              books and articles, email addresses, URLs, and Usenet group
              names.

Bold:: 
              Used for labeling menu choices in a graphical
              interface.

``Constant Width``:: 
              Used for function names, command options, computer output,
              environment variable names, literal strings, and code
              examples.


**``Constant Width Bold``**:: 
              Used for user input in computer dialogues and
              examples.


**``Constant Width Italic``**:: 
              Used for replaceable parameters, filesystem paths, and
              variable names.


.. _apacheckbk-PREFACE-2-NOTE-65:


.. tip::

   This icon signifies a tip, suggestion, or cool trick.


.. note::

   This icon signifies an additional note, or related information.


.. _apacheckbk-PREFACE-2-NOTE-66:


.. warning::

   This icon indicates a warning, caution, such as pointing out something
   that could go wrong.


.. _Documentation_Conventions_id103636:

Documentation Conventions
~~~~~~~~~~~~~~~~~~~~~~~~~


Because the topics covered in this book have been written about
extensively both online and in print, there are different sources of
information to which it will refer you. The most common ones are as
follows:


.. _The_online_manual_man_pages_on_a_Unixish_system_id103655:

The online manual ("man") pages on a Unixish system
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


References to the manpages will appear something like, "For
more information, see the **kill(1)** manpage." The
number in parentheses is the manual section; you can access this
page with a command such as:


.. code-block:: text

   % man 1 kill


.. _The_Apache_web_server_documentation_id103686:

The Apache Web server documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Such a reference may appear as "See the ``mod_auth`` 
documentation for details." This refers to a Web page like:


https://httpd.apache.org/docs/mod/mod_auth.html

In some cases, the reference will be to a specific Apache
directive rather than an actual module; in cases like this, you can
locate the appropriate Web page by looking up the directive name
on:


https://httpd.apache.org/docs/mod/quickreference.html

This page lists all of the directives available in the
standard Apache package. In some situations, the directive may be
specific to a nonstandard or third-party module, in which case the
documentation should be located wherever the module itself was
found. The links above are for the documentation for the latest
released version of the software - Version 2.4 as of this
writing. To access the documentation for earlier versions,
replace "**/docs/**" with the specific version, 
such as  "**/docs/2.2/**" in the URLs.


.. _Using_Code_Examples:

Using Code Examples
-------------------

.. index:: Using code examples


This book is here to help you get your job done. In general, you
may use the code in this book in your programs and documentation. You do
not need to contact us for permission unless you're reproducing a
significant portion of the code.

All code examples in this book are licensed under the Apache License,
Version 2.0. See the LICENSE file for details.

We appreciate, but do not require, attribution. An attribution
usually includes the title and author. For example:
"**Apache Cookbook**, Fourth Edition, by Rich Bowen.
Copyright 2004–2026 Rich Bowen."


.. _Wed_Like_to_Hear_from_You:

We'd Like to Hear from You
--------------------------

.. index:: We'd like to hear from you

.. index:: Contacting us


We have tested and verified the information in this book to the
best of our ability, but you may find that features have changed (which
may in fact resemble bugs). Please let us know about any errors you
find, as well as your suggestions for future editions, by filing an
issue or pull request on the book's GitHub repository:

https://github.com/rbowen/apache-cookbook

You can also reach Rich Bowen directly at rbowen@rcbowen.com.


.. _Acknowledgments:

Acknowledgments
---------------

.. index:: Acknowledgements


Originally, each recipe was going to be individually attributed,
but that turned out to be logistically impossible.

Many people have helped us during the writing of this book, by
posing a problem, providing a solution, proofreading, reviewing,
editing, or just (!) providing moral support. This multitude, to each of
whom we are profoundly grateful, includes ...
      


.. _Ken_Coar_id103929:

Ken Coar
~~~~~~~~


I dedicate this book to:

* My significantly better half, Cathy Coar, who has performed
  Heraclean feats of love and support on my behalf for more than three
  decades;

* My father, who never gave up the struggle to make me understand that
  I could do better; and

* All those individuals who have striven, through their coding, use,
  and/or feedback, to keep the Apache Web server a living, growing
  exemplar of what open software can be.

The earlier editions of this book benefited from the excellent team
at O'Reilly Media, whose patience and professionalism were remarkable. Our technical reviewers
provided much excellent feedback and helped make this a better book.

The people who have worked on the Apache Web server
documentation, and the people who develop the software itself, get a
big note of thanks, too; without the former, collating a lot of the
information in this book would have been a whole lot more difficult,
and without the latter, the book wouldn't have happened at all.

The users of the software, whose frequently challenging
questions populate the mailing lists, the IRC channels, and our
inboxes, deserve thanks for all the inspiration they unwittingly
provided for the recipes in this book.

But foremost among those to whom I owe gratitude is the first
individual to whom I dedicate this work: my wife Cathy,
without whose patience, support, and constructive criticism I would
never have achieved what I have.


.. _Rich_Bowen:

Rich Bowen
~~~~~~~~~~


This book is dedicated:

To my muses, Rhiannon, Ray, and Marguerite.

Also, to the members of the Apache httpd PMC, and the members of the
Apache Software Foundation, for their years of enriching my life, not
to mention my career.

To the kind strangers who took me under their wings when I stumbled
across Apache httpd back in the early 90s - Ken Coar, Jim Jagielski,
and Sally Khudairi - and who have become my friends as well as my
mentors.

To the denizens of the ``#httpd`` IRC channel on Freenode. You provided
most of the questions here, as well as hours and days and years of
fine-tuning the answers. This book would literally not exist without
you.

To the wonderful people we worked with at O'Reilly on earlier editions,
especially Ally MacDonald, who put up with our painfully slow progress
for more than 3 years.

To Terry Pratchett, Arthur C. Clarke, and Ray Bradbury, who told me the 
stories that got me writing in the first place. I miss you.

To Maria, who makes everything beautiful. 
And so that was all right, Best Beloved. Do you see?


.. rubric:: Footnotes

.. [#apacheckbk-PREFACE-2-FNOTE-1] An obscure reference to a board game called Clue and a somewhat less obscure developer of HTTP.
