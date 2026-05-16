.. raw:: latex

   \part{Getting Started}

.. _Chapter_Installation:

============
Installation
============

.. epigraph::

   Only in our dreams are we truly free. 'Twas always thus
   and always thus shall be.

   -- *Dead Poets Society*


.. index:: Installation

.. index:: stanza or stanzata; see containers


For this book to be useful, you need to install the Apache HTTP Server
software. So what better way to start than with a set of recipes
that deal with the installation?

Because most Open Source projects deliver source code, rather than
binaries -- that is, executable files -- there are always
third parties that provide a variety of packages for installing the
product. As a result, there are a number of different ways that you
might end up installing the Apache httpd.

I'll cover the most common ones in this chapter. The differences may be
subtle, but they end up being important to understand before you
move on to future chapters, as they affect things like where files
get put, where configuration directives get put, and what the
default configuration is.

In addition to installing it from a prepackaged kit, of which the
variations are legion, there's always the option of building and
installing it from the source yourself. This has both advantages and
disadvantages; on the one hand, you know **exactly** what
you installed and where you put it. On the other hand, you have to
manage upgrades yourself, and remember to do those upgrades. And
various modules and add-ons that you add later may expect things to
be in certain places, other than those that you have chosen.

While in past times, the httpd project strongly recommended that you always
build from source, times have changed. Many web server
administrators have tens or hundreds of servers to maintain, rather
than one. And security bugs on software such as httpd
need to be addressed in hours, rather than weeks or months,
if you want your servers to remain uncompromised. These, and many
other reasons, have changed the landscape of server maintenance, and
I now recommend that, unless you have a compelling reason to do
otherwise, you install using the packages that are available for your
particular operating system distribution of choice.

Such compelling reasons include, for example, actively hacking on the
httpd source code (or its documentation), or writing your own modules 
for httpd.

This chapter can be roughly divided into four parts. The first set of
recipes deal with installing (and uninstalling) httpd
from various packages. Next, I discuss installing from source. The
third set of recipes are about starting and stopping the server once
it's installed. Finally, there are several recipes dealing with some
basic configuration, and other things you'll need to know to get
started running a server.

If you're managing httpd across many machines, or deploying in
containers, you'll also want to look at
:ref:`Chapter_Automated_Deployment`, which covers Ansible, Puppet,
Docker, Kubernetes, and Terraform.




.. _Recipe_Which_Version:

Which version of Apache HTTP Server to use
------------------------------------------

.. index:: Version

.. index:: Which version


.. _Problem_Which_Version:

Problem
~~~~~~~


You want to know which version of httpd is the right
one for you.


.. _Solution_Which_Version:

Solution
~~~~~~~~


Although there is not necessarily one right answer for everyone,
the Apache HTTP Server development team works very hard to ensure that
every release of the software is the best, most stable, most secure
product that they are able to put together, and each release of the
product fixes problems that were found in earlier releases. So, it's
always our position that the latest version of the server is the one
that you should be running.

That means the latest release of the 2.4.x branch. Check
https://httpd.apache.org/download.cgi for the current release number.


.. _Discussion_Which_Version:

Discussion
~~~~~~~~~~


In 2026, there's very little good reason to run an old version. If
you're staying behind because of a custom module that hasn't been ported,
that's understandable — but it should be a conscious, temporary decision,
not inertia.

If you have a large install base running an older version of
the server, it can indeed be a large undertaking to move those
servers to the latest version, with the subtle changes to the
configuration syntax that would need to be made to your
configuration files. You will find, however, that it is worth the
effort.

If, however, you are doing a new web server installation, there
is absolutely no good reason not to do with the latest version of the
product. You'll benefit from all of the bug fixes, security
patches, and new features that come with the latest release.

Whatever version you're running, subscribe to the
``announce@httpd.apache.org`` mailing list. This is a very low-volume
list — a handful of messages per year — that notifies you when a new
release is available. Pay particular attention when a release
announcement mentions CVEs (security vulnerabilities). When a release
fixes a CVE, you should upgrade promptly — not next quarter, not when
you get around to it. Attackers read those announcements too, and
in an AI era, exploits for disclosed vulnerabilities can appear within
minutes. Subscribe at https://httpd.apache.org/lists.html.

.. index:: announce@httpd.apache.org
.. index:: CVE
.. index:: security updates

.. _See_Also_Which_Version:

See Also
~~~~~~~~


* https://httpd.apache.org/docs/2.4/new_features_2_4.html
          
* The Apache HTTP Server download page at
  https://httpd.apache.org/download.cgi

* The announce mailing list (subscribe for release and security notices):
  https://lists.apache.org/list.html?announce@httpd.apache.org

.. refcosplay



.. _Recipe_Package_or_source:

Should I install from source, or use a package?
-----------------------------------------------

.. index:: Package or source

.. index:: Installation,Package or source?

.. index:: Should I install from source, or use a package


.. _Problem_Package_or_source:

Problem
~~~~~~~


You need to decide whether to install httpd from
source, or to use a package provided for your particular Operating
System (OS).


.. _Solution_Package_or_source:

Solution
~~~~~~~~


Under almost all circumstances, you'll want to use a package rather
than building from source.


.. _Discussion_Package_or_source:

Discussion
~~~~~~~~~~


The time has long passed where system administrators were encourage to
download, configure, build, and install their services from source code.
While in the past that was a reasonable and responsible thing to do, in
order to ensure that you knew what you were running, and where it came
from, this is no longer either practical or responsible in today's
world.

Building from source has certain advantages — you can make your own
mind up about things like directory layout and file placement, what
modules you want to build statically vs. dynamically, and so on. But
this very advantage can become a disadvantage very quickly if more
than one person has to maintain a server, and doesn't know, or agree
with, your preferences.

Installing from packages ensures that all of your servers are set up
the same way. It ensures that if someone else needs to work on your
server, they don't have to guess where things are located.

Perhaps more importantly, it ensures that updating a server requires
nothing more than ``apt update`` or ``dnf update``. This will
obtain necessary dependencies (which can change from one version to
another), and take care of all of the details of getting files
installed and configured.

You can also be assured that the version in the package has been
tested on exactly the version of OS that you're running, and any
per-platform idiosyncracies have been accounted for.

Finally, using a package from a distribution means that there will be
a community that can help you when things go wrong. If you roll your
own, when things break, you'll probably be told to switch to a tested,
supported, packaged version.

There is one specific certain scenario in which I recommend that you
build from source. This is if you're actively involved in code or documentation  development
of httpd. In that case, you're likely building from the latest development branch out of svn.
You'll want to build and test changes as you work on them. If that's your situation, you
probably don't need this chapter.


.. _See_Also_Package_or_source:

See Also
~~~~~~~~


* :ref:`Recipe_Build_from_source`

* :ref:`Recipe_Source_from_svn`

* :ref:`Chapter_Automated_Deployment` for managing httpd across many servers

.. refcosplay



.. _Recipe_Which_MPM:

Which MPM should I use?
-----------------------

.. index:: MPM

.. index:: Which MPM should I use?

.. index:: Multi-processing Module


.. _Problem_Which_MPM:

Problem
~~~~~~~


There are several MPMs (Multi-Processing Modules) available when you
install httpd, and you're not sure which one you
should choose.


.. _Solution_Which_MPM:

Solution
~~~~~~~~


Use the default. On any modern Unix system (Linux, FreeBSD, macOS),
that's **event**. On Windows, it's **mpm_winnt** — you don't get a
choice.



.. _Discussion_Which_MPM:

Discussion
~~~~~~~~~~


MPMs - Multi-Processing Modules - are the code that determines how the
httpd responds to multiple requests at the same
time. Some of these handle multiprocessing with threads, while others
run multiple processes, each of which handles requests. And some MPMs
use a mixture of both approaches.

The following table summarizes the available MPMs:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - MPM
     - Description
   * - **event**
     - Hybrid multi-process/multi-threaded. Uses a dedicated listener
       thread to handle keep-alive connections, freeing worker threads
       for active requests. The default and best choice for most
       deployments in 2026.
   * - **worker**
     - Hybrid multi-process/multi-threaded. Similar to event but
       without the dedicated listener thread — keep-alive connections
       tie up a worker thread. Largely superseded by event.
   * - **prefork**
     - Multi-process, no threads. Each child process handles one
       request at a time. Only use this if you're running a module
       that isn't thread-safe (increasingly rare in 2026).
   * - **mpm_winnt**
     - Windows-only. Single parent process with a pool of worker
       threads. The only option on Windows — you don't get to choose.
   * - **motorz**
     - Experimental event-driven MPM (trunk only). Not for production.
   * - **mpm_os2**
     - OS/2-only. You're unlikely to encounter this.

It is not critical, for the purpose of this recipe, to explain in
great detail how each MPM works, particularly if you're unfamiliar
with the concepts of multi-threading. However, if you do wish to read
about them more, there's more information in the documentation at
https://httpd.apache.org/docs/mpm.html and the pages 
linked from there.

On non-Unix platforms, you don't have a choice of MPM, and so this
question isn't relevant. On Unix plaforms, you have several choices,
but in 2026 the answer is straightforward: **use event**. Every modern
operating system that runs httpd — Linux, FreeBSD, macOS, Solaris, even
a Raspberry Pi — supports threads and thread-safe polling (epoll or
kqueue), which is all event needs. The historical fallback logic
(worker if no epoll/kqueue, prefork if no threads at all) exists in the
build system for portability, but you're unlikely to encounter a system
where it matters.

The only practical reason to choose prefork in 2026 is if you're running
a module that isn't thread-safe — and the only common example of that
was the embedded PHP SAPI (``mod_php``), which you shouldn't be using
anyway. Use PHP-FPM instead. See :ref:`Recipe_php-fpm`.

.. index:: PHP

.. index:: Threading

.. index:: Worker

.. index:: php-fpm

.. index:: Prefork

.. index:: Event



.. _See_Also_Which_MPM:

See Also
~~~~~~~~


* :ref:`Recipe_php-fpm`

* https://httpd.apache.org/docs/mpm.html


.. _Recipe_Install_redhat:

Installing on RPM-based Linux distributions
-------------------------------------------

.. index:: Installation,Red Hat

.. index:: Installation,RPM

.. index:: dnf

.. index:: RPM

.. index:: Fedora

.. index:: RHEL

.. index:: Installing on RPM-based Linux distributions


.. _Problem_Install_redhat:

Problem
~~~~~~~


You want to install or upgrade httpd on a Linux
distribution which is RPM-based, such as Fedora, CentOS Stream, AlmaLinux, Rocky Linux, or
Red Hat Enterprise Linux (RHEL).


.. _Solution_Install_redhat:

Solution
~~~~~~~~


Use the **dnf** utility to install the necessary packages:


.. code-block:: text

   % sudo dnf install httpd


If ``httpd`` is already installed, **dnf** will respond with a message
something like:


.. code-block:: text

   Package httpd-2.4.x already installed.
   Nothing to do


To upgrade an existing install, use the ``update`` command, rather than
``install``:


.. code-block:: text

   % sudo dnf update httpd


.. _Discussion_Install_redhat:

Discussion
~~~~~~~~~~


The **dnf** utility manages package installation on Linux distributions in
the Red Hat family — that is, primarily, Fedora, CentOS Stream, AlmaLinux, Rocky Linux, and Red Hat
Enterprise Linux (RHEL). It knows where to fetch the latest versions of
packages, and it keeps track of what you've got installed, as well as
dependencies between different packages.


In addition to the **httpd** packages, you may wish to install several
packages, including **httpd-devel**, **httpd-manual**, and **httpd-tools**.
**httpd-devel** contains programs related to developing httpd,
as well as utilities such as **apxs**, which you might use to
install third-party modules. **httpd-manual** contains the
documentation (**i.e.**, the manual) for the server. And **httpd-tools**
contains a variety of tools that are useful in managing your httpd,
such as **ab**, the performance tester, **htpasswd**, which
allows you to create password files for authentication, and
**logresolve**, which is used for resolving IP addresses in server log
files.


.. code-block:: text

   % sudo dnf install httpd httpd-devel httpd-manual httpd-tools


Note that packages of httpd have to be prepared by
members of the various Linux distribution communities, and so may
lag behind the latest version of httpd released by
the httpd project. 

Decisions about where to place files on your system are made by the
packagers for the various platforms, and may vary from examples in this
book. For a full description of where Fedora and RHEL
packages place files and directories, you should consult
https://cwiki.apache.org/confluence/display/httpd/DistrosDefaultLayout.

Note that installing the package does not automatically enable or start
the service. After installing, you'll need to:

.. code-block:: bash

   $ sudo systemctl enable httpd
   $ sudo systemctl start httpd


.. _See_Also_Install_redhat:

See Also
~~~~~~~~


* https://cwiki.apache.org/confluence/display/httpd/DistrosDefaultLayout

* ``man dnf``

* :ref:`Recipe_Uninstall_redhat`

* :ref:`Recipe_Opening_firewall`


.. _Recipe_Uninstall_redhat:

Uninstalling on RPM-based distributions
---------------------------------------

.. index:: Uninstall,Red Hat

.. index:: Uninstall,RPM

.. index:: dnf

.. index:: Fedora

.. index:: RHEL

.. index:: Uninstalling on RPM-based distributions


.. _Problem_Uninstall_redhat:

Problem
~~~~~~~


You want to uninstall httpd from a system running an
RPM-based distribution, such as Fedora, CentOS Stream, AlmaLinux, Rocky Linux, or Red Hat Enterprise
Linux (RHEL).


.. _Solution_Uninstall_redhat:

Solution
~~~~~~~~


Use the **dnf** utility to remove the package


.. code-block:: text

   % sudo dnf remove httpd


.. _Discussion_Uninstall_redhat:

Discussion
~~~~~~~~~~


The above command will remove the **httpd** package, and 
anything else you may have installed which depends on it.

The **dnf** utility, as mentioned above in
:ref:`Discussion_Install_redhat`, manages package installation, and also
keeps track of package dependencies. If you've installed supplementary
packages such as **httpd-manual** or **httpd-devel**, **dnf** will uninstall
them when you uninstall **httpd**, because they depend upon it, and
cannot function without it.

Any files that you have modified, such as configuration files or web
site content, will not be removed.


.. _See_Also_Uninstall_redhat:

See Also
~~~~~~~~


* ``man dnf``

* :ref:`Recipe_Install_redhat`


.. _Recipe_Install_debian:

Installing from Debian packages
-------------------------------

.. index:: Install,Debian

.. index:: apt-get

.. index:: Debian,Install

.. index:: Ubuntu,Install

.. index:: Installing from Debian packages


.. _Problem_Install_debian:

Problem
~~~~~~~


You have a computer running Debian, or one of the Debian-based
distributions, such as Ubuntu, and wish to install httpd.


.. _Solution_Install_debian:

Solution
~~~~~~~~


Using **apt-get**, install the ``apache2`` package:


.. code-block:: text

   % sudo apt-get install apache2


.. _Discussion_Install_debian:

Discussion
~~~~~~~~~~


As with any package-based Linux distribution, it's usually best
to stick with the packages supplied by that distribution in order to
have ease of updates, and maximum interoperability with other packages
installed on the same system. On Debian, this means using **apt-get**.

It's a good idea to install the **apache2-dev** package as well, as it provides
utilities, such as **apxs**, which
will be useful in installing third-party modules, should the need
arise.

Debian has its own unique arragement of configuration files,
which is unlike that of any other distribution. Both modules and sites
(virtual hosts) are arranged in subdirectories so that they can be
enabled or disabled at will using utilities that come with Debian's
version of httpd. For example, to enable a particular module, you
will use the **a2enmod** command, which
makes the appropriate changes to the server configuration file to
cause that module to be loaded. For example:


.. code-block:: text

   % sudo a2enmod rewrite


For a full description of where Debian places its files and directories,
you should consult https://cwiki.apache.org/confluence/display/httpd/DistrosDefaultLayout.

Unlike the RPM-based distributions, ``apt install apache2`` on
Debian/Ubuntu automatically enables and starts the service. You don't
need a separate ``systemctl enable`` step. However, if ufw is enabled,
you'll still need to open the firewall — see :ref:`Recipe_Opening_firewall`.


.. _See_Also_Install_debian:

See Also
~~~~~~~~


* https://cwiki.apache.org/confluence/display/httpd/DistrosDefaultLayout
          
* ``man a2enmod``

* ``man a2ensite``

* ``man apt-get``   


.. _Recipe_Uninstall_debian:

Uninstalling on Debian
----------------------

.. index:: Uninstall,Debian

.. index:: Debian,Uninstall

.. index:: Ubuntu,Uninstall

.. index:: apt-get

.. index:: Uninstalling on Debian


.. _Problem_Uninstall_debian:

Problem
~~~~~~~


You've installed Apache httpd on your Debian or Ubuntu system and now you
want to uninstall it.


.. _Solution_Uninstall_debian:

Solution
~~~~~~~~


Use the _apt_get_ utility to remove the package and its dependencies:


.. code-block:: text

   % sudo apt-get remove apache2


.. _Discussion_Uninstall_debian:

Discussion
~~~~~~~~~~


The above command will remove the **apache2** package, and anything else
you may have installed which depends on it.

**apt** keeps track of package dependencies, so if you've installed
supplementary packages, such as **apache2-dev**, those will also be
uninstalled, since they won't work without the base package.

Any files that you've modified, such as configuration files or website
content, will not be removed. If you wish to do so, `apt-get purge
apache2` will take care of that for you.


.. _See_Also_Uninstall_debian:

See Also
~~~~~~~~


:ref:`Recipe_Install_debian`


.. _Recipe_Install_Windows:

Installing httpd on Microsoft Windows
-------------------------------------

.. index:: Install,Microsoft Windows

.. index:: Windows,Install

.. index:: Microsoft Windows,Install

.. index:: WAMP

.. index:: Installing Apache on Microsoft Windows


.. _Problem_Install_Windows:

Problem
~~~~~~~


You want to install httpd software on a Windows platform.


.. _apacheckbk-CHP-1-NOTE-69:


.. tip::

   If you already have httpd installed on your Windows system,
   remove it before installing a new version. Failure to do this
   results in unpredictable behavior. See :ref:`Recipe_Uninstall_windows`.


.. _Solution_Install_Windows:

Solution
~~~~~~~~


The Apache httpd project releases source code, not compiled binaries.
On Windows, you will need to use a third-party distribution. The
official list of recommended distributions is at
https://httpd.apache.org/docs/platform/windows.html#down

The recommended approach is to use **Apache Lounge**
(https://www.apachelounge.com/), which provides up-to-date Windows
binaries compiled with the latest Visual Studio. Download the zip
archive, extract it to a location such as ``C:\Apache24``, and then
open a command prompt as Administrator to install the service::

   cd C:\Apache24\bin
   httpd.exe -k install

You can then start the service with::

   httpd.exe -k start

or manage it from the Windows Services panel.

If you also need PHP and MySQL, consider **XAMPP**
(https://www.apachefriends.org/), which bundles Apache httpd, MariaDB,
PHP, and Perl into a single installer. XAMPP is convenient for
development, but Apache Lounge is preferred for production or when you
want a standalone httpd installation without the extras.


.. _Discussion_Install_Windows:

Discussion
~~~~~~~~~~


Apache Lounge has been the de facto source of Windows httpd binaries
for many years. The builds closely track the official release schedule
and are compiled against current versions of OpenSSL and other
dependencies. The zip archive approach gives you full control over the
installation layout and configuration.

WAMP distributions like XAMPP bundle httpd with a database and scripting
language — convenient for getting a development environment running
quickly, but they add components you may not need and can complicate
upgrades.

.. index:: Apache Lounge

.. index:: XAMPP

.. index:: WAMP

.. note::

   Other Windows distributions exist and are listed on the official
   download page. However, some that were popular in the past have been
   discontinued or moved behind commercial paywalls. Apache Lounge
   remains the most reliable source of standalone Windows httpd
   binaries.


.. _See_Also_Install_Windows:

See Also
~~~~~~~~


.. _Recipe_Uninstall_windows:

Uninstalling on Microsoft Windows
---------------------------------

.. index:: Uninstall

.. index:: Uninstall,Microsoft Windows

.. index:: Windows,Uninstall

.. index:: Microsoft Windows,Uninstall

.. index:: Uninstalling in Microsoft Windows


.. _Problem_Uninstall_windows:

Problem
~~~~~~~


You installed Apache httpd on Microsoft Windows, and now you wish to
uninstall it.


.. _Solution_Uninstall_windows:

Solution
~~~~~~~~


If you installed httpd from Apache Lounge (a ZIP extraction), uninstalling
is the reverse of installing: remove the service, then delete the files.

From an elevated command prompt:

.. code-block:: text

   C:\Apache24\bin> httpd.exe -k uninstall

Then delete the ``C:\Apache24`` directory (or wherever you extracted it).


.. _Discussion_Uninstall_windows:

Discussion
~~~~~~~~~~


Since Apache Lounge distributes httpd as a plain ZIP file (no MSI
installer), there's nothing in "Add/Remove Programs" to uninstall.
The ``httpd.exe -k uninstall`` command removes the Windows service
registration; after that, you just delete the directory.

If you installed a named service (e.g., ``httpd.exe -k install -n
"MyApache"``), uninstall it with the same name:

.. code-block:: text

   C:\Apache24\bin> httpd.exe -k uninstall -n "MyApache"

Any configuration files or site content you created won't be
automatically removed — you're responsible for cleaning those up.


.. _See_Also_Uninstall_windows:

See Also
~~~~~~~~


* :ref:`Recipe_Install_Windows`


.. _Recipe_Install_OSX:

Installing on macOS
-------------------

.. index:: Installation,macOS

.. index:: macOS,Install

.. index:: macOS,Install

.. index:: Installing on macOS


.. _Problem_Install_OSX:

Problem
~~~~~~~


You want to install httpd on macOS.


.. _Solution_Install_OSX:

Solution
~~~~~~~~


Apple still ships Apache httpd with macOS (as of 2026). To start it, open
the Terminal app, and type:


.. code-block:: text

   sudo apachectl start


.. _Discussion_Install_OSX:

Discussion
~~~~~~~~~~


Apple ships Apache httpd with macOS and updates it periodically via
system updates. As of early 2026, macOS ships httpd 2.4.66. You
don't have to install it yourself — it's already at
``/usr/sbin/httpd``.

However, if you want to install a different version of httpd, or
update more frequently than updates are available via the standard
mechanism, there are a few options available to you.

One is to download and build the source code yourself (See
:ref:`Recipe_Downloading` and :ref:`Recipe_Build_from_source`.

Another option is to use one of the third-party package managers which
is available for macOS.

I recommend Homebrew (https://brew.sh/). Once you've installed it,
install Apache httpd with:


.. code-block:: text

   brew install httpd



.. _See_Also_Install_OSX:

See Also
~~~~~~~~


* :ref:`Recipe_Downloading`

* :ref:`Recipe_Build_from_source`


.. _Recipe_Uninstall_OSX:

Uninstalling on macOS
---------------------

.. index:: Uninstallation,macOS

.. index:: macOS,Uninstall

.. index:: macOS,Uninstall

.. index:: Uninstalling on macOS


.. _Problem_Uninstall_OSX:

Problem
~~~~~~~

You want to disable Apache httpd that is installed on your macOS system.


.. _Solution_Uninstall_OSX:

Solution
~~~~~~~~


To disable the Apache httpd installation on your macOS
system, type the following in a Terminal window:


.. code-block:: text

   sudo launchctl bootout system/org.apache.httpd


.. _Discussion_Uninstall_OSX:

Discussion
~~~~~~~~~~


httpd is installed by default on macOS, as mentioned in
:ref:`Recipe_Install_OSX`. If it's running and you want to stop it
from starting at boot, use the ``launchctl bootout`` command shown
above. (Older documentation and tutorials may reference
``launchctl unload -w`` — that syntax is deprecated on modern macOS
and may produce errors.)

To stop it immediately without waiting for a reboot:
``sudo apachectl stop``.

If you installed httpd via Homebrew, uninstall it with
``brew uninstall httpd``.


.. _See_Also_Uninstall_OSX:

See Also
~~~~~~~~


:ref:`Recipe_Uninstalling_Apache`


.. _Recipe_Uninstalling_Apache:

Uninstalling httpd
------------------

.. index:: Uninstall

.. index:: Uninstall,manual

.. index:: Uninstalling Apache


.. _Problem_Uninstalling_Apache:

Problem
~~~~~~~


You have httpd installed on your system, and you want to remove it, but
it wasn't installed via one of the standard methods.


.. _Solution_Uninstalling_Apache:

Solution
~~~~~~~~


If you installed via an installation package, there are recipes
elsewhere in this chapter that show how to uninstall those.

* For RPM-based packages, see :ref:`Recipe_Uninstall_redhat`
* For deb-based packages, see :ref:`Recipe_Uninstall_debian`
* For Windows, see :ref:`Recipe_Uninstall_windows`

Other packaging systems may provide some similar mechanism. If
they don't, however, chances are that cleaning out all the files will
require a lot of manual work. Or, if you installed from source,
there's really not an automated way to uninstall, and you'll need
to clean up the files manually.


.. _Discussion_Uninstalling_Apache:

Discussion
~~~~~~~~~~


Unfortunately, there's no generic works-for-all removal method for the
httpd, because there are so many different ways that
you can install it.

I have provided recipes for the most common packaging systems. For
RPM-based packages, see :ref:`Recipe_Uninstall_redhat`. For
Debian-based packages, see :ref:`Recipe_Uninstall_debian`. And to
uninstall on Windows, see :ref:`Recipe_Uninstall_windows`.
      
However, if the software was installed by building from the sources (see
:ref:`Recipe_Build_from_source`), the burden of
knowing where files were put rests with the person who did the build
and install. On Windows with Apache Lounge, everything lives in the
directory where you extracted the ZIP (typically ``C:\Apache24``) — there's
no system registry integration or Add/Remove Programs entry.

For a Unixish system, if you have access to the directory in
which the server was built, look for the **--prefix**
option in the **config.nice** file.
That will give you a starting point, at least. Here are the directories
a typical httpd installation creates on your filesystem:

* **bin** 

* **build** 

* **cgi-bin** 

* **conf** 

* **error** 

* **htdocs** 

* **icons** 

* **include** 

* **lib** 

* **logs** 

* **man** 

* **manual** 

* **modules**

The location of some of these files can often be determined by typing
the command:


.. code-block:: text

   % sudo httpd -V


The output of this will tell you, among other things, the following
pieces of information:


.. code-block:: text

   -D HTTPD_ROOT="/etc/httpd"
   -D SUEXEC_BIN="/usr/sbin/suexec"
   -D DEFAULT_PIDLOG="/run/httpd/httpd.pid"
   -D DEFAULT_SCOREBOARD="logs/apache_runtime_status"
   -D DEFAULT_ERRORLOG="logs/error_log"
   -D AP_TYPES_CONFIG_FILE="conf/mime.types"
   -D SERVER_CONFIG_FILE="conf/httpd.conf"


In the example shown here, ``HTTPD_ROOT`` is set to **/etc/httpd**, which
indicates that other directories are likely to be in subdirectories
of that location. the ``DEFAULT_ERRORLOG`` is in ``logs/error_log``, and
the lack of a leading slash on that means that it is relative to the
``HTTPD_ROOT`` directory - that is, that the error log is located at
``/etc/httpd/logs/error_log``, and the other log files are likely to
be in that same directory.

Likewise, the configuration files are located in **/etc/httpd/conf**,
which you can determine by combining the ``HTTPD_ROOT`` and
``SERVER_CONFIG_FILE`` values.

If you installed from source using all of the defaults, everything is
likely to be in the same place, and that is usually going to be
the directory **/usr/local/apache2**.

To uninstall, you'll need to locate and remove each of these component
directories.


.. _See_Also_Uninstalling_Apache:

See Also
~~~~~~~~


* :ref:`Recipe_Build_from_source`

* :ref:`Recipe_Where_are_my_files`

* :ref:`Recipe_config.nice`


.. _Recipe_Downloading:

Downloading the httpd sources
-----------------------------

.. index:: Downloading

.. index:: Source,Downloading

.. index:: Downloading the Apache sources


.. _Problem_Downloading:

Problem
~~~~~~~


You want to download the Apache httpd source code so that you can
build it yourself.


.. _Solution_Downloading:

Solution
~~~~~~~~


Download the source tarball from
https://httpd.apache.org/download.cgi#apache24 and unpack it
using the **tar** utility.

.. code-block:: text

   % tar vzxf httpd-2.4.67.tar.gz


.. tip::

   The version number in examples throughout this chapter (2.4.67) was
   current at the time of writing. Check
   https://httpd.apache.org/download.cgi for the latest release version,
   and substitute that version number in the commands below.

Alternatively, you can obtain the source directly from version control
(SVN). See :ref:`Recipe_Source_from_svn`.


.. _Discussion_Downloading:

Discussion
~~~~~~~~~~


There are, in fact, a number of different ways to obtain the source
code for httpd. These include the method shown
above, obtaining a source package for your particular OS, and getting
it straight from revision control. The most common of these is to
get it from the httpd download site.

The page at https://httpd.apache.org/download.cgi lists the
latest releases of httpd. Downloads are served directly from the ASF's
CDN — the old mirror network was retired in 2021. You should still
verify the integrity of what you download using PGP signatures or SHA
checksums. See :ref:`Recipe_Verify_download` for details.

.. figure:: ../images/download_page_2026.png
   :alt: The httpd download page showing source links with PGP and SHA links

   The httpd download page. Note the [PGP], [SHA256], and [SHA512] links
   next to each source archive — these are separate downloads.

Each source archive (the ``.tar.gz`` or ``.tar.bz2`` file) is accompanied
by separate verification files. You need to download both the source
archive *and* its corresponding signature or checksum file — they're
separate links on the download page. Download the ``.tar.gz``, then also
grab the ``[PGP]`` or ``[SHA256]`` link next to it. These small files are
what you'll use to verify the download hasn't been tampered with.

Once you've downloaded the file and verified that it's valid, you can
unpack the archive (the "tarball") using the **tar**
utility.

.. code-block:: text

   % tar vzxf httpd-2.4.67.tar.gz


The ``vzxf`` argument supplied to **tar** is in fact four arguments. 

The ``v`` argument says to be verbose - that is, tell us everything that
it is doing. This will cause it to list all of the files that it is
unpacking as it unpacks them. 
  
The ``z`` argument says to undo the zip compression that has been
applied to the archive.

``x`` indicates that you wish to extract the archive.

Finally, ``f`` indicates that the next argument is the name of a file -
in this case, **httpd-2.4.67.tar.gz**.

The archive contents will now be unpacked into a subdirectory named
after the version that you've downloaded - in this case, the
directory will be named **httpd-2.4.67**.

For the next steps, go to the recipe :ref:`Recipe_Build_from_source`.

Another option is to obtain the source directly from version control.
All of the Apache httpd source code is developed in public, in a
Subversion repository at svn.apache.org. To obtain the
source directly from version control, see
:ref:`Recipe_Source_from_svn`.

No matter how you obtained the source, the directory tree will be
ready for configuration and building. Once the source is in place, you
should be able to move directly to building the package. (See
:ref:`Recipe_Build_from_source`.)


.. _See_Also_Downloading:

See Also
~~~~~~~~


* :ref:`Recipe_Build_from_source`

* :ref:`Recipe_Install_Windows`


* :ref:`Recipe_Source_from_svn`

* :ref:`Recipe_Verify_download`


.. _Recipe_Verify_download:

Verifying the validity of a downloaded file
-------------------------------------------

.. index:: Verifying download

.. index:: GPG

.. index:: PGP

.. index:: SHA256

.. index:: SHA512

.. index:: Verifying the validity of a downloaded file


.. _Problem_Verify_download:

Problem
~~~~~~~


You've downloaded httpd from a mirror server, and want
to be certain that it's unmodified from the original release.


.. _Solution_Verify_download:

Solution
~~~~~~~~


Use the PGP signature or the SHA256/SHA512 checksum, available next
to the download link, to verify that the file is what it should be:


.. code-block:: bash

   $ gpg --verify httpd-2.4.67.tar.gz.asc httpd-2.4.67.tar.gz
   $ sha256sum httpd-2.4.67.tar.gz
   $ cat httpd-2.4.67.tar.gz.sha256


On macOS, the command is ``shasum -a 256`` rather than ``sha256sum``
(unless you've installed GNU coreutils via Homebrew).

.. _Discussion_Verify_download:

Discussion
~~~~~~~~~~


.. _FIG_download_source:


.. figure:: ../images/download_source.png
   :alt: Download source

   Download source


Next to each download link, there are three additional links, which
assist in ensuring that the file that you are downloading is in fact
the one that you intend to be downloading. While downloads come from the ASF's CDN, it's still good practice
to verify that nothing went wrong in transit.

The verification files, labeled **PGP**,
**SHA256**, and **SHA512**, come directly from the **www.apache.org/dist**
site, as you can verify by hovering the mouse pointer over the link
and looking at the URL in the status bar. In that way, even though
the source file comes from a mirror site that you may never have
heard of, you know that these files come from a known trusted site.

Download the source compressed archive, and these three additional
files, into the same location, then verify each at the command line
using the commands listed in the recipe above.

First, use the **gpg** utility to check the PGP signature contained in
the **asc** file:


.. code-block:: text

   $ gpg --verify httpd-2.4.67.tar.gz.asc


Most likely, the first time you do this, you'lll receive the following
output:


.. code-block:: text

   gpg: Signature made Tue Apr 28 14:15:15 2026 EDT
   gpg:                using RSA key 65B2D44FE74BD5E3DE3AC3F082781DE46D5954FA
   gpg: Can't check signature: No public key


This requires a little bit of explanation.

The PGP signature is created by the release manager - the individual
member of the Project Management Committee (PMC) who steps up to make
a particular release. The signature is applied using a PGP key,
which is a cryptographic file that represents that person's
identity. A full discussion of the mathematical details of PGP can
be found at https://en.wikipedia.org/wiki/Pretty_Good_Privacy

For the sake of simplicity, however, I'll just say that a PGP key is
like a seal, which people used in simpler times to mark a letter and
ensure that it came from them. It's more secure than that, though,
as it is validated by a pass code, and by sophisticated encryption.

In order to verify a signature, you need to have the public key that
goes with the key ID referenced in the signature above. The easiest way
to get all httpd release signing keys at once is to import the project's
KEYS file:


.. code-block:: bash

   $ curl https://dist.apache.org/repos/dist/release/httpd/KEYS | gpg --import

You'll see a lot of output — the KEYS file contains every release manager's
key going back to the 1990s:

.. code-block:: text

   gpg: key 508EAEC5302DA568: "Ken Coar/Rodent of Unusual Size (Generic key) <Ken@Coar.Org>" not changed
   gpg: key 82781DE46D5954FA: public key "Eric Covener <covener@apache.org>" imported
   gpg: key 5A4B10AE43B56A27: public key "Joe Orton (Release Signing Key) <jorton@apache.org>" imported
   ...
   gpg: Total number processed: 74
   gpg:               imported: 20
   gpg:              unchanged: 22

Ignore the warnings about "bad signatures" and "SHA1 algorithm rejected" —
those are old cross-signatures between keys and don't affect your ability to
verify releases. What matters is that the release manager's key was imported
successfully.

You only need to do this once (or again when a new release manager starts
signing releases).

Alternatively, if you just want the specific key for a single release,
use the key fingerprint from the ``gpg --verify`` output:

.. code-block:: bash

   $ gpg --keyserver keyserver.ubuntu.com --recv-keys 65B2D44FE74BD5E3DE3AC3F082781DE46D5954FA

Now that you have the key, you'll try again to verify the signature:


.. code-block:: text

   $ gpg --verify httpd-2.4.67.tar.gz.asc
   gpg: assuming signed data in 'httpd-2.4.67.tar.gz'
   gpg: Signature made Tue Apr 28 14:15:15 2026 EDT
   gpg:                using RSA key 65B2D44FE74BD5E3DE3AC3F082781DE46D5954FA
   gpg: Good signature from "Eric Covener <covener@apache.org>" [unknown]
   gpg:                 aka "Eric Covener <ecovener@us.ibm.com>" [unknown]
   gpg: WARNING: This key is not certified with a trusted signature!
   gpg:          There is no indication that the signature belongs to the owner.
   Primary key fingerprint: 65B2 D44F E74B D5E3 DE3A  C3F0 8278 1DE4 6D59 54FA


Well, that looks almost right. It says that the signature is good,
which is what you cared about. That means that the file that you
downloaded matches the signature file that you downloaded, and
you've verified that you have a good (trustworthy) file.

If, on the other hand, you see something like:


.. code-block:: text

   $ gpg --verify httpd-2.4.67.tar.gz.asc
   gpg: assuming signed data in 'httpd-2.4.67.tar.gz'
   gpg: Signature made Tue Apr 28 14:15:15 2026 EDT
   gpg:                using RSA key 65B2D44FE74BD5E3DE3AC3F082781DE46D5954FA
   gpg: BAD signature from "Eric Covener <covener@apache.org>"


That would indicate that the file was tampered with between the time it was signed
and when you downloaded it, and you should try to get it from a different mirror server
and verify it again.

The "not certified with a trusted signature" warning means you haven't
personally verified that this key belongs to Eric (or whoever signed
the release). If you ever meet a release manager at a conference and
verify their key in person, you can sign it — after that, the warning
goes away. For day-to-day use, "Good signature" is what matters.




The other two files are rather simpler methods of verification, and
are called hashes. Stated very simply, a hashing algorithm is a
mathematical means of taking a sum of a file. Imagine if you added
up all of the characters in a file into a single number, and that
number represented the file. SHA256 and SHA512 are more sophisticated
versions of that idea — they produce a fixed-length fingerprint that
represents the contents of a file.

Although it is possible to have several different files that have the
same hash, it's unlikely, and it's difficult to do intentionally.
Thus, if the hash on a file matches the expected hash, it's almost
certain that the file hasn't been tampered with.

To check the hashes on the file, use the utilities mentioned in the
recipe above:


To verify with SHA256:


.. code-block:: text

   $ sha256sum httpd-2.4.67.tar.gz && cat httpd-2.4.67.tar.gz.sha256
   <check https://httpd.apache.org/download.cgi for current checksums>
   <check https://httpd.apache.org/download.cgi for current checksums>


.. note::

   The PGP signature is the strongest form of verification — it proves
   both integrity and authenticity (that the file was released by a
   trusted httpd committer). The SHA checksums verify integrity only.
   Either way, if they match, you're good.


.. _See_Also_Verify_download:

See Also
~~~~~~~~


* :ref:`Recipe_Downloading`


.. _Recipe_Source_from_svn:

Obtaining the source from version control
-----------------------------------------

.. index:: Subversion

.. index:: SVN

.. index:: GitHub mirror

.. index:: Version control

.. index:: Obtaining the source from version control


.. _Problem_Source_from_svn:

Problem
~~~~~~~


You wish to obtain the latest development version of the source code.


.. _Solution_Source_from_svn:

Solution
~~~~~~~~


For the very latest, up-to-the-minute development source code (not
guaranteed to actually be functional), clone the ``trunk`` branch using the
following:



.. code-block:: text

   svn checkout https://svn.apache.org/repos/asf/httpd/httpd/trunk httpd-trunk


To obtain a particular release branch, such as 2.4.x, you would
instead use a command like:


.. code-block:: text

   svn checkout https://svn.apache.org/repos/asf/httpd/httpd/branches/2.4.x httpd-2.4


.. _Discussion_Source_from_svn:

Discussion
~~~~~~~~~~


The Apache httpd source code is developed in Subversion (SVN), hosted at
``svn.apache.org``. This is the canonical repository — all commits,
branches, and tags live here. There is a read-only Git mirror on GitHub
(https://github.com/apache/httpd), but patches submitted via GitHub PRs
tend to get overlooked. If you want to contribute, work with SVN and send
patches to ``dev@httpd.apache.org``. See :ref:`Chapter_Contributing_to_apache`
for more on this.

You can read more about Subversion at https://subversion.apache.org/. If
you're more comfortable with Git, the GitHub mirror at
https://github.com/apache/httpd works fine for reading
the source and tracking changes — just be aware it's not where development
happens.

If you're interested in following the latest development of the
server, you want to follow the ``trunk`` branch, which is where active
development occurs.

On the other hand, when the software is released for general
consumption, a branch is created, where only bug fixes, and stable
complete features, are added. These branches are more likely to be
functional at any given moment, and, of course, move much more slowly
than the active development in trunk.

For a complete list of the available release branches, see
https://svn.apache.org/repos/asf/httpd/httpd/branches/

Tags represent specific release version
numbers. Tags are immutable - that is, once a release has been made,
it is never changed again, as it marks a particular point in the
history of development.

You can find the names of the release branches and tags at
https://svn.apache.org/repos/asf/httpd/httpd/
or with the commands:


.. code-block:: text

   svn ls https://svn.apache.org/repos/asf/httpd/httpd/tags/
   svn ls https://svn.apache.org/repos/asf/httpd/httpd/branches/


If you wanted to check out the source code for a particular release
tag, for example, the 2.4.67 release, you would do the following:


.. code-block:: text

   svn checkout https://svn.apache.org/repos/asf/httpd/httpd/tags/2.4.67 httpd-2.4.67


.. _apacheckbk-CHP-1-NOTE-71:


.. tip::

   Release tags follow the pattern ``X.Y.Z`` (e.g., ``2.4.67``).
   Other tags exist for internal development purposes — stick to
   the numeric release tags when checking out a specific version.


To keep your checked-out source up-to-date, run the following
command from the top level of the source directory:


.. code-block:: text

   svn update


This will fetch any files that have been changed or added since your
last checkout or update.

If you update to the latest version of the sources, you're
getting whatever the developers are currently working on, which may be
only partially finished. If you want reliability, stick with the
released versions, which have been extensively tested.

To build these various checkouts into a running server, see
:ref:`Recipe_Build_from_source`.

If you're interested in making changes to the source code, and
contributing those back to the httpd project, see the recipes in the
chapter :ref:`Chapter_Contributing_to_apache`, *Contributing to httpd
httpd*.


.. _See_Also_Source_from_svn:

See Also
~~~~~~~~


* :ref:`Recipe_Build_from_source`

* :ref:`Chapter_Contributing_to_apache` for basic SVN workflow and patch submission


.. _Recipe_Build_from_source:

Building httpd from the sources
-------------------------------

.. index:: Source,build

.. index:: Build from source

.. index:: Building Apache from the sources


.. _Problem_Build_from_source:

Problem
~~~~~~~


You want to build your httpd from the sources
directly rather than installing it from a prepackaged kit.


.. _Solution_Build_from_source:

Solution
~~~~~~~~


Assuming that you already have the httpd source tree—whether
you installed it from a tarball, Git, or some distribution
package, the following commands—executed in the top directory of the
tree, builds the server package with most of the standard modules as
DSOs:


.. code-block:: text

   ./buildconf
   ./configure --prefix=/usr/local/apache
   > --enable-layout=Apache --enable-modules=most --enable-mods-shared=all \
   > --with-mpm=event
   make
   sudo make install


If you want more detailed information about the various options
provided to the **configure** command, and their meanings, you can
use the following command:


.. code-block:: text

   ./configure --help


.. _Discussion_Build_from_source:

Discussion
~~~~~~~~~~


Building the server from the sources can be complex and
time-consuming, but it's essential if you intend to make any changes
to the source code. It gives you much more control over things, such
as the use of shareable object libraries and the database routines
available to modules. Building from source is also **de rigeur** 
if you're developing your own httpd modules.

If you want to build the modules statically into the server,
replace any occurrences of
``--enable-mods-shared=list``
with
``--enable-mods=list``.

The options to the **configure** script are many and varied; if
you haven't used it before to build httpd, the document at
https://httpd.apache.org/docs/install.html is a
good crash course. The default options generally produce a
working server, although the filesystem locations and module choices
may not be what you'd like; they may include modules you 
don't want or omit some you do. (See 
:ref:`Chapter_Common_modules`, for some examples.)

The **buildconf** command creates the **configure** script, and
is only strictly necessary if you obtained the source from version control (see
:ref:`Recipe_Source_from_svn`). If you downloaded the source in a release
tarball, on the other hand, the **configure** script is already part of
the package.

**buildconf** itself has a number of dependencies. In particular, you'll
need to have a C compiler, **autoconf**, **libtool**, and several
development libraries installed. On a fresh Linux system, you may need to
install all of these before building. On RPM-based distributions
(AlmaLinux, Fedora, CentOS Stream, RHEL, etc.):


.. code-block:: text

   sudo dnf install gcc make autoconf libtool \
       expat-devel pcre2-devel openssl-devel \
       libxml2-devel svn


On Debian-based distributions (Debian, Ubuntu, Mint, etc.):


.. code-block:: text

   sudo apt install build-essential autoconf libtool \
       libexpat1-dev libpcre2-dev libssl-dev \
       libxml2-dev subversion


.. index:: autoconf
.. index:: libtool
.. index:: expat-devel
.. index:: pcre2-devel
.. index:: openssl-devel
.. index:: build-essential
.. index:: Build prerequisites

You'll also probably need to have a checkout of APR, which you can
obtain by typing the following at the root directory of your httpd
source tree:


.. code-block:: text

   svn co http://svn.apache.org/repos/asf/apr/apr/trunk srclib/apr


.. note::

   This is the command that ``buildconf`` itself will suggest if APR is
   missing. You can also check https://apr.apache.org/ for the latest
   release version and check out a specific tag instead of trunk if you
   prefer a stable release.


When you run **configure**, you'll see eleventy billion messages scroll
past which are checking whether various things are available on the
target system. These are ensuring that the build process has what it
needs for success. The **configure** script the writes the Makefile
that will orchestrate the build.

Prerequisites include APR and PCRE, two libraries that you'll need to
obtain and install. Further information on these prerequisites may be
found at https://apr.apache.org/ and
https://pcre.org/ respectively, or you can install them via
your package manager.

If you checked out a copy of APR, as shown above, you can instruct
**configure** to use it with the ``--with-included-apr`` option. You may
also discover that, on your particular development machine, other
libraries need to be installed, such as **libxml2**. Just follow the
error messages and obtain the libraries that they complain about.

The **make** command compiles the code into binary files, and _make
``install`` places these files into their final locations. Each of these
steps may take a considerable amount of time.


.. _See_Also_Build_from_source:

See Also
~~~~~~~~


* :ref:`Recipe_Downloading`

* https://httpd.apache.org/docs/install.html

* https://apr.apache.org/

* https://pcre.org/

* :ref:`Recipe_Building_from_source_advanced`


.. _Recipe_Building_from_source_advanced:

Building from source, advanced
------------------------------

.. index:: Source,build

.. index:: Build from source

.. index:: configure

.. index:: Commands,configure


.. _Problem_Building_from_source_advanced:

Problem
~~~~~~~


The **configure** script, that
is used to set up a build from source, has many options, and it's not
clear which ones are really important.


.. _Solution_Building_from_source_advanced:

Solution
~~~~~~~~


Here are some of the most important and useful options that you
you might want to use:

``--prefix``
      Specifies the top level of the directory tree into which
      files will be put. The default is usually
      ``--prefix=/usr/local/apache2``, but different
      layouts can change this (see the
      --enable-layout option in this section).

.. index:: Layout

.. index:: File layout

``--enable-layout``
      This allows you to select one of the predefined filesystem
      structures; that is, where **make install** should put all the
      files. To see where files will be put for a particular layout,
      examine the :file:`config.layout` file in the top level of the source
      tree.

Currently the predefined layouts include:

* AIX

* Apache

* BSDI 

* Darwin 

* Debian

* Fedora

* FreeBSD 

* GNU 

* OpenBSD 

* OpenWrt

* opt 

* RedHat 

* RPM

* Slackware-FHS

* Solaris 

* SuSE

See :ref:`Recipe_Where_are_my_files` for further discussion of the
various layouts.
``--enable-mods-shared``
              This option controls which modules will be built as DSOs
              rather than being linked statically into the server. An
              excellent shortcut value is **most**. See
              :ref:`Chapter_Common_modules` for more on working with modules.

``--enable-ssl``
              If you're going to be running a secure server, you will
              need to include this option, as the SSL module is
              **not** activated by default. See
              :ref:`Chapter_SSL_and_TLS` for SSL/TLS configuration recipes.

``--enable-md``
    Enables _mod_md_, which provides automatic provisioning and
    configuration of Let's Encrypt SSL/TLS certificates. See
    :ref:`Recipe_acme_mod_md` for configuration details.

``--enable-http2``
    Enables HTTP/2 protocol handling, which is not enabled by default.
    See :ref:`Recipe_enabling-http2` for setup details.

``--enable-suexec``
        Use this option if you want the **suexec** utility to be
        built. Because of the degree to which it depends on the
        rest of the server build, you should specify this when
        configuring the main server build, and not try to build
        **suexec** later. See
        :ref:`Running_CGI_Scripts_as_a_Different_User_with_suexec_id144040`.

``--with-apr``, ``--with-apr-util``
              If you have multiple versions of the Apache Portable
              Runtime library and utilities installed—as you might if
              you build httpd on a system with other APR-dependent software
              installed—you can use these options to ensure that the
              httpd is built with a compatible APR version.

``--with-included-apr``
        This option is a nice shorthand way of specifying the
        compatible bundled version of APR should be used. 
        
``--with-mpm``
        The Multi-Processing Model, or MPM, defines how the server
        handles requests by setting the relationship between threads and
        child processes. Usually the **configure** script will choose one
        appropriate for the platform on which you're building, but
        sometimes you may want to override this. For example, if you're
        going to be using the PHP scripting module, you need to use the
        **prefork** MPM in order to
        avoid problems. See :ref:`Recipe_Which_MPM` for guidance on
        choosing an MPM.

``--with-port``
        This option is useful if you are building the server under a
        non-**root** username but intend to run it as a system daemon. The
        **configure** script chooses a different default for the port number
        depending upon whether it's being run by **root** or not. With this
        option you can override this behaviour. The most common use of this
        option is:


.. code-block:: text

   --with-port=80


.. tip::

   Starting a service on port 1024 or lower requires root privileges. If
   you want a non-root user to be able to start up the server, you'll
   want to have it start up on a higher port. 8080 is a common
   alternative to 80 in this situation.


.. _Discussion_Building_from_source_advanced:

Discussion
~~~~~~~~~~


Minimal documentation for all of the **configure** options is available from the
script itself:


.. code-block:: text

   % ./configure --help


However, for more detailed understanding you need to consult the
httpd documentation itself—or look at the source code.


.. _See_Also_Building_from_source_advanced:

See Also
~~~~~~~~


* https://httpd.apache.org/docs/install.html

* :ref:`Recipe_Where_are_my_files`


.. _Recipe_Opening_firewall:

Opening the firewall
--------------------

.. index:: firewall
.. index:: firewalld
.. index:: ufw
.. index:: iptables


.. _Problem_Opening_firewall:

Problem
~~~~~~~

You've installed and started httpd, but you can't reach it from another
machine.


.. _Solution_Opening_firewall:

Solution
~~~~~~~~

Your operating system's firewall is likely blocking incoming connections
on ports 80 and 443. The fix depends on which firewall manager you're
running.

**Fedora, RHEL, CentOS Stream, AlmaLinux, Rocky Linux** (firewalld):

.. code-block:: bash

   $ sudo firewall-cmd --permanent --add-service=http
   $ sudo firewall-cmd --permanent --add-service=https
   $ sudo firewall-cmd --reload

**Ubuntu, Debian** (ufw):

.. code-block:: bash

   $ sudo ufw allow 'Apache Full'

Or, if the Apache profile isn't registered:

.. code-block:: bash

   $ sudo ufw allow 80/tcp
   $ sudo ufw allow 443/tcp

**SUSE** (firewalld): same commands as Fedora/RHEL above.


.. _Discussion_Opening_firewall:

Discussion
~~~~~~~~~~

Most Linux distributions do not automatically open firewall ports when you
install a service — and that's the right default from a security
perspective. But it means that after installing httpd, your first test from
another machine will fail silently until you allow the traffic through.

If you're testing locally (``curl http://localhost/``), the firewall won't
be an issue because loopback traffic bypasses it. The problem only appears
when you try to reach the server from a different host.

On cloud instances (EC2, GCE, Azure VMs), you'll also need to open ports
80/443 in the cloud provider's security group or network ACL — the OS
firewall and the cloud firewall are independent layers.

On macOS, the built-in firewall is off by default. If you've enabled it
(System Settings → Network → Firewall), you'll be prompted to allow
incoming connections when httpd starts for the first time.


.. _Recipe_Starting_stopping:

Starting, stopping, and restarting httpd
----------------------------------------

.. index:: Starting

.. index:: Stopping

.. index:: Restarting

.. index:: apachectl

.. index:: apache2ctl

.. index:: Commands,apachectl

.. index:: Commands,apache2ctl


.. _Problem_Starting_stopping:

Problem
~~~~~~~


You want to be able to start and stop the server at need, using
the appropriate tools.


.. _Solution_Starting_stopping:

Solution
~~~~~~~~


On Unixish systems, including Linux and macOS, use the **apachectl** script.
On Microsoft Windows, there will usually be items in the start menu
for controlling the server, but the exact nature and layout of those
tools will vary from one packaging to another.


.. tip::

   Some third-party distributions of Apache httpd rename the **apachectl**
   script to something else, such as **apache2ctl**, or **apache**.


.. _Discussion_Starting_stopping:

Discussion
~~~~~~~~~~


The basic httpd package includes tools to make it easy to
control the server. For Unixish systems, this is usually a script
called **apachectl**, but prepackaged
distributions may replace or rename it. For example, on
Ubuntu, it is named **apache2ctl**. It can only perform one action
at a time, and the action is specified by the argument on the command
line. The options of interest are:

``apachectl start``
        This will start the server if it isn't already running. If
        it **is** running, this option has no effect
        and may produce a warning message.

.. note::

   On first start, you may see the warning::

      AH00558: httpd: Could not reliably determine the server's fully
      qualified domain name

   This is harmless — httpd has started successfully despite the warning.
   To silence it, add ``ServerName localhost`` (or your actual hostname)
   to your configuration file.
   For detailed information about this and every other ``AH#####`` error
   code, see https://httpd.rcbowen.com/errors/.


``apachectl graceful``
        This option causes the server to reload its configuration
        files and gracefully restart its operation. Any current
        connections in progress are allowed to complete. The server will
        be started if it isn't running.


``apachectl restart``
        Like the graceful option, this one makes
        the server reload its configuration files. However, existing
        connections are terminated immediately. If the server isn't
        running, this command will
        try to start it.


``apachectl stop``
        This shuts the server down immediately. Any existing
        connections are terminated at once.

``apachectl graceful-stop``
        This option causes the server to shut down, but any current
        connections in progress are allowed to complete. This is
        useful in gracefully removing a server from a balanced pool of
        servers without any clients being aware of it.

Finally, note that **apachectl** is just a script that passes arguments
to **httpd**, the main httpd binary. You may directly
invoke **httpd** with any of the above options using the ``-k`` flag
(**e.g.**, ``httpd -k restart``), and other options are also available.

.. note::

   If you built httpd from source, ``apachectl`` won't be in your
   ``$PATH`` by default — you'll need the full path (e.g.,
   ``/usr/local/apache2/bin/apachectl``). You can add the bin directory
   to your ``$PATH``, or simply use the full path each time.

   If you installed httpd from a **package** on a systemd-based Linux
   distribution, the preferred way to manage the service is with
   ``systemctl`` — for example, ``systemctl start httpd`` (or
   ``systemctl start apache2`` on Debian/Ubuntu). The ``apachectl``
   script may still be available, but on some distributions it simply
   calls ``systemctl`` under the hood.

Any time you modify the server-wide configuration files
(such as ``httpd.conf``), you must
restart the server for the changes to take effect.


**Verifying that it worked**: Once you've started the server, you can
verify that it's running by requesting a page from it. From the server
itself:

.. code-block:: text

   curl http://localhost/

If ``curl`` is not installed on your system, you can use
``wget -qO- http://localhost/`` instead, or simply open
``http://localhost/`` in a web browser on the same machine.

If all is well, you should see a short HTML page containing the text
"It works!" — this is the default placeholder page installed with httpd.
You can also open ``http://your-server-ip/`` in a browser from another
machine. If you can't connect remotely, check that your firewall
allows traffic on port 80 (see :ref:`Recipe_Opening_firewall`) and that no
other service is already bound to that port.


.. _See_Also_Starting_stopping:

See Also
~~~~~~~~


:ref:`Recipe_Starting_at_boot`


.. _Recipe_Starting_at_boot:

Starting httpd at boot
----------------------

.. index:: Starting,at boot


.. _Problem_Starting_at_boot:

Problem
~~~~~~~


You want your httpd to start automatically when your
system boots up.


.. _Solution_Starting_at_boot:

Solution
~~~~~~~~


Modern operating systems have facilities to start services on startup.
The exact mechanism for this will vary from one platform
to another, and may vary depending on the exact way you installed
httpd.

On Linux and macOS:

.. index:: RHEL,Starting at boot

.. index:: Fedora,Starting at boot

.. index:: chkconfig

.. index:: Commands,chkconfig

.. index:: systemctl

.. index:: Commands,systemctl

For RPM-based installations (Fedora, CentOS Stream, AlmaLinux, Rocky Linux, and RHEL), use the
**systemctl** utility to enable the service to start at boot:


.. code-block:: text

   % sudo systemctl enable httpd


.. index:: Debian,Starting at boot

.. index:: Ubuntu,Starting at boot

For Debian and Ubuntu, which also use systemd, you'll
use ``systemctl``:


.. code-block:: text

   % sudo systemctl enable apache2


On macOS, Apple's bundled httpd starts at boot automatically — no
action is needed. If you've previously disabled it and want to
re-enable it:


.. code-block:: text

   sudo launchctl bootstrap system /System/Library/LaunchDaemons/org.apache.httpd.plist

To disable it from starting at boot:

.. code-block:: text

   sudo launchctl bootout system/org.apache.httpd

.. note::

   Older documentation uses ``launchctl load -w`` — that syntax is
   deprecated on modern macOS and will produce errors.


.. _Discussion_Starting_at_boot:

Discussion
~~~~~~~~~~


The solutions provided here assume that you're using one of the most
commonly used services managers. On other Unix platforms, you may need
to edit scripts that control the server startup process, which
typically are stored in the directory **/etc/rc.d**, or the local startup
script, which is often named **/etc/rc.local**. Consult your operating
system's documentation for specifics.


.. _See_Also_Starting_at_boot:

See Also
~~~~~~~~


* :ref:`Recipe_Build_from_source`
          
* :ref:`Recipe_Starting_stopping`
          

.. _Recipe_config.nice:

Upgrading using config.nice
---------------------------

.. index:: config.nice

.. index:: Upgrading using config.nice


.. _Problem_config.nice:

Problem
~~~~~~~


You built your httpd software from the source, and
now you want to upgrade it while keeping all the same configuration
options.


.. _Solution_config.nice:

Solution
~~~~~~~~


Unpack the source of the new version into a separate tree, and
execute the **config.nice** script
created by your build of the earlier version.


.. warning::

   This technique is primarily intended for use when upgrading
   within the same major version series, such as from 2.4.58 to 2.4.67.


For example, suppose you built and installed version 2.4.58 long
ago, and you now want to upgrade your system to 2.4.67. Assume
you've just downloaded the source tar file, and saved it in
``/tmp``.


.. code-block:: text

   % tar vzxf /tmp/httpd-2.4.67.tar.gz
   % cd httpd-2.4.67
   % sudo /path/to/httpd-2.4.58/config.nice
   % sudo make


.. _Discussion_config.nice:

Discussion
~~~~~~~~~~


When you execute the **configure** script to set up your compilation
and installation preferences, it creates a file called
**config.nice** with all the options you chose. 
Running this script executes **configure** with all those
options. This means you don't need to remember or write down all the
options you specified when you got things working the way that
you liked.

In addition, **config.nice**
allows you to specify additional options, which it adds to those with
which it invokes **configure**. When **configure** runs, it will create
**config.nice** again with the complete new set of options. For
example, if you wanted to rebuild with the same set of options,
but with a different name for the resulting executable:


.. code-block:: text

   % sudo ./config.nice --with-program-name='apache24'


.. _See_Also_config.nice:

See Also
~~~~~~~~


* :ref:`Recipe_Build_from_source`

.. refcosplay



.. _Recipe_Where_are_my_files:

Where are my files
------------------

.. index:: File locations

.. index:: File layout

.. index:: Layout

.. index:: Where are my files


.. _Problem_Where_are_my_files:

Problem
~~~~~~~


You've installed httpd, whether from source or
an installation kit, but you're not sure where all the files have been
put.


.. _Solution_Where_are_my_files:

Solution
~~~~~~~~


If you installed from source, the directory layout will be determined
by the **--enable-layout** argument that you provided to the
**configure** script. If you did not specify such an argument, then
the **Apache** (default) layout - usually **/usr/local/apache2** -
will have been used.

Note that a source-built installation does **not** place binaries in
your system ``$PATH``. You'll find ``httpd``, ``apachectl``, and other
tools under the ``bin/`` directory of your prefix — e.g.,
``/usr/local/apache2/bin/httpd``.

These layouts are defined in the file **config.layout**, which is in the
top level of the source directory. Look for a ``<Layout>``
stanza that matches the layout specified. This will define where
your files have been placed.

On the other hand, if you installed via a package, the location of the
files will have been determined by whoever built that package. You
can generally find the typical directory layout defined in the
Apache httpd wiki at 
https://cwiki.apache.org/confluence/display/httpd/DistrosDefaultLayout


.. _Discussion_Where_are_my_files:

Discussion
~~~~~~~~~~


One of the significant difference between one OS or distribution and
another is where they choose to put files. Thus, the location of the
Apache httpd files will vary from one OS to another, and from one
installation method to another.

If you installed httpd from source, you specified where the files
would be put, as part of the configuration options. There are two
main ways to do this.

You might have specified a **--with-prefix** argument, in which case all
of the various directories will have been created under that prefix
directory. For example, if you specified **--with-prefix=/usr/www**,
then configuration files will be placed in **/usr/www/conf**, binaries
in **/usr/www/bin**, and so on.

However, since there are a number of generally-accepted
"best-practice" directory layouts that large numbers of people agree
on, these layouts are defined in a file called **config.layout**, and
you can choose one of them when you build the server, using the
``--enable-layout`` option. Looking at the **config.layout** file is very
instructive.

For example, if you were to specify **--enable-layout=Apache** at
configure time, it would have been installed using the **Apache** layout
specified in **config.layout**, which looks like:


.. code-block:: text

   #   Classical Apache path layout.
   <Layout Apache>
       prefix:        /usr/local/apache2
       exec_prefix:   ${prefix}
       bindir:        ${exec_prefix}/bin
       sbindir:       ${exec_prefix}/bin
       libdir:        ${exec_prefix}/lib
       libexecdir:    ${exec_prefix}/modules
       mandir:        ${prefix}/man
       sysconfdir:    ${prefix}/conf
       datadir:       ${prefix}
       installbuilddir: ${datadir}/build
       errordir:      ${datadir}/error
       iconsdir:      ${datadir}/icons
       htdocsdir:     ${datadir}/htdocs
       manualdir:     ${datadir}/manual
       cgidir:        ${datadir}/cgi-bin
       includedir:    ${prefix}/include
       localstatedir: ${prefix}
       runtimedir:    ${localstatedir}/logs
       logfiledir:    ${localstatedir}/logs
       proxycachedir: ${localstatedir}/proxy
   </Layout>


Other layouts defined in in **config.layout** include 'RedHat',
'OpenBSD', 'Debian', and so on, allowing you to specify a file layout
that most closely matches your preferred norms.

If you installed the software from an RPM package, use the
-ql option to see where the files have been
installed:


.. code-block:: text

   dnf repoquery -l httpd

or equivalently, using ``rpm`` directly:

.. code-block:: text

   rpm -ql httpd

If you installed the server using **apt-get** (**i.e.**, on Debian or
Ubuntu), you can get a list of file location using:


.. code-block:: text

   % apt-file list apache2


If you installed using some other packaging mechanism, you'll need to
check with the distribution documentation to find out where
the files are stored.

Finally, if you're unsure how the server was installed, you can
determine some information about where things were installed (as well
as other details of how it was built) using the **-V** argument to
**httpd**.


.. code-block:: text

   $ /usr/local/apache2/bin/httpd -V
   Server version: Apache/2.4.67 (Unix)
   Server built:   May  9 2026 18:00:25
   Server's Module Magic Number: 20120211:142
   Server loaded:  APR 2.0.0-dev, PCRE 10.44 2024-06-07
   Compiled using: APR 2.0.0-dev, PCRE 10.44 2024-06-07
   Architecture:   64-bit
   Server MPM:     event
     threaded:     yes (fixed thread count)
       forked:     yes (variable process count)
   Server compiled with....
    -D APR_HAS_SENDFILE
    -D APR_HAS_MMAP
    -D APR_HAVE_IPV6 (IPv4-mapped addresses enabled)
    -D APR_USE_PROC_PTHREAD_SERIALIZE
    -D APR_USE_PTHREAD_SERIALIZE
    -D SINGLE_LISTEN_UNSERIALIZED_ACCEPT
    -D APR_HAS_OTHER_CHILD
    -D AP_HAVE_RELIABLE_PIPED_LOGS
    -D DYNAMIC_MODULE_LIMIT=256
    -D HTTPD_ROOT="/usr/local/apache2"
    -D SUEXEC_BIN="/usr/local/apache2/bin/suexec"
    -D DEFAULT_PIDLOG="logs/httpd.pid"
    -D DEFAULT_SCOREBOARD="logs/apache_runtime_status"
    -D DEFAULT_ERRORLOG="logs/error_log"
    -D AP_TYPES_CONFIG_FILE="conf/mime.types"
    -D SERVER_CONFIG_FILE="conf/httpd.conf"


.. tip::

   Remember that the **httpd** binary may be called different things, such
   as **apache**, or **apache2**, on different installations.


In the above output, note that the server root (``HTTPD_ROOT``) is
``/usr/local/apache2``, and other file paths (e.g., ``SERVER_CONFIG_FILE``) are
expressed as file paths relative to that location. Thus, the main
server configuration file, on this particular system, is at
``/usr/local/apache2/conf/httpd.conf``.

One of the advantages—and disadvantages—of open software is that
everyone can build an installation kit. And everyone pretty much
chooses options different from everyone else.


.. _See_Also_Where_are_my_files:

See Also
~~~~~~~~


* https://httpd.apache.org/docs/programs/configure.html

.. _Recipe_docker:

Running httpd in a Docker container
-----------------------------------

.. index:: Docker
.. index:: Container
.. index:: httpd Docker image

.. _Problem_Recipe_docker:

Problem
~~~~~~~


You want to run Apache httpd inside a Docker container for easy deployment and reproducibility.


.. _Solution_Recipe_docker:

Solution
~~~~~~~~


.. note::

   This recipe assumes Docker is already installed. If ``docker`` is not
   available on your system, see https://docs.docker.com/engine/install/.
   On RHEL-based systems (AlmaLinux, Fedora, CentOS Stream), Podman is
   available as a drop-in replacement:
   ``sudo dnf install podman-docker``.

Use the official ``httpd`` Docker image from Docker Hub. The simplest
approach is to run the image directly, mounting your local content
into the container:

.. code-block:: bash

   $ docker run -d --name my-httpd -p 8080:80 \
       -v /path/to/your/site:/usr/local/apache2/htdocs/:ro \
       httpd:2.4

For a more reproducible setup, create a :file:`Dockerfile` that copies
your content and configuration into the image:

.. code-block:: text

   FROM httpd:2.4
   COPY ./my-site/ /usr/local/apache2/htdocs/
   COPY ./my-httpd.conf /usr/local/apache2/conf/httpd.conf

Build and run it:

.. code-block:: bash

   $ docker build -t my-httpd-app .
   $ docker run -d --name my-httpd -p 8080:80 my-httpd-app


.. _Discussion_Recipe_docker:

Discussion
~~~~~~~~~~


The official ``httpd`` image on Docker Hub
(https://hub.docker.com/_/httpd) is maintained by the Docker
community and provides a minimal Apache httpd installation based on
Debian. It's available in several variants:

- ``httpd:2.4`` — the current stable release, updated with each new
  2.4.x point release. This is the tag you should use.
- ``httpd:2.4-alpine`` — a smaller image based on Alpine Linux,
  useful when image size matters.

**Volume mounts.** The ``-v`` flag in the ``docker run`` command
mounts a host directory into the container. The ``:ro`` suffix makes
the mount read-only, which is good practice for serving static
content. The key paths inside the container are:

- :file:`/usr/local/apache2/htdocs/` — the ``DocumentRoot``
- :file:`/usr/local/apache2/conf/httpd.conf` — the main
  configuration file
- :file:`/usr/local/apache2/conf/extra/` — supplemental
  configuration files (SSL, virtual hosts, etc.)
- :file:`/usr/local/apache2/logs/` — log files

**Custom configuration.** To start with the default configuration
and customize it, first extract the file from a running container:

.. code-block:: bash

   $ docker run --rm httpd:2.4 cat /usr/local/apache2/conf/httpd.conf \
       > my-httpd.conf

Edit that file locally, then copy it into your image via the
:file:`Dockerfile` or mount it at runtime.

**SSL/TLS.** For HTTPS, you'll need to uncomment the SSL
lines in the configuration file and mount your certificates into the
container. See :ref:`Chapter_SSL_and_TLS` for details on configuring
SSL.

**Logging.** By default, the official image sends access and error
logs to ``stdout`` and ``stderr``, which makes them accessible via
``docker logs``. If you need file-based logs for tools that
parse them, mount a volume on :file:`/usr/local/apache2/logs/`.


.. _See_Also_Recipe_docker:

See Also
~~~~~~~~


* https://hub.docker.com/_/httpd



.. _Recipe_systemd_integration:

Integrating httpd with systemd
-------------------------------

.. index:: mod_systemd

.. index:: systemd

.. index:: systemctl

.. index:: journalctl

.. index:: sd_notify

.. index:: Commands,systemctl

.. index:: Commands,journalctl


.. _Problem_systemd_integration:

Problem
~~~~~~~


You are running httpd on a modern Linux distribution that uses
systemd, and you want proper integration -- reliable startup
notification, clean shutdown behavior, status reporting, and
journal-based logging.


.. _Solution_systemd_integration:

Solution
~~~~~~~~


Load :module:`mod_systemd` in your server configuration:

.. code-block:: apache

   LoadModule systemd_module modules/mod_systemd.so

Then define a systemd service unit file. On most distributions that
ship httpd as a package, this file is already provided. If you built
from source, create the file
:file:`/etc/systemd/system/httpd.service`:

.. code-block:: text

   [Unit]
   Description=The Apache HTTP Server
   After=network.target

   [Service]
   Type=notify
   ExecStart=/usr/local/apache2/bin/httpd -D FOREGROUND -k start
   ExecReload=/usr/local/apache2/bin/httpd -k graceful
   KillMode=mixed

   [Install]
   WantedBy=multi-user.target

After creating or modifying the unit file, reload the systemd
daemon so that it picks up the changes:

.. code-block:: bash

   sudo systemctl daemon-reload

You can now manage the server with ``systemctl``:

.. code-block:: bash

   sudo systemctl start httpd
   sudo systemctl stop httpd
   sudo systemctl reload httpd
   sudo systemctl restart httpd
   sudo systemctl status httpd

Enable the service to start automatically at boot:

.. code-block:: bash

   sudo systemctl enable httpd

And view server log output via the journal:

.. code-block:: bash

   journalctl -u httpd
   journalctl -u httpd -f


.. _Discussion_systemd_integration:

Discussion
~~~~~~~~~~


The :module:`mod_systemd` module was contributed by Red Hat and
provides the integration layer between httpd and systemd, using the
``sd_notify`` protocol to communicate process state. On Fedora, RHEL,
CentOS Stream, AlmaLinux, and Rocky Linux, mod_systemd is loaded by
default -- the httpd RPM package ships with
:file:`/etc/httpd/conf.modules.d/00-systemd.conf`, and the
``httpd.service`` unit file is configured with ``Type=notify`` to take
advantage of it. If you install httpd from packages on any of these
distributions, this integration is already in place and working.

Debian and Ubuntu, by contrast, do **not** use mod_systemd. Their
``apache2.service`` unit file uses ``Type=forking`` instead, and
manages the lifecycle differently. The recipes in this section apply
primarily to RPM-based distributions; if you are on Debian/Ubuntu,
the ``systemctl`` commands still work, but the underlying mechanism
is different.

On any distribution that uses systemd as its init system -- which is
nearly all of them at this point -- you can enable mod_systemd
yourself if it is not already loaded.

**How sd_notify works**

When httpd is managed by systemd with ``Type=notify``, systemd does
not consider the service "started" until the process explicitly
signals readiness via the ``sd_notify`` protocol. Without
:module:`mod_systemd`, systemd has no way to know when httpd has
finished initialization and is actually ready to serve requests. The
module sends this readiness notification, as well as ongoing status
updates, so that ``systemctl status`` can display useful information
about the running server.

**The unit file explained**

Several settings in the unit file deserve attention:

``Type=notify``
Tells systemd to wait for an ``sd_notify`` readiness signal from
the service before marking it as active. This is what
:module:`mod_systemd` provides.

``ExecStart=/usr/local/apache2/bin/httpd -D FOREGROUND -k start``
Runs httpd in the foreground so that systemd can directly track the
main process. Adjust the path to match your installation -- on
RPM-based distributions, this is typically
:file:`/usr/sbin/httpd`; on Debian/Ubuntu, it is
:file:`/usr/sbin/apache2`.

``ExecReload=/usr/local/apache2/bin/httpd -k graceful``
Maps ``systemctl reload`` to a graceful restart. This causes
httpd to re-read its configuration files while allowing in-flight
requests to complete before child processes are replaced. Again,
adjust the path to match your installation.

``KillMode=mixed``
When stopping the service, systemd sends ``SIGTERM`` to the main
(parent) process only. If child processes are still running after
the configured ``TimeoutStopSec`` elapses, systemd sends
``SIGKILL`` to the entire process group. This allows httpd's parent
process to coordinate an orderly shutdown of its children, falling
back to a forceful kill only if something is stuck.

**systemctl commands and how they map to httpd signals**

If you have been managing httpd with ``apachectl`` or direct signals
(see :ref:`Recipe_Starting_stopping`), the ``systemctl`` equivalents
are straightforward:

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - systemctl command
     - Signal / action
     - Behavior
   * - ``systemctl start httpd``
     - Starts the httpd process
     - Equivalent to ``apachectl start``. systemd waits for the
       ``sd_notify`` readiness signal before reporting the service
       as active.
   * - ``systemctl stop httpd``
     - ``SIGTERM`` (via ``KillMode=mixed``)
     - Sends ``SIGTERM`` to the parent process, which then
       terminates its children. Equivalent to ``apachectl stop``.
   * - ``systemctl reload httpd``
     - Runs ``ExecReload`` (graceful restart)
     - Re-reads configuration; in-flight requests complete
       normally. Equivalent to ``apachectl graceful``.
   * - ``systemctl restart httpd``
     - Full stop then start
     - Terminates all processes and starts fresh. Equivalent to
       ``apachectl stop`` followed by ``apachectl start``. All
       in-flight connections are dropped.

The distinction between ``systemctl reload`` and ``systemctl restart``
is important in production. A **reload** performs a graceful restart --
children finish their current requests before exiting, and new
children are spawned with the updated configuration. There is no
interruption of service for clients. A **restart**, on the other hand,
fully stops and then starts the server, which means a brief window
during which the server is not listening and all active connections
are terminated. Prefer ``systemctl reload`` whenever you have changed
configuration and want to apply it without downtime.

**Journal integration**

When httpd runs under systemd, its standard output and standard error
are captured by the systemd journal. You can view the logs with
``journalctl``:

.. code-block:: bash

   # Show all httpd log entries
   journalctl -u httpd

   # Follow logs in real time (like tail -f)
   journalctl -u httpd -f

   # Show logs since the last boot
   journalctl -u httpd -b

   # Show logs from the last hour
   journalctl -u httpd --since "1 hour ago"

This is in addition to -- not a replacement for -- the log files
configured with ``ErrorLog`` and ``CustomLog`` in your httpd
configuration. The journal captures startup and shutdown messages,
module loading errors, and anything written to stderr, which can be
especially useful for diagnosing problems that occur before httpd has
finished initializing and opened its own log files.

**ExtendedStatus and server-status**

Loading :module:`mod_systemd` automatically enables
``ExtendedStatus``, which causes httpd to track detailed per-request
statistics in the scoreboard. These statistics are what make the
output of :module:`mod_status` (the ``server-status`` handler) useful.
If you explicitly set ``ExtendedStatus Off`` in your configuration,
the status information reported by :module:`mod_systemd` to systemd
will be limited.

**A note on Debian and Ubuntu**

On Debian-based distributions, the service name is ``apache2`` rather
than ``httpd``, and the unit file is
:file:`/lib/systemd/system/apache2.service`. The ``systemctl``
commands are the same, substituting ``apache2`` for ``httpd``:

.. code-block:: bash

   sudo systemctl reload apache2
   journalctl -u apache2

**Socket activation**

Note that :module:`mod_systemd` does **not** provide support for
systemd socket activation. The server manages its own listening
sockets via the ``Listen`` directive.


.. _See_Also_systemd_integration:

See Also
~~~~~~~~


* :ref:`Recipe_Starting_stopping`

* :ref:`Recipe_Starting_at_boot`

* https://httpd.apache.org/docs/2.4/mod/mod_systemd.html

* https://httpd.apache.org/docs/2.4/stopping.html

* ``httpd.service(8)`` man page (Fedora/RHEL):
  https://www.mankier.com/8/httpd.service — comprehensive reference
  for systemd integration, socket activation, SELinux, and more.

* Fedora Quick Docs — Getting started with Apache HTTP Server:
  https://docs.fedoraproject.org/en-US/quick-docs/getting-started-with-apache-http-server/

* ``man systemctl``

* ``man journalctl``


Summary
-------


There are, as you have seen in this chapter, a number of different
ways you might choose to install Apache httpd. This presents
difficulties througout the rest of the book - and in adminstering the
httpd in general - because different installations have
different files in different places. Scripts, configuration files, and
binary programs may be called different things from one system to
another. This can make it difficult to follow instructions, without
first determining what these differences are.

Don't worry, you'll figure this out pretty quickly. You'll learn to
substitute ``apache.conf`` for ``httpd.conf`` and ``/etc/httpd`` for
``/usr/local/apache`` in your mind as you read.

Much like your website is unique, your installation of your web server
is going to be unique. Put things where they make the most sense to
you, and document these decisions for the people that will follow
after you.
