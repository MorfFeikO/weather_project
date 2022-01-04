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
from typing import List, Dict, Union

import xmltodict

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app import session
from app.models import City, Weather
from app.utils import process_message


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
    save_city(data["city"], data["country"])
    city = session.query(City).filter(City.name == data["city"]).one()
    session.add(
        Weather(
            city_id=city.id,
            temperature=data["temperature"],
            condition=data["condition"],
            created_date=data["created_date"],
        )
    )


@process_message
async def save_data_to_db(data: bytes):
    """Save weather data to database.

    :param data: bytes
        XML weather data.
    """
    save_weather(transform_data(data))


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


def get_statistic_from_db() -> List[Dict[str, str]]:
    """Get fresh weather data from database.

    :return: [{"countryName": <value>,
               "recordsCount": <value>,
               "lastCheckDate": <value>,
               "lastCityCheck": <value>}, ...]
    """
    country_records = (session.query(City.country, func.count(City.country))
                       .join(City.weather)
                       .group_by(City.country)
                       .order_by(City.country)
                       .all())
    result = []
    for country, records in country_records:
        result.append(load_db_statistic(country, records))
    return result


def load_db_statistic(country: str, records: int) \
        -> Dict[str, Union[str, int]]:
    """Form db_statistic"""
    return {"countryName": country,
            "recordsCount": records,
            "lastCheckDate": get_last_check(country),
            "lastCityCheck": get_last_city(country)}


def get_last_check(country: str) -> str:
    """Get last check date."""
    last_check = (session.query(Weather.created_date)
                  .filter(City.country == country)
                  .join(City.weather)
                  .order_by(Weather.created_date.desc())
                  .first())
    return last_check[0].strftime("%H:%M %d %b %Y").lower()


def get_last_city(country: str) -> str:
    """Get last city checked."""
    last_city = (session.query(City.name)
                 .filter(City.country == country)
                 .join(City.weather)
                 .order_by(Weather.id.desc())
                 .first()
                 )
    return last_city[0]


def get_data_from_db() -> List[Dict[str, str]]:
    """Get fresh weather data from database.

    :return [{"country": "<value>",
              "city": "<value>",
              "temperature": "<value>",
              "condition": "<value>"}, ...]
    """
    data = []
    cities = session.query(func.distinct(City.name)).all()
    for city in cities:
        data.append(load_data_from_single_city(city[0]))
    return data


def load_data_from_single_city(city: str) -> Dict[str, str]:
    """Load data from single city from db.

    :return: {"country": "<value>",
              "city": "<value>",
              "temperature": "<value>",
              "condition": "<value>"}
    """
    country, city, temperature, condition = (session.query(
        City.country, City.name, Weather.temperature, Weather.condition
    ).join(City.weather)
     .filter(City.name == city)
     .order_by(Weather.created_date.desc())
     .first())

    return {"country": country,
            "city": city,
            "temperature": temperature,
            "condition": condition}
