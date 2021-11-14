"""
Operations with weather data files module.
...
Functions:
    save_data_to_file(data)
        Save weather data to file.

    get_data_from_files()
        Get fresh weather data from files.

    get_statistic_from_data()
        Get statistic from files.
"""
import os
import re
import json
import datetime

from app.models import CityFiles, CountryFiles, FreshWeather


def get_files_list():
    """Get list of files in a weather data path"""
    filepath = get_filepath()
    if os.path.exists(filepath):
        return os.listdir(filepath)
    return []


def get_filepath(data_folder="data"):
    """Get weather data files path"""
    return os.path.join(os.getcwd(), data_folder)


def filename_parser(filename):
    """Parse data from filename"""
    pattern = r'(\D*)_(\D*)_(\d{4})(\d{2})(\d{2})'
    country, city, year, month, day = re.findall(pattern, filename)[0]
    return country, city, datetime.date(int(year), int(month), int(day))


def get_city_objects():
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
    Get fresh weather data from files.
    ...
    :return:
        data: list
            List of FreshWeather(country, city, temperature, condition)
             namedtuple objects.
    """
    data = []
    for _, city_obj in get_city_objects().items():
        file = os.path.join(get_filepath(), city_obj.get_last_check_filename())
        with open(file, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            data.append(FreshWeather(
                json_data['country'],
                json_data['city'],
                json_data['temperature'],
                json_data['condition'])
            )
    return data


def get_statistic_from_files():
    """
    Get statistic from files.
    ...
    :return:
        countries: dict
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
    Save weather data to file
    ...
    :arg:
        data: namedtuple
            WeatherData(country, city, temperature, condition, created_date)
    """
    filepath = get_filepath()
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    filename = f"{data.country}_{data.city}_{data.created_date}.txt"
    with open(os.path.join(filepath, filename), 'w', encoding='utf-8') as json_file:
        json.dump(data_to_json(data), json_file)


def data_to_json(data):
    """Covert data to dict with fields: country, city, temperature, condition."""
    return {
        "country": data.country,
        "city": data.city,
        "temperature": data.temperature,
        "condition": data.condition,
    }
