import pytest
from flask import session


def test_login_attempt(client, auth):
    # test that viewing the page renders without template errors
    assert client.get("http://localhost/login").status_code == 200

    # test that successful login redirects to the index page
    response = auth.login()
    assert response.headers["Location"] == "http://localhost/"

    # login request set the user_id in the session
    # check that the user is loaded from the session
    with client:
        client.get("http://localhost/")
        assert session["_user_id"] == "1"


def test_register(client, app, database):
    # test that viewing the page renders without template errors
    assert client.get("/signup").status_code == 200

    # test that successful registration redirects to the login page
    response = client.post("/signup", data={"email": "a", "password": "a"})
    assert "http://localhost/login" == response.headers["Location"]

    # test that the user was inserted into the database
    with database() as db:
        user = db.query("user", filters={"email": "a"})
        assert user
        assert user[0].email == "a"
