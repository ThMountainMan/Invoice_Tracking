import database as DB
from dateutil import parser
import logging

# Init the Logger
log = logging.getLogger(__name__)


def DB_Update():
    pass


def DB_Validation():
    """ Try to read the First entry from the DB """
    try:
        Test_Data = DB.Invoices.get(1)
        if not Test_Data.invoice_id:
            return False
        else:
            return True
    except Exception:
        return False


def DB_CreateDB(config):
    pass


def DB_CreateTables(config):
    pass


def DB_CreateDummys():
    """ Fill the DB with test Data .... """

    log.info("Adding Test entrys to the Database ...")

    new_payment = DB.PaymentDetails(label="Test Account",
                                    name="Klaus Albers",
                                    bank="Butterbrot Bank",
                                    IBAN="125454-dfsdf-45454",
                                    BIC="1234567")

    new_personal = DB.PersonalDetails(label="Test Person",
                                      name_company="Nothing CoKg",
                                      name="Hans Wurst",
                                      street="Schinkenstrasse 45",
                                      postcode=45356,
                                      city="Darmstadt",
                                      mail="hans@wurst.de",
                                      phone=11123456,
                                      payment_id=1)

    new_expense = DB.Expenses(expense_id="2020-001",
                              date=parser.parse("2020-01-01"),
                              cost=1234,
                              comment="This is a test Expense")

    new_Agency = DB.Agencys(name="Agency Stargazer",
                            percentage=10)

    new_jobtype = DB.Jobtypes(name="Test Job")

    new_customer = DB.Customers(name="Agency Hupentitt",
                                contact="Tittz Mc Gee",
                                email="this@that.de",
                                phone=101234568,
                                street="Wumsstreet 56",
                                postcode=123456,
                                city="Hannesburg",
                                country="Germany")

    new_invoice = DB.Invoices(invoice_id="2021-001",
                              date=parser.parse("2021-02-02"),
                              description="This is a Test invoice",
                              invoice_ammount=1234,
                              invoice_mwst=16,
                              paydate=None,
                              customer_id=1,
                              jobcode_id=1,
                              agency_id=1,
                              invoice_data={'comment': "Item has been sold and I have done this",
                                            'ammount': 4,
                                            'price': 45})

    DB.PaymentDetails.create(new_payment)
    DB.PersonalDetails.create(new_personal)
    DB.Expenses.create(new_expense)

    DB.Agencys.create(new_Agency)
    DB.Customers.create(new_customer)
    DB.Jobtypes.create(new_jobtype)

    DB.Invoices.create(new_invoice)
