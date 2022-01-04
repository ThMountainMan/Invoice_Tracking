import os, sys
import tempfile
import shutil
import pytest

sys.path.append("./")
sys.path.append("./src")

from src import start, database

# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), "test_data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_path = tempfile.mkdtemp()
    print(db_path)
    # create the app with common test config
    app = start.main(enviroment="test")
    app.config["DB_PATH"] = db_path
    # create the database and load test data
    with app.app_context():
        database.init()
        # get_db().executescript(_data_sql)

        with database.DbConnection() as db:
            db.execute(_data_sql)

    yield app

    # close and remove the temporary database
    shutil.rmtree(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, email="test@super.de", password="password"):
        return self._client.post("/login", data={"email": email, "password": password})

    def logout(self):
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
