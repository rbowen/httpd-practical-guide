
.. _Chapter_per_request:

==========================
Programmable Configuration
==========================

.. epigraph::

   We are the robots.

   -- Kraftwerk, *The Robots*


.. index:: Per-request configuration

.. index:: mod_macro

.. index:: Modules,mod_macro


Apache httpd 2.4 introduced a powerful expression parser engine, along
with the ``<If>``, ``<ElseIf>``, and ``<Else>`` directives, enabling
per-request configuration decisions based on arbitrary expressions.
These features are covered in detail in our companion book, *mod_rewrite
And Friends*, in the chapter titled *Configurable Configuration*.

In this chapter, I focus on other methods for scripting, or
programming, your configuration file. This includes the ``Define`` and
``IfDefine`` directives, the ``mod_macro`` module, and mass virtual
hosting with ``mod_vhost_alias``.

.. Requires httpd 2.4


.. admonition:: Modules covered in this chapter

   :module:`mod_macro`, :module:`mod_rewrite`, :module:`mod_vhost_alias`


.. _recipe-expr-stubs:

Recipes moved to *mod_rewrite And Friends*
------------------------------------------

The following recipes have been moved to our companion book,
*mod_rewrite And Friends*, in the chapter *Configurable Configuration*.
The labels below are preserved so that cross-references from other
chapters continue to resolve.

.. _Recipe_expr:

General purpose expression parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ — See *mod_rewrite And Friends*,
*Configurable Configuration*.

.. _Recipe_If:

Using the <If> Directive
~~~~~~~~~~~~~~~~~~~~~~~~ — See *mod_rewrite And Friends*,
*Configurable Configuration*.

.. _Recipe_else:

Using the <Else> directive
~~~~~~~~~~~~~~~~~~~~~~~~~~ — See *mod_rewrite And Friends*,
*Configurable Configuration*.

.. _Recipe_image-theft-if:

Preventing image theft using <If>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ — See *mod_rewrite And Friends*,
*Configurable Configuration*.

.. _Recipe_expr-errordocument:

Using an expression in an ErrorDocument
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ — See *mod_rewrite And
Friends*, *Configurable Configuration*.

.. _Recipe_locationmatch-backref:

Using backreferences from a <LocationMatch>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ — See *mod_rewrite And
Friends*, *Configurable Configuration*.

.. _Recipe_setenvifexpr:

**Setting an environment variable based on an expression** — See
*mod_rewrite And Friends*, *Configurable Configuration*.

.. _Recipe_setting-headers-with-expr:

**Setting HTTP headers based on expressions** — See *mod_rewrite And
Friends*, *Configurable Configuration*.

.. _Recipe_LogMessage-with-expr:

**Setting custom log messages with the expression engine** — See
*mod_rewrite And Friends*, *Configurable Configuration*.

.. _Recipe_expr-auth:

**Authorization using expressions** — See *mod_rewrite And Friends*,
*Configurable Configuration*.


.. Requires httpd 2.4

.. _Recipe_Define:

Setting variables with Define
-----------------------------

.. index:: Define

.. index:: IfDefine

.. index:: Configuration variables

.. index:: Variables in configuration files


.. _Problem_Define:

Problem
~~~~~~~


You want to set a variable, and then use it multiple times in your
configuration file.


.. _Solution_Define:

Solution
~~~~~~~~


Set a variable with ``Define``, and then reference that variable in
other directive values:


.. code-block:: text

   Define DOCROOT "/var/www"
   
   DocumentRoot "${DOCROOT}"
   
   <Directory "${DOCROOT}">
       # ...
   </Directory>


.. _Discussion_Define:

Discussion
~~~~~~~~~~


The ``Define`` directive, which is new in httpd 2.4, allows you to
define variables which can then be used as part of the arguments to
any further configuration directives. ``Define`` can be set in server
(global) scope, or in a ``VirtualHost``.

However, because variable definition, and variable substitution,
happens when the configuration file is loaded, rather than at request
time, ``Define`` cannot be used in ``.htaccess`` files.


.. warning::

   While you can set a ``Define`` inside a ``<VirtualHost>`` block, it is not
   scoped to that block. Which means that the value defined is still in
   effect after the closing ``</VirtualHost>`` tag. So, if you're going to
   use ``Define`` in a ``<VirtualHost>``, I recommend that you ``UnDefine`` it
   at the bottom of the section. (See :ref:`Recipe_Undefine` for more detail.)


If the second parameter is omitted, the variable is simply set to
``TRUE``, which can then be consulted in an ``IfDefine`` statement. This
is equivalent to using the ``-D`` flag on server startup. (See
:ref:`Recipe_IfDefine` for more detail.)

There's no restriction on variable names. The examples in this recipe,
and in the documentation, use all upper-case variable names, but this
is not required. You should, however, use the ``${VAR}`` syntax to
reference the variable.

You should also take great care to avoid any variable overlap with
your usage of ``mod_macro``, if any, to avoid confusion.


.. _See_Also_Define:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/core.html#define

* :ref:`Recipe_IfDefine`

* :ref:`Recipe_Undefine`

* :ref:`Recipe_mod_macro`


.. _Recipe_IfDefine:

Using IfDefine for conditional configuration
--------------------------------------------

.. index:: Define

.. index:: IfDefine

.. index:: -D


.. _Problem_IfDefine:

Problem
~~~~~~~


You wish to have certain parts of the configuration in effect only in
certain conditions.


.. _Solution_IfDefine:

Solution
~~~~~~~~


Use ``<IfDefine>`` to turn blocks of configuration on or off, based on
the presence of a particular variable. Use the ``-D`` flag at server
startup to set these variables on or off.

For example, in your configuration, you might use the following
configuration:


.. code-block:: text

   <IfDefine testing>
       LogLevel debug
       DocumentRoot /var/www/devel
   </IfDefine>
   <IfDefine !testing>
       LogLevel info
       DocumentRoot /var/www/production
   </IfDefine>


And then start your server using the ``-Dtesting`` parameter to invoke
the development environment.


.. code-block:: text

   httpd -Dtesting -k start


.. _Discussion_IfDefine:

Discussion
~~~~~~~~~~


The ``-D`` flag sets (mnemonic: "-Define") an environment variable,
which the configuration engine can then use to determine whether to
turn certain configuration blocks on or off. With the recipe given
above, to use the first of these blocks, you would start your server
using:


.. code-block:: text

   httpd -Dtesting -k start


But to start the server using the second block - the production
environment, you'd omit that first argument:


.. code-block:: text

   httpd -k start


In this way, you can deploy the same configuration file to multiple
servers, and control what configuration is actually in play by the server startup
parameters.


.. note::

   You might find older howto articles that tell you to start ``httpd``
   with the ``-DSSL`` flag in order to enable SSL. This is no longer the
   case by default, but you could use the above technique to set things
   up that way, if you wanted.


You can also use ``IfDefine`` to test the value of variables that have
been set with the ``Define`` directive, if you prefer to put the
variable in the configuration file rather than in the server startup
flags:


.. code-block:: text

   Define testing
   
   <IfDefine testing>
       LogLevel debug
       DocumentRoot /var/www/devel
   </IfDefine>
   <IfDefine !testing>
       LogLevel info
       DocumentRoot /var/www/production
   </IfDefine>


In your production environment, you'd comment out that line ...


.. code-block:: text

   # Define testing
   
   <IfDefine testing>
       LogLevel debug
       DocumentRoot /var/www/devel
   </IfDefine>
   <IfDefine !testing>
       LogLevel info
       DocumentRoot /var/www/production
   </IfDefine>


Then restart the server, to start it in production mode.

The advantage here is that you can very obviously tell, by looking at
the active configuration file, what the current configuration is,
rather than having to look at a process list to figure out how the
server was invoked.


.. _See_Also_IfDefine:

See Also
~~~~~~~~


* :ref:`Recipe_Define`

* :ref:`Recipe_Undefine`

* http://httpd.apache.org/docs/trunk/mod/core.html#ifdefine


.. _Recipe_Undefine:

Undefine
--------

.. index:: UnDefine


.. _Problem_Undefine:

Problem
~~~~~~~


You want to undefine a variable after using it, so that it doesn't
cause conflict in other parts of the configuration.


.. _Solution_Undefine:

Solution
~~~~~~~~


Use ``UnDefine`` to remove a variable.


.. code-block:: text

   Define DOCROOT "/var/www/html"
   
   DocumentRoot "${DOCROOT}"
   
   <Directory "${DOCROOT}">
       # ...
   </Directory>
   
   UnDefine DOCROOT


.. _Discussion_Undefine:

Discussion
~~~~~~~~~~


As your configuration grows larger, using variables can be a great way
to ensure that changing a value one place doesn't overlook changing it
elsewhere. This is particularly true of managing directory paths, as
things are moved around.

However, on a server with multiple virtual hosts, multiple
applications, and multiple content managers, it frequently happens
that the same variable **name** gets used for more than one thing,
across these scattered parts of the site.

If you end up using the same variable name in multiple places - such
as in the ``DOCROOT`` example, above, in the case of having many virtual
hosts - you should "clean up" after yourself by undefining these
variables. This will ensure that the value from one usage doesn't
bleed over into another, resulting in unexpected, and hard to find,
errors.

Also consider using ``mod_macro`` to manage scenarios where you have
many examples of repeated, or, at least, very similar, configuration
blocks. (See :ref:`Recipe_mod_macro` for further discussion.)


.. _See_Also_Undefine:

See Also
~~~~~~~~


* :ref:`Recipe_Define`

* :ref:`Recipe_mod_macro`


.. _Recipe_mod_macro:

Using mod_macro to script configuration sections
------------------------------------------------

.. index:: mod_macro

.. index:: Modules,mod_macro

.. index:: Scripting configuration sections


.. _Problem_mod_macro:

Problem
~~~~~~~


You have repeated configuration blocks with only minor differences,
and you wish to convert this to a macro with variables.


.. _Solution_mod_macro:

Solution
~~~~~~~~


Use ``mod_macro`` to define the repeated blocks and fill in the
variables. For example, you might use ``mod_macro`` to define your
standard virtual host layout:


.. code-block:: text

   # Standardized virtual host
   <Macro VHost $name $domain>
     <VirtualHost *:80>
         ServerName $domain
         ServerAlias www.$domain
   
         DocumentRoot "/var/www/vhosts/$name"
         ErrorLog "/var/log/httpd/$name.error_log"
         CustomLog "/var/log/httpd/$name.access_log" combined
     </VirtualHost>
   
     # Grant access to the doc directory
     <Directory /var/www/vhosts/$name>
         AllowOverride None
         Require all granted
     </Directory>
   
   </Macro>


Then invoke that with the details of each virtual host:


.. code-block:: text

   Use VHost example  example.com
   Use VHost apache   apache.org
   Use VHost personal mysite.me


These values are filled in at server startup.


.. _Discussion_mod_macro:

Discussion
~~~~~~~~~~


``mod_macro``, as the name implies, lets you write macros as part of
your server configuration.

``mod_macro`` has been available as a third-party module for many years.
With the 2.4 release of httpd, it's one of the included modules. This
has the advantage that it is always developed, tested, and documented,
right alongside the core code. So you don't have to go looking for it
somewhere else. And you're always ensured that it will work correctly
for the version that you're installing.

When ``mod_macro`` was first introduced, many web server administrators
were running just one or two websites, and didn't need this kind of
power. However, over the years, it has become more and more common
that server administrators have tens, or even hundreds, of virtual
host, with multiple applications running on each, and need to manage
these configurations in a way that is clear and efficient. ``mod_macro``
offers one such way of doing this, providing consistency across your
configuration, and a very fast way of adding new instances, or
removing ones that are no longer needed.

In the above recipe example, once you have decided on a standardized
layout of our virtual hosts document directories and log files, it now
takes only a single line to add a new virtual host. And it provides a
single place to update things that you need to change globally, such
as an SSL cipher suite that you wish to change across all hosts, for
example.


.. _See_Also_mod_macro:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_macro.html

* :ref:`Recipe_multi-part-macro`


.. _Recipe_multi-part-macro:

Multi-part macros with mod_macro
--------------------------------

.. index:: mod_macro,multi-part macros


.. _Problem_multi-part-macro:

Problem
~~~~~~~


While the recipe given in :ref:`Recipe_mod_macro` might be nice an ideal
world, in the real world, every virtual host is different in some
small way. You want to use ``mod_macro``, but still allow for these
uniquenesses.


.. _Solution_multi-part-macro:

Solution
~~~~~~~~


Split your macro into two parts, and insert the unique parts between.


.. code-block:: text

   # Start standardized virtual host
   <Macro VhostStart $name $domain>
     <VirtualHost *:80>
         ServerName $domain
         ServerAlias www.$domain
   
         DocumentRoot "/var/www/vhosts/$name"
         ErrorLog "/var/log/httpd/$name.error_log"
         CustomLog "/var/log/httpd/$name.access_log" combined
   </Macro>
   
   # End standardized virtual host
   <Macro VhostEnd $name $domain>
   </VirtualHost>
   
     <Directory /var/www/vhosts/$name>
         AllowOverride None
         Require all granted
     </Directory>
   
   </Macro>


Now, each virtual host consists of two ``Use`` directives, with,
optionally, unique configuration appearing between:


.. code-block:: text

   # www.rcbowen.com virtual host
   Use VhostStart rcbowen rcbowen.com
   
   # Unique to this site.
   Alias /stats/ /opt/webstats/rcbowen.com/
   
   Use VhostEnd   rcbowen rcbowen.com


The resulting configuration will be a standardized virtualhost, as in
:ref:`Recipe_mod_macro`, but with local variations.


.. _Discussion_multi-part-macro:

Discussion
~~~~~~~~~~


Using ``mod_macro``, or any templating solution, assumes that every site
is identical in layout and requirements. This is seldom true in the
real world. The solution offered here lets you gain most of the
advantages of a macro, but with the ability to make per-use
modifications.

Of course, the resulting configuration is no longer a simple one-line
invocation of the macro, but this approach avoids repeating any of the
parts that are identical between sites.

This same technique can be used for other portions of your
configuration, such as a standard way to deploy an application - say,
Wordpress or Drupal - that you need to invoke multiple times in your
configuration, with local variations.

Finally, note that order matters in configuration files. If there's
a standard file location, such as the ``DocumentRoot``, that you will
need to override on a per-site basis, you can put this in the first
half of the macro, and then override before invoking the second half
of the macro.


.. _See_Also_multi-part-macro:

See Also
~~~~~~~~


* :ref:`Recipe_mod_macro`


.. _Recipe_vhost_alias:

Configuring virtual hosts with mod_vhost_alias
----------------------------------------------

.. index:: mod_vhost_alias

.. index:: Modules,mod_vhost_alias

.. index:: Virtual hosts,mod_vhost_alias


.. _Problem_vhost_alias:

Problem
~~~~~~~


You want to automatically define a virtual host based on the hostname.


.. _Solution_vhost_alias:

Solution
~~~~~~~~


Use ``mod_vhost_alias``. This module is discussed in
:ref:`Recipe_mod_vhost_alias`.

.. note::

   The primary recipe for ``mod_vhost_alias`` lives in
   :ref:`Chapter_Virtual_hosts`, **Virtual Hosts**. See
   :ref:`Recipe_mod_vhost_alias` for the full discussion, including
   configuration examples and directory layout conventions.



.. admonition:: DRAFT — Review needed

   The following recipe was auto-generated and needs editorial review.
   Check technical accuracy, voice/tone, and fit with surrounding content.

.. _Recipe_mod_version:

Version-conditional configuration with mod_version
---------------------------------------------------

.. index:: mod_version

.. index:: Modules,mod_version

.. index:: IfVersion

.. index:: Version-conditional configuration


.. _Problem_mod_version:

Problem
~~~~~~~


You need a single configuration file to work correctly across multiple
versions of Apache httpd -- for example, during a phased migration
from 2.2 to 2.4, or across a fleet where not every server has been
upgraded at the same time.


.. _Solution_mod_version:

Solution
~~~~~~~~


Use ``mod_version`` and the ``<IfVersion>`` directive to wrap
configuration blocks that should only apply to specific httpd
versions:


.. code-block:: text

   <IfVersion >= 2.4>
       Require all granted
   </IfVersion>
   <IfVersion < 2.4>
       Order allow,deny
       Allow from all
   </IfVersion>


.. _Discussion_mod_version:

Discussion
~~~~~~~~~~


``mod_version`` provides the ``<IfVersion>`` container directive,
which evaluates at configuration-load time -- not at request time --
and includes or excludes the enclosed directives based on the running
httpd version. This makes it invaluable when you maintain a shared
configuration that must be portable across different httpd releases.

The ``<IfVersion>`` directive accepts a version number in the form
``major[.minor[.patch]]``. If you omit the minor or patch components
they are assumed to be zero. So ``<IfVersion >= 2.4>`` is equivalent
to ``<IfVersion >= 2.4.0>``.

The following comparison operators are available:

.. code-block:: text

   =  or ==     httpd version is equal
   >            httpd version is greater than
   >=           httpd version is greater or equal
   <            httpd version is less than
   <=           httpd version is less or equal
   ~            version matches a regular expression

If you omit the operator entirely, ``=`` is assumed. So
``<IfVersion 2.4.2>`` is equivalent to ``<IfVersion = 2.4.2>``.

Any operator can be negated by prefixing it with an exclamation mark.
For example, ``<IfVersion !~ ^2.2>`` matches everything that is
*not* a 2.2.x release.

**Handling the 2.2 to 2.4 authorization change**

One of the most common uses for ``<IfVersion>`` is the authorization
syntax change between 2.2 and 2.4. In httpd 2.4 the old ``Order``,
``Allow``, and ``Deny`` directives were replaced by ``mod_authz_core``
and the ``Require`` directive. A shared configuration can handle both:


.. code-block:: text

   <Directory "/var/www/html">
       <IfVersion >= 2.4>
           Require all granted
       </IfVersion>
       <IfVersion < 2.4>
           Order allow,deny
           Allow from all
       </IfVersion>
   </Directory>


**Enabling features only available in newer versions**

Some directives were introduced in specific point releases. For
example, ``Protocols`` (for HTTP/2 support) appeared in 2.4.17. You
can guard it so that older 2.4.x installations don't throw an error:


.. code-block:: text

   <IfVersion >= 2.4.17>
       Protocols h2 h2c http/1.1
   </IfVersion>


**Testing for specific minor versions with regular expressions**

The ``~`` operator lets you match against a regular expression. This
is useful when you need to work around a bug in a particular set of
releases, or target a family of point releases:


.. code-block:: text

   <IfVersion ~ ^2\.4\.[0-4]$>
       # Workaround for a bug fixed in 2.4.5
       SetEnv downgrade-1.0
   </IfVersion>

You can also write this with the ``=`` operator and a
slash-delimited regex:

.. code-block:: text

   <IfVersion = /^2\.4\.[0-4]$/>
       SetEnv downgrade-1.0
   </IfVersion>


**When to use <IfVersion> versus <IfModule>**

Both ``<IfVersion>`` and ``<IfModule>`` let you conditionally include
configuration blocks, but they answer different questions.
``<IfModule>`` asks *"Is this module loaded?"* while ``<IfVersion>``
asks *"What version of httpd is running?"* The distinction matters:

* Use ``<IfModule>`` when functionality depends on an optional module
  that may or may not be compiled in, regardless of version --
  for example, ``mod_ssl`` or ``mod_http2``.

* Use ``<IfVersion>`` when functionality depends on the httpd version
  itself -- for example, when the core syntax changed between
  releases, or a directive was added in a specific point release.

* In migration scenarios, ``<IfVersion>`` is usually the right choice,
  because the old and new directives may both be recognized by a
  transitional version (via ``mod_access_compat``) but only one
  set is correct.

Because ``<IfVersion>`` is evaluated at configuration time and not at
request time, it carries no per-request performance cost. The
directives inside a non-matching ``<IfVersion>`` block are simply
skipped when the configuration is loaded, exactly like ``<IfDefine>``
or ``<IfModule>``.


.. note::

   ``mod_version`` must be loaded for ``<IfVersion>`` to be
   recognized. On most distributions it is compiled in by default. If
   you are unsure, check with ``httpd -M | grep version``.


.. _See_Also_mod_version:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_version.html

* :ref:`Recipe_If`

* :ref:`Recipe_IfDefine`

* :ref:`Recipe_Define`


Summary
-------


This chapter covered several ways to make your Apache httpd
configuration more dynamic and maintainable. The ``Define`` and
``IfDefine`` directives let you parameterize and conditionalize your
configuration files, while ``mod_macro`` brings true templating to
complex, repetitive setups like mass virtual hosting.

For coverage of the expression parser, the ``<If>``/``<ElseIf>``/``<Else>``
directives, expression-based headers, environment variables,
backreferences, and authorization expressions, see our companion book,
*mod_rewrite And Friends*, in the chapter *Configurable Configuration*.
