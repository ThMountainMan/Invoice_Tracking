"""
Implementing the general bottle setup with the additional feature to support
a threaded (non blocking) execution
"""

import logging
import threading

from os.path import abspath, dirname
import os

import flask
from flask import Flask
from gevent import monkey
from gevent.pywsgi import WSGIServer

from config import appconfig as AppConfig

# Apply GEVENT patches to bottle server to enable asynchronous functionality
monkey.patch_all()

TEMPLATE_FOLDER = os.path.join(dirname(dirname(abspath(__file__))), "src", "views")
STATIC_FOLDER = os.path.join(
    dirname(dirname(abspath(__file__))), "src", "web", "static"
)

app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

log = logging.getLogger(__name__)


class ServerThread(threading.Thread):
    def __init__(self, server, **kwargs):
        log.info("initalizing threaded server")
        self.server = server
        threading.Thread.__init__(self, **kwargs)

    def stop(self, wait=True, timeout=None):
        log.info("shutdown threaded server")
        self.server.srv.close()
        if wait:
            self.join(timeout=timeout)


# @bottle.error(500)
def _error_handler_500(error):
    """Log internal errors and call the default handler."""
    log.error("http error 500:\n%s\n%s", error.exception, error.traceback)
    return flask.app.default.default_error_handler(error)


def _run(**kwargs):
    # bottle.run(**kwargs)
    kwargs["server"].serve_forever()


def run(blocking=True):
    server = WSGIServer((AppConfig.web_host, AppConfig.web_port), app)
    kwargs = {
        "server": server,
        "quiet": AppConfig.debug,
        "debug": AppConfig.debug,
    }
    if blocking:
        log.info("start blocking http server")
        _run(**kwargs)
    else:
        log.info("start non-blocking http server")
        thread = ServerThread(server, target=_run, kwargs=kwargs)
        thread.start()
        return thread
