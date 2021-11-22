import pytest
import datetime

from app.models import CityFiles, CountryFiles


@pytest.fixture
def test_city():
    test_city = CityFiles('Rome', 'Italy')

    test_city.add_check_date(datetime.date(2021, 11, 20))
    test_city.add_check_date(datetime.date(2021, 11, 21))
    test_city.add_check_date(datetime.date(2021, 10, 23))
    return test_city


@pytest.fixture
def test_country():
    test_country = CountryFiles('Italy')

    test_country.add_check_date(datetime.date(2021, 11, 20))
    test_country.add_check_date(datetime.date(2021, 11, 21))
    test_country.add_check_date(datetime.date(2021, 10, 23))
    return test_country


def test_city_files_add_check_date(test_city):
    assert test_city.last_check == '20211121'
    assert len(test_city.checks) == 3


def test_city_files_add_check_date_duplicate(test_city):
    test_city.add_check_date(datetime.date(2021, 11, 20))
    assert test_city.last_check == '20211121'
    assert len(test_city.checks) == 3


def test_city_files_get_last_check_name(test_city):
    assert test_city.get_last_check_filename() == 'Italy_Rome_20211121.txt'


def test_country_files_add_check_date(test_country):
    assert test_country.first_check == '23 oct 2021'
    assert test_country.last_check == '21 nov 2021'
    assert test_country.count == 3
    assert len(test_country.checks) == 3


def test_country_files_add_check_date_duplicate(test_country):
    test_country.add_check_date(datetime.date(2021, 11, 20))
    assert test_country.first_check == '23 oct 2021'
    assert test_country.last_check == '21 nov 2021'
    assert test_country.count == 4
    assert len(test_country.checks) == 3

