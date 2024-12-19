
# RCAIDE/Core/Units.py
# 
# 
# Created:  Dec 2024, Niranjan Nanjappa 


# ----------------------------------------------------------------------------------------------------------------------
#  Container
# ----------------------------------------------------------------------------------------------------------------------   

class Units():
    """ RCAIDE.Core.Units()
        Unit conversion toolbox
        Works by converting values in to and out of the base unit
        
        Important Note and Warning - 
            This does not enforce unit consistency!!!
            Unit consistency is the responsibility of the user
        
        Usage:
          from RCAIDE.Framework.Core import Units
          a = 4. * Units.mm  # convert in to base unit
          b = a  / Units.mm  # convert out of base unit
          
        Comments:
          Retreving an attribute of Units (ie Units.mm) returns 
          the conversion ratio to the base unit.  So in the above
          example Units.mm = 0.001, which is the conversion ratio
          to meters.  Thus the * (multiplication) operation converts 
          from the current units to the base units and / (division) 
          operation converts from the base units to the desired units.
         
        Base Units:
          mass        : kilogram
          length      : meters
          time        : seconds
          temperature : Kelvin
          angle       : radian
          current     : Ampere
          luminsoity  : candela
    """
    # FUNDAMENTAL CONVERSION FACTORS
    # Length
    _FEET_TO_M = 0.3048
    _INCH_TO_M = 0.0254
    _MILE_TO_M = 1609.34
    _NM_TO_M = 1852
    _YARD_TO_M = 0.9144
    _KM_TO_M = 1000
    _DM_TO_M = 0.1
    _CM_TO_M = 0.01
    _MM_TO_M = 0.001

    # Time
    _MIN_TO_S = 60
    _HOUR_TO_S = 3600
    _DAY_TO_S = 86400
    _WEEK_TO_S = 604800
    _MONTH_TO_S = 2592000  # 30-day month
    _YEAR_TO_S = 31536000  # 365-day year
    _MS_TO_S = 0.001

    # Mass
    _GRAM_TO_KG = 0.001
    _MG_TO_KG = 1e-6
    _POUND_TO_KG = 0.453592
    _OUNCE_TO_KG = 0.0283495
    _TON_TO_KG = 1000

    # Force
    _LBF_TO_N = 4.44822  # Pound force to Newton

    # DERIVED CONVERSION FACTORS
    # Area (using square of length factors)
    _ACRE_TO_SQM = 4046.86
    _SQYARD_TO_SQM = _YARD_TO_M ** 2
    _SQFEET_TO_SQM = _FEET_TO_M ** 2
    _SQINCH_TO_SQM = _INCH_TO_M ** 2
    _SQKM_TO_SQM = _KM_TO_M ** 2
    _SQDM_TO_SQM = _DM_TO_M ** 2
    _SQCM_TO_SQM = _CM_TO_M ** 2
    _HECTARE_TO_SQM = 10000

    # Volume (using cube of length factors)
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

    # Power
    _KW_TO_W = 1000
    _BTU_PER_HOUR_TO_W = 0.29307107
    _HP_TO_W = 745.7

    # Pressure (Force per unit area)
    _ATM_TO_PA = 101325
    _BAR_TO_PA = 100000
    _MBAR_TO_PA = 100
    _MPA_TO_PA = 1e6
    _KPA_TO_PA = 1000
    _PSI_TO_PA = _LBF_TO_N / (_INCH_TO_M ** 2)
    _PSF_TO_PA = _LBF_TO_N / (_FEET_TO_M ** 2)

    # Speed (Distance per time)
    _KNOT_TO_MS = _NM_TO_M / _HOUR_TO_S
    _KMS_TO_MS = _KM_TO_M
    _MPH_TO_MS = _MILE_TO_M / _HOUR_TO_S
    _FPM_TO_MS = _FEET_TO_M / _MIN_TO_S
    _FPS_TO_MS = _FEET_TO_M

    # Angle
    _DEG_TO_RAD = 0.0174533

    def __init__(self, factor):
        self.factor = factor

    def __mul__(self, value):
        return value * self.factor

    def __rmul__(self, value):
        return value * self.factor

    def __truediv__(self, value):
        return value / self.factor

    # Area properties
    @classmethod
    @property
    def acre(cls): return cls(cls._ACRE_TO_SQM)
    
    @classmethod
    @property
    def square_yard(cls): return cls(cls._SQYARD_TO_SQM)
    
    @classmethod
    @property
    def square_feet(cls): return cls(cls._SQFEET_TO_SQM)
    
    @classmethod
    @property
    def square_inch(cls): return cls(cls._SQINCH_TO_SQM)
    
    @classmethod
    @property
    def square_kilometer(cls): return cls(cls._SQKM_TO_SQM)
    
    @classmethod
    @property
    def square_decimeter(cls): return cls(cls._SQDM_TO_SQM)
    
    @classmethod
    @property
    def square_meter(cls): return cls(1.0)
    
    @classmethod
    @property
    def square_centimeter(cls): return cls(cls._SQCM_TO_SQM)
    
    @classmethod
    @property
    def hectare(cls): return cls(cls._HECTARE_TO_SQM)

    # Power properties
    @classmethod
    @property
    def kilowatt(cls): return cls(cls._KW_TO_W)
    
    @classmethod
    @property
    def btu_per_hour(cls): return cls(cls._BTU_PER_HOUR_TO_W)
    
    @classmethod
    @property
    def horsepower(cls): return cls(cls._HP_TO_W)
    
    @classmethod
    @property
    def watt(cls): return cls(1.0)

    # Pressure properties
    @classmethod
    @property
    def atmosphere(cls): return cls(cls._ATM_TO_PA)
    
    @classmethod
    @property
    def bar(cls): return cls(cls._BAR_TO_PA)
    
    @classmethod
    @property
    def millibar(cls): return cls(cls._MBAR_TO_PA)
    
    @classmethod
    @property
    def pascal(cls): return cls(1.0)
    
    @classmethod
    @property
    def megapascal(cls): return cls(cls._MPA_TO_PA)
    
    @classmethod
    @property
    def kilopascal(cls): return cls(cls._KPA_TO_PA)
    
    @classmethod
    @property
    def psf(cls): return cls(cls._PSF_TO_PA)
    
    @classmethod
    @property
    def psi(cls): return cls(cls._PSI_TO_PA)

    # Speed properties
    @classmethod
    @property
    def knots(cls): return cls(cls._KNOT_TO_MS)
    
    @classmethod
    @property
    def kilometer_per_second(cls): return cls(cls._KMS_TO_MS)
    
    @classmethod
    @property
    def meter_per_second(cls): return cls(1.0)
    
    @classmethod
    @property
    def mile_per_hour(cls): return cls(cls._MPH_TO_MS)
    
    @classmethod
    @property
    def feet_per_minute(cls): return cls(cls._FPM_TO_MS)
    
    @classmethod
    @property
    def feet_per_second(cls): return cls(cls._FPS_TO_MS)

    # Time properties
    @classmethod
    @property
    def minute(cls): return cls(cls._MIN_TO_S)
    
    @classmethod
    @property
    def hour(cls): return cls(cls._HOUR_TO_S)
    
    @classmethod
    @property
    def second(cls): return cls(1.0)
    
    @classmethod
    @property
    def day(cls): return cls(cls._DAY_TO_S)
    
    @classmethod
    @property
    def week(cls): return cls(cls._WEEK_TO_S)
    
    @classmethod
    @property
    def month(cls): return cls(cls._MONTH_TO_S)
    
    @classmethod
    @property
    def year(cls): return cls(cls._YEAR_TO_S)
    
    @classmethod
    @property
    def millisecond(cls): return cls(cls._MS_TO_S)

    # Volume properties
    @classmethod
    @property
    def cubic_meter(cls): return cls(1.0)
    
    @classmethod
    @property
    def liter(cls): return cls(cls._LITER_TO_M3)
    
    @classmethod
    @property
    def deciliter(cls): return cls(cls._DL_TO_M3)
    
    @classmethod
    @property
    def centiliter(cls): return cls(cls._CL_TO_M3)
    
    @classmethod
    @property
    def milliliter(cls): return cls(cls._ML_TO_M3)
    
    @classmethod
    @property
    def cubic_yard(cls): return cls(cls._CUYD_TO_M3)
    
    @classmethod
    @property
    def cubic_foot(cls): return cls(cls._CUFT_TO_M3)
    
    @classmethod
    @property
    def cubic_inch(cls): return cls(cls._CUIN_TO_M3)
    
    @classmethod
    @property
    def bushel(cls): return cls(cls._BUSHEL_TO_M3)
    
    @classmethod
    @property
    def barrel(cls): return cls(cls._BARREL_TO_M3)
    
    @classmethod
    @property
    def fluid_ounce(cls): return cls(cls._FLOZ_TO_M3)
    
    @classmethod
    @property
    def gallon(cls): return cls(cls._GALLON_TO_M3)
    
    @classmethod
    @property
    def pint(cls): return cls(cls._PINT_TO_M3)
    
    @classmethod
    @property
    def quart(cls): return cls(cls._QUART_TO_M3)

    # Mass properties
    @classmethod
    @property
    def kilogram(cls): return cls(1.0)
    
    @classmethod
    @property
    def gram(cls): return cls(cls._GRAM_TO_KG)
    
    @classmethod
    @property
    def milligram(cls): return cls(cls._MG_TO_KG)
    
    @classmethod
    @property
    def pound(cls): return cls(cls._POUND_TO_KG)
    
    @classmethod
    @property
    def lbs(cls): return cls(cls._POUND_TO_KG)
    
    @classmethod
    @property
    def lb(cls): return cls(cls._POUND_TO_KG)
    
    @classmethod
    @property
    def ounce(cls): return cls(cls._OUNCE_TO_KG)
    
    @classmethod
    @property
    def metric_ton(cls): return cls(cls._TON_TO_KG)

    # Angle properties
    @classmethod
    @property
    def degree(cls): return cls(cls._DEG_TO_RAD)
    
    @classmethod
    @property
    def radian(cls): return cls(1.0)