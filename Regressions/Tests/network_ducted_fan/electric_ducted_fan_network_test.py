# Regression/scripts/Tests/network_ducted_fan/electric_ducted_fan_netowrk.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core                          import Units , Data 
from RCAIDE.Library.Plots                           import *        

# python imports     
import numpy as np  
import sys
import matplotlib.pyplot as plt  

# local imports 
sys.path.append('../../Vehicles')
from NASA_X48    import vehicle_setup as vehicle_setup
from NASA_X48    import configs_setup as configs_setup 

# ----------------------------------------------------------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------------------------------------------------------

def main(): 
    regression_flag = False 
    
    # vehicle data
    vehicle  = vehicle_setup(regression_flag) 
    
    # Set up vehicle configs
    configs  = configs_setup(vehicle)

    # create analyses
    analyses = analyses_setup(configs)

    # mission analyses 
    mission = mission_setup(analyses)
    
    # create mission instances (for multiple types of missions)
    missions = missions_setup(mission) 
     
    # mission analysis 
    results = missions.base_mission.evaluate()  

    # load older results
    save_results(results)
    old_results = load_results()    

    # plt the old results
    plot_mission(results)
    plot_mission(old_results,'k-')
    plt.show()

    # check the results
    if regression_flag:
        check_results(results,old_results)
    else: 
        check_results(old_results,old_results)    
    return 

# ----------------------------------------------------------------------
#   Define the Vehicle Analyses
# ----------------------------------------------------------------------

def analyses_setup(configs):
    
    analyses = RCAIDE.Framework.Analyses.Analysis.Container()
    
    # build a base analysis for each config
    for tag,config in list(configs.items()):
        analysis = base_analysis(config)
        analyses[tag] = analysis
    
    return analyses

def base_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Framework.Analyses.Vehicle() 
    
    # ------------------------------------------------------------------
    #  Weights
    weights         = RCAIDE.Framework.Analyses.Weights.Weights_UAV()
    weights.vehicle = vehicle
    analyses.append(weights)
    
    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics                                       = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method()
    aerodynamics.vehicle                               = vehicle
    aerodynamics.settings.number_of_spanwise_vortices  = 25
    aerodynamics.settings.number_of_chordwise_vortices = 5       
    aerodynamics.settings.model_fuselage               = False
    aerodynamics.settings.drag_coefficient_increment   = 0.0000
    analyses.append(aerodynamics)
 
  
    # ------------------------------------------------------------------
    #  Energy
    energy= RCAIDE.Framework.Analyses.Energy.Energy()
    energy.vehicle  = vehicle 
    analyses.append(energy)
    
    # ------------------------------------------------------------------
    #  Planet Analysis
    planet = RCAIDE.Framework.Analyses.Planets.Planet()
    analyses.append(planet)
    
    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   
    
    # done!
    return analyses    

# ----------------------------------------------------------------------
#   Plot Mission
# ----------------------------------------------------------------------

def plot_mission(results):
      
    
    # Plot Electric Motor and Propeller Efficiencies 
    plot_electric_propulsor_efficiencies(results)
    
        
    return 

# ----------------------------------------------------------------------
#   Define the Mission
# ----------------------------------------------------------------------
    
def mission_setup(analyses):
    
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------
    
    mission = RCAIDE.Framework.Mission.Sequential_Segments()
    mission.tag = 'the_mission'
     
    # unpack Segments module
    Segments = RCAIDE.Framework.Mission.Segments 
    base_segment = Segments.Segment()
    
    # ------------------------------------------------------------------
    #   First Climb Segment: constant Mach, constant segment angle 
    # ------------------------------------------------------------------
    
    segment = Segments.Cruise.Constant_Mach_Constant_Altitude(base_segment)
    segment.tag = "cruise" 
    segment.analyses.extend( analyses.base ) 
    segment.altitude       = 1000 * Units.feet
    segment.mach_number    = 0.2   * Units.kts
    segment.distance       = 1000 * Units.feet  
    segment.initial_battery_state_of_charge                          = 1.0 
                
    # define flight dynamics to model             
    segment.flight_dynamics.force_x                                  = True  
    segment.flight_dynamics.force_z                                  = True     
    
    # define flight controls 
    segment.assigned_control_variables.throttle.active               = True           
    segment.assigned_control_variables.throttle.assigned_propulsors  = [['center_propulsor','starboard_propulsor','port_propulsor']] 
    segment.assigned_control_variables.body_angle.active             = True                   
      
    mission.append_segment(segment) 
    return mission

def missions_setup(mission):

    missions     = RCAIDE.Framework.Mission.Missions() 
    mission.tag  = 'base_mission'
    missions.append(mission)
    
    # done!
    return missions  
    
def check_results(new_results,old_results):

    # check segment values
    check_list = [
        'segments.cruise.conditions.aerodynamics.angles.alpha',
        'segments.cruise.conditions.aerodynamics.coefficients.drag.total',
        'segments.cruise.conditions.aerodynamics.coefficients.lift.total',  
    ]

    # do the check
    for k in check_list:
        print(k)

        old_val = np.max( old_results.deep_get(k) )
        new_val = np.max( new_results.deep_get(k) )
        err = (new_val-old_val)/old_val
        print('Error at Max:' , err)
        assert np.abs(err) < 1e-6 , 'Max Check Failed : %s' % k

        old_val = np.min( old_results.deep_get(k) )
        new_val = np.min( new_results.deep_get(k) )
        err = (new_val-old_val)/old_val
        print('Error at Min:' , err)
        assert np.abs(err) < 1e-6 , 'Min Check Failed : %s' % k        

        print('') 

    return 



def load_results():
    return RCAIDE.load('results_mission_x48.res')

def save_results(results):
    RCAIDE.save(results,'results_mission_x48.res')
    return    

if __name__ == '__main__': 
    main()    
    plt.show()
        
