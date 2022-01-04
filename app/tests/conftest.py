"""Module with pytest fixtures."""
import datetime
import os
import json
import shutil
import pytest


from app import session, engine, base, settings
from app.models import File, City, Weather

TEST_DIR = settings.TEST_DIR
FOLDER_NAME = ".files_data"
test_folder = TEST_DIR / FOLDER_NAME


@pytest.fixture
def data_folder_with_one_file(folder=test_folder):
    """Test folder with data creation fixture."""
    os.mkdir(folder)
    filename = "China_Beijing_20211121.txt"
    file_data = {
        "country": "China",
        "city": "Beijing",
        "temperature": "23.0",
        "condition": "sunny"
    }

    with open(os.path.join(test_folder, filename), "w", encoding="utf-8") \
            as json_file:
        json.dump(file_data, json_file)
    yield folder
    shutil.rmtree(folder)


@pytest.fixture
def country_file_obj(data_folder_with_one_file, key="statistics"):
    """CountryFile obj for tests."""
    filename = os.listdir(data_folder_with_one_file)
    country_file = File(filename[0], key=key)
    country_file.add_date(country_file.date)
    return country_file


@pytest.fixture
def city_file_obj(data_folder_with_one_file, key="data"):
    """CityFile obj for tests."""
    filename = os.listdir(data_folder_with_one_file)
    country_file = File(filename[0], key=key)
    country_file.add_date(country_file.date)
    return country_file


@pytest.fixture
def test_session():
    """Test db session."""
    base.metadata.create_all(engine)
    with session:
        yield session
    base.metadata.drop_all(engine)


@pytest.fixture
def test_response_data():
    """Test xml response data."""
    return (
        b'<?xml version="1.0" encoding="UTF-8"?>'
        b'<current>'
        b'<city id="702550" name="Lviv">'
        b'<coord lon="24.0232" lat="49.8383"></coord>'
        b'<country>UA</country>'
        b'<timezone>7200</timezone>'
        b'<sun rise="2021-11-15T05:36:15" set="2021-11-15T14:40:59"></sun>'
        b'</city>'
        b'<temperature value="4.21" min="4.21" max="4.21" unit="celsius">'
        b'</temperature>'
        b'<feels_like value="1.56" unit="celsius"></feels_like>'
        b'<humidity value="100" unit="%"></humidity>'
        b'<pressure value="1031" unit="hPa"></pressure>'
        b'<wind>'
        b'<speed value="3" unit="m/s" name="Light breeze"></speed>'
        b'<gusts></gusts>'
        b'<direction value="80" code="E" name="East"></direction>'
        b'</wind>'
        b'<clouds value="90" name="overcast clouds"></clouds>'
        b'<visibility value="5000"></visibility>'
        b'<precipitation mode="no"></precipitation>'
        b'<weather number="701" value="mist" icon="50d"></weather>'
        b'<lastupdate value="2021-11-15T11:03:22"></lastupdate>'
        b'</current>'
    )


@pytest.fixture
def test_file():
    """File obj test data."""
    file = File("China_Beijing_20211121.txt")
    return file


@pytest.fixture
def test_city():
    """CityFiles obj test data."""
    city = File("China_Beijing_20211121.txt", key="data")
    return city


@pytest.fixture
def test_country():
    """CityFiles obj test data."""
    country = File("China_Beijing_20211121.txt", key="statistics")
    return country


@pytest.fixture
def test_data():
    """Test data for db operations."""
    return {
        "country": "China",
        "city": "Beijing",
        "temperature": "23",
        "condition": "clear sky",
        "created_date": datetime.date(2021, 11, 21)
    }


@pytest.fixture
def test_xml():
    """XML data for tests."""
    return (b'<?xml version="1.0" encoding="UTF-8"?>'
            b"<current>"
            b"<country>China</country>"
            b"<city>Beijing</city>"
            b"<temperature>23</temperature>"
            b"<condition>clear sky</condition>"
            b"<created_date>2021-11-21 13:44:28.36545</created_date>"
            b"</current>")


@pytest.fixture
def test_db(test_session):
    """Test db with data."""
    test_session.add(City(name="Beijing", country="China"))
    test_session.commit()
    beijing = test_session.query(City).filter(City.name == "Beijing").one()
    test_session.add(Weather(
        city_id=beijing.id,
        temperature=23.0,
        condition="clear sky",
        created_date=datetime.datetime(2021, 11, 21)))
    test_session.commit()

    test_session.add(City(name="Hong Kong", country="China"))
    test_session.commit()
    hong_kong = test_session.query(City).filter(City.name == "Hong Kong").one()
    test_session.add(Weather(
        city_id=hong_kong.id,
        temperature=20.0,
        condition="sunny",
        created_date=datetime.datetime(2021, 11, 22)))
    test_session.commit()
    yield test_session


@pytest.fixture
def test_db_single_line(test_session):
    """Test db with data."""
    test_session.add(City(name="Beijing", country="China"))
    test_session.commit()
    beijing = test_session.query(City).filter(City.name == "Beijing").one()
    test_session.add(Weather(
        city_id=beijing.id,
        temperature=23.0,
        condition="clear sky",
        created_date=datetime.datetime(2021, 11, 21)))
    test_session.commit()
