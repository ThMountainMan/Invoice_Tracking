# Helper to interact with the Database

import os

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, VARCHAR, FLOAT, JSON
from sqlalchemy import ForeignKey, extract
from sqlalchemy.ext.declarative import declared_attr

from app_config import AppConfig

import logging

# Init the Logger
log = logging.getLogger(__name__)


class Database:
    def __init__(self, config):
        # Create the connection engine
        self.config = config
        self._engine = db.create_engine(
            self._CreateDbString(), echo=self.config.debug)
        self._session = sessionmaker(bind=self._engine)
        self._Session = self._session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _CreateDbString(self):
        # In case we have a local DB File
        if int(self.config.local):
            cur_path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(cur_path, 'db')
            if not os.path.exists(path):
                os.makedirs(path)
            return f'sqlite:///{path}\\invoice_database.db'

        # In Case we want to connect to a remote SQL DB
        else:
            return f"mysql+pymysql://{self.config.db_user}:{self.config.db_pw}@{self.config.db_host}:{self.config.db_port}/{self.config.db_name}"

    @ property
    def connection(self):
        self._conn = self._engine.connect()
        return self._conn

    @ property
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
dbObject = Database(AppConfig)
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

    @ declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(Integer, primary_key=True)

    @ classmethod
    def create(cls, obj):
        # Create a new Entry in the DB
        # check if the entry is already existant
        try:
            session.add(obj)
            session.commit()
            return obj.id
        except Exception as e:
            session.rollback()
            log.error(f"Not able to creare object in '{__tablename__}' with the Error:\n{e}")
        return None

    @ classmethod
    def delete(cls, id):
        # Delete Entry based on ID
        obj = session.query(cls).filter(cls.id == id).first()
        session.delete(obj)
        session.commit()

    @ classmethod
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

    @ classmethod
    def get_all(cls):
        # Return all entrys in the DB
        return session.query(cls).all()

    @ classmethod
    def count(cls):
        # Return the total count of all entrys
        return session.query(cls).count()

    @ classmethod
    def check_link(cls):
        # TODO: Impement a method that checks if a foreign key is uesd in an
        # Invoice or not, so that we can delete an object safely
        pass

    @ classmethod
    def update(cls, id, dUpdate):
        # Update a DB entry
        # REVIEW: Does this actually work as expected?
        obj = cls.get(id)
        try:
            for key, value in dUpdate.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)

            session.commit()
        except Exception:
            session.rollback()


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
# Personal Details
# ===========


class PersonalDetails(BaseMixin, Base):
    """ DB Interaction for personal Details """

    label = Column(VARCHAR)

    name_company = Column(VARCHAR)
    name = Column(VARCHAR)

    street = Column(VARCHAR)
    postcode = Column(Integer)
    city = Column(VARCHAR)

    mail = Column(VARCHAR)
    phone = Column(VARCHAR)

    taxnumber = Column(VARCHAR)

    payment_id = Column(Integer, ForeignKey("paymentdetails.id"))
    payment_details = relationship("PaymentDetails", foreign_keys=[payment_id])


class PaymentDetails(BaseMixin, Base):
    """ DB Interaction for payment Details """

    label = Column(VARCHAR)

    name = Column(VARCHAR)
    bank = Column(VARCHAR)
    IBAN = Column(VARCHAR)
    BIC = Column(VARCHAR)


# ===========
# EXPENSES
# ===========

class Expenses(BaseMixin, Base):
    """ DB Interaction class for Expenses """

    expense_id = Column(VARCHAR)
    date = Column(Date)
    cost = Column(FLOAT)
    comment = Column(VARCHAR)

    @ classmethod
    def get_latest_id(cls):
        obj = session.query(cls).order_by(cls.id.desc()).first()
        if not obj:
            return 1
        return obj.id + 1

    @ classmethod
    def get_all(cls, year=None):
        if year:
            # Return DB entrys filterd by year
            return session.query(cls).filter(extract('year', cls.date) == int(year)).all()
        else:
            # Return all entrys in the DB
            return session.query(cls).all()
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
    invoice_data = Column(JSON)

    customer_id = Column(Integer, ForeignKey("customers.id"))
    jobcode_id = Column(Integer, ForeignKey("jobtypes.id"))
    agency_id = Column(Integer, ForeignKey("agencys.id"))
    personal_id = Column(Integer, ForeignKey("personaldetails.id"))

    customer = relationship("Customers", foreign_keys=[customer_id])
    jobtype = relationship("Jobtypes", foreign_keys=[jobcode_id])
    agency = relationship("Agencys", foreign_keys=[agency_id])
    personal = relationship("PersonalDetails", foreign_keys=[personal_id])

    @ classmethod
    def get_latest_id(cls):
        obj = session.query(cls).order_by(cls.id.desc()).first()
        if not obj:
            return 1
        return obj.id + 1

    @ classmethod
    def get_all(cls, year=None):
        if year:
            # Return DB entrys filterd by year
            return session.query(cls).filter(extract('year', cls.date) == int(year)).all()
        else:
            # Return all entrys in the DB
            return session.query(cls).all()
    # ===========
# CUSTOMERS
# ===========


class Customers(BaseMixin, Base):
    """ DB Interaction class for Customers """

    name = Column(VARCHAR)
    email = Column(VARCHAR)
    phone = Column(VARCHAR)
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
