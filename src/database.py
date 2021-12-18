# Helper to interact with the Database

import logging
import os
from datetime import datetime

import sqlalchemy
from sqlalchemy import FLOAT, JSON, VARCHAR, Column, Date, ForeignKey, Integer, extract
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from contextlib import contextmanager

from app_config import AppConfig
from db_migration import migration

# Init the Logger
log = logging.getLogger(__name__)

Base = declarative_base()
Session = sessionmaker()


class NotExists(Exception):
    """Is raised if a database instance could not be found"""


class RegisteredModels(dict):
    def register(self, writeable=True, admin_only=False):
        def _register(cls):
            self[cls.__tablename__] = cls
            cls._writeable = writeable
            cls._admin_only = admin_only
            return cls

        return _register

    def get_model(self, model_or_name):
        if isinstance(model_or_name, str):
            try:
                return self[model_or_name]
            except KeyError:
                raise NotExists(f"No database model with name {model_or_name} found!")
        return model_or_name


models = RegisteredModels()


class DbConnection:
    def __init__(self):
        self.session = Session()
        self.created_at = datetime.datetime.now()
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
        log.debug("begin new transaction")
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
        log.debug("commit changes to database")
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

    def get(self, model, id_):
        """
        READ

        Get a single model instance by its primary_key.
        The given id_ can be a single value like and int or a tuple
        of the values which represent the primary key.
        """
        model = self.get_model(model)
        instance = self.session.query(model).get(id_)
        if instance is None:
            raise NotExists(f"{model.__tablename__} with id={id_} does not exist!")
        return instance

    def update(self, model, id_, attributes, do_commit=None):
        """
        UPDATE

        attributes is a dictionary with table column names and values.
        """
        instance = self.get(model, id_)
        attributes = self._convert_db_file_objects(attributes)
        for name, value in attributes.items():
            setattr(instance, name, value)
        self.merge(instance, do_commit=do_commit)
        return instance

    def delete(self, model, id_, do_commit=None):
        """
        DELETE

        Returns True if the db instance with the given ID was deleted.
        False if it could not be found.
        """
        try:
            instance = self.get(model, id_)
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

    def __del__(self):
        """
        Workaround for bug ticket #80022 - Queue Pool Error
        Returning the session back to the pool when garbage collected.

        """
        try:
            self.session.close()
        except:
            pass

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


@models.register(writeable=False)
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


@models.register(writeable=True)
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


@models.register(writeable=True)
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


@models.register(writeable=True)
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


@models.register(writeable=True)
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


@models.register(writeable=True)
class Agencys(BaseMixin, Base):
    """DB Interaction class for Agencys"""

    name = Column(VARCHAR)
    percentage = Column(FLOAT)


# ===========
# JOBTYYPES
# ===========


@models.register(writeable=True)
class Jobtypes(BaseMixin, Base):
    """DB Interaction class for Jobtypes"""

    name = Column(VARCHAR)


# Create the Database based on the definition available in the File
# Base.metadata.create_all(dbObject.engine)
