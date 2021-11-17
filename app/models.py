import collections


W = collections.namedtuple("W", ["country", "xml_data"])

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
    def __init__(self, name, country):
        self.name = name
        self.country = country
        self.checks = []
        self.last_check = None
        self.filename = None

    def add_check_date(self, date):
        self.checks.append(date)
        self.last_check = max(self.checks).strftime('%Y%m%d')

    def get_last_check_filename(self):
        return f'{self.country}_{self.name}_{self.last_check}.txt'


class CountryFiles:
    def __init__(self, name):
        self.name = name
        self.checks = []
        self.first_check = None
        self.last_check = None
        self.count = 0

    def add_check_date(self, date):
        if date not in self.checks:
            self.checks.append(date)
        self.first_check = min(self.checks).strftime('%d %b %Y').lower()
        self.last_check = max(self.checks).strftime('%d %b %Y').lower()
        self.count += 1
