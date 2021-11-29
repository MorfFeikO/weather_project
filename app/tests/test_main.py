"""Test main.py"""
import pytest

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@pytest.mark.asyncio
@pytest.mark.parametrize("url", ['/', '/statistic', '/weather'])
def test_index(test_session, url):
    """Test routes status code."""
    response = client.get(url)
    assert response.status_code == 200
