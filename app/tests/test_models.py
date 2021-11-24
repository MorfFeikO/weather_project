"""Test models.py."""
import datetime
import pytest

from app.models import File


@pytest.fixture
def test_file():
    file = File("China_Beijing_20211121.txt")
    file.add_date(file.get_date())
    return file


@pytest.fixture
def test_city():
    """CityFiles obj test data."""
    city = File("China_Beijing_20211121.txt", key="data")
    city.add_date(city.get_date())
    return city


@pytest.fixture
def test_country():
    """CityFiles obj test data."""
    country = File("China_Beijing_20211121.txt", key="statistics")
    country.add_date(country.get_date())
    return country


def test_file_getters(test_file):
    assert test_file.get_country() == "China"
    assert test_file.get_city() == "Beijing"
    assert test_file.get_date() == datetime.date(2021, 11, 21)
    assert test_file.get_first_check() is None
    assert test_file.get_last_check() == "20211121"
    assert test_file.get_name() is None
    assert test_file.get_count() is None
    assert test_file.get_filename() is None


@pytest.mark.parametrize(
    "date, expected",
    [(datetime.date(2021, 11, 22), 2), (datetime.date(2021, 11, 21), 1)],
)
def test_file_add_date(test_file, date, expected):
    test_file.add_date(date)
    assert len(test_file.checks) == expected


def test_file_filename_parser(test_file):
    """Test filename_parser()."""
    assert test_file.parse_filename() == (
        "China",
        "Beijing",
        datetime.date(2021, 11, 21),
    )


@pytest.mark.parametrize(
    "test_input, expected",
    [("file.net", IndexError), ("Italy_Rome_11201246.txt", ValueError)],
)
def test_filename_parser_errors(test_input, expected):
    """Test filenames_parser() raise errors."""
    file = File(test_input)
    with pytest.raises(expected):
        file.parse_filename()


def test_city_getters(test_city):
    assert test_city.get_name() == "Beijing"
    assert test_city.get_filename() == "China_Beijing_20211121.txt"


def test_country_getters(test_country):
    assert test_country.get_first_check() == "21 nov 2021"
    assert test_country.get_last_check() == "21 nov 2021"
    assert test_country.get_name() == "China"
    assert test_country.get_count() == 1


def test_country_add_date(test_country):
    test_country.add_date(datetime.date(2021, 11, 22))
    assert test_country.count == 2
