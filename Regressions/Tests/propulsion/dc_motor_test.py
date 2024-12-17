# motor_test.py
# 
# Created:  M. Clarke, Feb 2020 
#           Mar 2020, M. Clarke
#           Sep 2020, M. Clarke 

#----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import RCAIDE
from Legacy.trunk.S.Core import Units, Data, Container

from Legacy.trunk.S.Core import (
Data, Container,
)
from Legacy.trunk.S.Methods.Propulsion.electric_motor_sizing import size_from_mass , size_optimal_motor
from Legacy.trunk.S.Methods.Propulsion                       import propeller_design
import numpy as np
import copy, time

def main():
    '''This script checks the functions in in Motor.py used to compute motor torques 
    and output voltage and currents'''
    # Propeller 
    prop                         = RCAIDE.Library.Components.Propulsors.Converters.Propeller()
    prop.number_of_blades        = 2.0 
    prop.freestream_velocity     = 50.0
    prop.angular_velocity        = 209.43951023931953
    prop.tip_radius              = 1.5
    prop.hub_radius              = 0.05
    prop.design_Cl               = 0.7 
    prop.design_altitude         = 0.0 * Units.km
    prop.design_thrust           = 2271.2220451593753 

    airfoil                        = RCAIDE.Library.Components.Airfoils.Airfoil()    
    airfoil.coordinate_file        = '../Vehicles/Airfoils/NACA_4412.txt'
    airfoil.polar_files            = ['../Vehicles/Airfoils/Polars/NACA_4412_polar_Re_50000.txt' ,
                                   '../Vehicles/Airfoils/Polars/NACA_4412_polar_Re_100000.txt' ,
                                   '../Vehicles/Airfoils/Polars/NACA_4412_polar_Re_200000.txt' ,
                                   '../Vehicles/Airfoils/Polars/NACA_4412_polar_Re_500000.txt' ,
                                   '../Vehicles/Airfoils/Polars/NACA_4412_polar_Re_1000000.txt' ] 
    prop.append_airfoil(airfoil) 
    prop.airfoil_polar_stations    = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    prop                           = propeller_design(prop)    
    
    # Motor
    #------------------------------------------------------------------
    # Design Motors
    #------------------------------------------------------------------
    # Propeller (Thrust) motor
    motor                      = RCAIDE.Library.Components.Propulsors.Converters.DC_Motor()
    motor.mass_properties.mass = 9. * Units.kg 
    motor.efficiency           = 0.935
    motor.gear_ratio           = 1. 
    motor.gearbox_efficiency   = 1. # Gear box efficiency     
    motor.no_load_current      = 2.0 
    motor.propeller_radius     = prop.tip_radius
    motor.nominal_voltage      = 400
    motor                      = size_optimal_motor(motor,prop)  
   
    
    # Find the operating conditions
    atmosphere = RCAIDE.Library.Attributes.Atmospheres.Earth.US_Standard_1976()
    atmosphere_conditions =  atmosphere.compute_values(prop.design_altitude) 
    V  = prop.freestream_velocity
    conditions = Data()
    conditions.freestream                               = Data()
    conditions.propulsion                               = Data()
    conditions.frames                                   = Data()
    conditions.frames.body                              = Data()
    conditions.frames.inertial                          = Data()
    conditions.freestream.update(atmosphere_conditions)
    conditions.freestream.dynamic_viscosity             = atmosphere_conditions.dynamic_viscosity
    conditions.freestream.velocity                      = np.array([[V,0,0]])
    conditions.propulsion.throttle                      = np.array([[1.0]])
    conditions.frames.body.transform_to_inertial        = np.array([np.eye(3)]) 
    conditions.propulsion.propeller_power_coefficient   = np.array([[0.02]]) 
    
    #------------------------------------
    # Motor Omega Function  
    #------------------------------------
    # create copy of motor to test functions 
    motor_1 = motor    
    
    # Define function specific inputs 
    voltage_1 =  400
    motor_1.inputs.voltage      = np.array([[voltage_1]]) 
    motor_1.inputs.propeller_CP = conditions.propulsion.propeller_power_coefficient
    
    # Run Motor Omega Function 
    omega_1  = motor_1.omega(conditions)   
    torque_1 = motor_1.outputs.torque[0][0] 
    
    #------------------------------------
    # Motor Current Function 
    #------------------------------------
    # create copy of motor to test functions 
    motor_2 = motor    
    
    # Define function specific inputs  
    motor_2.inputs.voltage = np.array([[voltage_1]])
    motor_2.outputs.omega  = np.array([[prop.angular_velocity]])
    
    # Run Motor Current Function 
    i, etam = motor_2.current(conditions) 
    current_2 = i[0][0]
    
    #------------------------------------
    # Motor Torque Function 
    #------------------------------------    
    # create copy of motor to test functions  
    motor_3  = motor      
    
    # Define function specific inputs  
    motor_3.inputs.voltage = np.array([[voltage_1]]) 
    motor_3.inputs.omega  = np.array([[prop.angular_velocity]])   
    
    # Run Motor Torque Function 
    motor_3.torque(conditions)
    torque_3 = motor_3.outputs.torque[0][0] 
    
    #------------------------------------
    # Motor Voltage-Current Function 
    #------------------------------------    
    # create copy of motor to test functions   
    motor_4  = motor     
    
    # Define function specific inputs    
    motor_4.inputs.torque = np.array([[torque_1]])
    
    # Run Motor Voltage-Current Function 
    motor_4.voltage_current(conditions) 
    voltage_4 = motor_4.outputs.voltage[0][0]
    current_4 = motor_4.outputs.current[0][0]
    
    #------------------------------------
    # Low Fidelity Motor  
    #------------------------------------     
     
    # Truth values
    omega_1_truth    = 197.31166405767365
    torque_1_truth   = 934.4117082048164
    current_2_truth  = 572.2006877833089
    torque_3_truth   = 803.2247688894328
    voltage_4_truth  = 417.0841366120573
    current_4_truth  = 665.3288953823401 
  
    error = Data()
    error.omega_test     = np.max(np.abs(omega_1_truth   - omega_1[0][0]  ))
    error.torque_test_1  = np.max(np.abs(torque_1_truth  - torque_1 ))
    error.current_test_1 = np.max(np.abs(current_2_truth - current_2))
    error.torque_test_2  = np.max(np.abs(torque_3_truth  - torque_3 ))
    error.voltage_test   = np.max(np.abs(voltage_4_truth - voltage_4))
    error.current_test_2 = np.max(np.abs(current_4_truth - current_4)) 
    
    print('Errors:')
    print(error)
    
    for k,v in list(error.items()):
        assert(np.abs(v)<1e-6)
     
    return

# ----------------------------------------------------------------------        
#   Call Main
# ----------------------------------------------------------------------    

if __name__ == '__main__':
    main()