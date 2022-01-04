"""Test services.py."""
from unittest.mock import MagicMock
import pytest

from lxml import etree
from lxml.etree import XMLSchemaValidateError
from aiohttp import ClientSession

import app.services
from app import url_pattern
from app.models import WeatherXML


from app.services import get_data_from_response, create_lxml_weather, \
    fetch_url_data, gather_weather
# from app.services import send_data_to_rabbitmq


def test_create_lxml_weather():
    """Test create_lxml_weather()."""
    test_result = create_lxml_weather(
        "Ukraine", "Lviv", "4.21", "clear sky", "2021-11-21"
    )
    root = etree.fromstring(test_result)
    assert len(root.getchildren()) == 5


def test_get_data_from_response(test_response_data):
    """Test get_data_from_response()."""
    test_result = get_data_from_response(test_response_data)
    assert test_result == ("Lviv", "4.21", "mist")


@pytest.mark.usefixtures("test_response_data")
@pytest.mark.asyncio
@pytest.mark.parametrize("url, country", [
    (url_pattern.format("Lviv"), "Ukraine"),
])
async def test_fetch_url_data(
        monkeypatch, url, country
):
    """Test fetch_url_data()."""
    mock = MagicMock()
    mock.return_value = b""
    monkeypatch.setattr(app.services, "create_lxml_weather", mock)

    async with ClientSession() as session:
        test_result = await fetch_url_data(session, url, country)
        assert test_result.country == country


@pytest.mark.usefixtures("test_response_data")
@pytest.mark.asyncio
@pytest.mark.parametrize("url, country", [
    (url_pattern.format(""), "Ukraine"),
    (url_pattern.format("Lv"), "Ukraine"),
])
async def test_fetch_url_data_error(
        url, country
):
    """Test fetch_url_data_error()."""

    async with ClientSession() as session:
        with pytest.raises(XMLSchemaValidateError):
            await fetch_url_data(session, url, country)


@pytest.mark.asyncio
async def test_gather_weather(monkeypatch):
    """Test gather_weather()."""

    async def mock_fetch(_, __, ___):
        return WeatherXML("Ukraine", b"")

    monkeypatch.setattr(app.services, "fetch_url_data", mock_fetch)

    test_result = await gather_weather()
    assert isinstance(test_result, list)
    assert len(test_result) == 25
#
#
# @pytest.mark.asyncio
# async def test_send_data_to_rabbitmq(monkeypatch):
#     """Test send_data_to_rabbitmq pass."""
#
#     async def mock_weather():
#         return [WeatherXML("Ukraine", b"")]
#
#     monkeypatch.setattr(app.services, "gather_weather", mock_weather)
#
#     await send_data_to_rabbitmq()
