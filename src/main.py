# This Script shall provide the basis for a Invoice Generator / Tracker Tool
# Things will probably be quite messy at the beginning and change a lot during
# the process !!!!

import sys
import os
from datetime import datetime
from check_db import DB_Validation, DB_CreateDB, DB_CreateTables
import database as DB
from database import session as DB_Session
from website import start


def main():
    pass


if __name__ == '__main__':

    # Parse the config file
    config = DB._ParseConfig()

    print("Adding new Entry to the DB!")

    new_Agency = DB.Agencys(name="Agency ONE", percentage=16.0)

    new_Customer = DB.Customers(name="BaumSchule Winterberg E.V",
                                contact="Marianna Winter",
                                street="This That Road 34",
                                postcode=12345,
                                city='Duesseldorf',
                                country="UK")

    new_JobCode = DB.Jobtypes(name="Super First Jobtype")

    new_Invoice = DB.Invoices(invoice_id="2021-001",
                              date=datetime.now(),
                              description="This was a super Job",
                              invoice_ammount="2755.86",
                              invoice_mwst="16",
                              paydate=datetime.now(),
                              customer_id=1,
                              jobcode_id=1,
                              agency_id=1)

    DB.Agencys.create(new_Agency)
    DB.Customers.create(new_Customer)
    DB.Jobtypes.create(new_JobCode)
    DB.Invoices.create(new_Invoice)

    # DB.Agencys.delete(ID)

    #result = DB.Agencys.get_all()
    # for i in result:
    #    print(i.name)

    try:
        Test = DB.Invoices.get(1)
        Tdict = Test.__dict__
        # for i in Tdict:
        #    print(Tdict[i])

        print(Test.jobtype)

        print(Tdict)
    except Exception:
        pass

    # DB_Session.commit()
