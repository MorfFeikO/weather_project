# """Test db_requests.py."""
# import datetime
# import pytest
#
# from sqlalchemy.orm import aliased
#
# import app.db_requests
# from app.models import City, Weather, CountryDBStatistic, FreshWeather
# from app.db_requests import (
#     save_city,
#     save_weather,
#     transform_data,
#     get_statistic_from_db,
#     get_data_from_db
# )
#
#
# c = aliased(City, name="c")
# w = aliased(Weather, name="w")
#
#
# def test_save_city(test_session, test_data):
#     """Test save_city()."""
#     save_city(city=test_data["city"], country=test_data["country"])
#     city = test_session.query(c.name, c.country).all()
#     assert len(city) == 1
#     assert city[0].name == "Beijing"
#     assert city[0].country == "China"
#
#
# @pytest.mark.parametrize("country, city, expected_len", [
#     ("China", "Beijing", 1),
#     ("China", "Hong Kong", 2),
# ])
# def test_save_city_duplicate(
#         test_session, test_data, country, city, expected_len
# ):
#     """Test save_city() with duplicate in db."""
#     save_city(city=test_data["city"], country=test_data["country"])
#
#     save_city(city=city, country=country)
#     city = test_session.query(c.name, c.country).all()
#     assert len(city) == expected_len
#
#
# def test_save_weather(test_session, test_data):
#     """Test save_weather()."""
#     save_weather(test_data)
#     city = test_session.query(
#         c.name, c.country, w.temperature, w.condition, w.created_date
#     ).join(c.weather).all()
#     assert len(city) == 1
#     assert city[0].name == "Beijing"
#     assert city[0].country == "China"
#     assert city[0].temperature == float("23")
#     assert city[0].condition == "clear sky"
#     assert city[0].created_date == datetime.datetime(2021, 11, 21)
#
#
# def test_save_weather_duplicate(monkeypatch, test_session, test_data):
#     """Test save_weather() with duplicate in db."""
#
#     def mock_city_save(city=test_data["city"], country=test_data["country"]):
#         test_session.add(City(name=city, country=country))
#         test_session.commit()
#
#     monkeypatch.setattr(app.db_requests, "save_city", mock_city_save)
#
#     save_weather(test_data)
#     city = test_session.query(
#         c.name, c.country, w.temperature, w.condition, w.created_date
#     ).join(c.weather).all()
#     assert len(city) == 1
#     assert city[0].temperature == float("23")
#     assert city[0].condition == "clear sky"
#     assert city[0].created_date == datetime.datetime(2021, 11, 21)
#
#
# @pytest.mark.parametrize("bytes_data", [
#     (b"<root><country>China</country><city>Beijing</city>"
#      b"<temperature>23</temperature><condition>clear sky</condition>"
#      b"<created_date>2021-11-21 13:44:28.36545</created_date></root>")
# ])
# def test_transform_data(bytes_data):
#     """Test transform_data()."""
#     test_result = transform_data(bytes_data)
#     assert isinstance(test_result, dict)
#     assert len(test_result) == 5
#     assert test_result["country"] == "China"
#
#
# def test_get_statistic_from_db(test_db):
#     """Test get_statistic_from_db()."""
#     test_result = get_statistic_from_db()
#     assert isinstance(test_result, dict)
#     assert len(test_result) == 1
#     for _, statistic in test_result.items():
#         isinstance(statistic, CountryDBStatistic)
#         assert statistic.country == "China"
#         assert statistic.records == 2
#         assert statistic.last_check == "00:00 22 nov 2021"
#         assert statistic.last_city == "Hong Kong"
#
#
# def test_get_statistic_from_db_empty(test_session):
#     """Test get_statistic_from_db() empty db."""
#     test_result = get_statistic_from_db()
#     assert isinstance(test_result, dict)
#     assert len(test_result) == 0
#
#
# def test_get_data_from_db(test_db):
#     """Test get_data_from_db()."""
#     test_result = get_data_from_db()
#     assert isinstance(test_result, list)
#     assert len(test_result) == 2
#     for data in test_result:
#         assert isinstance(data, FreshWeather)
#         assert data.country == "China"
#
#
# def test_get_data_from_db_empty(test_session):
#     """Test get_data_from_db() empty db."""
#     test_result = get_data_from_db()
#     assert isinstance(test_result, list)
#     assert len(test_result) == 0
