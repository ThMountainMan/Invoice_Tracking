#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

import flask
from config import appconfig
from server import app

log = logging.getLogger(__name__)


# =========================================
# BASIC FUNCTIONS
# =========================================


@app.route("/export/<year>")
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


# @app.route("/static/<filepath>")
# def server_static(filepath):
#     return static_file(filepath, root=os.path.join(os.path.dirname(__file__), "static"))
