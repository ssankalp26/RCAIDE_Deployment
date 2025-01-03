#  RCAIDE/Library/Methods/Emissions/Chemical_Reactor_Network_Method/train_CRN_EI_surrogates.py
#  
#  Created: 2024, M. Clarke, M. Guidotti

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
import RCAIDE 
from RCAIDE.Library.Methods.Emissions.Chemical_Reactor_Network_Method.evaluate_cantera import evaluate_cantera 

# package imports    
import numpy    as np  

# ----------------------------------------------------------------------------------------------------------------------
#  Train Cantera Model 
# ----------------------------------------------------------------------------------------------------------------------
def train_CRN_EI_surrogates(emissions): 
    """
    Generates training data for emission index surrogate models using Chemical Reactor Network simulations.

    Parameters
    ----------
    emissions : Data
        Container for emissions data and settings
        
        - training : Data
            Training data container

            - pressure : ndarray
                Array of pressure values to evaluate [Pa]
            - temperature : ndarray
                Array of temperature values to evaluate [K]
            - air_mass_flowrate : ndarray
                Array of air mass flow rates to evaluate [kg/s]
            - fuel_to_air_ratio : ndarray
                Array of fuel-to-air ratios to evaluate [-]
        
        - vehicle : Data
            Vehicle configuration data

            - networks : list
                List of propulsion system networks

                - propulsors : list
                    Propulsion units containing combustors

    Returns
    -------
    Updates emissions.training with:

    EI_CO2 : ndarray
        CO2 emission index training data [kg_CO2/kg_fuel]
    EI_CO : ndarray
        CO emission index training data [kg_CO/kg_fuel]
    EI_H2O : ndarray
        H2O emission index training data [kg_H2O/kg_fuel]
    EI_NO : ndarray
        NO emission index training data [kg_NO/kg_fuel]
    EI_NO2 : ndarray
        NO2 emission index training data [kg_NO2/kg_fuel]

    Notes
    -----
    This function evaluates emission indices across a grid of operating conditions
    to generate training data for surrogate models. The grid is formed by the
    combinations of the input arrays (pressure, temperature, mass flow, and
    fuel-to-air ratio).

    **Extra modules required:**

    * numpy
    * Cantera 

    **Major Assumptions**

    * Operating points form a regular grid
    * All combinations of input parameters are valid

    **Theory**
    Training data is generated by:

    1. Creating a grid of operating points
    2. Evaluating detailed chemical kinetics at each point
    3. Storing resulting emission indices in 4D arrays
    
    The grid dimensions are:
    :math:`[P] × [T] × [\dot{m}] × [FAR]`

    Where:

    * :math:`P` = Pressure points
    * :math:`T` = Temperature points
    * :math:`\dot{m}` = Mass flow rate points
    * :math:`FAR` = Fuel-to-air ratio points

    See Also
    --------
    RCAIDE.Library.Methods.Emissions.Chemical_Reactor_Network_Method.evaluate_cantera 
    RCAIDE.Library.Methods.Emissions.Chemical_Reactor_Network_Method.build_CRN_EI_surrogates
    RCAIDE.Library.Methods.Emissions.Chemical_Reactor_Network_Method.evaluate_CRN_emission_indices

    References
    ----------
    [1] Goodwin, D. G., Speth, R. L., Moffat, H. K., & Weber, B. W. (2023). Cantera: An object-oriented software toolkit for chemical kinetics,thermodynamics, and transport processes (Version 3.0.0) [Computer software]. https://www.cantera.org
    """
    # unpack data 
    P              = emissions.training.pressure         
    T              = emissions.training.temperature      
    mdot           = emissions.training.air_mass_flowrate
    FAR            = emissions.training.fuel_to_air_ratio
    
    vehicle        = emissions.vehicle
    for network in vehicle.networks:   
        for propulsor in  network.propulsors:
            if  isinstance(propulsor,RCAIDE.Library.Components.Propulsors.Turbofan) or \
                isinstance(propulsor,RCAIDE.Library.Components.Propulsors.Turbojet) or \
                isinstance(propulsor,RCAIDE.Library.Components.Propulsors.Turboshaft) or \
                isinstance(propulsor,RCAIDE.Library.Components.Propulsors.ICE_Propeller):            
                combustor = propulsor.combustor              
            else:
                combustor = False 
            
    len_P    = len(P)
    len_T    = len(T)
    len_mdot = len(mdot)
    len_far  = len(FAR) 
    
    EI_CO2 = np.zeros((len_P,len_T,len_mdot,len_far))
    EI_CO  = np.zeros((len_P,len_T,len_mdot,len_far))
    EI_H2O = np.zeros((len_P,len_T,len_mdot,len_far))
    EI_NO2 = np.zeros((len_P,len_T,len_mdot,len_far))
    EI_NO  = np.zeros((len_P,len_T,len_mdot,len_far))  
    
    if combustor == False:
        emissions.no_combustor = True
        return 
    
    for p_i in range(len_P):
        for t_i in range(len_T):
            for mdot_i in  range(len_mdot):
                for far_i in  range(len_far):
                    
                    # Call cantera 
                    results = evaluate_cantera(combustor,T[t_i],P[p_i],mdot[mdot_i],FAR[far_i]) 
                    
                    EI_CO2[p_i, t_i, mdot_i,far_i] = results.EI_CO2
                    EI_CO [p_i, t_i, mdot_i,far_i] = results.EI_CO 
                    EI_H2O[p_i, t_i, mdot_i,far_i] = results.EI_H2O
                    EI_NO [p_i, t_i, mdot_i,far_i] = results.EI_NO 
                    EI_NO2[p_i, t_i, mdot_i,far_i] = results.EI_NO2
    
    emissions.training.EI_CO2 = EI_CO2
    emissions.training.EI_CO =  EI_CO
    emissions.training.EI_H2O = EI_H2O
    emissions.training.EI_NO =  EI_NO
    emissions.training.EI_NO2 = EI_NO2
    
    return 