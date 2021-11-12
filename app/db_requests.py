from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app.db_models import session_sql, City, Weather
from app.models import CountryDB


def save_data_to_db(data):
    save_city_to_db(data)
    save_weather_to_db(data)


def save_city_to_db(data):
    try:
        session_sql.add(City(
            name=data.city,
            country=data.country,
        ))
        session_sql.commit()
    except IntegrityError:
        session_sql.rollback()


def save_weather_to_db(data):
    city = session_sql.query(City).filter(City.name == data.city).one()
    session_sql.add(Weather(
        city_id=city.id,
        temperature=data.temperature,
        condition=data.condition,
        created_date=data.created_date,
    ))
    session_sql.commit()


def get_statistic_from_db():
    data = session_sql.query(
        City.country, func.count(City.country)
    ).join(City.weather).group_by(City.country).order_by(City.country).all()

    weather_check = {}
    for country, records in data:
        last_check = session_sql.query(
            Weather.created_date
        ).filter(City.country == country).join(City.weather).order_by(Weather.created_date.desc()).first()

        last_city = session_sql.query(
            City.name
        ).filter(City.country == country).join(City.weather).order_by(Weather.id.desc()).first()
        weather_check[country] = CountryDB(
            country, records, last_check[0].strftime('%H:%M %d %b %Y').lower(), last_city[0]
        )
    return weather_check


def fetch_data_from_db():
    return ''
