# Scrit to set up and configure the Database
from mysql.connector import connect, Error


def DB_Update():
    pass


def DB_Validation(config):
    Proceed = False
    try:
        with connect(host=config.get('address'),
                     user=config.get('user'),
                     password=config.get('password'),
                     port=config.get('port')) as connection:

            with connection.cursor() as cursor:
                # Display all available Databases on MySQL Server
                # Check if the needed DB is already available
                show_db_query = "SHOW DATABASES"

                cursor.execute(show_db_query)
                for db in cursor:
                    if config.get('database') in db[0]:
                        Proceed = True
                        break

    except Error as e:
        print(e)
    finally:
        return Proceed


def DB_CreateDB(config):
    Proceed = False
    try:
        with connect(host=config.get('address'),
                     user=config.get('user'),
                     password=config.get('password'),
                     port=config.get('port')) as connection:

            with connection.cursor() as cursor:
                # Display all available Databases on MySQL Server
                # Check if the needed DB is already available
                print(f"Create new Database : {config.get('database')}")
                create_db_query = f"CREATE DATABASE {config.get('database')}"
                cursor.execute(create_db_query)

        Proceed = True

    except Error as e:
        print(e)
    finally:
        return Proceed


def DB_CreateTables(config):
    Proceed = False
    try:
        with connect(host=config.get('address'),
             user=config.get('user'),
             password=config.get('password'),
             port=config.get('port'),
             database=config.get('database')) as connection:

            with connection.cursor() as cursor:
                # We need to create the Database for the Invoice Tool
                print(f"Create new Tables in {config.get('database')}:")

                create_customer_table_query = """
                CREATE TABLE customers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    contact VARCHAR(100),
                    street VARCHAR(100),
                    postcode VARCHAR(100),
                    city VARCHAR(100),
                    country VARCHAR(100)
                )
                """

                print(" - Create CUSTOMERS table ...")
                cursor.execute(create_customer_table_query)

                # ===================================================

                create_agency_table_query = """
                CREATE TABLE agencys (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    percentage DECIMAL(3,1)
                )
                """

                print(" - Create AGENCYS table ...")
                cursor.execute(create_agency_table_query)

                # ===================================================

                create_jobtype_table_query = """
                CREATE TABLE jobtypes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100)
                )
                """

                print(" - Create JOBTYPES table ...")
                cursor.execute(create_jobtype_table_query)

                # ===================================================

                create_invoice_table_query = """
                CREATE TABLE invoices (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    invoice_id VARCHAR(8)
                    date DATE,
                    description LONGTEXT,
                    invoice_ammount DECIMAL(8,2),
                    invoice_mwst INT,
                    paydate DATE,

                    customer_id INT,
                    jobcode_id INT,
                    agency_id INT,

                    FOREIGN KEY(customer_id) REFERENCES customers(id),
                    FOREIGN KEY(jobcode_id) REFERENCES jobtypes(id),
                    FOREIGN KEY(agency_id) REFERENCES agencys(id)
                )
                """

                print(" - Create INVOICES table ...")
                cursor.execute(create_invoice_table_query)

        Proceed = True

    except Error as e:
        print(e)
    finally:
        return Proceed
