# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('C:/Users/Admin/Desktop/SETECO/src'))
sys.path.insert(0, os.path.abspath('C:/Users/Admin/Desktop/SETECO/src/models'))
sys.path.insert(0, os.path.abspath('C:/Users/Admin/Desktop/SETECO/src/models/cliente'))

project = 'StockManagerMyE'
copyright = '2024, Esteban Alexander Zambrano'
author = 'Esteban Alexander Zambrano'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # Si usas Google-style o NumPy-style docstrings
    'sphinx.ext.todo',      # Para mostrar las tareas pendientes
]

templates_path = ['_templates']
exclude_patterns = []

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
