
.. _Chapter_Security:

========
Security
========

.. epigraph::

   Just because you're paranoid don't mean they're not after you.

   -- Nirvana, *Territorial Pissings*


.. index:: Security


The Internet is a hostile place. From "script kiddies" who are playing
games and trying to score points by compromising servers, to serious
attackers who are trying to steal your corporate data, there are many
people constantly trying to attack your server.

While some of these attacks are directed - that is, specific attacks
against your server in order to accomplish some specific goal - most
of them are random "shotgun" attacks attempting to find servers that
have common exploits available.

In either case, there are many things that you can do to reduce the
risk of being compromised.

This is **not** a comprehensive coverage of server security. For that,
I strongly recommend that you obtain one of the excellent books that
are available covering the topic of web server security. Several that
I recommend include Ivan Ristic's 'ModSecurity Handbook', Dafydd
Stuttard's 'The Web Application Hacker's Handbook', and Chris
Shifflett's 'Essential PHP Security'. This last one, although the
title indicates that it's specifically about PHP, covers the general
classes of web application exploits in some detail, so while the
examples are in PHP, the concepts are universal.

However, in the context of securing your Apache HTTP Server, there are
a number of things that you must get right up front, or else
everything else is just going to be shutting the barn door after the
horse has already left.

The most important measure that you can take is to keep apprised of
new releases, and read the ``CHANGES`` file
to determine if the new version fixes a security hole to which you may be
subject. Running the latest version of the Apache httpd is usually a good
measure in the fight against
security vulnerabilities.

// TODO - Move recipes from ch02.asciidoc - the AAA chapter.

// TODO: Recipes:
//
// http://www.petefreitag.com/item/505.cfm
//
// ServerSignature
// User and Group

// Don't expose the file tree


.. _Restricting_Access_to_Files_Outside_Your_Web_Root_id137175:

Restricting Access to Files Outside Your Web Root
-------------------------------------------------

.. index:: Restrict access outside of web root

.. index:: Require

.. index:: Allow

.. index:: Deny

.. index:: Order


.. _Problem_id137190:

Problem
~~~~~~~


You want to make sure that files outside of your Web directory
are not accessible.


.. _Solution_id137224:

Solution
~~~~~~~~


For Unix systems, running httpd 2.4 and later:


.. code-block:: text

   <Directory />
      Require all denied
   </Directory>


For Microsoft Windows systems:


.. code-block:: text

   <Directory C:/>
       Require all denied
   </Directory>


Repeat for each drive letter on the system.


.. _Discussion_id137267:

Discussion
~~~~~~~~~~


Good security technique is to deny access to everything, and
then selectively permit access where it is needed. By placing a
``Require all denied`` directive on the entire filesystem, you ensure that files cannot be
loaded from any part of your filesystem unless you explicitly permit
it, using a ``Require all granted`` directive applied to some other ``<Directory>`` section in your
configuration.

For example:


.. code-block:: text

   <Directory />
       Require all denied
   </Directory>
   
   DocumentRoot /var/www/htdocs
   <Directory /var/www/htdocs>
       Require all granted
   </Directory>


If you want to create an **Alias** to some other section of your
filesystem, you will need to explicitly permit this with the
following:


.. code-block:: text

   Alias /example /var/example
   <Directory /var/example>
       Require all granted
   </Directory>


.. _See_Also_id137382:


See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_access.html


.. _Limiting_Methods_by_User_id137414:

Limiting Methods by User
------------------------

.. index:: Limit

.. index:: LimitExcept

.. index:: RequireAny

.. index:: Require,method

.. index:: Require,valid-user

.. index:: Restrict access by HTTP method


.. _Problem_id137428:

Problem
~~~~~~~


You want to allow some users to use certain methods but prevent
their use by others. For instance, you wish authenticated users to be
able to access content using any HTTP method, but unauthenticated
users only to be able to use the **GET** method.


.. _Solution_id137472:

Solution
~~~~~~~~


For httpd 2.4 and later, use a RequireAny block to restrict the method
that may be used for unauthenticated users:


.. code-block:: text

   AuthName "Restricted Access"
   AuthType Basic
   AuthUserFile /etc/httpd/authusers
   
   <RequireAny>
       Require valid-user
       Require method GET
   </RequireAny>


.. _Discussion_id137530:


Discussion
~~~~~~~~~~


It is often desirable to give general access to one or more HTTP
        methods, while restricting
        others. For example, although you may wish any user to be able to
        ``GET`` certain documents, you may wish
        for only site administrators to ``POST`` data back to those documents.

It is important to use the **LimitExcept** directive, rather than
        attempting to enumerate all possible methods, as you're likely to miss
        one.


.. _See_Also_id137594:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_auth.html


          
* http://httpd.apache.org/docs/mod/mod_access.html


          
* http://httpd.apache.org/docs/mod/core.html#limit


          
* http://httpd.apache.org/docs/mod/core.html#limitexcept


// TODO - Recipes

// -Indexes
// -Includes
// -FollowSymLinks, SymlinksIfOwnerMatch
// Turn off negotiation
// Turn off .htaccess files

// Disable unnecessary modules
// TODO: Review. This is probably all wrong now.

.. _Running_a_Minimal_Module_Set_id136520:

Running a Minimal Module Set
----------------------------


.. _Problem_id136534:

Problem
~~~~~~~


You want to eliminate all modules that you don't need in order
        to reduce the potential exposure to security holes. What modules do
        you really need?


.. _Solution_id136573:

Solution
~~~~~~~~


If you are building from source, you can individually disable modules
you don't need:


.. code-block:: bash

   % ./configure --disable-access \
   > --disable-auth --disable-charset-lite \
   > --disable-include --disable-log-config --disable-env --disable-setenvif \
   > --disable-mime --disable-status --disable-autoindex --disable-asis \
   > --disable-cgid --disable-cgi --disable-negotiation --disable-dir \
   > --disable-imap --disable-actions --disable-alias --disable-userdir

You may wish to leave ``mod_dir``, **mod_mime**, and ``mod_log_config``
enabled, as they are recommended for a functional server.


.. _Discussion_id136662:

Discussion
~~~~~~~~~~


A frequent security recommendation is that you eliminate
        everything that you don't need; if you don't need something and don't
        use it, then you are likely to overlook security announcements about
        it or forget to configure it securely. The question that is less
        frequently answered is exactly what you do and don't need.

A number of httpd package distributions come with everything
        enabled, and people end up running modules that they don't really
        need—or perhaps are not even aware that they are running.

This recipe is an attempt to get to the very smallest httpd
        possible, reducing it to the minimum set of modules that httpd
        will run. That is, if you take any of these out, httpd will not even
        start up, let alone serve a functional Web site.


The three modules that are most recommended for a functional server are:

``mod_dir`` takes a request for **/** and turns it into a request for
**/index.html**, or whatever other file you have indicated with the
**DirectoryIndex** directive as the default document for a directory.
Without this module, users typing just your hostname into their browser
will get a 404 error rather than a default document.

``mod_mime`` enables httpd to determine the MIME type of a particular file
and send the appropriate header, enabling the browser to render the file
correctly. Without ``mod_mime``, your Web server will treat **all** files
as having the MIME type set by the **DefaultType** directive.

``mod_log_config``, while not technically required, is highly recommended.
Running your Web server without any activity logfiles will leave you
without any idea of how your site is being used. Note that it is not
possible to disable the **ErrorLog** functionality, so you will always
have error log information.


.. tip::

   The default distributed configuration file will need some
   adjustment to run under these reduced conditions. Many sections
   of the configuration files are protected by **<IfModule>** sections
   and will still function in the absence of the required modules.


.. _See_Also_new2:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_dir.html
          
* http://httpd.apache.org/docs/mod/mod_mime.html
          
* http://httpd.apache.org/docs/mod/mod_log_config.html

// TODO - Recipes
// Reduce Timeout
// Use event mpm to block Slowloris
// Limit large requests
// Block problematic IP addresses
// Using mod_security to block spam posts
// Keepalive recommendations


.. admonition:: DRAFT — Review needed

   The following recipe was auto-generated and needs editorial review.
   Check technical accuracy, voice/tone, and fit with surrounding content.

.. _Recipe_mod_security_recipes:

mod_security_recipes
--------------------

.. index:: mod_security
.. index:: ModSecurity
.. index:: Web application firewall
.. index:: WAF
.. index:: OWASP Core Rule Set


.. _Problem_mod_security_recipes:

Problem
~~~~~~~


You want to add a web application firewall (WAF) to Apache httpd so
that you can inspect incoming requests and block common attacks such as
SQL injection, cross-site scripting (XSS), and remote code execution.


.. _Solution_mod_security_recipes:

Solution
~~~~~~~~


Install ModSecurity (``mod_security2``) and the OWASP Core Rule Set
(CRS). On Debian/Ubuntu:

.. code-block:: bash

   $ sudo apt-get install libapache2-mod-security2
   $ sudo a2enmod security2

On RHEL/Fedora/CentOS:

.. code-block:: bash

   $ sudo dnf install mod_security mod_security_crs

Copy the recommended configuration and activate it:

.. code-block:: bash

   $ sudo cp /etc/modsecurity/modsecurity.conf-recommended \
        /etc/modsecurity/modsecurity.conf

Edit :file:`/etc/modsecurity/modsecurity.conf` and change the engine
from detection-only to active blocking:

.. code-block:: apache

   SecRuleEngine On

Then include the OWASP Core Rule Set. A typical
:file:`/etc/apache2/mods-enabled/security2.conf` looks like:

.. code-block:: apache

   <IfModule security2_module>
       IncludeOptional /etc/modsecurity/modsecurity.conf
       IncludeOptional /usr/share/modsecurity-crs/crs-setup.conf
       IncludeOptional /usr/share/modsecurity-crs/rules/*.conf
   </IfModule>

Restart httpd:

.. code-block:: bash

   $ sudo apachectl graceful


.. _Discussion_mod_security_recipes:

Discussion
~~~~~~~~~~


ModSecurity operates as an embedded WAF inside httpd, inspecting every
request and response against a set of rules. The OWASP Core Rule Set
(CRS) provides a maintained collection of generic attack-detection
rules that cover the OWASP Top 10 vulnerability categories.

**Detection vs. blocking**

The ``SecRuleEngine`` directive has three modes:

``DetectionOnly``
    Logs rule matches but doesn't block requests. Use this when first
    deploying ModSecurity so you can tune rules before enforcing them.

``On``
    Actively blocks requests that trigger rules. Deploy this after
    you've reviewed your audit log and resolved false positives.

``Off``
    Disables the engine entirely.

**Tuning false positives**

The audit log (controlled by ``SecAuditLog``) is your primary tool
for identifying false positives. When a legitimate request is
blocked, note the rule ID from the log and add an exclusion:

.. code-block:: apache

   # Exclude rule 941100 from /api/submit (false positive on JSON body)
   <Location /api/submit>
       SecRuleRemoveById 941100
   </Location>

You can also adjust the CRS paranoia level in
:file:`crs-setup.conf`—level 1 (default) catches the most obvious
attacks with few false positives; level 4 is the most aggressive.

**Verifying the installation**

Confirm that ModSecurity is loaded and actively processing requests:

.. code-block:: bash

   $ curl -I 'http://localhost/?param="><script>alert(1)</script>'

If the engine is on, you should receive a ``403 Forbidden`` response.
Check the ModSecurity audit log for the matching rule entry.

.. tip::

   Always deploy in ``DetectionOnly`` mode first on a production
   server. Review the audit log for at least a few days before
   switching to ``On``.


.. _See_Also_mod_security_recipes:

See Also
~~~~~~~~


* https://modsecurity.org

* https://coreruleset.org — the OWASP Core Rule Set project

* Ivan Ristić, *ModSecurity Handbook* — the definitive guide to
  ModSecurity configuration and rule writing


.. admonition:: DRAFT — Review needed

   The following recipe was auto-generated and needs editorial review.
   Check technical accuracy, voice/tone, and fit with surrounding content.

.. _I_sect16_d1e12260:

Chrooting httpd with mod_security
---------------------------------

.. index:: chroot
.. index:: SecChrootDir
.. index:: mod_security,chroot


.. _Problem_chroot_modsecurity:

Problem
~~~~~~~


You want to confine httpd to an isolated portion of the filesystem so
that even if an attacker exploits a vulnerability, they cannot access
files outside the jail.


.. _Solution_chroot_modsecurity:

Solution
~~~~~~~~


Install ModSecurity (see :ref:`Recipe_mod_security_recipes`) and add a
single directive to your configuration:

.. code-block:: apache

   SecChrootDir /chroot/apache

Create the chroot directory and ensure it contains the document root
and any files that the child processes need at runtime:

.. code-block:: bash

   $ sudo mkdir -p /chroot/apache/var/www/htdocs
   $ sudo cp -a /var/www/htdocs/* /chroot/apache/var/www/htdocs/

Restart httpd:

.. code-block:: bash

   $ sudo apachectl graceful

After the restart, the child processes see :file:`/chroot/apache` as
their root filesystem. The ``DocumentRoot`` in your configuration
should be the path *inside* the jail—for example,
:file:`/var/www/htdocs`, not :file:`/chroot/apache/var/www/htdocs`.


.. _Discussion_chroot_modsecurity:

Discussion
~~~~~~~~~~


**chroot** is a Unix system call that
causes a process to see a replacement root filesystem. Any files
outside the new root are completely invisible to the confined process.
By jailing httpd this way, you limit the damage an attacker can do
even after a successful exploit—they can only reach files that exist
inside the jail.

The traditional trouble with chrooting httpd is the sheer
inconvenience. You must copy every shared library, configuration file,
and runtime dependency into the jail *before* starting the server. If
you're running :module:`mod_ssl`, you need the OpenSSL libraries. If
you have Perl CGI programs, you need Perl and all its modules.
Maintaining this parallel filesystem is tedious and error-prone.

``SecChrootDir`` elegantly sidesteps most of this pain. ModSecurity
performs the chroot *after* the parent process has loaded all modules
and libraries but *before* it forks the child worker processes. This
means:

- Shared libraries (OpenSSL, PCRE, etc.) are already mapped into
  memory and do not need to be present inside the jail.
- Only resources that the child processes access *at request time*
  must exist inside the jail—primarily document files, CGI scripts,
  and any external programs they invoke.
- :module:`mod_ssl`, :module:`mod_rewrite`, and other modules work
  without modification because they were loaded before the chroot.

The one limitation is that anything spawned by the child processes
(CGI scripts, piped loggers, external programs called by
``RewriteMap``) must have all of their dependencies present inside the
jail. For example, if you run a Python CGI script, the Python
interpreter and its standard library need to be copied into the
chroot tree.

.. tip::

   After enabling ``SecChrootDir``, test thoroughly. A common failure
   mode is a ``404 Not Found`` on every request because the
   ``DocumentRoot`` path doesn't exist relative to the new root. Use
   ``strace`` or ``truss`` on a child process to watch for failed
   ``open()`` calls if something isn't working.


.. _See_Also_chroot_modsecurity:

See Also
~~~~~~~~


* :ref:`Recipe_mod_security_recipes` — installing and configuring
  ModSecurity

* https://modsecurity.org


.. _I_sect16_d1e12429:

Blocking Worms with mod_security
--------------------------------

// TODO: Wow. This is terrible. How about a useful recipe here.

Problem
~~~~~~~


You want to use the ``mod_security`` third-party module to
intercept common probes before they actually reach your Web server's
pages.


Solution
~~~~~~~~


If you have ``mod_security``
installed (see :ref:`Recipe_mod_security`), then
you can use its basic 'core rules' accessory package to intercept many
of the most common attack and probe forms that hit Web servers. The
core rules package is periodically updated to keep pace with new
issues that appear on the Web.


Discussion
~~~~~~~~~~


Installing the core rules package and following the instructions
in the **README** file makes this
very simple. In addition, the files in the package make it easy to
write your own rules by illustrating the formats.


See Also
~~~~~~~~


* http://modsecurity.org/projects/rules


.. _Recipe_Securing_Logfiles:

Securing_Logfiles
-----------------

.. index:: Logging,Sensitive information

.. index:: Securing log files

.. index:: Logging,Securing log files


.. _Problem_Securing_Logfiles:

Problem
~~~~~~~


You have potentially sensitive information in your log files. How do
you ensure that it doesn't fall into the wrong hands?


.. _Solution_Securing_Logfiles:

Solution
~~~~~~~~


Don't log potentially sensitive information. If you must, delete or
encrypt these log files frequently.


.. _Discussion_Securing_Logfiles:

Discussion
~~~~~~~~~~


.. _See_Also_Securing_Logfiles:

See Also
~~~~~~~~


* :ref:`Recipe_Logging_POST`


.. _Recipe_File_permissions:

Setting Correct File Permissions
--------------------------------


.. _Problem_File_permissions:

Problem
~~~~~~~


You want to set file permissions to provide the maximum level of
security.


.. _Solution_File_permissions:

Solution
~~~~~~~~


The **bin** directory under the
        **ServerRoot** should be owned by user
        root, group root, and have file permissions of 755 (``rwxr-xr-x``). Files contained therein should
        also be owned by root.root and be mode 755.

Document directories, such as **htdocs**, **cgi-bin**, and **icons**, will have to have permissions set in
        a way that makes the most sense for the development model of your
        particular Web site, but under no circumstances should any of these
        directories or files contained in them be writable by the Web server
        user.


.. _apacheckbk-CHP-6-NOTE-101:


.. tip::

   The solution provided here is specific to Unixish systems.
   Users of other operating systems should adhere to the principles
   laid out here, although the
   actual implementation will vary.


The **conf** directory should
        be readable and writable only by root, as should all the files
        contained therein.

The **include** and **libexec** directories should be readable by
        everyone, writable by no one.

The **logs** directory should
        be owned and writable by root. You may, if you like, permit other
        users to read files in this directory, as it is often useful for users
        to be able to access their logfiles, particularly for troubleshooting
        purposes.

The **man** directory should be
        readable by all users.

Finally, the **proxy**
        directory should be owned by and writable by the server user.


.. _apacheckbk-CHP-6-NOTE-103:


.. tip::

   On most Unixish file systems, a **directory**
   must have the ``x`` bit set in order
   for the files therein to be visible.


.. _Discussion_File_permissions:

Discussion
~~~~~~~~~~


You should be aware that if you ask 12 people for the correct
ways to set file permissions on your httpd, you will get a
dozen different answers. The recommendations here are intended to be
as paranoid as possible. You should feel free to relax these
recommendations, based on your particular view of the world and how
much you trust your users. However, if you set file permissions any
more restrictive than this, your httpd is likely not to
function. There are, of course, exceptions to this, and cases in which
you could possibly be more paranoid are pointed out later.

The most important consideration when setting file permissions
is the httpd user—the user as which httpd runs. This is
configured with the **User** and
**Group** directives in your **httpd.conf** file, setting what user and
group the httpd processes will run as. This user needs to have read
access to nearly everything but should not have write access to
anything.

The recommended permissions for the **bin** directory permit anyone to run programs
contained therein. This is necessary in order for users to create
password files using the **htpasswd**
and **htdigest** utilities, run CGI
programs using the **suexec**
utility, check the version of httpd using **httpd** -v, or use any of the
other programs in this directory. There is no known security risk of
permitting this access. The Web server itself cannot be stopped or
started by an unprivileged user under normal conditions. These files,
or the directory, should never be writable by nonroot users, as this
would allow compromised files to be executed with root
privileges.

Extra-paranoid server administrators may wish to make the
**bin** directory and its contents
readable and executable only by root. However, the only real benefit
to doing so is that other users cannot run the utilities or **httpd** server, such as on a different port.
Some of those utilities, such as **htpasswd** and **htdigest**, are intended to be run by content
providers (**i.e.**, users) in addition to the Webmaster.

The **conf** directory,
containing the server configuration files, can be locked down as
tightly as you like. Although it is unlikely that reading the server
configuration files will allow a user to gain additional privileges on
the server, more information is always useful for someone trying to
compromise your server. You may, therefore, wish to make this
directory readable only by root. However, most people will consider
this just a little too paranoid.

Document directories are particularly problematic when it comes
to making permission recommendations, as the recommended setting will
vary from one server to another. On a server with only one content
provider, these directories should be owned by that user and readable
by the httpd user. On a server with more than one content developer,
the files should be owned by a group of users who can modify the files
but still be readable by the httpd user. The **icons** directory is a possible exception to
this rule, because the contents of that directory are rarely modified
and do not need to be writable by any users.

The **include** and **libexec** directories contain files that are
needed by the httpd executable at runtime and only need to be
readable by root, which starts as root, and by no other users.
However, since the **include**
directory contains C header files, it may occasionally be useful for
users to have access to those files to build applications that need
those files.

The **logs** directory should
under no circumstances ever be writable by anyone other than root. If
the directory is ever writable by another user, it is possible to gain
control of the httpd process at start time and gain root privileges
on the server. Whether you permit other users to read files in this
directory is up to you and is not required. However, on most servers,
it is very useful for users to be able to access the
logfiles—particularly the ``error_log`` file, in order to troubleshoot
problems without having to contact the server administrator.

The **man** directory contains
the manpages for the various utilities that come with httpd. These
need to be readable by all users. However, it is recommended that you
move them to the system **man** path,
or install them there when you install httpd by providing an argument
to the —mandir argument specifying the location of
your system **man**
directory.

Finally, the **proxy**
directory should be owned by, and writable by, the server user. This
is the only exception to the cardinal rule that nothing should be
writable by this user. The **proxy**
directory contains files created by and managed by ``mod_proxy``, and they need to be writable by
the unprivileged httpd processes. If you are not running a proxy
server with ``mod_proxy``, you may
remove this directory entirely.

// TODO: Use a find command to set file, directory permissions
// correctly.

viz:


.. code-block:: text

   find /home/bob/public_html -type d | xargs chmod o+rx
   find /home/bob/public_html -type f | xargs chmod o+r 


See also ch18.asciidoc, recipe :ref:`Discussion_UserDir` for overlap.


.. _See_Also_File_permissions:

See Also
~~~~~~~~


* Learning the Unix Operating System,
            Fifth Edition, by Jerry Peek, Grace Todino-Gonquet, and John
            Strang (O'Reilly)


          
* http://www.onlamp.com/pub/a/bsd/2000/09/06/FreeBSD_Basics.html


.. _Protecting_Server_Files_from_Malicious_Scripts_id135552:

Protecting Server Files from Malicious Scripts
----------------------------------------------


.. _Problem_id135567:

Problem
~~~~~~~


Scripts running on your Web server may access, modify, or
        destroy files located on your Web server if they are not adequately
        protected. You want to ensure that this cannot happen.


.. _Solution_id135616:

Solution
~~~~~~~~


Ensure that none of your files are writable by the ``nobody`` user or the ``nobody`` group, and that sensitive files are
        not readable by that user and group:


.. code-block:: text

   % sudo find / -user nobody
   & sudo find / -group nobody


.. _Discussion_id135656:

Discussion
~~~~~~~~~~


The **User** and **Group** directives specify a user and group
under whose privileges the Web server will run. These are often set to
the values of ``nobody`` and ``nobody``, respectively, but they can vary in
different setups. It is often advisable to create a completely new
user and group for this purpose, so that there is no chance that the
user has been given additional privileges of which you are not
aware.

Because everything runs with these privileges, any files or
directories that are accessible by this user and/or group will be
accessible from any script running on the server. This means that a
script running under one virtual host may possibly modify or delete
files contained within another virtual host, either intentionally or
accidentally, if those files have permissions making this
possible.

Ideally, no files anywhere on your server should be owned by, or
writable by, the server user, unless for the explicit purpose of being
used as a datafile by a script. And, even for this purpose, it is
recommended that a real database be used, so that the file itself
cannot be modified by the server user. And if files simply must be
writable by the server, they should definitely not be in some
Web-accessible location, such as **/cgi-bin/**.


.. _See_Also_id135752:

See Also
~~~~~~~~


* :ref:`Running_CGI_Scripts_as_a_Different_User_with_suexec_id144040`

* :ref:`Recipe_File_permissions`

.. admonition:: DRAFT — Review needed

   The following recipe was auto-generated and needs editorial review.
   Check technical accuracy, voice/tone, and fit with surrounding content.

.. _Recipe_security_headers:

Setting security headers (HSTS, CSP, CORS, X-Frame-Options)
-----------------------------------------------------------

.. index:: Security headers
.. index:: HSTS
.. index:: Content-Security-Policy
.. index:: CORS
.. index:: X-Frame-Options
.. index:: Clickjacking protection
.. index:: mod_headers,security

.. _Problem_Recipe_security_headers:

Problem
~~~~~~~


You want to protect your site against clickjacking, protocol downgrade
attacks, and cross-site scripting by setting modern security headers.


.. _Solution_Recipe_security_headers:

Solution
~~~~~~~~


Enable :module:`mod_headers` and add the following directives to your
server or virtual host configuration:

.. code-block:: apache

   # Enforce HTTPS for one year, including subdomains
   Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"

   # Prevent clickjacking — only allow framing by same origin
   Header always set X-Frame-Options "SAMEORIGIN"

   # Block MIME-type sniffing
   Header always set X-Content-Type-Options "nosniff"

   # Enable the browser XSS filter (legacy, but still useful)
   Header always set X-XSS-Protection "1; mode=block"

   # Restrict resource loading to same origin by default
   Header always set Content-Security-Policy "default-src 'self'"

   # Control the Referrer header sent with outgoing requests
   Header always set Referrer-Policy "strict-origin-when-cross-origin"

   # Restrict browser features your site doesn't need
   Header always set Permissions-Policy "geolocation=(), camera=(), microphone=()"

For sites that need to serve resources to other origins (CORS), add:

.. code-block:: apache

   <Location /api>
       Header always set Access-Control-Allow-Origin "https://trusted.example.com"
       Header always set Access-Control-Allow-Methods "GET, POST, OPTIONS"
       Header always set Access-Control-Allow-Headers "Content-Type, Authorization"
   </Location>

Restart httpd:

.. code-block:: bash

   $ sudo apachectl graceful


.. _Discussion_Recipe_security_headers:

Discussion
~~~~~~~~~~


Each of these headers tells the browser to enforce a specific security
policy on behalf of your site. None of them require changes to your
application code—httpd injects them into every response.

**Strict-Transport-Security (HSTS)**

``Strict-Transport-Security`` tells the browser to use HTTPS for all
future requests to this domain for the duration specified by
``max-age`` (in seconds). The ``includeSubDomains`` flag extends the
policy to every subdomain. Once a browser has seen this header, it
will refuse to connect over plain HTTP, even if the user types
``http://`` in the address bar. This prevents SSL-stripping attacks.

.. warning::

   Only enable HSTS when you are certain that your entire site (and
   all subdomains, if using ``includeSubDomains``) works correctly
   over HTTPS. Removing HSTS requires waiting for ``max-age`` to
   expire in every client's cache. Start with a short ``max-age``
   (e.g., ``3600``) during testing.

**X-Frame-Options**

``X-Frame-Options`` controls whether your pages can be embedded in
``<iframe>`` or ``<frame>`` elements. Setting it to ``SAMEORIGIN``
allows your own site to frame its pages but prevents other domains
from doing so, which blocks clickjacking attacks. The older ``DENY``
value prevents all framing. Note that the ``Content-Security-Policy``
header's ``frame-ancestors`` directive is the modern replacement and
is more flexible, but ``X-Frame-Options`` is still respected by older
browsers.

**Content-Security-Policy (CSP)**

``Content-Security-Policy`` is the most powerful—and most
complex—security header. ``default-src 'self'`` restricts all resource
loading (scripts, styles, images, fonts, frames) to the same origin
as the page. You'll almost certainly need to customize this for your
site. Common additions include:

.. code-block:: apache

   # Allow scripts from your CDN and inline styles
   Header always set Content-Security-Policy "default-src 'self'; script-src 'self' https://cdn.example.com; style-src 'self' 'unsafe-inline'"

Start in report-only mode to discover violations without breaking
your site:

.. code-block:: apache

   Header always set Content-Security-Policy-Report-Only "default-src 'self'; report-uri /csp-report"

**Cross-Origin Resource Sharing (CORS)**

CORS headers are only needed if your server provides APIs or resources
consumed by JavaScript running on a *different* origin. The
``Access-Control-Allow-Origin`` header specifies which origins may
make cross-origin requests. Never use ``*`` (wildcard) if the request
includes credentials such as cookies.

**The ``always`` condition**

Note the use of ``Header always set`` rather than plain
``Header set``. The ``always`` condition ensures the header is sent
even on error responses (``4xx``, ``5xx``). Without it, error pages
generated by httpd would not carry your security headers.

.. tip::

   After deploying, test your headers with
   https://securityheaders.com or Mozilla Observatory
   (https://observatory.mozilla.org). Both tools grade your site
   and flag missing or misconfigured headers.


.. _See_Also_Recipe_security_headers:

See Also
~~~~~~~~


* https://httpd.apache.org/docs/current/mod/mod_headers.html

* https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
  — MDN reference for CSP directives

* https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
  — MDN reference for HSTS

* :ref:`Recipe_acme_mod_md` — automatic TLS certificates
  (a prerequisite for deploying HSTS)


.. admonition:: DRAFT — Review needed

   The following recipe was auto-generated and needs editorial review.
   Check technical accuracy, voice/tone, and fit with surrounding content.

.. _Recipe_mod_evasive:

DDoS protection with mod_evasive
--------------------------------

.. index:: DDoS protection
.. index:: mod_evasive
.. index:: Rate limiting
.. index:: DOSPageCount
.. index:: DOSSiteCount

.. _Problem_Recipe_mod_evasive:

Problem
~~~~~~~


You want to protect your server against denial-of-service attacks by
automatically detecting and blocking clients that send an abnormally
high number of requests in a short period.


.. _Solution_Recipe_mod_evasive:

Solution
~~~~~~~~


Install ``mod_evasive``. On Debian/Ubuntu:

.. code-block:: bash

   $ sudo apt-get install libapache2-mod-evasive
   $ sudo a2enmod evasive

On RHEL/Fedora/CentOS:

.. code-block:: bash

   $ sudo dnf install mod_evasive

Add the following configuration to your server config or a dedicated
:file:`conf-enabled/evasive.conf` file:

.. code-block:: apache

   <IfModule mod_evasive20.c>
       DOSHashTableSize    3097
       DOSPageCount        5
       DOSSiteCount        50
       DOSPageInterval     1
       DOSSiteInterval     1
       DOSBlockingPeriod   10
       DOSLogDir           "/var/log/apache2/mod_evasive"
       DOSEmailNotify      admin@example.com
   </IfModule>

Create the log directory:

.. code-block:: bash

   $ sudo mkdir -p /var/log/apache2/mod_evasive
   $ sudo chown www-data:www-data /var/log/apache2/mod_evasive

Restart httpd:

.. code-block:: bash

   $ sudo apachectl graceful


.. _Discussion_Recipe_mod_evasive:

Discussion
~~~~~~~~~~


``mod_evasive`` maintains an internal hash table of IP addresses and
tracks request rates per page and across the entire site. When a
client exceeds the configured thresholds, the module returns
``403 Forbidden`` for the duration of the blocking period.

**Configuration directives explained**

``DOSHashTableSize``
    The size of the internal hash table used to track clients. A larger
    table reduces hash collisions when you have many concurrent
    clients. The value should be a prime number; ``3097`` is a
    reasonable default for moderate traffic.

``DOSPageCount``
    The number of requests for the *same page* from a single IP that
    triggers blocking within the ``DOSPageInterval``. For example,
    with ``DOSPageCount 5`` and ``DOSPageInterval 1``, a client that
    requests the same URL more than 5 times in 1 second is blocked.

``DOSSiteCount``
    The number of requests for *any page* on the site from a single IP
    that triggers blocking within the ``DOSSiteInterval``. This
    catches clients that spread rapid requests across many different
    URLs.

``DOSPageInterval`` / ``DOSSiteInterval``
    The time window (in seconds) for the page and site counters.

``DOSBlockingPeriod``
    How long (in seconds) a blocked client receives ``403`` responses.
    Every new request during the blocking period resets the timer, so
    a client that keeps hammering will stay blocked indefinitely.

``DOSLogDir``
    Directory where lock files are written for blocked IPs. Each
    blocked IP gets a file named ``dos-<IP>``. You can use this for
    integration with external tools like ``fail2ban``.

``DOSEmailNotify``
    Optional email address to notify when an IP is blocked. This uses
    the system's ``mail`` command, so ensure it's configured.

**Integration with fail2ban**

For more persistent blocking, you can combine ``mod_evasive`` with
``fail2ban``. Configure fail2ban to watch the ``DOSLogDir`` for new
lock files and add firewall rules that block repeat offenders at the
network layer:

.. code-block:: text

   # /etc/fail2ban/jail.local
   [apache-evasive]
   enabled  = true
   filter   = apache-evasive
   logpath  = /var/log/apache2/mod_evasive/dos-*
   bantime  = 3600
   maxretry = 1

**Whitelisting trusted clients**

``mod_evasive`` provides a ``DOSWhitelist`` directive to exempt
trusted IP addresses (such as monitoring systems or load balancer
health checks) from rate limiting:

.. code-block:: apache

   DOSWhitelist 127.0.0.1
   DOSWhitelist 10.0.0.*

.. tip::

   Start with generous thresholds on a production server and tighten
   them gradually. Overly aggressive settings can block legitimate
   users—particularly those behind shared NAT gateways or corporate
   proxies where many users share a single IP address.


.. _See_Also_Recipe_mod_evasive:

See Also
~~~~~~~~


* https://github.com/jzdziarski/mod_evasive

* :ref:`Recipe_mod_reqtimeout` — defending against Slowloris and other
  slow-request attacks

* :ref:`Recipe_mod_security_recipes` — a complementary web application
  firewall approach



.. admonition:: DRAFT — Review needed

   The following recipe was auto-generated and needs editorial review.
   Check technical accuracy, voice/tone, and fit with surrounding content.

.. _Recipe_mod_reqtimeout:

Defending Against Slowloris with mod_reqtimeout
-----------------------------------------------

.. index:: mod_reqtimeout

.. index:: Slowloris

.. index:: request timeout

.. index:: DoS protection

.. index:: RequestReadTimeout


.. _Problem_mod_reqtimeout:

Problem
~~~~~~~


You want to protect your server against Slowloris and other
slow-request denial-of-service (DoS) attacks, while ensuring that
legitimate clients—including those uploading large files—are not
rejected.


.. _Solution_mod_reqtimeout:

Solution
~~~~~~~~


The :module:`mod_reqtimeout` module is enabled by default in httpd
2.4 and ships with sensible defaults. Verify that it is loaded:

.. code-block:: apache

   LoadModule reqtimeout_module modules/mod_reqtimeout.so

The default configuration, set automatically when the module is
loaded, is:

.. code-block:: apache

   RequestReadTimeout handshake=0 header=20-40,MinRate=500 body=20,MinRate=500

For servers that accept large file uploads, relax the body timeout on
the upload paths while keeping the rest of the server protected:

.. code-block:: apache

   # Server-wide defaults — protect against slow requests
   RequestReadTimeout handshake=5 header=20-40,MinRate=500 body=20,MinRate=500

   # Relax body timeout for an upload endpoint
   <Location /uploads>
       RequestReadTimeout body=60-300,MinRate=1000
   </Location>

For HTTPS virtual hosts where CRL lookups may be slow, allow extra
time for the TLS handshake:

.. code-block:: apache

   <VirtualHost *:443>
       SSLEngine on
       # ...
       RequestReadTimeout handshake=10 header=20-40,MinRate=500 body=20,MinRate=500
   </VirtualHost>


.. _Discussion_mod_reqtimeout:

Discussion
~~~~~~~~~~


**What is a Slowloris attack?**

A Slowloris attack is a denial-of-service technique that consumes
server resources by opening many connections and sending HTTP headers
(or body data) extremely slowly—just enough to prevent the server from
closing the connection for inactivity. Because each connection ties up
a server thread or process, an attacker with very modest bandwidth can
exhaust the server's connection pool and prevent legitimate clients
from connecting. The attack is particularly effective against
thread-per-connection servers like the ``prefork`` and ``worker`` MPMs.

**How mod_reqtimeout defends against it**

:module:`mod_reqtimeout` counters this by imposing deadlines on each
stage of request reception. If a client fails to complete a stage
within the configured time, the server closes the connection and
returns a ``408 Request Timeout`` error. This is logged at
``LogLevel`` ``info``; you can make it visible by setting:

.. code-block:: apache

   LogLevel reqtimeout:info

The ``RequestReadTimeout`` directive controls three independent
stages, each with its own timeout:

``handshake``
    The time allowed to complete the TLS handshake (HTTPS only). The
    default of ``0`` means no timeout is applied. Set this to a
    positive value (e.g., ``5`` or ``10``) on TLS-enabled virtual hosts.
    Note that clients configured to check Certificate Revocation Lists
    (CRLs) may take extra time if the CRL server is slow to respond,
    so allow for that overhead. The ``handshake`` stage was added in
    httpd 2.4.39.

``header``
    The time allowed to receive the complete HTTP request headers
    (request line plus all header fields). The default
    ``header=20-40,MinRate=500`` means the client has an initial
    timeout of 20 seconds, which is extended by 1 second for every 500
    bytes of header data received, up to a maximum of 40 seconds.

``body``
    The time allowed to receive the complete request body. The default
    ``body=20,MinRate=500`` gives the client 20 seconds, extended by
    1 second for every 500 bytes received. With no upper limit
    specified, the timeout grows as long as data keeps arriving at
    the minimum rate.

Each stage accepts the syntax ``timeout[-maxtimeout][,MinRate=rate]``:

- A single value (e.g., ``body=30``) sets a hard deadline with no
  dynamic extension.
- A range (e.g., ``header=20-40``) sets an initial timeout that can
  grow up to the maximum.
- ``MinRate=bytes`` specifies the minimum data rate, in bytes per
  second, below which the connection is considered too slow. For every
  ``MinRate`` bytes received, the timeout extends by 1 second.

**The large upload problem**

A common issue reported on the ``users@httpd`` mailing list—notably
"httpd 2.4.39 mod_reqtimeout causes large uploads to fail"
(August 2019)—occurs when the default body timeout is too short for
clients uploading large files over slow connections. With
``body=20,MinRate=500``, a client must sustain at least 500 bytes per
second or the connection is closed. This is fine for typical form
submissions but can terminate multi-gigabyte uploads that stall
briefly during transmission.

The solution is to apply a more generous body timeout selectively,
using ``<Location>`` or ``<LocationMatch>`` blocks, so that only the
upload-heavy paths receive relaxed limits:

.. code-block:: apache

   # Allow up to 5 minutes for uploads, extending as long as
   # the client sends at least 1000 bytes/sec
   <Location /api/upload>
       RequestReadTimeout body=60-300,MinRate=1000
   </Location>

   # Same approach for a WebDAV directory
   <Location /webdav>
       RequestReadTimeout body=120-600,MinRate=500
   </Location>

This preserves the tight server-wide defaults that block Slowloris
attacks, while giving known upload endpoints the breathing room they
need.

.. tip::

   ``RequestReadTimeout`` can appear in ``server config`` and
   ``virtual host`` contexts but **not** in ``<Directory>`` or
   :file:`.htaccess`. Use ``<Location>`` blocks to scope overrides
   to specific URL paths.

**Interaction with mod_ssl**

For HTTPS connections, the TLS handshake must complete before headers
or body data can be received. When :module:`mod_ssl` is in use, keep
these points in mind:

- The ``handshake`` stage covers the initial TLS negotiation. If your
  certificate chain is long or your OCSP responder is slow, increase
  this value.
- The ``body`` timeout *includes* any time spent on TLS
  renegotiation, which may occur mid-stream for client certificate
  authentication. Allow additional time if you use per-directory
  ``SSLVerifyClient`` directives that trigger renegotiation.
- When sharing a configuration between HTTP and HTTPS virtual hosts,
  don't set timeouts so low that the TLS overhead causes spurious
  ``408`` errors on the HTTPS side.

**AcceptFilter interaction on Linux and FreeBSD**

On systems using an ``AcceptFilter`` (the default on Linux and
FreeBSD), the kernel may hold the connection until at least one byte of
data arrives before handing it to the server process. This means the
``handshake`` and ``header`` timeouts only begin counting *after* the
server process has received the socket. In practice this is rarely an
issue, but it explains why the very first byte of a connection is not
subject to ``mod_reqtimeout`` on these platforms.

**Recommended starting configuration**

For a general-purpose server that handles both browsing and
occasional file uploads:

.. code-block:: apache

   # Protect the TLS handshake, headers, and body globally
   RequestReadTimeout handshake=5 header=20-40,MinRate=500 body=20,MinRate=500

   # Relax body limits where uploads are expected
   <LocationMatch "^/(uploads|api/files)">
       RequestReadTimeout body=60-300,MinRate=1000
   </LocationMatch>


.. _See_Also_mod_reqtimeout:

See Also
~~~~~~~~


* https://httpd.apache.org/docs/current/mod/mod_reqtimeout.html

* https://en.wikipedia.org/wiki/Slowloris_(computer_security)

* :ref:`Running_a_Minimal_Module_Set_id136520` — reducing attack
  surface by disabling unused modules

* The ``users@httpd.apache.org`` mailing list thread "httpd 2.4.39
  mod_reqtimeout causes large uploads to fail" (August 2019)


Summary
-------


Security is a huge topic, and this chapter just scratches the surface
of one aspect of securing your server. Please don't think that you can
do just these things and be forever secure. Security is an ongoing
process of learning and vigilence, not a "do it once and forget it"
kind of thing at all.

There are a number of very good books available on the topic of
securing services and servers on the Internet, and more come out every
year. And there are books on securing web applications, securing your
mobile apps, using the internet in a safe manner, and so on.

And there are a number of organizations that offer security
certifications, where you can hone your paranoia to a razor edge, and
learn how to secure any platform or service.

But, I hope that this chapter goes a long way towards securing at
least the Apache httpd portion of your Internet presence.

Never stop learning.

