"""App config.

Objects:
    config_map: dict{"prod":<value>, "test":<value>}
    PROJECT_DIR
"""
import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

APP_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent


page_url = {
    "base_url": os.getenv("BASE_URL", "http://api.openweathermap.org/data"),
    "version": os.getenv("VERSION", "2.5"),
    "url_path": os.getenv("URL_PATH", "weather"),
}

queries = {
    "city": "q={}",
    "unit": f"units={os.getenv('UNITS', 'metric')}",
    "secret": f"appid={os.getenv('OPEN_WEATHER_API_SECRET')}",
    "mode": f"mode={os.getenv('MODE', 'xml')}",
    }


error_data = b'<?xml version="1.0" encoding="UTF-8"?>' \
             b'<root>' \
             b'<country>XMLValidationError</country>' \
             b'<city></city>'\
             b'<temperature></temperature>' \
             b'<condition></condition>'\
             b'<created_date></created_date>' \
             b'</root>'


def get_default_info() -> dict:
    """Get default country/cities info."""
    return {
        "Ukraine": ("Kyiv", "Dnipro", "Odesa", "Lviv", "Kharkiv"),
        "UK": ("Aberdeen", "Belfast", "Glasgow", "Liverpool", "London"),
        "USA": ("New York", "Los Angeles", "Chicago", "San Diego", "Dallas"),
        "China": ("Hong Kong", "Beijing", "Shanghai", "Guangzhou", "Lanzhou"),
        "Italy": ("Rome", "Milan", "Florence", "Verona", "Venice"),
    }


def create_db_url() -> str:
    """Generate database url."""
    return f"postgresql+pg8000://" \
           f"{os.getenv('POSTGRES_USER')}:" \
           f"{os.getenv('POSTGRES_PASSWORD')}@" \
           f"{os.getenv('POSTGRES_HOST')}/" \
           f"{os.getenv('POSTGRES_DB')}"


def joiner(symbol: str, dict_: dict) -> str:
    """Join dict values to string with given symbol."""
    return symbol.join([value for _, value in dict_.items()])


def create_weather_url_pattern() -> str:
    """Join url path and query."""
    return '?'.join((
        joiner(symbol="/", dict_=page_url),
        joiner(symbol="&", dict_=queries)
    ))


class BaseConfig:
    """Base app config."""
    SECRET_KEY: str = os.getenv('OPEN_WEATHER_API_SECRET')
    SQLALCHEMY_DATABASE_URI: str = create_db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True
    URL_PATTERN: str = create_weather_url_pattern()
    DEFAULT_INFO: dict = get_default_info()
    TEMPLATE_DIR = str(PROJECT_DIR / "templates")
    WEATHER_SCHEMA = str(PROJECT_DIR / "schema.xsd")
    RABBITMQ_HOST: str = os.getenv('RABBITMQ_HOST', "rabbitmq")


class TestingConfig(BaseConfig):
    """Testing app config."""
    TEST_DIR = APP_DIR / "tests"
    SQLALCHEMY_DATABASE_URI: str = \
        f"sqlite:///{TEST_DIR / 'test_db.sqlite3'}?check_same_thread=False"
    RABBITMQ_HOST: str = 'localhost'


config_map = {
    "test": TestingConfig,
    "prod": BaseConfig
}
