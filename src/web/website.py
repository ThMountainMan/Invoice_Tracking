#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

import bottle
from config import appconfig as AppConfig
from bottle import route, static_file

log = logging.getLogger(__name__)


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


@route("/static/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root=os.path.join(os.path.dirname(__file__), "static"))


if __name__ == "__main__":
    bottle.debug(False)
    bottle.run(host=AppConfig.web_host, port=AppConfig.web_port)
