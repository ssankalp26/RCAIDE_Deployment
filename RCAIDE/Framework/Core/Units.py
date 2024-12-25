import math

class _Units:
    """
    A container for unit conversions to SI (or SI-derived) units.
    Multiplying a value by one of these factors converts that value
    into the chosen SI base/derived unit.

    For example:
        34 * Units.lbs   -> kg
        5  * Units.btu   -> J
        10 * Units.lbf   -> N
    """
    

    _conversions = {
        # ------------------------------------------------
        # UNITLESS (dimensionless quantities)
        # ------------------------------------------------
        "unitless": 1.0,  # Alias for less
        "less": 1.0,  # Dimensionless
        # ------------------------------------------------
        # MASS -> kilograms (kg)
        # ------------------------------------------------
        "kilogram":         1.0,
        "kg":               1.0,
        "gram":             1e-3,             # 1 g = 0.001 kg
        "g":                1e-3,
        "milligram":        1e-6,
        "mg":               1e-6,
        "metric_ton":       1000.0,           # 1 metric ton = 1000 kg
        "ton":              1000.0,
        "pound_mass":       0.45359237,       # 1 lbm = 0.45359237 kg
        "lbm":              0.45359237,
        # Commonly, "lb" or "lbs" is used ambiguously between mass/force;
        # here we'll treat "lbs" as pound-mass for convenience:
        "pound":            0.45359237,
        "pounds":           0.45359237,
        "lb":               0.45359237,
        "lbs":              0.45359237,
        "ounce":            0.028349523125,   # 1 oz = 0.0283495 kg
        "oz":               0.028349523125,
        "slug":             14.5939029372,    # 1 slug = approx 14.5939 kg

        # ------------------------------------------------
        # FORCE -> newtons (N)
        # ------------------------------------------------
        "newton":           1.0,
        "N":                1.0,
        "pound_force":      4.448221615,      # 1 lbf = 4.448221615 N
        "lbf":              4.448221615,

        # ------------------------------------------------
        # LENGTH -> meters (m)
        # ------------------------------------------------
        "meter":            1.0,
        "meters":            1.0,
        "m":                1.0,
        "kilometer":        1000.0,
        "km":               1000.0,
        "centimeter":       0.01,
        "cm":               0.01,
        "millimeter":       0.001,
        "mm":               0.001,
        "decimeter":        0.1,
        "dm":               0.1,
        "mile":             1609.344,
        "miles":            1609.344,
        "nautical_mile":    1852.0,
        "nmi":              1852.0,
        "yard":             0.9144,
        "yd":               0.9144,
        "foot":             0.3048,
        "feet":             0.3048,
        "ft":               0.3048,
        "inch":             0.0254,
        "inches":           0.0254,
        "in":               0.0254,

        # ------------------------------------------------
        # AREA -> square meters (m^2)
        # ------------------------------------------------
        "square_meter":     1.0,
        "m^2":              1.0,
        "meters**2":        1.0,
        "acre":             4046.8564224,
        "square_yard":      0.9144**2,
        "square_feet":      0.3048**2,
        "square_foot":      0.3048**2,
        "square_inch":      0.0254**2,
        "square_kilometer": 1000.0**2,
        "square_decimeter": 0.1**2,
        "square_cm":        0.01**2,
        "square_millimeter":0.001**2,
        "hectare":          10000.0,

        # ------------------------------------------------
        # VOLUME -> cubic meters (m^3)
        # ------------------------------------------------
        "cubic_meter":      1.0,
        "m^3":              1.0,
        "liter":            1e-3,
        "l":                1e-3,
        "deciliter":        1e-4,
        "centiliter":       1e-5,
        "milliliter":       1e-6,
        "ml":               1e-6,
        "cubic_yard":       0.9144**3,
        "cubic_foot":       0.3048**3,
        "cubic_inch":       0.0254**3,
        "us_bushel":        0.03523907,       # approx
        "us_barrel":        0.119240471196,   # approx
        "fluid_ounce":      2.95735296875e-5,
        "fl_oz":            2.95735296875e-5,
        "gallon":           3.785411784e-3,   # US liquid gallon
        "quart":            0.946352946e-3,
        "pint":             0.473176473e-3,

        # ------------------------------------------------
        # TIME -> seconds (s)
        # ------------------------------------------------
        "second":           1.0,
        "s":                1.0,
        "millisecond":      1e-3,
        "ms":               1e-3,
        "minute":           60.0,
        "min":              60.0,
        "hour":             3600.0,
        "h":                3600.0,
        "day":              86400.0,
        "week":             604800.0,
        "month":            2629800.0,        # ~30.4375 days in seconds
        "year":             31557600.0,       # ~365.25 days in seconds

        # ------------------------------------------------
        # SPEED -> meters/second (m/s)
        # ------------------------------------------------
        "meter_per_second": 1.0,
        "m/s": 1.0,
        "mps":              1.0,
        "kilometer_per_second": 1000.0,
        "kps":                  1000.0,
        "mile_per_hour":    0.44704,
        "mph":              0.44704,
        "foot_per_minute":  0.3048 / 60.0,
        "fpm":              0.3048 / 60.0,
        "foot_per_second":  0.3048,
        "fps":              0.3048,
        "knot":             0.514444,
        "kts":             0.514444,
        "knots":            0.514444,

        # Rotational speed -> rad/s
        "rpm": 2.0 * math.pi / 60.0,  # 1 revolution/min = 2π rad / 60 s

        # Optionally, a more explicit name:
        "revolution_per_minute": 2.0 * math.pi / 60.0,

        # ------------------------------------------------
        # POWER -> watts (W)
        # ------------------------------------------------
        "watt":             1.0,
        "W":                1.0,
        "kilowatt":         1000.0,
        "KW":               1000.0,
        "horsepower":       745.7,
        "hp":               745.7,
        "btu_per_hour":     0.29307107,       # 1 BTU/h ~ 0.293 W

        # ------------------------------------------------
        # PRESSURE -> pascals (Pa)
        # ------------------------------------------------
        "pascal":           1.0,
        "pa":               1.0,
        "kilopascal":       1e3,
        "kpa":              1e3,
        "megapascal":       1e6,
        "mpa":              1e6,
        "bar":              1e5,
        "millibar":         1e2,
        "mbar":             1e2,
        "atmosphere":       101325.0,
        "atm":              101325.0,
        "pound_per_square_inch": 6894.757293,
        "psi":                   6894.757293,
        "pound_per_square_foot": 47.8802589,
        "psf":                   47.8802589,


        # ------------------------------------------------
        # ANGLE -> radians (rad)
        # ------------------------------------------------
        "radian":           1.0,
        "rad":              1.0,
        "deg":           math.pi / 180.0,
        "degree":           math.pi / 180.0,
        "degrees":          math.pi / 180.0,

        # ------------------------------------------------
        # FUEL CONSUMPTION -> kg/(W/s)
        # ------------------------------------------------
        "lb_per_hp_per_hr": (0.45359237 / 745.7) / 3600.0,  # lb/hp/hr to kg/W/s
        "lb/hp/hr": (0.45359237 / 745.7) / 3600.0,

        # ------------------------------------------------
        # ENERGY -> joules (J)
        # ------------------------------------------------
        "joule":            1.0,         # SI base for energy
        "j":                1.0,
        "watt_hour":        3600.0,      # 1 Wh = 3600 J
        "Wh":               3600.0,
        "kilowatt_hour":    3.6e6,       # 1 kWh = 3.6e6 J
        "kwh":              3.6e6,
        "btu":              1055.06,     # 1 BTU ~ 1055.06 J
        "watt": 1.0, "W": 1.0,
    }

    def __getattr__(self, name: str) -> float:
        """Allows attribute-like access, e.g. Units.lbs"""
        try:
            return self._conversions[name]
        except KeyError:
            raise AttributeError(f"Unit '{name}' is not defined.")

    def __getitem__(self, name: str) -> float:
        """Allows dict/key-like access, e.g. Units['lbs']"""
        try:
            return self._conversions[name]
        except KeyError:
            raise KeyError(f"Unit '{name}' is not defined.")


# A globally available instance:
Units = _Units()

   