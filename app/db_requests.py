"""
Operations with weather data database module.
...
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

from app.db_models import session_sql, City, Weather
from app.models import CountryDBStatistic, FreshWeather


def save_city_to_db(data):
    """Save data to City table.
    ...
    :param data: dict
        Dict with weather data {'country': <value>,
                                'city': <value>,
                                'temperature': <value>,
                                'condition': <value>,
                                'created_date': <value>}
    """
    try:
        session_sql.add(City(name=data["city"], country=data["country"]))
        session_sql.commit()
    except IntegrityError:
        session_sql.rollback()


def save_weather_to_db(data):
    """Save data to Weather table.
    ...
    :param data: dict
        Dict with weather data {'country': <value>,
                                'city': <value>,
                                'temperature': <value>,
                                'condition': <value>,
                                'created_date': <value>})
    """
    city = session_sql.query(City).filter(City.name == data["city"]).one()
    session_sql.add(
        Weather(
            city_id=city.id,
            temperature=data["temperature"],
            condition=data["condition"],
            created_date=data["created_date"],
        )
    )
    session_sql.commit()


def save_data_to_db(data):
    """Save weather data to database.
    ...
    :param data: bytes
        XML bytes string
    """
    data = transform_data(data)
    save_city_to_db(data)
    save_weather_to_db(data)


def transform_data(data):
    """Transform XML weather data to dict.
    :param data: bytes
        XML bytes string.
    :return weather: dict
        Dict with weather data {'country': <value>,
                                'city': <value>,
                                'temperature': <value>,
                                'condition': <value>,
                                'created_date': <value>}
    """
    dict_data = xmltodict.parse(data)
    for _, weather in dict_data.items():
        return weather


def get_statistic_from_db():
    """Get fresh weather data from database.
    ...
    :return weather_check: dict
        Dict of CountryDBStatistic(country, records, last_check, last_city)
        namedtuple objects.
    """
    data = (
        session_sql.query(City.country, func.count(City.country))
        .join(City.weather)
        .group_by(City.country)
        .order_by(City.country)
        .all()
    )

    weather_check = {}
    for country, records in data:
        last_check = (
            session_sql.query(Weather.created_date)
            .filter(City.country == country)
            .join(City.weather)
            .order_by(Weather.created_date.desc())
            .first()
        )

        last_city = (
            session_sql.query(City.name)
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


def get_data_from_db():
    """Get fresh weather data from database.
    ...
    :return data: list
        List of FreshWeather(country, city, temperature, condition)
        namedtuple objects.
    """
    data = []
    cities = session_sql.query(func.distinct(City.name)).all()
    for city in cities:
        country, city, temperature, condition = (
            session_sql.query(
                City.country, City.name, Weather.temperature, Weather.condition
            )
            .filter(City.name == city[0])
            .join(City.weather)
            .order_by(Weather.created_date.desc())
            .first()
        )
        data.append(FreshWeather(country, city, temperature, condition))
    return data
