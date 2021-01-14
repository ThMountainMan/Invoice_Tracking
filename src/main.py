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
    try:
        # Try to read the First entry from the DB
        # If that does not work -> Create Dummy Entrys !!!
        Test = DB.Invoices.get(1)
        print(Test.jobtype)
    except Exception:
        from create_db_dummys import filldb
        filldb()

    # DB_Session.commit()
