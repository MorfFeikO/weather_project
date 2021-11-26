import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

PROJECT_DIR = pathlib.Path(__file__).resolve().parent
BASE_DIR = PROJECT_DIR.parent


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
    SECRET_KEY = os.getenv('OPEN_WEATHER_API_SECRET')
    SQLALCHEMY_DATABASE_URI: str = create_db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    URL_PATTERN: str = create_weather_url_pattern()


class TestingConfig(BaseConfig):
    """Testing app config."""
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'db.sqlite3'}"


config_map = {
    "test": TestingConfig,
    "prod": BaseConfig
}
