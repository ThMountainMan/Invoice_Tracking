"""
Implementing the general bottle setup with the additional feature to support
a threaded (non blocking) execution
"""
from gevent import monkey

# monkey.patch_all()

import logging
import os
from os.path import dirname

from flask import Flask
from flask_login import LoginManager
from gevent.pywsgi import WSGIServer

import api
from api.errors import errors
from config import appconfig, ProdConfig, DevConfig, TestConfig
from database import DbConnection, User

TEMPLATE_FOLDER = os.path.join(dirname(__file__), "views")
STATIC_FOLDER = os.path.join(dirname(__file__), "static")

log = logging.getLogger(__name__)


def create_app(enviroment="dev"):
    app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

    if enviroment == "prd":
        app.config.from_object(ProdConfig)
    elif enviroment == "dev":
        app.config.from_object(DevConfig)
    elif enviroment == "test":
        app.config.from_object(TestConfig)
    else:
        log.error("No Valid enviroment Selected!!!")

    # Overwrite the appconfig values for the DB Connection in order to init the DB properly
    appconfig.db_migration = app.config["DB_MIGRATION"]
    appconfig.db_path = app.config["DB_PATH"]
    appconfig.db_name = app.config["DB_NAME"]

    # app.config["SECRET_KEY"] = appconfig.secret_key

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


def run(app):
    # app = create_app()
    if app.config["DEBUG"]:
        app.run(
            host="0.0.0.0",
            port=app.config["SERVER_PORT"],
            debug=app.config["DEBUG"],
            use_reloader=False,
        )
    else:
        http_server = WSGIServer(("0.0.0.0", app.config["SERVER_PORT"]), app)
        http_server.serve_forever()
