## @ingroup Energy-Networks
# RCAIDE/Energy/Networks/Constant_Speed_Internal_Combustion_Engine_Network.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core                                                                     import Data   
from RCAIDE.Library.Methods.Propulsors.Constant_Speed_ICE_Propulsor.compute_cs_ice_performance import compute_cs_ice_performance
from .Network                                                                                  import Network   
  
# ----------------------------------------------------------------------------------------------------------------------
#  Internal_Combustion_Propeller_Constant_Speed
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Networks
class Constant_Speed_Internal_Combustion_Engine_Network(Network):
    """ An internal combustion engine with a constant speed propeller.
    
        Assumptions:
        0.5 Throttle corresponds to 0 propeller pitch. Less than 0.5 throttle implies negative propeller pitch.
        
        Source:
        None
    """      
    def __defaults__(self):
        """ This sets the default values for the network to function.
    
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
        self.tag                          = 'internal_combustion_engine_constant_speed'      
         
    # manage process with a driver function
    def evaluate_thrust(self,state):
        """ Calculate thrust given the current state of the vehicle
    
            Assumptions:
    
            Source:
            N/A
    
            Inputs:
            state [state()]
    
            Outputs:
            results.thrust_force_vector [newtons]
            results.vehicle_mass_rate   [kg/s]
            conditions.energy:
                rpm                     [radians/sec]
                torque                  [N-M]
                power                   [W]
    
            Properties Used:
            Defaulted values
        """           
        # Step 1: Unpack
        conditions  = state.conditions  
        fuel_lines  = self.fuel_lines 
    
        total_thrust  = 0. * state.ones_row(3) 
        total_power   = 0. * state.ones_row(1) 
        total_mdot    = 0. * state.ones_row(1)   
    
        # Step 2: loop through compoments of network and determine performance
        for fuel_line in fuel_lines:
            if fuel_line.active:   
    
                # Step 2.1: Compute and store perfomrance of all propulsors 
                fuel_line_T,fuel_line_P = compute_cs_ice_performance(fuel_line,state)  
                total_thrust += fuel_line_T   
                total_power  += fuel_line_P  
    
                # Step 2.2: Link each ice constant speed propeller the its respective fuel tank(s)
                for fuel_tank in fuel_line.fuel_tanks:
                    mdot = 0. * state.ones_row(1)   
                    for ice_propeller in fuel_line.propulsors:
                        for source in (ice_propeller.active_fuel_tanks):
                            if fuel_tank.tag == source:  
                                mdot += conditions.energy[fuel_line.tag][ice_propeller.tag].fuel_flow_rate 
    
                    # Step 2.3 : Determine cumulative fuel flow from fuel tank 
                    fuel_tank_mdot = fuel_tank.fuel_selector_ratio*mdot + fuel_tank.secondary_fuel_flow 
    
                    # Step 2.4: Store mass flow results 
                    conditions.energy[fuel_line.tag][fuel_tank.tag].mass_flow_rate  = fuel_tank_mdot  
                    total_mdot += fuel_tank_mdot                    
    
        # Step 3: Pack results 
        conditions.energy.thrust_force_vector  = total_thrust
        conditions.energy.power                = total_power 
        conditions.energy.vehicle_mass_rate    = total_mdot          
    
        # A PATCH TO BE DELETED IN RCAIDE
        results = Data()
        results.thrust_force_vector       = total_thrust
        results.power                     = total_power
        results.vehicle_mass_rate         = total_mdot     
        # --------------------------------------------------  
        
        return results
    def unpack_unknowns(self,segment):
        """Unpacks the unknowns set in the mission to be available for the mission.

        Assumptions:
        N/A
        
        Source:
        N/A
        
        Inputs: 
        
        Outputs: 
        
        Properties Used:
        N/A
        """            
 
        fuel_lines   = segment.analyses.energy.networks.internal_combustion_engine_constant_speed.fuel_lines  
        RCAIDE.Library.Mission.Common.Unpack_Unknowns.energy.fuel_line_unknowns(segment,fuel_lines)
        return    
    
    def add_unknowns_and_residuals_to_segment(self,segment):
        """ This function sets up the information that the mission needs to run a mission segment using this network 
         
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            segment
            eestimated_propulsor_group_throttles           [-]
            estimated_propulsor_group_rpms                 [-]  
            
            Outputs:
            segment
    
            Properties Used:
            N/A 
        """

        fuel_lines  = segment.analyses.energy.networks.internal_combustion_engine_constant_speed.fuel_lines
        ones_row    = segment.state.ones_row   
         
        for fuel_line_i, fuel_line in enumerate(fuel_lines):    
            # ------------------------------------------------------------------------------------------------------            
            # Create fuel_line results data structure  
            # ------------------------------------------------------------------------------------------------------
            segment.state.conditions.energy[fuel_line.tag]       = RCAIDE.Framework.Mission.Common.Conditions()       
            fuel_line_results                                    = segment.state.conditions.energy[fuel_line.tag]   
            segment.state.conditions.noise[fuel_line.tag]        = RCAIDE.Framework.Mission.Common.Conditions()  
            noise_results                                        = segment.state.conditions.noise[fuel_line.tag] 
    
            for fuel_tank in fuel_line.fuel_tanks:               
                fuel_line_results[fuel_tank.tag]                 = RCAIDE.Framework.Mission.Common.Conditions()  
                fuel_line_results[fuel_tank.tag].mass_flow_rate  = ones_row(1)  
                fuel_line_results[fuel_tank.tag].mass            = ones_row(1)  
                
            # ------------------------------------------------------------------------------------------------------
            # Assign network-specific  residuals, unknowns and results data structures
            # ------------------------------------------------------------------------------------------------------
            for propulsor in fuel_line.propulsors:           
                fuel_line_results[propulsor.tag]                         = RCAIDE.Framework.Mission.Common.Conditions()
                fuel_line_results[propulsor.tag].engine                  = RCAIDE.Framework.Mission.Common.Conditions()
                fuel_line_results[propulsor.tag].rotor                   = RCAIDE.Framework.Mission.Common.Conditions()  
                fuel_line_results[propulsor.tag].throttle                = 0. * ones_row(1)
                fuel_line_results[propulsor.tag].y_axis_rotation         = 0. * ones_row(1)   
                fuel_line_results[propulsor.tag].engine.efficiency       = 0. * ones_row(1)
                fuel_line_results[propulsor.tag].engine.torque           = 0. * ones_row(1) 
                fuel_line_results[propulsor.tag].engine.power            = 0. * ones_row(1)  
                fuel_line_results[propulsor.tag].rotor.torque            = 0. * ones_row(1) 
                fuel_line_results[propulsor.tag].engine.rpm              = segment.state.conditions.energy.rpm * ones_row(1)                 
                fuel_line_results[propulsor.tag].rotor.thrust            = 0. * ones_row(1)
                fuel_line_results[propulsor.tag].rotor.rpm               = 0. * ones_row(1)
                fuel_line_results[propulsor.tag].rotor.pitch_command     = 0. * ones_row(1)
                fuel_line_results[propulsor.tag].rotor.disc_loading      = 0. * ones_row(1)                 
                fuel_line_results[propulsor.tag].rotor.power_loading     = 0. * ones_row(1)
                fuel_line_results[propulsor.tag].rotor.tip_mach          = 0. * ones_row(1)
                fuel_line_results[propulsor.tag].rotor.efficiency        = 0. * ones_row(1)   
                fuel_line_results[propulsor.tag].rotor.figure_of_merit   = 0. * ones_row(1) 
                fuel_line_results[propulsor.tag].rotor.power_coefficient = 0. * ones_row(1)    
                noise_results[propulsor.tag]                             = RCAIDE.Framework.Mission.Common.Conditions()          
            
        # Ensure the mission knows how to pack and unpack the unknowns and residuals
        segment.process.iterate.unknowns.network                    = self.unpack_unknowns        
             
        return segment 

    __call__ = evaluate_thrust
