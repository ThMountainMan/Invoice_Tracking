#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Startup script for the Invoice Tracker Webservice
"""

import logging
import os
import sys

from config import read_config, write_config

THISDIR = os.path.dirname(__file__)
DEFAULT_CFG = os.path.relpath("config.yaml")


# Only for debug. We add additional search pathes to external packages
# site.addsitedir(os.path.abspath(os.path.join(THISDIR, "..", ".debug")))


def main(config_file=DEFAULT_CFG, enviroment="dev"):
    # Init the Logger Functionality
    log = init_logger()
    # if not os.path.exists(config_file):
    #     log.warning("Create default config file: %s", config_file)
    #     write_config(config_file)
    #     # sys.exit(f"Config file {config_file} created!")

    # log.info("Read config file: %s", config_file)
    # read_config(config_file)
    import server

    app = server.create_app(enviroment)
    if enviroment == "test":
        return app

    import database

    # Init the DB
    log.info("init database...")
    with app.app_context():
        database.init()
    log.info("starting server...")
    return server.run(app=app)


def init_logger():

    FORMAT = "[%(levelname)-5s] %(name)-20s %(message)s"
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=FORMAT)
    log = logging.getLogger()
    log.info("init logging: level=%s file=%s", logging.INFO, "server_logging.log")

    level = getattr(logging, "INFO")
    log.setLevel(level)
    # define a Handler which writes to sys.stdout
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter(FORMAT))
    # log.addHandler(console)
    log.info("log file: %s", "server_logging.log")
    fhandler = logging.FileHandler("server_logging.log")
    fhandler.setFormatter(
        logging.Formatter(
            "%(levelname)-8s %(name)-30s %(funcName)-30s " "ln:%(lineno)04i %(message)s"
        )
    )
    log.addHandler(fhandler)
    return log


if __name__ == "__main__":
    # Validate the DB connection
    # TODO: Do we need to validate the DB connection ?
    # Start the Server
    main()
