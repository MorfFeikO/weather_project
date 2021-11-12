"""
fastapi Routes
"""

import uvicorn

from fastapi import FastAPI

from app.services import replace_with_rabbitmq
from app.db_requests import fetch_data_from_db, get_statistic_from_db
from app.files_requests import fetch_data_from_files, get_statistic_from_files

app = FastAPI()


@app.get('/weather')
def check_weather():
    replace_with_rabbitmq()
    db_data = fetch_data_from_db()
    files_data = fetch_data_from_files()
    return [db_data, files_data]


@app.get('/statistic')
def get_statistic():
    db_data = get_statistic_from_db()
    files_data = get_statistic_from_files()
    return [db_data, files_data]


if __name__ == '__main__':
    uvicorn.run("main:app", port=1111, host='127.0.0.1')
