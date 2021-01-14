import sys
import os
from datetime import datetime
from dateutil import parser
from database import _ParseConfig
import database as DB

import bottle
from bottle import route, run, static_file
from bottle import request, redirect, template


def start():
    config = _ParseConfig()
    port = config['webserver'].get('port')

    # =========================================
    # Invoice Related Functions
    # =========================================

    @route("/invoices")
    @route("/")
    def home():
        print("Home ...")
        Data = DB.Invoices.get_all()

        return template("invoices.tpl", input=Data)

    @route("/invoice_show/<id>")
    def invoice_get(id=None):
        print("Home ...")
        Data = DB.Invoices.get(id)
        return template("INVOICE.tpl", invoice=Data)
        # return template("invoices_detail.tpl", input=Data)

    @route("/invoice_add")
    @route("/invoice_add", method="POST")
    def invoice_add(id=None):
        print("Add Invoice ...")
        # Check if there is a submitted Form
        if request.method == 'POST':
            print("Create Invoice ...")
            # Get the Form Data as Dict
            Data = request.forms

            print(type((Data.get('customer_id'))))
            # Prepare the Data for DB input
            new_invoice = DB.Invoices(invoice_id=Data.get('id'),
                                      date=parser.parse(Data.get('date')),
                                      description=Data.get('description1'),
                                      invoice_ammount=Data.get('price1'),
                                      invoice_mwst=Data.get('amount1'),
                                      paydate=parser.parse(Data.get('date')),
                                      customer_id=Data.get('customer_id'),
                                      jobcode_id=Data.get('jobtype_id'),
                                      agency_id=Data.get('agency_id'))

            DB.Invoices.create(new_invoice)
            redirect("/invoices")
        else:
            customers = DB.Customers.get_all()
            agencys = DB.Agencys.get_all()
            jobtypes = DB.Jobtypes.get_all()
            newid = f"{datetime.now().year}-{DB.Invoices.get_latest_id():03}"
            return template("invoices_edit.tpl", id=newid, customers=customers, agencys=agencys, jobtypes=jobtypes)

    @route("/invoice_delete/<id>")
    def invoice_delete(id=None):
        if id:
            print(f"Deleting Invoice with ID : {id}")
            DB.Invoices.delete(id)
            redirect("/invoices")
        else:
            redirect("/invoices")

    # =========================================
    # Customer Related Functions
    # =========================================

    @route("/customers")
    def customer():
        print("Customer ...")
        Data = DB.Customers.get_all()
        return template("customers.tpl", input=Data)

    @route("/customer_add")
    @route("/customer_add", method="POST")
    def customer_add():
        # Check if there is a submitted Form
        if request.method == 'POST':
            # Get the Form Data as Dict
            Data = request.forms
            # Prepare the Data for DB input
            new_customer = DB.Customers(name=Data.get('name'),
                                        contact=Data.get('contact'),
                                        street=Data.get('street'),
                                        postcode=Data.get('postcode'),
                                        city=Data.get('city'),
                                        country=Data.get('country'))

            DB.Customers.create(new_customer)
            redirect("/customers")
        else:
            print("Add Customer Form ...")
            return template("customers_edit.tpl", customer=None)

    @route("/customer_edit/<id>")
    @route("/customer_edit/<id>", method="POST")
    def customer_edit(id=None):
        # We want to edit an existing CUSTOMER
        # So we need to get the data based on the # ID
        if id:
            if request.method == 'POST':
                # Get the Form Data as Dict
                Data = request.forms
                # Prepare the Data for DB input
                dUpdate = {'name': Data.get('name'),
                           'contact': Data.get('contact'),
                           # 'email':Data.get('email'),
                           'street': Data.get('street'),
                           'postcode': Data.get('postcode'),
                           'city': Data.get('city'),
                           'country': Data.get('country')}

                DB.Customers.update(id, dUpdate)
                redirect("/customers")

            else:
                Data = DB.Customers.get(id)
                print(Data.name)
                return template("customers_edit.tpl", customer=Data)
        else:
            redirect("/customers")

    @route("/customer_delete/<id>")
    def customer_delete(id=None):
        if id:
            print(f"Deleting Customer with ID : {id}")
            DB.Customers.delete(id)
            redirect("/customers")
        else:
            redirect("/customers")

    # =========================================
    # Jobtype Related Functions
    # =========================================

    @ route("/jobtypes")
    def jobtype():
        print("Jobtypes ...")
        Data = DB.Jobtypes.get_all()
        return template("jobtypes.tpl", input=Data)

    @route("/jobtype_add")
    @route("/jobtype_add", method="POST")
    def jobtype_add():
        # Check if there is a submitted Form
        if request.method == 'POST':
            # Get the Form Data as Dict
            Data = request.forms
            # Prepare the Data for DB input
            new_jobtype = DB.Jobtypes(name=Data.get('name'))

            DB.Jobtypes.create(new_jobtype)
            redirect("/jobtypes")
        else:
            print("Add Jobtype Form ...")
            return template("jobtypes_edit.tpl", jobtype=None)

    @route("/jobtype_edit/<id>")
    @route("/jobtype_edit/<id>", method="POST")
    def jobtype_edit(id=None):
        # We want to edit an existing CUSTOMER
        # So we need to get the data based on the # ID
        if id:
            if request.method == 'POST':
                # Get the Form Data as Dict
                Data = request.forms
                # Prepare the Data for DB input
                dUpdate = {'name': Data.get('name'),
                           'contact': Data.get('contact'),
                           # 'email':Data.get('email'),
                           'street': Data.get('street'),
                           'postcode': Data.get('postcode'),
                           'city': Data.get('city'),
                           'country': Data.get('country')}

                DB.Jobtypes.update(id, dUpdate)
                redirect("/jobtypes")

            else:
                Data = DB.Jobtypes.get(id)
                return template("jobtypes_edit.tpl", jobtype=Data)
        else:
            redirect("/jobtypes")

    @route("/jobtype_delete/<id>")
    def jobtype_delete(id=None):
        if id:
            print(f"Deleting Jobtype with ID : {id}")
            DB.Jobtypes.delete(id)
            redirect("/jobtypes")
        else:
            redirect("/jobtypes")

    # =========================================
    # Agency Related Functions
    # =========================================

    @ route("/agencys")
    def agency():
        print("Agencsy ...")
        Data = DB.Agencys.get_all()
        return template("agencys.tpl", input=Data)

    @ route("/agency_add")
    @ route("/agency_add", method="POST")
    def agency_add():
        # Check if there is a submitted Form
        if request.method == 'POST':
            print("Add Agency Sumitted Data ...")
            # Get the Form Data as Dict
            Data = request.forms
            # Prepare the Data for DB input
            new_Agency = DB.Agencys(name=Data.get('name'),
                                    percentage=Data.get('percentage'))

            DB.Agencys.create(new_Agency)
            redirect("/agencys")

        else:
            print("Add Agency Form ...")
            return template("agencys_edit.tpl")

    @route("/agency_edit/<id>")
    @route("/agency_edit/<id>", method="POST")
    def agency_edit(id=None):
        # We want to edit an existing CUSTOMER
        # So we need to get the data based on the # ID
        if id:
            if request.method == 'POST':
                # Get the Form Data as Dict
                Data = request.forms
                # Prepare the Data for DB input
                dUpdate = {'name': Data.get('name'),
                           'percentage': Data.get('percentage')}

                DB.Agencys.update(id, dUpdate)
                redirect("/agencys")

            else:
                Data = DB.Agencys.get(id)
                return template("agencys_edit.tpl", agency=Data)
        else:
            redirect("/agencys")

    @route("/agency_delete/<id>")
    def agency_delete(id=None):
        if id:
            print(f"Deleting Agency with ID : {id}")
            DB.Agencys.delete(id)
            redirect("/agencys")
        else:
            redirect("/agencys")

    # =========================================
    # BASIC FUNCTIONS
    # =========================================

    @ route('/static/<filename>')
    def server_static(filename):
        return static_file(filename, root=r"F:\\Development\\Projects\\Invoice_Tracking\\src\\static")

    bottle.debug(True)
    run(host='localhost', port=port)


if __name__ == '__main__':
    start()
