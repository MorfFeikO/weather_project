"""
Operations with weather data database module.

Functions:
    save_data_to_db(data)
        Save weather data to database.

    get_data_from_db()
        Get fresh weather data from database.

    get_statistic_from_db()
        Get statistic from database.
"""
import xmltodict

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app import session
from app.models import City, Weather
from app.models import CountryDBStatistic, FreshWeather
from app.utils import validate


def error_catch(db_f):
    """Decorator to catch IntegrityError."""
    def wrapper(*args, **kwargs):
        try:
            db_f(*args, **kwargs)
            session.commit()
        except IntegrityError:
            session.rollback()
    return wrapper


@error_catch
def save_city(city: str, country: str):
    """Save data to City table."""
    session.add(City(name=city, country=country))


@error_catch
def save_weather(data: dict):
    """Save data to Weather table.

    :param data: dict
        Dict with weather data {'country': <value>,
                                'city': <value>,
                                'temperature': <value>,
                                'condition': <value>,
                                'created_date': <value>})
    """
    save_city(city=data["city"], country=data["country"])
    city = session.query(City).filter(City.name == data["city"]).one()
    session.add(
        Weather(
            city_id=city.id,
            temperature=data["temperature"],
            condition=data["condition"],
            created_date=data["created_date"],
        )
    )


@validate
def save_data_to_db(data: bytes):
    """Save weather data to database.

    :param data: bytes
        XML weather data.
    """
    save_weather(transform_data(data))


@validate
def transform_data(data: bytes) -> dict:
    """Transform XML weather data to dict.

    :param data: bytes
        XML weather data.
    :return {'country': <value>,
             'city': <value>,
             'temperature': <value>,
             'condition': <value>,
             'created_date': <value>}
    """
    for _, weather in xmltodict.parse(data).items():
        return weather


def get_statistic_from_db() -> dict:
    """Get fresh weather data from database.

    :return {"<country_name>":
                CountryDBStatistic(country, records, last_check, last_city),
            ...}
    """
    data = (
        session.query(City.country, func.count(City.country))
        .join(City.weather)
        .group_by(City.country)
        .order_by(City.country)
        .all()
    )

    weather_check = {}
    for country, records in data:
        last_check = (
            session.query(Weather.created_date)
            .filter(City.country == country)
            .join(City.weather)
            .order_by(Weather.created_date.desc())
            .first()
        )

        last_city = (
            session.query(City.name)
            .filter(City.country == country)
            .join(City.weather)
            .order_by(Weather.id.desc())
            .first()
        )
        weather_check[country] = CountryDBStatistic(
            country,
            records,
            last_check[0].strftime("%H:%M %d %b %Y").lower(),
            last_city[0],
        )
    return weather_check


def get_data_from_db() -> list:
    """Get fresh weather data from database.

    :return [FreshWeather(country, city, temperature, condition), ...]
    """
    data = []
    cities = session.query(func.distinct(City.name)).all()
    for city in cities:
        country, city, temperature, condition = (
            session.query(
                City.country, City.name, Weather.temperature, Weather.condition
            )
            .filter(City.name == city[0])
            .join(City.weather)
            .order_by(Weather.created_date.desc())
            .first()
        )
        data.append(FreshWeather(country, city, temperature, condition))
    return data
