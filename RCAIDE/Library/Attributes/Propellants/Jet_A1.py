## @ingroup Library-Attributes-Propellants
# RCAIDE/Library/Attributes/Propellants/Jet_A1.py
# 
#
# Created:  Mar 2024, M. Clarke

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 

from .Propellant import Propellant
from RCAIDE.Framework.Core import Data

# ---------------------------------------------------------------------------------------------------------------------- 
#  Jet_A1 Propellant Class
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup  Library-Attributes-Propellants
class Jet_A1(Propellant):
    """Jet A1 class propellant  
    """

    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """    
        self.tag                       = 'Jet A1'
        self.reactant                  = 'O2'
        self.density                   = 804.0                            # kg/m^3 (15 C, 1 atm)
        self.specific_energy           = 43.15e6                          # J/kg
        self.energy_density            = 34692.6e6                        # J/m^3
        self.max_mass_fraction         = Data({'Air' : 0.0633, 'O2' : 0.3022})  # kg propellant / kg oxidizer
        self.temperatures.flash        = 311.15                           # K
        self.temperatures.autoignition = 483.15                           # K
        self.temperatures.freeze       = 226.15                           # K
        self.temperatures.boiling      = 0.0                              # K