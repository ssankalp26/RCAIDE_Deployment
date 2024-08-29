# RCAIDE/Library/Methods/Stability/Moment_of_Inertia/compute_cubiod_moment_of_inertia.py 
# 
# Created:  Dec 2023, M. Clarke  
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE 
import RCAIDE
from RCAIDE.Framework.Core import Units 

# package imports 
import numpy as np 


# ----------------------------------------------------------------------------------------------------------------------
#  Compute Cuboid Moment of Intertia
# ----------------------------------------------------------------------------------------------------------------------   
def compute_cubiod_moment_of_inertia(origin,mass,length,width,height,inner_length=0,inner_width=0,inner_height=0,center_of_gravity=[[0,0,0]]):  
    I_total = np.zeros((3, 3)) 

    return I_total 