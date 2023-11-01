## @ingroup Methods-Propulsion
# RCAIDE/Methods/Propulsion/internal_combustion_engine_propulsor.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Core import Units , Data 
from RCAIDE.Methods.Propulsion.compute_number_of_compoment_groups import compute_number_of_compoment_groups

# pacakge imports  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# compute_propulsor_performance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Propulsion
def compute_propulsor_performance(i,fuel_line_tag,propulsor_group_tag,engines,rotors,N_rotors,conditions): 
    ''' Computes the performance of an internal combustion engine propulsor unit
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs: 
    i                     - index of unique compoment                 [-]
    fuel_line_tag         - tag of network                            [string]
    propulsor_group_tag   - tag of propulsor group                    [string]
    engines               - data structure of engines                 [-]
    rotors                - data structure of engines                 [-]
    N_rotors              - number of rotors in propulsor group       [-]
    escs                  - data structure of engines                 [-]
    state                 - operating data structure                  [-]
    voltage               - system voltage                            [Volts]
     
    Outputs:      
    outputs              - propulsor operating outputs                [-]
    total_thrust         - thrust of propulsor group                  [N]
    total_power          - power of propulsor group                   [V]
    total_current        - current of propulsor group                 [N]
    
    Properties Used: 
    N.A.        
    '''
    ice_net_pg_results      = conditions.energy[fuel_line_tag][propulsor_group_tag]
    noise_pg_results        = conditions.noise[fuel_line_tag][propulsor_group_tag]
    unique_rotor_tags       = ice_net_pg_results.unique_rotor_tags
    unique_engine_tags      = ice_net_pg_results.unique_engine_tags  
    engine                  = engines[unique_engine_tags[i]]
    rotor                   = rotors[unique_rotor_tags[i]]  

    # Throttle the engine
    engine.inputs.omega  = ice_net_pg_results.rotor.rpm * Units.rpm 
    
    # Run the engine
    engine.calculate_power_out_from_throttle(conditions,ice_net_pg_results.engine.throttle)
    mdot         = engine.outputs.fuel_flow_rate * N_rotors[i]
    torque       = engine.outputs.torque     
    
    # link
    rotor.inputs.omega = ice_net_pg_results.rotor.rpm * Units.rpm 

    # Spin the rotor 
    F, Q, P, Cp, outputs, etap = rotor.spin(conditions) 

    # Check to see if magic thrust is needed, the ESC caps throttle at 1.1 already
    eta                 = ice_net_pg_results.engine.throttle  
    P[eta>1.0]          = P[eta>1.0]*eta[eta>1.0]
    F[eta[:,0]>1.0,:]   = F[eta[:,0]>1.0,:]*eta[eta[:,0]>1.0,:]

    # Determine Conditions specific to this instantation of engine and rotors
    R                   = rotor.tip_radius
    rpm                 = engine.inputs.speed / Units.rpm 
    F_mag               = np.atleast_2d(np.linalg.norm(F, axis=1)).T
    total_thrust        = F * N_rotors[i]
    total_power         = P * N_rotors[i]  
      
    # Pack specific outputs

    # Create the outputs
    ice_net_pg_results.mass_flow_rate            = mdot
    ice_net_pg_results.engine.power              = total_power 
    ice_net_pg_results.engine.torque             = torque
    ice_net_pg_results.engine.throttle           = eta 
    ice_net_pg_results.rotor.torque              = Q
    ice_net_pg_results.rotor.rpm                 = rpm
    ice_net_pg_results.rotor.tip_mach            = (R*rpm*Units.rpm)/conditions.freestream.speed_of_sound    
    ice_net_pg_results.rotor.disc_loading        = (F_mag)/(np.pi*(R**2))             
    ice_net_pg_results.rotor.power_loading       = (F_mag)/(P)    
    ice_net_pg_results.rotor.efficiency          = etap
    ice_net_pg_results.rotor.figure_of_merit     = outputs.figure_of_merit
    noise_pg_results.rotor                       = outputs 
 
    return outputs , total_thrust , total_power ,mdot

# ----------------------------------------------------------------------------------------------------------------------
# compute_unique_propulsor_groups
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Propulsion
def compute_unique_propulsor_groups(self): 
    '''Computes the unique rotor groups on a bus    
    
    Assumptions:
    None

    Source:
    N/A

    Inputs: 
    bus                     - bus control unit data structure [-]
    
    Outputs:  
    sorted_propulsors. 
        rotor_indexes       - rotor indexes                   [-]
        unique_rotor_tags   - rotor tags                      [string(s)]
        unique_engine_tags      - engine tags                 [string(s)]
        unique_esc_tags         - electronic speed rotor tags [string(s)]
        N_rotors            - number of rotors                [-]

    Properties Used:
    N/A 
    '''
    
    engines                    = self.engines 
    rotors                     = self.rotors  
    active_propulsor_groups    = self.active_propulsor_groups 
    N_active_propulsor_groups  = len(active_propulsor_groups)
    
    # determine propulsor group indexes 
    engine_group_indexes,engine_group_names,unique_engine_tags              = compute_number_of_compoment_groups(engines,active_propulsor_groups)
    rotor_group_indexes,rotor_groups_names,unique_rotor_tags    = compute_number_of_compoment_groups(rotors,active_propulsor_groups) 
    
    # make sure that each rotor has a engine and esc
    if (len(rotor_group_indexes)!=len(engine_group_indexes)):
        assert('The number of rotors and/or esc is not the same as the number of engines')  
        
    # Count the number of unique pairs of rotors and engines 
    unique_rotor_groups,N_rotors   = np.unique(rotor_group_indexes, return_counts=True)
    unique_engine_groups,_         = np.unique(engine_group_indexes, return_counts=True) 
    if (unique_rotor_groups == unique_engine_groups).all(): # rotors and engines are paired  
        rotor_indexes  = []
        engine_indexes = [] 
        for group in range(N_active_propulsor_groups):
            rotor_indexes.append(np.where(unique_rotor_groups[group]   == rotor_group_indexes)[0][0])
            engine_indexes.append(np.where(unique_engine_groups[group] == engine_group_indexes)[0][0]) 
    else: 
        rotor_indexes   = rotor_group_indexes
        engine_indexes  = engine_group_indexes 
        N_rotors        = np.ones_like(engine_group_indexes)   
    
    sorted_propulsors = Data(rotor_indexes       = rotor_indexes,
                             unique_rotor_tags   = unique_rotor_tags,
                             unique_engine_tags  = unique_engine_tags, 
                             N_rotors            = N_rotors)
    return sorted_propulsors
