
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
        a = 4. * Units.mm   # Convert 4 millimeters into meters (the base length unit)
        b = a / Units.mm    # Convert back from meters to millimeters

    Explanation:
        Accessing an attribute of Units (e.g. Units.mm) returns the conversion factor
        to the base unit. For instance, Units.mm = 0.001 means 1 mm = 0.001 m.
        Multiplying by Units.mm converts from millimeters to meters.
        Dividing by Units.mm converts from meters to millimeters.
    
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

    Note on Temperature:
        Temperature scales involving offsets (°C, °F) cannot be handled by a simple scale factor.
        If using this class for temperature, restrict yourself to conversions that are pure scale
        factors (e.g., Rankine to Kelvin). Otherwise, handle offsets outside of this tool.
    """

    # Fundamental conversion factors to base units:
    # Length (base unit: meter)
    length_conversions = {
        'm': 1.0,
        'km': 1000.0,
        'dm': 0.1,
        'cm': 0.01,
        'mm': 0.001,
        'micrometer': 1e-6,
        'nanometer': 1e-9,
        'inch': 0.0254,
        'ft': 0.3048,
        'yard': 0.9144,
        'mile': 1609.34,
        'nautical_mile': 1852.0
    }

    # Time (base unit: second)
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

    # Mass (base unit: kilogram)
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

    # Angle (base unit: radian)
    angle_conversions = {
        'radian': 1.0,
        'degree': 0.0174533
    }

    # Current (base unit: Ampere)
    current_conversions = {
        'A': 1.0,
        'mA': 1e-3,
        'µA': 1e-6
    }

    # Luminous intensity (base unit: candela)
    # Note: Conversions for luminous intensity are not as straightforward since candela is a base SI unit.
    # Commonly, people convert luminous flux (lumens) and illuminance (lux), but these are different quantities.
    # Here, we only provide direct scale multiples (e.g., millicandela).
    luminous_intensity_conversions = {
        'cd': 1.0,
        'mcd': 1e-3
    }

    # Temperature (base unit: Kelvin)
    # For temperature, we provide only ratio-based units. Realistically, Celsius and Fahrenheit require offsets.
    # If strictly using ratio-based conversions, you could do something like Rankine = Kelvin * 1.8
    temperature_conversions = {
        'K': 1.0,
        'R': 1.8,  # Rankine = Kelvin * 1.8 (no offset at absolute scale)
        # Celsius and Fahrenheit are not included due to their offset nature.
    }

    # Area (base unit: square meter)
    # Area conversions are derived from length conversions squared.
    area_conversions = {
        'square_meter': 1.0,
        'hectare': 10000.0,
        'acre': 4046.86,
        'square_kilometer': 1000.0**2,
        'square_decimeter': 0.1**2,
        'square_centimeter': 0.01**2,
        'square_millimeter': 0.001**2,
        'square_inch': 0.0254**2,
        'square_foot': 0.3048**2,
        'square_yard': 0.9144**2
    }

    # Volume (base unit: cubic meter)
    # Volume conversions are derived from length conversions cubed where applicable.
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

    # Power (base unit: watt)
    power_conversions = {
        'watt': 1.0,
        'kilowatt': 1000.0,
        'btu_per_hour': 0.29307107,
        'horsepower': 745.7
    }

    # Pressure (base unit: pascal)
    # psi and psf use lbf (pound-force) and inch/foot conversions:
    # lbf to newton: 1 lbf = 4.44822 N
    # psi = lbf/in² = 4.44822 / (0.0254²) Pa
    # psf = lbf/ft²  = 4.44822 / (0.3048²) Pa
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

    # Speed (base unit: meter per second)
    # knot = nautical mile / hour
    # mph = mile / hour
    # fps = foot / second
    # fpm = foot / minute
    knot_to_ms = length_conversions['nautical_mile'] / time_conversions['hour']
    mph_to_ms = length_conversions['mile'] / time_conversions['hour']
    fps_to_ms = length_conversions['ft']
    fpm_to_ms = length_conversions['ft'] / time_conversions['minute']
    kms_to_ms = length_conversions['km']  # km/s (just scale length)

    speed_conversions = {
        'meter_per_second': 1.0,
        'kilometer_per_second': kms_to_ms,
        'knots': knot_to_ms,
        'mile_per_hour': mph_to_ms,
        'feet_per_second': fps_to_ms,
        'feet_per_minute': fpm_to_ms
    }

    # Force (base unit: newton)
    # We provide lbf as a convenience.
    force_conversions = {
        'newton': 1.0,
        'pound_force': _LBF_TO_N
    }

    # The following method transforms a dictionary of unit factors into class properties.
    @classmethod
    def _create_properties(cls, conversions_dict):
        for unit_name, factor in conversions_dict.items():
            # Create a property for each unit
            # Example: @property def mm(cls): return cls(factor)
            # Instead of rewriting, we can use a closure:
            def make_property(f):
                return property(lambda self: self.__class__(f))
            
            # For class-level access, we define it as a classmethod property
            # We’ll define a small descriptor that returns a Units instance:
            setattr(cls, unit_name, classmethod(property(lambda c, f=factor: c(f))))

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

# Dynamically create the unit properties
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
