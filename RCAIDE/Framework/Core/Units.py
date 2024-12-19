
# RCAIDE/Core/Units.py
# 
# 
# Created:  Dec 2024, Niranjan Nanjappa 


# ----------------------------------------------------------------------------------------------------------------------
#  Container
# ----------------------------------------------------------------------------------------------------------------------   

from typing import Dict, Set, Union, Optional
import re
from math import pi

class Units:
    # Base unit definitions
    BASE_UNITS = {
        'MASS': {
            'kg': 1.0,
            'g': 0.001,
            'mg': 1e-6,
            'lb': 0.45359237,
            'oz': 0.028349523125
        },
        'DISTANCE': {
            'm': 1.0,
            'km': 1000.0,
            'cm': 0.01,
            'mm': 0.001,
            'mile': 1609.344,
            'yard': 0.9144,
            'foot': 0.3048,
            'inch': 0.0254
        },
        'TIME': {
            's': 1.0,
            'min': 60.0,
            'hr': 3600.0,
            'day': 86400.0
        },
        'ANGLE': {
            'rad': 1.0,
            'deg': pi/180,
            'grad': pi/200
        },
        'LUMINESCENCE': {
            'cd': 1.0,
            'lm': 1.0  # lumen at 1 steradian
        }
    }

    # Unit synonyms
    SYNONYMS = {
        'meters': 'm',
        'meter': 'm',
        'metres': 'm',
        'metre': 'm',
        'seconds': 's',
        'second': 's',
        'sec': 's',
        'minutes': 'min',
        'minute': 'min',
        'hours': 'hr',
        'hour': 'hr',
        'kilometers': 'km',
        'kilometer': 'km',
        'mps': 'm/s',
        'meters_per_second': 'm/s',
        'metres_per_second': 'm/s',
        'kph': 'km/hr',
        'kilometers_per_hour': 'km/hr',
        'mph': 'mile/hr',
        'miles_per_hour': 'mile/hr',
        'newton': 'kg*m/s^2',
        'newtons': 'kg*m/s^2',
        'pascal': 'kg/(m*s^2)',
        'pascals': 'kg/(m*s^2)',
        'joule': 'kg*m^2/s^2',
        'joules': 'kg*m^2/s^2'
    }

    def __init__(self, value: float, unit_str: str):
        """Initialize a Units object with a value and unit string."""
        self.value = float(value)
        # Clean and standardize the unit string
        self.unit_str = self._standardize_unit_string(unit_str)
        # Parse the unit string into components
        self.parsed_units = self._parse_unit_string(self.unit_str)

    @staticmethod
    def _standardize_unit_string(unit_str: str) -> str:
        """Standardize unit string format."""
        # Remove whitespace and convert to lowercase
        unit_str = unit_str.lower().replace(' ', '')
        
        # Remove Units[] wrapper if present
        unit_str = re.sub(r'^units\[(.*)\]$', r'\1', unit_str)
        
        # Replace special multiplication and division symbols
        unit_str = unit_str.replace('⋅', '*').replace('×', '*')
        unit_str = unit_str.replace('²', '^2').replace('³', '^3')
        
        # Replace synonyms
        for synonym, standard in Units.SYNONYMS.items():
            if unit_str == synonym:
                return standard
        
        return unit_str

    def _parse_unit_string(self, unit_str: str) -> Dict[str, float]:
        """Parse a unit string into its components with exponents."""
        parsed_units = {}
        
        # Handle parentheses
        while '(' in unit_str:
            # Find innermost parentheses
            match = re.search(r'\(([^()]+)\)', unit_str)
            if not match:
                break
            
            inner_expr = match.group(1)
            # If this is in denominator, invert all exponents
            if re.search(r'/\s*\(', unit_str[:match.start()]):
                inner_expr = self._invert_expression(inner_expr)
            
            unit_str = unit_str[:match.start()] + inner_expr + unit_str[match.end():]
        
        # Split by multiplication and division
        parts = re.split(r'[*/]', unit_str)
        operators = re.findall(r'[*/]', unit_str)
        
        current_denominator = False
        
        for i, part in enumerate(parts):
            if not part:
                continue
                
            # Check for exponents
            if '^' in part:
                base, exp = part.split('^')
                exp = float(exp)
            else:
                base = part
                exp = 1.0
            
            # Adjust exponent if in denominator
            if current_denominator:
                exp = -exp
            
            # Strip any remaining non-alphabetic characters
            base = re.sub(r'[^a-zA-Z]', '', base)
            
            # Update parsed units
            if base in parsed_units:
                parsed_units[base] += exp
            else:
                parsed_units[base] = exp
            
            # Update denominator flag based on operators
            if i < len(operators):
                current_denominator = (operators[i] == '/')
        
        return parsed_units

    def _invert_expression(self, expr: str) -> str:
        """Invert all exponents in an expression."""
        parts = expr.split('*')
        inverted_parts = []
        for part in parts:
            if '^' in part:
                base, exp = part.split('^')
                inverted_parts.append(f"{base}^{-float(exp)}")
            else:
                inverted_parts.append(f"{part}^-1")
        return '*'.join(inverted_parts)

    def convert_to(self, target_unit: str) -> 'Units':
        """Convert to another unit."""
        target_unit = self._standardize_unit_string(target_unit)
        target_parsed = self._parse_unit_string(target_unit)
        
        # Verify compatibility
        if not self._is_compatible(target_parsed):
            raise ValueError(f"Cannot convert from {self.unit_str} to {target_unit}")
        
        # Calculate conversion factor
        factor = self._conversion_factor(self.parsed_units, target_parsed)
        
        return Units(self.value * factor, target_unit)

    def _is_compatible(self, target_parsed: Dict[str, float]) -> bool:
        """Check if units are compatible for conversion."""
        # For each base unit category, check if the exponents match
        for category in self.BASE_UNITS:
            source_exp = sum(self.parsed_units.get(unit, 0) 
                           for unit in self.BASE_UNITS[category])
            target_exp = sum(target_parsed.get(unit, 0) 
                           for unit in self.BASE_UNITS[category])
            if abs(source_exp - target_exp) > 1e-10:  # Use small epsilon for float comparison
                return False
        return True

    def _conversion_factor(self, source_parsed: Dict[str, float], 
                          target_parsed: Dict[str, float]) -> float:
        """Calculate the conversion factor between units."""
        factor = 1.0
        
        # Process source units
        for unit, exp in source_parsed.items():
            for category in self.BASE_UNITS:
                if unit in self.BASE_UNITS[category]:
                    factor *= self.BASE_UNITS[category][unit] ** exp
                    
        # Process target units
        for unit, exp in target_parsed.items():
            for category in self.BASE_UNITS:
                if unit in self.BASE_UNITS[category]:
                    factor /= self.BASE_UNITS[category][unit] ** exp
                    
        return factor

    def __str__(self) -> str:
        """String representation of the Units object."""
        return f"{self.value} {self.unit_str}"

    def __repr__(self) -> str:
        """Detailed string representation of the Units object."""
        return f"Units({self.value}, '{self.unit_str}')"

# Example usage and tests
def run_tests():
    # Test basic conversions
    length = Units(1, "m")
    assert abs(length.convert_to("cm").value - 100) < 1e-10
    
    speed = Units(1, "m/s")
    assert abs(speed.convert_to("km/hr").value - 3.6) < 1e-10
    
    # Test case insensitivity
    speed2 = Units(1, "M/S")
    assert abs(speed2.convert_to("KM/HR").value - 3.6) < 1e-10
    
    # Test synonyms
    speed3 = Units(1, "mps")
    assert abs(speed3.convert_to("kilometers_per_hour").value - 3.6) < 1e-10
    
    # Test Units[] format
    speed4 = Units(1, "Units[m/s]")
    assert abs(speed4.convert_to("kph").value - 3.6) < 1e-10
    
    # Test derived units
    force = Units(1, "kg*m/s^2")  # 1 Newton
    assert abs(force.convert_to("kg*m/s^2").value - 1) < 1e-10
    
    # Test area
    area = Units(1, "m^2")
    assert abs(area.convert_to("cm^2").value - 10000) < 1e-10
    
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
    
    # Additional example usage
    examples = [
        (Units(1, "m/s"), "km/hr"),
        (Units(1, "kg*m/s^2"), "newton"),
        (Units(1, "m^2"), "cm^2"),
        (Units(100, "km/hr"), "m/s"),
        (Units(1, "pascal"), "kg/(m*s^2)")
    ]
    
    for unit, target in examples:
        converted = unit.convert_to(target)
        print(f"{unit} = {converted}")