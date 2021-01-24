from datetime import datetime
from dateutil import parser
from app_config import AppConfig
import database as DB

import bottle
from bottle import route, static_file
from bottle import request, redirect, template

import export

import logging

log = logging.getLogger(__name__)

# =========================================
# Invoice Related Functions
# =========================================


@route("/invoices/<year>")
@route("/invoices")
@route("/")
def invoices(year=None):
    # If there is a year specified, gett all invoices for this years
    Data = DB.Invoices.get_all(year)
    Expenses = DB.Expenses.get_all(year)

    jobtypes = DB.Jobtypes.get_all()
    # Calculations for the income overview
    income = sum([res.invoice_ammount for res in Data if res.paydate])
    outstanding = sum([res.invoice_ammount for res in Data if not res.paydate])
    expenses = sum([res.cost for res in Expenses])
    dOverview = {'income': round(income, 2), 'outstanding': round(outstanding, 2),
                 'expenses': round(expenses, 2), 'profit': round(income - expenses, 2)}
    # Return the template with the data
    return template("invoices.tpl", overview=dOverview, input=Data, jobtypes=jobtypes)


@ route("/invoice_show/<id>")
def invoice_get(id=None):

    Data = DB.Invoices.get(id)
    log.info(f"Show invoice -{Data.invoice_id}- with id : {id} ...")

    # Data manipulation
    # TODO:  process the data so that we can use it!!
    item_comment = Data.invoice_data['comment']
    item_price = round(float(Data.invoice_data['price']), 2)
    item_count = round(float(Data.invoice_data['ammount']), 2)
    invoice_subtotal = round(item_price * item_count, 2)

    invoice_mwst = round(Data.invoice_ammount * (Data.invoice_mwst / 100), 2)
    invoice_total = round(Data.invoice_ammount + invoice_mwst, 2)

    return template("Invoice/Invoice_V1.tpl",
                    invoice=Data,
                    invoice_subtotal=invoice_subtotal,
                    invoice_mwst=invoice_mwst,
                    invoice_total=invoice_total)


@ route("/invoice_print/<id>")
def invoice_print(id=None):
    Data = DB.Invoices.get(id)
    export.export_to_pdf(f"http://localhost:8080/invoice_show/{id}", Data)
    redirect("/invoices")


@ route("/invoice_add")
@ route("/invoice_add", method="POST")
def invoice_add(id=None):
    print("Add Invoice ...")
    # Check if there is a submitted Form
    if request.method == 'POST':
        print("Create Invoice ...")
        # Get the Form Data as Dict
        Data = request.forms

        # Data Postprocessing before submitting to DB
        # for i in range(1,)
        item_comment = Data.get('comment1')
        item_price = round(float(Data.get('price1')), 2)
        item_count = float(Data.get('ammount1'))
        invoice_subtotal = round(item_price * item_count, 2)

        invoice_mwst = round(invoice_subtotal * (float(Data.get('mwst')) / 100), 2)
        invoice_total = round(invoice_subtotal + invoice_mwst, 2)

        print(type((Data.get('customer_id'))))
        # Prepare the Data for DB input
        new = DB.Invoices(invoice_id=Data.get('id'),
                          date=parser.parse(Data.get('date')),
                          description=Data.get('comment1'),
                          invoice_ammount=invoice_total,
                          invoice_mwst=Data.get('mwst'),
                          paydate=None,
                          # Get all related Data
                          customer_id=Data.get('customer_id'),
                          jobcode_id=Data.get('jobtype_id'),
                          agency_id=Data.get('agency_id'),
                          personal_id=Data.get('personal_id'),
                          # Get the Invoice item data
                          invoice_data={'comment': Data.get('comment1'),
                                        'ammount': Data.get('ammount1'),
                                        'price': Data.get('price1')})

        DB.Invoices.create(new)
        redirect("/invoices")
    else:
        customers = DB.Customers.get_all()
        agencys = DB.Agencys.get_all()
        jobtypes = DB.Jobtypes.get_all()
        personas = DB.PersonalDetails.get_all()
        newid = f"{datetime.now().year}-{DB.Invoices.get_latest_id():03}"
        return template("invoices_edit.tpl",
                        id=newid,
                        customers=customers,
                        agencys=agencys,
                        jobtypes=jobtypes,
                        personas=personas)


@ route("/invoice_delete/<id>")
def invoice_delete(id=None):
    print(f"Deleting Invoice with ID : {id}")
    DB.Invoices.delete(id)
    redirect("/invoices")


@ route("/invoice_pay/<id>", method="POST")
def invoice_pay(id=None):
    # We want to edit an existing CUSTOMER
    # So we need to get the data based on the # ID
    # Get the Form Data as Dict
    Data = request.forms
    # Prepare the Data for DB input
    print(Data.get('date'))
    dUpdate = {'paydate': parser.parse(Data.get('date'))}

    DB.Invoices.update(id, dUpdate)
    redirect("/invoices")

# =========================================
# Customer Related Functions
# =========================================


@ route("/customers")
def customers():
    print("Customer ...")
    Data = DB.Customers.get_all()
    return template("customers.tpl", input=Data)


@ route("/customer_add")
@ route("/customer_add", method="POST")
@ route("/customer_edit/<id>")
@ route("/customer_edit/<id>", method="POST")
def customer_edit(id=None):
    # Check what kind of request has beeing made
    # We can either update or create a new entry
    # The decission is made besed on the ID
    if request.method == 'POST':
        # Receive the HTML form data as dictionary
        Data = request.forms
        # Prepare the Data for DB input
        # decide if we want to update or to create
        if id:
            # We want to update an existion entry
            dUpdate = {'name': Data.get('name'),
                       'contact': Data.get('contact'),
                       'email': Data.get('email'),
                       'phone': Data.get('phone'),
                       'street': Data.get('street'),
                       'postcode': Data.get('postcode'),
                       'city': Data.get('city'),
                       'country': Data.get('country')}
            # Send the new data to the Database
            DB.Customers.update(id, dUpdate)

        else:
            # We want to create a new DB entry
            new = DB.Customers(name=Data.get('name'),
                               contact=Data.get('contact'),
                               email=Data.get('email'),
                               phone=Data.get('phone'),
                               street=Data.get('street'),
                               postcode=Data.get('postcode'),
                               city=Data.get('city'),
                               country=Data.get('country'))
            # Send the new data to the Database
            DB.Customers.create(new)

        # get back to the overview
        redirect("/customers")

    # If the reueast was to edit an agency
    else:
        Data = DB.Customers.get(id) if id else None
        # Return the template with the DB data
        return template("customers_edit.tpl", customer=Data)


@ route("/customer_delete/<id>")
def customer_delete(id=None):
    print(f"Deleting Customer with ID : {id}")
    DB.Customers.delete(id)
    redirect("/customers")


# =========================================
# Jobtype Related Functions
# =========================================


@ route("/jobtypes")
def jobtypes():
    print("Jobtypes ...")
    Data = DB.Jobtypes.get_all()
    return template("jobtypes.tpl", input=Data)


@ route("/jobtype_add")
@ route("/jobtype_add", method="POST")
@ route("/jobtype_edit/<id>")
@ route("/jobtype_edit/<id>", method="POST")
def jobtype_edit(id=None):
    # Check what kind of request has beeing made
    # We can either update or create a new entry
    # The decission is made besed on the ID
    if request.method == 'POST':
        # Receive the HTML form data as dictionary
        Data = request.forms
        # Prepare the Data for DB input
        # decide if we want to update or to create
        if id:
            # We want to update an existion entry
            dUpdate = {'name': Data.get('name'),
                       'contact': Data.get('contact'),
                       # 'email':Data.get('email'),
                       'street': Data.get('street'),
                       'postcode': Data.get('postcode'),
                       'city': Data.get('city'),
                       'country': Data.get('country')}
            # Send the new data to the Database
            DB.Jobtypes.update(id, dUpdate)

        else:
            # We want to create a new DB entry
            new = DB.Jobtypes(name=Data.get('name'))
            # Send the new data to the Database
            DB.Jobtypes.create(new)

        # get back to the overview
        redirect("/jobtypes")

    # If the reueast was to edit an agency
    else:
        Data = DB.Jobtypes.get(id) if id else None
        # Return the template with the DB data
        return template("jobtypes_edit.tpl", jobtype=Data)


@ route("/jobtype_delete/<id>")
def jobtype_delete(id=None):
    print(f"Deleting Jobtype with ID : {id}")
    DB.Jobtypes.delete(id)
    redirect("/jobtypes")


# =========================================
# Agency Related Functions
# =========================================


@ route("/agencys")
def agencys():
    print("Agencys ...")
    Data = DB.Agencys.get_all()
    return template("agencys.tpl", input=Data)


@ route("/agency_add")
@ route("/agency_add", method="POST")
@ route("/agency_edit/<id>")
@ route("/agency_edit/<id>", method="POST")
def agency_edit(id=None):
    # Check what kind of request has beeing made
    # We can either update or create a new entry
    # The decission is made besed on the ID
    if request.method == 'POST':
        # Receive the HTML form data as dictionary
        Data = request.forms
        # Prepare the Data for DB input
        # decide if we want to update or to create
        if id:
            # We want to update an existion entry
            dUpdate = {'name': Data.get('name'),
                       'percentage': Data.get('percentage')}
            # Send the new data to the Database
            DB.Agencys.update(id, dUpdate)

        else:
            # We want to create a new DB entry
            new = DB.Agencys(name=Data.get('name'),
                             percentage=Data.get('percentage'))
            DB.Agencys.create(new)

        # get back to the overview
        redirect("/agencys")

    # If the reueast was to edit an agency
    else:
        Data = DB.Agencys.get(id) if id else None
        # Return the template with the DB data
        return template("agencys_edit.tpl", agency=Data)


@ route("/agency_delete/<id>")
def agency_delete(id=None):
    print(f"Deleting Agency with ID : {id}")
    try:
        DB.Agencys.delete(id)
    except Exception:
        pass
    finally:
        redirect("/agencys")

# =========================================
# EXPENSES FUNCTIONS
# =========================================


@ route("/expenses")
def expenses():
    print("Customer ...")
    Data = DB.Expenses.get_all()
    return template("expenses.tpl", input=Data)


@ route("/expense_add")
@ route("/expense_add", method="POST")
@ route("/expense_edit/<id>")
@ route("/expense_edit/<id>", method="POST")
def expense_edit(id=None):
    # Check what kind of request has beeing made
    # We can either update or create a new entry
    # The decission is made besed on the ID
    if request.method == 'POST':
        # Receive the HTML form data as dictionary
        Data = request.forms
        # Prepare the Data for DB input
        # decide if we want to update or to create
        if id:
            # We want to update an existion entry
            dUpdate = {'expense_id': Data.get('id'),
                       'date': Data.get('date'),
                       'cost': Data.get('cost'),
                       'comment': Data.get('comment')}

            # Send the new data to the Database
            DB.Expenses.update(id, dUpdate)

        else:
            # We want to create a new DB entry
            new = DB.Expenses(expense_id=Data.get('expense_id'),
                              date=parser.parse(Data.get('date')),
                              cost=Data.get('cost'),
                              comment=Data.get('comment'))
            # Send the new data to the Database
            DB.Expenses.create(new)

        # get back to the overview
        redirect("/expenses")

    # If the reueast was to edit an expense
    else:
        Data = DB.Expenses.get(id) if id else None
        newid = f"{datetime.now().year}-{DB.Expenses.get_latest_id():03}"
        # Return the template with the DB data
        return template("expenses_edit.tpl", expense=Data, new_id=newid)


@ route("/expense_delete/<id>")
def expense_delete(id=None):
    print(f"Deleting expense with ID : {id}")
    DB.Expenses.delete(id)
    redirect("/expenses")


# =========================================
# PERSONAL FUNCTIONS
# =========================================


@ route("/personal")
def personals():
    print("Customer ...")
    Data = DB.PersonalDetails.get_all()
    return template("personal.tpl", input=Data)


@ route("/personal_add")
@ route("/personal_add", method="POST")
@ route("/personal_edit/<id>")
@ route("/personal_edit/<id>", method="POST")
def personal_edit(id=None):
    # Check what kind of request has beeing made
    # We can either update or create a new entry
    # The decission is made besed on the ID
    if request.method == 'POST':
        # Receive the HTML form data as dictionary
        Data = request.forms
        # Prepare the Data for DB input
        # decide if we want to update or to create
        if id:
            # We want to update an existion entry
            dUpdate = {'label': Data.get('label'),
                       'name_company': Data.get('name_company'),
                       'name': Data.get('name'),
                       'street': Data.get('street'),
                       'postcode': Data.get('postcode'),
                       'city': Data.get('city'),
                       'mail': Data.get('mail'),
                       'phone': Data.get('phone'),
                       'payment_id': Data.get('payment_details'),
                       'taxnumber': Data.get('taxnumber')
                       }
            # Send the new data to the Database
            DB.PersonalDetails.update(id, dUpdate)

        else:
            # We want to create a new DB entry
            new = DB.PersonalDetails(label=Data.get('label'),
                                     name_company=Data.get('company_name'),
                                     name=Data.get('name'),
                                     street=Data.get('street'),
                                     postcode=Data.get('postcode'),
                                     city=Data.get('city'),
                                     mail=Data.get('mail'),
                                     phone=Data.get('phone'),
                                     payment_id=Data.get('payment_details'),
                                     taxnumber=Data.get('taxnumber')
                                     )
            # Send the new data to the Database
            DB.PersonalDetails.create(new)

        # get back to the overview
        redirect("/personal")

    # If the reueast was to edit an agency
    else:
        Data = DB.PersonalDetails.get(id) if id else None
        payment = DB.PaymentDetails.get_all()
        # Return the template with the DB data
        return template("personal_edit.tpl", data=Data, payment=payment)


@ route("/personal_delete/<id>")
def personal_delete(id=None):
    print(f"Deleting expense with ID : {id}")
    DB.PersonalDetails.delete(id)
    redirect("/personal")


# =========================================
# BANK DETAILS FUNCTIONS
# =========================================


@ route("/payment")
def payments():
    print("Customer ...")
    Data = DB.PaymentDetails.get_all()
    return template("payment.tpl", input=Data)


@ route("/payment_add")
@ route("/payment_add", method="POST")
@ route("/payment_edit/<id>")
@ route("/payment_edit/<id>", method="POST")
def payment_edit(id=None):
    # Check what kind of request has beeing made
    # We can either update or create a new entry
    # The decission is made besed on the ID
    if request.method == 'POST':
        # Receive the HTML form data as dictionary
        Data = request.forms
        # Prepare the Data for DB input
        # decide if we want to update or to create
        if id:
            # We want to update an existion entry
            dUpdate = {'label': Data.get('label'),
                       'name': Data.get('name'),
                       'bank': Data.get('bank'),
                       'IBAN': Data.get('IBAN'),
                       'BIC': Data.get('BIC'),
                       }
            # Send the new data to the Database
            DB.PaymentDetails.update(id, dUpdate)

        else:
            # We want to create a new DB entry
            new = DB.PaymentDetails(label=Data.get('label'),
                                    name=Data.get('name'),
                                    bank=Data.get('bank'),
                                    IBAN=Data.get('IBAN'),
                                    BIC=Data.get('BIC'),
                                    )
            # Send the new data to the Database
            DB.PaymentDetails.create(new)

        # get back to the overview
        redirect("/payment")

    # If the reueast was to edit an agency
    else:
        Data = DB.PaymentDetails.get(id) if id else None
        # Return the template with the DB data
        return template("payment_edit.tpl", data=Data)


@ route("/payment_delete/<id>")
def payment_delete(id=None):
    print(f"Deleting Payment Details with ID : {id}")
    DB.PaymentDetails.delete(id)
    redirect("/payment")

# =========================================
# BASIC FUNCTIONS
# =========================================


@ route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=r".\\static")


@ route('/static/js/<filename>')
def server_static_js(filename):
    return static_file(filename, root=r".\\static\\js")


@ route('/static/css/<filename>')
def server_static_css(filename):
    return static_file(filename, root=r".\\static\\css")


if __name__ == '__main__':
    bottle.debug(False)

    bottle.run(host=AppConfig.web_host, port=AppConfig.web_port)
