"""
Startup script for the Invoice Tracker Webservice
"""

import server
import os
import sys
import site
import logging
import website
from app_config import AppConfig
import database as DB
import create_db_dummys


FORMAT = "[%(levelname)-5s] %(name)-20s %(message)s"

THISDIR = os.path.dirname(__file__)
SVC_NAME = "Invoice_Tracker"
SVC_DISPLAY_NAME = f"_{SVC_NAME}"
DEFAULT_CFG = os.path.abspath(os.path.join(THISDIR, 'config.yml'))

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=FORMAT)

log = logging.getLogger()

# Only for debug. We add additional search pathes to external packages
site.addsitedir(os.path.abspath(
    os.path.join(THISDIR, '..', '.debug')
))


def main(config_file=DEFAULT_CFG, blocking=True, argv=None):
    if os.path.exists(config_file):
        log.info("read config file: %s", config_file)
        # read_config(config_file)
    # else:
        #log.info("create config file: %s", config_file)
        # TODO: Create function to write default config file
        # write_config(config_file)
        #sys.exit(f"Config file {config_file} created!")
    else:
        sys.exit(f"Config file {config_file} not found!")
    init_logger()

    log.info("starting server...")
    #os.makedirs(appconfig.tempdir, exist_ok=True)
    return server.run(blocking=blocking)


def init_logger():
    log.info("init logging: level=%s file=%s", logging.INFO, "server_logging.log")

    level = getattr(logging, 'INFO')
    log.setLevel(level)
    # define a Handler which writes to sys.stdout
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter(FORMAT))
    log.addHandler(console)
    logging.info("log file: %s", "server_logging.log")
    if True:
        fhandler = logging.FileHandler("server_logging.log")
        fhandler.setFormatter(
            logging.Formatter(
                "%(levelname)-8s %(name)-30s %(funcName)-30s "
                "ln:%(lineno)04i %(message)s"
            )
        )
        log.addHandler(fhandler)


if __name__ == "__main__":
    try:
        # Try to read the First entry from the DB
        # If that does not work -> Create Dummy Entrys !!!
        Test = DB.Invoices.get(1)
        print(Test.invoice_id)
    except Exception:
        create_db_dummys.fill_db()

    if True:
        main(blocking=True)
