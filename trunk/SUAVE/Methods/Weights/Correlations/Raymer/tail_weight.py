## @ingroup Methods-Weights-Correlations-Raymer
# tail_weight.py
#
# Created:  May 2020, W. Van Gijseghem
# Modified:

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import numpy as np
from SUAVE.Core import Units

def tail_vertical_Raymer(vehicle, wing):
    """ Calculates vertical tail weight based on Raymer method

        Assumptions:

        Source:
            Aircraft Design: A Conceptual Approach

        Inputs:
            vehicle - data dictionary with vehicle properties                    [dimensionless]
            wing    - data dictionary with specific tail properties              [dimensionless]

        Outputs:
              tail_weight: vertical tail weight                                [kilograms]

        Properties Used:
            N/A
    """
    H = 0
    if wing.t_tail:
        H = 1
    DG = vehicle.mass_properties.max_takeoff / Units.lbs
    Lt = (wing.origin[0] + wing.aerodynamic_center[0] - vehicle.wings['main_wing'].origin[0] -
          vehicle.wings['main_wing'].aerodynamic_center[0]) / Units.ft
    Svt = wing.areas.reference / Units.ft ** 2
    Kz = Lt
    sweep = wing.sweeps.quarter_chord
    Av = wing.aspect_ratio
    t_c = wing.thickness_to_chord
    tail_weight = 0.0026 * (1 + H) ** 0.225 * DG ** 0.556 * vehicle.envelope.ultimate_load ** 0.536 \
                  * Lt ** (-0.5) * Svt ** 0.5 * Kz ** 0.875 * np.cos(sweep) ** (-1) * Av ** 0.35 * t_c ** (-0.5)
    return tail_weight * Units.lbs


def tail_horizontal_Raymer(vehicle, wing, elevator_fraction=0.4):
    """ Calculates horizontal tail weight based on Raymer method

        Assumptions:
            If all-moving horizontal tail, change Kuht to 1.143
        Source:
            Aircraft Design: A Conceptual Approach

        Inputs:
            vehicle - data dictionary with vehicle properties                    [dimensionless]
            wing    - data dictionary with specific tail properties              [dimensionless]
            elevator_fraction - fraction of horizontal tail for elevator = 0.4

        Outputs:
            tail_weight: vertical tail weight                                [kilograms]

        Properties Used:
            N/A
    """
    Kuht    = 1 # not a all-moving unit horizontal tail
    Fw      = vehicle.fuselages['fuselage'].width / Units.ft
    Bh      = wing.spans.projected / Units.ft
    DG      = vehicle.mass_properties.max_takeoff / Units.lbs
    Sht     = wing.areas.reference / Units.ft ** 2
    Lt      = (wing.origin[0] + wing.aerodynamic_center[0] - vehicle.wings['main_wing'].origin[0] -
                vehicle.wings['main_wing'].aerodynamic_center[0]) / Units.ft
    Ky      = 0.3 * Lt
    sweep   = wing.sweeps.quarter_chord
    Ah      = wing.aspect_ratio
    Se      = elevator_fraction * Sht

    tail_weight = 0.0379 * Kuht * (1 + Fw / Bh) ** (-0.25) * DG ** 0.639 *\
                  vehicle.envelope.ultimate_load ** 0.1 * Sht ** 0.75 * Lt ** -1 *\
                  Ky ** 0.704 * np.cos(sweep) ** (-1) * Ah ** 0.166 * (1 + Se / Sht) ** 0.1
    return tail_weight * Units.lbs
