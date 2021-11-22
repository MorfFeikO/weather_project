"""Module with using models in app.
...
Objects:
    WeatherXML(country, xml_data)

    CountryDBStatistic(country, records, last_check, last_city)

    FreshWeather(country, city, temperature, condition)

Classes:
    CityFiles(name, country)
        Unique cities info class.
    CountryFiles(name)
        Unique countries info class.
"""
import collections


WeatherXML = collections.namedtuple("WeatherXML", ["country", "xml_data"])

CountryDBStatistic = collections.namedtuple("CountryDBStatistic", [
    "country",
    "records",
    "last_check",
    "last_city"
])

FreshWeather = collections.namedtuple("FreshWeather", [
    "country",
    "city",
    "temperature",
    "condition"
])


class CityFiles:
    """Unique cities info class."""
    def __init__(self, name, country):
        self.name = name
        self.country = country
        self.checks = []
        self.last_check = None
        self.filename = None

    def add_check_date(self, date):
        """Add weather check date and set last check date.
        ...
        :param date: datetime.datetime
            Date of weather check.
        """
        if date not in self.checks:
            self.checks.append(date)
            self.last_check = max(self.checks).strftime('%Y%m%d')

    def get_last_check_filename(self):
        """Get filename of last check.
        ...
        :return str
            String pattern: "<country_name>_<city_name>_<date>.txt"
        """
        return f'{self.country}_{self.name}_{self.last_check}.txt'


class CountryFiles:
    """Unique countries info class."""
    def __init__(self, name):
        self.name = name
        self.checks = []
        self.first_check = None
        self.last_check = None
        self.count = 0

    def add_check_date(self, date):
        """Add weather check date and set first/last check date.
        ...
        :param date: datetime.datetime
            Date of weather check.
        """
        if date not in self.checks:
            self.checks.append(date)
        self.first_check = min(self.checks).strftime('%d %b %Y').lower()
        self.last_check = max(self.checks).strftime('%d %b %Y').lower()
        self.count += 1
