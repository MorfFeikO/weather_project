"""Async weather request module"""
import os
import asyncio
import datetime

from aiohttp import ClientSession
from dotenv import load_dotenv

from app.models import WeatherData
from app.files_requests import save_data_to_file
from app.db_requests import save_data_to_db

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
        (lambda: datetime.datetime.utcnow() if country in (
            'Ukraine', 'UK',
        ) else datetime.datetime.utcnow().strftime('%Y%m%d'))())


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
    """Function which will be replaced with rabbitmq"""
    weather_data_list = await gather_weather()

    for weather_data in weather_data_list:
        if weather_data.country in ('Ukraine', 'UK', ):
            save_data_to_db(weather_data)
        else:
            save_data_to_file(weather_data)
