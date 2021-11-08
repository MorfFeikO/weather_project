"""
Simple fastapi app

Functions:
    pong()
        Simple fastapi test function
"""

import os
import requests
import asyncio

from fastapi import FastAPI
from dotenv import load_dotenv


app = FastAPI()
load_dotenv()


URL_PATTERN = 'http://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid={}'
DEFAULT_INFO = {
    'Ukraine': ('Kyiv', 'Dnipro', 'Odesa', 'Lviv', 'Kharkiv'),
    'United Kingdom': ('Aberdeen', 'Belfast', 'Glasgow', 'Liverpool', 'London'),
    'USA': ('New York', 'Los Angeles', 'Chicago', 'San Diego', 'Dallas'),
    'China': ('Hong Kong', 'Beijing', 'Shanghai', 'Guangzhou', 'Lanzhou'),
    'Italy': ('Rome', 'Milan', 'Florence', 'Verona', 'Venice')
}
# mode param to xml, to get xml format


@app.get('/ping')
def pong():
    """Simple fastapi test function"""
    return {'ping': 'pong!'}


def single_city_weather(country: str, city: str, unit: str = 'metric'):
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
