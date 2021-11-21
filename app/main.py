"""
fastapi Routes
"""
import asyncio

import uvicorn
import time
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from app.services import send_data_to_rabbitmq, send_data_to_rabbitmq_old
from app.db_requests import get_data_from_db, get_statistic_from_db, get_data_from_db_async
from app.files_requests import get_data_from_files, get_statistic_from_files, get_data_from_files_async

from app.files_requests_old import get_data_from_files as gf

app = FastAPI()


BASE_DIR = Path(__file__).parent.parent
template_folder = BASE_DIR / 'templates'

templates = Jinja2Templates(directory=str(template_folder))


@app.get('/')
def index(request: Request):
    args = {"request": request}
    return templates.TemplateResponse(
        "start_page.html",
        args
    )


@app.get('/weather')
async def check_weather(request: Request):  # TODO: try\except if smth wrong
    await send_data_to_rabbitmq()  # TODO: here code may run through.

    print('GOING TO PRINT WITHOUT LOADING FULLY')
    start = time.time()
    data = get_data_from_db()
    print('!!!!!!!!!!!!!GET DATA FROM DB time - ', time.time() - start)

    start = time.time()
    data2 = get_data_from_files()
    print('!!!!!!!!!!!!GET DATA FROM FILES time - ', time.time() - start)

    data.extend(data2)
    data.sort(key=lambda x: x.country)
    args = {"request": request, "data": data}
    return templates.TemplateResponse("check_weather.html", args)


@app.get('/weather_async')
async def check_weather2(request: Request):  # TODO: try\except if smth wrong
    full_start = time.time()
    await send_data_to_rabbitmq()  # TODO: here code may run through.
    print('GOING TO PRINT WITHOUT LOADING FULLY')
    """
    start = time.time()
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(get_data_from_db_async()),
        loop.create_task(get_data_from_files_async())
    ]
    data = await asyncio.gather(*tasks)
    print('!!!!!!!!!!!!!GET FULL ASYNC DATA TIME - ', time.time() - start)
    output_data = data[0]
    output_data.extend(data[1])
    output_data.sort(key=lambda x: x.country)
    """

    start = time.time()
    data = await get_data_from_db_async()
    print(data)
    print('!!!!!!!!!!!!!GET DATA FROM DB time - ', time.time() - start)

    start = time.time()
    data2 = await get_data_from_files_async()
    print(data2)
    print('!!!!!!!!!!!!GET DATA FROM FILES time - ', time.time() - start)

    data.extend(data2)
    data.sort(key=lambda x: x.country)
    args = {"request": request, "data": data}
    print('!!!!!!!!!!!!FULL END', time.time() - full_start)
    return templates.TemplateResponse("check_weather.html", args)


@app.get('/weather_old')
async def check_weather(request: Request):  # TODO: try\except if smth wrong
    await send_data_to_rabbitmq_old()  # TODO: here code may run through.

    print('GOING TO PRINT WITHOUT LOADING FULLY')
    start = time.time()
    data = get_data_from_db()
    print('!!!!!!!!!!!!!GET DATA FROM DB time - ', time.time() - start)

    start = time.time()
    data2 = gf()
    print('!!!!!!!!!!!!GET DATA FROM FILES time - ', time.time() - start)

    data.extend(data2)
    data.sort(key=lambda x: x.country)
    args = {"request": request, "data": data}
    return templates.TemplateResponse("check_weather.html", args)


@app.get('/statistic')
def get_statistic(request: Request):
    start = time.time()
    db_data = get_statistic_from_db()
    print('!!!!!!!!!!!!!!!!!STATISTIC FROM DB', time.time() - start)

    start = time.time()
    files_data = get_statistic_from_files()
    print('!!!!!!!!!!!!!!STATISTIC FROM FILES', time.time() - start)

    args = {"request": request, "db_data": db_data, "files_data": files_data}
    return templates.TemplateResponse("statistics_weather.html", args)


if __name__ == '__main__':
    uvicorn.run("main:app", port=1111, host='127.0.0.1')
