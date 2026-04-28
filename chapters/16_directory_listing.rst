
.. _Chapter_Directory_listing:

=================
Directory Listing
=================

.. epigraph::

   | We're not gonna take it. No, we ain't gonna take it.
   | We're not gonna take it anymore.

   -- Twisted Sister, *We're Not Gonna Take It*


.. index:: Directory listing

.. index:: mod_autoindex

.. index:: Modules,mod_autoindex

.. index:: Indexing

.. index:: Autoindexing


The default Apache HTTP Server package includes a module, ``mod_autoindex``, for displaying a directory
listing as a Web page. The default display is simple and informative, but
the module provides all sorts of controls to let you tweak and customize
the output.


.. admonition:: Modules covered in this chapter

   :module:`mod_autoindex`


.. _Recipe_enabling-autoindex:

Generating Directory/Folder Listings
------------------------------------

.. index:: Enabling autoindexing

.. index:: Directory listing,enabling

.. index:: Autoindexing,enabling


.. _Problem_enabling-autoindex:

Problem
~~~~~~~


You want to see a directory listing when a directory is requested.


.. _Solution_enabling-autoindex:

Solution
~~~~~~~~


Turn on **Options Indexes** for the directory in question:


.. code-block:: text

   <Directory /www/htdocs/images>
       Options +Indexes
   </Directory>


.. _Discussion_enabling-autoindex:

Discussion
~~~~~~~~~~


When a URL maps to a directory or folder in the filesystem,
Apache httpd will respond to the request in one of three ways:


#. If ``mod_dir`` is part of
   the server configuration, **and**
   the mapped directory is within the scope of a **DirectoryIndex** directive, 
   **and** the server can find one of the files
   identified in that directive, then the file will be used to
   generate the response.

#. If ``mod_autoindex`` is
   part of the server configuration and the mapped directory is
   within the scope of an **Options**
   directive that has enabled the **Indexes** keyword, then the server will
   construct a directory listing at runtime and supply it as the
   response.

#. The server will return a 404 ("Resource Not Found") status.
          
Enabling directory listings
---------------------------


The real keys to enabling the server's ability to
automatically generate a listing of files in a directory are the
inclusion of ``mod_autoindex`` in
the configuration and the Indexes keyword to the
**Options** directive. This can be
done either as an absolute form, as in:


.. code-block:: text

   Options FollowSymLinks Indexes


Or in a selective or relative form such as:


.. code-block:: text

   Options -ExecCGI +Indexes


Enabling directory listings should be done with caution.
Because of the scope inheritance mechanism (see
http://httpd.apache.org/docs/sections.html#merging
for more details), directories farther down the tree also will be
affected; and because the server will apply the sequence of rules
listed at the beginning of this section in an effort to provide some
sort of response, a single missing file can result in inadvertent
exposure of your filesystem's contents.


Disabling directory indexing below an enabled directory
-------------------------------------------------------


There are two ways to work around this issue and
ensure that the indexing applies only to the single
directory:

* Add an "**Options** -Indexes" to **.htaccess** files in each
    subdirectory.
            
* Add an "**Options** -Indexes" to a **<Directory>** container that
   matches all the subdirectories.

For example, to permit directory indexes for directory
**/usr/local/htdocs/archives** but
not any subdirectories thereof:


.. code-block:: text

   <Directory /usr/local/htdocs/archives>
       Options +Indexes
   </Directory>
   
   <Directory /usr/local/htdocs/archives/*>
       Options -Indexes
   </Directory>


If this needs to apply only to certain subdirectories, the
task becomes a little more complex. You may be able to accomplish it
with a **<DirectoryMatch>** directive if the
list of subdirectories is reasonably small:


.. code-block:: text

   <Directory /usr/local/htdocs/archives>
       Options +Indexes
   </Directory>
   
   <DirectoryMatch /usr/local/htdocs/archives/(images|video|audio)>
       Options -Indexes
   </DirectoryMatch>


.. _See_Also_enabling-autoindex:

See Also
~~~~~~~~


* :ref:`Recipe_DirectoryIndex`

* http://httpd.apache.org/docs/mod/core.html#options -
   ``Options`` documentation
          
* http://httpd.apache.org/docs/mod/mod_dir.html -
   ``mod_dir`` documentation
          
* http://httpd.apache.org/docs/mod/mod_autoindex.html -
   ``mod_autoindex`` documentation


.. _Recipe_formatting-directory-list:

Specifying How the List Will Be Formatted
-----------------------------------------

.. index:: Formatting directory listing

.. index:: Directory listing,Formatting

.. index:: Indexing,Formatting

.. index:: AutoIndexing,Formatting

.. index:: IndexOptions,FancyIndexing

.. index:: IndexOptions,HTMLTables


.. _Problem_formatting-directory-list:

Problem
~~~~~~~


You want to specify different levels of formatting on the listing.


.. _Solution_formatting-directory-list:

Solution
~~~~~~~~


There are three levels of formatting that can be set. The list
may be unformatted, formatted, or can be rendered in an HTML table.

To enable fancy indexing, do one of the following:


.. code-block:: text

   IndexOptions FancyIndexing
   IndexOptions FancyIndexing HTMLTables


.. _Discussion_formatting-directory-list:

Discussion
~~~~~~~~~~


The 'fancy' formatting is the one that you're most used to
seeing because it's the default setting in most configurations of
httpd.

The **HTMLTable** formtting is
rather less common, and gives a slightly less plain look to the
listing.


.. _See_Also_formatting-directory-list:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_autoindex.html#indexoptions
  - ``IndexOptions`` documentation


.. _Recipe_autoindex-suppress:

Suppressing Certain Columns
---------------------------

.. index:: Suppressing columns in directory indexes

.. index:: Autoindex,suppressing columns

.. index:: Directory listings,suppressing columns

.. index:: IndexOptions,SuppressLastModified


.. _Problem_autoindex-suppress:

Problem
~~~~~~~


You don't want to show certain columns in the directory listing.


.. _Solution_autoindex-suppress:

Solution
~~~~~~~~


Various columns can be suppressed with one of the **Suppress*** 
arguments to the **IndexOptions** directive. For example, to suppress the 
last modified date column:


.. code-block:: text

   IndexOptions SuppressLastModified


.. _Discussion_autoindex-suppress:

Discussion
~~~~~~~~~~


With the exception of the filename, all of the columns in a
directory listing may be suppressed using one of the following
**IndexOptions** arguments:

* **SuppressDescription**—hide the description column.

* **SuppressIcon**—don't display the icon usually shown next to the filename.

* **SuppressLastModified**—hide the column that lists the file datestamp.

* **SuppressSize**—hide the column showing the file size.


.. _See_Also_autoindex-suppress:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_autoindex.html -
   ``mod_autoindex`` documentation


.. _Recipe_Client-formatting:

Allowing the Client to Specify the Formatting
---------------------------------------------

.. index:: Directory listing,Client-specified formatting

.. index:: Indexing,Client-specified formatting

.. index:: Autoindexing,Client-specified formatting


.. _Problem_Client-formatting:

Problem
~~~~~~~


You want to allow the end user to specify how the list will be
formatted. 


.. _Solution_Client-formatting:

Solution
~~~~~~~~


The user may specify which of the formatting options she wishes
to use by adding an ``F`` argument to the query string.

To specify a plain bulleted list:


.. code-block:: text

   http://www.example.com/icons/?F=0


To specify a formatted list:


.. code-block:: text

   http://www.example.com/icons/?F=1


To specify a list arranged in an HTML table:


.. code-block:: text

   http://www.example.com/icons/?F=2


.. _Discussion_Client-formatting:

Discussion
~~~~~~~~~~


Unless **IndexOptions IgnoreClient** is in effect, the end user may apply a number
of layout customizations by adding query string arguments. The
``F`` argument controls the formatting of the list.


.. _See_Also_Client-formatting:

See Also
~~~~~~~~


* :ref:`Recipe_autoindex-user-specified-format`


.. _Recipe_autoindex-icons:

Changing the Listing Icons
--------------------------

.. index:: Directory listing,Icons

.. index:: Indexing,Icons

.. index:: Autoindexing,Icons

.. index:: Icons for directory listings


.. _Problem_autoindex-icons:

Problem
~~~~~~~


You want to use different icons in the directory listing.


.. _Solution_autoindex-icons:

Solution
~~~~~~~~


Use **AddIcon** and its variants
to specify which icons are to be used by different kinds of
files:


.. code-block:: text

   AddIcon /icons/image.gif .gif .jpg .png


.. _Discussion_autoindex-icons:

Discussion
~~~~~~~~~~


There are a number of variants of the **AddIcon** directive that allow you to
associate certain icons with various files, groups of files, or types
of files.

The **AddIcon** directive sets an
icon to be used for files that match a particular pattern. The first
argument is the URI of the icon file to be used. The argument or
arguments following this are file extensions, partial filenames, or
complete filenames, with which this icon should be used.

You also can specify the argument ``^^DIRECTORY^^`` for directories, or
``^^BLANKICON^^`` to be used for blank lines, to
ensure correct spacing.

To specify an icon to be used for the parent directory link, use
an argument of ``"..":``


.. code-block:: text

   AddIcon /icons/up_one.gif ".."


You also may use **AddIconByEncoding** to specify an icon to be
used for files with a particular encoding such as, ``x-gzip``:


.. code-block:: text

   AddIconByEncoding /icons/gzip.gif x-gzip


Use **AddIconByType** for
        associating an icon with a particular MIME type:


.. code-block:: text

   AddIconByType /icons/text.gif text/*
   AddIconByType /icons/html.gif text/html


Finally, you can specify the default icon to be used if nothing
        else matches:


.. code-block:: text

   DefaultIcon /icons/unknown.png


With any of these directives, you also may specify an alternate
        text to be displayed for clients that have image loading turned off.
        The syntax for this is to include the alt text in parentheses before
        the image path:


.. code-block:: text

   AddIcon (IMAGE,/icons/image.gif) .gif .png .jpg


.. _See_Also_autoindex-icons:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_autoindex.html#addicon
   - ``AddIcon`` documentation


.. _Recipe_AddDescription:

Adding Descriptions to Files
----------------------------

.. index:: AddDescription

.. index:: Directory listing,Adding descriptions to files

.. index:: Indexing,Adding descriptions to files

.. index:: Autoindexing,Adding descriptions to files

.. index:: IndexOptions,DescriptionWidth


.. _Problem_AddDescription:

Problem
~~~~~~~


You want to put a brief description of files in the
listing.


.. _Solution_AddDescription:

Solution
~~~~~~~~


Use the **AddDescription**
directive to add a description to certain files or groups of
files:


.. code-block:: text

   AddDescription "GIF image" .gif


.. _Discussion_AddDescription:

Discussion
~~~~~~~~~~


You may set a description for a particular file, or for any file
that matches a particular pattern. The first argument to **AddDescription** is the description that you
want to use, and the second is a substring that will be compared to
file names. Any file that matches the pattern will have the
description used for it.

By default, you have 23 characters available for this
description. That space can be altered explicitly by setting **IndexOptions DescriptionWidth**, or by
suppressing one of the other columns.

You should ensure that the description isn't too long, or it
will be truncated when it reaches the width limit. This can be
annoying when the description is truncated and therefore unreadable.
Also, because you're permitted to use HTML in the description, it's
possible that the HTML could be truncated, leaving unclosed HTML
tags.


.. _See_Also_AddDescription:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_autoindex.html#adddescription


.. _Recipe_ScanHTMLTitles:

Autogenerated Document Titles
-----------------------------

.. index:: ScanHTMLTitles

.. index:: Directory listing,ScanHTMLTitles

.. index:: Indexing,ScanHTMLTitles

.. index:: AutoIndex,ScanHTMLTitles

.. index:: Indexing,Autogenerate file descriptions

.. index:: IndexOptions,ScanHTMLTitles


.. _Problem_ScanHTMLTitles:

Problem
~~~~~~~


You want to have the description of HTML files autogenerated.


.. _Solution_ScanHTMLTitles:

Solution
~~~~~~~~


Place the following in the **<Directory>** scope where you want to
have descriptions automatically loaded from 
the **<Title>** tags of HTML files:


.. code-block:: text

   IndexOptions ScanHTMLTitles


.. _Discussion_ScanHTMLTitles:

Discussion
~~~~~~~~~~


If generating a directory listing of a directory full of HTML
files, it is often convenient to have the titles of those documents
automatically displayed in the description column.

The **ScanHTMLTitles** option has ``mod_autoindex`` look in each HTML
file for the contents of the **<Title>** tag, and use that
value for the description.

This process is, of course, rather file-access intensive, and so
will cause a significant performance degradation proportional to the
number of HTML files that are in the directory.


.. _See_Also_ScanHTMLTitles:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_autoindex.html#indexoptions


.. _Recipe_Index-sorting:

Sorting a directory listing
---------------------------

.. index:: Directory listing,sorting

.. index:: Indexing,sorting

.. index:: Autoindexing,sorting

.. index:: Sorting a directory listing


.. _Problem_Index-sorting:

Problem
~~~~~~~


You want to sort the directory listing by something other than
the defaults.


.. _Solution_Index-sorting:

Solution
~~~~~~~~


.. code-block:: text

   IndexOrderDefault Descending Date


.. _Discussion_Index-sorting:

Discussion
~~~~~~~~~~


The **IndexOrderDefault**
directive allows you to specify, in your configuration file or
**.htaccess** file, the order in
which the directory listing will be displayed, by default. If, for
example, you wish to have files displayed with the most recent one
first, you could use the directive shown in the Solution above.

The possible arguments to **IndexOrderDefault** are:


* Name—the file or directory name
          
* Date—the date and time that the file was most recently modified
          
* Size—the size of the file, in bytes

* Description—the file description, if any, set with the **AddDescription** directive

Any of these may be ordered **Ascending** or **Descending**.

The value of **IndexOrderDefault** may be overridden by the
end user by supplying ``QUERY_STRING``
arguments, unless you explicitly forbid it using **IndexOptions IgnoreClient**.


.. _See_Also_Index-sorting:

See Also
~~~~~~~~


* :ref:`Recipe_IgnoreClient`

* :ref:`Recipe_client-defined-sortorder`


.. _Recipe_client-defined-sortorder:

Allowing a Client-Specified Sort Order
--------------------------------------

.. index:: Directory listing,sorting

.. index:: Indexing,sorting

.. index:: Allowing a client-specified sort order

.. index:: Directory listing,client-specified sort order

.. index:: Indexing,client-specified sort order


.. _Problem_client-defined-sortorder:

Problem
~~~~~~~


You want to allow the end user to specify the order in which the
listing should be ordered.


.. _Solution_client-defined-sortorder:

Solution
~~~~~~~~


Users can supply ``QUERY_STRING`` arguments to modify the sort order:


http://servername/directory/?C=D&O=D

Or you can provide a form allowing the user to select the sort
order, by placing the following form in a **HeaderName** file:


.. code-block:: text

    <form action="" method="get">
    Order by by <select name="C">
    <option value="N" selected="selected"> Name</option>
    <option value="M"> Date Modified</option>
    <option value="S"> Size</option>
    <option value="D"> Description</option>
    </select>
    <select name="O">
    <option value="A" selected="selected"> Ascending</option>
    <option value="D"> Descending</option>
    </select>
    <input type="submit" value="Go" />
    </form>


.. _Discussion_client-defined-sortorder:

Discussion
~~~~~~~~~~


Allowing the end user to control his experience is a powerful
way to make your Web content more useful.

Unless this feature has been explicitly disabled using the
**IgnoreClient** argument to **IndexOptions**, you will always be able to
reorder the directory listing using the **?C=** and **?O=** ``QUERY_STRING`` options.

**O** (order) can be set to
either **A**, for Ascending, or
**D**, for Descending, and **C** (column) may be set to one of the
following:


* N—name of the file or directory


          
* M—the last modified date of the file or directory

          
* S—the size of the file in bytes

 
* D—the description of the file, set with the **AddDescription** directive


The argument parsing routine will quit if it encounters an
        invalid argument.


.. _See_Also_client-defined-sortorder:

See Also
~~~~~~~~


* :ref:`Recipe_autoindex-user-specified-format`
          
* :ref:`Recipe_IgnoreClient`
          
* :ref:`ACB-CH-12-headerfooter`


.. _I_sect112_d1e19544:

Listing the Directories First
-----------------------------

.. index:: Directory listing,directories first

.. index:: FoldersFirst

.. index:: IndexOptions,FoldersFirst

.. index:: Indexing,directories first


Problem
~~~~~~~


You want to have the folders (directories) listed at the top of the directory
listing.


Solution
~~~~~~~~


To have the directories displayed first in the directory
listing, rather than in alphabetical order with the rest of the files,
place the following in your configuration file:


.. code-block:: text

   IndexOptions FoldersFirst


Discussion
~~~~~~~~~~


By default, directory listings are displayed in alphabetical
order, including the directories. However, some people are used to
having the directories at the top, followed by the files. This allows
for faster navigation through deep directory structures.

Adding the **FoldersFirst**
option puts the folders at the top of the listing, followed by the
files in alphabetical order.


See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_autoindex.html#indexoptions
  - ``IndexOptions`` documentation


.. _I_sect112_d1e19584:

Ordering by Version Number
--------------------------


Problem
~~~~~~~


You want to have files ordered by version number so that 1.10
        comes after 1.9 rather than before 1.2.


Solution
~~~~~~~~


To have files sorted in version number order, add the following
        to your configuration file:


.. code-block:: text

   IndexOptions VersionSort


Discussion
~~~~~~~~~~


Sites that distribute software will often have multiple versions
        of the software in the directory, and it is useful to have them
        ordered by version number rather than alphabetically. In this way,
        **httpd-1.10.tar.gz** will be listed
        after **httpd-1.9.tar.gz**, rather
        than between **httpd-1.1.tar.gz** and
        **httpd-1.2.tar.gz**, as it would be
        in alphabetical order.


See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_autoindex.html#addicon


.. _ACB-CH-12-headerfooter:

Display a Standard Header and Footer on Directory Listings
----------------------------------------------------------


Problem
~~~~~~~


You want to display a header above and a footer below your
        directory listing.


Solution
~~~~~~~~


.. code-block:: text

   # Remove the standard HTML header, if desired
   IndexOptions +SuppressHTMLPreamble
   HeaderName /includes/header.html
   ReadmeName /includes/footer.html


Discussion
~~~~~~~~~~


The directives **HeaderName** and
        **ReadmeName** specify the URI of files
        to be used as a header and footer, respectively, for directory
        listings.

If your **HeaderName** file
        contains an HTML ``<head>`` tag,
        ``<title>`` tag, or other things
        associated with the start of an HTML document, you will want to use
        the **IndexOptions \+SuppressHTMLPreamble** directive to disable ``mod_autoindex``'s automatically generated
        HTML heading. Failure to do so will result in an HTML document with
        two heading elements, with the result that any heading attributes set
        in your header will probably be ignored by the browser.

The argument to both **HeaderName** and **ReadmeName** is a URI relative to the current
        directory. That is, if there is no leading slash, it is interpreted as
        a path relative to the current directory, but if there is a leading
        slash, it is interpreted as a URI path—that is, relative to the
        **DocumentRoot**.

Your **HeaderName** and **ReadmeName** can be arbitrarily complex to
        produce whatever page layout you like wrapped around the
        auto-generated directory listing. You could, for example, open
        ``<table>`` or ``<div>`` sections in the header, which
        you then close in the footer, in order to produce page layout
        effects.


See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_autoindex.html


.. _I_sect112_d1e19646:


Allowing the End User to Specify Version Sorting
------------------------------------------------


Problem
~~~~~~~


You want to let the end user enable or disable version
        sorting.


Solution
~~~~~~~~


The user may specify whether to enable or disable the version
        ordering by adding a ``V`` query string
        argument to the URL:

To enable version ordering:


.. code-block:: text

   http://www.example.com/download/?V=1


To disable it:


.. code-block:: text

   http://www.example.com/download/?V=0


Discussion
~~~~~~~~~~


Like the ``F`` argument, the
        ``V`` argument allows the user to
        impose his own custom formatting
        on a directory listing.


See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_autoindex.html


.. _Recipe_Hiding-directory-items:

Hiding Things from the Listing
------------------------------

.. index:: Directory listing,Hiding files

.. index:: AutoIndex,Hiding files

.. index:: Indexing,Hiding Files

.. index:: IndexIgnore


.. _Problem_Hiding-directory-items:

Problem
~~~~~~~


You want to omit certain files from the directory listing.


.. _Solution_Hiding-directory-items:

Solution
~~~~~~~~


Use the ``IndexIgnore`` directive to specify what files you don't want
listed.


.. code-block:: text

   IndexIgnore *.tmp *.swp .svn secret.txt .htaccess


.. _Discussion_Hiding-directory-items:

Discussion
~~~~~~~~~~


Certain files should be ommitted from directory listings.
Temporary files, swap files, and various other generated files don't
need to be shown to users visiting your Web site. Revision control
directories, such as the **CVS**
directory created by CVS, the **.svn** directory created by Subversion,
or the **.git** directory created by Git, also
should not be displayed, as they are unlikely to contain any
information that would be of use to your visitors.


.. note::

   Although this technique can be used to hide private or secret
   documents, it must be understood that these files can still be
   accessed by someone who knows, or guesses, the filename. The files
   are hidden from the directory listing, but they are still
   accessible. Do not use this technique with an expectation of
   security.

   Files that are password-protected are automatically omitted
   from directory listings.


.. _See_Also_Hiding-directory-items:

See Also
~~~~~~~~


* :ref:`Recipe_ShowForbidden`
          
* http://httpd.apache.org/docs/mod/mod_autoindex.html


.. _Recipe_ShowForbidden:

Showing Forbidden Files
-----------------------


.. _Problem_ShowForbidden:

Problem
~~~~~~~


Password-protected files and directories don't show up
in the directory listing.


.. _Solution_ShowForbidden:

Solution
~~~~~~~~


Place the following **IndexOptions** directive in a **<Directory>** block
referring to the directory in question, or in a **.htaccess** file in that directory:


.. code-block:: text

   IndexOptions +ShowForbidden


.. _Discussion_ShowForbidden:

Discussion
~~~~~~~~~~


Directory listings attempt, by default, to protect documents from
prying eyes, if those documents would not be accessible to the client.
As part of that, password-protected files and directories are not
included in the directory listing.

The **ShowForbidden** argument was added for the **IndexOptions** directive,
specifically to address this request.


.. _See_Also_ShowForbidden:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_autoindex.html


.. _I_sect112_d1e18864:

Applying a Stylesheet
---------------------


Problem
~~~~~~~


You want to apply a CSS stylesheet to a directory listing
without supplying a whole **HeaderName** document.


Solution
~~~~~~~~


.. code-block:: text

   IndexStyleSheet /styles/listing.css


Discussion
~~~~~~~~~~


The **IndexStyleSheet** directive
        sets the name of the file that will be used as the CSS for the index
        listing.


See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_autoindex.html


.. _I_sect112_d1e18950:

Searching for Certain Files in a Directory Listing
--------------------------------------------------


Problem
~~~~~~~


You want to provide a way to filter the listing by
        filename.


Solution
~~~~~~~~


Use a P (pattern) argument in the ``QUERY_STRING`` of the URL:


http://servername/directory/?P=a*

Or place the following HTML form in a **HeaderName** file to provide a search feature
        on a directory listing.


.. code-block:: text

    <form action="" method="get">
    Show files matching <input type="text" name="P" value="*" />
    <input type="submit" value="Go" />
    <form>


Discussion
~~~~~~~~~~


``mod_autoindex`` provides several options for client control over the
        output of directory listings. By inserting options in the ``QUERY_STRING`` of the URL, changes can be made
        to the sort order, output formatting, and, as shown in this recipe,
        the files that are shown in the listing.

Using the **?P=** ``QUERY_STRING``, the file listing is filtered
        by the supplied argument. For example, with a URL of: http://servname/directory/?P=a*, any file starting with
        **``a``** will be listed.




See Also
~~~~~~~~


* :ref:`Recipe_autoindex-user-specified-format`

* :ref:`ACB-CH-12-headerfooter`


.. _Recipe_autoindex-user-specified-format:

Complete User Control of Output
-------------------------------


.. _Problem_autoindex-user-specified-format:

Problem
~~~~~~~


You want to combine some of the above techniques to give the end
user full control of the output of a directory listing.


.. _Solution_autoindex-user-specified-format:

Solution
~~~~~~~~


Place the following HTML in a file and use it as the header for
your directory listing:


.. code-block:: text

    <form action="" method="get">
    Show me a <select name="F">
    <option value="0"> Plain list</option>
    <option value="1" selected="selected"> Fancy list</option>
    <option value="2"> Table list</option>
    <select>
    Sorted by <select name="C">
    <option value="N" selected="selected"> Name</option>
    <option value="M"> Date Modified</option>
    <option value="S"> Size</option>
    <option value="D"> Description</option>
    <select>
    <select name="O">
    <option value="A" selected="selected"> Ascending</option>
    <option value="D"> Descending</option>
    <select>
    <select name="V">
    <option value="0" selected="selected"> in Normal
    order</option>
    <option value="1"> in Version order</option>
    <select>
    Matching <input type="text" name="P" value="*" />
    <input type="submit" value="Go" />
    <form>


.. _Discussion_autoindex-user-specified-format:

Discussion
~~~~~~~~~~


Several of these recipes show how to let the end user specify
formatting options in the query string. However, they're likely not
going to know about this.

This recipe allows you to give the end user the full bag of
tricks, and lets her select various formatting options right there in
the page. If you save the above HTML as **header.html**, you can use this in your
directory listing with the **HeaderName** directive:


.. code-block:: text

   HeaderName /header.html


The user can than select various options, reorder the listing,
search for various strings, and alter the formatting of the output to
their heart's content.


.. _See_Also_autoindex-user-specified-format:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_autoindex.html


.. _Recipe_IgnoreClient:

Don't Allow the End User to Modify the Listing
----------------------------------------------

.. index:: IgnoreClient

.. index:: IndexOptions,IgnoreClient


.. _Problem_IgnoreClient:

Problem
~~~~~~~


You don't want the end user to be able to modify the output of
the directory listing.


.. _Solution_IgnoreClient:

Solution
~~~~~~~~


Place the following **IndexOptions** directive in the **<Directory>** scope where you wish this
restriction to be in place:


.. code-block:: text

   IndexOptions +IgnoreClient


.. _Discussion_IgnoreClient:

Discussion
~~~~~~~~~~


Although it is generably preferable to allow the end user to
have some control over her user experience, there may be times when
you wish for a particular directory listing to be presented in a
particular way, without the option of a user to modify that
display.

Although most users will probably be unaware of the ability to
do so, by default any user can modify the output of the directory
listing with a combination of ``QUERY_STRING`` arguments. With the recipe
shown above, this feature is disabled.

When **IgnoreClient** is set,
**SuppressColumnSorting** is also put
into effect. That is, the clickable header at the top of each column
is removed so that the user isn't misled into thinking that he can
alter the sort order by these links.

**IgnoreClient** can be used in conjunction with **IndexOrderDefault**
to enforce a certain nondefault directory listing order.


.. _See_Also_IgnoreClient:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_autoindex.html


.. _Recipe_Listing-aliases:

Aliases in Directory Listings
-----------------------------

.. index:: Directory listing,Aliases

.. index:: Alias,Autoindexing

.. index:: Indexing,Aliases

.. index:: Autoindexing,Aliases


.. _Problem_Listing-aliases:

Problem
~~~~~~~


Aliases don't show up in directory listings.


.. _Solution_Listing-aliases:

Solution
~~~~~~~~


In the directory to be listed, put a file or directory named the
same as the **Alias**. It will be
displayed in the listing, but clicking on it will invoke the **Alias**.


.. _Discussion_Listing-aliases:

Discussion
~~~~~~~~~~


Aliases don't show up in directory listings,
because ``mod_autoindex`` generates the listing by
asking the filesystem for an actual directory listing. The filesystem
doesn't know about the aliases.

There is no way to get ``mod_autoindex`` to pick up on these 
**Alias** es and list them.

You can, however, place items in the directory that act as
placeholders for the **Alias**. Because
an **Alias** is consulted before the
filesystem, when you actually click on the file the **Alias** 
will be invoked and the file ignored.

For example, if you have the following configuration:


.. code-block:: text

   Alias /images /mnt/extra/images


In your document root directory do the following:


.. code-block:: text

   touch images


.. note::

   The ``touch`` command creates a zero-byte file with the specified name.
   If your operating system doesn't have the ``touch`` command, just create
   a file in a text editor, with nothing in it, and save it with the
   specified name.


This will cause ``images`` to show up in the directory listing. However,
when one clicks on that, it will invoke the ``Alias``.


.. _See_Also_Listing-aliases:

See Also
~~~~~~~~


* http://httpd.apache.org/docs/mod/mod_autoindex.html

* http://httpd.apache.org/docs/mod/mod_alias.html


.. _Recipe_autoindex-scriptalias:

Directory Listings in ScriptAliased Directories
-----------------------------------------------

.. index:: ScriptAlias,directory listing

.. index:: Directory listing,ScriptAlias

.. index:: mod_autoindex,ScriptAlias

.. index:: Indexing,ScriptAlias

.. index:: Autoindexing,ScriptAlias


.. _Problem_autoindex-scriptalias:

Problem
~~~~~~~


You want to allow directory indexing in a directory named
in a **ScriptAlias** directive.


.. warning::

   This is almost always a bad idea because it can reveal to
   strangers and possible attackers the names of specific 
   scripts that may be subvertible.


.. _Solution_autoindex-scriptalias:

Solution
~~~~~~~~


Add the following lines to the ``<Directory>`` container that defines the
characteristics of your ``ScriptAlias``ed directory:


.. code-block:: text

   Options +Indexes


.. _Discussion_autoindex-scriptalias:

Discussion
~~~~~~~~~~


The **ScriptAlias** directive imposes a lot of restrictions on 
directories to which it is applied, primarily for reasons of
security. After all, such directories contain scripts of arbitrary
code that will be executed on your system; if you should happen to be
using a well-known and popular script in which a vulnerability is
subsequently detected, anyone on the Web may be able to take advantage
of it.

One of the restrictions imposed explicitly by design is
disallowing directory listings in ``ScriptAlias``ed parts 
of the filesystem. This amounts to what's called 
"security through obscurity"—namely, hiding
an issue and hoping that no one discovers it even though it's easily
accessible—but it's better than advertising what scripts your server
can execute.

However, under some circumstances you may want to allow
directory listings in such directories—or at least the use of
pseudolistings provided by files named in a ``DirectoryIndex`` directive. To do this
you need to override the special protections.

To do this, you add the ``Indexes`` option to the directory in question,
even though it is usually explicitly excluded.

Summary
-------


Auto-indexed directories are very useful in many different scenarios,
usually involving a large number of files which you want to make
available for random browsing.

In this chapter, I've discussed how to make these indexes more useful,
more user-friendly, and more attractive.

See also the ``mod_autoindex`` documentation at
http://httpd.apache.org/docs/mod/mod_autonidex.html for
more detail and examples.


