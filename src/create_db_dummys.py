import database as DB


def filldb():
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
