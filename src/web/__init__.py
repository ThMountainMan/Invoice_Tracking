import logging
import os
from os.path import abspath, dirname

import bottle

from . import agencys, customer, expenses, invoices, jobtype, personal, website

# Add the Template Path to bottle
# This is done to run the Scrip on Linux as well
bottle.TEMPLATE_PATH.insert(
    0, os.path.join(dirname(dirname(abspath(__file__))), "views")
)
