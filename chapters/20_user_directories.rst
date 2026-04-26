
.. _Chapter_userdir:

================
User Directories
================

.. epigraph::

   Our house, in the middle of our street.

   -- Madness, *Our House*


.. index:: User directories

.. index:: UserDir

.. index:: public_html


Since the initial release of Apache httpd, a userdir functionality has
been provided. A non-privileged user (**i.e.**, not ``root``) can put web
content in their home directory, or other specified location, and have
that served **via** a specially formatted URL. For example, a user with a
username of ``dpitts`` would be able to have this content served **via** the
URL http://example.com/~dpitts without having to have write
access to the main website content directory.

In this chapter, I explore the various aspects of configuring this
functionality.


.. admonition:: Modules covered in this chapter

   :module:`mod_userdir`


.. _Recipe_UserDir:

Giving a non-privileged user their own web space
------------------------------------------------

.. index:: UserDir

.. index:: User directories

.. index:: public_html


.. _Problem_UserDir:

Problem
~~~~~~~


You want to give each user on your system their own web space.


.. _Solution_UserDir:

Solution
~~~~~~~~


If you want users' web locations to be under their home
directories, add this to your ``httpd.conf`` file:


.. code-block:: text

   UserDir public_html


To put all users' web directories under a central location, rather
than their home directories:


.. code-block:: text

   UserDir "/www/users/*/htdocs"


If you want to let users access their home directory without
having to use a tilde (``~``) in the
URL, see :ref:`Recipe_UserDir_without_tilde`


.. _Discussion_UserDir:

Discussion
~~~~~~~~~~


The first solution is the simplest and most widely used of the
possible recipes I present here. With this directive in place, all
users on your system are able to create a directory called _public_html_ in their home directories and
put web content there. Their web space is accessible **via** a URL
starting with a tilde (``~``), followed by their username. So, a user 
named ``maria`` accesses her personal Web space **via** the URL:


.. code-block:: text

   http://www.example.com/~maria/


If you installed Apache httpd from the standard source distribution,
your default configuration file includes an example of this setup. It
also contains a ``<Directory>``
section referring to the directory ``/home/*/public_html``, with various options
and permissions turned on. You need to uncomment that section in order
for anyone to have access to these user web sites. This section should
look something like the following:


.. code-block:: text

   <Directory "/home/*/public_html">
       AllowOverride FileInfo AuthConfig Limit
       Options MultiViews Indexes SymLinksIfOwnerMatch IncludesNoExec
       Require method GET POST OPTIONS PROPFIND
   </Directory>


.. tip::

   See :ref:`glob_matching` for a discussion of using the ``*``
   wildcard in directory paths.


Make sure you understand what each of these directives is
enabling before you uncomment this section in your configuration.

It is common practice to ``AllowOverride All`` in userdir directories,
as many users will wish to override the global configuration with
``.htaccess`` files. The example shown here takes a more conservative
approach.

The second solution differs in that the argument to 
**UserDir** is given as a full pathname and so
is not interpreted as relative to the user's home directory, but as an
actual filesystem path. The ``*`` in
the file path is replaced by the username. For example, 
http://example.com/~iwinter/
is translated to ``/www/users/iwinter/htdocs``. This directory
structure needs to be configured in a manner similar to the previous
example.

In each case, the directory in question, and directories in the
path leading up to it, need to be readable for the Apache httpd
configured user
(usually **nobody** or **www** or **apache**), and also have the 
execute bit set
for that user, so the httpd server can read content out of that
directory. (The execute bit is needed in order to get a directory
listing.) Thus, for user **rbowen**, the
directories **/**, **/home**, **/home/rbowen**, and **/home/rbowen/public_html** 
(or the corresponding directory paths for the other
solutions) all need to execute access, and the last one also requires
read access.

On Unixish systems, you would set these permissions by issuing
the following commands:


.. code-block:: text

   chmod o+x / /home /home/bob
   chmod o+rx /home/bob/public_html


The files within the directory need only be readable, while each
subdirectory needs to be executable as well.


.. code-block:: text

   find /home/bob/public_html -type d | xargs chmod o+rx
   find /home/bob/public_html -type f | xargs chmod o+r 


This will recurse through subdirectories, making each file readable,
and each directory navigable, to the Apache httpd process.

If you use the first solution, many users may be concerned about
these file permissions, and rightly so, as it usually allows all other
users read access to these directories. Make sure that your users are
aware of this, and that they keep personal files in directories that
are not world readable.

The advantage of the second solution over the first one is
that these files are stored in a location that is not inside the
user's home directory, and so the user may keep sensible file
permissions on her home directory. This lets her store personal files
there without concern that other users may have free access to
them.


.. _See_Also_UserDir:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_userdir.html
            
* :ref:`Recipe_UserDir_without_tilde`

* :ref:`Recipe_Disable_Userdir`

See also userdirlog recipe in ch04


.. _Recipe_Disable_Userdir:

Disable UserDir directories
---------------------------

.. index:: UserDir,Disable

.. index:: Disable UserDir

.. index:: public_html,Disable


.. _Problem_Disable_Userdir:

Problem
~~~~~~~


You wish to disable the userdir functionality, either for all users,
or for specific users.


.. _Solution_Disable_Userdir:

Solution
~~~~~~~~


Disable the UserDir feature with the following directive:


.. code-block:: text

   UserDir disabled


To disable this feature for just a particular user:


.. code-block:: text

   # Disable userdir for root
   UserDir disabled root


Or, you can specify more than one user with a space-separated list of
usernames.


.. code-block:: text

   # Dicable userdir for dangerous users
   UserDir disabled dpitts sungo rbowen jbrose


.. _Discussion_Disable_Userdir:

Discussion
~~~~~~~~~~


The **UserDir** functionality discussed in :ref:`Recipe_UserDir` may be
disabled for any or all users with the **disabled** keyword. This
results in a Not Found response being returned for request for that
particular user URL.

It is particularly recommended that you disable **UserDir** for the
username **root**. While it is unlikely that sensitive content in
the **root** home directory will be readable by the Apache httpd
process, every layer of security helps.


.. _See_Also_Disable_Userdir:

See Also
~~~~~~~~


* :ref:`Recipe_UserDir`

* http://httpd.apache.org/docs/mod/mod_userdir.html 


.. _Recipe_remote-userdir-server:

Pointing userdirs to another server
-----------------------------------

.. index:: UserDir,Remote server

.. index:: public_html,Remote server


.. _Problem_remote-userdir-server:

Problem
~~~~~~~


You want to keep all of your UserDir content on a separate web server,
and send requests there.


.. _Solution_remote-userdir-server:

Solution
~~~~~~~~


Specify a URL as the argument for ``UserDir``:


.. code-block:: text

   UserDir http://users.example.com/


This will cause a request for
http://example.com/~roberto/resume.html
to be redirected to http://users.example.com/roberto/resume.html


.. _Discussion_remote-userdir-server:

Discussion
~~~~~~~~~~


For reasons of security, or possibly convenience, it may be desirable
to keep user-editable content on a separate server from your main
website. In the example given here, the main website is on the
server ``example.com`` and user-editable content on a separate server
``users.example.com``, but you still wish to support ``~`` style URLs on
the main server.

The recipe given will give us the best of both worlds, with
``~username`` requests resulting in a redirect to the user-specific URL
on the other website.


.. _See_Also_remote-userdir-server:

See Also
~~~~~~~~


* :ref:`Recipe_UserDir`

* :ref:`Recipe_userdir-checking-alternatives`


.. _Recipe_userdir-checking-alternatives:

Checking several alternative UserDir locations
----------------------------------------------

.. index:: UserDir,Checking alternatives


.. _Problem_userdir-checking-alternatives:

Problem
~~~~~~~


You have several different locations where user content is stored, and
you want httpd to check them all.


.. _Solution_userdir-checking-alternatives:

Solution
~~~~~~~~


Specify several arguments to ``UserDir``, listing the alternatives:


.. code-block:: text

   UserDir public_html /usr/web http://users.example.com/


.. _Discussion_userdir-checking-alternatives:

Discussion
~~~~~~~~~~


In the recipe given above, a request for
http://example.com/~rbowen/books.html will cause httpd to look several
places. First, it will look for the file
``/home/rbowen/public_html/books.html``. If that
exists, it will stop looking. If it doesn't, it will check
for the existence of ``/usr/web/rbowen/books.html``. Finally, it will
issue a redirect to http://users.example.com/rbowen/books.html


.. _See_Also_userdir-checking-alternatives:

See Also
~~~~~~~~


* :ref:`Recipe_remote-userdir-server`


.. _Recipe_per-userdir-scriptalias:

Creating a CGI Directory for Each User
--------------------------------------

.. index:: CGI

.. index:: Per-user CGI directory

.. index:: UserDir,CGI directory

.. index:: cgi-bin,per-user

.. index:: ScriptAliasMatch


.. _Problem_per-userdir-scriptalias:

Problem
~~~~~~~


You want each user to have their own **cgi-bin** directory
rather than giving them all access to the main server CGI directory.


.. _Solution_per-userdir-scriptalias:

Solution
~~~~~~~~


Put this in your **httpd.conf**:


.. code-block:: text

   <Directory "/home/*/public_html/cgi-bin/">
       Options ExecCGI
       SetHandler cgi-script
   </Directory>
   
   ScriptAliasMatch "/~([^/]+)/cgi-bin/(.*)" "/home/$1/public_html/cgi-bin/$2"


.. _Discussion_per-userdir-scriptalias:

Discussion
~~~~~~~~~~


You can't use a regular **ScriptAlias** in
this case, because for each user, the first argument to 
**ScriptAlias** would be different. The ``<Directory>`` container 
and the **ScriptAliasMatch** directive are functionally 
equivalent. [#ch18_fn1]_

This recipe lets each user put CGI scripts in her own personal
Web space. Files accessed **via** URLs starting with:


.. code-block:: text

   http://www.example.com/~username/cgi-bin/


are treated as CGI scripts.

If you have **suexec** enabled, you'll gain the added benefit that
CGI programs run from this target directory will be run with the user
ID of the user specified in the URL. For example, a CGI program
accessed **via** the URL http://www.example.com/~rbowen/cgi-bin/example.cgi
would be run as the user ``rbowen``.


.. warning::

   Allowing users to set up their own scripts to be automatically
   executed without some sort of review is asking for trouble, either
   from malicious users (perish the thought!) or exploitable insecure
   scripts.


The same thing can be accomplished using a Directory block with a
wildcard:


.. _See_Also_per-userdir-scriptalias:

See Also
~~~~~~~~


* :ref:`Recipe_ScriptAlias`


.. _Recipe_UserDir_without_tilde:

Enabling a userdir without the tilde
------------------------------------

.. index:: UserDir,Without tilde


.. _Problem_UserDir_without_tilde:

Problem
~~~~~~~


You want to enable user directories, but without having to have the
tilde (``~``) in the URL.


.. _Solution_UserDir_without_tilde:

Solution
~~~~~~~~


.. code-block:: text

   RewriteEngine On
   RewriteCond "/home/$1/public_html" -d [NC]
   RewriteRule "^/([^/]+)/(.*)" "/home/$1/public_html/$2"


.. _Discussion_UserDir_without_tilde:

Discussion
~~~~~~~~~~


This solution provides **UserDir** functionality without
having to use a tilde (``~``) in the URL.

Using the **RewriteCond**
directive, the rule first checks for the existence of the user's home
directory, and, if it exists, it rewrites requests into that directory.
Performing this check first ensures that other URLs continue to work
correctly, and only those URLs starting with a valid username are
rewritten to a user's home directory.

This rewrite ruleset takes advantage of a little-known fact
about ``mod_rewrite`` —in particular,
that a ``RewriteRule`` is always
considered first, and, if it matches, the ``RewriteCond`` is evaluated after that.
Consequently, you can use ``$1`` in the
``RewriteCond``, even though the value
of that variable is set in the ``RewriteRule`` appearing on the following
line.

This scenario might also be a good time to use ``mod_macro``. See the
recipe provided in :ref:`Recipe_Logging_userdir` for inspiration on how
you might accomplish that.


.. _See_Also_UserDir_without_tilde:

See Also
~~~~~~~~


* :ref:`Recipe_Logging_userdir`


.. _Recipe_per_userdir_logging:

Providing per-userdir log files
-------------------------------


.. _Problem_per_userdir_logging:

Problem
~~~~~~~


You want to provide each user with a dedicated log file.


.. _Solution_per_userdir_logging:

Solution
~~~~~~~~


See :ref:`Recipe_Logging_userdir` for the solution to this problem.

Summary
-------


This is a short chapter, and a seldom-used feature. 10 years ago,
tildes in URLs were a very common site, but they have faded from
popularity as the cost of registering domain names, and the cost of
dedicated web hosting, has fallen. However, these techniques may still
find use inside any organization that wishes to provide per-user websites
without a great deal of administrative overhead.


.. rubric:: Footnotes

.. [#ch18_fn1] That is, they do exactly the same thing.
