from flask import session
import pytest


def test_index(client):
    assert client.get("/").status_code == 302


def test_login(client):
    assert client.get("/login").status_code == 200


def test_signup(client):
    assert client.get("/signup").status_code == 200


@pytest.mark.parametrize(
    "page",
    ["/agencys", "/customers", "/expenses", "/jobtypes", "/personal", "/users"],
)
def test_no_access(client, page):
    assert client.get(page).status_code == 302

    with client:
        client.get(page)
        assert session["_flashes"][0][1] == "Please log in to access this page."
