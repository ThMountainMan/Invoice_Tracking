# Helper to interact with the Database

import yaml
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, VARCHAR, DECIMAL
from sqlalchemy import ForeignKey


def _ParseConfig():
    with open("../recources/db_config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
    return cfg


class Database:
    def __init__(self):
        # Parse the config file to get the connection details
        self._ParseConfig()
        # Create the connection engine
        self._engine = db.create_engine(f"mysql+pymysql://{self.user}:{self.pw}@{self.host}:{self.port}/{self.database}")
        self._conn = self._engine.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _ParseConfig(self):
        with open("../recources/db_config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)

        self.config = cfg["database"]
        self.user = self.config.get('user')
        self.pw = self.config.get('password')
        self.host = self.config.get('address')
        self.port = self.config.get('port')
        self.database = self.config.get('database')

    @property
    def connection(self):
        return self._conn

    @property
    def engine(self):
        return self._engine

    def session(self):
        return self._session

    def close(self, commit=True):
        self.connection.close()

    def rollback(self):
        self.connection.rollback()

    def execute(self, sql, params=None):
        pass

    def fetchall(self):
        pass

    def fetchone(self):
        pass

    def query(self, sql, params=None):
        pass


# =========================================
# Configuration of the DB Connection Object
# =========================================

# Define the Base for the Database assignement
Base = declarative_base()

# Define a DB session
dbObject = Database()
Session = sessionmaker(bind=dbObject.engine)
session = Session()

# =========================================
# Definition for DB Interaction
# =========================================

# ===========
# INVOICES
# ===========


class Invoice(Base):
    """ DB Interaction class for Invoices """

    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    invoice_id = Column(VARCHAR)
    date = Column(Date)
    description = Column(VARCHAR)
    invoice_ammount = Column(DECIMAL)
    invoice_mwst = Column(DECIMAL)
    paydate = Column(Date)

    customer_id = Column(Integer, ForeignKey("customers.id"))
    jobcode_id = Column(Integer, ForeignKey("jobtypes.id"))
    agency_id = Column(Integer, ForeignKey("agencys.id"))

    customer = relationship("Customer", foreign_keys=[customer_id])
    jobcode = relationship("Jobtype", foreign_keys=[jobcode_id])
    agency = relationship("Agency", foreign_keys=[agency_id])

    def get_all(self, arg):
        pass

    def get(self, arg):
        pass

    def update(self, arg):
        pass

    def edit(self, arg):
        pass

    def delete(self, arg):
        pass


# ===========
# CUSTOMERS
# ===========


class Customer(Base):
    """ DB Interaction class for Customers """

    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR)
    contact = Column(VARCHAR)
    street = Column(VARCHAR)
    postcode = Column(Integer)
    city = Column(VARCHAR)
    country = Column(VARCHAR)

    def get_all(self, arg):
        pass

    def get(self, arg):
        pass

    def update(self, arg):
        pass

    def edit(self, arg):
        pass

    def delete(self, arg):
        pass


# ===========
# AGENCYS
# ===========

class Agency(Base):
    """ DB Interaction class for Agencys """

    __tablename__ = 'agencys'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR)
    percentage = Column(DECIMAL)

    def get_all(self, arg):
        pass

    def get(self, arg):
        pass

    def update(self, arg):
        pass

    def edit(self, arg):
        pass

    def delete(self, arg):
        pass


# ===========
# JOBTYYPES
# ===========

class Jobtype(Base):
    """ DB Interaction class for Jobtypes """

    __tablename__ = 'jobtypes'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR)

    def get_all(self, arg):
        pass

    def get(self, arg):
        pass

    def update(self, arg):
        pass

    def edit(self, arg):
        pass

    def delete(self, arg):
        pass
