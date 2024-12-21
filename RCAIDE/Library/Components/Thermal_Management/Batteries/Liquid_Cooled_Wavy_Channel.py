# RCAIDE/Library/Components/Thermal_Management/Batteries/Liquid_Cooled_Wavy_Channel.py
# 
# Created:  Apr 2024 S. Shekar 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Framework.Core                                                          import Units
from RCAIDE.Library.Attributes.Coolants.Glycol_Water                                import Glycol_Water
from RCAIDE.Library.Components.Component                                            import Component  
from RCAIDE.Library.Attributes.Materials.Aluminum                                   import Aluminum
from RCAIDE.Library.Components                                                      import Component
from RCAIDE.Library.Components.Component                                            import Container
from RCAIDE.Library.Methods.Thermal_Management.Batteries.Liquid_Cooled_Wavy_Channel import  wavy_channel_rating_model,append_wavy_channel_conditions,append_wavy_channel_segment_conditions 
from RCAIDE.Library.Plots.Thermal_Management                                        import plot_wavy_channel_conditions

# ----------------------------------------------------------------------------------------------------------------------
# Liquid_Cooled_Wavy_Channel
# ----------------------------------------------------------------------------------------------------------------------
class Liquid_Cooled_Wavy_Channel(Component):
    """
    A class representing a liquid cooling system using wavy channels for enhanced heat 
    transfer in battery thermal management.

    Attributes
    ----------
    tag : str
        Unique identifier for the cooling system, defaults to 'wavy_channel_heat_acquisition'
        
    heat_transfer_efficiency : float
        Overall efficiency of the heat transfer process, defaults to 1.0
        
    coolant : Glycol_Water
        Coolant properties for calculations, defaults to Glycol_Water()
        
    coolant_Reynolds_number : float
        Reynolds number of the coolant flow, defaults to 1.0
        
    coolant_velocity : float
        Velocity of coolant in channels, defaults to 1.0
        
    coolant_flow_rate : float
        Volume flow rate of coolant, defaults to 1.0
        
    coolant_inlet_temperature : float
        Temperature of coolant entering the system, defaults to None
        
    coolant_hydraulic_diameter : float
        Hydraulic diameter of cooling channels, defaults to 1.0
        
    channel_side_thickness : float
        Thickness of channel walls for conduction, defaults to 0.001
        
    channel_top_thickness : float
        Thickness of non-conducting channel top, defaults to 0.001
        
    channel_width : float
        Width of cooling channels, defaults to 0.005
        
    channel_height : float
        Height of cooling channels, defaults to 0.003
        
    channel_contact_angle : float
        Contact arc angle, defaults to 47.5 degrees
        
    channel : Aluminum
        Channel material properties, defaults to Aluminum()
        
    channel_aspect_ratio : float
        Ratio of channel height to width, defaults to 1.0
        
    channels_per_module : float
        Number of cooling channels per battery module, defaults to 1
        
    battery_contact_area : float
        Total contact area with battery, defaults to 1.0
        
    contact_area_per_module : float
        Contact area per battery module, defaults to 1.0
        
    power_draw : float
        Power consumption of the cooling system, defaults to 1.0
        
    single_side_contact : bool
        Flag for single-sided cooling contact, defaults to True
        
    design_heat_removed : float
        Design heat removal capacity, defaults to None
        
    percent_operation : float
        Operating capacity percentage, defaults to 1.0
        
    type : str
        Cooling system type identifier, defaults to 'Liquid'

    Notes
    -----
    The wavy channel design enhances heat transfer through:
    
    * Increased surface area for heat exchange
    * Improved mixing and turbulence
    * Optimized coolant flow patterns
    
    **Assumptions:**

    * The wavy channel heat Acquisition loops through the battery pack.
    * The coolant is assumed to be Glycol Water unless specified otherwise. 
    * The geometry parameters are set based on nominal values to be further optmized.
           
    **Definitions**

    'Wavy Channel'
        Cooling channel with sinusoidal path for enhanced heat transfer
        
    'Hydraulic Diameter'
        Characteristic dimension for internal flow calculations

    See Also
    --------
    RCAIDE.Library.Components.Thermal_Management.Batteries.Air_Cooled
        Alternative cooling approach using forced air
    RCAIDE.Library.Components.Thermal_Management.Batteries.Cryocooler
        Alternative cooling approach for extreme temperatures
    """

    def __defaults__(self):
        """
        Sets default values for the wavy channel cooling system attributes.
        """
        self.tag                           = 'wavy_channel_heat_acquisition' 
        self.heat_transfer_efficiency      = 1
        self.coolant                       = Glycol_Water()
        self.coolant_Reynolds_number       = 1.
        self.coolant_velocity              = 1.
        self.coolant_flow_rate             = 1
        self.coolant_inlet_temperature     = None
        self.coolant_hydraulic_diameter    = 1.
        self.channel_side_thickness        = 0.001
        self.channel_top_thickness         = 0.001
        self.channel_width                 = 0.005
        self.channel_height                = 0.003
        self.channel_contact_angle         = 47.5 * Units.degrees
        self.channel                       = Aluminum()
        self.channel_aspect_ratio          = 1. 
        self.channels_per_module           = 1
        self.battery_contact_area          = 1.
        self.contact_area_per_module       = 1.  
        self.power_draw                    = 1. 
        self.single_side_contact           = True 
        self.design_heat_removed           = None   
        self.percent_operation             = 1.0
        self.type                          = 'Liquid'
        return
    
    def append_operating_conditions(self, segment, coolant_line):
        """
        Adds operating conditions for the cooling system to a mission segment.

        Parameters
        ----------
        segment : Data
            Mission segment to which conditions are being added
        coolant_line : Data
            Cooling system flow path information
        """
        append_wavy_channel_conditions(self, segment, coolant_line)
        return
    
    def append_segment_conditions(self, segment, coolant_line, conditions):
        """
        Adds specific segment conditions to the cooling system analysis.

        Parameters
        ----------
        segment : Data
            Mission segment being analyzed
        coolant_line : Data
            Cooling system flow path information
        conditions : Data
            Operating conditions for the segment
        """
        append_wavy_channel_segment_conditions(self, segment, coolant_line, conditions)
        return
    
    def compute_thermal_performance(self, battery, bus, coolant_line, Q_heat_gen, T_cell, state, delta_t, t_idx):
        """
        Calculates thermal performance of the wavy channel cooling system.

        Parameters
        ----------
        battery : Data
            Battery pack information
        bus : Data
            Electrical bus data
        coolant_line : Data
            Cooling system flow path information
        Q_heat_gen : float
            Heat generation rate
        T_cell : float
            Current cell temperature
        state : Data
            Current system state
        delta_t : float
            Time step size
        t_idx : int
            Time index in the simulation

        Returns
        -------
        float
            Updated battery temperature
        """
        T_battery_current = wavy_channel_rating_model(self, battery, bus, coolant_line, 
                                                    Q_heat_gen, T_cell, state, delta_t, t_idx)
        return T_battery_current
    
    def plot_operating_conditions(self, results, coolant_line, save_filename, save_figure, 
                                show_legend, file_type, width, height):
        """
        Creates visualization plots of the cooling system operating conditions.

        Parameters
        ----------
        results : Data
            Simulation results data
        coolant_line : Data
            Cooling system flow path information
        save_filename : str
            Path for saving the plot
        save_figure : bool
            Flag to save the figure
        show_legend : bool
            Flag to display plot legend
        file_type : str
            Output file format
        width : float
            Plot width
        height : float
            Plot height
        """
        plot_wavy_channel_conditions(self, results, coolant_line, save_filename, 
                                   save_figure, show_legend, file_type, width, height)
        return