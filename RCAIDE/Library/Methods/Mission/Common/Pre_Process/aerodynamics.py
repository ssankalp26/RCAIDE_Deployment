## @ingroup Methods-Missions-Segments-Common-Pre_Process
# RCAIDE/Methods/Missions/Common/Pre_Process/aerodynamics.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
import RCAIDE 
# ----------------------------------------------------------------------------------------------------------------------
#  aerodynamics
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Missions-Segments-Common-Pre_Process
def aerodynamics(mission):
    """ Runs aerdoynamics model and build surrogate
    
        Assumptions:
            N/A
        
        Inputs:
            None
            
        Outputs:
            None 

        Properties Used:
        N/A                
    """      
    last_tag = None
    for tag,segment in mission.segments.items():        
        if (type(segment.analyses.aerodynamics) == RCAIDE.Framework.Analyses.Aerodynamics.Subsonic_VLM) or (type(segment.analyses.aerodynamics) == RCAIDE.Framework.Analyses.Aerodynamics.Supersonic_VLM): 
            if last_tag: 
                segment.analyses.aerodynamics.process.compute.lift.inviscid_wings = mission.segments[last_tag].analyses.aerodynamics.process.compute.lift.inviscid_wings 
            else:
                aero                      = segment.analyses.aerodynamics   
                aero.process.compute.lift.inviscid_wings.geometry                = aero.geometry 
                aero.process.compute.lift.inviscid_wings.settings.model_fuselage = aero.settings.model_fuselage
                aero.process.compute.lift.inviscid_wings.initialize()  
                
                last_tag = tag  
    return 