#
# NLTK documentation build configuration file, created by
# sphinx-quickstart on Wed Nov  2 17:02:59 2011.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import os
import sys

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# build docs using nltk from the upper dir, not the installed version
sys.path.insert(0, os.path.abspath(".."))

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.imgmath",
    "sphinx.ext.viewcode",
]


def run_apidoc(app):
    """Generage API documentation"""
    import better_apidoc

    better_apidoc.APP = app
    better_apidoc.main(
        [
            "better-apidoc",
            "-t",
            os.path.join(".", "web", "_templates"),
            "--force",
            "--separate",
            "-o",
            os.path.join(".", "web", "api"),
            os.path.join(".", "nltk"),
        ]
    )


def generate_custom_files():
    """Generating contents in the ``howto`` folder,
    based on the ``ntlk/test/*.doctest`` files, as well
    as contents in the ``team`` folder, based on
    ``team.json``.
    """
    import glob
    import json
    import re

    from jinja2 import Template

    modules = []

    web_folder = os.path.dirname(os.path.abspath(__file__))
    howto_folder = os.path.join(web_folder, "howto")
    if not os.path.exists(howto_folder):
        os.makedirs(howto_folder)

    # Load jinja template
    with open(os.path.join(web_folder, "_templates", "doctest.rst")) as f:
        doctest_template = Template(f.read())

    print("Generating HOWTO pages...")
    # Iterate over .doctest files, and find the module_name.
    pattern = re.compile(r"(\w+)\.doctest$")
    for path in glob.glob(os.path.join(web_folder, "..", "nltk", "test", "*.doctest")):
        match = pattern.search(path)
        module_name = match.group(1)
        # Ignore index.doctest, we already have an index, i.e. howto.rst
        if module_name == "index":
            continue
        # Write .rst files based on the doctest_template.
        doctest_template.stream(module_name=module_name).dump(
            os.path.join(howto_folder, f"{module_name}.rst")
        )
        modules.append(module_name)

    print(f"Generated {len(modules)} HOWTO pages.")

    # Load the team JSON data
    with open(os.path.join(web_folder, "team", "team.json")) as f:
        full_data = json.load(f)
    print("Team data loaded!")

    # Load the team jinja template
    with open(os.path.join(web_folder, "_templates", "team.html")) as f:
        team_template = Template(f.read())

    for members_type, members_data in full_data.items():
        team_template.stream(members=members_data).dump(
            os.path.join(web_folder, "team", f"{members_type}_team.html")
        )
        print(f"{members_type.title()} team HTML page written!")


# Build the Team & HOWTO page before creating the Sphinx build
generate_custom_files()

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = ".rst"

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "NLTK"
copyright = "2022, NLTK Project"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = "3.6.7"
# The full version, including alpha/beta/rc tags.
release = "3.6.7"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build", "api/modules.rst", "dev/*.rst"]

# The reST default role (used for this markup: `text`) to use for all documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# A list of ignored prefixes for module index sorting.
modindex_common_prefix = ["nltk."]


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "nltk_theme"


def setup(app):
    app.connect("builder-inited", run_apidoc)


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {"navigation_depth": 1}
# Required for the theme, used for linking to a specific tag in the website footer
html_context = {"github_user": "nltk", "github_repo": "nltk"}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%b %d, %Y"
# html_last_updated_fmt = "%d %b %Y"

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
html_domain_indices = True

# If false, no index is generated.
# We don't use the genindex.
html_use_index = False

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = "NLTKdoc"


# -- Options for LaTeX output --------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [("index", "NLTK.tex", "NLTK Documentation", "Steven Bird", "manual")]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [("index", "nltk", "NLTK Documentation", ["Steven Bird"], 1)]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        "index",
        "NLTK",
        "NLTK Documentation",
        "Steven Bird",
        "NLTK",
        "One line description of project.",
        "Miscellaneous",
    )
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# -- Options for Autodoc output ------------------------------------------------
# If it's "mixed", then the documentation for each parameter isn't listed
# e.g. nltk.tokenize.casual.TweetTokenizer(preserve_case=True, reduce_len=False, strip_handles=False, match_phone_numbers=True)
# and that's it.
# With "seperated":
# nltk.tokenize.casual.TweetTokenizer
# ...
# __init__(preserve_case=True, reduce_len=False, strip_handles=False, match_phone_numbers=True)
#     Create a TweetTokenizer instance with settings for use in the tokenize method.
#     Parameters
#         preserve_case (bool) – Flag indicating whether to preserve the casing (capitalisation) of text used in the tokenize method. Defaults to True.
#         reduce_len (bool) – Flag indicating whether to replace repeated character sequences of length 3 or greater with sequences of length 3. Defaults to False.
#         strip_handles (bool) – Flag indicating whether to remove Twitter handles of text used in the tokenize method. Defaults to False.
#         match_phone_numbers (bool) – Flag indicating whether the tokenize method should look for phone numbers. Defaults to True.
autodoc_class_signature = "separated"

# Put the Python 3.5+ type hint in the signature and also at the Parameters list
autodoc_typehints = "both"
