
.. _Chapter_SSL_and_TLS:

===========
SSL and TLS
===========

.. index:: SSL

.. index:: TLS

.. index:: Secure websites


Transport Layer Security (TLS) and Secure Socket Layer (SSL) are
cryptographic protocols. They are the standard way to implement
secure Web sites.

By encrypting the traffic between the server and the client,
which is what TLS/SSL does, that content is protected from a third party
listening to the traffic going past.

**All** of the traffic exchanged is encrypted once the TLS/SSL session has
been set up. This means that even the URLs being requested are
encrypted.

The exact mechanism by which this encryption is accomplished is
discussed extensively in the TLS/SSL specifications, the current
version at the time of the booking writing is TLS 1.3 which you can read at
https://tools.ietf.org/html/rfc8446. For a more user-friendly
discussion of TLS/SSL, we recommend looking through the ``mod_ssl``
manual, which you can find at
http://httpd.apache.org/docs/2.4/ssl. This document not
only discusses the specific details of setting up ``mod_ssl`` but
also covers the general theory behind TLS/SSL and contains pictures
illustrating the concepts.

You can also find some friendly explanation at
http://en.wikipedia.org/wiki/Transport_Layer_Security.

As people tends to use SSL for both TLS and SSL, this chapter will use
SSL to designate the encryption layer you use.

In this chapter, we talk about some of the common things that you
might want to do with your secure server, including installing it.


.. _Installing_SSL_id138166:

Installing SSL
--------------


.. _Problem_id138179:

Problem
~~~~~~~


You want to install SSL on your Apache server.


.. _Solution_id138216:

Solution
~~~~~~~~


The solutions to this problem fall into several categories, depending
on how you installed Apache in the first place (or whether you are
willing to rebuild Apache to get SSL).

If you installed a binary distribution of Apache, your best bet
is to return to the place from which you acquired that binary
distribution and try to find the necessary files for adding SSL to
it.

If you built Apache yourself from source, just add
**--enable-ssl** to the **./configure** arguments when
you build Apache to include SSL as one of the built-in modules.

If configure doesn't find your openssl installation you have to
use **--with-ssl=** with the path to your openssl installation.
On most Linux distribution the configure can detect the location
of openssl. Make sure our install openssl-dev or openssl-devel
package.

Consult Chapters :ref:`Chapter_Installation`, **Installation**, and
:ref:`Chapter_Common_modules`, **Adding Common Modules**, for more
information on installing third-party modules, particularly if you
have installed a binary distribution of Apache rather than building it
yourself from the source code.

If you are attempting to install SSL on Apache for Windows, there is a
discussion of this in the Compiling on Windows document, which you can
find at
http://httpd.apache.org/docs/2.4/platform/win_compiling.html
for Apache 2.4.

Finally, note that the Apache SSL modules are an interface
between Apache and the OpenSSL libraries, which you must install
before any of this can work. You can obtain the OpenSSL libraries from
http://www.openssl.org. Although you may already
have these libraries installed on your server, it is recommended that
you obtain the latest version of the libraries to have the most recent
security patches and to protect yourself from exploits.


.. _Discussion_id138405:

Discussion
~~~~~~~~~~


So, why is this so complicated? Well, there are a variety of reasons,
most of which revolve around the legality of encryption. For a long
time, encryption has been a restricted technology in the United
States. Because Apache is primarily based out of the United States,
there is a great deal of caution regarding distributing encryption
technology with the package. Even though major changes have been made
in the laws, permitting SSL to be shipped with Apache 2.x, there are
still some gray areas that make it problematic to ship compiled binary
distributions of Apache httpd with SSL enabled in some countries.

This makes the situation particularly unpleasant on Microsoft Windows,
where most people do not have a compiler readily available to them,
and so must attempt to acquire binary builds from third parties to
enable SSL on their Apache server on Windows. The URL given previously
for compiling Apache 2.x with SSL on Windows assumes that you do have
a compiler. Check
http://httpd.apache.org/docs/2.4/platform/windows.html
for details on how to install your Apache server on Windows.


.. _See_Also_id138460:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/platform/win_compiling.html

* http://httpd.apache.org/docs/platform/windows.html

* https://wiki.apache.org/httpd/SSL

* http://www.openssl.org


.. _I_sect17_d1e12801:

Installing SSL on Windows
-------------------------


Problem
~~~~~~~


You want to install Apache with SSL on Microsoft Windows.


Solution
~~~~~~~~


Obtain binary distribution from any of the following:

* XAMPP from http://apachefriends.org

* ApacheHaus from http://www.apachehaus.com/cgi-bin/download.plx

* Apache Lounge from http://www.apachelounge.com/download/

* BitNami WAMP Stack from http://bitnami.com/stack/wamp

* WampServer from http://www.wampserver.com/

and install what you have downloaded following their instructions.


Discussion
~~~~~~~~~~


As was mentioned in the previous recipe, it is certainly possible to
build Apache with SSL from source on Microsoft Windows.  However, to
be honest, this is beyond the expertise of most of us.

So, save yourself some pain, take advantage of the great work that has
been done by the people that prepared ithe binaries above.


.. _Generating_SSL_Certificates_id138549:

Generating Self-Signed SSL Certificates
---------------------------------------


.. _Problem_id138563:

Problem
~~~~~~~


You want to generate a self-signed certificate to use on your SSL
server.


.. _Solution_id138616:

Solution
~~~~~~~~


Use the **openssl** command-line program that comes with OpenSSL:


++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting7_d1e12878" data-type="programlisting">
<code class="prompt">% </code><strong><code> openssl genrsa -out server.key 2048</code></strong>
<code class="prompt">% </code><strong><code> openssl req -new -key server.key -out server.csr</code></strong>
<code class="prompt">% </code><strong><code> openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt</code></strong></pre>
++++++++++++++++++++++++++++++++++++++

Then move these files to your Apache server's configuration directory,
such as **/www/conf/**, and then add the following lines in your
**httpd.conf** configuration file:


.. code-block:: text

   SSLEngine on
   SSLCertificateFile "/www/conf/server.crt"
   SSLCertificateKeyFile "/www/conf/server.key"


.. _Discussion_id138686:

Discussion
~~~~~~~~~~


The SSL certificate is a central part of the SSL conversation and is
required before you can run a secure server. Thus, generating the
certificate is a necessary first step to configuring your secure
server.

Generating the key is a multistep process, but it is fairly simple.


.. _Generating_the_private_key_id138712:

Generating the private key
^^^^^^^^^^^^^^^^^^^^^^^^^^


In the first step, we generate the private key. SSL is a
private/public key encryption system, with the private key residing on
the server and the public key going out with each connection to the
server and encrypting data sent back to the server.

The first argument passed to the **openssl** program tells **openssl**
that we want to generate an RSA key (**genrsa**), which is an
encryption algorithm that all major browsers support.

You may, if you wish, specify an argument telling **openssl** what to
use as the source of randomness. The -rand flag will accept one or
more filenames, which will be used as a key for the random number
generator. If no -rand argument is provided, OpenSSL will attempt to
use **/dev/urandom** by default if that exists, and it will try
**/dev/random** if **/dev/urandom** does not exist. It is important to
have a good source of randomness in order for the encryption to be
secure. If your system has neither **/dev/urandom** nor **/dev/random**,
you should consider installing a random number generator, such as
**egd**. You can find out more information about this on the OpenSSL Web
site at http://www.openssl.org/docs/crypto/RAND_egd.html.

The ``-out`` argument specifies the name of the key file that we will
generate. This file will be created in the directory in which you are
running the command, unless you provide a full path for this
argument. Naming the key file after the hostname on which it will be
used will help you keep track of the file, although the name of the
file is not actually important.

And, finally, an argument of 2048 is specified, which tells **openssl**
the size of the private key to generate in bit. 2048 is a safe
value at the time of this writing.

Your output should look something like:


.. code-block:: text

   Generating RSA private key, 2048 bit long modulus (2 primes)
   .........................................................++++++
   ........++++++
   e is 65537 (0x10001)


.. _Generating_the_certificate_signing_request_id138871:

Generating the certificate signing request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


The next step of the process is to generate a certificate signing
request. The reason it is called this is because the resultant file is
usually sent to a **certificate authority** (CA) for signing and is,
therefore, a signing request. (A certificate is just a signed key,
showing that someone certifies it to be valid and owned by the right
entity.)

A certificate authority is some entity that can sign SSL
certificates. What this usually means is that it is one of the few
dozen companies whose business it is to sign SSL certificates for use
on SSL servers. When a certificate is signed by one of these
certificate authorities browsers will automatically accept the
certificate as being valid. If a certificate is signed by a CA that is
not listed in the browser's list of trusted CAs, then the browser will
generate a warning, telling you that the certificate was signed by an
unknown CA and asking you if you are sure that you want to accept the
certificate.

This is a bit of an oversimplification of the process but conveys
enough of it for the purposes of this recipe.

The alternative is that you sign the certificate yourself, which is
what we'll be doing in the coming steps.

The arguments to this command specify the key for which the
certificate is being generated (the -key argument) and the name of the
file that you wish to generate (the -out argument).

If you want a certificate that will be accepted without warning or
comment by all major browsers, you will send the **csr** file, along
with a check or credit card information, to one of these CAs.

During this step, you'll be asked a number of questions. The answers
to these questions will become part of the certificate, and will be
used by the browser to verify that the certificate is coming from a
trusted source. End users may inspect these details any time they
connect to your Web site.

The questions will look like the following:


++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting7_d1e13021" data-type="programlisting">Country Name (2 letter code) [GB]: <strong><code>EX</code></strong>
State or Province Name (full name) [Berkshire]: <strong><code>CO</code></strong>
Locality Name (eg, city) [Newbury]: <strong><code>Example City</code></strong>
Organization Name (eg, company) [My Company Ltd]: <strong><code>Institute of Examples</code></strong>
Organizational Unit Name (eg, section) []: <strong><code>Demonstration Services</code></strong>
Common Name (eg, your name or your server's hostname) []: <strong><code>www.example.com</code></strong>
Email Address []: <strong><code>big-cheese@example.com</code></strong>
Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:</pre>
++++++++++++++++++++++++++++++++++++++

All of these values are optional, with the exception of the Common
Name. You must supply the correct value here, which is the hostname of
the server on which this certicate will be used. It is crucial that
the hostname that you put in here exactly match the hostname that will
be used to access the site. Failure to do this will result in a
warning message each time a user connects to your Web site.


Removing the passphrase
^^^^^^^^^^^^^^^^^^^^^^^


If, in the first step, we put a passphrase on the private key,
we will have to remove it.

The private is encrypted if you used one option like
**-des3** to encrypt it or if the openssl you are using 
does that by default.
The key encrypted so that only someone with the passphrase can read
the contents of the key.  A side-effect of this is that every time you
start up your Apache server, you will need to type in the
passprase. This is extremely inconvenient, as it means that starting
up the Web server always requires a manual step. This is particularly
a problem for reboots or other automated restarts of the Apache
server, when there might not be a human handy to type in the
passphrase.

++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting7_d1e13021" data-type="programlisting">
<code class="prompt">%</code><strong><code> cp server.key server.key.org</code></strong>
<code class="prompt">%</code><strong><code> openssl rsa -in server.key.org -out server.key</code></strong>
</pre>
++++++++++++++++++++++++++++++++++++++


Therefore, we're going to remove the passphrase from the key so that
this isn't an issue.

The key is copied to a backup location just in case we screw something
up, and then the command is issued to remove the passphrase, resulting
in an unencrupted key. You must remember to change the permissions on
the file so that only root can read this file. Failure to do so may
result in someone stealing that file and then being able to run a Web
site while pretending to be you.

Note that the **SSLPassPhraseDialog** directive allows to get
the passpharse from an external program.


.. _Signing_your_key_id138959:

Signing your certificate
^^^^^^^^^^^^^^^^^^^^^^^^


If you choose not to send the CSR to a Certificate Authority, and,
instead, sign your own public key (also called "signing your own
certificate," because signing your public key results in a self-signed
certificate), this will result in a perfectly usable certificate, and
save you a little money. This is especially useful for testing
purposes, but it may also be sufficient if you are running SSL on a
small site or a server on your internal network.

The process of signing a key means that the signer trusts that the key
does indeed belong to the person listed as the owner. If you pay
Entrust or one of the other commercial CAs for a certificate, they
will actually do research on you and verify, to some degree of
certainty, that you really are who you claim to be. They will then
sign your public key and send you the resulting certificate, putting
their stamp of approval on it and verifying to the world that you are
legitimate.

In the example given, we sign the key with the key itself, which is a
little silly, as it basically means that we trust ourselves. However,
for the purposes of the actual SSL encryption, this is sufficient.

If you prefer, you can use the **CA.pl** script that comes with OpenSSL
to generate a CA certificate of your own. The advantage of this
approach is that you can distribute this CA certificate to users, who
can install it in their browsers, enabling them to automatically trust
this certificate and any other certificates that you create with that
same CA. This is particularly useful for large companies where you
might have several SSL servers using certificates signed by the same
CA.

Of the arguments listed in the command, one of the most important ones
is the -days argument, which specifies how many days the certificate
will be good for. If you are planning to purchase a commercial
certificate, you should generate your own self-signed key that is good
for perhaps 30 days so that you can use it while you are waiting for
the commercial certificate to arrive. If you are generating a key for
actual use on your server, you may want to make this a year or so, so
that you don't have to generate new keys very often.

The -signkey argument specifies what key will be used to sign the
certificate. This can be either the private key that you generated in
the first step or a CA private key generated with the **CA.pl** script,
as mentioned earlier.

If this step goes well, you should see some output like the following:


.. code-block:: text

   Signature ok
   subject=C = EX, ST = CO, L = Example City, O = Institute of Examples, OU = Demonstration Services, CN = www.example.com, emailAddress = big-cheese@example.com
   Getting Private key


.. _Configuring_the_server_id139081:

Configuring the server
^^^^^^^^^^^^^^^^^^^^^^


Once you have generated the key and certificate, you can use them on
your server using the three lines of configuration shown in the previous
solution.


.. _The_easy_way_id139102:

The easy way
^^^^^^^^^^^^


Now that we've gone through the long and painful way of doing this,
you should know that there is a simpler way. OpenSSL comes with a
handy script, called **CA.pl**, which simplifies the process of creating
keys. The use of **CA.pl** is described in
:ref:`Generating_a_Trusted_CA_id139220` so you can see it in action. It
is useful, however, to know some of what is going on behind the
script. At least, we tend to think so.  It also gives you considerably
more control as to how the certificate is made.


.. _See_Also_id139140:

See Also
~~~~~~~~


* The manpage for the **openssl** tool, **``man openssl``**

* **CA.pl** documentation at
  http://www.openssl.org/docs/apps/CA.pl.html


.. _Generating_a_Trusted_CA_id139220:

Generating a Trusted CA
-----------------------


.. _Problem_id139234:

Problem
~~~~~~~


You want to generate SSL keys that browsers will accept without a
warning message.


.. _Solution_id139289:

Solution
~~~~~~~~


Issue the following commands:


++++++++++++++++++++++++++++++++++++++
<pre id="I_programlisting7_d1e13160" data-type="programlisting">
<code class="prompt">%</code> <strong><code>CA.pl -newca</code></strong>
<code class="prompt">%</code> <strong><code>CA.pl -newreq</code></strong>
<code class="prompt">%</code> <strong><code>CA.pl -sign</code></strong>
<code class="prompt">%</code> <strong><code>CA.pl -pkcs12</code></strong></pre>
++++++++++++++++++++++++++++++++++++++


.. _Discussion_id139326:

Discussion
~~~~~~~~~~


:ref:`Generating_SSL_Certificates_id138549` discusses the lengthy steps
that are required to create keys and sign them. Fortunately, OpenSSL
comes with a script to automate much of this process so that you don't
have to remember all of those arguments. This script, called **CA.pl**,
is located where your SSL libraries are installed, for example,
**/usr/share/ssl/misc/CA.pl**.

The lines in the Solution hide a certain amount of detail, as you will
be asked a number of questions in the process of creating the key and
the certificate. Note also that you will probably need to be in the
directory where this script lives to get successful results from this
recipe.

If you want to omit the passphrase on the certificate so that you
don't have to provide the passphrase each time you start up the
server, use ``-newreq-nodes`` rather than ``-newreq`` when generating
the certificate request.

After running this sequence of commands, you can generate more
certificates by repeating the **-newreq** and **-signreq** commands.

Having run these commands, you will have generated a number of
files. The file **newcert.pem** is the file you specify in your
**SSLCertificateFile** directive, the file **newreq.pem** is your
**SSLCertificateKeyFile**, and the file **demoCA/cacert.pem** is the CA
certificate file, which will need to be imported into your users'
browsers (for some browsers) so that they can automatically trust
certificates signed by this CA. And, finally, **newcert.p12** serves the
same purpose as **demoCA/cacert.pem** for certain other browsers.


.. _Importing_the_CA_id139466:

Importing the CA
^^^^^^^^^^^^^^^^


If your users are using Internet Explorer, you need to create a
special file for them to import. Use the following command:


.. code-block:: text

   openssl X509 -demoCA/cacert.pem -out cacert.crt -outform DER


Then you can send them the **cacert.crt** file.

Clicking on that file will launch the SSL certificate wizard and guide
users through installing the CA certificate into their browser.

Other browsers, such as Mozilla, expect to directly import the
**cacert.pem** file. Users will navigate through their menus (Edit =&gt;
Preferences =&gt; Privacy and Security =&gt; Certificates), then click
on Manage Certificates, then on the Authorities tab, and finally on
Import, to select the certificate file.

After importing a CA certificate, all certificates signed by that CA
should be usable in your browser without receiving any kind of
warning.


.. _See_Also_id139540:


See Also
~~~~~~~~


* The manpage for the **CA.pl** script
* **CA.pl** documentation at
  http://www.openssl.org/docs/apps/CA.pl.html


.. _Serving_a_Portion_of_Your_Site_via_SSL_id139588:

Serving a Portion of Your Site _via_ SSL
----------------------------------------


.. _Problem_id139602:

Problem
~~~~~~~


You want to have a certain portion of your site available **via** SSL
exclusively.


.. _Solution_id139643:

Solution
~~~~~~~~


This is done by making changes to your **httpd.conf** file.

Add a line such as the following:


.. code-block:: text

   Redirect "/secure/" "https://secure.example.com/secure/"


Or:


.. code-block:: text

   <Directory /www/secure>
       SSLRequireSSL
   </Directory>


Note that the **SSLRequireSSL** directive does not issue a redirect. It
merely forbids non-SSL requests.

Or you can accomplish this using ``mod_rewrite``:


.. code-block:: text

   RewriteEngine On
   RewriteCond %{HTTPS} !=on
   RewriteRule ^/(.*) https://%{SERVER_NAME}/$1 [R,L]


.. _Discussion_id139705:

Discussion
~~~~~~~~~~


It is perhaps best to think of your site's normal pages and its
SSL-protected pages as being handled by two separate virtual hosts
rather than one. Although they may point to the same content, they run
on different ports, are configured differently, and, most important,
the browser considers them to be completely separate servers. So you
should, too.

Don't think of enabling SSL for a particular directory; rather, you
should think of it as redirecting requests for one server to another.

Note that the **Redirect** directive preserves path information, which
means that if a request is made for **/secure/something.html**, then the
redirect will be to
**https://secure.example.com/secure/something.html**.

Be careful where you put this directive. Make sure that you only put
it in the HTTP (non-SSL) virtual host declaration. Putting it in the
global section of the **config** file may cause looping, as the new URL
will match the **Redirect** requirement and get redirected itself.

Finally, note that if you want the entire site to be available only
**via** SSL, you can accomplish this by simply redirecting all URLs,
rather than a particular directory:


.. code-block:: text

   Redirect / https://secure.example.com/


Again, be sure to put that inside the non-SSL virtual host declaration.

You will see various solutions proposed for this situation using
**RedirectMatch** or various **RewriteRule** directives. There are special
cases in which this is necessary, but in most cases, the simple
solution offered here works just fine. In particular, you might be
compelled to use this solution when you only have access to your
**.htaccess** file, and not to the main server configuration file.

So, the entire setup might look something like this:


.. code-block:: text

   NameVirtualHost *
   
   <VirtualHost *>
       ServerName regular.example.com
       DocumentRoot /www/docs
   
       Redirect /secure/ https://secure.example.com/secure/
   </VirtualHost>
   
   <VirtualHost _default_:443>
       SSLEngine On
       SSLCertificateFile /www/conf/ssl/ssl.crt
       SSLCertificateKeyFile /www/conf/ssl/ssl.key
   
       ServerName secure.example.com
       DocumentRoot /www/docs
   </VirtualHost>


The other two solutions are perhaps more straightforward, although
they each have a small additional requirement for use.

The second recipe listed, using **SSLRequireSSL**, is
a directive added specifically to address
this need. Placing the **SSLRequireSSL** directive in a particular
**&lt;Directory&gt;** section will ensure that non-SSL accesses to that
directory are not permitted. It does not redirect users to the SSL
host; it merely forbids non-SSL access.

The third recipe, using **RewriteCond** and **RewriteRule** directives,
requires that you have ``mod_rewrite`` installed and enabled. Using
the **RewriteCond** directive to check if the client is already using
SSL, the **RewriteRule** is invoked only if they are not.  In that case,
the request is redirected to a request for the same content but using
HTTPS instead of HTTP.

Note that we strongly advise to use HTTPS for your whole server.


.. _See_Also_id140073:


See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_ssl.html

* http://httpd.apache.org/docs/mod/mod_alias.html

* http://httpd.apache.org/docs/mod/mod_rewrite.html


.. _Authenticating_with_Client_Certificates_id140141:

Authenticating with Client Certificates
---------------------------------------


.. _Problem_id140155:

Problem
~~~~~~~


You want to use client certificates to authenticate access to your
site.


.. _Solution_id140221:

Solution
~~~~~~~~


Add the following ``mod_ssl`` directives to your **httpd.conf** file:


.. code-block:: text

   SSLVerifyClient require
   SSLVerifyDepth 1
   SSLCACertificateFile conf/ssl.crt/ca.crt


.. _Discussion_id140254:

Discussion
~~~~~~~~~~


If you happen to be lucky enough to have a small, closed user
community, such as an intranet, or a Web site for a group of friends
or family, it is possible to distribute client certificates so that
each user can identify himself.

Create client certificates, signing them with your CA certificate
file, and then specify the location of this CA certificate file using
the **SSLCACertificateFile** directive, as shown above.

Client certificates are created in the same manner as server
certificates, except that the CN (Common Name) on the certificate is
the name of the client certificate owner.


.. _See_Also_id140311:

See Also
~~~~~~~~


* :ref:`Generating_SSL_Certificates_id138549`

* http://httpd.apache.org/docs/mod/mod_ssl.html


.. _I_sect17_d1e13480:

SSL Virtual Hosts
-----------------


Problem
~~~~~~~


You want to run several SSL hosts on a single IP address.


Solution
~~~~~~~~


There are several possible answers to this problem, depending on your
perspective.

Server Name Indication (SNI) is the extension to the SSL protocol
to allow to use several SSL hosts on a single IP address. Basically
the client will send the SNI in the Hello TLS message and Apache
httpd will know which certificate/key pair to use for the SSL
encrypted connection.

If not using SNI you can only run one SSL host
**per** IP address and port. This has to do with the way that SSL works,
and is not a limitation specifically of Apache. Attempting to run
multiple SSL hosts on the same IP address and port will result in
warning messages being displayed by the browser, because it will be
receiving the wrong certificate.

One other possible answer is to use a wildcard certificate. This is
covered in the next recipe.

Finally, if you don't care about the warning messages, you can set up
name-based virtual hosts in the usual way, and simply have Apache use
the same certificate for all of them.

Discussion
~~~~~~~~~~


When an https (SSL) request is made by a browser, the first thing that
happens is that the certificate is sent to the browser in order for
the SSL encryption to be set up. This happens before the browser has
told the server what URL it is requesting, in order to fix SNI allows
the client to include the requested hostname in the first message of
the SSL handshake. This allows the server to find the correct named
virtual host and use the corresponding certificate.

There are basically three types of solutions. Either you ignore the
problem, you find a way to use one certificate on multiple hostnames,
or you use more IP addresses or ports. We'll discuss each of these in
turn.


Ignore the problem
^^^^^^^^^^^^^^^^^^


In some situations, you may be content to ignore the problem. For test
servers, or servers where you have a very small audience and can
explain the situation to each person, this may be a perfectly
acceptable scenario.

In that case, you can set up name-based virtual hosts, and use the
same certificate for each one. However, when you connect to any of
them, except for the one for which the hostname matches the Common
Name on the certificate, you will get a warning message from the
browser. In Firefox, this will look like the image below, and will say
something like:

You have attempted to establish a connection with
``www.example1.com``. However, the security certificate presented belogs
to ``www.example2.com``. It is possible, although unlikely, that someone
may be trying to intercept your communication with this Web site. If
you suspect the certificate shown does not belong to
``www.example1.com``, please cancel the connection and notify the site
administrator.

At this point you, the site administrator, know that everything is
fine, and that there's no actual problem. The person on the other end,
however, may have any of a number of different reactions. She may
panic, and press "Cancel" immediately. She might ignore the message
entirely and click "OK," which is almost as bad because ignoring such
warning messages is bound to get one into problems eventually. Or she
may indeed take the suggested action and contact you, the site
administrator. In any of these cases, you probably can immediately see
why this isn't a valid solution when you're running an actual secure
Web site and performing tasks like taking credit card transactions.


Use one certificate on several hosts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


It is possible to use a single certificate on multiple hostnames if
all of those hostnames are in the same domain. This is called a
wildcard certificate, and is discussed in the next recipe.


Use Server Name Indication
^^^^^^^^^^^^^^^^^^^^^^^^^^


The recommended solution is that you use SNI and configure
each virtual host.
Something like:


.. code-block:: text

   NameVirtualHost *:443
   <VirtualHost *:443>
     ServerName www.example.com
     # Other SSL directives here
   </VirtualHost>
   <VirtualHost *:443>
     ServerName www.example2.com
     # Other SSL directives for example2 here
   </VirtualHost>


See Also
~~~~~~~~


* https://wiki.apache.org/httpd/NameBasedSSLVHostsWithSNI

* https://www.ietf.org/rfc/rfc4366.txt


.. _I_sect17_d1e13557:

Wildcard Certificates
---------------------


Problem
~~~~~~~


You want to use a single certificate for multiple hostnames in the
same domain.


Solution
~~~~~~~~


Use a wildcard certificate, which works for any name within a
particular domain, such as "*.example.com."


Discussion
~~~~~~~~~~


Using the technique described in
:ref:`Generating_SSL_Certificates_id138549`, create a certificate with a
Common Name of ``\*.example.com``, where ``example.com`` is the domain for
which you wish to use the certificate. This certificate will now work
for any hostname in the ``example.com`` domain, such as
``www.example.com`` or ``secure.example.com``.

On many browsers, however, the certificate will not work for
``example.com`` or for ``one.two.example.com``, but only for hostnames
strictly of the form ``**hostname**.example.com``.

Most certificate authorities will charge considerably more to sign
wildcard certificates. This is not because it is somehow more
complicated to sign these certificates, but because it is a simple
business decision, based on the fact that buying a wildcard
certificate means that you don't need to buy multiple single-host
certificates.


.. _See_Also_new7:

See Also
~~~~~~~~


* :ref:`Generating_SSL_Certificates_id138549`

Using Let's Encrypt signed certificates
---------------------------------------


Problem
~~~~~~~


You want to use a certificate that is signed by Certificate Authority known by all recent
browsers. Let's Encrypt is a free, automated and open Certicate Authority which is known
by all recent browsers.

Solution
~~~~~~~~


Use Let's Encrypt to sign your certificate.
Let's Encrypt needs that you prove you own the website on which
the certificate is going to be used.
It requires that you have a shell access to the website or that you can
upload a specific file in website. 

Discussion
~~~~~~~~~~


For more details look to 
https://letsencrypt.org/getting-started/. The certifcates
signed by Let's Encrypt are valid for 90 days you can automate the
renewal using mod_md. If you don't want to use mod_md you can renew
your cerficate manually certbot-auto for example. See
https://certbot.eff.org/docs/install.html#certbot-auto
The tools like certbot or certbot-auto provided by the EFF will
add the mod_ssl directives to the Apache httpd configuration
to load the signed Certificate and the corresponding chain.
Install certbot and its apache plugin.
For example (here on fedora/centos, on debian use **apt install**):

++++++++++++++++++++++++++++++++++++++
<pre data-type="programlisting">
<code class="prompt">% </code><strong><code> yum install certbot certbot-apache</code></strong>
</pre>
++++++++++++++++++++++++++++++++++++++

Make sure your Apache httpd server is correctly configured and uses a self signed certificate.
Check :ref:`Generating_SSL_Certificates_id138549` above.
Check that you have a valid **ServeName** directive in your http.conf
Then run **certbot -i apache**

++++++++++++++++++++++++++++++++++++++
<pre data-type="programlisting">
<code class="prompt">% </code><strong><code> certbot -i apache</code></strong>
Saving debug log to /var/log/letsencrypt/letsencrypt.log

How would you like to authenticate with the ACME CA?
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
1: Apache Web Server plugin - Beta (apache)
2: Spin up a temporary webserver (standalone)
3: Place files in webroot directory (webroot)
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Select the appropriate number [1-3] then [enter] (press 'c' to cancel): <strong><code>1</code></strong>
Plugins selected: Authenticator apache, Installer apache
Enter email address (used for urgent renewal and security notices) (Enter 'c' to
cancel): <strong><code>big-cheese@example.com</code></strong>

* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please read the Terms of Service at
https://letsencrypt.org/documents/LE-SA-v1.2-November-15-2017.pdf. You must
agree in order to register with the ACME server at
https://acme-v02.api.letsencrypt.org/directory
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(A)gree/(C)ancel: <strong><code>A</code></strong>

* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Would you be willing to share your email address with the Electronic Frontier
Foundation, a founding partner of the Let's Encrypt project and the non-profit
organization that develops Certbot? We'd like to send you email about our work
encrypting the web, EFF news, campaigns, and ways to support digital freedom.
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: <strong><code>Y</code></strong>

Which names would you like to activate HTTPS for?
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
1: www.example.com
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Select the appropriate numbers separated by commas and/or spaces, or leave input
blank to select all options shown (Enter 'c' to cancel): <strong><code>1</code></strong>
Obtaining a new certificate
Performing the following challenges:
http-01 challenge for www.example.com
Waiting for verification...
Cleaning up challenges
Deploying Certificate to VirtualHost /etc/httpd/conf.d/ssl.conf

Please choose whether or not to redirect HTTP traffic to HTTPS, removing HTTP access.
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
1: No redirect - Make no further changes to the webserver configuration.
2: Redirect - Make all requests redirect to secure HTTPS access. Choose this for
new sites, or if you're confident your site works on HTTPS. You can undo this
change by editing your web server's configuration.
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Select the appropriate number [1-2] then [enter] (press 'c' to cancel): <strong><code>2</code></strong>
Redirecting vhost in /etc/httpd/conf/httpd.conf to ssl vhost in /etc/httpd/conf.d/ssl.conf

* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Congratulations! You have successfully enabled https://www.example.com

You should test your configuration at:
https://www.ssllabs.com/ssltest/analyze.html?d=www.example.com
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/www.example.com/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/www.example.com/privkey.pem
   Your cert will expire on YYYY-MM-DD. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot again
   with the "certonly" option. To non-interactively renew **all** of
   your certificates, run "certbot renew"
 - Your account credentials have been saved in your Certbot
   configuration directory at /etc/letsencrypt. You should make a
   secure backup of this folder now. This configuration directory will
   also contain certificates and private keys obtained by Certbot so
   making regular backups of this folder is ideal.
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le

</pre>
++++++++++++++++++++++++++++++++++++++

So you will receive an email expiry alert from Let's Encrypt so you can renew
your certificate using **certbot renew** before it expires.

In /etc/httpd/conf.d/ssl.conf **certbot** have written something like the
following:


.. code-block:: text

   VirtualHost _default_:443>
   ServerName www.example.com:443
   SSLEngine on
   SSLCertificateFile /etc/letsencrypt/live/www.example.com/cert.pem
   SSLCertificateKeyFile /etc/letsencrypt/live/www.example.com/privkey.pem
   SSLCertificateChainFile /etc/letsencrypt/live/www.example.com/chain.pem
   </VirtualHost>


Note that **SSLCertificateFile** now replaces **SSLCertificateChainFile** so if
you are using a Apache httpd version 2.4.7 or later. **certbot** will use
only **SSLCertificateFile**.

The tool will restart httpd to enable the new certificate.

See Also
~~~~~~~~


* https://letsencrypt.org/getting-started/

* https://certbot.eff.org/docs/install.html#certbot-auto

Using Let's Encrypt with mod_md
-------------------------------


Problem
~~~~~~~


Let's Encrypt certificates are valid for 90 days, so each 90 days
you have to renew your certificates and use certbot-auto or a manual
process to keep your Apache httpd up to date.

Solution
~~~~~~~~


One of the solutions is to use _mod_md_.
_mod_md_ allows to do update you Let's Encrypt certificate automaticly.

Discussion
~~~~~~~~~~


You have to install mod_md, if you are build Apache httpd on your own
you have to add the option **--enable-md** to
the **./configure** parameters.
mod_md is easy to configure, in httpd.conf you have to add something like:


.. code-block:: text

   MDomain www.example.com
   MDCertificateAgreement URL to Let's encrypt Term of Service.
   
   <VirtualHost _default_:443>
   ServerName www.example.com:443
   SSLEngine on
   </VirtualHost>
   


You need to add a **MDCertificateAgreement** directive pointing to Let's Encrypt
current Terms of Service. The Terms of Service might change the actual version
is https://letsencrypt.org/documents/LE-SA-v1.2-November-15-2017.pdf

So the whole configuration at the time of the writing is:


.. code-block:: text

   MDomain www.example.com
   MDCertificateAgreement https://letsencrypt.org/documents/LE-SA-v1.2-November-15-2017.pdf
   
   <VirtualHost _default_:443>
   ServerName www.example.com:443
   SSLEngine on
   </VirtualHost>
   


If the link to the Terms of Service has changed you will get a message like:

++++++++++++++++++++++++++++++++++++++
<pre data-type="programlisting">
[Tue Mar 05 16:59:26.723162 2019] [md:error] [pid 17783:tid 3052403520] (70008)Partial results are valid but processing is incomplete: www.example.com: the CA requires you to accept the terms-of-service as specified in &#60;https://letsencrypt.org/documents/LE-SA-v1.2-November-15-2017.pdf&#62;. Please read the document that you find at that URL and, if you agree to the conditions, configure "MDCertificateAgreement url" with exactly that URL in your Apache. Then (graceful) restart the server to activate.
</pre>
++++++++++++++++++++++++++++++++++++++


Adjust httpd.conf and Restart httpd and let's encrypt certificate will be installed.
You get something like:

++++++++++++++++++++++++++++++++++++++
<pre data-type="programlisting">
[Tue Mar 05 17:07:24.269380 2019] [md:notice] [pid 18157:tid 3054275392] AH10059: The Managed Domain www.example.org has been setup and changes will be activated on next (graceful) server restart.
</pre>
++++++++++++++++++++++++++++++++++++++


Restart httpd one more time and it will using your certificate signed by Let's Encrypt.
mod_md will then trigger automatic update of the certicate before it expires.

See Also
~~~~~~~~


* https://letsencrypt.org

* https://datatracker.ietf.org/doc/draft-ietf-acme-acme/

Using HTTP/2 with mod_ssl and mod_http2.
----------------------------------------


Problem
~~~~~~~


You want the modern and recent browsers to render you pages as fast as possible.

Solution
~~~~~~~~


The protocol HTTP/2 allows to multiplex HTTP/1.1 connection in order to
reduce the latency when displaying a page on a browser.
HTTP/2 in the browser requires TLS 1.2, the browser in the Hello TLS will
list the protocol it is supporting. The Web server can do HTTP/2 if mod_http2
is configured and enabled. Note that mod_http2 requires additional threads and
resources, make you have space for those before enabling HTTP/2


Discussion
~~~~~~~~~~


You have to install mod_http2, if you are build Apache httpd on your own
you have to add the option **--enable-http2** to
the **./configure** parameters. Note that you need install libnghttp2 too. 

The basic of mod_http2 are easy to configure, in httpd.conf you have to add something like:


.. code-block:: text

   <VirtualHost _default_:443>
     Protocols h2 http/1.1
   </VirtualHost>


See Also
~~~~~~~~


* https://http2.github.io/faq/

* https://tools.ietf.org/html/rfc7540

* https://httpd.apache.org/docs/2.4/mod/mod_http2.html

* https://en.wikipedia.org/wiki/Application-Layer_Protocol_Negotiation

Summary
-------


TLS/SSL supported via _mod_ssl_ and the libraries provided by **OpenSSL** allows to
make sure your content is protected from a third party listening to the traffic going past
as weel as make sure that your Web site will accessible to eveyone using recent browsers.

