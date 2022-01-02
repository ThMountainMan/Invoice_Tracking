# Helper to interact with the Database

import logging
import os
from contextlib import contextmanager
from datetime import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import (
    FLOAT,
    JSON,
    VARCHAR,
    Column,
    Date,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    UniqueConstraint,
    create_engine,
    desc,
    event,
    extract,
)
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.attributes import QueryableAttribute
from sqlalchemy.sql.sqltypes import String

# from app_config import AppConfig
from config import appconfig
from db_migration import migration

# TODO: This can be deleted once the integration is finished
AppConfig = appconfig

# Init the Logger
log = logging.getLogger(__name__)

Base = declarative_base()
Session = sessionmaker()


def init(config=appconfig, create=False):

    if appconfig.debug:
        log.info("enable sql echo logging (debug)")
    url = f"sqlite:///{config.db_path}/{config.db_name}.db"

    # Run the DB Migration if needed
    migration.run_migrations(script_location=appconfig.db_migration, dsn=url)

    # This needs to be added in order to have constraint check
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    engine = create_engine(url, echo=config.echo)
    log.info("connect to database %s", engine.url)
    if create:
        log.info("create database based on the modelling")
        Base.metadata.create_all(engine)
    Session.configure(bind=engine)


class NotExists(Exception):
    """Failure Class for catching errors"""


class AvailableDBModels(dict):
    def register(self, editable=True, admin_rights=False):
        def _register(cls):
            self[cls.__tablename__] = cls
            cls._editable = editable
            cls._admin_rights = admin_rights
            return cls

        return _register

    def get_model(self, model):
        if isinstance(model, str):
            try:
                return self[model]
            except KeyError:
                raise NotExists(
                    f"Not able to find corrosponding model for :  {model} !"
                )
        return model


models = AvailableDBModels()


class DbConnection:
    def __init__(self):
        self.session = Session()
        self.created_at = datetime.now()
        self._within_transaction = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value:
            self.session.rollback()
        self.session.close()

    @contextmanager
    def transaction(self, do_commit=True, do_close=True):
        """Enter the with block"""
        assert (
            self._within_transaction is False
        ), "Attempt to start a transaction multiple times!"
        self.begin()
        try:
            yield self
        except:
            self.rollback()
            raise
        else:
            if do_commit:
                self.commit()
        finally:
            self._within_transaction = False
            if do_close:
                self.close()
        return self

    def begin(self):
        log.debug("start a new transaction")
        self._within_transaction = True
        # self.session.begin_nested()  # establish a savepoint

    def _default_commit(self, do_commit):
        if do_commit is None:
            do_commit = False if self._within_transaction else True
        return do_commit

    def get_model(self, model_or_name):
        return models.get_model(model_or_name)

    def execute(self, clause, params=None, do_commit=None, **kwargs):
        rv = self.session.execute(clause, params=params, **kwargs)
        if self._default_commit(do_commit):
            self.commit()
        return rv

    def commit(self):
        """Store pending changes to the datbase"""
        log.debug("committing changes to database")
        self._within_transaction = False
        self.session.commit()

    def rollback(self):
        """Store pending changes to the datbase"""
        log.debug("rollback pending database changes")
        self._within_transaction = False
        self.session.rollback()

    def close(self):
        log.debug("close database session")
        assert (
            self._within_transaction is False
        ), "About to close a transaction whithout rollback() or commit()"
        self.session.close()

    def create(self, model, attributes, do_commit=None):
        """
        CREATE
        attributes is a dictionary with model column names and values.
        """
        # Create an instance of the class pathing in all the given attributes
        if isinstance(model, str):
            model = self.get_model(model)
        # attributes = self._convert_db_file_objects(attributes)
        new = model(**attributes)
        self.add(new, do_commit=do_commit)
        return new

    def add(self, new, do_commit=None):
        """
        Store a model instance in the database.
        """
        self.session.add(new)
        self.session.flush()
        self.session.refresh(new)
        if self._default_commit(do_commit):
            self.commit()
        return new

    def merge(self, instance, do_commit=None):
        """
        Sync changes made to an instance back into the database.
        """
        self.session.merge(instance)
        self.session.flush()
        if self._default_commit(do_commit):
            self.commit()
        return instance

    def detatch(self, instance):
        self.session.expunge(instance)

    def get(self, model, id):
        """
        READ DB entry
        """
        model = self.get_model(model)
        instance = self.session.query(model).get(id)
        if instance is None:
            raise NotExists(f"{model.__tablename__} with id={id} does not exist!")
        return instance

    def update(self, model, id, attributes, do_commit=None):
        """
        UPDATE

        attributes is a dictionary with table column names and values.
        """
        instance = self.get(model, id)
        attributes = self._convert_db_file_objects(attributes)
        for name, value in attributes.items():
            setattr(instance, name, value)
        self.merge(instance, do_commit=do_commit)
        return instance

    def delete(self, model, id, do_commit=None):
        """
        DELETE

        Returns True if the db instance with the given ID was deleted.
        False if it could not be found.
        """
        try:
            instance = self.get(model, id)
        except NotExists:
            return False
        self.session.delete(instance)
        if self._default_commit(do_commit):
            self.commit()
        return True

    def query(
        self, model, filters=None, offset=None, limit=None, order_by=None, reverse=False
    ):
        filters = filters or {}
        model = self.get_model(model)
        q = self.session.query(model)
        for attr, value in filters.items():
            if attr == "__filter__":
                # The user provides and own filter statement
                q = q.filter(value)
            elif isinstance(value, (list, tuple)):
                q = q.filter(getattr(model, attr).in_(value))
            else:
                q = q.filter(getattr(model, attr) == value)
        if order_by:
            if isinstance(order_by, (str, QueryableAttribute)):
                order_by = [order_by]
            for stmt in order_by:
                if isinstance(stmt, str):
                    stmt = self._get_attribute(stmt, model)
                if reverse:
                    stmt = desc(stmt)
                q = q.order_by(stmt)
        if offset:
            q = q.offset(offset)
        if limit:
            q = q.limit(limit)
        return q.all()

    def query_one(self, model, filters):
        found = self.query(model, filters, limit=1)
        if found:
            return found[0]
        return None

    def _get_attribute(self, text, model):
        """Expecting string with "model.attrib". Searching the model by it's name and returning it's attribute"""
        if "." in text:
            name, text = text.split(".")
            model = self.get_model(name.strip("'\""))
        return getattr(model, text)

    def _convert_db_file_objects(self, attributes):
        conn = None
        _attributes = {}
        for attr, value in attributes.items():
            if hasattr(value, "save"):
                if conn is None:
                    conn = self.session.connection()
                lobject = conn.connection.lobject(0, "rw", 0)
                value.save(lobject)
                self.session.commit()
                value = lobject.oid
            _attributes[attr] = value
        return _attributes


@models.register(editable=False)
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

    id = Column(Integer, primary_key=True)

    # General User ID to seperate different User Content
    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey("user.id"), nullable=False)


# ===========
# VERSION
# ===========


@models.register(editable=True)
class Version(Base):
    """Version to store the version nr of the DB"""

    # TODO: Implement a propper version control !!

    __tablename__ = "version"
    id = Column(Integer, primary_key=True)
    version = Column(Integer)


# ===========
# USER
# ===========


@models.register(editable=True)
class User(UserMixin, Base):
    """User Related Data"""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)

    name = Column(VARCHAR)
    email = Column(VARCHAR, unique=True)
    password = Column(VARCHAR)
    user_role = Column(VARCHAR)


# ===========
# Personal Details
# ===========


@models.register(editable=True)
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

    payment_id = Column(Integer, ForeignKey("paymentdetails.id", ondelete="RESTRICT"))
    payment_details = relationship(
        "PaymentDetails", foreign_keys=[payment_id], lazy=False
    )

    user_id = Column(Integer, ForeignKey("user.id"))

    ForeignKeyConstraint(
        ["payment_id"], ["paymentdetails.id"], name="fk_personal_payment_id"
    )


@models.register(editable=True)
class PaymentDetails(BaseMixin, Base):
    """DB Interaction for payment Details"""

    label = Column(VARCHAR)

    name = Column(VARCHAR)
    bank = Column(VARCHAR)
    IBAN = Column(VARCHAR)
    BIC = Column(VARCHAR)

    user_id = Column(Integer, ForeignKey("user.id"))

    def __str__(self):
        return str(self.label)


# ===========
# EXPENSES
# ===========


@models.register(editable=True)
class Expenses(BaseMixin, Base):
    """DB Interaction class for Expenses"""

    expense_id = Column(VARCHAR, unique=True)
    date = Column(Date)
    cost = Column(FLOAT)
    comment = Column(VARCHAR)

    user_id = Column(Integer, ForeignKey("user.id"))

    # explicit/composite unique constraint.  'name' is optional.
    UniqueConstraint(expense_id, name="uc_expenses_id")

    @classmethod
    def generate_id(cls):
        session = Session()
        obj = session.query(cls).order_by(cls.id.desc()).first()
        if not obj:
            return f"{datetime.datetime.now().year}-{1:03}"
        year, id = obj.expense_id.split("-")
        if int(year) != datetime.now().year:
            new_year = datetime.now().year
            new_id = 1
        else:
            new_year = year
            new_id = int(id) + 1

        return f"{new_year}-{new_id:03}"


# ===========
# INVOICES
# ===========


@models.register(editable=True)
class Invoices_Item(BaseMixin, Base):
    """DB Interaction class for Invoices Items"""

    description = Column(VARCHAR)
    count = Column(FLOAT)
    cost = Column(FLOAT)

    parent_id = Column(Integer, ForeignKey("invoices.id"))
    parent = relationship("Invoices", foreign_keys=[parent_id])


@models.register(editable=True)
class Invoices(BaseMixin, Base):
    """DB Interaction class for Invoices"""

    invoice_id = Column(VARCHAR, unique=True)
    date = Column(Date)
    description = Column(VARCHAR)
    invoice_ammount = Column(FLOAT)
    invoice_mwst = Column(FLOAT)
    paydate = Column(Date)
    invoice_data = Column(JSON)

    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="RESTRICT"))
    jobcode_id = Column(Integer, ForeignKey("jobtypes.id", ondelete="RESTRICT"))
    agency_id = Column(Integer, ForeignKey("agencys.id", ondelete="RESTRICT"))
    personal_id = Column(Integer, ForeignKey("personaldetails.id", ondelete="RESTRICT"))

    user_id = Column(Integer, ForeignKey("user.id"))

    items = relationship("Invoices_Item", lazy=False)
    customer = relationship("Customers", foreign_keys=[customer_id], lazy=False)
    jobtype = relationship("Jobtypes", foreign_keys=[jobcode_id], lazy=False)
    agency = relationship("Agencys", foreign_keys=[agency_id], lazy=False)
    personal = relationship("PersonalDetails", foreign_keys=[personal_id], lazy=False)

    ForeignKeyConstraint(
        ["customer_id"], ["customers.id"], name="fk_invoice_customer_id"
    )
    ForeignKeyConstraint(["jobcode_id"], ["jobtypes.id"], name="fk_invoice_jobcode_id")
    ForeignKeyConstraint(["agency_id"], ["agencys.id"], name="fk_invoice_agency_id")

    ForeignKeyConstraint(
        ["personal_id"], ["personaldetails.id"], name="fk_invoice_personal_id"
    )

    # explicit/composite unique constraint.  'name' is optional.
    UniqueConstraint(invoice_id, name="uc_invoices_id")

    @classmethod
    def generate_id(cls):
        session = Session()
        obj = session.query(cls).order_by(cls.id.desc()).first()
        if not obj:
            return f"{datetime.datetime.now().year}-{1:03}"
        year, id = obj.invoice_id.split("-")
        if int(year) != datetime.now().year:
            new_year = datetime.now().year
            new_id = 1
        else:
            new_year = year
            new_id = int(id) + 1

        return f"{new_year}-{new_id:03}"

    @classmethod
    def get_latest_invoice_id(cls):
        session = Session()
        obj = session.query(cls).order_by(cls.id.desc()).first()
        return obj.id

    def get_sum(self):
        sum = 0
        for item in self.items:
            sum += item.cost * item.count
        return float(round(sum, 2))

    def get_total(self):
        sum = self.get_sum()
        sum_mwst = self.get_sum_mwst()
        return sum + sum_mwst

    def get_mwst(self):
        return float(round(self.invoice_mwst, 2))

    def get_sum_mwst(self):
        sum = self.get_sum()
        mwst = 0
        if self.invoice_mwst:
            mwst = self.invoice_mwst / 100 * sum
        return float(round(mwst, 2))


# ===========
# CUSTOMERS
# ===========


@models.register(editable=True)
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

    user_id = Column(Integer, ForeignKey("user.id"))


# ===========
# AGENCYS
# ===========


@models.register(editable=True)
class Agencys(BaseMixin, Base):
    """DB Interaction class for Agencys"""

    name = Column(VARCHAR)
    percentage = Column(FLOAT)


# ===========
# JOBTYYPES
# ===========


@models.register(editable=True)
class Jobtypes(BaseMixin, Base):
    """DB Interaction class for Jobtypes"""

    name = Column(VARCHAR)


# Create the Database based on the definition available in the File
# Base.metadata.create_all(dbObject.engine)
