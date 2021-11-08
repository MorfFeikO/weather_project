import time
from main import DEFAULT_INFO, single_city_weather


def find_weather():
    weather_list = []
    for country in DEFAULT_INFO:
        for city in DEFAULT_INFO[country]:
            weather_list.append(single_city_weather(country, city))
    return weather_list


if __name__ == '__main__':
    start = time.time()
    ans = find_weather()
    delta = time.time() - start
    print(delta)
    for el in ans:
        print(el)
