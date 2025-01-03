# RCAIDE/Library/Plots/Performance/Aerodynamics/plot_disc_and_power_loading.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Framework.Core import Units
from RCAIDE.Library.Plots.Common import set_axes, plot_style 

# python imports 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------      
def plot_disc_and_power_loading(results,
                            save_figure=False,
                            show_legend = True,
                            save_filename="Disc_And_Power_Loading",
                            file_type = ".png",
                            width = 11, height = 7):
    """Plots rotor disc and power loadings

    Assumptions:
    None

    Source: 
    None
    
    Inputs
    results.segments.conditions.propulsion.
        disc_loadings
        power_loading 

    Outputs:
    Plots

    Properties Used:
    N/A
    """
 
    # get plotting style 
    ps      = plot_style()  

    parameters = {'axes.labelsize': ps.axis_font_size,
                  'xtick.labelsize': ps.axis_font_size,
                  'ytick.labelsize': ps.axis_font_size,
                  'axes.titlesize': ps.title_font_size}
    plt.rcParams.update(parameters)
     
    # get line colors for plots 
    line_colors   = cm.inferno(np.linspace(0,0.9,len(results.segments)))    
    
    fig = plt.figure(save_filename)
    fig.set_size_inches(width,height)  
    axis_1 = plt.subplot(2,1,1)
    axis_2 = plt.subplot(2,1,2)   
    pi     = 0 
    for network in results.segments[0].analyses.energy.vehicle.networks:   
        for p_i, propulsor in enumerate(network.propulsors):  
            if (p_i == 0) or (network.identical_propulsors == False):    
                plot_propulsor_data(results,propulsor,axis_1,axis_2,line_colors,ps,pi) 
              
    if show_legend:             
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 4) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig.tight_layout()
    fig.subplots_adjust(top=0.8) 
    
    # set title of plot 
    title_text  =  'Disc and Power Loading' 
    fig.suptitle(title_text)
    if save_figure:
        plt.savefig(save_filename + file_type)  
        
    return fig 

def plot_propulsor_data(results,propulsor,axis_1,axis_2,line_colors,ps,pi):
    if 'rotor' in  propulsor:
        thrustor =  propulsor.rotor
    elif 'propeller' in  propulsor:
        thrustor =  propulsor.propeller

    for i in range(len(results.segments)): 
        bus_results  = results.segments[i].conditions.energy
        time         = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min    
        DL           = bus_results[propulsor.tag][thrustor.tag].disc_loading[:,0]
        PL           = bus_results[propulsor.tag][thrustor.tag].power_loading[:,0]   
        if pi == 0 and i ==0: 
            axis_1.plot(time,DL, color = line_colors[i], marker = ps.markers[pi], linewidth = ps.line_width, label = thrustor.tag) 
        else:
            axis_1.plot(time,DL, color = line_colors[i], marker = ps.markers[pi], linewidth = ps.line_width) 
    
        axis_1.set_ylabel(r'Disc Loading (N/m^2)')
        set_axes(axis_1)    
        
        axis_2.plot(time,PL, color = line_colors[i], marker = ps.markers[pi], linewidth = ps.line_width)
        axis_2.set_xlabel('Time (mins)')
        axis_2.set_ylabel(r'Power Loading (N/W)')
        set_axes(axis_2)   
    return 