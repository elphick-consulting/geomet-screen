# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------

project = 'geomet-screen'
copyright = '2026, Elphick Consulting'
author = 'Elphick Consulting'
release = '0.1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_gallery.gen_gallery',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']

html_theme_options = {
    "repository_url": "https://github.com/elphick-consulting/geomet-screen",
    "use_repository_button": True,
}

# -- Sphinx Gallery configuration --------------------------------------------

sphinx_gallery_conf = {
    'examples_dirs': '../../examples',   # path to example scripts
    'gallery_dirs': 'auto_examples',     # path to gallery generated output
    'filename_pattern': '/plot_',        # pattern to identify example files
    'matplotlib_animations': False,
    'image_scrapers': ('matplotlib',),
    'default_thumb_file': None,
    'capture_repr': ('_repr_html_',),  # Capture HTML representations (for plotly)
}
