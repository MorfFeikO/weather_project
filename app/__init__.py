"""App initialize.

Objects:
    app: FastAPI()
    templates: Jinja2Templates()
    session: Session()
    base: declarative_base()
    url_pattern: str
    default_info: str
"""
import os

from functools import lru_cache

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from app.config import config_map, PROJECT_DIR, ERROR_DATA


app = FastAPI()


@lru_cache(maxsize=128)
def get_settings():
    """Get app config settings."""
    return config_map[os.getenv("CONFIG", "prod")]()


settings = get_settings()

templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
session = Session(bind=engine)
base = declarative_base()
base.metadata.create_all(engine)

url_pattern = settings.URL_PATTERN
default_info = settings.DEFAULT_INFO
weather_schema = settings.WEATHER_SCHEMA
rabbitmq_host = settings.RABBITMQ_HOST
