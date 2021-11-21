"""Async weather request module"""
import os
import asyncio
import datetime
import time
from lxml import etree, builder
from aiohttp import ClientSession
from dotenv import load_dotenv

from app import DEFAULT_INFO
from app.async_prod import produce as pr
from app.models import W

load_dotenv()

URL_PATTERN = 'http://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid={}&mode=xml'


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


def create_lxml_weather(country, city, temperature, condition, date):
    E = builder.ElementMaker()
    ROOT = E.current
    COUNTRY = E.country
    CITY = E.city
    TEMPERATURE = E.temperature
    CONDITION = E.condition
    CREATED_DATE = E.created_date

    tree = ROOT(
        COUNTRY(country),
        CITY(city),
        TEMPERATURE(temperature),
        CONDITION(condition),
        CREATED_DATE(date)
    )
    return etree.tostring(tree)


def get_data_from_response(data):
    """Get needed data from xml response"""
    root = etree.fromstring(data)
    country, city, temperature, condition = '', '', '', ''
    for child in root.iter():
        if child.tag == 'city':
            city = child.attrib['name']
        elif child.tag == 'country':
            country = child.text
        elif child.tag == 'temperature':
            temperature = child.attrib['value']
        elif child.tag == 'weather':
            condition = child.attrib['value']
    return country, city, temperature, condition


async def fetch_url_data(session, url, country):
    """
    [ASYNC] Get weather info from single city
    ...
    :param:
        session: ClientSession()
            async ClientSession obj
        url: str
            URL for api call

    :return:
        W: namedtuple
            W(country, xml_data) namedtuple object with fetched weather data.
    """
    async with session.get(url) as response:
        resp = await response.read()
        _, city, temperature, condition = get_data_from_response(resp)
        created_at = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
    return W(
        country,
        create_lxml_weather(country, city, temperature, condition, created_at)
    )


async def gather_weather():
    """Get route for all cities"""
    tasks = []
    async with ClientSession() as session:
        loop = asyncio.get_event_loop()
        for country, cities in DEFAULT_INFO.items():
            for city in cities:
                url = get_city_url(city)
                task = loop.create_task(fetch_url_data(session, url, country))
                tasks.append(task)
        weather = await asyncio.gather(*tasks)
    return weather


async def send_data_to_rabbitmq2():
    weather_data_list = await gather_weather()

    loop = asyncio.get_event_loop()
    tasks = []
    for weather_data in weather_data_list:
        task = loop.create_task(pr(
            loop,
            message_body=weather_data.xml_data,
            queue_name=weather_data.country
        ))
        tasks.append(task)
    await asyncio.gather(*tasks)


async def send_data_to_rabbitmq():
    start = time.time()
    weather_data_list = await gather_weather()

    loop = asyncio.get_event_loop()
    for weather_data in weather_data_list:
        await pr(
            loop,
            message_body=weather_data.xml_data,
            queue_name=weather_data.country
        )
    print('!!!!!!!!!!!!!!!!!SENDING TO SAVE TIME I accomplished?', time.time() - start)


async def send_data_to_rabbitmq_old():
    start = time.time()
    weather_data_list = await gather_weather()

    loop = asyncio.get_event_loop()
    for weather_data in weather_data_list:
        await pr(
            loop,
            message_body=weather_data.xml_data,
            queue_name=weather_data.country
        )
    print('!!!!!!!!!!!!!!!!!SENDING TO SAVE TIME I accomplished?', time.time() - start)

