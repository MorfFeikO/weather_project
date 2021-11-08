"""
Simple fastapi app

Functions:
    pong()
        Simple fastapi test function
"""
import os
import time
import asyncio
import uvicorn

from aiohttp import ClientSession
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


def get_city_url(city: str, unit: str = 'metric'):
    """Get single city url"""
    api = os.getenv('OPEN_WEATHER_API_SECRET')
    return URL_PATTERN.format(city, unit, api)


async def fetch_url_data(session, url, country, city):
    """Get info from single city"""
    try:
        async with session.get(url) as response:
            resp = await response.json()
            city_weather = {
                'country': country,
                'city': city,
                'temperature': resp['main']['temp'],
                'description': resp['weather'][0]['description'],
            }
    except Exception as e:
        print('exc - ', e)
    else:
        return city_weather


@app.get('/cities')
async def main():
    """Get route for all cities"""
    start = time.time()
    tasks = []
    async with ClientSession() as session:
        for country in DEFAULT_INFO:
            for city in DEFAULT_INFO[country]:
                url = get_city_url(city)
                task = asyncio.create_task(fetch_url_data(session, url, country, city))
                tasks.append(task)
        weather = await asyncio.gather(*tasks)
    delta = time.time() - start
    print('DELTA!!!!!!!!!!!!', delta)
    return weather


@app.get('/ping')
def pong():
    """Simple fastapi test function"""
    return {'ping': 'pong!'}


if __name__ == '__main__':
    uvicorn.run("main:app", port=1111, host='127.0.0.1')
