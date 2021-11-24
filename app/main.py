"""
fastapi Routes.
...
Routes:
    @app.get('/')
    index()
        Route to start page.

    @app.get('/weather')
    check_weather()
        Route to fresh weather report.

    @app.get('/statistic')
    get_statistic()
        Route to weather statistic report.
"""
import pathlib
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from app.services import send_data_to_rabbitmq
from app.db_requests import get_data_from_db, get_statistic_from_db
from app.files_requests import get_data_from_files, get_data

app = FastAPI()

BASE_DIR = pathlib.Path(__file__).parent.parent
template_folder = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(template_folder))


@app.get("/")
def index(request: Request):
    """Route to start page."""
    args = {"request": request}
    return templates.TemplateResponse("start_page.html", args)


@app.get("/weather")
async def check_weather(request: Request):  # TODO: try\except if smth wrong
    """Route to fresh weather report."""
    await send_data_to_rabbitmq()
    db_data = get_data_from_db()
    files_data = get_data_from_files()
    db_data.extend(files_data)
    db_data.sort(key=lambda x: x.country)
    args = {"request": request, "data": db_data}
    return templates.TemplateResponse("check_weather.html", args)


@app.get("/statistic")
def get_statistic(request: Request):
    """Route to weather statistic report."""
    db_data = get_statistic_from_db()
    files_data = get_data(data_type="statistics")
    args = {"request": request, "db_data": db_data, "files_data": files_data}
    return templates.TemplateResponse("statistics_weather.html", args)


if __name__ == "__main__":
    uvicorn.run("main:app", port=1111, host="127.0.0.1")
