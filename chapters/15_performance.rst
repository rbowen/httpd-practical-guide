
.. _Chapter_Performance_and_testing:

=======================
Performance and Testing
=======================

.. index:: Performance

.. index:: Testing


// TODO: Add recipe about Nikto and friends, either here or in the
// security chapter.

// TODO: Review EVERY recipe in this chapter carefuly. Update for
// 2.2/2.4.

Your Web site can probably be made to run faster if you are willing
to make a few trade-offs and spend a little time benchmarking your site to
see what is really slowing it down.

There are a number of things that you can configure differently to
get a performance boost. Although, there are other things to which you may
have to make more substantial changes. It all depends on what you can
afford to give up and what you are willing to trade off. For example, in
many cases, you may need to trade performance for security, or vice
versa.

In this chapter, we make some recommendations of things that you can
change, and we warn against things that can cause substantial slow-downs.
Be aware that Web sites are very individual, and what may speed up one Web
site may not necessarily speed up another Web site.

Topics covered include hardware considerations, configuration file
changes, and dynamic content
generation, which can all be factors in getting every ounce of performance
out of your Web site.


.. _apacheckbk-CHP-11-NOTE-116:


.. note::

   Very frequently, application developers create programs in
   conditions that don't accurately reflect the conditions under which they
   will run in production. Consequently, the application that seemed to run
   adequately fast with the test database of 100 records, runs painfully
   slowly with the production database of 200,000 records.

   By ensuring that your test environment is at least as demanding as
   your production environment, you greatly reduce the chances that your
   application will perform unexpectedly slow when you roll it out.


.. _Recipe_how-much-ram:

Determining How Much Memory You Need


.. _Problem_how-much-ram:

Problem
~~~~~~~


You want to ensure that you have sufficient RAM in your server.


.. _Solution_how-much-ram:

Solution
~~~~~~~~


Find the instances of Apache in your process list, and determine
an average memory footprint for an Apache process. Multiply this
number by your peak load (maximum number of concurrent Web clients
you'll be serving).


.. _Discussion_how-much-ram:

Discussion
~~~~~~~~~~


Because there is very little else that you can do at the
hardware level to make your server faster, short of purchasing faster
hardware, it is important to make sure that you have as much RAM as
you need.

Determining how much memory you need is an inexact science, to
say the least. In order to take an educated guess, you need to observe
your server under load, and see how much memory it is using.

The amount of memory used by one Apache process will vary
greatly from one server to another, based on what modules you have
installed and what the server is being called upon to do. Only by
looking at your own server can you get an accurate estimate of what
this quantity is for your particular situation.

Tools such as **top** and
**ps** may be used to examine your
process list and determine the size of processes. The
server-status handler, provided by ``mod_status``, may be used to determine the
total number of Apache processes running at a given time.

If, for example, you determine that your Apache processes are
using 4 MB of memory each, and under peak load, you find that you are
running 125 Apache processes, then you will need, at a bare minimum,
500 MB of RAM in the server to handle this peak load. Remember that
memory is also needed for the operating system, and any other
applications and services that are running on the system, in addition
to Apache. So in reality you will need more than this amount to handle
this peak load.

If, by contrast, you are unable to add more memory to the
server, for whatever reason, you can use the same technique to figure
out the maximum number of child processes that you are capable of
serving at any one time, and use the **MaxClients** directive to limit Apache to that
many processes:


.. code-block:: text

   MaxClients 125


.. _See_Also_how-much-ram:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/misc/perf-tuning.html


.. _Recipe_benchmarking-ab:

Benchmarking Apache with ab


.. _Problem_benchmarking-ab:

Problem
~~~~~~~


You want to benchmark changes that you are making to verify that
        they are in fact making a difference in performance.


.. _Solution_benchmarking-ab:

Solution
~~~~~~~~


Use **ab** (Apache bench), which
you will find in the **bin**
directory of your Apache installation:


.. code-block:: text

   ab -n 1000 -c 10 http://www.example.com/test.html


.. _Discussion_benchmarking-ab:

Discussion
~~~~~~~~~~


Apache bench is a command-line utility that comes with Apache
and lets you do very basic performance testing of your server. It is
especially useful for making small changes to your configuration and
testing server performance before and after the change.

The arguments given in the previous example tell **ab** to request the resource
**http://www.example.com/test.html** 1000 times
(-n 1000 indicates the number of requests) and to
make these requests 10 at a time (-c 10 indicates the
concurrency level).

Other arguments that may be specified can be seen by running
**ab** with the -h
flag. Of particular interest is the -k flag, which
enables keepalive mode. See the following keepalive recipe for additional details
on this matter.

There are a few things to note about **ab** when using it to evaluate
performance.

Apache bench does not mimic Web site usage by real people. It
requests the same resource
repeatedly to test the performance of that one thing. For example, you
may use **ab** to test the performance
of a particular CGI program, before and after a performance-related
change was made to it. Or you may use it to measure the impact of
turning on **.htaccess** files, or
content negotiation, for a particular directory. Real users, of
course, do not repeatedly load the same page, and so performance
measurements made using **ab** may not
reflect actual real-world performance of your Web site.

You should probably not run the Web server and **ab** on the same machine, as this will
introduce more uncertainty into the measurement. With both **ab** and the Web server itself consuming
system resources, you will receive significantly slower performance
than if you were to run **ab** on some
other machine, accessing the server over the network. However, also be
aware that running **ab** on another
machine will introduce network latency, which is not present when
running it on the same machine as the server.

Finally, there are many factors that can affect performance of
the server, so you will not get the same numbers each time you run the
test. Network conditions, other processes running on the client or
server machine, and a variety of other things may influence your
results slightly one way or another. The best way to reduce the impact
of environmental changes is to
run a large number of tests and average your results. Also, make sure
that you change as few things as possible—ideally, just one—between
tests, so that you can be more sure what change has made any
differences you can see.

Finally, you need to understand that, while **ab** gives you a good idea of whether certain
changes have improved performance, it does not give a good simulation
of actual users. Actual users don't simply fetch the same resource
repeatedly; they obtain a variety of different resources from various
places on your site. Thus, actual site usage conditions may produce
different performance issues than those revealed by **ab**.


.. _See_Also_benchmarking-ab:

See Also
~~~~~~~~


* The manpage for the **ab** tool
          
* http://httpd.apache.org/docs/programs/ab.html


.. _Tuning_Keepalive_Settings_id149968:

Tuning KeepAlive Settings


.. _Problem_id149983:

Problem
~~~~~~~


You want to tune the keepalive-related directives to the best
        possible setting for your Web site.


.. _Solution_id150027:

Solution
~~~~~~~~


Turn on the **KeepAlive**
        setting, and set the related directives to sensible values:


.. code-block:: text

   KeepAlive On
   MaxKeepAliveRequests 0
   KeepAliveTimeout 15


.. _Discussion_id150056:

Discussion
~~~~~~~~~~


The default behavior of HTTP is for each document to be
requested over a new connection. This causes a lot of time to be spent
opening and closing connections. **KeepAlive** allows multiple requests to be
made over a single connection, thus reducing the time spent
establishing socket connections. This, in turn, speeds up the load
time for clients requesting content from your site.

In addition to turning keepalive on using the **KeepAlive** directive, there are two directives that allow you to adjust the
way that it is done.

The first of these, **MaxKeepAliveRequests**, indicates how many
keepalive requests should be permitted over a single connection. There
is no reason to have this number set low. The default value for this
directive is 100, and this seems to work pretty well for most sites.
Setting this value to 0 means that an unlimited number of requests
will be permitted over a single connection. This might allow users to
load all of their content from your site over a single connection,
depending on the value of **KeepAliveTimeout** and how quickly they went
through the site.

**KeepAliveTimeout** indicates
how long a particular connection will be held open when no further
requests are received. The optimal setting for this directive depends
entirely on the nature of your Web site. You should probably think of
this value as the amount of time it takes users to absorb the content
of one page of your site before they move on to the next page. If the
users move on to the next page before the **KeepAliveTimeout** has expired, when they
click on the link for the next page of content, they will get that
next document over the same connection. If, however, that time has
already expired, they will need
to establish a new connection to the server for that next page.

You also should be aware that if users load a resource from your
site and then go away, Apache will still maintain that open connection
for them for **KeepAliveTimeout**
seconds, which makes that child process unable to serve any other
requests during that time. Therefore, setting **KeepAliveTimeout** too high is just as
undesirable as setting it too low.

In the event that **KeepAliveTimeout** is set too high, you will
see (**i.e.**, with the **server-status**
handler—see :ref:`Recipe_mod_status`) that
a significant number of processes are in keepalive mode, but are
inactive. Over time, this number will continue to grow, as more child
processes are spawned to take the place of child processes that are in
this state.

Conversely, setting **KeepAliveTimeout** too low will result in
conditions similar to having **KeepAlive** turned off entirely, when a single
client will require many connections over the course of a brief visit.
This is harder to detect than the opposite condition. In general, it
is probably better to err on the side of setting it too high, rather
than too low.

Because the length of time that any given user looks at any
given document on your site is going to be as individual as the users
themselves, and varies from page to page around your Web site, it is
very difficult to determine the best possible value of this directive
for a particular site. However, it is unlikely that this is going to
make any large impact on your overall site performance when compared
to other things that you can do. Leaving it at the default value of 5
tends to work pretty well for most sites.


.. _See_Also_id150221:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/core.html#keepalive


          
* http://httpd.apache.org/docs/mod/core.html#maxkeepaliverequests


          
* http://httpd.apache.org/docs/mod/core.html#keepalivetimeout


.. _Avoiding_DNS_Lookups_id150548:

Avoiding DNS Lookups


.. _Problem_id150562:

Problem
~~~~~~~


You want to avoid situations where you have to do DNS lookups of
        client addresses, as this is a very slow process.


.. _Solution_id150596:

Solution
~~~~~~~~


Always set the **HostNameLookups** directive to Off:


.. code-block:: text

   HostNameLookups Off


Make sure that, whenever possible, **Allow** from and/or **Deny** from directives use
the IP address, rather than the hostname of the hosts in
question.


.. _Discussion_id150703:

Discussion
~~~~~~~~~~


DNS lookups can take a very long time—anywhere from 0 to 60
seconds—and should be avoided at all costs. In the event that a client
address cannot be looked up at all, it can take up to a minute for the
lookup to time out, during which time the child process that is doing
the lookup cannot do anything else.

There are a number of cases in which Apache will need to do DNS
lookups, and so the goal here is to completely avoid those
situations.


.. _HostNameLookups_id150732:

HostNameLookups
^^^^^^^^^^^^^^^


Before Apache 1.3, **HostNameLookups**, which determines whether
Apache logs client IP addresses or hostnames, defaulted to
on, meaning that each Apache log entry required a DNS lookup to convert the
client IP address to a hostname to put in the logfile. Fortunately,
that directive now defaults to off, and so this is
primarily an admonition to leave it alone.

If you need to have these addresses converted to hostnames,
this should be done by another program, preferably running on a
machine other than your production Web server. That is, you really
should copy the file to some other machine for the purpose of
processing, so that the effort required to do this processing does
not negatively effect your Web server's performance.

Apache comes with a utility called **logresolve**, which will process your
logfile, replacing IP addresses with hostnames. Additionally, most
logfile analysis tools will also perform this name resolution as
part of the log analysis process.


.. _Allow_and_Deny_from_hostnames_id150792:

Allow and Deny from hostnames
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


When you do host-based access control using the **Allow** from and **Deny** from directives,
Apache takes additional precautions to make sure that the client is
not spoofing its hostname. In particular, it does a DNS lookup on
the IP address of the client to obtain the name to compare against
the access restriction. It then looks up the name that was obtained,
just to make sure that the DNS record is not being faked. [#apacheckbk-CHP-11-FNOTE-1]_

For the sake of better performance, therefore, it is much
better to use an IP address, rather than a name, in **Allow** and **Deny** directives.


.. _See_Also_id150864:

See Also
~~~~~~~~


* :ref:`Recipe_Log_Hostnames`


.. _Optimizing_Symbolic_Links_id150895:

Optimizing Symbolic Links


.. _Problem_id150910:

Problem
~~~~~~~


You wish to balance the security needs associated with symbolic
        links with the performance impact of a solution, such as using
        **Options**
        **SymLinksIfOwnerMatch**, which
        causes a server slowdown.


.. _Solution_id150950:

Solution
~~~~~~~~


For tightest security, use **Options**
        **SymlinksIfOwnerMatch**, or
        **Options**
        **-FollowSymLinks** if you seldom or
        never use symlinks.

For best performance, use **Options**
        **FollowSymlinks**.


.. _Discussion_id151025:

Discussion
~~~~~~~~~~


Symbolic links are an area in which you need to weigh
performance against security and make the decision that makes the most
sense in your particular situation.

In the normal everyday operation of a Unixish operating system,
symbolic links are considered to be the same as the file to which they
link. [#apacheckbk-CHP-11-FNOTE-2]_ When you **cd** into a
directory, you don't need to be aware of whether that was a symlink or
not. It just works.

Apache, by contrast, has to consider whether each file and
directory is a symlink or not, if the server is configured not to
follow symlinks. And, additionally, if **Option** SymlinksIfOwnerMatch
is turned on, Apache not only has to check if the particular file is a
symlink, but also has to check the ownership of the link itself and of
the target, in the event that it is a symlink. Although this enforces
a certain security policy, it takes a substantial amount of time and
so slows down the operation of your server.

In the trade-off between security and performance, in the matter
of symbolic links, here are the guidelines.

If you are primarily concerned about security, never permit the
following of symbolic links. It may permit someone to create a link
from a document directory to content that you would not want to be on
a public server. Or, if there are cases in which you really need
symlinks, use **Options**
SymlinksIfOwnerMatch, which requires that someone may
only link to files that they own and will presumably protect you from
having a user link to a portion of the filesystem that is not already
under her control.

If you are concerned about performance, always use **Options**
**FollowSymlinks**, and never use
**Options**
**SymlinksIfOwnerMatch**. **Options**
**FollowSymlinks** permits Apache to
follow symbolic links in the manner of most Unixish applications—that
is, Apache does not even need to check to see if the file in question
is a symlink or not.


.. _See_Also_id151158:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/core.html#options


.. _Recipe_Performance_impact_of_htaccess_files:

Performance impact of htaccess files

.. index:: .htaccess,Performance

.. index:: htaccess,Performance

.. index:: AllowOverride


.. _Problem_Performance_impact_of_htaccess_files:

Problem
~~~~~~~


You want **per**-directory configuration but
want to avoid the performance hit of **.htaccess** files.


.. _Solution_Performance_impact_of_htaccess_files:

Solution
~~~~~~~~


Turn on **AllowOverride** only in
directories where it is required, and tell Apache not to waste time
looking for **.htaccess** files elsewhere:


.. code-block:: text

   AllowOverride None


Then use **&lt;Directory&gt;**
sections to selectively enable **.htaccess** files only where needed.


.. _Discussion_Performance_impact_of_htaccess_files:

Discussion
~~~~~~~~~~


**.htaccess** files can cause a
substantial reduction in Apache's performance, because it must check
for a **.htaccess** in every
directory along the path to the requested file to be assured of
getting all of the relevant configuration overrides. This is necessary
because Apache configuration directives apply not only to the
directory in which they are set, but also to all subdirectories. Thus,
we must check for **.htaccess** files
in parent directories, as well as in the current directory, to find
any directives that would trickle down the current directory.

For example, if, for some reason, you had **AllowOverride**
**All** enabled for all directories
and your **DocumentRoot** was **/usr/local/apache/htdocs**, then a request
for the URL
**http://example.com/events/parties/christmas.html**
would result in the following files being looked for and, if found,
opened and searched for configuration directives:


.. code-block:: text

   /.htaccess
   /usr/.htaccess
   /usr/local/.htaccess
   /usr/local/apache/.htaccess
   /usr/local/apache/htdocs/.htaccess
   /usr/local/apache/htdocs/events/.htaccess
   /usr/local/apache/htdocs/events/parties/.htaccess


Now, hopefully, you would never have **AllowOverride** All enabled
for your entire filesystem, so
this is a worst-case scenario. However, occasionally, when people do
not adequately understand what this configuration directive does, they
will enable this option for their entire filesystem and suffer poor
performance as a result.

The recommended solution is by far the best way to solve this
problem. The **&lt;Directory&gt;** directive is
specifically for this situation, and **.htaccess** files should really only be used
in the situation where configuration changes are needed and access to
the main server configuration file is not readily available.

For example, if you have a **.htaccess** file in **/usr/local/apache/htdocs/events** containing
the directive:


.. code-block:: text

   AddEncoding x-gzip tgz


You should instead simply replace this with the following in
your main configuration file:


.. code-block:: text

   <Directory /usr/local/apache/htdocs/event>
       AddEncoding x-gzip tgz
   </Directory>


Which is to say, anything that appears in a **.htaccess** can, instead, appear in a
**&lt;Directory&gt;** section, referring to
that same directory.

If you are compelled to permit **.htaccess** files somewhere on your Web site,
you should only permit them in the specific directory where they are
needed. For example, if you particularly need to permit **.htaccess** files in the directory **/www/htdocs/users/leopold/**, then you should
explicitly allow then for only this directory:


.. code-block:: text

   <Directory /www/htdocs/users/leopold>
       AllowOverride All
   </Directory>


This directive lets
you be very specific about what types of directives you permit in
**.htaccess** files, and you should
make an effort only to permit those directives that are actually
needed. That is, rather than using the All argument,
you should allow specific types of directives as needed. In
particular, the Options argument to **AllowOverride** should be avoided, if
possible, as it may enable users to turn on features that you have
turned off for security reasons.

Finally, note that as hard drive performance improves, and the prevalance 
of SSD (Solid State Drive) increases, the performance impact of these
additional file accesses drops. Many people report that benchmarking
the use of unnecessary ``.htaccess`` files does not result in the kind
of performance degradation we saw just a few years ago.

We still recommend avoiding the use of ``.htaccess`` files whenever
possible, for the simple reason that it makes it so much more
difficult to troubleshoot problems when you have to look in multiple
places to determine what configuration is actually in effect.


.. _See_Also_Performance_impact_of_htaccess_files:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/howto/htaccess.html

* :ref:`Recipe_AllowOverride-categories`

* :ref:`Recipe_AllowOverrideList`


.. _Disabling_Content_Negotiation_id151667:

Disabling Content Negotiation


.. _Problem_id151681:

Problem
~~~~~~~


Content negotiation causes a big reduction in performance.


.. _Solution_id151717:

Solution
~~~~~~~~


Disable content negotiation where it is not needed. If you do
require content negotiation, use the type-map
handler, rather than the MultiViews option:


.. code-block:: text

   Options -MultiViews
   AddHandler type-map var


.. _Discussion_id151751:

Discussion
~~~~~~~~~~


If at all possible, disable content negotiation. However, if you
must do content negotiation—if,
for example, you have a multilingual Web site—you should use the
type-map handler, rather than
the MultiViews method.

When MultiViews is used, Apache needs to get a
directory listing each time a request is made. The resource requested
is compared to the directory listing to see what variants of that
resource might exist. For example, if **index.html** is requested, the variants
**index.html.en** and **index.html.fr** might exist to satisfy that
request. Each matching variant is compared with the user's
preferences, expressed in the various ``Accept`` headers passed by the client. This
information allows Apache to determine which resource is best suited
to the user's needs.

However, this process can be very time-consuming, particularly
for large directories or resources with large numbers of variants. By
putting the information in a **.var**
file and allowing the type-map handler to be used
instead, you eliminate the requirement to get a directory listing, and
greatly reduce the amount of work that Apache must do to determine the
correct variant to send to the user.

The **.var** file just needs to
contain a listing of the variants of a particular resource and
describe their important attributes.

If you have, for example, English, French, and Hebrew variants
of the resource **index.html**, you may express this in a
**.var** file called **index.html.var** containing information about
each of the various variants. This file might look like the
following:


.. code-block:: text

   URI: index.html.en
   Content-language: en
   Content-type: text/html
   
   URI: index.html.fr
   Content-language: fr
   Content-type: text/html
   
   URI: index.html.he.iso8859-8
   Content-language: he
   Content-type: text/html;charset=ISO-8859-8


This file should be placed in the same directory as the variants
        of this resource, which are called **index.html.en**, **index.html.fr**, and **index.html.he.iso8859-8**.

Note that the Hebrew variant of the document indicates an
        alternate character set, both in the name of the file itself, and in
        the ``Content-type`` header
        field.

Enable the **.var** file by
        adding a **AddHandler** directive to
        your configuration file, as follows:


.. code-block:: text

   AddHandler type-map .var


.. _apacheckbk-CHP-11-NOTE-122:


.. tip::

   Each of the file extensions used in these filenames should
   have an associated directive
   in your configuration file. This is not something that you should
   have to add—these should appear in your default configuration file.
   Each of the language indicators will have an associated **AddLanguage** directive, while the character
   set indicator will have an **AddCharset** directive.


In contrast to MultiViews, this technique gets
        all of its information from this **.var** file instead of from a directory
        listing, which is much less efficient.

You can further reduce the performance impact of content
        negotiation by indicating that negotiated documents can be cached.
        This is accomplished by the directive:


.. code-block:: text

   CacheNegotiatedDocs On


Caching negotiated documents can cause unpleasant results, such
        as people getting files in a language that they cannot read or in
        document formats that they don't know how to render.

If possible, you should completely avoid content negotiation in
        any form, as it will greatly slow down your server no matter which
        technique you use.


.. _See_Also_id152114:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_negotiation.html
            


          
* http://httpd.apache.org/docs/mod/mod_mime.html#addhandler


          
* http://httpd.apache.org/docs/mod/mod_mime.html#addcharset


          
* http://httpd.apache.org/docs/mod/mod_mime.html#addlanguage


          
* http://httpd.apache.org/docs/mod/core.html#optionsr


.. _Optimizing_Process_Creation_id152208:

Optimizing Process Creation


.. _Problem_id152223:

Problem
~~~~~~~


You're using Apache 1.3, or Apache 2.0 with the **prefork** MPM, and you want to tune **MinSpareServers** and **MaxSpareServers** to the best settings for
        your Web site.


.. _Solution_id152289:

Solution
~~~~~~~~


Will vary from one site to another. You'll need to watch traffic
        on your site and decide accordingly.


.. _Discussion_id152309:

Discussion
~~~~~~~~~~


The **MinSpareServers** and
**MaxSpareServers** directives control
the size of the server pool so that incoming requests will always have
a child process waiting to serve them. In particular, if there are
fewer than **MinSpareServers** idle
processes, Apache will create more processes until that minimum is
reached. Similarly, if there are ever more than **MaxSpareServers** processes, Apache will kill
off processes until there are fewer than that maximum. These things
will happen as the site traffic fluctuates on a normal day.

The best values for these directives for your particular site
depends on the amount and the rate at which traffic fluctuates. If
your site is prone to large spikes in traffic, **MinSpareServers** needs
to be large enough to absorb those spikes. The idea is to never have a
situation where requests come in to your site, and there are no idle
server processes waiting to handle the request. If traffic patterns on
your site are fairly smooth curves with no abrupt spikes, the default
values may be sufficient.

The best way to watch exactly how much load there is on your
server is by looking at the server-status handler
output. (See :ref:`Recipe_mod_status`.)

You also should set **MaxClients** to a value such that you don't
run out of server resources during heavy server loads. For example, if
your average Apache process consumes 2 MB of memory and you have a
total of 256 MB of RAM available, allowing a little bit of memory for
other processes, you probably don't want to set **MaxClients** any higher than about 120. If you
run out of RAM and start using swap space, your server performance
will abruptly go downhill and will not recover until you are no longer
using swap. You can watch memory usage by running a program such as
**top**, which shows running processes
and how much memory each is using.


.. _See_Also_id152467:

See Also
~~~~~~~~


* :ref:`Tuning_Thread_Creation_id152525`


.. _Tuning_Thread_Creation_id152525:

Tuning Thread Creation


.. _Problem_id152539:

Problem
~~~~~~~


You're using Apache 2.0 with one of the threaded MPMs, and you
        want to optimize the settings for the number of threads.


.. _Solution_id152586:

Solution
~~~~~~~~


Will vary from server to server.


.. _Discussion_id152605:

Discussion
~~~~~~~~~~


The various threaded MPMs on Apache 2.0 handle thread creation
        somewhat differently. In Apache 1.3, the Windows and Netware versions
        are threaded, whereas the Unixish version is not. Tuning the thread
        creation values will vary from one of these versions to
        another.


.. _Setting_the_number_of_threads_on_single-child_MPMs_id152627:

Setting the number of threads on single-child MPMs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


On MPMs that run Apache with a single threaded child process,
          such as the Windows MPM (``mpm_winnt``) and the Windows and Netware
          versions of Apache 1.3, there are a fixed number of threads in the
          child process. This number is controlled by the **ThreadsPerChild** directive and must be
          large enough to handle the peak traffic of the site on any given
          day. There really is no performance tuning that can be done here, as
          this number is fixed throughout the lifetime of the Apache
          process.


.. _Number_of_threads_when_using_the_worker_MPM_id152686:

Number of threads when using the worker MPM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


The **worker** MPM has a
          fixed number of threads per child process but has a variable number
          of child processes so that increased server load can be absorbed. A
          typical configuration might look like the following:


.. code-block:: text

   StartServers 2
   MaxClients 150
   MinSpareThreads 25
   MaxSpareThreads 75
   ThreadsPerChild 25
   ServerLimit 16


The **MinSpareThreads** and
          **MaxSpareThreads** directives
          control the size of the idle pool of threads, so that incoming
          clients will always have an idle thread waiting to serve their
          request. The **ThreadsPerChild**
          directive indicates how many threads are in each child process so
          when the number of available idle threads drops below **MinSpareThreads**, Apache will launch a new
          child process populated with **ThreadsPerChild** threads. Similarly, when
          server load is reduced and the number of idle threads is greater
          than **MaxSpareThreads**, Apache will
          kill off one or more child processes to reduce the idle pool to that
          number or less.

The goal, when setting these values, is to ensure that there
          are always idle threads ready to serve any incoming client's request
          without having to create a new one. The previous example will work
          for most sites, as it will ensure that there is at least one
          completely unused child process, populated with 25 threads, waiting
          for incoming requests. As soon as threads within this process start
          to be used, a new child process will be launched for future
          requests.

The values of **MaxClients**
          and **ServerLimit** should be set so
          that you will never run out of RAM when a new child process is
          launched. Look at your process list, using **top** or a similar utility, and ensure that
          **ServerLimit**, multiplied by the
          size of an individual server process, does not exceed your available
          RAM. **MaxClients** should be less
          than, or equal to, **ServerLimit**
          multiplied by **ThreadsPerChild**.


.. _Setting_the_number_of_threads_when_using_Netware_or_the_id152878:

Setting the number of threads when using netware or the perchild MPM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Whereas with most of the other MPMs the **MinSpareThreads** and **MaxSpareThreads** directives are
          server-wide, in the **perchild**
          and **netware** MPMs, these
          directives are assessed per
          child process. Of course, with the **netware** MPM, there is only one child
          process, so it amounts to the same thing.

With the **netware** MPM,
          threads are created and reaped as needed to keep the number of spare
          threads between the limits imposed by **MinSpareThreads** and **MaxSpareThreads**. The
          total number of threads must be kept at all times below the limit
          imposed by the **MaxThreads**
          directive.


.. _See_Also_id153083:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mpm.html


.. _Caching_Frequently_Viewed_Files_id153126:

Caching Frequently Viewed Files


.. _Problem_id153140:

Problem
~~~~~~~


You want to cache files that are viewed frequently, such as your
site's front page, so that they don't have to be loaded from the
filesystem every time.


.. _Solution_id153184:

Solution
~~~~~~~~


Use ``mod_file_cache`` to cache these files, or an open file handle, in
memory, for faster loading of the files.


.. code-block:: text

   MMapFile /www/htdocs/index.html
   CacheFile /www/htdocs/other_page.html


.. _Discussion_id153318:

Discussion
~~~~~~~~~~


For files that are frequently accessed, it may be desirable to cache
that file in some fashion to save disk access time. The ``MMapFile`` directive loads a file into RAM,
and subsequent requests for that file are served directly out of RAM,
rather than from the filesystem. The ``CacheFile`` directive, on the
other hand, opens the file and caches the file handle, saving time on subsequent file
opens.

This functionality is provided by the ``mod_file_cache`` module, which is labelled as
experimental, and is not built into Apache by default. To enable this
module, you need to specify the ``--enable-file-cache``
flag to ``configure`` when building Apache httpd. ``mod_file_cache`` provides
both the ``MMapFile`` and ``CacheFile`` directives.

These directives take a single file as an argument, and there is
not a provision for specifying a directory or set of directories.
However, If you wish to have the entire contents of a directory mapped into
memory, the documentation provides the following suggestion. For the
directory in question, you would run the following command:


.. code-block:: text

   find /www/htdocs -type f -print | sed -e 's/.*/MMapFile &/' > /www/conf/mmap.conf


This produces a file, ``/www/conf/mmap.conf``, with one ``MMapFile``
diretive for each file in your document directory.

In your main server configuration file, you would then load the
file created by that command, using the **Include** directive:


.. code-block:: text

   Include /www/conf/mmap.conf


This would cause every file contained in that directory to have
the ``MMapFile`` directive invoked on it.

Note that when files are cached using one of these two
directives, any changes to the file will require a server restart
before they become visible.


.. _See_Also_id153536:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_file_cache.html


.. _Distributing_Load_Evenly_Between_Several_Servers_id153837:

Distributing Load Evenly Between Several Servers


.. _Problem_id153852:

Problem
~~~~~~~


You want to serve the same content from several servers and have
        hits distributed evenly among the servers.


.. _Solution_id153887:

Solution
~~~~~~~~


Use DNS round-robin to have requests distributed evenly, or at
        least fairly evenly, among the servers:


.. code-block:: text

   www.example.com.   86400    IN   A  192.168.10.2
   www.example.com.   86400    IN   A  192.168.10.3
   www.example.com.   86400    IN   A  192.168.10.4
   www.example.com.   86400    IN   A  192.168.10.5
   www.example.com.   86400    IN   A  192.168.10.6
   www.example.com.   86400    IN   A  192.168.10.7


Add the following to your configuration file:


.. code-block:: text

   FileETag MTime Size


.. _Discussion_id153939:

Discussion
~~~~~~~~~~


This example is an excerpt from a BIND zone file. The actual
        syntax may vary, depending on
        the particular name server software you are running.

By giving multiple addresses to the same hostname, you cause
        hits to be evenly distributed among the various servers listed. The
        name server, when asked for this particular name, will give out the
        addresses listed in a round-robin fashion, causing requests to be sent
        to one server after the other. The individual servers need be configured only to answer requests from
        the specified name.

Running the **host** command on
        the name in question will result in a list of possible answers, but
        each time you run the command, you'll get a different answer
        first:


.. code-block:: text

   % host www.example.com
   www.example.com has address 192.168.10.2
   www.example.com has address 192.168.10.3
   www.example.com has address 192.168.10.4
   www.example.com has address 192.168.10.5
   www.example.com has address 192.168.10.6
   www.example.com has address 192.168.10.7
   
   % host www.example.com
   www.example.com has address 192.168.10.7
   www.example.com has address 192.168.10.2
   www.example.com has address 192.168.10.3
   www.example.com has address 192.168.10.4
   www.example.com has address 192.168.10.5
   www.example.com has address 192.168.10.6


.. _apacheckbk-CHP-11-NOTE-124:


.. tip::

   Make sure that when you update your DNS zone file, you also
   update the serial number and restart or reload your DNS
   server.


One of the document aspects used to determine cache freshness is
        the ``ETag`` value the server
        associates with it. This usually includes a calculation based on the
        document's actual disk location, which may be different on the
        different backend hosts. The **FileETag** settings cause that
        information to be omitted, so if the documents are truly identical
        they should all be given the same ``ETag`` value, and be indistinguishable when it
        comes to caching them.


.. _See_Also_id154026:

See Also
~~~~~~~~


* DNS and Bind by Paul Albitz and
            Cricket Liu (O'Reilly)


          
* :ref:`Forwarding_Requests_to_Another_Server_id147962`


.. _Caching_Directory_Listings_id154056:

Caching Directory Listings


.. _Problem_id154071:

Problem
~~~~~~~


You want to provide a directory listing but want to reduce the
        performance hit of doing so.


.. _Solution_id154109:

Solution
~~~~~~~~


Use the TrackModified argument to **IndexOptions** to allow browsers to cache the
        results of an auto-generated directory index:


.. code-block:: text

   IndexOptions +TrackModified


.. _Discussion_id154142:

Discussion
~~~~~~~~~~


When sending a directory listing to a client, Apache has to open
        that directory, obtain a directory listing, and determine various
        attributes of the files contained therein. This is very time
        consuming, and it would be nice to avoid this when possible.

By default, the Last Modified time sent with a directory listing
        is the time that the content is being served. Thus, when a client, or
        proxy server, makes a **HEAD** or
        conditional **GET** request to
        determine if it can use the copy that it has in cache, it will always
        decide to get a fresh copy of the content. The
        TrackModified option to **IndexOptions** cause ``mod_autoindex`` to send a Last Modified time
        corresponding to the file in the directory that was most recently
        modified. This enables browsers and proxy servers to cache this
        content, rather than retrieving it from the server each time, and also
        ensures that the listing that they have cached is in fact the latest
        version.

Note that clients that don't implement any kind of caching will
        not benefit from this directive. In particular, testing with **ab** will show no improvement from turning on
        this setting, as **ab** does not do any
        kind of content caching.


.. _See_Also_id154249:

See Also
~~~~~~~~


* The manpage for the **ab** tool


          
* http://httpd.apache.org/docs/programs/ab.html


.. _Speeding_Up_Perl_CGI_Programs_with_mod_perl_id154280:

Speeding Up Perl CGI Programs with mod_perl


.. _Problem_id154295:

Problem
~~~~~~~


You have existing functional Perl CGI programs and want them to
        run faster.


.. _Solution_id154344:

Solution
~~~~~~~~


If you have the ``mod_perl``
        module installed, you can configure it to run your Perl CGI programs
        instead of running ``mod_cgi``. This
        gives you a big performance boost, without having to modify your CGI
        code.

There are two slightly different ways to do this.

For Apache 1.3 and ``mod_perl`` version 1:


.. code-block:: text

   Alias /cgi-perl/ /usr/local/apache/cgi-bin/
   <Location /cgi-perl>
       Options ExecCGI
       SetHandler perl-script
       PerlHandler Apache::PerlRun
       PerlSendHeader On
   </Location>
   
   Alias /perl/ /usr/local/apache/cgi-bin/
   <Location /perl>
       Options ExecCGI
       SetHandler perl-script
       PerlHandler Apache::Registry
       PerlSendHeader On
   </Location>


For Apache 2.0 and ``mod_perl``
        version 2, the syntax changes slightly:


.. code-block:: text

   PerlModule ModPerl::PerlRun
   Alias /cgi-perl/ /usr/local/apache2/cgi-bin/
   <Location /cgi-perl>
       SetHandler perl-script
       PerlResponseHandler ModPerl::PerlRun
       Options +ExecCGI
   </Location>
   
   PerlModule ModPerl::Registry
   Alias /perl/ /usr/local/apache2/cgi-bin/
   <Location /perl>
       SetHandler perl-script
       PerlResponseHandler ModPerl::Registry
       Options +ExecCGI
   </Location>


.. _Discussion_id154562:

Discussion
~~~~~~~~~~


By using ``mod_perl``'s CGI
        modes, you can improve the performance of existing CGI programs
        without modifying the CGI code itself in any way. Given the previous
        configuration sections, a CGI program that was previously accessed **via**
        the URL
        **http://www.example.com/cgi-bin/program.cgi** will
        now be accessed **via** the URL
        **http://www.example.com/cgi-perl/program.cgi** to
        run it in **PerlRun** mode or **via** the
        URL **http://www.example.com/perl/program.cgi** to
        run it in **Registry** mode.

The primary difference between **PerlRun** and **Registry** is that, in **Registry**, the program code itself is cached
        after compilation, whereas in **PerlRun** mode, it is not. While this means
        that code run under **Registry** is
        faster than that executed under **PerlRun**, it also means that a greater
        degree of code quality is required. In particular, global variables
        and other careless coding practices may cause memory leaks, which, if
        run in cached mode, could eventually cause the server to run out of
        available memory.

When writing Perl CGI code to run under ``mod_perl``, and, in general, when writing any
        Perl code, it is recommended that you place the following two lines at
        the top of each program file, following the ``#!`` line:


.. code-block:: text

   use strict;
   use warnings;


Code that runs without error messages, with these two lines in
        them, runs without problems under **Registry**.


.. _apacheckbk-CHP-11-NOTE-125:


.. note::

   **strict** is not available
   before Perl 5, and **warnings** is
   not available before Perl 5.6. In versions of Perl earlier than 5.6,
   you can get behavior similar to **warnings** by using the -w
   flag to Perl. This is accomplished by adding it to the **#!** line of your Perl programs:

   #!/usr/bin/perl -w


.. _See_Also_id154769:

See Also
~~~~~~~~


* Programming Perl, Third Edition, by
  Larry Wall, Tom Christiansen, and Jon Orwant (O'Reilly)


.. _I_sect111_d1e18571:

Caching Dynamic Content


Problem
~~~~~~~


You want to cache dynamically generated documents that don't
actually change very often.


Solution
~~~~~~~~


In Apache 2.2, use the following recipe:


.. code-block:: text

   CacheEnable disk / 
   CacheRoot /var/www/cache
   CacheIgnoreCacheControl On
   CacheDefaultExpire 600


In 2.3 and later, you can use something like this:


.. code-block:: text

   CacheEnable disk / 
   CacheRoot /var/www/cache
   CacheDefaultExpire 600
   CacheMinExpire 600


Discussion
~~~~~~~~~~


Caching is usually explicitly disabled for dynamic content.
Dynamic content, by definition, is content that is generated on
demand—that is, created fresh each time it is requested. Thus, caching
it is contrary to its very nature

However, it is often—even usually—the case that dynamically
generated content doesn't actually change very much from one minute to
the next. This means that you end up wasting an awful lot of time
generating content that hasn't actually changed since the last time it
was requested. If you're doing this several times per second, you're
probably causing your server a great deal more work than is really
necessary.

The recipes above solve this problem in two slightly different
ways. The solution for 2.3 is better, but, as of this writing, 2.3
hasn't been released yet, so it's not a terribly practical solution
yet.

The recipe for Apache 2.2 takes the approach of disabling cache
control—that is, it tells Apache to ignore the request made by the
dynamic content that it not be cached, and caches it anyway. Then, for
good measure, a default cache expiration time of 5 minutes (600
seconds) is set, so that any content that is cached will be retained
at least that long.

The solution for 2.3 is slightly more elegant. It sets a minimum
cache expiration time of five minutes, as well as setting the default
expiration time. This ensures that all content is cached at least for
five minutes, but the content itself may specify a longer time, if
desired. The main difference here is that in the 2.2 solution if the
content itself sends a request that it be cached longer this will be
ignored, whereas in the 2.3 solution it will be honored.

You'll first see the 2.3 solution working when the 2.4 version
of the server is released. 2.3 is a development branch, and it will be
called 2.4 when it is ready for general use.

Make sure that the directory specified as the CacheRoot exists
and is writeable by the Apache user.


.. _See_Also_new9:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/caching.html


.. _Recipe_mod_ratelimit:

mod_ratelimit

.. index:: mod_ratelimit

.. index:: Modules,mod_ratelimit

.. index:: Rate limit

.. index:: RATE_LIMIT

.. index:: Slowing down downloads


.. _Problem_mod_ratelimit:

Problem
~~~~~~~


You want to throttle, or rate-limit, a portion of your website.


.. _Solution_mod_ratelimit:

Solution
~~~~~~~~


Use ``mod_ratelimit`` to impose a speed limit on a portion of your site.


.. code-block:: text

   <Location "/downloads">
       SetOutputFilter RATE_LIMIT
       SetEnv rate-limit 400
       SetEnv rate-initial-burst 512
   </Location>


.. _Discussion_mod_ratelimit:

Discussion
~~~~~~~~~~


``mod_ratelimit`` provides a filter, ``RATE_LIMIT``, which can throttle
transfer speeds to a specified rate in kilobytes per second (KiB/s),
specified with the environment variable ``rate-limit``. Optionally, you
may also configure a burst speed, **via** the environment variable
``rate-initial-burst``, at which data is initially sent
before being throttled back to the ``rate-limit`` value.

This can be useful for a directory containing downloadable files,
which is negatively impacting the performance of the rest of your
site, or other virtual hosts. You may also wish to apply rate limiting
to particular abusive clients.


.. _See_Also_mod_ratelimit:

See Also
~~~~~~~~


* :ref:`Recipe_mod_dialup`


.. _Recipe_mod_dialup:

mod_dialup


.. _Problem_mod_dialup:

Problem
~~~~~~~


.. _Solution_mod_dialup:

Solution
~~~~~~~~


.. _Discussion_mod_dialup:

Discussion
~~~~~~~~~~


.. _See_Also_mod_dialup:

See Also
~~~~~~~~


.. _Recipe_nikto:

Security scanning with Nikto


.. _Problem_nikto:

Problem
~~~~~~~


.. _Solution_nikto:

Solution
~~~~~~~~


.. _Discussion_nikto:

Discussion
~~~~~~~~~~


.. _See_Also_nikto:

See Also
~~~~~~~~


Summary


.. todo:: 


.. rubric:: Footnotes

.. [#apacheckbk-CHP-11-FNOTE-1] For example, the owner of the IP address could very easily put a PTR record in his reverse-DNS zone, pointing his IP address at a name belonging to someone else.
.. [#apacheckbk-CHP-11-FNOTE-2] Of course, this is not true at the filesystem level, but we're just talking about the practical user level.
