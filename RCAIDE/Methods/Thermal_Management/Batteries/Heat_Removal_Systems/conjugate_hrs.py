
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports   

# python packaged 
import numpy as np
from scipy.optimize import minimize

def design_conjugate_cooling_heat_removal_system(hrs,battery,inlet_coolant_temperature = 278 ,T_bat = 315, Q_gen = 5000):
    
    # solve for mass flow rate in the channel    
    opt_params = size_conjugate_cooling(hrs,battery,inlet_coolant_temperature,T_bat,Q_gen)
        
    hrs.coolant_flowrate             = opt_params[0]
    hrs.channel_side_thickness       = opt_params[1]        
    hrs.channel_width                = opt_params[2]       
    hrs.channel_contact_angle        = opt_params[3]
    return  

def size_conjugate_cooling(hrs,battery,inlet_coolant_temperature,T_bat, Q_gen, m_coolant_lower_bound=0.0001, m_coolant_upper_bound=10.0, theta_lowerbound=0.1, theta_uperbound=47.5 ): 
    
    # Inital Mass Flow Rate
    mass_flow_rate = hrs.coolant_flow_rate
    
    # Inital Channel Geometric Properties    
    b        = hrs.channel_side_thickness                           
    d        = hrs.channel_width                        
    c        = battery.cell.height       
    a        = hrs.channel_top_thickness
    
    theta    = hrs.channel_contact_angle    
    
    arguments = (hrs,battery,inlet_coolant_temperature,T_bat, Q_gen)
    
    cons     = [{'type':'ineq', 'fun': constraint_2,'args': arguments}] 
    #{'type':'eq', 'fun': constraint_1,'args': arguments},
    initials = [mass_flow_rate, b, d, theta]
    
    bnds     = [(m_coolant_lower_bound, m_coolant_upper_bound), (0.5*b,1.5*b), (0.5*d,1.5*d),(theta_lowerbound, theta_uperbound )]

    sol = minimize(objective,initials , args=arguments , method='SLSQP', bounds=bnds, tol=1e-6, constraints= cons) 
    
    if sol.success == False:
        print('Heat Removal System Sizing Failed ')
    return sol.x   


# objective function
def objective(x,hrs,battery,inlet_coolant_temperature,T_bat,Q_gen) : 
    
    # Mass flow rate 
    m_coolant = x[0] 
    
    # Gemotric variables 
    b        = x[1]               
    d        = x[2]               
    theta    = x[3]  
    c        = battery.cell.height 
    a        = hrs.channel_top_thickness
    
    # Battery 
    d_cell    = battery.cell.diameter                    
    h_cell    = battery.cell.height                      
    A_cell    = np.pi*d_cell*h_cell                      
    N_battery = battery.pack.electrical_configuration.total
     
            
    coolant  = hrs.coolant
    AR       = d/c    
    T_i      = inlet_coolant_temperature 
    n_pump   = 0.7
  
    # Channel Properties 
    channel_density= hrs.channel_density
    
    #Length of Channel 
    L_extra  = 4*d_cell             # Assumption made by Zhao et al. 
    L_chan   = N_battery*theta*np.pi*(d_cell+b+0.5*d)+L_extra

    # Hydraullic diameter    
    dh = (4*c*d)/(2*(c+d))   
 
    # Thermophysical Properties of Coolant  
    rho  = coolant.density
    mu   = coolant.compute_absolute_viscosity(T_i)  
    
    # COMPUTE POWER  Q_convec  
    
    #calculate the velocity of the fluid in the channel 
    v=rho*c*d*m_coolant
    
    # calculate the Reynolds Number 
    Re=(rho*dh*v)/mu
    
    # fanning friction factor (eq 32)
    if Re< 2300:
        f= 24*(1-(1.3553*AR)+(1.9467*AR**2)-(1.7012*AR**3)+(0.9564*AR**4)-(0.2537*AR**5))
    elif Re>=2300:
        f= (0.0791*(Re**(-0.25)))*(1.8075-0.1125*AR)
        
    # Calculate the pressure drop in the channel 
    dp     = 2*f*rho*v*v*L_chan/dh
    
    # Calculate the Power consumed
    Power   = m_coolant*dp/(n_pump*rho)
 
    # Mass calculations - Channel  
    rho_line        = channel_density*(2*a*((2*b)+d)+(2*b*c))
    mass_channel    = rho_line*L_chan
    
    # Mass calculations - Liquid 
    mass_liquid     = rho*c*d
    
    mass_heat_removal_system = mass_channel+mass_liquid
    
    return  Power 


# hard efficiency constraint
def constraint_1( x,hrs,battery,inlet_coolant_temperature,T_bat,Q_gen): 
    # Battery 
    d_cell    = battery.cell.diameter                    
    h_cell    = battery.cell.height                      
    A_cell    = np.pi*d_cell*h_cell                      
    N_battery = battery.pack.electrical_configuration.total
    
    # Mass Flow Rate Variable
    m_coolant = x[0] 

    #include gemotric variables 
    b        = x[1]               
    d        = x[2]               
    theta    = x[3]  
    c        = h_cell
        
    # Inital Channel Geometric Properties    
      
    k_chan   = hrs.channel_thermal_conductivity                  
    coolant  = hrs.coolant
    AR       = d/c    
    T_i      = inlet_coolant_temperature 

    # Surface area of the channel 
    A_chan = N_battery*theta*A_cell/360

    # Hydraullic diameter    
    dh = (4*c*d)/(2*(c+d))   

    # Thermophysical Properties of Coolant  
    rho  = coolant.density
    mu   = coolant.compute_absolute_viscosity(T_i)  
    cp   = coolant.compute_cp(T_i)
    Pr   = coolant.compute_prandtl_number(T_i) 
    k    = coolant.compute_thermal_conductivity(T_i) 

    #calculate the velocity of the fluid in the channel 
    v=rho*c*d*m_coolant

    # calculate the Reynolds Number 
    Re=(rho*dh*v)/mu

    # fanning friction factor (eq 32)
    if Re< 2300:
        f= 24*(1-(1.3553*AR)+(1.9467*AR**2)-(1.7012*AR**3)+(0.9564*AR**4)-(0.2537*AR**5))
    elif Re>=2300:
        f= (0.0791*(Re**(-0.25)))*(1.8075-0.1125*AR)

    # Nusselt Number (eq 12)   
    if Re< 2300:
        Nu= 8.235*(1-(2.0421*AR)+(3.0853*AR**2)-(2.4765*AR**3)+(1.0578*AR**4)-(0.1861*AR**5))    
    elif Re >= 2300:
        Nu = ((f/2)*(Re-1000)*Pr)/(1+(12.7*(f**0.5)*(Pr**(2/3)-1)))   

    # heat transfer coefficient of the channeled coolant (eq 11)
    h = k*Nu/dh

    # Overall Heat Transfer Coefficient from battery surface to the coolant fluid (eq 10)
    U_total = 1/((1/h)+(b/k_chan))

    # Calculate NTU
    NTU = U_total*A_chan/(m_coolant*cp)

    # Calculate Outlet Temparture To ( eq 8)
    T_o = ((T_bat-T_i)*(1-np.exp(-NTU)))+T_i

    # Calculate the Log mean temperature 
    T_lm = ((T_bat-T_i)-(T_bat-T_o))/(np.log((T_bat-T_i)/(T_bat-T_o)))

    # Calculated Heat Convected 
    Q_conv = U_total*A_chan*T_lm 

    # Residuals 
    Heat_Residual = Q_gen - Q_conv    
    
    return Heat_Residual

def constraint_2( x,hrs,battery,inlet_coolant_temperature,T_bat,Q_gen,T_threshold=380): 
   
    # Battery 
    d_cell            = battery.cell.diameter                    
    h_cell            = battery.cell.height                      
    A_cell            = np.pi*d_cell*h_cell                      
    N_battery         = battery.pack.electrical_configuration.total
    Cp_batery         = battery.cell.specific_heat_capacity 
    mass_battery      = battery.cell.mass    
    N_battery_series  = battery.pack.electrical_configuration.series 
    N_battery_parllel = battery.pack.electrical_configuration.parallel

    # Mass Flow Rate Variable
    m_coolant = x[0] 

    #include gemotric variables 
    b        = x[1]               
    d        = x[2]               
    theta    = x[3]  
    c        = h_cell
        
    # Inital Channel Geometric Properties    
      
    k_chan   = hrs.channel_thermal_conductivity                   # Conductivity of the Channel (Replace with function)    
    coolant  = hrs.coolant
    AR       = d/c    
    T_i      = inlet_coolant_temperature 

    # Surface area of the channel 
    A_chan = N_battery*theta*A_cell/360

    # Hydraullic diameter    
    dh = (4*c*d)/(2*(c+d))   

    # Thermophysical Properties of Coolant  
    rho  = coolant.density
    mu   = coolant.compute_absolute_viscosity(T_i)  
    cp   = coolant.compute_cp(T_i)
    Pr   = coolant.compute_prandtl_number(T_i) 
    k    = coolant.compute_thermal_conductivity(T_i) 

    #calculate the velocity of the fluid in the channel 
    v=rho*c*d*m_coolant

    # calculate the Reynolds Number 
    Re=(rho*dh*v)/mu

    # fanning friction factor (eq 32)
    if Re< 2300:
        f= 24*(1-(1.3553*AR)+(1.9467*AR**2)-(1.7012*AR**3)+(0.9564*AR**4)-(0.2537*AR**5))
    elif Re>=2300:
        f= (0.0791*(Re**(-0.25)))*(1.8075-0.1125*AR)

    # Nusselt Number (eq 12)   
    if Re< 2300:
        Nu= 8.235*(1-(2.0421*AR)+(3.0853*AR**2)-(2.4765*AR**3)+(1.0578*AR**4)-(0.1861*AR**5))    
    elif Re >= 2300:
        Nu = ((f/2)*(Re-1000)*Pr)/(1+(12.7*(f**0.5)*(Pr**(2/3)-1)))   

    # heat transfer coefficient of the channeled coolant (eq 11)
    h = k*Nu/dh

    # Overall Heat Transfer Coefficient from battery surface to the coolant fluid (eq 10)
    U_total = 1/((1/h)+(b/k_chan))

    # Calculate NTU
    NTU = U_total*A_chan/(m_coolant*cp)

    # Calculate Outlet Temparture To ( eq 8)
    T_o = ((T_bat-T_i)*(1-np.exp(-NTU)))+T_i

    # Calculate the Log mean temperature 
    T_lm = ((T_bat-T_i)-(T_bat-T_o))/(np.log((T_bat-T_i)/(T_bat-T_o)))

    # Calculated Heat Convected 
    Q_conv = U_total*A_chan*T_lm 

    # Net Heat  
    Q_net= Q_gen - Q_conv    
    
    delta_bat   = Q_net/(Cp_batery*mass_battery*N_battery_parllel*N_battery_series)  
    
    T_bat_new= T_bat+delta_bat
    
    return T_threshold-T_bat_new