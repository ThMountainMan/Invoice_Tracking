# Helper to interact with the Database

import os
import yaml
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, VARCHAR, FLOAT
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declared_attr


def _ParseConfig():
    with open("../recources/db_config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
    return cfg


class Database:
    def __init__(self):
        # Parse the config File
        self._ParseConfig()
        # Create the connection engine
        self._engine = db.create_engine(
            self._CreateDbString(), echo=bool(int(self.config.get('debug'))))
        self._session = sessionmaker(bind=self._engine)
        self._Session = self._session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _ParseConfig(self):
        with open("../recources/db_config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
        self.config = cfg

    def _CreateDbString(self):
        # In case we have a local DB File
        if int(self.config.get('use_local')):
            cur_path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(cur_path, 'db')
            if not os.path.exists(path):
                os.makedirs(path)
            return f'sqlite:///{path}\\invoice_database.db'

        # In Case we want to connect to a remote SQL DB
        else:
            self.db_config = self.config["database"]
            self.user = self.db_config.get('user')
            self.pw = self.db_config.get('password')
            self.host = self.db_config.get('address')
            self.port = self.db_config.get('port')
            self.database = self.db_config.get('database')

            return f"mysql+pymysql://{self.user}:{self.pw}@{self.host}:{self.port}/{self.database}"

    @property
    def connection(self):
        self._conn = self._engine.connect()
        return self._conn

    @property
    def engine(self):
        return self._engine

    def ReturnSession(self):
        return self._Session

    def close(self, commit=True):
        self._session.close()

    def rollback(self):
        self._session.rollback()


# =========================================
# Configuration of the DB Connection Object
# =========================================

# Define the Base for the Database assignement
Base = declarative_base()
# Define a DB session
dbObject = Database()
session = dbObject.ReturnSession()

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
    def create(cls, obj):
        # Create a new Entry in the DB
        # check if the entry is already existant
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
    def get(cls, id=None, name=None):
        # Return a specific result
        if name:
            result = session.query(cls).filter(cls.name == name).first()
        elif id:
            result = session.query(cls).filter(cls.id == id).first()
        else:
            result = None
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
# VERSION
# ===========

class Version(Base):
    """ Version to store the version nr of the DB """
    # TODO: Implement a propper version control !!

    __tablename__ = "version"
    id = Column(Integer, primary_key=True)
    version = Column(Integer)

# ===========
# INVOICES
# ===========


class Invoices(BaseMixin, Base):
    """ DB Interaction class for Invoices """

    invoice_id = Column(VARCHAR)
    date = Column(Date)
    description = Column(VARCHAR)
    invoice_ammount = Column(FLOAT)
    invoice_mwst = Column(FLOAT)
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
    percentage = Column(FLOAT)


# ===========
# JOBTYYPES
# ===========

class Jobtypes(BaseMixin, Base):
    """ DB Interaction class for Jobtypes """

    name = Column(VARCHAR)


# Create the Database based on the definition available in the File
Base.metadata.create_all(dbObject.engine)
