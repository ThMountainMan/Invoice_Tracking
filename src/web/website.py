#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from os.path import abspath, dirname

import bottle
import database as DB

import pandas as pd
from app_config import AppConfig
from bottle import redirect, request, route, static_file, template
from dateutil import parser

from . import process_form_data as fData

log = logging.getLogger(__name__)


# Add the Template Path to bottle
# This is done to run the Scrip on Linux as well
bottle.TEMPLATE_PATH.insert(
    0, os.path.join(dirname(dirname(abspath(__file__))), "views")
)


# =========================================
# BASIC FUNCTIONS
# =========================================


@route("/export/<year:int>")
def export_csv(year=None):
    """[summary]

    Args:
        year ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    # https://stackoverflow.com/questions/29525808/sqlalchemy-orm-conversion-to-pandas-dataframe
    # pd.read_sql(db.query(Invoices).statement, dbObject._session().bind)

    pass


@route("/static/<path>/<filename>")
def server_static(path, filename):
    return static_file(
        filename, root=os.path.join(os.path.dirname(__file__), "static", path)
    )


if __name__ == "__main__":
    bottle.debug(False)
    bottle.run(host=AppConfig.web_host, port=AppConfig.web_port)
