
# -- Path setup for local extensions -----------------------------------------

import sys, os
sys.path.insert(0, os.path.abspath('_ext'))

# -- Custom roles ------------------------------------------------------------

from docutils.parsers.rst import roles
from docutils import nodes

def module_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Custom role for Apache module names: :module:`mod_rewrite`"""
    node = nodes.literal(rawtext, text, classes=['module'])
    return [node], []

roles.register_local_role('module', module_role)


# Apache httpd: A Practical Guide
# by Rich Bowen

# -- Project information -----------------------------------------------------

project = 'Apache httpd: A Practical Guide'
copyright = '2004–2026, Rich Bowen. Licensed under the Apache License, Version 2.0. Apache, Apache HTTP Server, Apache httpd, and the Apache oak leaf logo are trademarks of The Apache Software Foundation'
author = 'Rich Bowen'

# The full version, including alpha/beta/rc tags
release = '0.2'
version = '0.2'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'version_badge',
]

# The master toctree document
master_doc = 'index'

# List of patterns to exclude from source
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'README.md',
    'chapters/23_puppet.rst',
    'chapters/appendix.rst',
    'chapters/13_troubleshooting.rst',
    'chapters/appendix_b.rst',
    'CHANGES.rst',
]

# The suffix of source filenames
source_suffix = '.rst'

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'

html_theme_options = {
    'description': 'Solutions and examples for Apache HTTP Server administrators',
    'github_user': 'rbowen',
    'github_repo': 'httpd-practical-guide',
    'fixed_sidebar': True,
    'sidebar_width': '260px',
}

html_static_path = ['_static']

# -- Options for LaTeX/PDF output --------------------------------------------

latex_documents = [
    (master_doc, 'apache_httpd_practical_guide.tex',
     'Apache httpd: A Practical Guide',
     'Rich Bowen', 'manual'),
]

latex_elements = {
    # Empty string: we set custom geometry below (avoids option clash)
    'papersize': '',
    'pointsize': '11pt',
    'preamble': r'''
\usepackage{makeidx}
\makeindex
% KDP 6x9 trade paperback geometry
\geometry{paperwidth=6in, paperheight=9in, inner=0.75in, outer=0.5in, top=0.75in, bottom=0.75in}
% Fix fancyhdr headheight warning
\setlength{\headheight}{14pt}
% Override Sphinx's default tocdepth=0 with our own value.
% Must use AtBeginDocument because Sphinx sets tocdepth=0 after the preamble.
% Depth levels: -1=parts, 0=chapters, 1=sections (recipes), 2=subsections
% We want Parts + Chapters + recipe titles in the TOC.
\AtBeginDocument{\setcounter{tocdepth}{1}}
''',
}

# -- Options for EPUB output -------------------------------------------------

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_show_urls = 'footnote'
epub_use_index = True
epub_basename = 'apache_httpd_practical_guide'

# -- Options for todo extension ----------------------------------------------

# Set to True during development to see todo items in the rendered output
todo_include_todos = False

# -- Intersphinx configuration -----------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Numbered figures and tables ---------------------------------------------

numfig = False
