
.. _Chapter_Security:

========
Security
========

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
we strongly recommend that you obtain one of the excellent books that
are available covering the topic of web server security. Several that
we recommend include Ivan Ristic's 'ModSecurity Handbook', Dafydd
Stuttard's 'The Web Application Hacker's Handbook', and Chris
Shifflett's 'Essential PHP Security'. This last one, although the
title indicates that it's specifically about PHP, covers the general
classes of web application exploits in some detail, so while the
examples are in PHP, the concepts are universal.

However, in the context of securing your Apache http server, there are
a number of things that you must get right up front, or else
everything else is just going to be shutting the barn door after the
horse has already left.

The most important measure that you can take is to keep apprised of
new releases, and read the ``CHANGES`` file
to determine if the new version fixes a security hole to which you may be
subject. Running the latest version of the Apache server is usually a good
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

[role="v24"]

.. code-block:: text

   <Directory />
      Require all denied
   </Directory>


For httpd 2.2 and earlier:

[role="v22"]

.. code-block:: text

   <Directory />
       Order deny,allow
       Deny from all
       AllowOverride None
       Options None
   </Directory>


For Microsoft Windows systems, running 2.4 and later:

[role="v24"]

.. code-block:: text

   <Directory C:/>
       Require all denied
   </Directory>


For httpd 2.2 and earlier:

[role="v22"]

.. code-block:: text

   <Directory C:/>
       Order deny,allow
       Deny from all
       AllowOverride None
       Options None
   </Directory>


Repeat for each drive letter on the system.


.. _Discussion_id137267:

Discussion
~~~~~~~~~~


Good security technique is to deny access to everything, and
then selectively permit access where it is needed. By placing a
**Require all denied** directive (**Deny from all** for 2.2 and
earlier) on the entire filesystem, you ensure that files cannot be
loaded from any part of your filesystem unless you explicitly permit
it, using a **Require all granted** (**Allow from all** on 2.2 and
earlier) directive applied to some other **&lt;Directory&gt;** section in your
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


For httpd 2.2 and earlier, apply user authentication 
**per** method using the **Limit** directive:


.. code-block:: text

   AuthName "Restricted Access"
   AuthType Basic
   AuthUserFile /etc/httpd/authusers
   
   Order Deny,Allow
   Allow from all
   
   <Limit GET>
       Satisfy Any
   </Limit>
   
   <LimitExcept GET>
       Satisfy All
       Require valid-user
   </Limit>


.. _Discussion_id137530:


Discussion
~~~~~~~~~~


// TODO: Expand discussion to cover 2.2 and 2.4 syntax, and explain
// how the logic flow works in each case.

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


// TODO: This recipe is probably rubbish, and is definitely rubbish
// for 2.4. Review and rewrite.

For Apache 1.3, you can run a bare-bones server with just three
        modules (actually, you can get away with not running any modules at
        all, but it is not recommended):


++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting6_d1e11732" data-type="programlisting">% <strong><code>./configure --disable-module=all --enable-module=dir \</code></strong>
&gt;<strong><code>--enable-module=mime --enable-module=log_config \</code></strong></pre>
++++++++++++++++++++++++++++++++++++++

For Apache 2.x, this is slightly more complicated, as you must
        individually disable modules you don't want:


++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting6_d1e11741" data-type="programlisting">% <strong><code>./configure --disable-access \</code></strong>
&gt; <strong><code>--disable-auth --disable-charset-lite \</code></strong>
&gt; <strong><code>--disable-include --disable-log-config --disable-env --disable-setenvif \</code></strong>
&gt; <strong><code>--disable-mime --disable-status --disable-autoindex --disable-asis \</code></strong>
&gt; <strong><code>--disable-cgid --disable-cgi --disable-negotiation --disable-dir \</code></strong>
&gt;<strong><code>--disable-imap --disable-actions --disable-alias --disable-userdir</code></strong></pre>
++++++++++++++++++++++++++++++++++++++

Note that with 2.x, as with 1.3, you may wish to enable
        ``mod_dir``, **mod_mime**, and ``mod_log_config``, by simply leaving them off
        of this listing.


.. _Discussion_id136662:

Discussion
~~~~~~~~~~


A frequent security recommendation is that you eliminate
        everything that you don't need; if you don't need something and don't
        use it, then you are likely to overlook security announcements about
        it or forget to configure it securely. The question that is less
        frequently answered is exactly what you do and don't need.

A number of Apache package distributions come with everything
        enabled, and people end up running modules that they don't really
        need—or perhaps are not even aware that they are running.

This recipe is an attempt to get to the very smallest Apache
        server possible, reducing it to the minimum set of modules that Apache
        will run. That is, if you take any of these out, Apache will not even
        start up, let alone serve a functional Web site.


.. _Apache_13_id136704:

Apache 1.3
^^^^^^^^^^


With Apache 1.3, this question is fairly easy to answer. We've
          reduced it to a set of three modules, and actually you can eliminate
          all of the modules if you really want to, as long as you're aware of
          the implications of doing so.

``mod_dir`` is the module
          that takes a request for **/** and
          turns it into a request for **/index.html**, or whatever other file
          you have indicated with the **DirectoryIndex** directive as the default
          document for a directory. Without this module, users typing just
          your hostname into their browser will immediately get a 404 error,
          rather than a default document. Granted, you could require that
          users specify a hostname and filename in their URL, in which case
          you could dispense with this module requirement. This would,
          however, make your Web site fairly hard to use.

``mod_mime`` enables Apache
          to determine what MIME type a particular file is and send the
          appropriate MIME header with that file, enabling the browser to know
          how to render that file. Without ``mod_mime``, your Web server will treat
          **all** files as having the MIME type set by the
          **DefaultType** directive. If this
          happens to match the actual type of the file, well and good;
          otherwise, this will cause the browser to render the document
          incorrectly. If your Web site consists only of one type of files,
          you can omit this module.

Finally, ``mod_log_config``,
          while not technically required at all, is highly recommended.
          Running your Web server without any activity logfiles will leave you
          without any idea of how your site is being used, which can be
          detrimental to the health of your server. However, you should note
          that it is not possible to disable the **ErrorLog** functionality of Apache, and so,
          if you really don't care about the access information of your Web
          site, you could feasibly leave off ``mod_log_config`` and still have error log
          information.


.. _apacheckbk-CHP-6-NOTE-105:


.. tip::

   The default distributed configuration file will need some
   adjustment to run under these reduced conditions. In particular,
   you will probably need to remove **Order**, **Allow**, and **Deny** directives (provided by ``mod_access``), and
   you will need to remove **LogFormat** and **CustomLog** directives if you remove
   ``mod_log_config``. Many other
   sections of the configuration files are protected by **&lt;IfModule&gt;** sections and will still
   function in the absence of the required modules.


.. _Apache_20_id137084:

Apache 2.x
^^^^^^^^^^


With Apache 2.x, a new configuration utility is used, and so
          the command-line syntax is more complicated. In particular, there is
          no single command-line option to let you remove all modules, and so
          every module must be specified with a —disable
          directive.

The list of modules that are minimally required for Apache 2.x
          is the same as that for 1.3. ``mod_dir``, **mod_mime**, and ``mod_log_config`` are each recommended, but
          not mandated, for the same
          reasons outlined previously.


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


.. _Recipe_mod_security_recipes:

mod_security_recipes
--------------------


.. _Problem_mod_security_recipes:

Problem
~~~~~~~


.. _Solution_mod_security_recipes:

Solution
~~~~~~~~


.. _Discussion_mod_security_recipes:

Discussion
~~~~~~~~~~


.. _See_Also_mod_security_recipes:

See Also
~~~~~~~~


.. todo:: rules packages


.. todo:: testing that it's enabled (separate recipe?)


.. _I_sect16_d1e12260:

Chrooting Apache with mod_security
----------------------------------


.. todo:: 


Problem
~~~~~~~


You want to chroot Apache to make it more secure.


Solution
~~~~~~~~


There are a number of different ways to chroot Apache. One of
the simplest is to use ``mod_security``, and add the following
directive:


.. code-block:: text

   SecChrootDir /chroot/apache


Discussion
~~~~~~~~~~


**chroot** is a Unix command that
causes a program to run in a jail. That is to say, when the command is
launched, the accessible file system is replaced with another path,
and the running application is forbidden to access any files outside
of its new file system. By doing this, you are able to control what
resources the program has access to and prevent it from writing to
files outside of that directory, or running any programs that are not
in that directory. This prevents a large number of exploits by simply
denying the attacker access to the necessary tools.

The trouble with **chroot** is
that it is very inconvenient. For example, when you chroot Apache, you
must copy into the new file system any and all libraries or other
files that Apache needs to run. For example, if you're running
``mod_ssl``, you'd need to copy all
of the OpenSSL libraries into the chroot jail so that Apache could
access them. And if you had Perl CGI programs, you'd need to copy
Perl, and all its modules, into the chroot directory.

``mod_security`` gets around
this complexity by chrooting Apache, not when it starts up, but
immediately before it forks its child processes. This solves the
``mod_ssl`` problem mentioned above,
but it would not solve the Perl problem because the Perl CGI program is run by the forked child
process. However, the number of things that you'll need to move or
copy into the chroot jail is greatly reduced, and tends to consist
only of things that you're running as CGI programs, rather than all of
the libraries that Apache needs while it is starting up. This greatly
reduced complexity increases the probability that someone would
actually chroot Apache, as otherwise the complexity is such that most
of us would never be willing to put up with the inconvenience.

If you're running Apache 1.3, you'll need to make sure that
``mod_security`` appears first in
your **LoadModule** list, so that it
can have the necessary level of control over how things are
orchestrated. It's important that the chrooting happen at just the
right moment, and in order for
this to happen, ``mod_security``
needs to get there first before another module can take over.

See Also
~~~~~~~~


* http://modsecurity.org


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
ways to set file permissions on your Apache server, you will get a
dozen different answers. The recommendations here are intended to be
as paranoid as possible. You should feel free to relax these
recommendations, based on your particular view of the world and how
much you trust your users. However, if you set file permissions any
more restrictive than this, your Apache server is likely not to
function. There are, of course, exceptions to this, and cases in which
you could possibly be more paranoid are pointed out later.

The most important consideration when setting file permissions
is the Apache server user—the user as which Apache runs. This is
configured with the **User** and
**Group** directives in your **httpd.conf** file, setting what user and
group the Apache processes will run as. This user needs to have read
access to nearly everything but should not have write access to
anything.

The recommended permissions for the **bin** directory permit anyone to run programs
contained therein. This is necessary in order for users to create
password files using the **htpasswd**
and **htdigest** utilities, run CGI
programs using the **suexec**
utility, check the version of Apache using **httpd** -v, or use any of the
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
by the Apache user. On a server with more than one content developer,
the files should be owned by a group of users who can modify the files
but still be readable by the Apache user. The **icons** directory is a possible exception to
this rule, because the contents of that directory are rarely modified
and do not need to be writable by any users.

The **include** and **libexec** directories contain files that are
needed by the Apache executable at runtime and only need to be
readable by root, which starts as root, and by no other users.
However, since the **include**
directory contains C header files, it may occasionally be useful for
users to have access to those files to build applications that need
those files.

The **logs** directory should
under no circumstances ever be writable by anyone other than root. If
the directory is ever writable by another user, it is possible to gain
control of the Apache process at start time and gain root privileges
on the server. Whether you permit other users to read files in this
directory is up to you and is not required. However, on most servers,
it is very useful for users to be able to access the
logfiles—particularly the ``error_log`` file, in order to troubleshoot
problems without having to contact the server administrator.

The **man** directory contains
the manpages for the various utilities that come with Apache. These
need to be readable by all users. However, it is recommended that you
move them to the system **man** path,
or install them there when you install Apache by providing an argument
to the —mandir argument specifying the location of
your system **man**
directory.

Finally, the **proxy**
directory should be owned by, and writable by, the server user. This
is the only exception to the cardinal rule that nothing should be
writable by this user. The **proxy**
directory contains files created by and managed by ``mod_proxy``, and they need to be writable by
the unprivileged Apache processes. If you are not running a proxy
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

But, we hope that this chapter goes a long way towards securing at
least the Apache httpd portion of your Internet presence.

Never stop learning.

