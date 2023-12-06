# Regression/scripts/Vehicles/Solar_UAV.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE
from RCAIDE.Core                             import Units, Data
from RCAIDE.Energy.Networks.Solar            import Solar
from RCAIDE.Methods.Propulsion.Design        import design_propeller
from RCAIDE.Methods.Power.Battery.Sizing     import initialize_from_energy_and_power, initialize_from_mass
from RCAIDE.Methods.Weights.Correlation_Buildups.UAV import empty

# python imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#   Build the Vehicle
# ----------------------------------------------------------------------------------------------------------------------
def vehicle_setup(): 
    # ------------------------------------------------------------------
    #   Initialize the Vehicle
    # ------------------------------------------------------------------    
    
    vehicle = RCAIDE.Vehicle()
    vehicle.tag = 'Solar'
     
    # ################################################# Vehicle-level Properties ########################################################  
    # mass properties
    vehicle.mass_properties.takeoff         = 250. * Units.kg
    vehicle.mass_properties.operating_empty = 250. * Units.kg
    vehicle.mass_properties.max_takeoff     = 250. * Units.kg 
    
    # basic parameters
    vehicle.reference_area                    = 80.       
    vehicle.envelope.ultimate_load            = 2.0
    vehicle.envelope.limit_load               = 1.5
    vehicle.envelope.maximum_dynamic_pressure = 0.5*1.225*(40.**2.) #Max q

    ############################################################  Wings ################################################################   

    # ------------------------------------------------------------------        
    #   Main Wing
    # ------------------------------------------------------------------   

    wing                         = RCAIDE.Components.Wings.Wing()
    wing.tag                     = 'main_wing' 
    wing.areas.reference         = vehicle.reference_area
    wing.spans.projected         = 40.0 * Units.meter
    wing.aspect_ratio            = (wing.spans.projected**2)/wing.areas.reference 
    wing.sweeps.quarter_chord    = 0.0 * Units.deg
    wing.symmetric               = True
    wing.thickness_to_chord      = 0.12
    wing.taper                   = 1.0
    wing.vertical                = False
    wing.high_lift               = True 
    wing.dynamic_pressure_ratio  = 1.0
    wing.chords.mean_aerodynamic = wing.areas.reference/wing.spans.projected
    wing.chords.root             = wing.areas.reference/wing.spans.projected
    wing.chords.tip              = wing.areas.reference/wing.spans.projected
    wing.twists.root             = 0.0 * Units.degrees
    wing.twists.tip              = 0.0 * Units.degrees
    wing.highlift                = False  
    wing.vertical                = False 
    wing.number_ribs             = 26.
    wing.number_end_ribs         = 2.
    wing.transition_x_upper      = 0.6
    wing.transition_x_lower      = 1.0
    wing.origin                  = [[3.0,0.0,0.0]] # meters
    wing.aerodynamic_center      = [3.0,0.0,0.0] # meters
    
    # add to vehicle
    vehicle.append_component(wing)
    
    # ------------------------------------------------------------------        
    #  Horizontal Stabilizer
    # ------------------------------------------------------------------   
    wing                         = RCAIDE.Components.Wings.Wing()
    wing.tag                     = 'horizontal_stabilizer' 
    wing.aspect_ratio            = 20. 
    wing.sweeps.quarter_chord    = 0 * Units.deg
    wing.thickness_to_chord      = 0.12
    wing.taper                   = 1.0
    wing.areas.reference         = vehicle.reference_area * .15
    wing.areas.wetted            = 2.0 * wing.areas.reference
    wing.areas.exposed           = 0.8 * wing.areas.wetted
    wing.areas.affected          = 0.6 * wing.areas.wetted       
    wing.spans.projected         = np.sqrt(wing.aspect_ratio*wing.areas.reference)
    wing.twists.root             = 0.0 * Units.degrees
    wing.twists.tip              = 0.0 * Units.degrees 
    wing.vertical                = False 
    wing.symmetric               = True
    wing.dynamic_pressure_ratio  = 0.9      
    wing.number_ribs             = 5.0
    wing.chords.root             = wing.areas.reference/wing.spans.projected
    wing.chords.tip              = wing.areas.reference/wing.spans.projected
    wing.chords.mean_aerodynamic = wing.areas.reference/wing.spans.projected  
    wing.origin                  = [[10.,0.0,0.0]] # meters
    wing.aerodynamic_center      = [0.5,0.0,0.0] # meters
  
    # add to vehicle
    vehicle.append_component(wing)    
    
    # ------------------------------------------------------------------
    #   Vertical Stabilizer
    # ------------------------------------------------------------------
    
    wing                         = RCAIDE.Components.Wings.Wing()
    wing.tag                     = 'vertical_stabilizer' 
    wing.aspect_ratio            = 20.       
    wing.sweeps.quarter_chord    = 0 * Units.deg
    wing.thickness_to_chord      = 0.12
    wing.taper                   = 1.0
    wing.areas.reference         = vehicle.reference_area * 0.1
    wing.spans.projected         = np.sqrt(wing.aspect_ratio*wing.areas.reference) 
    wing.chords.root             = wing.areas.reference/wing.spans.projected
    wing.chords.tip              = wing.areas.reference/wing.spans.projected
    wing.chords.mean_aerodynamic = wing.areas.reference/wing.spans.projected 
    wing.areas.wetted            = 2.0 * wing.areas.reference
    wing.areas.exposed           = 0.8 * wing.areas.wetted
    wing.areas.affected          = 0.6 * wing.areas.wetted    
    wing.twists.root             = 0.0 * Units.degrees
    wing.twists.tip              = 0.0 * Units.degrees  
    wing.origin                  = [[10.,0.0,0.0]] # meters
    wing.aerodynamic_center      = [0.5,0.0,0.0] # meters
    wing.symmetric               = True  
    wing.vertical                = True 
    wing.t_tail                  = False
    wing.dynamic_pressure_ratio  = 1.0
    wing.number_ribs             = 5.
  
    # add to vehicle
    vehicle.append_component(wing)  
    
    # ------------------------------------------------------------------
    #   Nacelle  
    # ------------------------------------------------------------------
    nacelle              = RCAIDE.Components.Nacelles.Nacelle()
    nacelle.diameter     = 0.2 * Units.meters
    nacelle.length       = 0.01 * Units.meters
    nacelle.tag          = 'nacelle' 
    nacelle.areas.wetted =  nacelle.length *(2*np.pi*nacelle.diameter/2.)
    vehicle.append_component(nacelle) 
    

    # ########################################################  Energy Network  #########################################################       
    # build network
    net                              = Solar()  

    #------------------------------------------------------------------------------------------------------------------------------------      
    # Sun 
    #------------------------------------------------------------------------------------------------------------------------------------  
    sun                                            = RCAIDE.Energy.Processes.Solar_Radiation()
    net.solar_flux                                 = sun 
    net.maximum_power_point_tracking_efficency     = 0.95 
    
    #------------------------------------------------------------------------------------------------------------------------------------  
    # Bus
    #------------------------------------------------------------------------------------------------------------------------------------  
    bus                        = RCAIDE.Energy.Distribution.Bus_Power_Control_Unit() 
    bus.voltage                = 40

    #------------------------------------------------------------------------------------------------------------------------------------  
    # Solar Panel 
    #------------------------------------------------------------------------------------------------------------------------------------ 
    panel                      = RCAIDE.Energy.Propulsors.Converters.Solar_Panel()
    panel.area                 = vehicle.reference_area * 0.9
    panel.efficiency           = 0.25
    panel.mass_properties.mass = panel.area*(0.60 * Units.kg)
    bus.solar_panel            = panel


    #------------------------------------------------------------------------------------------------------------------------------------           
    # Battery
    #------------------------------------------------------------------------------------------------------------------------------------  
    bat = RCAIDE.Energy.Storages.Batteries.Lithium_Ion_Generic() 
    bat.mass_properties.mass = 90.0 * Units.kg
    bat.specific_energy      = 600. * Units.Wh/Units.kg
    bat.resistance           = 0.05
    bat.pack.maximum_voltage = 45.0
    bat.thermal_management_system = RCAIDE.Energy.Thermal_Management.Batteries.No_Heat_Exchanger() 
    initialize_from_mass(bat) 
    bus.batteries.append(bat)                                
          
    #------------------------------------------------------------------------------------------------------------------------------------  
    # Propulsor
    #------------------------------------------------------------------------------------------------------------------------------------   
    propulsor  = RCAIDE.Energy.Propulsors.Propulsor()  
    
    #------------------------------------------------------------------------------------------------------------------------------------  
    # Electronic Speed Controller    
    #------------------------------------------------------------------------------------------------------------------------------------ 
    esc            = RCAIDE.Energy.Propulsors.Modulators.Electronic_Speed_Controller()
    esc.efficiency = 0.95 
    propulsor.electronic_speed_controller  = esc   
    #------------------------------------------------------------------------------------------------------------------------------------  
    # Propeller    
    #------------------------------------------------------------------------------------------------------------------------------------    
    propeller                                       = RCAIDE.Energy.Propulsors.Converters.Propeller()
    propeller.number_of_blades                      = 2.0
    propeller.tip_radius                            = 4.25 * Units.meters
    propeller.hub_radius                            = 0.05 * Units.meters
    propeller.cruise.design_freestream_velocity     = 40.0 * Units['m/s'] 
    propeller.cruise.design_angular_velocity        = 150. * Units['rpm']
    propeller.cruise.design_Cl                      = 0.7
    propeller.cruise.design_altitude                = 14.0 * Units.km
    propeller.cruise.design_thrust                  = 110.  
    propeller                                       = design_propeller(propeller) 
    propulsor.rotor                                 = propeller  

    #------------------------------------------------------------------------------------------------------------------------------------           
    # Motor 
    #------------------------------------------------------------------------------------------------------------------------------------   
    motor                      = RCAIDE.Energy.Propulsors.Converters.Motor()
    motor.resistance           = 0.008
    motor.no_load_current      = 4.5  * Units.ampere
    motor.speed_constant       = 120. * Units['rpm'] # RPM/volt converted to (rad/s)/volt    
    motor.rotor_radius         = propeller.tip_radius
    motor.propeller_Cp         = propeller.cruise.design_power_coefficient
    motor.gear_ratio           = 12. # Gear ratio
    motor.gearbox_efficiency   = .98 # Gear box efficiency
    motor.expected_current     = 160. # Expected current
    motor.mass_properties.mass = 2.0  * Units.kg
    propulsor.motor            = motor 


    #------------------------------------------------------------------------------------------------------------------------------------           
    # Payload 
    #------------------------------------------------------------------------------------------------------------------------------------
    payload                      = RCAIDE.Energy.Peripherals.Payload()
    payload.power_draw           = 50. * Units.watts 
    payload.mass_properties.mass = 5.0 * Units.kg
    bus.payload                  = payload
    
    #------------------------------------------------------------------------------------------------------------------------------------  
    # Avionics
    #------------------------------------------------------------------------------------------------------------------------------------  
    avionics            = RCAIDE.Energy.Peripherals.Avionics()
    avionics.power_draw = 50. * Units.watts
    bus.avionics        = avionics     

    # append propulsor to distribution line 
    bus.propulsors.append(propulsor)     
    
    # append bus   
    net.busses.append(bus)
        
    # add the solar network to the vehicle
    vehicle.append_energy_network(net)      

    # define weights analysis
    vehicle.weight_breakdown = empty(vehicle)
    
    return vehicle

# ----------------------------------------------------------------------
#   Define the Configurations
# ---------------------------------------------------------------------

def configs_setup(vehicle):
    
    # ------------------------------------------------------------------
    #   Initialize Configurations
    # ------------------------------------------------------------------
    
    configs    = RCAIDE.Components.Configs.Config.Container() 
    config     = RCAIDE.Components.Configs.Config(vehicle)
    config.tag = 'base' 
    config.networks.solar.busses.bus.active_propulsor_groups = ['propulsor']      
    configs.append(config) 
    
    return configs