"""Async weather request module.
...
Functions:
    send_data_to_rabbitmq()
        Send data to rabbitmq.
"""
import os
import asyncio
import datetime

from lxml import etree, builder
from aiohttp import ClientSession

from app import DEFAULT_INFO, url_pattern
from app.async_prod import produce as pr
from app.models import WeatherXML


def get_url(city: str) -> str:
    """Get url for api call."""
    return url_pattern.format(city)


def create_lxml_weather(country, city, temperature, condition, date):
    """Create XML data.
    :return lxml tree
    """
    elem = builder.ElementMaker()
    e_root = elem.current
    e_country = elem.country
    e_city = elem.city
    e_temperature = elem.temperature
    e_condition = elem.condition
    e_created_date = elem.created_date

    tree = e_root(
        e_country(country),
        e_city(city),
        e_temperature(temperature),
        e_condition(condition),
        e_created_date(date),
    )
    return etree.tostring(tree)


def get_data_from_response(data):
    """Get data from xml response.
    ...
    :return tuple(country, city, temperature, condition)
    """
    root = etree.fromstring(data)
    country, city, temperature, condition = "", "", "", ""
    for child in root.iter():
        if child.tag == "city":
            city = child.attrib["name"]
        elif child.tag == "country":
            country = child.text
        elif child.tag == "temperature":
            temperature = child.attrib["value"]
        elif child.tag == "weather":
            condition = child.attrib["value"]
    return country, city, temperature, condition


async def fetch_url_data(session, url, country):
    """Get weather info from single city.
    ...
    :param session: ClientSession()
        async ClientSession obj
    :param url: str
        URL for api call
    :param country: str
        Name of country
    :return WeatherXML: namedtuple
        WeatherXML(country, xml_data) namedtuple object with fetched weather data.
    """
    async with session.get(url) as response:
        resp = await response.read()
        _, city, temperature, condition = get_data_from_response(resp)
        created_at = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
    return WeatherXML(
        country, create_lxml_weather(country, city, temperature, condition, created_at)
    )


async def gather_weather():
    """Get weather data for all requested cities cities.
    :return weather: list
        List of WeatherXML(country, xml_data) namedtuple objects.
    """
    tasks = []
    async with ClientSession() as session:
        loop = asyncio.get_event_loop()
        for country, cities in DEFAULT_INFO.items():
            for city in cities:
                url = get_url(city)
                task = loop.create_task(fetch_url_data(session, url, country))
                tasks.append(task)
        weather = await asyncio.gather(*tasks)
    return weather


async def send_data_to_rabbitmq():
    """Send data to rabbitmq."""
    weather_data_list = await gather_weather()

    loop = asyncio.get_event_loop()
    for weather_data in weather_data_list:
        await pr(
            loop, message_body=weather_data.xml_data, queue_name=weather_data.country
        )
