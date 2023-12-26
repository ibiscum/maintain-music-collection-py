import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as client:
        yield client

# def test_app():
#     client = TestClient(app)
#     yield client  # testing happens here


