import os
import re
import json
import datetime

from app.models import CityFiles, CountryFiles


def save_data_to_file(data):
    data_folder = "data"
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    filename = f"{data.country}_{data.city}_{data.created_date}.txt"
    with open(os.path.join(data_folder, filename), 'w', encoding='utf-8') as json_file:
        json.dump(data._asdict(), json_file)


def filename_parser(filename):
    pattern = r'(\D*)_(\D*)_(\d{4})(\d{2})(\d{2})'
    country, city, year, month, day = re.findall(pattern, filename)[0]
    return country, city, datetime.date(int(year), int(month), int(day))


def fetch_data_from_files():
    data_folder = "data"
    d = []
    if os.path.exists(data_folder):
        filepath = os.path.join(os.getcwd(), data_folder)
        files = os.listdir(filepath)

        cities = {}
        for filename in files:
            country, city, date = filename_parser(filename)
            if city not in cities:
                cities[city] = CityFiles(city, country)
            cities[city].add_check_date(date)

        for city_name, city_obj in cities.items():
            filename = city_obj.get_last_check_filename()
            with open(os.path.join(filepath, filename), 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                d.append(data)
    return d


def get_statistic_from_files():
    data_folder = "data"
    countries = {}
    if os.path.exists(data_folder):
        files = os.listdir(os.path.join(os.getcwd(), data_folder))
        for filename in files:
            country, _, date = filename_parser(filename)
            if country not in countries:
                countries[country] = CountryFiles(country)
            countries[country].add_check_date(date)
    return countries
