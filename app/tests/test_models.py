"""Test models.py."""
import datetime
import pytest

from app.models import CityFiles, CountryFiles, CityFile, CountryFile, File


@pytest.fixture
def test_city():
    """CityFiles obj test data."""
    city = CityFiles("Rome", "Italy")

    city.add_check_date(datetime.date(2021, 11, 20))
    city.add_check_date(datetime.date(2021, 11, 21))
    city.add_check_date(datetime.date(2021, 10, 23))
    return city


@pytest.fixture
def test_country():
    """CityCountries obj test data."""
    country = CountryFiles("Italy")

    country.add_check_date(datetime.date(2021, 11, 20))
    country.add_check_date(datetime.date(2021, 11, 21))
    country.add_check_date(datetime.date(2021, 10, 23))
    return country


def test_city_files_add_check_date(test_city):
    """Test CityFiles.add_check_date(date)."""
    assert test_city.last_check == "20211121"
    assert len(test_city.checks) == 3


def test_city_files_add_check_date_duplicate(test_city):
    """Test CityFiles.add_check_date(date) with duplicate data add."""
    test_city.add_check_date(datetime.date(2021, 11, 20))
    assert test_city.last_check == "20211121"
    assert len(test_city.checks) == 3


def test_city_files_get_last_check_name(test_city):
    """Test CityFiles.get_last_check_filename()."""
    assert test_city.get_last_check_filename() == "Italy_Rome_20211121.txt"


def test_city_files_repr(test_city):
    """Test CityFiles.repr()."""
    assert repr(test_city) == "CityFiles(Rome, Italy)"


def test_country_files_add_check_date(test_country):
    """Test CountryFiles.add_check_date(date)."""
    assert test_country.first_check == "23 oct 2021"
    assert test_country.last_check == "21 nov 2021"
    assert test_country.count == 3
    assert len(test_country.checks) == 3


def test_country_files_add_check_date_duplicate(test_country):
    """Test CountryFiles.add_check_date(date) with duplicate data add."""
    test_country.add_check_date(datetime.date(2021, 11, 20))
    assert test_country.first_check == "23 oct 2021"
    assert test_country.last_check == "21 nov 2021"
    assert test_country.count == 4
    assert len(test_country.checks) == 3


def test_country_files_repr(test_country):
    """Test CityFiles.repr()."""
    assert repr(test_country) == "CountryFiles(Italy)"


##########################################
@pytest.fixture
def test_city():
    """CityFiles obj test data."""
    city = File("China_Beijing_20211121.txt", key="data")
    city.add_date(city.get_date())
    return city


def test_city_getters(test_city):
    assert test_city.get_name() == "Beijing"
    assert test_city.get_filename() == "China_Beijing_20211121.txt"


@pytest.fixture
def test_country():
    """CityFiles obj test data."""
    country = File("China_Beijing_20211121.txt", key="statistics")
    country.add_date(country.get_date())
    return country


def test_country_getters(test_country):
    assert test_country.get_first_check() == "20211121"
    assert test_country.get_name() == "China"
    assert test_country.get_count() == 1


def test_country_add_date(test_country):
    test_country.add_date(datetime.date(2021, 11, 22))
    assert test_country.count == 2


@pytest.fixture
def test_file():
    file = File("China_Beijing_20211121.txt")
    file.add_date(file.get_date())
    return file


def test_file_getters(test_file):
    assert test_file.get_country() == "China"
    assert test_file.get_city() == "Beijing"
    assert test_file.get_date() == datetime.date(2021, 11, 21)
    assert test_file.get_first_check() is None
    assert test_file.get_last_check() == "20211121"
    assert test_file.get_name() is None
    assert test_file.get_count() is None


@pytest.mark.parametrize(
    "date, expected",
    [(datetime.date(2021, 11, 22), 2), (datetime.date(2021, 11, 21), 1)],
)
def test_file_add_date(test_file, date, expected):
    test_file.add_date(date)
    assert len(test_file.checks) == expected
