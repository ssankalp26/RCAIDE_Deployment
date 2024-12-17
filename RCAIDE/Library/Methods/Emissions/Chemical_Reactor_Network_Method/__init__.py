# RCAIDE/Methods/Emissions/__init__.py

# 

"""
Chemical Reactor Network (CRN) Method 

This module provides functionality for building, training and evaluating surrogate models as well 
as direct computation for emission indices using Chemical Reactor Networks.

Notes
-----
The Chemical Reactor Network Method package contains tools for:
- Building CRN emission index surrogate models
- Training CRN emission index surrogate models
- Evaluating chemical reactions using Cantera
- Computing emission indices using CRN models

See Also
--------
Cantera : External chemical kinetics package used for reactor calculations
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
from .build_CRN_EI_surrogates       import build_CRN_EI_surrogates
from .train_CRN_EI_surrogates       import train_CRN_EI_surrogates
from .evaluate_cantera              import evaluate_cantera
from .evaluate_CRN_emission_indices import *  