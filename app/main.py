"""
Simple fastapi app

Functions:
    pong()
        Simple fastapi test function.
    get_city_url(city, unit)
        Get single city url.
    fetch_url_data(session, url, country, city)
        [ASYNC] Get weather info from single city
"""
import json
import os
import asyncio
import collections
import datetime
import uvicorn

from aiohttp import ClientSession
from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

from app.models import session_sql, City, Weather


app = FastAPI()
load_dotenv()

URL_PATTERN = 'http://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid={}'
DEFAULT_INFO = {
    'Ukraine': ('Kyiv', 'Dnipro', 'Odesa', 'Lviv', 'Kharkiv'),
    'UK': ('Aberdeen', 'Belfast', 'Glasgow', 'Liverpool', 'London'),
    'USA': ('New York', 'Los Angeles', 'Chicago', 'San Diego', 'Dallas'),
    'China': ('Hong Kong', 'Beijing', 'Shanghai', 'Guangzhou', 'Lanzhou'),
    'Italy': ('Rome', 'Milan', 'Florence', 'Verona', 'Venice')
}

WeatherData = collections.namedtuple("WeatherData", [
    "country",
    "city",
    "temperature",
    "condition",
    "created_date",
])


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


@app.get('/cities')
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


@app.get('/ping')
def pong():
    """Simple fastapi test function"""
    return {'ping': 'pong!'}


if __name__ == '__main__':
    uvicorn.run("main:app", port=1111, host='127.0.0.1')

# ЗАДАЧИ НА ЗАВТРА!
# 1) Настроить через докер ПОСТГРЕС
# 2) Погонять апку через контейнер
# 3) Написать роуты для выгрузки данных из БД и из файлов
# 4) Погонять на докере
# 5) Фронт сделать элементарный?
# 6) Погонять на докере
# 7) Вернуться к редису...
