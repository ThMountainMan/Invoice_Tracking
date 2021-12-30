"""
Implementing the general bottle setup with the additional feature to support
a threaded (non blocking) execution
"""
from gevent import monkey

monkey.patch_all()

import logging
import os
from os.path import dirname

from flask import Flask
from gevent.pywsgi import WSGIServer

from api.errors import errors
from config import appconfig

TEMPLATE_FOLDER = os.path.join(dirname(__file__), "views")
STATIC_FOLDER = os.path.join(dirname(__file__), "static")


app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)
app.register_blueprint(errors)


log = logging.getLogger(__name__)


def run():
    if appconfig.debug:

        app.jinja_env.auto_reload = True
        app.config["TEMPLATES_AUTO_RELOAD"] = True

        app.run(
            host=appconfig.web_host,
            port=appconfig.web_port,
            debug=True,
            use_reloader=False,
        )
    else:
        http_server = WSGIServer((appconfig.web_host, appconfig.web_port), app)
        http_server.serve_forever()
