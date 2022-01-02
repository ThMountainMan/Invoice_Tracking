# from . import agencys, customer, expenses, invoices, jobtype, personal, website, users

# Add all blueprints to the app
from .agencys import setup_agencys
from .authentification import auth as bp_auth
from .customer import setup_customers
from .expenses import app_expenses
from .invoices import app_invoices
from .jobtype import setup_jobtypes
from .personal import setup_personal
from .users import setup_users


def register_app_routes(app):
    app.register_blueprint(setup_agencys)
    app.register_blueprint(setup_customers)
    app.register_blueprint(setup_jobtypes)
    app.register_blueprint(setup_personal)
    app.register_blueprint(setup_users)

    app.register_blueprint(bp_auth)
    app.register_blueprint(app_expenses)
    app.register_blueprint(app_invoices)

    return app
