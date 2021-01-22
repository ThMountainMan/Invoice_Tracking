# This Script shall provide the basis for a Invoice Generator / Tracker Tool
# Things will probably be quite messy at the beginning and change a lot during
# the process !!!!

import sys
import os
import database as DB
import server


def main():
    try:
        # Try to read the First entry from the DB
        # If that does not work -> Create Dummy Entrys !!!
        Test = DB.Invoices.get(1)
        print(Test.jobtype)
    except Exception:
        import create_db_dummys

    server.run()


if __name__ == '__main__':
    main()
