========
Glossary
========

.. glossary::
   :sorted:

   Apache httpd
      The Apache HTTP Server, commonly referred to as Apache. An open-source,
      cross-platform web server maintained by the Apache Software Foundation.

   module
      A loadable component that extends the functionality of Apache httpd.
      Modules are loaded with the ``LoadModule`` directive.

   directive
      A configuration command in the Apache httpd configuration files.

   virtual host
      A method of hosting multiple websites on a single server, either
      by IP address or by hostname.

   MPM
      Multi-Processing Module. The component of Apache httpd responsible for
      binding to network ports, accepting requests, and dispatching them to
      child processes or threads. Examples include ``prefork``, ``worker``,
      and ``event``.

   .htaccess
      A per-directory configuration file that allows decentralized management
      of web server configuration. Parsed at request time when ``AllowOverride``
      permits it.

   SSL
      Secure Sockets Layer. The predecessor to TLS, providing encrypted
      communication between web browsers and servers.

   TLS
      Transport Layer Security. The modern successor to SSL for encrypting
      web traffic.

   CGI
      Common Gateway Interface. A protocol for web servers to execute
      external programs and return their output as web pages.

   SSI
      Server Side Includes. A simple server-side scripting language for
      including dynamic content in HTML pages.

   proxy
      A server that acts as an intermediary for requests from clients
      seeking resources from other servers.

   reverse proxy
      A proxy server that retrieves resources on behalf of a client from
      one or more backend servers. The resources are then returned to the
      client as if they originated from the proxy server itself.
