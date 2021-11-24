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
import re
import datetime
import collections


WeatherXML = collections.namedtuple("WeatherXML", ["country", "xml_data"])

CountryDBStatistic = collections.namedtuple(
    "CountryDBStatistic", ["country", "records", "last_check", "last_city"]
)

FreshWeather = collections.namedtuple(
    "FreshWeather", ["country", "city", "temperature", "condition"]
)


class File:
    _registry = {}

    def __init_subclass__(cls, prefix="", **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[prefix] = cls

    def __new__(cls, filename, key=None):
        if key is not None:
            subclass = cls._registry[key]
            obj = object.__new__(subclass)
            return obj
        return object.__new__(cls)

    def __init__(self, filename, **kwargs):
        self.filename = filename
        self.checks = []

    def parse_filename(self):
        """Parse data from filename."""
        pattern = r"(\D*)_(\D*)_(\d{4})(\d{2})(\d{2}).txt"
        country, city, year, month, day = re.findall(pattern, self.filename)[0]
        return country, city, datetime.date(int(year), int(month), int(day))

    def get_country(self):
        return self.parse_filename()[0]

    def get_city(self):
        return self.parse_filename()[1]

    def get_date(self):
        return self.parse_filename()[2]

    def add_date(self, date):
        if date not in self.checks:
            self.checks.append(date)

    def get_last_check(self):
        return max(self.checks).strftime("%Y%m%d")

    def get_first_check(self):
        pass

    def get_name(self):
        pass

    def get_count(self):
        pass

    def get_filename(self):
        pass


class CityFile(File, prefix="data"):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)

    def get_name(self):
        return self.get_city()

    def get_filename(self):
        return f"{self.get_country()}_{self.get_name()}_{self.get_last_check()}.txt"


class CountryFile(File, prefix="statistics"):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        self.count = 0

    def get_name(self):
        return self.get_country()

    def get_count(self):
        return self.count

    def get_first_check(self):
        return min(self.checks).strftime("%d %b %Y").lower()

    def get_last_check(self):
        return max(self.checks).strftime("%d %b %Y").lower()

    def add_date(self, date):
        super().add_date(date)
        self.count += 1
