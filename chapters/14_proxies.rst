
.. _Chapter_Proxies:

=======
Proxies
=======

.. epigraph::

   Don't stand so close to me.

   -- The Police, *Don't Stand So Close to Me*


.. index:: Proxies

.. index:: Content proxying


Proxy means to act on behalf of another. In the context of a Web
server, this means one server fetching content from another server, then
returning it to the client. For example, you may have several Web servers
that hide behind a proxy server. The proxy server is responsible for
making sure requests go to the right backend server.

``mod_proxy``, which comes with
Apache HTTP Server, handles proxying behavior. The recipes in this chapter cover
various techniques that can be used to take advantage of this capability.
I discuss securing your proxy server, caching content proxied through
your server, and ways to use ``mod_proxy`` to map requests to services running
on alternate ports.

Additional information about ``mod_proxy`` can be found at
http://httpd.apache.org/docs/mod/mod_proxy.html.

Apache httpd has a number of submodules, such as ``mod_proxy_balancer``, which give additional
functionality to ``mod_proxy``. These
will be discussed in this chapter, too.

Please make sure that you don't enable proxying until you understand
the security concerns involved and have taken steps to secure your proxy
server. (See :ref:`Recipe_Securing-proxy` for
details.)

You also may wish to consider a dedicated proxy server, such as httpd
Traffic Server (http://trafficserver.apache.org/), Varnish
(https://varnish-cache.org/), or
Squid (http://www.squid-cache.org), which are focused
entirely on one task, and thus have more options related to this
task.


.. admonition:: Modules covered in this chapter

   :module:`mod_proxy`, :module:`mod_proxy_balancer`,
   :module:`mod_proxy_ftp`


.. _Recipe_Securing-proxy:

Securing Your Proxy Server
--------------------------


.. _Problem_Securing-proxy:

Problem
~~~~~~~


You want to enable proxying, but you don't want an open proxy
that can be used by just anyone.


.. _Solution_Securing-proxy:

Solution
~~~~~~~~


For proxy access control:


.. code-block:: text

   <Proxy *>
       Require host .yourdomain.com
   </Proxy>


.. _Discussion_Securing-proxy:

Discussion
~~~~~~~~~~


Running an open proxy is a concern because it permits Internet
users to use your proxy server to cover their tracks as they visit Web
sites. This can be a problem for a numbers of reasons. The user is
effectively stealing your bandwidth and is certainly part of the
problem. However, perhaps more concerning is the fact that you are
probably enabling people to circumvent restrictions that have been put
in place by their network administrators, or perhaps you are providing
users with anonymity while they visit a Web site, and as a
consequence, these visits appear to come from your network.

In these recipes, **``.yourdomain.com``**
should be replaced by the name of your particular domain, or, better
yet, the network address(es) that are on your network. (IP addresses
are harder to fake than host and domain names.) For example, rather
than the line appearing in the recipe, you might use a line such
as:

For example:


.. code-block:: text

   Require IP 192.168.1


Note that every request for resources that goes through your
proxy server generates a logfile entry, containing the address of the
client and the resource that she requested through your proxy server.
For example, one such request might look like:


.. code-block:: text

   192.168.1.5 - - [26/Feb/2003:21:26:13 -0500] "GET http://httpd.apache.org/docs/mod/
        mod_proxy.html HTTP/1.1" 200 49890


Your users, if made aware of this fact, will no doubt find it
invasive, because this will show all HTTP traffic through the proxy
server.

It is possible to configure your server not to log these
requests. To do this, you need to set an environment variable for
proxied requests:


.. code-block:: text

   <Directory proxy:*>
       SetEnv PROXIED 1
   </Directory>


Then, in your log directive, specify that these requests are not
        to be logged:


.. code-block:: text

   CustomLog /www/logs/access_log common env=!PROXIED


.. _See_Also_Securing-proxy:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_proxy.html
          
* http://httpd.apache.org/docs/mod/mod_log_config.html


.. _Preventing_Your_Proxy_Server_from_Being_Used_as_an_Open_id147710:

Preventing Your Proxy Server from Being Used as an Open Mail Relay
------------------------------------------------------------------


.. _Problem_id147725:

Problem
~~~~~~~


If your httpd is set up to operate as a proxy, it is
possible for it to be used as a mail relay unless precautions are
taken. This means that your system may be functioning as an "open
relay" even though your mail server software is securely
configured.


.. _Solution_id147773:

Solution
~~~~~~~~


Use ``mod_rewrite`` to forbid proxy requests to port 25 (SMTP):


.. code-block:: text

   <Directory proxy:*>
       RewriteEngine On
       RewriteRule "^proxy:[a-z]*://[^/]*:25(/|$)" "-" [F,NC,L]
   </Directory>


.. _Discussion_id147804:

Discussion
~~~~~~~~~~


To use the httpd proxy as an SMTP relay is fairly trivial, but
then so is preventing it. The solution simply tells the server to
respond with a ``403 Forbidden`` to any
attempts to use it to proxy to a remote mail server (port 25). Other
ports, such as HTTP (port 80), HTTPS (port 443), and FTP (ports 20 and
21), which are commonly permitted proxy access, will not be
affected.


.. _See_Also_id147905:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_proxy.html


          
* http://httpd.apache.org/docs/mod/core.html#directory


          
* http://httpd.apache.org/docs/mod/mod_rewrite.html


.. _Forwarding_Requests_to_Another_Server_id147962:

Forwarding Requests to Another Server
-------------------------------------


.. _Problem_id147977:

Problem
~~~~~~~


You want requests for particular URLs to be transparently
        forwarded to another server.


.. _Solution_id148030:

Solution
~~~~~~~~


Use **ProxyPass** and **ProxyPassReverse** directives in your
        **httpd.conf**:


.. code-block:: text

   ProxyPass /other/ http://other.server.com/
   ProxyPassReverse /other/ http://other.server.com/


.. _Discussion_id148089:

Discussion
~~~~~~~~~~


These directives will cause requests to URLs starting with
        **/other/** to be forwarded to the
        server **other.server.com**, with the path
        information preserved. That is to say, a request for
        **http://www.server.com/other/something.html** will
        be translated into a request for
        **http://other.server.com/something.html**. Content
        obtained from this other server will be returned to the client, who
        will be unable to determine that any such technique was employed. The
        **ProxyPassReverse** directive ensures
        that any redirect headers sent from the backend server (in this case,
        **other.server.com**) will be modified so that they
        appear to come from the main server.

This method is often used to have the dynamic portion of the
        site served by a server running ``mod_perl``—often even on the same machine,
        but on a different port—while the static portions of the site are
        served from the main server, which can be lighter weight, and so run
        faster.

Note that URLs contained within documents are not rewritten as
        they pass through the proxy, and links within documents should be
        relative, rather than absolute, so that they work correctly.
        ``mod_proxy_html`` can be used to do that.

Use this recipe when you have a frontend server and one or more
        backend servers, inaccessible from the Internet, and you wish to serve
        content from them. In the example given, when a request is made for a
        URL starting with ``/other/``, httpd
        makes a request for the URL
        **http://other.server.com**, and returns the content
        obtained by the client. For example, a request for the URL ``/other/example.html`` results in a request for
        the URL
        **http://other.server.com/example.html**.

The **ProxyPassReverse**
        directive ensures that any header fields returned by the secondary
        server (which contain the name of the server, such as ``Location`` headers) will be rewritten to
        contain the URL that the end user will actually be using, ensuring
        that the redirect actually functions as desired.

Note that links within HTML documents on the secondary site
        should all be relative, rather than absolute, so that these links work
        for users using the content **via** the proxy server. In the recipe given,
        for example, a link to **/index.html** removes the ``/other/`` portion of the URL, causing the
        request to no longer hit the proxied portion of the server.

Using this technique, you can have content for one Web site
        actually served by multiple Web server machines. This can be used as a
        means to traverse the border of your network, or it can be used as a
        load-sharing technique to lessen the burden on your primary Web
        server.


.. _See_Also_id148203:


See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_proxy.html


          
* :ref:`Distributing_Load_Evenly_Between_Several_Servers_id153837`


.. _Blocking_Proxied_Requests_to_Certain_Places_id148235:

Blocking Proxied Requests to Certain Places
-------------------------------------------


.. _Problem_id148250:

Problem
~~~~~~~


You want to use your proxy server as a content filter,
        forbidding requests to certain places.


.. _Solution_id148285:

Solution
~~~~~~~~


Use **ProxyBlock** in the
        **httpd.conf** to deny access to
        particular sites:


.. code-block:: text

   ProxyBlock forbiddensite.com www.competitor.com monster.com


.. _Discussion_id148340:

Discussion
~~~~~~~~~~


This example forbids proxied requests to the sites listed. These
        arguments are substring matches; ``example.com`` will also match ``www.example.com``, and an argument of ``example`` would match both.


.. code-block:: text

   ProxyBlock "*"


Will block all proxy requests.

If you want more fine-grained control of what content is
        requested through your proxy server, you may want to use something
        more sophisticated, such as Squid, which is more full-featured in that
        area.


.. _See_Also_id148381:

See Also
~~~~~~~~


* The Squid proxy server, found at http://www.squid-cache.org


.. _Proxying_mod_perl_Content_to_Another_Server_id148425:

Proxying mod_perl Content to Another Server
-------------------------------------------


.. _Problem_id148440:

Problem
~~~~~~~


You want to run a second HTTP server for dynamically generated
        content and have httpd transparently map requests for this content to
        the other server.


.. _Solution_id148476:

Solution
~~~~~~~~


First, install httpd, running on an alternate port, such as
        port 90, on which you will generate this dynamic content. Then, on
        your main server:


.. code-block:: text

   ProxyPass /dynamic/ http://localhost:90/
   ProxyPassReverse /dynamic/ http://localhost:90/


.. _Discussion_id148503:

Discussion
~~~~~~~~~~


Most dynamic content generation techniques use a great deal more
system resources than serving static content. This can slow down the
process of serving static content from the same server, because child
processes will be consumed with producing this dynamic content, and
thus unable to serve the static files.

By giving the dynamic content its own dedicated server, you
allow the static content to be served much more rapidly, and the
dynamic content has a dedicated server. Each server can have a smaller
set of modules installed than it would otherwise require because it'll
be performing a smaller subset of the functionality needed to do both
tasks.

This technique can be used for a ``mod_perl`` server, a PHP server, or any other
dynamic content method. Or you could reverse the technique and have,
for example, a dedicated machine for serving image files using
``mod_mmap_static`` to serve the
files very rapidly out of an in-memory cache.

In the example, all URLs starting with **/dynamic/** will be forwarded to the other
server, which will, presumably, handle only requests for dynamic
content. URLs that do not match this URL, however, will fall through
and be handled by the frontend server.


.. _See_Also_new8:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_proxy.html

* :ref:`Chapter_Dynamic_content`, **Dynamic Content**


.. _Configuring_a_Caching_Proxy_Server_id148610:

Configuring a Caching Proxy Server
----------------------------------


.. _Problem_id148624:

Problem
~~~~~~~


You want to run a caching proxy server.


.. _Solution_id148658:

Solution
~~~~~~~~


Configure your server to proxy requests and provide a location
        for the cached files to be placed:


.. code-block:: text

   ProxyRequests on
   CacheRoot /var/spool/httpd/proxy


.. _Discussion_id148683:

Discussion
~~~~~~~~~~


Running a caching proxy server allows users on your network to
have more rapid access to content that others have already requested.
They will perhaps not be getting the most recent version of the
document in question, but since they are retrieving the content from a
local copy rather than from the remote Web server, they will get it
much more quickly.

With the contents of the WWW growing ever more dynamic, running
a caching proxy server perhaps makes less sense than it once did, when
most of the Web was composed of static content. However, because
``mod_proxy`` is fairly smart about
what it caches and what it does not cache, this sort of setup will
still speed things up by caching the static portions of documents,
such as the image files, while retrieving the most recent version of
those documents that change over time.

The directory specified in the **CacheRoot** directive specifies where cached
content will be stored. This directory must be writable by the user
that httpd is running as (typically nobody), so that it is able to
store these files there.


.. _See_Also_id148807:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_proxy.html


.. _Filtering_Proxied_Content_id148839:


Filtering Proxied Content
-------------------------


.. _Problem_id148853:

Problem
~~~~~~~


You want to apply some filter to proxied content, such as
altering certain words.


.. _Solution_id148910:

Solution
~~~~~~~~


Use ``mod_ext_filter`` to create output filters to
apply to content before it is sent to the user:


.. code-block:: text

   ExtFilterDefine usehttpd mode=output \
       intype=text/html cmd="/bin/sed s/8080/80/g"
   
   <Proxy *>
       SetOutputFilter usehttpd
   </Proxy>


.. _Discussion_id148942:

Discussion
~~~~~~~~~~


The recipe offered is a very simple-minded "usehttpd"
filter, replacing the Apache Tomcat default port with
Apache httpd one.
This could be expanded to a variety of more
sophisticated content modification, because the **cmd** argument can be any command line, such
as a Perl script, or arbitrary program, which can filter the content
in any way you want. All proxied content will be passed through this
filter before it is delivered to the client.

Note also that there are ethical and legal issues surrounding
techniques like these, which you may need to deal with. I don't
presume to take a position on any of them. In particular, modifying
proxied content that does not belong to you may be a violation of the
owner's copyright and may be considered by some to be unethical.
Thankfully, this is just a technical book, not a philosophical one. I
can tell you how to do it, but whether you should is left to your
conscience and your lawyers.


.. _See_Also_id149076:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_proxy.html

* http://httpd.apache.org/docs/mod/mod_ext_filter.html

* :ref:`Recipe_mod_ext_filter`


.. _Requiring_Authentication_for_a_Proxied_Server_id149122:

Requiring Authentication for a Proxied Server
---------------------------------------------


.. _Problem_id149136:

Problem
~~~~~~~


You wish to proxy content from a server, but it requires a login
and password before content may be served from this proxied
site.


.. _Solution_id149171:

Solution
~~~~~~~~


Use standard authentication techniques to require logins for proxied content:

.. code-block:: apache

   ProxyPass "/secretserver/" "http://127.0.0.1:8080"
   <Directory "proxy:http://127.0.0.1:8080/">
       AuthName SecretServer
       AuthType Basic
       AuthUserFile /path/to/secretserver.htpasswd
       Require valid-user
   </Directory>


.. _Discussion_id149206:

Discussion
~~~~~~~~~~


This technique can be useful if you are running some sort of
        special-purpose or limited-function Web server on your system, but you
        need to apply httpd's rich set of access control and its other
        features to access it. This is done by using the **ProxyPass** directive to make the
        special-purpose server's URI space part of your main server, and using
        the special ``proxy``:**``path``**
        **&lt;Directory&gt;** container syntax
        to apply httpd settings only to the mapped URIs.


.. _See_Also_id149271:

See Also
~~~~~~~~


* :ref:`Recipe_htpasswd`


.. _Recipe_mod_proxy_balancer:

Load Balancing with mod_proxy_balancer
--------------------------------------


.. _Problem_mod_proxy_balancer:

Problem
~~~~~~~


You want to balance the load between several backend servers.


.. _Solution_mod_proxy_balancer:

Solution
~~~~~~~~


Use ``mod_proxy_balancer`` to
        create a load-balanced cluster:


.. code-block:: text

       <Proxy balancer://mycluster>
           BalancerMember http://192.168.1.50:80 
           BalancerMember http://192.168.1.51:80
       </Proxy>
       ProxyPass /application balancer://mycluster/


.. _Discussion_mod_proxy_balancer:

Discussion
~~~~~~~~~~


``mod_proxy_balancer`` is a
module that provides load balancing between multiple
backend servers. This kind of functionality has traditionally been
associated with expensive and complex commercial solutions. This
module makes this simple to configure, and it's included in the
standard installation of httpd.

The example given above sets up a two-member balanced cluster
and proxies the URL ``/application`` to
that cluster.

``mod_proxy_balancer`` offers a
wide variety of options, which you can find in detail in the
documentation, available here: http://httpd.apache.org/docs/current/mod/mod_proxy_balancer.html.

For example, you can indicate that a particular server is more
powerful than another, and so should be allowed to assume more of the
load than other machines in the cluster. In the following
configuration line, the configuration indicates that one particular machine should
receive twice as much traffic as other machines:


.. code-block:: text

       BalancerMember http://192.168.1.51:80 loadfactor=2


Traffic may be balanced by traffic (bytes transferred) or by
        request (number of requests made per host) by putting additional
        arguments on the **ProxyPass**
        directive:


.. code-block:: text

       ProxyPass /application balancer://mycluster/ lbmethod=bytraffic


See the ``mod_proxy``
        documentation for more information on this point.

And there is a Web-based balancer manager tool, which can be
        configured as follows:


.. code-block:: text

   <Location /balancer-manager>
       SetHandler balancer-manager
   </Location>


The balancer manager lets you set servers available or
        unavailable, and change their load factor, without restarting the
        server. This allows you to take servers offline for maintenance, do
        whatever needs to be done, and bring them back up, without ever
        affecting the end user.


.. _See_Also_mod_proxy_balancer:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/curremt/mod/mod_proxy_balancer.html


.. _I_sect110_d1e16904:

Proxied Virtual Host
--------------------


Problem
~~~~~~~


You want to have an entire virtual host proxied to a different
        server.


Solution
~~~~~~~~


Place a **ProxyPass** directive
        in your **VirtualHost** configuration
        block:


.. code-block:: text

   <VirtualaHost *:80>
       ServerName server2.example.com
       ProxyPass / http://192.168.1.52:80
       ProxyPassReverse / http://192.168.1.52:80
   </VirtualHost>


Discussion
~~~~~~~~~~


This recipe will pass all requests to this virtual host to the
specified backend server and serve the content from there. The
**ProxyPassReverse** directive ensures
that redirects issued from the backend server will be correctly
rewritten to the front-end server, rather than having clients try to
request content directly from the backend server.

It can be useful to collect logfiles on the frontend server,
rather than on the backend server. Requests to the backend server will
appear to come from the proxy server, rather than from the original
client address. However, logfiles collected on the proxy (frontend) server will have the original
client address.


See Also
~~~~~~~~


* http://httpd.apache.org/docs/current/mod/mod_proxy.html


.. _Recipe_dont_proxy_certain_files:

Refusing to proxy certain file types or certain URLs
----------------------------------------------------


.. _Problem_dont_proxy_certain_files:

Problem
~~~~~~~


You don't want people using your proxy server to access
particular URLs or patterns of URLs (such as MP3 or streaming video
files) or certain download sites.


.. _Solution_dont_proxy_certain_files:

Solution
~~~~~~~~


You can block by hostname using a portion of the hostname:


.. code-block:: text

   # Don't allow anyone to access .mil sites through us
   ProxyBlock .mil


You can block by specific backend URLs:

For example:

.. code-block:: apache

   # Don't allow anyone to access to http://other-host.org/path
   <Directory proxy:http://other-host.org/path>
       Require all denied
   </Directory>

Or you can block according to regular expression pattern matching:


.. code-block:: text

   <Directory proxy:*>
       RewriteEngine On
       #
       # Disable proxy access to movies and audio files
       #
       RewriteRule "\.(avi|mp4|mp3)$" "-" [F,NC]
       #
       # Don't allow anyone to access .mil sites through us
       #
       RewriteRule "^[a-z]+://[-.a-z0-9]*\.mil($|/)" "-" [F,NC]
   </Directory>


.. _Discussion_dont_proxy_certain_files:

Discussion
~~~~~~~~~~


All of these solutions will result in a client that attempts to
access a blocked URL receiving a
``403 Forbidden`` status from the
server.

The first solution uses a feature built into the proxy module
itself: the **ProxyBlock** directive.
It's simple and efficient; however, the
pattern matching it can perform is extremely limited and prone to
confusion. For instance, if you specify:


.. code-block:: text

   ProxyBlock .mil


the server denies access to both http://www.navy.mil/ and http://example.milles.com/. This might not be what was intended!

The second method allows you to impose limitations based on the
URL being fetched (or gateway, in the case of a **ProxyPass** directive).

The third method, which allows more complex what-to-block
patterns to be constructed, is both more flexible and more powerful,
and somewhat less efficient. Use it only when the other methods prove
insufficient.


.. _apacheckbk-CHP-6-NOTE-99:


.. tip::

   **&lt;ProxyMatch&gt;**
   containers work as well, so more complex patterns may be
   used.


The flags to the **RewriteRule**
directive tell it, first, that any URL matching the pattern should
result in the server returning a ``403 Forbidden`` error (``F`` or
forbidden), and second that the pattern match is case-insensitive
(``NC`` or nocase).

One disadvantage of the ``mod_rewrite`` solution is that it can be too
specific. The first **RewriteRule**
pattern can be defeated if the client specifies path-info or a query
string, or if the origin server uses a different suffix naming scheme
for these types of files. A little cleverness on your part can cover
these sorts of conditions, but beware of trying to squeeze too many
possibilities into a single regular expression pattern. It's generally
better to have multiple **RewriteRule**
directives than to have a single all-singing all-dancing one that no one can read—and
is, hence, prone to error.


.. _See_Also_dont_proxy_certain_files:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_proxy.html

* http://httpd.apache.org/docs/mod/mod_rewrite.html


.. _I_sect110_d1e16958:

Refusing to Proxy FTP
---------------------


Problem
~~~~~~~


You want to make sure that FTP (or, perhaps, other protocols)
        are not proxied through your server.


Solution
~~~~~~~~


Make sure that ``mod_proxy_ftp`` isn't loaded:


.. code-block:: text

   # LoadModule proxy_ftp_module modules/mod_proxy_ftp.so


Discussion
~~~~~~~~~~


``mod_proxy`` has several
helper modules that provide the protocol-specific proxying
functionality. These modules are ``mod_proxy_http``, for proxying HTTP requests;
``mod_proxy_ftp``, for proxying FTP
requests; and ``mod_proxy_connect``,
for support for the ``CONNECT`` HTTP
method, used primarily for tunneling SSL requests through proxy
servers.

If you want ``mod_proxy`` to
never proxy FTP requests, you need merely to ensure that the **LoadModule** directive for ``mod_proxy_ftp`` is commented out, as shown
above.


See Also
~~~~~~~~


* http://httpd.apache.org/docs/current/mod/mod_proxy_ftp.html
          
* http://httpd.apache.org/docs/current/mod/mod_proxy.html


.. _Recipe_mod_proxy_html:

Rewriting proxied HTLM contents
-------------------------------


.. _Problem_mod_proxy_html:

Problem
~~~~~~~


You want to rewrite HTML links in page contents like
**ProxyPassReverse** does for the HTTP headers.


.. _Solution_mod_proxy_html:

Solution
~~~~~~~~


Use ``mod_proxy_html`` togother with  **ProxyPass** and **ProxyPassReverse** directives
your **httpd.conf**:


.. code-block:: text

   ProxyPass /other/ http://other.server.com/
   ProxyPassReverse /other/ http://other.server.com/
   ProxyHTMLEnable On
   ProxyHTMLURLMap  http://other.server.com /other


.. _Discussion_mod_proxy_html:

Discussion
~~~~~~~~~~


As described previously in :ref:`Forwarding_Requests_to_Another_Server_id147962`
The **ProxyPass** and **ProxyPassReverse** will forward requests URLs starting with
**/other/** to to the server **other.server.com**, **ProxyHTMLURLMap** will rewrite
any HTML links containing **http://other.server.com** to **other**.
``mod_sed`` can also be used to filter page contents.


.. _See_Also_mod_proxy_html:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/current/mod/mod_proxy_html.html
          
* http://httpd.apache.org/docs/current/mod/mod_sed.html


.. _Recipe_mod_proxy_h2:

Proxying HTTP/2 requests to HTTP/1.1 backend servers.
-----------------------------------------------------


.. _Problem_mod_proxy_h2:

Problem
~~~~~~~


You want to use HTTP/2 in Apache httpd but your backend server can do only
HTTP/1.1.


.. _Solution_mod_proxy_h2:

Solution
~~~~~~~~


Use _mod_http2_ and _mod_proxy_ to convert HTTP/2 to HTTP/1.1, HTTP/2
from browsers requires _mod_ssl_ and a valid SSL configuration.
See :ref:`Chapter_SSL_and_TLS` for the detail of the SSL configurations. in
your **httpd.conf** configuration file:


.. code-block:: text

   <VirtualHost _default_:443>
   
      Protocols h2 http/1.1
      ProtocolsHonorOrder on
      SSLEngine on
      SSLCertificateFile /www/conf/ssl/ssl.crt
      SSLCertificateKeyFile /www/conf/ssl/ssl.key
   
      ServerName secure.example.com
   
      ProxyPass "/" "http://other.server.com/"
   
   </VirtualHost>


.. _Discussion_mod_proxy_h2:

Discussion
~~~~~~~~~~


Let's see what this configuration does:
With **Protocols** and **ProtocolsHonorOrder**, Apache HTTPD is told to use HTTP/2
for the **VirtualHost**.
With the **ProxyPass** directive, Apache httpd is told to forward the requests to the HTTP/1.1
server **other.server.com**. Apache httpd will demultiplex and decode the HTTP/1.1 
that are in the HTTP/2 stream.


.. _See_Also_mod_proxy_h2:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/current/howto/http2.html

.. admonition:: DRAFT — Review needed

   The following recipe was auto-generated and needs editorial review.
   Check technical accuracy, voice/tone, and fit with surrounding content.

.. _Recipe_proxy_ajp:

Connecting to Tomcat via AJP (mod_proxy_ajp)
--------------------------------------------

.. index:: mod_proxy_ajp
.. index:: AJP
.. index:: Tomcat
.. index:: Java application server

.. _Problem_Recipe_proxy_ajp:

Problem
~~~~~~~


You want to proxy requests from Apache httpd to an Apache Tomcat application server using the AJP protocol.


.. _Solution_Recipe_proxy_ajp:

Solution
~~~~~~~~


Enable :module:`mod_proxy` and :module:`mod_proxy_ajp`, then use
``ProxyPass`` with the ``ajp://`` scheme to forward requests to Tomcat's
AJP connector (default port 8009):

.. code-block:: apache

   LoadModule proxy_module       modules/mod_proxy.so
   LoadModule proxy_ajp_module   modules/mod_proxy_ajp.so

   ProxyPass        "/app" "ajp://backend.example.com:8009/app"
   ProxyPassReverse "/app" "http://backend.example.com/app"

Starting with Tomcat 8.5.51 and 9.0.31, AJP connections require a
shared secret. Pass it as a parameter on the ``ProxyPass`` line
(available in Apache HTTP Server 2.4.42 and later):

.. code-block:: apache

   ProxyPass "/app" "ajp://backend.example.com:8009/app" secret=YourSharedSecret

To balance across multiple Tomcat instances, combine
:module:`mod_proxy_balancer` with AJP workers:

.. code-block:: apache

   <Proxy "balancer://tomcat-cluster">
       BalancerMember "ajp://app1.example.com:8009" loadfactor=1
       BalancerMember "ajp://app2.example.com:8009" loadfactor=2
       ProxySet lbmethod=bytraffic
   </Proxy>

   ProxyPass        "/app" "balancer://tomcat-cluster/app"
   ProxyPassReverse "/app" "http://www.example.com/app"


.. _Discussion_Recipe_proxy_ajp:

Discussion
~~~~~~~~~~


The Apache JServ Protocol (AJP) is a binary protocol designed
specifically for communication between a front-end web server and a Java
application server such as Apache Tomcat. Compared with proxying over
HTTP, AJP is more efficient in several ways:

* **Binary encoding.** Common HTTP headers are encoded as short integer
  tokens rather than full strings, reducing bandwidth and parsing
  overhead.

* **Persistent connections.** AJP reuses TCP connections across
  requests, which avoids the overhead of creating a new connection for
  every request.

* **Client metadata forwarding.** AJP natively passes the client's IP
  address, SSL status, and other metadata to the backend, eliminating
  the need for ``X-Forwarded-For`` or ``X-Forwarded-Proto`` headers.

**The ``secret`` parameter.** Modern versions of Tomcat require AJP
connections to present a shared secret (the ``requiredSecret`` attribute
in Tomcat's ``server.xml``). Without a matching ``secret`` parameter on
the ``ProxyPass`` line, Tomcat will reject the connection with a 403
error. This is a security measure to prevent unauthorized services from
connecting to the AJP port.

**When to use AJP vs. HTTP proxying.** AJP is the traditional choice
when both servers are on the same network or the same host, and you want
the most efficient communication path. However, if your backend is
remote or if you need to proxy through an intermediate network that
inspects HTTP traffic, proxying over HTTP (or HTTP/2) may be simpler
because it does not require special port configuration or firewall rules
for the AJP port.

.. warning::

   The AJP port (8009 by default) should **never** be exposed to the
   public Internet. AJP does not encrypt traffic — it trusts that the
   front-end server has already handled TLS termination and access
   control. Always firewall the AJP port so that only the Apache
   front-end can reach it.

Note that ``ProxyPassReverse`` is usually not needed with AJP, because
the original ``Host`` header is forwarded to Tomcat and Tomcat generates
self-referential URLs relative to that host. The exception is when the
URL path on the proxy differs from the path on the backend — for example,
if you expose ``/apps/foo`` on the proxy but the Tomcat application is
deployed at ``/foo``.


.. _See_Also_Recipe_proxy_ajp:

See Also
~~~~~~~~


* https://httpd.apache.org/docs/current/mod/mod_proxy_ajp.html


.. admonition:: DRAFT — Review needed

   The following recipe was auto-generated and needs editorial review.
   Check technical accuracy, voice/tone, and fit with surrounding content.

.. _Recipe_proxy_http2_backend:

HTTP/2 backend proxy connections (mod_proxy_http2)
--------------------------------------------------

.. index:: mod_proxy_http2
.. index:: HTTP/2 backend
.. index:: Proxy HTTP/2

.. _Problem_Recipe_proxy_http2_backend:

Problem
~~~~~~~


You want your reverse proxy to communicate with backend servers over HTTP/2 for improved multiplexing and performance.


.. _Solution_Recipe_proxy_http2_backend:

Solution
~~~~~~~~


Enable :module:`mod_proxy` and :module:`mod_proxy_http2`, then use the
``h2://`` (TLS) or ``h2c://`` (cleartext) scheme in your ``ProxyPass``
directive:

.. code-block:: apache

   LoadModule proxy_module        modules/mod_proxy.so
   LoadModule proxy_http2_module  modules/mod_proxy_http2.so

   # HTTP/2 over TLS to the backend
   ProxyPass        "/app" "h2://backend.example.com"
   ProxyPassReverse "/app" "https://backend.example.com"

For backends that speak cleartext HTTP/2:

.. code-block:: apache

   # HTTP/2 cleartext to the backend
   ProxyPass        "/app" "h2c://backend.example.com"
   ProxyPassReverse "/app" "http://backend.example.com"

Note that the ``ProxyPassReverse`` directive still uses the standard
``https://`` or ``http://`` scheme — the ``h2://`` and ``h2c://`` schemes
are used only in ``ProxyPass`` to tell Apache which protocol to speak
with the backend.


.. _Discussion_Recipe_proxy_http2_backend:

Discussion
~~~~~~~~~~


:module:`mod_proxy_http2` allows Apache's reverse proxy to speak HTTP/2
to backend servers, which can improve performance through multiplexed
streams and header compression. This is independent of the protocol used
between the client and Apache — the front-end connection can be HTTP/1.1
or HTTP/2.

**Key characteristics:**

* **No HTTP/1.1 fallback.** Unlike a browser, :module:`mod_proxy_http2`
  does *not* fall back to HTTP/1.1 if the backend does not support
  HTTP/2. The backend must speak HTTP/2. If it doesn't, the connection
  will fail.

* **Connection reuse.** When multiple front-end requests are proxied to
  the same backend, :module:`mod_proxy_http2` attempts to reuse a single
  TCP connection using HTTP/2 multiplexing. However, each HTTP/1.1
  front-end request currently maps to a separate HTTP/2 request — they
  are not consolidated into streams on a shared connection.

* **Experimental status.** The module is marked experimental. Its
  directives and behavior may change between releases. Check the
  CHANGES file when upgrading.

**When to use h2:// vs. h2c://:**

Use ``h2://`` (HTTP/2 over TLS) when the backend requires encrypted
connections or when proxying across a network boundary. Use ``h2c://``
(cleartext HTTP/2) when the backend is on the same host or on a trusted
internal network where encryption is unnecessary.

**Interaction with front-end HTTP/2.** You can serve clients over HTTP/2
(using :module:`mod_http2` and the ``Protocols`` directive) *and*
separately proxy to backends over HTTP/2 using :module:`mod_proxy_http2`.
These are independent — you can use either or both.

.. note::

   :module:`mod_proxy_http2` relies on the ``libnghttp2`` library for
   its HTTP/2 engine. Ensure this library is installed and that Apache
   was built with HTTP/2 support.


.. _See_Also_Recipe_proxy_http2_backend:

See Also
~~~~~~~~


* https://httpd.apache.org/docs/current/mod/mod_proxy_http2.html


.. admonition:: DRAFT — Review needed

   The following recipe was auto-generated and needs editorial review.
   Check technical accuracy, voice/tone, and fit with surrounding content.

.. _Recipe_proxy_hcheck:

Health checking proxy backends (mod_proxy_hcheck)
-------------------------------------------------

.. index:: mod_proxy_hcheck
.. index:: Health check
.. index:: Backend health
.. index:: Proxy health checking

.. _Problem_Recipe_proxy_hcheck:

Problem
~~~~~~~


You want Apache httpd to periodically verify that backend servers are healthy before forwarding requests to them.


.. _Solution_Recipe_proxy_hcheck:

Solution
~~~~~~~~


Enable :module:`mod_proxy`, :module:`mod_proxy_balancer`, and
:module:`mod_proxy_hcheck`, then add health-check parameters to your
``BalancerMember`` directives:

.. code-block:: apache

   LoadModule proxy_module         modules/mod_proxy.so
   LoadModule proxy_balancer_module modules/mod_proxy_balancer.so
   LoadModule proxy_http_module    modules/mod_proxy_http.so
   LoadModule proxy_hcheck_module  modules/mod_proxy_hcheck.so
   LoadModule watchdog_module      modules/mod_watchdog.so

   # Define a condition: accept 2xx/3xx/4xx status as healthy
   ProxyHCExpr ok234 {%{REQUEST_STATUS} =~ /^[234]/}

   <Proxy "balancer://myapp">
       BalancerMember "http://app1.example.com/" hcmethod=HEAD hcexpr=ok234 hcinterval=10
       BalancerMember "http://app2.example.com/" hcmethod=HEAD hcexpr=ok234 hcinterval=10
       BalancerMember "http://app3.example.com/" hcmethod=TCP  hcinterval=5 hcpasses=2 hcfails=3
   </Proxy>

   ProxyPass        "/" "balancer://myapp/"
   ProxyPassReverse "/" "balancer://myapp/"


.. _Discussion_Recipe_proxy_hcheck:

Discussion
~~~~~~~~~~


:module:`mod_proxy_hcheck` performs health checks independently of
client traffic — even if no requests are being proxied, the module
periodically tests each backend worker and takes unhealthy workers out
of rotation.

**Health check methods.** The ``hcmethod`` parameter selects the type of
check:

* ``TCP`` — Verify that a TCP connection to the backend can be
  established. This is the lightest check: it confirms the server is
  reachable and the port is open, but does not verify that the
  application is working.

* ``HEAD`` — Send an HTTP ``HEAD`` request and evaluate the response
  status. This confirms the application is responding to HTTP requests
  without transferring a response body.

* ``GET`` — Send an HTTP ``GET`` request. This is necessary if your
  health-check expression needs to inspect the response body (see
  below). Use the ``hcuri`` parameter to target a lightweight status
  page rather than an expensive application endpoint.

* ``OPTIONS`` — Send an HTTP ``OPTIONS`` request. Useful for backends
  that implement an ``OPTIONS`` handler for health checking.

**Check frequency and thresholds.** ``hcinterval`` sets the number of
seconds between checks (default 30). ``hcfails`` sets how many
consecutive failures are required before the worker is disabled
(default 1). ``hcpasses`` sets how many consecutive successes are
required before a disabled worker is re-enabled (default 1). Setting
``hcpasses`` and ``hcfails`` to values greater than 1 avoids flapping
when a backend is unstable.

**Response expressions.** The ``ProxyHCExpr`` directive defines named
expressions that evaluate the backend's response. The expression can
check headers via standard httpd expression syntax, or inspect the
response body using the ``hc('body')`` function:

.. code-block:: apache

   # Disable the backend if the status page says "Under maintenance"
   ProxyHCExpr in_maint {hc('body') !~ /Under maintenance/}

   <Proxy "balancer://myapp">
       BalancerMember "http://app1.example.com/" hcmethod=GET hcexpr=in_maint hcuri=/status.php hcinterval=30
   </Proxy>

.. warning::

   Health check expressions that inspect the response body
   (``hcmethod=GET`` with ``hc('body')``) consume more resources than
   ``HEAD`` or ``TCP`` checks. Always target a small, purpose-built
   status endpoint via ``hcuri`` rather than a full application page.

**Templates.** If you have many workers with the same check parameters,
use ``ProxyHCTemplate`` to define a reusable set of defaults:

.. code-block:: apache

   ProxyHCTemplate fast_tcp hcmethod=TCP hcinterval=5 hcpasses=2 hcfails=3

   <Proxy "balancer://myapp">
       BalancerMember "http://app1.example.com/" hctemplate=fast_tcp
       BalancerMember "http://app2.example.com/" hctemplate=fast_tcp
   </Proxy>

**Thread pool.** Health checks run in a dedicated thread pool managed by
the ``mod_watchdog`` module. The ``ProxyHCTPsize`` directive controls
the number of threads in this pool (default 16). For large deployments
with many workers, increase this value so that checks can run in
parallel.

.. note::

   :module:`mod_proxy_hcheck` requires :module:`mod_watchdog`, which
   provides the periodic task infrastructure. On most distributions
   ``mod_watchdog`` is built by default but may not be loaded — make
   sure to load it explicitly.


.. _See_Also_Recipe_proxy_hcheck:

See Also
~~~~~~~~


* https://httpd.apache.org/docs/current/mod/mod_proxy_hcheck.html



.. admonition:: DRAFT — Review needed

   The following recipe was auto-generated and needs editorial review.
   Check technical accuracy, voice/tone, and fit with surrounding content.

.. _Recipe_mod_proxy_fcgi:

Proxying PHP and Other FastCGI Applications with mod_proxy_fcgi
---------------------------------------------------------------

.. index:: mod_proxy_fcgi
.. index:: PHP-FPM
.. index:: FastCGI
.. index:: ProxyPassMatch


.. _Problem_mod_proxy_fcgi:

Problem
~~~~~~~


You want to run PHP (or another FastCGI application) as a separate
process and have Apache forward requests to it, rather than embedding
the interpreter inside the web server process with ``mod_php``.


.. _Solution_mod_proxy_fcgi:

Solution
~~~~~~~~


Enable :module:`mod_proxy` and :module:`mod_proxy_fcgi`, then configure
Apache to forward PHP requests to a PHP-FPM pool.

There are three common approaches. Choose the one that best fits your
deployment.

**Approach 1: ProxyPassMatch (regex-based, traditional)**

.. code-block:: apache

   LoadModule proxy_module       modules/mod_proxy.so
   LoadModule proxy_fcgi_module  modules/mod_proxy_fcgi.so

   # Match any request ending in .php and forward it to PHP-FPM
   # listening on TCP port 9000
   ProxyPassMatch "^/(.*\.php(/.*)?)$" "fcgi://127.0.0.1:9000/var/www/html/$1"

**Approach 2: SetHandler with Unix Domain Socket (recommended)**

.. code-block:: apache

   LoadModule proxy_module       modules/mod_proxy.so
   LoadModule proxy_fcgi_module  modules/mod_proxy_fcgi.so

   # Forward .php requests to PHP-FPM via a Unix domain socket
   <FilesMatch "\.php$">
       SetHandler "proxy:unix:/run/php/php-fpm.sock|fcgi://localhost"
   </FilesMatch>

   # Ensure the DirectoryIndex includes index.php
   DirectoryIndex index.php index.html

**Approach 3: ProxyPass to a defined worker (best for connection reuse)**

.. code-block:: apache

   LoadModule proxy_module       modules/mod_proxy.so
   LoadModule proxy_fcgi_module  modules/mod_proxy_fcgi.so

   # Define a worker for connection pooling
   <Proxy "fcgi://localhost/" enablereuse=on max=10>
   </Proxy>

   <FilesMatch "\.php$">
       SetHandler "proxy:fcgi://localhost/"
   </FilesMatch>

A matching PHP-FPM pool configuration (:file:`/etc/php-fpm.d/www.conf`
or :file:`/etc/php/8.x/fpm/pool.d/www.conf`) would look like this:

.. code-block:: ini

   [www]
   user = www-data
   group = www-data

   ; Use a Unix domain socket (matches Approach 2 above)
   listen = /run/php/php-fpm.sock
   listen.owner = www-data
   listen.group = www-data
   listen.mode = 0660

   ; Or use TCP (matches Approaches 1 and 3 above)
   ; listen = 127.0.0.1:9000

   pm = dynamic
   pm.max_children = 50
   pm.start_servers = 5
   pm.min_spare_servers = 5
   pm.max_spare_servers = 35


.. _Discussion_mod_proxy_fcgi:

Discussion
~~~~~~~~~~


The shift from ``mod_php`` (which embeds the PHP interpreter inside every
Apache process) to PHP-FPM via :module:`mod_proxy_fcgi` has been the
single largest change in how PHP is deployed with Apache. PHP-FPM runs
as a separate process manager, which brings several advantages:

* **MPM freedom.** ``mod_php`` requires the ``prefork`` MPM because
  the PHP interpreter is not thread-safe on most platforms. With
  PHP-FPM, you can use the ``event`` or ``worker`` MPMs, which handle
  concurrent connections far more efficiently.

* **Resource isolation.** PHP-FPM processes are separate from Apache
  child processes. A runaway PHP script won't consume an Apache worker
  indefinitely.

* **Multiple PHP versions.** You can run different PHP-FPM pools (each
  with a different PHP version) and route virtual hosts to the
  appropriate pool.


Understanding the Three URL Syntaxes
------------------------------------

:module:`mod_proxy_fcgi` supports three URL forms, each with different
trade-offs:

``fcgi://hostname:port/path``
    The TCP form. Apache connects to PHP-FPM over a TCP socket.
    Works across network boundaries (e.g., PHP-FPM on a different host)
    but has slightly more overhead than a Unix socket.

``unix:/path/to/socket|fcgi://localhost/``
    The Unix Domain Socket (UDS) form, available since version 2.4.9.
    Apache connects to PHP-FPM through a local socket file. This is
    faster and more secure than TCP because the connection never
    leaves the machine, and file permissions control access to the
    socket. The hostname after ``fcgi://`` is ignored when using UDS
    syntax — ``localhost`` is conventional.

    :version: 2.4.9

``ProxyPassMatch`` with ``fcgi://``
    Regex-based routing. This lets you match specific URL patterns (such
    as ``\.php$``) and construct the backend path using captured groups.
    Useful when you need fine-grained control over which requests are
    forwarded. However, the ``$1`` backreference in the URL means each
    request produces a unique backend URL, which historically prevented
    connection reuse. Since version 2.4.47, parameters like
    ``enablereuse=on`` are honored with backreferences, though the
    default remains ``enablereuse=off`` for backward compatibility.

    :version: 2.4.47 (parameters honored with backreferences)


SetHandler vs. ProxyPassMatch
-----------------------------

The ``SetHandler`` approach (Approaches 2 and 3) is generally preferred
over ``ProxyPassMatch`` for several reasons:

* Apache resolves the filename on disk *before* forwarding the request,
  so ``SCRIPT_FILENAME`` and ``PATH_INFO`` are set accurately. With
  ``ProxyPassMatch``, you must construct the filesystem path yourself
  in the substitution string, which can lead to subtle PATH_INFO errors.

* ``SetHandler`` works inside ``<FilesMatch>``, ``<Directory>``, and
  :file:`.htaccess` contexts, giving you fine-grained per-directory
  control.

* With a defined ``<Proxy>`` worker (Approach 3), Apache can pool and
  reuse connections to PHP-FPM, improving performance under load.


Connection Reuse
----------------

By default, :module:`mod_proxy_fcgi` does **not** reuse connections —
each request opens a new connection to the backend and closes it
afterward. For PHP-FPM, this is safe but wasteful. If PHP-FPM is
configured to accept concurrent connections (which it does by default),
you can enable connection reuse:

.. code-block:: apache

   # On a ProxyPass or <Proxy> block:
   ProxyPass "/app/" "fcgi://127.0.0.1:9000/" enablereuse=on

   # Or with SetHandler, define a Proxy worker first:
   <Proxy "fcgi://localhost/" enablereuse=on max=10>
   </Proxy>

The ``max`` parameter limits the number of pooled connections per Apache
child process. Set this to a value that balances connection reuse
against exhausting PHP-FPM's ``pm.max_children``.


Common Pitfalls
---------------

**Timeout issues.** PHP-FPM has its own ``request_terminate_timeout``
setting, but Apache also enforces a ``ProxyTimeout`` (which defaults to
the value of the ``Timeout`` directive, usually 60 seconds). If a PHP
script runs longer than the proxy timeout, Apache returns a
``504 Gateway Timeout`` even if PHP-FPM is still working. Align
the two values:

.. code-block:: apache

   # Allow long-running scripts (e.g., imports) up to 300 seconds
   ProxyTimeout 300

**PATH_INFO handling.** When using ``ProxyPassMatch``, Apache does not
automatically split the URL into ``SCRIPT_NAME`` and ``PATH_INFO``.
Frameworks that rely on ``PATH_INFO`` (such as some REST routing
schemes) may break. You can work around this by setting the
``proxy-fcgi-pathinfo`` environment variable:

.. code-block:: apache

   # Enable best-guess PATH_INFO splitting
   SetEnv proxy-fcgi-pathinfo 1

.. tip::

   Since version 2.4.26, the ``ProxyFCGIBackendType`` directive
   controls how :module:`mod_proxy_fcgi` sets environment variables
   like ``SCRIPT_FILENAME``. The default value ``FPM`` is correct for
   PHP-FPM. Set it to ``GENERIC`` only if you are proxying to a
   non-PHP FastCGI application that expects the ``proxy:fcgi://``
   prefix on ``SCRIPT_FILENAME``.

**Socket permission errors.** When using Unix domain sockets, the Apache
user (typically ``www-data`` or ``apache``) must have read/write
access to the socket file. In the PHP-FPM pool configuration, set
``listen.owner`` and ``listen.group`` to match the Apache user, or use
``listen.mode = 0660`` and add the Apache user to the PHP-FPM group.

**PHP files downloading instead of executing.** If ``.php`` files are
served as downloads rather than being processed, the handler is not
being applied. Verify that :module:`mod_proxy` and
:module:`mod_proxy_fcgi` are loaded, and that the ``<FilesMatch>``
block or ``ProxyPassMatch`` directive is active for the virtual host
in question.


A Complete Virtual Host Example
-------------------------------

Putting it all together — a production-style virtual host using the
recommended UDS approach with the ``event`` MPM:

.. code-block:: apache

   <VirtualHost *:443>
       ServerName www.example.com
       DocumentRoot /var/www/example

       SSLEngine on
       SSLCertificateFile    /etc/letsencrypt/live/example.com/fullchain.pem
       SSLCertificateKeyFile /etc/letsencrypt/live/example.com/privkey.pem

       # Forward PHP requests to PHP-FPM via Unix domain socket
       <FilesMatch "\.php$">
           SetHandler "proxy:unix:/run/php/php-fpm.sock|fcgi://localhost"
       </FilesMatch>

       DirectoryIndex index.php index.html

       <Directory /var/www/example>
           AllowOverride All
           Require all granted
       </Directory>

       # Proxy timeout for long-running scripts
       ProxyTimeout 120

       ErrorLog  ${APACHE_LOG_DIR}/example-error.log
       CustomLog ${APACHE_LOG_DIR}/example-access.log combined
   </VirtualHost>


.. _See_Also_mod_proxy_fcgi:

See Also
~~~~~~~~


* https://httpd.apache.org/docs/current/mod/mod_proxy_fcgi.html

* https://httpd.apache.org/docs/current/mod/mod_proxy.html#proxypassmatch

* https://www.php.net/manual/en/install.fpm.php

* :ref:`Forwarding_Requests_to_Another_Server_id147962`

* :ref:`Recipe_mod_proxy_balancer`


.. admonition:: DRAFT — Review needed

   The following recipe was auto-generated and needs editorial review.
   Check technical accuracy, voice/tone, and fit with surrounding content.

.. _Recipe_websocket_proxy:

Proxying WebSocket Connections
------------------------------

.. index:: mod_proxy_wstunnel
.. index:: WebSocket
.. index:: ws://
.. index:: wss://


.. _Problem_websocket_proxy:

Problem
~~~~~~~

You have a backend application — such as a Node.js, Python, or Java
server — that uses WebSocket connections for real-time communication,
and you want Apache httpd to act as the reverse proxy in front of it.


.. _Solution_websocket_proxy:

Solution
~~~~~~~~

Load :module:`mod_proxy_wstunnel` (along with :module:`mod_proxy`) and
use ``ProxyPass`` with a ``ws://`` scheme to forward WebSocket
traffic to the backend.

A minimal configuration that proxies WebSocket connections on a
dedicated path to a Node.js backend running on port 3000:

.. code-block:: apache

   LoadModule proxy_module modules/mod_proxy.so
   LoadModule proxy_wstunnel_module modules/mod_proxy_wstunnel.so
   LoadModule proxy_http_module modules/mod_proxy_http.so

   <VirtualHost *:80>
       ServerName app.example.com

       # WebSocket traffic — must come before the general proxy rule
       ProxyPass "/ws/" "ws://localhost:3000/ws/"

       # Regular HTTP traffic
       ProxyPass "/" "http://localhost:3000/"
       ProxyPassReverse "/" "http://localhost:3000/"
   </VirtualHost>

For a production deployment with TLS termination at Apache — where
clients connect over ``wss://`` but the backend speaks plain
``ws://`` — wrap the above in an SSL virtual host:

.. code-block:: apache

   <VirtualHost *:443>
       ServerName app.example.com

       SSLEngine on
       SSLCertificateFile /etc/letsencrypt/live/app.example.com/fullchain.pem
       SSLCertificateKeyFile /etc/letsencrypt/live/app.example.com/privkey.pem

       # WebSocket — clients use wss://, we proxy to ws:// on the backend
       ProxyPass "/ws/" "ws://localhost:3000/ws/"

       # HTTP
       ProxyPass "/" "http://localhost:3000/"
       ProxyPassReverse "/" "http://localhost:3000/"
   </VirtualHost>

If your application serves both HTTP and WebSocket traffic on the
same URL path — that is, the client opens a regular HTTP connection and
then *upgrades* it to WebSocket — use ``RewriteRule`` to detect the
``Upgrade`` header and route accordingly:

.. code-block:: apache

   <VirtualHost *:443>
       ServerName app.example.com

       SSLEngine on
       SSLCertificateFile /etc/letsencrypt/live/app.example.com/fullchain.pem
       SSLCertificateKeyFile /etc/letsencrypt/live/app.example.com/privkey.pem

       RewriteEngine On
       RewriteCond %{HTTP:Upgrade} websocket [NC]
       RewriteCond %{HTTP:Connection} upgrade [NC]
       RewriteRule ^/?(.*) "ws://localhost:3000/$1" [P,L]

       ProxyPass "/" "http://localhost:3000/"
       ProxyPassReverse "/" "http://localhost:3000/"
   </VirtualHost>


.. _Discussion_websocket_proxy:

Discussion
~~~~~~~~~~

WebSocket is a protocol that provides full-duplex communication
over a single TCP connection. Unlike regular HTTP, where the client
sends a request and the server sends a response, a WebSocket
connection stays open and either side can send data at any time. This
makes it ideal for real-time applications such as chat, live
dashboards, collaborative editing, and online games.

The WebSocket handshake begins as a normal HTTP request. The client
sends an ``Upgrade: websocket`` header, and if the server agrees, the
connection is "upgraded" from HTTP to the WebSocket protocol. After
the upgrade, HTTP is no longer spoken on that connection —
it becomes a raw bidirectional tunnel.

``mod_proxy_wstunnel`` understands this upgrade mechanism. When
Apache receives a request with a ``ws://`` or ``wss://`` scheme in
the ``ProxyPass`` target, it knows to expect the WebSocket handshake
and to maintain the persistent tunnel once the upgrade succeeds.

**Ordering matters.** Because ``ProxyPass`` directives are
matched in the order they appear, more specific rules (like those for
``/ws/``) must come *before* more general rules (like ``/``).
If you reverse the order, the general HTTP proxy rule will
match first, and your WebSocket connections will fail with a ``400
Bad Request`` or simply hang.

**The ``RewriteRule`` approach.** When your application does not
use a dedicated WebSocket URL path — for example, the Socket.IO
library negotiates WebSocket on the same path it uses for HTTP
long-polling — you cannot rely on URL-based ``ProxyPass`` routing.
Instead, use ``RewriteRule`` with conditions that inspect the
``Upgrade`` and ``Connection`` request headers, as shown in the
third configuration example above. The ``[P]`` flag tells
``mod_rewrite`` to hand the rewritten URL to the proxy, and
``mod_proxy_wstunnel`` handles the tunneling from there.

**TLS termination.** A very common pattern — and one that appeared
repeatedly on the Apache users mailing list from 2017 through 2024
— is to terminate TLS at Apache and proxy unencrypted WebSocket
traffic to the backend. From the client's perspective the connection
is ``wss://`` (WebSocket Secure), but Apache handles the SSL/TLS
layer and forwards to the backend over plain ``ws://``. This is
exactly what the second example above does. The backend application
does not need to be configured with certificates at all.

If your backend also requires TLS (for example, in environments with
strict end-to-end encryption requirements), use ``wss://`` in the
``ProxyPass`` target:

.. code-block:: apache

   ProxyPass "/ws/" "wss://backend.example.com:3443/ws/"

You will also need to configure ``SSLProxyEngine on`` and
potentially ``SSLProxyVerify``, ``SSLProxyCACertificateFile``, and
related directives if the backend uses self-signed or internal
certificates.

**Timeouts.** WebSocket connections are long-lived by design,
and the default ``ProxyTimeout`` (which inherits from the server's
``Timeout`` directive, typically 60 seconds) will close idle
WebSocket connections after just one minute of silence. For
applications that rely on infrequent messages, increase this value:

.. code-block:: apache

   ProxyTimeout 600

This sets the idle timeout to 10 minutes. Alternatively, have your
application send periodic *ping* frames to keep the connection alive
— the WebSocket protocol defines ping/pong frames for exactly this
purpose.

If you see ``AH10224: tunnel timed out`` in your error log, the
``ProxyTimeout`` value is the first thing to check.

**Connection persistence and the ``disablereuse`` parameter.** By
default, ``mod_proxy`` pools and reuses backend connections. For
WebSocket tunnels, each connection is unique to a client session and
cannot be reused. In most cases ``mod_proxy_wstunnel`` handles this
correctly, but if you encounter connection confusion (for example,
messages arriving at the wrong client), you can explicitly disable
connection reuse for the WebSocket path:

.. code-block:: apache

   ProxyPass "/ws/" "ws://localhost:3000/ws/" disablereuse=on

**Load balancing WebSocket connections.** You can combine
``mod_proxy_wstunnel`` with ``mod_proxy_balancer`` to distribute
WebSocket connections across multiple backends:

.. code-block:: apache

   <Proxy "balancer://wscluster">
       BalancerMember "ws://192.168.1.50:3000"
       BalancerMember "ws://192.168.1.51:3000"
       ProxySet lbmethod=byrequests
   </Proxy>

   ProxyPass "/ws/" "balancer://wscluster/ws/"

Be aware that WebSocket connections are long-lived and stateful. If
your application stores session state in memory on a particular
backend, you will need sticky sessions (``stickysession``) or an
external session store (such as Redis) to ensure that a client's
WebSocket connection reaches the same backend that holds its state.
A simple round-robin load balancer will distribute *new* connections
evenly but cannot migrate an established WebSocket tunnel from one
backend to another.

**Changes in 2.4.47 and later.** Starting with Apache httpd 2.4.47,
the core ``mod_proxy_http`` module gained the ability to handle
the WebSocket ``Upgrade`` mechanism directly, without requiring
``mod_proxy_wstunnel``. In this newer approach, you add the ``upgrade``
parameter to a regular HTTP ``ProxyPass``:

.. code-block:: apache

   ProxyPass "/" "http://localhost:3000/" upgrade=websocket

This tells ``mod_proxy_http`` to honor ``Upgrade: websocket``
requests and tunnel them transparently. This is now the recommended
approach in the official documentation. However,
``mod_proxy_wstunnel`` remains fully functional, widely deployed,
and appropriate for use on older versions. If you are running 2.4.47
or later and are setting up a new configuration, the
``upgrade=websocket`` approach on ``ProxyPass`` is simpler and avoids
the need for separate ``ws://`` rules.

**A complete working example** — proxying to a simple Node.js
WebSocket server. First, the Node.js backend, saved to
:file:`/opt/app/server.js`:

.. code-block:: javascript

   const http = require('http');
   const { WebSocketServer } = require('ws');

   const server = http.createServer((req, res) => {
       res.writeHead(200, { 'Content-Type': 'text/plain' });
       res.end('Hello from the HTTP side\n');
   });

   const wss = new WebSocketServer({ server, path: '/ws/' });
   wss.on('connection', (ws) => {
       console.log('Client connected');
       ws.on('message', (msg) => {
           console.log('Received:', msg.toString());
           ws.send('Echo: ' + msg.toString());
       });
       ws.on('close', () => console.log('Client disconnected'));
   });

   server.listen(3000, () => {
       console.log('Listening on http://localhost:3000');
   });

And the Apache configuration in
:file:`/etc/httpd/conf.d/app.conf`:

.. code-block:: apache

   <VirtualHost *:443>
       ServerName app.example.com

       SSLEngine on
       SSLCertificateFile /etc/letsencrypt/live/app.example.com/fullchain.pem
       SSLCertificateKeyFile /etc/letsencrypt/live/app.example.com/privkey.pem

       ProxyRequests off
       ProxyPreserveHost on

       # Increase timeout for long-lived WebSocket connections
       ProxyTimeout 600

       # WebSocket path — must be listed before the catch-all
       ProxyPass "/ws/" "ws://localhost:3000/ws/"

       # Everything else — regular HTTP proxy
       ProxyPass "/" "http://localhost:3000/"
       ProxyPassReverse "/" "http://localhost:3000/"
   </VirtualHost>

Clients connecting to ``wss://app.example.com/ws/`` will have their
connections tunneled to the Node.js WebSocket server. Regular HTTP
requests to ``https://app.example.com/`` will be proxied as normal.

**Common errors and troubleshooting:**

- ``AH01144: No protocol handler was valid for the URL /ws/`` —
  You forgot to load ``mod_proxy_wstunnel``. Add ``LoadModule
  proxy_wstunnel_module modules/mod_proxy_wstunnel.so`` to your
  configuration.

- ``400 Bad Request`` on WebSocket handshake — Check the ordering
  of your ``ProxyPass`` directives. The WebSocket rule must appear
  before the general HTTP proxy rule.

- ``AH10224: tunnel timed out`` — The WebSocket connection was
  idle longer than ``ProxyTimeout`` allows. Increase the value or
  implement application-level ping/pong.

- WebSocket works over HTTP but fails over HTTPS — Make sure that
  ``SSLEngine on`` is configured and that your SSL certificate is
  valid. Some clients (especially browsers) will silently refuse
  to establish a ``wss://`` connection if the certificate is
  untrusted.


.. _See_Also_websocket_proxy:

See Also
~~~~~~~~

* http://httpd.apache.org/docs/current/mod/mod_proxy_wstunnel.html

* http://httpd.apache.org/docs/current/mod/mod_proxy.html — see the
  *Protocol Upgrade* section for the 2.4.47+ ``upgrade=`` parameter

* :ref:`Recipe_Securing-proxy`

* :ref:`Recipe_mod_proxy_balancer`

* https://datatracker.ietf.org/doc/html/rfc6455 — The WebSocket
  Protocol (RFC 6455)


Summary
-------


_mod_proxy_ allows to run a reverse proxy as well as a forward proxy using Apache httpd.
Make sure you secured your server before enabling _mod_proxy_.

