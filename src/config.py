import logging
import os
import secrets
import globconf
from os import environ, path
from dotenv import load_dotenv

log = logging.getLogger(__name__)


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


def root_dir(*names):
    """Get the Current Directory"""
    return os.path.relpath(os.path.join(__file__, "../..", *names))


class AppConfig(globconf.Config):
    """
    Configuration file read and create.
    """

    # Configuration file for Invoice Tracking Tool
    debug = False
    echo = False
    # Use a local db or connect to an existing DB
    local = True

    # Define the Path for the HTML to PDF Converter
    pfd_creator = root_dir("bin\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    tempdir = None
    # database
    # Settings if we want to connect to a remote DB
    db_path = root_dir("db")
    db_migration = root_dir("src", "db_migration")
    # ( only valid if use_local = False )
    db_ip = "192.168.178.71"
    db_port = "3307"
    db_name = "invoice_database"
    db_user = "invoice_tool"
    db_pwd = ""

    secret_key = secrets.token_hex(16)

    # webserver
    # Settings related to the webserver
    web_port = 8080
    web_host = "0.0.0.0"

    # invoices
    # Settings related to the webserver
    invoice_path = root_dir("Invoices")


def read_config(path):
    try:
        appconfig.load(path, clear=False)
    except IOError as e:
        log.warn("Couldn't load config file=%s (error=%s)", path, e)


def write_config(path):
    try:
        appconfig.dump(path)
    except IOError as e:
        log.warn("Couldn't write config file=%s (error=%s)", path, e)


appconfig = AppConfig()
appconfig.init_defaults()


class Config:
    """Base config."""

    SECRET_KEY = environ.get("SECRET_KEY")
    SESSION_COOKIE_NAME = environ.get("SESSION_COOKIE_NAME", "session")
    STATIC_FOLDER = os.path.join(basedir, "static")
    TEMPLATES_FOLDER = os.path.join(basedir, "views")
    LOCAL_DB = True
    DB_MIGRATION = root_dir("src", "db_migration")
    SERVER_PORT = 8080


class ProdConfig(Config):
    """Production config"""

    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    DATABASE_URI = environ.get("PROD_DATABASE_URI")
    LOCAL_DB = True
    DB_MIGRATION = root_dir("src", "db_migration")
    DB_PATH = root_dir("db")
    DB_NAME = "invoice_database"


class DevConfig(Config):
    """Development config"""

    FLASK_ENV = "development"
    DEBUG = True
    ECHO = True
    TESTING = True
    TEMPLATES_AUTO_RELOAD = True
    DATABASE_URI = environ.get("DEV_DATABASE_URI")
    LOCAL_DB = True
    DB_MIGRATION = root_dir("src", "db_migration")
    DB_PATH = root_dir("db")
    DB_NAME = "invoice_database"


class TestConfig(Config):
    """Test config"""

    FLASK_ENV = "development"
    DEBUG = True
    ECHO = True
    TESTING = True
    TEMPLATES_AUTO_RELOAD = False
    DATABASE_URI = environ.get("DEV_DATABASE_URI")
    LOCAL_DB = True
    DB_MIGRATION = root_dir("src", "db_migration")
    DB_PATH = root_dir("db")
    DB_NAME = "test_db"
