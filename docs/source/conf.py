# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..//..//src'))
# -- Project information -----------------------------------------------------

project = 'Python API for Makeblock'
copyright = '2020, Makeblock Co., Ltd'
author = 'makeblock'

master_doc = 'index'
# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc','sphinx_rtd_theme','sphinx.ext.autosummary','sphinx.ext.autosectionlabel','autoapi.extension']

autodoc_default_flags = ['members']
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'member-order': 'bysource'
}
autoapi_dirs = ['..//..//src']
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
pygments_style = 'sphinx'
highlight_language = 'python'
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
add_module_names = False
autosummary_generate = True
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = 'sphinx_rtd_theme'
# 'sphinx_hand_theme'
# import sphinx_hand_theme
# html_theme_path = [sphinx_hand_theme.get_html_theme_path()]

#'sphinx_rtd_theme'
#'alabaster'
#
#
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
html_theme_options = {
    # Toc options
    'collapse_navigation': True
}

language = 'en'