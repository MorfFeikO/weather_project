"""Test db_requests.py."""
import datetime
from unittest.mock import MagicMock

import pytest
import app.db_requests
from app.models import City, Weather
from app.db_requests import (
    save_city,
    save_weather,
    transform_data,
    get_statistic_from_db,
    get_data_from_db,
    load_data_from_single_city,
    get_last_city,
    get_last_check,
    load_db_statistic,
)


def test_save_city(test_session, test_data):
    """Test save_city()."""
    save_city(city=test_data["city"], country=test_data["country"])
    city = test_session.query(City.name, City.country).all()
    assert len(city) == 1
    assert city[0].name == "Beijing"
    assert city[0].country == "China"


@pytest.mark.parametrize("country, city, expected_len", [
    ("China", "Beijing", 1),
    ("China", "Hong Kong", 2),
])
def test_save_city_duplicate(
        test_session, test_data, country, city, expected_len
):
    """Test save_city() with duplicate in db."""
    save_city(city=test_data["city"], country=test_data["country"])

    save_city(city=city, country=country)
    city = test_session.query(City.name, City.country).all()
    assert len(city) == expected_len


def test_save_weather(test_session, test_data):
    """Test save_weather()."""
    save_weather(test_data)
    city = test_session.query(City.name,
                              City.country,
                              Weather.temperature,
                              Weather.condition,
                              Weather.created_date).join(City.weather).all()
    assert len(city) == 1
    assert city[0].name == "Beijing"
    assert city[0].country == "China"
    assert city[0].temperature == float("23")
    assert city[0].condition == "clear sky"
    assert city[0].created_date == datetime.datetime(2021, 11, 21)


def test_save_weather_duplicate(monkeypatch, test_session, test_data):
    """Test save_weather() with duplicate in db."""

    def mock_city_save(_, __):
        test_session.add(City(name=test_data["city"],
                              country=test_data["country"]))
        test_session.commit()

    monkeypatch.setattr(app.db_requests, "save_city", mock_city_save)

    save_weather(test_data)
    test_city = test_session.query(City.name,
                                   City.country,
                                   Weather.temperature,
                                   Weather.condition,
                                   Weather.created_date
                                   ).join(City.weather).all()
    assert len(test_city) == 1
    assert test_city[0].temperature == float("23")
    assert test_city[0].condition == "clear sky"
    assert test_city[0].created_date == datetime.datetime(2021, 11, 21)


# def test_save_data_to_db():
#     pass


def test_transform_data(test_xml):
    """Test transform_data()."""
    test_result = transform_data(test_xml)
    assert len(test_result) == 5
    assert test_result["country"] == "China"
    assert test_result["city"] == "Beijing"
    assert test_result["temperature"] == "23"
    assert test_result["condition"] == "clear sky"
    assert test_result["created_date"] == "2021-11-21 13:44:28.36545"


class TestGetStatisticFromDB:
    """Test get_statistic_from_db()."""
    mock = MagicMock()
    smock = MagicMock()

    @pytest.mark.usefixtures("test_db_single_line")
    def test_get_statistic_from_db(self, monkeypatch):
        """Test get_statistic_from_db()."""

        self.mock.return_value = {"countryName": "China",
                                  "recordsCount": 4,
                                  "lastCheckDate": "00:00 22 nov 2021",
                                  "lastCityCheck": "Hong Kong"}

        monkeypatch.setattr(app.db_requests, "load_db_statistic", self.mock)

        expected_result = [{
            "countryName": "China",
            "recordsCount": 4,
            "lastCheckDate": "00:00 22 nov 2021",
            "lastCityCheck": "Hong Kong"}]
        assert get_statistic_from_db() == expected_result

    @staticmethod
    @pytest.mark.usefixtures("test_session")
    def test_get_statistic_from_db_empty():
        """Test get_statistic_from_db() with empty db."""
        assert get_statistic_from_db() == []

    def test_load_db_statistic(self, monkeypatch):
        """Test load_db_statistic()."""

        self.mock.return_value = "00:00 22 nov 2021"
        monkeypatch.setattr(app.db_requests, "get_last_check", self.mock)

        self.smock.return_value = "Hong Kong"
        monkeypatch.setattr(app.db_requests, "get_last_city", self.smock)

        expected_result = {
            "countryName": "China",
            "recordsCount": 4,
            "lastCheckDate": "00:00 22 nov 2021",
            "lastCityCheck": "Hong Kong"
        }
        assert load_db_statistic("China", 4) == expected_result

    @staticmethod
    @pytest.mark.usefixtures("test_db")
    def test_get_last_check():
        """Test_get_last_check()."""
        assert get_last_check("China") == "00:00 22 nov 2021"

    @staticmethod
    @pytest.mark.usefixtures("test_db")
    def test_get_last_city():
        """Test get_last_city()."""
        assert get_last_city("China") == "Hong Kong"


class TestGetDataFromDB:
    """Test get_data_from_db() and load_data_from_single_city()."""
    mock = MagicMock()

    @pytest.mark.usefixtures("test_db")
    def test_get_data_from_db(self, monkeypatch):
        """Test get_data_from_db()."""

        self.mock.return_value = {"country": "test_country",
                                  "city": "test_city",
                                  "temperature": "test_temperature",
                                  "condition": "test_condition"}

        monkeypatch.setattr(app.db_requests,
                            "load_data_from_single_city",
                            self.mock)

        test_result = get_data_from_db()
        assert len(test_result) == 2
        for data in test_result:
            assert len(data) == 4
            for key in data:
                assert key in ("city", "condition", "country", "temperature")

    @staticmethod
    @pytest.mark.usefixtures("test_session")
    def test_get_data_from_db_empty():
        """Test get_data_from_db() empty db."""
        test_result = get_data_from_db()
        assert len(test_result) == 0

    @staticmethod
    @pytest.mark.usefixtures("test_db")
    def test_load_data_from_single_city():
        """Test load_data_from_single_city()."""
        test_result = load_data_from_single_city("Beijing")
        expected_result = {"country": "China",
                           "city": "Beijing",
                           "temperature": 23.0,
                           "condition": "clear sky"}
        assert test_result == expected_result
