"""
SQLAlchemy db models and db connection module.

Objects:
    session_sql:
        Bound session object.

Classes:
    Weather:
        Database weather model.
    City:
        Database city model.
"""
import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()

engine = create_engine(
    f"postgresql+pg8000://"
    f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
)
conn = engine.connect()
session_sql = Session(bind=engine)
base = declarative_base()


class Weather(base):
    """
    Database weather model.
    ...
    :args:
        id: Integer, pk
        city_id: ForeignKey("City.id")
        temperature: Float
        condition: String(100)
        created_date: DateTime()
    """

    __tablename__ = "weather"

    id = Column("id", Integer, primary_key=True)
    city_id = Column("city_id", ForeignKey("city.id"))
    temperature = Column("temperature", Float)
    condition = Column("condition", String(100))
    created_date = Column("created_date", DateTime())


class City(base):
    """
    Database city model.
    ...
    :args:
        id: Integer, pk
        name: String(85)
        country: String(56)
        UniqueConstraint(name, country)
    """

    __tablename__ = "city"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(85))
    country = Column("country", String(56))
    weather = relationship("Weather", cascade="all,delete", backref="city")

    __table_args__ = (UniqueConstraint("name", "country", name="location"),)


base.metadata.create_all(engine)
