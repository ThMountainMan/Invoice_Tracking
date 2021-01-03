# This Script shall provide the basis for a Invoice Generator / Tracker Tool
# Things will probably be quite messy at the beginning and change a lot during
# the process !!!!

import sys
from datetime import datetime

from HelperClasses import Costumer, Agency, Invoce, Jobtype
from check_db import DB_Validation, DB_CreateDB, DB_CreateTables
import database as DB
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

    #Test = DB.get_customer(5)[0]
    #for i in Test:
    #    print(f"{i} - {Test[i]}")
    #DB.create_customer(dCustumer)
    #DB.create_agency(dAgency)
    #DB.create_jobtype(dJobtype)
    #DB.create_invoice(dInvoice)


if __name__ == '__main__':

    # Parse the config file
    config = DB._ParseConfig()

    dCustumer = {'name': "BaumSchule Winterberg E.V",
                 'contact': "Marianna Winter",
                 'street': "This That Road 34",
                 'postcode': 12345,
                 'city': 'Duesseldorf',
                 'country': "UK"}

    dJobtype = {'name': "Super First Jobtype"}

    dAgency = {'name': "Agency ONE",
               'percentage': 16.0}

    dInvoice = {'invoice_id': "2021-001",
                'date': datetime.now(),
                'description': "This was a super Job",
                'invoice_ammount': "2755.86",
                'invoice_mwst': "16",
                'paydate': datetime.now(),
                'customer_id': 1,
                'jobcode_id': 1,
                'agency_id': 1}

    #start(config)
    print("Hallo")
    print(DB.get_invoice())
    #main()
