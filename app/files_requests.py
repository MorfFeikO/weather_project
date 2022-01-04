"""
Operations with weather data files module.

Functions:
    save_data_to_file(data)
        Save weather data to file.

    get_data_from_files()
        Get fresh weather data from files.

    get_statistic_from_files()
        Get statistic from files.
"""
import os
import json
import datetime
import logging
from typing import List, Optional, Tuple, Dict
import xmltodict

from app.models import File
from app.utils import process_message


def get_filepath(data_folder: str = ".files_data") -> str:
    """Get weather data files path.

    :param data_folder: str
        Default: "files_data"
    """
    if not data_folder:
        logging.warning("Empty folder name. Created default folder.")
        return get_filepath()
    filepath = os.path.join(os.getcwd(), data_folder)
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    return filepath


def get_files_list() -> List[Optional[str]]:
    """Get list of files in a weather data path."""
    filepath = get_filepath()
    if os.path.exists(filepath):
        return os.listdir(filepath)
    return []


def get_data(data_type: str) -> dict:
    """Get data from file names in stored folder.

    :param data_type: str
        "data" -> Get cities data.
            :return: {"<city_name>": CityFile(), ...}

        "statistics" -> Get countries statistics.
            :return: {"<country_name>": CountryFile(), ...}
    """
    dict_ = {}
    for filename in get_files_list():
        try:
            file_obj = File(filename, key=data_type)
            if file_obj.name not in dict_:
                dict_[file_obj.name] = file_obj
            dict_[file_obj.name].add_date(file_obj.date)
        except (IndexError, ValueError, ):
            logging.error("""
            There is a file with wrong data pattern in files folder.
            """)
            continue
    return dict_


def get_statistic_from_files() -> List[Dict[str, str]]:
    """Get statistic from files.

    :return: [{"countryName": <value>,
               "firstCheckDate": <value>,
               "lastCheckDate": <value>,
               "countValue": <value>}, ...]
    """
    result = []
    data = get_data(data_type=TYPE["statistics"])
    for _, value in data.items():
        result.append(
            {"countryName": value.name,
             "firstCheckDate": value.first_check,
             "lastCheckDate": value.last_check,
             "countValue": value.count}
        )
    return result


def get_data_from_files() -> List[Dict[str, str]]:
    """Get fresh weather data from files.

    :return: [{"country": "<value>",
               "city": "<value>",
               "temperature": "<value>",
               "condition": "<value>"}, ...]
    """
    result = []
    data = get_data(data_type=TYPE["data"])
    for _, city_file in data.items():
        result.append(load_data_from_single_file(city_file))
    return result


def load_data_from_single_file(city_file):
    """Get fresh weather data from single file.

    :return: {"country": "<value>",
              "city": "<value>",
              "temperature": "<value>",
              "condition": "<value>"}
    """
    file = os.path.join(get_filepath(), city_file.last_check_filename)
    with open(file, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


@process_message
async def save_data_to_file(data: bytes) -> None:
    """Save weather data to file.

    :param data: bytes
        XML weather data.
    """
    country, city, created_date, weather_data = xml_to_dict(data)
    filename = f"{country}_{city}_{created_date}.txt"
    with open(os.path.join(get_filepath(), filename), "w", encoding="utf-8") \
            as json_file:
        json.dump(weather_data, json_file)


def xml_to_dict(data: bytes) -> Tuple[str, str, str, Dict[str, str]]:
    """Convert data from xml to dict.

    :param data: bytes
        XML weather data.
    :return country,
            city,
            created_date,
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


TYPE = {
    "data": "data",
    "statistics": "statistics"
}
