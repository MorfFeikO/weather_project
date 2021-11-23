"""Test files_requests.py."""
import json
import os
import pathlib
import datetime
import pytest
import shutil

import app.files_requests
from app.files_requests import get_filepath, get_files_list, filename_parser, \
    get_city_data, get_data_from_files, get_statistic_from_files, xml_to_dict, \
    save_data_to_file
from app.models import CityFiles, FreshWeather, CountryFiles

BASE_DIR = pathlib.Path(__file__).parent


@pytest.mark.parametrize("test_input, expected", [
    ("folder", BASE_DIR.parent.parent / "folder"),
    ("files_data", BASE_DIR.parent.parent / "files_data")
])
def test_get_filepath(test_input, expected):
    """Test get_filepath()."""
    assert get_filepath(test_input) == str(expected)


@pytest.mark.parametrize("test_input, expected", [
    ("data", []),
    ("test_data", os.listdir(BASE_DIR / "test_data"))
])
def test_get_files_list(monkeypatch, test_input, expected):
    """Test get_files_list()."""
    def mock_path():
        return BASE_DIR / test_input

    monkeypatch.setattr(app.files_requests, 'get_filepath', mock_path)
    assert get_files_list() == expected


def test_filename_parser():
    """Test filename_parser()."""
    filename = 'Italy_Rome_20211120.txt'
    assert filename_parser(filename) == ('Italy', 'Rome', datetime.date(2021, 11, 20))


@pytest.mark.parametrize("test_input, expected", [
    ('file.net', IndexError),
    ('Italy_Rome_11201246.txt', ValueError)
])
def test_filename_parser_errors(test_input, expected):
    """Test filenames_parser() raise errors."""
    filename = test_input
    with pytest.raises(expected):
        filename_parser(filename)


@pytest.mark.parametrize("test_input, expected", [
    (['China_Beijing_20211121.txt'], 1),
    (['China_Beijing_20211121.txt', 'China_Beijing_20211120.txt'], 1),
    (['China_Beijing_20211121.txt', 'China_Beijing_20211120.txt', 'Ukraine_Lviv_20211121.txt'], 2),
    ([], 0),
    (['China_Beijing_20211121.txt', "file.txt"], 1),
    (['China_Beijing_20212121.txt'], 0)
])
def test_get_city_data(monkeypatch, test_input, expected):
    """Test get_city_data()."""
    def mock_files_list():
        return test_input

    monkeypatch.setattr(app.files_requests, "get_files_list", mock_files_list)
    test_func = get_city_data()
    for key, value in test_func.items():
        assert isinstance(value, CityFiles)
    assert len(get_city_data()) == expected
    assert isinstance(test_func, dict)


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


def test_get_data_form_files_empty(monkeypatch):
    """Test_get_data_from_files() return empty dict."""
    def mock_city_data():
        return {}

    monkeypatch.setattr(app.files_requests, "get_city_data", mock_city_data)
    test_func = get_data_from_files()
    assert len(test_func) == 0
    assert isinstance(test_func, list)


@pytest.mark.parametrize("test_input, expected", [
    (['China_Beijing_20211121.txt'], 1),
    (['China_Beijing_20211121.txt', 'China_Beijing_20211120.txt'], 1),
    (['China_Beijing_20211121.txt', 'China_Beijing_20211120.txt', 'Ukraine_Lviv_20211121.txt'], 2),
    ([], 0),
    (['China_Beijing_20211121.txt', "file.txt"], 1),
    (['China_Beijing_20212121.txt'], 0)
])
def test_get_static_from_files(monkeypatch, test_input, expected):
    """Test get statistic_from_files()."""
    def mock_files_list():
        return test_input

    monkeypatch.setattr(app.files_requests, "get_files_list", mock_files_list)
    test_func = get_statistic_from_files()
    for key, value in test_func.items():
        assert isinstance(value, CountryFiles)
    assert len(get_city_data()) == expected
    assert isinstance(test_func, dict)


def test_xml_to_string():
    """Test xml_to_string()."""
    input_data = b'<root><country>China</country><city>Beijing</city>' \
                 b'<temperature>4.28</temperature><condition>clear sky</condition>' \
                 b'<created_date>2021-11-21 13:44:28.36545</created_date></root>'
    expected = ("China", "Beijing", "20211121", {
        "country": "China",
        "city": "Beijing",
        "temperature": "4.28",
        "condition": "clear sky"
    })
    assert xml_to_dict(input_data) == expected


def test_save_data_to_file(monkeypatch):
    """Test save_data_to_file()."""
    def mock_path():
        return BASE_DIR / "test_data_2"

    def mock_data(data):
        return ("China", "Hong Kong", "20211121", {
            "country": "China",
            "city": "Hong Kong",
            "temperature": "4.28",
            "condition": "clear sky"
        })

    monkeypatch.setattr(app.files_requests, "get_filepath", mock_path)
    monkeypatch.setattr(app.files_requests, "xml_to_dict", mock_data)

    save_data_to_file("")
    filepath = BASE_DIR / "test_data_2"
    filename = 'China_Hong Kong_20211121.txt'
    assert os.listdir(filepath) == [filename]
    with open(os.path.join(filepath, filename), "rb") as f:
        data = json.load(f)
        assert data['country'] == 'China'
        assert data['city'] == 'Hong Kong'
        assert data['temperature'] == "4.28"
        assert data['condition'] == "clear sky"
    shutil.rmtree(filepath, ignore_errors=True)
