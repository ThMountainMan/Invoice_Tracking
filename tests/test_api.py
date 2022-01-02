import sys

import pytest

sys.path.append("./")
sys.path.append("./src")

from src.server import create_app

app = create_app()


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index(client):
    assert client.get("/").status_code == 302


def test_health(client):
    assert client.get("/agencys").status_code == 302
