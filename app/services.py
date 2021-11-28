"""Async weather request module.

Functions:
    send_data_to_rabbitmq()
        Send data to rabbitmq.
"""
import asyncio
import datetime

from lxml import etree, builder
from aiohttp import ClientSession

from app import default_info, url_pattern
from app.producer import producer
from app.models import WeatherXML


def create_lxml_weather(
        country: str, city: str, temperature: str, condition: str, date: str
) -> bytes:
    """Create XML data string."""
    elem = builder.ElementMaker()
    tree = elem.current(
        elem.country(country),
        elem.city(city),
        elem.temperature(temperature),
        elem.condition(condition),
        elem.created_date(date),
    )
    declaration = b'<?xml version="1.0" encoding="UTF-8"?>'
    return b"".join((declaration, etree.tostring(tree)))


def get_data_from_response(data: bytes) -> tuple:  # TODO: verify xml wrapper
    """Get data from xml response."""
    result = []
    root = etree.fromstring(data)
    for key in attributes:
        for el in root.iter(key):
            result.append(el.attrib[attributes[key]])
    city, temperature, condition = result
    return city, temperature, condition


async def fetch_url_data(session: ClientSession, url: str, country: str):
    """Get weather info from single city.

    :return WeatherXML: namedtuple
        WeatherXML(country, xml_data).
    """
    async with session.get(url) as response:
        resp = await response.read()
        city, temperature, condition = get_data_from_response(resp)
        created_date = (
            datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
        )
    return WeatherXML(country, create_lxml_weather(
        country, city, temperature, condition, created_date
    ))


async def gather_weather():  # TODO: ValueError on cities
    """Get weather data for all requested cities cities.

    :return weather: list
        [WeatherXML(country, xml_data), ...].
    """
    tasks = []
    async with ClientSession() as session:
        loop = asyncio.get_event_loop()
        for country, cities in default_info.items():
            for city in cities:
                url = url_pattern.format(city)
                task = loop.create_task(fetch_url_data(session, url, country))
                tasks.append(task)
        weather = await asyncio.gather(*tasks)
    return weather


async def send_data_to_rabbitmq():
    """Send data to rabbitmq."""
    weather_data_list = await gather_weather()

    loop = asyncio.get_event_loop()
    for weather_data in weather_data_list:
        await producer(
            loop,
            message_body=weather_data.xml_data,
            queue_name=weather_data.country
        )


attributes = {
    "city": "name",
    "temperature": "value",
    "weather": "value",
}
