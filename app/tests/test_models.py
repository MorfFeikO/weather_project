"""Test models.py."""
import datetime
import pytest

from app.models import CityFiles, CountryFiles


@pytest.fixture
def test_city():
    """CityFiles obj test data."""
    city = CityFiles('Rome', 'Italy')

    city.add_check_date(datetime.date(2021, 11, 20))
    city.add_check_date(datetime.date(2021, 11, 21))
    city.add_check_date(datetime.date(2021, 10, 23))
    return city


@pytest.fixture
def test_country():
    """CityCountries obj test data."""
    country = CountryFiles('Italy')

    country.add_check_date(datetime.date(2021, 11, 20))
    country.add_check_date(datetime.date(2021, 11, 21))
    country.add_check_date(datetime.date(2021, 10, 23))
    return country


def test_city_files_add_check_date(test_city):
    """Test CityFiles.add_check_date(date)."""
    assert test_city.last_check == '20211121'
    assert len(test_city.checks) == 3


def test_city_files_add_check_date_duplicate(test_city):
    """Test CityFiles.add_check_date(date) with duplicate data add."""
    test_city.add_check_date(datetime.date(2021, 11, 20))
    assert test_city.last_check == '20211121'
    assert len(test_city.checks) == 3


def test_city_files_get_last_check_name(test_city):
    """Test CityFiles.get_last_check_filename()."""
    assert test_city.get_last_check_filename() == 'Italy_Rome_20211121.txt'


def test_city_files_repr(test_city):
    """Test CityFiles.repr()."""
    assert repr(test_city) == 'CityFiles(Rome, Italy)'


def test_country_files_add_check_date(test_country):
    """Test CountryFiles.add_check_date(date)."""
    assert test_country.first_check == '23 oct 2021'
    assert test_country.last_check == '21 nov 2021'
    assert test_country.count == 3
    assert len(test_country.checks) == 3


def test_country_files_add_check_date_duplicate(test_country):
    """Test CountryFiles.add_check_date(date) with duplicate data add."""
    test_country.add_check_date(datetime.date(2021, 11, 20))
    assert test_country.first_check == '23 oct 2021'
    assert test_country.last_check == '21 nov 2021'
    assert test_country.count == 4
    assert len(test_country.checks) == 3


def test_country_files_repr(test_country):
    """Test CityFiles.repr()."""
    assert repr(test_country) == 'CountryFiles(Italy)'
