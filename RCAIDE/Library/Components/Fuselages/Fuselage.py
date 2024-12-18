# RCAIDE/Compoments/Fuselages/Fuselage.py
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from RCAIDE.Framework.Core                import Data 
from RCAIDE.Library.Components.Component  import Container
from RCAIDE.Library.Components            import Component
from RCAIDE.Library.Methods.Weights.Moment_of_Inertia.compute_fuselage_moment_of_inertia import  compute_fuselage_moment_of_inertia

 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Fuselage
# ---------------------------------------------------------------------------------------------------------------------- 
class Fuselage(Component):
    """
    A standard fuselage component for tube and wing aircraft configurations.

    Attributes
    ----------
    tag : str
        Identifier for the fuselage component, defaults to 'fuselage'
    origin : list
        Origin coordinates of the fuselage, defaults to [[0.0,0.0,0.0]]
    aerodynamic_center : list
        Location of the aerodynamic center, defaults to [0.0,0.0,0.0]
    differential_pressure : float
        Pressure differential between cabin and external atmosphere, defaults to 0.0
    seats_abreast : float
        Number of seats side by side in the cabin, defaults to 0.0
    seat_pitch : float
        Distance between seats, defaults to 0.0
    number_coach_seats : float
        Total number of coach seats, defaults to 0.0
    areas : Data
        Container for area-related parameters including front_projected, side_projected, and wetted areas
    effective_diameter : float
        Effective diameter of the fuselage, defaults to 0.0
    width : float
        Width of the fuselage, defaults to 0.0
    heights : Data
        Container for height measurements at maximum, quarter length, three quarters length, 
        wing root quarter chord, and vertical root quarter chord
    lengths : Data
        Container for length measurements including nose, tail, total, cabin, fore_space, and aft_space
    x_rotation : float
        Rotation angle around x-axis, defaults to 0.0
    y_rotation : float
        Rotation angle around y-axis, defaults to 0.0
    z_rotation : float
        Rotation angle around z-axis, defaults to 0.0
    fineness : Data
        Container for fineness ratios of nose and tail
    nose_curvature : float
        Curvature parameter for the nose section, defaults to 1.5
    tail_curvature : float
        Curvature parameter for the tail section, defaults to 1.5
    fuel_tanks : Container
        Container for fuel tank components
    vsp_data : Data
        Container for OpenVSP-related parameters including xsec_surf_id and xsec_num
    Segments : Container
        Container for fuselage segments

    Returns
    -------
    None

    Notes
    -----
    This class represents a conventional tube and wing aircraft fuselage component.
    It provides functionality for defining the geometry, structural properties, and
    configuration of an aircraft fuselage.

    **Assumptions:**
        Conventional fuselage configuration

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
        
        self.tag                                    = 'fuselage'
        self.origin                                 = [[0.0,0.0,0.0]]
        self.aerodynamic_center                     = [0.0,0.0,0.0] 
        self.differential_pressure                  = 0.0    
        self.seats_abreast                          = 0.0
        self.seat_pitch                             = 0.0
        self.number_coach_seats                     = 0.0

        self.areas                                  = Data()
        self.areas.front_projected                  = 0.0
        self.areas.side_projected                   = 0.0
        self.areas.wetted                           = 0.0
        
        self.effective_diameter                     = 0.0
        self.width                                  = 0.0  
        
        self.heights                                = Data() 
        self.heights.maximum                        = 0.0
        self.heights.at_quarter_length              = 0.0
        self.heights.at_three_quarters_length       = 0.0
        self.heights.at_wing_root_quarter_chord     = 0.0
        self.heights.at_vertical_root_quarter_chord = 0.0 
        
        self.lengths                                = Data()     
        self.lengths.nose                           = 0.0
        self.lengths.tail                           = 0.0
        self.lengths.total                          = 0.0 
        self.lengths.cabin                          = 0.0 
        self.lengths.fore_space                     = 0.0
        self.lengths.aft_space                      = 0.0 
        
        self.x_rotation                             = 0.0
        self.y_rotation                             = 0.0
        self.z_rotation                             = 0.0 

        self.fineness                               = Data() 
        self.fineness.nose                          = 0.0 
        self.fineness.tail                          = 0.0  
        self.nose_curvature                         = 1.5
        self.tail_curvature                         = 1.5   
    
        self.fuel_tanks                             = Container()
 
        self.vsp_data                               = Data()
        self.vsp_data.xsec_surf_id                  = ''    # There is only one XSecSurf in each VSP geom.
        self.vsp_data.xsec_num                      = None  # Number if XSecs in fuselage geom. 
        self.Segments                               = Container()
        
    def append_segment(self,segment):
        """ Adds a segment to the fuselage. 
    
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

        # Assert database type
        if not isinstance(segment,Data):
            raise Exception('input component must be of type Data()')

        # Store data
        self.Segments.append(segment)

        return
    
    def append_fuel_tank(self,fuel_tank):
        """ Adds a fuel tank to the fuselage 
    
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

        # Assert database type
        if not isinstance(fuel_tank,Data):
            raise Exception('input component must be of type Data()')
    
        # Store data
        self.Fuel_Tanks.append(fuel_tank)

        return 

    def compute_moment_of_inertia(self, center_of_gravity=[[0, 0, 0]]): 
        I =  compute_fuselage_moment_of_inertia(self,center_of_gravity) 
        return I    