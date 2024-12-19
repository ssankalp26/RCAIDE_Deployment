
# RCAIDE/Core/Units.py
# 
# 
# Created:  Dec 2024, Niranjan Nanjappa 


# ----------------------------------------------------------------------------------------------------------------------
#  Container
# ----------------------------------------------------------------------------------------------------------------------   

class Units:
    """
    A comprehensive unit conversion class similar to Pint, using base SI units:
    - Length: meter (m)
    - Mass: kilogram (kg)
    - Time: second (s)
    - Temperature: Kelvin (K)
    - Angle: radian (rad)
    - Current: Ampere (A)
    - Luminous intensity: candela (cd)
    
    All other units are derived from these base units.
    The class is case-insensitive, supports synonyms and multiple notations, and allows 
    accessing units as attributes or like a dictionary.
    
    Example:
        speed_in_ms = 10 * Units.mps
        speed_in_kmh = speed_in_ms / Units["km/h"]
        print(speed_in_kmh)
        
        # Using synonyms and case-insensitivity:
        speed_in_fps = speed_in_ms / Units.FPS
        print(speed_in_fps)
        
        # Using a special notation:
        speed_in_ms_alt = 10 * Units["M/s"]
        print(speed_in_ms_alt)
    """

    # Fundamental Conversion Factors
    _FEET_TO_M = 0.3048
    _INCH_TO_M = 0.0254
    _MILE_TO_M = 1609.34
    _NM_TO_M = 1852.0
    _YARD_TO_M = 0.9144
    _KM_TO_M = 1000.0
    _DM_TO_M = 0.1
    _CM_TO_M = 0.01
    _MM_TO_M = 0.001

    _MIN_TO_S = 60
    _HOUR_TO_S = 3600
    _DAY_TO_S = 86400
    _WEEK_TO_S = 604800
    _MONTH_TO_S = 2592000   # 30-day month assumption
    _YEAR_TO_S = 31536000   # 365-day year
    _MS_TO_S = 0.001

    _GRAM_TO_KG = 0.001
    _MG_TO_KG = 1e-6
    _POUND_TO_KG = 0.453592
    _OUNCE_TO_KG = 0.0283495
    _TON_TO_KG = 1000.0

    _LBF_TO_N = 4.44822

    # Areas and volumes are derived from length conversions
    # Area:
    _ACRE_TO_SQM = 4046.86
    _SQYARD_TO_SQM = _YARD_TO_M ** 2
    _SQFEET_TO_SQM = _FEET_TO_M ** 2
    _SQINCH_TO_SQM = _INCH_TO_M ** 2
    _SQKM_TO_SQM = _KM_TO_M ** 2
    _SQDM_TO_SQM = _DM_TO_M ** 2
    _SQCM_TO_SQM = _CM_TO_M ** 2
    _HECTARE_TO_SQM = 10000.0

    # Volume:
    _CUYD_TO_M3 = _YARD_TO_M ** 3
    _CUFT_TO_M3 = _FEET_TO_M ** 3
    _CUIN_TO_M3 = _INCH_TO_M ** 3
    _LITER_TO_M3 = 0.001
    _DL_TO_M3 = _LITER_TO_M3 / 10
    _CL_TO_M3 = _LITER_TO_M3 / 100
    _ML_TO_M3 = _LITER_TO_M3 / 1000
    _GALLON_TO_M3 = 0.00378541
    _QUART_TO_M3 = _GALLON_TO_M3 / 4
    _PINT_TO_M3 = _GALLON_TO_M3 / 8
    _FLOZ_TO_M3 = _GALLON_TO_M3 / 128
    _BUSHEL_TO_M3 = 0.0352391
    _BARREL_TO_M3 = 0.158987

    # Power:
    _KW_TO_W = 1000.0
    _BTU_PER_HOUR_TO_W = 0.29307107
    _HP_TO_W = 745.7

    # Pressure:
    _ATM_TO_PA = 101325
    _BAR_TO_PA = 100000
    _MBAR_TO_PA = 100
    _MPA_TO_PA = 1e6
    _KPA_TO_PA = 1000
    _PSI_TO_PA = _LBF_TO_N / (_INCH_TO_M ** 2)
    _PSF_TO_PA = _LBF_TO_N / (_FEET_TO_M ** 2)

    # Speed:
    _KNOT_TO_MS = _NM_TO_M / _HOUR_TO_S
    _MPH_TO_MS = _MILE_TO_M / _HOUR_TO_S
    _FPM_TO_MS = _FEET_TO_M / _MIN_TO_S
    _FPS_TO_MS = _FEET_TO_M
    _KMS_TO_MS = _KM_TO_M  # For km/s, 1 km/s = 1000 m/s

    # Angle:
    _DEG_TO_RAD = 0.0174533

    # Base Units:
    # length: meter (m)
    # time: second (s)
    # mass: kilogram (kg)
    # temperature: Kelvin (K)
    # angle: radian (rad)
    # luminous intensity: candela (cd)
    # current: Ampere (A)
    # force: newton (N)
    # pressure: pascal (Pa)
    # power: watt (W)
    # area: square_meter (m²)
    # volume: cubic_meter (m³)
    # speed: meter_per_second (m/s)

    # Dictionary of units: factor to base units
    # Base units themselves have factor 1.0
    _units = {
        # Base units:
        "meter": 1.0,
        "m": 1.0,
        "kilogram": 1.0,
        "kg": 1.0,
        "second": 1.0,
        "s": 1.0,
        "radian": 1.0,
        "rad": 1.0,
        "kelvin": 1.0,
        "k": 1.0,
        "ampere": 1.0,
        "a": 1.0,
        "candela": 1.0,
        "cd": 1.0,
        "watt": 1.0,
        "pascal": 1.0,
        "newton": 1.0,
        "square_meter": 1.0,
        "cubic_meter": 1.0,
        "meter_per_second": 1.0,

        # Length units:
        "mm":  _MM_TO_M,
        "millimeter": _MM_TO_M,
        "cm": _CM_TO_M,
        "centimeter": _CM_TO_M,
        "dm": _DM_TO_M,
        "decimeter": _DM_TO_M,
        "km": _KM_TO_M,
        "kilometer": _KM_TO_M,
        "inch": _INCH_TO_M,
        "foot": _FEET_TO_M,
        "ft": _FEET_TO_M,
        "yard": _YARD_TO_M,
        "mile": _MILE_TO_M,
        "nautical_mile": _NM_TO_M,

        # Time units:
        "minute": _MIN_TO_S,
        "min": _MIN_TO_S,
        "hour": _HOUR_TO_S,
        "h": _HOUR_TO_S,
        "day": _DAY_TO_S,
        "week": _WEEK_TO_S,
        "month": _MONTH_TO_S,
        "year": _YEAR_TO_S,
        "ms": _MS_TO_S,
        "millisecond": _MS_TO_S,

        # Mass units:
        "g": _GRAM_TO_KG,
        "gram": _GRAM_TO_KG,
        "mg": _MG_TO_KG,
        "milligram": _MG_TO_KG,
        "pound": _POUND_TO_KG,
        "lb": _POUND_TO_KG,
        "lbs": _POUND_TO_KG,
        "ounce": _OUNCE_TO_KG,
        "metric_ton": _TON_TO_KG,
        "ton": _TON_TO_KG,

        # Angle units:
        "degree": _DEG_TO_RAD,

        # Area units:
        "acre": _ACRE_TO_SQM,
        "square_yard": _SQYARD_TO_SQM,
        "sq_yard": _SQYARD_TO_SQM,
        "square_feet": _SQFEET_TO_SQM,
        "sq_feet": _SQFEET_TO_SQM,
        "square_inch": _SQINCH_TO_SQM,
        "sq_inch": _SQINCH_TO_SQM,
        "square_kilometer": _SQKM_TO_SQM,
        "sq_kilometer": _SQKM_TO_SQM,
        "square_decimeter": _SQDM_TO_SQM,
        "sq_decimeter": _SQDM_TO_SQM,
        "square_centimeter": _SQCM_TO_SQM,
        "sq_centimeter": _SQCM_TO_SQM,
        "hectare": _HECTARE_TO_SQM,

        # Volume units:
        "liter": _LITER_TO_M3,
        "l": _LITER_TO_M3,
        "deciliter": _DL_TO_M3,
        "dl": _DL_TO_M3,
        "centiliter": _CL_TO_M3,
        "cl": _CL_TO_M3,
        "milliliter": _ML_TO_M3,
        "ml": _ML_TO_M3,
        "cubic_yard": _CUYD_TO_M3,
        "cu_yard": _CUYD_TO_M3,
        "cubic_foot": _CUFT_TO_M3,
        "cu_foot": _CUFT_TO_M3,
        "cubic_inch": _CUIN_TO_M3,
        "cu_inch": _CUIN_TO_M3,
        "bushel": _BUSHEL_TO_M3,
        "barrel": _BARREL_TO_M3,
        "fluid_ounce": _FLOZ_TO_M3,
        "floz": _FLOZ_TO_M3,
        "gallon": _GALLON_TO_M3,
        "quart": _QUART_TO_M3,
        "pint": _PINT_TO_M3,

        # Power units:
        "kilowatt": _KW_TO_W,
        "kw": _KW_TO_W,
        "btu_per_hour": _BTU_PER_HOUR_TO_W,
        "btu/h": _BTU_PER_HOUR_TO_W,
        "horsepower": _HP_TO_W,
        "hp": _HP_TO_W,

        # Pressure units:
        "atmosphere": _ATM_TO_PA,
        "atm": _ATM_TO_PA,
        "bar": _BAR_TO_PA,
        "millibar": _MBAR_TO_PA,
        "mbar": _MBAR_TO_PA,
        "megapascal": _MPA_TO_PA,
        "mpa": _MPA_TO_PA,
        "kilopascal": _KPA_TO_PA,
        "kpa": _KPA_TO_PA,
        "psi": _PSI_TO_PA,
        "psf": _PSF_TO_PA,

        # Speed units:
        "knots": _KNOT_TO_MS,
        "knot": _KNOT_TO_MS,
        "kilometer_per_second": _KMS_TO_MS,
        "km/s": _KMS_TO_MS,
        "meter_per_second": 1.0,
        # We'll add synonyms below for m/s
        "mile_per_hour": _MPH_TO_MS,
        "mph": _MPH_TO_MS,
        "feet_per_minute": _FPM_TO_MS,
        "fpm": _FPM_TO_MS,
        "feet_per_second": _FPS_TO_MS,
        "fps": _FPS_TO_MS,

        # Temperature:
        # Kelvin is base, only ratio scale like Rankine
        "rankine": 1.8,
        "r": 1.8,

        # Force:
        "pound_force": _LBF_TO_N,
        "lbf": _LBF_TO_N,
    }

    # Synonyms map: these will be resolved to canonical names if needed
    _synonyms = {
        "m/s": "meter_per_second",
        "mps": "meter_per_second",
        "m·s⁻¹": "meter_per_second",

        "metre": "meter",
        "millimetre": "millimeter",
        "centimetre": "centimeter",
        "decimetre": "decimeter",
        "kilometre": "kilometer",

        "secs": "second",
        "hr": "hour",
        "yrs": "year",
        
        "millimetre": "millimeter",
        "millilitre": "milliliter",

        "lbm": "pound",  # sometimes used, map to pound (mass)
    }

    @staticmethod
    def _normalize_key(key: str) -> str:
        # case-insensitive and strip spaces
        return key.strip().lower()

    @classmethod
    def _finalize_units(cls):
        # First, ensure synonyms point to their canonical units
        updates = {}
        for syn, canonical in cls._synonyms.items():
            syn_norm = cls._normalize_key(syn)
            can_norm = cls._normalize_key(canonical)
            if can_norm not in cls._units:
                raise ValueError(f"Synonym '{syn}' refers to non-existent unit '{canonical}'.")
            updates[syn_norm] = cls._units[can_norm]

        # Add synonym entries
        cls._units.update(updates)

        # Ensure all keys are stored lowercase
        lower_units = {}
        for k, v in cls._units.items():
            lower_units[cls._normalize_key(k)] = v
        cls._units = lower_units

    _finalize_units()

    def __init__(self, factor: float):
        self.factor = factor

    def __mul__(self, value: float) -> float:
        return value * self.factor

    def __rmul__(self, value: float) -> float:
        return value * self.factor

    def __truediv__(self, value: float) -> float:
        return value / self.factor

    @classmethod
    def __getitem__(cls, key: str):
        norm = cls._normalize_key(key)
        if norm not in cls._units:
            raise KeyError(f"Unit '{key}' not found.")
        return cls(cls._units[norm])

    def __getattr__(self, attr: str):
        norm = self._normalize_key(attr)
        if norm not in self._units:
            raise AttributeError(f"Unit '{attr}' not found.")
        return self.__class__(self._units[norm])

    @classmethod
    def register_unit(cls, name: str, factor: float, synonyms: list = None):
        norm_name = cls._normalize_key(name)
        cls._units[norm_name] = factor
        if synonyms:
            for syn in synonyms:
                norm_syn = cls._normalize_key(syn)
                cls._units[norm_syn] = factor

    @classmethod
    def list_units(cls):
        return sorted(cls._units.keys())


# Example usage
if __name__ == "__main__":
    # 10 m/s in km/h:
    speed_in_ms = 10 * Units.mps
    speed_in_kmh = speed_in_ms / Units["km/h"]
    print("10 m/s in km/h:", speed_in_kmh)

    # 10 m/s in mph:
    speed_in_mph = speed_in_ms / Units.mph
    print("10 m/s in mph:", speed_in_mph)

    # Convert 1 meter to millimeters:
    mm_value = 1 / Units.mm
    print("1 m in mm:", mm_value)

    # Check synonyms and case-insensitivity:
    speed_in_ms_again = 10 * Units["M/s"]
    print("10 M/s in m/s:", speed_in_ms_again)

    # List some units:
    print("All units:", Units.list_units())
