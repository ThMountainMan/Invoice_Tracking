# Helper to interact with the Database

import logging
import os
from datetime import datetime

import sqlalchemy
from sqlalchemy import FLOAT, JSON, VARCHAR, Column, Date, ForeignKey, Integer, extract
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

from app_config import AppConfig
from db_migration import migration

# Init the Logger
log = logging.getLogger(__name__)


class Database:
    def __init__(self, config):
        # Create the connection engine
        self.config = config
        self._engine = sqlalchemy.create_engine(
            self._CreateDbString(), echo=self.config.debug
        )
        self._session = sessionmaker(
            bind=self._engine, autocommit=False, autoflush=False
        )
        # self._Session = self._session()
        self._scoped_session = scoped_session(self._session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _CreateDbString(self):
        # In case we have a local DB File
        if not self.config.local:
            return f"mysql+pymysql://{self.config.db_user}:{self.config.db_pw}@{self.config.db_host}:{self.config.db_port}/{self.config.db_name}?charset=utf8"

        path = self.config.db_path
        if not path:
            cur_path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(cur_path, "db")

        if not os.path.exists(path):
            os.makedirs(path)
        return f"sqlite:///{path}//{self.config.db_name}.db?charset=utf8"

    @property
    def connection(self):
        self._conn = self._engine.connect()
        return self._conn

    @property
    def engine(self):
        return self._engine

    def ReturnScopedSession(self):
        return self._scoped_session

    def ReturnSession(self):
        return self._Session

    def check_db_version(self):
        pass

    def migration(self):
        # Run the DB Migration if needed
        migration.run_migrations(
            script_location="./src/db_migration", dsn=self._CreateDbString()
        )

    def close(self, commit=True):
        self._session.close()

    def rollback(self):
        self._session.rollback()


# =========================================
# Configuration of the DB Connection Object
# =========================================

# Define a DB session
dbObject = Database(AppConfig)
# Define the Base for the Database assignement
Base = declarative_base(bind=dbObject.engine)
# Check if we need to migrate the DB
dbObject.migration()
# Create a session for the DB
db = dbObject.ReturnScopedSession()


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

    __table_args__ = {"mysql_engine": "InnoDB"}

    id = Column(Integer, primary_key=True)

    @classmethod
    def create(cls, obj):
        # Create a new Entry in the DB
        # check if the entry is already existant
        try:
            db.add(obj)
            db.commit()
            return obj.id
        except Exception as e:
            db.rollback()
            log.error(
                f"Not able to create object in '{cls.__tablename__(cls)}' with the Error:\n{e}"
            )
        return None

    @classmethod
    def delete(cls, id):
        # Delete Entry based on ID
        obj = db.query(cls).filter(cls.id == id).first()
        if cls.check_relation():
            return False

        db.delete(obj)
        db.commit()

    @classmethod
    def check_relation(cls):
        # Check if we have any relation with this class
        pass

    @classmethod
    def get(cls, id=None, name=None):
        # Return a specific result
        if name:
            return db.query(cls).filter(cls.name == name).first()
        elif id:
            return db.query(cls).filter(cls.id == id).first()
        else:
            return None

    @classmethod
    def get_all(cls):
        # Return all entrys in the DB
        return db.query(cls).all()

    @classmethod
    def count(cls):
        # Return the total count of all entrys
        return db.query(cls).count()

    @classmethod
    def check_link(cls):
        # TODO: Impement a method that checks if a foreign key is uesd in an
        # Invoice or not, so that we can delete an object safely
        pass

    @classmethod
    def update(cls, id, dUpdate):
        # Update a DB entry
        # REVIEW: Does this actually work as expected?
        obj = cls.get(id)
        try:
            for key, value in dUpdate.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)

            db.commit()
        except Exception:
            db.rollback()


# ===========
# Personal Details
# ===========


class PersonalDetails(BaseMixin, Base):
    """DB Interaction for personal Details"""

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
    """DB Interaction for payment Details"""

    label = Column(VARCHAR)

    name = Column(VARCHAR)
    bank = Column(VARCHAR)
    IBAN = Column(VARCHAR)
    BIC = Column(VARCHAR)


# ===========
# EXPENSES
# ===========


class Expenses(BaseMixin, Base):
    """DB Interaction class for Expenses"""

    expense_id = Column(VARCHAR)
    date = Column(Date)
    cost = Column(FLOAT)
    comment = Column(VARCHAR)

    @classmethod
    def get_latest_id(cls):
        obj = db.query(cls).order_by(cls.id.desc()).first()
        if not obj:
            return f"{datetime.now().year}-{1:03}"
        # Split the String
        year, id = obj.expense_id.split("-")

        # Check if the Year is still valid
        if int(year) != datetime.now().year:
            # We need to create an ID with a new year
            new_year = datetime.now().year
            # also we probably need to start to count from 1 again
            new_id = 1
        else:
            new_year = year
            # Increment the ID
            new_id = int(id) + 1

        return f"{new_year}-{new_id:03}"

    @classmethod
    def get_all(cls, year=None):
        if year:
            # Return DB entrys filterd by year
            return db.query(cls).filter(extract("year", cls.date) == int(year)).all()
        else:
            # Return all entrys in the DB
            return db.query(cls).all()


# ===========
# INVOICES
# ===========


class Invoices_Item(BaseMixin, Base):
    """DB Interaction class for Invoices Items"""

    description = Column(VARCHAR)
    count = Column(FLOAT)
    cost = Column(FLOAT)

    parent_id = Column(Integer, ForeignKey("invoices.id"))
    parent = relationship("Invoices", foreign_keys=[parent_id])


class Invoices(BaseMixin, Base):
    """DB Interaction class for Invoices"""

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

    items = relationship("Invoices_Item")
    customer = relationship("Customers", foreign_keys=[customer_id])
    jobtype = relationship("Jobtypes", foreign_keys=[jobcode_id])
    agency = relationship("Agencys", foreign_keys=[agency_id])
    personal = relationship("PersonalDetails", foreign_keys=[personal_id])

    @classmethod
    def get_latest_id(cls):
        obj = db.query(cls).order_by(cls.id.desc()).first()
        if not obj:
            return f"{datetime.now().year}-{1:03}"
        # Split the String
        year, id = obj.invoice_id.split("-")

        # Check if the Year is still valid
        if int(year) != datetime.now().year:
            # We need to create an ID with a new year
            new_year = datetime.now().year
            # also we probably need to start to count from 1 again
            new_id = 1
        else:
            new_year = year
            # Increment the ID
            new_id = int(id) + 1

        return f"{new_year}-{new_id:03}"

    @classmethod
    def get_latest_invoice_id(cls):
        obj = db.query(cls).order_by(cls.id.desc()).first()

    @classmethod
    def get_all(cls, year=None):
        if year:
            # Return DB entrys filterd by year
            return db.query(cls).filter(extract("year", cls.date) == int(year)).all()
        else:
            # Return all entrys in the DB
            return db.query(cls).all()

    def get_ammount(self):
        # ToDo: Generate function to return all incoive items
        _items = (
            db.query(Invoices_Item).filter(Invoices_Item.parent_id == self.id).all()
        )
        sum = 0
        mwst = 0
        sum_mwst = 0

        _dict = {"sum": sum, "mwst": mwst, "sum_mwst": sum_mwst}

        for i in _items:
            sum += i.cost * i.count

        if self.invoice_mwst:
            mwst = self.invoice_mwst / 100 * sum
            sum_mwst = sum + mwst
        else:
            sum_mwst = sum

        _dict["sum"] = float(round(sum, 2))
        _dict["mwst"] = float(round(mwst, 2))
        _dict["sum_mwst"] = float(round(sum_mwst, 2))

        return _dict

    def get_items(self):
        return db.query(Invoices_Item).filter(Invoices_Item.parent_id == self.id).all()


# ===========
# CUSTOMERS
# ===========


class Customers(BaseMixin, Base):
    """DB Interaction class for Customers"""

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
    """DB Interaction class for Agencys"""

    name = Column(VARCHAR)
    percentage = Column(FLOAT)


# ===========
# JOBTYYPES
# ===========


class Jobtypes(BaseMixin, Base):
    """DB Interaction class for Jobtypes"""

    name = Column(VARCHAR)


# Create the Database based on the definition available in the File
# Base.metadata.create_all(dbObject.engine)
