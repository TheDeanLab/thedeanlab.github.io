import datetime

# -- Project information -----------------------------------------------------
year = datetime.date.today().year
project = "The Dean Lab"
copyright = f"{year}, Dean Lab, UT Southwestern Medical Center"
author = "Dean Lab, UT Southwestern Medical Center"


# -- General configuration ---------------------------------------------------

autosectionlabel_prefix_document = True
autosummary_generate = False

# Both the class’ and the __init__ method’s docstring are concatenated
# and inserted.
autoclass_content = "class"  # "both"

# inheritance_graph_attrs = {'rankdir': "TB",
#                           'clusterrank': 'local'}
# inheritance_node_attrs  = {'style': 'filled'}

# This value selects how automatically documented members are sorted
# (http://sphinx-doc.org/latest/ext/autodoc.html)
autodoc_member_order = "groupwise"

# This value is a list of autodoc directive flags that should be
# automatically applied to all autodoc
# directives. (http://sphinx-doc.org/latest/ext/autodoc.html)
autodoc_default_flags = [
    "members",
    "inherited-members",
    "show-inheritance",
]

autodoc_inherit_docstrings = True

# The suffix of source filenames.
source_suffix = ".rst"

# If true, the current module name will be prepended to all
# description unit titles (such as .. function::).
add_module_names = True

# The default language to highlight source code
highlight_language = "python"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_show_sphinx = False

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]

html_logo = "cell.png"

pygments_style = "sphinx"
