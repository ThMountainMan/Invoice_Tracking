# Helper to interact with the Database

import yaml
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, VARCHAR, DECIMAL
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declared_attr


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

# ===============================
# Basic Function definition
# ===============================


class BaseMixin(object):
    """
    Some general Functionality for reusing
    This Class and Functions are inherited in all other classes,
    so it is easier just to define one "Base Class" with all needed
    functionality
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(Integer, primary_key=True)

    @classmethod
    def create(cls, **kw):
        # Create a new Entry in the DB
        obj = cls(**kw)
        session.add(obj)
        session.commit()
        return obj.id

    @classmethod
    def delete(cls, id):
        # Delete Entry based on ID
        obj = session.query(cls).filter(cls.id == id).first()
        session.delete(obj)
        session.commit()

    @classmethod
    def get(cls, id):
        # Return a specific result
        result = session.query(cls).filter(cls.id == id).first()
        # TODO: Enable more Filters for this querry !!!!
        return result

    @classmethod
    def get_all(cls):
        # Return all entrys in the DB
        return session.query(cls).all()

    @classmethod
    def count(cls):
        # Return the total count of all entrys
        return session.query(cls).count()

    @classmethod
    def update(cls, id, **kw):
        # Update a DB entry
        # REVIEW: Does this actually work as expected?
        obj = cls.get(id)
        obj.update(**kw)
        session.commit()


# ===========
# INVOICES
# ===========


class Invoices(BaseMixin, Base):
    """ DB Interaction class for Invoices """

    invoice_id = Column(VARCHAR)
    date = Column(Date)
    description = Column(VARCHAR)
    invoice_ammount = Column(DECIMAL)
    invoice_mwst = Column(DECIMAL)
    paydate = Column(Date)

    customer_id = Column(Integer, ForeignKey("customers.id"))
    jobcode_id = Column(Integer, ForeignKey("jobtypes.id"))
    agency_id = Column(Integer, ForeignKey("agencys.id"))

    customer = relationship("Customers", foreign_keys=[customer_id])
    jobtype = relationship("Jobtypes", foreign_keys=[jobcode_id])
    agency = relationship("Agencys", foreign_keys=[agency_id])


# ===========
# CUSTOMERS
# ===========

class Customers(BaseMixin, Base):
    """ DB Interaction class for Customers """

    name = Column(VARCHAR)
    contact = Column(VARCHAR)
    street = Column(VARCHAR)
    postcode = Column(Integer)
    city = Column(VARCHAR)
    country = Column(VARCHAR)


# ===========
# AGENCYS
# ===========

class Agencys(BaseMixin, Base):
    """ DB Interaction class for Agencys """

    name = Column(VARCHAR)
    percentage = Column(DECIMAL)


# ===========
# JOBTYYPES
# ===========

class Jobtypes(BaseMixin, Base):
    """ DB Interaction class for Jobtypes """

    name = Column(VARCHAR)
