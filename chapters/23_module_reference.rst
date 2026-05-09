.. index::
   single: modules; reference catalog
   single: module reference

.. epigraph::

   "A good craftsman knows what every tool in the shop does, even the ones
   gathering dust in the back drawer."

   -- Workshop proverb

.. _Chapter_Module_Reference:

========================
Module reference
========================

Apache httpd ships with 143 modules. That's a lot of tools in the box. Some of
them you'll use every day—:module:`mod_ssl`, :module:`mod_rewrite`,
:module:`mod_proxy`—and those get full recipe treatment in their respective
chapters. Others you might never touch, but knowing they exist saves you from
reinventing wheels or installing third-party code when httpd already has what
you need.

This chapter is a reference catalog, not a recipe collection. I'm not going to
walk you through step-by-step configurations here. Instead, I'll give you a
brief description of every module that hasn't already gotten full coverage
elsewhere, organized by category. Think of it as the "what does this thing do?"
quick-reference you wish the official docs had.

For modules with deep coverage in other chapters, I've included a table that
maps each one to its primary chapter. For everything else, you get 2-5
sentences: what it does, when you'd want it, and any key directives worth
knowing about. If a module is rarely useful, I'll tell you that too. No point
pretending every module is equally important.

One note on availability: most modules ship with httpd 2.4 (the current stable
release). A few exist only in trunk (the development branch that will become
2.6). I've marked those with a version badge so you know what's available to
you today versus what's coming.

.. index::
   single: modules; covered in other chapters


Modules covered in other chapters
----------------------------------

The following modules have full recipe or section-level treatment in other
chapters. If you need to configure them, head to the referenced chapter for
detailed walkthroughs.

**Authentication and sessions** (see :ref:`Chapter_AAA`):

- :module:`core`, :module:`mod_access_compat`, :module:`mod_allowmethods`
- :module:`mod_auth_basic`, :module:`mod_auth_bearer`, :module:`mod_auth_digest`, :module:`mod_auth_form`
- :module:`mod_authn_anon`, :module:`mod_authn_core`, :module:`mod_authn_dbd`, :module:`mod_authn_dbm`, :module:`mod_authn_file`, :module:`mod_authn_socache`
- :module:`mod_authnz_fcgi`, :module:`mod_authnz_ldap`
- :module:`mod_autht_core`, :module:`mod_autht_jwt`
- :module:`mod_authz_core`, :module:`mod_authz_dbd`, :module:`mod_authz_groupfile`, :module:`mod_authz_owner`, :module:`mod_authz_user`
- :module:`mod_dbd`, :module:`mod_ldap`
- :module:`mod_session`, :module:`mod_session_cookie`, :module:`mod_session_crypto`, :module:`mod_session_dbd`
- :module:`mod_socache_shmcb`

**Installation and MPMs** (see :ref:`Chapter_Installation`):

- :module:`event`, :module:`prefork`, :module:`worker`, :module:`mod_systemd`

**Logging** (see :ref:`Chapter_Logging`):

- :module:`mod_log_config`, :module:`mod_logio`, :module:`mod_remoteip`, :module:`mod_dumpio`

**URL mapping** (see :ref:`Chapter_URL_Mapping`):

- :module:`mod_speling`

**mod_rewrite** (see :ref:`Chapter_mod_rewrite`):

- :module:`mod_rewrite`

**Security** (see :ref:`Chapter_Security`):

- :module:`core` (also here), :module:`mod_reqtimeout`

**SSL/TLS** (see :ref:`Chapter_SSL_and_TLS`):

- :module:`mod_ssl`, :module:`mod_http2`, :module:`mod_md`

**Dynamic content** (see :ref:`Chapter_Dynamic_content`):

- :module:`mod_cgi`, :module:`mod_cgid`, :module:`mod_env`, :module:`mod_setenvif`

**Proxies and load balancing** (see :ref:`Chapter_Proxies`):

- :module:`mod_proxy`, :module:`mod_proxy_http`, :module:`mod_proxy_ftp`, :module:`mod_proxy_wstunnel`
- :module:`mod_proxy_ajp`, :module:`mod_proxy_balancer`, :module:`mod_proxy_fcgi`, :module:`mod_proxy_hcheck`, :module:`mod_proxy_http2`

**Performance** (see :ref:`Chapter_Performance_and_testing`):

- :module:`mod_cache`, :module:`mod_cache_disk`, :module:`mod_expires`, :module:`mod_file_cache`
- :module:`mod_brotli`, :module:`mod_ratelimit`, :module:`mod_dialup`

**Directory listings** (see :ref:`Chapter_Directory_listing`):

- :module:`mod_autoindex`

**Filters and handlers** (see :ref:`Chapter_Filters_And_Handlers`):

- :module:`mod_filter`, :module:`mod_mime`, :module:`mod_negotiation`, :module:`mod_reflector`
- :module:`mod_deflate`, :module:`mod_ext_filter`, :module:`mod_sed`, :module:`mod_substitute`
- :module:`mod_asis`, :module:`mod_data`, :module:`mod_imagemap`

**Virtual hosts** (see :ref:`Chapter_Virtual_hosts`):

- :module:`mod_vhost_alias`

**Programmable configuration** (see :ref:`Chapter_per_request`):

- :module:`mod_macro`, :module:`mod_version`

**mod_info and mod_status** (see :ref:`Chapter_info_and_status`):

- :module:`mod_info`, :module:`mod_status`


.. index::
   single: modules; content handling
   single: mod_alias
   single: mod_dir
   single: mod_actions
   single: mod_include
   single: mod_mime_magic
   single: mod_cern_meta

Content handling
-----------------

Modules that control how httpd finds, identifies, and serves content.

.. _Module_ref_mod_alias:

:module:`mod_alias`
~~~~~~~~~~~~~~~~~~~~

.. index:: mod_alias

Maps URL paths to filesystem locations and handles simple redirects. The
``Alias`` directive maps a URL prefix to a directory, and ``Redirect`` sends
clients elsewhere. You'll use this constantly—it's one of the first modules
most people encounter. The key directives are ``Alias``, ``AliasMatch``,
``Redirect``, ``RedirectMatch``, and ``ScriptAlias``. For anything more complex
than prefix-based mapping, you'll want :module:`mod_rewrite` instead.

See :ref:`Chapter_URL_Mapping` for detailed usage patterns.

.. _Module_ref_mod_dir:

:module:`mod_dir`
~~~~~~~~~~~~~~~~~~

.. index:: mod_dir

Handles two things: appending trailing slashes to directory URLs (so
``/images`` becomes ``/images/``) and choosing which file to serve as the
directory index. The ``DirectoryIndex`` directive lets you specify index file
names (``index.html``, ``index.php``, etc.) in priority order. The
``FallbackResource`` directive—added in 2.4—is particularly useful for
front-controller frameworks that want every request funneled through a single
script.

See :ref:`Chapter_URL_Mapping` and :ref:`Chapter_Directory_listing` for
recipes.

.. _Module_ref_mod_actions:

:module:`mod_actions`
~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_actions

Lets you invoke a CGI script based on either the MIME type of the requested
resource or the HTTP method used. The ``Action`` directive associates a media
type with a handler script, and ``Script`` maps HTTP methods (GET, POST, etc.)
to scripts. This was more useful in the early CGI era. Today, most people
accomplish the same thing with :module:`mod_proxy_fcgi` or application
frameworks. Still handy if you need to run a preprocessing script whenever a
particular content type is requested.

.. _Module_ref_mod_include:

:module:`mod_include`
~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_include

Server Side Includes (SSI)—the original server-side templating system. Parses
HTML files for special directives like ``<!--#include virtual="/header.html"
-->`` and ``<!--#echo var="DATE_LOCAL" -->``. SSI was how people built dynamic
pages before PHP existed. It's still useful for simple composition tasks: shared
headers, footers, conditional content based on environment variables. Enable it
with ``Options +Includes`` and make sure your files are identified (typically
via ``AddOutputFilter INCLUDES .shtml``).

See :ref:`Chapter_Dynamic_content` for context on SSI versus modern
alternatives.

.. _Module_ref_mod_mime_magic:

:module:`mod_mime_magic`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_mime_magic

Determines a file's MIME type by examining its contents (magic bytes) rather
than relying on the file extension. Works like the Unix ``file`` command.
The ``MimeMagicFile`` directive points to a magic file database. In practice,
:module:`mod_mime`'s extension-based approach covers 99% of cases, and this
module adds overhead. I'd only reach for it if you're serving user-uploaded
files with unreliable extensions.

.. _Module_ref_mod_cern_meta:

:module:`mod_cern_meta`
~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_cern_meta

A relic from CERN httpd compatibility days. Lets you specify per-file HTTP
headers via companion metafiles. For example, a file ``foo.html`` could have a
``foo.html.meta`` file containing additional headers. Nobody uses this anymore.
Use :module:`mod_headers` instead—it's more flexible, doesn't require extra
files on disk, and isn't a maintenance headache. I mention this module solely
because you might encounter it in very old configurations.


.. index::
   single: modules; authentication
   single: mod_authz_host
   single: mod_authz_dbm

Authentication and authorization
----------------------------------

Most auth modules get full coverage in :ref:`Chapter_AAA`. These two
have only partial treatment there.

.. _Module_ref_mod_authz_host:

:module:`mod_authz_host`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_authz_host

Provides host-based access control via the ``Require ip`` and ``Require host``
directives. This is how you restrict access to specific IP ranges or hostnames
without requiring user authentication. Common patterns include locking down
``/server-status`` to localhost or allowing only your office subnet to reach
admin pages. It's the authorization half of what ``Allow``/``Deny`` used to do
in 2.2. Works within ``<RequireAll>``, ``<RequireAny>``, and ``<RequireNone>``
containers for complex logic.

See :ref:`Chapter_AAA` for integration with other ``Require``
providers.

.. _Module_ref_mod_authz_dbm:

:module:`mod_authz_dbm`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_authz_dbm

Provides group authorization using DBM files. Where :module:`mod_authz_groupfile`
reads a plain text file of group memberships, this module reads the same
information from a DBM database—faster lookups when you have many groups or
large membership lists. Create the DBM file with ``dbmmanage`` or ``htdbm``.
The key directive is ``AuthDBMGroupFile``. Pairs naturally with
:module:`mod_authn_dbm` if you're already storing passwords in DBM format.

See :ref:`Chapter_AAA` for the full DBM authentication story.


.. index::
   single: modules; caching
   single: mod_cache_socache
   single: mod_socache_redis
   single: mod_socache_dbm
   single: mod_socache_memcache
   single: mod_socache_dc
   single: mod_slotmem_plain
   single: mod_slotmem_shm

Caching and shared object caches
----------------------------------

These modules provide various backends for httpd's shared object cache (socache)
infrastructure and slot-based shared memory. The socache framework is used by
:module:`mod_ssl` (session cache), :module:`mod_authn_socache` (credential
cache), and :module:`mod_cache_socache` (HTTP response cache), among others.

.. _Module_ref_mod_cache_socache:

:module:`mod_cache_socache`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_cache_socache

An HTTP caching storage backend that uses the shared object cache framework
instead of disk files. Faster than :module:`mod_cache_disk` for small objects
because everything stays in memory (or memcache/redis depending on your socache
provider). Configure it with ``CacheSocache`` followed by the provider name.
Best suited for caching small, frequently-requested responses behind a reverse
proxy. For large objects or persistence across restarts, stick with
:module:`mod_cache_disk`.

See :ref:`Chapter_Performance_and_testing` for the broader caching picture.

.. _Module_ref_mod_socache_redis:

:module:`mod_socache_redis`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_socache_redis

A shared object cache provider backed by Redis. Available in httpd 2.4
(added around the 2.4.10 timeframe). Particularly useful if you're already
running Redis in your infrastructure and want a centralized SSL session cache
shared across multiple httpd instances. Configure it as
``SSLSessionCache "redis:host=redis.example.com:6379"`` or use it with any
socache consumer. Supports authentication via ``RedisConnPoolTTL`` and server
specification with ``host:port`` syntax.

.. _Module_ref_mod_socache_dbm:

:module:`mod_socache_dbm`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_socache_dbm

Stores shared cache data in DBM files on disk. Slower than ``shmcb`` (the
shared-memory provider) but persists across restarts. Use it when you need
cache survival across graceful restarts and don't have Redis or Memcache
available. The syntax is ``SSLSessionCache "dbm:/path/to/cache"``. Honestly,
for most deployments ``shmcb`` is better—the restart penalty is minimal.

.. _Module_ref_mod_socache_memcache:

:module:`mod_socache_memcache`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_socache_memcache

Distributed shared object cache provider using Memcached. Similar use case to
Redis but uses the memcache protocol. Good when you already have Memcached
infrastructure. Specify servers as
``SSLSessionCache "memcache:mc1.example.com:11211,mc2.example.com:11211"``.
Like Redis, this gives you cache sharing across multiple httpd instances—
essential if you're load-balancing SSL termination and want session resumption
to work regardless of which server handles the next connection.

.. _Module_ref_mod_socache_dc:

:module:`mod_socache_dc`
~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_socache_dc

Distcache-based shared object cache provider. Distcache was a distributed
session caching system. The project has been effectively dead for years—its
website is gone, and nobody maintains it. I'd consider this module deprecated
in all but name. Use ``shmcb``, Redis, or Memcache instead. It exists in the
source tree for historical reasons.

.. _Module_ref_mod_slotmem_plain:

:module:`mod_slotmem_plain`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_slotmem_plain

Provides a plain file-based slot memory provider. "Slot memory" is httpd's
internal mechanism for sharing fixed-size data structures between worker
processes—used primarily by :module:`mod_proxy_balancer` to track backend
status. The "plain" variant stores data in a flat file. You almost never
configure this directly; it's infrastructure that other modules consume. If
you're not doing custom module development, you can ignore it.

.. _Module_ref_mod_slotmem_shm:

:module:`mod_slotmem_shm`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_slotmem_shm

The shared-memory variant of the slot memory provider. This is what
:module:`mod_proxy_balancer` actually uses in most deployments to share load
balancer state between processes. Like :module:`mod_slotmem_plain`, you don't
configure it directly—it's loaded automatically when needed. The only reason
you'd ever think about it is during compilation (making sure shared memory
support is available) or when debugging balancer issues.


.. index::
   single: modules; proxy
   single: mod_proxy_express
   single: mod_proxy_fdpass
   single: mod_proxy_scgi
   single: mod_proxy_uwsgi
   single: mod_proxy_connect
   single: mod_proxy_html

Proxy modules
--------------

The proxy framework is covered extensively in :ref:`Chapter_Proxies`. These
modules have minimal coverage there.

.. _Module_ref_mod_proxy_express:

:module:`mod_proxy_express`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_proxy_express

Mass reverse proxying made easy. Instead of writing hundreds of ``ProxyPass``
lines, you store URL-to-backend mappings in a DBM file and
:module:`mod_proxy_express` looks them up dynamically per request. Enable with
``ProxyExpressEnable On`` and point to your map with ``ProxyExpressDBMFile``.
Ideal for hosting platforms that add and remove backends frequently without
restarting httpd. Create the DBM file with ``httxt2dbm``.

.. _Module_ref_mod_proxy_fdpass:

:module:`mod_proxy_fdpass`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_proxy_fdpass

Passes the client's socket file descriptor directly to another process via a
Unix domain socket. The receiving process gets the raw TCP connection and
handles the HTTP exchange itself. This is extremely specialized—used when
you want another daemon to handle certain requests at the socket level without
httpd doing any HTTP processing. Very few people need this. It only works on
Unix platforms that support ``sendmsg()`` with ``SCM_RIGHTS``.

.. _Module_ref_mod_proxy_scgi:

:module:`mod_proxy_scgi`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_proxy_scgi

Proxy support for the SCGI (Simple CGI) protocol. SCGI is a simpler
alternative to FastCGI—fewer features but easier to implement. Some Python
frameworks (notably older Zope/Plone setups and some custom Python apps) speak
SCGI. Configure with ``ProxyPass "/app" "scgi://localhost:4000/"``. The
``ProxySCGISendfile`` directive lets the backend delegate file serving back to
httpd for efficiency. If your app supports both SCGI and FastCGI, prefer
FastCGI—it's more widely supported and better tested.

.. _Module_ref_mod_proxy_uwsgi:

:module:`mod_proxy_uwsgi`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_proxy_uwsgi

Native proxy support for the uWSGI binary protocol. If you're running Python
(Django, Flask) or Ruby applications behind uWSGI, this module lets httpd talk
directly to the uWSGI application server without HTTP overhead. Configure with
``ProxyPass "/app" "uwsgi://localhost:3031/"``. Available in 2.4.30+. This is
faster than proxying via HTTP because the uwsgi wire protocol has less parsing
overhead. Supports both TCP and Unix domain sockets
(``uwsgi://localhost:3031/`` or ``unix:/path/to/sock|uwsgi://localhost/``).

.. _Module_ref_mod_proxy_connect:

:module:`mod_proxy_connect`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_proxy_connect

Handles the HTTP ``CONNECT`` method for SSL/TLS tunneling through a forward
proxy. When a client wants to make an HTTPS request through your proxy, it
sends a ``CONNECT`` request, and this module establishes the tunnel. Essential
for forward proxy deployments; irrelevant for reverse proxies. The
``AllowCONNECT`` directive restricts which ports can be tunneled (default: 443
and 563). If you're building a forward proxy, you need this. Otherwise, ignore
it.

See :ref:`Chapter_Proxies` for forward proxy configuration.

.. _Module_ref_mod_proxy_html:

:module:`mod_proxy_html`
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_proxy_html

Rewrites URLs embedded in HTML responses when reverse-proxying. If your backend
serves content with absolute URLs (``http://internal.example.com/path``) and
clients access it through a different URL, this module rewrites links, form
actions, and other URL references in the HTML so they work correctly. Directives
include ``ProxyHTMLURLMap`` for defining rewrite rules and ``ProxyHTMLEnable``
to activate it. Requires :module:`mod_xml2enc` for proper character encoding
handling. Useful but fragile—modern apps should use relative URLs instead.

See :ref:`Chapter_Proxies` for reverse proxy patterns.


.. index::
   single: modules; logging
   single: mod_log_debug
   single: mod_log_forensic
   single: mod_unique_id

Logging and debugging
----------------------

Most logging is covered in :ref:`Chapter_Logging`. These modules provide
specialized debugging capabilities.

.. _Module_ref_mod_log_debug:

:module:`mod_log_debug`
~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_log_debug

Adds configurable debug logging that you can place in specific contexts. The
``LogMessage`` directive logs a custom message at a given log level, and
you can attach it to particular ``<Location>`` or ``<Directory>`` blocks.
Supports expression-based messages using ``%{expr:...}`` syntax. Invaluable
when you need to trace why a specific URL path is behaving unexpectedly
without turning up ``LogLevel`` globally. Use it surgically—add a
``LogMessage`` where you're debugging, remove it when done.

See :ref:`Chapter_Logging` for broader debug logging strategies.

.. _Module_ref_mod_log_forensic:

:module:`mod_log_forensic`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_log_forensic

Logs a unique ID at the beginning *and* end of each request. If a request
causes a crash, you'll have the "begin" entry without a matching "end"
entry—identifying exactly which request killed the process. Enable with
``ForensicLog /path/to/forensic.log``. Each entry includes all request headers.
This generates significant log volume, so enable it only when investigating
crashes or hangs. Pairs well with :module:`mod_unique_id` for correlation with
regular access logs.

See :ref:`Chapter_Logging` for forensic logging recipes.

.. _Module_ref_mod_unique_id:

:module:`mod_unique_id`
~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_unique_id

Generates a globally unique identifier for every request and sets it in the
``UNIQUE_ID`` environment variable. The ID is guaranteed unique across all
requests to a given server (and mostly unique across a cluster). Use it to
correlate access logs with application logs, forensic logs, or error logs.
Include it in your ``LogFormat`` with ``%{UNIQUE_ID}e`` and pass it to backends
via a request header. If you do any kind of distributed tracing, this is your
starting point.

See :ref:`Chapter_Logging` for tracing recipes.


.. index::
   single: modules; request manipulation
   single: mod_headers
   single: mod_buffer
   single: mod_request
   single: mod_charset_lite
   single: mod_xml2enc
   single: mod_echo

Request and response manipulation
-----------------------------------

Modules that modify request or response data in transit.

.. _Module_ref_mod_headers:

:module:`mod_headers`
~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_headers

Your go-to module for manipulating HTTP headers on both requests and responses.
``Header set`` adds or overrides response headers, ``Header append`` adds
values, ``RequestHeader set`` modifies inbound request headers. Supports
conditional operations via ``expr=`` expressions. You'll use this for security
headers (``Strict-Transport-Security``, ``X-Content-Type-Options``), CORS
headers, cache control overrides, and passing information to backends. One of
the most frequently used modules in any production configuration.

See :ref:`Chapter_Security` and :ref:`Chapter_Performance_and_testing` for security and
caching header recipes.

.. _Module_ref_mod_buffer:

:module:`mod_buffer`
~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_buffer

Buffers input and/or output filter stacks. The ``BufferSize`` directive
specifies how much data to accumulate before passing it along. Useful when
you have a filter chain that works better with larger chunks—for example,
if a compression filter performs poorly on tiny writes. In practice, I've
rarely needed this. The main use case is when you're chaining multiple output
filters and one of them needs to see complete chunks. An input buffer can
also prevent a slow-sending client from tying up a backend connection.

.. _Module_ref_mod_request:

:module:`mod_request`
~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_request

Makes HTTP request bodies available to multiple consumers. Normally, a request
body can only be read once. The ``KeptBodySize`` directive tells httpd to
retain up to N bytes of the request body so it can be accessed by
authorization modules, filters, or other handlers that run after the primary
handler has already consumed it. Essential for :module:`mod_auth_form` (which
reads POST bodies for login credentials) and useful when you need a filter to
inspect a POST body that will also be forwarded to a backend.

.. _Module_ref_mod_charset_lite:

:module:`mod_charset_lite`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_charset_lite

Translates response character encodings on the fly. If your content is stored
in one charset (say, ISO-8859-1) but you want to serve it as UTF-8, this module
handles the conversion. Configure with ``CharsetSourceEnc`` and
``CharsetDefault``. The "lite" in the name means it relies on ``iconv()`` and
doesn't handle every edge case. In 2025, the right answer is almost always to
store your content as UTF-8 from the start. This module exists for legacy
content that you can't easily convert at rest.

.. _Module_ref_mod_xml2enc:

:module:`mod_xml2enc`
~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_xml2enc

Provides enhanced charset detection and conversion for modules that use libxml2
for processing—primarily :module:`mod_proxy_html` and :module:`mod_substitute`.
Without it, those modules may misinterpret character encodings in proxied
content. If you're using :module:`mod_proxy_html` to rewrite URLs in proxied
HTML, you almost certainly need this loaded too. It sniffs the encoding from
XML declarations, meta tags, and HTTP headers, then ensures libxml2 gets
properly encoded input.

.. _Module_ref_mod_echo:

:module:`mod_echo`
~~~~~~~~~~~~~~~~~~~

.. index:: mod_echo

A trivial protocol module that echoes back whatever the client sends. It exists
purely as a teaching example for module developers—demonstrating how to
implement a protocol handler. Configure with ``<IfModule mod_echo.c>`` and
``Listen`` on a different port, then ``ProtocolEcho On``. It has zero
production utility. If you're learning to write httpd modules, read its source
code. Otherwise, move along.


.. index::
   single: modules; security
   single: mod_allowhandlers
   single: mod_ssl_ct
   single: mod_policy

Security
---------

Specialized security modules beyond what's covered in :ref:`Chapter_Security`.

.. _Module_ref_mod_allowhandlers:

:module:`mod_allowhandlers`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_allowhandlers

:version:`trunk`

Restricts which handlers can be invoked for requests in a given context. Think
of it as a whitelist (or blacklist with ``not``) for handlers. If you want to
ensure that only ``server-status`` and ``static`` handlers can run, and nothing
else (no CGI, no PHP, no server-info), you lock it down with
``AllowHandlers not cgi-script php-script``. Also provides a ``forbidden``
handler that returns 403. This is defense-in-depth—if an attacker somehow
enables a handler via ``.htaccess``, this stops it from executing.

.. _Module_ref_mod_ssl_ct:

:module:`mod_ssl_ct`
~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_ssl_ct

:version:`trunk`

Implements Certificate Transparency (RFC 6962) for httpd—delivering Signed
Certificate Timestamps (SCTs) to clients. When this was developed, CT
enforcement was still being rolled out. Today, Certificate Authorities embed
SCTs in certificates by default, and browsers require CT as part of normal
certificate issuance. That makes this module largely unnecessary for most
deployments—your CA handles it. It remains relevant only if you're using
privately-issued certificates and need to submit them to CT logs yourself.
Note: the upstream ``certificate-transparency`` C++ tools (which this module
depends on) have been archived by Google.

.. _Module_ref_mod_policy:

:module:`mod_policy`
~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_policy

:version:`trunk`

A set of output filters that test HTTP responses for protocol compliance.
You can enforce rules like "all responses must have a ``Content-Type``,"
"responses must include freshness headers," "no HTTP/1.0 responses," and
similar policies. Designed for large deployments where backend applications
might emit non-compliant responses that hurt cacheability or client behavior.
Directives include ``PolicyType``, ``PolicyLength``, ``PolicyKeepalive``,
``PolicyMaxage``, ``PolicyValidation``, and ``PolicyVary``. Violations can be
logged or can result in a 502 rejection. Fascinating concept, but I've never
seen it deployed in the wild.


.. index::
   single: modules; WebDAV
   single: mod_dav
   single: mod_dav_fs
   single: mod_dav_lock

WebDAV
-------

WebDAV (web Distributed Authoring and Versioning) extends HTTP with methods
for remote file management—creating, moving, copying, and locking resources.
It's the protocol behind many file-sharing solutions, CalDAV, and CardDAV.

.. _Module_ref_mod_dav:

:module:`mod_dav`
~~~~~~~~~~~~~~~~~~

.. index:: mod_dav

The core WebDAV framework module. It implements the WebDAV HTTP methods
(``PROPFIND``, ``PROPPATCH``, ``MKCOL``, ``COPY``, ``MOVE``, ``LOCK``,
``UNLOCK``) but delegates actual storage to provider modules. Enable with
``Dav On`` in a ``<Directory>`` or ``<Location>`` context. You always need
at least one storage provider (:module:`mod_dav_fs` for filesystem storage)
alongside it. WebDAV was big in the 2000s for collaborative editing. Today
it's mostly used by CalDAV/CardDAV clients and a few file sync tools.

.. _Module_ref_mod_dav_fs:

:module:`mod_dav_fs`
~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_dav_fs

The filesystem storage provider for WebDAV. Stores WebDAV properties in a
DBM database (specified by ``DavLockDB``) and serves files directly from the
filesystem. The ``DavLockDB`` directive points to the lock database location.
This is what you use for simple "shared drive over HTTP" setups. Don't forget
to set appropriate permissions on the document root—httpd needs write access
for WebDAV to work, which has obvious security implications.

.. _Module_ref_mod_dav_lock:

:module:`mod_dav_lock`
~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_dav_lock

A generic locking module for WebDAV providers that don't implement their own
lock management. If you're building a custom DAV provider (maybe backed by a
database or cloud storage) and don't want to implement RFC 4918 locking
yourself, this module provides it for you. For filesystem-based WebDAV
(:module:`mod_dav_fs`), you don't need this—:module:`mod_dav_fs` handles its
own locks. Only relevant if you're working with third-party DAV provider
modules.


.. index::
   single: modules; user management
   single: mod_userdir
   single: mod_usertrack
   single: mod_suexec
   single: mod_ident

User management
----------------

Modules related to user-level features and identity tracking.

.. _Module_ref_mod_userdir:

:module:`mod_userdir`
~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_userdir

Maps ``http://example.com/~username/`` to a directory in that user's home
folder (typically :file:`/home/username/public_html`). The ``UserDir``
directive specifies the subdirectory name. This was the original "personal
homepage" feature—every Unix account gets a web presence. Still useful on
university and shared hosting servers. Security note: you should explicitly
``UserDir disabled root`` and consider disabling it for system accounts. You
can also enable it only for specific users with ``UserDir enabled alice bob``.

.. _Module_ref_mod_usertrack:

:module:`mod_usertrack`
~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_usertrack

Sets a tracking cookie (``Apache``, by default) on each visitor's browser,
giving you a unique identifier per user session. The ``CookieTracking On``
directive enables it, ``CookieName`` changes the name, ``CookieDomain`` sets
the domain scope, and ``CookieExpires`` controls lifetime. The module predates modern
analytics tools. Log the cookie value in your access log with
``%{Apache}C`` (or whatever you named it) and you can correlate requests from
the same user. In an era of GDPR and privacy regulations, be aware that setting
tracking cookies without consent may have legal implications in some
jurisdictions.

.. _Module_ref_mod_suexec:

:module:`mod_suexec`
~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_suexec

Allows CGI scripts to run as a user and group other than the httpd process
owner. The ``SuexecUserGroup`` directive (in a ``<VirtualHost>``) specifies
which user/group to use. The actual privilege switching is done by the
``suexec`` helper binary, which is setuid root and extremely paranoid about
what it will execute (document root checks, ownership checks, no sticky bits,
etc.). Essential for shared hosting where each customer's scripts should run
under their own account. Not needed in container-based deployments where each
tenant gets their own httpd instance.

See :ref:`Chapter_Dynamic_content` for CGI execution models.

.. _Module_ref_mod_ident:

:module:`mod_ident`
~~~~~~~~~~~~~~~~~~~~

.. index:: mod_ident

Performs RFC 1413 ``ident`` lookups to determine the remote username associated
with a TCP connection. The ``IdentityCheck On`` directive enables it. This is
a relic from a more trusting era of the internet—the ident protocol relies on
the remote host honestly reporting who initiated the connection. In practice,
almost no hosts run identd anymore, the lookups add latency, and the results
are untrustworthy. The ``%l`` log format token captures the ident result. Don't
enable this unless you're running on a private network where you control all
clients. Even then, there are better ways to identify users.


.. index::
   single: modules; infrastructure
   single: mod_so
   single: mod_unixd
   single: mod_watchdog
   single: mpm_common
   single: mod_example_hooks

Infrastructure and internals
-----------------------------

Modules that provide core infrastructure or exist as developer tooling.

.. _Module_ref_mod_so:

:module:`mod_so`
~~~~~~~~~~~~~~~~~

.. index:: mod_so

The module that makes all other modules possible. :module:`mod_so` provides
``LoadModule``—the directive that loads shared object (``.so``) modules at
startup. On virtually every httpd installation, this is statically compiled
in and you never think about it. The only time you'd care is when building
httpd from source with ``--enable-so`` (which is the default). Without it,
every module must be compiled statically into the httpd binary.

.. _Module_ref_mod_unixd:

:module:`mod_unixd`
~~~~~~~~~~~~~~~~~~~~

.. index:: mod_unixd

Provides basic security operations on Unix platforms: switching to an
unprivileged user/group after binding to privileged ports, setting the
``umask``, and handling ``chroot``. The ``User`` and ``Group`` directives
live here. You configure this in every httpd installation—specifying which
user (typically ``www-data`` or ``apache``) the server runs as. The
``ChrootDir`` directive can jail httpd into a directory, though chroot jails
have largely been superseded by containers and namespaces.

.. _Module_ref_mod_watchdog:

:module:`mod_watchdog`
~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_watchdog

An infrastructure module that provides a periodic callback mechanism for other
modules. Think of it as a cron-within-httpd. Modules like
:module:`mod_proxy_hcheck` (health checking) and :module:`mod_heartmonitor` use
watchdog to schedule recurring tasks. You don't configure it directly—it's
loaded automatically when a module that needs periodic execution is present.
If you see ``mod_watchdog`` in your module list, it's there because something
else depends on it.

.. _Module_ref_mpm_common:

``mpm_common``
~~~~~~~~~~~~~~~

.. index:: mpm_common

Not a loadable module but a documentation grouping for directives shared across
all Multi-Processing Modules (MPMs). Directives like ``MaxRequestWorkers``,
``StartServers``, ``ServerLimit``, ``ThreadsPerChild``, ``MaxConnectionsPerChild``,
``GracefulShutdownTimeout``, and ``ListenBacklog`` are defined here. When you're
tuning performance and process/thread counts, you're working with mpm_common
directives regardless of whether you're running event, worker, or prefork.

See :ref:`Chapter_Performance_and_testing` for tuning guidance.

.. _Module_ref_mod_example_hooks:

:module:`mod_example_hooks`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_example_hooks

A demonstration module that logs which hooks are called during request
processing. It exists solely as a reference for module developers—showing the
order and context of all available hooks. If you're writing a new httpd module
and want to understand the request lifecycle, compile this in, hit the server,
and read the log output. Zero production utility. Located in the
:file:`modules/examples/` directory of the source tree.


.. index::
   single: modules; specialized
   single: mod_heartbeat
   single: mod_heartmonitor
   single: mod_crypto
   single: mod_firehose

Specialized and rarely used
-----------------------------

Modules that serve narrow use cases or exist only in trunk.

.. _Module_ref_mod_heartbeat:

:module:`mod_heartbeat`
~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_heartbeat

Sends multicast UDP messages advertising this server's current load (busy/idle
worker counts). Designed to work with :module:`mod_heartmonitor` on a front-end
proxy for dynamic load balancing based on real-time backend capacity. The idea
is appealing: instead of static weights, route traffic to whichever backend has
capacity. In practice, multicast adds network complexity, and most people use
:module:`mod_proxy_hcheck` for health checking with simpler
:module:`mod_lbmethod_bybusyness` for load distribution. Consider this
experimental and rarely deployed.

.. _Module_ref_mod_heartmonitor:

:module:`mod_heartmonitor`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_heartmonitor

The receiving side of :module:`mod_heartbeat`. Runs on the front-end proxy,
collects heartbeat messages from backend servers, and writes their status to a
file that :module:`mod_lbmethod_heartbeat` reads for load balancing decisions.
Configured with ``HeartbeatListen`` (the multicast address to monitor) and
``HeartbeatStorage`` (where to write the status file). Same caveats as
:module:`mod_heartbeat`—interesting concept, complex deployment, largely
unused in practice.

.. _Module_ref_mod_crypto:

:module:`mod_crypto`
~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_crypto

:version:`trunk`

Provides input/output filters for symmetric encryption and decryption of
content using the ``CryptoKey`` and ``CryptoDriver`` directives. You could
encrypt response bodies or decrypt request bodies in-flight. The documentation
is sparse and the use cases are niche—most encryption needs are handled at the
transport layer (TLS) or the application layer. I could imagine using this for
encrypting cached content at rest, but that's speculative. Experimental and
trunk-only.

.. _Module_ref_mod_firehose:

:module:`mod_firehose`
~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_firehose

:version:`trunk`

Multiplexes all HTTP request/response data to a file or pipe, including
headers and bodies. Think of it as a full traffic recorder. Configured with
``FirehoseConnectionInput``, ``FirehoseConnectionOutput``,
``FirehoseRequestInput``, and ``FirehoseRequestOutput``. Designed for traffic
analysis and replay testing. The output format is multiplexed so you can
demultiplex individual connections afterward. Trunk-only and experimental. For
most debugging needs, :module:`mod_dumpio` (which logs to the error log) is
sufficient and already available in 2.4.


.. index::
   single: modules; load balancing methods
   single: mod_lbmethod_byrequests
   single: mod_lbmethod_bytraffic
   single: mod_lbmethod_bybusyness
   single: mod_lbmethod_heartbeat

Load balancer methods
----------------------

These modules implement the algorithms that :module:`mod_proxy_balancer` uses
to distribute requests across backend servers. You select one via the
``lbmethod`` parameter in your ``<Proxy balancer://...>`` configuration.

See :ref:`Chapter_Proxies` for full load balancer configuration.

.. _Module_ref_mod_lbmethod_byrequests:

:module:`mod_lbmethod_byrequests`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_lbmethod_byrequests

The default load balancing method. Distributes requests using a weighted
round-robin algorithm. Each backend gets a share of requests proportional to
its ``loadfactor`` weight. Simple, predictable, and works well when backends
have similar capacity and requests have similar cost. Use ``lbmethod=byrequests``
(or just leave it as the default). If your requests vary wildly in processing
time, consider ``bybusyness`` instead.

.. _Module_ref_mod_lbmethod_bytraffic:

:module:`mod_lbmethod_bytraffic`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_lbmethod_bytraffic

Distributes requests based on the amount of traffic (bytes) each backend has
handled. Backends that have transferred less data get more requests. Useful
when request sizes vary significantly—a backend serving large file downloads
shouldn't also get hammered with small API requests. Use
``lbmethod=bytraffic``. The weights are based on cumulative bytes
transferred, so it favors backends that have served less data overall.

.. _Module_ref_mod_lbmethod_bybusyness:

:module:`mod_lbmethod_bybusyness`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_lbmethod_bybusyness

Routes each new request to whichever backend currently has the fewest active
connections. This is often the best algorithm for heterogeneous backends or
variable request durations—it naturally adapts to slow backends by sending them
fewer requests. Use ``lbmethod=bybusyness``. If a backend is slow (maybe it's
under GC pressure), it'll accumulate connections and stop getting new ones.
My personal go-to for most reverse proxy setups.

.. _Module_ref_mod_lbmethod_heartbeat:

:module:`mod_lbmethod_heartbeat`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_lbmethod_heartbeat

Uses real-time load data from :module:`mod_heartmonitor` (fed by
:module:`mod_heartbeat` running on backends) to make routing decisions.
Backends advertise their busy/idle worker counts, and this method routes
to the least-loaded server. Theoretically optimal—but requires the full
heartbeat infrastructure (multicast networking, heartmonitor on the proxy,
heartbeat on every backend). In practice, ``bybusyness`` gives you 90% of
the benefit with zero additional infrastructure.


.. index::
   single: modules; trunk-only
   single: mod_journald
   single: mod_syslog

Trunk-only logging modules
----------------------------

These modules are coming in httpd 2.6 and provide alternative ErrorLog
providers.

.. _Module_ref_mod_journald:

:module:`mod_journald`
~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_journald

:version:`trunk`

Provides a ``journald`` error log provider for systems running systemd. Instead
of writing to a file, httpd sends error log messages directly to the systemd
journal with structured metadata (module name, log level, PID). Enable with
``ErrorLog journald``. Useful if your infrastructure consolidates logging
via ``journalctl`` and you want httpd error messages in the same stream as
other system services. Pairs naturally with :module:`mod_systemd`.

.. _Module_ref_mod_syslog:

:module:`mod_syslog`
~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_syslog

:version:`trunk`

Provides a ``syslog`` error log provider, sending error log messages to the
system syslog daemon. Configure with ``ErrorLog syslog`` or
``ErrorLog syslog:facility``. In 2.4, syslog support is built into the core
for Unix platforms. This trunk module refactors it into a proper provider
module and may add enhanced structured logging. For most people, the behavior
will be identical to what they already have.


.. index::
   single: modules; Lua
   single: mod_lua

Additional modules with partial coverage
------------------------------------------

A few modules have substantial mentions scattered across multiple chapters but
no single dedicated recipe section. They're worth a brief note here.

.. _Module_ref_mod_lua:

:module:`mod_lua`
~~~~~~~~~~~~~~~~~~

.. index:: mod_lua

Embeds the Lua scripting language into httpd, letting you write request
handlers, authentication providers, input/output filters, and hook functions in
Lua. Configure with ``LuaHookAccessChecker``, ``LuaHookAuthChecker``,
``LuaMapHandler``, and similar directives. Lua scripts run within the httpd
process (no fork overhead). It's a lightweight alternative to writing C modules
when you need server-level logic but don't want the complexity of a full
application framework. See :ref:`Chapter_info_and_status` for some Lua-based
status page examples.

.. _Module_ref_mod_include_deeper:

:module:`mod_include` (SSI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: mod_include; extended reference

Server Side Includes offer conditional logic (``<!--#if expr="..." -->``),
variable setting, file inclusion, and command execution. The expression syntax
in 2.4+ supports the full ``ap_expr`` parser, making conditionals quite
powerful. Key directives: ``SSIStartTag``, ``SSIEndTag`` (customize the
delimiters), ``SSIUndefinedEcho`` (what to display for undefined variables),
and ``SSILastModified`` (whether to update ``Last-Modified`` based on included
files). Enable with ``Options +Includes`` and either ``AddOutputFilter
INCLUDES .shtml`` or ``SetOutputFilter INCLUDES``.

See :ref:`Chapter_Dynamic_content` for SSI examples.


.. index::
   single: modules; platform-specific

.. note:: **Platform-specific modules**

   The following modules exist for specific operating systems and are not
   covered in this book:

   - :module:`mpm_netware` — MPM for Novell NetWare (a dead platform)
   - :module:`mpmt_os2` — MPM for OS/2 (also a dead platform)
   - :module:`mod_nw_ssl` — SSL for NetWare
   - :module:`mod_isapi` — ISAPI extensions for Windows (use mod_proxy_fcgi instead)
   - :module:`mod_privileges` — Solaris privileges for per-vhost security (Solaris is in maintenance mode)
   - :module:`mpm_winnt` — Windows MPM (covered briefly in :ref:`Chapter_Installation`)

   If you're running httpd on any of these platforms, the official
   documentation is your best resource. This book assumes a Unix/Linux
   deployment.


Summary
--------

That's the full module catalog. A few closing observations:

- If you're running a typical reverse proxy or web application server, you
  probably use about 20-30 modules. The rest exist for specialized needs.

- The ``socache`` family (shmcb, redis, memcache, dbm) all do the same thing
  via different backends. Pick whichever matches your infrastructure.

- The heartbeat/heartmonitor system is clever but overengineered for most
  deployments. Use ``bybusyness`` instead.

- Trunk-only modules (marked with :version:`trunk`) will appear in httpd 2.6.
  Don't try to use them on 2.4 unless you're building from source.

- When in doubt about whether you need a module, you probably don't.
  Start minimal and add modules only when you have a concrete requirement.
  Every loaded module consumes memory and increases your attack surface.
