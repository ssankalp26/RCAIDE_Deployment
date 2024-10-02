# SUAVE/__init__.py
#

""" SUAVE Package Setup
"""

# ----------------------------------------------------------------------
#  IMPORT!!
# ----------------------------------------------------------------------

# packages
from . import Plugins
from . import Core
from . import Components
from . import Analyses
from . import Methods
from . import Attributes
from . import Optimization 

# the vehicle class
from .Vehicle import Vehicle

from warnings import simplefilter
simplefilter('ignore')

