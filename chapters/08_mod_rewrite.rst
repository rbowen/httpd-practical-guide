
.. _Chapter_mod_rewrite:

==============================
URL Rewriting with mod_rewrite
==============================

.. epigraph::

   | Should I stay or should I go now?
   | If I go, there will be trouble.
   | And if I stay, it will be double.

   -- The Clash, *Should I Stay or Should I Go*


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
expressions. In this chapter, I'll cover the most important
use of regex in Apache httpd — URL rewriting with :module:`mod_rewrite`.

:module:`mod_rewrite` is the most powerful, and perhaps the most
misunderstood, module in the Apache httpd. Its primary purpose is
to manipulate and rewrite incoming requests based on a wide variety of
conditions and variables. You can redirect users to a canonical
hostname, force HTTPS, present clean URLs that hide your back-end
implementation, and much more.

This chapter covers only the most common, essential recipes. For
comprehensive coverage — including ``RewriteMap``, ``RewriteCond``
variables, the full flags reference, logging, time-based and
browser-based rewriting, and dozens of additional recipes — please see
my companion book, *mod_rewrite And Friends*, available on Amazon. That
book is dedicated entirely to :module:`mod_rewrite` and related URL
manipulation techniques, and goes into far greater depth than I can
here.

.. note::

   Every ``RewriteRule`` directive requires that the rewrite engine be
   turned on in the appropriate scope. When in doubt, place the
   following before your rules::

      RewriteEngine On


.. _Recipe_canonical-hostname:

Enforcing a Preferred Hostname
------------------------------

.. index:: Canonical hostname

.. index:: www vs no-www

.. index:: RewriteRule,Canonical hostname

.. index:: Enforcing a preferred hostname


.. _Problem_canonical-hostname:

Problem
~~~~~~~

You want all visitors to reach your site via a single canonical
hostname — for example, ``www.example.com`` rather than
``example.com`` — so that search engines don't treat them as separate
sites.


.. _Solution_canonical-hostname:

Solution
~~~~~~~~

In a ``.htaccess`` file or ``<Directory>`` context where you don't
control virtual host definitions:

.. code-block:: apache

   RewriteEngine On
   RewriteCond %{HTTP_HOST} !^www\. [NC]
   RewriteRule ^ http://www.example.com%{REQUEST_URI} [R=301,L]

If you have access to the server configuration, a pair of virtual
hosts is more efficient:

.. code-block:: apache

   <VirtualHost *:80>
     ServerName example.com
     Redirect permanent / http://www.example.com/
   </VirtualHost>

   <VirtualHost *:80>
     ServerName www.example.com
     DocumentRoot /var/www/html
   </VirtualHost>


.. _Discussion_canonical-hostname:

Discussion
~~~~~~~~~~

The ``RewriteCond`` checks whether the incoming ``Host`` header does
*not* start with ``www.``. If it doesn't, the ``RewriteRule`` issues
a 301 (permanent) redirect to the ``www`` version of the URL.

The virtual-host approach is preferred when possible, because the
redirect happens once — on the first request to the wrong hostname —
and the rewrite engine is never invoked at all. With the
``RewriteRule`` approach, every single request is tested against the
condition, adding a small but unnecessary overhead.

To redirect in the opposite direction (``www`` to non-``www``),
simply flip the condition:

.. code-block:: apache

   RewriteCond %{HTTP_HOST} ^www\.(.+)$ [NC]
   RewriteRule ^ http://%1%{REQUEST_URI} [R=301,L]


.. _See_Also_canonical-hostname:

See Also
~~~~~~~~

* https://httpd.apache.org/docs/current/rewrite/remapping.html
* *mod_rewrite And Friends* by Rich Bowen (Amazon) for additional
  hostname canonicalization patterns


.. _Recipe_rewrite-https-redirect:

Redirecting HTTP to HTTPS
-------------------------

.. index:: HTTPS redirect

.. index:: SSL redirect

.. index:: RewriteRule,HTTPS


Problem
~~~~~~~

You want to ensure that all traffic to your site uses HTTPS, and
that any plain HTTP request is redirected to the secure version.


Solution
~~~~~~~~

In the server configuration for your port-80 virtual host:

.. code-block:: apache

   <VirtualHost *:80>
     ServerName www.example.com
     RewriteEngine On
     RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
   </VirtualHost>

Or in a ``.htaccess`` file:

.. code-block:: apache

   RewriteEngine On
   RewriteCond %{HTTPS} off
   RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]


Discussion
~~~~~~~~~~

In the virtual-host approach, the entire port-80 host exists only
to redirect — every request, regardless of path, is sent to the
``https://`` equivalent. No ``RewriteCond`` is needed because this
virtual host, by definition, only receives non-HTTPS requests.

In a ``.htaccess`` file, you don't control which virtual host the
request arrived on, so the ``RewriteCond %{HTTPS} off`` test ensures
the rule fires only for plain HTTP connections.

Use ``R=301`` (permanent redirect) once you've confirmed everything
works. During testing, ``R=302`` (temporary) is safer — browsers
cache 301 redirects aggressively and getting one wrong can be painful
to undo.

.. tip::

   Modern best practice is to combine this redirect with the
   ``Strict-Transport-Security`` header on your HTTPS virtual host,
   so that browsers remember to use HTTPS without needing the
   redirect on subsequent visits.


.. _Recipe_path_to_querystring:

Clean URLs — Rewriting Paths to Query Strings
----------------------------------------------

.. index:: Query string

.. index:: SEO

.. index:: Beautiful URLs

.. index:: Clean URLs


.. _Problem_path_to_querystring:

Problem
~~~~~~~

You want human-readable URLs like ``/book/apache/bowen`` to be
internally rewritten to a back-end script with query-string arguments,
such as ``/cgi-bin/book.cgi?subject=apache&author=bowen``.


.. _Solution_path_to_querystring:

Solution
~~~~~~~~

.. code-block:: apache

   RewriteEngine On
   RewriteRule "^/book/([^/]+)/([^/]+)" "/cgi-bin/book.cgi?subject=$1&author=$2" [PT]


.. _Discussion_path_to_querystring:

Discussion
~~~~~~~~~~

The parenthesised groups in the pattern capture the path segments.
``$1`` and ``$2`` in the target insert those captured values as
query-string parameters. The rewrite is entirely internal — the user
sees only the clean URL in their browser.

The ``[PT]`` (passthrough) flag tells httpd to keep processing the
rewritten URL through the normal request pipeline, so that CGI
handling, alias resolution, and other modules still apply. Without
it, httpd would attempt to serve the rewritten path as a literal
file.

If the original URL might already carry a query string that you
want to preserve, add the ``QSA`` (query string append) flag:

.. code-block:: apache

   RewriteRule "^/book/([^/]+)/([^/]+)" "/cgi-bin/book.cgi?subject=$1&author=$2" [QSA,PT]

Without ``QSA``, the original query string is silently discarded.


.. _See_Also_path_to_querystring:

See Also
~~~~~~~~

* https://httpd.apache.org/docs/current/mod/mod_rewrite.html
* *mod_rewrite And Friends* by Rich Bowen (Amazon) for advanced
  URL-to-query-string techniques, including ``RewriteMap``


.. _Recipe_rewrite-htaccess:

Using RewriteRule in .htaccess Files
------------------------------------

.. index:: Rewrite,htaccess

.. index:: htaccess,Rewrite


.. _Problem_rewrite-htaccess:

Problem
~~~~~~~

Your ``RewriteRule`` works in the server configuration but fails
when you move it to a ``.htaccess`` file.


.. _Solution_rewrite-htaccess:

Solution
~~~~~~~~

Remove any leading slash (and directory path) from your
``RewriteRule`` pattern. Paths in ``.htaccess`` files are always
relative to the directory the file lives in.


.. _Discussion_rewrite-htaccess:

Discussion
~~~~~~~~~~

``.htaccess`` files provide per-directory configuration, and
``RewriteRule`` behaves differently inside them. The key difference:
the directory prefix is stripped before the pattern is applied.

In ``httpd.conf``:

.. code-block:: apache

   RewriteRule ^/images/(.+)\.jpg /images/$1.png

In a ``.htaccess`` file in the document root:

.. code-block:: apache

   RewriteRule ^images/(.+)\.jpg images/$1.png

In a ``.htaccess`` file inside the ``images/`` directory itself:

.. code-block:: apache

   RewriteRule ^(.+)\.jpg $1.png

The rule is the same in each case — only the path prefix changes.
Forgetting to remove the leading slash is the single most common
:module:`mod_rewrite` mistake in ``.htaccess`` files.

See :ref:`Chapter_htaccess`, **.htaccess Files**, for a full
discussion of ``.htaccess`` advantages and limitations.


.. _See_Also_rewrite-htaccess:

See Also
~~~~~~~~

* :ref:`Chapter_htaccess`, **.htaccess Files**
* *mod_rewrite And Friends* by Rich Bowen (Amazon) for
  per-directory rewrite edge cases and debugging techniques


.. _further_reading_mod_rewrite:

Further Reading
---------------

This chapter has covered only the most frequently needed
:module:`mod_rewrite` recipes. The module is extraordinarily flexible,
supporting conditional rewriting based on time of day, browser type,
query-string content, environment variables, database lookups via
``RewriteMap``, and much more.

For comprehensive coverage of all of these topics, please see:

* **mod_rewrite And Friends** by Rich Bowen — available on Amazon.
  This companion book is dedicated entirely to :module:`mod_rewrite`
  and covers dozens of additional recipes, including ``RewriteMap``
  (text, DBM, program, and SQL maps), the complete flags reference,
  conditional rewriting with ``RewriteCond``, ``<If>``-based
  alternatives, logging and debugging, and real-world case studies.

* The official Apache httpd documentation:
  https://httpd.apache.org/docs/current/rewrite/

* The Apache httpd wiki:
  https://wiki.apache.org/httpd/RewriteGuide


.. _Recipe_rewrite-syntax:
.. _Recipe_simple-rewrite:
.. _Recipe_rewrite-flags:
.. _Rewrite-flags-definitions:
.. _Recipe_rewrite-pt:
.. _Recipe_rewrite-env-flag:
.. _Recipe_rewrite-handler-flag:
.. _Recipe_rewrite-next-flag:
.. _Recipe_rewrite-nc-flag:
.. _Recipe_rewrite-cookie-flag:
.. _CO-flag-arguments:
.. _Recipe_rewrite-qsa-flag:
.. _Recipe_RewriteCond:
.. _Recipe_rewrite-time-of-day:
.. _Recipe_rewritecond-mobile-client:
.. _Recipe_rewrite-expr:
.. _Recipe_RewriteCond_filetest:
.. _Recipe_rewritecond_alpha:
.. _Recipe_rewrite-by-query-string:
.. _Recipe_RewriteOptions:
.. _Recipe_rewrite-content-type:
.. _Recipe_image-theft:
.. _Recipe_php-source-rewrite:
.. _Recipe_rewrite-path-to-vhost:
.. _Recipe_rewrite-dynamic-vhost:
.. _Recipe_RewriteMap:
.. _Recipe_RewriteMap-default-value:
.. _Recipe_RewriteMap-rnd:
.. _Recipe_RewriteMap-rnd-weighted:
.. _Recipe_RewriteMap-dbm:
.. _Recipe_RewriteMap-int:
.. _RewriteMapIntFunctions:
.. _Recipe_RewriteMap-prg:
.. _Recipe_RewriteMap-dbd:
.. _Recipe_rewritecond-backreference:
.. _Recipe_rewrite-new-extension:
.. _Recipe_rewrite-looping:
.. _Recipe_rewrite-proxy:
.. _Recipe_rewrite_variable:
.. _Recipe_rewrite-logging:

Additional Recipes
------------------

The recipes formerly in this chapter — including RewriteMap, RewriteCond
variables, the flags reference, logging, time-based rewriting,
browser-based content serving, and more — have moved to
*mod_rewrite And Friends* by Rich Bowen, available on Amazon.
