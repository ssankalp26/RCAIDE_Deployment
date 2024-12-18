# RCAIDE/Compoments/Fuselages/Tube_Fuselage.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports     
from .Fuselage import Fuselage
from RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_fuselage_moment_of_inertia import  compute_fuselage_moment_of_inertia
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Tube_Fuselage
# ----------------------------------------------------------------------------------------------------------------------  
class Tube_Fuselage(Fuselage):
    """
    A conventional tube-shaped fuselage component for standard aircraft configurations

    Attributes
    ----------
    tag : str
        Identifier for the fuselage component, defaults to 'tube_fuselage'

    Notes
    -----
    This class represents a conventional tube and wing aircraft fuselage.
    Implementation inherits all base geometric and structural properties from
    the parent Fuselage class.

    **Definitions**
    'Tube Fuselage'
        Standard cylindrical fuselage configuration with tapered ends,
        commonly used in commercial and general aviation aircraft

    References
    ----------
    None
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
        self.tag                                    = 'tube_fuselage'
        
    def compute_moment_of_inertia(self, center_of_gravity): 
        I =  compute_fuselage_moment_of_inertia(self,center_of_gravity) 
        return I        
  