"""Test main.py"""
import pytest

from fastapi.testclient import TestClient

import app.files_requests
import app.db_requests
import app.services
from app import settings
from app.main import app as fast_app


TEST_DIR = settings.TEST_DIR

client = TestClient(fast_app)


@pytest.fixture
def monkeypatch_fixture(monkeypatch):
    """Monkeypatch main.py relative functions fixture."""
    monkeypatch.setattr(app.files_requests, "save_data_to_file", None)
    monkeypatch.setattr(app.files_requests, "get_data_from_files", [])
    monkeypatch.setattr(app.db_requests, "save_data_to_db", None)
    monkeypatch.setattr(app.db_requests, "get_data_from_db", [])
    monkeypatch.setattr(app.db_requests, "get_statistic_from_db", {})


@pytest.mark.asyncio
@pytest.mark.usefixtures("test_session", "monkeypatch_fixture")
@pytest.mark.parametrize("url", ['/', '/statistic', '/weather'])
def test_main(monkeypatch, url):
    """Test routes status code."""

    def mock_get_data(data_type):
        _ = data_type
        return {}

    monkeypatch.setattr(app.services, "send_data_to_rabbitmq", None)
    monkeypatch.setattr(app.files_requests, "get_data", mock_get_data)

    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.usefixtures("test_session", "monkeypatch_fixture")
@pytest.mark.parametrize("url", ['/', '/statistic', '/weather'])
def test_connection_error(monkeypatch, url):
    """Test routes status code."""

    def mock_get_data(data_type):
        _ = data_type
        raise ConnectionError("testing error")

    monkeypatch.setattr(app.services, "send_data_to_rabbitmq", None)
    monkeypatch.setattr(app.files_requests, "get_data", mock_get_data)

    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.usefixtures("test_session", "monkeypatch_fixture")
@pytest.mark.parametrize("url", ['/', '/statistic', '/weather'])
def test_rabbit_connection_error(monkeypatch, url):
    """Test routes status code."""

    def mock_get_data(data_type):
        _ = data_type
        return {}

    def mock_rabbit():
        raise ConnectionError("testing error")

    monkeypatch.setattr(app.services, "send_data_to_rabbitmq", mock_rabbit)
    monkeypatch.setattr(app.files_requests, "get_data", mock_get_data)

    response = client.get(url)
    assert response.status_code == 200
