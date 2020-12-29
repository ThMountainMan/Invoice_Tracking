# Helper to interact with the Database

import yaml
from mysql.connector import connect, Error


def _ParseConfig():
    with open("../recources/db_config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
    return cfg["database"]


class Database:
    def __init__(self, config):
        self._conn = connect(host=config.get('address'),
                             user=config.get('user'),
                             password=config.get('password'),
                             database=config.get('database'))
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()


def establish_connection():
    """ Establish a Database Connection """

    try:
        config = _ParseConfig()
    except Exception as e:
        raise FileNotFoundError(f"The Config File could not be found :(\n{e}")

    print("Establishing Connection to :\n")
    print(f" - Database : {config.get('address')}")
    print(f" - User : {config.get('user')}")

    # TODO: Implement DB Connection
    """ Here the connection part will happen """


# ----------------------------------------------------------------
# Methods to retrieve Information from the Database
# ----------------------------------------------------------------


def get_invoices(db_connection, filter=None):
    """ Get all available invoices - filter is optional """
    pass


def get_customers(db_connection, filter=None):
    """ Get all available customers - filter is optional """
    pass


def get_agencys(db_connection, filter=None):
    """ Get all available agencys - filter is optional """
    pass


# ----------------------------------------------------------------
# Methods to create Information in the Database
# ----------------------------------------------------------------


def create_invoice(db_connection, arg):
    """ Create a new invoice in the database """
    pass


def create_customer(db_connection, arg):
    """ Create a new customer in the database """
    pass


def create_agency(db_connection, arg):
    """ Create a new agency in the database """
    pass


# ----------------------------------------------------------------
# Methods to edit Information in the Database
# ----------------------------------------------------------------


def edit_invoice(db_connection, arg):
    """ Edit an invoice in the database """
    pass


def edit_customer(db_connection, arg):
    """ Create a customer in the database """
    pass


def edit_agency(db_connection, arg):
    """ Create a agency in the database """
    pass


if __name__ == '__main__':
    establish_connection()
