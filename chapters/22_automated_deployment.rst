.. epigraph::

   "The optimist proclaims that we live in the best of all possible
   worlds, and the pessimist fears that this is true."

   -- James Branch Cabell

.. _Chapter_Automated_Deployment:

==============================
Automated deployment
==============================

.. index::
   single: automation
   single: Ansible
   single: Puppet
   single: Chef
   single: Docker
   single: containers
   single: Terraform
   single: OpenTofu
   single: configuration management
   single: infrastructure as code
   single: deployment; automated

Introduction
------------

If you're still SSH-ing into servers and hand-editing configuration files in
production, I need you to stop. Right now. Close that terminal. I don't care
if it's "just one server" or "just a quick fix." The moment you make a change
by hand that isn't recorded somewhere reproducible, you've created a snowflake
server --- one that will betray you at 3 AM when you need to rebuild it from
scratch and can't remember what you did six months ago.

The Apache HTTP Server is, at its core, a collection of text files. Configuration
files, content files, certificate files. Text files are *exactly* what
configuration management tools were designed to manage. Every tool in this chapter
treats httpd configuration as code: versioned, tested, repeatable, and auditable.
Whether you're managing two servers or two thousand, the investment in automation
pays for itself the first time you need to rebuild after a failed upgrade, scale
horizontally under load, or prove to an auditor exactly what changed and when.

The landscape in 2026 looks like this: **Ansible** dominates the configuration
management space for new deployments, largely because it's agentless and its
learning curve is gentle. **Puppet** and **Chef** remain entrenched in large
enterprises that adopted them years ago --- they work well, they're mature, and
there's no compelling reason to rip them out if your team already knows them.
**Containers** (Docker and Podman) have changed the conversation entirely for
many deployments: if your httpd instance is stateless and your configuration is
baked into an image, you may not need traditional configuration management at all.
**Terraform** and **OpenTofu** sit at a different layer --- they provision the
infrastructure (the VM, the network, the load balancer) but deliberately do not
configure the software running on it. The common real-world pattern is Terraform
to provision, then Ansible (or a container image) to configure.

This chapter shows you how to use each of these tools to deploy and manage
Apache httpd. It is not a tutorial on any of these tools themselves --- I assume
you have a basic working knowledge of whichever platform you're using, or at
least access to its documentation. Each section stands alone, so feel free to
skip directly to the tool you care about.

.. admonition:: Modules covered

   This chapter does not focus on specific httpd modules. It covers external
   tools for deploying and managing Apache httpd configurations.


.. _Recipe_Ansible_Install:

Installing and starting httpd with Ansible
------------------------------------------

.. index::
   single: Ansible; installing httpd
   single: Ansible; playbook
   single: Ansible; handlers

Problem
~~~~~~~

You need to install Apache httpd on one or more servers and ensure the service
is running and enabled at boot, using an Ansible playbook.

Solution
~~~~~~~~

Create a playbook that installs the package, deploys a minimal configuration,
and starts the service. Use a handler for graceful restarts so that
configuration changes don't unnecessarily bounce the service:

.. code-block:: yaml

   ---
   # file: install_httpd.yml
   - name: Install and start Apache httpd
     hosts: webservers
     become: true

     vars:
       httpd_package: "{{ 'httpd' if ansible_os_family == 'RedHat' else 'apache2' }}"
       httpd_service: "{{ 'httpd' if ansible_os_family == 'RedHat' else 'apache2' }}"

     tasks:
       - name: Install httpd package
         ansible.builtin.package:
           name: "{{ httpd_package }}"
           state: present

       - name: Ensure httpd is running and enabled
         ansible.builtin.service:
           name: "{{ httpd_service }}"
           state: started
           enabled: true

       - name: Deploy main configuration file
         ansible.builtin.template:
           src: templates/httpd.conf.j2
           dest: /etc/httpd/conf/httpd.conf
           owner: root
           group: root
           mode: '0644'
           validate: httpd -t -f %s
         notify: Graceful restart httpd
         when: ansible_os_family == 'RedHat'

     handlers:
       - name: Graceful restart httpd
         ansible.builtin.service:
           name: "{{ httpd_service }}"
           state: reloaded

Discussion
~~~~~~~~~~

A few things to note about this playbook:

The ``ansible.builtin.package`` module is a generic wrapper that delegates to
``yum``, ``dnf``, or ``apt`` depending on the target system. If you know your
fleet is homogeneous, you can use ``ansible.builtin.dnf`` or
``ansible.builtin.apt`` directly for slightly better performance and
platform-specific options (like enabling a particular repository).

The ``validate`` parameter on the template task runs ``httpd -t -f %s`` against
the rendered file *before* putting it in place. If the configuration is
syntactically invalid, Ansible will fail the task and leave the existing
configuration untouched. This is one of the most underused features in Ansible
for httpd management --- use it.

Handlers only fire once, at the end of the play, regardless of how many tasks
notify them. This means that if you change three configuration files in a single
run, you get one graceful restart, not three. Use ``state: reloaded`` rather
than ``state: restarted`` to send a ``SIGHUP`` (graceful restart) instead of
stopping and starting the process, which avoids dropping active connections.

The conditional ``when: ansible_os_family == 'RedHat'`` is a simplistic example.
In production, you'd typically use separate task files included with
``ansible.builtin.include_tasks`` for each OS family.

See also
~~~~~~~~

- :ref:`Recipe_Ansible_Vhosts` for template-driven virtual host management
- :ref:`Recipe_Ansible_Roles` for using pre-built Galaxy roles
- The Ansible documentation for the ``package`` module:
  https://docs.ansible.com/ansible/latest/collections/ansible/builtin/package_module.html


.. _Recipe_Ansible_Vhosts:

Managing virtual hosts with Ansible templates
---------------------------------------------

.. index::
   single: Ansible; templates
   single: Ansible; virtual hosts
   single: Jinja2; httpd templates

Problem
~~~~~~~

You need to deploy multiple virtual host configurations from a central list,
using Jinja2 templates to generate consistent, correct configuration files
across your fleet.

Solution
~~~~~~~~

Define your virtual hosts as a list of dictionaries in your inventory or
group variables, then use a template with a loop to generate one configuration
file per vhost:

.. code-block:: yaml

   ---
   # file: group_vars/webservers.yml
   httpd_vhosts:
     - server_name: www.example.com
       document_root: /var/www/example.com/html
       server_aliases:
         - example.com
       extra_directives: |
         ErrorLog /var/log/httpd/example.com-error.log
         CustomLog /var/log/httpd/example.com-access.log combined

     - server_name: api.example.com
       document_root: /var/www/api.example.com/html
       server_aliases: []
       extra_directives: |
         ProxyPass / http://localhost:8080/
         ProxyPassReverse / http://localhost:8080/

The Jinja2 template:

.. code-block:: jinja

   {# file: templates/vhost.conf.j2 #}
   # Managed by Ansible - DO NOT EDIT MANUALLY
   <VirtualHost *:80>
       ServerName {{ item.server_name }}
   {% for alias in item.server_aliases %}
       ServerAlias {{ alias }}
   {% endfor %}
       DocumentRoot {{ item.document_root }}

       <Directory {{ item.document_root }}>
           AllowOverride None
           Require all granted
       </Directory>

   {{ item.extra_directives | indent(4) }}
   </VirtualHost>

The playbook task that deploys them:

.. code-block:: yaml

   ---
   # file: deploy_vhosts.yml (tasks section)
   - name: Deploy virtual host configurations
     ansible.builtin.template:
       src: templates/vhost.conf.j2
       dest: "/etc/httpd/conf.d/{{ item.server_name }}.conf"
       owner: root
       group: root
       mode: '0644'
       validate: httpd -t -f %s
     loop: "{{ httpd_vhosts }}"
     notify: Graceful restart httpd

   - name: Remove unmanaged vhost configurations
     ansible.builtin.find:
       paths: /etc/httpd/conf.d
       patterns: "*.conf"
       excludes: "{{ httpd_vhosts | map(attribute='server_name') | map('regex_replace', '$', '.conf') | list }}"
     register: unmanaged_vhosts

Discussion
~~~~~~~~~~

The key pattern here is **data-driven configuration**: your virtual hosts are
defined as structured data, and the template is generic. Adding a new vhost is
a one-line change to your variables file, not a new template or task.

The ``validate`` parameter works per-file here. Each rendered vhost
configuration is syntax-checked before being placed on disk. This catches
typos in your variables (like a missing ``DocumentRoot`` path) before they can
break the running server.

The "remove unmanaged configurations" pattern is worth discussing. Without it,
if you remove a vhost from your list, the old configuration file remains on
disk. You have two choices: either use ``ansible.builtin.find`` as shown above
to locate orphaned files, or adopt a pattern where you first purge the entire
configuration directory and then regenerate all files. The latter is cleaner
but creates more churn in your change reports.

The ``extra_directives`` field is a pragmatic escape hatch. Trying to model
every possible httpd directive as a structured variable leads to madness.
Instead, accept that some vhosts need custom directives and provide a free-form
text block that gets templated verbatim.

See also
~~~~~~~~

- :ref:`Recipe_Ansible_TLS` for adding TLS to your vhost templates
- :ref:`Recipe_Ansible_Install` for the base playbook structure
- The Jinja2 template documentation: https://jinja.palletsprojects.com/


.. _Recipe_Ansible_Roles:

Deploying a complete httpd stack with Ansible roles
---------------------------------------------------

.. index::
   single: Ansible; roles
   single: Ansible; Galaxy
   single: geerlingguy.apache

Problem
~~~~~~~

You want a batteries-included Ansible role that handles package installation,
service management, module loading, virtual hosts, and TLS configuration
without writing everything from scratch.

Solution
~~~~~~~~

The most widely used Ansible role for httpd is Jeff Geerling's
``geerlingguy.apache``, available on Ansible Galaxy. Install it and configure
it through role variables:

.. code-block:: bash

   $ ansible-galaxy install geerlingguy.apache

Then use it in a playbook:

.. code-block:: yaml

   ---
   # file: site.yml
   - name: Configure web servers
     hosts: webservers
     become: true

     vars:
       apache_listen_port: 80
       apache_listen_port_ssl: 443
       apache_create_vhosts: true
       apache_vhosts:
         - servername: www.example.com
           documentroot: /var/www/example.com/html
           extra_parameters: |
             ErrorLog /var/log/httpd/example-error.log
             CustomLog /var/log/httpd/example-access.log combined
       apache_vhosts_ssl:
         - servername: www.example.com
           documentroot: /var/www/example.com/html
           certificate_file: /etc/pki/tls/certs/example.com.crt
           certificate_key_file: /etc/pki/tls/private/example.com.key
           certificate_chain_file: /etc/pki/tls/certs/example.com-chain.crt
       apache_mods_enabled:
         - rewrite
         - ssl
         - headers
       apache_state: started

     roles:
       - geerlingguy.apache

Discussion
~~~~~~~~~~

The ``geerlingguy.apache`` role (with over 400 stars on GitHub and millions of
downloads) handles the cross-platform differences between Red Hat and Debian
families, manages the service lifecycle, and provides a sensible set of
defaults. It's a good starting point for most deployments.

**When to use a Galaxy role versus writing your own:**

Use a Galaxy role when:

- You need something up and running quickly
- Your requirements are generic (standard vhosts, common modules)
- You want cross-platform support without maintaining OS-specific logic
- You're working with a team that's new to Ansible

Write your own when:

- You have highly specific configuration requirements
- You need to integrate with internal systems (custom certificate authorities,
  proprietary monitoring agents)
- The Galaxy role's abstraction doesn't match your mental model
- You want to minimize external dependencies in your automation

One common mistake is treating Galaxy roles as black boxes. Read the role's
:file:`defaults/main.yml` and :file:`tasks/main.yml` before using it. If you
find yourself overriding more than a handful of variables, you've probably
outgrown the role and should fork it or write your own.

Pin your role versions in a :file:`requirements.yml` file:

.. code-block:: yaml

   ---
   # file: requirements.yml
   roles:
     - name: geerlingguy.apache
       version: "3.3.0"

This prevents unexpected breakage when a role updates its interface.

See also
~~~~~~~~

- :ref:`Recipe_Ansible_Vhosts` for a DIY approach to vhost templates
- :ref:`Recipe_Ansible_TLS` for certificate management
- Galaxy role page: https://galaxy.ansible.com/geerlingguy/apache


.. _Recipe_Ansible_TLS:

Managing TLS certificates with Ansible
---------------------------------------

.. index::
   single: Ansible; TLS
   single: Ansible; Let's Encrypt
   single: certbot
   single: TLS; automation

Problem
~~~~~~~

You need to deploy TLS certificates to your httpd servers and optionally
automate certificate issuance with Let's Encrypt via certbot.

Solution
~~~~~~~~

For pre-existing certificates (purchased or issued by an internal CA), deploy
them as files and reference them in your vhost template:

.. code-block:: yaml

   ---
   # file: deploy_tls.yml
   - name: Deploy TLS certificates
     hosts: webservers
     become: true

     tasks:
       - name: Create certificate directory
         ansible.builtin.file:
           path: /etc/pki/tls/certs
           state: directory
           mode: '0755'

       - name: Deploy certificate file
         ansible.builtin.copy:
           src: "files/certs/{{ inventory_hostname }}.crt"
           dest: /etc/pki/tls/certs/server.crt
           owner: root
           group: root
           mode: '0644'
         notify: Graceful restart httpd

       - name: Deploy private key
         ansible.builtin.copy:
           src: "files/keys/{{ inventory_hostname }}.key"
           dest: /etc/pki/tls/private/server.key
           owner: root
           group: root
           mode: '0600'
         notify: Graceful restart httpd

       - name: Deploy certificate chain
         ansible.builtin.copy:
           src: "files/certs/{{ inventory_hostname }}-chain.crt"
           dest: /etc/pki/tls/certs/server-chain.crt
           owner: root
           group: root
           mode: '0644'
         notify: Graceful restart httpd

For Let's Encrypt automation with certbot:

.. code-block:: yaml

   ---
   # file: certbot.yml
   - name: Configure Let's Encrypt certificates
     hosts: webservers
     become: true

     tasks:
       - name: Install certbot and httpd plugin
         ansible.builtin.package:
           name:
             - certbot
             - "{{ 'python3-certbot-apache' if ansible_os_family == 'Debian'
                   else 'certbot-apache' }}"
           state: present

       - name: Obtain certificate (webroot method)
         ansible.builtin.command:
           cmd: >
             certbot certonly --webroot
             -w /var/www/html
             -d {{ item.server_name }}
             {% for alias in item.server_aliases | default([]) %}
             -d {{ alias }}
             {% endfor %}
             --non-interactive --agree-tos
             --email admin@example.com
           creates: "/etc/letsencrypt/live/{{ item.server_name }}/fullchain.pem"
         loop: "{{ httpd_vhosts }}"

       - name: Ensure certbot renewal timer is active
         ansible.builtin.systemd:
           name: certbot-renew.timer
           state: started
           enabled: true

Discussion
~~~~~~~~~~

A few important considerations for TLS automation:

**Private key permissions matter.** The key file must be mode ``0600`` and owned
by root. Ansible's ``copy`` module sets permissions atomically, so there's no
window where the key is world-readable on disk.

**The webroot method vs. the Apache plugin:** The webroot method
(``--webroot``) serves the ACME challenge from a directory that httpd already
serves, which means httpd must already be running with a vhost that serves
:file:`/.well-known/acme-challenge/`. The Apache plugin (``--apache``) modifies
the httpd configuration directly, which conflicts with Ansible's desire to be
the sole manager of configuration. I recommend the webroot method for
Ansible-managed servers.

**Certificate renewal** is handled by certbot's built-in timer. However, you
need a post-renewal hook to reload httpd:

.. code-block:: bash

   # /etc/letsencrypt/renewal-hooks/deploy/reload-httpd.sh
   #!/bin/bash
   systemctl reload httpd

Deploy this hook with Ansible as well.

**Vault-encrypting private keys:** If you're storing pre-existing private keys
in your Ansible repository (as opposed to generating them with certbot), encrypt
them with ``ansible-vault``. Never commit unencrypted private keys to version
control.

See also
~~~~~~~~

- :ref:`Recipe_Ansible_Vhosts` for the vhost template that references these
  certificates
- The certbot documentation: https://certbot.eff.org/docs/
- The ``community.crypto`` Ansible collection for programmatic certificate
  generation


.. _Recipe_Puppet_Basic:

Basic httpd configuration with Puppet
--------------------------------------

.. index::
   single: Puppet; httpd configuration
   single: Puppet; puppetlabs/apache module
   single: Puppet Forge

Problem
~~~~~~~

You need to manage Apache httpd installation and configuration using Puppet,
leveraging the official ``puppetlabs/apache`` module from Puppet Forge.

Solution
~~~~~~~~

Install the module from Puppet Forge (currently at version 12.3.x):

.. code-block:: bash

   $ puppet module install puppetlabs/apache

Then declare the class in your manifest:

.. code-block:: ruby

   # site.pp or a profile class
   class { 'apache':
     default_vhost => false,
     mpm_module    => 'event',
     serveradmin   => 'admin@example.com',
     server_tokens => 'Prod',
     trace_enable  => 'Off',
   }

This single class declaration:

- Installs the httpd package
- Manages the main configuration file
- Ensures the service is running and enabled
- Disables the default virtual host (so you can define your own)
- Sets the MPM to event (the recommended MPM for 2.4.x)

Discussion
~~~~~~~~~~

The ``puppetlabs/apache`` module (version 12.3.x at the time of writing) is the
most comprehensive Puppet module for httpd management. It has over 1,000 forks
on GitHub and is actively maintained by Puppet, Inc. The module follows Puppet's
standard package/file/service pattern but abstracts it behind a rich parameter
interface.

The ``default_vhost => false`` parameter is critical. Without it, the module
creates a catch-all vhost on port 80 that will interfere with your own
definitions. Always disable it and define your vhosts explicitly.

The module supports both Red Hat and Debian family systems and handles the
significant differences between them (split configuration layout on
Debian/Ubuntu vs. monolithic on Red Hat, different module loading mechanisms,
different default paths).

If you're using Puppet with Hiera (and you should be), move the parameters to
your Hiera data:

.. code-block:: yaml

   ---
   # hieradata/common.yaml
   apache::default_vhost: false
   apache::mpm_module: event
   apache::serveradmin: admin@example.com
   apache::server_tokens: Prod
   apache::trace_enable: Off

This separates data from code, which is the entire point of Hiera.

See also
~~~~~~~~

- :ref:`Recipe_Puppet_Vhosts` for virtual host management
- :ref:`Recipe_Puppet_Modules` for controlling which httpd modules are loaded
- Puppet Forge module page:
  https://forge.puppet.com/modules/puppetlabs/apache


.. _Recipe_Puppet_Vhosts:

Managing virtual hosts with Puppet
-----------------------------------

.. index::
   single: Puppet; virtual hosts
   single: Puppet; apache::vhost

Problem
~~~~~~~

You need to define and manage multiple virtual hosts through Puppet, including
SSL-enabled vhosts.

Solution
~~~~~~~~

Use the ``apache::vhost`` defined type:

.. code-block:: ruby

   # Plain HTTP vhost
   apache::vhost { 'www.example.com':
     port          => 80,
     docroot       => '/var/www/example.com/html',
     serveraliases => ['example.com'],
     access_log_format => 'combined',
     directories   => [
       {
         path    => '/var/www/example.com/html',
         options => ['FollowSymLinks'],
         allow_override => ['None'],
         require => 'all granted',
       },
     ],
   }

   # HTTPS vhost
   apache::vhost { 'www.example.com-ssl':
     servername    => 'www.example.com',
     port          => 443,
     docroot       => '/var/www/example.com/html',
     ssl           => true,
     ssl_cert      => '/etc/pki/tls/certs/example.com.crt',
     ssl_key       => '/etc/pki/tls/private/example.com.key',
     ssl_chain     => '/etc/pki/tls/certs/example.com-chain.crt',
     ssl_protocol  => ['all', '-SSLv3', '-TLSv1', '-TLSv1.1'],
     ssl_cipher    => 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384',
     headers       => [
       'always set Strict-Transport-Security "max-age=63072000"',
     ],
   }

   # HTTP to HTTPS redirect
   apache::vhost { 'www.example.com-redirect':
     servername      => 'www.example.com',
     port            => 80,
     docroot         => '/var/www/example.com/html',
     redirect_status => 'permanent',
     redirect_dest   => 'https://www.example.com/',
   }

Discussion
~~~~~~~~~~

The ``apache::vhost`` defined type accepts an enormous number of parameters ---
over 100 at last count. This is both its strength and its weakness. You can
configure nearly anything without dropping to raw ERB templates, but the
parameter list can be overwhelming.

The resource title (``'www.example.com'`` in the first example) is used as the
filename for the vhost configuration file. This means resource titles must be
unique. For servers that serve both HTTP and HTTPS on the same name, the
convention is to append ``-ssl`` to the HTTPS resource title and set
``servername`` explicitly.

The ``directories`` parameter takes an array of hashes, where each hash
represents a ``<Directory>`` block. The hash keys map directly to httpd
directives. This works for common cases but becomes unwieldy for complex
access control or authentication configurations. For those, consider using the
``custom_fragment`` parameter to inject raw configuration.

**A word about the redirect pattern:** Defining a vhost that exists solely to
redirect HTTP to HTTPS is the standard approach. The ``redirect_status`` and
``redirect_dest`` parameters create a ``Redirect permanent / https://...``
directive in the vhost.

See also
~~~~~~~~

- :ref:`Recipe_Puppet_Basic` for the base Apache class
- :ref:`Recipe_Puppet_Modules` for ensuring :module:`mod_ssl` and
  :module:`mod_headers` are loaded
- Module reference:
  https://forge.puppet.com/modules/puppetlabs/apache/reference


.. _Recipe_Puppet_Modules:

Controlling the module list with Puppet
----------------------------------------

.. index::
   single: Puppet; httpd modules
   single: Puppet; apache::mod
   single: Puppet; purging modules

Problem
~~~~~~~

You want Puppet to control exactly which httpd modules are loaded, removing any
that aren't explicitly declared in your manifests.

Solution
~~~~~~~~

Enable module purging in the base class, then declare only the modules you need:

.. code-block:: ruby

   class { 'apache':
     default_vhost => false,
     mpm_module    => 'event',
     purge_configs => true,
   }

   # Explicitly load only the modules we need
   class { 'apache::mod::ssl': }
   class { 'apache::mod::rewrite': }
   class { 'apache::mod::headers': }
   class { 'apache::mod::proxy': }
   class { 'apache::mod::proxy_http': }
   class { 'apache::mod::deflate':
     types => [
       'text/html',
       'text/plain',
       'text/xml',
       'text/css',
       'application/javascript',
       'application/json',
     ],
   }

Discussion
~~~~~~~~~~

The ``purge_configs => true`` parameter tells the module to remove any
configuration files from the module configuration directory that aren't managed
by Puppet. This gives you a declarative, complete picture of your module list:
what's in Puppet is what's on disk, nothing more.

This is aggressive behavior. The first time you enable it on an existing server,
Puppet will remove every module configuration file that isn't explicitly declared.
This *will* break things if you haven't declared all the modules your vhosts
depend on. Test thoroughly in a non-production environment first.

Each ``apache::mod::*`` class may accept configuration parameters specific to
that module. For example, ``apache::mod::deflate`` accepts a ``types`` parameter
that controls which MIME types are compressed. Check the module reference for
available parameters.

Some modules have dependencies. If you declare ``apache::mod::proxy_http``, the
module automatically ensures ``apache::mod::proxy`` is also loaded. But don't
rely on this --- be explicit about your dependencies.

See also
~~~~~~~~

- :ref:`Recipe_Puppet_Basic` for the base class configuration
- :ref:`Recipe_Puppet_Vhosts` for vhosts that depend on these modules
- Module reference for available ``apache::mod::*`` classes:
  https://forge.puppet.com/modules/puppetlabs/apache/reference


.. _Recipe_Chef_Basic:

Managing httpd with Chef
-------------------------

.. index::
   single: Chef; httpd management
   single: Chef; apache2 cookbook
   single: Chef Supermarket

Problem
~~~~~~~

You need to install and configure Apache httpd using Chef, leveraging the
community ``apache2`` cookbook.

Solution
~~~~~~~~

Add the ``apache2`` cookbook (maintained by Sous Chefs, currently at version
9.3.x) to your :file:`Berksfile` or :file:`Policyfile.rb`:

.. code-block:: ruby

   # Policyfile.rb
   name 'webserver'
   default_source :supermarket

   cookbook 'apache2', '~> 9.3'

Then include the recipe and configure it through attributes:

.. code-block:: ruby

   # recipes/default.rb

   # Set attributes
   node.default['apache']['mpm'] = 'event'
   node.default['apache']['traceenable'] = 'Off'
   node.default['apache']['servertokens'] = 'Prod'

   # Include the default recipe (installs + configures + starts service)
   include_recipe 'apache2::default'

   # Enable specific modules
   apache2_module 'ssl'
   apache2_module 'rewrite'
   apache2_module 'headers'
   apache2_module 'deflate'

   # Disable modules we don't need
   apache2_module 'status' do
     action :disable
   end

Discussion
~~~~~~~~~~

The ``apache2`` cookbook has had a long and somewhat turbulent history. Originally
maintained by Opscode (now Progress Chef), it was adopted by the Sous Chefs
community organization. The current 9.x line (maintained at
``sous-chefs/apache2`` on GitHub) uses custom resources extensively and works
well with modern Chef Infra Client.

The ``apache2_module`` custom resource is the primary interface for module
management. It handles the platform-specific differences between ``a2enmod`` on
Debian and LoadModule directives on Red Hat.

Chef's attribute precedence system means you can set defaults in the cookbook's
attributes file, override them at the role or environment level, and further
override them per-node. This is powerful but can make it hard to understand
*why* a particular value ended up on a node. Use ``chef-shell`` or
``knife node show`` to inspect the final merged attributes.

**A note on Chef's current position:** Chef remains a capable tool, and the
Sous Chefs community keeps important cookbooks maintained. However, new
deployments choosing Chef in 2026 are rare outside organizations already
invested in the ecosystem. If you're starting fresh, Ansible's lower barrier
to entry makes it a more pragmatic choice for most teams.

See also
~~~~~~~~

- :ref:`Recipe_Chef_Templates` for virtual host management
- :ref:`Recipe_Chef_InSpec` for compliance testing
- Sous Chefs apache2 cookbook: https://supermarket.chef.io/cookbooks/apache2


.. _Recipe_Chef_Templates:

Template-driven virtual hosts with Chef
----------------------------------------

.. index::
   single: Chef; templates
   single: Chef; virtual hosts
   single: Chef; notifications

Problem
~~~~~~~

You need to deploy virtual host configuration files from Chef templates with
proper service notification on changes.

Solution
~~~~~~~~

.. code-block:: ruby

   # recipes/vhosts.rb

   # Data-driven vhost deployment
   vhosts = node['my_webapp']['vhosts'] || []

   vhosts.each do |vhost|
     template "/etc/httpd/conf.d/#{vhost['server_name']}.conf" do
       source 'vhost.conf.erb'
       owner 'root'
       group 'root'
       mode '0644'
       variables(
         server_name: vhost['server_name'],
         document_root: vhost['document_root'],
         server_aliases: vhost['server_aliases'] || [],
         extra_directives: vhost['extra_directives'] || ''
       )
       notifies :reload, 'service[httpd]', :delayed
     end

     directory vhost['document_root'] do
       owner 'apache'
       group 'apache'
       mode '0755'
       recursive true
     end
   end

The corresponding ERB template:

.. code-block:: erb

   # file: templates/vhost.conf.erb
   # Managed by Chef - DO NOT EDIT MANUALLY
   <VirtualHost *:80>
       ServerName <%= @server_name %>
   <% @server_aliases.each do |server_alias| %>
       ServerAlias <%= server_alias %>
   <% end %>
       DocumentRoot <%= @document_root %>

       <Directory <%= @document_root %>>
           AllowOverride None
           Require all granted
       </Directory>

   <%= @extra_directives %>
   </VirtualHost>

Discussion
~~~~~~~~~~

The ``notifies :reload, 'service[httpd]', :delayed`` line is Chef's equivalent
of Ansible's handler pattern. The ``:delayed`` timing means the reload happens
at the end of the Chef run, not immediately. This collapses multiple
notifications into a single reload, just like Ansible handlers.

If you need immediate notification (the service must reload before a subsequent
resource can work), use ``:immediately`` instead, but be aware this can cause
multiple reloads in a single run.

The pattern of iterating over a data structure to create multiple resources is
idiomatic Chef. The data (list of vhosts) comes from node attributes, which can
be set in roles, environments, data bags, or Policyfile attributes.

See also
~~~~~~~~

- :ref:`Recipe_Chef_Basic` for the base cookbook setup
- :ref:`Recipe_Chef_InSpec` for validating the deployed configuration


.. _Recipe_Chef_InSpec:

Chef InSpec for httpd compliance testing
-----------------------------------------

.. index::
   single: Chef; InSpec
   single: compliance testing
   single: InSpec; httpd

Problem
~~~~~~~

You want to verify that your httpd deployment meets security and configuration
requirements, using Chef InSpec as a compliance testing framework.

Solution
~~~~~~~~

Create an InSpec profile that tests your httpd configuration:

.. code-block:: ruby

   # controls/httpd.rb
   title 'Apache httpd Security Baseline'

   control 'httpd-01' do
     impact 1.0
     title 'Apache httpd should be installed'
     desc 'The httpd package must be installed and at the expected version.'

     describe package('httpd') do
       it { should be_installed }
       its('version') { should cmp >= '2.4.67' }
     end
   end

   control 'httpd-02' do
     impact 1.0
     title 'Apache httpd service should be running'

     describe service('httpd') do
       it { should be_running }
       it { should be_enabled }
     end
   end

   control 'httpd-03' do
     impact 0.7
     title 'ServerTokens should be restrictive'

     describe apache_conf('/etc/httpd/conf/httpd.conf') do
       its('ServerTokens') { should cmp 'Prod' }
     end
   end

   control 'httpd-04' do
     impact 1.0
     title 'TLS should be enforced'

     describe port(443) do
       it { should be_listening }
       its('protocols') { should include 'tcp' }
     end

     describe ssl(port: 443) do
       it { should_not be_enabled('TLSv1') }
       it { should_not be_enabled('TLSv1.1') }
       it { should be_enabled('TLSv1.2') }
       it { should be_enabled('TLSv1.3') }
     end
   end

   control 'httpd-05' do
     impact 0.5
     title 'Directory listing should be disabled'

     describe command('httpd -t -D DUMP_RUN_CFG') do
       its('exit_status') { should eq 0 }
     end

     describe apache_conf('/etc/httpd/conf/httpd.conf') do
       its('Options') { should_not include 'Indexes' }
     end
   end

Run it against a target:

.. code-block:: bash

   $ inspec exec httpd-baseline/ -t ssh://webserver1.example.com

Discussion
~~~~~~~~~~

InSpec is valuable regardless of which configuration management tool you use.
You can run the same InSpec profile against servers managed by Ansible, Puppet,
Chef, or even manually configured boxes. It answers the question "is the system
in the state I expect?" independently of how it got there.

The ``apache_conf`` resource parses httpd configuration files and exposes
directives as properties. It understands ``Include`` directives and will follow
them, giving you a complete view of the merged configuration.

InSpec profiles can be shared via Chef Supermarket or as Git repositories.
Organizations like the CIS (Center for Internet Security) publish InSpec
profiles for their benchmarks, including profiles that cover httpd hardening.

The ``impact`` value (0.0 to 1.0) communicates severity to compliance
dashboards. A failed control with impact 1.0 is critical; impact 0.3 is
informational.

See also
~~~~~~~~

- :ref:`Recipe_Chef_Basic` for the cookbook that configures httpd
- InSpec documentation: https://docs.chef.io/inspec/
- CIS Apache HTTP Server Benchmark:
  https://www.cisecurity.org/benchmark/apache_http_server


.. _Recipe_Docker_Basic:

Running httpd in Docker
------------------------

.. index::
   single: Docker; httpd
   single: containers; httpd
   single: Docker; official image

Problem
~~~~~~~

You want to run Apache httpd in a Docker container, using the official image
as a base, with your own configuration and content.

Solution
~~~~~~~~

The official ``httpd`` image on Docker Hub provides a ready-to-run Apache httpd.
The most basic usage mounts your content and optionally your configuration:

.. code-block:: bash

   # Run with default config, serving local content
   $ docker run -d --name my-httpd \
       -p 8080:80 \
       -v /path/to/your/content:/usr/local/apache2/htdocs/:ro \
       httpd:2.4

   # Run with custom configuration
   $ docker run -d --name my-httpd \
       -p 8080:80 \
       -v /path/to/httpd.conf:/usr/local/apache2/conf/httpd.conf:ro \
       -v /path/to/your/content:/usr/local/apache2/htdocs/:ro \
       httpd:2.4

For a custom image that bakes in your configuration:

.. code-block:: dockerfile

   # Dockerfile
   FROM httpd:2.4

   # Copy custom configuration
   COPY httpd.conf /usr/local/apache2/conf/httpd.conf
   COPY conf.d/ /usr/local/apache2/conf/extra/

   # Copy content
   COPY public-html/ /usr/local/apache2/htdocs/

   # Expose port 80
   EXPOSE 80

   # Health check
   HEALTHCHECK --interval=30s --timeout=3s \
     CMD curl -f http://localhost/ || exit 1

Build and run:

.. code-block:: bash

   $ docker build -t my-httpd:latest .
   $ docker run -d --name my-httpd -p 80:80 my-httpd:latest

Discussion
~~~~~~~~~~

The official ``httpd`` Docker image is based on Debian and includes a standard
Apache httpd compiled from source into :file:`/usr/local/apache2/`. This is
different from a distribution package install --- the paths are not
:file:`/etc/httpd/` or :file:`/etc/apache2/`. The key paths inside the
container are:

- :file:`/usr/local/apache2/conf/httpd.conf` --- main configuration
- :file:`/usr/local/apache2/conf/extra/` --- additional configuration files
- :file:`/usr/local/apache2/htdocs/` --- default document root
- :file:`/usr/local/apache2/logs/` --- log directory
- :file:`/usr/local/apache2/modules/` --- compiled modules

**Image tags:** Use ``httpd:2.4`` for the latest 2.4.x release. The image is
available in both Debian (default) and Alpine (``httpd:2.4-alpine``) variants.
The Alpine variant is significantly smaller (~60MB vs ~170MB) but uses musl
libc, which can cause compatibility issues with some third-party modules.

**Logging in containers:** By default, httpd logs to files inside the container.
For Docker, you should redirect logs to stdout/stderr so they appear in
``docker logs``:

.. code-block:: apache

   ErrorLog /proc/self/fd/2
   CustomLog /proc/self/fd/1 combined

This is already the default in the official image.

**The ``:ro`` mount flag** makes the volume read-only inside the container, which
is a defense-in-depth measure for content and configuration.

See also
~~~~~~~~

- :ref:`Recipe_Docker_Compose` for multi-container setups
- :ref:`Recipe_Docker_Minimal` for building minimal images
- Docker Hub official image: https://hub.docker.com/_/httpd


.. _Recipe_Docker_Compose:

Docker Compose for httpd with TLS
----------------------------------

.. index::
   single: Docker Compose; httpd
   single: Docker; TLS
   single: certbot; Docker
   single: containers; TLS

Problem
~~~~~~~

You need to run httpd with TLS termination in Docker, including automated
certificate management with Let's Encrypt, using Docker Compose to orchestrate
the services.

Solution
~~~~~~~~

.. code-block:: yaml

   # docker-compose.yml
   services:
     httpd:
       image: httpd:2.4
       container_name: httpd
       ports:
         - "80:80"
         - "443:443"
       volumes:
         - ./httpd.conf:/usr/local/apache2/conf/httpd.conf:ro
         - ./conf.d:/usr/local/apache2/conf/extra:ro
         - ./content:/usr/local/apache2/htdocs:ro
         - certs:/etc/letsencrypt:ro
         - acme-challenge:/var/www/certbot:ro
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost/server-status?auto"]
         interval: 30s
         timeout: 5s
         retries: 3
         start_period: 10s
       restart: unless-stopped
       depends_on:
         certbot:
           condition: service_completed_successfully

     certbot:
       image: certbot/certbot:latest
       container_name: certbot
       volumes:
         - certs:/etc/letsencrypt
         - acme-challenge:/var/www/certbot
       command: >
         certonly --webroot -w /var/www/certbot
         -d www.example.com -d example.com
         --non-interactive --agree-tos
         --email admin@example.com
       # For renewal, run:
       # docker compose run --rm certbot renew

   volumes:
     certs:
     acme-challenge:

The httpd configuration needs to serve the ACME challenge directory and
reference the Let's Encrypt certificates:

.. code-block:: apache

   # In your vhost configuration
   <VirtualHost *:80>
       ServerName www.example.com

       # Serve ACME challenges
       Alias /.well-known/acme-challenge/ /var/www/certbot/.well-known/acme-challenge/
       <Directory /var/www/certbot>
           Require all granted
       </Directory>

       # Redirect everything else to HTTPS
       RewriteEngine On
       RewriteCond %{REQUEST_URI} !^/\.well-known/acme-challenge/
       RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]
   </VirtualHost>

   <VirtualHost *:443>
       ServerName www.example.com
       DocumentRoot /usr/local/apache2/htdocs

       SSLEngine On
       SSLCertificateFile /etc/letsencrypt/live/www.example.com/fullchain.pem
       SSLCertificateKeyFile /etc/letsencrypt/live/www.example.com/privkey.pem
   </VirtualHost>

Discussion
~~~~~~~~~~

This pattern uses named volumes to share state between the httpd and certbot
containers. The ``certs`` volume holds the Let's Encrypt certificates and
account data. The ``acme-challenge`` volume holds the challenge files that
certbot places and httpd serves.

**Certificate renewal** is not automatic in this setup. You need to run the
renewal command periodically (via cron or a systemd timer on the host):

.. code-block:: bash

   $ docker compose run --rm certbot renew && docker compose exec httpd httpd -k graceful

The ``depends_on`` with ``condition: service_completed_successfully`` ensures
that httpd doesn't start until certbot has obtained the initial certificate.
On subsequent starts (when the certificate already exists), certbot exits
immediately with success.

**Health checks** are important in container orchestration. The health check
shown uses :module:`mod_status` (which you'll need to enable) to verify that
httpd is actually serving requests, not just that the process is running.

See also
~~~~~~~~

- :ref:`Recipe_Docker_Basic` for single-container basics
- :ref:`Recipe_Docker_Minimal` for production-hardened images
- Docker Compose documentation: https://docs.docker.com/compose/


.. _Recipe_Docker_Minimal:

Building a minimal httpd container image
-----------------------------------------

.. index::
   single: Docker; minimal image
   single: Docker; multi-stage build
   single: containers; security hardening
   single: Docker; attack surface

Problem
~~~~~~~

You want to build a minimal httpd container image with only the modules you
actually need, reducing the attack surface and image size.

Solution
~~~~~~~~

Use a multi-stage build to compile httpd from source with only your required
modules, then copy the binaries into a minimal runtime image:

.. code-block:: dockerfile

   # Stage 1: Build httpd from source with only needed modules
   FROM debian:bookworm-slim AS builder

   RUN apt-get update && apt-get install -y \
       build-essential \
       libssl-dev \
       libpcre3-dev \
       libapr1-dev \
       libaprutil1-dev \
       curl \
       && rm -rf /var/lib/apt/lists/*

   ENV HTTPD_VERSION=2.4.67

   RUN curl -fSL https://dlcdn.apache.org/httpd/httpd-${HTTPD_VERSION}.tar.gz \
       -o httpd.tar.gz \
       && tar xzf httpd.tar.gz \
       && cd httpd-${HTTPD_VERSION} \
       && ./configure \
           --prefix=/usr/local/apache2 \
           --enable-mods-static="authz_core authz_host dir mime log_config \
                                 unixd headers rewrite ssl socache_shmcb" \
           --enable-ssl \
           --with-ssl=/usr \
           --disable-autoindex \
           --disable-cgid \
           --disable-userdir \
           --disable-include \
           --disable-env \
       && make -j$(nproc) \
       && make install

   # Stage 2: Minimal runtime
   FROM debian:bookworm-slim

   RUN apt-get update && apt-get install -y \
       libssl3 libpcre3 libapr1 libaprutil1 curl \
       && rm -rf /var/lib/apt/lists/* \
       && adduser --system --no-create-home --group httpd

   COPY --from=builder /usr/local/apache2 /usr/local/apache2

   # Remove unnecessary files from the install
   RUN rm -rf /usr/local/apache2/manual \
       /usr/local/apache2/man \
       /usr/local/apache2/include \
       /usr/local/apache2/build

   COPY httpd.conf /usr/local/apache2/conf/httpd.conf
   COPY content/ /usr/local/apache2/htdocs/

   # Run as non-root (bind to high port, or use capabilities)
   USER httpd
   EXPOSE 8080

   CMD ["/usr/local/apache2/bin/httpd", "-D", "FOREGROUND"]

Discussion
~~~~~~~~~~

This approach produces an image significantly smaller than the official httpd
image, because you only include the modules you actually use. For a typical
static content server with TLS, the resulting image can be under 40MB.

The ``--enable-mods-static`` flag compiles modules directly into the httpd
binary rather than as loadable ``.so`` files. This means you don't need a
``modules/`` directory full of files you never load, and there's no possibility
of loading unexpected modules at runtime.

**Modules to always include:**

- ``authz_core`` --- required for ``Require`` directives
- ``authz_host`` --- required for IP-based access control
- ``dir`` --- required for ``DirectoryIndex``
- ``mime`` --- required for content-type detection
- ``log_config`` --- required for access logging
- ``unixd`` --- required for user/group switching

**Running as non-root:** The ``USER httpd`` directive means the container
process runs as an unprivileged user. This requires either binding to a port
above 1024 (like 8080) or using Linux capabilities (``CAP_NET_BIND_SERVICE``).
In Kubernetes or behind a reverse proxy, binding to a high port is preferred.

**Trade-offs:** This approach requires rebuilding the image to change the module
set. If your module requirements change frequently, the official image with
dynamic modules may be more practical.

See also
~~~~~~~~

- :ref:`Recipe_Docker_Basic` for the standard official image approach
- :ref:`Recipe_Podman` for running in Podman with rootless containers
- Docker multi-stage builds documentation:
  https://docs.docker.com/build/building/multi-stage/


.. _Recipe_Podman:

Running httpd in Podman (rootless)
-----------------------------------

.. index::
   single: Podman; httpd
   single: Podman; rootless
   single: Podman; Quadlet
   single: systemd; containers
   single: containers; rootless

Problem
~~~~~~~

You want to run httpd as a rootless container using Podman, integrated with
systemd so it starts at boot and is managed like any other system service.

Solution
~~~~~~~~

The modern way to run Podman containers as systemd services is **Quadlet** ---
declarative unit files that systemd's generator converts into full service
definitions. Create a ``.container`` file:

.. code-block:: text

   # ~/.config/containers/systemd/httpd.container
   [Unit]
   Description=Apache httpd web server
   After=network-online.target

   [Container]
   Image=docker.io/library/httpd:2.4
   PublishPort=8080:80
   Volume=/home/webuser/content:/usr/local/apache2/htdocs:ro,Z
   Volume=/home/webuser/httpd.conf:/usr/local/apache2/conf/httpd.conf:ro,Z
   HealthCmd=curl -f http://localhost/ || exit 1
   HealthInterval=30s
   AutoUpdate=registry

   [Service]
   Restart=on-failure
   TimeoutStartSec=60

   [Install]
   WantedBy=default.target

Reload and start:

.. code-block:: bash

   $ systemctl --user daemon-reload
   $ systemctl --user start httpd.service
   $ systemctl --user enable httpd.service

   # Enable lingering so the user service starts at boot (not just at login)
   $ loginctl enable-linger $(whoami)

For a system-wide (root) deployment, place the file at
:file:`/etc/containers/systemd/httpd.container` and drop the ``--user`` flag.

Discussion
~~~~~~~~~~

**Podman vs. Docker:** Podman is a daemonless container engine that's wire-
compatible with Docker. The primary advantages for httpd deployments are:

1. **Rootless by default** --- containers run as your user, not as root. No
daemon running as root means a smaller attack surface.
2. **Systemd integration** --- Quadlet files are native systemd units. You
manage containers with ``systemctl``, view logs with ``journalctl``, and
define dependencies with standard systemd syntax.
3. **No daemon** --- Podman doesn't require a background service. If the
``podman`` process isn't running, your containers still are (they're just
regular processes).

**Quadlet replaced ``podman generate systemd``:** The older approach of
generating unit files with ``podman generate systemd`` is deprecated. Quadlet
(introduced in Podman 4.4, stable since Podman 5.x) is the declarative
replacement. A ``.container`` file uses INI syntax similar to standard systemd
units, with a ``[Container]`` section for Podman-specific options.

**The ``:Z`` volume flag** applies the correct SELinux label to the mounted
files so that the container process can read them. Without it on SELinux-enabled
systems (RHEL, Fedora), you'll get permission denied errors. On systems without
SELinux, the flag is harmlessly ignored.

``AutoUpdate=registry`` enables automatic image updates via
``podman auto-update``. When run (typically via a systemd timer), it checks
if a newer version of the image exists, pulls it, and restarts the container.
This is useful for keeping httpd patched but should be used cautiously in
production --- test updates in staging first.

**Port binding:** In rootless mode, you cannot bind to ports below 1024 without
adjusting ``net.ipv4.ip_unprivileged_port_start``. The common approach is to
bind to a high port (8080) and use a host-level reverse proxy or firewall rule
to redirect port 80 to 8080.

See also
~~~~~~~~

- :ref:`Recipe_Docker_Basic` for Docker-specific instructions
- :ref:`Recipe_Docker_Minimal` for building minimal images (works with Podman too)
- Podman Quadlet documentation:
  https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html



.. _Recipe_K8s_Deployment:

Deploying httpd on Kubernetes
------------------------------

.. index::
   single: Kubernetes; httpd
   single: Kubernetes; Deployment
   single: Kubernetes; Service
   single: Kubernetes; Ingress
   single: Kubernetes; ConfigMap
   single: Kubernetes; health checks
   single: Kubernetes; rolling updates
   single: kubectl
   single: containers; Kubernetes

Problem
~~~~~~~

You want to run httpd in a Kubernetes cluster with proper configuration
management, health checks, and zero-downtime rolling updates.

Solution
~~~~~~~~

Start with a ConfigMap that holds your httpd configuration:

.. code-block:: yaml

   # httpd-configmap.yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: httpd-config
   data:
     httpd.conf: |
       ServerRoot "/usr/local/apache2"
       Listen 80
       LoadModule mpm_event_module modules/mod_mpm_event.so
       LoadModule authz_core_module modules/mod_authz_core.so
       LoadModule dir_module modules/mod_dir.so
       LoadModule mime_module modules/mod_mime.so
       LoadModule log_config_module modules/mod_log_config.so
       LoadModule unixd_module modules/mod_unixd.so
       LoadModule status_module modules/mod_status.so

       ServerName localhost
       DocumentRoot "/usr/local/apache2/htdocs"

       <Directory "/usr/local/apache2/htdocs">
           Require all granted
       </Directory>

       # Health check endpoint for Kubernetes probes
       <Location "/healthz">
           SetHandler server-status
           Require all granted
       </Location>

       ErrorLog /proc/self/fd/2
       CustomLog /proc/self/fd/1 combined

Now the Deployment itself:

.. code-block:: yaml

   # httpd-deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: httpd
     labels:
       app: httpd
   spec:
     replicas: 3
     strategy:
       type: RollingUpdate
       rollingUpdate:
         maxSurge: 1
         maxUnavailable: 0
     selector:
       matchLabels:
         app: httpd
     template:
       metadata:
         labels:
           app: httpd
         annotations:
           # Forces a rolling update when the ConfigMap changes
           checksum/config: "PLACEHOLDER"
       spec:
         containers:
           - name: httpd
             image: httpd:2.4-alpine
             ports:
               - containerPort: 80
                 protocol: TCP
             resources:
               requests:
                 cpu: 100m
                 memory: 128Mi
               limits:
                 cpu: 500m
                 memory: 256Mi
             readinessProbe:
               httpGet:
                 path: /healthz
                 port: 80
               initialDelaySeconds: 5
               periodSeconds: 10
               failureThreshold: 3
             livenessProbe:
               httpGet:
                 path: /healthz
                 port: 80
               initialDelaySeconds: 15
               periodSeconds: 20
               failureThreshold: 3
             volumeMounts:
               - name: httpd-config-volume
                 mountPath: /usr/local/apache2/conf/httpd.conf
                 subPath: httpd.conf
         volumes:
           - name: httpd-config-volume
             configMap:
               name: httpd-config

Expose the Deployment with a Service and Ingress:

.. code-block:: yaml

   # httpd-service.yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: httpd
   spec:
     selector:
       app: httpd
     ports:
       - port: 80
         targetPort: 80
         protocol: TCP
     type: ClusterIP

.. code-block:: yaml

   # httpd-ingress.yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: httpd
     annotations:
       nginx.ingress.kubernetes.io/rewrite-target: /
   spec:
     ingressClassName: nginx
     rules:
       - host: www.example.com
         http:
           paths:
             - path: /
               pathType: Prefix
               backend:
                 service:
                   name: httpd
                   port:
                     number: 80

Apply everything:

.. code-block:: bash

   $ kubectl apply -f httpd-configmap.yaml
   $ kubectl apply -f httpd-deployment.yaml
   $ kubectl apply -f httpd-service.yaml
   $ kubectl apply -f httpd-ingress.yaml

To trigger a rolling update after changing the ConfigMap, compute a new
checksum and patch the annotation:

.. code-block:: bash

   $ kubectl create configmap httpd-config \
       --from-file=httpd.conf=./httpd.conf \
       --dry-run=client -o yaml | kubectl apply -f -
   $ kubectl patch deployment httpd -p \
       "{\"spec\":{\"template\":{\"metadata\":{\"annotations\":{\"checksum/config\":\"$(sha256sum httpd.conf | cut -d' ' -f1)\"}}}}}"

Discussion
~~~~~~~~~~

**The ConfigMap hash annotation trick.** Kubernetes does *not* automatically
restart pods when a mounted ConfigMap changes. The contents eventually propagate
(within the kubelet sync period, typically 60--120 seconds), but httpd won't
re-read :file:`httpd.conf` without a restart. The annotation trick works because
any change to the pod template --- even a meaningless annotation --- triggers a
new rollout. When you update the ``checksum/config`` annotation with the SHA-256
of your configuration file, Kubernetes sees a spec change and performs a rolling
update according to your ``strategy`` settings.

If you use Helm or Kustomize (see the next recipe), this annotation can be
computed automatically during rendering.

**Health probes.** I'm using :module:`mod_status` at :file:`/healthz` as both
the readiness and liveness endpoint. The readiness probe determines whether a
pod receives traffic --- if it fails, the pod is removed from the Service's
endpoint list. The liveness probe determines whether Kubernetes restarts the
container. I've set the liveness ``initialDelaySeconds`` higher than readiness
because you want to detect startup problems (readiness) before you start killing
pods (liveness).

For production, you might separate these: use a lightweight ``/healthz`` that
simply returns 200 for liveness, and a ``/readyz`` endpoint that verifies your
content directory is mounted and any backend proxy targets are reachable.

**Rolling update strategy.** Setting ``maxUnavailable: 0`` means Kubernetes will
never kill an existing pod until a new one passes its readiness probe. Combined
with ``maxSurge: 1``, you get true zero-downtime deployments at the cost of
briefly running one extra pod during updates. If you're resource-constrained,
you can set ``maxSurge: 0, maxUnavailable: 1`` --- you'll save resources but
accept one pod being down during the rollout.

**Resource sizing.** The values above (100m CPU request, 256Mi memory limit)
are conservative starting points for a static content server. If httpd is doing
reverse proxying or handling TLS termination, bump memory to 512Mi. Use
``kubectl top pods`` after your deployment is running to see actual consumption
and adjust.

**Ingress controllers.** The Ingress resource is just an API object --- it does
nothing without an Ingress controller running in the cluster. Common choices:

- **ingress-nginx** (community NGINX controller): the most widely deployed.
  Good for general-purpose HTTP routing.
- **AWS ALB Ingress Controller** (now AWS Load Balancer Controller): creates an
  actual ALB per Ingress. Best for EKS deployments where you want AWS-native
  load balancing.
- **Traefik**: auto-discovers services and supports both Ingress and its own
  IngressRoute CRD.

**When to skip Ingress and use a LoadBalancer Service directly:** If you have
a single service with no host-based or path-based routing, a ``type:
LoadBalancer`` Service is simpler. Ingress earns its keep when you have multiple
services behind one external IP, need TLS termination at the edge, or want
host-based virtual hosting (which, as an httpd user, you certainly appreciate).

See also
~~~~~~~~

- :ref:`Recipe_Helm_httpd` for managing this deployment with Helm
- :ref:`Recipe_Docker_Basic` for the container image fundamentals
- Kubernetes Deployment documentation:
  https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Ingress documentation:
  https://kubernetes.io/docs/concepts/services-networking/ingress/


.. _Recipe_Helm_httpd:

Managing httpd configuration with Helm
---------------------------------------

.. index::
   single: Helm; httpd
   single: Helm; Bitnami chart
   single: Helm; values.yaml
   single: Kubernetes; Helm
   single: Kustomize

Problem
~~~~~~~

You want a repeatable, version-controlled way to deploy httpd across multiple
environments (dev, staging, prod) without maintaining raw YAML manifests for
each one.

Solution
~~~~~~~~

The Bitnami Apache chart on ArtifactHub provides a production-ready Helm chart
for httpd. Add the repository and install:

.. code-block:: bash

   $ helm repo add bitnami https://charts.bitnami.com/bitnami
   $ helm repo update
   $ helm install my-httpd bitnami/apache

To customize the deployment, create a :file:`values.yaml` override file:

.. code-block:: yaml

   # values.yaml
   replicaCount: 3

   image:
     registry: docker.io
     repository: bitnami/apache
     tag: 2.4.65-debian-12-r2

   resources:
     requests:
       cpu: 100m
       memory: 128Mi
     limits:
       cpu: 500m
       memory: 256Mi

   # Supply a custom httpd.conf via ConfigMap name
   httpdConfConfigMap: my-httpd-conf

   service:
     type: ClusterIP
     ports:
       http: 80

   ingress:
     enabled: true
     ingressClassName: nginx
     hostname: www.example.com
     path: /
     pathType: Prefix
     annotations:
       nginx.ingress.kubernetes.io/rewrite-target: /

Install (or upgrade) with your values:

.. code-block:: bash

   $ kubectl create configmap my-httpd-conf \
       --from-file=httpd.conf=./httpd.conf
   $ helm install my-httpd bitnami/apache -f values.yaml

When your configuration changes, upgrade the release:

.. code-block:: bash

   $ kubectl create configmap my-httpd-conf \
       --from-file=httpd.conf=./httpd.conf \
       --dry-run=client -o yaml | kubectl apply -f -
   $ helm upgrade my-httpd bitnami/apache -f values.yaml

For multiple environments, create per-environment files:

.. code-block:: bash

   $ helm upgrade my-httpd bitnami/apache \
       -f values.yaml \
       -f values-prod.yaml

Where :file:`values-prod.yaml` overrides just what differs:

.. code-block:: yaml

   # values-prod.yaml
   replicaCount: 5

   resources:
     requests:
       cpu: 250m
       memory: 256Mi
     limits:
       cpu: "1"
       memory: 512Mi

   ingress:
     hostname: www.example.com
     tls: true

Discussion
~~~~~~~~~~

**When Helm makes sense.** Helm shines when you deploy the same application
across multiple environments or clusters with minor variations. Instead of
maintaining three nearly-identical sets of YAML manifests (dev, staging, prod),
you maintain one chart and three small values files. Helm also gives you
rollback (``helm rollback my-httpd 1``), release history, and atomic upgrades.

**When Helm is overkill.** If you have a single cluster and a single
environment, the raw manifests from the previous recipe are simpler to
understand and debug. Helm adds a layer of indirection --- when something goes
wrong, you're debugging the rendered templates, not the manifests you wrote.

**Chart pinning.** Always pin your chart version in CI/CD:

.. code-block:: bash

   $ helm install my-httpd bitnami/apache --version 11.2.0 -f values.yaml

Without ``--version``, ``helm install`` pulls the latest chart, which might
introduce breaking changes on a Tuesday afternoon when you least expect it.
Record pinned versions in a :file:`Chart.lock` or your deployment documentation.

**Creating your own chart.** If you find yourself overriding more than a dozen
values, or if you need resources the Bitnami chart doesn't support (custom
sidecars, init containers for content sync, non-standard health endpoints),
create your own chart:

.. code-block:: bash

   $ helm create my-httpd-chart

This scaffolds a chart with templates for Deployment, Service, Ingress,
ServiceAccount, and HPA. Replace the generated templates with your customized
manifests and parameterize only what varies between environments.

**Kustomize as an alternative.** If you dislike Helm's templating approach
(Go templates can be painful to debug), Kustomize takes a different philosophy:
you write plain YAML manifests as a "base," then apply patches and overlays per
environment. Kustomize is built into ``kubectl``:

.. code-block:: bash

   $ kubectl apply -k overlays/production/

Kustomize also solves the ConfigMap rollout problem natively --- its
``configMapGenerator`` appends a content hash to the ConfigMap name, so any
change automatically triggers a new rollout without annotation tricks.

The choice between Helm and Kustomize often comes down to team preference. Helm
is better for distributing reusable charts (like Bitnami's). Kustomize is
better when you own the manifests and just need environment-specific overrides.

See also
~~~~~~~~

- :ref:`Recipe_K8s_Deployment` for the raw manifest approach
- Bitnami Apache chart on ArtifactHub:
  https://artifacthub.io/packages/helm/bitnami/apache
- Helm documentation: https://helm.sh/docs/
- Kustomize documentation: https://kustomize.io/


.. _Recipe_Terraform_Basic:

Provisioning an httpd server with Terraform
---------------------------------------------

.. index::
   single: Terraform; httpd
   single: Terraform; AWS EC2
   single: Terraform; user_data
   single: infrastructure as code

Problem
~~~~~~~

You need to provision a cloud server (AWS EC2) that will run httpd, including
the networking (security groups for ports 80 and 443) and initial bootstrap.

Solution
~~~~~~~~

.. code-block:: hcl

   # main.tf
   terraform {
     required_version = ">= 1.5"
     required_providers {
       aws = {
         source  = "hashicorp/aws"
         version = "~> 5.0"
       }
     }
   }

   provider "aws" {
     region = var.aws_region
   }

   variable "aws_region" {
     default = "us-east-1"
   }

   variable "instance_type" {
     default = "t3.small"
   }

   # Find the latest Amazon Linux 2023 AMI
   data "aws_ami" "al2023" {
     most_recent = true
     owners      = ["amazon"]

     filter {
       name   = "name"
       values = ["al2023-ami-*-x86_64"]
     }
   }

   # Security group allowing HTTP, HTTPS, and SSH
   resource "aws_security_group" "httpd" {
     name        = "httpd-server"
     description = "Allow HTTP, HTTPS, and SSH inbound"

     ingress {
       from_port   = 80
       to_port     = 80
       protocol    = "tcp"
       cidr_blocks = ["0.0.0.0/0"]
       description = "HTTP"
     }

     ingress {
       from_port   = 443
       to_port     = 443
       protocol    = "tcp"
       cidr_blocks = ["0.0.0.0/0"]
       description = "HTTPS"
     }

     ingress {
       from_port   = 22
       to_port     = 22
       protocol    = "tcp"
       cidr_blocks = [var.admin_cidr]
       description = "SSH from admin"
     }

     egress {
       from_port   = 0
       to_port     = 0
       protocol    = "-1"
       cidr_blocks = ["0.0.0.0/0"]
     }

     tags = {
       Name = "httpd-server"
     }
   }

   variable "admin_cidr" {
     description = "CIDR block for SSH access"
     type        = string
   }

   # EC2 instance with user_data bootstrap
   resource "aws_instance" "httpd" {
     ami                    = data.aws_ami.al2023.id
     instance_type          = var.instance_type
     vpc_security_group_ids = [aws_security_group.httpd.id]
     key_name               = var.key_pair_name

     user_data = <<-EOF
       #!/bin/bash
       dnf install -y httpd mod_ssl
       systemctl enable --now httpd
       echo "<h1>Hello from $(hostname)</h1>" > /var/www/html/index.html
     EOF

     tags = {
       Name = "httpd-server"
     }
   }

   variable "key_pair_name" {
     description = "Name of the EC2 key pair for SSH access"
     type        = string
   }

   output "public_ip" {
     value = aws_instance.httpd.public_ip
   }

   output "public_dns" {
     value = aws_instance.httpd.public_dns
   }

Deploy it:

.. code-block:: bash

   $ terraform init
   $ terraform plan -var="admin_cidr=203.0.113.0/32" -var="key_pair_name=my-key"
   $ terraform apply -var="admin_cidr=203.0.113.0/32" -var="key_pair_name=my-key"

Discussion
~~~~~~~~~~

This example deliberately keeps the httpd configuration minimal --- just
``dnf install`` and ``systemctl enable``. That's intentional. **Terraform's job
is to provision infrastructure, not to configure applications.** The ``user_data``
script is a bootstrap, not a configuration management tool.

In production, the ``user_data`` script would typically do one of two things:

1. **Install and configure an Ansible pull** to fetch configuration from a Git
repository
2. **Signal a configuration management tool** (Ansible, Puppet) that the
instance is ready to be configured

The ``user_data`` approach has limitations:

- It runs only once, at instance creation. Subsequent changes require
  destroying and recreating the instance (or using a separate mechanism).
- Debugging is painful. If the script fails, you need to SSH in and check
  :file:`/var/log/cloud-init-output.log`.
- It's not idempotent by default. You have to write it carefully.

**Security group considerations:** Note that the SSH ingress rule uses a
variable (``var.admin_cidr``) rather than ``0.0.0.0/0``. Never open SSH to the
world in production. Better yet, use AWS Systems Manager Session Manager and
remove SSH access entirely.

**State management:** Terraform tracks the state of your infrastructure in a
state file. For team usage, store this in a remote backend (S3 + DynamoDB for
locking). Never commit :file:`terraform.tfstate` to version control --- it
contains sensitive values.

See also
~~~~~~~~

- :ref:`Recipe_Terraform_Ansible` for the common Terraform + Ansible pattern
- :ref:`Recipe_OpenTofu` for the open-source Terraform alternative
- AWS EC2 user_data documentation:
  https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html


.. _Recipe_Terraform_Ansible:

Terraform + Ansible integration
--------------------------------

.. index::
   single: Terraform; Ansible integration
   single: Ansible; Terraform integration
   single: infrastructure as code; layered approach

Problem
~~~~~~~

You want to use Terraform to provision infrastructure and Ansible to configure
httpd on that infrastructure --- the "provision then configure" pattern that's
become the standard approach for cloud deployments.

Solution
~~~~~~~~

Use Terraform's ``local-exec`` provisioner to trigger an Ansible playbook after
the instance is created, or (better) generate a dynamic inventory from Terraform
outputs:

**Approach 1: Terraform output → Ansible dynamic inventory**

.. code-block:: hcl

   # outputs.tf
   output "webserver_ips" {
     value = aws_instance.httpd[*].public_ip
   }

Generate an inventory file from Terraform output:

.. code-block:: bash

   #!/bin/bash
   # generate_inventory.sh
   echo "[webservers]" > inventory.ini
   terraform output -json webserver_ips | \
     jq -r '.[]' >> inventory.ini
   echo "" >> inventory.ini
   echo "[webservers:vars]" >> inventory.ini
   echo "ansible_user=ec2-user" >> inventory.ini
   echo "ansible_ssh_private_key_file=~/.ssh/my-key.pem" >> inventory.ini

Then run your Ansible playbook:

.. code-block:: bash

   $ terraform apply
   $ ./generate_inventory.sh
   $ ansible-playbook -i inventory.ini site.yml

**Approach 2: local-exec provisioner (less recommended)**

.. code-block:: hcl

   resource "aws_instance" "httpd" {
     # ... instance config ...

     provisioner "local-exec" {
       command = <<-EOT
         sleep 30  # Wait for SSH to become available
         ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook \
           -i '${self.public_ip},' \
           -u ec2-user \
           --private-key ~/.ssh/my-key.pem \
           site.yml
       EOT
     }
   }

Discussion
~~~~~~~~~~

The dynamic inventory approach (Approach 1) is strongly preferred over
``local-exec`` for several reasons:

1. **Separation of concerns:** Terraform creates infrastructure. Ansible
configures it. They run independently and can be triggered separately.
2. **Idempotency:** You can re-run Ansible without re-running Terraform. With
``local-exec``, the provisioner only runs when the resource is created.
3. **Debugging:** When Ansible fails, you can fix and re-run it without
touching infrastructure.
4. **Scaling:** Adding more servers means running ``terraform apply`` then
regenerating the inventory and running Ansible again.

The ``local-exec`` approach (Approach 2) has the appeal of being "all in one
command," but it creates tight coupling and is fragile (the ``sleep 30`` is a
hack --- the instance might not have SSH ready in 30 seconds, or it might be
ready in 5).

**A more sophisticated approach** uses Terraform's ``terraform-inventory`` plugin
or the ``ansible.builtin.aws_ec2`` dynamic inventory plugin in Ansible, which
queries AWS directly for instances matching certain tags. This eliminates the
need for a generated inventory file entirely:

.. code-block:: yaml

   # aws_ec2.yml (Ansible dynamic inventory)
   plugin: amazon.aws.aws_ec2
   regions:
     - us-east-1
   filters:
     tag:Role: webserver
     instance-state-name: running
   keyed_groups:
     - key: tags.Environment
       prefix: env

This inventory plugin queries AWS in real-time, so your inventory is always
accurate regardless of when you last ran Terraform.

See also
~~~~~~~~

- :ref:`Recipe_Terraform_Basic` for the Terraform configuration
- :ref:`Recipe_Ansible_Install` for the Ansible playbook
- :ref:`Recipe_OpenTofu` for using OpenTofu instead of Terraform
- Ansible AWS EC2 dynamic inventory plugin:
  https://docs.ansible.com/ansible/latest/collections/amazon/aws/aws_ec2_inventory.html


.. _Recipe_OpenTofu:

OpenTofu as a Terraform alternative
-------------------------------------

.. index::
   single: OpenTofu
   single: Terraform; alternatives
   single: infrastructure as code; open source
   single: OpenTofu; migration

Problem
~~~~~~~

You want to use an open-source, community-driven infrastructure-as-code tool
that's compatible with your existing Terraform configurations, without vendor
lock-in concerns.

Solution
~~~~~~~~

OpenTofu is a fork of Terraform created in 2023 after HashiCorp changed
Terraform's license from MPL 2.0 to BSL 1.1. It's maintained by the Linux
Foundation and is a drop-in replacement for Terraform. As of 2026, OpenTofu
is at version 1.10.x (with 1.11 in development).

Install OpenTofu:

.. code-block:: bash

   # macOS
   $ brew install opentofu

   # Linux (official installer)
   $ curl -fsSL https://get.opentofu.org/install-opentofu.sh | sh

   # Verify
   $ tofu --version

Migrate an existing Terraform project:

.. code-block:: bash

   # In your existing Terraform project directory:
   $ tofu init    # Initializes using existing .tf files
   $ tofu plan    # Should produce the same plan as 'terraform plan'
   $ tofu apply   # Identical behavior

The ``.tf`` files from :ref:`Recipe_Terraform_Basic` work unchanged:

.. code-block:: hcl

   # main.tf --- works with both 'terraform' and 'tofu' commands
   terraform {
     required_version = ">= 1.5"
     required_providers {
       aws = {
         source  = "hashicorp/aws"
         version = "~> 5.0"
       }
     }
   }

   # ... rest of configuration unchanged ...

Discussion
~~~~~~~~~~

The migration from Terraform to OpenTofu is genuinely straightforward for most
projects:

1. The HCL configuration language is identical.
2. The state file format is compatible (OpenTofu reads Terraform state files
and vice versa).
3. Most providers (including the AWS provider) work with both tools.
4. The CLI commands are the same, just ``tofu`` instead of ``terraform``.

**When to choose OpenTofu over Terraform:**

- **License concerns:** If your organization's legal team has concerns about the
  BSL 1.1 license (which restricts competitive use), OpenTofu's MPL 2.0 license
  is unambiguously open source.
- **Community governance:** OpenTofu is governed by the Linux Foundation with
  multiple corporate backers. No single vendor can change the license.
- **Feature parity plus extras:** OpenTofu has added features not in Terraform,
  including client-side state encryption and early variable/locals evaluation.

**When to stay with Terraform:**

- **Terraform Cloud/Enterprise:** If you use HashiCorp's managed service for
  state management and run orchestration, there's no OpenTofu equivalent (though
  third-party alternatives like Spacelift and env0 support OpenTofu).
- **Stability and support:** HashiCorp provides commercial support. OpenTofu
  relies on community support and corporate sponsors.
- **Team familiarity:** If your team knows ``terraform`` and your workflows are
  built around it, the migration cost may not be worth it for a running system.

For the purposes of this book, every Terraform example works identically with
OpenTofu. Just substitute ``tofu`` for ``terraform`` in the commands.

See also
~~~~~~~~

- :ref:`Recipe_Terraform_Basic` for the base Terraform configuration
- :ref:`Recipe_Terraform_Ansible` for the Terraform + Ansible pattern
- OpenTofu documentation: https://opentofu.org/docs/
- Migration guide: https://opentofu.org/docs/intro/upgrading/


Summary
-------

.. index::
   single: automation; choosing a tool

The tools in this chapter solve different problems at different layers:

- **Ansible, Puppet, Chef** manage the *configuration* of servers that already
  exist. They answer: "Given this server, make httpd look like this."
- **Docker, Podman** package httpd *with its configuration* into an immutable
  artifact. They answer: "Given this image, run httpd anywhere."
- **Terraform, OpenTofu** create the *infrastructure* that httpd runs on. They
  answer: "Give me a server to put httpd on."

If you're starting from scratch in 2026, my opinionated recommendation is:

1. For **traditional server deployments** (VMs, bare metal): Ansible.
It's the most accessible tool with the largest community for new projects.
2. For **containerized deployments**: Docker or Podman with Quadlet for systemd
integration. If you're on RHEL/Fedora, Podman is the default and integrates
beautifully.
3. For **cloud infrastructure provisioning**: OpenTofu (or Terraform if you're
already using it). Pair with Ansible or containers for the actual httpd
configuration.

The real-world pattern is usually a combination: Terraform provisions the VM,
Ansible configures it, and InSpec validates it. Or: Terraform provisions a
container orchestration cluster, and Docker images contain your httpd. The
tools are complementary, not competing.

Whatever you choose, the goal is the same: your httpd configuration is
versioned, reproducible, testable, and deployable without SSH-ing into a server.
If you achieve that, the specific tool matters far less than the discipline.
