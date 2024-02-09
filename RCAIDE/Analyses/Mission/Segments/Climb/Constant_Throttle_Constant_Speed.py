## @ingroup Analyses-Mission-Segments-Climb
# RCAIDE/Analyses/Mission/Segments/Climb/Constant_Throttle_Constant_Speed.py
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
# Constant_Throttle_Constant_Speed
# ---------------------------------------------------------------------------------------------------------------------- 
 
## @ingroup Analyses-Mission-Segments-Climb
class Constant_Throttle_Constant_Speed(Evaluate):
    """ Climb at a constant throttle setting and true airspeed. This segment may not always converge as the vehicle 
        could be deficient in thrust. Useful as a check to see the climb rate at the top of climb.
    
        Assumptions:
        You set a reasonable throttle setting that can provide enough thrust.
        
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
        self.altitude_start    = None # Optional
        self.altitude_end      = 10. * Units.km
        self.throttle          = 0.5
        self.air_speed         = None
        self.true_course_angle = 0.0 * Units.degrees      

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission Specific Unknowns and Residuals 
        # --------------------------------------------------------------------------------------------------------------   
        self.body_angle_control.active             = True            
        self.body_angle_control.initial_values     = [[5.0 * Units.degrees]]  
        self.wind_angle.active                     = True 
        self.wind_angle.initial_values             = [[1.0 * Units.deg]]               

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------      
        initialize                         = self.process.initialize  
        initialize.velocities              = Segments.Climb.Constant_Throttle_Constant_Speed.update_velocity_vector_from_wind_angle
        initialize.conditions              = Segments.Climb.Constant_Throttle_Constant_Speed.initialize_conditions
        iterate                            = self.process.iterate
        iterate.unknowns.mission           = Segments.Climb.Constant_Throttle_Constant_Speed.unpack_body_angle 
        iterate.differentials_altitude     = Segments.Climb.Constant_Throttle_Constant_Speed.update_differentials_altitude
        iterate.velocities                 = Segments.Climb.Constant_Throttle_Constant_Speed.update_velocity_vector_from_wind_angle
        iterate.residuals.total_forces     = Common.Residuals.climb_descent_forces  
        return

