import pytest

from app import app, session, engine, base


@pytest.fixture
def test_session():
    base.metadata.create_all(engine)
    with session:
        yield session
    base.metadata.drop_all(engine)
