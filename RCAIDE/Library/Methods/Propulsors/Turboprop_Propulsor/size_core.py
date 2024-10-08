## @ingroup Methods-Energy-Propulsors-Turboprop_Propulsor
# RCAIDE/Methods/Energy/Propulsors/Turboprop_Propulsor/size_core.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from RCAIDE.Library.Methods.Propulsors.Turboprop_Propulsor import compute_thrust
# Python package imports
import numpy                                               as np

# ----------------------------------------------------------------------------------------------------------------------
#  size_core
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Energy-Propulsors-Turboshaft_Propulsor 
def size_core(turboprop,turboprop_conditions,conditions):
    """Sizes the core flow for the design condition.

    Assumptions:
    Perfect gas
    Turboshaft engine with free power turbine

    Sources:
    [1] 

    Inputs:
    conditions.freestream.speed_of_sound [m/s] (conditions is also passed to turboprop.compute(..))
    turboprop.inputs.
      bypass_ratio                            [-]
      total_temperature_reference             [K]
      total_pressure_reference                [Pa]
      number_of_engines                       [-]

    Outputs:
    turboprop.outputs.non_dimensional_power  [-]

    Properties Used:
    turboprop.
      reference_temperature                   [K]
      reference_pressure                      [Pa]
      total_design                            [W] - Design power
    """             
 
    compute_thrust(turboprop,turboprop_conditions,conditions)  
    Fsp                         = turboprop_conditions.non_dimensional_thrust
        
    return    
