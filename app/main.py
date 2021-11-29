"""
fastapi Routes.

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
import uvicorn
from typing import Callable
from fastapi import Request, HTTPException, Response
from fastapi.routing import APIRoute

from app.services import send_data_to_rabbitmq
from app.db_requests import get_data_from_db, get_statistic_from_db
from app.files_requests import get_data_from_files, get_data

from app import app, templates


class ConnectionErrorRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except ConnectionError as exc:
                body = await request.body()
                detail = {"error": str(exc), "body": body.decode()}
                raise HTTPException(status_code=404, detail=detail)
        return custom_route_handler


app.router.route_class = ConnectionErrorRoute


@app.get("/")
def index(request: Request):
    """Route to start page."""
    args = {"request": request}
    return templates.TemplateResponse("start_page.html", args)


@app.get("/weather")
async def check_weather(request: Request, err_msg=None):
    """Route to fresh weather report."""
    try:
        await send_data_to_rabbitmq()
    except ConnectionError as exc:
        err_msg = {"error": str(exc)}
    finally:
        db_data = get_data_from_db()
        files_data = get_data_from_files()
        db_data.extend(files_data)
        db_data.sort(key=lambda x: x.country)
        args = {"request": request, "data": db_data, "err-msg": err_msg}
        return templates.TemplateResponse("check_weather.html", args)


@app.get("/statistic")
def get_statistic(request: Request):
    """Route to weather statistic report."""
    db_data = get_statistic_from_db()
    files_data = get_data(data_type="statistics")
    args = {"request": request,
            "db_data": db_data,
            "files_data": files_data}
    return templates.TemplateResponse("statistics_weather.html", args)


if __name__ == "__main__":
    uvicorn.run("main:app", port=1111, host="127.0.0.1")
