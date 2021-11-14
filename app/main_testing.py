"""
Synchron module for comparison with async
"""

import time
import os
import requests
from app.services import DEFAULT_INFO, URL_PATTERN


def find_weather():
    """Find weather in all cities synchron"""
    weather_list = []
    for country, cities in DEFAULT_INFO.items():
        for city in cities:
            weather_list.append(single_city_weather(country, city))
    return weather_list


def single_city_weather(country: str, city: str, unit: str = 'metric'):
    """Find weather in single city synchron"""
    api = os.getenv('OPEN_WEATHER_API_SECRET')
    url = URL_PATTERN.format(city, unit, api)
    response = requests.get(url)
    if response.status_code != 200:
        print('Error in city', city)
    city_weather = {
        'country': country,
        'city': city,
        'temperature': response.json()['main']['temp'],
        'description': response.json()['weather'][0]['description'],
    }
    return city_weather


if __name__ == '__main__':
    start = time.time()
    ans = find_weather()
    delta = time.time() - start
    print(delta)
    for el in ans:
        print(el)
