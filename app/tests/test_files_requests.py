"""Test files_requests.py."""
# import json
import os
import pathlib
import shutil
from unittest.mock import MagicMock
import pytest


import app.files_requests
from app.files_requests import (
    get_filepath,
    get_files_list,
    get_data_from_files,
    xml_to_dict,
    # save_data_to_file,
    get_data,
)
from app.models import FreshWeather, CountryFile, CityFile
from app import settings
from app.config import PROJECT_DIR

BASE_DIR = pathlib.Path(__file__).parent
TEST_DIR = settings.TEST_DIR


class TestGetFilepath:
    """Test get_filepath()."""

    @staticmethod
    def test_with_dir_exists():
        """Test with directory exists."""
        path = PROJECT_DIR / "test_dir"
        os.mkdir(path)
        assert get_filepath(path) == str(path)
        shutil.rmtree(path)

    @staticmethod
    @pytest.mark.parametrize("folder, expected", [
        ("", ".files_data"),
        ("test_folder", "test_folder")
    ])
    def test_with_dir_not_exists(folder, expected):
        """Test with directory not exists."""
        assert get_filepath(folder) == str(PROJECT_DIR / expected)
        shutil.rmtree(PROJECT_DIR / expected)

    @staticmethod
    def test_with_dir_default():
        """Test with default directory."""
        assert get_filepath() == str(PROJECT_DIR / ".files_data")
        shutil.rmtree(PROJECT_DIR / ".files_data")


class TestGetData:
    """Test get_data()."""
    mock_list = MagicMock()

    @pytest.mark.parametrize("files_list, input_data, expected", [
        ([], "statistics", {}),
        ([], "data", {})
    ])
    def test_empty(self, monkeypatch, files_list, input_data, expected):
        """Test with empty folder."""

        self.mock_list.return_value = files_list
        monkeypatch.setattr(
            app.files_requests, "get_files_list", self.mock_list
        )

        test_func = get_data(input_data)
        assert test_func == expected

    @pytest.mark.parametrize("files_list, expected_len, expected_instance", [
            (["China_Beijing_20211121.txt"], 1, CityFile),
            (["China_Beijing_20211121.txt", "China_Beijing_20211120.txt"],
             1,
             CityFile),
            (["China_Beijing_20211121.txt", "Ukraine_Lviv_20211121.txt"],
             2,
             CityFile)
        ])
    def test_get_data_cityfile(self, monkeypatch, files_list, expected_len,
                               expected_instance):
        """Test folder with files."""

        self.mock_list.return_value = files_list
        monkeypatch.setattr(
            app.files_requests, "get_files_list", self.mock_list
        )

        test_func = get_data(data_type="data")
        for _, weather in test_func.items():
            assert isinstance(weather, expected_instance)
        assert len(test_func) == expected_len

    @pytest.mark.parametrize("files_list, expected_len, expected_instance", [
            (["China_Beijing_20211121.txt"], 1, CountryFile),
            (["China_Beijing_20211121.txt", "China_Beijing_20211120.txt"],
             1,
             CountryFile),
            (["China_Beijing_20211121.txt", "Ukraine_Lviv_20211121.txt"],
             2,
             CountryFile),
        ])
    def test_get_data_countryfile(self, monkeypatch, files_list, expected_len,
                                  expected_instance):
        """Test folder with files."""

        self.mock_list.return_value = files_list
        monkeypatch.setattr(
            app.files_requests, "get_files_list", self.mock_list
        )

        test_func = get_data(data_type="statistics")
        for _, weather in test_func.items():
            assert isinstance(weather, expected_instance)
        assert len(test_func) == expected_len

    @pytest.mark.parametrize("files_list, data_type", [
        (["file.net"], "statistics"),
        (["file.net"], "data"),
        (["Italy_Rome_11201246.txt"], "statistics"),
        (["Italy_Rome_11201246.txt"], "data")
    ])
    def test_errors(self, monkeypatch, files_list, data_type):
        """Test errors raise."""

        self.mock_list.return_value = files_list
        monkeypatch.setattr(
            app.files_requests, "get_files_list", self.mock_list
        )

        test_func = get_data(data_type)
        assert len(test_func) == 0


class TestGetFilesList:
    """Test get_files_list()."""
    mock_path = MagicMock()

    def test_get_files_list(self, monkeypatch):
        """Test get_files_list(). with empty folder."""

        self.mock_path.return_value = TEST_DIR / "random_dir"
        monkeypatch.setattr(app.files_requests, "get_filepath", self.mock_path)

        test_func = get_files_list()
        assert test_func == []

    @pytest.mark.usefixtures("test_data_folder")
    def test_get_files_list_with_default_data(self, monkeypatch):
        """Test get_files_list() with default data creation."""

        self.mock_path.return_value = TEST_DIR / "test_data"
        monkeypatch.setattr(app.files_requests, "get_filepath", self.mock_path)

        test_func = get_files_list()
        assert test_func == os.listdir(TEST_DIR / "test_data")


class TestGetDataFromFiles:
    """Test get_data_from_files()."""
    mock_path = MagicMock()

    @pytest.mark.usefixtures("test_data_folder")
    def test_get_data_from_files(self, monkeypatch):
        """Test get data from files."""

        self.mock_path.return_value = TEST_DIR / "test_data"
        monkeypatch.setattr(app.files_requests, "get_filepath", self.mock_path)

        test_func = get_data_from_files()
        for weather in test_func:
            assert isinstance(weather, FreshWeather)
        assert len(test_func) == 2

    def test_get_data_from_files_empty(self, monkeypatch):
        """Test get data from files return empty dict."""

        self.mock_path.return_value = TEST_DIR / "random_dir"
        monkeypatch.setattr(app.files_requests, "get_filepath", self.mock_path)

        test_func = get_data_from_files()
        assert len(test_func) == 0


def test_xml_to_string():
    """Test xml_to_string()."""
    input_data = (
        b'<?xml version="1.0" encoding="UTF-8"?>'
        b"<current><country>China</country><city>Beijing</city>"
        b"<temperature>4.28</temperature><condition>clear sky</condition>"
        b"<created_date>2021-11-21 13:44:28.36545</created_date></current>"
    )
    expected = ("China", "Beijing", "20211121", {
            "country": "China",
            "city": "Beijing",
            "temperature": "4.28",
            "condition": "clear sky",
        })
    assert xml_to_dict(input_data) == expected


# @pytest.mark.asyncio
# async def test_save_data_to_file(monkeypatch, test_data_folder):
#     """Test save_data_to_file()."""
#
#     def mock_path():
#         return test_data_folder
#
#     def mock_data(_):
#         return ("China", "Hong Kong", "20211121", {
#             "country": "China",
#             "city": "Hong Kong",
#             "temperature": "4.28",
#             "condition": "clear sky",
#         })
#
#     monkeypatch.setattr(app.files_requests, "get_filepath", mock_path)
#     monkeypatch.setattr(app.files_requests, "xml_to_dict", mock_data)
#
#     filename = "China_Hong Kong_20211121.txt"
#     filepath = str(test_data_folder)
#     await save_data_to_file.__wrapped__(b"")
#
#     assert filename in os.listdir(filepath)
#     with open(os.path.join(filepath, filename), "rb") as file:
#         data = json.load(file)
#         assert data["country"] == "China"
#         assert data["city"] == "Hong Kong"
#         assert data["temperature"] == "4.28"
#         assert data["condition"] == "clear sky"
