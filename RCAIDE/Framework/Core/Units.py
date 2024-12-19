
# RCAIDE/Core/Units.py
# 
# 
# Created:  Dec 2024, Niranjan Nanjappa 


# ----------------------------------------------------------------------------------------------------------------------
#  Container
# ----------------------------------------------------------------------------------------------------------------------   

class Units:
    """ 
    RCAIDE.Core.Units()
    A unit conversion toolbox that works by converting values into and out of the base units.

    Important:
        This does not enforce unit consistency. The user is responsible for ensuring that the 
        units being converted are consistent and meaningful.

    Usage:
        from Units import Units
        a = 4. * Units.mm        # Convert 4 millimeters into meters
        b = a / Units.mm         # Convert back from meters to millimeters
        speed = 10 * Units['m/s']  # Convert 10 m/s into base units (m/s)
    
    Explanation:
        Accessing an attribute of Units (e.g. Units.mm) returns the conversion factor
        to the base unit. For instance, Units.mm = 0.001 means 1 mm = 0.001 m.
        Multiplying by Units.mm converts from millimeters to meters.
        Dividing by Units.mm converts from meters to millimeters.
        Similarly, Units['m/s'] returns the same factor as Units.meter_per_second.
    
    Base Units:
        mass        : kilogram (kg)
        length      : meter (m)
        time        : second (s)
        temperature : Kelvin (K)
        angle       : radian (rad)
        current     : Ampere (A)
        luminous intensity: candela (cd)
        power       : watt (W)
        pressure    : pascal (Pa)
        area        : square meter (m²)
        volume      : cubic meter (m³)
        speed       : meter per second (m/s)

    Note on Temperature:
        Temperature scales involving offsets (°C, °F) cannot be handled by a simple scale factor.
        For such units, handle offsets outside of this tool.
    """

    # Fundamental conversion factors to base units:
    # Length (meter)
    length_conversions = {
        'm': 1.0,
        'km': 1000.0,
        'dm': 0.1,
        'cm': 0.01,
        'mm': 0.001,
        'micrometer': 1e-6,
        'nanometer': 1e-9,
        'inch': 0.0254,
        'foot': 0.3048,
        'yard': 0.9144,
        'mile': 1609.34,
        'nautical_mile': 1852.0
    }

    # Time (second)
    time_conversions = {
        's': 1.0,
        'ms': 0.001,
        'minute': 60.0,
        'hour': 3600.0,
        'day': 86400.0,
        'week': 604800.0,
        'month': 2592000.0,  # 30-day month assumption
        'year': 31536000.0   # 365-day year
    }

    # Mass (kilogram)
    mass_conversions = {
        'kg': 1.0,
        'g': 0.001,
        'mg': 1e-6,
        'metric_ton': 1000.0,
        'pound': 0.453592,
        'lb': 0.453592,
        'lbs': 0.453592,
        'ounce': 0.0283495
    }

    # Angle (radian)
    angle_conversions = {
        'radian': 1.0,
        'degree': 0.0174533
    }

    # Current (Ampere)
    current_conversions = {
        'A': 1.0,
        'mA': 1e-3,
        'µA': 1e-6
    }

    # Luminous intensity (candela)
    luminous_intensity_conversions = {
        'cd': 1.0,
        'mcd': 1e-3
    }

    # Temperature (Kelvin)
    temperature_conversions = {
        'K': 1.0,
        'R': 1.8  # Rankine
    }

    # Area (square meter)
    area_conversions = {
        'square_meter': 1.0,
        'hectare': 10000.0,
        'acre': 4046.86,
        'square_kilometer': (1000.0**2),
        'square_decimeter': (0.1**2),
        'square_centimeter': (0.01**2),
        'square_millimeter': (0.001**2),
        'square_inch': (0.0254**2),
        'square_foot': (0.3048**2),
        'square_yard': (0.9144**2)
    }

    # Volume (cubic meter)
    volume_conversions = {
        'cubic_meter': 1.0,
        'liter': 0.001,
        'deciliter': 0.001/10,
        'centiliter': 0.001/100,
        'milliliter': 0.001/1000,
        'cubic_inch': (0.0254**3),
        'cubic_foot': (0.3048**3),
        'cubic_yard': (0.9144**3),
        'gallon': 0.00378541,
        'quart': 0.00378541/4,
        'pint': 0.00378541/8,
        'fluid_ounce': 0.00378541/128,
        'bushel': 0.0352391,
        'barrel': 0.158987
    }

    # Power (watt)
    power_conversions = {
        'watt': 1.0,
        'kilowatt': 1000.0,
        'btu_per_hour': 0.29307107,
        'horsepower': 745.7
    }

    # Pressure (pascal)
    _LBF_TO_N = 4.44822
    _IN2 = (0.0254**2)
    _FT2 = (0.3048**2)
    pressure_conversions = {
        'pascal': 1.0,
        'atmosphere': 101325.0,
        'bar': 100000.0,
        'millibar': 100.0,
        'megapascal': 1e6,
        'kilopascal': 1000.0,
        'psi': _LBF_TO_N / _IN2,
        'psf': _LBF_TO_N / _FT2
    }

    # Speed (meter per second)
    knot_to_ms = length_conversions['nautical_mile'] / time_conversions['hour']
    mph_to_ms = length_conversions['mile'] / time_conversions['hour']
    fps_to_ms = length_conversions['foot']
    fpm_to_ms = length_conversions['foot'] / time_conversions['minute']
    kms_to_ms = length_conversions['km']  # km/s
    speed_conversions = {
        'meter_per_second': 1.0,
        'mps': 1.0,  # A short form for m/s
        'kilometer_per_second': kms_to_ms,
        'knots': knot_to_ms,
        'mile_per_hour': mph_to_ms,
        'feet_per_second': fps_to_ms,
        'feet_per_minute': fpm_to_ms
    }

    # Force (newton)
    force_conversions = {
        'newton': 1.0,
        'pound_force': _LBF_TO_N
    }

    # Add synonyms or alternative notations
    # For example, 'm/s' as a synonym for 'meter_per_second'
    _synonyms = {
        'm/s': 'meter_per_second',
        'm·s⁻¹': 'meter_per_second',   # Another notation
        'N': 'newton'
    }

    def __init__(self, factor: float):
        self.factor = factor

    def __mul__(self, value):
        # Convert value to base unit
        return value * self.factor

    def __rmul__(self, value):
        # Convert value to base unit (right multiplication)
        return value * self.factor

    def __truediv__(self, value):
        # Convert from base unit to target unit
        return value / self.factor

    @classmethod
    def _create_properties(cls, conversions_dict):
        for unit_name, factor in conversions_dict.items():
            # Create a property for each unit name
            setattr(cls, unit_name, classmethod(property(lambda c, f=factor: c(f))))

    @classmethod
    def __getitem__(cls, key):
        # Lookup the factor in the _all_conversions dictionary
        if key in cls._all_conversions:
            return cls(cls._all_conversions[key])
        # If the key is a synonym, translate and try again
        if key in cls._synonyms and cls._synonyms[key] in cls._all_conversions:
            return cls(cls._all_conversions[cls._synonyms[key]])
        raise KeyError(f"Unit '{key}' not found.")


# Dynamically create unit properties
Units._create_properties(Units.length_conversions)
Units._create_properties(Units.time_conversions)
Units._create_properties(Units.mass_conversions)
Units._create_properties(Units.angle_conversions)
Units._create_properties(Units.current_conversions)
Units._create_properties(Units.luminous_intensity_conversions)
Units._create_properties(Units.temperature_conversions)
Units._create_properties(Units.area_conversions)
Units._create_properties(Units.volume_conversions)
Units._create_properties(Units.power_conversions)
Units._create_properties(Units.pressure_conversions)
Units._create_properties(Units.speed_conversions)
Units._create_properties(Units.force_conversions)

# Combine all conversions into a single dictionary
Units._all_conversions = {}
for d in [Units.length_conversions, Units.time_conversions, Units.mass_conversions,
          Units.angle_conversions, Units.current_conversions, Units.luminous_intensity_conversions,
          Units.temperature_conversions, Units.area_conversions, Units.volume_conversions,
          Units.power_conversions, Units.pressure_conversions, Units.speed_conversions,
          Units.force_conversions]:
    Units._all_conversions.update(d)

# Add synonyms by copying entries from _synonyms
for syn, actual in Units._synonyms.items():
    if actual in Units._all_conversions:
        Units._all_conversions[syn] = Units._all_conversions[actual]


# Example usage:
if __name__ == "__main__":
    # Using attribute access:
    a = 4 * Units.mm   # Convert 4 mm to m
    print("4 mm in meters:", a)

    # Using dictionary-style access:
    speed_in_ms = 10 * Units['m/s']  # 10 m/s in m/s (base)
    print("10 m/s in m/s:", speed_in_ms)

    # Convert 10 m/s to mph:
    mph = speed_in_ms / Units.mile_per_hour
    print("10 m/s in mph:", mph)
