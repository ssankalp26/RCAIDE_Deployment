
# RCAIDE/Core/Units.py
# 
# 
# Created:  Dec 2024, Niranjan Nanjappa 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------        

from .               import Data
from warnings        import warn
import random

import string
chars = string.punctuation + string.whitespace
t_table = str.maketrans( chars          + string.ascii_uppercase , 
                            '_'*len(chars) + string.ascii_lowercase )

# ----------------------------------------------------------------------------------------------------------------------
#  Container
# ----------------------------------------------------------------------------------------------------------------------   

class Units():
    """ RCAIDE.Core.Units()
        Unit conversion toolbox
        Works by converting values in to and out of the base unit
        
        Important Note and Warning - 
            This does not enforce unit consistency!!!
            Unit consistency is the responsibility of the user
        
        Usage:
          from RCAIDE.Framework.Core import Units
          a = 4. * Units.mm  # convert in to base unit
          b = a  / Units.mm  # convert out of base unit
          
        Comments:
          Retreving an attribute of Units (ie Units.mm) returns 
          the conversion ratio to the base unit.  So in the above
          example Units.mm = 0.001, which is the conversion ratio
          to meters.  Thus the * (multiplication) operation converts 
          from the current units to the base units and / (division) 
          operation converts from the base units to the desired units.
         
        Base Units:
          mass        : kilogram
          length      : meters
          time        : seconds
          temperature : Kelvin
          angle       : radian
          current     : Ampere
          luminsoity  : candela
        
    """
            
        
    class Units:
        # Conversion factors to base units
        _FEET_TO_METERS = 0.3048
        _DEGREES_TO_RADIANS = 0.0174533
        _MINUTES_TO_SECONDS = 60
        _SLUGS_TO_KG = 14.5939
    
        def __init__(self, factor):
            self.factor = factor
    
        def __mul__(self, value):
            return value * self.factor
    
        def __rmul__(self, value):
            return value * self.factor
    
        # Class level properties
        @classmethod
        @property
        def feet_per_sec(cls):
            return cls(cls._FEET_TO_METERS)
    
        @classmethod
        @property
        def degrees(cls):
            return cls(cls._DEGREES_TO_RADIANS)
    
        @classmethod
        @property
        def minutes(cls):
            return cls(cls._MINUTES_TO_SECONDS)
    
        @classmethod
        @property
        def slugs(cls):
            return cls(cls._SLUGS_TO_KG)