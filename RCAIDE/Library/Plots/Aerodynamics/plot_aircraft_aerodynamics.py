# RCAIDE/Library/Plots/Aerodynamics/plot_aircraft_aerodynamic_analysis.py
# 
# 
# Created:  Dec 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Framework.Core import Units
from RCAIDE.Library.Plots.Common import set_axes, plot_style 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------   
def plot_aircraft_aerodynamics(results,
                            save_figure = False,
                            line_color = 'bo-',
                            line_color2 = 'rs--',
                            save_filename = "Aircraft_Aerodynamic_Analysis",
                            file_type = ".png",
                            width = 11, height = 7):
    

    # get plotting style 
    ps      = plot_style()  

    parameters = {'axes.labelsize': ps.axis_font_size,
                  'xtick.labelsize': ps.axis_font_size,
                  'ytick.labelsize': ps.axis_font_size,
                  'axes.titlesize': ps.title_font_size}
    plt.rcParams.update(parameters)
    
    #------------------------------------------------------------------------
    # setup figures
    #------------------------------------------------------------------------
    fig = plt.figure(save_filename + " Lift Coefficients")  
    fig.set_size_inches(12,6) 
    axis_1 = fig.add_subplot(1, 2, 1, projection='3d')
    axis_2 = fig.add_subplot(1, 2, 2, projection='3d') 
 
    X, Y = np.meshgrid(results.Mach, results.alpha)
    surf = axis_1.plot_surface(X, Y/Units.degree, results.lift_coefficient   , cmap=cm.jet,linewidth=0, antialiased=False) 
    surf = axis_2.plot_surface(X, Y/Units.degree, results.drag_coefficient   , cmap=cm.jet,linewidth=0, antialiased=False) 

    axis_1.set_title('$C_L$') 
    axis_2.set_title('$C_L$')            
    axis_1.set_ylabel('AoA') 
    axis_2.set_ylabel('AoA')  
    axis_1.set_xlabel('Mach') 
    axis_2.set_xlabel('Mach')   
    
    # set title of plot 
    title_text    = 'Aircraft Aerodynamic Analysis '    
    fig.suptitle(title_text) 
    
    plt.tight_layout()    
    if save_figure:    
        fig.savefig(save_filename + file_type) 
    
    plt.tight_layout()
    return
