## @ingroup Analyses-Mission-Segments-Climb
# RCAIDE/Analyses/Mission/Segments/Climb/Constant_Mach_Linear_Altitude.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Core                                     import Units 
from RCAIDE.Analyses.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Methods.Mission                          import Common,Segments


# ----------------------------------------------------------------------------------------------------------------------
# Constant_Mach_Linear_Altitude
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Analyses-Mission-Segments-Climb
class Constant_Mach_Linear_Altitude(Evaluate):
    """ Climb at a constant mach number but linearly change altitudes over a distance.
    
        Assumptions:
        None
        
        Source:
        None
    """       
    
    def __defaults__(self):
        """ This sets the default solver flow. Anything in here can be modified after initializing a segment.
    
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
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.mach              = 0.5
        self.distance          = 10. * Units.km
        self.altitude_start    = None
        self.altitude_end      = None
        self.true_course_angle = 0.0 * Units.degrees    

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission Specific Unknowns and Residuals 
        # --------------------------------------------------------------------------------------------------------------    
        self.body_angle_control.active             = True            
        self.body_angle_control.initial_values     = [[3.0 * Units.degrees]]  
        self.throttle_control.active               = True
        self.throttle_control.propulsor_list       = None
        self.throttle_control.initial_values       = [[0.5]]       
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Climb.Constant_Mach_Linear_Altitude.initialize_conditions  
        iterate                            = self.process.iterate
        iterate.residuals.total_forces     = Common.Residuals.climb_descent_forces 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.climb_descent   
        

        return

