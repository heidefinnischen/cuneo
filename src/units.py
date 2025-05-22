LENGTH_UNITS = {
# id: singular name, plural name, short, factor
    'm': ['meter', 'meters', 'm', 1.0],
    'km': ['kilometer', 'kilometers', 'km', 1000.0],
    'cm': ['centimeter', 'centimeters', 'cm', 0.01],
    'mm': ['millimeter', 'millimeters', 'mm', 0.001],
    'μm': ['micrometer', 'micrometers', 'μm', 1e-6],
    'nm': ['nanometer', 'nanometers', 'nm', 1e-9],
    'in': ['inch', 'inches', 'in', 0.0254],
    'ft': ['foot', 'feet', 'ft', 0.3048],
    'yd': ['yard', 'yards', 'yd', 0.9144],
    'mi': ['mile', 'miles', 'mi', 1609.34],
    'nmi': ['nautical mile', 'nautical miles', 'nmi', 1852.0],
    }

SPEED_UNITS = {
    'm/s':    ['meter per second', 'meters per second', 'm/s', 1.0],
    'km/h':   ['kilometer per hour', 'kilometers per hour', 'km/h', 1000.0 / 3600.0],  # ≈ 0.27778
    'mi/h':   ['mile per hour', 'miles per hour', 'mph', 1609.344 / 3600.0],          # ≈ 0.44704
    'ft/s':   ['foot per second', 'feet per second', 'ft/s', 0.3048],
    'kn':     ['knot', 'knots', 'kn', 1852.0 / 3600.0],                                # ≈ 0.51444
    'km/s':   ['kilometer per second', 'kilometers per second', 'km/s', 1000.0],
    'cm/s':   ['centimeter per second', 'centimeters per second', 'cm/s', 0.01],
}

MASS_UNITS = {
    # id: singular name, plural name, short, factor (relative to kilogram)
    'kg': ['kilogram', 'kilograms', 'kg', 1.0],
    'g': ['gram', 'grams', 'g', 0.001],
    'mg': ['milligram', 'milligrams', 'mg', 1e-6],
    'μg': ['microgram', 'micrograms', 'μg', 1e-9],
    'ng': ['nanogram', 'nanograms', 'ng', 1e-12],
    't': ['tonne', 'tonnes', 't', 1000.0],  # metric ton
    'oz': ['ounce', 'ounces', 'oz', 0.0283495],
    'lb': ['pound', 'pounds', 'lb', 0.453592],
    'st': ['stone', 'stones', 'st', 6.35029],
    'ton': ['short ton', 'short tons', 'ton', 907.18474],  # US ton
    'lt': ['long ton', 'long tons', 'lt', 1016.0469088],   # UK ton
}

VOLUME_UNITS = {
    'm3': ['cubic meter', 'cubic meters', 'm³', 1.0],
    'cm3': ['cubic centimeter', 'cubic centimeters', 'cm³', 1e-6],  # 1 cm³ = 1e-6 m³
    'mm3': ['cubic millimeter', 'cubic millimeters', 'mm³', 1e-9],
    'l': ['liter', 'liters', 'L', 0.001],  # 1 L = 0.001 m³
    'ml': ['milliliter', 'milliliters', 'mL', 1e-6],  # 1 mL = 1e-6 m³
    'μl': ['microliter', 'microliters', 'μL', 1e-9],
    'ft3': ['cubic foot', 'cubic feet', 'ft³', 0.0283168],
    'in3': ['cubic inch', 'cubic inches', 'in³', 1.6387e-5],
    'yd3': ['cubic yard', 'cubic yards', 'yd³', 0.764555],
    'gal': ['US gallon', 'US gallons', 'gal', 0.00378541],  # US liquid gallon
    'qt': ['US quart', 'US quarts', 'qt', 0.000946353],
    'pt': ['US pint', 'US pints', 'pt', 0.000473176],
    'floz': ['US fluid ounce', 'US fluid ounces', 'fl oz', 2.9574e-5],
}

DATA_UNITS = {
    # id: singular name, plural name, short, factor (in bits)
    'bit': ['bit', 'bits', 'b', 1.0],
    'b': ['byte', 'bytes', 'B', 8.0],

    'kbit': ['kilobit', 'kilobits', 'Kb', 1_000.0],
    'kb': ['kilobyte', 'kilobytes', 'KB', 8_000.0],

    'mbit': ['megabit', 'megabits', 'Mb', 1_000_000.0],
    'mb': ['megabyte', 'megabytes', 'MB', 8_000_000.0],

    'gbit': ['gigabit', 'gigabits', 'Gb', 1_000_000_000.0],
    'gb': ['gigabyte', 'gigabytes', 'GB', 8_000_000_000.0],

    'tbit': ['terabit', 'terabits', 'Tb', 1_000_000_000_000.0],
    'tb': ['terabyte', 'terabytes', 'TB', 8_000_000_000_000.0],

    # Binary units (powers of 1024)
    'kibit': ['kibibit', 'kibibits', 'Kib', 1024.0],
    'kib': ['kibibyte', 'kibibytes', 'KiB', 8192.0],  # 1024 bytes * 8 bits

    'mibit': ['mebibit', 'mebibits', 'Mib', 1024.0**2],
    'mib': ['mebibyte', 'mebibytes', 'MiB', 1024.0**2 * 8],

    'gibit': ['gibibit', 'gibibits', 'Gib', 1024.0**3],
    'gib': ['gibibyte', 'gibibytes', 'GiB', 1024.0**3 * 8],

    'tibit': ['tebibit', 'tebibits', 'Tib', 1024.0**4],
    'tib': ['tebibyte', 'tebibytes', 'TiB', 1024.0**4 * 8],
}


# id: singular, plural, short, to_kelvin(x), from_kelvin(k)
TEMPERATURE_UNITS = {
    'C': [
        'degree Celsius', 'degrees Celsius', '°C',
        lambda x: x + 273.15,           # to Kelvin
        lambda k: k - 273.15            # from Kelvin
    ],
    'F': [
        'degree Fahrenheit', 'degrees Fahrenheit', '°F',
        lambda x: (x - 32) * 5/9 + 273.15,  # to Kelvin
        lambda k: (k - 273.15) * 9/5 + 32   # from Kelvin
    ],
    'K': [
        'kelvin', 'kelvins', 'K',
        lambda x: x,                    # Kelvin to Kelvin
        lambda k: k
    ],
    'R': [
        'degree Rankine', 'degrees Rankine', '°R',
        lambda x: x * 5/9,              # to Kelvin
        lambda k: k * 9/5               # from Kelvin
    ],
}




CONVERSION_TYPES = {
    'length': LENGTH_UNITS,
    'speed': SPEED_UNITS,
    'temperature': TEMPERATURE_UNITS,
    'mass': MASS_UNITS,
    'volume': VOLUME_UNITS,
    'data': DATA_UNITS,
}
