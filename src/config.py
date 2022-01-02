import logging
import os
import secrets
import globconf

log = logging.getLogger(__name__)


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
