# RCAIDE/Compoments/Fuselages/Blended_Wing_Body_Fuselage.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from .Fuselage import Fuselage

# python imports 
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Blended_Wing_Body_Fuselage
# ----------------------------------------------------------------------------------------------------------------------  
class Blended_Wing_Body_Fuselage(Fuselage):
    """
    A blended wing body fuselage component that inherits from the base Fuselage class.

    Attributes
    ----------
    tag : str
        Identifier for the fuselage component, defaults to 'bwb_fuselage'
    aft_centerbody_area : float
        Area of the aft centerbody section, defaults to 0.0
    aft_centerbody_taper : float
        Taper ratio of the aft centerbody section, defaults to 0.0
    cabin_area : float
        Total cabin area, defaults to 0.0

    Returns
    -------
    None

    Notes
    -----
    This class extends the base Fuselage class to represent a blended wing body configuration,
    where the fuselage smoothly transitions into the wing structure.

    """
    
    def __defaults__(self):
        """ This sets the default values for the component to function.
        
        Assumptions:
        None
    
        Source:
        N/A
    
        Inputs:
        None
    
        Outputs:
        None
    
        Properties Used:
        None
        """      
          
        self.tag                   = 'bwb_fuselage'
        self.aft_centerbody_area   = 0.0
        self.aft_centerbody_taper  = 0.0
        self.cabin_area            = 0.0
        
    def compute_moment_of_inertia(self, center_of_gravity): 
        I =  np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]) 
        return I        