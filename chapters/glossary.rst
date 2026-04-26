========
Glossary
========

.. glossary::
   :sorted:

   Apache httpd
      The Apache HTTP Server, commonly referred to as Apache. An open-source,
      cross-platform web server maintained by the Apache Software Foundation.
      The current major version is 2.4.

   module
      A loadable component that extends the functionality of Apache httpd.
      Modules are loaded with the :term:`LoadModule` directive and can add
      new :term:`directive`\s, :term:`handler`\s, :term:`filter`\s, and
      authentication providers. See :ref:`Chapter_Common_modules`.

   directive
      A configuration command in the Apache httpd configuration files that
      controls the behavior of the server. Each directive has a defined
      :term:`context` in which it may appear. For example,
      :term:`DocumentRoot` is a directive that sets the document directory.

   context
      The scope in which a :term:`directive` may legally appear.
      Common contexts include server config (global), :term:`<VirtualHost>`,
      :term:`<Directory>`, :term:`<Location>`, :term:`<Files>`, and
      :term:`.htaccess`.

   virtual host
      A method of hosting multiple websites on a single server, either
      by IP address (address-based) or by hostname (name-based).
      Configured with :term:`<VirtualHost>` container directives.
      See :ref:`Chapter_Virtual_hosts`.

   name-based virtual host
      A :term:`virtual host` configuration where multiple hostnames share
      a single IP address. The server uses the ``Host`` header sent by the
      client to determine which virtual host should handle the request.

   MPM
      Multi-Processing Module. The component of Apache httpd responsible for
      binding to network ports, accepting requests, and dispatching them to
      child processes or threads. The three main Unix MPMs are ``prefork``
      (process-based), ``worker`` (hybrid process/thread), and ``event``
      (optimized hybrid). Only one MPM can be active at a time.

   event MPM
      The recommended :term:`MPM` for modern Unix systems. It uses a
      dedicated listener thread to handle idle keepalive connections
      efficiently, freeing worker threads to process new requests.

   prefork MPM
      A :term:`MPM` that uses multiple child processes, each handling one
      request at a time with no threading. Once required for non-thread-safe
      libraries like older PHP, it is now largely superseded by :term:`event MPM`.

   worker MPM
      A hybrid :term:`MPM` using multiple child processes, each containing
      multiple threads. It offers better resource utilization than
      :term:`prefork MPM` but lacks the keepalive optimization of
      :term:`event MPM`.

   .htaccess
      A per-directory configuration file that allows decentralized management
      of web server configuration. Parsed on every matching request when
      :term:`AllowOverride` permits it. Convenient on shared hosting but
      carries a performance cost. See :ref:`Chapter_htaccess`.

   httpd.conf
      The main configuration file for the Apache HTTP Server. Its location
      varies by platform and installation method. On Red Hat/Fedora systems
      it is typically ``/etc/httpd/conf/httpd.conf``; on Debian/Ubuntu,
      ``/etc/apache2/apache2.conf``.

   SSL
      Secure Sockets Layer. The predecessor to :term:`TLS`, providing
      encrypted communication between web browsers and servers. All SSL
      versions are now deprecated in favor of TLS, but the term is still
      widely used colloquially.

   TLS
      Transport Layer Security. The modern successor to :term:`SSL` for
      encrypting web traffic. TLS 1.2 and 1.3 are the currently recommended
      versions. Configured in Apache httpd via :term:`mod_ssl`.

   CGI
      Common Gateway Interface. A protocol for web servers to execute
      external programs and return their output as web content. Each request
      spawns a new process. See :ref:`Chapter_Dynamic_content`.

   FastCGI
      An extension of :term:`CGI` that keeps application processes running
      persistently, avoiding the overhead of spawning a new process for each
      request. Apache httpd communicates with FastCGI backends via
      ``mod_proxy_fcgi``.

   SSI
      Server Side Includes. A simple server-side scripting language,
      processed by :term:`mod_include`, for including dynamic content such
      as file timestamps, environment variables, and conditional text in
      HTML pages.

   proxy
      A server that acts as an intermediary for requests from clients
      seeking resources from other servers. Apache httpd implements
      forward proxy functionality with :term:`mod_proxy`.

   reverse proxy
      A :term:`proxy` server that retrieves resources on behalf of a client
      from one or more backend servers. The resources are returned to the
      client as if they originated from the proxy server itself. Configured
      with :term:`ProxyPass` and :term:`ProxyPassReverse`.
      See :ref:`Chapter_Proxies`.

   forward proxy
      A :term:`proxy` that sits between a client and the internet, making
      requests on behalf of the client. Unlike a :term:`reverse proxy`,
      clients explicitly configure their browser to use a forward proxy.

   load balancing
      The distribution of incoming requests across multiple backend servers
      to improve performance and reliability. Apache httpd provides load
      balancing via ``mod_proxy_balancer`` with scheduling algorithms such as
      byrequests, bytraffic, and bybusyness.

   HTTP
      HyperText Transfer Protocol. The foundational application-layer
      protocol of the World Wide Web, defining how clients request resources
      and how servers respond. Defined by a series of :term:`RFC` documents.

   HTTPS
      HTTP over :term:`TLS` (or :term:`SSL`). Provides encrypted, authenticated
      communication between browser and server. Uses port 443 by default.

   HTTP/1.1
      The most widely deployed version of the :term:`HTTP` protocol
      (RFC 2616, later refined by RFC 7230–7235). Introduced persistent
      connections (:term:`keepalive`), chunked transfer encoding, and the
      Host header that enables :term:`name-based virtual host`ing.

   HTTP/2
      A major revision of the :term:`HTTP` protocol that introduces
      multiplexed streams, header compression, and server push. Enabled in
      Apache httpd via ``mod_http2``.

   WebSocket
      A protocol providing full-duplex communication channels over a single
      TCP connection. Apache httpd supports WebSocket proxying via
      ``mod_proxy_wstunnel``.

   ACME
      Automatic Certificate Management Environment. The protocol used by
      :term:`Let's Encrypt` and other certificate authorities to automate
      certificate issuance and renewal. Apache httpd supports ACME via
      :term:`mod_md`.

   Let's Encrypt
      A free, automated, and open :term:`certificate authority` that issues
      :term:`TLS` certificates via the :term:`ACME` protocol. See
      :ref:`Chapter_SSL_and_TLS`.

   certificate authority
      CA. A trusted third party that issues digital :term:`certificate`\s,
      verifying the identity of the certificate holder. Examples include
      :term:`Let's Encrypt`, DigiCert, and Sectigo.

   certificate
      A digital document (typically :term:`X.509` format) that binds a
      public key to an identity (such as a domain name). Used by
      :term:`TLS` to establish encrypted connections.

   X.509
      The standard format for public key certificates used by :term:`TLS`.
      An X.509 certificate contains the subject, issuer, public key,
      validity period, and digital signature.

   OCSP
      Online Certificate Status Protocol. A method for checking the
      revocation status of a :term:`certificate` in real time. OCSP
      stapling, enabled via ``SSLUseStapling``, allows the server to
      include the OCSP response in the TLS handshake.

   SNI
      Server Name Indication. A :term:`TLS` extension that allows the
      client to indicate the hostname it is connecting to during the TLS
      handshake. This enables the server to present the correct
      :term:`certificate` when hosting multiple HTTPS sites on a single
      IP address.

   FQDN
      Fully Qualified Domain Name. The complete domain name for a host,
      including all parent domains up to the root. For example,
      ``www.example.com.`` is an FQDN.

   DNS
      Domain Name System. The distributed system that translates human-readable
      hostnames into IP addresses. Correct DNS configuration is essential for
      :term:`virtual host`\s to function properly.

   CIDR
      Classless Inter-Domain Routing. A notation for specifying IP address
      ranges, such as ``10.0.0.0/24``. Used in Apache httpd access control
      directives such as ``Require ip``.

   IPv6
      Internet Protocol version 6. The successor to IPv4, using 128-bit
      addresses. Apache httpd fully supports IPv6 in :term:`Listen`
      directives and access control.

   RFC
      Request for Comments. A formal document published by the IETF
      (Internet Engineering Task Force) that defines internet standards
      and protocols such as :term:`HTTP` (RFC 2616 / RFC 7230–7235) and
      :term:`TLS`.

   MIME type
      Multipurpose Internet Mail Extensions type. A label that identifies
      the format of a file or resource (e.g., ``text/html``,
      ``image/png``). Apache httpd maps file extensions to MIME types using
      :term:`mod_mime` and the ``mime.types`` file.

   DSO
      Dynamic Shared Object. A :term:`module` compiled as a shared library
      (``.so`` on Unix, ``.dll`` on Windows) that can be loaded into the
      server at runtime with :term:`LoadModule`, without recompiling httpd.

   handler
      A representation of the action to be performed when a file is
      requested. Handlers are either built into the server or provided by
      a :term:`module`. Examples include ``cgi-script``, ``server-status``,
      and ``default-handler``. Set with :term:`SetHandler` or
      :term:`AddHandler`.

   filter
      A processing stage that transforms content either on input or output.
      Apache httpd implements a filter chain, where content passes through
      multiple filters in sequence. Examples include :term:`mod_deflate`
      (compression) and :term:`mod_substitute` (text replacement).

   environment variable
      A name-value pair that can be set during request processing and used
      by directives, :term:`CGI` scripts, :term:`SSI`, and logging.
      Set with ``SetEnv``, ``SetEnvIf``, ``PassEnv``, and related
      directives.

   regular expression
      A pattern-matching language used to describe sets of strings. httpd
      httpd uses the PCRE (Perl Compatible Regular Expressions) library.
      Directives ending in ``Match`` (such as :term:`RedirectMatch`) and
      :term:`mod_rewrite` use regular expressions extensively.
      See :ref:`Chapter_regex`.

   backreference
      A captured group from a :term:`regular expression` match, referenced
      by number: ``$1``, ``$2``, etc. in :term:`RewriteRule`, or ``%1``,
      ``%2``, etc. in :term:`RewriteCond`. Used to insert matched text
      into replacement strings.

   content negotiation
      The process by which Apache httpd selects the best representation of
      a resource based on the client's stated preferences for language,
      media type, character set, and encoding. Provided by
      :term:`mod_negotiation` and enabled with the ``MultiViews`` option.

   URL mapping
      The process by which a requested URL is translated into a resource
      on the server—whether a file on disk, a :term:`CGI` script, a
      :term:`redirect`, or a :term:`proxy` pass-through. See
      :ref:`Chapter_URL_Mapping`.

   graceful restart
      A restart method (``apachectl graceful``) that allows Apache httpd
      to re-read its configuration without dropping any in-progress
      connections. Child processes finish serving current requests before
      being replaced.

   keepalive
      A feature of :term:`HTTP/1.1` (and later) that allows multiple
      requests to be sent over a single TCP connection, avoiding the
      overhead of establishing a new connection for each request. Controlled
      by the ``KeepAlive``, ``KeepAliveTimeout``, and
      ``MaxKeepAliveRequests`` directives.

   subrequest
      An internal request made by the server to itself during the
      processing of another request. Used by :term:`SSI`, :term:`mod_rewrite`
      (with the ``[PT]`` flag), and :term:`mod_include`. Not visible to the
      client.

   piped log
      A logging configuration where Apache httpd writes log entries to the
      standard input of an external program rather than to a file. Used
      with :term:`rotatelogs` for log rotation without restarting the
      server.

   Common Log Format
      CLF. A standardized access log format defined as
      ``%h %l %u %t "%r" %>s %b``. Records the client IP, identity, user,
      timestamp, request line, status code, and response size.

   Combined Log Format
      An extension of the :term:`Common Log Format` that adds the
      ``Referer`` and ``User-Agent`` request headers.
      Defined as the ``combined`` log format in the default configuration.

   authentication
      The process of verifying the identity of a user or client—"Are you
      who you claim to be?" Apache httpd supports Basic, Digest, and
      form-based authentication. See :ref:`Chapter_AAA`.

   authorization
      The process of determining whether an authenticated user is permitted
      to access a resource—"Are you allowed to be here?" Controlled by
      :term:`Require` directives and modules such as ``mod_authz_core``.

   access control
      Restricting access to resources based on criteria such as IP address,
      hostname, or time of day. Distinguished from :term:`authentication`
      (identity) and :term:`authorization` (permissions).

   basic authentication
      An :term:`HTTP` authentication scheme where the username and password
      are sent Base64-encoded (but not encrypted) with each request.
      Provided by ``mod_auth_basic``. Should be used only over
      :term:`HTTPS`.

   digest authentication
      An :term:`HTTP` authentication scheme that sends a cryptographic
      hash of the credentials rather than the cleartext password. Provided
      by ``mod_auth_digest``. More secure than :term:`basic authentication`
      but less widely used than form-based login.

   LDAP
      Lightweight Directory Access Protocol. A protocol for accessing
      directory services such as Active Directory or OpenLDAP. Apache httpd
      integrates with LDAP for authentication and authorization via
      ``mod_authnz_ldap``.

   PHP
      A widely used server-side scripting language for web development.
      In modern Apache httpd deployments, PHP is typically run via
      :term:`PHP-FPM` and :term:`FastCGI` rather than the legacy
      ``mod_php`` handler.

   PHP-FPM
      PHP FastCGI Process Manager. A :term:`FastCGI` implementation for
      :term:`PHP` that manages a pool of PHP worker processes. Apache httpd
      communicates with PHP-FPM via ``mod_proxy_fcgi``.

   HSTS
      HTTP Strict Transport Security. A security mechanism (defined in
      RFC 6797) that instructs browsers to only access a site over
      :term:`HTTPS`. Enabled by setting the ``Strict-Transport-Security``
      response header.

   SELinux
      Security-Enhanced Linux. A mandatory access control framework that
      can restrict the actions of the httpd process. SELinux policies must
      be configured correctly for Apache httpd to serve files, connect to
      backends, and write logs.

   suexec
      A support program shipped with Apache httpd that allows :term:`CGI`
      scripts and :term:`SSI` commands to run under a user ID different
      from the server's main user. Provides additional security for
      multi-user environments.

   DocumentRoot
      The :term:`directive` that specifies the directory from which httpd
      httpd serves files. For example, ``DocumentRoot "/var/www/html"``.
      Each :term:`virtual host` typically defines its own DocumentRoot.

   ServerRoot
      The :term:`directive` that sets the base directory for the server
      installation. Relative paths in other directives are resolved from
      ServerRoot.

   ServerName
      The :term:`directive` that specifies the hostname and port that the
      server uses to identify itself. Critical for :term:`virtual host`
      matching and for constructing self-referential URLs.

   ServerAlias
      A :term:`directive` used inside a :term:`<VirtualHost>` to list
      additional hostnames that should be matched to that virtual host.

   Listen
      The :term:`directive` that tells Apache httpd which IP addresses and
      ports to bind to. For example, ``Listen 80`` or ``Listen 443``.

   LoadModule
      The :term:`directive` that loads a :term:`DSO` module into the server
      at startup. Syntax: ``LoadModule module_name modules/mod_example.so``.

   AllowOverride
      The :term:`directive` that controls which directive categories may
      appear in :term:`.htaccess` files. ``AllowOverride None`` disables
      ``.htaccess`` entirely (recommended for performance);
      ``AllowOverride All`` permits all directives.

   Options
      The :term:`directive` that controls which server features are
      available in a directory. Common values include ``Indexes`` (directory
      listings), ``FollowSymLinks``, ``ExecCGI``, ``Includes``
      (:term:`SSI`), and ``MultiViews`` (:term:`content negotiation`).

   Require
      The :term:`directive` that specifies authorization rules in httpd
      httpd 2.4 and later. Examples include ``Require all granted``,
      ``Require user alice``, ``Require ip 10.0.0.0/8``, and
      ``Require valid-user``.

   Alias
      The :term:`directive` (from :term:`mod_alias`) that maps a URL path
      to a filesystem directory outside the :term:`DocumentRoot`. For
      example, ``Alias "/icons" "/usr/share/httpd/icons"``.

   Redirect
      The :term:`directive` (from :term:`mod_alias`) that sends an HTTP
      redirect response to the client, instructing the browser to request
      a different URL. Supports ``permanent`` (301), ``temp`` (302),
      ``seeother`` (303), and ``gone`` (410) types.

   RedirectMatch
      A variant of :term:`Redirect` that uses a :term:`regular expression`
      to match the request URL, allowing pattern-based redirects.

   ProxyPass
      The :term:`directive` (from :term:`mod_proxy`) that maps a local
      URL path to a remote backend server. For example,
      ``ProxyPass "/app" "http://backend:8080/app"``.

   ProxyPassReverse
      The :term:`directive` that adjusts the ``Location``,
      ``Content-Location``, and ``URI`` headers in responses from a
      :term:`reverse proxy` backend so that they point to the proxy server
      rather than the backend.

   RewriteRule
      The primary :term:`directive` of :term:`mod_rewrite`. It matches a
      :term:`regular expression` against the request URL and rewrites it
      to a new value. Supports numerous flags such as ``[R]`` (redirect),
      ``[L]`` (last), ``[PT]`` (passthrough), and ``[QSA]`` (query string
      append).

   RewriteCond
      A :term:`directive` that adds a condition to the following
      :term:`RewriteRule`. Conditions can test server variables, HTTP
      headers, file attributes, and more. Multiple RewriteCond directives
      are ANDed by default.

   RewriteMap
      A :term:`directive` that defines a mapping function for use in
      :term:`RewriteRule` substitutions. Supports text files, DBM files,
      external programs, SQL queries, and built-in functions such as
      ``tolower`` and ``escape``.

   SetHandler
      A :term:`directive` that forces all matching requests to be processed
      by the specified :term:`handler`. For example,
      ``SetHandler server-status``.

   AddHandler
      A :term:`directive` that associates a :term:`handler` with one or
      more file extensions. For example,
      ``AddHandler cgi-script .cgi .pl``.

   ErrorDocument
      The :term:`directive` that specifies a custom response for a given
      HTTP error code. For example,
      ``ErrorDocument 404 /custom_404.html``.

   LogFormat
      The :term:`directive` (from ``mod_log_config``) that defines a named
      log format string using percent-encoded variables. The format can
      then be referenced by :term:`CustomLog`.

   CustomLog
      The :term:`directive` that specifies the location and format of an
      access log file. For example,
      ``CustomLog /var/log/httpd/access_log combined``.

   ErrorLog
      The :term:`directive` that specifies the file to which the server
      writes diagnostic and error messages.

   LogLevel
      The :term:`directive` that controls the verbosity of the
      :term:`ErrorLog`. Levels range from ``emerg`` (most severe) to
      ``trace8`` (most verbose). Can be set globally or per module:
      ``LogLevel rewrite:trace3``.

   Include
      The :term:`directive` that incorporates other configuration files
      into the main configuration. Accepts glob patterns, e.g.,
      ``Include conf.d/*.conf``.

   Define
      The :term:`directive` that sets a configuration variable for use
      in ``${VARIABLE}`` substitutions and ``<IfDefine>`` tests throughout
      the configuration.

   <VirtualHost>
      A container :term:`directive` that encloses configuration for a
      :term:`virtual host`. Takes an address:port argument, e.g.,
      ``<VirtualHost *:80>``.

   <Directory>
      A container :term:`directive` that applies enclosed directives to
      the specified filesystem directory and its subdirectories.

   <Location>
      A container :term:`directive` that applies enclosed directives to
      requests matching the specified URL path. Processed after
      :term:`<Directory>` sections.

   <Files>
      A container :term:`directive` that applies enclosed directives to
      requests for files matching the specified name or pattern.

   <If>
      A container :term:`directive` (Apache httpd 2.4+) that encloses
      directives to be applied only when a runtime expression evaluates
      to true. Part of the :term:`expression parser`. For example,
      ``<If "%{HTTP_HOST} == 'example.com'">``.

   expression parser
      A runtime expression evaluation engine in Apache httpd 2.4+ that
      provides boolean, string comparison, and :term:`regular expression`
      operations. Used in :term:`<If>`, ``<ElseIf>``, ``<Else>``, and many
      directives that accept ``expr`` arguments.

   apachectl
      A front-end control script for the Apache httpd daemon. Supports
      commands such as ``start``, ``stop``, ``restart``,
      ``graceful`` (graceful restart), ``configtest``, and ``-S``
      (dump virtual host settings).

   htpasswd
      A command-line utility shipped with Apache httpd for creating and
      managing password files used by :term:`basic authentication`
      (``mod_authn_file``). Supports MD5, bcrypt, SHA, and crypt hashing.

   htdbm
      A command-line utility for managing :term:`DBM` password files used
      by ``mod_authn_dbm``. Offers the same hashing options as
      :term:`htpasswd` but stores credentials in a DBM database for
      faster lookups.

   htdigest
      A command-line utility for managing password files used by
      :term:`digest authentication` (``mod_auth_digest``).

   ab
      Apache Bench. A command-line :term:`benchmarking` tool shipped with
      Apache httpd for measuring the performance of an HTTP server. Usage:
      ``ab -n 1000 -c 10 http://localhost/``.

   benchmarking
      The process of measuring server performance under controlled
      conditions, typically using tools like :term:`ab`, ``siege``, or
      ``wrk``. Used to identify bottlenecks and validate tuning changes.

   rotatelogs
      A :term:`piped log` program shipped with Apache httpd that rotates
      log files based on time intervals or file size, without requiring a
      server restart.

   logresolve
      A utility shipped with Apache httpd that resolves IP addresses in
      log files to hostnames for post-processing analysis.

   apxs
      APache eXtenSion tool. A utility for building and installing
      :term:`module`\s as :term:`DSO`\s without recompiling the entire
      server. Typically provided by the ``httpd-devel`` or ``apache2-dev``
      package.

   a2enmod
      A Debian/Ubuntu utility that enables an Apache httpd :term:`module`
      by creating a symlink from ``mods-available/`` to ``mods-enabled/``.
      Its counterpart is ``a2dismod``.

   a2ensite
      A Debian/Ubuntu utility that enables a :term:`virtual host`
      configuration by creating a symlink from ``sites-available/`` to
      ``sites-enabled/``. Its counterpart is ``a2dissite``.

   DBM
      A family of simple key-value database file formats (GDBM, SDBM,
      NDBM, Berkeley DB). Apache httpd uses DBM files for faster
      lookups in password files, group files, and :term:`RewriteMap`
      definitions.

   mod_rewrite
      A powerful :term:`module` for rule-based URL rewriting using
      :term:`regular expression`\s. Provides :term:`RewriteRule`,
      :term:`RewriteCond`, and :term:`RewriteMap` directives. See
      :ref:`Chapter_mod_rewrite`.

   mod_ssl
      The :term:`module` that provides :term:`SSL` and :term:`TLS`
      support for Apache httpd. Configures certificates, cipher suites,
      :term:`OCSP` stapling, and related settings.

   mod_proxy
      The core :term:`module` for :term:`proxy` and :term:`reverse proxy`
      functionality. Works with protocol-specific sub-modules such as
      ``mod_proxy_http``, ``mod_proxy_fcgi``, ``mod_proxy_wstunnel``, and
      ``mod_proxy_balancer``.

   mod_headers
      A :term:`module` that allows you to set, append, merge, or remove
      HTTP request and response headers. For example,
      ``Header set X-Content-Type-Options "nosniff"``.

   mod_deflate
      A :term:`module` that compresses response content using the
      ``deflate`` (zlib) algorithm before sending it to the client,
      reducing bandwidth usage. See :ref:`Chapter_Filters_And_Handlers`.

   mod_brotli
      A :term:`module` that compresses response content using the Brotli
      algorithm, which typically achieves better compression ratios than
      :term:`mod_deflate` for text-based content.

   mod_expires
      A :term:`module` that controls the ``Expires`` and
      ``Cache-Control: max-age`` response headers, enabling client-side
      caching of static resources.

   mod_cache
      A :term:`module` that implements HTTP caching on the server side,
      storing responses for reuse. Works with backends such as
      ``mod_cache_disk`` and ``mod_cache_socache``.

   mod_alias
      The :term:`module` that provides the :term:`Alias`,
      :term:`Redirect`, :term:`RedirectMatch`, ``AliasMatch``,
      ``ScriptAlias``, and ``ScriptAliasMatch`` directives for simple URL
      mapping.

   mod_dir
      A :term:`module` that handles trailing-slash redirects and
      :term:`DirectoryIndex` lookups when a request maps to a directory.

   DirectoryIndex
      The :term:`directive` (from :term:`mod_dir`) that specifies the file
      or files to look for when a client requests a directory. Default is
      typically ``index.html``.

   mod_autoindex
      The :term:`module` that generates directory listings when no
      :term:`DirectoryIndex` file is found. Controlled by the ``Indexes``
      :term:`Options` value and the ``IndexOptions`` directive. See
      :ref:`Chapter_Directory_listing`.

   mod_negotiation
      The :term:`module` that implements :term:`content negotiation`,
      selecting the best resource variant based on client preferences for
      language, media type, and encoding.

   mod_mime
      The :term:`module` that maps file extensions to :term:`MIME type`\s,
      languages, handlers, and filters. Reads the ``mime.types``
      configuration file.

   mod_include
      The :term:`module` that processes :term:`SSI` directives in HTML
      files, enabling server-side dynamic content.

   mod_md
      Managed Domains. A :term:`module` that automates :term:`TLS`
      certificate provisioning and renewal using the :term:`ACME` protocol
      (e.g., :term:`Let's Encrypt`). Eliminates the need for external
      certificate management tools.

   mod_macro
      A :term:`module` that allows the definition and use of macros in
      Apache httpd configuration files, reducing repetition. For example,
      define a ``VHost`` macro once and ``Use`` it for each virtual host.

   mod_vhost_alias
      A :term:`module` for mass :term:`virtual host` configuration.
      Automatically maps hostnames to directories using
      ``VirtualDocumentRoot`` and ``VirtualScriptAlias`` directives,
      without individual ``<VirtualHost>`` blocks.

   mod_log_config
      The :term:`module` that provides the :term:`LogFormat` and
      :term:`CustomLog` directives for configuring access logs.

   mod_log_forensic
      A :term:`module` that logs a unique request ID both before and after
      request processing, allowing administrators to identify requests that
      caused a crash. Analyzed with the ``check_forensic`` tool.

   mod_setenvif
      A :term:`module` that sets :term:`environment variable`\s based on
      attributes of the request, such as headers, remote host, or
      :term:`URI`. Commonly used for conditional logging and browser-specific
      behavior.

   mod_security
      A widely-used third-party web application firewall (WAF) :term:`module`
      that inspects HTTP traffic and blocks malicious requests using
      configurable rules. See :ref:`Chapter_Security`.

   mod_substitute
      A :term:`module` that performs string or :term:`regular expression`
      substitutions on response bodies—useful for rewriting content from
      a :term:`reverse proxy` backend.

   mod_ext_filter
      A :term:`module` that allows any external program to act as an
      output :term:`filter`, processing response bodies before delivery
      to the client.

   mod_remoteip
      A :term:`module` that replaces the client IP address in the request
      with the value of a header such as ``X-Forwarded-For``, allowing
      accurate logging and access control when Apache httpd sits behind
      a :term:`reverse proxy` or load balancer.

   mod_status
      A :term:`module` that provides a real-time status page showing
      current server activity, including active connections, request
      processing times, and worker utilization. See
      :ref:`Chapter_info_and_status`.

   mod_info
      A :term:`module` that displays the complete server configuration—
      loaded modules, directives, and their settings—on a web page. Useful
      for debugging. See :ref:`Chapter_info_and_status`.

   mod_userdir
      A :term:`module` that maps ``~username`` URL paths to directories
      inside users' home directories, allowing individual users to publish
      web content. See :ref:`Chapter_userdir`.

   mod_speling
      A :term:`module` (yes, the name is intentionally misspelled) that
      corrects minor URL misspellings and case errors by searching for
      similarly named files on disk.

   mod_lua
      A :term:`module` that embeds the Lua programming language into
      Apache httpd, allowing request processing, authentication, and
      content generation to be scripted in Lua.

   URI
      Uniform Resource Identifier. A string that identifies a resource.
      A :term:`URL` is a specific type of URI that includes the access
      mechanism (scheme). In Apache httpd documentation, "URI" often refers
      to the path component of a request.

   URL
      Uniform Resource Locator. A :term:`URI` that specifies the scheme
      (e.g., ``http://``), host, port, path, and optional query string for
      a resource.

   status code
      A three-digit number returned in every :term:`HTTP` response
      indicating the result of the request. Categories: 1xx (informational),
      2xx (success), 3xx (redirection), 4xx (client error), 5xx (server
      error).

   APR
      Apache Portable Runtime. A set of cross-platform C libraries that
      provide a consistent interface to operating-system facilities such as
      file I/O, networking, memory management, and threads. Used internally
      by Apache httpd.

   PCRE
      Perl Compatible Regular Expressions. The :term:`regular expression`
      library used by Apache httpd. Its syntax is based on Perl 5 regex and
      is shared by many other tools and languages.

   systemd
      A system and service manager for Linux that manages the lifecycle of
      daemons including Apache httpd. The ``httpd.service`` unit provides
      ``start``, ``stop``, ``restart``, and ``reload`` commands.

   logrotate
      A Linux utility that rotates, compresses, and removes log files on
      a schedule. Commonly used to manage Apache httpd log files via a
      configuration in ``/etc/logrotate.d/``.

   chroot
      A Unix mechanism that changes the apparent root directory for a
      process, restricting its view of the filesystem. Can be used to
      sandbox Apache httpd for additional security.

   Brotli
      A compression algorithm developed by Google that typically provides
      better compression ratios than gzip/deflate for web content.
      Supported by :term:`mod_brotli`.
