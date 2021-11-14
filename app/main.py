"""
fastapi Routes
"""

import uvicorn

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from app.services import replace_with_rabbitmq
from app.db_requests import get_data_from_db, get_statistic_from_db
from app.files_requests import get_data_from_files, get_statistic_from_files

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get('/')
def index(request: Request):
    args = {"request": request}
    return templates.TemplateResponse("start_page.html", args)


@app.get('/weather')
def check_weather(request: Request):  # TODO: try\except if smth wrong
    replace_with_rabbitmq()
    data = get_data_from_db()
    data.extend(get_data_from_files())
    data.sort(key=lambda x: x.country)
    args = {"request": request, "data": data}
    return templates.TemplateResponse("check_weather.html", args)


@app.get('/statistic')
def get_statistic(request: Request):
    db_data = get_statistic_from_db()
    files_data = get_statistic_from_files()
    args = {"request": request, "db_data": db_data, "files_data": files_data}
    return templates.TemplateResponse("statistics_weather.html", args)


if __name__ == '__main__':
    uvicorn.run("main:app", port=1111, host='127.0.0.1')
