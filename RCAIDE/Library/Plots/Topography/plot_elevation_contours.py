# RCAIDE/Library/Plots/Topography/plot_elevation_contours.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Framework.Core                             import Units
from RCAIDE.Framework.Analyses.Geodesics.Geodesics import Calculate_Distance
from RCAIDE.Library.Plots.Common import plot_style

# python imports 
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.colors 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------    
def plot_elevation_contours(topography_file,
                            number_of_latitudinal_points  = 100,
                            number_of_longitudinal_points = 100, 
                            use_lat_long_coordinates      = True, 
                            save_figure = False,  
                            show_legend = True,
                            save_filename = "Elevation_Contours",
                            file_type = ".png",
                            width = 11, height = 7): 
    

    """This plots the elevation contours

    Assumptions:
    None

    Source:
    topography_file

    Inputs:
    vehicle

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
     
     
    colors_undersea = plt.cm.terrain(np.linspace(0, 0.17, 56))
    colors_land     = plt.cm.terrain(np.linspace(0.25, 1, 200)) 
    
    # combine them and build a new colormap
    colors          = np.vstack((colors_undersea, colors_land))
    cut_terrain_map = matplotlib.colors.LinearSegmentedColormap.from_list('cut_terrain', colors) 
    
    data = np.loadtxt(topography_file)
    Long = data[:,0]
    Lat  = data[:,1]
    Elev = data[:,2]    

    x_min_coord = np.min(Lat)
    x_max_coord = np.max(Lat)
    y_min_coord = np.min(Long)
    y_max_coord = np.max(Long)
    if np.min(Long)>180: 
        y_min_coord = np.min(Long)-360
    if np.max(Long)>180:
        y_max_coord = np.max(Long)-360  
    
    top_left_map_coords      = np.array([x_max_coord,y_min_coord])
    bottom_left_map_coords   = np.array([x_min_coord,y_min_coord]) 
    top_right_map_coords     = np.array([x_max_coord,y_max_coord])
    bottom_right_map_coords  = np.array([x_min_coord,y_max_coord]) 
    
    x_dist_max = Calculate_Distance(top_left_map_coords,bottom_left_map_coords) * Units.kilometers
    y_dist_max = Calculate_Distance(bottom_right_map_coords,bottom_left_map_coords) * Units.kilometers
    
    [long_dist,lat_dist]  = np.meshgrid(np.linspace(0,y_dist_max,number_of_longitudinal_points),np.linspace(0,x_dist_max,number_of_latitudinal_points))
    [long_deg,lat_deg]    = np.meshgrid(np.linspace(np.min(Long),np.max(Long),number_of_longitudinal_points),np.linspace(np.min(Lat),np.max(Lat),number_of_latitudinal_points)) 
    elevation             = griddata((Lat,Long), Elev, (lat_deg, long_deg), method='linear')     
    elevation             = elevation/Units.feet
    norm                  = FixPointNormalize(sealevel=0,vmax=np.max(elevation),vmin=np.min(elevation)) 
    
    fig = plt.figure(save_filename)
    fig.set_size_inches(width,height)
    axis = fig.add_subplot(1,1,1) 
    
    if use_lat_long_coordinates:
        CS   = axis.contourf(long_deg,lat_deg,elevation,cmap =cut_terrain_map,norm=norm,levels = 20)   
        cbar = fig.colorbar(CS, ax=axis)     
        cbar.ax.set_ylabel('Elevation above sea level [ft]', rotation =  90)  
        axis.set_xlabel('Longitude [°]')
        axis.set_ylabel('Latitude [°]') 
    else: 
        CS   = axis.contourf(long_dist/Units.nmi,lat_dist/Units.nmi,elevation,cmap =cut_terrain_map,norm=norm,levels = 20)  
        cbar = fig.colorbar(CS, ax=axis)        
        cbar.ax.set_ylabel('Elevation above sea level [ft]', rotation =  90) 
        axis.set_xlabel('Longitudinal Distance [nmi]')
        axis.set_ylabel('Latitudinal Distance [nmi]') 
     
    return  fig   

class FixPointNormalize(matplotlib.colors.Normalize):
    """ 
    Inspired by https://stackoverflow.com/questions/20144529/shifted-colorbar-matplotlib
    Subclassing Normalize to obtain a colormap with a fixpoint 
    somewhere in the middle of the colormap.
    This may be useful for a `terrain` map, to set the "sea level" 
    to a color in the blue/turquise range. 
    """
    def __init__(self, vmin=None, vmax=None, sealevel=0, col_val = 0.21875, clip=False):
        # sealevel is the fix point of the colormap (in data units)
        self.sealevel = sealevel
        # col_val is the color value in the range [0,1] that should represent the sealevel.
        self.col_val = col_val
        matplotlib.colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.sealevel, self.vmax], [0, self.col_val, 1]
        return np.ma.masked_array(np.interp(value, x, y)) 
    
  