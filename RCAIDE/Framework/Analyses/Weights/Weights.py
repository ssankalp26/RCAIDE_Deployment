# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from RCAIDE.Framework.Core     import Data
from RCAIDE.Framework.Analyses import Analysis  

# ----------------------------------------------------------------------
#  Analysis
# ---------------------------------------------------------------------- 
class Weights(Analysis):
    """ This is a class that call the functions that computes the weight of 
    an aircraft depending on its configration
    
    Assumptions:
        None

    Source:
        N/A

    Inputs:
        None
        
    Outputs:
        None

    Properties Used:
         N/A
    """
    def __defaults__(self):
        """This sets the default values and methods for the weights analysis.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """           
        self.tag = 'weights'
        
        self.vehicle  = Data()
        self.settings = Data()
        
        self.settings.empty = None
               
        
    def evaluate(self,conditions=None):
        """Evaluate the weight analysis.
    
        Assumptions:
        None

        Source:
        N/A

        Inputs:
        self.vehicle           [Data]
        self.settings          [Data]
        self.settings.empty    [Data]

        Outputs:
        self.weight_breakdown  [Data]
        results                [Data]

        Properties Used:
        N/A
        """         
        # unpack
        vehicle  = self.vehicle
        settings = self.settings
        empty    = self.settings.empty

        # evaluate
        results = empty(vehicle,settings)
        
        # storing weigth breakdown into vehicle
        vehicle.weight_breakdown = results 

        # updating empty weight
        vehicle.mass_properties.operating_empty = results.empty
              
        return results 