# Helper to interact with the Database

import yaml
from mysql.connector import connect, Error


def _ParseConfig():
    with open("../recources/db_config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
    return cfg["database"]


class Database:
    def __init__(self):
        self._ParseConfig()
        self._conn = connect(host=self.config.get('address'),
                             user=self.config.get('user'),
                             password=self.config.get('password'),
                             database=self.config.get('database'),
                             port=self.config.get('port'))
        self._cursor = self._conn.cursor(dictionary=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _ParseConfig(self):
        with open("../recources/db_config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
        self.config = cfg["database"]

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

    def rollback(self):
        self.connection.rollback()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    # ----------------------------------------------------------------
    # Methods to retrieve Information from the Database
    # ----------------------------------------------------------------

    def get_invoices(self, filter=None):
        """ Get all available invoices - filter is optional """
        if filter:
            sql = f'SELECT * FROM invoices WHERE id = {filter}'
        else:
            sql = 'SELECT * FROM invoices'

        return self.query(sql, params=None)

    def get_customers(self, filter=None):
        """ Get all available customers - filter is optional """
        if filter:
            sql = f'SELECT * FROM customers WHERE id = {filter}'
        else:
            sql = 'SELECT * FROM customers'

        return self.query(sql, params=None)

    def get_agencys(self, filter=None):
        """ Get all available agencys - filter is optional """
        if filter:
            sql = f'SELECT * FROM agencys WHERE id = {filter}'
        else:
            sql = 'SELECT * FROM agencys'

        return self.query(sql, params=None)

    # ----------------------------------------------------------------
    # Methods to create Information in the Database
    # ----------------------------------------------------------------

    def create_invoice(self, arg):
        """ Create a new invoice in the database """
        sql = f"""
        INSERT INTO
            invoices (date, description, invoice_ammount, invoice_mwst, paydate, customer_id, jobcode_id, agency_id)
        VALUES
            ('{arg['date']}', '{arg['description']}', {arg['invoice_ammount']}, {arg['invoice_mwst']}, '{arg['paydate']}', {arg['customer_id']}, {arg['jobcode_id']}, {arg['agency_id']})
        """
        self.execute(sql, params=None)
        return self.cursor.lastrowid

    def create_customer(self, arg):
        """ Create a new customer in the database """
        sql = f"""
        INSERT INTO
            customers (name, contact, street, postcode, city, country)
        VALUES
            ('{arg['name']}','{arg['contact']}','{arg['street']}',{arg['postcode']},'{arg['city']}','{arg['country']}')
        """
        self.execute(sql, params=None)
        return self.cursor.lastrowid

    def create_agency(self, arg):
        """ Create a new agency in the database """
        sql = f"""
        INSERT INTO
            agencys (name, percentage)
        VALUES
            ('{arg['name']}',{arg['percentage']})
        """
        self.execute(sql, params=None)
        return self.cursor.lastrowid

    def create_jobtype(self, arg):
        """ Create a new Jobtype in the database """
        sql = f"""
        INSERT INTO
            jobtypes (name)
        VALUES
            ('{arg['name']}')
        """
        self.execute(sql, params=None)
        return self.cursor.lastrowid

    # ----------------------------------------------------------------
    # Methods to edit Information in the Database
    # ----------------------------------------------------------------

    def edit_invoice(self, arg, id):
        """ Edit an invoice in the database """
        update_query = f"""
        UPDATE
            invoices
        SET
            date = {arg['date']}
            description = '{arg['description']}'
            invoice_ammount = {arg['invoice_ammount']}
            invoice_mwst = {arg['invoice_mwst']}
            paydate = {arg['paydate']}
            customer_id = {arg['customer_id']}
            jobcode_id = {arg['jobcode_id']}
            agency_id = {arg['agency_id']}

        WHERE
            id = {id}
        """
        self.execute(update_query, params=None)
        return id

    def edit_customer(self, arg, id):
        """ Edit a customer in the database """
        update_query = f"""
        UPDATE
            customers
        SET
            name = '{arg['name']}',
            contact = '{arg['contact']}',
            street = '{arg['street']}',
            postcode = {arg['postcode']},
            city = '{arg['city']}',
            country = '{arg['country']}'
        WHERE
            id = {id}
        """
        self.execute(update_query, params=None)
        return id

    def edit_agency(self, arg, id):
        """ Create a agency in the database """
        update_query = f"""
        UPDATE
            agencys
        SET
            name = '{arg['name']}'
            percentage = {arg['percentage']}
        WHERE
            id = {id}
        """
        self.execute(update_query, params=None)
        return id

    def edit_jobtype(self, arg, id):
        """ Create a agency in the database """
        update_query = f"""
        UPDATE
            jobtypes
        SET
            name = '{arg['name']}'
        WHERE
            id = {id}
        """
        self.execute(update_query, params=None)
        return id


# =========================================
# Function Definition for DB Interaction
# =========================================

# ===========
# INVOICES
# ===========
def get_invoice(filter=None):
    with Database() as db:
        try:
            request = db.get_invoices(filter=filter)
            print(f'Requested INVOICES')
            print(request)
            return request
        except Exception as e:
            # If we encounter some problem, rollback the last changes
            print(e)


def create_invoice(data):
    with Database() as db:
        try:
            newID = db.create_invoice(data)
            print(f'Created new INVOICE with ID : {newID}')
            print(db.query(f"SELECT * FROM invoices where id= '{newID}'"))
            return newID
        except Exception as e:
            # If we encounter some problem, rollback the last changes
            print(e)
            db.rollback()


def edit_invoice(data, id):
    with Database() as db:
        try:
            db.edit_invoice(data, id)
            print(f'Edited INVOICE with ID : {id}')
            print(db.query(f"SELECT * FROM invoices where id= '{id}'"))
            return id
        except Exception as e:
            # If we encounter some problem, rollback the last changes
            print(e)
            db.rollback()


# ===========
# CUSTOMERS
# ===========

def get_customer(filter=None):
    with Database() as db:
        try:
            request = db.get_customers(filter=filter)
            print(f'Requested CUSTOMERS')
            print(request)
            return request
        except Exception as e:
            # If we encounter some problem, rollback the last changes
            print(e)


def create_customer(data):
    with Database() as db:
        try:
            newID = db.create_customer(data)
            print(f'Created new CUSTOMER with ID : {newID}')
            print(db.query(f"SELECT * FROM customers where id= '{newID}'"))
            return newID
        except Exception as e:
            # If we encounter some problem, rollback the last changes
            print(e)
            db.rollback()


def edit_customer(data, id):
    with Database() as db:
        try:
            db.edit_customer(data, id)
            print(f'Edited CUSTOMER with ID : {id}')
            print(db.query(f"SELECT * FROM invoices where id= '{id}'"))
            return id
        except Exception as e:
            # If we encounter some problem, rollback the last changes
            print(e)
            db.rollback()


# ===========
# AGENCYS
# ===========
def get_agency(filter=None):
    with Database() as db:
        try:
            request = db.get_agencys(filter=filter)
            print(f'Requested AGENCYS')
            print(request)
            return request
        except Exception as e:
            # If we encounter some problem, rollback the last changes
            print(e)


def create_agency(data):
    with Database() as db:
        try:
            newID = db.create_agency(data)
            print(f'Created new AGENCY with ID : {newID}')
            print(db.query(f"SELECT * FROM agencys where id= '{newID}'"))
            return newID
        except Exception as e:
            # If we encounter some problem, rollback the last changes
            print(e)
            db.rollback()


def edit_agency(data, id):
    with Database() as db:
        try:
            db.edit_agency(data, id)
            print(f'Edited AGENCY with ID : {id}')
            print(db.query(f"SELECT * FROM invoices where id= '{id}'"))
            return id
        except Exception as e:
            # If we encounter some problem, rollback the last changes
            print(e)
            db.rollback()


# ===========
# JOBTYYPES
# ===========
def get_jobtype(filter=None):
    with Database() as db:
        try:
            request = db.get_jobtypes(filter=filter)
            print(f'Requested JOBTYPE')
            print(request)
            return request
        except Exception as e:
            # If we encounter some problem, rollback the last changes
            print(e)


def create_jobtype(data):
    with Database() as db:
        try:
            newID = db.create_jobtype(data)
            print(f'Created new JOBTYPE with ID : {newID}')
            print(db.query(f"SELECT * FROM jobtypes where id= '{newID}'"))
            return newID
        except Exception as e:
            # If we encounter some problem, rollback the last changes
            print(e)
            db.rollback()


def edit_jobtype(data, id):
    with Database() as db:
        try:
            db.edit_jobtype(data, id)
            print(f'Edited JOBTYPE with ID : {id}')
            print(db.query(f"SELECT * FROM jobtypes where id= '{id}'"))
            return id
        except Exception as e:
            # If we encounter some problem, rollback the last changes
            print(e)
            db.rollback()
