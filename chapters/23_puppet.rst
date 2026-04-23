
.. _Chapter_Puppet:

==============================
Configuring Apache with Puppet
==============================

.. index:: Puppet

.. index:: Puppet,apache module

.. index:: Configuration files


The Apache HTTP server package is quite a complex beast -- some might
call it 'featureful,' and others have referred to it as the
'all-singing, all-dancing Web server' -- because it comes with an
abundance of features, settings, options, directives, knobs, and dials
with which it can be configured.

The **puppetlabs/apache** module from PuppetForge provides one way to
make sense out of all these options, and choose only the ones you want
-- while silently making adjustments to others in order to make your
choices work.

The PuppetForge **puppetlabs/apache** page can be found at
https://forge.puppet.com/puppetlabs/apache,
and it's quite replete with examples and explanations.


.. tip::

   .Check Version Compatibility!
   ====
   Before chraging ahead with any of these recipes, you should check the
   PuppetForge page and verify that the module is compatible with the
   version of Puppet you're using.  You may have to install an older
   version of the module if your Puppet environment is running somewhat
   behind the latest release.
   ====


This chapter does **not** provide a primer on how to install, configure,
nor use the Puppet configuration tool -- only on how to use the
**puppetlabs/apache** Puppet module to help configure your server.  One
initial warning seems appropriate, though, since it addresses an issue
often overlooked which can make debugging a **real** trial:


.. _apacheckbk-PUPPET-1-NOTE-1:


**Ensuring Proper Name Scoping**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. warning::

   To avoid having to troubleshoot hard-to-debug scoping issues, it is a
   good practice to use '**``::``**' as a prefix whenever refering to something
   that hasn't been defined in the current scope.  For example:

   ** **Facts*::
     Use ``$::fqdn`` or ``$::operatingsystemrelease`` (or, if being
     interpolated in strings, ``"${::fqdn}"`` or
     ``"${::operatingsystemrelease}"``) rather than just the bare ``$fqdn``
     name.  Facts are not namespaced -- that is, they are simple names
     with no embedded '**``::``**' sequences to narrow their scope -- they're
     **always** global.

   ** **Global parameters*::
     (Such as set in the host's manifest or
     Foreman!footnoteref:[apacheckbk-PUPPET-1-FNOTE-1,Foreman
     (https://theforeman.org/) is a F/LOSS tool for managing
     virtual machines **via** a Web interface.] parameters.)  Similar to
     facts, these names are not namespaced, and should be treated the
     same way when referenced: ``$::gblvarname`` or ``"${::gblvarname}"``.

   ** **Resource declarations and class/resource references*::
     It's entirely possible for a Puppet module to include a class or
     resource name that happens to be the same as a top-level Puppet
     module.  For this reason, you should **always** fully scope your
     references -- both internal to your module **and external** -- so
     Puppet will be sure which one you mean.  For example:

     include ::mymodule::apache
     class { '::apache':
       require     => Class['::mymodule::apache'],
     }
     $mymodvar     =  $::mymodule::apache::somevar
     $apachemodvar =  $::apache::somevar


Now, on to the reipes!


.. _Recipe_Basic_Config:

Basic Configuration


.. todo:: 


.. _Problem_Basic_Config:

Problem
~~~~~~~


.. todo:: 


.. _Solution_Basic_Config:

Solution
~~~~~~~~


.. todo:: 


.. _Discussion_Basic_Config:

Discussion
~~~~~~~~~~


.. todo:: 


.. _See_Also_Basic_Config:

See Also
~~~~~~~~


.. todo:: 


.. _Recipe_Server_Tokens:

Specifying Server Tokens


.. todo:: 


.. _Problem_Server_Tokens:

Problem
~~~~~~~


.. todo:: 


.. _Solution_Server_Tokens:

Solution
~~~~~~~~


.. todo:: 


.. _Discussion_Server_Tokens:

Discussion
~~~~~~~~~~


.. todo:: 


.. _See_Also_Server_Tokens:

See Also
~~~~~~~~


.. todo:: 


.. _Recipe_VHosts:

Virtual Hosts

.. index:: Virtual hosts

.. index:: Vhosts


.. todo:: 


.. _Problem_VHosts:

Problem
~~~~~~~


.. todo:: 


.. _Solution_VHosts:

Solution
~~~~~~~~


.. todo:: 


.. _Discussion_VHosts:

Discussion
~~~~~~~~~~


.. todo:: 


.. _See_Also_VHosts:

See Also
~~~~~~~~


* <<Chapter_Virtual_hosts>, **Virtual Hosts**


.. todo:: 


.. _Recipe_SSL:

Setting Up SSL

.. index:: SSL

.. index:: TLS

.. index:: Secure websites


.. todo:: 


.. _Problem_SSL:

Problem
~~~~~~~


.. todo:: 


.. _Solution_SSL:

Solution
~~~~~~~~


.. code-block:: text

   class { '::apache::mod::ssl':
     ssl_compression => true,
   }
   
   $base_host        =  'myweb.example.com'
   
   ::apache::vhost { "${base_host}-https":
     servername      => $base_host,
     port            => '443',
     docroot         => "/var/www/${base_host}",
     ssl             => true,
     ssl_cert        => "/etc/pki/httpd/${base_host}.crt",
     ssl_key         => "/etc/pki/httpd/${base_host}.key",
   }


.. todo:: 


.. _Discussion_SSL:

Discussion
~~~~~~~~~~


.. todo:: 


.. _See_Also_SSL:

See Also
~~~~~~~~


* :ref:`Chapter_SSL_and_TLS`, **SSL and TLS**


.. todo:: 


.. _Recipe_Redirect_to_SSL:

Redirecting all +http://+ requests to +https://+


.. todo:: 


.. _Problem_Redirect_to_SSL:

Problem
~~~~~~~


.. todo:: 


.. _Solution_Redirect_to_SSL:

Solution
~~~~~~~~


.. code-block:: text

   class { '::apache::mod::ssl':
     ssl_compression => true,
   }
   
   $base_host        =  'myweb.example.com'
   
   ::apache::vhost { "${base_host}-http":
     servername      => $base_host,
     port            => '80',
     docroot         => "/var/www/${base_host}",
     redirect_status => 'permanent',
     redirect_dest   => "https://${base_host}/",
   }
   
   ::apache::vhost { "${base_host}-https":
     servername      => $base_host,
     port            => '443',
     docroot         => "/var/www/${base_host}",
     ssl             => true,
   }


.. _Discussion_Redirect_to_SSL:

Discussion
~~~~~~~~~~


.. todo:: 


.. _See_Also_Redirect_to_SSL:

See Also
~~~~~~~~


* :ref:`Recipe_SSL`
* :ref:`Chapter_SSL_and_TLS`, **SSL and TLS**


.. todo:: 


.. _Recipe_ModuleList:

Managing the Module List


.. todo:: 


.. _Problem_ModuleList:

Problem
~~~~~~~


.. todo:: 


.. _Solution_ModuleList:

Solution
~~~~~~~~


.. todo:: 


.. _Discussion_ModuleList:

Discussion
~~~~~~~~~~


.. todo:: 


.. _See_Also_ModuleList:

See Also
~~~~~~~~


.. todo:: 


Summary


.. todo:: 
