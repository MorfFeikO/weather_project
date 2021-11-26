import os
import pathlib


PROJECT_DIR = pathlib.Path(__file__).resolve().parent
BASE_DIR = PROJECT_DIR.parent


def create_db_url() -> str:
    """Generate database url."""
    return f"postgresql+pg8000://" \
           f"{os.getenv('POSTGRES_USER')}:" \
           f"{os.getenv('POSTGRES_PASSWORD')}@" \
           f"{os.getenv('POSTGRES_HOST')}/" \
           f"{os.getenv('POSTGRES_DB')}"


class BaseConfig:
    """Base app config."""
    SECRET_KEY = os.getenv('OPEN_WEATHER_API_SECRET')
    SQLALCHEMY_DATABASE_URI = create_db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(BaseConfig):
    """Testing app config."""
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'db.sqlite3'}"


config_map = {
    "test": TestingConfig,
    "prod": BaseConfig
}
