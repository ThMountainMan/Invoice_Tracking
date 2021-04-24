#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dateutil import parser
from app_config import AppConfig
import database as DB

import os
import bottle
from bottle import route, static_file
from bottle import request, redirect, template

import export
import process_form_data as fData

import logging
log = logging.getLogger(__name__)

# =========================================
# Invoice Related Functions
# =========================================

# Add the Template Path to bottle
# This is done to run the Scrip on Linux as well
bottle.TEMPLATE_PATH.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'views'))


@route("/invoices/<year>")
@route("/invoices")
@route("/")
def invoices(year=None):
    # If there is a year specified, get all invoices for this years
    Data = DB.Invoices.get_all(year)
    # Get all expenses for the selected year
    Expenses = DB.Expenses.get_all(year)
    # Get all available Jobtypes ( for the filter )
    jobtypes = DB.Jobtypes.get_all()

    # Calculations for the income overview
    income = sum([res.get_ammount()['sum_mwst']
                 for res in Data if res.paydate])
    outstanding = sum([res.get_ammount()['sum_mwst']
                      for res in Data if not res.paydate])
    expenses = sum([res.cost for res in Expenses])
    dOverview = {'income': round(income, 2), 'outstanding': round(outstanding, 2),
                 'expenses': round(expenses, 2), 'profit': round(income - expenses, 2)}

    # Return the template with the defined data
    return template("invoices.tpl", overview=dOverview, input=Data, jobtypes=jobtypes)


@ route("/invoice_show/<id>", method=["POST", 'GET'])
def invoice_get(id=None):

    Data = DB.Invoices.get(id)
    log.info(f"Show invoice -{Data.invoice_id}- with id : {id} ...")

    html_data = template("Invoice/Invoice_V1.tpl",
                         invoice=Data,
                         items=Data.get_items(),
                         total=Data.get_ammount()['sum'],
                         mwst=Data.get_ammount()['mwst'],
                         total_mwst=Data.get_ammount()['sum_mwst'])

    if request.method == "POST":
        File, Path = export.export_to_pdf(html_data, Data)
        return static_file(File, root=Path, download=File)
        # redirect("/invoices")
    else:
        return html_data


@ route("/invoice_edit/<id>")
@ route("/invoice_edit/<id>", method="POST")
def invoice_edit(id=None):
    print("Edit Invoice ...")
    if request.method == 'POST' and id:
        # Get the Data for the given invoice
        Data = DB.Invoices.get(id)


@ route("/invoice_add")
@ route("/invoice_add", method="POST")
def invoice_add(id=None):
    print("Add Invoice ...")
    # Check if there is a submitted Form
    if request.method == 'POST':
        print("Create Invoice ...")
        # Get the Form Data as Dict
        Data = request.forms

        # Prepare the Data for DB input
        new = DB.Invoices(invoice_id=Data.get('id'),
                          date=parser.parse(Data.get('date')),
                          description=None,
                          invoice_mwst=Data.get('mwst'),
                          paydate=None,
                          # Get all related Data
                          customer_id=Data.get('customer_id'),
                          jobcode_id=Data.get('jobtype_id'),
                          agency_id=Data.get('agency_id'),
                          personal_id=Data.get('personal_id'))

        # Create a new Invoice in the DB
        newID = DB.Invoices.create(new)

        # Creat a joint list of the invoice items
        lItems = map(list, zip(request.POST.getall('ammount'), request.POST.getall(
            'price'), request.POST.getall('comment')))

        for _item in lItems:
            _new = DB.Invoices_Item(parent_id=newID,
                                    description=_item[2].encode('iso-8859-1'),
                                    count=_item[0],
                                    cost=_item[1])
            # Create a new DB entry for the items
            DB.Invoices_Item.create(_new)

        # redirect(f"/invoice_show/{newID}", code=307)
        # redirect(f"/invoice_show/{newID}")
        redirect("/invoices")
    else:
        customers = DB.Customers.get_all()
        agencys = DB.Agencys.get_all()
        jobtypes = DB.Jobtypes.get_all()
        personas = DB.PersonalDetails.get_all()
        newid = DB.Invoices.get_latest_id()
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
            # Send the new data to the Database
            DB.Customers.update(id, fData.process_update_data_Customer(Data))

        else:
            # We want to create a new DB entry
            new = DB.Customers(name=Data.get('name').encode('iso-8859-1'),
                               contact=Data.get('contact').encode(
                                   'iso-8859-1'),
                               email=Data.get('email').encode('iso-8859-1'),
                               phone=Data.get('phone'),
                               street=Data.get('street').encode('iso-8859-1'),
                               postcode=Data.get('postcode'),
                               city=Data.get('city').encode('iso-8859-1'),
                               country=Data.get('country').encode('iso-8859-1'))
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

    for i in Data:
        print(i.name)

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
        # decide if we want to update or to creates
        if id:
            # We want to update an existion entry
            # Send the new data to the Database
            DB.Jobtypes.update(id, fData.process_update_data_Jobtype(Data))

        else:
            # We want to create a new DB entry
            new = DB.Jobtypes(name=Data.get('name').encode('iso-8859-1'))
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
            # Send the new data to the Database
            DB.Agencys.update(id, fData.process_update_data_Agency(Data))

        else:
            # We want to create a new DB entry
            new = DB.Agencys(name=Data.get('name').encode('iso-8859-1'),
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
            # Send the new data to the Database
            DB.Expenses.update(id, fData.process_update_data_Expense(Data))

        else:
            # We want to create a new DB entry
            new = DB.Expenses(expense_id=Data.get('expense_id'),
                              date=parser.parse(Data.get('date')),
                              cost=Data.get('cost'),
                              comment=Data.get('comment').encode('iso-8859-1'))
            # Send the new data to the Database
            DB.Expenses.create(new)

        # get back to the overview
        redirect("/expenses")

    # If the reueast was to edit an expense
    else:
        Data = DB.Expenses.get(id) if id else None
        newid = DB.Expenses.get_latest_id()
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
            # Send the new data to the Database
            DB.PersonalDetails.update(
                id, fData.process_update_data_PersonalData(Data))

        else:
            # We want to create a new DB entry
            new = DB.PersonalDetails(label=Data.get('label').encode('iso-8859-1'),
                                     name_company=Data.get(
                                         'company_name').encode('iso-8859-1'),
                                     name=Data.get('name').encode(
                                         'iso-8859-1'),
                                     street=Data.get('street').encode(
                                         'iso-8859-1'),
                                     postcode=Data.get('postcode'),
                                     city=Data.get('city').encode(
                                         'iso-8859-1'),
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
            # Send the new data to the Database
            DB.PaymentDetails.update(
                id, fData.process_update_data_PaymentDetails(Data))

        else:
            # We want to create a new DB entry
            new = DB.PaymentDetails(label=Data.get('label').encode('iso-8859-1'),
                                    name=Data.get('name').encode('iso-8859-1'),
                                    bank=Data.get('bank').encode('iso-8859-1'),
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


@ route('/static/<path>/<filename>')
def server_static(path, filename):
    return static_file(filename, root=os.path.join(os.path.dirname(__file__), 'static', path))


if __name__ == '__main__':
    bottle.debug(False)
    bottle.run(host=AppConfig.web_host, port=AppConfig.web_port)
