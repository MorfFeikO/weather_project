import os
import pathlib

from functools import lru_cache

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from app.config import config_map


DEFAULT_INFO = {
    "Ukraine": ("Kyiv", "Dnipro", "Odesa", "Lviv", "Kharkiv"),
    "UK": ("Aberdeen", "Belfast", "Glasgow", "Liverpool", "London"),
    "USA": ("New York", "Los Angeles", "Chicago", "San Diego", "Dallas"),
    "China": ("Hong Kong", "Beijing", "Shanghai", "Guangzhou", "Lanzhou"),
    "Italy": ("Rome", "Milan", "Florence", "Verona", "Venice"),
}

app = FastAPI()


@lru_cache(maxsize=128)
def get_settings():
    return config_map[os.getenv("CONFIG", "prod")]()


settings = get_settings()

BASE_DIR = pathlib.Path(__file__).parent.parent
template_folder = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(template_folder))

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
session = Session(bind=engine)
base = declarative_base()

base.metadata.create_all(engine)

url_pattern = settings.URL_PATTERN
