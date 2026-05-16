.. _Chapter_Logging:

=======
Logging
=======

.. epigraph::

   "There are those quintessential moments in a man's life: Losing
   his virginity; getting married; becoming a father; and having the
   right girl smile at him."

   -- *St. Elmo's Fire*


.. index:: Logging

.. index:: Log files

.. index:: Access log

.. index:: Error log


Every request that arrives at your server tells a story. Who asked for
what, when they asked, how long it took, and whether it worked. Your
log files are the only witnesses to these stories, and if you haven't
configured them well, those witnesses are useless — either mute or
babbling incoherently.

Apache HTTP Server provides one of the most flexible logging systems of
any web server. You can log almost any piece of information about a
request, in almost any format, to almost any destination. You can split
logs by virtual host, filter them by condition, pipe them to external
programs, format them as JSON for your observability stack, or send them
straight to the systemd journal. The defaults are reasonable, but the
defaults are also thirty years old. Modern infrastructure demands more.

This chapter covers both the fundamentals — understanding what's in your
logs and how to control it — and the modern patterns you'll need in 2026:
structured logging for automated ingestion, timing instrumentation for
performance work, and integration with centralized logging
infrastructure. I'll assume you know what a log file is. I won't assume
you've memorized every ``%`` format token.


.. admonition:: Modules covered in this chapter

   :module:`mod_log_config`, :module:`mod_logio`,
   :module:`mod_log_forensic`, :module:`mod_log_debug`,
   :module:`mod_journald`, :module:`mod_syslog`,
   :module:`mod_remoteip`, :module:`mod_setenvif`,
   :module:`mod_unique_id`



.. _HTTP_Status_Code_Reference:

.. topic:: HTTP status codes in your logs

   For quick reference when reading access logs, here are the status codes
   you'll see most often:

   +-------+---------------------------+-------------------------------------------+
   | Code  | Name                      | What it means in your logs                |
   +-------+---------------------------+-------------------------------------------+
   | 200   | OK                        | Normal successful response                |
   +-------+---------------------------+-------------------------------------------+
   | 206   | Partial Content           | Range request (video streaming, resume)   |
   +-------+---------------------------+-------------------------------------------+
   | 301   | Moved Permanently         | Permanent redirect (check your Redirect   |
   |       |                           | directives)                               |
   +-------+---------------------------+-------------------------------------------+
   | 302   | Found                     | Temporary redirect                        |
   +-------+---------------------------+-------------------------------------------+
   | 304   | Not Modified              | Conditional GET — client cache is valid   |
   +-------+---------------------------+-------------------------------------------+
   | 400   | Bad Request               | Malformed request from client             |
   +-------+---------------------------+-------------------------------------------+
   | 401   | Unauthorized              | Authentication required but not provided  |
   +-------+---------------------------+-------------------------------------------+
   | 403   | Forbidden                 | Access denied (check permissions,         |
   |       |                           | Require directives)                       |
   +-------+---------------------------+-------------------------------------------+
   | 404   | Not Found                 | File doesn't exist (most common error)    |
   +-------+---------------------------+-------------------------------------------+
   | 408   | Request Timeout           | Client too slow sending request           |
   +-------+---------------------------+-------------------------------------------+
   | 500   | Internal Server Error     | Something crashed (check error log!)      |
   +-------+---------------------------+-------------------------------------------+
   | 502   | Bad Gateway               | Backend didn't respond properly (proxy)   |
   +-------+---------------------------+-------------------------------------------+
   | 503   | Service Unavailable       | Backend overloaded or down                |
   +-------+---------------------------+-------------------------------------------+
   | 504   | Gateway Timeout           | Backend too slow (proxy timeout)          |
   +-------+---------------------------+-------------------------------------------+

   A healthy production server's log should be dominated by 200s and 304s.
   A sudden increase in 5xx codes means something is broken on your end. A
   flood of 4xx codes usually means either broken links (404), scrapers
   hitting non-existent paths (404), or an authentication misconfiguration
   (401/403).


.. _Recipe_Understanding_Log_Formats:

.. _Section_Log_Fundamentals:

Log file fundamentals
---------------------

.. index:: Common Log Format

.. index:: CLF; see Logging,Common Log Format

.. index:: Combined log format

.. index:: LogFormat directive

.. index:: directives,LogFormat

.. index:: directives,CustomLog

.. index:: ErrorLog directive

.. index:: directives,ErrorLog

.. index:: LogLevel directive

.. index:: directives,LogLevel

.. index:: Logging,error log

.. index:: Logging,per-module log level

.. index:: LogFormat tokens

.. index:: Logging,custom fields

.. index:: Logging,request headers

.. index:: Logging,response headers

.. index:: Logging,environment variables

.. index:: Logging,notes


httpd maintains two separate log streams: the **access log**, which
records every request the server handles, and the **error log**, which
records problems, diagnostics, and anything the server needs to tell you
that isn't tied to a single successful response. You need to understand
both before you can configure them effectively.


.. _Section_Access_Log_Formats:

Access log formats
~~~~~~~~~~~~~~~~~~

httpd ships with two standard log formats. The Common Log Format (CLF)
records the bare essentials:

.. code-block:: apache

   LogFormat "%h %l %u %t \"%r\" %>s %b" common

The Combined Log Format adds the ``Referer`` and ``User-Agent`` request
headers:

.. code-block:: apache

   LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined

You then reference either format by its nickname in a ``CustomLog``
directive:

.. code-block:: apache

   CustomLog "/var/log/httpd/access_log" combined

A typical Combined log entry looks like this:

.. code-block:: text

   192.0.2.47 - jdoe [09/May/2026:14:23:01 -0400] "GET /api/v2/users HTTP/1.1" 200 1543 "https://example.com/dashboard" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"

Broken apart, field by field:

+-------------------+------------------+------------------------------------------+
| Format token      | Example value    | Meaning                                  |
+-------------------+------------------+------------------------------------------+
| ``%h``            | 192.0.2.47       | Remote hostname (IP unless                |
|                   |                  | ``HostnameLookups On``)                   |
+-------------------+------------------+------------------------------------------+
| ``%l``            | ``-``            | Remote logname from identd (always        |
|                   |                  | ``-`` in practice — leave it alone)       |
+-------------------+------------------+------------------------------------------+
| ``%u``            | jdoe             | Authenticated username (``-`` if none)    |
+-------------------+------------------+------------------------------------------+
| ``%t``            | [09/May/2026:... | Timestamp when request was received       |
+-------------------+------------------+------------------------------------------+
| ``%r``            | GET /api/v2/...  | First line of the request                 |
+-------------------+------------------+------------------------------------------+
| ``%>s``           | 200              | Final HTTP status code                    |
+-------------------+------------------+------------------------------------------+
| ``%b``            | 1543             | Response body size in bytes (``-`` if     |
|                   |                  | zero)                                     |
+-------------------+------------------+------------------------------------------+
| ``%{Referer}i``   | https://...      | Referer header from request               |
+-------------------+------------------+------------------------------------------+
| ``%{User-Agent}i``| Mozilla/5.0 ...  | User-Agent header from request            |
+-------------------+------------------+------------------------------------------+

The ``>`` in ``%>s`` means "use the final status" — the one actually sent
to the client. Without it, ``%s`` gives you the status of the original
request before any internal redirect. For almost every use case, ``%>s``
is what you want.

The ``%l`` field exists for historical reasons. The identd protocol it
queries is essentially dead. You'll see a dash there on every single
request, but it occupies its spot in the format because removing it would
break every log parser ever written for CLF. Leave it.

The ``LogFormat`` directive has two forms. When you give it a nickname (the
last argument), it defines a named format you can reference later. When you
use it without a nickname, it sets the default format for any
``TransferLog`` directives. In practice, always use the named form with
``CustomLog`` — it's clearer and more maintainable.


.. _Section_Format_Tokens:

Format tokens
~~~~~~~~~~~~~

The ``LogFormat`` string supports a rich set of ``%{name}X`` tokens. The
letter after the closing brace tells httpd where to look:

.. code-block:: text

   %{Foobar}i    - Request header "Foobar"
   %{Foobar}o    - Response header "Foobar"
   %{Foobar}e    - Environment variable "Foobar"
   %{Foobar}n    - Note from another module (e.g., mod_rewrite)
   %{Foobar}C    - Cookie "Foobar" from the request

**Request headers** (``%{name}i``): Log any header sent by the client.
Common uses include ``%{X-Forwarded-For}i`` for proxy chains,
``%{Accept-Language}i`` for content negotiation debugging, and
``%{Authorization}i`` (be careful — this contains credentials).

**Response headers** (``%{name}o``): Log any header your server sends
back. Useful for cache debugging (``%{X-Cache}o``), content type
verification (``%{Content-Type}o``), or custom application headers.

**Environment variables** (``%{name}e``): Log any variable set by
``SetEnv``, ``SetEnvIf``, ``RewriteRule``, or your application. This is
how you inject application-level metadata into the access log — set a
variable in your app or rewrite rules, then log it.

**Notes** (``%{name}n``): Internal module notes. For example,
:module:`mod_rewrite` sets notes you can log. The forensic ID from
:module:`mod_log_forensic` is available as ``%{forensic-id}n``.

**Cookies** (``%{name}C``): Log a specific cookie value from the request.
Useful for session tracking, though be mindful of privacy regulations.

**Status-code filtering**: You can restrict a token to only log for
certain status codes:

.. code-block:: apache

   # Only log Referer on 400 and 404 errors
   LogFormat "%h %t \"%r\" %>s %400,404{Referer}i" errors_with_referer

   # Log User-Agent on everything EXCEPT 200 and 304
   LogFormat "%h %t \"%r\" %>s %!200,304{User-Agent}i" non_success_agents

When a token doesn't match the condition, it outputs ``-``.

**Redirect tracking**: The ``<`` and ``>`` modifiers choose between the
original request and the final (redirected) request:

.. code-block:: apache

   # Original request URI (before internal redirect)
   %<U
   # Final status (after all internal redirects)
   %>s


**Recommended log formats for different use cases**:

.. code-block:: apache

   # Development: verbose, human-readable
   LogFormat "%a %u [%{%H:%M:%S}t] \"%m %U%q\" %>s %b %{ms}T" dev

   # Production: combined + timing + request ID (the minimum I'd recommend)
   LogFormat "%a %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %{ms}T %L" production

   # API server: focused on method, path, status, timing
   LogFormat "%a [%{%Y-%m-%dT%H:%M:%S}t.%{msec_frac}t] \"%m %U\" %>s %B %{ms}T \"%{X-Request-ID}i\"" api

   # CDN/static: focused on bandwidth
   LogFormat "%a %t \"%r\" %>s %O %{ms}T \"%{Referer}i\"" cdn

Pick the one closest to your needs and adjust. There's no "one true
format" — the right format depends on what questions you'll be asking
your logs.


.. _Section_Error_Log:

The error log
~~~~~~~~~~~~~

The error log is where httpd tells you about problems: configuration
errors, runtime failures, access denials, and module diagnostics. Unlike
the access log, you don't control its format — the format is fixed and
includes a timestamp, module name, severity level, client address (when
applicable), and the message.

The error log location and verbosity are controlled by two directives:

.. code-block:: apache

   ErrorLog "/var/log/httpd/error_log"
   LogLevel warn

A typical error log entry in httpd 2.4 looks like:

.. code-block:: text

   [Fri May 09 14:23:01.738219 2026] [core:error] [pid 12345:tid 67890] [client 192.0.2.47:54321] AH00124: Request exceeded the limit of 10 internal redirects

The fields are:

1. **Timestamp** with microsecond precision
2. **Module and level** in brackets: ``[module:level]``
3. **Process and thread ID**: ``[pid:tid]``
4. **Client address** (when the error relates to a specific request)
5. **Error code and message**: the ``AH#####`` codes are stable identifiers
you can search for

The ``LogLevel`` directive accepts these severity levels, from most to
least severe:

.. code-block:: text

   emerg, alert, crit, error, warn, notice, info, debug, trace1-trace8

The default ``warn`` is appropriate for production. You'll see errors,
critical issues, and warnings, but not the firehose of informational
messages.


.. _Section_Per_Module_LogLevel:

Per-module log levels
~~~~~~~~~~~~~~~~~~~~~

The per-module syntax (available since httpd 2.4) is enormously useful for
debugging. Instead of setting the entire server to ``debug`` — which
generates gigabytes of output on a busy server — you can surgically
increase logging for just the module you're troubleshooting:

.. code-block:: apache

   # Debug SSL handshake issues without flooding everything else
   LogLevel warn
   LogLevel mod_ssl:debug

   # Trace mod_rewrite rule processing
   LogLevel warn
   LogLevel mod_rewrite:trace6

   # See mod_proxy connection details
   LogLevel warn
   LogLevel mod_proxy:debug
   LogLevel mod_proxy_http:debug

The trace levels (``trace1`` through ``trace8``) produce increasingly
detailed output. For :module:`mod_rewrite`, ``trace3`` shows you which
rules match, ``trace6`` shows the full rewrite processing, and
``trace8`` dumps everything including pattern matching details.

.. warning::

   Never leave ``trace`` levels enabled in production. They generate
   enormous volumes of output and will fill your disk. Use them for
   debugging, then remove them.


**Reading the AH error codes**: Every error message from httpd's core and
bundled modules includes a stable error code like ``AH00124``. These are
searchable — both in the httpd documentation and on the web. When you see
an error you don't understand, search for the AH code first. It's far
more reliable than searching for the error message text, which may vary
between versions. A complete reference for every ``AH#####`` code, with
explanations and fix suggestions, is available at
https://httpd.rcbowen.com/errors/.

**Common error log entries and what they mean**:

.. code-block:: text

   [core:error] AH00124: Request exceeded the limit of 10 internal redirects

Your ``RewriteRule`` directives are looping. A rule redirects to a path
that matches the same rule again. Add a ``RewriteCond`` to break the
cycle, or check for ``[L]`` flag usage.

.. code-block:: text

   [core:error] AH00126: Invalid URI in request GET /%s HTTP/1.1

A bot or scanner sent a malformed request. Not actionable unless you see
it at high volume (which might indicate an attack).

.. code-block:: text

   [authz_core:error] AH01630: client denied by server configuration

Your ``Require`` directives are blocking access. Check your
``<Directory>`` or ``<Location>`` access control.

.. code-block:: text

   [proxy:error] AH00957: HTTP: attempt to connect to 10.0.1.5:8080 failed

Your backend is down or unreachable. This is the #1 error you'll see in a
reverse proxy setup.

.. code-block:: text

   [ssl:error] AH02032: Hostname provided via SNI and target URL don't match

A client is connecting with a ``ServerName`` that doesn't match any
configured virtual host. Common with bots probing IP addresses directly.

**Silencing noisy errors**: Some errors are informational noise that
clutters your logs. You can suppress specific modules:

.. code-block:: apache

   # Reduce noise from SSL renegotiation messages
   LogLevel warn
   LogLevel ssl:error

   # Suppress favicon 404 noise (handle it instead)
   <Location "/favicon.ico">
       ErrorDocument 404 "No favicon"
       LogLevel crit
   </Location>

Per-directory ``LogLevel`` (available since 2.4.10) lets you silence
errors for specific paths without affecting the rest of your site.


Correlating error and access log entries
-----------------------------------------

.. index:: Log correlation

.. index:: %L format token

.. index:: Logging,unique ID

.. index:: mod_unique_id


.. _Recipe_Correlating_Logs:

.. _Problem_Correlating_Logs:

Problem
~~~~~~~

A client reports an error, and you can see it in the error log, but you
can't tell which access log entry it corresponds to. You need a way to
link the two.


.. _Solution_Correlating_Logs:

Solution
~~~~~~~~

Use the ``%L`` token in your ``LogFormat``. httpd assigns each request
a unique log ID that appears in both the error log and the access log:

.. code-block:: apache

   LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %L" combined_with_id
   CustomLog "/var/log/httpd/access_log" combined_with_id

Now when you see an error log entry like:

.. code-block:: text

   [Fri May 09 14:23:01.738219 2026] [proxy:error] [pid 12345:tid 67890] (111)Connection refused: AH00957: HTTP: attempt to connect to 10.0.1.5:8080 (backend) failed [log_id: Yx8AAFmaIgQAAGR2D-gAAAAD]

You can grep the access log for that same ID:

.. code-block:: bash

   grep 'Yx8AAFmaIgQAAGR2D-gAAAAD' /var/log/httpd/access_log


.. _Discussion_Correlating_Logs:

Discussion
~~~~~~~~~~

The ``%L`` token was introduced to solve a real operational pain point.
Before it existed, correlating errors with requests on a busy server
required matching timestamps and client IPs — unreliable at best when
you're handling hundreds of requests per second.

The log ID is generated internally by httpd whenever an error is logged
for a request. If no error occurs for a given request, ``%L`` outputs
``-`` in the access log (since no error log entry needs correlation).

There's also ``%{c}L`` which gives you the *connection* log ID rather
than the request log ID. This is useful for correlating connection-level
errors (like TLS handshake failures) that happen before a request is
fully formed.

If you're already using :module:`mod_unique_id`, the unique ID it
generates is separate from the log ID. You can log both:

.. code-block:: apache

   LogFormat "%h %t \"%r\" %>s %b %L %{UNIQUE_ID}e" full_id

The ``UNIQUE_ID`` from :module:`mod_unique_id` is useful for passing to
backend applications (it's available as an environment variable and
request header), while ``%L`` is specifically for error-to-access log
correlation.


.. _See_Also_Correlating_Logs:

See Also
~~~~~~~~

* :ref:`Section_Error_Log` for error log format details
* :ref:`Recipe_Forensic_Logging` for even more detailed request capture
* :module:`mod_unique_id` documentation:
  https://httpd.apache.org/docs/2.4/mod/mod_unique_id.html


.. _Recipe_Conditional_Logging:

Conditional logging
--------------------

.. index:: Conditional logging

.. index:: SetEnvIf directive

.. index:: directives,SetEnvIf

.. index:: env= clause

.. index:: Logging,excluding requests

.. index:: Logging,filtering


.. _Problem_Conditional_Logging:

Problem
~~~~~~~

You want to exclude certain requests from your access log — health
checks, static assets, internal monitoring probes — without losing the
ability to log them separately if needed.


.. _Solution_Conditional_Logging:

Solution
~~~~~~~~

Use ``SetEnvIf`` (or ``SetEnvIfNoCase``) to set an environment variable,
then use the ``env=`` clause on ``CustomLog`` to include or exclude
requests:

.. code-block:: apache

   # Mark requests we want to suppress
   SetEnvIf Request_URI "^/health$" no_log
   SetEnvIf Request_URI "^/status$" no_log
   SetEnvIf User-Agent "^ELB-HealthChecker" no_log
   SetEnvIf Remote_Addr "^10\.0\.0\." internal_request

   # Main log excludes marked requests
   CustomLog "/var/log/httpd/access_log" combined env=!no_log

   # Separate log captures only internal requests
   CustomLog "/var/log/httpd/internal_access_log" combined env=internal_request

To exclude image requests from the main log:

.. code-block:: apache

   SetEnvIf Request_URI "\.(gif|jpg|jpeg|png|svg|ico|webp|woff2|css|js)$" static_asset
   CustomLog "/var/log/httpd/access_log" combined env=!static_asset
   CustomLog "/var/log/httpd/static_log" combined env=static_asset


.. _Discussion_Conditional_Logging:

Discussion
~~~~~~~~~~

The ``env=`` clause is evaluated *after* the request is processed but
*before* the log entry is written. The environment variable just needs to
exist — its value doesn't matter. You're testing presence, not content.

The ``!`` prefix inverts the test: ``env=!no_log`` means "log this
request only if the ``no_log`` variable is NOT set."

Each ``CustomLog`` directive is independent. You can have multiple
directives, each with different conditions, writing to different files in
different formats. This lets you maintain a clean primary log while still
capturing everything in a verbose secondary log:

.. code-block:: apache

   # Everything goes to the verbose log (for compliance)
   CustomLog "/var/log/httpd/full_access_log" combined

   # The operational log skips noise
   CustomLog "/var/log/httpd/access_log" combined env=!no_log

You can also use ``expr=`` for more complex conditions (available since
httpd 2.4.13):

.. code-block:: apache

   # Only log requests that took more than 1 second
   CustomLog "/var/log/httpd/slow_requests.log" combined "expr=%T > 1"

   # Only log 5xx errors
   CustomLog "/var/log/httpd/errors.log" combined "expr=%{REQUEST_STATUS} >= 500"

The ``expr=`` syntax gives you access to the full ``ap_expr`` expression
parser, which is far more powerful than ``SetEnvIf`` for complex
conditions.

.. note::

   Be aware that ``SetEnvIf`` runs early in request processing, before
   authentication and most other modules. If you need to filter based on
   information that's only available later (like the response status),
   use ``expr=`` instead.



**Practical filtering patterns I use frequently**:

.. code-block:: apache

   # Suppress Kubernetes liveness/readiness probes
   SetEnvIf Request_URI "^/healthz$" no_log
   SetEnvIf Request_URI "^/readyz$" no_log

   # Suppress Let's Encrypt ACME challenges
   SetEnvIf Request_URI "^/\.well-known/acme-challenge/" no_log

   # Suppress Prometheus metrics scraping
   SetEnvIf Request_URI "^/server-status$" no_log
   SetEnvIf Request_URI "^/metrics$" no_log

   # Suppress requests from your monitoring system by User-Agent
   SetEnvIf User-Agent "^Datadog Agent" no_log
   SetEnvIf User-Agent "^Prometheus" no_log

   # Mark requests from specific client IP ranges
   SetEnvIf Remote_Addr "^192\.168\." internal_net
   SetEnvIf Remote_Addr "^10\." internal_net

The ``env=`` filtering happens per ``CustomLog`` directive independently.
This means you can set up a layered logging strategy:

.. code-block:: apache

   # Layer 1: Verbose log captures everything (for compliance/forensics)
   CustomLog "/var/log/httpd/full.log" combined

   # Layer 2: Operational log skips health checks and static assets
   CustomLog "/var/log/httpd/ops.log" combined env=!no_log

   # Layer 3: Error-only log for alerting (5xx responses only)
   CustomLog "/var/log/httpd/errors.log" combined "expr=%{REQUEST_STATUS} >= 500"

   # Layer 4: Slow request log for performance monitoring
   CustomLog "/var/log/httpd/slow.log" performance "expr=%T >= 3"

This layered approach costs minimal extra I/O (the data is already in
memory) but gives you purpose-built logs for different operational needs.


.. _See_Also_Conditional_Logging:

See Also
~~~~~~~~

* :ref:`Section_Format_Tokens` for logging the variables themselves
* ``ap_expr`` documentation:
  https://httpd.apache.org/docs/2.4/expr.html
* :module:`mod_setenvif` documentation:
  https://httpd.apache.org/docs/2.4/mod/mod_setenvif.html


.. _Recipe_Per_Vhost_Logging:

Per-virtual-host logging
-------------------------

.. index:: Virtual hosts,logging

.. index:: Logging,per virtual host

.. index:: Logging,vhost


.. _Problem_Per_Vhost_Logging:

Problem
~~~~~~~

You run multiple virtual hosts and want each one to log to its own
file, rather than mixing everything into a single access log.


.. _Solution_Per_Vhost_Logging:

Solution
~~~~~~~~

Place ``CustomLog`` and ``ErrorLog`` directives inside each
``<VirtualHost>`` block:

.. code-block:: apache

   <VirtualHost *:443>
       ServerName www.example.com
       DocumentRoot "/var/www/example"

       ErrorLog "/var/log/httpd/example.com-error_log"
       CustomLog "/var/log/httpd/example.com-access_log" combined
   </VirtualHost>

   <VirtualHost *:443>
       ServerName api.example.com
       DocumentRoot "/var/www/api"

       ErrorLog "/var/log/httpd/api.example.com-error_log"
       CustomLog "/var/log/httpd/api.example.com-access_log" combined
   </VirtualHost>

If you have many virtual hosts and want automatic file naming without
repeating yourself, use the ``%v`` token in a global ``CustomLog``:

.. code-block:: apache

   LogFormat "%v %h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" vhost_combined
   CustomLog "/var/log/httpd/all_vhosts_access_log" vhost_combined


.. _Discussion_Per_Vhost_Logging:

Discussion
~~~~~~~~~~

When a ``CustomLog`` or ``ErrorLog`` directive appears inside a
``<VirtualHost>`` block, it overrides the global directive for that
vhost. The request will *only* appear in the vhost's log — it will not
also appear in the global log. This is a common point of confusion.

If you want both — a per-vhost log and a combined global log — you need
``CustomLog`` in both scopes, or you can use just the global
``CustomLog`` with ``%v`` prepended to identify which vhost served
each request.

The ``%v`` approach (a single log file with the virtual host name
prepended) has a practical advantage: you end up with one file instead of
dozens. You can then split it later with a tool like ``split-logfile``
(shipped with httpd in the :file:`support/` directory), or ingest it
directly into a log aggregator that can filter by field.

The per-file approach has its own advantage: you can apply different
retention policies, different rotation schedules, or hand individual log
files to different teams or customers.

For ``ErrorLog``, per-vhost separation is especially valuable. Without
it, all errors from all vhosts land in one file, and a misbehaving vhost
can drown out errors from others. You can also set different ``LogLevel``
per vhost:

.. code-block:: apache

   <VirtualHost *:443>
       ServerName staging.example.com
       ErrorLog "/var/log/httpd/staging-error_log"
       LogLevel info
   </VirtualHost>



**Using macros for DRY vhost logging**:

If you have many virtual hosts with a consistent naming pattern, you can
use :module:`mod_macro` to avoid repeating yourself:

.. code-block:: apache

   <Macro VHostLog $domain>
       ErrorLog "/var/log/httpd/${domain}-error_log"
       CustomLog "/var/log/httpd/${domain}-access_log" combined
   </Macro>

   <VirtualHost *:443>
       ServerName www.example.com
       Use VHostLog example.com
       # ... rest of vhost config
   </VirtualHost>

   <VirtualHost *:443>
       ServerName shop.example.com
       Use VHostLog shop.example.com
       # ... rest of vhost config
   </VirtualHost>

**Directory-scoped logging** (since httpd 2.4): You can place
``CustomLog`` inside ``<Directory>``, ``<Location>``, or ``<Files>``
containers:

.. code-block:: apache

   # Log all API requests to a separate file
   <Location "/api/">
       CustomLog "/var/log/httpd/api_access_log" combined
   </Location>

This is useful when different teams own different URL spaces and want
their own logs, or when you need different log verbosity for different
parts of your site.


.. _See_Also_Per_Vhost_Logging:

See Also
~~~~~~~~

* :ref:`Recipe_Rotating_Logs` for managing many log files
* The ``split-logfile`` utility:
  https://httpd.apache.org/docs/2.4/programs/split-logfile.html


.. _Recipe_Rotating_Logs:

Rotating log files
-------------------

.. index:: Log rotation

.. index:: rotatelogs program

.. index:: logrotate

.. index:: Logging,rotation


.. _Problem_Rotating_Logs:

Problem
~~~~~~~

Your access logs grow indefinitely, consuming disk space and making
analysis unwieldy. You need to rotate them — either by time interval
or by file size — without losing any entries or restarting the server.


.. _Solution_Rotating_Logs:

Solution
~~~~~~~~

**Method 1: rotatelogs (built-in, no restart needed)**

Time-based rotation (new file every 24 hours):

.. code-block:: apache

   CustomLog "|/usr/sbin/rotatelogs /var/log/httpd/access_log.%Y-%m-%d 86400" combined
   ErrorLog "|/usr/sbin/rotatelogs /var/log/httpd/error_log.%Y-%m-%d 86400"

Size-based rotation (new file every 100 MB):

.. code-block:: apache

   CustomLog "|/usr/sbin/rotatelogs /var/log/httpd/access_log.%Y-%m-%d-%H%M%S 100M" combined

Combined (rotate every 24 hours OR at 500 MB, whichever comes first):

.. code-block:: apache

   CustomLog "|/usr/sbin/rotatelogs -f /var/log/httpd/access_log.%Y-%m-%d 86400 500M" combined

**Method 2: logrotate (system-level, requires graceful restart)**

Create :file:`/etc/logrotate.d/httpd`:

.. code-block:: text

   /var/log/httpd/*_log {
       daily
       rotate 30
       compress
       delaycompress
       missingok
       notifempty
       sharedscripts
       postrotate
           /usr/bin/systemctl reload httpd.service > /dev/null 2>&1 || true
       endscript
   }


.. _Discussion_Rotating_Logs:

Discussion
~~~~~~~~~~

These two approaches solve the same problem differently:

**rotatelogs** uses piped logging — httpd writes to a pipe, and the
``rotatelogs`` program receives the data and writes it to the
appropriate file. Because the pipe stays open, httpd never needs to be
restarted or signaled. The ``-f`` flag forces ``rotatelogs`` to open the
file immediately on startup (useful so monitoring tools don't complain
about a missing file).

The filename argument supports ``strftime(3)`` format tokens. Common
patterns:

- ``%Y-%m-%d`` — daily rotation: :file:`access_log.2026-05-09`
- ``%Y-%m-%d-%H`` — hourly rotation: :file:`access_log.2026-05-09-14`
- ``%Y%m%d%H%M%S`` — used with size-based rotation to get unique names

The ``rotatelogs`` approach has a subtle timing consideration: the
rotation happens at UTC epoch boundaries unless you pass the ``-l`` flag
for local time:

.. code-block:: apache

   CustomLog "|/usr/sbin/rotatelogs -l /var/log/httpd/access_log.%Y-%m-%d 86400" combined

**logrotate** is the traditional Unix approach. It renames the current
file and signals httpd to reopen its logs. The ``postrotate`` script
sends a ``SIGUSR1`` (graceful restart) which causes httpd to close and
reopen all log file handles. The brief moment between the rename and
the signal is theoretically a window for lost entries, but in practice
``delaycompress`` and the graceful restart make this reliable.

Choose ``rotatelogs`` when:

- You can't tolerate any possibility of lost entries
- You want rotation without system-level cron/logrotate infrastructure
- You're in a container where logrotate might not be available

Choose ``logrotate`` when:

- You want compression, retention policies, and other logrotate features
- You prefer a single system-wide log management approach
- Your monitoring expects predictable file paths (no timestamps in names)



**Cleanup of old rotated files**: ``rotatelogs`` doesn't delete old files.
You'll need a separate cron job:

.. code-block:: bash

   # Delete access logs older than 30 days
   find /var/log/httpd/ -name "access_log.*" -mtime +30 -delete

Or use the ``-n`` flag (available since httpd 2.4.5) to keep only a
specified number of files:

.. code-block:: apache

   # Keep only the 7 most recent rotated files
   CustomLog "|/usr/sbin/rotatelogs -n 7 /var/log/httpd/access_log 86400" combined

With ``-n``, ``rotatelogs`` uses numeric suffixes (``.1``, ``.2``, etc.)
instead of timestamp-based names, and automatically removes older files
beyond the specified count.

**Rotation for ErrorLog**: Don't forget the error log. It grows too:

.. code-block:: apache

   ErrorLog "|/usr/sbin/rotatelogs -l /var/log/httpd/error_log.%Y-%m-%d 86400"

**Multiple vhosts with rotatelogs**: Each piped ``CustomLog`` spawns its
own ``rotatelogs`` process. If you have 50 vhosts each with their own
rotated log, that's 50 extra processes (100 if you rotate both access and
error logs). On servers with many vhosts, consider using a single log with
``%v`` and splitting later, or use ``logrotate`` instead.


.. _See_Also_Rotating_Logs:

See Also
~~~~~~~~

* :ref:`Recipe_Piped_Logging` for more piped logging patterns
* ``rotatelogs`` documentation:
  https://httpd.apache.org/docs/2.4/programs/rotatelogs.html


.. _Recipe_Logging_Behind_Proxy:

Logging behind a reverse proxy
-------------------------------

.. index:: Reverse proxy logging

.. index:: X-Forwarded-For header

.. index:: mod_remoteip

.. index:: Logging,proxy

.. index:: %a vs %h


.. _Problem_Logging_Behind_Proxy:

Problem
~~~~~~~

Your httpd instance sits behind a load balancer, CDN, or reverse proxy.
The access log shows the proxy's IP address for every request instead of
the actual client's address.


.. _Solution_Logging_Behind_Proxy:

Solution
~~~~~~~~

Use :module:`mod_remoteip` to replace the connection's remote address
with the client IP from the ``X-Forwarded-For`` header:

.. code-block:: apache

   LoadModule remoteip_module modules/mod_remoteip.so

   RemoteIPHeader X-Forwarded-For
   RemoteIPTrustedProxy 10.0.0.0/8
   RemoteIPTrustedProxy 172.16.0.0/12

Once :module:`mod_remoteip` is configured, the ``%a`` format token
automatically reflects the true client IP:

.. code-block:: apache

   LogFormat "%a %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
   CustomLog "/var/log/httpd/access_log" combined

If you need to log both the proxy IP and the client IP:

.. code-block:: apache

   LogFormat "%a %{c}a %l %u %t \"%r\" %>s %b" proxy_aware


.. _Discussion_Logging_Behind_Proxy:

Discussion
~~~~~~~~~~

There are several format tokens related to the remote address, and the
distinction matters:

- ``%h`` — Remote hostname (or IP if ``HostnameLookups Off``). With
  :module:`mod_remoteip` loaded, this reflects the *adjusted* client IP.
- ``%a`` — Client IP address. With :module:`mod_remoteip`, this is the
  true client IP extracted from the proxy header.
- ``%{c}a`` — The *underlying peer* IP address of the TCP connection —
  always the proxy's IP regardless of :module:`mod_remoteip`.

The ``RemoteIPTrustedProxy`` directive is critical for security. Without
it, any client could forge an ``X-Forwarded-For`` header and spoof their
IP. Only IPs listed as trusted proxies will have their forwarded
addresses honored.

If your proxy uses a non-standard header, adjust accordingly:

.. code-block:: apache

   # For Cloudflare
   RemoteIPHeader CF-Connecting-IP

   # For custom proxies
   RemoteIPHeader X-Real-IP

For AWS Application Load Balancers, the ``X-Forwarded-For`` header may
contain multiple comma-separated IPs (the client, plus each proxy in the
chain). :module:`mod_remoteip` handles this correctly — it walks the
chain from right to left, stripping trusted proxy IPs until it finds
the first untrusted IP, which it treats as the client.

.. note::

   If you're using ``%h`` (hostname) in your log format, switch to
   ``%a`` (IP address). With :module:`mod_remoteip` active, ``%a`` is
   the canonical way to log the client's address. You should also have
   ``HostnameLookups Off`` in production — DNS lookups per request are
   a serious performance penalty.



**The PROXY protocol alternative**: If your load balancer supports the
PROXY protocol (HAProxy, AWS NLB), you can use :module:`mod_remoteip`
with ``RemoteIPProxyProtocol``:

.. code-block:: apache

   <VirtualHost *:443>
       RemoteIPProxyProtocol On
       RemoteIPProxyProtocolExceptions 127.0.0.1
   </VirtualHost>

The PROXY protocol passes the client IP at the TCP level, before any HTTP
headers are parsed. It's more reliable than header-based approaches
because it can't be spoofed by the client (only the proxy can inject it).

**Logging the full proxy chain**: Sometimes you want to see the entire
``X-Forwarded-For`` chain, not just the extracted client IP. Log the raw
header alongside the resolved address:

.. code-block:: apache

   LogFormat "%a [chain: %{X-Forwarded-For}i] %t "%r" %>s %b" proxy_debug

This is useful for debugging multi-tier proxy setups where you're not
sure which proxy is adding what.

**Testing your mod_remoteip configuration**: After setup, verify it's
working:

.. code-block:: bash

   # From a machine behind the proxy, make a request
   curl -H "X-Forwarded-For: 203.0.113.195" http://your-server/test

   # Check the access log - should show 203.0.113.195 as %a
   # (only if the curl source IP is in RemoteIPTrustedProxy)


.. _See_Also_Logging_Behind_Proxy:

See Also
~~~~~~~~

* :module:`mod_remoteip` documentation:
  https://httpd.apache.org/docs/2.4/mod/mod_remoteip.html
* :ref:`Recipe_Measuring_Request_Timing` for timing that accounts for
  proxy latency


.. _Recipe_JSON_Logging:

Json/structured logging
-----------------------

.. index:: JSON logging

.. index:: Structured logging

.. index:: Logging,JSON format

.. index:: ELK stack

.. index:: OpenSearch

.. index:: Splunk

.. index:: CloudWatch Logs


.. _Problem_JSON_Logging:

Problem
~~~~~~~

You want your access logs in JSON format for direct ingestion into a log
aggregation system (Elasticsearch/OpenSearch, Splunk, CloudWatch Logs,
Datadog) without needing an intermediate parsing step.


.. _Solution_JSON_Logging:

Solution
~~~~~~~~

Craft a ``LogFormat`` that outputs valid JSON. No extra modules needed —
:module:`mod_log_config` can do this with a carefully constructed format
string:

.. code-block:: apache

   LogFormat "{ \"timestamp\": \"%{%Y-%m-%dT%H:%M:%S%z}t\", \"remote_addr\": \"%a\", \"remote_user\": \"%u\", \"request_method\": \"%m\", \"request_uri\": \"%U%q\", \"protocol\": \"%H\", \"status\": %>s, \"body_bytes_sent\": %B, \"http_referer\": \"%{Referer}i\", \"http_user_agent\": \"%{User-Agent}i\", \"request_time_ms\": %{ms}T, \"vhost\": \"%v\" }" json

   CustomLog "/var/log/httpd/access_log.json" json

A more complete version that handles edge cases (null values, proper
escaping):

.. code-block:: apache

   LogFormat "{ \"time\": \"%{%Y-%m-%dT%H:%M:%S}t.%{usec_frac}t%{%z}t\", \"vhost\": \"%v\", \"client\": \"%a\", \"method\": \"%m\", \"uri\": \"%U\", \"query\": \"%q\", \"protocol\": \"%H\", \"status\": %>s, \"bytes_body\": %B, \"bytes_sent\": %O, \"duration_us\": %D, \"referer\": \"%{Referer}i\", \"useragent\": \"%{User-Agent}i\", \"request_id\": \"%L\" }" json_full

   CustomLog "/var/log/httpd/access_log.json" json_full


.. _Discussion_JSON_Logging:

Discussion
~~~~~~~~~~

This approach works because :module:`mod_log_config` lets you put
arbitrary literal characters in the format string. You're essentially
constructing JSON by hand using literal braces, colons, commas, and
escaped quotes around the dynamic tokens.

There are a few important considerations:

**Numeric fields**: For fields like ``status`` and ``bytes``, don't wrap
them in quotes. Use ``%>s`` and ``%B`` bare so they produce valid JSON
numbers. Note that ``%b`` outputs ``-`` when zero bytes are sent, which
would break JSON. Use ``%B`` (which outputs ``0``) instead.

**The escaping problem**: If a field value contains a literal double
quote or backslash — and ``User-Agent`` strings sometimes do — your JSON
will break. httpd 2.4 escapes non-printable characters and quotes in
logged values using ``\xHH`` notation, which is *not* valid JSON
escaping. For most real-world traffic this isn't a problem, but be aware
it can happen.

To handle this robustly, you have three options:

1. Accept that occasional lines may be malformed and configure your
ingestion pipeline to skip parse errors
2. Pipe through a program that sanitizes the output (see
   :ref:`Recipe_Piped_Logging`)
3. Use a log shipper (Fluent Bit, Filebeat) that can parse the
Combined format natively, and use JSON output from the *shipper*
instead

**Timestamp format**: The ``%{%Y-%m-%dT%H:%M:%S%z}t`` produces ISO 8601
format, which every log aggregator understands. Adding
``.%{usec_frac}t`` gives you microsecond precision — useful for
performance analysis.

**Ingestion examples**:

For Fluent Bit reading JSON logs directly:

.. code-block:: text

   [INPUT]
       Name tail
       Path /var/log/httpd/access_log.json
       Parser json
       Tag  httpd.access

For Filebeat:

.. code-block:: json

   {
     "filebeat.inputs": [{
       "type": "log",
       "paths": ["/var/log/httpd/access_log.json"],
       "json.keys_under_root": true,
       "json.add_error_key": true
     }]
   }

For CloudWatch Logs Agent, the JSON format means your fields are
automatically available for Logs Insights queries without custom parsing:

.. code-block:: text

   fields @timestamp, client, method, uri, status, duration_us
   | filter status >= 500
   | sort duration_us desc



**A production-ready JSON format**:

After much trial and error across many deployments, here's the JSON
format I recommend as a starting point:

.. code-block:: apache

   # Define the JSON format
   LogFormat "{      "@timestamp": "%{%Y-%m-%dT%H:%M:%S}t.%{usec_frac}t%{%z}t",      "server": "%v",      "client.ip": "%a",      "client.port": "%{remote}p",      "http.method": "%m",      "url.path": "%U",      "url.query": "%q",      "http.version": "%H",      "http.response.status_code": %>s,      "http.response.body.bytes": %B,      "network.bytes_in": %I,      "network.bytes_out": %O,      "event.duration_us": %D,      "http.request.referrer": "%{Referer}i",      "user_agent.original": "%{User-Agent}i",      "http.request.id": "%L",      "connection.requests": %k,      "tls.protocol": "%{SSL_PROTOCOL}e",      "tls.cipher": "%{SSL_CIPHER}e"    }" json_ecs

   CustomLog "/var/log/httpd/access.json" json_ecs

This format uses field names from the Elastic Common Schema (ECS), which
makes it immediately useful in OpenSearch/Elasticsearch without field
mapping gymnastics. Adjust the field names to match your organization's
schema conventions.

.. tip::

   You can split a long ``LogFormat`` across multiple lines using
   backslash continuation. httpd treats the whole thing as one line. This
   dramatically improves readability of complex JSON formats.

**Testing your JSON format**: After configuring, verify the output is
valid JSON:

.. code-block:: bash

   # Grab the last 10 lines and validate each one
   tail -10 /var/log/httpd/access.json | while read line; do
       echo "$line" | python3 -c "import sys,json; json.load(sys.stdin)" 2>&1 || echo "INVALID: $line"
   done

If you see parse errors, they're almost certainly from unescaped
characters in user-agent strings or referrer URLs. Decide whether to
accept occasional invalid lines or implement a sanitization pipe.


.. _See_Also_JSON_Logging:

See Also
~~~~~~~~

* :ref:`Recipe_Piped_Logging` for post-processing log output
* :ref:`Recipe_Measuring_Request_Timing` for the timing tokens used above
* :ref:`Recipe_Log_Analysis` for tools that consume structured logs


.. _Recipe_Logging_Journald:

Logging to the systemd journal
-------------------------------

.. index:: systemd journal

.. index:: journald

.. index:: mod_journald

.. index:: journalctl


.. _Problem_Logging_Journald:

Problem
~~~~~~~

Your server runs on a systemd-based Linux distribution and you want httpd
to log directly to the systemd journal, taking advantage of structured
metadata and centralized journal management.


.. _Solution_Logging_Journald:

Solution
~~~~~~~~

.. note::

   :module:`mod_journald` is available in the httpd development trunk
   (2.5.x) and in some distribution builds that backport it. Check
   whether your distribution packages include it. On RHEL/Fedora/CentOS
   Stream, it may be available as a separate package. If you run httpd
   from source, you'll need to build from trunk or apply the module
   patch.

Load the module and point ``ErrorLog`` at the journald provider:

.. code-block:: apache

   LoadModule journald_module modules/mod_journald.so

   ErrorLog "journald"
   LogLevel info

You can also send access logs to the journal:

.. code-block:: apache

   CustomLog "journald" combined

View the logs using ``journalctl``:

.. code-block:: bash

   # All httpd messages
   journalctl -u httpd.service

   # Only error log messages
   journalctl -u httpd.service LOG=error_log

   # Filter by virtual host
   journalctl -u httpd.service SERVER_HOSTNAME=www.example.com

   # Filter by URI
   journalctl -u httpd.service REQUEST_URI=/api/health

   # Follow in real time
   journalctl -u httpd.service -f


.. _Discussion_Logging_Journald:

Discussion
~~~~~~~~~~

:module:`mod_journald` provides structured logging to systemd-journald.
"Structured" here means that each log entry carries typed metadata fields
— not just a flat string. The journal records these fields:

- ``LOG`` — the log name (``error_log`` for ErrorLog, or the first
  argument of CustomLog)
- ``REQUEST_HOSTNAME`` — the ``Host`` header value
- ``REQUEST_USER`` — authenticated username
- ``REQUEST_USERAGENT_IP`` — client IP address
- ``REQUEST_URI`` — the request path
- ``SERVER_HOSTNAME`` — the server's hostname

This means you can filter and search logs without any text parsing. You
don't need grep — ``journalctl`` gives you field-based queries natively.

**When to use journald logging**:

- You're already using ``journalctl`` as your primary log interface
- You want automatic log rotation (the journal handles its own retention)
- You want structured metadata without crafting JSON format strings
- You're running httpd in a systemd service and want unified log
  management

**When NOT to use journald logging**:

- High-throughput access logging. The :module:`mod_journald`
  documentation explicitly warns that systemd-journald is not designed
  for high-throughput logging. On a busy server, sending access logs to
  the journal can significantly impact performance. Use it for error
  logs; for access logs, stick with files or pipes.
- You need logs accessible to non-root users who don't have journal
  permissions
- You're shipping logs to a remote aggregator (file-based logs are
  easier for shippers to tail)

A practical compromise: send error logs to journald (low volume, benefits
from structured queries) and keep access logs in files (high volume,
easily shipped):

.. code-block:: apache

   ErrorLog "journald"
   CustomLog "/var/log/httpd/access_log.json" json


.. _See_Also_Logging_Journald:

See Also
~~~~~~~~

* :ref:`Recipe_Logging_Syslog` for the traditional syslog alternative
* :module:`mod_journald` documentation:
  https://httpd.apache.org/docs/trunk/mod/mod_journald.html
* ``journalctl`` man page: ``man journalctl``


.. _Recipe_Logging_Syslog:

Logging to syslog and remote syslog
-------------------------------------

.. index:: syslog

.. index:: mod_syslog

.. index:: Logging,syslog

.. index:: Logging,remote syslog

.. index:: rsyslog

.. index:: syslog-ng


.. _Problem_Logging_Syslog:

Problem
~~~~~~~

You want to send httpd error logs to the system syslog daemon — either
for local consolidation with other service logs or for forwarding to a
remote log server.


.. _Solution_Logging_Syslog:

Solution
~~~~~~~~

For error logs, httpd has built-in syslog support via :module:`mod_syslog`:

.. code-block:: apache

   # Default facility (local7)
   ErrorLog "syslog"

   # Specify a facility
   ErrorLog "syslog:local6"

For access logs to syslog, pipe through the ``logger`` utility:

.. code-block:: apache

   CustomLog "|/usr/bin/logger -t httpd -p local6.info" combined

To forward these messages to a remote syslog server, configure your
system's syslog daemon. For rsyslog, add to
:file:`/etc/rsyslog.d/httpd.conf`:

.. code-block:: text

   local6.*    @@logserver.example.com:514

For syslog-ng:

.. code-block:: text

   destination d_remote { tcp("logserver.example.com" port(514)); };
   filter f_httpd { facility(local6); };
   log { source(s_local); filter(f_httpd); destination(d_remote); };


.. _Discussion_Logging_Syslog:

Discussion
~~~~~~~~~~

The ``ErrorLog syslog`` syntax uses the :module:`mod_syslog` provider.
The default facility is ``local7``. You can use any standard syslog
facility: ``auth``, ``daemon``, ``local0`` through ``local7``, etc.
Choose a facility that doesn't conflict with other services on your
system — ``local6`` is a common choice for httpd.

.. warning::

   The syslog facility is effectively global. If you set different
   facilities in different ``<VirtualHost>`` blocks, the last one wins
   for the entire server. This is a long-standing limitation.

For access logs, there's no direct ``CustomLog "syslog"`` equivalent in
2.4 stable. However, the trunk (2.5.x) documentation shows that
:module:`mod_journald` and :module:`mod_syslog` can serve as providers
for ``CustomLog``:

.. code-block:: apache

   # Available in trunk / some distributions
   CustomLog "syslog:user" combined

If this isn't available in your build, the piped ``logger`` approach
works universally and gives you more control over the syslog tag and
priority.

**Remote forwarding**: The syslog daemon on your server handles the
forwarding — httpd doesn't need to know about remote servers. This
separation of concerns is a feature: you can change your log
infrastructure (switch from rsyslog to syslog-ng, change the remote
server, add TLS) without touching httpd's configuration.

**Security considerations**: Syslog over UDP (the default) provides no
encryption or guaranteed delivery. For sensitive environments:

- Use TCP (``@@`` in rsyslog) instead of UDP (``@``)
- Configure TLS between your syslog client and server
- Or use a dedicated log shipper (Fluent Bit, Filebeat) that handles
  reliable delivery and encryption natively


.. _See_Also_Logging_Syslog:

See Also
~~~~~~~~

* :ref:`Recipe_Logging_Journald` for the systemd alternative
* :ref:`Recipe_Piped_Logging` for more piped logging options
* rsyslog documentation: https://www.rsyslog.com/doc/


.. _Recipe_Forensic_Logging:

Forensic logging with mod_log_forensic
----------------------------------------

.. index:: Forensic logging

.. index:: mod_log_forensic

.. index:: ForensicLog directive

.. index:: Logging,forensic

.. index:: Crash debugging


.. _Problem_Forensic_Logging:

Problem
~~~~~~~

You need to capture complete request headers *before* the request is
processed — either because the server crashes during processing (so the
normal access log entry never gets written) or because you need to know
exactly what the client sent for debugging or security analysis.


.. _Solution_Forensic_Logging:

Solution
~~~~~~~~

Enable :module:`mod_log_forensic`:

.. code-block:: apache

   LoadModule log_forensic_module modules/mod_log_forensic.so
   ForensicLog "/var/log/httpd/forensic_log"

To correlate forensic entries with your access log, add the forensic ID
to your ``LogFormat``:

.. code-block:: apache

   LogFormat "%h %l %u %t \"%r\" %>s %b %{forensic-id}n" forensic_combined
   CustomLog "/var/log/httpd/access_log" forensic_combined


.. _Discussion_Forensic_Logging:

Discussion
~~~~~~~~~~

:module:`mod_log_forensic` writes *two* entries for each request:

1. A ``+`` line when the request arrives (before processing), containing
the complete request headers
2. A ``-`` line when the request completes

A forensic log entry looks like:

.. code-block:: text

   +3ZdeEj8AAQEAAAx0BbEAAAAA|GET /app/dashboard HTTP/1.1|Host:www.example.com|User-Agent:Mozilla/5.0 ...|Accept:text/html|Cookie:session=abc123
   -3ZdeEj8AAQEAAAx0BbEAAAAA

Each header is separated by ``|``. The format is fixed — you can't
customize it.

The key use case is crash debugging. If httpd (or a module) crashes while
processing a request, the normal access log entry never gets written.
But the forensic ``+`` line was already written before processing began.
You can identify crashes by finding ``+`` lines without matching ``-``
lines:

.. code-block:: bash

   # The check_forensic script ships with httpd
   check_forensic /var/log/httpd/forensic_log

This script outputs all forensic IDs that have a ``+`` but no ``-`` —
these are requests that never completed.

.. warning::

   The forensic log captures ALL request headers, including
   ``Authorization`` headers (which may contain passwords or tokens) and
   cookies (which contain session IDs). Protect forensic log files
   with strict permissions and don't retain them longer than necessary.

.. note::

   :module:`mod_log_forensic` is strict about logging. If it can't write
   the ``+`` entry (disk full, permissions problem), it will cause the
   child process to exit immediately. This is by design — it prioritizes
   complete forensic records over availability. Don't enable it on a
   server where disk space is unreliable.

POST body content is *not* captured by :module:`mod_log_forensic`. It
records only the request line and headers. If you need to capture request
bodies (and you should think carefully before doing so), you'd need
:module:`mod_dumpio` — but that module dumps everything at the
``trace7`` level to the error log, which is unwieldy.



**When to enable forensic logging**:

- During active incident investigation (enable temporarily)
- On servers processing security-sensitive transactions
- When debugging intermittent crashes that you can't reproduce
- When you need to prove exactly what a client sent (dispute resolution)

**Forensic logging overhead**: The performance impact is relatively low —
it's writing one extra log line before processing and one after. The main
cost is disk I/O and storage. On a server handling 1000 requests/second,
a forensic log will grow at roughly 500KB-1MB per second, depending on
average header size. Plan your storage accordingly, and definitely set up
rotation:

.. code-block:: apache

   ForensicLog "|/usr/sbin/rotatelogs /var/log/httpd/forensic_log.%Y-%m-%d 86400"

**Parsing the forensic log programmatically**:

.. code-block:: bash

   # Extract all unique User-Agent values from incomplete requests
   check_forensic /var/log/httpd/forensic_log | while read id; do
       grep "^+$id" /var/log/httpd/forensic_log | grep -oP 'User-Agent:[^|]+'
   done | sort -u


.. _See_Also_Forensic_Logging:

See Also
~~~~~~~~

* :ref:`Recipe_Correlating_Logs` for the ``%L`` correlation approach
* :ref:`Recipe_Debug_Logging` for :module:`mod_log_debug`
* :module:`mod_log_forensic` documentation:
  https://httpd.apache.org/docs/2.4/mod/mod_log_forensic.html


.. _Recipe_Debug_Logging:

Debug logging with mod_log_debug
---------------------------------

.. index:: mod_log_debug

.. index:: LogMessage directive

.. index:: directives,LogMessage

.. index:: Debug logging

.. index:: Conditional debug output


.. _Problem_Debug_Logging:

Problem
~~~~~~~

You want to inject custom debug messages into the error log based on
conditions — for example, logging the value of a variable at a specific
point in request processing, or logging a message only for requests
matching certain criteria.


.. _Solution_Debug_Logging:

Solution
~~~~~~~~

:version:`2.4`

Use :module:`mod_log_debug` and its ``LogMessage`` directive:

.. code-block:: apache

   LoadModule log_debug_module modules/mod_log_debug.so

   # Log a message for all requests to /api/
   <Location "/api/">
       LogMessage "API request received for %{REQUEST_URI}e"
   </Location>

   # Log only when a specific condition is met
   LogMessage "Slow backend response" "expr=%{RESPONSE_STATUS} == 503"

   # Log the value of a request header
   <Location "/debug/">
       LogMessage "X-Debug-Token: %{reqenv:X-Debug-Token}" hook=fixups
   </Location>

   # Log at every processing hook (for timing analysis)
   <Location "/problematic/">
       LogMessage "Hook reached: %{REQUEST_URI}e" hook=all
   </Location>


.. _Discussion_Debug_Logging:

Discussion
~~~~~~~~~~

:module:`mod_log_debug` (available since httpd 2.3.14) gives you a
``printf``-style debugging tool for request processing. The
``LogMessage`` directive writes to the error log at ``info`` level.

The directive takes up to three arguments:

1. **Message** — the text to log, which can include ``ap_expr``
variables like ``%{REQUEST_URI}e``, ``%{reqenv:VARNAME}``, etc.
2. **hook=name** — which processing phase to log at. The default is
``log_transaction`` (after the request is complete). Other useful
hooks: ``fixups`` (just before the handler), ``translate_name``
(early), or ``all`` (every phase).
3. **expr=condition** — only log when this expression is true.

The ``hook=all`` option is particularly powerful for performance
debugging. Combined with the error log's microsecond timestamps, you can
see exactly how long each processing phase takes:

.. code-block:: text

   [Fri May 09 14:23:01.001234 2026] [log_debug:info] [pid 12345] Hook translate_name: /api/users
   [Fri May 09 14:23:01.001567 2026] [log_debug:info] [pid 12345] Hook check_access: /api/users
   [Fri May 09 14:23:01.002890 2026] [log_debug:info] [pid 12345] Hook check_authn: /api/users
   [Fri May 09 14:23:01.045678 2026] [log_debug:info] [pid 12345] Hook handler: /api/users
   [Fri May 09 14:23:01.945678 2026] [log_debug:info] [pid 12345] Hook log_transaction: /api/users

From this you can see that the handler phase took ~900ms — the backend
is slow.

This is far more targeted than setting ``LogLevel debug`` globally. You
get exactly the information you need, only for the requests you care
about, without the noise of every module's debug output.

.. note::

   :module:`mod_log_debug` has ``Experimental`` status in the official
   documentation, but it has been available and stable since 2.3.14 (and
   is present in all 2.4.x releases). Don't let the "experimental" label
   scare you away from using it.


.. _See_Also_Debug_Logging:

See Also
~~~~~~~~

* :ref:`Section_Error_Log` for ``LogLevel`` per-module
  debugging
* :ref:`Recipe_Forensic_Logging` for capturing raw request data
* :module:`mod_log_debug` documentation:
  https://httpd.apache.org/docs/2.4/mod/mod_log_debug.html


.. _Recipe_Piped_Logging:

Piped logging
--------------

.. index:: Piped logging

.. index:: Logging,piped

.. index:: CustomLog pipe

.. index:: Fluent Bit

.. index:: logstash


.. _Problem_Piped_Logging:

Problem
~~~~~~~

You want to send log output to an external program — for rotation,
filtering, transformation, or direct ingestion into a logging pipeline —
rather than writing to a static file.


.. _Solution_Piped_Logging:

Solution
~~~~~~~~

Prefix the log destination with a pipe character (``|``) followed by the
program path:

.. code-block:: apache

   # Pipe to rotatelogs
   CustomLog "|/usr/sbin/rotatelogs /var/log/httpd/access_log.%Y-%m-%d 86400" combined

   # Pipe to Fluent Bit's stdin input
   CustomLog "|/opt/fluent-bit/bin/fluent-bit -i stdin -o es -p Host=opensearch.internal -p Port=9200 -p Index=httpd-access" json

   # Pipe to a custom processing script
   CustomLog "|/usr/local/bin/log-processor.sh" combined

   # Pipe to cronolog (an alternative to rotatelogs)
   CustomLog "|/usr/bin/cronolog /var/log/httpd/%Y/%m/access_log.%d" combined

For reliable piping (program restarts if it dies):

.. code-block:: apache

   # The "||" prefix restarts the program if it exits
   CustomLog "||/usr/local/bin/my-log-processor" combined


.. _Discussion_Piped_Logging:

Discussion
~~~~~~~~~~

Piped logging is one of httpd's most powerful features. The server
spawns the target program at startup and writes log entries to its
standard input. This gives you a live stream of log data that you can
process however you want.

**The ``|`` vs ``||`` distinction**: A single pipe (``|``) means httpd
starts the program once at server startup. If the program dies, log
entries are lost until the server is restarted. A double pipe (``||``)
tells httpd to restart the program if it exits — this is more resilient
but creates a brief gap during the restart.

**Security**: The piped program runs as the user that started httpd
(typically root, before privilege dropping). Make sure the program is
secure and ideally drops privileges itself.

**Performance**: Each log entry is written immediately to the pipe.
There's no batching or buffering at the httpd level (unless you enable
``BufferedLogs``; see :ref:`Recipe_BufferedLogs`). For high-throughput
logging into a complex pipeline, consider writing to a file and having
the pipeline tail the file instead.

**Common piped logging patterns**:

1. **Rotation**: ``rotatelogs`` is the canonical example
2. **Syslog**: ``logger -t httpd -p local6.info`` sends to syslog
3. **Log shipping**: pipe directly to Fluent Bit, Logstash, or Vector
4. **Filtering**: a script that drops or modifies entries
5. **Splitting**: a script that writes to different files based on content

A practical Fluent Bit integration using a file (more reliable than
direct piping):

.. code-block:: apache

   # httpd writes JSON to a file
   CustomLog "/var/log/httpd/access_log.json" json

Then configure Fluent Bit to tail the file:

.. code-block:: text

   [INPUT]
       Name        tail
       Path        /var/log/httpd/access_log.json
       Parser      json
       Tag         httpd.access
       Refresh_Interval 5

   [OUTPUT]
       Name        opensearch
       Match       httpd.access
       Host        opensearch.internal
       Port        9200
       Index       httpd-access

This "file + tail" pattern is generally more reliable than direct piping
because:

- If the shipper crashes, no log entries are lost (they're in the file)
- httpd never blocks waiting for a slow downstream system
- You can replay logs by re-reading the file



**Error handling in piped programs**: If your piped program can't keep up
or blocks, httpd will eventually block too (the pipe buffer fills up).
On Linux, the default pipe buffer is 64KB. A slow consumer can
stall your entire server. For this reason:

- Keep piped programs fast and non-blocking
- Don't do complex processing inline — write to a spool and process
  asynchronously
- Consider the "file + tail" pattern for anything complex

**A useful pattern — tee to file and pipe**:

.. code-block:: apache

   # Write to file AND pipe to a processor simultaneously
   CustomLog "|/usr/bin/tee -a /var/log/httpd/access_log | /usr/local/bin/log-alert" combined

This gives you the safety of a file (nothing lost if the processor dies)
plus real-time processing. The ``tee`` approach works but adds another
process; for production, a proper log shipper is more robust.

**Piped logging and graceful restarts**: When httpd does a graceful
restart (``apachectl graceful``), piped logging programs are *not*
restarted. The pipe stays open. This means your piped program must handle
long-running operation without memory leaks or file descriptor exhaustion.
On a full restart (``apachectl restart``), the piped program is terminated
and a new instance is spawned.


.. _See_Also_Piped_Logging:

See Also
~~~~~~~~

* :ref:`Recipe_Rotating_Logs` for rotatelogs specifically
* :ref:`Recipe_JSON_Logging` for the JSON format to pipe
* :ref:`Recipe_Logging_Syslog` for the syslog piped approach
* :ref:`Recipe_BufferedLogs` for buffering piped output


.. _Recipe_Measuring_Request_Timing:

Measuring request timing
--------------------------

.. index:: Request timing

.. index:: %T format token

.. index:: %D format token

.. index:: Logging,performance

.. index:: Slow requests


.. _Problem_Measuring_Request_Timing:

Problem
~~~~~~~

You want to identify slow requests by logging how long each request takes
to process.


.. _Solution_Measuring_Request_Timing:

Solution
~~~~~~~~

Add timing tokens to your ``LogFormat``:

.. code-block:: apache

   # Time in seconds (integer)
   LogFormat "%h %t \"%r\" %>s %b %T" timed

   # Time in microseconds (most precise)
   LogFormat "%h %t \"%r\" %>s %b %D" timed_micro

   # Time in milliseconds (best balance of precision and readability)
   LogFormat "%h %t \"%r\" %>s %b %{ms}T" timed_ms

A practical format for identifying slow requests:

.. code-block:: apache

   LogFormat "%a %t \"%r\" %>s %b %{ms}T \"%{Referer}i\" \"%{User-Agent}i\"" performance
   CustomLog "/var/log/httpd/access_log" performance

Combined with conditional logging to create a slow-request log:

.. code-block:: apache

   CustomLog "/var/log/httpd/slow_requests.log" performance "expr=%T >= 2"


.. _Discussion_Measuring_Request_Timing:

Discussion
~~~~~~~~~~

httpd provides three timing tokens:

+-------------+----------------+-------------------------------------------+
| Token       | Unit           | Notes                                     |
+-------------+----------------+-------------------------------------------+
| ``%T``      | Seconds        | Integer — rounds down. A 1.9s request     |
|             |                | shows as ``1``.                           |
+-------------+----------------+-------------------------------------------+
| ``%D``      | Microseconds   | Most precise, but large numbers are hard  |
|             |                | to read at a glance.                      |
+-------------+----------------+-------------------------------------------+
| ``%{ms}T``  | Milliseconds   | :version:`2.4.13`. Best for human         |
|             |                | reading and log analysis.                 |
+-------------+----------------+-------------------------------------------+
| ``%{us}T``  | Microseconds   | :version:`2.4.13`. Same as ``%D``.        |
+-------------+----------------+-------------------------------------------+
| ``%{s}T``   | Seconds        | :version:`2.4.13`. Same as ``%T``.        |
+-------------+----------------+-------------------------------------------+

The timer starts when httpd reads the first byte of the request from the
OS and stops when the last byte of the response is handed to the OS for
sending. This means:

- It does NOT include TCP/TLS handshake time
- It does NOT include time for the response to traverse the network
- It DOES include time spent waiting for backend applications (proxy,
  CGI, PHP-FPM)
- It DOES include time to read a slow client's request body (large
  uploads)

For performance monitoring, I recommend ``%{ms}T`` — milliseconds are
the right granularity for web requests. A human can quickly see that
``45`` is fine and ``3500`` is a problem.

To find your slowest requests:

.. code-block:: bash

   # Top 20 slowest requests today
   awk '{print $(NF-2), $0}' /var/log/httpd/access_log | sort -rn | head -20

Or with the ``expr=`` conditional logging, maintain a dedicated slow
request log that you can monitor with alerts.


.. _See_Also_Measuring_Request_Timing:

See Also
~~~~~~~~

* :ref:`Recipe_JSON_Logging` for including timing in structured logs
* :ref:`Recipe_Debug_Logging` for per-phase timing with ``hook=all``
* :ref:`Recipe_Tracking_Bytes` for bandwidth measurement


.. _Recipe_Tracking_Bytes:

Tracking bytes with mod_logio
------------------------------

.. index:: mod_logio

.. index:: %I format token

.. index:: %O format token

.. index:: Bandwidth accounting

.. index:: Logging,bytes transferred


.. _Problem_Tracking_Bytes:

Problem
~~~~~~~

You want to log the actual number of bytes transferred over the network
— including headers, SSL overhead, and chunked encoding — not just the
response body size.


.. _Solution_Tracking_Bytes:

Solution
~~~~~~~~

Load :module:`mod_logio` and use the ``%I`` and ``%O`` format tokens:

.. code-block:: apache

   LoadModule logio_module modules/mod_logio.so

   LogFormat "%a %l %u %t \"%r\" %>s %b %I %O \"%{Referer}i\" \"%{User-Agent}i\"" bandwidth
   CustomLog "/var/log/httpd/access_log" bandwidth


.. _Discussion_Tracking_Bytes:

Discussion
~~~~~~~~~~

The standard ``%b`` and ``%B`` tokens measure only the response body
size — the content you're sending, minus HTTP headers. For most logging
purposes, that's fine. But for bandwidth accounting, capacity planning,
or billing, you need the *actual* bytes on the wire.

:module:`mod_logio` provides two additional tokens:

+--------+-----------------------------------------------------------+
| Token  | Meaning                                                   |
+--------+-----------------------------------------------------------+
| ``%I`` | Total bytes received from the client (request headers +   |
|        | body). Includes SSL/TLS overhead.                         |
+--------+-----------------------------------------------------------+
| ``%O`` | Total bytes sent to the client (response headers + body). |
|        | Includes SSL/TLS overhead.                                |
+--------+-----------------------------------------------------------+

The difference between ``%O`` and ``%b`` can be significant:

- HTTP response headers typically add 200-500 bytes per response
- TLS record framing adds overhead to every packet
- Chunked transfer encoding adds framing bytes

For a server handling millions of small requests (APIs, image
thumbnails), the header overhead measured by ``%O`` but not ``%b`` can
represent 10-20% of your actual bandwidth.

:module:`mod_logio` also provides a combined token ``%S`` (since httpd
2.4.7) which is the sum of ``%I`` and ``%O`` — total bytes in both
directions for the request.

A bandwidth-monitoring log format:

.. code-block:: apache

   LogFormat "%v %a %t \"%r\" %>s %I %O %S %{ms}T" bandwidth_full
   CustomLog "/var/log/httpd/bandwidth.log" bandwidth_full

This gives you per-vhost, per-request bandwidth data that you can
aggregate for capacity planning.


.. _See_Also_Tracking_Bytes:

See Also
~~~~~~~~

* :ref:`Recipe_Measuring_Request_Timing` for performance measurement
* :ref:`Recipe_JSON_Logging` for including ``%O`` in structured logs
* :module:`mod_logio` documentation:
  https://httpd.apache.org/docs/2.4/mod/mod_logio.html


.. _Recipe_BufferedLogs:

BufferedLogs for performance
-----------------------------

.. index:: BufferedLogs directive

.. index:: directives,BufferedLogs

.. index:: Logging,performance

.. index:: Logging,buffering


.. _Problem_BufferedLogs:

Problem
~~~~~~~

On a high-traffic server, you want to reduce the I/O overhead of
writing to log files on every single request.


.. _Solution_BufferedLogs:

Solution
~~~~~~~~

Enable ``BufferedLogs`` in your server configuration (global scope only):

.. code-block:: apache

   BufferedLogs On


.. _Discussion_BufferedLogs:

Discussion
~~~~~~~~~~

Normally, httpd writes each log entry to disk immediately after the
request completes. On a server handling thousands of requests per second,
this means thousands of small writes per second. ``BufferedLogs`` causes
:module:`mod_log_config` to batch multiple log entries in memory and
write them together in larger blocks.

The trade-offs:

**Advantages**:

- Fewer disk I/O operations (better for spinning disks)
- Slightly reduced per-request overhead
- May improve throughput under extreme load

**Disadvantages**:

- If the server crashes, buffered entries that haven't been flushed are
  lost
- Log entries appear with a slight delay
- Cannot be set per virtual host — it's a global setting
- Interleaving of entries from different requests/threads may change

**When to use it**: Honestly, for most servers in 2026, you don't need
this. Modern SSDs handle thousands of small writes effortlessly, and the
OS filesystem layer provides its own write buffering. ``BufferedLogs``
was more impactful in the era of spinning disks and slow I/O subsystems.

Consider enabling it if:

- You're writing to a network filesystem (NFS) where each write has
  latency
- You've profiled your server and confirmed that log I/O is a
  bottleneck
- You're processing tens of thousands of requests per second and every
  microsecond matters

For most servers, the crash-safety risk outweighs the performance gain.
If log write performance is genuinely a problem, piped logging to a
buffered receiver (Fluent Bit, rsyslog) is usually a better approach.


.. _See_Also_BufferedLogs:

See Also
~~~~~~~~

* :ref:`Recipe_Piped_Logging` for an alternative approach to log
  performance
* :ref:`Recipe_Rotating_Logs` for managing high-volume log files
* :module:`mod_log_config` documentation:
  https://httpd.apache.org/docs/2.4/mod/mod_log_config.html#bufferedlogs


.. _Recipe_Log_Analysis:

Log analysis in 2026
---------------------

.. index:: Log analysis

.. index:: GoAccess

.. index:: AWStats

.. index:: OpenSearch

.. index:: ELK stack

.. index:: CloudWatch Logs Insights


.. _Problem_Log_Analysis:

Problem
~~~~~~~

You've been collecting log data and now you want to analyze it — see
traffic patterns, identify problems, generate reports, or set up
dashboards. What tools should you use in 2026?


.. _Solution_Log_Analysis:

Solution
~~~~~~~~

The right tool depends on your scale and needs:

**For quick, real-time terminal analysis**: GoAccess

.. code-block:: bash

   # Real-time dashboard in your terminal
   goaccess /var/log/httpd/access_log --log-format=COMBINED

   # Generate a standalone HTML report
   goaccess /var/log/httpd/access_log --log-format=COMBINED -o /var/www/stats/report.html

   # Real-time HTML report (auto-refreshing)
   goaccess /var/log/httpd/access_log --log-format=COMBINED -o /var/www/stats/report.html --real-time-html

**For serious infrastructure-scale analysis**: OpenSearch or Elasticsearch

Feed JSON-formatted logs (see :ref:`Recipe_JSON_Logging`) via Fluent Bit,
Filebeat, or Logstash into OpenSearch. Query with dashboards.

**For AWS environments**: CloudWatch Logs Insights

Ship logs to CloudWatch, then query:

.. code-block:: text

   fields @timestamp, client, method, uri, status, duration_us
   | filter status >= 500
   | stats count(*) as errors by uri
   | sort errors desc
   | limit 20


.. _Discussion_Log_Analysis:

Discussion
~~~~~~~~~~

The log analysis landscape has changed dramatically. Here's an honest
assessment of the options:

**GoAccess** (https://goaccess.io/) — version 1.10 as of early 2026.
This is the best tool for single-server, file-based log analysis.
It's fast (processes millions of lines in seconds), runs in a terminal
or generates beautiful HTML reports, respects privacy (no data leaves
your server), and understands all common log formats out of the box.
Use it when you want a quick answer to "what's happening on my server?"
without setting up infrastructure.

**OpenSearch / Elasticsearch + Kibana / Dashboards** — the standard for
multi-server, searchable, dashboarded log analysis. This is significant
infrastructure to run (or pay for as a managed service), but it gives
you full-text search, field-based filtering, time-series visualization,
and alerting. If you're running more than a handful of servers, this is
the way.

**CloudWatch Logs Insights** — if you're on AWS, this is the lowest-
friction option. Ship logs to CloudWatch (via the CloudWatch agent or
Fluent Bit), and you get a SQL-like query language without managing
any additional infrastructure. The query syntax is limited compared to
full Elasticsearch, but it's often enough.

**Splunk** — the enterprise incumbent. Expensive but powerful.
If your organization already has Splunk, feed your JSON logs into it.

**AWStats** — still exists, still works, but hasn't had significant
development in years. I'd use GoAccess instead for the same use case.

**Webalizer** — dead. Don't use it.

**Google Analytics / client-side tracking** — these solve a different
problem (user behavior analytics, not server operations). They miss
bot traffic, API calls, and errors. They're complementary to server
logs, not a replacement.

My recommendation for most people: start with GoAccess for immediate
visibility. When you outgrow a single server, invest in OpenSearch or
your cloud provider's managed log solution, and switch to JSON logging
as the output format.


.. _See_Also_Log_Analysis:

See Also
~~~~~~~~

* :ref:`Recipe_JSON_Logging` for producing analysis-ready logs
* :ref:`Recipe_Measuring_Request_Timing` for the data to analyze
* GoAccess: https://goaccess.io/
* OpenSearch: https://opensearch.org/



.. _Recipe_Format_Token_Reference:

Quick reference: LogFormat tokens
----------------------------------

.. index:: LogFormat tokens,reference

.. index:: Format tokens,complete list


For convenience, here is a consolidated reference of the most commonly
used ``LogFormat`` tokens. For the complete list, see the
:module:`mod_log_config` documentation.

**Request information**:

+---------------------+----------------------------------------------------+
| Token               | Description                                        |
+---------------------+----------------------------------------------------+
| ``%r``              | First line of request (method + URI + protocol)    |
+---------------------+----------------------------------------------------+
| ``%m``              | Request method (GET, POST, etc.)                   |
+---------------------+----------------------------------------------------+
| ``%U``              | URL path (without query string)                    |
+---------------------+----------------------------------------------------+
| ``%q``              | Query string (with leading ``?``, or empty)        |
+---------------------+----------------------------------------------------+
| ``%H``              | Request protocol (HTTP/1.1, HTTP/2, etc.)          |
+---------------------+----------------------------------------------------+
| ``%{Header}i``      | Any request header value                           |
+---------------------+----------------------------------------------------+

**Client information**:

+---------------------+----------------------------------------------------+
| Token               | Description                                        |
+---------------------+----------------------------------------------------+
| ``%h``              | Remote hostname/IP (affected by mod_remoteip)      |
+---------------------+----------------------------------------------------+
| ``%a``              | Client IP (affected by mod_remoteip)               |
+---------------------+----------------------------------------------------+
| ``%{c}a``           | Underlying connection peer IP (always the proxy)   |
+---------------------+----------------------------------------------------+
| ``%l``              | Remote logname from identd (always ``-``)          |
+---------------------+----------------------------------------------------+
| ``%u``              | Remote user (authenticated)                        |
+---------------------+----------------------------------------------------+

**Response information**:

+---------------------+----------------------------------------------------+
| Token               | Description                                        |
+---------------------+----------------------------------------------------+
| ``%>s``             | Final HTTP status code                             |
+---------------------+----------------------------------------------------+
| ``%s``              | Original status (before internal redirects)        |
+---------------------+----------------------------------------------------+
| ``%b``              | Response body bytes (``-`` if zero) — CLF format   |
+---------------------+----------------------------------------------------+
| ``%B``              | Response body bytes (``0`` if zero)                |
+---------------------+----------------------------------------------------+
| ``%{Header}o``      | Any response header value                          |
+---------------------+----------------------------------------------------+
| ``%I``              | Total bytes received (mod_logio required)          |
+---------------------+----------------------------------------------------+
| ``%O``              | Total bytes sent (mod_logio required)              |
+---------------------+----------------------------------------------------+
| ``%S``              | Total bytes transferred: %I + %O (mod_logio)      |
+---------------------+----------------------------------------------------+

**Timing**:

+---------------------+----------------------------------------------------+
| Token               | Description                                        |
+---------------------+----------------------------------------------------+
| ``%T``              | Request time in seconds (integer)                  |
+---------------------+----------------------------------------------------+
| ``%D``              | Request time in microseconds                       |
+---------------------+----------------------------------------------------+
| ``%{ms}T``          | Request time in milliseconds (2.4.13+)             |
+---------------------+----------------------------------------------------+
| ``%{us}T``          | Request time in microseconds (2.4.13+)             |
+---------------------+----------------------------------------------------+

**Timestamps**:

+---------------------------+------------------------------------------------+
| Token                     | Description                                    |
+---------------------------+------------------------------------------------+
| ``%t``                    | Standard timestamp [DD/Mon/YYYY:HH:MM:SS +TZ]  |
+---------------------------+------------------------------------------------+
| ``%{%Y-%m-%dT%H:%M:%S}t``| Custom strftime format                         |
+---------------------------+------------------------------------------------+
| ``%{msec_frac}t``         | Millisecond fraction (.NNN)                    |
+---------------------------+------------------------------------------------+
| ``%{usec_frac}t``         | Microsecond fraction (.NNNNNN)                 |
+---------------------------+------------------------------------------------+
| ``%{begin:%s}t``          | Unix epoch at request start                    |
+---------------------------+------------------------------------------------+
| ``%{end:%s}t``            | Unix epoch at request end                      |
+---------------------------+------------------------------------------------+

**Server information**:

+---------------------+----------------------------------------------------+
| Token               | Description                                        |
+---------------------+----------------------------------------------------+
| ``%v``              | Canonical ServerName of the serving vhost          |
+---------------------+----------------------------------------------------+
| ``%V``              | Server name per UseCanonicalName                   |
+---------------------+----------------------------------------------------+
| ``%p``              | Canonical server port                              |
+---------------------+----------------------------------------------------+
| ``%A``              | Local IP address                                   |
+---------------------+----------------------------------------------------+
| ``%P``              | Process ID of the child                            |
+---------------------+----------------------------------------------------+
| ``%{tid}P``         | Thread ID                                          |
+---------------------+----------------------------------------------------+

**Metadata and correlation**:

+---------------------+----------------------------------------------------+
| Token               | Description                                        |
+---------------------+----------------------------------------------------+
| ``%L``              | Request log ID (for error log correlation)         |
+---------------------+----------------------------------------------------+
| ``%{c}L``           | Connection log ID                                  |
+---------------------+----------------------------------------------------+
| ``%{VARNAME}e``     | Environment variable                               |
+---------------------+----------------------------------------------------+
| ``%{VARNAME}n``     | Module note                                        |
+---------------------+----------------------------------------------------+
| ``%{VARNAME}C``     | Cookie value                                       |
+---------------------+----------------------------------------------------+
| ``%k``              | Keepalive request count on this connection          |
+---------------------+----------------------------------------------------+
| ``%X``              | Connection status (``X`` = aborted, ``+`` = keep-  |
|                     | alive, ``-`` = closed)                             |
+---------------------+----------------------------------------------------+
| ``%R``              | Handler that generated the response                |
+---------------------+----------------------------------------------------+

**Modifiers**: Place between ``%`` and the format character:

- ``>`` — use value from final request (after internal redirects)
- ``<`` — use value from original request
- ``400,404`` — only log for these status codes (else ``-``)
- ``!200,304`` — only log for statuses NOT in this list



Summary
-------

Logging is infrastructure. Like any infrastructure, it's invisible when
it works and catastrophic when it doesn't. The recipes in this chapter
give you the tools to build a logging setup that's useful for daily
operations, powerful for debugging, and ready for whatever observability
stack you're feeding.

Start with the Combined format and a rotation strategy. Add timing
(``%{ms}T``) because you'll always want to find slow requests. Consider
JSON output early — converting later is painful. And keep your error log
verbosity production-appropriate, but remember that per-module
``LogLevel`` lets you zoom in surgically when things go wrong.

Your future self, at 2 AM debugging a production issue, will thank your
past self for setting up good logging.
