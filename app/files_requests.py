"""
Operations with weather data files module.

Functions:
    save_data_to_file(data)
        Save weather data to file.

    get_data_from_files()
        Get fresh weather data from files.

    get_statistic_from_data()
        Get statistic from files.
"""
import os
import json
import datetime
import xmltodict

from app.models import FreshWeather, File


def get_files_list():
    """Get list of files in a weather data path."""
    filepath = get_filepath()
    if os.path.exists(filepath):
        return os.listdir(filepath)
    return []


def get_filepath(data_folder="files_data"):
    """Get weather data files path."""
    return os.path.join(os.getcwd(), data_folder)


def get_data(data_type):
    """"""
    dict_ = {}
    for filename in get_files_list():
        try:
            file_obj = File(filename, key=data_type)
            if file_obj.get_name() not in dict_:
                dict_[file_obj.get_name()] = file_obj
            dict_[file_obj.get_name()].add_date(file_obj.get_date())
        except IndexError:
            continue  # log info
        except ValueError:
            continue  # log info
    return dict_


def get_data_from_files():
    """Get fresh weather data from files.

    :return data: list
        List of FreshWeather(country, city, temperature, condition)
        namedtuple objects.
    """
    data = []
    for _, city_obj in get_data(data_type="data").items():
        filepath = get_filepath()
        file = os.path.join(filepath, city_obj.get_filename())
        with open(file, "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)
            data.append(
                FreshWeather(
                    json_data["country"],
                    json_data["city"],
                    json_data["temperature"],
                    json_data["condition"],
                )
            )
    return data


def save_data_to_file(data):
    """Save weather data to file.

    :arg data: namedtuple
        WeatherData(country, city, temperature, condition, created_date)
    """
    filepath = get_filepath()  # TODO: validate xml data
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    country, city, created_date, data = xml_to_dict(data)
    filename = f"{country}_{city}_{created_date}.txt"
    with open(os.path.join(filepath, filename), "w", encoding="utf-8") as json_file:
        json.dump(data, json_file)


def xml_to_dict(data):
    """Covert data from xml to dict.

    :param data: bytes
        XML bytes string.
    :return tuple(country, city, created_date, value)
        Country name, city name, created date and
        value = {'country': <value>,
                 'city': <value>,
                 'temperature': <value>,
                 'condition': <value>}
    """
    dict_data = xmltodict.parse(data)
    for _, value in dict_data.items():
        country = value["country"]
        city = value["city"]
        created_date = datetime.datetime.strptime(
            value["created_date"], "%Y-%m-%d %H:%M:%S.%f"
        ).strftime("%Y%m%d")
        del value["created_date"]
        return country, city, created_date, value
