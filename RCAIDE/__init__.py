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

# Define the version of the package
def get_version():
    """Read the version from the VERSION file."""
    # Get the directory of the current file
    current_dir = os.path.dirname(__file__)
    # Construct the full path to the VERSION file
    version_file_path = os.path.join(current_dir, 'VERSION')
    
    with open(version_file_path, 'r') as version_file:
        return version_file.read().strip()

