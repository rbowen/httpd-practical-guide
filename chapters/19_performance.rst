.. raw:: latex

   \part{Operations}

.. comment::
   NOTE: The Nikto security scanning recipe has been relocated to
   Chapter 10 (Security). The mod_dialup recipe has been removed
   (novelty module, not relevant to production workloads).
   The mod_perl/CGI speedup recipe has been removed (dated; mod_proxy_fcgi
   is the modern approach, covered briefly in the MPM recipe discussion).
   Disabling content negotiation and optimizing symbolic links recipes
   were removed as too obscure for a 2026 audience.

.. _Chapter_Performance_and_testing:

===========
Performance
===========

.. epigraph::

   I feel the need — the need for speed.

   -- Kenny Loggins, *Danger Zone* (via Top Gun)


.. index:: performance
.. index:: tuning
.. index:: optimization


Your site can almost certainly be made faster. The question is how much
time you're willing to invest, and what trade-offs you'll accept.
Performance tuning is not a one-size-fits-all exercise — a configuration
that doubles throughput on one server can tank another. The only way to
know what works for *your* workload is to measure, change one thing, and
measure again.

This chapter covers the levers that matter most in a modern Apache HTTP
Server deployment: choosing and tuning the right Multi-Processing Module
(MPM), enabling HTTP/2, configuring compression, setting up content
caching, and controlling browser cache behavior. I've ordered the
recipes roughly from "biggest impact, least effort" to "specialized
tuning for specific workloads." If you're short on time, start with the
MPM and compression recipes — those two changes alone can transform a
sluggish server.

A word of caution: don't tune in production without testing first. Set
up a staging environment that mirrors your production load as closely as
possible, apply your changes there, benchmark, and only then roll them
out. I've seen more outages caused by "performance improvements" than by
any other category of configuration change.


.. admonition:: Modules covered in this chapter

   :module:`mod_brotli`, :module:`mod_cache`, :module:`mod_cache_disk`,
   :module:`mod_deflate`, :module:`mod_expires`, :module:`mod_file_cache`,
   :module:`mod_headers`, :module:`mod_http2`, :module:`mod_ratelimit`,
   :module:`mod_status`, :module:`mpm_common`, :module:`event`,
   :module:`worker`, :module:`prefork`


.. _Recipe_choosing-mpm:

.. index:: MPM
.. index:: Multi-Processing Module
.. index:: event MPM
.. index:: worker MPM
.. index:: prefork MPM
.. index:: mod_php
.. index:: PHP-FPM

Choosing the right MPM
----------------------


.. _Problem_choosing-mpm:

Problem
~~~~~~~

You want to select the Multi-Processing Module that gives you the best
performance characteristics for your workload.


.. _Solution_choosing-mpm:

Solution
~~~~~~~~

Use the Event MPM. It is the default on all modern distributions and
the best choice for the vast majority of workloads:

.. code-block:: bash

   # Verify your current MPM (RHEL/CentOS/Fedora)
   httpd -V | grep -i mpm

   # Verify on Debian/Ubuntu
   apachectl -V | grep -i mpm

On RHEL-family systems, edit :file:`/etc/httpd/conf.modules.d/00-mpm.conf`
and ensure only the Event MPM is loaded:

.. code-block:: apache

   # /etc/httpd/conf.modules.d/00-mpm.conf
   # Only ONE MPM may be loaded at a time.

   # LoadModule mpm_prefork_module modules/mod_mpm_prefork.so
   # LoadModule mpm_worker_module modules/mod_mpm_worker.so
   LoadModule mpm_event_module modules/mod_mpm_event.so

On Debian/Ubuntu, use the ``a2dismod`` / ``a2enmod`` mechanism:

.. code-block:: bash

   sudo a2dismod mpm_prefork
   sudo a2enmod mpm_event
   sudo systemctl restart apache2


.. _Discussion_choosing-mpm:

Discussion
~~~~~~~~~~

httpd offers three production MPMs, each with a fundamentally different
concurrency model:

**Prefork** spawns one process per connection. Each process handles
exactly one request at a time. This is the oldest model, and it still
exists for a single reason: non-thread-safe modules. The canonical
example is ``mod_php`` (also called ``libapache2-mod-php`` on Debian
systems). Because PHP's internal state is not thread-safe, embedding
PHP directly in a multi-threaded httpd process causes crashes. If you
must run ``mod_php``, you're stuck with Prefork.

But you almost certainly shouldn't run ``mod_php`` anymore. PHP-FPM
(FastCGI Process Manager) is the modern way to run PHP with httpd. It
runs PHP in a separate pool of processes, communicating with httpd over
a FastCGI socket. This frees httpd to use the Event MPM while PHP
manages its own process lifecycle. The performance difference is
dramatic — I've seen sites go from 200 concurrent connections on Prefork
to 2,000+ on Event with PHP-FPM, on identical hardware.

**Worker** spawns multiple processes, each containing multiple threads.
A request is handled by a single thread within a process. This is more
memory-efficient than Prefork because threads share the process's
address space. Worker handles high concurrency well, but it has a
weakness: KeepAlive connections tie up a worker thread while idle.

**Event** extends the Worker model by adding a dedicated listener thread
per process. When a connection goes idle (waiting for a new request on a
KeepAlive connection, or waiting for I/O), it is handed off to the
listener thread, freeing the worker thread to handle other requests.
This makes Event dramatically more efficient under KeepAlive-heavy
workloads — which is essentially all modern web traffic.

The bottom line: use Event unless you have a specific, known reason not
to. The only legitimate reason is running a non-thread-safe module
that cannot be replaced with an external process manager.

.. table:: MPM comparison at a glance
   :widths: 25 25 25 25

   +-------------------+----------+----------+----------+
   |                   | Prefork  | Worker   | Event    |
   +===================+==========+==========+==========+
   | Concurrency model | Process  | Thread   | Thread + |
   |                   |          |          | async IO |
   +-------------------+----------+----------+----------+
   | Memory per conn.  | High     | Low      | Lowest   |
   +-------------------+----------+----------+----------+
   | KeepAlive cost    | Blocks a | Blocks a | Nearly   |
   |                   | process  | thread   | free     |
   +-------------------+----------+----------+----------+
   | HTTP/2 support    | Degraded | Full     | Full     |
   +-------------------+----------+----------+----------+
   | Thread safety req | No       | Yes      | Yes      |
   +-------------------+----------+----------+----------+
   | Recommended       | Legacy   | Niche    | Default  |
   +-------------------+----------+----------+----------+


.. _See_Also_choosing-mpm:

See Also
~~~~~~~~

* https://httpd.apache.org/docs/current/mpm.html
* https://httpd.apache.org/docs/current/mod/event.html
* :ref:`Recipe_tuning-event-mpm`
* :ref:`Recipe_enabling-http2`


.. _Recipe_tuning-event-mpm:

.. index:: ThreadsPerChild
.. index:: MaxRequestWorkers
.. index:: ServerLimit
.. index:: AsyncRequestWorkerFactor
.. index:: StartServers
.. index:: MinSpareThreads
.. index:: MaxSpareThreads
.. index:: MaxConnectionsPerChild
.. index:: event MPM; tuning

Tuning the event MPM
--------------------


.. _Problem_tuning-event-mpm:

Problem
~~~~~~~

You want to tune the Event MPM's directives to handle your expected
concurrency without running out of memory or rejecting connections.


.. _Solution_tuning-event-mpm:

Solution
~~~~~~~~

Configure the Event MPM parameters based on your available RAM and
expected peak concurrency. Here is a well-tuned configuration for a
server with 8 GB of RAM serving a moderately busy site:

.. code-block:: apache

   <IfModule mpm_event_module>
       StartServers              3
       MinSpareThreads          75
       MaxSpareThreads         250
       ThreadsPerChild          25
       MaxRequestWorkers        400
       ServerLimit               16
       MaxConnectionsPerChild 10000
       AsyncRequestWorkerFactor   2
   </IfModule>

For a high-traffic server with 32 GB of RAM:

.. code-block:: apache

   <IfModule mpm_event_module>
       StartServers              5
       MinSpareThreads         150
       MaxSpareThreads         500
       ThreadsPerChild          64
       MaxRequestWorkers       1024
       ServerLimit               16
       MaxConnectionsPerChild 50000
       AsyncRequestWorkerFactor   2
   </IfModule>


.. _Discussion_tuning-event-mpm:

Discussion
~~~~~~~~~~

The Event MPM has several interlocking directives. Here's what each
one actually does:

``ThreadsPerChild`` sets the number of worker threads spawned within
each child process. This is the most important tuning knob. Each thread
can handle one active request at a time. The default is 25, which is
conservative. On a server with plenty of RAM, values of 64 or even 128
are common. Higher values mean fewer child processes for the same total
capacity, which reduces inter-process overhead.

``MaxRequestWorkers`` (formerly ``MaxClients``) is the hard ceiling on
the total number of threads available to handle requests across all
child processes. Once all threads are busy, new connections queue until
a thread becomes available. If the queue fills, clients receive 503
errors.

The relationship between these two directives is:

.. code-block:: text

   MaxRequestWorkers = ServerLimit × ThreadsPerChild

``ServerLimit`` sets the maximum number of child processes. You
cannot set ``MaxRequestWorkers`` higher than ``ServerLimit ×
ThreadsPerChild``. If you need more capacity than the default allows,
increase ``ServerLimit`` — but note that this directive can only be
changed by stopping and starting httpd, not by a graceful restart.

``AsyncRequestWorkerFactor`` is specific to the Event MPM and controls
how many additional connections can be in an asynchronous (idle) state
per worker thread. The total connection capacity of a child process is:

.. code-block:: text

   connections = ThreadsPerChild + (AsyncRequestWorkerFactor × idle_workers)

With the default value of 2 and 25 threads per child, a single process
can hold up to 75 connections (25 active + 50 idle KeepAlive). Increase
this value if your site has a high ratio of idle KeepAlive connections
to active requests — which is typical for sites with long-polling or
Server-Sent Events.

``StartServers`` controls how many child processes are spawned at
startup. Set this to roughly the number you expect to be running during
normal (non-peak) operation. httpd dynamically spawns and kills
children based on load, but starting with a reasonable number avoids
a thundering herd of process creation when traffic ramps up after a
restart.

``MinSpareThreads`` and ``MaxSpareThreads`` control how eagerly httpd
creates or destroys idle threads. If idle threads drop below
``MinSpareThreads``, httpd spawns new child processes. If they exceed
``MaxSpareThreads``, httpd kills idle children. The defaults are fine for
most workloads.

``MaxConnectionsPerChild`` sets how many connections a child process
handles before it's recycled (killed and replaced). This guards against
memory leaks in modules or the server itself. A value of 0 means
children never die, which is fine if you're confident about memory
stability. Values between 5000 and 50000 are common for production.

**The tuning formula.** Start with this approach:

1. Determine how much RAM httpd can use (total RAM minus OS, database,
and other services).

2. Measure the RSS (Resident Set Size) of a typical httpd child process
under load using ``ps`` or ``top``.

3. Divide available RAM by per-process RSS to get your maximum number of
child processes (``ServerLimit``).

4. Multiply ``ServerLimit × ThreadsPerChild`` to get your
``MaxRequestWorkers``.

.. code-block:: bash

   # Measure average httpd process size
   ps -C httpd -o rss= | awk '{sum+=$1; n++} END {print sum/n/1024 " MB average"}'

If each process uses 50 MB and you have 3 GB available for httpd,
you can run about 60 processes. With ``ThreadsPerChild 25``, that gives
you ``MaxRequestWorkers 1500``. You probably don't need that many — set
``ServerLimit`` conservatively and let httpd scale dynamically.

**Warning: the "reached MaxRequestWorkers" error.** If you see this in
your error log:

.. code-block:: text

   AH00286: server reached MaxRequestWorkers setting, consider raising...

don't blindly increase the value. First check whether your threads are
actually doing useful work or are blocked waiting for slow backends. A
slow database or upstream proxy can exhaust your thread pool regardless
of how many threads you configure. Use :module:`mod_status` with
``ExtendedStatus On`` to see what each thread is doing.


.. _See_Also_tuning-event-mpm:

See Also
~~~~~~~~

* https://httpd.apache.org/docs/current/mod/event.html
* https://httpd.apache.org/docs/current/mod/mpm_common.html
* :ref:`Recipe_how-much-ram`
* :ref:`Recipe_benchmarking`


.. _Recipe_how-much-ram:

.. index:: memory
.. index:: RAM
.. index:: sizing
.. index:: MaxRequestWorkers; memory calculation
.. index:: ps command
.. index:: top command

Determining how much memory you need
------------------------------------


.. _Problem_how-much-ram:

Problem
~~~~~~~

You want to ensure your server has sufficient RAM to handle peak load
without swapping.


.. _Solution_how-much-ram:

Solution
~~~~~~~~

Measure the memory footprint of your httpd processes under realistic
load, then calculate the maximum you can safely run:

.. code-block:: bash

   # Get the RSS of each httpd process in MB
   ps -C httpd -o pid,rss,comm --sort=-rss | head -20

   # Or get an average
   ps -C httpd -o rss= | awk '{sum+=$1; n++} END {
       printf "Processes: %d\nAvg RSS: %.1f MB\nTotal: %.1f MB\n",
              n, sum/n/1024, sum/1024
   }'

Then apply the formula:

.. code-block:: text

   Available RAM for httpd = Total RAM - OS overhead - other services
   Max child processes = Available RAM / average process RSS
   MaxRequestWorkers = Max child processes × ThreadsPerChild


.. _Discussion_how-much-ram:

Discussion
~~~~~~~~~~

The single biggest hardware factor affecting httpd performance is RAM.
A server that swaps is a server that has failed — swap latency is orders
of magnitude slower than RAM, and under load, a swapping server
enters a death spiral where thrashing consumes the very CPU cycles
needed to recover.

The golden rule: ``MaxRequestWorkers`` must be set low enough that httpd
*never* drives the system into swap, even at peak load.

**What consumes memory in an httpd process?** The base httpd process
uses relatively little memory. The real consumers are:

- Loaded modules (especially heavy ones like :module:`mod_ssl`,
  :module:`mod_lua`, or embedded interpreters)
- Per-request buffers (particularly for large request bodies or
  proxied responses)
- Application frameworks running inside httpd (this is rare in
  modern deployments; most apps run in external processes)
- Shared memory segments for the scoreboard and SSL session cache

With the Event MPM and no embedded application code, a typical httpd
child process uses 30–80 MB of RSS. With PHP-FPM as the backend, the
httpd processes stay lean and the PHP memory usage is accounted for
separately in the FPM pool.

**Measuring under realistic load.** Don't measure memory on a freshly
started, idle server. httpd processes grow as they handle requests — they
allocate buffers, load cached data, and accumulate state. Measure after
the server has been handling production-like traffic for at least 30
minutes.

If you're using ``MaxConnectionsPerChild`` to recycle processes (and
you should), measure processes that have handled several thousand
requests — that's their steady-state size.

**Don't forget the other tenants.** On a server that also runs a
database, cache daemon, or application server, you must subtract their
memory requirements first. A common mistake is calculating httpd
capacity based on total RAM, then watching the OOM killer slaughter
processes when MySQL and httpd both try to use the same memory.

**The safety margin.** I recommend keeping at least 10–15% of total RAM
free as a safety margin. The kernel needs memory for filesystem caches,
network buffers, and its own bookkeeping. Starve it of this and you'll
see mysterious slowdowns even without hitting swap.


.. _See_Also_how-much-ram:

See Also
~~~~~~~~

* https://httpd.apache.org/docs/current/misc/perf-tuning.html
* :ref:`Recipe_tuning-event-mpm`


.. _Recipe_benchmarking:

.. index:: benchmarking
.. index:: ab (Apache Bench)
.. index:: h2load
.. index:: load testing
.. index:: performance testing

Benchmarking with ab and h2load
-------------------------------


.. _Problem_benchmarking:

Problem
~~~~~~~

You want to measure the impact of configuration changes on server
performance, and you need a tool that supports both HTTP/1.1 and
HTTP/2 testing.


.. _Solution_benchmarking:

Solution
~~~~~~~~

Use ``ab`` (Apache Bench) for quick HTTP/1.1 tests:

.. code-block:: bash

   # 10,000 requests, 100 concurrent connections, with KeepAlive
   ab -n 10000 -c 100 -k http://www.example.com/index.html

Use ``h2load`` (part of the nghttp2 package) to benchmark HTTP/2:

.. code-block:: bash

   # Install nghttp2 (includes h2load)
   # RHEL/CentOS:
   sudo dnf install nghttp2

   # Debian/Ubuntu:
   sudo apt install nghttp2-client

   # 10,000 requests, 100 concurrent streams, 10 connections
   h2load -n 10000 -c 10 -m 100 https://www.example.com/index.html


.. _Discussion_benchmarking:

Discussion
~~~~~~~~~~

**ab (Apache Bench)** ships with httpd and is the quickest way to
measure throughput for a single URL. Its output includes requests per
second, mean response time, and percentile distribution. Key flags:

- ``-n`` — total number of requests
- ``-c`` — number of concurrent connections
- ``-k`` — enable HTTP/1.1 KeepAlive
- ``-H`` — add a custom header (useful for testing with
  ``Accept-Encoding: gzip, br`` to verify compression)
- ``-p`` / ``-T`` — POST a file with a given content type

.. code-block:: text

   $ ab -n 5000 -c 50 -k http://localhost/index.html
   ...
   Requests per second:    4523.17 [#/sec] (mean)
   Time per request:       11.055 [ms] (mean)
   Transfer rate:          12845.23 [Kbytes/sec] received

**h2load** is the HTTP/2 equivalent. Because HTTP/2 multiplexes many
streams over fewer TCP connections, the concurrency model is different.
Key flags:

- ``-n`` — total requests
- ``-c`` — number of TCP connections
- ``-m`` — maximum concurrent streams per connection (this is the
  HTTP/2 multiplexing factor)
- ``-t`` — number of threads (for saturating the client side)

.. code-block:: text

   $ h2load -n 10000 -c 4 -m 100 https://localhost/index.html
   finished in 1.23s, 8130.08 req/s, 24.39MB/s

**Best practices for benchmarking:**

1. Never run the benchmark tool on the same machine as the server.
You'll measure the client's resource contention, not the server's
capacity.

2. Change one variable at a time. If you change ``ThreadsPerChild`` and
enable compression simultaneously, you won't know which change
affected the results.

3. Run each test multiple times and average the results. Network jitter,
kernel scheduling, and background processes introduce noise.

4. Use a representative URL. Benchmarking a static HTML file tells you
nothing about the performance of your CGI scripts or proxied
applications. Test what your users actually hit.

5. Watch the server side too. While the benchmark runs, monitor httpd
with :module:`mod_status` (``/server-status?auto``) and watch system
metrics with ``top``, ``vmstat``, or ``sar``. A throughput number
without context is meaningless — you need to know whether the
bottleneck was CPU, memory, disk I/O, or network.

**Limitations of synthetic benchmarks.** Both ``ab`` and ``h2load``
hammer a single URL repeatedly. Real users browse multiple pages, have
varied connection speeds, and experience different cache states. For
realistic load testing, consider tools like ``wrk2``, ``k6``, or
``Locust`` — but even ``ab`` is invaluable for A/B testing specific
configuration changes.


.. _See_Also_benchmarking:

See Also
~~~~~~~~

* ``ab`` documentation: https://httpd.apache.org/docs/current/programs/ab.html
* ``h2load`` documentation: https://nghttp2.org/documentation/h2load-howto.html
* :ref:`Recipe_tuning-event-mpm`


.. _Recipe_keepalive-tuning:

.. index:: KeepAlive
.. index:: MaxKeepAliveRequests
.. index:: KeepAliveTimeout
.. index:: persistent connections
.. index:: HTTP/1.1; KeepAlive

Tuning KeepAlive settings
-------------------------


.. _Problem_keepalive-tuning:

Problem
~~~~~~~

You want to configure KeepAlive for the best balance between connection
reuse and resource consumption.


.. _Solution_keepalive-tuning:

Solution
~~~~~~~~

Enable KeepAlive with a moderate timeout and a high request limit:

.. code-block:: apache

   KeepAlive On
   MaxKeepAliveRequests 100
   KeepAliveTimeout 5


.. _Discussion_keepalive-tuning:

Discussion
~~~~~~~~~~

HTTP KeepAlive allows multiple requests to travel over a single TCP
connection, eliminating the overhead of connection establishment
(TCP three-way handshake plus TLS negotiation for HTTPS). On a typical
web page that loads 30–50 sub-resources, KeepAlive can cut page load
time by 30% or more.

``KeepAlive On`` enables persistent connections. This is the default
in httpd, and you should leave it on. There is almost no scenario where
disabling KeepAlive improves performance in 2026.

``MaxKeepAliveRequests`` limits how many requests a client can send over
a single connection. The default of 100 is sensible. Setting it to 0
(unlimited) is fine for most sites. Setting it too low forces clients to
open new connections unnecessarily.

``KeepAliveTimeout`` is where the real tuning happens. This directive
controls how many seconds httpd waits for the next request on an idle
KeepAlive connection before closing it. The default is 5 seconds, and
for most sites this is the right value.

Setting it too high (say, 30 or 60 seconds) means idle connections
linger, holding resources. With the Prefork or Worker MPM, this is
catastrophic — each idle connection burns a process or thread. With the
Event MPM, the impact is much less severe because idle KeepAlive
connections are handled asynchronously by the listener thread. However,
even with Event, each idle connection consumes a file descriptor and
a small amount of memory.

Setting it too low (say, 1 second) defeats the purpose of KeepAlive
entirely — by the time the browser parses the HTML and starts requesting
sub-resources, the connection is already gone.

**The Event MPM changes the calculus.** Before the Event MPM, the
standard advice was to set ``KeepAliveTimeout`` as low as 2 seconds,
because each idle connection blocked a worker. With Event, you can
safely set it to 5–10 seconds without significant resource impact. The
listener thread can hold thousands of idle connections with minimal
overhead.

**HTTP/2 makes this mostly irrelevant.** HTTP/2 multiplexes all
requests over a single connection by design — there is no concept of
"KeepAlive" because the connection is inherently persistent. If most
of your traffic is HTTP/2, the KeepAlive settings affect only the
dwindling HTTP/1.1 clients.


.. _See_Also_keepalive-tuning:

See Also
~~~~~~~~

* https://httpd.apache.org/docs/current/mod/core.html#keepalive
* https://httpd.apache.org/docs/current/mod/core.html#keepalivetimeout
* :ref:`Recipe_enabling-http2`


.. _Recipe_avoiding-dns:

.. index:: DNS lookups
.. index:: HostnameLookups
.. index:: performance; DNS
.. index:: logresolve

Avoiding DNS lookups
--------------------


.. _Problem_avoiding-dns:

Problem
~~~~~~~

You want to eliminate DNS lookups in the request path, as they
introduce unpredictable latency.


.. _Solution_avoiding-dns:

Solution
~~~~~~~~

Ensure ``HostnameLookups`` is disabled, and use IP addresses rather
than hostnames in access control directives:

.. code-block:: apache

   # This is the default — make sure it stays this way
   HostnameLookups Off

   # Use IP addresses for access control
   <Directory "/var/www/admin">
       Require ip 10.0.0.0/8
       Require ip 192.168.1.0/24
   </Directory>


.. _Discussion_avoiding-dns:

Discussion
~~~~~~~~~~

A DNS lookup can take anywhere from 1 millisecond to 60 seconds,
depending on resolver availability, network conditions, and whether the
query requires iterating through the DNS hierarchy. During a lookup,
the thread handling that request is blocked and cannot serve anyone else.

There are two situations where httpd performs DNS lookups:

1. **HostnameLookups On** — httpd resolves every client's IP address to
a hostname and logs the hostname instead of the IP. This is a
per-request DNS hit and is devastating to performance at scale. Leave
it off. If you need hostnames in logs for analysis, run
``logresolve`` (ships with httpd) on the log files after the fact,
or let your log analysis tool handle resolution.

2. **Hostname-based access control** — when you use ``Require host
example.com`` instead of ``Require ip``, httpd must do a reverse DNS
lookup on the client IP, then a forward lookup on the resulting
hostname to verify it matches. That's *two* DNS queries per request.
Always use IP-based access control (``Require ip``) unless you have
a compelling reason not to.

.. code-block:: bash

   # Resolve hostnames in log files after the fact
   logresolve < /var/log/httpd/access_log > /tmp/resolved_log


.. _See_Also_avoiding-dns:

See Also
~~~~~~~~

* https://httpd.apache.org/docs/current/mod/core.html#hostnamelookups
* https://httpd.apache.org/docs/current/programs/logresolve.html
* https://httpd.apache.org/docs/current/dns-caveats.html


.. _Recipe_htaccess-performance:

.. index:: .htaccess
.. index:: AllowOverride
.. index:: performance; .htaccess

Performance impact of .htaccess files
-------------------------------------


.. _Problem_htaccess-performance:

Problem
~~~~~~~

You want to understand and mitigate the performance cost of
:file:`.htaccess` files.


.. _Solution_htaccess-performance:

Solution
~~~~~~~~

Disable :file:`.htaccess` lookups entirely wherever possible:

.. code-block:: apache

   <Directory "/">
       AllowOverride None
   </Directory>

Move any necessary directives from :file:`.htaccess` into the main
server configuration or a ``<Directory>`` block:

.. code-block:: apache

   # Instead of a .htaccess file in /var/www/html/images/
   <Directory "/var/www/html/images">
       ExpiresActive On
       ExpiresDefault "access plus 1 year"
   </Directory>


.. _Discussion_htaccess-performance:

Discussion
~~~~~~~~~~

When ``AllowOverride`` is set to anything other than ``None`` for a
directory tree, httpd must check for :file:`.htaccess` files on *every
single request*. And it doesn't just check the target directory — it
checks every component of the path from the document root down.

For a request to :file:`/var/www/html/blog/2026/05/post.html`, httpd
opens and reads (or attempts to open):

- :file:`/var/www/html/.htaccess`
- :file:`/var/www/html/blog/.htaccess`
- :file:`/var/www/html/blog/2026/.htaccess`
- :file:`/var/www/html/blog/2026/05/.htaccess`

That's four filesystem ``stat()`` and potentially four ``open()`` calls
*per request*, regardless of whether the files exist. On a busy server
handling thousands of requests per second, this adds up.

The cost is not just the system calls. When httpd finds a
:file:`.htaccess` file, it must parse it, merge the directives with the
existing configuration, and potentially re-run the directory walk. This
parsing happens on every request — there is no caching of
:file:`.htaccess` contents between requests.

**When .htaccess is unavoidable.** If you're running a shared hosting
environment where users cannot modify the main httpd configuration,
:file:`.htaccess` is the only option. In that case, set ``AllowOverride``
as restrictively as possible — for example, ``AllowOverride FileInfo``
rather than ``AllowOverride All`` — to limit the directives that can
appear in :file:`.htaccess` and reduce parsing overhead.

**If you control the server, don't use .htaccess.** Every directive that
works in :file:`.htaccess` also works in a ``<Directory>`` block in the
main configuration (with a few obscure exceptions). The main
configuration is parsed once at startup and cached in memory.
:file:`.htaccess` is parsed on every request. There is no performance
reason to prefer :file:`.htaccess` over main configuration.


.. _See_Also_htaccess-performance:

See Also
~~~~~~~~

* https://httpd.apache.org/docs/current/howto/htaccess.html
* https://httpd.apache.org/docs/current/mod/core.html#allowoverride


.. _Recipe_enabling-http2:

.. index:: HTTP/2
.. index:: mod_http2
.. index:: h2
.. index:: h2c
.. index:: ALPN
.. index:: Protocols directive
.. index:: multiplexing
.. index:: header compression

Enabling HTTP/2
---------------


.. _Problem_enabling-http2:

Problem
~~~~~~~

You want to enable HTTP/2 on your server to take advantage of
multiplexed streams, header compression, and improved connection
efficiency.


.. _Solution_enabling-http2:

Solution
~~~~~~~~

Load :module:`mod_http2` and add the ``h2`` protocol to your HTTPS
virtual hosts:

.. code-block:: apache

   LoadModule http2_module modules/mod_http2.so

   <VirtualHost *:443>
       ServerName www.example.com
       Protocols h2 http/1.1

       SSLEngine on
       SSLCertificateFile    /etc/tls/certs/example.com.crt
       SSLCertificateKeyFile /etc/tls/private/example.com.key
   </VirtualHost>

To enable cleartext HTTP/2 (``h2c``) on port 80 — useful for
testing and internal services, though browsers won't use it:

.. code-block:: apache

   <VirtualHost *:80>
       ServerName www.example.com
       Protocols h2c http/1.1
   </VirtualHost>

Or enable both globally:

.. code-block:: apache

   Protocols h2 h2c http/1.1


.. _Discussion_enabling-http2:

Discussion
~~~~~~~~~~

HTTP/2 (RFC 9113, previously RFC 7540) fundamentally changes how data
moves between client and server. While HTTP semantics remain the same —
methods, headers, bodies, status codes — the wire format is completely
different:

- **Multiplexing**: multiple requests and responses share a single TCP
  connection simultaneously, eliminating HTTP/1.1's head-of-line
  blocking.
- **Header compression** (HPACK): repeated headers are compressed and
  deduplicated, reducing overhead on chatty pages with many
  sub-resources.
- **Stream prioritization**: clients can signal which resources they
  need most urgently.
- **Server push** (deprecated in most browsers as of 2023, but still
  supported by httpd).

**TLS is required in practice.** The spec allows cleartext HTTP/2
(``h2c``), but every major browser requires TLS. You need a TLS library
that supports ALPN (Application-Layer Protocol Negotiation) — this is
how the client and server agree to use HTTP/2 during the TLS handshake.
OpenSSL 1.0.2+ supports ALPN. If your OpenSSL is older than that,
upgrade it before attempting HTTP/2.

**Protocol order matters.** The ``Protocols`` directive lists protocols
in server preference order. Place ``h2`` before ``http/1.1``:

.. code-block:: apache

   Protocols h2 http/1.1

If you reverse the order, HTTP/1.1 will be preferred and most clients
will never use HTTP/2. You can override this with
``ProtocolsHonorOrder Off`` to let the client's preference win, but
there's rarely a reason to do so.

**MPM requirements.** HTTP/2 works on all MPMs, but the Prefork MPM
limits HTTP/2 to one stream per connection — completely negating the
multiplexing benefit. Use the Event MPM for production HTTP/2
deployments. This is one more reason to migrate from ``mod_php`` to
PHP-FPM: it frees you from Prefork.

**Cipher suite requirements.** Browsers enforce a cipher blocklist for
HTTP/2. If your ``SSLCipherSuite`` includes deprecated ciphers (like
those using CBC mode with TLS 1.2), browsers will silently fall back to
HTTP/1.1 without any error message. Use a modern cipher configuration:

.. code-block:: apache

   SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
   SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
   SSLHonorCipherOrder on

**Verifying HTTP/2 is active:**

.. code-block:: bash

   # Check with curl
   curl -vso /dev/null --http2 https://www.example.com/ 2>&1 | grep ALPN

   # Expected output:
   # * ALPN: server accepted h2

   # Check with nghttp
   nghttp -nv https://www.example.com/

In Firefox, open Developer Tools → Network, right-click the column
headers, enable "Protocol", and look for "h2". In Chrome, navigate to
``chrome://net-internals/#http2`` to see active sessions.

**Performance impact.** The benefits of HTTP/2 are most pronounced for
pages with many sub-resources loaded over high-latency connections.
A page that loads 50 CSS, JavaScript, and image files benefits
enormously from multiplexing. A single-resource API endpoint sees
less benefit, though header compression still helps.

**H2 push is deprecated in browsers.** While httpd still supports
``H2PushResource`` and ``Link: rel=preload`` headers for server push,
Chrome removed push support in version 106 (2022) and other browsers
have followed. The ``103 Early Hints`` mechanism is the modern
replacement for preloading sub-resources. Don't invest time in push
configuration for browser-facing traffic.


.. _See_Also_enabling-http2:

See Also
~~~~~~~~

* https://httpd.apache.org/docs/current/howto/http2.html
* https://httpd.apache.org/docs/current/mod/mod_http2.html
* :ref:`Recipe_choosing-mpm`


.. _Recipe_compression:

.. index:: compression
.. index:: mod_deflate
.. index:: mod_brotli
.. index:: gzip
.. index:: Brotli
.. index:: Accept-Encoding
.. index:: Content-Encoding
.. index:: BREACH attack

Compression with mod_deflate and mod_brotli
-------------------------------------------


.. _Problem_compression:

Problem
~~~~~~~

You want to compress responses to reduce bandwidth usage and improve
page load times, using the best available algorithm for each client.


.. _Solution_compression:

Solution
~~~~~~~~

Load both :module:`mod_brotli` and :module:`mod_deflate`. Brotli will
be used when the client supports it (95%+ of modern browsers); deflate
(gzip) serves as the fallback:

.. code-block:: apache

   LoadModule brotli_module  modules/mod_brotli.so
   LoadModule deflate_module modules/mod_deflate.so

   # Brotli compression (preferred — better ratios)
   AddOutputFilterByType BROTLI_COMPRESS text/html text/plain text/xml
   AddOutputFilterByType BROTLI_COMPRESS text/css text/javascript
   AddOutputFilterByType BROTLI_COMPRESS application/javascript
   AddOutputFilterByType BROTLI_COMPRESS application/json application/xml
   AddOutputFilterByType BROTLI_COMPRESS application/xhtml+xml
   AddOutputFilterByType BROTLI_COMPRESS image/svg+xml
   AddOutputFilterByType BROTLI_COMPRESS application/rss+xml
   AddOutputFilterByType BROTLI_COMPRESS application/atom+xml

   # Gzip/deflate fallback for older clients
   AddOutputFilterByType DEFLATE text/html text/plain text/xml
   AddOutputFilterByType DEFLATE text/css text/javascript
   AddOutputFilterByType DEFLATE application/javascript
   AddOutputFilterByType DEFLATE application/json application/xml
   AddOutputFilterByType DEFLATE application/xhtml+xml
   AddOutputFilterByType DEFLATE image/svg+xml

   # Set Brotli quality (0–11, default 5)
   BrotliCompressionQuality 5

   # Set deflate compression level (1–9, default 6)
   DeflateCompressionLevel 6

   # Don't compress already-compressed content
   SetEnvIfNoCase Request_URI "\.(?:gif|jpe?g|png|webp|avif)$" no-brotli no-gzip
   SetEnvIfNoCase Request_URI "\.(?:zip|gz|bz2|xz|7z)$" no-brotli no-gzip
   SetEnvIfNoCase Request_URI "\.(?:woff2?|ttf|otf|eot)$" no-brotli no-gzip
   SetEnvIfNoCase Request_URI "\.(?:mp[34]|avi|mov|webm|ogg)$" no-brotli no-gzip


.. _Discussion_compression:

Discussion
~~~~~~~~~~

Compression reduces the size of text-based responses by 60–90%,
making it one of the highest-impact performance optimizations you can
apply. A 100 KB JavaScript file compresses to 15–25 KB with gzip, or
12–20 KB with Brotli. On mobile networks with limited bandwidth, this
translates directly to faster page loads.

**Brotli vs. deflate.** Brotli (``Content-Encoding: br``) was designed
by Google specifically for web content. It incorporates a built-in
dictionary of common HTML, CSS, and JavaScript patterns, giving it a
15–25% compression advantage over gzip on typical web content. All
modern browsers have supported Brotli since 2016–2017. The only clients
that don't support it are legacy bots, ancient browsers, and some
command-line tools (though ``curl`` supports Brotli since version 7.57).

:version:`2.4.26` — :module:`mod_brotli` was introduced in httpd 2.4.26.

**How httpd selects the algorithm.** When both modules are loaded, httpd
examines the client's ``Accept-Encoding`` header. If it includes ``br``,
Brotli is used. If it includes only ``gzip`` or ``deflate``, the deflate
filter handles compression. The ``Vary: Accept-Encoding`` header is
added automatically so that caches store separate copies.

**Compression quality levels.** Higher quality means better compression
ratio but more CPU time. For dynamic content compressed on every
request, moderate levels are appropriate:

- Brotli quality 4–6 (default 5): good balance of ratio and speed
- Brotli quality 11: maximum compression, 10× slower — use only for
  pre-compressed static files
- Deflate level 6 (default): good balance
- Deflate level 9: diminishing returns, noticeably more CPU

**Don't compress binary content.** Images (JPEG, PNG, WebP, AVIF),
videos, audio files, and compressed archives are already compressed.
Running them through another compression pass wastes CPU for zero (or
even negative) size reduction. The ``AddOutputFilterByType`` approach
limits compression to specific MIME types, which is the safest method.

**Pre-compression for static assets.** For large static files that
don't change frequently, you can compress them ahead of time at maximum
quality and serve the pre-compressed versions:

.. code-block:: bash

   # Pre-compress with maximum Brotli quality
   brotli -q 11 -o style.css.br style.css
   gzip -9 -k style.css

Then use :module:`mod_rewrite` or :module:`mod_negotiation` to serve
the pre-compressed variants. This gives you the best compression ratios
without spending CPU on every request.

**The BREACH attack.** Compressing responses that contain both
user-controlled input and secret tokens (like CSRF tokens) over TLS can
leak secret data through response size variation. This is the BREACH
attack. Mitigations include:

- Randomizing token placement in the HTML
- Separating secrets from user-reflected content
- Disabling compression for pages that combine secrets and user input

For most static asset compression, BREACH is not a concern — it only
applies to dynamic pages that reflect user input alongside secrets.


.. _See_Also_compression:

See Also
~~~~~~~~

* https://httpd.apache.org/docs/current/mod/mod_brotli.html
* https://httpd.apache.org/docs/current/mod/mod_deflate.html
* https://www.brotli.org/
* :ref:`Recipe_disk-caching`


.. _Recipe_disk-caching:

.. index:: caching
.. index:: mod_cache
.. index:: mod_cache_disk
.. index:: CacheEnable
.. index:: CacheRoot
.. index:: CacheDirLevels
.. index:: CacheDirLength
.. index:: CacheQuickHandler
.. index:: CacheLock
.. index:: htcacheclean

Setting up HTTP content caching (mod_cache)
-------------------------------------------


.. _Problem_disk-caching:

Problem
~~~~~~~

You want to cache frequently requested content on disk to reduce
origin server load and speed up response times for repeat requests.


.. _Solution_disk-caching:

Solution
~~~~~~~~

Enable :module:`mod_cache` with the :module:`mod_cache_disk` storage
backend:

.. code-block:: apache

   LoadModule cache_module      modules/mod_cache.so
   LoadModule cache_disk_module modules/mod_cache_disk.so

   # Set the disk cache root
   CacheRoot "/var/cache/httpd/mod_cache_disk"

   # Enable caching for the entire site
   CacheEnable disk "/"

   # Directory structure (2 levels, 1 character per level)
   CacheDirLevels 2
   CacheDirLength 1

   # Default expiry for content without explicit cache headers
   CacheDefaultExpire 3600

   # Maximum cache lifetime (1 week)
   CacheMaxExpire 604800

   # Prevent thundering herd on popular expired entries
   CacheLock on
   CacheLockPath "/tmp/mod_cache-lock"
   CacheLockMaxAge 5

   # Exclude paths that should never be cached
   CacheDisable "/admin"
   CacheDisable "/api"

Run ``htcacheclean`` as a daemon to keep the cache directory from
growing without bound:

.. code-block:: bash

   htcacheclean -d30 -p/var/cache/httpd/mod_cache_disk -l500M -n

Create a systemd service for ``htcacheclean`` so it starts at boot:

.. code-block:: bash

   cat > /etc/systemd/system/htcacheclean.service << 'EOF'
   [Unit]
   Description=Apache httpd cache cleaner
   After=httpd.service

   [Service]
   Type=forking
   ExecStart=/usr/bin/htcacheclean -d30 -p/var/cache/httpd/mod_cache_disk -l500M -n
   ExecStop=/bin/kill -TERM $MAINPID

   [Install]
   WantedBy=multi-user.target
   EOF

   systemctl enable --now htcacheclean


.. _Discussion_disk-caching:

Discussion
~~~~~~~~~~

:module:`mod_cache` implements an RFC 7234-compliant HTTP cache. It
understands ``Cache-Control``, ``Expires``, conditional requests
(``If-Modified-Since``, ``If-None-Match``), and content negotiation via
``Vary``. When a cached response is still fresh, it's served directly
without invoking any content handler — no CGI execution, no proxy
request, no database query.

**How it works.** :module:`mod_cache` is the brains — it makes caching
decisions based on HTTP headers. :module:`mod_cache_disk` is the storage
backend — it manages the on-disk file structure. The cached response
includes both headers and body, stored in a directory hierarchy derived
from an MD5 hash of the URL.

**CacheDirLevels and CacheDirLength** control the directory tree
structure. With ``CacheDirLevels 2`` and ``CacheDirLength 1``, a URL
whose hash starts with "aB" gets stored under
:file:`/var/cache/httpd/mod_cache_disk/a/B/`. This prevents any single
directory from accumulating too many files, which would slow filesystem
operations. The product of levels × length must not exceed 20. For most
sites, 2 levels of length 1 works well.

**The quick handler.** By default, ``CacheQuickHandler on`` means the
cache runs very early in request processing — before authentication,
authorization, and output filters. This gives maximum performance but
means cached content bypasses access control. If you cache
authenticated content, unauthenticated users will receive it.

For sites with mixed public and authenticated content:

.. code-block:: apache

   CacheQuickHandler off

This lets authentication run before the cache check. The performance
cost is modest — the cache still prevents origin requests.

**CacheLock and the thundering herd.** When a popular cached resource
expires, hundreds of simultaneous requests may hit the origin at once.
``CacheLock on`` serializes cache refreshes — only the first request
goes to the origin, while subsequent requests receive the stale content
until the refresh completes. This is essential for high-traffic sites
with backend services that can't absorb sudden load spikes.

**mod_cache_disk vs. mod_cache_socache.** The alternative storage
backend :module:`mod_cache_socache` stores cached content in shared
memory (via :module:`mod_socache_shmcb` or similar). It's faster for
very small, frequently accessed objects (think: API responses under
1 KB), but it's limited by available shared memory and isn't suitable
for large objects. For general-purpose content caching,
:module:`mod_cache_disk` is the right choice.

**Common troubleshooting: empty cache directory.** If your cache stays
empty, check:

1. The ``CacheRoot`` directory exists and is writable by the httpd user.
2. The origin response includes ``Expires`` or ``Cache-Control: max-age``
headers (or you've set ``CacheDefaultExpire``).
3. The response does not include ``Cache-Control: no-store`` or
``Cache-Control: private``.

Verify with ``curl -I`` that the origin content is cacheable.


.. _See_Also_disk-caching:

See Also
~~~~~~~~

* https://httpd.apache.org/docs/current/mod/mod_cache.html
* https://httpd.apache.org/docs/current/mod/mod_cache_disk.html
* https://httpd.apache.org/docs/current/caching.html
* https://httpd.apache.org/docs/current/programs/htcacheclean.html
* :ref:`Recipe_browser-caching-expires`
* :ref:`Recipe_troubleshooting-cache`


.. _Recipe_browser-caching-expires:

.. index:: mod_expires
.. index:: ExpiresActive
.. index:: ExpiresByType
.. index:: ExpiresDefault
.. index:: Cache-Control header
.. index:: browser caching
.. index:: immutable

Controlling browser caching with mod_expires
--------------------------------------------


.. _Problem_browser-caching-expires:

Problem
~~~~~~~

You want to instruct browsers and CDNs to cache your static assets for
appropriate durations, reducing redundant requests to your server.


.. _Solution_browser-caching-expires:

Solution
~~~~~~~~

Enable :module:`mod_expires` and set expiration policies by content
type:

.. code-block:: apache

   LoadModule expires_module modules/mod_expires.so

   ExpiresActive On

   # Default: 1 hour from access time
   ExpiresDefault "access plus 1 hour"

   # HTML: short lifetime (changes frequently)
   ExpiresByType text/html "access plus 10 minutes"

   # CSS and JavaScript: 1 year (use cache-busting filenames)
   ExpiresByType text/css "access plus 1 year"
   ExpiresByType application/javascript "access plus 1 year"

   # Images: 1 year
   ExpiresByType image/jpeg "access plus 1 year"
   ExpiresByType image/png "access plus 1 year"
   ExpiresByType image/gif "access plus 1 year"
   ExpiresByType image/webp "access plus 1 year"
   ExpiresByType image/avif "access plus 1 year"
   ExpiresByType image/svg+xml "access plus 1 year"

   # Fonts: 1 year
   ExpiresByType font/woff2 "access plus 1 year"
   ExpiresByType font/woff "access plus 1 year"
   ExpiresByType application/font-woff2 "access plus 1 year"

   # Favicon
   ExpiresByType image/x-icon "access plus 1 year"

For assets with cache-busting filenames, add ``immutable`` via
:module:`mod_headers`:

.. code-block:: apache

   <FilesMatch "\.[a-f0-9]{8,}\.(css|js|png|jpg|svg|woff2)$">
       Header set Cache-Control "public, immutable"
   </FilesMatch>


.. _Discussion_browser-caching-expires:

Discussion
~~~~~~~~~~

Without explicit caching headers, browsers use heuristics to decide how
long to cache a resource. These heuristics vary between browsers and
are often wrong — sometimes too aggressive, sometimes too conservative.
:module:`mod_expires` eliminates the guesswork by setting explicit
``Expires`` and ``Cache-Control: max-age`` headers on every response.

**What mod_expires sets.** For each matched response, the module adds
two headers:

- ``Expires: Thu, 15 May 2027 12:00:00 GMT`` — an absolute timestamp
- ``Cache-Control: max-age=31536000`` — a relative duration in seconds

Modern browsers prefer ``max-age`` but :module:`mod_expires` sets both
for compatibility with legacy HTTP/1.0 caches.

**Access vs. modification base time.** You can calculate expiry from
either ``access`` (when the client made the request) or
``modification`` (the file's last-modified time on disk):

.. code-block:: apache

   ExpiresByType text/html "modification plus 1 hour"

In practice, ``access`` is almost always what you want. The
``modification`` mode has edge cases with dynamic content (which has no
meaningful modification time) and doesn't work well with proxy caches.

**The cache-busting strategy.** The gold standard for static assets is:

1. Set long cache lifetimes (one year) for CSS, JavaScript, images, and
fonts.
2. Include a content hash or version number in the filename:
   :file:`style.a3f2b1c4.css`, :file:`app.v2.1.0.js`.
3. When the content changes, the filename changes, so browsers fetch
the new version immediately.
4. Set HTML documents to short lifetimes (minutes) because they contain
the references to versioned assets.

This gives returning visitors instant cache hits while ensuring they
always get updated content when you deploy changes.

**The ``immutable`` hint.** When a browser has a cached resource that
hasn't expired, it may still send a conditional request to revalidate
it when the user navigates (as opposed to hitting the back button). The
``immutable`` ``Cache-Control`` directive tells the browser to skip
revalidation entirely — the resource will never change at this URL. Use
it only with cache-busted filenames.

**Interaction with other modules.** If a CGI script, application
framework, or :module:`mod_headers` already sets ``Cache-Control`` on a
response, :module:`mod_expires` will not override it. This means your
application's ``Cache-Control: no-store`` on API responses is respected
automatically.


.. _See_Also_browser-caching-expires:

See Also
~~~~~~~~

* https://httpd.apache.org/docs/current/mod/mod_expires.html
* https://httpd.apache.org/docs/current/mod/mod_headers.html
* RFC 9111 (HTTP Caching): https://www.rfc-editor.org/rfc/rfc9111
* https://web.dev/articles/http-cache


.. _Recipe_file-cache:

.. index:: mod_file_cache
.. index:: MMapFile
.. index:: CacheFile
.. index:: memory-mapped files
.. index:: static content

Caching with mod_file_cache
---------------------------


.. _Problem_file-cache:

Problem
~~~~~~~

You have a small set of static files that are read extremely frequently
and never change between server restarts. You want to eliminate all
filesystem overhead when serving them.


.. _Solution_file-cache:

Solution
~~~~~~~~

Use :module:`mod_file_cache` to pre-load files into memory at server
startup:

.. code-block:: apache

   LoadModule file_cache_module modules/mod_file_cache.so

   # Memory-map files (fastest — file contents are in RAM)
   MMapFile /var/www/html/index.html
   MMapFile /var/www/html/style.css
   MMapFile /var/www/html/logo.png

Or use ``CacheFile`` to keep the file descriptor open (less memory
usage, still avoids open/close overhead):

.. code-block:: apache

   CacheFile /var/www/html/index.html
   CacheFile /var/www/html/style.css


.. _Discussion_file-cache:

Discussion
~~~~~~~~~~

:module:`mod_file_cache` provides two mechanisms:

``MMapFile`` memory-maps the file at server startup. The file contents
are loaded into the server's address space and served directly from
RAM on every request, with zero filesystem I/O. This is extremely fast
but comes with constraints:

- The file must not change while httpd is running. Changes on disk
  won't be reflected until httpd is restarted.
- Memory usage increases by the size of each mapped file.
- On 32-bit systems (rare in 2026), you're limited by address space.

``CacheFile`` opens the file descriptor at startup and keeps it open.
This avoids the overhead of opening and closing the file on each
request, but the kernel still reads the file contents from disk (or
its own page cache). It uses less memory than ``MMapFile`` but provides
less benefit.

**When to use mod_file_cache.** Honestly? Almost never in 2026. Modern
Linux kernels are excellent at page caching — files that are read
frequently will be in the kernel's page cache anyway. The benefit of
:module:`mod_file_cache` over the kernel's own caching is marginal on
modern hardware. It's most useful in very specific scenarios:

- Embedded systems with limited I/O bandwidth
- Files that must be served with absolute minimum latency (sub-millisecond SLA)
- Systems where the kernel's page cache is under pressure from other
  workloads

For the vast majority of servers, properly configured
:module:`mod_cache_disk` and :module:`mod_expires` will give you more
benefit with far less operational complexity.

**The operational headache.** Every time you update a cached file, you
must restart (not reload) httpd. A graceful restart will re-map the
files, but a configuration reload with ``apachectl graceful`` will not
re-read the file contents from disk. This makes :module:`mod_file_cache`
a poor fit for files that change with any regularity.


.. _See_Also_file-cache:

See Also
~~~~~~~~

* https://httpd.apache.org/docs/current/mod/mod_file_cache.html
* :ref:`Recipe_disk-caching`
* :ref:`Recipe_browser-caching-expires`


.. _Recipe_ratelimit:

.. index:: mod_ratelimit
.. index:: rate limiting
.. index:: bandwidth throttling
.. index:: RATE_LIMIT filter
.. index:: rate-limit environment variable
.. index:: rate-initial-burst

Rate limiting with mod_ratelimit
--------------------------------


.. _Problem_ratelimit:

Problem
~~~~~~~

You want to throttle the bandwidth for certain parts of your site —
for example, a downloads directory that is consuming excessive
bandwidth and impacting performance for other content.


.. _Solution_ratelimit:

Solution
~~~~~~~~

Apply the ``RATE_LIMIT`` output filter to the target location and set
the rate via environment variable:

.. code-block:: apache

   LoadModule ratelimit_module modules/mod_ratelimit.so

   <Location "/downloads">
       SetOutputFilter RATE_LIMIT
       SetEnv rate-limit 400
       SetEnv rate-initial-burst 512
   </Location>


.. _Discussion_ratelimit:

Discussion
~~~~~~~~~~

:module:`mod_ratelimit` provides a bandwidth throttle that limits the
speed at which response data is sent to the client. The ``rate-limit``
environment variable specifies the maximum transfer rate in KiB/s
(kilobytes per second). In the example above, downloads are limited to
400 KiB/s (approximately 3.2 Mbit/s) after an initial burst of 512 KB
at full speed.

:version:`2.4.48` — The ``rate-initial-burst`` feature was added in
httpd 2.4.48.

The initial burst allows the first chunk of data to be sent at full
speed, which helps with perceived responsiveness — the client sees data
arriving immediately, then the throttle takes effect for the remainder
of the transfer.

**Use cases:**

- Preventing large file downloads from saturating your network
  connection and starving other content
- Providing tiered download speeds (faster for authenticated users,
  throttled for anonymous)
- Protecting backend proxy connections from being overwhelmed by
  fast-reading clients

**Conditional rate limiting.** You can apply rate limiting conditionally
using :module:`mod_setenvif` or :module:`mod_rewrite`:

.. code-block:: apache

   # Rate limit only for files larger than 10 MB
   <LocationMatch "\.(?:iso|zip|tar\.gz)$">
       SetOutputFilter RATE_LIMIT
       SetEnv rate-limit 200
   </LocationMatch>

   # Different rates based on client
   SetEnvIf Remote_Addr "^10\." !rate-limit
   <Location "/downloads">
       SetOutputFilter RATE_LIMIT
       SetEnv rate-limit 500
   </Location>

In this example, internal clients (10.x.x.x) are not rate-limited, while
external clients are throttled to 500 KiB/s.

**Limitations.** :module:`mod_ratelimit` is a per-connection throttle,
not a per-user or per-IP request rate limiter. It controls *bandwidth*,
not *request frequency*. If you need to limit the number of requests per
second from a given client (to protect against abuse or DDoS), you'll
need :module:`mod_evasive` (third-party) or a reverse proxy like
``mod_proxy`` in front of a rate-limiting layer.


.. _See_Also_ratelimit:

See Also
~~~~~~~~

* https://httpd.apache.org/docs/current/mod/mod_ratelimit.html
* :ref:`Recipe_load-balancing-overview`


.. _Recipe_load-balancing-overview:

.. index:: load balancing
.. index:: mod_proxy_balancer
.. index:: scalability
.. index:: horizontal scaling

Load balancing overview
-----------------------


.. _Problem_load-balancing-overview:

Problem
~~~~~~~

Your single server can no longer handle the traffic. You need to
distribute requests across multiple backend servers.


.. _Solution_load-balancing-overview:

Solution
~~~~~~~~

Use :module:`mod_proxy_balancer` to distribute requests across a pool of
backend servers:

.. code-block:: apache

   LoadModule proxy_module          modules/mod_proxy.so
   LoadModule proxy_http_module     modules/mod_proxy_http.so
   LoadModule proxy_balancer_module modules/mod_proxy_balancer.so
   LoadModule lbmethod_byrequests_module modules/mod_lbmethod_byrequests.so
   LoadModule slotmem_shm_module    modules/mod_slotmem_shm.so

   <Proxy "balancer://webapp">
       BalancerMember "http://backend1.internal:8080"
       BalancerMember "http://backend2.internal:8080"
       BalancerMember "http://backend3.internal:8080"
       ProxySet lbmethod=byrequests
   </Proxy>

   ProxyPass        "/" "balancer://webapp/"
   ProxyPassReverse "/" "balancer://webapp/"


.. _Discussion_load-balancing-overview:

Discussion
~~~~~~~~~~

Load balancing is the natural next step when you've optimized a single
server as far as it can go and still need more capacity. httpd's built-in
:module:`mod_proxy_balancer` supports several balancing algorithms:

- ``byrequests`` — round-robin, distributes requests evenly by count
- ``bytraffic`` — distributes by byte count, balancing bandwidth
- ``bybusyness`` — sends to the least-busy backend
- ``heartbeat`` — uses heartbeat signals from backends to route traffic

For most applications, ``byrequests`` or ``bybusyness`` works well.

**Health checking.** :module:`mod_proxy_hcheck` can periodically ping
your backends and remove unhealthy ones from the pool:

.. code-block:: apache

   <Proxy "balancer://webapp">
       BalancerMember "http://backend1.internal:8080" hcmethod=TCP hcinterval=5
       BalancerMember "http://backend2.internal:8080" hcmethod=TCP hcinterval=5
   </Proxy>

**Session stickiness.** If your application requires session affinity
(requests from the same user always go to the same backend), configure a
sticky session route:

.. code-block:: apache

   Header add Set-Cookie "ROUTEID=.%{BALANCER_WORKER_ROUTE}e; path=/" env=BALANCER_ROUTE_CHANGED
   <Proxy "balancer://webapp">
       BalancerMember "http://backend1.internal:8080" route=1
       BalancerMember "http://backend2.internal:8080" route=2
       ProxySet stickysession=ROUTEID
   </Proxy>

This is a performance topic because it's the escape hatch when
vertical scaling (bigger hardware, better tuning) reaches its limits.
But load balancing is a deep topic — for full coverage including failover
strategies, connection pooling, and WebSocket proxying, see the
Proxies and Gatekeeping chapter.


.. _See_Also_load-balancing-overview:

See Also
~~~~~~~~

* :ref:`Chapter_Proxies` (full load balancing treatment)
* https://httpd.apache.org/docs/current/mod/mod_proxy_balancer.html
* https://httpd.apache.org/docs/current/mod/mod_proxy_hcheck.html


.. _Recipe_troubleshooting-cache:

.. index:: caching; troubleshooting
.. index:: X-Cache header
.. index:: CacheHeader
.. index:: CacheDetailHeader
.. index:: mod_cache; debugging
.. index:: cache-status
.. index:: htcacheclean

Troubleshooting cache behavior
------------------------------


.. _Problem_troubleshooting-cache:

Problem
~~~~~~~

Your cache is not working as expected — content that should be cached
isn't, or stale content is being served when it shouldn't be. You need
to diagnose what :module:`mod_cache` is doing.


.. _Solution_troubleshooting-cache:

Solution
~~~~~~~~

Enable diagnostic headers:

.. code-block:: apache

   CacheHeader on
   CacheDetailHeader on

Then inspect responses with ``curl``:

.. code-block:: bash

   curl -s -D- -o /dev/null https://www.example.com/page.html

Look for the ``X-Cache`` and ``X-Cache-Detail`` headers:

.. code-block:: text

   X-Cache: HIT from localhost
   X-Cache-Detail: "cache hit" from localhost

Or, if content was not served from cache:

.. code-block:: text

   X-Cache: MISS from localhost
   X-Cache-Detail: "url not cached: no expiry information" from localhost


.. _Discussion_troubleshooting-cache:

Discussion
~~~~~~~~~~

Cache troubleshooting is one of the most common questions on the httpd
users mailing list. The ``X-Cache-Detail`` header is your best friend —
it tells you *why* a caching decision was made.

**Understanding X-Cache values:**

- ``HIT`` — served from cache, response was fresh
- ``REVALIDATE`` — cached response was stale, successfully revalidated
  with origin (304 Not Modified)
- ``MISS`` — not served from cache

**Common "why isn't it caching?" causes:**

1. **No expiry information.** The origin sends neither ``Expires`` nor
``Cache-Control: max-age``. Fix by setting ``CacheDefaultExpire``:

   .. code-block:: apache

      CacheDefaultExpire 3600

2. **Cache-Control: private or no-store.** The origin explicitly
prohibits caching. Check your application's headers.

3. **Permissions.** The ``CacheRoot`` directory isn't writable by the
httpd user:

   .. code-block:: bash

      chown -R apache:apache /var/cache/httpd/mod_cache_disk
      chmod 750 /var/cache/httpd/mod_cache_disk

4. **Vary header explosion.** If responses include ``Vary:
Accept-Encoding, Cookie, User-Agent``, the cache stores a separate
entry for every combination — effectively preventing cache hits. Fix
by normalizing or removing unnecessary ``Vary`` values.

5. **Query strings.** By default, ``mod_cache`` treats URLs with
different query strings as different resources. If your application
uses query strings for tracking but serves the same content,
consider ``CacheIgnoreQueryString On`` (:version:`2.4.39`).

**Logging cache decisions.** Include the ``cache-status`` environment
variable in your access log:

.. code-block:: apache

   LogFormat "%h %l %u %t \"%r\" %>s %b \"%{cache-status}e\"" cache_log
   CustomLog "logs/cache.log" cache_log

For separate log files per cache status:

.. code-block:: apache

   CustomLog "logs/cache-hit.log" common env=cache-hit
   CustomLog "logs/cache-miss.log" common env=cache-miss

**Cache interaction with mod_deflate.** This is a subtle gotcha. With
``CacheQuickHandler on`` (the default), the cache stores and serves
responses *before* :module:`mod_deflate` runs. This means:

- Compressed responses may bypass the cache
- Cached responses may be served uncompressed

The fix is to disable the quick handler and explicitly order filters:

.. code-block:: apache

   # Cache uncompressed, compress on delivery (one cache copy, CPU per request)
   CacheQuickHandler off
   AddOutputFilterByType CACHE;DEFLATE text/html text/css application/javascript

   # Or: compress first, cache compressed (less CPU, more storage variants)
   CacheQuickHandler off
   AddOutputFilterByType DEFLATE;CACHE text/html text/css application/javascript

**htcacheclean maintenance.** Even if caching is working, an unmanaged
cache directory will grow until it fills the disk. Symptoms include
random I/O errors in the error log and degraded cache performance as
directory listing operations slow down. Always run ``htcacheclean`` as
a daemon.

Monitor cache size and hit rates over time. If your hit rate is below
50%, you may need to increase ``CacheMaxExpire`` or investigate why
your origin is sending uncacheable headers.

.. warning::

   Remove ``CacheHeader`` and ``CacheDetailHeader`` before deploying
   to production. These headers expose internal cache topology
   information to clients.


.. _See_Also_troubleshooting-cache:

See Also
~~~~~~~~

* https://httpd.apache.org/docs/current/mod/mod_cache.html#cacheheader
* https://httpd.apache.org/docs/current/mod/mod_cache.html#cachedetailheader
* https://httpd.apache.org/docs/current/caching.html
* :ref:`Recipe_disk-caching`
* :ref:`Recipe_browser-caching-expires`


Summary
-------

Performance tuning is iterative. You measure, change one thing, measure
again, and decide whether the change was worth it. There's no universal
"fast configuration" — every site has a different mix of static and
dynamic content, a different traffic pattern, and different constraints
on CPU, memory, and network.

That said, if you take away only three things from this chapter, make
them these:

1. **Use the Event MPM.** If you're still on Prefork because of
``mod_php``, switch to PHP-FPM and Event. This is the single biggest
performance improvement most servers can make.

2. **Enable compression.** Load :module:`mod_brotli` and
   :module:`mod_deflate`. This costs negligible CPU and saves enormous
   bandwidth.

3. **Set explicit cache headers.** Use :module:`mod_expires` to tell
browsers how long to cache your static assets. This eliminates
redundant requests entirely.

Everything else in this chapter — HTTP/2, server-side caching, MPM
tuning, KeepAlive — is refinement on top of these three fundamentals.


.. rubric:: Footnotes

.. [#fn-mpm-formula] The Event MPM connection formula is:
   total_connections = ThreadsPerChild × (1 + AsyncRequestWorkerFactor).
   This is a theoretical maximum; actual capacity depends on the ratio
   of active to idle connections.
