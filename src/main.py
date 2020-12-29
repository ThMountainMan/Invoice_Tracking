# This Script shall provide the basis for a Invoice Generator / Tracker Tool
# Things will probably be quite messy at the beginning and change a lot during
# the process !!!!

import sys
from datetime import datetime
from HelperClasses import Costumer, Agency, Invoce
from check_db import DB_Validation, DB_CreateDB, DB_CreateTables
import database


def main():
    # Validate the DB Connection
    db_config = database._ParseConfig()

    if not DB_Validation(db_config):
        print("No Valid DB found ... Creating the necessarry recources ...")
        # The DB is not available and we need to create it
        Check = DB_CreateDB(db_config)
        Check = DB_CreateTables(db_config)

    else:
        # DB Validation sucess and we can procees as normal
        print("Alles Super Duper hier ....")


if __name__ == '__main__':
    main()
