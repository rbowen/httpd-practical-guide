
.. _Chapter_Logging:

=======
Logging
=======

.. epigraph::

   | Every breath you take, every move you make,
   | every bond you break, every step you take,
   | I'll be watching you.

   -- The Police, *Every Breath You Take*


.. index:: Logging

.. index:: Log files


Apache httpd can, and usually does, record information about every request
it processes. Controlling how this is done and extracting useful
information out of these logs after the fact is at least as important as
gathering the information in the first place.

The logfiles may record two types of data: information about the
request itself, and possibly one or more messages about abnormal
conditions encountered during processing (such as file permissions).

As the server administrator, you have a great deal of control over the
format, location, and contents, of these log files. In the 2.4 version
of the server, even more options have been added for you to determine
what is logged, and how that information is presented.

One aspect of activity logging you should be aware of is that most
logging is done **after** the request has been completely processed.
This means that the interval between the time a request begins
and when it finishes may be long enough to matter in certain cases.

For example, if your logfiles are rotated while a particularly large
file is being downloaded, the log entry for the request will appear in the
new logfile when the request completes, rather than in the old logfile
when the request was started. In contrast, an error message is written to
the error log as soon as it is encountered.

The Web server will continue to record information in its logfiles as
long as it's running. This can result in extremely large logfiles for
a busy site and uncomfortably large ones even for a modest site. To
keep the file sizes from growing ever larger, most sites rotate or
**roll over** their logfiles on a semi-regular basis. Rolling over a
logfile simply means persuading the server to stop writing to the
current file and start recording to a new one. Because of httpd's
determination to see that no records are lost, cajoling it to do this
according to a specific timetable may require a bit of effort; some of
the recipes in this chapter cover how to accomplish the task
successfully and reliably.

(see Recipes :ref:`Recipe_Rotate_By_Time` and
:ref:`Recipe_System_logrotate`)
.. index:: containers,<VirtualHost>

The log declaration directives, **CustomLog** and **ErrorLog**, can appear
inside **&lt;VirtualHost&gt;** containers, outside them (in what's
called the main or global server, or sometimes the global scope), or
both. Entries will only be logged in one set or the other; if a
**&lt;VirtualHost&gt;** container applies to the request or error and
has an applicable log directive, the message will be written only to
that vhost's logs and won't appear in any globally declared files. By
contrast if no **&lt;VirtualHost&gt;** log directive applies, the server
will fall back on logging the entry according to the global
directives.

In 2.4 and later, you can also declare log directives in a
**per**-directory scope, so that certain log files reflect only a smaller
portion of your web content.

However, whichever scope is used for determining what logging
directives to use, all **CustomLog** directives in that scope are
processed and treated independently. That is, if you have a
**CustomLog** directive in the global scope and two inside a
**&lt;VirtualHost&gt;** container, **both** of these will be
used. Similarly, if a **CustomLog** directive uses the ``env=`` option, it
has no effect on what requests will be logged by other **CustomLog**
directives in the same scope.
.. index:: directives,CustomLog

.. index:: directives,<VirtualHost>

.. index:: containers,<VirtualHost>


.. refcosplay

.. admonition:: Modules covered in this chapter

   :module:`mod_dumpio`, :module:`mod_log_config`, :module:`mod_logio`,
   :module:`mod_macro`, :module:`mod_setenvif`


.. _Recipe_Understanding_CLF:

Understanding the Common Log Format
-----------------------------------

.. index:: Common Log Format; see Logging,Common Log Format

.. index:: CLF; see Logging,Common Log Format

.. index:: Logging,Common Log Format

.. index:: Logging,CLF; see Logging,Common Log Format

.. index:: Understanding the Common Log Format (CLF)


.. _Problem_Understanding_CLF:

Problem
~~~~~~~


You'd like to understand what information is being logged in the
common log format that httpd uses by default.


.. _Solution_Understanding_CLF:

Solution
~~~~~~~~


The Common Log Format is defined by the following **LogFormat** directive:
.. index:: directives,LogFormat


.. code-block:: text

   LogFormat "%h %l %u %t \"%r\" %>s %b" common


It consists of 7 fields:

.. index:: Logging,Common log format,fields


.. _CLF_fields:


**Common Log Format Fields**


+----------------+---------------------------------------------------------+
| Field          | Description                                             |
+----------------+---------------------------------------------------------+
| Remote host    | The IP address of the requesting client                 |
+----------------+---------------------------------------------------------+
| Remote logname | Usually blank - the remote username supplied by identd. |
+----------------+---------------------------------------------------------+
| Remote user    | The username, if the request was authenticated          |
+----------------+---------------------------------------------------------+
| Timestamp      | The request timestamp, in standard english format       |
+----------------+---------------------------------------------------------+
| Request        | The first line of the request                           |
+----------------+---------------------------------------------------------+
| Status         | The final request status code                           |
+----------------+---------------------------------------------------------+
| Bytes          | The number of bytes transferred to the client           |
+----------------+---------------------------------------------------------+


.. _Discussion_Understanding_CLF:

Discussion
~~~~~~~~~~


When you are using the common log format, entries in your
log file will look something like the following:


.. code-block:: text

   164.75.17.12 - - [02/Jun/2015:11:14:00 -0400] "GET /icons/blank.gif HTTP/1.1" 200 148


This represents various details about who made a request to your
server, what they requested, when it happened, and what the result
was.

The Common Log Format, or CLF, has been a standard for web server
access logs since the very earliest days of the Web. The Common Log
Format was defined by the developers of the earliest web servers, and
have stuck with us ever since, although modern web servers offer the
option of extending this log format, as you will see in further
recipes, below.

.. index:: Logging,format names

.. index:: Logging,format names,common

The **LogFormat** directive shown above defines a log format named
'``common``', which can then be used in **CustomLog** directives elsewhere
in your configuration files:
.. index:: directives,LogFormat

.. index:: directives,CustomLog


.. code-block:: text

   CustomLog /var/log/httpd/access_log common


You can also define your own log formats, using any of the variables
supplied by ``mod_log_config`` and supporting modules such as
``mod_logio``. (See :ref:`Recipe_logging_logio` below.)
.. index:: Modules,mod_log_config

.. index:: Modules,mod_logio


A few of the fields in the above table require a little extra
explanation.

The 'Remote logname' field is a historical artifact, and is almost
always going to be empty. That is, rather than actual data being
logged here, you'll see '-' as a placeholder in this field.

In the earliest days of the web, this would often contain identifying
information about the person requesting the web resource. Often it was
their email address, or other identifying username information.

Things were simpler then.

Very soon, this information started to be exploited to send spam to
these website visitors, and most web clients (browsers) disabled this
feature.

However, by this time, there were already a number of popular software
packages available for doing log file analysis, so the log format was
maintained unchanged, even though this field is almost always blank.

The remote user field is also usually blank, since most web content is
not authenticated. If, however, you use HTTP Authentication to require
a user to authenticate in order to access a resource, the provided
username will be logged in this field. These days, most people use
some other type of authentication (such as cookie-based), which does
not populate the ``REMOTE_USER`` environmental variable, so it is fairly
uncommon to see anything in this field.

See :ref:`Chapter_AAA`, *Authentication, Authorization and Access
Control*, for more discussion of user authentication.

See :ref:`Recipe_Status_codes` for discussion of what the status code
field means.


.. _See_Also_Understanding_CLF:

See Also
~~~~~~~~


* :ref:`Recipe_Understanding_Combined_Log_Format`

* :ref:`Recipe_Status_codes`

* :ref:`Chapter_AAA`, **Authentication, Authorization and Access Control**

* http://httpd.apache.org/docs/mod/mod_log_config.html


.. refcosplay

.. _Recipe_Understanding_Combined_Log_Format:

Understanding Combined Log Format
---------------------------------

.. index:: Combined Log Format; see Logging,Common Log Format

.. index:: Logging,Combined Log Format

.. index:: mod_log_config; see Modules,mod_log_config

.. index:: Modules,mod_log_config

.. index:: Understanding the Combined Log Format (CLF)


.. _Problem_Understanding_Combined_Log_Format:

Problem
~~~~~~~


You'd like to understand what information is being logged in the
common log format that Apache httpd uses by default.


.. _Solution_Understanding_Combined_Log_Format:

Solution
~~~~~~~~


The Combined Log Format is defined by the following **LogFormat** directive:
.. index:: directives,LogFormat


.. code-block:: text

   LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"" combined


It consists of 9 fields:


.. _CombinedLF_fields:


**Common Log Format Fields**


+----------------+---------------------------------------------------------+
| Field          | Description                                             |
+----------------+---------------------------------------------------------+
| Remote host    | The IP address of the requesting client                 |
+----------------+---------------------------------------------------------+
| Remote logname | Usually blank - the remote username supplied by identd. |
+----------------+---------------------------------------------------------+
| Remote user    | The username, if the request was authenticated          |
+----------------+---------------------------------------------------------+
| Timestamp      | The request timestamp, in standard english format       |
+----------------+---------------------------------------------------------+
| Request        | The first line of the request                           |
+----------------+---------------------------------------------------------+
| Status         | The final request status code                           |
+----------------+---------------------------------------------------------+
| Bytes          | The number of bytes transferred to the client           |
+----------------+---------------------------------------------------------+
| Referer        | The URL that linked to the requested resource           |
+----------------+---------------------------------------------------------+
| User agent     | The browser identifier string for the requesting client |
+----------------+---------------------------------------------------------+


.. _Discussion_Understanding_Combined_Log_Format:

Discussion
~~~~~~~~~~


.. index:: Logging; see Logging,Common Log Format

Although the Common Log Format became standard very quickly, there
were of course other things that people wanted to log. In the early
days, two other log directives - **RefererLog** and **AgentLog** - created
log files that logged, respectively, the request referrer and the user
agent (browser) string making the request.
.. index:: directives,RefererLog

.. index:: directives,AgentLog


.. note::

   **Yes, I know**

   The misspelling of "Referrer" as "Referer" is a legacy artifect from
   the earliest days of the web. Don't bother reporting it. It makes a
   lot of people grind their teeth when they see it, but we're kind of
   stuck with it.



A combined log file was desired - one that logged the referrer and the
agent string alongside the request itself, rather than separately,
with no correlation to the actual resource being requested.

Thus the combined log format was created.

Later on, when all log file configuration was consolidated into the
_mod_log_config_ module, these special-purpose log directives were
deprecated, and all log file formatting is now done with the
**LogFormat** directive.
.. index:: Modules,mod_log_config

.. index:: directives,LogFormat


Log entries in the combined log format look something like:


.. code-block:: text

   17.42.199.8 - - [03/Jun/2015:13:27:34 -0400] "GET
   /products/pony.html HTTP/1.1" 200 4241
   "http://anothersite.com/ponies.html" "Mozilla/5.0 (X11; Linux
   x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81
   Safari/537.36"


This looks very much like the above-mentioned common log format, but
with two new fields added on the end.

The two additions were the **Referer** (yes, "Referer" with one r. Dee
the note above. It's spelled incorrectly in the specifications) and
the **User-agent**.

**Referer** is the URL of the page that linked to the current
request. For example, if file **a.html** contains a link such as:


.. code-block:: text

   <a href="b.html">another page</a>


When the link is followed, the request header for **b.html** will
contain a **Referer** field that has the URL of **a.html** as its value.

The **Referer** field is not required nor reliable; some users prefer
software or anonymizing tools that ensure that you can't tell where
they've been. However, this is usually a fairly small number and may
be disregarded for most Web sites.

Request headers also often include a field called the
**User-agent**. This is defined as the name and version of the client
software being used to make the request. For instance, a **User-agent**
field value might look like this:


.. code-block:: text

   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like
   Gecko) Chrome/43.0.2357.81 Safari/537.36"


This tells you that the client is claiming to be Mozilla 5.0
running on a Linux system.

I say "claiming to be" because the ``User-agent`` field is neither
required nor reliable; many users prefer software or anonymizing tools
that ensure that you can't tell what they're using. Some software
even lies about itself so it can work around sites that cater
specifically to one browser or another. It's a good idea to design
your site to be as browser-agnostic (**i.e.**, works for any browser) as
possible for this reason, among others. If you're going to make
decisions based on the value of the field, you might as well believe
it hasn't been faked—because there's no way to tell if it has.


.. tip::

   **Mobile user or not?**

   Many Web sites use the value of the **User-agent** field to determine
   whether the visitor is using a mobile device (**e.g.**, a tablet or
   smartphone) or not, in order to tailor the page layout for better
   readability.



To use the combined log format in your access log, invoke it with the
**CustomLog** directive:
.. index:: directives,CustomLog


.. code-block:: text

   CustomLog /var/log/httpd/access_log combined


.. _See_Also_Understanding_Combined_Log_Format:

See Also
~~~~~~~~


* :ref:`Recipe_Understanding_CLF`

* http://httpd.apache.org/docs/mod/mod_log_config.html

* :ref:`Recipe_Logging_request_header`

* :ref:`Recipe_image-theft`


.. refcosplay

.. _Recipe_Status_codes:

Understanding HTTP status codes
-------------------------------

.. index:: HTTP

.. index:: HTTP,status codes

.. index:: Status Codes; see HTTP,status codes

.. index:: HTTP,status codes,understanding them


.. _Problem_Status_codes:

Problem
~~~~~~~


You'd like to know what the HTTP status codes in your log file mean.


.. _Solution_Status_codes:

Solution
~~~~~~~~


The various HTTP status codes are defined in the HTTP specification
itself, as follows:


.. refcosplay

.. _HTTP_status_codes:


HTTP status codes
---------------------

+-----------------------+---------------------------------+
| Code                  | Abstract                        |
+-----------------------+---------------------------------+
| **Informational 1xx** |                                 |
+-----------------------+---------------------------------+
| 100                   | Continue                        |
+-----------------------+---------------------------------+
| 101                   | Switching protocols             |
+-----------------------+---------------------------------+
| **Successful 2xx**    |                                 |
+-----------------------+---------------------------------+
| 200                   | OK                              |
+-----------------------+---------------------------------+
| 201                   | Created                         |
+-----------------------+---------------------------------+
| 202                   | Accepted                        |
+-----------------------+---------------------------------+
| 203                   | Nonauthoritative information    |
+-----------------------+---------------------------------+
| 204                   | No content                      |
+-----------------------+---------------------------------+
| 205                   | Reset content                   |
+-----------------------+---------------------------------+
| 206                   | Partial content                 |
+-----------------------+---------------------------------+
| **Redirection 3xx**   |                                 |
+-----------------------+---------------------------------+
| 300                   | Multiple choices                |
+-----------------------+---------------------------------+
| 301                   | Moved permanently               |
+-----------------------+---------------------------------+
| 302                   | Found                           |
+-----------------------+---------------------------------+
| 303                   | See other                       |
+-----------------------+---------------------------------+
| 304                   | Not modified                    |
+-----------------------+---------------------------------+
| 305                   | Use proxy                       |
+-----------------------+---------------------------------+
| 306                   | (Unused)                        |
+-----------------------+---------------------------------+
| 307                   | Temporary redirect              |
+-----------------------+---------------------------------+
| **Client error 4xx**  |                                 |
+-----------------------+---------------------------------+
| 400                   | Bad request                     |
+-----------------------+---------------------------------+
| 401                   | Unauthorized                    |
+-----------------------+---------------------------------+
| 402                   | Payment required                |
+-----------------------+---------------------------------+
| 403                   | Forbidden                       |
+-----------------------+---------------------------------+
| 404                   | Not found                       |
+-----------------------+---------------------------------+
| 405                   | Method not allowed              |
+-----------------------+---------------------------------+
| 406                   | Not acceptable                  |
+-----------------------+---------------------------------+
| 407                   | Proxy authentication required   |
+-----------------------+---------------------------------+
| 408                   | Request timeout                 |
+-----------------------+---------------------------------+
| 409                   | Conflict                        |
+-----------------------+---------------------------------+
| 410                   | Gone                            |
+-----------------------+---------------------------------+
| 411                   | Length required                 |
+-----------------------+---------------------------------+
| 412                   | Precondition failed             |
+-----------------------+---------------------------------+
| 413                   | Request entity too large        |
+-----------------------+---------------------------------+
| 414                   | Request-URI too long            |
+-----------------------+---------------------------------+
| 415                   | Unsupported media type          |
+-----------------------+---------------------------------+
| 416                   | Requested range not satisfiable |
+-----------------------+---------------------------------+
| 417                   | Expectation failed              |
+-----------------------+---------------------------------+
| **Server error 5xx**  |                                 |
+-----------------------+---------------------------------+
| 500                   | Internal server error           |
+-----------------------+---------------------------------+
| 501                   | Not implemented                 |
+-----------------------+---------------------------------+
| 502                   | Bad gateway                     |
+-----------------------+---------------------------------+
| 503                   | Service unavailable             |
+-----------------------+---------------------------------+
| 504                   | Gateway timeout                 |
+-----------------------+---------------------------------+
| 505                   | HTTP version not supported      |
+-----------------------+---------------------------------+


.. _Discussion_Status_codes:

Discussion
~~~~~~~~~~

.. index:: RFC

.. index:: Request for Comments; see RFC

.. index:: RFC,HTTP Protocol (2616)

.. index:: RFC,HTTP Status Codes (additional) (6585)

The status codes are defined
by the HTTP protocol specification documents, which
you can access at http://tools.ietf.org/html/rfc2616.
:ref:`HTTP_status_codes` gives a brief description of the
codes defined in the HTTP specification. Other RFCs, such as RCF 6585
(http://tools.ietf.org/html/rfc6585) propose other status
codes, so this list may not be complete.

Codes are in 5 categories. Codes starting with 1 are informational.
Status values starting with 2 indicate a successful request. Status
values starting with 3 indicate that the request was redirected to
some other resource. Status values starting with 4 indicate that an
error occurred on the client side. And status values starting with 5
indicate that an error occurred on the server side.

The RFCs mentioned above discuss the detailed meaning of each error
code in greater detail.


.. _See_Also_Status_codes:

See Also
~~~~~~~~


* http://tools.ietf.org/html/rfc2616 (HTTP Protocol)
* http://tools.ietf.org/html/rfc6585 (Additional HTTP Status Codes)


.. _Recipe_LogFormat:

Adding more information to the access log
-----------------------------------------

.. index:: directives,LogFormat

.. index:: Logging,Access log

.. index:: Logging,LogFormat

.. index:: Logging,Adding more information to the access log


.. _Problem_LogFormat:

Problem
~~~~~~~


You want to add more information to your access log file.


.. _Solution_LogFormat:

Solution
~~~~~~~~

.. index:: directives,LogFormat

Use the **LogFormat** directive to create a new log format, adding the
variables that you're interested in. There's a wide variety of
variables available, including any environment variable, request
header field, and many other things.

.. index:: Modules,mod_log_config

These are documented in the ``mod_log_config`` documentation at
http://httpd.apache.org/docs/mod/mod_log_config.html.


For example, if you wanted to log the ``QUERY_STRING```, you could create
a query string log format:
.. index:: directives,LogFormat

.. index:: directives,CustomLog

.. index:: Logging,format names


.. code-block:: text

   LogFormat "%t \"%r\" %q" querylog
   CustomLog /var/log/httpd/query_log querylog


.. _Discussion_LogFormat:

Discussion
~~~~~~~~~~


The following variables are available for use in **LogFormat**
directives.

.. index:: Modules,mod_remoteip

.. index:: Modules,mod_headers

.. index:: Modules,mod_setenvif

.. index:: Modules,mod_identd

.. index:: Logging,Common Log Format


.. _LogFormat_fields:


**LogFormat available variables**


+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Format String                 | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%%``                        | The percent sign. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%a``                        | Client IP address of the request (see the _mod_remoteip_ module). |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%{c}a``                     | Underlying peer IP address of the connection (see the _mod_remoteip_ module). |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%A``                        | Local IP-address. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%B``                        | Size of response in bytes, excluding HTTP headers. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%b``                        | Size of response in bytes, excluding HTTP headers. In CLF format, **i.e.**, a '-' rather than a 0 when no bytes are sent. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%{``**``VARNAME````**}C``   | The contents of cookie **VARNAME** in the request sent to the server. Only version 0 cookies are fully supported. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%D``                        | The time taken to serve the request, in microseconds. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| %{**``VARNAME``**}e           | The contents of the environment variable **VARNAME**. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%f``                        | Filename. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%h``                        | Remote hostname. Will log the IP address if **HostnameLookups** is set to ``Off``, which is the default. If it logs the hostname for only a few hosts, you probably have access control directives mentioning them by name. See the **Require host** documentation. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%H``                        | The request protocol. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%{``**``VARNAME``**``}i``   | The contents of the **VARNAME**: header field(s) in the request sent to the server. Changes made by other modules (**e.g.**, _mod_headers_) affect this. If you're interested in what the request header was prior to when most modules would have modified it, use _mod_setenvif_ to copy the header into an internal environment variable and log that value with the **``%{``***``VARNAME``***``}e``** described above. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%k``                        | Number of keepalive requests handled on this connection. Interesting if **KeepAlive** is being used, so that, for example, a '1' means the first keepalive request after the initial one, '2' the second, etc...; otherwise this is always 0 (indicating the initial request). |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%l``                        | Remote logname (from **identd**, if supplied). This will return a dash unless _mod_ident_ is present and **IdentityCheck** is set to ``On``. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%L``                        | The request log ID from the error log (or '-' if nothing has been logged to the error log for this request). Look for the matching error log line to see what request caused what error. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%m``                        | The request method. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%{``**``VARNAME``**``}n``   | The contents of note **VARNAME** from another module. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%{``**``VARNAME``**``}o``   | The contents of **VARNAME**: header field(s) in the response. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%p``                        | The canonical port of the server serving the request. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%{``**``format``**``}p``    | The canonical port of the server serving the request, or the server's actual port, or the client's actual port. Valid formats are ``canonical``, ``local``, or ``remote``. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%P``                        | The process ID of the child that serviced the request. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%{``**``format``**``}P``    | The process ID or thread ID of the child that serviced the request. Valid formats are ``pid``, ``tid``, and ``hextid``. ``hextid`` requires APR 1.2.0 or higher. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%q``                        | The query string (prepended with a ``?`` if a query string exists, otherwise an empty string). |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%r``                        | First line of request. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%R``                        | The handler generating the response (if any). |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%s``                        | Status. For requests that have been internally redirected, this is the status of the original request. Use ``%>s`` for the final status. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%t``                        | Time the request was received, in the format **``[18/Sep/2011:19:18:28 -0400]``**. The last number indicates the timezone offset from GMT. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%{``**``format``**``}t``    | The time, in the form given by ``format``, which should be in an extended ``strftime(3)`` format (potentially localized). If the format starts with **``begin:``** (default) the time is taken at the beginning of the request processing. If it starts with **``end:``** it is the time when the log entry gets written, close to the end of the request processing. In addition to the formats supported by ``strftime(3)``, the following format tokens are supported: |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%T``                        | The time taken to serve the request, in seconds. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%{``**``UNIT``**``}T``      | The time taken to serve the request, in a time unit given by **``UNIT``**. Valid units are **``ms``** for milliseconds, **``us``** for microseconds, and **``s``** for seconds. Using **``s``** gives the same result as **``%T``** without any format; using **``us``** gives the same result as **``%D``**. Combining **``%T``** with a unit is available in 2.4.13 and later. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%u``                        | Remote user if the request was authenticated. May be bogus if return status (``%s``) is 401 (unauthorized). |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%U``                        | The URL path requested, not including any query string. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%v``                        | The canonical **ServerName** of the server serving the request. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%V``                        | The server name according to the **UseCanonicalName** setting. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%X``                        | Connection status when response is completed:                                                                                                                                                                                                                                                                                                                                                                                                                             |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``X =``                       | Connection aborted before the response completed. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``\`` =+                      | Connection may be kept alive after the response is sent. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``- =``                       | Connection will be closed after the response is sent. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%I``                        | Bytes received, including request and headers. Cannot be zero. You need to enable _mod_logio_ to use this. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%O``                        | Bytes sent, including headers. May be zero in rare cases such as when a request is aborted before a response is sent. You need to enable _mod_logio_ to use this. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%S``                        | Bytes transferred (received and sent), including request and headers, cannot be zero. This is the combination of **``%I``** and **``%O``**. You need to enable _mod_logio_ to use this. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%{``**``VARNAME``**``}^ti`` | The contents of **VARNAME**: trailer line(s) in the request sent to the server. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``%{``**``VARNAME``**``}^to`` | The contents of **VARNAME**: trailer line(s) in the response sent from the server. |
+-------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


Any of these variables can be strung together to create your own
custom access log format, and you can have as many access logs as you
wish, logging this information.


.. _See_Also_LogFormat:

See Also
~~~~~~~~


* **LogFormat** documentation at http://httpd.apache.org/docs/mod/mod_log_config.html
* _mod_headers_ documentation at http://httpd.apache.org/docs/mod/mod_headers.html
* _mod_logio_ documentation at http://httpd.apache.org/docs/mod/mod_logio.html
* _mod_remoteid_ documentation at http://httpd.apache.org/docs/mod/mod_remoteid.html
* _mod_setenvif_ documentation at http://httpd.apache.org/docs/mod/mod_setenvif.html
* **``man 3 strftime``**


.. refcosplay

.. _Recipe_Understanding_ErrorLog:

Understanding your error_log
----------------------------

.. index:: ErrorLog

.. index:: Logging,ErrorLog

.. index:: Error log format

.. index:: Understanding your error_log


.. _Problem_Understanding_ErrorLog:

Problem
~~~~~~~


You want to understand what the entries in the error log mean.


.. _Solution_Understanding_ErrorLog:

Solution
~~~~~~~~


Error log entries contain a few standard fields, and then a free-form
error message.

The default error log format looks like:


.. code-block:: text

   [Wed Oct 11 14:32:52 2000] [error] [client 127.0.0.1] client denied by
   server configuration: /export/home/live/ap/htdocs/test


The fields in this error message are:

* Date/Time of error condition
* Log level at which the error message was logged
* The elient address making the request
* Free-form error message

The error log format can be customized with the ``ErrorLogFormat`` directive. By default it looks like:


.. code-block:: text

   [Fri Jun 05 16:28:52.598613 2015] [core:info] [pid 31581:tid
   140214657406720] [client 127.0.0.1:57772] AH00128: File does not
   exist: /var/www/html/missing


The fields in the error message are:

* Date/Time of the error condition
* The module reporting the error, and the log level at which it was
  logged
* Process ID, and thread ID, which handled the request
* The client IP address and port number
* Error code, starting with 'AH'
* Free-form error message


.. _Discussion_Understanding_ErrorLog:

Discussion
~~~~~~~~~~


You can use the ``ErrorLogFormat`` directive to create your own custom error
log format to include additional information to help in
troubleshooting.

The error code - in the example above it is AH00128 - is a unique
identifier that can help you find troubleshooting tips online.
Eventually, we will have these tips in the Apache httpd documentation,
but searching online for this code will find numerous third-party
websites telling you how to resolve the problem.


.. _See_Also_Understanding_ErrorLog:

See Also
~~~~~~~~


* :ref:`Recipe_Correlating_error_access`

* ``ErrorLogFormat`` documentation at
  http://httpd.apache.org/docs/mod/core.html#errorlogformat


.. _Recipe_Detailed_Errors:

Getting More Detailed Errors
----------------------------

.. index:: Debug logging

.. index:: LogLevel

.. index:: Logging,Detailed errors

.. index:: Logging,LogLevel

.. index:: Getting more detailed errors


.. _Problem_Detailed_Errors:

Problem
~~~~~~~


You want more information in the error log in order to debug a
problem.


.. _Solution_Detailed_Errors:

Solution
~~~~~~~~


Change (or add) the **LogLevel** line in your **httpd.conf** file.
There are several possible arguments, which are enumerated
here.

For example:


.. code-block:: text

   LogLevel debug


In 2.4 and later, this tuning can be done **per**-module, as well as
globally:


.. code-block:: text

   LogLevel warn rewrite:trace6


.. _Discussion_Detailed_Errors:

Discussion
~~~~~~~~~~


There are several hierarchical levels of error logging
available, each identified by its own keyword. The default value of
**LogLevel** is **warn**. Listed in descending order of importance, the possible values
are:

``emerg``::
Emergencies; Web server is unusable


``alert``::
Action must be taken immediately


``crit``::
Critical conditions


``error``::
Error conditions


``warn``::
Warning conditions


``notice``::
Normal but significant condition


``info``::
Informational


``debug``::
Debug-level messages


``emerg`` results in the least information being recorded and ``debug`` in the most. However, at ``debug`` level a lot of information will
probably be recorded that is unrelated to the issue you're
investigating, so it's a good idea to revert to the previous setting
when the problem is solved.

In 2.4 and later, additional log levels ``trace1`` through ``trace8``
have been added, to provide trace messages that can be used to
troubleshoot code-level problems. These are also used to replace the
old ``RewriteLog`` functionalty:


.. code-block:: text

   LogLevel warn rewrite:trace5


Even though the various logging levels are hierarchical in
nature, one oddity is that ``notice``
level messages are **always** logged regardless of
the setting of the **LogLevel** directive.

The severity levels are rather loosely defined and even more
loosely applied. In other words, the severity at which a particular
error condition gets logged is decided at the discretion of the
developer who wrote the code—your opinion may differ.

Here are some sample messages of various severities, taken from the
log file of an Apache httpd server:


.. code-block:: text

   [Thu Apr 18 01:37:40 2002] [alert] [client 64.152.75.26] /home/smith/public_html/
        test/.htaccess: Invalid command 'Test', perhaps mis-spelled or defined by a
        module not included in the server configuration
   [Thu Apr 25 22:21:58 2002] [error] PHP Fatal error:  Call to undefined function:
        decode_url(  ) in /usr/apache/htdocs/foo.php on line 8
   [Mon Apr 15 09:31:37 2002] [warn] pid file /usr/apache/logs/httpd.pid overwritten --
        Unclean shutdown of previous Apache run?
   [Mon Apr 15 09:31:38 2002] [info] Server built: Apr 12 2002 09:14:06
   [Mon Apr 15 09:31:38 2002] [notice] Accept mutex: sysvsem (Default: sysvsem)


On a 2.4 server, they would look different, depending on how you have
``ErrorLogFormat`` set (See :ref:`Recipe_Understanding_ErrorLog` for more
details), but might look something like:


.. code-block:: text

   [Mon Jul 13 06:35:16.436308 2015] [authz_core:error] [pid 16776:tid
   139634570925824] [client 155.94.138.10:40830] AH01630: client denied
   by server configuration: /var/www/vhosts/k2/register, referer:
   http://kenya.rcbowen.com/


More information is included in 2.4 error messages, including the
module that is logging the message (``authz_core`` in this case), the
client address (``155.94.138.10``) and an error code (``AH01630``) which
is useful in looking up detailed remediation techniques on your
favorite search engine.

These are fairly normal messages that you might encounter on a
production Web server. If you set the logging level to
Debug, however, you might see many more messages of
cryptic import, such as:


.. code-block:: text

   [Thu Mar 28 10:29:50 2002] [debug] proxy_cache.c(992): No CacheRoot, so no caching. Declining.
   [Thu Mar 28 10:29:50 2002] [debug] proxy_http.c(540): Content-Type: text/html


These are exactly what they seem to be: debugging messages
intended to help an httpd developer figure out what the proxy module
is doing.

And, in the 2.4 version, you can set your ``LogLevel`` to one of the
trace levels to get even more information:


.. code-block:: text

   [Thu Jul 16 21:53:01.342801 2015] [proxy:trace2] [pid 4923:tid
   140434407937792] proxy_util.c(2754): FCGI: fam 2 socket created to
   connect to 127.0.0.1


.. _See_Also_Detailed_Errors:

See Also
~~~~~~~~


* See the detailed documentation of the **LogLevel**

directive at the httpd site: http://httpd.apache.org/docs/mod/core.html#loglevel

* :ref:`Problem_Understanding_ErrorLog`


.. _Recipe_logging_proxied_ipaddress:

Logging a Proxied Client's IP Address
-------------------------------------

.. index:: Logging,logging a proxied client's address

.. index:: Proxies,logging a proxied client's address


.. _Problem_logging_proxied_ipaddress:

Problem
~~~~~~~


You want to log the IP address of the actual client requesting
your pages, even if they're being requested through a proxy.


.. _Solution_logging_proxied_ipaddress:

Solution
~~~~~~~~


.. admonition:: DRAFT — Review needed

   The following content needs editorial review.
   Check technical accuracy, voice/tone, and fit with surrounding content.

Use :module:`mod_remoteip` with the ``RemoteIPHeader`` directive to
replace the connection-level client IP with the address reported in the
``X-Forwarded-For`` header (or a similar header set by your proxy or
load balancer):

.. code-block:: apache

   LoadModule remoteip_module modules/mod_remoteip.so

   RemoteIPHeader X-Forwarded-For
   RemoteIPTrustedProxy 10.0.0.0/8
   RemoteIPTrustedProxy 172.16.0.0/12
   RemoteIPTrustedProxy 192.168.0.0/16


.. _Discussion_logging_proxied_ipaddress:

Discussion
~~~~~~~~~~


.. admonition:: DRAFT — Review needed

   The following content needs editorial review.
   Check technical accuracy, voice/tone, and fit with surrounding content.

When a client connects through a reverse proxy or load balancer, the
IP address that httpd sees is the address of the proxy, not the
original client. Most proxies add an ``X-Forwarded-For`` header
containing the real client IP, but by default httpd ignores this
header and logs only the direct connection's address.

:module:`mod_remoteip` solves this. When loaded, it overrides the
client IP for the connection with the address from the header you
specify in ``RemoteIPHeader``. This affects everything that uses the
client IP — log format tokens like ``%a`` and ``%h``, access control
with ``Require ip``, and environment variables like
``REMOTE_ADDR`` passed to CGI scripts.

**Trust only your proxies.**
The ``RemoteIPTrustedProxy`` directive is essential. Without it,
:module:`mod_remoteip` trusts *any* host presenting the header, which
means a client could forge its IP address by sending a fake
``X-Forwarded-For`` header directly. Always list only the addresses
of your actual proxies and load balancers:

.. code-block:: apache

   # Trust only the load balancer at 10.0.1.50
   RemoteIPTrustedProxy 10.0.1.50

If you have internal proxies on RFC 1918 networks, use
``RemoteIPInternalProxy`` instead — it additionally trusts private
IP addresses reported within the header chain:

.. code-block:: apache

   RemoteIPInternalProxy 10.0.2.0/24

**Multiple proxies.** When a request passes through several proxies,
the ``X-Forwarded-For`` header contains a comma-separated list of
addresses. :module:`mod_remoteip` processes this list from right to
left, stopping at the first address that isn't in the trusted proxy
list. That address becomes the client IP for the request.

**Verifying it works.** After enabling :module:`mod_remoteip`, check
your access log. The ``%a`` format token should now show the real
client address rather than the proxy's address. You can also use the
``%{REMOTE_ADDR}e`` token to confirm the environment variable is set
correctly.


.. _See_Also_logging_proxied_ipaddress:

See Also
~~~~~~~~


* The :module:`mod_remoteip` documentation at
  https://httpd.apache.org/docs/current/mod/mod_remoteip.html

* The HTTP/1.1 specification (RFC 7230-7235) at
  https://httpwg.org/specs/


.. _Recipe_Correlating_error_access:

Correlating error log entries with access log entries
-----------------------------------------------------

.. index:: LogFormat

.. index:: ErrorLogFormat

.. index:: Correlating log entries

.. index:: Logging,ErrorLogFormat

.. index:: Logging,LogFormat

.. index:: Logging,Correlating entries


.. _Problem_Correlating_error_access:

Problem
~~~~~~~


You have the error log and the access log, but it's hard to tell which
error messages go with which access log entries.


.. _Solution_Correlating_error_access:

Solution
~~~~~~~~


Prior to version 2.4, there's no good solution to this, other than
comparing time stamps, which is error prone on very busy servers,
where multiple request may arrive within a given second.

In 2.4, a new log format variable, ``%L``, can be put in both the access
log and the error log, and will log a request ID which can then be
correlated between the two log files.


.. code-block:: text

   LogFormat "%h %t [log id %L] \"%r\"" access_with_id
   CustomLog /var/log/httpd/access_log_id access_with_id
   
   ErrorLogFormat "[%{u}t] [%-m:%l] [log id %L] [pid %P:tid %T]
       %7F: %E: [client\ %a] %M% ,\ referer\ %{Referer}i"
   ErrorLog /var/log/httpd/error_log_id


.. _Discussion_Correlating_error_access:

Discussion
~~~~~~~~~~


A common problem when troubleshooting is attempting to correlate an
error message with the request that resulted in the error condition.

If you have direct access to the server at the exact moment that the
error condition is happening, you can ``tail -f`` both the error log and
the access log, in order to see what conditions happen at the same
time. This can be difficult, though, on a server with any traffic, as
messages will scroll off the screen before you can figure out what's
happening.

Usually, though, you have the error log and the access log, and you're
trying to correlate an error message with the request that happened at
the same time.

Another difficulty, as mentioned in the introduction to this chapter,
is that while error messages are logged immediately when they occur,
access log entries happen only when the request has been completed.
This time lag can occasionally be long enough that it's difficult to
correlate messages.

The ``%L`` log format variable addresses this
difficulty. A unique request ID will be put in each log file that uses
this variable, so that all log entries can be directly correlated.


.. _See_Also_Correlating_error_access:

See Also
~~~~~~~~


* ``ErrorLogFormat`` documentation at
  http://httpd.apache.org/docs/mod/core.html#errorlogformat

* ``LogFormat`` documentation at
  http://httpd.apache.org/docs/mod/mod_log_config.html#logformat


.. _Recipe_Log_MAC_Address:

Logging the value of the MAC address
------------------------------------

.. index:: Logging,MAC address

.. index:: MAC address,Logging


.. _Problem_Log_MAC_Address:

Problem
~~~~~~~


You want to record the MAC (hardware) address of clients that
access your server.


.. _Solution_Log_MAC_Address:

Solution
~~~~~~~~


This cannot be logged reliably in most network situations and
not by httpd at all.


.. _Discussion_Log_MAC_Address:

Discussion
~~~~~~~~~~


The MAC address is not meaningful except on local area networks
(LANs) and is not available in wide area network transactions. When a
network packet goes through a router, such as when leaving a LAN, the
router will typically rewrite the MAC address field with the router's
hardware address. Thus, in practice, the MAC address of the original
client machine making the request is never available to the web server
actually responding to the request.


.. _See_Also_Log_MAC_Address:

See Also
~~~~~~~~


* The TCP/IP protocol specifications (see

http://www.rfc-editor.org/cgi-bin/rfcsearch.pl
and search for "TCP" in the title field)


.. _Recipe_logging_cookies:

Logging Cookies
---------------

.. index:: Cookies

.. index:: Logging,cookies

.. index:: Logging cookies


.. _Problem_logging_cookies:

Problem
~~~~~~~


You want to record all the cookies sent to your server by
clients and all the cookies your server asks clients to set in their
databases; this can be useful when debugging Web applications that use
cookies.


.. _Solution_logging_cookies:

Solution
~~~~~~~~


To log cookies received from the client:


.. code-block:: text

   CustomLog logs/cookies_in.log "%{UNIQUE_ID}e %{Cookie}i"
   CustomLog logs/cookies2_in.log "%{UNIQUE_ID}e %{Cookie2}i"


To log cookie values set and sent by the server to the
        client:


.. code-block:: text

   CustomLog logs/cookies_out.log "%{UNIQUE_ID}e %{Set-Cookie}o"
   CustomLog logs/cookies2_out.log "%{UNIQUE_ID}e %{Set-Cookie2}o"


Use the
%{Set-Cookie}o format variable for debugging cookies. See the Discussion text for
additional details.


.. _Discussion_logging_cookies:

Discussion
~~~~~~~~~~


Cookie fields tend to be very long and complex, so the previous
statements will create separate files for logging them. The cookie log
entries can be correlated against the client request access log using
the server-set ``UNIQUE_ID``
environment variable (assuming that ``mod_unique_id`` is active in the server and
that the activity log format includes the environment variable with a
%{UNIQUE_ID}e format variable).

The ``Cookie`` and ``Set-Cookie`` header fields are the standard
mechanism for HTTP cookies. The older ``Cookie2`` and
``Set-Cookie2`` fields were designed to correct
some of the shortcomings in the original specifications, but they
never achieved widespread adoption and are now obsolete.

Because of the manner in which the syntax of the cookie header
fields has changed over time, these logging instructions may or may
not capture the complete details of the cookies.

Bear in mind that these logging directives will record all
cookies, and not just the ones in which you may be particularly
interested. For example, here is the log entry for a client request
that included two cookies, one named ``RFC2109-1`` and one named ``RFC2109-2``:


.. code-block:: text

   PNCSUsCoF2UAACI3CZs RFC2109-1="This is an old-style cookie, with space characters
        embedded"; RFC2109-2=This_is_a_normal_old-style_cookie


Even though there's only one log entry, it contains information about
two cookies.

On the cookie-setting side, here are the ``Set-Cookie`` header fields
sent by the server in its response header:


.. code-block:: text

   Set-Cookie: RFC2109-1="This is an old-style cookie, with space characters embedded";
        Version=1; Path=/; Max-Age=60; Comment="RFC2109 demonstration cookie"
   Set-Cookie: RFC2109-2=This_is_a_normal_old-style_cookie; Version=1; Path=/; Max-
        Age=60; Comment="RFC2109 demonstration cookie"


And here's the corresponding log entry for the response (this
was all one line in the logfile, so line wrapping was added to make it
all fit on the page):


.. code-block:: text

   eCF1vsCoF2UAAHB1DMIAAAAA RFC2109-1=\"This is an old-style cookie, with space
       characters embedded\"; Version=1; Path=/; Max-Age=60; Comment=\"RFC2109
       demonstration cookie\", RFC2109-2=This_is_a_normal_old-style_cookie;
       Version=1; Path=/; Max-Age=60; Comment=\"RFC2109 demonstration cookie\"





.. _See_Also_logging_cookies:

See Also
~~~~~~~~


* RFC 2109, "HTTP State Management Mechanism" (IETF definition of
  ``Cookie`` and ``Set-Cookie`` header fields) at
  ```ftp://ftp.isi.edu/in-notes/rfc2109.txt`` <``ftp://ftp.isi.edu/in-notes/rfc2109.txt``>`_


* RFC 2965, "HTTP State Management Mechanism" (IETF definition of
  ``Cookie2`` and ``Set-Cookie2`` header fields) at
  ```ftp://ftp.isi.edu/in-notes/rfc2965.txt`` <``ftp://ftp.isi.edu/in-notes/rfc2965.txt``>`_


* The original Netscape cookie proposal at
  http://home.netscape.com/newsref/std/cookie_spec.html


.. _Recipe_dont_log_local:

Not Logging Image Requests from Local Pages
-------------------------------------------

.. index:: Logging,don't log image requests

.. index:: Not logging image requests from local pages


.. _Problem_dont_log_local:

Problem
~~~~~~~


You want to log requests for images on your site, except when
they're requests from one of your own pages. You might want to do this
to keep your logfile size down, or possibly to track down sites that
are hijacking your artwork and using it to adorn their pages.


.. _Solution_dont_log_local:

Solution
~~~~~~~~

.. index:: directives,SetEnvIfNoCase


Use **SetEnvIfNoCase** to restrict logging to only those requests from
outside of your site:


.. code-block:: text

   <FilesMatch \.(jpg|gif|png)$>
       SetEnvIfNoCase Referer "^http://www.example.com/" local_referrer=1
   </FilesMatch>
   CustomLog logs/access_log combined env=!local_referrer


.. _Discussion_dont_log_local:

Discussion
~~~~~~~~~~


In many cases, documents on a Web server include references to
images also kept on the server, but the only item of real interest for
log analysis is the referencing page itself. How can you keep the
server from logging all the requests for the images that happen when
such a local page is accessed?

The **SetEnvIfNoCase** directive will set an environment variable if the
page that linked to the image is from the **www.example.com** site
(obviously, you should replace that site name with your own) and the
request is for a GIF, PNG, or JPEG image.


.. _apacheckbk-CHP-3-NOTE-83:


.. tip::

   .. index:: directives,SetEnvIf

   **SetEnvIfNoCase** is the same as **SetEnvIf** except that variable
   comparisons are done in a case-insensitive manner.


.. index:: directives,CustomLog

The **CustomLog** directive will log all requests that do not have that
environment variable set, **i.e.**, everything except requests for
images that come from links on your own pages.

This recipe only works for clients that actually report the
referring page. Some people regard the URL of the referring page to be
no business of anyone but themselves, and some clients permit the user
to select whether to include this information or not. There are also
'anonymizing' sites on the Internet that act as proxies and conceal
this information.


.. _See_Also_dont_log_local:

See Also
~~~~~~~~


* :ref:`Recipe_image-theft`


.. _Recipe_Rotate_By_Time:

Rotating Logfiles at a Particular Time
--------------------------------------

.. index:: Commands,rotatelogs

.. index:: Logging,rotation of files

.. index:: Rotating log files; see Logging,rotation of log files

.. index:: CustomLog; see directives,CustomLog


.. _Problem_Rotate_By_Time:

Problem
~~~~~~~


You want to automatically roll over the httpd logs every day
without having to shut down and restart the server.


.. _Solution_Rotate_By_Time:

Solution
~~~~~~~~

.. index:: directives,CustomLog

.. index:: Commands,rotatelogs


Use **CustomLog** and the **rotatelogs** program:


.. code-block:: text

   CustomLog "| /usr/sbin/rotatelogs /var/log/httpd/access_log.%Y-%m-%d 86400" combined


.. _Discussion_Rotate_By_Time:

Discussion
~~~~~~~~~~


The **rotatelogs** script is designed to use an httpd feature called
piped logging, which is just a fancy name for sending log output to
another program rather than to a file. By inserting the **rotatelogs**
script between the Web server and the actual logfiles on disk, you can
avoid having to restart the server to create new files; the script
automatically opens a new file at the designated time and starts
writing to it.

.. index:: functions,strftime(3)

The first argument to the
**rotatelogs** script is the base name of the file to which records
should be logged. If it contains one or more **``%``** characters, it
will be treated as a ``strftime(3)`` format string; otherwise, the
rollover time (in seconds since 1 January 1970), in the form of a
10-digit number, will be appended to the base name. For example, a
base name of ``foo`` would result in logfile names like
**foo.1020297600**, whereas a base name of ``foo.%Y-%m-%d`` would cause
the logfiles to be named something like **foo.2002-04-29**.

The second argument is the interval (in seconds) between
rollovers. Rollovers will occur whenever the system time is a multiple
of this value. For instance, a 24-hour day contains 86,400 seconds; if
you specify a rollover interval of 86400, a new logfile will be
created every night at midnight — when the system time, which is based
at representing midnight on 1 January 1970, is a multiple of 24
hours.


.. _apacheckbk-CHP-3-NOTE-85:


.. tip::

   Note that the rollover interval is in actual clock seconds
   elapsed, so when time changes because of daylight savings, this does
   not in any way affect the interval between rollovers.


.. _See_Also_Rotate_By_Time:

See Also
~~~~~~~~


* The **rotatelogs** manpage; try:


.. code-block:: text

   man rotatelogs


* **rotatelogs** documentation online at http://httpd.apache.org/docs/programs/rotatelogs.html


.. _Recipe_System_logrotate:

Rotating Logs on the First of the Month
---------------------------------------

.. index:: Commands,logrotate

.. index:: Logile rotation,by system; see Logging,rotation of files

.. index:: Logfile rotation,monthly

.. index:: Logfile rotation

.. index:: Rotating log files; see Logfile rotation


.. _Problem_System_logrotate:

Problem
~~~~~~~


You want to close the previous month's logs and open new ones on
the first of each month.


.. _Solution_System_logrotate:

Solution
~~~~~~~~


Use your operating system's **logrotate** facility.


.. _Discussion_System_logrotate:

Discussion
~~~~~~~~~~


**rotatelogs**, mentioned in an earlier recipe, has a number of useful
features, but does not, at this time, have a way to specify a specific
date and time to rotate your log files. However, almost every Unix
system comes equipped with a log rotate facility, usually called
**logrotate**.

While the exact details of this utility will vary from one system to
another, typically there's a configuration file called
**``/etc/logrotate.conf``** and a directory of service-specific
configuration files, often in **``/etc/logrotate.d``**.

Create a file in that directory called **httpd** with the following
contents:


.. code-block:: text

   /var/log/httpd/*log {
       monthly
       missingok
       notifempty
       sharedscripts
       delaycompress
       postrotate
           /bin/systemctl reload httpd.service > /dev/null 2> /dev/null || true
       endscript
   }


.. tip::

   The syntax used here is specific to Fedora, RHEL, and
   other RPM-based distributions, but it will be similar
   on other Unixes. In particular, you'll need to update the ``postrotate``
   section to reflect your system's method of restarting services.


See the documentation for **logrotate** for other options that are
available to you.


.. _See_Also_System_logrotate:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/logs.html#piped

* **``man logrotate``**

* :ref:`Recipe_Rotate_By_Time`


.. _Recipe_Log_Hostnames:

Logging Hostnames Instead of IP Addresses
-----------------------------------------

.. index:: Logging,hostnames

.. index:: Logging,IP addresses

.. index:: directives,HostnameLookups

.. index:: Log hostnames

.. index:: Commands,logresolve


.. _Problem_Log_Hostnames:

Problem
~~~~~~~


You want to see hostnames in your activity log instead of IP
addresses.


.. _Solution_Log_Hostnames:

Solution
~~~~~~~~


You can let the Web server resolve the hostname when it
processes the request by enabling runtime lookups with the httpd
directive:


.. code-block:: text

   HostnameLookups On


Or you can let httpd use the IP address during normal
processing and then postprocess the log file using the **logresolve**
program that comes with the server.


.. code-block:: text

   logresolve -c < access_log.raw > access_log.resolved


The latter method is greatly recommended, for reasons of performance.


.. _Discussion_Log_Hostnames:

Discussion
~~~~~~~~~~


The httpd activity logging mechanism can record either the
client's IP address or its hostname (or both). Logging the hostname
directly requires that the server spend some time to perform a DNS
lookup to turn the IP address (which it already has) into a hostname.
This can have some serious impact on the server's performance,
however, because it needs to consult the name service in order to turn
the address into a name; and while a server child or thread is busy
waiting for that, it isn't handling client requests.

The alternative suggested in the solution above is to have the
server record only the client's IP address and resolve the address to
a name afterwards, perhaps even on a different system that is not
handling Web traffic, so that it won't impact your server's
performance.

In theory, this is an excellent choice; in practice, however,
there are some pitfalls. For one thing, the
**logresolve** application included with httpd
(usually installed in the **``bin/``** subdirectory under the ``ServerRoot``)
will only resolve IP addresses that appear at the very beginning of
the log entry, and so it's not very flexible if you want to use a
nonstandard format for your logfile.

For another, if too much time passes between the collection and
resolution of the IP addresses, the DNS may have changed sufficiently
so that misleading or incorrect results may be obtained. This is
especially a problem with dynamically allocated IP addresses such as
those issued by home service ISPs. Although, for these dynamically
allocated IP addresses, the hostnames tend not to be particularly
informative anyway.

In practice, however, all log analysis software provides
hostname resolution functionality, and it generally makes most sense
to use that functionality than trying to resolve the IP addresses in
the logfile before that stage.


.. _See_Also_Log_Hostnames:

See Also
~~~~~~~~


* The **logresolve** manpage: **``man logresolve``**

* http://httpd.apache.org/docs/programs/logresolve.html

* :ref:`Recipe_Log_Analysis`


.. _Recipe_Per_Vhost_Log:

Maintaining Separate Logs for Each Virtual Host
-----------------------------------------------

.. index:: Logging,Virtual hosts

.. index:: Virtual hosts,logging

.. index:: directives,VirtualHost

.. index:: directives,CustomLog

.. index:: Maintaining separate logs for each virtual host

.. index:: Commands,split-logfile


.. _Problem_Per_Vhost_Log:

Problem
~~~~~~~


You want to have separate activity logs for each of your virtual
hosts.


.. _Solution_Per_Vhost_Log:

Solution
~~~~~~~~


Unless you have many hundr eds of virtual hosts, it is simpler to have
a **CustomLog** directive for each **&lt;VirtualHost&gt;** declaration. See
:ref:`Recipe_log_per_vhost`

However,
once you get to a certain number, you'll notice performance
degradation due to the large number of open file handles.

In this case, combine your log files, with a custom log file format
that inserts the answering hostname:


.. code-block:: text

   LogFormat "%v %h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"" combined_plus_vhost
   CustomLog logs/access_log combined_plus_vhost


Then, once your log file has been rotated (See
:ref:`Recipe_System_logrotate` and :ref:`Recipe_Rotate_By_Time`), split the
log file up using the **split-logfile** program that comes with the
httpd.


.. code-block:: text

   split-logfile < access_log


This will produce one log file **per** virtual host.


.. _Discussion_Per_Vhost_Log:

Discussion
~~~~~~~~~~


In order for **split-logfile** to work, the logging format you're using
must begin with "``%v``". This inserts the name of the virtual host at
the beginning of each log entry; **split-logfile** will use this to
figure out to which file the entry should be written. The hostname
will be removed from the record before it gets written.

One log file will be created for each hostname that answered requests.
For example, the log entries for the ``www.example.org`` virtual host
will be put in a file named **``www.example.org.log``**.


.. _See_Also_Per_Vhost_Log:

See Also
~~~~~~~~


* :ref:`Recipe_Log_Hostnames`

* http://httpd.apache.org/docs/programs/split-logfile.html
  - **split-logfile** documentation

* :ref:`Recipe_log_per_vhost`


.. _Recipe_Logging_Proxy:

Logging Proxy Requests
----------------------

.. index:: Proxies,logging

.. index:: Logging proxy requests


.. _Problem_Logging_Proxy:

Problem
~~~~~~~


You want to log requests that go through your proxy to a
different file than the requests coming directly to your
server.


.. _Solution_Logging_Proxy:

Solution
~~~~~~~~

.. index:: directives,SetEnv

.. index:: directives,CustomLog

Use the **SetEnv** directive to
earmark those requests that came through the proxy server, in order to
trigger conditional logging:


.. code-block:: text

   <Proxy *>
       SetEnv is_proxied 1
   </Proxy>
   CustomLog logs/proxy_log combined env=is_proxied


.. _Discussion_Logging_Proxy:

Discussion
~~~~~~~~~~


The **<Proxy **>* block will be applied to all proxied requests.
**SetEnv** sets an
environment variable which can then be used to trigger conditional
logging with the **CustomLog** directive.

If you wanted to log only requests that were **not** proxied, you could
negate the conditional:


.. code-block:: text

   CustomLog logs/proxy_log combined env=!is_proxied


.. _See_Also_Logging_Proxy:

See Also
~~~~~~~~


* _mod_log_config_ documentation at
  http://httpd.apache.org/docs/mod/mod_log_config.html

* The **Conditional Logs** section on
  http://httpd.apache.org/docs/logs.html#accesslog


.. _Recipe_Logging_server_ip:

Logging Server IP Addresses
---------------------------

.. index:: Logging,server IP address


.. _Problem_Logging_server_ip:

Problem
~~~~~~~


You want to log the IP address of the server that responds to a
request, possibly because you have virtual hosts with multiple
addresses each.


.. _Solution_Logging_server_ip:

Solution
~~~~~~~~

.. index:: directives,LogFormat

.. index:: directives,CustomLog


Use the ``%A`` format variable in a **LogFormat** or **CustomLog** directive:


.. code-block:: text

   CustomLog logs/served-by.log "%A"


.. _Discussion_Logging_server_ip:

Discussion
~~~~~~~~~~


The ``%A`` logging directive signals the activity
logging system to insert the local IP address—that is, the address of
the server—into the log record at the specified point. This can be
useful when your server handles multiple IP addresses. For example,
you might have a configuration that includes elements such as the
following:


.. code-block:: text

   Listen 10.0.0.42
   Listen 192.168.19.243
   Listen 263.41.0.80
   <VirtualHost 192.168.19.243>
       ServerName private.example.com
   </VirtualHost>
   <VirtualHost 10.0.0.42 263.41.0.80>
       ServerName foo.example.com
       ServerAlias bar.example.com
   </VirtualHost>


This might be meaningful if you want internal users to access
**Foo.Example.Com** using the ``10.0.0.42`` address rather than the one
published to the rest of the network (such as to segregate internal
from external traffic over the network cards). The second virtual host
is going to receive requests aimed at both addresses even though it
has only one ``ServerName``; using the
``%A`` directive in your log format can help you determine
how many hits on the site are coming in over each network
interface.


.. _See_Also_Logging_server_ip:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_log_config.html
  - _mod_log_config_ documentation


.. _Recipe_Logging_request_header:

Logging Arbitrary Request Header Fields
---------------------------------------

.. index:: Logging,request headers

.. index:: Logging arbitrary request header fields


.. _Problem_Logging_request_header:

Problem
~~~~~~~


You want to record the values of arbitrary fields clients send
to their request header, perhaps to tune the types of content you have
available to the needs of your visitors.


.. _Solution_Logging_request_header:

Solution
~~~~~~~~


Use the **``%{...}i``** log format directive in your
access log format declaration. For example, to log the ``Host`` header,
you might use:


.. code-block:: text

   %{Host}i


.. _Discussion_Logging_request_header:

Discussion
~~~~~~~~~~


The HTTP request sent by a Web browser can be very complex, and
if the client is a specialized application rather than a browser, it
may insert additional metadata that's meaningful to the server. For
instance, one useful request header field is the ``Accept`` field, which tells the server what
kinds of content the client is capable of and willing to receive.
Given a **CustomLog** line such as this:
.. index:: directives,CustomLog


.. code-block:: text

   CustomLog logs/accept_log "\"%{Accept}i\""


a resulting log entry might look like this:


.. code-block:: text

   PNb6VsCoF2UAAH1dAUo "text/html, image/png, image/jpeg, image/gif,
        image/x-xbitmap, */*"


This tells you that the client that made that request is
explicitly ready to handle HTML pages and certain types of images,
but, in a pinch, will take whatever the server gives it (indicated by
the wildcard ``\**/\**`` entry).


.. _See_Also_Logging_request_header:

See Also
~~~~~~~~


* :ref:`Problem_Understanding_Combined_Log_Format`

* :ref:`Recipe_Logging_response_header`


.. _Recipe_Logging_response_header:

Logging Arbitrary Response Header Fields
----------------------------------------

.. index:: Logging,response headers

.. index:: Logging arbitrary response header fields


.. _Problem_Logging_response_header:

Problem
~~~~~~~


You want to record the values of arbitrary fields the server has
included in a response header, probably to debug a script or
application.


.. _Solution_Logging_response_header:

Solution
~~~~~~~~


Use the **``%{...}o``** log format directive in your
access log format declaration. For example, to log the ``Last-Modified``
header field value, you would do the following:


.. code-block:: text

   %{Last-Modified}o


.. _Discussion_Logging_response_header:

Discussion
~~~~~~~~~~


The HTTP response sent by httpd when answering a request can be
very complex, according to the server's configuration. Advanced
scripts or application servers may add custom fields to the server's
response, and knowing what values were set may be of great help when
trying to track down an application problem.

Other than the fact that you're recording fields the server is
**sending** rather than receiving, this recipe is
analogous to :ref:`Recipe_Logging_request_header` in this
chapter; refer to that recipe for more details. The only difference in
the syntax of the logging format variable is that response fields are
logged using an **``o``** directive, and request fields are
logged using **``i``**.


.. _See_Also_Logging_response_header:

See Also
~~~~~~~~


* :ref:`Recipe_Logging_request_header`


.. _Recipe_logging_to_syslog:

Logging to syslog
-----------------

.. index:: syslog

.. index:: Logging to syslog

.. index:: Logging,syslog


.. _Problem_logging_to_syslog:

Problem
~~~~~~~

You want to send your log entries to syslog.


.. _Solution_logging_to_syslog:

Solution
~~~~~~~~

To log your error log to syslog, simply tell httpd to log to
**syslog**:


.. code-block:: text

   ErrorLog syslog:local6.info


.. note::

   Some other **syslog** reporting
   class than user, such as ``local1``
   might be more appropriate in your environment. Consult with your
   sysadmin for details of your local syslog configuration.


Logging your access log to syslog takes a little more work. Add
the following to your configuration file:


.. code-block:: text

   CustomLog "| /usr/bin/logger -t apache -p local6.info" combined


This will use the **logger** utility, which is standard on any Unix
system, to log to the **local6.info** syslog facility.


.. _Discussion_logging_to_syslog:

Discussion
~~~~~~~~~~


There are several compelling reasons for logging to syslog. The first
of these is to have many servers log to a central logging
facility. The second is that there are many existing tools for
monitoring syslog and sending appropriate notifications on certain
events. Allow httpd to take advantage of these tools,
and your particular installation may benefit. Also, in the event that
your server is either compromised, or has some kind of catastrophic
failure, having logfiles on a dfferent physical machine can be of
enormous benefit in finding out what happened.

httpd supports logging your error log to syslog by default.
This is by far the more useful log to handle this way, since syslog is
typically used to track error conditions, rather than merely
informational messages.

.. index:: directives,ErrorLog

The syntax of the **ErrorLog**
directive allows you to specify ``syslog`` as an argument, or to specify a
particular syslog facility. In this example, the ``local6`` syslog
facility was specified. In your **``/etc/syslog.conf``** file, you can
specify where a particular log facility should be sent—whether to a
file, or to a remote syslog server.

For example, to send these log files to a remote server, you might put
the following in **syslog.conf**:


.. code-block:: text

   # <level> @<IP>:<port>
   local6.info @10.11.12.13:514


Because httpd does not support logging your access log to
syslog by default, you need to accomplish this with a piped logfile
directive.

Consult your **syslogd** manual
for further detail on setting up a networked syslog server.


.. _See_Also_logging_to_syslog:

See Also
~~~~~~~~


* The man pages for **syslogd** and **syslog.conf**

* The docs for **logger**: **``man logger``**

* http://rafaelsteil.com/apache-remote-logging-with-rsyslog/


.. _Recipe_Logging_userdir:

Logging User Directories
------------------------

.. index:: Logging,User directories

.. index:: userdir,Logging

.. index:: mod_userdir

.. index:: Modules,mod_userdir

.. index:: mod_macro

.. index:: Modules,mod_macro


.. _Problem_Logging_userdir:

Problem
~~~~~~~


You want each user directory web site (**i.e.**, those that are
accessed **via** http://server/~username)
to have its own logfile.


.. _Solution_Logging_userdir:

Solution
~~~~~~~~


.. index:: directives,RewriteRule

.. index:: directives,LogFormat

.. index:: directives,CustomLog

Use the following **RewriteRule** to trigger on userdir requests, and
invoke conditional logging.


.. code-block:: text

   RewriteRule ^/~([^/]+)/ - [E=userdir:$1]
   LogFormat "%{userdir}e %h %l %u %t \"%r\" %>s %b" common
   CustomLog logs/userdir_logs common env=userdir


.. index:: Commands,split-logfile

Then use **split-logfile** to break up the log file afterwards.


.. code-block:: text

   split-logfile < userdir_logs


.. index:: Modules,mod_macro

Or, with 2.4, use a combination of _mod_macro_ and **per**-directory
logging to give each user his or her own log file:


.. code-block:: text

   <Macro userdirlog $username>
     <Directory /home/$username/public_html>
       CustomLog /var/log/httpd/logs/$username.access_log combined
     </Directory>
   </Macro>


You will need to invoke this macro for each user for whom you wish to
provide a log file:


.. code-block:: text

   Use userdirlog rbowen
   Use userdirlog rhiannon
   Use userdirlog jbrose


.. _Discussion_Logging_userdir:

Discussion
~~~~~~~~~~


In many hosting situations, rather than having virtual hosts, users
run their website in their home directory, and have a userdir type
URL. That is, a user named, for example, ``rbowen``, would have a
website address of ``http://pages.example.com/~rbowen`` and the module
_mod_userdir_ will map those requests to their home directory.
.. index:: Modules,mod_userdir


In these situations, however, users are typically unable to view their
own log files without having to filter through the requests to
everyone else's website as well.

This recipe attempts to give each user their own log file, to make it
easier to track their own requests.

The first line of the recipe inspects the URL, and if it is a userdir
request, it puts the username in an environment variable named
**userdir**:


.. code-block:: text

   RewriteRule ^/~([^/]+)/ - [E=userdir:$1]


The regular expression **``^/~([^/]+)/``** matches a URI request
that starts with **``~``**, and captures everything up to the first
slash - **i.e.**, the username.

The next two lines of the recipe create a custom log file format named
'userlog' which looks just like the **common** log file format, but puts
the **userdir** environment variable on the start of the line, so that
you know whose request it was.


.. code-block:: text

   LogFormat "%{userdir}e %h %l %u %t \"%r\" %>s %b" userlog
   CustomLog logs/userdir_logs userlog env=userdir


Finally, you periodically rotate the log file out, and, using the
**split-logfile** script, you split that log file into one **per** username.

See :ref:`Recipe_Per_Vhost_Log` for more discussion of the
**split-logfile** utility.

The biggest problem with this approach is that the user does not have
a live log file. That is to say, they don't have their own individual
log file until after you have rotated and post-processed the log file.
This means that while they can do periodic traffic statistical
analysis, and otherwise investigate their traffic after the fact, they
can't do real-time debugging of their site, since the live log file
intermingles all of the various website requests.

This could be partially addressed by piping the log file through
**grep** to isolate their own log entries:
.. index:: Commands,grep

.. index:: Commands,tail


.. code-block:: text

   tail -f /var/log/httpd/logs/userdir_logs | egrep '^rbowen '


The command above, for example would isolate the requests that were
made to the web space of a user named ``rbowen``.

A somewhat more elaborate approach could be done with httpd 2.4 using
_mod_macro_ and **per**-directory logging.
.. index:: Modules,mod_macro


First, you create the macro:


.. code-block:: text

   <Macro userdirlog $username>
     <Directory /home/$username/public_html>
       CustomLog /var/log/httpd/logs/$username.access_log combined
     </Directory>
   </Macro>


Then, each time you add a new user account, add an invocation of this
macro to your configuration file for that user:


.. code-block:: text

   Use userdirlog rbowen
   Use userdirlog sungo
   Use userdirlog dpitts


This will create a unique log file for each user who has requests
going to their home directory.

This approach has the small disadvantage that for systems with many
thousands of users, you'll end up having thousands of open file
handles, which can significantly affect file system performance.


.. _See_Also_Logging_userdir:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_log_config.html

* http://httpd.apache.org/docs/programs/split-logfile.html

* http://httpd.apache.org/docs/mod/mod_macro.html

* :ref:`Recipe_Per_Vhost_Log`


.. refcosplay

.. _Recipe_Logging_environment_variables:

Logging environment variables
-----------------------------

.. index:: Logging,Environment variables

.. index:: Environment variables,Logging

.. index:: mod_log_config

.. index:: Modules,mod_log_config

.. index:: directives,LogFormat

.. index:: LogFormat


.. _Problem_Logging_environment_variables:

Problem
~~~~~~~


You want to log the value of particular environment variable.


.. _Solution_Logging_environment_variables:

Solution
~~~~~~~~


Use the **``%{``**``VARNAME``**``}e``** logging template to log that variable. For
example, to log a variable named **HairColor**, you'd do the following:


.. code-block:: text

   LogFormat %{HairColor}e haircolor
   CustomLog /var/log/httpd/haircolor.log haircolor


.. _Discussion_Logging_environment_variables:

Discussion
~~~~~~~~~~


Any environment variable may be logged using the **``**``{...}``**``e`** variable in a
**LogFormat** declaration.

Presumably you'd also want to add some other identifying information,
such as a time stamp and the request, to a log entry, so that the log
file was more useful than merely a list of values.

However, just having an anonymized list of values might be useful for
use in generating statistics. For example, if you just wanted to count
the occurrences of various values in your **haircolor** log file, you
could pipe the file through **uniq** to count these items:
.. index:: Commands,uniq

.. index:: Commands,sort


.. code-block:: text

   % sort haircolor.log | uniq.log


This will result in a list of the various unique entiries in the log
file, and the number of times they occur:


.. code-block:: text

       25  brown
       78  red
       12  bald
       98  black


.. _See_Also_Logging_environment_variables:

See Also
~~~~~~~~


* :ref:`Recipe_LogFormat`

* :ref:`Recipe_Securing_Logfiles`


.. _Recipe_logging_logio:

Logging the size of uploaded content
------------------------------------

.. index:: mod_logio

.. index:: Modules,mod_logio

.. index:: Modules,mod_log_config

.. index:: Logging,Full upload and download sizes

.. index:: Logging the size of uploaded content


.. _Problem_logging_logio:

Problem
~~~~~~~


_mod_log_config_ usually only logs the size of downloaded files. You
want to log the complete amount of data transferred, including
uploaded files.


.. _Solution_logging_logio:

Solution
~~~~~~~~


Use _mod_logio_ to log the complete data upload and download sizes.


.. code-block:: text

   LogFormat "%h %t \"%r\" %b %I %O" combined_io
   CustomLog logs/access_io.log combined_io


The ``%I`` variable will log the total bytes of input, and ``%O`` will log
the total bytes of output. These both include the HTTP headers.


.. _Discussion_logging_logio:

Discussion
~~~~~~~~~~


_mod_logio_ must be loaded to use this recipe. That is, your
configuration file must contain a **LoadModule** directive, something
like:
.. index:: directives,LoadModule


.. code-block:: text

   LoadModule logio_module modules/mod_logio.so


The ``%b`` log directive which is used in most access log formats logs
the size of data sent to the client, not including HTTP headers. Thus,
if you're really interested in how much data you're using, this is
only part of the picture, missing not only the HTTP headers, but also
the size of the request. The request can be large if you allow file
uploads, or if you have very large HTTP POST forms on your site.

Using _mod_logio_, you can capture the rest of the data transfer size.

``%I`` logs the entire size of the request, including headers and any
POST data, including file uploads.

``%O`` logs the entire size of the response, including headers.

In httpd 2.4.7, there's also a ``%S`` directive that logs the total bytes
transferred, both sent and received, including the request and the
headers.


.. _See_Also_logging_logio:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_logio.html


.. _Recipe_log_forensic:

Logging incomplete requests
---------------------------

.. index:: mod_log_forensic

.. index:: Modules,mod_log_forensic

.. index:: Long-lived requests

.. index:: Logging,incomplete requests


.. _Problem_log_forensic:

Problem
~~~~~~~


You want to identify requests that never complete.


.. _Solution_log_forensic:

Solution
~~~~~~~~


Use _mod_log_forensic_ to log requests that never complete.


.. code-block:: text

   ForensicLog logs/forensic.log


.. _Discussion_log_forensic:

Discussion
~~~~~~~~~~


_mod_log_forensic_ must be loaded to use this recipe. That is, your
configuration file must contain a **LoadModule** directive, something
like:
.. index:: directives,LoadModule


.. code-block:: text

   LoadModule log_forensic_module modules/mod_log_forensic.so


Using the recipe above will create a log file that logs two entries
for every request - one when the request is received, and one when the
response has been sent and the request completed.

Each initial log entry will look something like:


.. code-block:: text

   +yQtJf8CoAB4AAFNXBIEAAAAA|GET /manual/de/images/down.gif
   HTTP/1.1|Host:localhost%3a8080|User-Agent:Mozilla/5.0 (X11; U; Linux
   i686; en-US; rv%3a1.6) Gecko/20040216 Firefox/0.8|Accept:image/png,
   etc...


.. index:: Modules,mod_unique_id

If you're using _mod_unique_id_, its generated ID number will be used.
Otherwise, _mod_log_forensic_ will create its own unique identifier
and use that.

When the request is completed, only the ID number is logged:


.. code-block:: text

   -yQtJf8CoAB4AAFNXBIEAAAAA


By correlating these two log entries, you can identify which requests
never completed, and, thus, what resources on your website may be
long-running, or crashing the server before the request is completed.

.. index:: Commands,check_forensic

The script _check_forensic_, which comes with the server, does that
correlation for you.


.. code-block:: text

   % check_forensic forensic.log


The output of this script will be a list of requests that don't have a
matching end-of-request log entry.


.. tip::

   The _check_forensic_ script is often not installed in your execution
   path when the server is installed. It is located in the **support**
   directory of the source tree, and may be found at
   ``https://svn.apache.org/repos/asf/httpd/httpd/trunk/support/check_forensic``
   if you're unable to locate it on your system.


You can also add the unique identifier to your access log using the
**``%{``***``forensic-id``***``}n``** log format variable, for easier
correlation with the associated log file entry.


.. _See_Also_log_forensic:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/trunk/mod/mod_log_forensic.html

* https://svn.apache.org/repos/asf/httpd/httpd/trunk/support/check_forensic


.. _Recipe_log_debug:

Logging your own custom messages
--------------------------------

.. index:: mod_log_debug

.. index:: Modules,mod_log_debug

.. index:: Logging,Debug

.. index:: Logging,custom log messages

.. index:: directives,LogMessage


.. _Problem_log_debug:

Problem
~~~~~~~


You'd like to insert your own messages into the error log as part of
debugging some problem.


.. _Solution_log_debug:

Solution
~~~~~~~~


Use _mod_log_debug_ to create custom error log messages, and trigger
them at specified times.

For example, to log that a particular directory has been requested:


.. code-block:: text

   <Location "/ponies/">
     LogMessage "A resource from /ponies/ has been requested"
   </Location>


Or, if you want to only log under certain conditions, these can be
specified. The following recipe, for example, will log every time you
get a request from an IPv6 address.


.. code-block:: text

   LogMessage "IPv6 address %{REMOTE_ADDR} requested a resource." "expr=-T %{IPV6}"


.. _Discussion_log_debug:

Discussion
~~~~~~~~~~


The _mod_log_debug_ module was created to make it easier to debug
situations by inserting log file entries at strategic times.


.. tip::

   _mod_log_debug_ is only available in version 2.4.


The module can use the expression engine to evaluate arbitrary
conditions, and insert log entries based on their values. It can also
be tied to a particular hook - that is, a particular phase of the
request handling process.

For example, to log the value of a particular variable at a specific
moment in the request handling process, you can specify that hook in
the argument to **LogMessage**:


.. code-block:: text

   LogMessage "Username is %{REMOTE_USER}" hook=check_authn


If you wanted to track the value of a particular variable across all
requests, to see how and when it had changed, you could specify
``hook=all``, and one log entry would appear for each of the various
hooks. This would also allow you to determine how much time (in
microseconds) were being spent in each part of the request processing.


.. _See_Also_log_debug:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_log_debug.html

* :ref:`Chapter_per_request`, **Programmable Configuration**


.. _Recipe_Logging_POST:

Logging POST Contents
---------------------

.. index:: mod_dumpio

.. index:: Modules,mod_dumpio

.. index:: Logging,POST

.. index:: POST,Logging


.. _Problem_Logging_POST:

Problem
~~~~~~~


You want to record data submitted with the POST method, such as
from a Web form.


.. _Solution_Logging_POST:

Solution
~~~~~~~~


Ensure that _mod_dumpio_ is loaded,
and put the following in your configuration file:
.. index:: directives,DumpIOLogLevel

.. index:: directives,DumpIOInput


.. code-block:: text

   DumpIOLogLevel debug
   DumpIOInput On


.. _Discussion_Logging_POST:

Discussion
~~~~~~~~~~


_mod_dumpio_ is a debugging module which can log the contents of the
request, including the POST values. When configured as above, it will
log the entirety of the request body.

The **DumpIOLogLevel** directive specifies at which log level these
messages will appear. For example, if you set it to **debug**, then
you'll only see this information when **LogLevel** is set to **debug**.
.. index:: directives,LogLevel


Log entries for POST data will look like:


.. code-block:: text

   [Sun Feb 11 16:49:27 2007] [debug] mod_dumpio.c(51): mod_dumpio:dumpio_in (data-HEAP): 11 bytes
   [Sun Feb 11 16:49:27 2007] [debug] mod_dumpio.c(67): mod_dumpio: dumpio_in (data-HEAP): fname=Larry
   


In the log entry shown here, the form value
**fname** was set to **Larry**.

The output from _mod_dumpio_
is very noisy. A typical request may generate somewhere between 30 and
50 lines of log entries. The entry shown here is just a tiny part of
what was logged with the **POST**.

.. index:: Logging,Sensitive information


.. warning::

   **Use with care and disable when done**

   Logging POST data is potentially very dangerous in terms of data
   security. Consider, for example, if you are collecting personal
   information (social security numbers, phone numbers, home addresses)
   or financial information (credit card numbers), and this information
   ends up in a log file which is later stolen somehow. All of that
   information will be stored, plain text, in that log file.


Carefully consider what information you log, and how long you retain
it, to ensure that you don't end up having sensitive information
leaked when your site is compromised.

See :ref:`Recipe_Securing_Logfiles` for further discussion of this point.


.. _See_Also_Logging_POST:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_dumpio.html

* :ref:`Chapter_Security`, **Security**

* :ref:`Recipe_Securing_Logfiles`

* :ref:`Recipe_dumpio`


.. _Recipe_dumpio:

Logging the HTTP response
-------------------------

.. index:: mod_dumpio

.. index:: Modules,mod_dumpio

.. index:: Logging,HTTP Response


.. _Problem_dumpio:

Problem
~~~~~~~


You want to log everything that is sent back to the client (**i.e.**, the
HTTP response).


.. _Solution_dumpio:

Solution
~~~~~~~~


Ensure that _mod_dumpio_ is loaded, and put the following in your
configuration file:
.. index:: directives,DumpIOLogLevel

.. index:: directives,DumpIOOutput


.. code-block:: text

   DumpIOLogLevel debug
   DumpIOOutput On


.. _Discussion_dumpio:

Discussion
~~~~~~~~~~


Like the recipe immediately above, this recpie uses _mod_dumpio_ to
log aspects of the HTTP transaction. In this case, it logs the
entirety of the HTTP response, including headers, and the complete
body of the document returned. So, for example, if the request was for
an HTML document, the complete contents of that document will be
logged.

While this is enormously useful for debugging, it does create very
large log files, very quickly, so use sparingly, and don't leave this
enabled in production.


.. warning::

   **Potential for logging sensitive information**

   The security warning in the recipe above is also relevant here. Be very
   cautious about logging potentially sensitive information, as it makes
   this information available to anyone that compromises your system.


See :ref:`Recipe_Securing_Logfiles` for further discussion of this topic.


.. _See_Also_dumpio:

See Also
~~~~~~~~


* :ref:`Recipe_Securing_Logfiles`

* :ref:`Recipe_Logging_POST`


.. _Recipe_Log_Analysis:

Log Analysis
------------

.. index:: Logging,Analysis

.. index:: Logging,Statistics

.. index:: Log file analysis


.. _Problem_Log_Analysis:

Problem
~~~~~~~


You want to generate some statistics from the log files that you're
collecting.


.. _Solution_Log_Analysis:

Solution
~~~~~~~~


There are a wide variety of third-party products for extracting useful
statistics from the log files that you're collecting.

Some of the most popular Open Source options are listed here:


.. _Analytics_software:


**Popular log file analytics software**


+-----------+---------------------------+
| Name      | URL                       |
+-----------+---------------------------+
| AWStats   | http://www.awstats.org/   |
+-----------+---------------------------+
| GoAccess  | http://goaccess.io/       |
+-----------+---------------------------+
| Webalizer | http://www.webalizer.org/ |
+-----------+---------------------------+


There are, additionally, many proprietary options, such as Sawmill,
and also options that provide live analysis, rather than processing your
log files, such as Google Analytics and Mint.


.. _Discussion_Log_Analysis:

Discussion
~~~~~~~~~~


In the past, analyzing httpd log files was the most popular way to
generate statistics about traffic to your website. However, it is now
much more common to use JavaScript-based solutions, like Google
Analytics, to provide real-time tracking of website access.

If you are more concerned about data security, you may opt to analyse
your log files yourself, and that's where the server-side programs,
like those listed in the table above, are useful.

At the websites listed above, you can see examples of the graphs and
tables that can be generated from your log files, giving you insight
into the trends of your audience, as well as what you might do to
improve your site, based on what parts are more visited than others.


.. _See_Also_Log_Analysis:

See Also
~~~~~~~~


* https://en.wikipedia.org/wiki/List_of_web_analytics_software

Summary
-------


The Apache HTTP Server provides a large number of ways to collect logs of what
happens on your server. In this chapter I've covered all of the
standard logging modules, as well as a handful of third-party tools.
