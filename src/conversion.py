from .units import *

from decimal import Decimal, getcontext, InvalidOperation, ROUND_HALF_UP
# Set precision
getcontext().prec = 28

class Conversion:

    def convert_temperature(self, value, from_unit, to_unit, temperature_units):

        to_kelvin = temperature_units[from_unit][3]
        from_kelvin = temperature_units[to_unit][5]
        kelvin_value = to_kelvin(value)
        return from_kelvin(kelvin_value)

    def convert_value(self, value, from_unit, to_unit, category, conversion_types=CONVERSION_TYPES):
        category = category.lower()

        if category == 'temperature':
            return self.convert_temperature(value, from_unit, to_unit, conversion_types.get(category))

        units_dict = conversion_types.get(category)
        if units_dict is None:
            raise ValueError(f"Unsupported category: {category}")

        # Generic factor-based conversion
        from_factor = units_dict[from_unit][3]
        to_factor = units_dict[to_unit][3]
        return value * from_factor / to_factor

    def format_conversion_result(self, value) -> str:
        if not isinstance(value, Decimal):
            value = Decimal(str(value))

        abs_val = abs(value)

        # Use scientific notation if number is very small or very large
        if abs_val != 0 and (abs_val < Decimal("0.001") or abs_val >= Decimal("10000")):
            # Round to 3 significant digits using quantize and adjusted exponent
            exponent = value.adjusted()  # position of most significant digit
            digits = 3
            quant = Decimal('1e{}'.format(exponent - digits + 1))
            rounded = value.quantize(quant, rounding=ROUND_HALF_UP)

            # Format as scientific notation with 3 significant digits
            # 'E' formatting automatically formats to 3 digits after decimal point for '.3E'
            return f"{rounded:.3E}".replace("E+0", "E").replace("E+", "E").replace("E-0", "E-")

        # Otherwise, round and strip trailing zeros, 7 decimal places
        value = self.round_to_7_places(value)
        s = format(value, 'f').rstrip('0').rstrip('.') if '.' in str(value) else str(value)
        return s

    def round_to_7_places(self, val: Decimal) -> Decimal:
        if val.is_zero():
            return Decimal("0")
        return val.quantize(Decimal("0.0000001"), rounding=ROUND_HALF_UP)

