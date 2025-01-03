# RCAIDE/__init__.py
# 
"""
=============================================
RCAIDE (:mod:`RCAIDE`)
=============================================

.. currentmodule:: RCAIDE

RCAIDE (Rapid Conceptual Aircraft Integrated Design Environment) - A framework for aircraft design and analysis

Sub-folders
============================================

.. autosummary::
   :toctree: generated/

   Framework    -- Core framework functionality and utilities
   Library      -- Components, methods, and analysis tools

Functions
==========================================

.. autosummary::
   :toctree: generated/

   load         -- Load saved RCAIDE data
   save         -- Save RCAIDE data

Classes
-------
.. autosummary::
   :toctree: generated/
   
   Vehicle      -- Base vehicle class for all analyses

Notes
-----
RCAIDE is designed to provide a flexible and extensible environment for aircraft
design and analysis. It uses a modular approach where vehicles can be built up
from components and analyzed through various mission profiles.
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from . import Framework
from . import Library

from .Vehicle  import Vehicle
from .load     import load 
from .save     import save

import importlib.resources
from warnings import simplefilter
import os

simplefilter('ignore')

# Get the version from VERSION file
with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as version_file:
    __version__ = version_file.read().strip()

# Make all important items available at package level
__all__ = [
    '__version__',
    'Framework',
    'Library',
    'Vehicle',
    'load',
    'save'
]

