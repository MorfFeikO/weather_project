import pytest

from lxml import etree
from aiohttp import ClientSession

import app.services
from app import url_pattern
from app.models import WeatherXML
from app.producer import producer


from app.services import get_data_from_response, create_lxml_weather, \
    fetch_url_data, gather_weather, send_data_to_rabbitmq


def test_get_data_from_response(test_response_data):
    test_result = get_data_from_response(test_response_data)
    assert test_result == ("Lviv", "4.21", "mist")
    assert isinstance(test_result, tuple)


def test_create_lxml_weather():
    test_result = create_lxml_weather("Ukraine", "Lviv", "4.21", "clear sky", "2021-11-21")
    root = etree.fromstring(test_result)
    assert len(root.getchildren()) == 5


@pytest.mark.asyncio
@pytest.mark.parametrize("url, country, city", [
    (url_pattern.format("Lviv"), "Ukraine", "Lviv"),
])
async def test_fetch_url_data(monkeypatch, test_response_data, url, country, city):

    def mock_lxml(country, city, temperature, condition, created_date):
        return b""

    monkeypatch.setattr(app.services, "create_lxml_weather", mock_lxml)

    async with ClientSession() as session:
        test_result = await fetch_url_data(session, url, country)
        assert isinstance(test_result, WeatherXML)
        assert test_result.country == country
        assert isinstance(test_result.xml_data, bytes)


@pytest.mark.asyncio
@pytest.mark.parametrize("url, country, city", [
    (url_pattern.format(""), "Ukraine", ""),
    (url_pattern.format("Lv"), "Ukraine", "Lv"),
])
async def test_fetch_url_data_error(monkeypatch, test_response_data, url, country, city):

    async with ClientSession() as session:
        with pytest.raises(ValueError):
            await fetch_url_data(session, url, country)


@pytest.mark.asyncio
async def test_gather_weather(monkeypatch):

    async def mock_fetch(session, url, country):
        return WeatherXML("Ukraine", b"")

    monkeypatch.setattr(app.services, "fetch_url_data", mock_fetch)

    test_result = await gather_weather()
    assert isinstance(test_result, list)
    assert len(test_result) == 25


# @pytest.mark.asyncio
# async def test_send_data_to_rabbitmq(monkeypatch):
#
#     async def mock_weather():
#         return [WeatherXML("Ukraine", b"")]
#
#     async def mock_producer():
#         return True
#
#     monkeypatch.setattr(app.services, "gather_weather", mock_weather)
#     monkeypatch.setattr(app.producer, "producer", mock_producer)
#
#     test_result = await send_data_to_rabbitmq()
#     assert test_result is None
