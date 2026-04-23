
.. _Chapter_Proxies:

=======
Proxies
=======

.. index:: Proxies

.. index:: Content proxying


Proxy means to act on behalf of another. In the context of a Web
server, this means one server fetching content from another server, then
returning it to the client. For example, you may have several Web servers
that hide behind a proxy server. The proxy server is responsible for
making sure requests go to the right backend server.

``mod_proxy``, which comes with
Apache, handles proxying behavior. The recipes in this chapter cover
various techniques that can be used to take advantage of this capability.
We discuss securing your proxy server, caching content proxied through
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

You also may wish to consider a dedicated proxy server, such as Apache
Traffic Server (http://trafficserver.apache.org/), Varnish
(https://varnish-cache.org/), or
Squid (http://www.squid-cache.org), which are focused
entirely on one task, and thus have more options related to this
task.


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


For Apache 2.2:


.. code-block:: text

   <Proxy *>
       Order Deny,Allow
       Deny from all
       Allow from .yourdomain.com
   </Proxy>


For 2.4 and later:


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

For 2.2:


.. code-block:: text

   Allow from 192.168.1


Or for 2.4 and later:


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


If your Apache server is set up to operate as a proxy, it is
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


To use the Apache proxy as an SMTP relay is fairly trivial, but
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
        URL starting with ``/other/``, Apache
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
        content and have Apache transparently map requests for this content to
        the other server.


.. _Solution_id148476:

Solution
~~~~~~~~


First, install Apache, running on an alternate port, such as
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
that Apache is running as (typically nobody), so that it is able to
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
techniques like these, which you may need to deal with. We don't
presume to take a position on any of them. In particular, modifying
proxied content that does not belong to you may be a violation of the
owner's copyright and may be considered by some to be unethical.
Thankfully, this is just a technical book, not a philosophical one. We
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

++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting10_d1e16789" data-type="programlisting">ProxyPass "/secretserver/" "http://127.0.0.1:8080"
&lt;Directory "proxy:http://127.0.0.1:8080/"&gt;
    AuthName SecretServer
    AuthType Basic
    AuthUserFile <em><code>/path/to/secretserver.htpasswd</code></em>
    Require valid-user
&lt;/Directory&gt;</pre>
++++++++++++++++++++++++++++++++++++++


.. _Discussion_id149206:

Discussion
~~~~~~~~~~


This technique can be useful if you are running some sort of
        special-purpose or limited-function Web server on your system, but you
        need to apply Apache's rich set of access control and its other
        features to access it. This is done by using the **ProxyPass** directive to make the
        special-purpose server's URI space part of your main server, and using
        the special ``proxy``:**``path``**
        **&lt;Directory&gt;** container syntax
        to apply Apache settings only to the mapped URIs.


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
standard installation of the Apache Web server.

The example given above sets up a two-member balanced cluster
and proxies the URL ``/application`` to
that cluster.

``mod_proxy_balancer`` offers a
wide variety of options, which you can find in detail in the
documentation, available here: http://httpd.apache.org/docs/current/mod/mod_proxy_balancer.html.

For example, you can indicate that a particular server is more
powerful than another, and so should be allowed to assume more of the
load than other machines in the cluster. In the following
configuration line, we indicate that one particular machine should
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

For 2.2:

++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting6_d1e11209" data-type="programlisting">
# Don't allow anyone to access to http://other-host.org/path
&lt;Directory proxy:http://<em><code>other-host.org/path</code></em>&gt;
    Order Allow,Deny
    Deny from all
    Satisfy All
&lt;/Directory&gt;</pre>
++++++++++++++++++++++++++++++++++++++

Or for 2.4 and later:

++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting6_d1e11209" data-type="programlisting">
# Don't allow anyone to access to http://other-host.org/path
&lt;Directory proxy:http://<em><code>other-host.org/path</code></em>&gt;
    Require all denied
&lt;/Directory&gt;</pre>
++++++++++++++++++++++++++++++++++++++

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


Let's see what we are doing:
With **Protocols** and **ProtocolsHonorOrder** we tell Apache HTTDP to use HTTP/2
for the **VirtualHost**.
With the **ProxyPass** we tell Apache httpd to forward the requests to the HTTP/1.1
server **other.server.com**. Apache httpd will demultiplex and decode the HTTP/1.1 
that are in the HTTP/2 stream.


.. _See_Also_mod_proxy_h2:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/current/howto/http2.html

Summary
-------


_mod_proxy_ allows to run a reverse proxy as well as a forward proxy using Apache httpd.
Make sure you secured your server before enabling _mod_proxy_.

