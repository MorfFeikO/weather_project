"""Test files_requests.py."""
import json
import os
import pathlib
import datetime
import shutil
import pytest

import app.files_requests
from app.files_requests import (
    get_filepath,
    get_files_list,
    get_data_from_files,
    xml_to_dict,
    save_data_to_file,
    get_data,
)
from app.models import FreshWeather, CountryFile, CityFile

BASE_DIR = pathlib.Path(__file__).parent


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("folder", BASE_DIR.parent.parent / "folder"),
        ("files_data", BASE_DIR.parent.parent / "files_data"),
    ],
)
def test_get_filepath(test_input, expected):
    """Test get_filepath()."""
    assert get_filepath(test_input) == str(expected)


@pytest.mark.parametrize(
    "test_input, expected",
    [("data", []), ("test_data", os.listdir(BASE_DIR / "test_data"))],
)
def test_get_files_list(monkeypatch, test_input, expected):
    """Test get_files_list()."""

    def mock_path():
        return BASE_DIR / test_input

    monkeypatch.setattr(app.files_requests, "get_filepath", mock_path)
    assert get_files_list() == expected


def test_get_data_from_files(monkeypatch):
    """Test get_data_from_files()."""

    def mock_filepath():
        return BASE_DIR / "test_data"

    monkeypatch.setattr(app.files_requests, "get_filepath", mock_filepath)
    test_func = get_data_from_files()
    for weather in get_data_from_files():
        assert isinstance(weather, FreshWeather)
    assert len(test_func) == 2
    assert isinstance(test_func, list)


def test_get_data_from_files_empty(monkeypatch):
    """Test_get_data_from_files() return empty dict."""

    def mock_get_data(data_type="data"):
        return {}

    monkeypatch.setattr(app.files_requests, "get_data", mock_get_data)
    test_func = get_data_from_files()
    assert len(test_func) == 0
    assert isinstance(test_func, list)


def test_xml_to_string():
    """Test xml_to_string()."""
    input_data = (
        b"<root><country>China</country><city>Beijing</city>"
        b"<temperature>4.28</temperature><condition>clear sky</condition>"
        b"<created_date>2021-11-21 13:44:28.36545</created_date></root>"
    )
    expected = (
        "China",
        "Beijing",
        "20211121",
        {
            "country": "China",
            "city": "Beijing",
            "temperature": "4.28",
            "condition": "clear sky",
        },
    )
    assert xml_to_dict(input_data) == expected


def test_save_data_to_file(monkeypatch):
    """Test save_data_to_file()."""

    def mock_path():
        return BASE_DIR / "test_data_2"

    def mock_data(_):
        return (
            "China",
            "Hong Kong",
            "20211121",
            {
                "country": "China",
                "city": "Hong Kong",
                "temperature": "4.28",
                "condition": "clear sky",
            },
        )

    monkeypatch.setattr(app.files_requests, "get_filepath", mock_path)
    monkeypatch.setattr(app.files_requests, "xml_to_dict", mock_data)

    save_data_to_file("")
    filepath = BASE_DIR / "test_data_2"
    filename = "China_Hong Kong_20211121.txt"
    assert os.listdir(filepath) == [filename]
    with open(os.path.join(filepath, filename), "rb") as file:
        data = json.load(file)
        assert data["country"] == "China"
        assert data["city"] == "Hong Kong"
        assert data["temperature"] == "4.28"
        assert data["condition"] == "clear sky"
    shutil.rmtree(filepath, ignore_errors=True)


@pytest.mark.parametrize(
    "files_list, input_data, expected", [([], "statistics", {}), ([], "data", {})]
)
def test_get_data_empty(monkeypatch, files_list, input_data, expected):
    """"""

    def mock_list():
        return files_list

    monkeypatch.setattr(app.files_requests, "get_files_list", mock_list)
    assert get_data(input_data) == expected


@pytest.mark.parametrize(
    "files_list, input_data, expected_len, expected_instance",
    [
        (["China_Beijing_20211121.txt"], "statistics", 1, CountryFile),
        (
            ["China_Beijing_20211121.txt", "China_Beijing_20211120.txt"],
            "statistics",
            1,
            CountryFile,
        ),
        (
            [
                "China_Beijing_20211121.txt",
                "China_Beijing_20211120.txt",
                "Ukraine_Lviv_20211121.txt",
            ],
            "statistics",
            2,
            CountryFile,
        ),
        (["China_Beijing_20211121.txt"], "data", 1, CityFile),
        (
            ["China_Beijing_20211121.txt", "China_Beijing_20211120.txt"],
            "data",
            1,
            CityFile,
        ),
        (
            [
                "China_Beijing_20211121.txt",
                "China_Beijing_20211120.txt",
                "Ukraine_Lviv_20211121.txt",
            ],
            "data",
            2,
            CityFile,
        ),
    ],
)
def test_get_data(monkeypatch, files_list, input_data, expected_len, expected_instance):
    """Test get_data()."""

    def mock_files_list():
        return files_list

    monkeypatch.setattr(app.files_requests, "get_files_list", mock_files_list)
    tested_func = get_data(input_data)
    for _, weather in tested_func.items():
        assert isinstance(weather, expected_instance)
    assert len(tested_func) == expected_len
    assert isinstance(tested_func, dict)


@pytest.mark.parametrize(
    "test_input, data_type",
    [(["file.net"], "statistics"), (["Italy_Rome_11201246.txt"], "statistics")],
)
def test_get_data_errors(monkeypatch, test_input, data_type):
    """Test get_data() errors raise."""

    def mock_files_list():
        return test_input

    monkeypatch.setattr(app.files_requests, "get_files_list", mock_files_list)
    tested_func = get_data(data_type)
    assert len(tested_func) == 0
