from os.path import abspath, dirname

from . import agencys, customer, expenses, invoices, jobtype, personal, website, users

# # Add the Template Path to bottle
# # This is done to run the Scrip on Linux as well
# bottle.TEMPLATE_PATH.insert(
#     0, os.path.join(dirname(dirname(abspath(__file__))), "views")
# )
