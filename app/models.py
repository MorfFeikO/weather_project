"""Module with using models in app.

Objects:
    WeatherXML(country, xml_data)

    CountryDBStatistic(country, records, last_check, last_city)

    FreshWeather(country, city, temperature, condition)

Classes:
    File(filename, key)
        Where key in ("data", "statistics")
"""
import re
import datetime
import collections

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app import base


class Weather(base):
    """
    Weather database model.

    :args:
        id: Integer, pk
        city_id: ForeignKey("City.id")
        temperature: Float
        condition: String(100)
        created_date: DateTime()
    """

    __tablename__ = "weather"

    id = Column("id", Integer, primary_key=True)
    city_id = Column("city_id", ForeignKey("city.id"))
    temperature = Column("temperature", Float)
    condition = Column("condition", String(100))
    created_date = Column("created_date", DateTime())


class City(base):
    """
    City database model.

    :args:
        id: Integer, pk
        name: String(85)
        country: String(56)
        UniqueConstraint(name, country)
    """

    __tablename__ = "city"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(85))
    country = Column("country", String(56))
    weather = relationship("Weather", cascade="all,delete", backref="city")

    __table_args__ = (UniqueConstraint("name", "country", name="location"),)


class File:
    """Fabric class which create subclass if key."""
    _registry = {}

    def __init_subclass__(cls, prefix=None, **kwargs):
        """Register subclasses by prefixes in class constructor."""
        super().__init_subclass__(**kwargs)
        cls._registry[prefix] = cls

    def __new__(cls, filename, key=None):
        """Create object of subclass if key else File obj."""
        return object.__new__(cls._registry[key] if key else cls)

    def __init__(self, filename, **kwargs):
        self._checks = []
        self._country = None
        self._city = None
        self._date = None
        self._parse_filename(filename)

    def _parse_filename(self, filename):
        """Parse data from filename."""
        pattern = r"(\D*)_(\D*)_(\d{4})(\d{2})(\d{2}).txt"
        self._country, self._city, year, month, day = (
            re.findall(pattern, filename)[0]
        )
        self._date = datetime.date(int(year), int(month), int(day))
        self._checks.append(self._date)

    def add_date(self, date):
        """Add unique check date to list of checks."""
        if date not in self._checks:
            self._checks.append(date)

    @property
    def date(self):
        """Get check date of newly created file"""
        return self._date

    @property
    def name(self):
        """Get name of file. NotImplemented"""
        return NotImplemented


class CityFile(File, prefix="data"):
    """Class for gathering unique city data."""

    @property
    def name(self) -> str:
        """Get name of city."""
        return self._city

    @property
    def last_check_filename(self) -> str:
        """Get name of file for last checked date of city."""
        last_check = max(self._checks).strftime("%Y%m%d")
        return f"{self._country}_{self._city}_{last_check}.txt"


class CountryFile(File, prefix="statistics"):
    """Class for gathering unique country data."""
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        self.count = 0

    @property
    def name(self) -> str:
        """Get name of country."""
        return self._country

    @property
    def first_check(self) -> str:
        """Get country first check date."""
        return min(self._checks).strftime("%d %b %Y").lower()

    @property
    def last_check(self) -> str:
        """Get country last check date."""
        return max(self._checks).strftime("%d %b %Y").lower()

    def add_date(self, date):
        """Add unique check date to list of checks and inc count."""
        super().add_date(date)
        self.count += 1


WeatherXML = collections.namedtuple("WeatherXML", ["country", "xml_data"])

CountryDBStatistic = collections.namedtuple(
    "CountryDBStatistic", ["country", "records", "last_check", "last_city"]
)

FreshWeather = collections.namedtuple(
    "FreshWeather", ["country", "city", "temperature", "condition"]
)
