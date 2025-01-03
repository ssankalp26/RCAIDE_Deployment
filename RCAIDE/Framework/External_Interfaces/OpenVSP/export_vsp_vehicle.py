# RCAIDE/Framework/External_Interfaces/OpenVSP/export_vsp_vehicle.py
# 
# Created:  Jul 2016, T. MacDonald
# Modified: Jun 2017, T. MacDonald
#           Jul 2017, T. MacDonald
#           Oct 2018, T. MacDonald
#           Nov 2018, T. MacDonald
#           Jan 2019, T. MacDonald
#           Jan 2020, T. MacDonald 
#           Mar 2020, M. Clarke
#           May 2020, E. Botero
#           Jul 2020, E. Botero 
#           Feb 2021, T. MacDonald
#           May 2021, E. Botero 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports 
import RCAIDE
from RCAIDE.Framework.Core import Units, Data 
from RCAIDE.Framework.External_Interfaces.OpenVSP.vsp_rotor     import write_vsp_rotor_bem
from RCAIDE.Framework.External_Interfaces.OpenVSP.vsp_fuselage  import write_vsp_fuselage
from RCAIDE.Framework.External_Interfaces.OpenVSP.vsp_wing      import write_vsp_wing
from RCAIDE.Framework.External_Interfaces.OpenVSP.vsp_nacelle   import write_vsp_nacelle 
try:
    import vsp as vsp
except ImportError:
    try:
        import openvsp as vsp
    except ImportError:
        # This allows RCAIDE to build without OpenVSP
        pass
import numpy as np
import os

# ---------------------------------------------------------------------------------------------------------------------- 
# export_vsp_vehicle
# ---------------------------------------------------------------------------------------------------------------------- 
def export_vsp_vehicle(vehicle, vehicle_tag, fuel_tank_set_ind=3, verbose=True, write_file=True, OML_set_ind = 4, write_igs = False):
    """This writes a RCAIDE vehicle to OpenVSP format. It will take wing segments into account
    if they are specified in the vehicle setup file.
    
    Assumptions:
    Vehicle is composed of conventional shape fuselages, wings, and networks. Any network
    that should be created is tagged as 'turbofan'.

    Source:
    N/A

    Inputs:
    vehicle.
      tag                                       [-]
      wings.*.    (* is all keys)
        origin                                  [m] in all three dimensions
        spans.projected                         [m]
        chords.root                             [m]
        chords.tip                              [m]
        sweeps.quarter_chord                    [radians]
        twists.root                             [radians]
        twists.tip                              [radians]
        thickness_to_chord                      [-]
        dihedral                                [radians]
        tag                                     <string>
        Segments.*. (optional)
          twist                                 [radians]
          percent_span_location                 [-]  .1 is 10%
          root_chord_percent                    [-]  .1 is 10%
          dihedral_outboard                     [radians]
          sweeps.quarter_chord                  [radians]
          thickness_to_chord                    [-]
      networks.turbofan. (optional)
        number_of_engines                       [-]
        nacelle_diameter                        [m]
        origin                                  [m] in all three dimension, should have as many origins as engines
        OpenVSP_simple (optional)               <boolean> if False (default) create a flow through nacelle, if True creates a roughly biparabolic shape
      fuselages.fuselage (optional)
        width                                   [m]
        lengths.total                           [m]
        heights.
          maximum                               [m]
          at_quarter_length                     [m]
          at_wing_root_quarter_chord            [m]
          at_three_quarters_length              [m]
        effective_diameter                      [m]
        fineness.nose                           [-] ratio of nose section length to fuselage width
        fineness.tail                           [-] ratio of tail section length to fuselage width
        tag                                     <string>
        OpenVSP_values.  (optional)
          nose.top.angle                        [degrees]
          nose.top.strength                     [-] this determines how much the specified angle influences that shape
          nose.side.angle                       [degrees]
          nose.side.strength                    [-]
          nose.TB_Sym                           <boolean> determines if top angle is mirrored on bottom
          nose.z_pos                            [-] z position of the nose as a percentage of fuselage length (.1 is 10%)
          tail.top.angle                        [degrees]
          tail.top.strength                     [-]
          tail.z_pos (optional, 0.02 default)   [-] z position of the tail as a percentage of fuselage length (.1 is 10%)
    fuel_tank_set_index                         <int> OpenVSP object set containing the fuel tanks    

    Outputs:
    <tag>.vsp3           This is the OpenVSP representation of the aircraft

    Properties Used:
    N/A
    """    

    # -------------------------------------------------------------------------     
    # Reset OpenVSP to avoid including a previous vehicle
    # ------------------------------------------------------------------------- 
    if verbose:
        print('Reseting OpenVSP Model in Memory')
    try:
        vsp.ClearVSPModel()
    except NameError:
        print('VSP import failed')
        return -1
    
    area_tags = dict() # for wetted area assignment
    
    # ------------------------------------------------------------------------- 
    # Wings
    # -------------------------------------------------------------------------  
    # Default Set_0 in OpenVSP is index 3
    vsp.SetSetName(fuel_tank_set_ind, 'fuel_tanks')
    vsp.SetSetName(OML_set_ind, 'OML')
    
    for wing in vehicle.wings:       
        if verbose:
            print('Writing '+wing.tag+' to OpenVSP Model')
            area_tags, wing_id = write_vsp_wing(vehicle,wing,area_tags, fuel_tank_set_ind, OML_set_ind) 
    
    # ------------------------------------------------------------------------- 
    # Engines
    # -------------------------------------------------------------------------  
    for network in vehicle.networks: 
        for propulsor in network.propulsors: 
            for  tag ,  item in  propulsor.items():
                if isinstance(item, RCAIDE.Library.Components.Propulsors.Converters.Rotor):
                    vsp_bem_filename = item.tag + '.bem' 
                    write_vsp_rotor_bem(vsp_bem_filename,item) 
   
            if 'nacelle' in propulsor:
                nacelle =  propulsor.nacelle
                if verbose:
                    print('Writing '+ nacelle.tag +' to OpenVSP Model')
                write_vsp_nacelle(nacelle, OML_set_ind)
                     
    # ------------------------------------------------------------------------- 
    # Fuselage
    # ------------------------------------------------------------------------- 
    for fuselage in vehicle.fuselages:
        if type(fuselage) !=  RCAIDE.Library.Components.Fuselages.Blended_Wing_Body_Fuselage: 
            if verbose:
                print('Writing '+fuselage.tag+' to OpenVSP Model')
            try:
                area_tags = write_vsp_fuselage(fuselage, area_tags, vehicle.wings.main_wing, 
                                               fuel_tank_set_ind, OML_set_ind)
            except AttributeError:
                area_tags = write_vsp_fuselage(fuselage, area_tags, None, fuel_tank_set_ind,
                                               OML_set_ind)
        else:
            print('Blended Wing Body Fuselage defined')
    
    vsp.Update()
    

    # ------------------------------------------------------------------------- 
    # Fuselage
    # ------------------------------------------------------------------------- 
    for boom in vehicle.booms: 
        if verbose:
            print('Writing '+boom.tag+' to OpenVSP Model')
        try:
            area_tags = write_vsp_fuselage(boom, area_tags, vehicle.wings.main_wing, 
                                           fuel_tank_set_ind, OML_set_ind)
        except AttributeError:
            area_tags = write_vsp_fuselage(boom, area_tags, None, fuel_tank_set_ind,
                                               OML_set_ind) 
    # -------------------------------------------------------------------------     
    # Write the vehicle to the file    
    # ------------------------------------------------------------------------- 
    if write_file ==True:
        cwd = os.getcwd()
        filename = vehicle_tag + ".vsp3"
        if verbose:
            print('Saving OpenVSP File at '+ cwd + '/' + filename)
        vsp.WriteVSPFile(filename)
    elif verbose:
        print('Not Saving OpenVSP File')
        
    if write_igs:
        if verbose:
            print('Exporting IGS File')        
        vehicle_id = vsp.FindContainersWithName('Vehicle')[0]
        parm_id = vsp.FindParm(vehicle_id,'LabelID','IGESSettings')
        vsp.SetParmVal(parm_id, 0.)
        vsp.ExportFile(vehicle_tag + ".igs", OML_set_ind, vsp.EXPORT_IGES)
    
    return area_tags