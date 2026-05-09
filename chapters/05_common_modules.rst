.. raw:: latex

   \part{Core Configuration}

.. _Chapter_Common_modules:

=====================
Adding common modules
=====================

.. epigraph::

   | You can't always get what you want,
   | but if you try sometimes, you just might find
   | you get what you need.

   -- The Rolling Stones, *You Can't Always Get What You Want*


.. index:: Common modules

.. index:: Modules,common

.. index:: Adding common modules


A critical detail of the Apache HTTP Server is that it is modular.
There's a small core, and everything beyond the absolute basics is
implemented in modules.

The module API makes it fairly easy for anyone to create their own
modules to perform whatever task, large or small. As a result, a large
number of third-party modules have sprung up. By "third-party", I
mean modules that are maintained and distributed separately from the
main web server project. This is due to a variety of factors. Not
everything is of interest to enough people to necessitate being part
of the main project. Some modules are licensed incompatibly to the
Apache license. Some modules are for use only within a particular site
or company.

When a module gains sufficient popular following, sometimes the httpd
project will go encourage a module author to bring their module to the
main project. Or, alternatively, the author may approach the httpd
project and offer their module as a code donation, so that a larger
community will be working on it. Thus, modules like mod_ssl, mod_lua,
mod_macro, and others, have over the years become part of the main
server project.

Other modules, such as mod_perl, mod_security, or PHP, have a
sufficient community around them that they exist as vibrant
independent projects.

In this chapter, I show how to install and configure several
third-party modules, ranging from the trivial (mod_pony) to the more
useful. I'll show how to install them via packages, and from source.

This chapter does not cover writing your own modules. I feel that
this is beyond the scope of this book. Instead I recommend Nick Kew's
book, The Apache httpd Modules book.
http://www.amazon.com/The-Apache-Modules-Book-Application/dp/0132409674

I also recommend the online developer resource,
http://httpd.apache.org/dev/ , and the API guide,
http://ci.apache.org/projects/httpd/trunk/doxygen/

.. refcosplay



.. _Recipe_Finding_Modules:

Finding modules
---------------

.. index:: Modules,finding

.. index:: Finding modules

.. index:: Finding modules on GitHub


.. _Problem_Finding_Modules:

Problem
~~~~~~~


I'd like to see what third-party modules are available.


.. _Solution_Finding_Modules:

Solution
~~~~~~~~


There is no single comprehensive registry of third-party httpd modules.
The best approach is to search GitHub:

* https://github.com/search?q=apache+httpd+module&type=repositories
* Look for repositories tagged with the ``apache-httpd-module`` or
  ``httpd-module`` topics.

Your operating system's package manager is also a good starting point.
On Debian/Ubuntu, try ``apt search libapache2-mod-``. On
Fedora/RHEL/AlmaLinux, try ``dnf search mod_``.


.. _Discussion_Finding_Modules:

Discussion
~~~~~~~~~~


The Apache httpd project once maintained a module registry at
modules.apache.org, where third-party authors could list their modules
and users could post reviews. That site has been retired, and there is
no direct replacement.

In practice, GitHub has become the de facto home for third-party httpd
modules. Most active module projects are hosted there, and GitHub's
search and topic system makes them reasonably easy to find. When
searching, try terms like "apache httpd module" followed by the
functionality you're looking for — for example, "apache httpd module
rate limiting" or "apache httpd module markdown".

For Perl-based modules (especially those related to mod_perl), CPAN
(https://metacpan.org/) remains a useful source.

Your Linux distribution's package manager is often the easiest path,
since packaged modules will be compiled against the right version of
httpd and can be installed with a single command. The downside is that
distribution repositories tend to carry only the most popular modules,
and the versions may lag behind upstream.


.. _See_Also_Finding_Modules:

See Also
~~~~~~~~


* https://github.com/search?q=apache+httpd+module&type=repositories

* https://httpd.apache.org/docs/current/mod/ — the list of modules
  bundled with httpd itself


.. _Recipe_apxs:

Installing a module with apxs
-----------------------------

.. index:: apxs

.. index:: Installing modules with apxs

.. index:: Modules,installing with apxs


.. _Problem_apxs:

Problem
~~~~~~~


You have downloaded a third-party module that isn't listed in
this chapter, and you want to install it.


.. _Solution_apxs:

Solution
~~~~~~~~


Move to the directory where the module's source file was
unpacked, and then:


.. code-block:: text

   apxs -cia module.c


.. _Discussion_apxs:

Discussion
~~~~~~~~~~


Installing modules has
been pretty standard for a long time, and for most modules, the proces should be
fairly easy.

``apxs`` is a tool that comes with the web server which facilitates
building, installing and enabling a module.

If you installed httpd via a package, you will likely have to install
a second package to get the developer tools, such as ``apxs``.

On Debian (or Ubuntu, and related distributions), install the
``apache2-dev`` package:


.. code-block:: text

   apt-get install apache2-dev


On RPM-based distributions (Fedora, RHEL, AlmaLinux, Rocky Linux), install the
``httpd-devel`` package:


.. code-block:: text

   dnf install httpd-devel


The ``-cia`` option to ``apxs`` is a shortcut for the options ``-c -i -a``,
and means compile, install, and activate, respectively.

Compile builds the C source code into a ``.so`` file. Install copies
that file into the location where your server has module files.
Activate modifies your server configuration file to add ``LoadModule``
directive so that the module will be loaded on server restart.

This requires that your server is build with ``mod_so`` enabled, to
permit dynamic module loading.


.. _See_Also_apxs:

See Also
~~~~~~~~


* The **apxs** manpage, typically **ServerRoot/man/man8/apxs.8** or type
  ``man apxs`` at the command line.

* apxs documentation, at
  http://httpd.apache.org/docs/programs/apxs.html


.. _Recipe_Installing_PHP:

Running PHP programs
--------------------

.. index:: PHP

.. index:: PHP,Installing

.. index:: Running PHP programs


.. _Problem_Installing_PHP:

Problem
~~~~~~~


You want to use the PHP language on your httpd.


.. _Solution_Installing_PHP:

Solution
~~~~~~~~


There are a few different ways to install PHP on your httpd,
depending on how you installed Apache httpd itself, and your needs and
preferences.

Look in :ref:`Chapter_Dynamic_content`, **Dynamic Content**, for discussion of the various ways
to install and enable PHP on your httpd.


.. _Discussion_Installing_PHP:

Discussion
~~~~~~~~~~


I've devoted an entire chapter to the various ways of producing
dynamic content on Apache httpd, and PHP is a very important topic in
that discussion.


.. _See_Also_Installing_PHP:

See Also
~~~~~~~~


* :ref:`Recipe_enabling_mod_php`

* :ref:`Recipe_php-fpm`

.. refcosplay



.. _Recipe_modules_apache_org:

Finding third-party modules on GitHub
-------------------------------------

.. index:: Third-party modules on GitHub

.. index:: Modules,third party

.. index:: Third party modules


.. _Problem_modules_apache_org:

Problem
~~~~~~~


You're looking for a listing of Apache httpd modules for various
purposes, and you want to know where to find them now that the
old modules.apache.org registry has been retired.


.. _Solution_modules_apache_org:

Solution
~~~~~~~~


Search GitHub for the functionality you need:

* https://github.com/search?q=apache+httpd+module&type=repositories

Or browse by topic: https://github.com/topics/apache-httpd-module



.. _Discussion_modules_apache_org:

Discussion
~~~~~~~~~~


For many years, the Apache httpd project maintained a module registry
at modules.apache.org, where third-party authors could list their
modules and users could browse by category or post reviews. That site
has been retired and is no longer available.

Today, most third-party httpd modules are hosted on GitHub. If you're
looking for a module that does something specific, a GitHub search for
"apache httpd module" plus your use case (e.g., "apache httpd module
geoip") is usually the fastest way to find it.

Some things to look for when evaluating a third-party module on
GitHub:

* **Recent commits** — is the module actively maintained?
* **Compatibility** — does it mention support for httpd 2.4?
* **License** — is it Apache-2.0 or compatible?
* **Issues and pull requests** — is anyone using it and reporting
  problems?


.. _See_Also_modules_apache_org:

See Also
~~~~~~~~


.. _Recipe_mod_pony:

Installing and configuring mod_pony
-----------------------------------

.. index:: mod_pony

.. index:: Modules,mod_pony

.. index:: Pony

.. index:: Example module

.. index:: Modules,example

.. index:: Installing and configuring mod_pony


.. _Problem_mod_pony:

Problem
~~~~~~~


You've found mod_pony on GitHub and you want to install it
and try it out.


.. _Solution_mod_pony:

Solution
~~~~~~~~


Download mod_pony.c from the module repository at
https://github.com/rbowen/mod_pony

Install and enable it using apxs, as described above:


.. code-block:: text

   apxs -cia mod_pony.c


Configure the pony handler as described in the documentation:


.. code-block:: text

   <Location /pony>
     SetHandler pony
   </Location>


To verify that it works, load the address
http://your.server/pony in your browser to invoke the
``pony`` handler.


.. _Discussion_mod_pony:

Discussion
~~~~~~~~~~


mod_pony is a joke module that does nothing more than randomly display
either an ascii-art pony, or the words 'not yours'.


.. figure:: ../images/pony.png


.. figure:: ../images/no_pony.png


It is also a useful example of how to write a content module, so it's
a good place to start if you're interested in writing your own httpd
module.

It is used as an example in this chapter simply because it provides
the simplest possible example of how to install and configure a
third-party module on your Apache httpd server.


.. _See_Also_mod_pony:

See Also
~~~~~~~~


* mod_example and mod_example_hooks

* https://github.com/rbowen/mod_pony


.. _Recipe_mod_security:

mod_security
------------

.. index:: mod_security

.. index:: Modules,mod_security

.. index:: Security,mod_security


.. _Problem_mod_security:

Problem
~~~~~~~


You'd like to use mod_security to block unsavory requests to your web
server.


.. _Solution_mod_security:

Solution
~~~~~~~~


Obtain and install mod_security from http://modsecurity.org/
and install it using apxs, or install it via your operating system's
package manager.

To install via packages on Ubuntu or Debian:


.. code-block:: text

   $ sudo apt-get install libapache2-mod-security
   $ sudo a2enmod mod-security
   $ sudo /etc/init.d/apache2 force-reload


To install via packages on Fedora or RHEL:


.. code-block:: text

   $ sudo dnf install mod_security
   $ sudo /etc/init.d/httpd restart


To install on Microsoft Windows, obtain the installer from
http://modsecurity.org/download.html

To install using the source code, download the source tarball from
http://www.modsecurity.org/download.html and unpack it. Then:


.. code-block:: text

   $ $cd ModSecurity
   $ ./autogen.sh
   $ ./configure --with-apxs=/path/to/httpd/bin/apxs
   $ make
   $ sudo make install
   $ /usr/local/modsecurity/lib/mod_security2.so /usr/local/apache/modules/


Load ``mod_security`` into your server by adding the following line to
your httpd configuration file:


.. code-block:: text

   LoadModule security2_module modules/mod_security2.so


.. _Discussion_mod_security:

Discussion
~~~~~~~~~~


Building ``mod_security`` from source is slightly more complicated than
building simpler modules, like, say, ``mod_pony``, as there are various
library dependencies that ``mod_security`` needs to resolve in the build
process. In particular, you need to ensure that you have the following
libraries installed:

* libapr
* libapr-util
* libpcre
* libxml2
* liblua
* libcurl

These will almost certainly be installed if you have Apache httpd
installed, so there's not usually anything to worry about here.

.. index:: mod_uniqueid

.. index:: Modules,mod_uniqueid

You will also need to have ``mod_uniqueid`` installed to use many of the
features of ``mod_security``.

In the recipe above, you'll need to provide your correct file paths
for ``apxs`` and your modules directory in the appropriate places. That
is:


.. code-block:: text

   ./configure --with-apxs=/path/to/httpd/bin/apxs


In that command, replace ``/path/to/httpd/bin/apxs`` with the actual
path to your ``apxs`` utility, which you can usually obtain by typing
``which apxs``.

And in the last line of the recipe:


.. code-block:: text

   $ /usr/local/modsecurity/lib/mod_security2.so /usr/local/apache/modules/


Ensure that this is actually the location where your server stores
modules files, or replace it with the correct path.

Finally, there is an excellent book available by the creator of
``mod_security`` - mod_security Handbook, by Ivan Ristić, from Feisty
Duck publishing. You can find more information about this book at
https://www.feistyduck.com/books/modsecurity-handbook/


.. _See_Also_mod_security:

See Also
~~~~~~~~


* Ivan Ristić's book -
  https://www.feistyduck.com/books/modsecurity-handbook/

* The mod_security website, at http://modsecurity.org/

* The mod_security reference manual, at
  https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual

.. refcosplay



.. _Recipe_mod_security_rules:

mod_security rules
------------------

.. index:: mod_security,rules

.. index:: Securing your server with mod_security


.. _Problem_mod_security_rules:

Problem
~~~~~~~


Now that you have ``mod_security`` installed, how do I use it?


.. _Solution_mod_security_rules:

Solution
~~~~~~~~


There are a number of recipes about using ``mod_security`` to protect
your web server in :ref:`Chapter_Security`, **Security**.


.. _Discussion_mod_security_rules:

Discussion
~~~~~~~~~~


This chapter is primarily devoted to installing and enabling
third-party modules. Because ``mod_security`` is a web application
firewall, primarily focused on web application security, I've put the
relevant recipes in the Security chapter.


.. _See_Also_mod_security_rules:

See Also
~~~~~~~~


* :ref:`Chapter_Security`, **Security**

.. refcosplay



.. _Recipe_module_broken:

Why won't this module work?
---------------------------

.. index:: Why won't this module work

.. index:: Troublshooting,third-party modules


.. _Problem_module_broken:

Problem
~~~~~~~


You are trying to install a third-party module, but httpd
refuses to recognize it.


.. _Solution_module_broken:

Solution
~~~~~~~~


Consult the sources for the module, or its documentation, or ask
the author, in order to determine which version of httpd the package
supports.


.. _Discussion_module_broken:

Discussion
~~~~~~~~~~


As significant changes are made to httpd,
sometimes compatibility suffers as the API is changed. Although
efforts are made to keep this sort of thing to a minimum, sometimes it
is unavoidable.

To keep an incompatible module from being loaded and crashing
the web server when used, both modules and the server have a built-in
'magic' number that is recorded when they're built, and that relates
to the version of the API. When the server tries to load a module DSO,
it compares the module's magic number with the server's own, and if
they aren't compatible, the server refuses to load it.

The development team tries to keep the magic number
compatibility within major version numbers, but not across them. That
is, a module built for httpd 2.4 **should** work
with almost any 2.4 version of the server built after the module was,
but it won't work across major versions.



.. _See_Also_module_broken:

See Also
~~~~~~~~


* :ref:`Recipe_Finding_Modules`


.. _Recipe_Enabling_modules_debian:

Enabling modules on Ubuntu and Debian
-------------------------------------

.. index:: Ubuntu,Enabling and disabling modules

.. index:: Enabling and disabling modules on Debian and Ubuntu

.. index:: Debian,Enabling and disabling modules


.. _Problem_Enabling_modules_debian:

Problem
~~~~~~~


Debian, and related distributions such as Ubuntu, provide their own
tools for enabling and disabling modules.


.. _Solution_Enabling_modules_debian:

Solution
~~~~~~~~


Use the **a2enmod** and **a2dismod** tools to enable, and disable,
available modules, respectively.


.. code-block:: text

   a2enmod rewrite
   a2dismod mime_magic


.. _Discussion_Enabling_modules_debian:

Discussion
~~~~~~~~~~


Debian, and related distributions like Ubuntu, use a directory
structure built around its site- and server-management tools. In the
case of modules, there are two directories, and two command line
tools.

In the directory **/etc/apache2/mods-available/**, you will find
configuration files for the various
modules which have been installed with the server, and which may or
may not be enabled.

In the directory **/etc/apache2/mods-enabled/**, you will find symbolic
links (symlinks) to files in that other directory.

Two command line tools are provided to manage these symlinks.
**a2enmod** (Apache 2 Enable Module) creates the symlink, and **a2dismod**
(Apache 2 Disable Module) removes that symlink.

In this way, you can easily enable and disable various modules at will
without having to edit configuration files.


.. note::

   You will still need to restart your Apache httpd server in order for
   these configuration changes to take effect.


.. _See_Also_Enabling_modules_debian:

See Also
~~~~~~~~


* :ref:`Recipe_Debian_Vhosts`

* ``man a2enmod`` (Type this at the command line for the ``a2enmod`` user
  manual.

* ``man a2dismod`` (Type this at the command line for the ``a2dismod`` user
  manual.

Summary
-------


Apache httpd is modular - the core is as small as possible, and all
interesting functionality is in optional modules. this means that
httpd can be as simple, or as featureful, as you want it to be, by
enabling and disabling various modules for the functionality you want,
or don't want.

Everything else in this book is implemented by some module or other,
which you'll need to have enabled to use the functionalty discussed.

