
.. _Chapter_Troubleshooting_and_error_handling:

==================================
Troubleshooting and Error Handling
==================================

.. index:: Troubleshooting

.. index:: Error handling

.. index:: Error messages


// TODO: A lot of the stuff in this chapter is ancient lore, and needs
// to be scrapped. Review EVERYTHING in here.


.. warning::

   TODO: A number of the recipes in this chapter - particularly the
   Windows ones - are no longer relevant, and should be ditched. It would
   be worthwhile to go through the error messages in the source, and also
   common questions on Stack Overflow or the users list, for more
   relevant error conditions.


When you're running a Web site, things go wrong. And when they do,
it's important that they are handled gracefully, so that the user
experience is not too greatly diminished. In this chapter, you'll learn
how to handle error conditions, return useful messages to the user, and
capture information that will help you fix the problem so that it does not
happen again.

The Apache Web server is a very complex beast. The vanilla package
includes over 30 functional modules and more than 12 dozen configuration
directives. This means that there are significant opportunities for
interactions that produce unexpected or undesirable results. This Appendix
covers some of the more common issues that cause problems, as culled from
various support forums.


.. _Troubleshooting_Methodology_id158765:

Troubleshooting Methodology
---------------------------


.. _In_the_Error_Log_id158778:

In the Error Log
~~~~~~~~~~~~~~~~


The Apache software does quite a reasonable job of reporting the
details when it encounters
problems. The reports are recorded in the server's error log, which is
usually stored in one of the following places:


* ``/usr/local/apache/logs/error_log``

          
* ``/var/log/apache/error_log``

          
* **/var/log/httpd-error.log**

          
* ``/var/log/httpd/error_log``

          
* **C:\Program Files\Apache Group\error.log**

Where the error log is put depends on how you installed and
configured the server; the wealth of possible locations in the list
above is because popular prepackaged installation kits (from Red Hat,
SuSE, etc.) each has its own preferred location. Of course, the
definitive location can be determined by examining your **httpd.conf** file for the **ErrorLog**
directive(s).

So the very first thing you should do when Apache appears to be
misbehaving is see if the server has any comments to make.

If the messages in the error log don't make the cause of the
problem immediately clear, or if there aren't any messages that seem
to relate to the problem, it's a good idea to crank the logging level
up by changing the **LogLevel** setting
in the **httpd.conf** file:


.. code-block:: text

   LogLevel debug


The ``debug`` setting enables all
        possible error messages and makes the server extremely verbose, so
        it's a good idea to set it back to ``warning`` or ``error`` after it has helped you locate the
        cause of your problem.


.. _Characterize_the_Problem_id158947:

Characterize the Problem
~~~~~~~~~~~~~~~~~~~~~~~~


When you're trying to diagnose a problem, here is a question you
should ask yourself: "What is the current behavior, and in what ways
is it different from the expected or desired behavior?"

If you ask this question, a natural successive question is:
"What could cause the current behavior?"

Between the answers to these two questions often lies a
"Eureka!" moment. At the very least, they narrow your area of
research.


.. _Debugging_the_Configuration_id158982:

Debugging the Configuration
---------------------------


When diagnosing a problem by examining your server's
configuration, be sure to examine
all of the files involved. In particular, look for files identified in
Include directives, as well as those in the main **httpd.conf** file and in **.htaccess** files.

If you're editing the server-wide configuration files, be sure to
restart the server afterward to make the changes take effect!

If editing a configuration or **.htaccess** file seems to have no effect, test
that it's actually being processed by putting a line of gibberish into
the file and trying again.

If it seems that a **.htaccess**
file is being ignored, even when you insert gibberish, it indicates that it's within the scope of an
**AllowOverride None** directive.


.. _Debugging_Premature_End_of_Script_Headers_id159096:

Debugging Premature End of Script Headers
-----------------------------------------


When you're working with CGI scripts, certain messages can quickly
become extremely familiar and tiresome; typically the output in the
browser window will be either a blank page or an Internal Server Error
page.

This message has several different possible causes. These include,
but are not necessarily limited to:


* The CGI script is either not emitting any output at all, or it
is emitting content before the required header lines, or it's
neglecting to emit the obligatory blank line between the header and
the content.


* The script encountered an error and emitted the error message
instead of its expected
output.


* You're using **suexec** and
one or more of the **suexec**
constraints has been violated.

To test to see if the problem is an error condition or improper
CGI response formatting, run the script interactively from the command
line to verify that it is emitting content in compliance with the CGI
rules.

If you're using **suexec**, check
the **suexec** logfile to see if there
are security constraints being violated.

You can tell if you're using **suexec** with the following command:


++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting_d1e21876" data-type="programlisting">% <strong><code>httpd -l</code></strong>
Compiled-in modules:
  http_core.c
  mod_so.c
suexec: disabled; invalid wrapper /var/www/apache/bin/suexec</pre>
++++++++++++++++++++++++++++++++++++++

If you get a message that says that **suexec** is disabled, you can ignore that as a
      possible cause of the script's execution problems.

If **suexec** is enabled, though,
      you should look at its logfile to get more details about the problem.
      You can find the logfile with:


++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting_d1e21891" data-type="programlisting">% sudo <strong><code>suexec -V</code></strong>
 -D DOC_ROOT="/usr/local/apache/htdocs"
 -D GID_MIN=100
 -D HTTPD_USER="www"
 -D LOG_EXEC="/usr/local/apache/logs/suexec.log"
 -D SAFE_PATH="/usr/local/bin:/usr/bin:/bin"
 -D UID_MIN=100
 -D USERDIR_SUFFIX="public_html"</pre>
++++++++++++++++++++++++++++++++++++++

The important line is ``-D``
      ``LOG_EXEC="/usr/local/apache/logs/suexec.log"``;
      it tells you **exactly** where **suexec** is recording its errors.

You can find out more about CGI and **suexec** here:


* The CGI specification at http://www.ietf.org/rfc/rfc3875


        
* :ref:`Running_CGI_Scripts_as_a_Different_User_with_suexec_id144040`


        
* The **suexec** manpage


.. _Common_Problems_on_Windows_id159396:

Common Problems on Windows
--------------------------


Windows has its own distinct set of problem areas that don't apply
      to Unixish environments.


.. _Cannot_Determine_Hostname_id159448:

Cannot Determine Hostname
~~~~~~~~~~~~~~~~~~~~~~~~~


When trying to start Apache from a DOS window, you receive a
message like, "Cannot determine hostname. Use **ServerName** directive to set it
manually."

If you don't explicitly supply Apache with a name for your
system, it tries to figure it out. This message is the result of that
process failing.

The cure for this is really quite simple: edit your **conf\httpd.conf** file, look for the string
``ServerName``, and make sure there's
an uncommented directive such as:


.. code-block:: text

   ServerName localhost


or:


++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting_d1e21969" data-type="programlisting">ServerName <em><code>www.foo.com</code></em></pre>
++++++++++++++++++++++++++++++++++++++

in the file. Correct it if there is one there with wrong
information, or add one if you don't already have one.

Also, make sure that your Windows system has DNS enabled. See
the TCP/IP setup component of the Networking or Internet Options
control panel.

After verifying that DNS is enabled and that you have a valid
hostname in your **ServerName** directive, try to start the
server again.


.. _Finding_WS2_32DLL_on_Windows_id159567:

Finding WS2_32.DLL on Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


When trying to start Apache on Windows 95, a message like,
"Unable To Locate WS2_32.DLL..." appears. This file is necessary for
Apache to function properly.

Prior to Version 1.3.9, Apache for Windows used Winsock 1.1.
Beginning with Version 1.3.9, Apache began using Winsock 2 features
(specifically, WSADuplicateSocket()). ``WS2_32.DLL`` implements the Winsock 2 API.
Winsock 2 ships with Windows NT 4.0 and Windows 98. Some of the
earlier releases of Windows 95 did not include Winsock 2.

To fix it, install Winsock 2, which is available at http://www.microsoft.com/windows95/downloads/. Then
restart your server, and the problem should be gone.


.. _Fixing_WSADuplicateSocket_Errors_id159641:

Fixing WSADuplicateSocket Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


If, when trying to start Apache on Windows, it fails and the
Apache error log contains this message:


.. code-block:: text

   [crit] (10045) The attempted operation is not supported for the type of object 
       referenced: Parent: WSADuplicateSocket failed for socket ###


it indicates that your system is using a firewall product that
has inserted itself into the network software but doesn't fully
provide all the functionality of the native network calls.

To get rid of the problem, you need to reconfigure, disable, or
remove the firewall product that is running on the same box as the
Apache server.

This problem has been seen when Apache is run on systems along
with Virtual Private Networking (VPN) clients such
as **Aventail Connect**. **Aventail Connect** is a Layered Service Provider (LSP) that inserts
itself, as a shim, between the Winsock 2 API
and Windows' native Winsock 2 implementation. The **Aventail Connect** shim does not implement WSADuplicateSocket, which is the cause of
the failure.

The shim is not unloaded when **Aventail Connect** is shut down. Once observed, the problem persists
until the shim is either explicitly unloaded or the machine is
rebooted.

Another potential solution (not tested) is to add **apache.exe** to the **Aventail Connect** exclusion list (see below).

Apache is affected in a similar way by any firewall program that
isn't correctly configured. Assure you exclude your Apache server
ports (usually port 80) from the list of ports to block. Refer to your
firewall program's documentation for the how-to.

Relevant information specific to **Aventail Connect** can be found at How to Add an Application to Aventail Connect's
Application Exclusion List at http://support.aventail.com/akb/article00586.html.


.. _Handling_System_Error_1067_id159829:

Handling System Error 1067
~~~~~~~~~~~~~~~~~~~~~~~~~~


Sometimes, when starting Apache on Windows, you might get a
        message like "``System error 1067 has occurred. The process terminated unexpectedly.``" This uninformative
        message means that the Web server was unable to start correctly as a
        service for one reason or another.

As with any error, the first step should be to check your Apache
        error log. If that doesn't reveal anything useful, try checking the
        Windows application event log to find out why Apache won't start. If
        that doesn't help, try:


++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting_d1e22096" data-type="programlisting">D:\&gt;<strong><code>c:</code></strong>
C:\&gt;<strong><code>cd "\Program Files\Apache Group\Apache"</code></strong>
C:\Program Files\Apache Group\Apache&gt;<strong><code>apache</code></strong></pre>
++++++++++++++++++++++++++++++++++++++

(If you don't get the prompt back, hit Ctrl-C to cause Apache to
        exit.)

This will run Apache interactively rather than as a service; any
        error messages should show up on your screen rather than being
        concealed behind a ``System Error 1067`` alert box.


.. _Fixing_Build-Time_Error_Messages_id159934:

Fixing Build-Time Error Messages
--------------------------------


.. ___inet_Symbols_id159947:

__inet Symbols
~~~~~~~~~~~~~~


If you have installed BIND-8, then this is normally because of a
        conflict between your include files and your libraries. BIND-8
        installs its include files and libraries in **/usr/local/include/** and **/usr/local/lib/**, whereas the resolver that
        comes with your system is probably installed in **/usr/include/** and **/usr/lib/**.

If your system uses the header files in **/usr/local/include/** before those in
        **/usr/include/** but you do not use
        the new resolver library, then the two versions will conflict. To
        resolve this, you can either make sure you use the include files and
        libraries that came with your system, or make sure to use the new
        include files and libraries.

If you're using Apache 2.0 or later, or Apache 1.3 with the
        ``APACI`` build script, you can make
        changes to the library search lists by defining them on the **./configure** command line:


++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting_d1e22156" data-type="programlisting">% <strong><code>LIBS=-lbind ./configure </code></strong><em><code>...</code></em></pre>
++++++++++++++++++++++++++++++++++++++

If you're using Apache 1.3 or earlier and controlling the build
        process by editing the **Configuration** file directly, just add
        -lbind to the EXTRA_LDFLAGS line in
        the file.

After making the appropriate change to your build configuration
        process, Apache should build with the correct library.


.. _apacheckbk-APP-B-NOTE-127:


.. tip::

             Apache versions 1.2 and earlier use
             EXTRA_LFLAGS in the **Configuration** file instead.


As of BIND 8.1.1, the **bind**
        libraries and files are installed under **/usr/local/bind** by default, so you should not run into this
        problem. Should you want to use the bind resolvers, you'll have to add
        the following to the respective lines:


* For Apache 1.3 with APACI, or 2.0 and later:

++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting_d1e22199" data-type="programlisting">% <strong><code>CFLAGS=-I/usr/local/bin/include \</code></strong>
&gt; <strong><code>LDFLAGS=/usr/local/bind/lib LIBS=-lbind \</code></strong>
&gt;<strong><code>./configure </code></strong><em><code>...</code></em></pre>
++++++++++++++++++++++++++++++++++++++
    
* For Apache 1.2 or 1.3 with direct editing of **Configuration**, add/change the following lines in the file:      


.. code-block:: text

   EXTRA_CFLAGS=-I/usr/local/bind/include
   EXTRA_LDFLAGS=-L/usr/local/bind/lib
   EXTRA_LIBS=-lbind


.. _Getting_Server-Side_Includes_to_Work_id160173:

Getting Server-Side Includes to Work
------------------------------------


The solution is to make sure that **Options** **Includes** is turned on and that either **XBitHack** is turned
      **On**, or that you have the appropriate
      **AddHandler** directives set on the file
      type that you are using.

As discussed in :ref:`Getting_SSIs_to_Work_id142764`,
      there are a number of ways to enable SSI. If the unparsed SSI directives are appearing in the
      HTML when the page is loaded, this is a clear indication that SSI execution is not
      enabled for the document in question.

If the server has difficulty parsing an SSI directive, it will
      substitute the phrases "An error occurred while processing this
      directive" in its place in the response. If this happens, the cause of the problem should
      be listed in the server's error log. See also :ref:`Running_CGI_Scripts_as_a_Different_User_with_suexec_id144040`.


.. _Debugging_Rewrites_That_Result_in_Not_Found_Errors_id160270:

Debugging Rewrites That Result in "Not Found" Errors
----------------------------------------------------


If your **RewriteRule** directives
      keep resulting in ``404 Not Found`` error
      pages, add the ``PT`` (PassThrough) flag
      to the **RewriteRule** line. Without this
      flag, Apache won't process a lot of other factors that might apply, such
      as **Alias** settings.

You can verify that this is the cause of your problem by cranking
      the ``mod_rewrite`` logging level up to
      9 and seeing that the entries relating to the **RewriteRule** mention something about prefixes
      with ``document_root``:

++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting_d1e22302" data-type="programlisting">RewriteLog logs/rewrite-log
RewriteLogLevel 9

% <strong><code>tail logs/rewrite_log</code></strong>
<em><code>ip-address</code></em> - - [<em><code>date</code></em>] [<em><code>reqid</code></em>] (2) prefixed with document_root to
/usr/local/apache/htdocs/robots.text
<em><code>ip-address</code></em> - - [<em><code>date</code></em>] [<em><code>reqid</code></em>] (1) go-ahead with
/usr/local/apache/htdocs/robots.text [OK]</pre>
++++++++++++++++++++++++++++++++++++++


.. _apacheckbk-APP-B-NOTE-129:


.. tip::

   Don't forget to turn off the **RewriteLog** directive, or possibly just turn
   down the logging level, after you've done your checking! Otherwise,
   your disk space may disappear like the snows of yesteryear.


Without the ``PT`` flag, ``mod_rewrite`` assumes that any rewriting it
      does will be the last URL manipulation the server needs to do for the
      request. Because ``mod_rewrite``
      directives are handled very early in request processing, this can mean
      that **Alias**, **ScriptAlias** and other URL manipulations may
      not get executed. Specifying the flag tells ``mod_rewrite`` to not short-circuit processing
      but to let it continue as usual.


.. _htaccess_Files_Having_No_Effect_id160456:

.htaccess Files Having No Effect
--------------------------------


Make sure that **AllowOverride** is
      set to an appropriate value. Then, to make sure that the **.htaccess** file is being parsed at all, put
      the following line in the file and ensure that it causes a server error
      page to show up in your browser:


.. code-block:: text

   Garbage Goes Here


**.htaccess** files override the
      settings in the main server configuration file. Because this is
      frequently an undesired thing, **.htaccess** files are frequently disabled,
      which will cause your **.htaccess**
      file to be ignored.

**.htaccess** files are enabled
      using the **AllowOverride** directive,
      which lists categories of directives that may appear in an **.htaccess** file. For example, if you wish to
      put authentication-related
      directives in an **.htaccess** file,
      you will need to put the following line in the main server configuration
      file:


.. code-block:: text

   AllowOverride AuthConfig


**AllowOverride** **All** permits any directive to be put in the
      **.htaccess** file, while the directive
      **AllowOverride None** means, "Please
      ignore my **.htaccess** files."

Thus, the most common cause of an **.htaccess** file being ignored is simply that
      your configuration file tells Apache to ignore it.

If you put garbage in your **.htaccess** file, this should generate a Server
      Error message in the browser, which will verify that Apache is indeed
      looking at the contents of your file. However, if such a message is not
      displayed, this is a sure sign that your **.htaccess** file is being completely
      ignored.


.. _Address_Already_in_Use_id160617:

Address Already in Use
----------------------


If, when attempting to start your Apache server, you get the
      following error message:


.. code-block:: text

   [Thu May 15 01:23:40 2003] [crit] (98)Address already in use: make_sock: could not 
       bind to port 80


one of three things is happening:


* You are attempting to start the server as a nonroot user.
          Become the root user and try again.


        
* There is already some process running (perhaps another Apache
          server) using port 80. Run **netstat**, or perhaps look at the process
          list and kill any process that seems to fill this role.


        
* You have more than one **Listen** directive in your configuration
          file pointing to the same port number. Find the offending duplicate
          directive and remove it.


In the case of the first condition, you will need to become the
      root user in order to start Apache. By long tradition, only the root
      user may bind to any port lower than 1025. Because Apache typically runs
      on port 80, this requires root privileges.

The second condition can be a little trickier. Sometimes a child
      process will refuse to die and will remain running after Apache has been
      shut down. There are numerous reasons this might happen. Most of the
      time, you can kill this process forcibly using **kill** or **kill -9** while logged in as root. As long as this process is running
      and has the port occupied, you will be unable to start anything else
      wanting to bind to that same port.

In the case of the third condition, the second **Listen** directive attempts to bind to port 80,
      which has already been taken by the first **Listen** directive. Simply removing one of the
      **Listen** directives will clear up this
      problem.


.. todo:: Custom error response - ErrorDocument


.. _Recipe_ErrorDocument:

Returning a custom response to an error condition
-------------------------------------------------


.. _Problem_ErrorDocument:

Problem
~~~~~~~


.. _Solution_ErrorDocument:

Solution
~~~~~~~~


.. _Discussion_ErrorDocument:

Discussion
~~~~~~~~~~


.. _See_Also_ErrorDocument:

See Also
~~~~~~~~


.. _Handling_a_Missing_Host_Field_id145631:

Handling a Missing Host Field
-----------------------------


.. _Problem_id145644:

Problem
~~~~~~~


You have multiple virtual hosts in your configuration, and at
        least one of them is name-based. For name-based virtual hosts to work
        properly, the client must send a valid ``Host`` field in the request header. This
        recipe describes how you can deal with situations in which the field
        is **not** included.


.. _Solution_id145686:

Solution
~~~~~~~~


Add the following lines to your **httpd.conf** file:


++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting9_d1e15776" data-type="programlisting">Alias /NoHost.cgi <em><code>/usr/local/apache/cgi-bin</code></em>/NoHost.cgi
RewriteEngine On
RewriteCond "%{HTTP_HOST}" "^$"
RewriteRule "(.*)" "/NoHost.cgi$1" [PT]</pre>
++++++++++++++++++++++++++++++++++++++

The file **NoHost.cgi** can contain something like the following:


.. code-block:: text

   #! /usr/bin/perl -Tw
   
   my $msg = "To properly direct your request, this server requires that\n"
           . "your web client include the HTTP 'Host' request header field.\n"
           . "The request which caused this response did not include such\n"
           . "a field, so we cannot determine the correct document for you.\n";
   print "Status: 400 Bad Request\r\n\"
       . "Content-type: text/plain\r\n\"
       . 'Content-length: ' . length($msg) . "\r\n\"
       . "\r\n\"
       . $msg;
   exit(0);


.. _Discussion_id145736:

Discussion
~~~~~~~~~~


Once the directives in the solution are in place, all requests
        made of the server that do not include a ``Host`` field in the request header will be
        redirected to the specified CGI script, which can take appropriate
        action.

The solution uses a CGI script so that the response text can be
        tailored according to the attributes of the request and the server's
        environment. For instance, the script might respond with a list of
        links to valid sites on the server, determined by the script at
        runtime by examining the server's own configuration files. If all you
        need is a "please try again, this time with a ``Host`` field" sort of message, a static HTML
        file would suffice. Replace the **RewriteRule** directive in the solution with
        that below, and create the **nohost.html** accordingly:


.. code-block:: text

   RewriteRule ".*" "/nohost.html" [PT]


A more advanced version of the script approach could possibly
        scan the **httpd.conf** file for
        **ServerName** directives, construct a
        list of possibilities from them, and present links in a ``300 Multiple Choices`` response. Of course,
        there's an excellent chance they wouldn't work, because the client
        **still** did not include the ``Host`` field.


.. _See_Also_id145836:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_rewrite.html


.. _Changing_the_Response_Status_for_CGI_Scripts_id145868:

Changing the Response Status for CGI Scripts
--------------------------------------------


.. _Problem_id145882:

Problem
~~~~~~~


There may be times when you want to change the status for a
        response—for example, you want ``404 Not Found`` errors to be sent back to the client as ``403 Forbidden`` instead.


.. _Solution_id145958:

Solution
~~~~~~~~


Point your **ErrorDocument** to a
        CGI script instead of a static file. The CGI specification permits
        scripts to specify the response status code.

In addition to the other header fields the script emits, like
        the ``Content-type`` field, include one
        named ``Status`` with the value and
        text of the status you want to return:


.. code-block:: text

   #! /bin/perl -w
   print "Content-type: text/html;charset=iso-8859-1\r\n";
   print "Status: 403 Access denied\r\n";
       :


.. _Discussion_id146004:

Discussion
~~~~~~~~~~


If Apache encounters an error processing a document, such as not
        being able to locate a file, by default it will return a canned error
        response to the client. You can customize this error response with the
        **ErrorDocument** directive, and Apache
        will generally maintain the
        error status when it sends your custom error text to the
        client.

However, if you want to change the status to something else,
        such as hiding the fact that a file doesn't exist by returning a
        Forbidden status, you need to tell Apache about the change.

This requires that the **ErrorDocument** be a dynamic page, such as a
        CGI script. The CGI specification provides a very simple means of
        specifying the status code for a response: the ``Status`` CGI header field. The Solution shows
        how it can be used.


.. _See_Also_id146079:

See Also
~~~~~~~~


* :ref:`Chapter_Dynamic_content`, **Dynamic Content**

* http://httpd.apache.org/docs/mod/core.html#errordocument

* http://www.rfc-editor.org/cgi-bin/rfcdoctype.pl?loc=RFC&amp;letsgo=3875&amp;type=ftp&amp;file_format=txt


.. _Customized_Error_Messages_id146135:

Customized Error Messages
-------------------------


.. _Problem_id146149:

Problem
~~~~~~~


You want to display a customized error message, rather than the
        default Apache error page.


.. _Solution_id146187:

Solution
~~~~~~~~


Use the **ErrorDocument** directive in **httpd.conf**:


++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting9_d1e15946" data-type="programlisting">ErrorDocument 405 <em><code>/errors/notallowed.html</code></em></pre>
++++++++++++++++++++++++++++++++++++++


.. _Discussion_id146219:

Discussion
~~~~~~~~~~


The **ErrorDocument** directive
        allows you to create your own error pages to be displayed when
        particular error conditions occur. In the previous example, in the
        event of a ``405`` status code ``(Method Not Allowed)``, the specified URL is
        displayed for the user, rather than the default Apache error
        page.

The page can be customized to look like the rest of your Web
        site. When an error document looks significantly different from the
        rest of the site, this can leave the user feeling disoriented, or she
        may think she has left the site that she was on.


.. _See_Also_id146280:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/core.html#errordocument


.. _Providing_Error_Documents_in_Multiple_Languages_id146312:

Providing Error Documents in Multiple Languages
-----------------------------------------------


.. _Problem_id146326:

Problem
~~~~~~~


On a multilingual (content-negotiated) Web site, you want your
        error documents to be content-negotiated as well.


.. _Solution_id146364:

Solution
~~~~~~~~


The Apache 2.0 default configuration file contains a
configuration section, initially commented out, that allows you to
provide error documents in multiple languages customized to the look
of your Web site, with very little additional work.

Uncomment those lines. You can identify the lines by looking for
the following comment in your
default configuration file:


.. code-block:: text

   # The internationalized error documents require mod_alias, mod_include
   # and mod_negotiation.  To activate them, uncomment the following 30 lines.


In Apache 1.3 this is harder, but there's a solution in the
works, as of this writing, that will make it similar to the 2.0
implementation. Check the Apache Cookbook Web site for more
information.


.. _Discussion_id146407:

Discussion
~~~~~~~~~~


The custom error documents provided with Apache 2.0 combine a
variety of techniques to provide internationalized error messages. As
of this writing, these error messages are available in German,
English, Spanish, French, Dutch, Swedish, Italian, and Portuguese.
Based on the language preference set in the client browser, the error
message is delivered in the preferred language of the end user.

Using content negotiation, the correct variant of the document
(**i.e.**, the right language) is selected for the user, based on her
browser preference settings. For more information about content
negotiation, see the content negotiation documentation at 
http://httpd.apache.org/docs/content-negotiation.html

In addition to delivering the error message in the correct
language, this functionality also lets you customize the look of these
error pages so that they resemble the rest of your Web site. To
facilitate this, the files **top.html** and **bottom.html**, located in the **include** subdirectory of the **error** directory, should be modified to look
like the standard header and footer content that appears on your Web
site. The body of the error message documents is placed between the
header and the footer to create a page that is less jarring to users
when they transition from your main site to the error pages that are
generated.

You also will note that the error documents contain SSI
directives, which are used to further customize the error documents
for the user. For example, in the case of the 404 (file not found)
error document, the page will provide a link back to the page that the
user came from, if the environment variable ``HTTP_REFERER`` is defined, and if that
variable is not found, the page will merely notify the user that the
URL was not found. Other SSI directives may be put in these documents,
if you wish, to further customize them.


.. _See_Also_id146537:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/content-negotiation.html


          
* http://httpd.apache.org/docs-2.0/content-negotiation.html


          
* http://apache-cookbook.com


          
* :ref:`Getting_SSIs_to_Work_id142764`


.. _Redirecting_Invalid_URLs_to_Some_Other_Page_id146604:

Redirecting Invalid URLs to Some Other Page
-------------------------------------------


.. _Problem_id146619:

Problem
~~~~~~~


You want all "not found" pages to go to some other page instead,
        such as the front page of the site, so that there is no loss of
        continuity on bad URLs.


.. _Solution_id146640:

Solution
~~~~~~~~


Use the **ErrorDocument** directive to catch ``404 (Not Found)`` errors:


++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting9_d1e16081" data-type="programlisting">ErrorDocument 404 <em><code>/index.html</code></em>
DirectoryIndex index.html<em><code>/path/to/notfound.html</code></em></pre>
++++++++++++++++++++++++++++++++++++++


.. _Discussion_id146694:

Discussion
~~~~~~~~~~


The recipe given here will cause all 404 errors—every time
        someone requests an invalid URL—to return the URL **/index.html**, providing the user with the
        front page of your Web site, so that even invalid URLs still get valid
        content. Presumably, users accessing an invalid URL on your Web site
        will get a page that helps them find the information that they were
        looking for.

By contrast, this behavior may confuse the user who believes she
        knows exactly where the URL should take her. Make sure that the page
        that you provide as the global error document does in fact help the
        user find things on your site, and does not merely confuse or
        disorient her. You may, as shown in the example, return her to the
        front page of the site. From there she should be able to find what she
        was looking for.

When users get good content from bad URLs, they will never fix
        their bookmarks and will continue to use a bogus URL long after it has
        become invalid. You will continue to get 404 errors in your log file
        for these URLs, and the users will never be aware that they are using
        an invalid URL. If, by contrast, you actually return an error
        document, they will immediately be aware that the URL they are using
        is invalid and will update their bookmarks to the new URL when they
        find it.

Note that, even though a valid document is being returned, a
        status code of 404 is still returned to the client. This means that if
        you are using some variety of tool to validate the links on your Web
        site, you will still get good results, if the tool is checking the
        status code, rather than looking for error messages in the
        content.


.. _See_Also_id146760:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/core.html#errordocument


          
* http://httpd.apache.org/docs/mod/mod_dir.html


.. _Making_Internet_Explorer_Display_Your_Error_Page_id146805:

Making Internet Explorer Display Your Error Page
------------------------------------------------


.. _Problem_id146819:

Problem
~~~~~~~


You have an **ErrorDocument**
        directive correctly configured, but IE is displaying its own error
        page, rather than yours.


.. _Solution_id146871:

Solution
~~~~~~~~


Make the error document bigger—at least 512 bytes.


.. _Discussion_id146892:

Discussion
~~~~~~~~~~


Yes, this seems a little bizarre, and it is. In this case,
        Internet Explorer thinks it knows better than the Web site
        administrator. If the error document is smaller than 512 bytes, it
        will display its internal error message page, rather than your custom
        error page, whenever it receives a 400 or 500 series status code. This
        size is actually configurable in the browser, so this number may in
        fact vary from one client to another. "Friendly error messages" also
        can be turned off entirely in the browser preferences.

This can be extremely frustrating the first time you see it
        happen, because you just know you have it configured correctly and it
        seems to work in your other browsers. Furthermore, when some helpful
        person tells you that your error document just needs to be a little
        larger, it's natural to think that he is playing a little prank on
        you, because this seems a little too far-fetched.

But it's true. Make the page bigger. It needs to be at least 512
        bytes, or IE will ignore it and gleefully display its own "friendly"
        error message instead.

Exactly what you fill this space with is unimportant. You can,
        for example, just bulk it up with comments. For example, repeating the
        following comment six times would be sufficient to push you over that
        minimum file size:


.. code-block:: text

   <!-- message-obscuring clients are an abomination 
        and an insult to the user's intelligence -->


.. _See_Also_id146982:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/core.html#errordocument


.. _Notification_on_Error_Conditions_id147014:

Notification on Error Conditions
--------------------------------


.. _Problem_id147028:

Problem
~~~~~~~


You want to receive email notification when there's an error
        condition on your server.


.. _Solution_id147073:

Solution
~~~~~~~~


Point the **ErrorDocument** directive to a CGI program that sends mail, rather than to a static document:

++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting9_d1e16182" data-type="programlisting">ErrorDocument 404 <em><code>/cgi-bin/404.cgi</code></em></pre>
++++++++++++++++++++++++++++++++++++++

**404.cgi** looks like the following:


.. code-block:: text

   #!/usr/bin/perl
   use Mail::Sendmail;
   use strict;
   
   my $message = qq~
   Document not found: $ENV{REQUEST_URI}
   Link was from: $ENV{HTTP_REFERER}
   ~;
   
   my %mail = (
               To => 'admin@server.com',
               From => 'website@server.com',
               Subject => 'Broken link',
               Message => $message,
               );
   sendmail(%mail);
   
   print "Content-type: text/plain\n\n";
   print "Document not found. Admin has been notified\n";


.. _Discussion_id147167:

Discussion
~~~~~~~~~~


This recipe is provided as an example, rather than as a
        recommendation. On a Web site of any significant size or traffic
        level, actually putting this into practice generates a substantial
        quantity of email, even on a site that is very well maintained. This
        is because people mistype URLs, and other sites, over which you have
        no control, will contain incorrect links to your site. It may be
        educational, however, to put something like this in place, at least
        briefly, to gain an appreciation for the scale of your own Web
        site.

The **ErrorDocument** directive
        will cause all ``404 (Document Not Found)`` requests to be handled by the specified URL, and so
        your CGI program gets run and is passed environment variables that
        will be used in the script itself to figure out what link is bad and
        where the request came from.

The script used the **Mail::Sendmail** Perl module to deliver the
        email message, and this module should work fine on any operating
        system. The module is not a standard part of Perl, so you may have to
        install it from CPAN (http://www.cpan.org). A
        similar effect can, of course, also be achieved in PHP or any other
        programming language.

The last two lines of the program display a very terse page for
        the user, telling him that there was an error condition. You may wish,
        instead, to have the script redirect the user to some more informative
        and attractive page on your Web site. This could be accomplished by
        replacing those last two lines with something like the
        following:


.. code-block:: text

   print "Location: http://server.name/errorpage.html\n\n";


This would send a redirect header to the client, which would
        display the specified URL to the user.


.. _See_Also_id147310:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/core.html#errordocument

Summary
-------


.. todo:: 


