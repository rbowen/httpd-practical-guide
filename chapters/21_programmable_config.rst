
.. _Chapter_per_request:

==========================
Programmable Configuration
==========================

.. index:: Per-request configuration

.. index:: <If>

.. index:: <Else>

.. index:: <ElseIf>

.. index:: mod_macro

.. index:: Modules,mod_macro


A major new category of functionality in Apache httpd 2.4 is what is
collectively called "per-request configuration." This consists of the
``<If>``, ``<ElseIf>``, and ``<Else>`` directives, as well as a general
purpose expression parser engine that can be used to evaluate
arbitrary expressions for the purpose of configuring the
server.

Additionally, in this chapter, we'll cover other methods for
scripting, or programming, your configuration file. This includes
directives like ``IfDefine``, and the ``mod_macro`` module.

[role="v24"]

.. _Recipe_expr:

General purpose expression parser
---------------------------------

.. index:: Expression parser

.. index:: Per-request configuration,Expression parser


.. _Problem_expr:

Problem
~~~~~~~


You want to evaluate an arbitrary expression at request time.


.. _Solution_expr:

Solution
~~~~~~~~


The general purpose expression parser allows you to evaluate
expressions at request time, either to set the value of a directive,
or make configuration decisions based on truth value of an expression.

The full syntax for this expression language is described at
http://httpd.apache.org/docs/expr.html


.. _Discussion_expr:

Discussion
~~~~~~~~~~


In httpd 2.4, new functionality has been added to the configuration
language to allow you to put arbitrary logical expressions in some
configuration directives, which are evaluated at request-time, rather
than at configuration time.

Of course, ``mod_rewrite`` already provided this functionality to a
certain extent. But the new expression language extends that
flexibility to a variety of other directives that, before, were rather
static.

In addition to using these expressions in rewrite directives (See
:ref:`Recipe_rewrite-expr` for an example), you can now use expressions
in authorization directives:


.. code-block:: text

   Require expr "%{TIME_HOUR} -ge 9 && %{TIME_HOUR} -le 17"


(See :ref:`Recipe_Authorization_by_expression` for more detail on this syntax.)

Expressions can be used in ``Header`` directives:


.. code-block:: text

   Header set Set-Cookie testcookie "expr=-z %{req:Cookie}"


(See
http://httpd.apache.org/docs/mod/mod_headers.html#header
for more details.)

And they can be used in a variety of other directives, which are
listed in the sidebar of the expression engine documentation (That's 
http://httpd.apache.org/docs/expr.html).

And, last but definitely not least, expressions can be used in the
``<If>``, ``<Elseif>``, and ``<Else>`` directives which will be discussed in
the recipes below.

You will find examples of this new syntax throughout this book. And
there will be several more examples in this chapter.


.. warning::

   You must be using httpd 2.4 to take advantage of this new syntax. It
   is not available in 2.2, and will not be backported.


.. _See_Also_expr:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/expr.html

* http://httpd.apache.org/docs/mod/mod_headers.html#header

* :ref:`Chapter_AAA`, **Authentication, Authorization, and Access Control**

[role="v24"]

.. _Recipe_If:

Using the <If> Directive
------------------------

.. index:: <If>

.. index:: Conditional configuration

.. index:: Optional configuration


.. _Problem_If:

Problem
~~~~~~~


You want to make a portion of your configuration conditional upon some
value that you won't know until request time.


.. _Solution_If:

Solution
~~~~~~~~


Use the ``<If>`` directive to enclose the conditional configuration
block:


.. code-block:: text

   <If "-R '10.1.0.0/16'">
       RedirectMatch . http://intranet/
   </If>


.. _Discussion_If:

Discussion
~~~~~~~~~~


The ``<If>`` directive was added in the 2.4 release of httpd to answer
the request that has been made since the earliest days of the Apache
web server. People have always wanted a conditional syntax in their
configuration files, so that request-time variables could determine
what configuration is applied.

``mod_rewrite`` was a partial solution to that need, and was introduced
in httpd 1.3. However, there were always cases that ``mod_rewrite``
couldn't handle. And besides, the syntax of ``mod_rewrite`` can be
cumbersome and intimidating.

In the example given, a ``RedirectMatch`` directive is made conditional
upon the address of the requesting client. If they're on the ``10.1``
network (**i.e.**, a client internal to the local network) we want to
redirect them to the intranet site.

The ``-R`` operator does IP address range matching, and, in this
case, asks whether the requesting address is in that particular
network.


.. warning::

   With great power comes great responsibility. Request-time
   configuration necessarily introduces a performance hit, as these
   expressions are evaluated. As with any run-time functionality,
   consider whether there's a better way to do it, and, if there isn't
   consider whether you can order things in your configuration file such
   that the more common conditions are matched first. In this way, you'll
   ensure that less common scenarios aren't even tested if the more
   common one matches. See :ref:`Chapter_Performance_and_testing`,
   **Performance and Testing**, for
   further discussion of this technique.


.. _See_Also_If:

See Also
~~~~~~~~


* :ref:`Recipe_else`

* :ref:`Recipe_expr`

[role="v24"]

.. _Recipe_else:

Using the <Else> directive
--------------------------

.. index:: <Else>

.. index:: Conditional configuration

.. index:: Optional configuration


.. _Problem_else:

Problem
~~~~~~~


Now that you have an ``<If>`` directive, you want to be able to have an
``<Else>`` clause as well.


.. _Solution_else:

Solution
~~~~~~~~


Use the ``<ElseIf>`` and ``<Else>`` directives for complete control flow:


.. code-block:: text

   <If "-R '10.1.0.0/16'">
       RedirectMatch . http://admin.intranet/
   </If>
   <ElseIf "-R '10.0.0.0/8">
       RedirectMatch . http://intranet/
   </ElseIf>
   <Else>
       RedirectMatch . http://website.com/
   </Else>


.. _Discussion_else:

Discussion
~~~~~~~~~~


In the example shown here, we imagine that while the entire ``10.``
network is available inside our corporate network, the admins are on
the ``10.1`` portion of that network. For this elite group, we wish to
redirect requests over to the website ``http://admin.intranet/``. For
everyone else inside the ``10.`` network, we want to redirect them to
``http://intranet/``. And for those outside the network, we redirect
them to the main external website at ``http://website.com/``.

By being able to express these conditions in traditional
if/elseif/else syntax, we make the configuration file much more
readable, and, thus, more maintainable, than if we were to express
these as ``RewriteCond`` and ``RewriteRule`` directives.


.. _See_Also_else:

See Also
~~~~~~~~


* :ref:`Recipe_If`

* :ref:`Recipe_expr`

[role="v24"]

.. _Recipe_image-theft-if:

Preventing image theft using <If>
---------------------------------

.. index:: <If>

.. index:: Image theft

.. index:: Prevent hotlinking


.. _Problem_image-theft-if:

Problem
~~~~~~~


You want to prevent other web sites from using your images in their
pages, using the ``<If>`` syntax, rather than ``mod_rewrite``.


.. _Solution_image-theft-if:

Solution
~~~~~~~~


While the ``mod_rewrite`` solution to this problem - explored in
:ref:`Recipe_image-theft` - is more common, using ``<If>`` for this renders
it somewhat more readable:


.. code-block:: text

   <If   "%{HTTP_REFERER} != '' \
       && %{HTTP_REFERER} !~ /example\.com/ \
       && %{REQUEST_URI}  =~ /\.(jpe?g|gif|png)$/" \
   >
         Require all denied
   </If>


.. tip::

   Use ``\`` to break up extra-long configuration lines to make 
   them more readable.


.. _Discussion_image-theft-if:

Discussion
~~~~~~~~~~


It's not that the recipe is any shorter than the one using
``mod_rewrite`` -- with the additional line breaks in
there, it's actually slightly longer. However, many people find it to
be much more readable, which is a huge advantage when you're
maintaining and updating a configuration file.

The same logic is being employed. Three conditions are being checked -
two checks on the value of the Referer header, and one on the
requested URI itself - and, if they all pass, the request is denied.

The three conditions are combined with a logical AND (the ``&&``
operator means AND), and are evaluated in sequence. That is, if one of
the conditions is false, the expression engine doesn't bother
evaluating the rest of them, and skips over the conditional.

It's also possible to swap out the ``Require`` statement contained in
the ``<If>`` block with something else, such as a ``Redirect``, if we
wanted to take a different action. Or we can put several actions in
here - for example, add a ``LogMessage`` directive to capture that the
event occurred. (See :ref:`Recipe_log_debug` for more details.)


.. _See_Also_image-theft-if:

See Also
~~~~~~~~


* :ref:`Recipe_image-theft`

* :ref:`Recipe_log_debug`


.. _Recipe_expr-errordocument:

Using an expression in an ErrorDocument
---------------------------------------

.. index:: ErrorDocument,Dynamic


.. _Problem_expr-errordocument:

Problem
~~~~~~~


You want to dynamically set the value of ``ErrorDocument`` based on an
aspect of the request itself.


.. _Solution_expr-errordocument:

Solution
~~~~~~~~


Use an expression as part of the ``ErrorDocument`` definition, and it
will be evaluated at request time:


.. code-block:: text

   ErrorDocument 403 \
     /errors/forbidden.php?referer=%{escape:%{HTTP_REFERER}}


.. _Discussion_expr-errordocument:

Discussion
~~~~~~~~~~


In addition to merely checking a true or false value, the expression
engine can also be used to set the value of a configuration directive,
evaluated at request time.

In the example here, an error document is configured, per request,
based on the value of the ``HTTP_REFERER`` - that is, the page that
linked to the resource being requested. Additionally, the ``escape``
function is invoked, to ensure that the referer value is correctly hex
encoded.


.. tip::

   Unfortunately, not every directive allows for this kind of
   request-time customization. However, over time, expect for more of
   them to do so.


.. _See_Also_expr-errordocument:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/core.html#errordocument

* :ref:`Recipe_ErrorDocument`


.. _Recipe_locationmatch-backref:

Using backreferences from a <LocationMatch>
-------------------------------------------

.. index:: Backreferences,LocationMatch

.. index:: LocationMatch,Backreferences

.. index:: Expressions,Alias

.. index:: Expressions,ScriptAlias

.. index:: Expressions,Redirect

.. index:: Redirect,Expressions

.. index:: Alias,Expressions

.. index:: ScriptAlias,Expressions

.. index:: mod_alias

.. index:: Modules,mod_alias


.. _Problem_locationmatch-backref:

Problem
~~~~~~~


You've used a ``<LocationMatch>`` directive, and you'd like to use
backreferences in directives contained in that section.


.. _Solution_locationmatch-backref:

Solution
~~~~~~~~


Use a named capture in your ``<LocationMatch>`` regex, and then use the
``MATCH`` keyword to reference it in a later directive:


.. code-block:: text

   <LocationMatch "^/department/(?<dept>[^/]+)" >
       require ldap-group cn=%{env:MATCH_DEPT},ou=department 
   </LocationMatch>


.. _Discussion_locationmatch-backref:

Discussion
~~~~~~~~~~


In httpd 2.4.8 and onwards, regular expressions used in
``<LocationMatch>`` directives can use the ``(?<name>...)`` syntax to
create a named backreference, which is stashed in the environment
variable ``MATCH_NAME``. That is, ``MATCH_``, plus the upper-case version
of whatever you named the backreference.

This env var can then be referenced by directives contained in that
``<LocationMatch>`` block, as shown in the example above. In the example
show, the capture was named ``dept``, and so the environment variable,
used in the ``require`` statement, is named ``MATCH_DEPT``.

In httpd 2.4.19 and later, if an ``Alias``, ``ScriptAlias``, or ``Redirect``
directive is contained in a ``<LocationMatch>``, it can use expression
syntax to evaluate the destination path or URL, too.


.. code-block:: text

   <LocationMatch "/error/(?<NUMBER>[0-9]+)">
       Redirect permanent \
         http://example.com/errors/%{env:MATCH_NUMBER}.html
   </LocationMatch>


Over time, we expect more and more directives to have access to this
functionality, so check the documentation frequently to see whether
it's avaliable for something you need to do.


.. _See_Also_locationmatch-backref:

See Also
~~~~~~~~


[role="v24"]

.. _Recipe_setenvifexpr:

Setting an environment variable based on an expression
------------------------------------------------------

.. index:: SetEnvIfExpr

.. index:: Expressions,SetEnvIfExpr

.. index:: Environment variables,SetEnvIfExpr

.. index:: mod_setenvif

.. index:: Modules,mod_setenvif


.. _Problem_setenvifexpr:

Problem
~~~~~~~


You want to set an environment variable based on the value of an
evaluated expression.


.. _Solution_setenvifexpr:

Solution
~~~~~~~~


Use the (new in 2.4) ``SetEnfIfExpr`` directive:


.. code-block:: text

   SetEnvIfExpr "-R '10.0.0.0/8' ||    \
                 -R '172.16.0.0/12' || \
                 -R '192.168.0.0/16'"     PrivateNetwork


.. _Discussion_setenvifexpr:

Discussion
~~~~~~~~~~


The ``SetEnvIfExpr`` directive was added in the 2.4 release to make it
easier to set environment variables based on expressions. In the
example shown, we're able to set a single environment variable,
``PrivateNetwork``, based on whether the client IP address falls into
one of the private networks defined by RFC1918.


.. _See_Also_setenvifexpr:

See Also
~~~~~~~~


* https://tools.ietf.org/html/rfc1918

* http://httpd.apache.org/docs/mod/mod_setenvif.html#setenvifexpr

* :ref:`Recipe_If`

[role="v24"]

.. _Recipe_setting-headers-with-expr:

Setting HTTP headers based on expressions
-----------------------------------------

.. index:: Headers,Expressions

.. index:: Expressions,Setting headers

.. index:: mod_headers

.. index:: Modules,mod_headers

.. index:: Header

.. index:: RequestHeader


.. _Problem_setting-headers-with-expr:

Problem
~~~~~~~


You want to set an HTTP header based on the value of an evaluated
expression.


.. _Solution_setting-headers-with-expr:

Solution
~~~~~~~~


Use the ``expr=`` syntax of the ``Header`` or ``RequestHeader`` directives
to set a response or request header (respectively) using an expression:


.. code-block:: text

   Header append Cache-Control s-maxage=600 \
                 "expr=%{REQUEST_STATUS} == 200"


.. _Discussion_setting-headers-with-expr:

Discussion
~~~~~~~~~~


Adding the optional ``expr=`` argument to the end of a ``Header`` or
``RequestHeader`` directive causes that expression to be evaluated, and
the header set conditionally based on the value of the expression.


.. warning::

   Take careful note of how the quotes are placed around the ``expr=``
   argument in this example. Incorrectly quoting the argument will lead
   to httpd failing to start up, with a 'Header has too many arguments'
   error message.


.. _See_Also_setting-headers-with-expr:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_headers.html#header

* http://httpd.apache.org/docs/mod/mod_headers.html#requestheader


[role="v24"]

.. _Recipe_LogMessage-with-expr:

Setting custom log messages with the expression engine
------------------------------------------------------

.. index:: LogMessage

.. index:: Expressions,Custom log message


.. _Problem_LogMessage-with-expr:

Problem
~~~~~~~


You want to set a custom log message, using a value derived from an
expression.


.. _Solution_LogMessage-with-expr:

Solution
~~~~~~~~


Using expressions to set custom log messages is discussed in
:ref:`Recipe_log_debug`


.. _See_Also_LogMessage-with-expr:

See Also
~~~~~~~~


* :ref:`Recipe_log_debug`

* http://httpd.apache.org/docs/mod/mod_log_debug.html


.. _Recipe_expr-auth:

Authorization using expressions
-------------------------------

.. index:: Expressions,Authorization

.. index:: Authorization,Expressions

.. index:: AAA,Expressions


.. _Problem_expr-auth:

Problem
~~~~~~~


You wish to authorize access to a resource using the value of an
expression.


.. _Solution_expr-auth:

Solution
~~~~~~~~


This topic is discussed at length in :ref:`Chapter_AAA`, *Authentication,
Authorization, and Access Control*.


.. _See_Also_expr-auth:

See Also
~~~~~~~~


* :ref:`Chapter_AAA`, **Authentication, Authorization, and Access Control**

[role="v24"]

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
   use ``Define`` in a ``<VirtualHost>``, we recommend that you ``UnDefine`` it
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

   In earlier versions of Apache httpd, this technique was used to start
   the server with, or without, SSL enabled. Thus, you might find older
   howto articles that tell you to start ``httpd`` with the ``-DSSL`` flag,
   in order to enable SSL. This is no longer the case by default, but you
   could use the above technique to set things up that way, if you
   wanted.


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

In the above recipe example, once we have decided on a standardized
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
invocation of the macro, but we have avoided repeating any of the
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


Summary
-------


There's a lot more you can do with per-request configuration that's
not covered in this chapter. That's because it's covered in almost
every other chapter in this book. Because of the enormous power of
this feature, it pervades every part of configuring your server. So,
you'll see examples of it throughout the book.

Do be aware that the more you use expressions in your configuration,
the slower every request is going to be, as these expressions have to
evaluated with every request. So, as with any shiny new feature, use
it sparingly, and only where it is actually necessary.

