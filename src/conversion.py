from .units import *

class Conversion:

    def convert_temperature(self, value, from_unit, to_unit, temperature_units):
        from_unit = from_unit.upper()
        to_unit = to_unit.upper()

        to_kelvin = temperature_units[from_unit][3]
        from_kelvin = temperature_units[to_unit][4]
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
