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
