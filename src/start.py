#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import check_db

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
        log.info("Read config file: %s", config_file)
        # read_config(config_file)
    else:
        log.info("Create default config file: %s", config_file)
        AppConfig._createdefault()
        sys.exit(f"Config file {config_file} created!")

    # Init the Logger Functionality
    init_logger()

    log.info("starting server...")

    return server.run(blocking=blocking)


def init_logger():
    log.info("init logging: level=%s file=%s",
             logging.INFO, "server_logging.log")

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
    # Validate the DB connection
    if not check_db.DB_Validation():
        # If no data is available create dummy data
        check_db.DB_CreateDummys()

    # Start the Server
    if True:
        main(blocking=True)
