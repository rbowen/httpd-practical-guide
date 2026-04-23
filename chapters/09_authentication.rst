
.. _Chapter_AAA:

=================================================
Authentication, Authorization, and Access Control
=================================================

.. index:: AAA

.. index:: Authentication

.. index:: Authorization

.. index:: Access Control

.. index:: Security

.. index:: Password

.. index:: Username

.. index:: Logging in


A lot of topics fit under the heading of 'Security'. One of these is
covered in this chapter, while others are covered in the following
chapters, :ref:`Chapter_Security`, **Security**, and
:ref:`Chapter_SSL_and_TLS`, **SSL and TLS**.

In this chapter we discuss the topics of Authentication,
Authorization, and Access Control - topics that are 
distinct, but closely related and interconnected.

In this chapter, security means allowing people to see what you
want them to see and preventing them from seeing what you don't want them
to see. Additionally, there are the issues of what measures you need to
take on your server in order to restrict access **via** non-Web means. This
chapter illustrates the precautions you need to take to protect your
server from malicious access and modification of your Web site.

The most common questions ask how to protect documents and restrict
access. Unfortunately, because of
the complexity of the subject and the nature of the Web architecture,
these questions also tend to have the most complex answers or often no
convenient answers at all.

Normal security nomenclature and methodology separate the process of
applying access controls into two
discrete steps; in the case of the Web, they may be thought of as the
server asking itself these questions:

* Are you really who you claim to be?

* Are you allowed to be here?

These steps are called authentication and
authorization, respectively. Additionally, access control refers to
restricting access to a resource based on some other criteria,
possibly unrelated to your identity.

Here's a real-world
example: flight attendant checks your photo identification
(authentication) and your ticket (authorization) before permitting you to
board an airplane. However, he won't admit you until it's time to
board (access control).

Authentication can be broken down into what might be called
weak and strong. Weak
authentication is based on the correctness of credentials that the end
user supplies, which therefore may have been stolen from the real
owner. Hence the name "weak". Whereas strong authentication is based on
attributes of the request over which the end user has little or no
control, and it cannot change from request to request—such as the IP
address of her system, or her fingerprints.

Recipes in this chapter show you how to implement some of the
frequently requested password scenarios, as well as various ways to
restrict access from malicious or otherwise undesirable clients.


.. _Authentication_and_Authorization_sidebar:


.. sidebar:: Authentication and Authorization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   When checking for access to restricted documents, there are
   actually two different operations involved: checking to see who you are,
   and checking to see if you're allowed to see the document. Just like
   in the example of boarding a plane, earlier.
   
   The Web server doesn't know who you are, so you need to provide some proof of your identity, such as a
   username and matching password. This is the authentication step. When the server successfully compares
   these bits of information (called credentials)
   with those in its databases, the server will proceed, but if you're not
   in the list, or the information doesn't match, the server will turn you
   away with an error status.
   
   Once you have convinced the server you are who you say you are, it
   will look at the list of people allowed to access the document and see
   if you're on it; this is called authorization. If
   you are on the list, access proceed normally; otherwise, the server
   returns an error status and denies access.
   
   Regardless of which of the two steps failed, you'll receive the same
   error condition back on the client side.
   It is always a 401 (unauthorized) code, even if the failure
   was in authentication. This is to prevent would-be attackers from being
   able to tell when they have valid credentials, but just don't happen
   to be allowed to see that particular resource.
   


.. _Recipe_Basic_Auth:

Configuring Basic Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: Basic Authentication

.. index:: Authentication,Basic

.. index:: mod_auth_basic

.. index:: Modules,mod_auth_basic

.. index:: mod_authn_file

.. index:: Modules,mod_authn_file


.. _Problem_Basic_Auth:

Problem
~~~~~~~


You want to trigger a pop-up password dialog and validate the username
and password provided.


.. _Solution_Basic_Auth:

Solution
~~~~~~~~


For the directory you wish to protect, use the following
configuration:


.. code-block:: text

   <Directory /var/www/private>
     AuthType Basic
     AuthName "Restricted Files"
     # (Following line optional)
     AuthBasicProvider file
     AuthUserFile "/usr/local/apache/passwd/passwords"
     Require user rbowen
   </Directory>


.. _Discussion_Basic_Auth:

Discussion
~~~~~~~~~~


There's a lot packed into this short example, and several lines
require another example to further explain and elaborate.

In the example, we apply password protection to a directory
``/var/www/private``. Thus, any HTTP request that results in a file
being served from that directory will result in a standard
authentication dialog being raised in the browser, and the username
and password provided by the user being validated against the file
``/usr/local/apache/passwd/passwords``.


.. _basic_auth_img:


.. figure:: ../images/401_prompt.png
   :alt: Basic password dialog

   Basic password dialog


This is accomplished by the server sending a ``401 Unauthorized`` status
code to the client. This functionality is provided by the module
``mod_auth_basic``.

If the credentials supplied are deemed valid, then the resource will
be served. If not, then the server will once again return a `401
Unauthorized` response, and the process will be repeated.

You can also apply authentication to resources other than a directory.
For example, to authenticate a particular URL, you can use a
``<Location>`` container instead:


.. code-block:: text

   <Location /admin>
     AuthType Basic
     AuthName "Restricted Files"
     AuthBasicProvider file
     AuthUserFile "/usr/local/apache/passwd/passwords"
     Require user rbowen
   </Location>


Similarly, you can use ``<Files>``, or the various ``Match`` directives,
``<DirectoryMatch>``, ``<LocationMatch>``, and ``<FilesMatch>`` for
pattern-matched groups of resources.

These directives may also be placed directly into a ``.htaccess`` file,
without the surrounding container, in order to require authentication
for every request to that directory.

The value specified in the ``AuthName`` directive is sent to the client
as part of the authentication request, and appears in the password
dialog, in order to give the end-user some idea of what they are
logging in to. It is also used by the client to cache the provided
password locally on the client, for the duration of the authenticated
session, so that the credentials don't have to be requested for every
subsequent HTTP request.

The ``AuthBasicProvider`` directive, and the associated ``AuthUserFile``
directive, tells ``mod_auth_basic`` which authentication back-end to
delegate to (in this case, we used the ``file`` back-end, provided by
the module ``mod_authn_file``), and the specific password catalog to
validate against (in this case, the file
``/usr/local/apache/passwd/passwords``).

Details about how to create that password file may be found in
:ref:`Recipe_htpasswd`, later in this chapter.

``file`` is the default argument for ``AuthBasicProvider``, and is assumed
if that directive is omitted. You can, alternatively, delegate
password validation to a number of outer providers, including DBM
files, an SQL database, or LDAP, as well as numerous third-party
authentication modules.

The three authentication methods mentioned above are discussed in more
detail in the recipes :ref:`Recipe_dbm_auth`, :ref:`Recipe_sql_auth`, and
:ref:`Recipe_ldap_auth`, later in this chapter.

Finally, the ``Require`` directive tells the authentication back-end
which username, or usernames, are permitted access to this resource.
In this example, we require a username of ``rbowen``. You can also
specify several allowed username:


.. code-block:: text

   Require user rbowen irwinter mlpony


Or, if you want to permit any valid username that's listed in the
authentication store, use the ``valid-user`` keyword:


.. code-block:: text

   Require valid-user


Finally, you can put users into groups, and then require a particular
group. That's discussed in the recipe
:ref:`Recipe_authentication_groups`.


.. warning::

   When using Basic authentication, the username and password are passed
   plaintext (that is, unencrypted) across the HTTP connection. Anyone
   that is intercepting this HTTP traffic, for example on a public WiFi
   network, would be able to see your username and password. Therefore,
   we do not recommend that you use Basic authentication for highly
   sensitive resources, unless you also use SSL or TLS to encrypt the
   connection over which the resource is requested and returned. See
   :ref:`Chapter_SSL_and_TLS`, **SSL and TLS**, for further discussion of using encrypted
   communications.


.. _See_Also_Basic_Auth:

See Also
~~~~~~~~


* :ref:`Recipe_htpasswd`

* :ref:`Recipe_authentication_groups`

* :ref:`Recipe_dbm_auth`

* :ref:`Recipe_ldap_auth`

* :ref:`Recipe_sql_auth`


.. _HTTP_Browsers_and_Credentials_sidebar:

.HTTP, Browsers, and Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. sidebar:: Sidebar

   It is easy to draw incorrect conclusions about the behavior of
   the Web; when you have a page displayed in your browser, it is
   natural to think that you are still connected to that site. In
   actuality, however, that's not the case—once your browser fetches
   the page from the server, both disconnect and forget about each
   other. If you follow a link, or ask for another page from the same
   server, a completely new exchange has begun.
   
   When you think about it, this is fairly obvious. It would make
   no sense for your browser to stay connected to the server while you
   went off to lunch or home for the day.
   
   Each transaction that is unique and unrelated to others is
   called stateless, and it has a bearing on how
   HTTP access control works.
   
   When it comes to password-protected pages, the Web server
   doesn't remember whether you've accessed them before or not. Down at
   the HTTP level where the client (browser) and server talk to each
   other, the client has to prove who it is every time; it's the
   **client** that remembers your information.
   
   When accessing a protected area for the first time in a
   session, here's what actually gets exchanged between the client and
   the server:
   
   
   . The client requests the page.
   
               
   . The server responds, "You are not authorized to access
                 this resource (a ``401 unauthorized`` status). This
                 resource is part of authentication realm
                 **``XYZ``**." (This information is conveyed
                 using the ``WWW-Authenticate``
                 response header field; see RFC 2616 for more
                 information.)
               
   .  If the client isn't an interactive browser, at this point
                 it probably goes to step 7. If it is interactive, it asks the
                 user for a username and password, and shows the name of the
                 realm the server mentioned.
               
   . Having gotten credentials from the user, the client
                 reissues the request for the document—including the credentials
                 this time.
   
               
   .  The server examines the provided credentials. If they're
                 valid, it grants access and returns the document. If they
                 aren't, it responds as it did in step 2.
    
   . If the client receives the unauthorized response again, it
                 displays some message about it and asks the user if he wants to
                 try entering the username and password again. If the user says
                 yes, the client goes back to step 3.
               
   . If the user chooses not to reenter the username and
                 password, the client gives up and accepts the "unauthorized"
                 response from the server.
   
   
   Once the client has successfully authenticated with the
             server, it remembers the credentials, URL, and realm involved.
             Subsequent requests that it makes for the same document or one
             "beneath" it (**e.g.**, **/foo/bar/index.html** is "beneath"
             **/foo/index.html**) causes it to
             send the same credentials automatically. This makes the process
             start at step 4, so even though the challenge/response exchange is
             still happening between the client and the server, it's hidden from
             the user. This is why it's easy to get caught up in the fallacy of
             users being "logged on" to a site.
   
   This is how all HTTP weak authentication works. One of the
             common features of most interactive Web browsers is that the
             credentials are forgotten when the client is shut down. This is why
             you need to reauthenticate each time you access a protected document in a new browser
             session.


.. _Recipe_htpasswd:

Creating password files for Basic authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: Basic Authentication,Password file

.. index:: Authentication,Basic,Password file

.. index:: htpasswd

.. index:: Commands,htpasswd

.. index:: Passwords

.. index:: Password files,Basic


.. _Problem_htpasswd:

Problem
~~~~~~~


You need to create a password file to be used for Basic
authentication.


.. _Solution_htpasswd:

Solution
~~~~~~~~


Use the ``htpasswd`` utility, provided with your Apache http server, to
create and manage the password file.

To create a new password file, type the following at the command line:


.. code-block:: text

   htpasswd -c passwordfile rbowen


To add a password to an existing password file, omit the ``-c`` flag:


.. code-block:: text

   htpasswd passwordfile irwinter


In each case, you'll be promoted for the password, which will be
encrypted and added to the specified password file.


.. _Discussion_htpasswd:

Discussion
~~~~~~~~~~


The ``htpasswd`` utility is provided with your http server, and is used
to manage the text password catalog that is used by ``mod_authn_file``
to validate credentials passed from the client during Basic
authentication. See :ref:`Recipe_Basic_Auth` for further discussion of
implementing Basic authentication.

When you type the commands in the example above, you'll be promoted
for the password. You'll then be prompted for the password again, to
ensure that you typed it correctly the first time. The password will
not be shown as you type it, so that someone standing behind you can't
see what you're typing.


.. code-block:: text

   $ htpasswd -c passwordfile rbowen
   New password: 
   Re-type new password: 
   Adding password for user rbowen


If the passwords typed do not match, you'll get an error message, and
the password file will not be modified:


.. code-block:: text

   htpasswd: password verification error


When a password is added successfully, the resulting password file
will look like this:


.. code-block:: text

   rbowen:$apr1$MjNPPX0n$o9z6INJz4VY2/ym1QN4V10
   irwinter:$apr1$3oRpmxfa$m8VeLpEJv.XronAqvL4j90
   mlpony:$apr1$P.Mb010e$Sbqxy9w75udS0CkrNdKP41


Each line consists of three parts:

First is the username, stored plaintext as it was provided.

Next is the salt, which is between ``$apr1$`` and the next occurance of
``$``. The salt is randomly generated data that is used to make the
encrypted password more difficult to revese-engineer. It is needed as
part of the password validation process, and so is stored here.

For example, in the ``rbowen`` line, the salt is ``MjNPPX0n``.

Finally, there's the password, hashed (encrypted) using the MD5
algorithm. This is a one-way calculation. That is, someone who obtains
your password file cannot determine the passwords, except by a brute
force approach of guessing passwords.

The ``htpasswd`` utility provides several other options in addition to
the defaults. For example, you can use other encryption algorithms
using various command-line flags:


.. _htpasswd-options:

.htpasswd Options

+------+-------------------------------------------+
| Flag | Meaning                                   |
+------+-------------------------------------------+
| -m   | MD5 (This is the default)                 |
+------+-------------------------------------------+
| -B   | Use bcrypt encryption (very secure)       |
+------+-------------------------------------------+
| -d   | Use CRYPT (8 chars max, insecure)         |
+------+-------------------------------------------+
| -s   | Use SHA encryption (insecure)             |
+------+-------------------------------------------+
| -p   | Use plaintext for the password (insecure) |
+------+-------------------------------------------+


Type ``htpasswd`` at the command line without arguments to see all of
the available options.


.. warning::

   Ensure that the password file is located outside of the document
   directory. A password file in the document directory could potentially
   be downloaded, and then used to assist in a brute force password
   attack.


Note that it is very slow to search through a text password file. If
you have more than just a handful of users listed in a password file,
it may be useful to consider storing your passwords in some kind of
database, such as either a dbm file or an actual SQL database. See
recipes :ref:`Recipe_sql_auth`, :ref:`Recipe_dbm_auth`, and
:ref:`Recipe_ldap_auth` for further suggestions.


.. _See_Also_htpasswd:

See Also
~~~~~~~~


* :ref:`Recipe_Basic_Auth`

* :ref:`Recipe_sql_auth`

* :ref:`Recipe_dbm_auth`

* :ref:`Recipe_ldap_auth` 

* http://httpd.apache.org/docs/programs/htpasswd.html

* Type ``htpasswd`` without arguments for a full list of options.


.. _Recipe_Cracking_passwd:

Cracking passwords in a htpasswd file

.. index:: Cracking passwords

.. index:: htpasswd,cracking


.. _Problem_Cracking_passwd:

Problem
~~~~~~~


You have a htpasswd file, and need to determine the passwords that are
in it.


.. _Solution_Cracking_passwd:

Solution
~~~~~~~~


Use the utility John the Ripper to crack passwords.


.. _Discussion_Cracking_passwd:

Discussion
~~~~~~~~~~


``john``, or John the Ripper, is a password cracking utility which is
freely available on every major operating system. It is, by no means,
the only password cracking utility, but is one that we recommend, as
it is fast, easy to use, and free.

However, note that if the passwords are good ones, they're not going
to be easily crackable.

John uses a variety of different approaches, starting with word lists,
and getting more complex as it goes along. If your passwords use
common words or phrases, it will guess them fairly quickly. If you use
random passwords, it will take much longer, and may never guess them
at all.


.. tip::

   John can take hours, or even days, to crack passwords, as it is doing
   it by brute force - that is, but progressively trying more and more
   complicated strings until something matches.


.. _See_Also_Cracking_passwd:

See Also
~~~~~~~~


* http://www.openwall.com/john/

* :ref:`Recipe_good_passwords`


.. _Recipe_good_passwords:

Generating strong passwords
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: Passwords,strong

.. index:: Generating strong passwords


.. _Problem_good_passwords:

Problem
~~~~~~~


You want to use passwords that are hard, or impossible, to crack.


.. _Solution_good_passwords:

Solution
~~~~~~~~


We recommend using a tool such as ``pwgen`` to generate passwords that
are both hard to guess, and easy to remember. ``pwgen`` generates
passwords that appear random, but which are pronounceable, so that
they're easy to remember.


.. _Discussion_good_passwords:

Discussion
~~~~~~~~~~


Generating passwords that are both strong enough to not be easily
cracked, but which you can remember, is something of an art. You want
to avoid things that people - or computers - are likely to guess
first, such as common words or phrases, and anything that is short or
predictable.

``pwgen``, when run with no arguments, produces output that looks like:


.. code-block:: text

   dohx1Eo4 ki0cei4S Bu6ohqu8 sae6joKu aiTea9ee ShaeFah0 Ceph0sha haJe4sa0
   Fahya8up Vohzuiz0 ei8ieThu ooFoc5ph ees9Vox6 fee4Jiez tieYai4G doiwoo8P
   MeiRah9b xaiB8shi hae0eiSh Ijoh1Eit jahGh8ai eegah4Ko Ahfahw6a lailah0A
   eew7miPi nusuco0E meeV3voo vut8lu8H tu3Feeng oomePhu0 Eishohd7 Aik0veev
   ohx4ua3R aiPheew3 Amoof6hi Fief0no0 xe8veiVo Eipeit1u enguu8Ai The2oon0
   Pae6auch Naewuu0i XahTuow0 iGe5ieya eeB2othi uf4ooC2r Fiu6sai5 oo7Viedu
   riexei8K Jaitu5ai feing7Au Thee6aid Oom1aiqu ya6ohPee UqueSh8r oo3thooT
   ax7aeSh2 Amieko3a tai2wa3T Eup1teez Eegun1La eec1uCah ahch5Cha ohCh9ubo
   ou6Neimo haiT5ohS ohngu8Ah eiGh4oat Pei3phoo eeVai4pu eef7aMei Haix4zor
   xeV7ay2E Loobo7ie ur0cheiY ufuk6Oht phee7Quu iephiS4I yi2chu5W ooTh5cah
   anaize8V aigh1ieF beThai3J chevos7M aht2Kail ohWohr4F joKaeC6e dee6Oepo
   aChoPh5z ied1queY did4Loot Elae1jei veiz7Hee oB3vohd9 iejeiMu8 aiB1neeg
   phai3Coh ogaix5Oo ZueCai4K TohfahJ5 Oohair3b Phoh9fee quun3Die wij0Iemi
   daijui3X caiX3ut4 tho4Ahb6 xoonohW5 Ju2quai6 Iqu5jei2 eenoh4Ro fo1Loo1t
   ouH2aik4 ach9Eiwu Ahngu6ae Izoh7eek ahk9vohH oSooNg1O al0OyohV eeLa3eex
   aisohPh3 weSh6iex geib8Tei xelexoX4 Ye8keeH1 toa6iaSe kah3AeJi Mingi6th
   ohth6Sho eu5Tahvu Chauf7ye eeDie5ch Oom5rohh noh6Ooci Quaiqu7V aSh5Oofa
   UC3im8ee Je5ahbee ouf2EeXu Yiij9ahs eiShoh7L yoo3ooCh eew8Aeti eeHieh4u
   zoDeeb2e Xee5jie9 Quedoh8C ahXoo6pa Pulae2yu iCh0hohK Ifiewai1 WauXo4ui
   ooz6Aef8 yesen5Ee quahS9di Er9aiWae phae7eeT Acuoz6uc ahp5Ei1m choo0Pho


You will then pick one of these passwords and use it for your
password. They are phonetically pronounceable - for example, if you
were to pick ``did4Loot``, you'd remember this phoenetically as "did for
Loot", and ``ya6oPee`` would be "ya six oh Pee".

Multiple passwords are shown so that someone watching over your
shoulder would never know which one you picked.

You can also provide various command line options to change the
composition of the passwords:


.. code-block:: text

   Usage: pwgen [ OPTIONS ] [ pw_length ] [ num_pw ]
   
   Options supported by pwgen:
     -c or --capitalize
   	Include at least one capital letter in the password
     -A or --no-capitalize
   	Don't include capital letters in the password
     -n or --numerals
   	Include at least one number in the password
     -0 or --no-numerals
   	Don't include numbers in the password
     -y or --symbols
   	Include at least one special symbol in the password
     -s or --secure
   	Generate completely random passwords
     -B or --ambiguous
   	Don't include ambiguous characters in the password
     -h or --help
   	Print a help message
     -H or --sha1=path/to/file[#seed]
   	Use sha1 hash of given file as a (not so) random generator
     -C
   	Print the generated passwords in columns
     -1
   	Don't print the generated passwords in columns
     -v or --no-vowels
   	Do not use any vowels so as to avoid accidental nasty words


Thus, if a particilar application or website has certain password
requirements, you can adjust accordingly. Longer passwords are harder
to guess. Including special characters (**i.e.**, ``#``, ``$``, ``&``, and so on)
make it even harder to guess, but potentially harder to pronounce -
and therefore remember - too.

This is not the only password generator. There are many of
them, both available as command line utilities, and online tools. It's
just the one we particularly like.

Another useful technique is to take a familiar phrase, such as "in the
beginning God created the heavens and the earth", and compose a
password based on the first letter of each word in the phrase - in
this case, ``1tbGcth&t3``. (Don't use that specific password, of course,
because now it's right there in print.)


.. _See_Also_good_passwords:

See Also
~~~~~~~~


* ``man pwgen``

* https://linux.die.net/man/1/pwgen


.. _Recipe_authentication_groups:

Authentication Groups
~~~~~~~~~~~~~~~~~~~~~

.. index:: Authentication,Groups

.. index:: Basic Authentication,User groups

.. index:: mod_authz_groupfile

.. index:: Modules,mod_authz_groupfile

.. index:: Modules,mod_authz_groupfile


.. _Problem_authentication_groups:

Problem
~~~~~~~


Rather than specifying all of the permitted usernames in the ``Require``
directive, you'd like to maintain a group list in an easier-to-edit
format.


.. _Solution_authentication_groups:

Solution
~~~~~~~~


Use the ``Require group`` syntax to specify a group name, and maintain
the group list in a separate file.


.. code-block:: text

   AuthGroupFile /etc/httpd/passwords/auth_groups
   Require group admin


The file ``auth_groups`` should contain an ``admin`` line listing members
of that group:


.. code-block:: text

   admin: rbowen irwinter mlpony humbedooh


.. _Discussion_authentication_groups:

Discussion
~~~~~~~~~~


When your authentication group has more than a few members, it becomes
rather inconvenient to maintain that list in the server configuration
file. The ``AuthGroupFile`` directive allows you to put that user list
in a group file.


.. warning::

   The group file should be stored outside of your document directory, so
   that an attacker has no opportunity to download the group file to
   determine which users to focus on.


The group file itself is a plaintext file, listing groups, and their
members. A group file may have as many groups in it as you like.


.. code-block:: text

   admin: rbowen irwinter mlpony humbedooh
   marketing: sk rbowen rgardler
   infra: humbedooh pono mcduck


.. tip::

   Searching text group file can be very slow. If your groups are more
   than a handful of members, consider putting your groups in an actual
   database, such as either a dbm file or a SQL database. See
   :ref:`Recipe_dbm_group_file` for more discussion of this.


.. _See_Also_authentication_groups:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_authz_groupfile.html

* :ref:`Recipe_dbm_group_file`


.. _Recipe_Digest_Auth:

Configuring Digest Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: Digest Authentication

.. index:: Authentication,Digest

.. index:: mod_auth_digest

.. index:: Modules,mod_auth_digest


.. _Problem_Digest_Auth:

Problem
~~~~~~~


You want something more secure than Basic authentication, and want to
confige Digest authentication for username/password logins.


.. _Solution_Digest_Auth:

Solution
~~~~~~~~


Configure Digest authentication, using ``mod_auth_digest`` with the
following configuration:


.. code-block:: text

   <Location "/private/">
       AuthType Digest
       AuthName "Top Sekrit"
       AuthDigestDomain "/private/" "http://mirror.my.dom/private2/"
       
       AuthDigestProvider file
       AuthUserFile "/etc/httpd/passwords/digest_users"
       Require valid-user
   </Location>


.. _Discussion_Digest_Auth:

Discussion
~~~~~~~~~~


Digest authentication is a step more secure than Basic authentication
(See :ref:`Recipe_Basic_Auth`), in that the username and password are not
passed across the HTTP connection in plaintext, and, thus, the casual
observer on your public WiFi connection can't intercept your login
credentials.

Unfortunately, due to a variety of historical reasons, Digest
authentication never enjoyed the popularity of Basic authentication.
In particular, many popular browsers didn't support Digest until very
late, and, meanwhile, form-based authentication has become the norm.


Unlike Basic authentication, when you use Digest authentication the
password isn't passed across the connection in cleartext. Rather, a
**digest** (a cryptographic combination) of the username, password, and
authentication realm, is passed, making it harder, although not
impossible, to intercept.


.. warning::

   While Digest is indeed more secure than Basic, in the sense that a
   casual network sniffer can't intercept your username and password, it
   is still insecure in the sense that a decicated hacker can intercept
   enough information to hijack your login session. As with Basic
   authentication, it is strongly recommended that sensitive parts of
   your web presence be security with TLS. See :ref:`Chapter_SSL_and_TLS`,
   **SSL and TLS**,
   for more details.


In the example given, we are protecting a location ``/private/``, using
a password file stored at ``/etc/httpd/passwords/digest_users``. The
technique for creating that digest password file is discssed in
:ref:`Recipe_htdigest` later in this chapter.

The ``AuthDigestDomain`` directive lists locations that are protected by
this configuration. This allows the client to cache credentials and
reuse them, without additional prompting, when a resource is requested
from one of these other locations.

See :ref:`Recipe_htdigest` for details on how to create the password file
specified in the ``AuthUserFile`` directive.


.. _See_Also_Digest_Auth:

See Also
~~~~~~~~


* :ref:`Recipe_htdigest`

* http://www.faqs.org/rfcs/rfc2617.html

* :ref:`Recipe_Basic_Auth`


.. _Recipe_htdigest:

Managing password files for Digest authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: Digest Authentication

.. index:: Authentication,Digest

.. index:: mod_auth_digest

.. index:: Modules,mod_auth_digest

.. index:: Password files,Digest

.. index:: Paswords

.. index:: htdigest

.. index:: Commands,htdigest


.. _Problem_htdigest:

Problem
~~~~~~~


You need to create a password file to be used for Digest
authentication


.. _Solution_htdigest:

Solution
~~~~~~~~


Use the ``htdigest`` utility, provided with your Apache http server, to
create and manage the password file.

To create a new password file, type the following at the command line:


.. code-block:: text

   htdigest -c digest_users "Private" marguerite


To add a password to an existing password file, omit the ``-c`` flag:


.. code-block:: text

   htdigest digest_users file "Private" rhiannon


In each case, you'll be promoted for the password, which will be
encrypted and added to the specified password file.


.. _Discussion_htdigest:

Discussion
~~~~~~~~~~


As discussed in :ref:`Recipe_Digest_Auth`, Digest authentication is
intended to be a little more secure than Basic authentication, in that
the username and password are not passed across the internet in
plaintext.

As with Basic authentication, you must create a password file, against
which the provided username and password can be validated. Unlike
Basic authentication, passwords are tied to a particular realm, or
``AuthName``, to provide an additional layer of security. Thus, this
additional information is required when you create entries in that
password file.

Entries in the Digest password file look like:


.. code-block:: text

   rhiannon:Private:280898f80d9a270493e545e2d2de5524


That is, they consist of the username, the realm (``AuthName``), and the
encrypted (hashed) password.

This file may then be referenced as shown in the recipe in
:ref:`Recipe_Digest_Auth`, above.


.. _See_Also_htdigest:

See Also
~~~~~~~~


* :ref:`Recipe_Digest_Auth`

* http://httpd.apache.org/docs/programs/htdigest.html

* http://httpd.apache.org/docs/mod/mod_auth_digest.html

* :ref:`Recipe_htpasswd`


.. _Recipe_Form_Auth:

[role="v24"]
Form-based authentication

.. index:: Authentication,Form

.. index:: Form authentication

.. index:: mod_auth_form

.. index:: Modules,mod_auth_form

.. index:: mod_session

.. index:: Modules,mod_session

.. index:: mod_session_cookie

.. index:: Modules,mod_session_cookie


.. _Problem_Form_Auth:

Problem
~~~~~~~


You wish to implement form-based authentication.


.. _Solution_Form_Auth:

Solution
~~~~~~~~


In Apache httpd 2.4 and later, a module named ``mod_auth_form`` is
available which implements form-based authentication. To use it, you
must load both ``mod_auth_form``, ``mod_session``, and
``mod_session_cookie``, and implement the following configuration:


.. code-block:: text

   <Location /admin >
     AuthType form
     AuthFormLoginRequiredLocation "http://example.com/login.html"
     AuthFormProvider file
     AuthUserFile "conf/passwd"
     AuthName /admin
   
     Session On
     SessionCookieName admin-session path=/
   </Location>


The password file, specified by the ``AuthUserFile`` directive, should
be created using the ``htpasswd`` utility, as described in
:ref:`Recipe_htpasswd`.


.. tip::

   The file path for the password file is assumed to be relative to your
   server root (not the document root!) unless you provide a full path.
   In this case, for example, my server root is ``/etc/httpd``, so the
   password file is located at ``/etc/httpd/conf/passwd``.


At the location specified by the ``AuthFormLoginRequiredLocation``
directive, put an HTML form with the following field names:


.. code-block:: text

   <form method="POST" action="/dologin.html">
     Username: <input type="text" name="httpd_username" value="" />
     Password: <input type="password" name="httpd_password" value="" />
     <input type="submit" name="login" value="Login" />
   </form>


.. tip::

   The login form should be outside of the password-protected area,
   otherwise the unauthenticated user won't be able to reach it to log
   in.


Finally, configure a location for the ``POST`` action:


.. code-block:: text

   <Location "/dologin.html">
     SetHandler form-login-handler
   
     AuthType form
     AuthName /admin
     AuthFormLoginRequiredLocation "http://example.com/login.html"
     AuthFormLoginSuccessLocation "http://example.com/admin/index.html
     AuthFormProvider file
     AuthUserFile "conf/passwd"
   
     Session On
     SessionCookieName admin-session path=/
   </Location>


.. _Discussion_Form_Auth:

Discussion
~~~~~~~~~~


Form-based authentication has a lot of parts that must be configured,
which make this recipe seem somewhat complicated. So, we'll take each
step individually. These steps are:

* Enable the necessary modules
* Create an authenticated area
* Create the login form
* Create the login action handler
* Create password file to validate against

Enabling modules
^^^^^^^^^^^^^^^^


First of all, form authentication requires several modules that are
typically not enabled by default: ``mod_auth_form``, ``mod_session``,
``mod_session_cookie``, and, optionally, ``mod_session_crypto``.

To enable these modules in Debian (and Ubuntu):


.. code-block:: text

   sudo a2enmod session
   sudo service apache2 restart


To enable them in Fedora (and CentOS, and RHEL):


.. code-block:: text

   sudo yum install mod_session
   sudo service httpd restart


Or, if you installed some other way, you can enable these modules by
adding (or uncommenting) the relevant ``LoadModule`` directives:


.. code-block:: text

   LoadModule session_module modules/mod_session.so
   LoadModule session_cookie_module modules/mod_session_cookie.so
   LoadModule auth_form_module modules/mod_auth_form.so
   
   # Optional:
   # LoadModule session_crypto_module modules/mod_session_crypto.so


The authenticated area
^^^^^^^^^^^^^^^^^^^^^^


In order to trigger the authentication in the first place, we need to
configure an auth requirement for a particular location. This is
showin the first section of the recipe. In this case, we're requiring
login to location called ``/admin``. 

Pay attention to the entire example, because every directive matters,
and must be set correctly.

The ``AuthFormLoginRequiredLocation`` points to the login form, which we
will create in the next step.

The ``AuthUserFile`` directive points to a password file which we'll
create below.

The ``AuthName`` directive must match the location that is being
protected, or you'll get an Internal Server Error, and an error log
message that says something like:


.. code-block:: text

   [Sat May 28 10:17:31.093428 2016] [auth_form:error] [pid 25183]
     [client 127.0.0.1:49648] AH01810: need AuthName: /admin/


That error message simply means "I've been asked for credentials to an
area called ``/admin/``, but there's no corresponding ``AuthName``
configured.

And, finally, you need to select your ``SessionCookieName`` carefully.
This is what the authentication cookie will be called on the client
side. You need to be sure that the name is unique. If you call it
something like ``session`` or ``cookie``, there's a good chance that the
name will conflict with some other existing cookie, and overwrite it,
causing that other session to fail. 

As with any other authentication technique, you can enclose auth
directives in a ``<Location>``, ``<Directory>``, ``<Files>``, ``<Proxy>``, or
any of the various ``*Match`` equivalents, or use these directives in a
``.htaccess`` file.

The login form
^^^^^^^^^^^^^^


Next, we create the login form itself.

This can be a standalone page, or embedded in some other page, as you
like. 


.. tip::

   If you embed it in another page, you may wish to use
   Javascript to hide the form if the user has successfully
   authenticated. However, this technique is outside of the scope of this chapter.


The fields in the form, and their names, are required. That is, you
must have an input field named ``httpd_username``, and one named
``httpd_password``.

The form ``action`` is also important, as it is where we will configure
the authentication handler.

If, for some reason, you wish to rename the username and password
fields, you can do so using the ``AuthFormUsername`` and
``AuthFormPassword`` directives, respectively.


.. warning::

   The login form must be placed outside of the authenticated area,
   otherwise an unauthenticated user will never be able to access the
   login form.


The login action
^^^^^^^^^^^^^^^^


The login action is handled by the ``form-login-handler`` Handler, which
is configured with a ``SetHandler`` directive, in a ``<Location>``
indicating the URL which you pointed your form ``action`` to.

You'll need to repeat a number of the directives that you had in your
intial authentication configuration, and they must have the same
values.

The ``AuthFormLoginSuccessLocation`` is where you want users to be sent
upon successful login. It usually makes sense for this to be the
"front page" of the authenticated area that they were initially trying
to access.

The password file
^^^^^^^^^^^^^^^^^


The ``AuthFormProvider`` and ``AuthUserFile`` directives indicate the
password store agianst which you will validate the provided username
and password. In our example, it is a text file, which needs to be
created using the same technique discussed in :ref:`Recipe_htpasswd`.

However, if you wish, you can use other auth providers, including
``dbm``, ``dbd``, ``ldap``, or any third-party authentication provider.

However, in the recipe above, we assume a standard ``htpasswd`` style
password file. 

Testing
^^^^^^^


To test your setup, point a browser at the password-protected URL. You
should be redirected to the password form, where you can supply
credentials. Successfully authenticating should result in you being
redirected to the resource specified in
``AuthFormLoginSuccessLocation``.


.. _See_Also_Form_Auth:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/2.4/mod/mod_auth_form.html

* http://httpd.apache.org/docs/2.4/mod/mod_session.html

* :ref:`Recipe_htpasswd`


.. _Recipe_dbm_auth:

DBM password files
~~~~~~~~~~~~~~~~~~

.. index:: mod_authn_dbm

.. index:: Modules,mod_authn_dbm

.. index:: Authentication,dbm

.. index:: Password files,dbm

.. index:: htdbm

.. index:: Commands,htdbm


.. _Problem_dbm_auth:

Problem
~~~~~~~


Your password file is becoming very large, and you want to speed up
lookups by using a DBM database file.


.. _Solution_dbm_auth:

Solution
~~~~~~~~


Use the ``htdbm`` utility to create a dbm password database.


.. code-block:: text

   htdbm -c /www/passwords/passwords.dbm oliver


To add another password to the same file:


.. code-block:: text

   htdbm /www/passwords/passwords.dbm dodger


This dbm can now be used instead of a text password file with a
configuration as follows.


.. code-block:: text

   <Directory "/www/docs/private">
     AuthName "Private"
     AuthType Basic
     AuthBasicProvider dbm
     AuthDBMUserFile "/www/passwords/passwords.dbm"
     Require valid-user
   </Directory>


.. _Discussion_dbm_auth:

Discussion
~~~~~~~~~~


Text password files, while easy to create and maintain, suffer from
slow lookup speed. Since they are unindexed, every password lookup
requires that the file be searched, one line at a time, until the
desired entry is found.

Converting to a dbm file solves this problem, providing an indexed
lookup mechanism which is much faster.

The ``htdbm`` tool works much the same way as the ``htpasswd`` tool, to
create and manage the dbm file. Because you can't just open the
resulting password file in an editor to inspect it, ``htdbm`` offers a
few additional features you way want to know about.

The ``-x`` option will delete a user from the password file:


.. code-block:: text

   htdbm -x /www/passwords/passwords.dbm nancy


The ``-l`` option will list all of the users in the password file:


.. code-block:: text

   htdbm -l /www/passwords/passwords.dbm


.. warning::

   There is a second script that manages dbm files, named ``dbmmanage``.
   However, for historical reasons, this script is not available on all
   platforms.


.. _See_Also_dbm_auth:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/programs/htdbm.html

* http://httpd.apache.org/docs/mod/mod_authn_dbm.html

* :ref:`Recipe_convert_htpasswd_to_dbm`


.. _Recipe_convert_htpasswd_to_dbm:

Converting a text password file to dbm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: Converting htpasswd to dbm

.. index:: Password files,converting text to dbm

.. index:: dbmmanage

.. index:: Commands,dbmmanage

.. index:: htdbm

.. index:: Commands,htdbm

.. index:: awk

.. index:: Commands,awk

.. index:: mod_authn_dbm

.. index:: Modules,mod_authn_dbm


.. _Problem_convert_htpasswd_to_dbm:

Problem
~~~~~~~


You already have a text password file, created with ``htpasswd``, and
you want to convert it to a dbm file for use with ``mod_authn_dbm``.


.. _Solution_convert_htpasswd_to_dbm:

Solution
~~~~~~~~


If ``dbmmanage`` is available, you can use it to convert a text password
file to dbm. Run the following command at the command line.


.. code-block:: text

   dbmmanage  passwords.dbm import < passwd


If your system does not have ``dbmmanage`` available, you can accomplish
the same thing with this ``awk`` script, run from the command line:


.. code-block:: text

   htdbm -cbp passwords.dbm temp temp
   awk 'BEGIN { FS=":" }; {system ("htdbm -bp passwords.dbm " $1 " " $2)}' passwords 
   htdbm -x passwords.dbm temp


.. _Discussion_convert_htpasswd_to_dbm:

Discussion
~~~~~~~~~~


The ``dbmmanage`` utility provides an ``import`` argument for specifically
this scenario, and will import a file containing usernames and
encrypted passwords, and produce a ``dbm`` version of that password
file.

From the documentation:


.. code-block:: text

   import: Reads username:password entries (one _per_ line) from STDIN and adds
   them to filename. The passwords already have to be crypted.


However, the ``dbmmanage`` utility, as mentioned in an earlier recipe, has been
replaced with the ``htdbm`` utility on some platforms, and so the recipe
above will not be available to you.

The ``awk`` script provides may require a little explanation.

First, using the ``-c`` argument to htdbm, we create a new passwords
database, ``passwords.dbm``, with a single temporary entry.

Then, using the ``awk`` utility, we iterate through the existing
password file, splitting the entries into a username and password
using the separator ':'. (That's what the ``FS`` argument means.)

For each line, we call the ``htdbm`` program, providing the username and
password as arguments. The ``-b`` flag tells ``htdbm`` to expect the
password as a second argument, and the ``-p`` flag tells it not to
encrypt the provided password - because it's already encrypted.

In this way, we can conver an existing password file to a dbm
database, without having to reenter the individual passwords. You'll
see a line of output for each line in the passwords file:


.. code-block:: text

   Warning: storing passwords as plain text might just not work on this
   platform.
   Database passwords.dbm modified.


This is expected. You're not actually storing passwords as plain text,
because the passwords were already encrypted in the other file.

The third line of the recipe uses the ``-x`` flag of ``htdbm`` to remove 
the temporary ``temp`` entry that we created in the first step.

Once it's done, you can verify that the right thing has happened with
the ``-l`` flag:


.. code-block:: text

   htdbm -l passwords.dbm


This will produce output like:


.. code-block:: text

   Dumping records from database -- passwords.dbm
     Username                         Comment
     rbowen                          
     maria                           
     irwinter
     sarahrhi
     elisem
   Total #records : 5


Ensure that all of the entries in the original ``passwords`` file are
represented in the new ``passwords.dbm`` file before using it for
authentication.


.. _See_Also_convert_htpasswd_to_dbm:

See Also
~~~~~~~~


* :ref:`Recipe_dbm_auth`

* https://httpd.apache.org/docs/programs/dbmmanage.html

* https://httpd.apache.org/docs/programs/htdbm.html

* https://www.gnu.org/software/gawk/manual/gawk.html


.. _Recipe_dbm_group_file:

dbm_group_file
~~~~~~~~~~~~~~

.. index:: Authentication,Groups

.. index:: mod_authn_dbm

.. index:: Modules,mod_authn_dbm

.. index:: mod_authz_dbm

.. index:: Modules,mod_authz_dbm


.. _Problem_dbm_group_file:

Problem
~~~~~~~


You want to specify a group of accounts to be authenticated, as we did
in the earlier recipe, :ref:`Recipe_authentication_groups`, but using
accounts specified in a ``dbm`` database.


.. _Solution_dbm_group_file:

Solution
~~~~~~~~


There are two ways to store a list of groups. You can put it in the
comments field of the user password file:


.. code-block:: text

   htdbm -t passwords.dbm emarg marketing,sales,community


Or, you can store the group information in a separate file, where
the key is the username, and the value is a comma-separated list of
groups to which that user belongs.

Now, require authorization against a particular group using the 
``dbm-group`` keyword:


.. code-block:: text

   <Directory "/var/www/marketing/presentations">
     AuthType Basic
     AuthName "Marketing"
     AuthBasicProvider dbm
     AuthDBMUserFile "/etc/httpd/passwords.dbm"
     AuthDBMGroupFile "/etc/httpd/passwords.dbm"
     Require dbm-group marketing
   </Directory>


.. _Discussion_dbm_group_file:

Discussion
~~~~~~~~~~


The functionality discussed in this recipe is provided by the module
``mod_authz_dbm``.

When you update the password file, the module will notice that it has
changed, and reload it, so you don't have to restart the server for
these changes to take effect.

The ``htdbm`` utility is typically installed along with the Apache http
server itself. Check the documentation for your particular operating
system to determine if it's included in a secondary package.


.. _See_Also_dbm_group_file:

See Also
~~~~~~~~


* :ref:`Recipe_authentication_groups`

* http://httpd.apache.org/docs/mod/mod_authz_dbm.html

* http://httpd.apache.org/docs/programs/htdbm.html


.. _Recipe_sql_auth:

Authentication against an SQL database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: SQL authentication

.. index:: Authentication,SQL

.. index:: mod_authn_dbd

.. index:: Modules,mod_authn_dbd

.. index:: Database,authentication

.. index:: Authentication,mod_authn_dbd


.. _Problem_sql_auth:

Problem
~~~~~~~


You want to store authentication credentials in an RDBMS (Relational
Database) such as mysql or postgresql.


.. _Solution_sql_auth:

Solution
~~~~~~~~


Use ``mod_authn_dbd`` to validate user credentials:


.. code-block:: text

   DBDriver pgsql
   DBDParams "dbname=apacheauth user=apache password=abcd1234xyz"
   
   <Directory "/usr/www/myhost/private">
     AuthType Basic
     AuthName "My Server"
     AuthBasicProvider dbd
   
     Require valid-user
     AuthDBDUserPWQuery "SELECT password FROM authn WHERE user = %s"
   </Directory>


.. _Discussion_sql_auth:

Discussion
~~~~~~~~~~


``mod_authn_dbd`` provides mechanisms to store user credentials in a
database such as mysql or postgresql, and then query that database to
validate authentication to resources.

The module relies on ``mod_dbd`` for database access functionality, and
so that module must also be loaded, and used to configure your
database connection. Documentation for how to connect to your specific
database is found at
http://httpd.apache.org/docs/mod/mod_dbd.html#dbdparams.
Supported database engines are:

* FreeTDS (for MSSQL and SyBase)
* MySQL
* Oracle
* PostgreSQL
* SQLite2
* SQLite3
* ODBC

Passwords may be stored in the database encrypted with any of the
formats supported by the ``AuthType`` (Basic or Digest) which you have
chosen. These options are discussed in detail in the "Password
Formats" document, which you can find at
http://httpd.apache.org/docs/misc/password_encryptions.html

This module is often used in conjunction with ``mod_authz_dbd``, so that
authorization, as well as authentication, may be handled in your
database. See :ref:`Recipe_SQL_Authorization` for further discussion of
doing this.


.. _See_Also_sql_auth:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_authn_dbd.html

* http://httpd.apache.org/docs/mod/mod_dbd.html

* http://httpd.apache.org/docs/misc/password_encryptions.html

* :ref:`Recipe_SQL_Authorization`


.. _Recipe_SQL_Authorization:

[role="v24"]
~~~~~~~~~~~~
Using a database for group authorization

.. index:: SQL authorization

.. index:: Authorization,SQL

.. index:: mod_authz_dbd

.. index:: Modules,mod_authz_dbd

.. index:: Database,authorization

.. index:: Authorization,mod_authz_dbd


.. _Problem_SQL_Authorization:

Problem
~~~~~~~


You want to use a database to store authorization group information.


.. _Solution_SQL_Authorization:

Solution
~~~~~~~~


Use ``mod_authz_dbd`` to associate a user with an authorization group:


.. code-block:: text

   Require dbd-group team
   AuthzDBDQuery "SELECT group FROM authz WHERE user = %s"


.. _Discussion_SQL_Authorization:

Discussion
~~~~~~~~~~


``mod_authz_dbd`` is often used in conjunction with ``mod_authn_dbd`` to
store group authorization details in a database. See
:ref:`Recipe_sql_auth` for discussion of ``mod_authn_dbd``.

In the example shown above, your database would contain a table named
``authz``, with records contanining a username, and the group to which
that user belongs. You can have multiple records for a given user, so
that they can be in multiple authorization groups.

As with ``mod_authn_dbd``, this module relies on ``mod_dbd`` for its
database connectivity, so that module must be loaded and configured.

``mod_authz_dbd`` also offers session management options, if you want to
track when a user logged in and logged out.


.. note::

   This module is not available in Apache httpd version 2.2.


.. _See_Also_SQL_Authorization:

See Also
~~~~~~~~


* :ref:`Recipe_sql_auth`

* http://httpd.apache.org/docs/mod/mod_dbd.html

* http://httpd.apache.org/docs/mod/mod_authz_dbd.html


.. _Recipe_ldap_auth:

LDAP authentication and authorization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: LDAP authentication and authorization

.. index:: Authorization,LDAP

.. index:: Authentication,LDAP

.. index:: Authorization,mod_authnz_ldap


.. _Problem_ldap_auth:

Problem
~~~~~~~


You want to use LDAP, or a related service such a Active Directory, as
an authentication and authorization source.


.. _Solution_ldap_auth:

Solution
~~~~~~~~


Use ``mod_authnz_ldap`` to check user credentials.

To allow access for any authenticated user:


.. code-block:: text

   <Location /members>
     AuthType Basic
     AuthName "Members Only"
     AuthBasicProvider ldap
   
     AuthLDAPURL "ldap://ldap.apache.org.com/ou=People, o=Apache?cn"
     Require valid-user
   </Location>


Other more specific requirements can be made:


.. code-block:: text

   Require ldap-user "Bob Marley"
   Require ldap-group cn=Administrators, o=Marketing
   Require ldap-attribute city="Nairobi" "status=active"


In version 2.4, requirements can be combined using ``RequireAll`` 
or ``RequireAny`` for more complicated scenarios.


.. _Discussion_ldap_auth:

Discussion
~~~~~~~~~~


Many organizations already use an LDAP server for authentication and
authorization. Rather than setting up something different for website
authentication, you may wish to point your web server at your LDAP
server.

With ``mod_authnz_ldap``, you can require any LDAP-defined attribute or
group, and you can combine them in various ways using ``RequireAll`` or
``RequireAny``.

For more extensive documentation and examples, consult the
``mod_authnz_ldap`` documentation at
http://httpd.apache.org/docs/mod/mod_authnz_ldap.html


.. warning::

   When using Basic authentication, as shown in the example above, the
   username and password are passed plaintext (that is, unencrypted)
   across the HTTP connection.

   This is slightly better when using Digest authentication, but even
   there, someone with some deeper technical knowledge can often use the
   encrypted information to compromise a connection, without ever
   actually knowing the unencrypted password.

   This is particularly worrisome when using
   LDAP authentication, as it might mean that someone watching your HTTP
   traffic now has your users' credentials to company resources, rather
   than just giving them access to your web content. We recommend that
   you always use TLS/SSL when requiring authentication, to protect these
   credentials. See :ref:`Chapter_SSL_and_TLS`, **SSL and TLS**, for further discussion of
   using encrypted communications.


.. _See_Also_ldap_auth:

See Also
~~~~~~~~


* :ref:`Recipe_RequireAll`

* http://httpd.apache.org/docs/mod/mod_authnz_ldap.html


.. _Recipe_auth_anon:

Anonymous "authentication"

.. index:: Anonymous authentication

.. index:: Authentication,anonymous

.. index:: mod_authn_anon

.. index:: Modules,mod_authn_anon

.. index:: mod_auth_anon

.. index:: Modules,mod_auth_anon


.. _Problem_auth_anon:

Problem
~~~~~~~


You want to provide a way to allow anonymous users access to an
authenticated resource, while tracking some information about them,
such as an email address.


.. _Solution_auth_anon:

Solution
~~~~~~~~


Use ``mod_authn_anon`` (Formerly called ``mod_auth_anon`` in earlier
versions) to ask for an anonymous username, and optionally an email
address, to sign into your site.


.. code-block:: text

   <Directory "/var/www/html/downloads">
       AuthName "Use 'anonymous' & your email address for guest entry"
       AuthType Basic
       AuthBasicProvider file anon
       AuthUserFile "/etc/httpd/passwords"
   
       Anonymous_NoUserID off
       Anonymous_MustGiveEmail on
       Anonymous_VerifyEmail on
       Anonymous_LogEmail on
       Anonymous anonymous guest www test welcome
   
       Require valid-user
   </Directory>


Users who have valid credentials can provide them to authenticate as
usual.


.. _Discussion_auth_anon:

Discussion
~~~~~~~~~~


``mod_authn_anon`` provides a mechanism to allow anonymous access to a
portion of your website, while tracking the email addresses of the
individuals who access the site.

Several directives allow you to turn on or off specific behaviors of 
this functionality:


.. _mod_authn_anon_options:

.mod_authn_anon configuration options

+-------------------------+---------------------------------------------------------------------------------------------------------+
| Directive               | Meaning                                                                                                 |
+-------------------------+---------------------------------------------------------------------------------------------------------+
| Anonymous_NoUserId      | Set ``On`` to allow the username field to be left blank                                                 |
+-------------------------+---------------------------------------------------------------------------------------------------------+
| Anonymous_MustGiveEmail | Set ``On`` to require an entry in the email address field                                               |
+-------------------------+---------------------------------------------------------------------------------------------------------+
| Anonymous_VerifyEmail   | Set ``On`` to require that the provided email address contain at least one ``@`` and at least one ``.`` |
+-------------------------+---------------------------------------------------------------------------------------------------------+
| Anonymous_LogEmail      | Set ``On`` to log the provided email address in the error log                                           |
+-------------------------+---------------------------------------------------------------------------------------------------------+
| Anonymous               | List usernames which will be accepted                                                                   |
+-------------------------+---------------------------------------------------------------------------------------------------------+


.. tip::

   Although you can require an email address, and require that it be a
   valid email address, this only means that it contains at least one ``@``
   and at least one ``.``, which in no way guarantees that it is actually a
   valid email address, much less the actual email address of the person
   accessing your web site.


.. _See_Also_auth_anon:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_authn_anon.html


.. _Recipe_OpenDoor:

Let everyone in
~~~~~~~~~~~~~~~

.. index:: Allow from all

.. index:: Require all granted


.. _Problem_OpenDoor:

Problem
~~~~~~~


You want a particular directory or resource to be accessible to
everyone.


.. _Solution_OpenDoor:

Solution
~~~~~~~~


For httpd 2.4, use the ``Require all granted`` syntax to indicate that a
particular resource should be available to everyone.

[role="v24"]

.. code-block:: text

   <Directory /var/www>
       Require all granted
   </Directory>


For 2.2, use the ``Allow from all`` for the same result.

[role="v22"]

.. code-block:: text

   <Directory /var/www>
       Order allow,deny
       Allow from all
   </Directory>


.. _Discussion_OpenDoor:

Discussion
~~~~~~~~~~


.. note::

   Remember that more specific (**i.e.**, deeper) directory blocks override
   less specific ones. That is, if you have ``Require all denied`` for
   ``<Directory />``, but ``Require all granted`` for ``<Directory /var/www/>```, access to ``/var/www`` will in fact be permitted. See
   :ref:`Recipe_Relaxing` for additional discussion.


.. _See_Also_OpenDoor:

See Also
~~~~~~~~


* :ref:`Recipe_all_denied`
* :ref:`Recipe_Relaxing`


.. _Recipe_all_denied:

Don't let anybody in
~~~~~~~~~~~~~~~~~~~~

.. index:: Deny from all

.. index:: Require all denied


.. _Problem_all_denied:

Problem
~~~~~~~


You wish to ensure that a particular directory is not accessible to
anyone, under any circumstances.


.. _Solution_all_denied:

Solution
~~~~~~~~


For httpd 2.4, use the ``Require all denied`` syntax:

[role="v24"]

.. code-block:: text

   <Directory /etc/httpd>
       Require all denied
   </Directory>


For httpd 2.2, use the ``Deny from all`` directive:

[role="v22"]

.. code-block:: text

   <Directory /etc/httpd>
       Order deny,allow
       Deny from all
   </Directory>


.. _Discussion_all_denied:

Discussion
~~~~~~~~~~


.. note::

   Note that a restrictive configuration in a particular directory may be
   overridden or relaxed in a subdirectory, as discussed in
   :ref:`Recipe_Relaxing`.


.. _See_Also_all_denied:

See Also
~~~~~~~~


* :ref:`Recipe_Relaxing`
* :ref:`Recipe_OpenDoor`


.. _Recipe_Authorization_by_host:

Authorization_by_host

.. index:: Authorization,host

.. index:: Authorization,ip address

.. index:: Host-based authorization

.. index:: IP-address based authorization

.. index:: Access control,by address

.. index:: Allow

.. index:: Require


.. _Problem_Authorization_by_host:

Problem
~~~~~~~

You wish to restrict access to a resource based on the hostname or IP
address of the client.


.. _Solution_Authorization_by_host:

Solution
~~~~~~~~


This feature is provided by ``mod_authz_host``, and the syntax is
different for 2.2 and 2.4 servers.

In 2.2, use the "Allow from" and "Deny from" syntax:

[role="v22"]

.. code-block:: text

   # Allow from an IP address, or range of addresses
   Allow from 10.19.44.8
   Allow from 10.
   Allow from 10.1.0.0/16
   
   # Allow from a hostname, or all hosts in a domain or TLD
   Allow from www.apache.org
   Allow from .example.com
   Allow from .net


Multiple requirements can be combined in a variety of ways using the
``Order`` and ``Satisfy`` directives. Replace ``Allow`` with ``Deny`` to
reverse the meaning of any of the above requirements.

In 2.4, use the "Require host" and "Require ip" syntax:

[role="v24"]

.. code-block:: text

   # Allow from an IP address, or range of addresses
   Require ip 10.19.44.8
   Require ip 10.
   Require ip 10.1.0.0/16
   
   # Allow from a hostname, or all hosts in a domain or TLD
   Require host www.apache.org
   Require host .example.com
   Require host .net
   
   # Require the request be from localhost
   Require local


Use the ``Require not`` syntax to forbid, rather than allow, a
particular access.

Multiple requirements can be combined in a variety of ways using the
``<RequireAny>``, ``<RequireAll>``, and ``<RequireNone>`` containers.


.. _Discussion_Authorization_by_host:

Discussion
~~~~~~~~~~


Restricting access by network address is often an important aspect of
website security. With it, you can ensure that connections originate
from your company network, for example, or that they are not from a
particular country.

While this functionality has been available in all versions of Apache
httpd, the syntax is now much more flexible in the 2.4 version, with
the ability to combine multiple requirements in arbitrary ways using
the ``<RequireAny>``, ``<RequireAll>``, and ``<RequireNone>`` containers.

See :ref:`Recipe_RequireAll` for more discussion of combining multiple access
control requirements.

IP addresses can be IPv4 or IPv6 addresses, and can be expressed in
any valid format for addresses or network ranges.

The ``local`` keyword in the 2.4 configuration example
allows access to the server if any of the following conditions is true:

* the client address matches 127.0.0.0/8
* the client address is ::1
* both the client and the server address of the connection are the same


.. _See_Also_Authorization_by_host:

See Also
~~~~~~~~


* :ref:`Recipe_RequireAll`

* https://httpd.apache.org/docs/2.4/mod/mod_authz_host.html

* https://httpd.apache.org/docs/2.2/mod/mod_authz_host.html


.. _Recipe_Authorization_by_file_ownership:

Authorization_by_file_ownership

.. index:: File ownership

.. index:: Authorization,by file ownership

.. index:: mod_authz_owner

.. index:: Modules,mod_authz_owner


.. _Problem_Authorization_by_file_ownership:

Problem
~~~~~~~


You want to set access restrictions based on the file-system file and
directory ownership.


.. _Solution_Authorization_by_file_ownership:

Solution
~~~~~~~~


Use the ``Require file-owner`` and ``Require file-group`` configurations,
proivided by ``mod_authz_owner``, to require that the username on the
file or directory matches the username with which someone has
authenticated:


.. code-block:: text

   <Directory "/home/*/public_html/private">
       AuthType Basic
       AuthName MyPrivateFiles
       AuthBasicProvider dbm
       AuthDBMUserFile "/etc/httpd/conf/users.dbm"
       Require file-owner
   </Directory>


.. _Discussion_Authorization_by_file_ownership:

Discussion
~~~~~~~~~~


``mod_authz_owner`` provides two arguments to ``Require`` to allow you to
match an HTTP login username to the file owner in the filesystem. The
authentication itself is still done by one of the other ``mod_authn``
modules. In the recipe, we're using ``mod_authn_dbm`` for
authentication. This means that you'll still need to have a user file
* in this case ``/etc/httpd/conf/users.dbm`` - containing the valid
usernames and passwords that you're going to authenticate against.

``mod_authz_owner`` does **not** use the system passwords to authenticate.


.. warning::

   ``mod_authz_owner`` blindly assumes that an authenticated user is, in
   fact, the owner of the files that match that username. It is up to
   you, the system administrator, to ensure that the people that have the
   credentials for those HTTP authentication account are, in fact, the
   same people as the usernames in the filesystem.

   In particular, if you have a means where people can register for
   accounts, it may be possible for someone to guess usernames, create
   matching accounts, and then have access to files that you thought you
   protected.


.. _See_Also_Authorization_by_file_ownership:

See Also
~~~~~~~~


* https://httpd.apache.org/docs/mod/mod_authz_owner.html

[role="v24"]

.. _Recipe_Authorization_by_expression:

Authorization using complex expressions

.. index:: Expression parser

.. index:: Authorization,by expression

.. index:: Per-request configuration,authorization


.. _Problem_Authorization_by_expression:

Problem
~~~~~~~


In :ref:`Chapter_per_request`, **Programmable Configuration**, you learned
how to use the general purpose expression parser. You want to use it
to authorize requests against expressions.


.. _Solution_Authorization_by_expression:

Solution
~~~~~~~~


Use the ``Require expr`` syntax, with the expression that you have
created describing the conditions under which you wish to permit
access.


.. code-block:: text

   Require expr \
       "%{HTTP_USER_AGENT} !~ /BadAgent/
       &&
       %{REMOTE_ADDR} =~ /^10\./"


.. _Discussion_Authorization_by_expression:

Discussion
~~~~~~~~~~


In the recipe above, we require both that the client user agent not
match the string "BadAgent", and also that the request comes from the
``10.`` IP address range.

You can use the expression engine to craft any arbitrary expression,
based on any variables available to httpd, including request headers,
environment variables, and variables that you have yourself set in
other configuration directives.


.. tip::

   You can reverse the sense of a particular ``Require expr`` statement by
   using ``Require not expr``, as shown in previous examples. However, in
   the case of ``expr``, it is always possible to rephrase the expression
   itself to convey the negagive instead. Give some thought to which
   formulation will be more readable, so that the server administrator
   who comes after you will have no trouble understanding it.

   For example, the following two directives are identical in meaning:

   Require not expr "%{REMOTE_ADDR} =~ /^148\.19/"

   Require expr "%{REMOTE_ADDR} !~ /^148\.19/"


.. _See_Also_Authorization_by_expression:

See Also
~~~~~~~~


* :ref:`Recipe_expr`

* https://httpd.apache.org/docs/expr.html


.. _Recipe_system_password_auth:

Authentication against system passwords

.. index:: Authentication,system passwords

.. index:: mod_auth_pam

.. index:: Modules,mod_auth_pam

.. index:: mod_authnz_pam

.. index:: Modules,mod_authnz_pam

.. index:: PAM authentication


.. _Problem_system_password_auth:

Problem
~~~~~~~


You want all the users on your Unixish system to be able to
authenticate themselves over the Web using their already-assigned
usernames and passwords.


.. _Solution_system_password_auth:

Solution
~~~~~~~~


There are a number of third-party modules which use PAM - the
Pluggable Authentication Module - to do authentication. PAM is a
library that allows applications to access the underlying system
authentication. These modules are typically called either
``mod_auth_pam`` or ``mod_authnz_pam``.

However, at the time of this writing, none of these modules are
actively maintained, and so we do not recommend their use.


.. _Discussion_system_password_auth:

Discussion
~~~~~~~~~~


.. warning::

   We strongly recommend that you don't use system passwords for http
   authentication. In the event that your website were compromised,
   attackers would then also have access to system authentication
   information.

   However, if you must,
   make sure that you're doing it over SSL, so that the user credentials
   are protected.


We must stress that using system account information for Web
authentication is a very bad idea, unless your site is also secured
using SSL.

There are a number of reasons for this.

Any intruder who happens to obtain one of
your users' credentials not only can access the protected files over
the Web, but can actually log onto your system where it's possible to
do significant damage.
  
Web logins don't have the same
security controls as most operating systems; over the Web, an intruder
can keep hammering away at a username with password after password
without the system taking any defensive measures; all these
authentication modules will do is record a message in the
Apache error log. However, most operating systems will enter a
paranoid mode and at least ignore login attempts for a while after
some number of failures. Your Apache httpd server will not.

An account which is being attacked has no mechanism for notifying the
account owner that this is happening. When you log in to a server, you
may receive a message such as:


.. code-block:: text

   There were 6 failed login attempts since the last successful login.


For web accounts, there's no notification like this, so a user will
never be aware that their account is being attacked.

You also can't tell when an account has been compromised. You'll just
see successful requests in the access log.

If you happen to look at the logs at the right moment, you will see
failed attempts that indicate an ongoing attack, but once the account
is compromised, it will just look like normal accesses.

And, finally, unless all request are across SSL, the user's system
credentials are being passed plaintext across the wire with every
single HTTP request. This gives an attacker many opportunities to
intercept the password or replay your requests.

So, while you could do this, we strongly recommend against it.


.. _See_Also_system_password_auth:

See Also
~~~~~~~~


* The :ref:`Authentication_and_Authorization_sidebar` sidebar, earlier in this chapter

* The :ref:`HTTP_Browsers_and_Credentials_sidebar` sidebar, later in this chapter

* The :ref:`Weak_and_Strong_Authentication_sidebar` sidebar, later in this chapter


.. _Recipe_limit_upload_size:

Limiting Upload Size


.. _Problem_limit_upload_size:

Problem
~~~~~~~


You wish to place an upper limit on the size of files that may be
uploaded to your server **via** HTTP POST.


.. _Solution_limit_upload_size:

Solution
~~~~~~~~


Use the ``LimitRequestBody`` directive to set the limit. For example, to
limit uploads to 10MB:


.. code-block:: text

   <Directory "/usr/local/apache2/uploads">
       LimitRequestBody 10000000
   </Directory>


You may also wish to configure an ``ErrorDocument 413`` to provide
helpful information to the user in the event that they exceed this
limit.


.. _Discussion_limit_upload_size:

Discussion
~~~~~~~~~~


``LimitRequestBody`` places an upper limit on the ``Content-length`` of an
HTTP request. Requests that exceed this limit result in a 413 error -
"Request Entity Too Large".


.. _apacheckbk-CHP-6-NOTE-90:


.. warning::

   The same ``Content-length``
   field is used to indicate the amount of data included in a ``POST`` request, such as from a Web form
   submission, so be careful not to set your maximum too low or your
   forms may start getting this error!


.. _See_Also_limit_upload_size:

See Also
~~~~~~~~


* :ref:`Chapter_Troubleshooting_and_error_handling`, *Troubleshooting and
  Error Handling*


.. _Requiring_Both_Weak_and_Strong_Authentication_id130793:

Requiring Both Weak and Strong Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. _Problem_id130807:

Problem
~~~~~~~


You want to require both weak and strong authentication for a
particular resource. For example, you wish to ensure that users
accesses the site from a particular location and to require that they
provide a password.


.. _Solution_id130844:

Solution
~~~~~~~~


For httpd 2.2 and earlier, use the ``Satisfy all`` directive to ensure
that all requirements are enforced.

[role="v22"]

.. code-block:: text

   <Directory /www/htdocs/sensitive>
          
       # Enforce all restrictions
       Satisfy All
   
       # Require a password
       AuthType Basic
       AuthName Sensitive
       AuthUserFile /www/passwords/users
       AuthGroupFile /www/passwords/groups
       Require group sales
   
       # Require access from a certain network
       Order deny,allow
       Deny from all
       Allow from 192.168.1
   </Directory>


For 2.4, use the ``<RequireAll>`` container to group all requirements
which must be enforced.

[role="v24"]

.. code-block:: text

   <Directory /www/htdocs/sensitive>
          
       # Require a password
       AuthType Basic
       AuthName Sensitive
       AuthUserFile /www/passwords/users
       AuthGroupFile /www/passwords/groups
       Require group sales
   
     <RequireAll>
         Require group sales
         Require ip 192.168.1
     </RequireAll>
   
   </Directory>


.. _Discussion_id130899:

Discussion
~~~~~~~~~~


In this example, users must provide a login, identifying them as
a member of the ``sales`` group, and must also use a machine on the
192.168.1 network.

For the 2.2 solution,
the ``Satisfy All`` directive requires that all access
control measures be enforced for the specified scope. 

For the 2.4 solution, the ``<RequireAll>`` container provides the same
functionality. See :ref:`Recipe_RequireAll` for additional information on
what else this directive can do.

Users accessing
the resource from a nonmatching IP address will immediately receive
a ``Forbidden`` error message in their browser,
while, in the logfile, the following error message is logged:


.. code-block:: text

   [Sun May 25 15:31:53 2003] [error] [client 208.32.53.7] client denied 
   by server configuration: /usr/local/apache/htdocs/index.html


Users who are in the required set of IP addresses, however,
receive a password dialog box and are required to provide a valid
username and password.


.. _See_Also_id130954:

See Also
~~~~~~~~


* :ref:`Recipe_Relaxing`


.. _Weak_and_Strong_Authentication_sidebar:


.. sidebar:: Weak and Strong Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   The basic Apache security model for HTTP is based on the
   concepts of weak and strong authentication mechanisms. 
   
   Weak mechanisms are those that rely on information volunteered by a
   user; strong ones use credentials obtained without asking. For
   instance, a username and password constitute a set of weak
   credentials, whereas the IP address of the user's client system is
   regarded as a strong one.
   
   One difference between the two types lies in how Apache
   handles an authentication failure. If invalid weak credentials are
   presented, the server will respond with a ``401 Unauthorized`` status,
   which allows the user to try again. In contrast, a failure to 
   authenticate when strong credentials are required will result in 
   a ``403 Forbidden`` status—for which there is no opportunity to retry.
   
   In addition, strong and weak credentials can be required in
   combination; this is controlled by the **Satisfy** directive in httpd
   2.2, and the ``<RequireAll>``, ``<RequireAny>``, and ``<RequireNone>``
   containers in httd 2.4. The five possible requirements are:
   
   * None; no authentication required.
   * Only strong credentials are needed.
   * Only weak credentials are required.
   * Both strong and weak credentials are accepted; if either
                 is valid, access is permitted.
   * Both strong and weak credentials are required.
               


.. _Recipe_Relaxing:

Relaxing Restrictions for a Subdirectory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: Relaxing restrictions

.. index:: Satisfy

.. index:: <RequireAny>


.. _Problem_Relaxing:

Problem
~~~~~~~


There are times when you might want to apply a tight access policy
over portions of your site, such as with something like:


.. code-block:: text

   <Directory /usr/local/apache/htdocs/BoardOfDirectors>
       AuthUserFile /usr/local/apache/access/bod.htpasswd
       Require valid-user 
   </Directory>


Because of Apache's scoping rules, this blanket applies to all
documents in that directory and in any subordinate subdirectories
underneath it. But suppose that you want to make a subdirectory, such
as ``BoardOfDirectors/minutes``, available without restriction.


.. _Solution_Relaxing:

Solution
~~~~~~~~


Override the restriction of the parent directory in a subdirectory:

[role="v24"]

.. code-block:: text

   <Directory /usr/local/apache/htdocs/BoardOfDirectors/minutes>
       AuthUserFile /usr/local/apache/access/bod.htpasswd
       Require all granted
   </Directory>


For httpd 2.2, add the ``Satisfy Any`` directive to ensure that the
stronger authorization requirement isn't enforced:

[role="v22"]

.. code-block:: text

   <Directory /usr/local/apache/htdocs/BoardOfDirectors/minutes>
     Satisfy Any
     Order deny,allow
     Allow from all
   </Directory>


Alternatively, if you're using ``.htaccess`` files, place the file in
that directory (**i.e.**, ``BoardOfDirectors/minutes``) containing the contents
of the example above, minus the ``<Directory>`` tags.


.. _Discussion_Relaxing:

Discussion
~~~~~~~~~~


The ``Satisfy`` directive tells httpd how strictly to enforce access
control rules. You can either ``Satisfy All``, or ``Satisfy Any``, which
mean exactly what they say: ``Satisfy All`` requires that all specified
rules are enforced, while ``Satisfy Any`` allows you to get away with
the least restrictive of the rules.

In this case, ``Satisfy Any``, applied to ``Allow from all`` and ``Deny from all`` will cause the less restritive one - ``Allow from all`` - to
be followed.

By specifying ``Order deny,allow``, this configuration ensures that the
``Allow`` will be applied after any ``Deny`` that is already in place.

With httpd 2.4, the new ``<RequireAll>``, ``<RequireAny>``, and
``<RequireNome>`` containers allow from much more fine-grained
enforcement of access requirements. See :ref:`Recipe_RequireAll` for
further discussion.


.. tip::

   It's a far better practice to arrange your site's directory structure
   such that this is never required. This will avoid situations where you
   unintentionally expose sensitive documents, or unintentionall hide
   public documents, by forgetting the roles of various subdirectories.


.. _See_Also_Relaxing:

See Also
~~~~~~~~


* :ref:`Requiring_Both_Weak_and_Strong_Authentication_id130793`
* :ref:`Recipe_FilesRelax`
* :ref:`Recipe_RequireAll`


.. _Recipe_FilesRelax:

Lifting Restrictions Selectively For Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: Relaxing restrictions

.. index:: Satisfy


.. _Problem_FilesRelax:

Problem
~~~~~~~


You want most documents to be restricted, (for example, requiring a
username and password) but want a few to be available to the public.

For example, you may want **index.html** to be publicly accessible,
whereas the rest of the files in the directory require password
authentication.


.. _Solution_FilesRelax:

Solution
~~~~~~~~


For httpd 2.4, use a ``<Files>`` directive and ``Require all granted``
directive:

[role="v24"]

.. code-block:: text

   <Files index.html>
       Require all granted
   </Files>


This may be placed in a ``.htaccess`` file, or in a ``<Directory>`` block,
if you want to limit the scope for which it is in effect.

[role="v24"]

.. code-block:: text

   <Directory "/usr/local/apache/htdocs">
       Require all denied
       <Files index.html>
           Require all granted
       </Files>
   </Directory>


For httpd 2.4, use the ``Satisfy Any`` directive in the 
appropriate place in your ``.htaccess`` or ``httpd.conf`` file:


.. code-block:: text

   <Files index.html>
       Order Deny,Allow
       Allow from all
       Satisfy Any
   </Files>


.. _Discussion_FilesRelax:

Discussion
~~~~~~~~~~


Regardless of what sorts of restrictions you may have on other
files, or on the directory as a whole, the ``<Files>``
container in the solution makes the ``index.html`` file accessible to everyone
without limitation.

This method can be easily extended to apply to arbitrary
filename patterns using shell global characters. To extend it to use
regular expressions for the filename, use the ``<FilesMatch>``
directive instead.


.. _See_Also_FilesRelax:

See Also
~~~~~~~~


* :ref:`Recipe_Relaxing`
* :ref:`Requiring_Both_Weak_and_Strong_Authentication_id130793`
* http://httpd.apache.org/docs/mod/mod_access.html


.. _Authorizing_Using_File_Ownership_id132667:

Authorizing Using File Ownership


.. _Problem_id132682:

Problem
~~~~~~~


You wish to require user authentication based on system file
        ownership. That is, you want to require that the user that owns the
        file matches the username that authenticated.


.. _Solution_id132728:

Solution
~~~~~~~~


Use the **Require file-owner** directive:


.. code-block:: text

   <Directory /home/*/public_html/private>
       AuthType Basic
       AuthName "MyOwnFiles"
       AuthUserFile /some/master/authdb
       Require file-owner
   </Directory>


.. _Discussion_id132785:

Discussion
~~~~~~~~~~


The goal here is to require that username ``jones`` must authenticate in order to access
the ``/home/jones/public_html/private``
directory.

The user does not authenticate against the system password file
but against the **AuthUserFile** specified in the example.
Apache just requires that the name used for authentication matches the
name of the owner of the file or directory in question. Note also that
this is a feature of ``mod_auth`` and
is not available in other authentication modules.


.. _apacheckbk-CHP-6-NOTE-95:


.. tip::

   This feature was added in Apache 1.3.22. In Apache 2.2, this
   functionality is provided by the module ``mod_authz_owner``.


.. _See_Also_id132841:

See Also
~~~~~~~~


* The **Require file-group** keyword at 
  http://httpd.apache.org/docs/mod/mod_auth.html#require


.. _Recipe_Username:

Accessing the Authenticated Username
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: Authentication,username

.. index:: Username

.. index:: REMOTE_USER


.. _Problem_Username:

Problem
~~~~~~~


You want to know the name of the user who has authenticated.


.. _Solution_Username:

Solution
~~~~~~~~


Some scripting modules, such as ``mod_php``, provide a standard interface for
accessing values set by the server. For instance, to obtain the
username that was used to authenticate from within a PHP script, it
would access a field in the ``$_SERVER`` superglobal array:


.. code-block:: text

   $username = $_SERVER['REMOTE_USER'];


For a Perl or ``mod_perl`` script, use:


.. code-block:: text

   my $username = $ENV{REMOTE_USER};


In a Server-Side Include (SSI) directive, this may look like:


.. code-block:: text

   Hello, user <!--#echo var="REMOTE_USER" -->. Thanks for visiting.


Other scripting modules may provide specific means of accessing
this information. For those that don't, or for nonscript applications,
use the appropriate means to consult the ``REMOTE_USER`` 
environment variable.


.. _Discussion_Username:

Discussion
~~~~~~~~~~


When a user has authenticated, the environment variable ``REMOTE_USER`` is set to the name with which
she authenticated. You can access this variable in CGI programs, SSI
directives, PHP files, and a
variety of other methods. The value also will appear in your ``access_log`` file.

Note that although it is the convention for an authentication
module to set this variable, there are reportedly some third-party
authentication modules that do not set it but provide other methods
for accessing that information.


.. _See_Also_Username:

See Also
~~~~~~~~


* :ref:`Recipe_GetPassword`


.. _Recipe_GetPassword:

Obtaining the Password Used to Authenticate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: Authentication,obtaining the password

.. index:: Password


.. _Problem_GetPassword:

Problem
~~~~~~~


You want to get the password the user used to authenticate.


.. _Solution_GetPassword:

Solution
~~~~~~~~


Standard Apache modules do not make this value available. It is,
however, available from the Apache API if you wish to write your own
authentication methods. The API method you should be looking for is
``get_basic_auth``. Module authoring is beyond the scope of this book.


.. _Discussion_GetPassword:

Discussion
~~~~~~~~~~


For security reasons, although the username is available as an
environment variable, the password used to authenticate is
**not** available in any simple manner. The rationale
behind this is that it would be a simple matter for unscrupulous
individuals to capture passwords so that they could then use them for
their own purposes. Thus, the decision was made to make passwords near
to impossible to obtain.

The only way to change this is to rebuild the server from the
sources with a particular (strongly discouraged) compilation flag.
Alternately, if you write your own authentication module, you would of
course have access to this value, as you would need to verify it in
your code.


.. _See_Also_GetPassword:

See Also
~~~~~~~~


* :ref:`Recipe_Username`


.. _Recipe_BruteForcePassword:

Preventing Brute-Force Password Attacks

.. index:: Password,brute force attack

.. index:: mod_security,preventing brute force password attack

.. index:: Modules,mod_security


.. _Problem_BruteForcePassword:

Problem
~~~~~~~


You want to detect when someone is trying to break into an account by
guessing the password repeatedly.


.. _Solution_BruteForcePassword:

Solution
~~~~~~~~


Use ``mod_security`` to track failed login attempts, and block the
client after a certain number of attempts.


.. code-block:: text

   <Location /private>
       # If they are already blocked ...
           SecRule IP:password_block "@eq 1" \
               "phase:2,deny,\
               msg:'Client blocked due to password attack'"
   
       # Did Auth fail?
           SecRule RESPONSE_STATUS "^401" \
           "setvar:IP.passwd_fail_counter=+1"
   
       # If they've failed 5 times, block them for 5 minutes
           SecRule IP:passwd_fail_counter "@ge 5" \
           "phase:5,pass,t:none, \
           setvar:IP.password_block,\
           setvar:!IP.passwd_fail_counter,\
           expirevar:IP.password_block=300"
   </LocationMatch>


.. _Discussion_BruteForcePassword:

Discussion
~~~~~~~~~~


The recipe provided here relies on ``mod_security``, so you must have
that module loaded.

The recipe is in three parts.

Part one checks to see if the client is already blocked, by inspecting
the ``password_block`` variable. If they're already blocked,
``mod_security`` denies the request, and we're done.

Part two looks to see if the client is receiving a 401 response code,
which will indicate that they have failed to authenticate. If this
happens, a counter - ``passwd_fail_counter`` - is incremented so that we
know how many times they failed.

Finally, part three checks to see whether that counter is larger than
5.


.. warning::

   The first time someone requests a password-protected resource, they'll
   receive a 401 response code. Keep that in mind when you're setting the
   upper limit on the number of failures. Although we're checking for the
   counter to exceed 5, that actually means 4 failed password attempts,
   since the first one doesn't really count.


If the counter has gone over 5, we set the variable ``password_block``
to true. We clear the ``passwd_fail_counter`` variable. And we set an
expiration timer on the ``password_block`` counter for 300 seconds (5
minutes) so that nobody is blocked permanently. Once the timer runs
out, the client will have another chance to try to authenticate.
However the 5 minute timeout is likely to discourage any automated
attempt to log into your website.

Adjust the various numbers in this recipe to fit your particular
scenario, and your preferences.


.. _See_Also_BruteForcePassword:

See Also
~~~~~~~~


* :ref:`Recipe_mod_security_recipes`

* http://modsecurity.org/


.. _Recipe_Creds_In_URL:

Passing Credentials in the URL

.. index:: Authentication,Passing credentials in the URL

.. index:: Passing credentials in the URL

.. index:: Credentials in the URL


.. _Problem_Creds_In_URL:

Problem
~~~~~~~


You want to have a resource password-protected, but be able to provide
a URL with the credentials included, so that users don't have to type
them in.


.. _Solution_Creds_In_URL:

Solution
~~~~~~~~


Give your users a URL with the username and password provided in the
following format:

http://username:password@www.example.com/secret/


.. _Discussion_Creds_In_URL:

Discussion
~~~~~~~~~~


Embedding the username and password in the URL gives a way to
distribute a link to your users to access a password-protected site
directly without being prompted for the password.

The browser takes care of the details of sending the username and
password to the server in the ordinary way (**i.e.**, **via** the
``WWW-Authenticate`` header) and not as part of the URL.


.. _See_Also_Creds_In_URL:

See Also
~~~~~~~~


* The :ref:`HTTP_Browsers_and_Credentials_sidebar` sidebar, earlier in this chapter


.. _Recipe_DOS-attacks:

Blocking Denial of Service (DoS) attacks

.. index:: Denial of service attacks; see DDoS

.. index:: Distributed denial of service attacks; see DDoS

.. index:: DoS; see DDoS

.. index:: DDoS

.. index:: mod_evasive

.. index:: Modules,mod_evasive

.. index:: mod_qos

.. index:: Modules,mod_qos

.. index:: mod_security

.. index:: Modules,mod_security


.. _Problem_DOS-attacks:

Problem
~~~~~~~


You wish to block, a Denial of Service (DoS) or Distributed Denial of
Service (DDoS) attack.


.. _Solution_DOS-attacks:

Solution
~~~~~~~~


Use ``mod_qos`` to identify requests that are either too frequent for
one resource, or too frequent from one client:


.. code-block:: text

   QS_ErrorPage                  /error-docs/qs_error.html
   
   # Concurrent requests for any one resource
   QS_LocRequestLimitDefault                              200
   
   # Concurrent requests for a particular file type
   QS_LocRequestLimitMatch       "^.*\.gif$"              100
   
   # Concurrent requests to specific locations
   QS_LocRequestLimit            /images                  100
   QS_LocRequestLimit            /app/a                   300
   
   # Concurrent requests for a particular client
   QS_ClientEventRequestLimit                             20


Or, use ``mod_security`` to permanently block a client who is
particularly abusive:


.. code-block:: text

   SecRuleEngine On
   
   SecAuditEngine RelevantOnly
   SecAuditLogType Serial
   SecAuditLog logs/mod_security.log
   SecDataDir logs/mod_security-data
   
   # Count requests per second, per client                                        
   SecRule REQUEST_BASENAME "^.+$" \
     "phase:1,nolog,pass,initcol:\
     ip=%{REMOTE_ADDR},\
     setvar:ip.requests=+1,\
     expirevar:ip.requests=1,\
     id:10"
   
   # If more than 30 requests/sec, set block = 1, for 5 seconds, and count        
   # how many times we've blocked this particular client. (Count expires
   # after an hour.)
   SecRule ip:requests "@eq 30" \
       "phase:1,pass,nolog,setvar:\
       ip.block=1,\
       expirevar:ip.block=5,\
       setvar:ip.blocks=+1,\
       expirevar:ip.blocks=3600,\
       id:11"
   
   # If block is set to 1, return a 403 for 5 seconds and log it                  
   SecRule ip:block "@eq 1" \
     "phase:1,deny,log,\
     logdata:'req/sec: %{ip.requests}, blocks: %{ip.blocks}',\
     status:403,\
     id:12"
   
   # If we've blocked them more than 5 times, then block them for an hour
   SecRule ip:blocks "@ge 5" \
     "phase:1,deny,log,\
     logdata:'req/sec: %{ip.requests}, blocks: %{ip.blocks}',\
     status:403,\
     id:13"
   
   # Display a rate limit warning for clients who are blocked                     
   ErrorDocument 403 /error/slow_down.html


.. note::

   The ``mod_security`` section of this recipe borrows heavily from 
   Ioannis Cherovim's blog post at
   http://blog.cherouvim.com/simple-dos-protection-with-mod_security/,
   with updates for more recent versions of ``mod_security``.


.. _Discussion_DOS-attacks:

Discussion
~~~~~~~~~~


A denial of service attack, commonly referred to as a DoS, is when one
client attempts to overwhelm your site with request, resulting in your
site being unable to respond to legitimate requests.

A distributed denail of service attack (DDoS) is when this request
comes from multiple clients working in coordination.

Two third-party modules are shown here which address these requests by
blocking the clients. There are other third-party modules which do the
same thing, as well as a wide variety of firewall products which
perform this block at the network level, so that Apache httpd doesn't
even have to be aware that the attack is happening.

Many DoS (and DDoS) attacks attempt to overwhelm a site at the network
level, and mitigating those is beyond the scope of this book.


.. tip::

   In previous editions of this book, we recommended the module
   ``mod_evasive`` to address this situation. That module has, since that
   time, been abandoned, and is no longer actively developed.


The first recipe above uses ``mod_qos`` to identify clients which are
requesting resources too often, or resources which are being requested
too often, and denies those requests. See
http://mod-qos.sourceforge.net/ for more detail on this
module, and to download the latest release.

The second recipe uses ``mod_security``, which is discussed in further
detail in :ref:`Chapter_Security`, **Security**. ``mod_security`` is a general purpose
http-level firewall, and this particular recipe only shows a tiny
fraction of what it can do. In this recipe, we count request **per** IP
address, and when a particular IP address makes more than 30 requests
in a second, we block them for 5 seconds. When a client has been
blocked more than 5 times, we block them for an entire hour. In this
way, a momentary lapse causes a small inconvenience, but a more
determined attack causes a lengthy block.


.. _See_Also_DOS-attacks:

See Also
~~~~~~~~


* http://mod-qos.sourceforge.net/

* https://modsecurity.org/

* http://blog.cherouvim.com/simple-dos-protection-with-mod_security/


.. _Recipe_obscure-forbidden:

Obscure the address of forbidden URLs

.. index:: Obscure forbidden URLs

.. index:: Security by obscurity


.. _Problem_obscure-forbidden:

Problem
~~~~~~~


When access to a file is forbidden, you don't want the user's
browser to show its URL.


.. _Solution_obscure-forbidden:

Solution
~~~~~~~~


Use the ``ErrorDocument`` directive with a fully-qualified URL, so that
the browser redirects away from the forbidden page.


.. code-block:: text

   ErrorDocument 403 http://example.com/errors/forbidden.html


.. _Discussion_obscure-forbidden:

Discussion
~~~~~~~~~~


Ordinarily, when access to a document is forbidden, the browser will
display a message saying that the request was forbidden, but will
still show the address of the requested page.

By using a fully-qualified URL as the argument to ``ErrorDocument``, you
cause the browser to make a new request to the specified location.
This, in turn, causes the browser to display the new URL in the
address bar, thus obscuring the address which was originally
forbidden. This will prevent the casual user from determining which
URL was forbidden.

Note that this type of technique is referred to as "security by
obscurity." While it hides the information from casual inspection,
anyone with more than passing understanding of how their browser works
will be able to see what actually happened, and see the URL you're
trying to hide, either by looking in their browsers debugging panel,
or by examining network traffic.


.. _See_Also_obscure-forbidden:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/core.html#errordocument


.. _Recipe_RequireAll:

Combining requirements
~~~~~~~~~~~~~~~~~~~~~~

.. index:: RequireAny

.. index:: RequireAll

.. index:: RequireNone

.. index:: Satisfy

.. index:: Order


.. _Problem_RequireAll:

Problem
~~~~~~~


You want to combine several authorization requirements into a single
access policy.


.. _Solution_RequireAll:

Solution
~~~~~~~~


In 2.2, you must use the ``Order`` and ``Satisfy`` directives to combine
multiple requirements.

[role="v22"]

.. code-block:: text

   <Directory /var/www/pretty_ponies>
       Satisfy All
       Order allow,deny
   
       Require valid-user
       Allow from 10.10
   </Directory>


In 2.4, use the ``<RequireAny>``, ``<RequireAll>``, and ``<RequireNone>`` containers
to group several authorization requirements, giving much more
flexibility over the 2.2 configuration.

[role="v24"]

.. code-block:: text

   <Directory /var/www/pretty_ponies>
       <RequireAll>
           Require valid-user
           Require ip 10.10
       </RequireAll>
   </Direcory>


.. _Discussion_RequireAll:

Discussion
~~~~~~~~~~


As mentioned in earlier recipes, the ``Satisfy`` directive in httpd 2.2
specified whether all access restrictions must be enforced, or only
one of them.

The new syntax in httpd 2.4 gives a much more fine-grained control
over which access requirements must be enforced, and in what
combination.

In the examples given, the two recipes - the 2.2 and 2.4 recipes - are
functionally identical. However, as soon as more than two access
control requirements are in play, things get a little more complex. In
httpd 2.2 and earlier, you only had the option of specifing ``All`` or
``Any``, in 2.4 you can be more specific. For example if you want to say
"must be a valid user, and also must be from either the 10.10 network,
or the 192.168.10 network", you can do that as follows:


.. code-block:: text

   <RequireAll>
       Require valid-user
       <RequireAny>
           Require ip 10.10
           Require ip 192.168.10
       </RequireAny>
   </RequireAll>


In addition to the two directives shown above - ``<RequireAll>`` and
``<RequireAny>``, there's a third directive, ``<RequireNone>``, which
provides a negation of ``<RequireAll>``. Thus, the following two blocks
are identical:


.. code-block:: text

   <RequireAll>
       Require not ip 192.168.1
       Require not ip 10.10.3
       Require not localhost
   </RequireAll>


and ...


.. code-block:: text

   <RequireNone>
       Require ip 192.168.1
       Require ip 10.10.3
       Require localhost
   </RequireNone>


These containers can be nested to any depth, to express the complexity
of your access control requirements. For example, consider:


.. code-block:: text

   <RequireAll>
       <RequireAny>
   	Require user superadmin
   	<RequireAll>
   	    Require group admins
   	    Require ldap-group cn=Administrators,o=Airius
   	    <RequireAny>
   		Require group sales
   	Require ldap-attribute dept="sales"
   	    </RequireAny>
   	</RequireAll>
       </RequireAny>
       <RequireNone>
   	Require group temps
   	Require ldap-group cn=Temporary Employees,o=Airius
       </RequireNone>
   </RequireAll>


Consult the documentation for these directives for additional examples
of their use.


.. _See_Also_RequireAll:

See Also
~~~~~~~~


* https://httpd.apache.org/docs//mod/mod_authz_core.html#requireall
* https://httpd.apache.org/docs//mod/mod_authz_core.html#requireany
* https://httpd.apache.org/docs//mod/mod_authz_core.html#requirenone

Summary


This chapter covers a number of related concepts, all of which fit
loosely under Authentication, Authorization, and Access Control. Taken
together, they give some suggestions of how you can specify who can
access your web content.

Remember that this is only a small part of the larger topic of
security, albeit a very important part.

In the next chapter, we'll discuss some of the other aspects of
ensuring the security of your web server.

