## @ingroup Methods-Weights-Buildups-eVTOL 
# RCAIDE/Methods/Weights/Buildups/eVTOL/converge_evtol_weight.py
# 
# 
# Created:  Sep 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE
from RCAIDE.Library.Methods.Weights.Physics_Based_Buildups.Electric import compute_operating_empty_weight
from RCAIDE.Framework.Core import Data

# ----------------------------------------------------------------------------------------------------------------------
# converge_evtol_weight
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Weights-Buildups-eVTOL 
def converge_weight(vehicle,
                    print_iterations              = False,
                    miscelleneous_weight_factor   = 1.1,):
    '''Converges the maximum takeoff weight of an aircraft using the eVTOL 
    weight buildup routine.  
    
    Source:
    None
    
    Assumptions:
    None
    
    Inputs:
    vehicle                     RCAIDE Config Data Stucture
    print_iterations            Boolean Flag      
    miscelleneous_weight_factor          Factor capturing uncertainty in vehicle weight [Unitless]
    speed_of_sound:             Local Speed of Sound                           [m/s]
    max_tip_mach:               Allowable Tip Mach Number                      [Unitless]
    disk_area_factor:           Inverse of Disk Area Efficiency                [Unitless]
    max_thrust_to_weight_ratio: Allowable Thrust to Weight Ratio               [Unitless]
    safety_factor               Safety Factor in vehicle design                [Unitless]
    max_g_load                  Maximum g-forces load for certification        [UNitless]
    motor_efficiency:           Motor Efficiency                               [Unitless]
    
    Outputs:
    None
    
    Properties Used:
    N/A
    '''
    breakdown      = compute_operating_empty_weight(vehicle,miscelleneous_weight_factor) 
    build_up_mass  = breakdown.total    
    diff           = vehicle.mass_properties.max_takeoff - build_up_mass
    iterations     = 0
    
    while(abs(diff)>1):
        vehicle.mass_properties.max_takeoff = vehicle.mass_properties.max_takeoff - diff
        breakdown      = compute_operating_empty_weight(vehicle,miscelleneous_weight_factor)
        build_up_mass  = breakdown.total    
        diff           = vehicle.mass_properties.max_takeoff - build_up_mass 
        iterations     += 1
        if print_iterations:
            print(round(diff,3))
        if iterations == 100:
            print('Weight convergence failed!')
            return False 
    print('Converged MTOW = ' + str(round(vehicle.mass_properties.max_takeoff)) + ' kg')
    
    return True 
