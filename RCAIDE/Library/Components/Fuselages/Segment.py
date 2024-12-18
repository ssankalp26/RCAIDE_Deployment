# RCAIDE/Library/Compoments/Fuselage/Segment.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from RCAIDE.Framework.Core import Data, Container
from RCAIDE.Library.Components import Component  

# ---------------------------------------------------------------------------------------------------------------------- 
#  Segment
# ----------------------------------------------------------------------------------------------------------------------   
class Segment(Component):
    """
    A component representing a single cross-sectional segment of a fuselage
    Attributes
    ----------
    tag : str
        Identifier for the segment, defaults to 'segment'
    prev : Component
        Link to the previous segment in the fuselage chain
    next : Component
        Link to the next segment in the fuselage chain
    percent_x_location : float
        Longitudinal position as percentage of fuselage length
    percent_y_location : float
        Lateral position as percentage of fuselage width
    percent_z_location : float
        Vertical position as percentage of fuselage height
    height : float
        Vertical dimension of the segment cross-section
    width : float
        Lateral dimension of the segment cross-section
    curvature : float
        Shape parameter controlling cross-section corner rounding, defaults to 2

    Notes
    -----
    Segments are the building blocks of a fuselage, defining its shape through
    a series of connected cross-sections. Each segment's position is defined
    relative to the overall fuselage dimensions.

    **Definitions**
    'Curvature'
        Parameter controlling the smoothness of transition between vertical
        and horizontal surfaces at the corners of the cross-section
    """

    def __defaults__(self): 
        """This sets the default for fuselage segments in RCAIDE.

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
        self.tag                     = 'segment'
        self.prev                    = None
        self.next                    = None    
        self.percent_x_location      = 0  
        self.percent_y_location      = 0
        self.percent_z_location      = 0 
        self.height                  = 0 
        self.width                   = 0 
        self.curvature               = 2
         
class Segment_Container(Container):
    """ Container for fuselage segment
    
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

    def get_children(self):
        """ Returns the components that can go inside
        
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
        
        return []