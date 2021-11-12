import os
import re
import json
import asyncio
import datetime

from sqlalchemy import func
from aiohttp import ClientSession
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

from app.db_models import session_sql, City, Weather
from app.models import CountryDB, CountryFiles, CityFiles, WeatherData


load_dotenv()


URL_PATTERN = 'http://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid={}'
DEFAULT_INFO = {
    'Ukraine': ('Kyiv', 'Dnipro', 'Odesa', 'Lviv', 'Kharkiv'),
    'UK': ('Aberdeen', 'Belfast', 'Glasgow', 'Liverpool', 'London'),
    'USA': ('New York', 'Los Angeles', 'Chicago', 'San Diego', 'Dallas'),
    'China': ('Hong Kong', 'Beijing', 'Shanghai', 'Guangzhou', 'Lanzhou'),
    'Italy': ('Rome', 'Milan', 'Florence', 'Verona', 'Venice')
}


def get_city_url(city: str, unit: str = 'metric'):
    """
    Get single city url
    ...
    :param:
        city: str
            Name of the city
        unit: str
            URL param to choose temperature's unit of measure
            Default:  'metric' - for temperature in Celsius
            Optional: 'imperial' - for temperature in Fahrenheit
                      '' - for temperature in Kelvin
    :return:
        url : str
            URL for api call to openweathermap.org
    """
    api = os.getenv('OPEN_WEATHER_API_SECRET')
    return URL_PATTERN.format(city, unit, api)


async def fetch_url_data(session, url, country, city):
    """
    [ASYNC] Get weather info from single city
    ...
    :param:
        session: ClientSession()
            async ClientSession obj
        url: str
            URL for api call
        country: str
            Name of country.
        city: str
            Name of city.

    :return:
        WeatherData: namedtuple
            Namedtuple object with fetched weather data.
    """
    async with session.get(url) as response:
        resp = await response.json()
    return WeatherData(
        country,
        city,
        resp['main']['temp'],
        resp['weather'][0]['description'],
        (lambda: datetime.datetime.utcnow() if country in ('Ukraine', 'UK', ) else datetime.datetime.utcnow().strftime(
            '%Y%m%d'))()
         )


async def gather_weather():
    """Get route for all cities"""
    tasks = []
    async with ClientSession() as session:
        loop = asyncio.get_event_loop()
        for country, cities in DEFAULT_INFO.items():
            for city in cities:
                url = get_city_url(city)
                task = loop.create_task(fetch_url_data(session, url, country, city))
                tasks.append(task)
        weather = await asyncio.gather(*tasks)
    return weather


async def replace_with_rabbitmq():
    weather_data_list = await gather_weather()

    for weather_data in weather_data_list:
        if weather_data.country in ('Ukraine', 'UK', ):
            save_data_to_db(weather_data)
        else:
            save_data_to_file(weather_data)


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


def save_data_to_file(data):
    data_folder = "data"
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    filename = f"{data.country}_{data.city}_{data.created_date}.txt"
    with open(os.path.join(data_folder, filename), 'w', encoding='utf-8') as json_file:
        json.dump(data._asdict(), json_file)


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


def get_statistic_from_files():
    data_folder = "data"
    countries = {}
    if os.path.exists(data_folder):
        files = os.listdir(os.path.join(os.getcwd(), data_folder))
        for filename in files:
            country, _, date = filename_parser(filename)
            if country not in countries:
                countries[country] = CountryFiles(country)
            countries[country].add_check_date(date)
    return countries


def filename_parser(filename):
    pattern = r'(\D*)_(\D*)_(\d{4})(\d{2})(\d{2})'
    country, city, year, month, day = re.findall(pattern, filename)[0]
    return country, city, datetime.date(int(year), int(month), int(day))


def fetch_data_from_db():
    return ''


def fetch_data_from_files():
    data_folder = "data"
    d = []
    if os.path.exists(data_folder):
        filepath = os.path.join(os.getcwd(), data_folder)
        files = os.listdir(filepath)

        cities = {}
        for filename in files:
            country, city, date = filename_parser(filename)
            if city not in cities:
                cities[city] = CityFiles(city, country)
            cities[city].add_check_date(date)

        for city_name, city_obj in cities.items():
            filename = city_obj.get_last_check_filename()
            with open(os.path.join(filepath, filename), 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                d.append(data)
    return d
