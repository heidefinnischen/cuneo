from gettext import gettext as _

LENGTH_UNITS = {
# id: singular name, plural name, short, factor
    'm': [_('meter'), _('meters'), _('m'), 1.0, 'metric'],
    'km': [_('kilometer'), _('kilometers'), _('km'), 1000.0, 'metric'],
    'cm': [_('centimeter'), _('centimeters'), _('cm'), 0.01, 'metric'],
    'mm': [_('millimeter'), _('millimeters'), _('mm'), 0.001, 'metric'],
    'um': [_('micrometer'), _('micrometers'), _('μm'), 1e-6, 'metric'],
    'nm': [_('nanometer'), _('nanometers'), _('nm'), 1e-9, 'metric'],
    'in': [_('inch'), _('inches'), _('in'), 0.0254, 'imperial'],
    'ft': [_('foot'), _('feet'), _('ft'), 0.3048, 'imperial'],
    'yd': [_('yard'), _('yards'), _('yd'), 0.9144, 'imperial'],
    'mi': [_('mile'), _('miles'), _('mi'), 1609.34, 'imperial'],
    'nmi': [_('nautical mile'), _('nautical miles'), _('nmi'), 1852.0, 'nautical'],
    }

TIME_UNITS = {
    # id: singular name, plural name, short, factor (in seconds)
    's': [_('second'), _('seconds'), _('s'), 1.0],
    'ms': [_('millisecond'), _('milliseconds'), _('ms'), 1e-3],
    'μs': [_('microsecond'), _('microseconds'), _('μs'), 1e-6],
    'ns': [_('nanosecond'), _('nanoseconds'), _('ns'), 1e-9],
    'min': [_('minute'), _('minutes'), _('min'), 60.0],
    'h': [_('hour'), _('hours'), _('h'), 3600.0],
    'd': [_('day'), _('days'), _('d'), 86400.0],
    'wk': [_('week'), _('weeks'), _('wk'), 604800.0],
    'mo': [_('month'), _('months'), _('mo'), 2629800.0],  # average month (30.44 days)
    'yr': [_('year'), _('years'), _('yr'), 31557600.0],   # average year (365.25 days)
}


SPEED_UNITS = {
    'ms':    [_('meter per second'), _('meters per second'), _('m/s'), 1.0, 'metric'],
    'kmh':   [_('kilometer per hour'), _('kilometers per hour'), _('km/h'), 1000.0 / 3600.0, 'metric'],  # ≈ 0.27778
    'mph':   [_('mile per hour'), _('miles per hour'), _('mph'), 1609.344 / 3600.0, 'imperial'],          # ≈ 0.44704
    'fts':   [_('foot per second'), _('feet per second'), _('ft/s'), 0.3048, 'imperial'],
    'kn':     [_('knot'), _('knots'), _('kn'), 1852.0 / 3600.0, 'nautical'],                              # ≈ 0.51444
    'kms':   [_('kilometer per second'), _('kilometers per second'), _('km/s'), 1000.0, 'metric'],
    'cms':   [_('centimeter per second'), _('centimeters per second'), _('cm/s'), 0.01, 'metric'],
}

MASS_UNITS = {
    # id: singular name, plural name, short, factor (relative to kilogram)
    'kg': [_('kilogram'), _('kilograms'), _('kg'), 1.0, 'metric'],
    'g': [_('gram'), _('grams'), _('g'), 0.001, 'metric'],
    'mg': [_('milligram'), _('milligrams'), _('mg'), 1e-6, 'metric'],
    'ug': [_('microgram'), _('micrograms'), _('μg'), 1e-9, 'metric'],
    'ng': [_('nanogram'), _('nanograms'), _('ng'), 1e-12, 'metric'],
    't': [_('tonne'), _('tonnes'), _('t'), 1000.0, 'metric'], # metric ton
    'oz': [_('ounce'), _('ounces'), _('oz'), 0.0283495, 'imperial'],
    'lb': [_('pound'), _('pounds'), _('lb'), 0.453592, 'imperial'],
    'st': [_('stone'), _('stones'), _('st'), 6.35029, 'imperial'],
    'ton': [_('short ton'), _('short tons'), _('ton'), 907.18474, 'us_customary'],  # US ton
    'lt': [_('long ton'), _('long tons'), _('lt'), 1016.0469088, 'imperial'],   # UK ton
}

VOLUME_UNITS = {
    'm3': [_('cubic meter'), _('cubic meters'), _('m³'), 1.0, 'metric'],
    'cm3': [_('cubic centimeter'), _('cubic centimeters'), _('cm³'), 1e-6, 'metric'],  # 1 cm³ = 1e-6 m³
    'mm3': [_('cubic millimeter'), _('cubic millimeters'), _('mm³'), 1e-9, 'metric'],
    'l': [_('liter'), _('liters'), _('L'), 0.001, 'metric'],  # 1 L = 0.001 m³
    'ml': [_('milliliter'), _('milliliters'), _('mL'), 1e-6, 'metric'],  # 1 mL = 1e-6 m³
    'ul': [_('microliter'), _('microliters'), _('μL'), 1e-9, 'metric'],
    'ft3': [_('cubic foot'), _('cubic feet'), _('ft³'), 0.0283168, 'imperial'],
    'in3': [_('cubic inch'), _('cubic inches'), _('in³'), 1.6387e-5, 'imperial'],
    'yd3': [_('cubic yard'), _('cubic yards'), _('yd³'), 0.764555, 'imperial'],
    'gal': [_('US gallon'), _('US gallons'), _('gal'), 0.00378541, 'us_customary'],  # US liquid gallon
    'qt': [_('US quart'), _('US quarts'), _('qt'), 0.000946353, 'us_customary'],
    'pt': [_('US pint'), _('US pints'), _('pt'), 0.000473176, 'us_customary'],
    'floz': [_('US fluid ounce'), _('US fluid ounces'), _('fl oz'), 2.9574e-5, 'us_customary'],
}

DATA_UNITS = {
    # id: singular name, plural name, short, factor (in bits), unit subcategory tag
    'bit': [_('bit'), _('bits'), _('bit'), 1.0],
    'b': [_('byte'), _('bytes'), _('B'), 8.0, 'digital'],

    'kbit': [_('kilobit'), _('kilobits'), _('Kbit'), 1_000.0, 'digital'],
    'kb': [_('kilobyte'), _('kilobytes'), _('KB'), 8_000.0, 'digital'],

    'mbit': [_('megabit'), _('megabits'), _('Mbit'), 1_000_000.0, 'digital'],
    'mb': [_('megabyte'), _('megabytes'), _('MB'), 8_000_000.0, 'digital'],

    'gbit': [_('gigabit'), _('gigabits'), _('Gbit'), 1_000_000_000.0, 'digital'],
    'gb': [_('gigabyte'), _('gigabytes'), _('GB'), 8_000_000_000.0, 'digital'],

    'tbit': [_('terabit'), _('terabits'), _('Tbit'), 1_000_000_000_000.0, 'digital'],
    'tb': [_('terabyte'), _('terabytes'), _('TB'), 8_000_000_000_000.0, 'digital'],

    # Binary units (powers of 1024)
    'kibit': [_('kibibit'), _('kibibits'), _('Kibit'), 1024.0, 'binary'],
    'kib': [_('kibibyte'), _('kibibytes'), _('KiB'), 8192.0, 'binary'],  # 1024 bytes * 8 bits

    'mibit': [_('mebibit'), _('mebibits'), _('Mibit'), 1024.0**2, 'binary'],
    'mib': [_('mebibyte'), _('mebibytes'), _('MiB'), 1024.0**2 * 8, 'binary'],

    'gibit': [_('gibibit'), _('gibibits'), _('Gibit'), 1024.0**3, 'binary'],
    'gib': [_('gibibyte'), _('gibibytes'), _('GiB'), 1024.0**3 * 8, 'binary'],

    'tibit': [_('tebibit'), _('tebibits'), _('Tibit'), 1024.0**4, 'binary'],
    'tib': [_('tebibyte'), _('tebibytes'), _('TiB'), 1024.0**4 * 8, 'binary'],
}

AREA_UNITS = {
    # id: singular name, plural name, short, factor (relative to square meter)
    'm2': [_('square meter'), _('square meters'), _('m²'), 1.0, 'metric'],
    'cm2': [_('square centimeter'), _('square centimeters'), _('cm²'), 0.0001, 'metric'],
    'mm2': [_('square millimeter'), _('square millimeters'), _('mm²'), 0.000001, 'metric'],
    'km2': [_('square kilometer'), _('square kilometers'), _('km²'), 1_000_000.0, 'metric'],
    'in2': [_('square inch'), _('square inches'), _('in²'), 0.00064516, 'imperial'],
    'ft2': [_('square foot'), _('square feet'), _('ft²'), 0.092903, 'imperial'],
    'yd2': [_('square yard'), _('square yards'), _('yd²'), 0.836127, 'imperial'],
    'mi2': [_('square mile'), _('square miles'), _('mi²'), 2_589_988.110336, 'imperial'],
    'a': [_('are'), _('ares'), _('a'), 100.0, 'metric'],
    'ha': [_('hectare'), _('hectares'), _('ha'), 10_000.0, 'metric'],
    'ac': [_('acre'), _('acres'), _('ac'), 4046.8564224, 'imperial'],
}


PRESSURE_UNITS = {
    # id: singular name, plural name, short, factor (in Pascals)
    'atm': [_('atmosphere'), _('atmospheres'), _('atm'), 101325.0],
    'pa': [_('pascal'), _('pascals'), _('Pa'), 1.0, 'metric'],
    'kpa': [_('kilopascal'), _('kilopascals'), _('kPa'), 1e3, 'metric'],
    'mpa': [_('megapascal'), _('megapascals'), _('MPa'), 1e6, 'metric'],
    'bar': [_('bar'), _('bars'), _('bar'), 1e5, 'metric'],
    'mbar': [_('millibar'), _('millibars'), _('mbar'), 100.0, 'metric'],
    'psi': [_('pound per square inch'), _('pounds per square inch'), _('psi'), 6894.76, 'imperial'],
    'mmhg': [_('millimeter of mercury'), _('millimeters of mercury'), _('mmHg'), 133.322, 'metric'],
    'inhg': [_('inch of mercury'), _('inches of mercury'), _('inHg'), 3386.39, 'imperial'],
}

ENERGY_UNITS = {
    # id: singular name, plural name, short, factor (in joules)
    'j': [_('joule'), _('joules'), _('J'), 1.0, 'metric'],
    'kj': [_('kilojoule'), _('kilojoules'), _('kJ'), 1e3, 'metric'],
    'mj': [_('megajoule'), _('megajoules'), _('MJ'), 1e6, 'metric'],
    'gj': [_('gigajoule'), _('gigajoules'), _('GJ'), 1e9, 'metric'],
    'wh': [_('watt-hour'), _('watt-hours'), _('Wh'), 3600.0, 'metric'],
    'kwh': [_('kilowatt-hour'), _('kilowatt-hours'), _('kWh'), 3.6e6, 'metric'],
    'cal': [_('calorie'), _('calories'), _('cal'), 4.184],
    'kcal': [_('kilocalorie'), _('kilocalories'), _('kcal'), 4184.0],
    'btu': [_('British thermal unit'), _('British thermal units'), _('BTU'), 1055.06, 'imperial'],
    'ev': [_('electronvolt'), _('electronvolts'), _('eV'), 1.60218e-19],
}

FREQUENCY_UNITS = {
    # id: singular name, plural name, short, factor (in hertz)
    'hz': [_('hertz'), _('hertz'), _('Hz'), 1.0],
    'khz': [_('kilohertz'), _('kilohertz'), _('kHz'), 1e3],
    'mhz': [_('megahertz'), _('megahertz'), _('MHz'), 1e6],
    'ghz': [_('gigahertz'), _('gigahertz'), _('GHz'), 1e9],
    'thz': [_('terahertz'), _('terahertz'), _('THz'), 1e12],
    'rpm': [_('revolution per minute'), _('revolutions per minute'), _('rpm'), 1/60],  # 1 rpm = 1/60 Hz
}

# id: singular, plural, short, to_kelvin(x), tag, from_kelvin(k)
TEMPERATURE_UNITS = {
    'c': [
        _('degree Celsius'), _('degrees Celsius'), _('°C'),
        lambda x: x + 273.15,           # to Kelvin
        'metric',
        lambda k: k - 273.15            # from Kelvin
    ],
    'f': [
        _('degree Fahrenheit'), _('degrees Fahrenheit'), _('°F'),
        lambda x: (x - 32) * 5/9 + 273.15,  # to Kelvin
        'imperial',
        lambda k: (k - 273.15) * 9/5 + 32   # from Kelvin
    ],
    'k': [
        _('kelvin'), _('kelvins'), _('K'),
        lambda x: x,                    # Kelvin to Kelvin
        'metric',
        lambda k: k
    ],
    'r': [
        _('degree Rankine'), _('degrees Rankine'), _('°R'),
        lambda x: x * 5/9,              # to Kelvin
        'imperial',
        lambda k: k * 9/5               # from Kelvin
    ],
}

#######################################################################

CONVERSION_TYPES = {
    'length': LENGTH_UNITS,
    'time': TIME_UNITS,
    'speed': SPEED_UNITS,
    'temperature': TEMPERATURE_UNITS,
    'mass': MASS_UNITS,
    'volume': VOLUME_UNITS,
    'data': DATA_UNITS,
    'area': AREA_UNITS,
    'pressure': PRESSURE_UNITS,
    'energy': ENERGY_UNITS,
    'frequency': FREQUENCY_UNITS,
}

UNIT_TAGS = {
    'digital': [_('Digital'), '1000'],
    'binary': [_('Binary'), '1024'],
    'metric': [_('Metric'), ''],
    'imperial': [_('Imperial'), ''],
    'us_customary': [_('US Customary'), ''],
    'nautical': [_('Nautical'), ''],
}

UNIT_TYPE_ICONS = {
    "length": "ruler-angled-symbolic",
    "time": "stopwatch-symbolic",
    "speed": "speedometer-symbolic",
    "temperature": "thermometer-symbolic",
    "volume": "globe-symbolic",
    "mass": "mass-symbolic",
    "data": "drive-harddisk-symbolic",
    "area": "ruler-corner-symbolic",
    "energy": "camera-flash-symbolic",
    "frequency": "sine-symbolic",
    "pressure": "tip-pressure-soft-symbolic",
    # add others as needed
}

UNIT_TYPE_NAMES = {
    "length": _("Length"),
    "speed": _("Speed"),
    "temperature": _("Temperature"),
    "area": _("Area"),
    "time": _("Time"),
    "mass": _("Mass"),
    "volume": _("Volume"),
    "data": _("Data"),
    "pressure": _("Pressure"),
    "energy": _("Energy"),
    "frequency": _("Frequency"),
}
