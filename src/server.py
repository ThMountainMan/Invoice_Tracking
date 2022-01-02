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
from flask_login import LoginManager
from gevent.pywsgi import WSGIServer

import api
from api.errors import errors
from config import appconfig
from database import DbConnection, User

TEMPLATE_FOLDER = os.path.join(dirname(__file__), "views")
STATIC_FOLDER = os.path.join(dirname(__file__), "static")

log = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

    app.config["SECRET_KEY"] = appconfig.secret_key

    # blueprint for error handling
    app.register_blueprint(errors)

    app = api.register_app_routes(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    if appconfig.debug:
        app.jinja_env.auto_reload = True
        app.config["TEMPLATES_AUTO_RELOAD"] = True

    @login_manager.user_loader
    def load_user(user_id):
        with DbConnection() as db:
            user = db.get("user", user_id)
            return user

    return app


# app = create_app()


def run():
    app = create_app()
    if appconfig.debug:
        app.run(
            host=appconfig.web_host,
            port=appconfig.web_port,
            debug=True,
            use_reloader=False,
        )
    else:
        http_server = WSGIServer((appconfig.web_host, appconfig.web_port), app)
        http_server.serve_forever()
