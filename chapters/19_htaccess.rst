
.. _Chapter_htaccess:

===============
.htaccess Files
===============

.. epigraph::

   Breaking the law, breaking the law.

   -- Judas Priest, *Breaking the Law*


.. index:: .htaccess files

.. index:: htaccess files

.. index:: Per-directory configuration

.. index:: htaccess

.. index:: .htaccess


While I strongly recommend that all of your configuration changes are
made in the server configuration files (typically located in
``/etc/httpd/conf``) this is sometimes not possible. If for some reason,
you do not have permission to edit those configuration files, or for
some other reason don't want to, httpd provides a mechanism to
override the configuration on a per-directory basis.

By placing a file named ``.htaccess`` in a content directory, you can
modify the server's configuration for that specific directory, and for
all subdirectories thereof.

In the server configuration, you define whether you want to permit
this behavior, and, if you do, what you want to allow to be
overridden. Different sysadmins will feel differently about what they
want to allow unprivileged users on their system to override. You'll
need to consider this for yourself, and configure your server
accordingly.


.. _Recipe_AllowOverride-all:

Enabling .htaccess files
------------------------

.. index:: .htaccess,Enabling

.. index:: htaccess,Enabling

.. index:: AllowOverride

.. index:: AllowOverride,All


.. _Problem_AllowOverride-all:

Problem
~~~~~~~


You want to enable the use of ``.htaccess`` files on your server.


.. _Solution_AllowOverride-all:

Solution
~~~~~~~~


Find the ``<Directory>`` block referring to your ``DocumentRoot``
directory, and add the following to it:


.. code-block:: text

   AllowOverride All


.. _Discussion_AllowOverride-all:

Discussion
~~~~~~~~~~


The ``AllowOverride`` directive determines whether ``.htaccess`` files
will be permitted, or ignored. For more fine-grained control, see
:ref:`Recipe_AllowOverride-categories` and :ref:`Recipe_AllowOverrideList`.

Because ``AllowOverride`` configures per-directory behavior, it can
only be used in Directory context. Context, also sometimes called
scope, is discussed in :ref:`Recipe_Directive_goes_where`. In this case,
it means that the ``AllowOverride`` directive must be placed inside a
``<Directory>`` block where you want it to take effect. This block will
probably be the one that configures your document directory, such as
``<Directory /var/www/htdocs>``.


.. warning::

   Do not place ``AllowOverride`` in the directory block that looks like
   ``<Directory />`` as this tells httpd that you want to enable
   ``.htaccess`` files for your entire file system, including directories
   outside of the website document directories.


.. _See_Also_AllowOverride-all:

See Also
~~~~~~~~


* :ref:`Recipe_AllowOverride-categories`

* :ref:`Recipe_AllowOverrideList`

* http://httpd.apache.org/docs/mod/core.html#allowoverride

* http://httpd.apache.org/docs/howto/htaccess.html

* :ref:`Recipe_Directive_goes_where`


.. _Recipe_AllowOverride-categories:

Allowing specific types of directives in .htaccess files
--------------------------------------------------------

.. index:: AllowOverride

.. index:: .htaccess,What's permitted

.. index:: htaccess,What's permitted

.. index:: AllowOverride,AuthConfig

.. index:: AllowOverride,FileInfo

.. index:: AllowOverride,Indexes

.. index:: AllowOverride,Limit

.. index:: AllowOverride,Nonfatal

.. index:: AllowOverride,Options


.. _Problem_AllowOverride-categories:

Problem
~~~~~~~


Rather than just enabling ``.htaccess`` files, you want to exert a
little control over what can and cannot be placed in .htaccess files.


.. _Solution_AllowOverride-categories:

Solution
~~~~~~~~


Rather than using ``AllowOverride All``, specify, by category, what
kinds of directives you wish to permit in ``.htaccess`` files:


.. code-block:: text

   AllowOverride AuthConfig Indexes


.. _Discussion_AllowOverride-categories:

Discussion
~~~~~~~~~~


Each configuration directive that is part of the Apache httpd
configuration is placed in an override category, and this is indicated
in the documentation for that directive.

For example, if you look at the documentation for the ``Deny``
directive, you'll see in the documentation:


.. code-block:: text

   Override: Limit


This means that the directive is permitted in ``.htaccess`` files if
``AllowOverride`` is set to ``Limit``. Setting ``AllowOverride`` to ``All``,
as discussed in :ref:`Recipe_AllowOverride-all`, enables all of the
various categories of overrides.

Some directives may not be places in ``.htaccess`` files no matter what
``AllowOverride`` is set to, for a variety of reasons, usually
pertaining to security considerations.

``AllowOverride`` may be set to any of the following, or any combination
of them:


+------------+-------------------------------------------------------------+
| Override   | Meaning                                                     |
+------------+-------------------------------------------------------------+
| AuthConfig | Allow directives that deal with authentication and          |
+------------+-------------------------------------------------------------+
| FileInfo   |                                                             |
+------------+-------------------------------------------------------------+
| Indexes    | Permit the use of directives controlling directory indexing |
+------------+-------------------------------------------------------------+
| Limit      | Permit the use of directives controlling host access - that |
+------------+-------------------------------------------------------------+
| Nonfatal   | Defines how to handle errors in ``.htaccess`` files. |
+------------+-------------------------------------------------------------+
| Options    | Permit use of the ``Options`` directive. See                |
+------------+-------------------------------------------------------------+


You can permit more than one category by listing those categories that
you wish to permit:


.. code-block:: text

   AllowOverride Limit Options Indexes


And, to enable all of the categories:


.. code-block:: text

   AllowOverride All


And, to reiterate, some directives are never permitted in ``.htaccess``
files, no matter what you set ``AllowOverride`` to.


.. _See_Also_AllowOverride-categories:

See Also
~~~~~~~~


* :ref:`Recipe_AllowOverride-all`

* :ref:`Recipe_AllowOverrideList`

* :ref:`Recipe_AllowOverride-options`

* :ref:`Recipe_AllowOverride-nonfatal`

* http://httpd.apache.org/docs/mod/core.html#allowoverride


.. _Recipe_AllowOverrideList:

More fine-grained AllowOverride control
---------------------------------------

.. index:: AllowOverrideList

.. index:: AllowOverride,More fine-grained control


.. _Problem_AllowOverrideList:

Problem
~~~~~~~


You want more fine-grained control over what is permitted in
``.htaccess`` files than is granted by the usual use of the
``AllowOverride`` directive.


.. _Solution_AllowOverrideList:

Solution
~~~~~~~~


Use the ``AllowOverrideList`` directive to specify particular directives
that you wish to permit in ``.htaccess`` files.


.. code-block:: text

   AllowOverride None
   AllowOverrideList Redirect RedirectMatch


.. _Discussion_AllowOverrideList:

Discussion
~~~~~~~~~~


While the categories of directives permitted by ``AllowOverride`` (See
:ref:`Recipe_AllowOverride-options`) are sufficient in most cases,
sometimes you wish to permit only a subset of those directives placed
in the predefined categories.

The ``AllowOverrideList`` allows you to specify exactly what directives
you want to permit in ``.htaccess`` files. It is usually used in
conjunction with an ``AllowOverride`` directive which sets the ground
rules, so to speak, with ``AllowOverrideList`` setting the
exceptions.

For example, if you wanted to permit auth directives, and a few
``mod_rewrite`` directives, you might do the following:


.. code-block:: text

   AllowOverride AuthConfig
   AllowOverrideList RewriteRule RewriteCond RewriteBase


.. _See_Also_AllowOverrideList:

See Also
~~~~~~~~


* :ref:`Recipe_AllowOverride-categories`

* http://httpd.apache.org/docs/mod/core.html#allowoverridelist


.. _Recipe_disabling-htaccess:

Disabling .htaccess files.
--------------------------

.. index:: .htaccess,Disabling

.. index:: htaccess,Disabling

.. index:: AllowOverride,None


.. _Problem_disabling-htaccess:

Problem
~~~~~~~


You do not wish to permit the use of ``.htaccess`` files at all.


.. _Solution_disabling-htaccess:

Solution
~~~~~~~~


Set ``AllowOverride`` to ``None`` to disable the use of ``.htaccess`` files.


.. code-block:: text

   AllowOverride none


.. _Discussion_disabling-htaccess:

Discussion
~~~~~~~~~~


As an Apache httpd administrator, you want to disable the use of
``.htaccess`` files wherever and whenever possible, primarily because
they can have a significant impact on performance, but also because of
the potential security concerns. Furthermore, having your
configuration in one place, rather than scattered across the file
system, leads to far less confusion and hunting when it comes time to
troubleshoot problems.


.. note::

   As hard drive (and SSD) access rates become faster and faster, the
   performance impact of using ``.htaccess`` files becomes less and less.
   Anecdotally, it has been reported that there is almost no perceptible
   performance impact of using ``.htaccess`` files on most modern hardware.
   Despite this, I still recommend avoiding ``.htaccess`` files unless
   they are absolutely necessary, due to the maintenance benefits of
   having all of your configuration in one place.


Note also that when ``AllowOverride`` is enabled, httpd will check for
the presence of a ``.htaccess`` file in each traversed directory, for
every request to the server, resulting in additional file system
access on every HTTP request, regardless of whether you even have any
``.htaccess`` files in place. However, when ``AllowOverride`` is set to
``None``, these files are not even looked for. It is these additional
filesystem checks that can result in performance degradation from
using ``.htaccess`` files.

See :ref:`Recipe_htaccess-performance` for further discussion of this
performance impact.


.. _See_Also_disabling-htaccess:

See Also
~~~~~~~~


* :ref:`Recipe_htaccess-performance`

* http://httpd.apache.org/docs/mod/core.html#allowoverride


.. _Recipe_htaccess-testing:

Testing .htaccess files
-----------------------

.. index:: htaccess,testing

.. index:: .htaccess,testing


.. _Problem_htaccess-testing:

Problem
~~~~~~~


You think that your ``.htaccess`` files are being ignored, but you're
not certain.


.. _Solution_htaccess-testing:

Solution
~~~~~~~~


Test whether your ``.htaccess`` files are being loaded by putting
garbage in them, and seeing if this causes a server error. For
example, you might put the following directive in a ``.htaccess`` file.


.. code-block:: text

   BadConfigurationDirectiveHere


.. _Discussion_htaccess-testing:

Discussion
~~~~~~~~~~


When you just can't get your ``.htaccess`` files working, you might need
a sanity check to ensure that the files are in fact being loaded and
considered in the configuration. The best way to do this is to put
something in the ``.htaccess`` file that generates an error.

Under normal circumstances, putting garbage in a ``.htaccess`` file
will cause a ``Server Errror`` messaage when a browser loads content
from that directory. This comfirms that the server is indeed loading
your ``.htaccess`` file and finding an error in it.

If it does not result in an error, then you will have confirmed that
httpd is not loading your ``.htaccess`` file, which probably means that
``AllowOverride None`` is in effect. However, it may also indicate that
``AllowOverride NonFatal`` is set to either ``Unknown`` or ``All``.


.. _See_Also_htaccess-testing:

See Also
~~~~~~~~


* :ref:`Recipe_AllowOverride-nonfatal`

* :ref:`Recipe_disabling-htaccess`


.. _Recipe_AllowOverride-options:

Configuring what Options are permitted in .htaccess files
---------------------------------------------------------

.. index:: AllowOverride,Options

.. index:: Options


.. _Problem_AllowOverride-options:

Problem
~~~~~~~


When ``AllowOverride Options`` is too permissive, you want to have more
control over which options are permitted in ``.htaccess`` files.


.. _Solution_AllowOverride-options:

Solution
~~~~~~~~


Specify a comma-separated list of the ``Options`` that you want to
permit in ``.htaccess`` files:


.. code-block:: text

   AllowOverride Options=Indexes,MultiViews


.. _Discussion_AllowOverride-options:

Discussion
~~~~~~~~~~


Simply allowing ``AllowOverride Options`` permits ``.htaccess`` file users
to enable a wide variety of different behaviors, from CGI execution to
directory indexing to following symbolic links. You may want to permit
some of these, but not others, for reasons of security.

The ``Options`` argument to ``AllowOverride``
gives you the ability to exert this kind of fine-grained control over
what ``AllowOverride Options`` actually means, by specifying exactly
what ``Options`` you want to permit.

See :ref:`Recipe_Options` for a discussion of the various options and
their meanings.

Thus, if you put the following configuration in your main server
configuration file:


.. code-block:: text

   AllowOverride Options=Indexes,MultiViews


then ``.htaccess`` files could contain ``Options Indexes`` or ``Options
Multiviews`` directives, while other ``Options` settings would not be
permitted.


.. _See_Also_AllowOverride-options:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/core.html#options

* :ref:`Recipe_Options`


.. _Recipe_AllowOverride-nonfatal:

Handling errors in .htaccess files
----------------------------------

.. index:: AllowOverride,Nonfatal

.. index:: htaccess,Handling errors

.. index:: .htaccess,Handling errors

.. index:: Errors in .htaccess files


.. _Problem_AllowOverride-nonfatal:

Problem
~~~~~~~


You want to configure how errors in .htaccess files are handled,
perhaps preventing them from resulting in server errors.


.. _Solution_AllowOverride-nonfatal:


Solution
~~~~~~~~


Use the ``Nonfatal`` argument to ``AllowOverride`` to specify handling of
error conditions:


.. code-block:: text

   AllowOverride Nonfatal=All


.. _Discussion_AllowOverride-nonfatal:

Discussion
~~~~~~~~~~


The ``Nonfatal`` keyword allows the use of unrecognized or disallowed
configuration directives in ``.htaccess`` files, without resulting in an
Internal Server Error. The error will, however, still be logged.

Syntax errors in a valid dirctive will still cause an
Internal Server Error.

The ``Nonfatal`` keyword can take one of three possible arguments:


+-------------------+----------------------------------------------------+
| Nonfatal=Override | Treats directives forbidden by AllowOverride as    |
+-------------------+----------------------------------------------------+
| Nonfatal=Unknown  | Treats unknown directives as nonfatal. This covers |
+-------------------+----------------------------------------------------+
| Nonfatal=All      | Treats both the above as nonfatal. |
+-------------------+----------------------------------------------------+


.. warning::

   Hiding error conditions makes troubleshooting very difficult. I do
   not recommend the use of this configuration option. It is frequently
   the case that people who use ``.htaccess`` files don't have unfettered
   access to the error logs, and hiding their error conditions will make
   it very frustrating for them to try to figure out why things aren't
   working as expected.


.. _See_Also_AllowOverride-nonfatal:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/core.html#allowoverride


.. _Recipe_htaccess-performance:

Improving htaccess performance
------------------------------

.. index:: .htaccess,Performance

.. index:: htaccess,Performance


.. _Problem_htaccess-performance:

Problem
~~~~~~~


You've heard that ``.htaccess`` files cause a performance degradation on
your httpd, and want to reduce that impact.


.. _Solution_htaccess-performance:

Solution
~~~~~~~~


This problem is discussed in detail in
:ref:`Recipe_Performance_impact_of_htaccess_files`.

See Also
~~~~~~~~


* :ref:`Chapter_Performance_and_testing`, **Performance and Testing**


.. _Recipe_Renaming-htaccess:

Renaming .htaccess Files
------------------------

.. index:: .htaccess files,Renaming

.. index:: htaccess files,Renaming

.. index:: Renaming .htaccess files

.. index:: htaccess,Windows

.. index:: .htaccess,Windows

.. index:: htaccess,Microsoft Windows

.. index:: .htaccess,Microsoft Windows

.. index:: Windows,.htaccess files

.. index:: Microsoft Windows,.htaccess files


.. _Problem_Renaming-htaccess:

Problem
~~~~~~~


You want to change the default name of
**per**-directory configuration files on a Windows
system, because filenames beginning with a dot can cause
problems on Microsoft Windows servers.


.. _Solution_Renaming-htaccess:

Solution
~~~~~~~~


Use the **AccessFileName** directive to specify the new name:


.. code-block:: text

   AccessFileName htaccess.conf


.. _Discussion_Renaming-htaccess:

Discussion
~~~~~~~~~~


The default name for the per-directory configuration file is
``.htaccess``, as mentioned previously. However, there are cases where
you may want to rename this to something else.

In particular, naming a file with a leading ``.`` in Microsoft Windows
can be unintuitive, leading to support problems.


.. note::

   To name a file in Microsoft Windows with a leading ``.`` enclose the
   filename in quotes when you save it.


To avoid this difficulty, you can rename the override file to
something else, as show in the recipe above.

If you use the **AccessFileName**
directive, be sure to make any additional appropriate changes to your
configuration such as the **&lt;FilesMatch "^\.ht"&gt;** container that keeps the files from being
fetchable over the Web:


.. code-block:: text

   <FilesMatch "^ht\.">
       Require all denied
   </FilesMatch>


.. warning::

   Renaming the per-directory configuration file is likely to result in
   operator confusion, when files named ``.htaccess`` have no effect, as
   well as being unable to find the file currently in use.


You can set ``AccessFileName`` to multiple values:


.. code-block:: text

   AccessFileName .htaccess htaccess.conf


However, this can also introduce confusion and complexity.


.. _See_Also_Renaming-htaccess:

See Also
~~~~~~~~


* :ref:`Recipe_Performance_impact_of_htaccess_files`

* http://httpd.apache.org/docs/howto/htaccess.html

* :ref:`Recipe_Hiding-directory-items`


.. _Recipe_rewrite-htaccess-seeother:

Troubleshooting Rewrite directives in .htaccess files
-----------------------------------------------------


.. _Problem_rewrite-htaccess-seeother:

Problem
~~~~~~~


Why doesn't my ``RewriteRule`` work in an .htaccess file?


.. _Solution_rewrite-htaccess-seeother:

Solution
~~~~~~~~


This is discussed in :ref:`Chapter_mod_rewrite`, *URL Rewriting with
mod_rewrite* - specifically, in
:ref:`Recipe_rewrite-htaccess`.

Summary
-------


``.htaccess`` files are a critical part of many httpd
installations where more than one individual has responsibility for
content. In this chapter I show how to get the most out of
``.htaccess`` files, while also knowing when they are not the best
solution.

