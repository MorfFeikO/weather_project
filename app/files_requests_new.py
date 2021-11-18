"""
Operations with weather data files.
...
Functions:
    save_data_to_file(data)
        Save weather data in file on s3 AWS bucket.

    get_data_from_files()
        Get fresh weather data from files on s3 AWS bucket.

    get_statistic_from_data()
        Get statistic from files on s3 AWS bucket.
"""
import re
import json
import datetime
import xmltodict

from app.models import CityFiles, CountryFiles, FreshWeather
from app.files_storage import upload_data_to_file, get_files_list, download_data_from_file


def filename_parser(filename):
    """Parse data from filename.
    ...
    :param filename: str
        Name of file with weather data.
    :return: tuple(country, city, datetime.date())
    """
    pattern = r'(\D*)_(\D*)_(\d{4})(\d{2})(\d{2})'
    country, city, year, month, day = re.findall(pattern, filename)[0]
    return country, city, datetime.date(int(year), int(month), int(day))


def get_city_data():
    """Get dictionary of unique CityFiles objects"""
    cities = {}
    for filename in get_files_list():
        country, city, date = filename_parser(filename)
        if city not in cities:
            cities[city] = CityFiles(city, country)
        cities[city].add_check_date(date)
    return cities


def get_data_from_files():
    """
    Get fresh weather data from files on s3 AWS bucket.
    ...
    :return: data: list
        List of FreshWeather(country, city, temperature, condition)
        namedtuple objects.
    """
    data = []
    for _, city_obj in get_city_data().items():
        filename = city_obj.get_last_check_filename()
        content = download_data_from_file(filename)
        data.append(FreshWeather(
                content['country'],
                content['city'],
                content['temperature'],
                content['condition']))
    return data


def get_statistic_from_files():
    """
    Get statistic from files on s3 AWS bucket.
    ...
    :return: countries: dict
        Dictionary of unique CountryFiles objects.
    """
    countries = {}
    for filename in get_files_list():
        country, _, date = filename_parser(filename)
        if country not in countries:
            countries[country] = CountryFiles(country)
        countries[country].add_check_date(date)
    return countries


def save_data_to_file(data):
    """
    Save weather data in file on s3 AWS bucket.
    ...
    :param data: namedtuple
        WeatherData(country, city, temperature, condition, created_date)
    """
    country, city, created_date, data = xml_to_dict(data)
    filename = f"{country}_{city}_{created_date}.txt"
    content = json.dumps(data)
    upload_data_to_file(filename, content)


def xml_to_dict(data):
    """Covert data from xml to dict.
    ...
    :param data:
        XML string.
    """
    dict_data = xmltodict.parse(data)  # TODO: review type of data
    for _, value in dict_data.items():
        country = value['country']
        city = value['city']
        created_date = datetime.datetime.strptime(
            value['created_date'],
            "%Y-%m-%d %H:%M:%S.%f"
        ).strftime('%Y%m%d')
        del value['created_date']
        return country, city, created_date, value
