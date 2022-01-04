"""
fastapi Routes.

Routes:
    @app.get('api/weather')
    check_weather()
        Get weather info.

    @app.get('api/statistic')
    get_statistic()
        Get weather statistic.
"""
from typing import Dict, List, Union
# from typing import Callable
import uvicorn
# from fastapi import Request, Response, HTTPException
# from fastapi.routing import APIRoute

from app.services import send_data_to_rabbitmq
from app.db_requests import get_data_from_db, get_statistic_from_db
from app.files_requests import get_data_from_files, get_statistic_from_files

from app import app


# class ConnectionErrorRoute(APIRoute):
#     """Route which catch ConnectionError."""
#     def get_route_handler(self) -> Callable:
#         """ApiRoute super method rewrite."""
#         original_route_handler = super().get_route_handler()
#
#         async def custom_route_handler(request: Request) -> Response:
#             try:
#                 return await original_route_handler(request)
#             except ConnectionError as exc:
#                 body = await request.body()
#                 detail = {
#                     "request": request,
#                     "error": str(exc),
#                     "body": body.decode()
#                 }
#
#                 return HTTPException(status_code=404, detail=detail)
#         return custom_route_handler
#
#
# app.router.route_class = ConnectionErrorRoute


@app.get("/api/check")
async def check_weather():
    """Make weather request and save data."""
    await send_data_to_rabbitmq()
    return {}


@app.get("/api/weather")
def get_weather() -> List[Dict[str, str]]:
    """Get weather info.

    :return [{"country": "<value>",
              "city": "<value>",
              "temperature": "<value>",
              "condition": "<value>"}, ...]
    """
    data = get_data_from_db()
    data.extend(get_data_from_files())
    data.sort(key=lambda x: x["country"])
    return data


@app.get("/api/statistic")
def get_statistic() -> Dict[str, List[Dict[str, Union[str, int]]]]:
    """Get weather statistic.

    :return {"db": [{"countryName": <value>,
                     "recordsCount": <value>,
                     "lastCheckDate": <value>,
                     "lastCityCheck": <value>}, ...],
             "files": [{"countryName": <value>,
                        "firstCheckDate": <value>,
                        "lastCheckDate": <value>,
                        "countValue": <value>}, ...]}
    """
    return {"db": get_statistic_from_db(),
            "files": get_statistic_from_files()}


if __name__ == "__main__":
    uvicorn.run("main:app", port=1111, host="127.0.0.1")
