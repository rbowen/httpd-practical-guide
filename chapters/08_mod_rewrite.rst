
.. _Chapter_mod_rewrite:

==============================
URL Rewriting with mod_rewrite
==============================

.. index:: mod_rewrite

.. index:: Modules,mod_rewrite

.. index:: URL Rewriting

.. index:: Rewrite

.. index:: Regex,mod_rewrite

.. index:: Regular expressions,mod_rewrite

.. index:: SEO

.. index:: Search Engine Optimization


In the previous chapter, :ref:`Chapter_regex`, *Introduction to Regular
Expressions*, you learned about regular
expressions. In this chapter, you'll learn about the most important
use of regex in the Apache httpd - URL rewriting with mod_rewrite.

``mod_rewrite`` is the most powerful, and perhaps the most misunderstood,
module in the Apache web server. It's primary purpose is to manipulate
and rewrite requests into other request, based on a wide variety of
conditions and variables.

``mod_rewrite`` is often referenced in the context of SEO - Search Engine
Optimization. SEO is the science of getting your website noticed by
search engines, and thus improving your business performance by
getting higher rankings when people search for relevant keywords. It
should be clearly understood that mastering mod_rewrite is not a
guarantee that your website will be number one in Google search
results. SEO is part science, part wishful thinking. Getting high
website rankings has more to do with having valuable content than
having so-called beautiful URLs.

However, having URLs that people can remember, read over the phone,
and type in easily, has a real value, and many of the techniques
covered in this chapter will help you towards that goal.


.. _Recipe_rewrite-syntax:

Syntax of the RewriteRule directive
-----------------------------------

.. index:: RewriteRule,syntax


.. _Problem_rewrite-syntax:

Problem
~~~~~~~


You're confused about the syntax of the RewriteRule directive.


.. _Solution_rewrite-syntax:

Solution
~~~~~~~~


Study the following:

``RewriteRule`` **pattern** **target** [FLAGS]


.. _Discussion_rewrite-syntax:

Discussion
~~~~~~~~~~


The ``RewriteRule`` directive takes two required arguments and one
additional option argument.

The **pattern** argument is a regular expression which is compared to
the requested URI. 


.. warning::

   The pattern is **not** applied to the Query String - just to the base
   URI. If you want to match something in the query string, see
   :ref:`Recipe_rewrite-by-query-string` for how to do that.


If the pattern matches, then the URI is rewritten
to the place indicated by the **target** argument. 

There's one special
case - if you set the pattern to just ``-`` (dash) rather than a URI or
file path, then no rewriting is done at all. You'll do this when you
want to have the side-effects of the rewrite flags that you're using,
and don't really want to rewrite. For example, if you want to deny a
request (that is, return a FORBIDDEN response), you'd use the ``[F]``
flag, and the target of the rewrite doesn't matter, because the
end-user is just receiving an error message.


.. code-block:: text

   RewriteRule command\.exe - [F]


The (optional) flags argument provides hints to the rewrite engine as
to modifications to make to the rewriting, such as whether the
**target** is a URI or a directory path, whether the target should be
passed through proxying, and many other considerations.

Finally, remember that the ``RewriteRule`` directive will only be
honored in a scope where the ``RewriteEngine`` directive is set to ``on``.
You can turn this on globally for your entire server, or just for a
particular virtual host, directory, or ``.htaccess`` file. When in
doubt, add the following before your ``RewriteRule``s:


.. code-block:: text

   RewriteEngine On


.. _See_Also_rewrite-syntax:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_rewrite.html#rewriterule

* :ref:`Recipe_rewrite-by-query-string`

* :ref:`Recipe_rewrite-flags`


.. _Recipe_simple-rewrite:

Rewriting one URL to another
----------------------------

.. index:: RewriteRule

.. index:: Transparent rewrite

.. index:: Rewriting one URL to another


.. _Problem_simple-rewrite:

Problem
~~~~~~~


You want to transparently rewrite one URL to another. That is, when a
user requests ``/one``, you want to serve them the contents of the URL
``/two`` without them noticing a change in the browser address bar.


.. _Solution_simple-rewrite:

Solution
~~~~~~~~


While you could simply redirect one URL to the other, there are times
when you want to avoid displaying the new URL to the client browser by
doing a HTTP redirect.

Use ``RewriteRule`` to do an internal mapping:


.. code-block:: text

   RewriteRule ^/one /two [PT]


.. _Discussion_simple-rewrite:

Discussion
~~~~~~~~~~


Usually, when you want to redirect one URL to another, the ``Redirect``
directive is the right way to go. See :ref:`Recipe_Redirect` for examples
of how to do that.

The ``[PT]`` flag will be discussed in more detail in
:ref:`Recipe_rewrite-pt`. For the purposes of this recipe, we'll just say
that it serves to make the rewrite transparently pass from one URL to
another.

Also, note that this directive is intended to go in your ``httpd.conf``
* your main server configuration file. In a ``.htaccess`` file, the syntax
for this rewrite is going to be slightly different:


.. code-block:: text

   RewriteRule ^one two [PT]


The difference, as you can see on close examination, is the removal of
the leading slashes. The difference between
``RewriteRule`` in ``.htaccess`` files and in the main server
configuration file is discussed in more detail in
:ref:`Recipe_rewrite-htaccess`, **URL Rewriting with mod_rewrite**, and
also in :ref:`Chapter_htaccess`, **.htaccess Files**.


.. _See_Also_simple-rewrite:

See Also
~~~~~~~~


* :ref:`Chapter_htaccess`, **.htaccess Files**

* :ref:`Chapter_regex`, **Introduction to Regular Expressions**

* http://httpd.apache.org/docs/mod/mod_rewrite.html#rewriterule

* :ref:`Recipe_rewrite-pt`


.. _Recipe_rewrite-htaccess:

Using RewriteRule in .htaccess files
------------------------------------

.. index:: Rewrite,htaccess

.. index:: htaccess,Rewrite

.. index:: Using RewriteRule in .htaccess files


.. _Problem_rewrite-htaccess:

Problem
~~~~~~~


Why doesn't my ``RewriteRule`` work in an .htaccess file?


.. _Solution_rewrite-htaccess:

Solution
~~~~~~~~


Ensure that any leading slashes, or directory paths, are removed from
the ``RewriteRule`` patterns.


.. _Discussion_rewrite-htaccess:

Discussion
~~~~~~~~~~


``.htaccess`` files are per-directory configuration files, allowing you
to override the main server configuration for a single directory. They
are discussed at length in :ref:`Chapter_htaccess`, **.htaccess Files**.

Doing anything in a per-directory scope (**i.e.**, either in a ``.htaccess``
file or in a ``<Directory>`` block) can have some side effects which, if
not clearly understood, can cause some confusing behavior.

In particular, when using ``RewriteRule`` in ``.htaccess`` files, you need
to remember that leading path information is removed from the URL path
before the ``RewriteRule`` pattern is applied.

For example, consider the following ``RewriteRule``:


.. code-block:: text

   # In httpd.conf
   RewriteRule ^/images/(.+)\.jpg /images/$1.png


This rule rewrites requests for ``.jpg`` images, and rewrites them to a
same-named ``.png`` files. So far so good.

However, in a ``.htaccess`` file placed in the document root of your
site, the leading slash is removed. That is to say, the ``RewriteRule``
placed in this ``.htaccess`` file assumes that all paths are relative to
its own location. Thus:


.. code-block:: text

   # In .htaccess in root dir
   RewriteRule ^images/(.+)\.jpg images/$1.png


Note that this is identical to the earlier example, except for the
missing slash before ``images``.

Next, consider if we place this ``.htaccess`` file directly in the
``images`` subdirectory:


.. code-block:: text

   # In .htaccess in images/
   RewriteRule ^(.+)\.jpg $1.png


This time, note that not only is the leading slash removed, but also
the ``images/``. Once again, the same rule applies - ``RewriteRule``
placed in a ``.htaccess`` file assumes that all paths are relative to
its own location.

In a best-case scenario, avoiding ``.htaccess`` files entirely is
preferred, for reasons discussed at greater length in
:ref:`Chapter_htaccess`, **.htaccess Files**. However, if you are compelled to use ``.htaccess``
files, remember that all paths are assumed to be relative to the
directory that you're working in, and everything else will make sense.

Finally, if you continue to have difficulties getting your patterns to
match, your next step is to look at the rewrite log file, which is
discussed in :ref:`Recipe_rewrite-logging`.


.. _See_Also_rewrite-htaccess:

See Also
~~~~~~~~


* :ref:`Chapter_htaccess`, **.htaccess Files**

* :ref:`Recipe_rewrite-logging`


.. _Recipe_rewrite-flags:

What do the RewriteRule flags mean?
-----------------------------------

.. index:: RewriteRule,flags

.. index:: Rewrite,flags

.. index:: Flags,mod_rewrite

.. index:: mod_rewrite,flags


.. _Problem_rewrite-flags:

Problem
~~~~~~~


I would like to understand what the various flags mean on the end of
``RewriteRule`` directives.


.. _Solution_rewrite-flags:

Solution
~~~~~~~~


.. _Rewrite-flags-definitions:


**RewriteRule flags**


+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Flag and syntax   | Function                                                                                                                                                                                           |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| B                 | Escape non-alphanumeric characters before applying the transformation.                                                                                                                             |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| C                 | Rule is chained to the following rule. If the rule fails, the rule(s) chained to it will be skipped.                                                                                               |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CO=NAME:VAL       | Sets a cookie in the client browser. Full syntax is: CO=NAME:VAL:domain[:lifetime[:path[:secure[:httponly]]]]                                                                                      |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| DPI               | Causes the PATH_INFO portion of the rewritten URI to be discarded.                                                                                                                                 |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| END               | Stop the rewriting process immediately and don't apply any more rules. Also prevents further execution of rewrite rules in **per**-directory and .htaccess context. (Available in 2.3.9 and later) |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| E=[!]VAR[:VAL]    | Causes an environment variable VAR to be set (to the value VAL if provided). The form !VAR causes the environment variable VAR to be unset.                                                        |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| F                 | Returns a 403 FORBIDDEN response to the client browser.                                                                                                                                            |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| G                 | Returns a 410 GONE response to the client browser.                                                                                                                                                 |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| H=Content-handler | Causes the resulting URI to be sent to the specified Content-handler for processing.                                                                                                               |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| L                 | Stop the rewriting process immediately and don't apply any more rules. Especially note caveats for **per**-directory and .htaccess context (see also the END flag).                                |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| N                 | Re-run the rewriting process, starting again with the first rule, using the result of the ruleset so far as a starting point.                                                                      |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| NC                | Makes the pattern comparison case-insensitive.                                                                                                                                                     |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| NE                | Prevent mod_rewrite from applying hexcode escaping of special characters in the result of the rewrite.                                                                                             |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| NS                | Causes a rule to be skipped if the current request is an internal sub-request.                                                                                                                     |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| P                 | Force the substitution URL to be internally sent as a proxy request.                                                                                                                               |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| PT                | Forces the resulting URI to be passed back to the URL mapping engine for processing of other URI-to-filename translators, such as Alias or Redirect.                                               |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| QSA               | Appends any query string from the original request URL to any query string created in the rewrite target.                                                                                          |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| QSD               | Discard any query string attached to the incoming URI.                                                                                                                                             |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| R[=code]          | Forces an external redirect, optionally with the specified HTTP status code.                                                                                                                       |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| S=num             | Tells the rewriting engine to skip the next num rules if the current rule matches.                                                                                                                 |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| T=MIME-type       | Force the MIME-type of the target file to be the specified type.                                                                                                                                   |
+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


.. _Discussion_rewrite-flags:

Discussion
~~~~~~~~~~


A flag placed at the end of a ``RewriteRule`` influences the manner 
in which the pattern is applied to the URL, or the manner in which the
substitution is applied. While there are a large number of flags to
keep track of, there's really only a few of them that you'll become
intimately familiar with, so don't worry if the table above seems a
little overwhelming.

Some of these flags are used without arguments, like ``[PT]`` or
``[QSA]``, while others can take an argument, like ``[R=307]`` to do a
Temporary Redirect, or ``[S=7]`` to skip the next 7 ``RewriteRule``
directives.

Still others, such as the ``[CO]`` flag, accept several arguments. See
:ref:`Recipe_rewrite-cookie-flag` for more details on that one.

Many of the flags have a long form, as well as the shorter form.
For example, you can use the
flag ``[forbidden]`` rather than ``[F]``, if you want additional clarity.
However, these are hardly ever actually used in practice.


.. _See_Also_rewrite-flags:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/rewrite/flags.html

* The next few rules, which discuss specific individual flags.


.. _Recipe_rewrite-pt:

Rewrite to a local URL
----------------------

.. index::  [PT\] 

.. index:: Rewrite Flags,[PT\] 

.. index:: RewriteRule,flags,[PT\]

.. index:: Rewrite,flags,[PT\]


.. _Problem_rewrite-pt:

Problem
~~~~~~~


By default, ``RewriteRule`` attempts to rewrite to a file path. Usually,
however, we want it to rewrite to a local URL.


.. code-block:: text

   RewriteRule ^/productID/(\d+) /product_lookup.php?id=$1 [PT]


.. _Solution_rewrite-pt:

Solution
~~~~~~~~


Use the ``[PT]`` flag to indicate to ``RewriteRule`` that the target is a
URL, not a file path, and so should be passed through the URL mapping
process.


.. _Discussion_rewrite-pt:

Discussion
~~~~~~~~~~


Something that surprises many beginning users of ``mod_rewrite`` is that
``RewriteRule``, by default, rewrites to a file path, not to a URL. Most
of the time, this is invisible, since the file path is often identical
to the URL. However, sometimes it makes a difference. The main two
cases where it matters is when the target URL is an alias that is not
identical to a physical file path, and when the target is something
that requires additional processing, such as a CGI script, or a PHP
program.

In the case of the former, the rewrite will result in a `File Not
Found`` error message, because the ``Alias` doesn't correspond to an
actual on-disk file directly.

The latter case is even more troublesome, because, in certain
conditions, you may end up serving the source code of, say, a PHP
file, directly to the end-user, rather than having it processed by the
PHP handler.

The ``[PT]`` flag tells the Rewrite engine that the resulting target is
a URL, and that it needs to be re-mapped to a resource. This causes it
to get passed back to the URL mapping phase, which then applies
whatever mapping was intended, such as ``Alias`` evaluation, mapping to
handlers, and so on.

The ``[PT]`` flag is your greatest ally in getting ``RewriteRule`` to do
what you meant. We recommend you use it liberally.


.. _See_Also_rewrite-pt:

See Also
~~~~~~~~


* :ref:`Chapter_URL_Mapping`, **URL Mapping**

* http://httpd.apache.org/docs/rewrite/flags.html#flag_pt


.. _Recipe_rewrite-env-flag:

Setting environment variables with RewriteRule
----------------------------------------------

.. index::  [E\] 

.. index:: Rewrite Flags,[E\] 

.. index:: RewriteRule,flags,[E\] 

.. index:: Rewrite,flags,[E\]


.. _Problem_rewrite-env-flag:

Problem
~~~~~~~


You want to set an environment variable as a side-effect of a
``RewriteRule``.


.. _Solution_rewrite-env-flag:

Solution
~~~~~~~~


Use the ``[E]`` flag to specify the variable, and the value you wish to
set it to. This environment variable will then be available for the
remainder of the request's lifetime.


.. code-block:: text

   RewriteRule "\.(png|gif|jpg)$" "-" [E=image:1]
   CustomLog "logs/access_log" combined env=!image


.. _Discussion_rewrite-env-flag:

Discussion
~~~~~~~~~~


The syntax of the ``[E]`` flag is as follows:


.. code-block:: text

   [E=VAR:VAL]
   [E=!VAR]


That is, you must provide the name of the variable which you want to
set, and the value to which you want to set it. Or, if you prefix the
variable name with ``!``, then the variable is unset.

In the example given in the solution, an environment variable named
``image`` is set to a value of 1. This variable can then be checked
later. In the example we're using it in a ``CustomLog`` directive to
determine whether the request was for an image. In this specific
case, the result is that we decline to log request for images.

Environment variables you set in ``RewriteRule`` directives can also be
used in your dynamic content handlers, such as CGI or PHP.


.. tip::

   Relying on rewrite-set environment variables in your CGI or PHP
   programs can make it very hard to troubleshoot problems. It also can
   lead to the situation where the behavior of a program appears magical
   to someone encountering it for the first time. Be sure to clearly
   document, in your PHP code (or wherever you are relying on it), what
   you are relying on, and how the variable is set. Your future self will
   thank you.


.. _See_Also_rewrite-env-flag:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/rewrite/flags.html#flag_e


.. _Recipe_rewrite-handler-flag:

Setting a particular handler with RewriteRule
---------------------------------------------

.. index::  [H\] 

.. index:: Rewrite Flags,[H\] 

.. index:: RewriteRule,flags,[H\] 

.. index:: Rewrite,flags,[H\]


.. _Problem_rewrite-handler-flag:

Problem
~~~~~~~


You want to route a request to a particular handler with a
``RewriteRule``.


.. _Solution_rewrite-handler-flag:

Solution
~~~~~~~~


Use the ``[H]`` flag to specify which handler you wish to process a
rewritten request. In the following example, we are forcing all files
without a file extension to be handled by ``mod_php``.


.. code-block:: text

   RewriteRule "!\." "-" [H=application/x-httpd-php]


.. _Discussion_rewrite-handler-flag:

Discussion
~~~~~~~~~~


The ``[H]`` flag is useful for mapping a request to a particular
handler, which might not have happened automatically by other means.
In the example shown here, we want every file that doesn't have a file
extension to automatically be handled by ``mod_php``, without having to
have ``.php`` in either the file name or the URL.

The ``AddHandler`` directive is the way to associate a handler with a
particular file extension, while the ``SetHandler`` directive is the way
to associate a handler with a ``<Directory>`` or ``<Location>``.

But you'll want to use the ``[H]`` flag when the usual methods for
setting a handler aren't appropriate. Handlers are discussed further
in :ref:`Chapter_Filters_And_Handlers`, **Filters and Handlers**.


.. _See_Also_rewrite-handler-flag:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/rewrite/flags.html#flag_h

* http://httpd.apache.org/docs/mod/core.html#sethandler

* http://httpd.apache.org/docs/mod/core.html#addhandler

* :ref:`Chapter_Filters_And_Handlers`, **Filtes and Handlers**


.. _Recipe_rewrite-next-flag:

Global search and replace with RewriteRule
------------------------------------------

.. index::  [N\] 

.. index:: Rewrite Flags,[N\] 

.. index:: RewriteRule,flags,[N\] 

.. index:: Rewrite,flags,[N\]

.. index:: Search and replace in a URL


.. _Problem_rewrite-next-flag:

Problem
~~~~~~~


You want to replace all occurrences of a particular character in a URL
with another. For example, replace every ``-`` with a ``_``\ - that is,
replace all dashes with underscores.


.. _Solution_rewrite-next-flag:

Solution
~~~~~~~~


Use the ``[N]`` flag to continue replacing until they're all done:


.. code-block:: text

   RewriteRule (.*)-(.*) $1_$2 [N]


.. _Discussion_rewrite-next-flag:

Discussion
~~~~~~~~~~


The ``[N]`` flag tells the rewrite engine to go back to the top of the
rewrite rule set and start over. In this case, if the rule finds a ``-``
in the requested URI, it will replace it with a ``_``\, and then start
over again. This will continue as long as it still finds a ``-`` in the
requested URI. Thus, the end result is a global search and replace of
a particular character.

This could be useful, for example, if you had a brochure printed in
which underscores were mistakenly printed as dashes, and you want the
original URLs to continue working.

When using this technique, more generally, to replace ``string1`` with
``string2``, take care to avoid looping, if, for example, one string is
a substring of the other.


.. _See_Also_rewrite-next-flag:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/rewrite/flags.html#flag_n

* :ref:`Recipe_rewrite-looping`


.. _Recipe_rewrite-nc-flag:

Case-insensitive matching with RewriteRule
------------------------------------------

.. index::  [NC\] 

.. index:: Rewrite Flags,[NC\] 

.. index:: RewriteRule,flags,[NC\] 

.. index:: Rewrite,flags,[NC\]


.. _Problem_rewrite-nc-flag:

Problem
~~~~~~~


You want your ``RewriteRule`` to be case insensitive. That is, you want
it to work whether the URL is uppercase or lowercase.


.. _Solution_rewrite-nc-flag:

Solution
~~~~~~~~


Use the ``[NC]`` flag to make matching case insensitive.


.. code-block:: text

   RewriteRule /puppies /small-dogs [NC,R,L]


.. _Discussion_rewrite-nc-flag:

Discussion
~~~~~~~~~~


By default, URLs are case sensitive. That is, the URL
``http://www.example.com/puppies`` is a different resource than
``http://www.example.com/Puppoes``. However, it happens to all of us at
some point that a URL either gets put into a link incorrectly, or
perhaps goes into a print publication incorrectly, and we need it to
just work. This will happen occasionally when someone puts a URL into
an advertisement, and makes it all caps for effect, for example.

The ``[NC]`` flag ensures that a particular ``RewriteRule`` is compared
without caring whether the match is uppercase or lowercase.

If you want URLs in general to be case-insensitive on your server,
consider using ``mod_speling`` instead. See :ref:`Recipe_mod_speling` for a
discussion of that module.


.. _See_Also_rewrite-nc-flag:

See Also
~~~~~~~~


* :ref:`Recipe_mod_speling`

* http://httpd.apache.org/docs/rewrite/flags.html#flag_nc


.. _Recipe_rewrite-cookie-flag:

Setting a cookie with RewriteRule
---------------------------------

.. index::  [CO\] 

.. index:: Rewrite Flags,[CO\] 

.. index:: RewriteRule,flags,[CO\] 

.. index:: Rewrite,flags,[CO\]

.. index:: Cookies

.. index:: Setting a cookie with RewriteRule


.. _Problem_rewrite-cookie-flag:

Problem
~~~~~~~


You want to set a cookie as a side-effect of a ``RewriteRule``.


.. _Solution_rewrite-cookie-flag:

Solution
~~~~~~~~


Use the ``[CO]`` flag to return a cookie to the client.


.. code-block:: text

   RewriteRule ^/index.html /index.php [CO=frontdoor:yes:.example.com:1440:/]


.. _Discussion_rewrite-cookie-flag:

Discussion
~~~~~~~~~~


The ``[CO]`` takes a number of arguments, some of which are optional:


.. code-block:: text

   [CO=NAME:VALUE:DOMAIN:lifetime:path:secure:httponly]


The arguments that appear in upper-case above are required. The others
are optional. However, if you provide any argument, you must provide
all the preceeding arguments, since the meaning of a variable is
determined by the ordering. That is, if you provide a path argument,
you must also provide the lifetime argument before it.

The meaning of each argument is as follows:


.. _CO-flag-arguments:


**Cookie Flag Arguments**


+----------+-----------------------------------+
| Argument | Meaning                           |
+----------+-----------------------------------+
| Name     | The name of the cookie to be set  |
+----------+-----------------------------------+
| Value    | The value to which it will be set |
+----------+-----------------------------------+
| Domain   |                                   |
+----------+-----------------------------------+
| Lifetime |                                   |
+----------+-----------------------------------+
| Path     |                                   |
+----------+-----------------------------------+
| Secure   |                                   |
+----------+-----------------------------------+
| httponly |                                   |
+----------+-----------------------------------+


.. _See_Also_rewrite-cookie-flag:

See Also
~~~~~~~~


* https://tools.ietf.org/html/rfc6265

* http://httpd.apache.org/docs/rewrite/flags.html#flag_co


.. _Recipe_rewrite-qsa-flag:

Retaining a query string with RewriteRule
-----------------------------------------

.. index::  [QSA\] 

.. index:: Rewrite Flags,[QSA\]

.. index:: RewriteRule,flags,[QSA\] 

.. index:: Rewrite,flags,[QSA\]

.. index:: Query string


.. _Problem_rewrite-qsa-flag:

Problem
~~~~~~~


When you set a query string as part of a ``RewriteRule``, any existing
query string is discarded. You want to retain any query string sent by
the client.


.. _Solution_rewrite-qsa-flag:

Solution
~~~~~~~~


Use the ``[QSA]`` (Query String Append) flag to indicate that you want to retain the
client-supplied query string:


.. code-block:: text

   RewriteRule ^/product/(\d+) /product.php?id=$1 [QSA]


.. _Discussion_rewrite-qsa-flag:

Discussion
~~~~~~~~~~


Without the ``[QSA]`` flag, the above ``RewriteRule`` would set the
specified query string (``?id=$1``) and discard any query string that
had been supplied by the browser. This is often what you want.
However, if you want the client to be able to supply additional query
string arguments, and have they survive the rewrite, the ``[QSA]`` flag
is required.

``QSA`` stands for Query String Append, and this is exactly what
happens - that is, the client-supplied query string will be appended
to the end of the query string that the ``RewriteRule`` creates.

For example, in the above case, a request for the URI
``/product/148?sort=alpha`` will be mapped to
``/product.php?id=148&sort=alpha``.


.. warning::

   Because you are retaining the query string supplied by the client, it
   may be possible for the client to override your rewrite by supplying
   the right query string. Consider, for example, if, in the above case,
   the client requested the URI ``/product/148?id=734``. The ``RewriteRule``
   would map this request to ``/product.php?id=148&id=734``. You must be
   aware of this in your application code, and take care in which order
   you process the arguments, so that a malicious client can't circumvent
   some restriction you have in place - such as, in this case, peeking at
   product IDs that they're not supposed to see.


.. _See_Also_rewrite-qsa-flag:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/rewrite/flags.html#flag_qsa


.. _Recipe_RewriteCond:

RewriteCond - Conditionally running a RewriteRule
-------------------------------------------------

.. index:: RewriteCond

.. index:: RewriteRule,conditional


.. _Problem_RewriteCond:

Problem
~~~~~~~


You want to make your ``RewriteRule`` conditional upon some other
variable.


.. _Solution_RewriteCond:

Solution
~~~~~~~~


Use one or more ``RewriteCond`` conditions to impose another condition on the rewrite.


.. code-block:: text

   RewriteCond %{HTTP_USER_AGENT} iPhone
   RewriteRule ^/index.html /index_iphone.php [PT]


.. _Discussion_RewriteCond:

Discussion
~~~~~~~~~~


The ``RewriteRule`` directive can rewrite based on the value of the
requested URI - the ``REQUEST_URI`` variable - but is not able to look
at any other other variables. In order to include other variables in
your rewrite techniques, use the ``RewriteCond`` directive.

``RewriteCond`` is able to consider any variable available to httpd.
This includes any environment variable or request variable, such as
time of day, the client address, or, as seen in the recipe above, the
browser that the client is using.

In the recipe, we serve a special version of the site if the client is
using an iPhone - or, at least, a browser that reports that it is an
iPhone. (See :ref:`Recipe_rewritecond-mobile-client` for how to rewrite
something for all mobile clients.)

You may chain several ``RewriteCond`` directives together to create a
more complex conditional. Any number of ``RewriteCond`` directives apply
to a single following ``RewriteRule``.


.. tip::

   It is not possible to make several ``RewriteCond`` conditions apply to
   several ``RewriteRule`` directives. They apply to just one
   ``RewriteRule``. To make a set of conditions apply to multiple
   ``RewriteRule`` rules, you may need to repeat the conditions. Or,
   consider using the ``<If>`` directive for more complex scenarios. See
   :ref:`Recipe_If` for more about that.


.. _See_Also_RewriteCond:

See Also
~~~~~~~~


* :ref:`Recipe_rewritecond-mobile-client`

* :ref:`Recipe_If`

* http://httpd.apache.org/docs/mod/mod_rewrite.html#rewritecond


.. _Recipe_rewrite-time-of-day:

Rewrite based on the time of day
--------------------------------

.. index:: RewriteCond,time of day

.. index:: Time of day rewrite


.. _Problem_rewrite-time-of-day:

Problem
~~~~~~~


You want to serve different versions of a page depending on whether
it's day or night.


.. _Solution_rewrite-time-of-day:

Solution
~~~~~~~~


Use ``RewriteCond`` to rewrite based on the time of day.


.. code-block:: text

   RewriteEngine on
   RewriteCond   "%{TIME_HOUR}%{TIME_MIN}" ">0700"
   RewriteCond   "%{TIME_HOUR}%{TIME_MIN}" "<1900"
   RewriteRule   "^/open\.html$"             "open.day.html" [L]
   RewriteRule   "^/open\.html$"             "closed.night.html"


.. _Discussion_rewrite-time-of-day:

Discussion
~~~~~~~~~~


As seen in the earlier example, ``RewriteCond`` can be used to run a
``RewriteRule`` only under certain circumstances. In this recipe, we
want to write conditionally depending on the time of day, so we look
at the enviroment variables ``TIME_HOUR`` and ``TIME_MIN`` to determine
the current time stamp.


.. warning::

   Many systems have their time set to UTC (Coordinated Universal Time)
   rather than local time. Make sure you know how your system clock is
   set before using rules like this, as this will influence how these
   variables are evaluated.


It is very informative to carefully study the flow through these
rules, to try to think like ``mod_rewrite`` does.

In the event that the time is, in fact, after ``07:00`` and before
``19:00``, the two ``RewriteCond`` conditions will evaluate to true, and
the first of the two ``RewriteRule`` statements will be executed,
rewriting the request to ``open.day.html``.

Because the rule has a ``[L]`` (Last) flag, the execution of any rewrites will
be terminated, and the next ``RewriteRule`` will not be evaluated.

In the event that it is either earlier than ``07:00``, or later than
``19:00``, the ``RewriteCond`` conditions will fail, and the first
``RewriteRule`` will **not** be executed. However, in that case, the
second ``RewriteRule`` will be evaluated (unconditionally), and the
mapping to ``closed.night.html`` will be executed.

This same transformation could be applied using the ``<If>``
conditional. See :ref:`Chapter_per_request`, *Programmable
Configuration*, for more discussion of that directive.


.. _See_Also_rewrite-time-of-day:

See Also
~~~~~~~~


* :ref:`Recipe_RewriteCond`

* :ref:`Chapter_per_request`, **Programmable Configuration**


.. _Recipe_rewritecond-mobile-client:

Providing content specific to mobile clients
--------------------------------------------

.. index:: Mobile clients

.. index:: RewriteRule,mobile clients

.. index:: RewriteCond,mobile clients

.. index:: HTTP_USER_AGENT

.. index:: Browser string


.. _Problem_rewritecond-mobile-client:

Problem
~~~~~~~


You want to serve a different version of your website to mobile
clients.


.. _Solution_rewritecond-mobile-client:

Solution
~~~~~~~~


Use ``RewriteCond`` to look for the most common mobile client
``HTTP_USER_AGENT`` strings.


.. code-block:: text

   RewriteCond %{HTTP_USER_AGENT} (Mobi|iP(hone|od|ad)|Android|BlackBerry) [NC]
   RewriteRule /(.+)\.html /$1.mobile.html


.. _Discussion_rewritecond-mobile-client:

Discussion
~~~~~~~~~~


The above ruleset will catch 90+% of mobile user agents.

A more complete regular expression that catches upwards of 98% of
mobile user agents could be:


.. code-block:: text

   RewriteCond %{HTTP_USER_AGENT}
   (Mobile|iP(hone|od|ad)|Android|BlackBerry|IEMobile|
   Kindle|NetFront|Silk-Accelerated|(hpw|web)OS|Fennec|Minimo|
   Opera M(obi|ini)|Blazer|Dolfin|Dolphin|Skyfire|Zune) [NC]


.. warning::

   That's all one line, broken up to fit on this page.


Of course this regex must change all the time as new user agents come
to market, and have their own user agent string. Google, and other
search engine companies, have encouraged mobile client makers to
include the string ``Mobile`` in their user agent header, and most have
done so, but if you want to catch every one, you may have to be a
little more forgiving.


.. _See_Also_rewritecond-mobile-client:

See Also
~~~~~~~~


* http://www.useragentstring.com/pages/Mobile%20Browserlist/


.. _Recipe_rewrite-expr:

Rewrite based on arbitrary expression evaluation
------------------------------------------------

.. index:: Expression engine,RewriteCond


.. _Problem_rewrite-expr:

Problem
~~~~~~~


You want to rewrite conditionally based on some arbitrary expression
evaluation.


.. _Solution_rewrite-expr:

Solution
~~~~~~~~


Use the ``expr`` keyword to indicate that the argument to ``RewriteCond``
is to evaluated by the expression engine.


.. code-block:: text

   RewriteCond expr "%{HTTP:X-custom-header} in { 'fred', 'barney' }"
   RewriteRule ^ /flintstones.html [R]


.. _Discussion_rewrite-expr:

Discussion
~~~~~~~~~~


The expression engine is discussed in more detail in 
:ref:`Chapter_per_request`, **Programmable Configuration**, and provides a very powerful way to do
conditional configuration in the Apache http server. One of these ways
is by using it in ``RewriteCond``. The ``expr`` keyword tells
``RewriteCond`` to expect a logical statement that it will then evaluate
to either ``true`` or ``false``, and then act accordingly.

The expression parser was added to Apache httpd in version 2.4, and is
not available in versions 2.2 and earlier.


.. _See_Also_rewrite-expr:

See Also
~~~~~~~~


* :ref:`Chapter_per_request`, **Programmable Configuration**

* http://httpd.apache.org/docs/expr.html


.. _Recipe_RewriteCond_filetest:

RewriteCond file test operators
-------------------------------

.. index:: RewriteCond,filetest operators

.. index:: Filetest operators


.. _Problem_RewriteCond_filetest:

Problem
~~~~~~~


You only want to rewrite in the event that a file or directory doesn't
exist.


.. _Solution_RewriteCond_filetest:

Solution
~~~~~~~~


Use the ``-f`` and ``-d`` filetest operators to determine file existence
first.


.. code-block:: text

   RewriteCond /var/www/%{REQUEST_URI} !-f
   RewriteCond /var/www/%{REQUEST_URI} !-d
   RewriteRule ^ /archive/files/%{REQUEST_URI}


.. _Discussion_RewriteCond_filetest:

Discussion
~~~~~~~~~~


This recipe introduces syntax for ``RewriteCond`` that we haven't seen
before in this chapter. The ``-f`` and ``-d`` operators are two of a
larger set of filetest operators that allow you to inspect the local
file system and make decisions based on what you find.

The larger set of filetest operators is shown in the table below.


+----------+-------------------------------------------------+
| Operator | Meaning                                         |
+----------+-------------------------------------------------+
| -d       | Is a directory.                                 |
+----------+-------------------------------------------------+
| -f       | Is a regular file.                              |
+----------+-------------------------------------------------+
| -F       | Is an existing file, **via** subrequest.        |
+----------+-------------------------------------------------+
| -H       | Is a symbolic link, bash convention.            |
+----------+-------------------------------------------------+
| -l       | Is a symbolic link.                             |
+----------+-------------------------------------------------+
| -L       | Is a symbolic link, bash convention.            |
+----------+-------------------------------------------------+
| -s       | Is a regular file, with size greater than zero. |
+----------+-------------------------------------------------+
| -U       | Is an existing URL, **via** subrequest.         |
+----------+-------------------------------------------------+
| -x       | Has executable permissions.                     |
+----------+-------------------------------------------------+


Any of these tests may be prefaced with ``!`` to negate the test - that is, to mean the opposite.

In the example shown, we are testing to see if the specified file is
**not** a file, and is **not** a directory. The leading path ``/var/www/``
is added to make a full file system path out of the requested URI.


.. _See_Also_RewriteCond_filetest:

See Also
~~~~~~~~


:ref:`Recipe_rewritecond_alpha`


.. _Recipe_rewritecond_alpha:

Mapping into subdirectories alphabetically
------------------------------------------

.. index:: RewriteCond,Advanced syntax

.. index:: RewriteCond,comparison operators

.. index:: Alphabetical subdirectories


.. _Problem_rewritecond_alpha:

Problem
~~~~~~~


You've rearranged your directory structure such that
files beginning with letters between ``a`` and ``m`` were moved into a
subdirectory named ``a-m``, and files beginning with ``n`` through ``z``
were moved into a subdirectory named ``n-z``. You now wish to redirect
requests into the correct subdirectory.


.. _Solution_rewritecond_alpha:

Solution
~~~~~~~~


Inspect the first letter of the requested file, and redirect it into
the subdirectory based on its placement in the alphabet, using the
lexicographical comparision ability of ``RewriteCond``.


.. code-block:: text

   RewriteCond %{REQUEST_URI} ![an]-[mz]
   RewriteCond $1 <=n
   RewriteRule ^/(.)([^/]+) /a-m/$1$2 [R,L]
   
   RewriteCond %{REQUEST_URI} ![an]-[mz]
   RewriteRule ^/([^/]+)    /n-z/$1   [R]


You might also consider augmenting this further using the ``-d`` and
``-f`` operators discussed in :ref:`Recipe_RewriteCond_filetest` above.


.. _Discussion_rewritecond_alpha:

Discussion
~~~~~~~~~~


While ``RewriteRule`` can only consider the value of ``REQUEST_URI`` -
that is, the URL that the client requested - ``RewriteCond`` can inspect
any other variable that is available to httpd at request time. These
additional operators allow for all manner of evaluation and
comparison of these values so that you can make rewriting decisions.

In addition to the features described in earlier recipes,
``RewriteCond`` can perform many other comparisons that add to your
rewriting toolbox.

You can perform lexicographical comparisons - that is, compare two
strings based on their alphabetic qualities. The following table shows
the comparisons that you can make.


+---------------+---------------------------------------------+
| Operator      | Definition                                  |
+---------------+---------------------------------------------+
| <CondPattern  | Lexicographically precedes:                 |
+---------------+---------------------------------------------+
| >CondPattern  | Lexicographically follows:                  |
+---------------+---------------------------------------------+
| =CondPattern  | Lexicographically equal:                    |
+---------------+---------------------------------------------+
| <=CondPattern | Lexicographically less than or equal to:    |
+---------------+---------------------------------------------+
| >=CondPattern | Lexicographically greater than or equal to: |
+---------------+---------------------------------------------+


You can perform integer comparisons in much the same way. The
following table shows the comparisons you can make.


+----------+------------------------------------------+
| Operator | Definition                               |
+----------+------------------------------------------+
| -eq      | Is numerically equal to:                 |
+----------+------------------------------------------+
| -ge      | Is numerically greater than or equal to: |
+----------+------------------------------------------+
| -gt      | Is numerically greater than:             |
+----------+------------------------------------------+
| -le      | Is numerically less than or equal to:    |
+----------+------------------------------------------+
| -lt      | Is numerically less than:                |
+----------+------------------------------------------+


Finally, you can specify an arbitrary logical expressions using the
``expr`` keyword. This is discussed in greater detail in
:ref:`Chapter_per_request`, **Programmable Configuration**.

In the recipe given here, the ``<=`` operator is used to test whether
the first letter is before or after ``n`` in the alphabet.

An additional ``RewriteCond`` is used to ensure that a second write is
not performed on a request that has already been mapped to one of the
specified subdirectories. This ``RewriteCon`` must be repeated for the
second ``RewriteRule`` because each ``RewriteRule`` is bound only to the
``Rewritecond`` directives immediately preceeding it.

Thus:


.. code-block:: text

   1. RewriteCond %{REQUEST_URI} ![an]-[mz]
   2. RewriteCond $1 <=n
   3. RewriteRule ^/(.)([^/]+) /a-m/$1$2 [R,L]
   4. 
   5. RewriteCond %{REQUEST_URI} ![an]-[mz]
   6. RewriteRule ^/([^/]+)    /n-z/$1   [R]


In the listing above, the ``RewriteRule`` in line 3 is bound only by the
``RewriteCond`` directives in lines 1 and 2, while the ``RewriteRule`` in
line 6 is bound only by the ``RewriteCond`` in line 5.

The net effect is the solution described in the problem section above
* requests are sorted into subdirectories based on the first letter of
the requested file.


.. _See_Also_rewritecond_alpha:

See Also
~~~~~~~~


:ref:`Chapter_per_request`, **Programmable Configuration**

:ref:`Recipe_RewriteCond_filetest`


.. _Recipe_path_to_querystring:

Rewriting Path Information to Query String Arguments
----------------------------------------------------

.. index:: Query string

.. index:: SEO

.. index:: Search Engine Optimization

.. index:: Beautiful URLs

.. index:: PathInfo


.. _Problem_path_to_querystring:

Problem
~~~~~~~


You want to pass arguments as part of the URL but have these
components of the URL rewritten as ``QUERY_STRING`` arguments.


.. _Solution_path_to_querystring:

Solution
~~~~~~~~


This is just an example, of course; make appropriate changes to
the **RewriteRule** line to fit your
own environment and needs:


.. code-block:: text

   RewriteEngine on
   RewriteRule "^/book/([^/]*)/([^/]*)" "/cgi-bin/book.cgi?subject=$1&author=$2" [PT]


.. _Discussion_path_to_querystring:

Discussion
~~~~~~~~~~


One reason you might want or need to do this is if you're gluing
together two legacy systems that do things in different ways, such as
a client application and a vendor script.

Another reason often given for this kind of rewrite is so-called
beautiful URLs, as mentioned in the introduction to this chapter.
While it is not true - as frequently believed - that more attractive
URLs will improve your search engine rankings, it is true that URLs
which are easier to remember, or easier to guess, will lead to better
usability of your website, which may in turn lead to higher traffic.

For example, the **RewriteRule**
in the Solution will cause a user-requested URL like:


.. code-block:: text

   http://www.example.com/book/apache/bowen


to be rewritten on the back-end as:


.. code-block:: text

   http://www.example.com/cgi-bin/book.cgi?subject=apache&author=bowen


The ``[PT]`` flag on the **RewriteRule** directive instructs Apache to
keep processing the URL even after it has been modified; without the
flag, the server would directly try to treat the rewritten URL as a
filename, instead of continuing to the step at which it determines
it's a CGI script. It also allows multiple **RewriteRule** directives to make additional
refinements to the URL.

If the URL being rewritten already has a query string, or might,
change the ``[PT]`` to ``[QSA,PT]``. The QSA means 'query string append'
and will cause the query string generated by the rewrite to be added
to the query string in the original URL. Without QSA, the original
query string will be replaced.

The solution performs the rewrite in a manner completely
transparent to the user: the modification to the URL happens
within the server, rather than giving the user's client a new
URL to load.


.. _See_Also_path_to_querystring:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_rewrite.html

* <<Recipe_rewrite-by-query-string]]


.. _Recipe_rewrite-by-query-string:

Rewriting Based on the Query String
-----------------------------------

.. index:: Query String


.. _Problem_rewrite-by-query-string:

Problem
~~~~~~~


You want to translate one URI into another based on the value of
the query string.


.. _Solution_rewrite-by-query-string:

Solution
~~~~~~~~


In this example, we want to redirect a request for
``http://example.com/people?user=jrose`` to
``http://jrose.users.example.com`` instead.

Put this in your **httpd.conf**:


.. code-block:: text

   RewriteCond "%{QUERY_STRING}"   "^user=([^=]*)"
   RewriteRule "/people"           "http://%1.users.example.com/" [R]


.. _Discussion_rewrite-by-query-string:

Discussion
~~~~~~~~~~


``mod_rewrite`` does not
consider the query string as part of the URI for matching and
rewriting purposes, so you need to treat it separately. The given
example translates requests of the form:


http://example.com/people?user=jones

http://jones.users.example.com/

.. index::  [R\] 

.. index:: Rewrite Flags,[R\] 

.. index:: RewriteRule,flags,[R\] 

.. index:: Rewrite,flags,[R\]


The ``[R]`` tells ``mod_rewrite`` to redirect the browser to the
URL constructed by the **RewriteRule** directive.

This technique is, in some ways, the opposite of the one before it, :ref:`Recipe_path_to_querystring`, where we map a URL to a query string argument.


.. _See_Also_rewrite-by-query-string:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_alias.html

* :ref:`Recipe_path_to_querystring`


.. _Recipe_RewriteOptions:

Influencing rewrite behavior
----------------------------

.. index:: RewriteOptions

.. index:: Rewrite,RewriteOptions


.. _Problem_RewriteOptions:

Problem
~~~~~~~


You want to influence the way that rewrite rules are applied.


.. _Solution_RewriteOptions:

Solution
~~~~~~~~


The ``RewriteOptions`` directive subtly influences the way that
``RewriteRule`` directives are applied on your server, and can be set to
one of several values.


+---------+---------+
| Value   | Meaning |
+---------+---------+
| Inherit |         |
+---------+---------+


.. tip::

   ``Inherit`` is particularly useful for rewrite rules that you want to apply 
   to several virtual hosts - define them once in global scope, then put
   ``RewriteOptions Inherit`` in each ``VirtualHost`` block.


+-------------------+
| InheritBefore     |
+-------------------+
| InheritDown       |
+-------------------+
| InheritDownBefore |
+-------------------+
| IgnoreInherit     |
+-------------------+
| AllowNoSlash      |
+-------------------+
| AllowAnyURI       |
+-------------------+


.. warning::

   **Security Warning**

   Enabling the ``AllowAnyURI`` option will make the server vulnerable to security issues if used with rewrite rules which are not carefully authored. It is strongly recommended that this option is not used. In particular, beware of input strings containing the '@' character which could change the interpretation of the transformed URI, as **per** the above CVE names.


+-------------------+
| MergeBase         |
+-------------------+
| IgnoreContextInfo |
+-------------------+


.. _Discussion_RewriteOptions:

Discussion
~~~~~~~~~~


The default values of ``RewriteOptions`` are sufficient for most
situations. You'll only need to modify this directive if you need some
of the specific behavior described in the documentation.


.. _See_Also_RewriteOptions:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_rewrite.html#rewriteoptions


.. _Recipe_rewrite-content-type:

Setting the Content-Type According to Browser Capability
--------------------------------------------------------

.. index:: Content-Type

.. index:: HTTP_ACCEPT

.. index:: Rewrite,HTTP_ACCEPT


.. _Problem_rewrite-content-type:

Problem
~~~~~~~


You want to set ``Content-Type``
headers differently for different browsers, which may render the
content incorrectly otherwise.


.. _Solution_rewrite-content-type:

Solution
~~~~~~~~


Check the ``Accept`` headers with **RewriteCond** and then set the
``Content-Type`` header with a ``[T]`` flag:


.. code-block:: text

   RewriteCond "%{HTTP_ACCEPT}" "application/xhtml\+xml"
   RewriteCond "%{HTTP_ACCEPT}" "!application/xhtml\+xml\s*;\s*q=0+(?:\.0*[^0-9])"
   RewriteRule . - [T=application/xhtml+xml;charset=iso-8859-1]


.. _Discussion_rewrite-content-type:

Discussion
~~~~~~~~~~


Different browsers tend to deal with content differently and
sometimes need a nudge in the right direction. In this example, for
browsers that specify (using the ``HTTP_ACCEPT`` header) that they prefer XHTML
content, we want to send a ``Content-Type`` header specifying that the
content we are sending fulfills that requirement.

The ``[T]`` (Type) flag sets the ``Content-Type`` for the response.


.. _See_Also_rewrite-content-type:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_rewrite.html


.. _Recipe_image-theft:

Denying Access to Unreferred Requests
-------------------------------------

.. index:: Image theft

.. index:: Prevent hotlinking

.. index:: Denying unreferred requests

.. index:: Rewrite,image theft

.. index:: Rewrite,Prevent hotlinking

.. index:: Rewrite,Denying unreferred requests


.. _Problem_image-theft:

Problem
~~~~~~~


You want to prevent other Web sites from using your images (or
other types of documents) in their pages and allow your images to be
accessed only if they were referred from your own site.


.. _Solution_image-theft:

Solution
~~~~~~~~


Put this in your **httpd.conf**:


.. code-block:: text

   RewriteEngine On
   RewriteCond "%{HTTP_REFERER}" !=""
   RewriteCond "%{HTTP_REFERER}" "!^http://mysite.com/" [NC]
   RewriteRule "\.(jpe?g|gif|png)$ - [F]


.. _Discussion_image-theft:

Discussion
~~~~~~~~~~


This recipe is a series of **RewriteCond** directives, designed to
determine whether an image file is requested from within a document on
your site or if it is embedded in a page from another server. If the
the latter, then the other site is stealing your images and needs to
be stopped.

The first rule checks to see if the referer is even set. Some
clients don't send a referer, and some browsers can be configured not
to send referers. If we deny requests from all clients that don't send
a referer, we'll deny a lot of valid requests; so we let these ones
in.

Next, we check to see if the referer appears to be from some
site other than our own. If so, we keep going through the rules.
Otherwise, we'll stop processing the rewrite.

Finally, we check to see if this is a request for an image file.
If the file is a nonimage file, such as an HTML file, then we want to
allow people to link to these files from somewhere offsite.

If we've reached this point in the ruleset, we know that we have
a request for an image file from within a page on another Web site.
The **RewriteRule** matches a request
and returns ``Forbidden`` to the client.

There's a few other ways that you can do the same thing.

For example, you may wish, instead of simply forbidding the image, to
call attention to it a little more by replacing it with another image
entirely:


.. code-block:: text

   RewriteCond "%{HTTP_REFERER}" !=""
   RewriteCond "%{HTTP_REFERER}" "!^http://mysite.com/" [NC]
   RewriteRule "\.(jpe?g|gif|png)$ /stolen-image.png [R,L]


Rather than simply seeing a broken image in the page, all visitors
will now see a replacement image clearly stating that the site is
misusing your images.


.. tip::

   This technique has a tendency to get the problem fixed more
   quickly, since visitors to the thieving site will see "This Image Is
   Stolen!" —and that's typically not the impression the site's owners
   would like them to get. Simply returning a 403 (Forbidden) error
   will result in a broken-image icon on the referring page, and
   **everyone** is used to those nowadays and thinks nothing of
   them.


In httpd 2.4 and later, consider instead using the ``<If>`` directive,
which can accomplish the same thing, with a somewhat more readable
configuration syntax. This is covered in :ref:`Recipe_image-theft-if`.


.. _See_Also_image-theft:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_rewrite.html

* :ref:`Recipe_image-theft-if`


.. _Recipe_php-source-rewrite:

Showing Highlighted PHP Source
------------------------------

.. index:: PHP

.. index:: Source highlighting

.. index:: Syntax highlighting

.. index:: Highlighted PHP source


.. _Problem_php-source-rewrite:

Problem
~~~~~~~


You want to be able to see the syntax-highlighted source code of each
of your PHP scripts.


.. _Solution_php-source-rewrite:

Solution
~~~~~~~~


Add a line such as the following to your **httpd.conf** 
or .**htaccess** file:


.. code-block:: text

   RewriteRule "^(.+\.php)s$" "$1" [H=application/x-httpd-php-source]


.. _Discussion_php-source-rewrite:

Discussion
~~~~~~~~~~


The PHP interpreter has a built-in function to display PHP
source code syntax color-coded. Ordinarily, this function is invoked
for **.phps** files when your
configuration file contains the following line:


.. code-block:: text

   AddHandler application/x-httpd-php-source .phps


However, in order to take advantage of this functionality, you
need to make a copy, or symbolic link, of each PHP file you wish to
treat this way, replacing the **.php** file extension with a **.phps** file extension. This is impractical
and inconvenient.

The recipe given removes the need to do this, by rewriting any
request for a **.phps** file to that same filename, but with a **.php**
file extension instead, and associating the **php-source** handler 
with that request.


.. _See_Also_php-source-rewrite:

See Also
~~~~~~~~


* :ref:`Recipe_enabling_mod_php`

* http://php.net/manual/en/function.highlight-file.php


.. _Recipe_rewrite-path-to-vhost:

Mapping certain paths to another vhost
--------------------------------------

.. index:: Rewrite,virtual hosts

.. index:: Map path to virtual host


.. _Problem_rewrite-path-to-vhost:

Problem
~~~~~~~


You want to migrate pathnames under a single hostname to
distinct hostnames.


.. _Solution_rewrite-path-to-vhost:

Solution
~~~~~~~~


Use **RewriteRule** in **httpd.conf**:


.. code-block:: text

   RewriteRule "^/(one|two|three)(/.*)" "http://$1.example.com$2" [R]
   RewriteRule "^/([^./]*)(/.*)" "http://$1.example.com$2" [R]
   RewriteRule "^/~([^./]*)(/.*)" "http://$1.example.com$2" [R]


.. _Discussion_rewrite-path-to-vhost:

Discussion
~~~~~~~~~~


Three solutions are offered here, for three related scenarios.

The first recipe redirects requests of the form 
http://example.com/one/some/file.html to a
different host, such as 
http://one.example.com/some/file.html, specifying several
paths for which we want this to happen - in this example, ``one``,
``two``, and ``three``.

Of course, this first scenario could also be accomplished by a few
``Redirect`` directives:


.. code-block:: text

   Redirect /one/   http://one.example.com/
   Redirect /two/   http://two.example.com/
   Redirect /three/ http://three.example.com/


The second recipe does the same thing, except that
**any** top-level path segment is redirected in this manner. That is,
any request to the server will be redirected to the server named by
the first directory segment. [#wildcard-dns]_So, for example:


.. code-block:: text

   http://www.example.com/anything/file.html


will be redirected to:


.. code-block:: text

   http://anything.example.com/file.html


The third recipe redirects any userdir style request (ie, beginning
with ``~username``) to a server with that user's name. for example, a
request for:


.. code-block:: text

   http://www.example.com/~iwinter/something


will be redirected to:


.. code-block:: text

   http://iwinter.example.com/something


In each case, you'll need to ensure that the necessary DNS records in
place for these recipes to actually work.


.. _See_Also_rewrite-path-to-vhost:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_rewrite.html

* :ref:`Recipe_rewrite-dynamic-vhost`


.. _Recipe_rewrite-dynamic-vhost:

Rewriting a Hostname to a Directory
-----------------------------------

.. index:: Rewrite,virtual hosts

.. index:: Map virtual host to path

.. index:: Dynamic virtual host

.. index:: Virtual host,dynamic


.. _Problem_rewrite-dynamic-vhost:

Problem
~~~~~~~


You want requests for http://bogus.example.com/ to be turned into requests
for http://example.com/bogus/, or transparently mapped to a
particular directory.


.. _Solution_rewrite-dynamic-vhost:

Solution
~~~~~~~~


.. code-block:: text

   RewriteCond %{HTTP_HOST} ^([^.]+)\.example\.com [NC]
   RewriteRule (.*) http://example.com/%1$1 [R]


To do this transparently, without a redirect:


.. code-block:: text

   RewriteCond %{HTTP_HOST} ^([^.]+)\.example\.com$ [NC]
   RewriteRule (.*) /var/www/vhosts/%1$1


.. _Discussion_rewrite-dynamic-vhost:

Discussion
~~~~~~~~~~


This technique is occasionally needed when wildcard hostnames
are being supported. It gives the illusion that URLs are pointing to
separate hosts rather than subdirectories on only one system. Of
course, using the redirection (``[R]``)
flag will void the illusion because the replacement URL will be
visible to the end user. If you want it to be completely transparent
to the user, you can use the second option to get the equivalent
result with a rewrite internal to the server that the client never
sees.

In each example, the ``RewriteCond`` captures the initial segment of the
hostname, such as ``host`` in ``host.example.com``, and saves it in the
variable ``%1`` for later use. The ``RewriteRule`` then captures the
entire request, and constructs a final target using the hostname and
the request path.


.. _See_Also_rewrite-dynamic-vhost:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_rewrite.html

* :ref:`Recipe_mod_vhost_alias`

* :ref:`Recipe_rewrite-path-to-vhost`


.. _Recipe_RewriteMap:

Using RewriteMap to compress a large number of rules
----------------------------------------------------

.. index:: RewriteMap

.. index:: RewriteMap,txt

.. index:: RewriteMap,text map

.. index:: RewriteRule,RewriteMap


.. _Problem_RewriteMap:

Problem
~~~~~~~


You have a large number of almost-identical ``RewriteRule`` directives that you
wish to express as a single rule.


.. _Solution_RewriteMap:

Solution
~~~~~~~~


Use ``RewriteMap`` and place the mapping data in an external file. This
is done in the following steps.

1) Put the mapping data in an external text file. In this example,
imagine a grocery store website that wishes to map cereal names to the
product ID number. We'll call this file ``cereal.txt``.


.. code-block:: text

   cheerios 128
   crispix 227
   luckycharms 893
   frostedflakes 832


2) Create a map rule, giving it a name, and the location of the file
you just created. This is somewhat akin to
writing a named function in a programming language.


.. code-block:: text

   RewriteMap cerealID "txt:/var/www/maps/cereal.txt"


3) Invoke this map in a ``RewriteRule``.


.. code-block:: text

   RewriteRule ^/cereal/(.*) /cereals.php?id=${cerealID:$1} [PT]


Now, requests for ``http://example.com/cereal/cheerios`` will trigger a
lookup in your map file, resulting in a rewrite to ``/cereals.php?id=128``


.. _Discussion_RewriteMap:

Discussion
~~~~~~~~~~


There are many scenarios where you might have a large number of
lookupb-based mappings that you want to incorporate into
``RewriteRule`` directives. The naive way to do this, of course, is to have
hundreds of ``RewriteRule`` directives. The trouble with this is that
every request that comes into your server must be passed through this
long list of rules before it finds the right one, if at all.

By using a RewriteMap you greatly simplify not only the configuration
file, but also the lookup process itself.

Note that once the map file gets too big, you will start paying a
penalty in lookup speeds, at which time you need to look at converting
the text-based lookup file into a faster format, such as dbm. See 
:ref:`Recipe_RewriteMap-dbm` for a discussion of this technique.


.. _See_Also_RewriteMap:

See Also
~~~~~~~~


* https://httpd.apache.org/docs/rewrite/rewritemap.html

* :ref:`Recipe_RewriteMap-default-value`

* :ref:`Recipe_RewriteMap-dbm`


.. _Recipe_RewriteMap-default-value:

Specifying a default value for a RewriteMap
-------------------------------------------

.. index:: RewriteMap,default value

.. index:: RewriteRule,RewriteMap default value

.. index:: Default value for RewriteMap


.. _Problem_RewriteMap-default-value:

Problem
~~~~~~~


You have a ``RewriteMap``, and want to specify a default value to use
when none of the other options match.


.. _Solution_RewriteMap-default-value:

Solution
~~~~~~~~


Specify the default value when you invoke the ``RewriteMap``:


.. code-block:: text

   RewriteRule ^/cereal/(.*) /cereals.php?id=${cerealID:$1|0} [PT]


or, perhaps:


.. code-block:: text

   RewriteRule ^/cereal/(.*) /cereals.php?id=${cerealID:$1|NOTFOUND} [PT]


.. _Discussion_RewriteMap-default-value:

Discussion
~~~~~~~~~~


In this case, any cereal that we don't find in the lookup file will
result in an ID of 0, in the first example, and 'NOTFOUND' in the
second, which we can then handle as a special case in
``cereals.php``.

Any line in the map file starting with ``#`` will be considered to be a
comment, and ignored.


.. _See_Also_RewriteMap-default-value:

See Also
~~~~~~~~


* https://httpd.apache.org/docs/rewrite/rewritemap.html


.. _Recipe_RewriteMap-rnd:

Randomly selecting an entry from a map
--------------------------------------

.. index:: RewriteMap,rnd

.. index:: RewriteMap,Random

.. index:: RewriteRule,RewriteMap

.. index:: Random rewrite rule


.. _Problem_RewriteMap-rnd:

Problem
~~~~~~~


You wish to randomly select an entry from a map file, rather than
looking it up based on a lookup key.


.. _Solution_RewriteMap-rnd:

Solution
~~~~~~~~


The ``rnd`` map file type has a similar syntax to the ``txt`` lookup map
file. However, whereas each line contains one lookup key, it contains
more than one options that we'll be choosing from, separated by a pipe
("|") character.


.. code-block:: text

   cereal cheerios|frostedflakes|crispix|luckycharms
   grain wheat|corn|barley|rice|rye


In the above example, we have two possible maps - cereal and grain.

Next, declare the mapping using the ``RewriteMap`` directive:


.. code-block:: text

   RewriteMap lookup "rnd:/var/www/maps/randomcereal.txt"


You can now use this map in any ``RewriteRule``.


.. code-block:: text

   RewriteRule /random-cereal /cereal.php?cereal=${lookup:cereal}


.. _Discussion_RewriteMap-rnd:

Discussion
~~~~~~~~~~


The syntax here is very similar to the ``txt`` lookup map described in 
:ref:`Recipe_RewriteMap`, except that multiple values are provided rather
than just one value. Then, in the ``RewriteRule`` invoking the lookup,
we provide the literal lookup key - in this case, "cereal", to
indicate which line of the lookup file we want to randomize.


.. _See_Also_RewriteMap-rnd:

See Also
~~~~~~~~


* :ref:`Recipe_RewriteMap`

* http://httpd.apache.org/docs/rewrite/rewritemap.html#rnd


.. _Recipe_RewriteMap-rnd-weighted:

Weighted random RewriteMap
--------------------------

.. index:: RewriteMap,weighted rnd

.. index:: RewriteMap,weighted random

.. index:: Weighted random rewrite rule


.. _Problem_RewriteMap-rnd-weighted:

Problem
~~~~~~~


You want to randomly select an entry from a map files, but weight
certain options more heavily than others.


.. _Solution_RewriteMap-rnd-weighted:

Solution
~~~~~~~~


Use the ``rnd`` map file type, as discussed in
:ref:`Recipe_RewriteMap-rnd`, but repeat options that you want to be more
frequently chosen:


.. code-block:: text

   cereal cheerios|cheerios|cheerios|frostedflakes|crispix|crispix|luckycharms


.. _Discussion_RewriteMap-rnd-weighted:

Discussion
~~~~~~~~~~


In the example show above, ``frostedflakes`` and ``luckycharms`` will have
a relative probability of 1 of being chosen, while ``crispix`` will have
a relative probability of 2, and ``cheerios`` will have 3.


.. _See_Also_RewriteMap-rnd-weighted:

See Also
~~~~~~~~


* :ref:`Recipe_RewriteMap-rnd`

* http://httpd.apache.org/docs/rewrite/rewritemap.html#rnd


.. _Recipe_RewriteMap-dbm:

Converting a text RewriteMap to a dbm
-------------------------------------

.. index:: RewriteMap,dbm


.. _Problem_RewriteMap-dbm:

Problem
~~~~~~~


Your text-based rewrite map has grown large and slow, and you want to
speed up lookups.


.. _Solution_RewriteMap-dbm:

Solution
~~~~~~~~


Convert your text map file to a dbm:


.. code-block:: text

   httxt2dbm -i cereal.txt -o cereal.dbm


and use the ``dbm`` RewriteMap type:


.. code-block:: text

   RewriteMap cerealID "dbm:/var/www/maps/cereal.dbm"


Your ``RewriteRule`` directive remains unchanged:


.. code-block:: text

   RewriteRule ^/cereal/(.*) /cereals.php?id=${cerealID:$1} [PT]


.. _Discussion_RewriteMap-dbm:

Discussion
~~~~~~~~~~


Text files are a much slower lookup mechanism than a dbm file, because
they are not indexed. That is, every time the rule is invoked, the
``RewriteMap`` will need to go through the file one line at a time
looking for a match. A dbm, on the other hand, is an indexed database,
and so lookups are very fast.


.. _See_Also_RewriteMap-dbm:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/programs/httxt2dbm.html

* http://httpd.apache.org/docs/rewrite/rewritemap.html#dbm


.. _Recipe_RewriteMap-int:

Using built-in RewriteMap functions
-----------------------------------

.. index:: RewriteMap,int

.. index:: Internal RewriteMap functions


.. _Problem_RewriteMap-int:

Problem
~~~~~~~


Certain commonly-used functions, such as uppercase and lowercase, 
shouldn't need to be defined by everyone that needs them.


.. _Solution_RewriteMap-int:

Solution
~~~~~~~~


Use the various ``int`` map types in the definition of your maps.

There are four of these:


.. _RewriteMapIntFunctions:


+----------+-----------------------------------------------------------------+
| Function | Meaning                                                         |
+----------+-----------------------------------------------------------------+
| toupper  | Converts the key to all upper case.                             |
+----------+-----------------------------------------------------------------+
| tolower  | Converts the key to all lower case.                             |
+----------+-----------------------------------------------------------------+
| escape   | Translates special characters in the key to hex-encodings.      |
+----------+-----------------------------------------------------------------+
| unescape | Translates hex-encodings in the key back to special characters. |
+----------+-----------------------------------------------------------------+


To use one of these functions, you'll need to incorporate it into a
``RewriteMap`` declaration:


.. code-block:: text

   RewriteMap lc int:tolower
   RewriteRule (.*) ${lc:$1} [R]


.. _Discussion_RewriteMap-int:

Discussion
~~~~~~~~~~


While the built-in library of ``RewriteMap`` helper functions is very
sparse, it covers the most commonly requested cases.


.. _See_Also_RewriteMap-int:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/rewrite/rewritemap.html#int


.. _Recipe_RewriteMap-prg:

Invoking an external script for a RewriteMap
--------------------------------------------

.. index:: RewriteMap,prg

.. index:: RewriteMap,External program

.. index:: RewriteRule,Invoke external script


.. _Problem_RewriteMap-prg:

Problem
~~~~~~~


You wish to invoke a script or program to assist in rewriting URLs.


.. _Solution_RewriteMap-prg:

Solution
~~~~~~~~


Use a ``RewriteMap`` ``prg`` type to invoke an external script to process
your rewriting.

For example, if you had a complex rewriting algorithm that you had
implemented in a Perl script, you could invoke that with:


.. code-block:: text

   RewriteMap mangle prg:/www/bin/mangle.pl
   RewriteRule . ${mangle:%{REQUEST_URI}}


The ``mangle.pl`` script would then be expected to receive an argument
on ``STDIN``, do something to it, and send a result to ``STDOUT``:


.. code-block:: text

   #!/usr/bin/perl
   $| = 1; # Turn off I/O buffering
   while (<STDIN>) {
       my $return = do_mangle( $_ );
       print $return;
   }


.. _Discussion_RewriteMap-prg:

Discussion
~~~~~~~~~~


Your rewrite script can be implemented in whatever language you like.
Perl is used here arbitrarily. The only requirements are that your
program be able to read from ``STDIN``, and write unbuffered output to
``STDOUT``.

It is important that output be unbuffered, as the rewrite process will
wait for a return value until it arrives, and if output is buffered,
that may cause it to hang indefinitely.


.. warning::

   Your map program should be as simple as possible. If it fails in some
   way, it may cause rewrites to occur with unpredictable values.

   One copy of a ``RewriteMap`` program will be launched at server startup,
   and will remain running for the lifetime of the server. All requess
   will be sent through this one instance, which will therefore be a
   potential bottleneck. Thus, the program should be as simple, and as
   fast, as posslble.

   Use ``prg`` map files only as a last resort, when all other options have
   been exhausted.


.. _See_Also_RewriteMap-prg:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/rewrite/rewritemap.html#prg


.. _Recipe_RewriteMap-dbd:

Using an RDBMS in your rewrites
-------------------------------

.. index:: RewriteMap,dbd

.. index:: RewriteMap,fastdbd

.. index:: Database rewrites

.. index:: RewriteRule,database-driven


.. _Problem_RewriteMap-dbd:

Problem
~~~~~~~


You wish to store mappings in an RDBMS (database) and perform rewrites
based on SQL queries.


.. _Solution_RewriteMap-dbd:

Solution
~~~~~~~~


Use the ``dbd`` or ``fastdbd`` ``RewriteMap`` type to query a database in
your ``RewriteRules``.

``mod_dbd`` must be loaded to make use of
this map type.


.. code-block:: text

   RewriteMap cerealID \
       "dbd:SELECT cerealID FROM cereals WHERE name = %s"
   RewriteRule ^/cereal/(.*) /cereals.php?id=${cerealID:$1} [PT]


.. _Discussion_RewriteMap-dbd:

Discussion
~~~~~~~~~~


This map type has two variants, ``dbd`` and ``fastdbd``. The only
difference between the two is that ``dbd`` performs the query every time
a request is made, while ``fastdbd`` caches the results in memory so
that a trip to the database is not necessary.


.. tip::

   When using the ``fastdbd`` map type, you'll need to restart the httpd
   service when your database records change. If your data changes
   frequently, use ``dbd`` instead.


If the database used supports prepared statements, the statement is
prepared at server startup time, resulting in very fast query times.
It also performs appropriate argument escaping and quoting, to 
prevent SQL injection attacks.

To connect to your database, provide the database credentials in your
server configuration file. For example:


.. code-block:: text

   DBDriver mysql
   DBDParams "host=127.0.0.1 port=3306 user=username_here pass=password_here"


See the ``mod_dbd`` documentation for information about what other databases
are supported, and how to provide connection credentials, which may
vary from one database engine. 


.. _See_Also_RewriteMap-dbd:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/rewrite/rewritemap.html#dbd

* http://httpd.apache.org/docs/mod/mod_dbd.html


.. _Recipe_rewritecond-backreference:

Using a backreference from a RewriteCond
----------------------------------------

.. index:: RewriteCond

.. index:: Backreferences,RewriteCond

.. index:: Regular Expressions,Backreference


.. _Problem_rewritecond-backreference:

Problem
~~~~~~~


You wish to capture part of a match in a ``RewriteCond``, and then use
that value later as a backreference.


.. _Solution_rewritecond-backreference:

Solution
~~~~~~~~


Use the variable ``%1`` to refer to a backreference captured in a
``RewriteCond`` regular expression.


.. code-block:: text

   RewriteCond %{HTTP_HOST} ^([^.]+)\.example\.com [NC]
   RewriteRule (.*) http://example.com/%1$1 [R]


.. _Discussion_rewritecond-backreference:

Discussion
~~~~~~~~~~


While ``RewriteRule`` captures backreferences using the variables ``$1``,
``$2``, and so on, ``RewriteCond`` instead uses the variables ``%1``, ``%2``,
and so on.

In the ``RewriteCond``, the regular expression provided is:


.. code-block:: text

   ^([^.]+)\.example\.com


The parentheses at the beginning of the regular expression define a
backreference, comprised of the any characters appearing before the
first ``.`` in the requested hostname. Thus, if the requested hostname
is ``pony.example.com``, ``%1`` will be set to ``pony``.

The example shown here is borrowed from an earlier recipe,
:ref:`Recipe_rewrite-dynamic-vhost`, and is
provided again here to illustrate the concept.


.. _See_Also_rewritecond-backreference:

See Also
~~~~~~~~


* :ref:`Recipe_rewrite-dynamic-vhost`

* http://httpd.apache.org/docs/mod/mod_rewrite.html#rewritecond


.. _Recipe_rewrite-new-extension:

Rewriting requests to a new file extension
------------------------------------------

.. index:: File extensions

.. index:: RewriteRule,File extensions

.. index:: RewriteRule,flags,[PT\]]


.. _Problem_rewrite-new-extension:

Problem
~~~~~~~


You've recently rewritten your entire website, and now URLs end in
``.php`` rather than ``.html``, but you want old links to keep working.


.. _Solution_rewrite-new-extension:

Solution
~~~~~~~~


.. code-block:: text

   RewriteRule ^(.*)\.html $1\.php [PT]


.. _Discussion_rewrite-new-extension:

Discussion
~~~~~~~~~~


The solution here uses the ``[PT]`` flag to forward a request for a
``.html`` file to a ``.php`` file of the same name. For example, a request
for http://your.site.com/horses/pony.html will be passed transparently
on to the file ``/horses/pony.php``, without the client noticing.


.. _See_Also_rewrite-new-extension:

See Also
~~~~~~~~


.. _Recipe_rewrite-looping:

Using RewriteCond to avoid rewrite looping
------------------------------------------

.. index:: Rewrite,Looping

.. index:: Loop avoidance


.. _Problem_rewrite-looping:

Problem
~~~~~~~


My rewrite rule generates a browser error message that the web page
has a redirect loop. How do I avoid this?


.. _Solution_rewrite-looping:

Solution
~~~~~~~~


Avoid looping by using a ``RewriteCond`` to anticipate requests that
have already been rewritten:


.. code-block:: text

   RewriteCond %{REQUEST_URI} !/images/
   RewriteRule (.+)\.gif /images/$1.gif [R]


.. _Discussion_rewrite-looping:

Discussion
~~~~~~~~~~


In the example given, any request for a ``gif`` image file will be
redirected to the ``/images/`` directory. However, we do not wish to
redirect a request that is already destined for the ``/images/``
directory. To avoid this, we first check to see if the request 
already contains the substring ``/images/``.  That might mean that the
request has already been redirected, or that the initial request was
already for that directory. In either case, we don't want to redirect.

In the event that you do have a ``RewriteRule`` that loops, you will see
a message in your error log that looks like:


.. code-block:: text

   Request exceeded the limit of 10 internal
   redirects due to probable configuration error.
   Use 'LimitInternalRecursion' to increase the
   limit if necessary. Use 'LogLevel debug' to get
   a backtrace.


.. warning::

   While this error message suggests modifying ``LimitInternalRecursion``, 
   that will merely postpone the problem a few microseconds, while the
   rule loops that many more times. The specific error message covers
   other scenarios other than a looping ``RewriteRule``.


.. _See_Also_rewrite-looping:

See Also
~~~~~~~~


* https://httpd.apache.org/docs/2.4/mod/core.html#limitinternalrecursion

* http://wiki.apache.org/httpd/RewriteLooping


.. _Recipe_canonical-hostname:

Enforcing the use of a preferred hostname
-----------------------------------------

.. index:: Canonical hostname

.. index:: www vs no-www

.. index:: RewriteRule,Canonical hostname

.. index:: Enforcing a preferred hostname

.. index:: Preferred hostname

.. index:: Virtual hosts,preferred hostname


.. _Problem_canonical-hostname:

Problem
~~~~~~~


You wish to enforce the use of a particular hostname - for example,
``www.example.com`` rather than ``example.com`` - for accessing your
website. You wish to do this with ``RewriteRule``.


.. _Solution_canonical-hostname:

Solution
~~~~~~~~


To do this with ``RewriteRule``:


.. code-block:: text

   RewriteCond %{HTTP_HOST} !^www\. [NC]
   RewriteRule ^ http://www.example.com%{REQUEST_URI} [R,L]


While this can be accomplished using ``RewiteRule``, this is not the
best way to accomplish this goal.


.. _Discussion_canonical-hostname:

Discussion
~~~~~~~~~~


While you can use ``mod_rewrite`` to enforce a canonical hostname, this
is not the best way to accomplish it in most cases.

The recipe above is recommended if you do not have access to the
server's configuration file, and instead have to use ``.htaccess``
files. 

See :ref:`Chapter_htaccess`, **.htaccess Files**, for further discussion of the advantages and
disadvantages of ``.htaccess`` files.

Meanwhile, if you do have access to the server's configuration file,
consider using a redirect in one virtual host to send requests to the
other:


.. code-block:: text

   # Required for 2.2.x and below:
   #NameVirtualHost *:80
   
   # www.example.net and example.com VirtualHost
   * (Non-preferred hostnames)
   <VirtualHost *:80>
     ServerName www.example.net
     ServerAlias example.com
     Redirect permanent / http://www.example.com/
   </VirtualHost>
   
   # Canonical VirtualHost (Preferred hostname)
   <VirtualHost *:80>
     ServerName www.example.com
     DocumentRoot /usr/local/apache/htdocs
   </VirtualHost>


The main reason for using this approach, rather than the ``RewriteRule``
solution, is that a client using the "wrong" hostname will be
redirected on their first request, and the comparison won't need to be
done again. On the other hand, with the ``RewriteRule`` solution, the
hostname comparison will need to be made not just on the initial
request, but also on every subsequent request, thus slowing down all
requests to the server.


.. _See_Also_canonical-hostname:

See Also
~~~~~~~~


* http://wiki.apache.org/httpd/CanonicalHostNames


.. _Recipe_rewrite-proxy:

Rewriting to a proxied server
-----------------------------

.. index:: RewriteRule,Proxy

.. index::  [P\] 

.. index:: Rewrite Flags,[P\] 

.. index:: RewriteRule,flags,[P\]

.. index:: Rewrite,flags,[P\]

.. index:: Proxy

.. index:: mod_proxy

.. index:: Modules,mod_proxy

.. index:: ProxyPass


.. _Problem_rewrite-proxy:

Problem
~~~~~~~


You want to rewrite a request to another remote server, without
changing the browser's URL.


.. _Solution_rewrite-proxy:

Solution
~~~~~~~~


Use the ``[P]`` flag to rewrite the request through a proxy:


.. code-block:: text

   RewriteRule /(.*)\.(jpg|gif|png)$ \
           http://images.example.com/$1.$2 [P]


.. _Discussion_rewrite-proxy:

Discussion
~~~~~~~~~~


The recipe given here requires that ``mod_proxy`` be loaded, as the
``[P]`` flag invokes the proxying methods from that module to do its
work.

In the example shown, any request for an image - a URL ending in
``.jpg``, ``.gif``, or ``.png`` - will be proxied through to a separate
server, where those images are hosted. The client is unaware that this
is happening - that is, from the client's perspective, the URL does
not change.

If you're going to proxy an entire directory elsewhere, it is more
efficient to use the ``ProxyPass`` directive, rather than having to
invoke a regular expression with every request. See also
:ref:`Chapter_Proxies`, **Proxies**, for a more extensive discussion of using Apache
httpd as a proxy server.


.. _See_Also_rewrite-proxy:

See Also
~~~~~~~~


* :ref:`Chapter_Proxies`, **Proxies**

* http://httpd.apache.org/docs/rewrite/flags.html#flag_p

* http://httpd.apache.org/docs/mod/mod_proxy.html#proxypass


.. _Recipe_rewrite_variable:

Using a variable in a RewriteRule
---------------------------------

.. index:: Define

.. index:: RewriteRule,using a variable

.. index:: Variables,RewriteRule


.. _Problem_rewrite_variable:

Problem
~~~~~~~


You want to define a variable, and then use it in a ``RewriteRule``.


.. _Solution_rewrite_variable:

Solution
~~~~~~~~


Use the ``Define`` directive, and then use the variable in your
``RewriteRule``:


.. code-block:: text

   Define sales "(invoice|estimate|purchase_order|sales_order)"
   
   RewriteRule ^/${sales}/([0-9]*)$ /invoice_new.php?id=$1  [PT,QSA,L]
   RewriteRule ^/${sales}s$ /invoices_new.php [PT,QSA,L]


.. _Discussion_rewrite_variable:

Discussion
~~~~~~~~~~


In the example given, we have several different names for our invoice
script, and want to avoid having to repeat all of them for each of the
rewrite rules. So having them in a variable is a time saver when it
needs to get updated.


.. warning::

   Because ``Define``, and variable substitution, happen when the
   configuration file is parsed, rather than on each request, this recipe
   may only be used in your server configuration file, and not in
   ``.htaccess`` files.


.. _See_Also_rewrite_variable:

See Also
~~~~~~~~


* :ref:`Recipe_Define`


.. _Recipe_rewrite-logging:

Logging rewrites
----------------

.. index:: Logging,mod_rewrite

.. index:: mod_rewrite,Logging

.. index:: RewriteLog

.. index:: LogLevel

.. index:: Trace logging


.. _Problem_rewrite-logging:

Problem
~~~~~~~


When things go wrong with ``mod_rewrite``, it is useful to know exactly
what's happening. How can I log all rewrite activity?


.. _Solution_rewrite-logging:

Solution
~~~~~~~~


For httpd 2.2 and earlier:


.. code-block:: text

   RewriteLog logs/rewrite.log
   RewriteLogLevel 9


For httpd 2.4 and later:


.. code-block:: text

   LogLevel warn rewrite:trace5


.. _Discussion_rewrite-logging:

Discussion
~~~~~~~~~~


The very best way to debug your rewrite expressions is to follow the
logs and see exactly what ``mod_rewrite`` thought you meant. This is
also the best way to learn more about ``mod_rewrite``, and, indeed is
one of the main ways that this author
learned. [#rewrite-book]_

The way that log files are configured was changed significantly in
httpd 2.4, so the way that you'll log the actions of ``mod_rewrite``
will be different before and after that release.

In 2.2 and earlier, ``mod_rewrite`` provides its own logging directive,
``RewriteLog``, which specifies the location of your rewrite log file.
And there's an associated directive, ``RewriteLogLevel``, where you
configure how noisy that log file will be. ``RewriteLogLevel`` accepts
values from 0 through 5, with 5 being the level at which it tells you
everything it's doing, and 0 being the level where it is silent.
We generally recommend that you turn it all the way up, so that you
benefit from everything it has to offer.

Log entries will look something like:


.. code-block:: text

   127.0.0.1 - - [19/Nov/2009:14:42:55 --0500]
   [vhost.example.com/sid#8475130][rid#867d470/initial] (2) init rewrite
   engine with requested uri /rich_bowen.png
   127.0.0.1 - - [19/Nov/2009:14:42:55 --0500]
   [vhost.example.com/sid#8475130][rid#867d470/initial] (3) applying
   pattern '.' to uri '/rich_bowen.png'
   127.0.0.1 - - [19/Nov/2009:14:42:55 --0500]
   [vhost.example.com/sid#8475130][rid#867d470/initial] (4) RewriteCond:
   input='/var/www/vhost.example.com/rich_bowen.png' pattern='!-d' =>
   matched
   127.0.0.1 - - [19/Nov/2009:14:42:55 --0500]
   [vhost.example.com/sid#8475130][rid#867d470/initial] (4) RewriteCond:
   input='/var/www/vhost.example.com/rich_bowen.png' pattern='!-f' =>
   matched
   127.0.0.1 - - [19/Nov/2009:14:42:55 --0500]
   [vhost.example.com/sid#8475130][rid#867d470/initial] (2) rewrite
   /rich_bowen.png -> /index.php
   127.0.0.1 - - [19/Nov/2009:14:42:55 --0500]
   [vhost.example.com/sid#8475130][rid#867d470/initial] (2) local path
   result: /index.php
   127.0.0.1 - - [19/Nov/2009:14:42:55 --0500]
   [vhost.example.com/sid#8475130][rid#867d470/initial] (2) prefixed with
   document_root to /var/www/vhost.example.com/index.php
   127.0.0.1 - - [19/Nov/2009:14:42:55 --0500]
   [vhost.example.com/sid#8475130][rid#867d470/initial] (1) go-ahead with
   /var/www/vhost.example.com/index.php [OK]


If you read through that carefully line by line, you'll be able to
follow the flow through from the moment the request is received, and
see what regular expression is being applied, and to which requested
URI.

In this case, the rule set in question was:


.. code-block:: text

   RewriteCond %{DOCUMENT_ROOT}%{REQUEST_URI} !-d
   RewriteCond %{DOCUMENT_ROOT}%{REQUEST_URI} !-f
   RewriteRule . /index.php


You should be able to see each of those lines being considered, and
what happened. 

If you're using ``mod_rewrite`` in ``.htaccess`` or
**per**-directory context, you'll see the initial directory path being
removed at the beginning of a request, and added back on at the end.

Here's what each part of a log entry means:

``[vhost.example.com/sid#8475130]`` - The virtual host to which the request was directed, and the
associated Server ID.

``[rid#867d470/initial]`` - The request ID, and whether it was the
initial request or a subrequest.

``(4)`` - The log level at which this particular line was generated.


.. code-block:: text

   RewriteCond:   input='/var/www/vhost.example.com/rich_bowen.png'
   pattern='!-d' =>      matched`


The detailed log message. In this case, it tells us what the input and
pattern of a particular ``RewriteCond`` were, and then tells us that the
comparison was successful, and the rule matched.

In httpd 2.4 and later, logging was significantly enhanced. See
:ref:`Chapter_Logging`, **Logging**, for much more on this topic. One of the big
enhancements was that now logging can be configured **per**-module. In 2.2
and earlier, ``mod_rewrite`` and ``mod_ssl`` had their own log files, but
other modules were forced to log at the same level as the main server.
You can now configure the log level as precisely as you like, for each
module.

See :ref:`Recipe_Detailed_Errors` for details on the various log levels
you can select, and the syntax for setting levels **per** module.

To configure logging for ``mod_rewrite``, for example, 


.. code-block:: text

   LogLevel warn rewrite:trace5


Log entries will appear in the server error log, alongside the other
error and debug log entries. You can find just the entries from
``mod_rewrite`` by looking for lines containing ``rewrite``:


.. code-block:: text

   tail -f /var/log/httpd/error_log | grep rewrite


The log entries will look somewhat similar to the ones shown in the
2.2 example above, but contain a few more pieces of information. The
format in which this information is presented is configurable, using
the ``ErrorLogFormat`` directive (See :ref:`Recipe_Understanding_ErrorLog` 
for more details), but the following is an example entry:


.. code-block:: text

   [Wed Mar 23 09:15:49.396330 2016] [rewrite:trace3] [pid 10850:tid
   140168447084288] mod_rewrite.c(476): [client 127.0.0.1:44110]
   127.0.0.1 - - [localhost/sid#561991461450][rid#7f7b780236b0/initial]
   applying pattern '.' to uri '/favicon.ico', referer: http://localhost/


In addition to the information provided in the httpd 2.2 example,
you'll also see the source file, and line number, from which the
message was generated.

Logging ``mod_rewrite`` activity, and seeing what it does on every
single request, can be very eye-opening in terms of the performance
implications of using ``mod_rewrite``, as well as what differences it
can make to fine-tune your rule sets.

Finally, be sure to turn off rewrite logging on your production
server. Even the simplest ruleset can produce dozens of log entries
**per** request, and this can be a significant performance hit on servers
that are getting any amount of live traffic.


.. _See_Also_rewrite-logging:

See Also
~~~~~~~~


* :ref:`Recipe_Detailed_Errors`

* http://httpd.apache.org/docs/2.2/mod/mod_rewrite.html#rewriteloglevel

* http://wiki.apache.org/httpd/RewriteLog

* :ref:`Recipe_Understanding_ErrorLog`

Summary
-------


``mod_rewrite`` is a complicated topic, and this chapter only scratches
the surface of what is possible with this very powerful module.

Two thoughts we'll leave you with, before we move on to the next
chapter.

First, use ``mod_rewrite`` as a last resort, not as the first tool out
of your bag. While it is indeed very poweful, and can do almost
anything, it can be a drain on your servers performance when used for
things that have other, simpler solutions.

Second, if you want to learn more about ``mod_rewrite``, the very best
place to go is the documentation, at
http://httpd.apache.org/docs/rewrite/. There's also a book
on the topic - The Definitive Guide to Apache mod_rewrite, by Rich
Bowen - but, as of this writing, it is rather dated.


.. rubric:: Footnotes

.. [#wildcard-dns] You will still need to ensure that you have the appropriate DNS records in place, or a wildcard DNS record, in order for the hostnames to actually correspond to a target web server.
.. [#rewrite-book] I even wrote a book about it - The Definitive Guide to Apache mod_rewrite.
