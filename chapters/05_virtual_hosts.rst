
.. _Chapter_Virtual_hosts:

=============
Virtual Hosts
=============

.. index:: Virtual hosts

.. index:: Vhosts


As a person can be known by many names, so can a Web server
support multiple Web sites. In the Apache configuration file, each
alternate identity, and probably the "main" one as well, is known as a
virtual host (sometimes written as vhost) identified with a **&lt;VirtualHost&gt;** container directive.
Depending on the name used to access the Web server, Apache responds
appropriately, just as someone might answer differently depending on whether she is addressed as
"Miss Jones" or "Hey, Debbie!" If you want to have a single system support
multiple Web sites, you must configure Apache appropriately—and you'll need to know a
little bit about your system (such as the IP addresses assigned to it) in
order to do it correctly.

There are two different types of virtual host supported by Apache.
The first type, called address-based or IP-based, is tied to the numeric
network address used to reach the system, rather like telephone numbers.
Bruce Wayne never answered the parlour telephone with "Batman here!" nor
did he answer the phone in the Batcave by saying, "Bruce Wayne speaking."
However, it's the same person answering the phone, just as it's the same
Web server receiving the request. Even if the caller had a wrong number
and said, "Hi, Steve!," the phone was still answered the same way; nothing
would convince Batman to admit on the Batphone that it was Bruce Wayne
answering.

The other type of virtual host is called name-based because the
server's response depends on the
name by which it was called. To continue the telephone analogy, consider
an apartment shared by multiple roommates; you call the same number
whether you want to speak to Dave, Joyce, Amaterasu, or Georg. Just as
multiple people may share a single telephone number, multiple Web sites
can share the same IP address. However, all IP addresses shared by
multiple Apache virtual hosts need to be declared with a **NameVirtualHost** directive.

In the most simple of Apache configurations, there are no virtual
hosts. Instead, all of the directives in the configuration file apply
universally to the operation of the server. The environment defined by the
directives outside any **&lt;VirtualHost&gt;** containers is sometimes
called the "default server," "main server," or perhaps the "global
server." There is no official name for it, but it can become a factor when
adding virtual hosts to your configuration.

But what happens if you add a **&lt;VirtualHost&gt;**
container to such a configuration? How are those directives outside the
container interpreted, and what is their effect on the virtual
host?

The answer is not a simple one: essentially, the effect is specific
to each configuration directive. Some get inherited by the virtual hosts,
some get reset to a default value, and some pretend they've never been
used before. You'll need to consult the documentation for each directive
to know for sure.

There are two primary forms of virtual hosts: IP-based virtual
hosts, where each virtual host has its own unique IP address; and
name-based virtual hosts, where more than one virtual host
runs on the same IP address but with different names. This chapter will
show you how to configure each one and how to combine the two on the same
server. You'll also learn how to fix common problems that occur with
virtual hosts.


.. note::

   To avoid problems and confusing error messages, we strongly advise
   that you explicitly include the port number on directives specifying an
   IP address if they support supplying both the address and the port. For
   instance, use:

   NameVirtualHost *:80

   instead of:

   NameVirtualHost *

   Normal Web operations use port 80, and most SSL requests use port 443.


.. _Recipe_name_vhosts:

Setting Up Name-Based Virtual Hosts

.. index:: Virtual hosts,Name-based

.. index:: Name-based virtual hosts

.. index:: NameVirtualHost

.. index:: <VirtualHost>


.. _Problem_name_vhosts:

Problem
~~~~~~~


You have only one IP address, but you want to support more than
one Web site on your system.


.. _Solution_name_vhosts:

Solution
~~~~~~~~


[role="v22"]
httpd 2.2 solution
~~~~~~~~~~~~~~~~~~


For Apache httpd 2.2 and earlier, use the **NameVirtualHost** **:80* 
directive in conjunction with **&lt;VirtualHost&gt;** sections.


.. code-block:: text

   NameVirtualHost *:80
   
   <VirtualHost *:80>
       ServerName TheSmiths.name
       DocumentRoot "C:/Apache/Sites/TheSmiths"
   </VirtualHost>
           
   <VirtualHost *:80>
       ServerName JohnSmith.name
       DocumentRoot "C:/Apache/Sites/JustJohnSmith"
   </VirtualHost>


[role="v24"]
httpd 2.4 solution
~~~~~~~~~~~~~~~~~~


For 2.4 and later, just create the <VirtualHost> sections - the
**NameVirtualHost** directive is deprecated in 2.4.


.. code-block:: text

   <VirtualHost *:80>
       ServerName TheSmiths.name
       DocumentRoot "C:/Apache/Sites/TheSmiths"
   </VirtualHost>
           
   <VirtualHost *:80>
       ServerName JohnSmith.name
       DocumentRoot "C:/Apache/Sites/JustJohnSmith"
   </VirtualHost>


.. _Discussion_name_vhosts:

Discussion
~~~~~~~~~~


With IP addresses increasingly hard to come by, name-based
virtual hosting is the most common way to run multiple Web sites on
the same Apache server. The previous recipe works for most users in
most virtual hosting situations.

The **:80* in the previous
rules means that the specified hosts run on all addresses. For a
machine with only a single address, this means that it runs on that
address but will also run on the **loopback**, or
**localhost** address. Thus if you are sitting at the
physical server system, you can view the Web site.

The argument to the **&lt;VirtualHost&gt;** container directive
needs to match the argument in a **NameVirtualHost** directive. Putting the
hostname here may cause Apache to ignore the virtual host on server
startup, and requests to this virtual host may unexpectedly go
somewhere else. If your name server is down or otherwise unresponsive
at the time that your Apache server is starting up, then Apache can't
match the particular **&lt;VirtualHost&gt;** section to the
**NameVirtualHost** directive to which it belongs.

The **NameVirtualHost** directive is deprecated in 2.4 and later, in
which case httpd will discern the interface to answer on based on the
argument to the <VirtualHost> container directive.

Requests for which there is not a virtual host listed will go to
the first virtual host listed in the configuration file. In the case
of the previous example, requests coming to the server using hostnames
that are not explicitly mentioned in one of the virtual hosts will be
served by the ``TheSmiths.name``
virtual host.

Multiple names can be listed for a particular virtual host using
the **ServerAlias** directive, as shown
here:


.. code-block:: text

   ServerName TheSmiths.name
   ServerAlias www.TheSmiths.name Smith.Family.name


It is particularly instructive to run **httpd** **-S**
and observe the virtual host configuration as Apache understands it,
to see if it matches the way that you understand it. **httpd** **-S**
returns the virtual host configuration, showing which hosts are
name-based, which are IP-based, and what the defaults are.

The output of **httpd** **-S** will look like:


.. code-block:: text

   [rbowen@grenache:conf.d/vhosts]$ sudo httpd -S
   
   VirtualHost configuration:
   *:80  is a NameVirtualHost
         default server grenache.rcbowen.com (/etc/httpd/conf.d/vhosts/00_grenache.conf:4)
         port 80 namevhost grenache.rcbowen.com (/etc/httpd/conf.d/vhosts/00_grenache.conf:4)
         alias grenache
         port 80 namevhost www.apacheadmin.com (/etc/httpd/conf.d/vhosts/apacheadmin.com.conf:2)
         alias apacheadmin.com
   ...


It is important to understand that virtual hosts render the
server listed in the main body of your configuration file (the "main"
or "default" server mentioned earlier) no longer accessible—you must
create a virtual host section explicitly for that host. List this host
first, if you want it to be the default one.

Adding name-based virtual hosts to your Apache configuration
does not magically add entries to your DNS server. You must still add
records to your DNS server so that the names resolve to the IP address
of the server system. When users type your server name(s) into their
browser location bars, their computers first contact a DNS server to
look up that name and resolve it to an IP address. If there is no DNS
record, then their browsers can't find your server.

For more information on configuring your DNS server, consult the
documentation for the DNS software you happen to be running, or talk
to your ISP if you're not running your own DNS server.


.. _See_Also_name_vhosts:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/vhosts - Virtual hosts
   documentation

* :ref:`Recipe_dns`


.. _Recipe_Default_name_based_vhost:

Default_name_based_vhost

.. index:: Virtual hosts,Default

.. index:: Virtual hosts,Name-based

.. index:: Default virtual host,Name-based


.. _Problem_Default_name_based_vhost:

Problem
~~~~~~~


You want all unmatched requests, whether they specify a name or
use an IP address, to be directed to a default host, possibly with a
"host not found" error message.


.. _Solution_Default_name_based_vhost:

Solution
~~~~~~~~


Add the following **&lt;VirtualHost&gt;** section, and list it
before all of your other ones:


.. code-block:: text

   <VirtualHost *:80>
       ServerName default
       DocumentRoot /www/htdocs
       ErrorDocument 404 /site_list.html
   </VirtualHost>


.. _Discussion_Default_name_based_vhost:

Discussion
~~~~~~~~~~


Note that this recipe is used in the context of name-based
virtual hosts, so it is assumed that you have other virtual hosts that
are also using the **&lt;VirtualHost**
**:80&gt;* notation, and that there
is also an accompanying **NameVirtualHost** **:80* appearing above them. We have used the
``default`` name for clarity; you can
call it whatever you want.

Setting the **ErrorDocument 404**
to a list of the available sites on the server directs the user to
useful content, rather than leaving him stranded with an unhelpful 404
error message. You may wish to set **DirectoryIndex** to the site list as well, so
that users who go directly to the front page of this site also get
useful information.

It's a good idea to list explicitly all valid hostnames either
as **ServerName** s or **ServerAlias** es, so that
nobody ever winds up at the default site. However, if someone accesses
the site directly by IP address, or if a hostname is added to the
address in question before the appropriate virtual host is created,
the user still gets useful content.


.. _See_Also_Default_name_based_vhost:

See Also
~~~~~~~~


* :ref:`Recipe_Default-address-vhost`


.. _Recipe_Address-based-vhosts:

Address-based-vhosts

.. index:: Virtual hosts,Address-based

.. index:: Address-based virtual hosts

.. index:: IP-address based virtual hosts


.. _Problem_Address-based-vhosts:

Problem
~~~~~~~


You have multiple IP addresses assigned to your system, and you
want to support one Web site on each.


.. _Solution_Address-based-vhosts:

Solution
~~~~~~~~


Create a virtual host section for each IP address you want to
list on:


.. code-block:: text

   ServerName 127.0.0.1
   
   <VirtualHost 10.0.0.1>
       ServerName Example.Com
       DocumentRoot "C:/Apache/Sites/Example.Com"
   </VirtualHost>
   
   <VirtualHost 10.0.0.2>
       ServerName JohnSmith.Example.Com
       DocumentRoot "C:/Apache/Sites/JustJohnSmith"
   </VirtualHost>


.. _Discussion_Address-based-vhosts:

Discussion
~~~~~~~~~~


The virtual hosts defined in this example catch all requests to
the specified IP addresses, regardless of what hostname is used to get
there. Requests to any other IP address not listed go to the virtual
host listed in the main body of the configuration file.

The **ServerName** specified is
used as the primary name of the virtual host, when needed, but is not
used in the process of mapping a request to the correct host. Only the
IP address (not the ``Host`` header
field) is consulted to figure out which virtual host to serve requests
from.


.. _See_Also_Address-based-vhosts:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/2.2/vhosts/

* :ref:`Recipe_Default-address-vhost`


.. _Recipe_Default-address-vhost:

Default address virtual host

.. index:: Virtual hosts,Address-based

.. index:: Virtual hosts,Default

.. index:: Address-based virtual hosts

.. index:: IP-address based virtual hosts

.. index:: Default virtual host,Address-based


.. _Problem_Default-address-vhost:

Problem
~~~~~~~


You want to create a virtual host to catch all requests that
don't map to one of your address-based virtual hosts.


.. _Solution_Default-address-vhost:

Solution
~~~~~~~~


Use the **default** keyword to designate a default host:


.. code-block:: text

   <VirtualHost _default_>
       DocumentRoot /www/htdocs
   </VirtualHost>


.. _Discussion_Default-address-vhost:

Discussion
~~~~~~~~~~


The **default** keyword
creates a virtual host that catches all requests for any
**``address``**:**``port``**
combinations for which there is no virtual host configured.

The **default** directive
may—and should—be used in conjunction with a particular port number,
such as:


.. code-block:: text

   <VirtualHost _default_:443>


Using this syntax means that the specified virtual host catches
all requests to port 443, on all addresses for which there is not an
explicit virtual host configured. SSL virtual hosts are usually set up
using the **default** syntax, so
you'll see this syntax used in the default SSL configuration file,
along with the necessary directives to enable SSL.

**default** typically does not
work as people expect in the case of name-based virtual hosts. It does
not match names for which there are no virtual host sections, only
**``address``**:**``port``**
combinations for which there are no virtual hosts configured. If you
wish to create a default name-based host, see :ref:`Recipe_Default_name_based_vhost`.


.. _See_Also_Default-address-vhost:

See Also
~~~~~~~~


* :ref:`Recipe_Default_name_based_vhost`


.. _Recipe_mixing_address_and_name_based_vhosts:

Mixing Address-Based and Name-Based Virtual Hosts

.. index:: Mixing address-based and name-based virtual hosts

.. index:: Virtual Hosts,Mising name-based and address-based


.. _Problem_mixing_address_and_name_based_vhosts:

Problem
~~~~~~~


You have multiple IP addresses assigned to your system, and you
want to support more than one Web site on each address.


.. _Solution_mixing_address_and_name_based_vhosts:

Solution
~~~~~~~~


For httpd 2.2 and earlier, provide a **NameVirtualHost**
directive for each IP address, and proceed as you did with a single IP
address.

For 2.4 and later, the **NameVirtualHost** line is ommitted, and httpd
infers it from the argument to <VirtualHost> and does the right thing.


.. code-block:: text

   ServerName 127.0.0.1
   
   ## Omit these lines on 2.4 and later
   NameVirtualHost 10.0.0.1:80
   NameVirtualHost 10.0.0.2:80
   ## 
   
   <VirtualHost 10.0.0.1:80>
       ServerName TheSmiths.name
       DocumentRoot "C:/Apache/Sites/TheSmiths"
   </VirtualHost>
   
   <VirtualHost 10.0.0.1:80>
       ServerName JohnSmith.name
       DocumentRoot "C:/Apache/Sites/JustJohnSmith"
   </VirtualHost>
   
   <VirtualHost 10.0.0.2:80>
       ServerName Example.Com
       DocumentRoot "C:/Apache/Sites/Example.Com"
   </VirtualHost>
   
   <VirtualHost 10.0.0.2:80>
       ServerName DoriFerguson.Example.Com
       DocumentRoot "C:/Apache/Sites/JustDoriFerguson"
   </VirtualHost>


.. _Discussion_mixing_address_and_name_based_vhosts:

Discussion
~~~~~~~~~~


Using the address of the server, rather than the wildcard
``*`` argument, makes the virtual hosts
listen only to that IP address. However, you should notice that the
argument to **&lt;VirtualHost&gt;**
still must match the argument to the **NameVirtualHost** with which the 
virtual hosts are connected.

The argument to <VirtualHost> should be an IP:Port combination, rather
than a hostname.

The example here shows Microsoft Windows file path designations.


.. _See_Also_mixing_address_and_name_based_vhosts:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/vhosts/ - Virtual host
  documentation


.. _Recipe_mod_vhost_alias:

Mass Virtual Hosting with mod_vhost_alias

.. index:: Mass virtual hosting

.. index:: mod_vhost_alias

.. index:: Modules,mod_vhost_alias

.. index:: Virtual hosts,Mass virtual hosting

.. index:: Virtual hosts,mod_vhost_alias

.. index:: VirtualDocumentRoot

.. index:: VirtualScriptAlias


.. _Problem_mod_vhost_alias:

Problem
~~~~~~~


You want to host many virtual hosts, all of which have exactly
the same configuration.


.. _Solution_mod_vhost_alias:

Solution
~~~~~~~~


Use **VirtualDocumentRoot** and **VirtualScriptAlias** provided by
``mod_vhost_alias``:


.. code-block:: text

   VirtualDocumentRoot /www/vhosts/%-1/%-2.1/%-2/htdocs
   VirtualScriptAlias  /www/vhosts/%-1/%-2.1/%-2/cgi-bin


.. _Discussion_mod_vhost_alias:

Discussion
~~~~~~~~~~


This recipe uses directives from ``mod_vhost_alias``, which you may not have
installed when you built Apache, as it is not one of the modules that
is enabled by default.

These directives map requests to a directory built up from
pieces of the hostname that was requested. Each of the variables
represents one part of the hostname, so that each hostname is mapped
to a different directory.

In this particular example, requests for content from
**``www.example.com``** are served from the
directory **/www/vhosts/com/e/example/htdocs**, or from
**/www/vhosts/com/e/example/cgi-bin**
(for CGI requests). The full range of available variables is shown in
:ref:`mod_vhost_alias_variables_id122257`.


.. _mod_vhost_alias_variables_id122257:

.mod_vhost_alias variables

+----------+--------------------------------------------+
| Variable | Meaning                                    |
+----------+--------------------------------------------+
| %%       | Insert a %                                 |
+----------+--------------------------------------------+
| %p       | Insert the port number of the virtual host |
+----------+--------------------------------------------+
| %M.N     | Insert (part of) the name                  |
+----------+--------------------------------------------+


M and N may have positive or negative integer values, the
meanings of which are shown in :ref:`Meanings_of_variable_values_id122365`.


.. _Meanings_of_variable_values_id122365:


**Meanings of variable values**


+-------+--------------------------------------------+
| Value | Meaning                                    |
+-------+--------------------------------------------+
| 0     | The whole name                             |
+-------+--------------------------------------------+
| 1     | The first part of the name                 |
+-------+--------------------------------------------+
| -1    | The last part of the name                  |
+-------+--------------------------------------------+
| 2     | The second part of the name                |
+-------+--------------------------------------------+
| -2    | The next-to-last part of the name          |
+-------+--------------------------------------------+
| 2+    | The second, and all following, parts       |
+-------+--------------------------------------------+
| -2+   | The next-to-last, and all preceding, parts |
+-------+--------------------------------------------+


When the value is placed in the first part of the argument—in
the **``M``** part of
**``%M.N``**—it refers to parts of the hostname
itself. When used in the second part—the
**``N``**—it refers to a particular letter from
that part of the hostname. For example, in hostname
**``www.example.com``**, the meanings of the
variables are as shown in :ref:`Example_values_for_the_hostname_wwwexamplecom_id122542`.


.. _Example_values_for_the_hostname_wwwexamplecom_id122542:

.Example values for the hostname www.example.com

+--------+-----------------+
| Value  | Meaning         |
+--------+-----------------+
| %0     | www.example.com |
+--------+-----------------+
| %1     | www             |
+--------+-----------------+
| %2     | example         |
+--------+-----------------+
| %3     | com             |
+--------+-----------------+
| %-1    | com             |
+--------+-----------------+
| %-2    | example         |
+--------+-----------------+
| %-3    | www             |
+--------+-----------------+
| %-2.1  | e               |
+--------+-----------------+
| %-2.2  | x               |
+--------+-----------------+
| %-2.3+ | ample           |
+--------+-----------------+


Depending on the number of virtual hosts, you may wish to create
a directory structure subdivided alphabetically by domain name, by
top-level domain, or simply by hostname.

Note that ``mod_vhost_alias``
does not set the ``DOCUMENT_ROOT``
environment variable, and so applications that rely on this value may
not work in this kind of virtual hosting environment.


.. _See_Also_mod_vhost_alias:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_vhost_alias.html
          
* http://httpd.apache.org/docs/vhosts


.. _Recipe_mass_vhost_rewrite:

Mass Virtual Hosting Using Rewrite Rules

.. index:: Virtual hosts,Mass virtual hosting

.. index:: mod_rewrite

.. index:: Modules,mod_rewrite

.. index:: Virtual hosts,mod_rewrite

.. index:: Mass virtual hosting


.. _Problem_mass_vhost_rewrite:

Problem
~~~~~~~


Although there is a module—``mod_vhost_alias``—that is explicitly for the
purpose of supporting large numbers of virtual hosts, it is very
limiting and requires that every virtual host be configured exactly
the same way. You want to support a large number of vhosts, configured
dynamically, but at the same time, you want to avoid ``mod_vhost_alias``.


.. _Solution_mass_vhost_rewrite:

Solution
~~~~~~~~


Use directives from ``mod_rewrite`` to map
to a directory based on the hostname:


.. code-block:: text

   RewriteEngine on
   RewriteCond   "%{HTTP_HOST}"     "^(www\.)?([^.]+)\.com"
   RewriteRule   "^(.*)$"           "/home/%2$1"


.. _Discussion_mass_vhost_rewrite:

Discussion
~~~~~~~~~~


``mod_vhost_alias`` is useful,
but it is best for settings where each virtual host is identical in
every way but the hostname and document tree. Using ``mod_vhost_alias`` precludes the use of other
URL-mapping modules, such as ``mod_userdir``, **mod_rewrite**, and ``mod_alias``, and it can be very restrictive.
Using ``mod_rewrite`` is less
efficient, but it is more flexible.

For example, when using ``mod_vhost_alias``, you must do all of your
hosts with ``mod_vhost_alias``; with
this alternate approach, you can do some of your hosts using the
rewrite rules and others using conventional virtual host configuration
techniques.

The directives in the Solution map requests for
**``www.something.com``** (or without the
**``www``**) to the directory **/home/something**.


.. _See_Also_mass_vhost_rewrite:

See Also
~~~~~~~~


* :ref:`Recipe_rewrite-path-to-vhost`
          
* http://httpd.apache.org/docs/vhosts - Virtual host
  documentation
          
* http://httpd.apache.org/docs/mod/mod_rewrite.html -
  ``mod_rewrite`` documentation


.. _Recipe_log_per_vhost:

Logging for Each Virtual Host

.. index:: Logging,Per virtual host

.. index:: Virtual hosts,Logging


.. _Problem_log_per_vhost:

Problem
~~~~~~~


You want each virtual host to have its own logfiles.


.. _Solution_log_per_vhost:

Solution
~~~~~~~~


Specify **Errorlog** and **CustomLog** within each virtual host
declaration:


.. code-block:: text

   <VirtualHost *:80>
       ServerName   waldo.example.com
       DocumentRoot /home/waldo/www/htdocs
   
       ErrorLog     /home/waldo/www/logs/error_log
       CustomLog    /home/waldo/www/logs/access_log combined
   </VirtualHost>


.. _Discussion_log_per_vhost:

Discussion
~~~~~~~~~~


The various logging directives can be placed either in the main
body of your configuration file or within a **&lt;VirtualHost&gt;** 
section. When they are
placed within a virtual host, log entries for that virtual host go in
the specified logfiles, rather than into the logfile(s) defined in the
main server configuration.


.. _apacheckbk-CHP-4-NOTE-88:


.. warning::

   Each logfile counts against the total number of files and
   network connections your server is allowed to have. If you have 100
   virtual hosts, each with its own error and activity log, that's 200
   open channels—and if the server's quota is 256, you can only handle
   56 concurrent requests at any one time.

   Those numbers are just examples; actual values for maximum
   open file quotas vary by platform, but are generally
   **much** larger. Consult your platform's
   documentation to find out your actual limit.

   For this reason, we recommend that you have all your virtual
   hosts log to the same files, and split them apart later for analysis
   or examination.


In the recipe given here, the logfiles are placed within the
home directory of a particular user, rather than in the main log
directory. This gives you easier access to those files, but you still
need to take adequate precautions to set the permissions on the
directory in question. Consult :ref:`Recipe_File_permissions`
for a discussion of file permissions.


.. _See_Also_log_per_vhost:

See Also
~~~~~~~~


* :ref:`Chapter_Logging`, **Logging**

* :ref:`Chapter_Security`, **Security**

* :ref:`Recipe_Per_Vhost_Log`


.. _Recipe_split_logfile:

Splitting Up a Logfile

.. index:: Logging,Splitting a log file

.. index:: split-logfile

.. index:: LogFormat

.. index:: CustomLog

.. index:: Splitting up a log file


.. _Problem_split_logfile:

Problem
~~~~~~~


Because of a large number of virtual hosts, you want to have a
single logfile for all of them and split it up afterward.


.. _Solution_split_logfile:

Solution
~~~~~~~~


This scenario is covered in :ref:`Chapter_Logging`, **Logging**, in the recipe
:ref:`Recipe_Per_Vhost_Log`.


.. _Recipe_port_vhost:

Port-Based Virtual Hosts

.. index:: Virtual hosts,Port-based

.. index:: Port-based virtual hosts


.. _Problem_port_vhost:

Problem
~~~~~~~


You want to present different content for HTTP connections on
different ports.


.. _Solution_port_vhost:

Solution
~~~~~~~~


Explicitly list the port number in the **&lt;VirtualHost&gt;** declaration:


.. code-block:: text

   Listen 8080
   
   <VirtualHost 10.0.1.2:8080>
       DocumentRoot /www/vhosts/port8080
   </VirtualHost>
   
   Listen 9090
   
   <VirtualHost 10.0.1.2:9090>
       DocumentRoot /www/vhosts/port9090
   <VirtualHost>


.. _Discussion_port_vhost:

Discussion
~~~~~~~~~~


Port-based virtual hosting is somewhat less common than other
techniques shown in this chapter. However, there are a variety of
situations in which it can be useful. If you have only one IP address,
have no ability to add hostnames to DNS, or if your ISP blocks inbound
traffic on port 80, it may be useful to run virtual hosts on other
ports.

It also may be useful in development environments to run
separate httpd instances on different ports for different developers
or different setups.

Finally, you could have different web services running on different
ports, but expose them to the public **via** a proxy server, proxying
different hostnames or URLs to the different services.

Visitors to your Web site must list the port number in the URL that
they use. For example, to load content from the second virtual host
previously listed, the following URL might be used:


.. code-block:: text

   http://server.example.com:9090


.. _See_Also_port_vhost:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/vhosts - Virtual hosts
   documentation


.. _Recipe_vhost_several_addresses:

Displaying the Same Content on Several Addresses

.. index:: Virtual hosts,Multiple addresses


.. _Problem_vhost_several_addresses:

Problem
~~~~~~~


You want to have the same content displayed on two of your
addresses.


.. _Solution_vhost_several_addresses:

Solution
~~~~~~~~


Specify both addresses in the **&lt;VirtualHost&gt;** directive:


.. code-block:: text

   # These two lines optional in 2.4 and later
   NameVirtualHost 192.168.1.1:80
   NameVirtualHost 172.20.30.40:80
   
   <VirtualHost 192.168.1.1:80 172.20.30.40:80>
       DocumentRoot /www/vhosts/server
       ServerName server.example.com
       ServerAlias server
   </VirtualHost>


.. _Discussion_vhost_several_addresses:

Discussion
~~~~~~~~~~


This setup is most useful on a machine that has addresses that
are internal to your network, as well as those that are accessible
only from outside your network. If these are the only addresses, you
could use the ``*`` notation introduced in :ref:`Recipe_name_vhosts`.
However, if there are more addresses, this allows you to specify what
content appears on what address.


.. _See_Also_vhost_several_addresses:

See Also
~~~~~~~~


* :ref:`Recipe_name_vhosts`

* http://httpd.apache.org/docs/vhosts/


.. _Recipe_Debian_Vhosts:

Using Debian's virtual host tools.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: Virtual hosts,Ubuntu

.. index:: Ubuntu,Virtual hosts

.. index:: Virtual hosts,Debian

.. index:: Debian,Virtual hosts


.. _Problem_Debian_Vhosts:

Problem
~~~~~~~


Debian, and Debian derivatives like Ubuntu, have their own tools for
handling virtual hosts.


.. _Solution_Debian_Vhosts:

Solution
~~~~~~~~


Use the **a2ensite** utility to enable a site that has been configured,
and **a2dissite** to disable it:


.. code-block:: text

   a2ensite example.conf
   a2dissite anotherexample.conf


.. _Discussion_Debian_Vhosts:

Discussion
~~~~~~~~~~


Debian's distribution of Apache httpd uses a directory structure built
around its site management tools. In the case of virtual hosts, there
are two directories, and two command line tools.

In the directory **/etc/apache2/sites-available/** you will find one
configuration file for each virtual host. By default, there will be
just one, named **000-default**, which describes the default virtual
host.

In the directory **/etc/apache2/sites-enabled**, you will file symbolic
links (symlinks) to the files in **/etc/apache2/sites-available** which
are enabled.

Two command-line tools are provided to manage these symlinks.
**a2ensite** (Apache 2 Enable Site) creates the symlink, and **a2dissite**
(Apache 2 Disable Site) removes that symlink.

In this way, you can create multiple virtual host configurations in
the **sites-available** directory, and then enable and disable them at
will.


.. note::

   You will still need to restart your Apache httpd server in order for
   these configuration changes to take effect.


.. _See_Also_Debian_Vhosts:

See Also
~~~~~~~~


* :ref:`Recipe_Enabling_modules_debian`

* man a2ensite

* man a2dissite

Summary


Apache httpd provides a mechanism for running multiple websites on the
same physical hardware, on the same instance of the httpd server. This
chapter describes the various ways that you can leverage this
functionality.

Virtual hosting is one aspect of the larger topic called URL Mapping -
that is the mapping of a particular URL to the expected resource or
content. In the next chapter, :ref:`Chapter_URL_Mapping`, **URL Mapping**, 
other parts of this topic will be discussed.

