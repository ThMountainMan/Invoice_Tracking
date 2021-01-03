# This Script shall provide the basis for a Invoice Generator / Tracker Tool
# Things will probably be quite messy at the beginning and change a lot during
# the process !!!!

import sys
from datetime import datetime

#from HelperClasses import Costumer, Agency, Invoce, Jobtype
from check_db import DB_Validation, DB_CreateDB, DB_CreateTables
import database as DB
from database import session as DB_Session
from website import start


def CreateDBEntry():
    # Validate the DB Connection
    config = DB._ParseConfig()
    db_config = config['database']

    if not DB_Validation(db_config):
        print("No Valid DB found ... Creating the necessarry recources ...")
        # The DB is not available and we need to create it
        Check = DB_CreateDB(db_config)
        Check = DB_CreateTables(db_config)

    # DB Validation sucess and we can procees as normal
    print(f"Valid Database found : {db_config.get('address')} / {db_config.get('database')}")


if __name__ == '__main__':

    # Parse the config file
    config = DB._ParseConfig()

    print("Adding new Entry to the DB!")

    new_Agency = DB.Agency(name="Agency ONE",
                           percentage=16.0)

    new_Customer = DB.Customer(name="BaumSchule Winterberg E.V",
                               contact="Marianna Winter",
                               street="This That Road 34",
                               postcode=12345,
                               city='Duesseldorf',
                               country="UK")

    new_JobCode = DB.Jobtype(name="Super First Jobtype")

    new_Invoice = DB.Invoice(invoice_id="2021-001",
                            date=datetime.now(),
                            description="This was a super Job",
                            invoice_ammount="2755.86",
                            invoice_mwst="16",
                            paydate=datetime.now(),
                            customer_id=1,
                            jobcode_id=1,
                            agency_id=1)

    DB_Session.add(new_Agency)
    DB_Session.add(new_Customer)
    DB_Session.add(new_JobCode)
    DB_Session.add(new_Invoice)

    DB_Session.commit()
