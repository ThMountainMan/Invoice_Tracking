# This Script shall provide the basis for a Invoice Generator / Tracker Tool
# Things will probably be quite messy at the beginning and change a lot during
# the process !!!!

import sys
from datetime import datetime
from HelperClasses import Costumer, Agency, Invoce


if __name__ == '__main__':
    Costumer = Costumer()

    Costumer.id = 123
    Costumer.name = "Company XY"
    Costumer.contact = "Hans Peter"

    print(sys.executable)

    Costumer.print_out()
