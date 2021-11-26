"""Test models.py."""
import datetime
import pytest

from app.models import File


@pytest.fixture
def test_file():
    file = File("China_Beijing_20211121.txt")
    return file


@pytest.fixture
def test_city():
    """CityFiles obj test data."""
    city = File("China_Beijing_20211121.txt", key="data")
    return city


@pytest.fixture
def test_country():
    """CityFiles obj test data."""
    country = File("China_Beijing_20211121.txt", key="statistics")
    return country


def test_file_getters(test_file):
    """Test File obj getters."""
    assert test_file.date == datetime.date(2021, 11, 21)
    assert isinstance(test_file, File)
    assert test_file._country == "China"
    assert test_file._city == "Beijing"
    assert len(test_file._checks) == 1


@pytest.mark.parametrize("test_date, expected", [
    (datetime.date(2021, 11, 22), 2),
    (datetime.date(2021, 11, 21), 1)
])
def test_file_add_date(test_file, test_date, expected):
    """Test File obj add_date()."""
    test_file.add_date(test_date)
    assert len(test_file._checks) == expected


@pytest.mark.parametrize("test_filename, expected_error", [
    ("file.txt", IndexError),
    ("China_Beijing_20212121.txt", ValueError)
])
def test_error_raises(test_filename, expected_error):
    """Test File obj raises errors when initialized."""
    with pytest.raises(expected_error):
        File(test_filename)


def test_city_getters(test_city):
    """Test CityFile obj getters."""
    assert test_city.name == "Beijing"
    assert test_city.last_check_filename == "China_Beijing_20211121.txt"


@pytest.mark.parametrize("test_date, expected_count", [
    (datetime.date(2021, 11, 22), 2),
    (datetime.date(2021, 11, 21), 1)
])
def test_country_add_date(test_country, test_date, expected_count):
    """Test CountryFile add_date()."""
    test_country.add_date(test_date)
    assert len(test_country._checks) == expected_count


def test_country_getters(test_country):
    """Test CountryFile obj getters."""
    test_country.add_date(datetime.date(2021, 11, 22))
    assert test_country.name == "China"
    assert test_country.first_check == "21 nov 2021"
    assert test_country.last_check == "22 nov 2021"
