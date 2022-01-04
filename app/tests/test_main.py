"""Test main.py"""
from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient

import app.files_requests
import app.db_requests
import app.services
from app import settings
from app.main import app as fast_app


TEST_DIR = settings.TEST_DIR
client = TestClient(fast_app)


class TestGetWeather:
    """Test get_weather()."""
    mock_path = MagicMock()
    url = "/api/weather"

    @pytest.mark.usefixtures("test_session", "data_folder_with_one_file")
    def test_get_weather_empty_db(self, monkeypatch):
        """Test get_weather() with empty db."""
        self.mock_path.return_value = TEST_DIR
        monkeypatch.setattr(app.files_requests.os, "getcwd", self.mock_path)

        response = client.get(self.url)
        expected_result = [{
            "country": "China",
            "city": "Beijing",
            "temperature": '23.0',
            "condition": "sunny"
        }]
        assert response.status_code == 200
        assert response.json() == expected_result

    @pytest.mark.usefixtures("test_db")
    def test_get_weather_empty_files(self):
        """Test get_weather() with empty files folder."""
        response = client.get(self.url)
        expected_result = [{
            "country": "China",
            "city": "Beijing",
            "temperature": 23.0,
            "condition": "clear sky",
        }, {
            "country": "China",
            "city": "Hong Kong",
            "temperature": 20.0,
            "condition": "sunny"
        }]
        assert response.status_code == 200
        assert response.json() == expected_result

    @pytest.mark.usefixtures("test_session")
    def test_get_weather_empty(self):
        """Test get_weather() with no data in files and db."""
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.json() == []


class TestGetStatistic:
    """Test get_statistic()."""
    mock_path = MagicMock()
    url = "/api/statistic"

    @pytest.mark.usefixtures("test_session", "data_folder_with_one_file")
    def test_get_statistic_empty_db(self, monkeypatch):
        """Test get_statistic() with empty db."""
        self.mock_path.return_value = TEST_DIR
        monkeypatch.setattr(app.files_requests.os, "getcwd", self.mock_path)

        response = client.get(self.url)
        expected_result = {
            "db": [],
            "files": [{
                "countryName": "China",
                "firstCheckDate": "21 nov 2021",
                "lastCheckDate": "21 nov 2021",
                "countValue": 1
            }]
        }
        assert response.status_code == 200
        assert response.json() == expected_result

    @pytest.mark.usefixtures("test_db")
    def test_get_statistic_empty_files(self):
        """Test get_statistic() with empty files folder."""
        response = client.get(self.url)
        expected_result = {
            "db": [
                {"countryName": "China",
                 "recordsCount": 2,
                 "lastCheckDate": "00:00 22 nov 2021",
                 "lastCityCheck": "Hong Kong"}
            ],
            "files": []}
        assert response.status_code == 200
        assert response.json() == expected_result

    @pytest.mark.usefixtures("test_session")
    def test_get_statistic_empty(self):
        """Test get_statistic() with no data in files and db."""
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.json() == {"db": [], "files": []}



# @pytest.fixture
# def monkeypatch_fixture(monkeypatch):
#     """Monkeypatch main.py relative functions fixture."""
#     monkeypatch.setattr(app.files_requests, "save_data_to_file", None)
#     monkeypatch.setattr(app.files_requests, "get_data_from_files", [])
#     monkeypatch.setattr(app.db_requests, "save_data_to_db", None)
#     monkeypatch.setattr(app.db_requests, "get_data_from_db", [])
#     monkeypatch.setattr(app.db_requests, "get_statistic_from_db", {})
#
#
# @pytest.mark.asyncio
# @pytest.mark.usefixtures("test_session", "monkeypatch_fixture")
# @pytest.mark.parametrize("url", ['/', '/statistic', '/weather'])
# def test_main(monkeypatch, url):
#     """Test routes status code."""
#
#     def mock_get_data(data_type):
#         _ = data_type
#         return {}
#
#     monkeypatch.setattr(app.services, "send_data_to_rabbitmq", None)
#     monkeypatch.setattr(app.files_requests, "get_data", mock_get_data)
#
#     response = client.get(url)
#     assert response.status_code == 200
#
#
# @pytest.mark.asyncio
# @pytest.mark.usefixtures("test_session", "monkeypatch_fixture")
# @pytest.mark.parametrize("url", ['/', '/statistic', '/weather'])
# def test_connection_error(monkeypatch, url):
#     """Test routes status code."""
#
#     def mock_get_data(data_type):
#         _ = data_type
#         raise ConnectionError("testing error")
#
#     monkeypatch.setattr(app.services, "send_data_to_rabbitmq", None)
#     monkeypatch.setattr(app.files_requests, "get_data", mock_get_data)
#
#     response = client.get(url)
#     assert response.status_code == 200
#
#
# @pytest.mark.asyncio
# @pytest.mark.usefixtures("test_session", "monkeypatch_fixture")
# @pytest.mark.parametrize("url", ['/', '/statistic', '/weather'])
# def test_rabbit_connection_error(monkeypatch, url):
#     """Test routes status code."""
#
#     def mock_get_data(data_type):
#         _ = data_type
#         return {}
#
#     def mock_rabbit():
#         raise ConnectionError("testing error")
#
#     monkeypatch.setattr(app.services, "send_data_to_rabbitmq", mock_rabbit)
#     monkeypatch.setattr(app.files_requests, "get_data", mock_get_data)
#
#     response = client.get(url)
#     assert response.status_code == 200
