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

    @route("/invoices/<year>")
    @route("/invoices")
    @route("/")
    def invoices(year=None):
        print("Home ...")
        # If there is a year specified, gett all invoices for this years
        Data = DB.Invoices.get_all(year)
        Expenses = DB.Expenses.get_all(year)

        # Calculations for the income overview
        dOverview = {'income': sum([res.invoice_ammount for res in Data if res.paydate]),
                     'outstanding': sum([res.invoice_ammount for res in Data if not res.paydate]),
                     'expenses': sum([res.cost for res in Expenses])}
        # Return the template with the data
        return template("invoices.tpl", overview=dOverview, input=Data)

    @ route("/invoice_show/<id>")
    def invoice_get(id=None):
        print("Home ...")
        Data = DB.Invoices.get(id)

        # Data manipulation
        # TODO:  process the data so that we can use it!!
        item_comment = Data.invoice_data['comment']
        item_price = round(float(Data.invoice_data['price']), 2)
        item_count = round(float(Data.invoice_data['ammount']), 2)
        invoice_subtotal = item_price * item_count

        invoice_mwst = round(Data.invoice_ammount * (Data.invoice_mwst / 100), 2)
        invoice_total = Data.invoice_ammount + invoice_mwst

        return template("Invoice/Invoice_V1.tpl",
                        invoice=Data,
                        invoice_subtotal=invoice_subtotal,
                        invoice_mwst=invoice_mwst,
                        invoice_total=invoice_total)

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
            item_price = float(Data.get('price1'))
            item_count = float(Data.get('ammount1'))
            invoice_subtotal = item_price * item_count

            invoice_mwst = round(invoice_subtotal * (float(Data.get('mwst')) / 100), 2)
            invoice_total = invoice_subtotal + invoice_mwst

            print(type((Data.get('customer_id'))))
            # Prepare the Data for DB input
            new = DB.Invoices(invoice_id=Data.get('id'),
                              date=parser.parse(Data.get('date')),
                              description=Data.get('comment1'),
                              invoice_ammount=invoice_total,
                              invoice_mwst=Data.get('mwst'),
                              paydate=None,
                              customer_id=Data.get('customer_id'),
                              jobcode_id=Data.get('jobtype_id'),
                              agency_id=Data.get('agency_id'),
                              invoice_data={'comment': Data.get('comment1'),
                                            'ammount': Data.get('ammount1'),
                                            'price': Data.get('price1')})

            DB.Invoices.create(new)
            redirect("/invoices")
        else:
            customers = DB.Customers.get_all()
            agencys = DB.Agencys.get_all()
            jobtypes = DB.Jobtypes.get_all()
            newid = f"{datetime.now().year}-{DB.Invoices.get_latest_id():03}"
            return template("invoices_edit.tpl",
                            id=newid,
                            customers=customers,
                            agencys=agencys,
                            jobtypes=jobtypes)

    @ route("/invoice_delete/<id>")
    def invoice_delete(id=None):
        if id:
            print(f"Deleting Invoice with ID : {id}")
            DB.Invoices.delete(id)
            redirect("/invoices")
        else:
            redirect("/invoices")

    @ route("/invoice_pay/<id>", method="POST")
    def invoice_pay(id=None):
        # We want to edit an existing CUSTOMER
        # So we need to get the data based on the # ID
        if id:
            print(id)
            if request.method == 'POST':
                # Get the Form Data as Dict
                Data = request.forms
                # Prepare the Data for DB input
                print(Data.get('date'))
                dUpdate = {'paydate': parser.parse(Data.get('date'))}

                DB.Invoices.update(id, dUpdate)
                redirect("/invoices")
        else:
            redirect("/invoicess")
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
    def customer_add():
        # Check if there is a submitted Form
        if request.method == 'POST':
            # Get the Form Data as Dict
            Data = request.forms
            # Prepare the Data for DB input
            new = DB.Customers(name=Data.get('name'),
                               contact=Data.get('contact'),
                               email=Data.get('email'),
                               phone=Data.get('phone'),
                               street=Data.get('street'),
                               postcode=Data.get('postcode'),
                               city=Data.get('city'),
                               country=Data.get('country'))

            DB.Customers.create(new)
            redirect("/customers")
        else:
            print("Add Customer Form ...")
            return template("customers_edit.tpl", customer=None)

    @ route("/customer_edit/<id>")
    @ route("/customer_edit/<id>", method="POST")
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

    @ route("/customer_delete/<id>")
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
    def jobtypes():
        print("Jobtypes ...")
        Data = DB.Jobtypes.get_all()
        return template("jobtypes.tpl", input=Data)

    @ route("/jobtype_add")
    @ route("/jobtype_add", method="POST")
    def jobtype_add():
        # Check if there is a submitted Form
        if request.method == 'POST':
            # Get the Form Data as Dict
            Data = request.forms
            # Prepare the Data for DB input
            newnew = DB.Jobtypes(name=Data.get('name'))

            DB.Jobtypes.create(new)
            redirect("/jobtypes")
        else:
            print("Add Jobtype Form ...")
            return template("jobtypes_edit.tpl", jobtype=None)

    @ route("/jobtype_edit/<id>")
    @ route("/jobtype_edit/<id>", method="POST")
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

    @ route("/jobtype_delete/<id>")
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
    def agencys():
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
            new = DB.Agencys(name=Data.get('name'),
                             percentage=Data.get('percentage'))

            DB.Agencys.create(new)
            redirect("/agencys")

        else:
            print("Add Agency Form ...")
            return template("agencys_edit.tpl", agency=None)

    @ route("/agency_edit/<id>")
    @ route("/agency_edit/<id>", method="POST")
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

    @ route("/agency_delete/<id>")
    def agency_delete(id=None):
        if id:
            print(f"Deleting Agency with ID : {id}")
            DB.Agencys.delete(id)
            redirect("/agencys")
        else:
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
    def expense_add():
        # Check if there is a submitted Form
        if request.method == 'POST':
            # Get the Form Data as Dict
            Data = request.forms
            # Prepare the Data for DB input
            new = DB.Expenses(expense_id=Data.get('expense_id'),
                              date=parser.parse(Data.get('date')),
                              cost=Data.get('cost'),
                              comment=Data.get('comment'))

            DB.Expenses.create(new)
            redirect("/expenses")
        else:
            print("Add expense Form ...")
            newid = f"{datetime.now().year}-{DB.Expenses.get_latest_id():03}"
            return template("expenses_edit.tpl", expense=None, id=newid)

    @ route("/expense_edit/<id>")
    @ route("/expense_edit/<id>", method="POST")
    def expense_edit(id=None):
        # We want to edit an existing expense
        # So we need to get the data based on the # ID
        if id:
            if request.method == 'POST':
                # Get the Form Data as Dict
                Data = request.forms
                # Prepare the Data for DB input
                dUpdate = {'expense_id': Data.get('id'),
                           'date': Data.get('date'),
                           'cost': Data.get('cost'),
                           'comment': Data.get('comment')}

                DB.Expenses.update(id, dUpdate)
                redirect("/expenses")

            else:
                Data = DB.Expenses.get(id)
                return template("expenses_edit.tpl", expense=Data)
        else:
            redirect("/expenses")

    @ route("/expense_delete/<id>")
    def expense_delete(id=None):
        if id:
            print(f"Deleting expense with ID : {id}")
            DB.Expenses.delete(id)
            redirect("/expenses")
        else:
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
    def personal_add():
        # Check if there is a submitted Form
        if request.method == 'POST':
            # Get the Form Data as Dict
            Data = request.forms
            # Prepare the Data for DB input
            new = DB.PersonalDetails(label=Data.get('label'),
                                     name_company=Data.get('company_name'),
                                     name=Data.get('name'),
                                     street=Data.get('street'),
                                     postcode=Data.get('postcode'),
                                     city=Data.get('city'),
                                     mail=Data.get('mail'),
                                     phone=Data.get('phone'),
                                     payment_id=Data.get('payment_details'),
                                     )

            DB.PersonalDetails.create(new)
            redirect("/personal")
        else:
            print("Add Personal Form ...")

            payment = DB.PaymentDetails.get_all()
            return template("personal_edit.tpl", data=None, payment=payment)

    @ route("/personal_edit/<id>")
    @ route("/personal_edit/<id>", method="POST")
    def personal_edit(id=None):
        # We want to edit an existing expense
        # So we need to get the data based on the # ID
        if id:
            if request.method == 'POST':
                # Get the Form Data as Dict
                Data = request.forms
                # Prepare the Data for DB input
                dUpdate = {'label': Data.get('label'),
                           'name_company': Data.get('name_company'),
                           'name': Data.get('name'),
                           'street': Data.get('street'),
                           'postcode': Data.get('postcode'),
                           'city': Data.get('city'),
                           'mail': Data.get('mail'),
                           'phone': Data.get('phone'),
                           'payment_id': Data.get('payment_details')
                           }

                DB.PersonalDetails.update(id, dUpdate)
                redirect("/personal")

            else:
                Data = DB.PersonalDetails.get(id)
                payment = DB.PaymentDetails.get_all()
                return template("personal_edit.tpl", data=Data, payment=payment)
        else:
            redirect("/personal")

    @ route("/personal_delete/<id>")
    def personal_delete(id=None):
        if id:
            print(f"Deleting expense with ID : {id}")
            DB.PersonalDetails.delete(id)
            redirect("/personal")
        else:
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
    def payment_add():
        # Check if there is a submitted Form
        if request.method == 'POST':
            # Get the Form Data as Dict
            Data = request.forms
            # Prepare the Data for DB input
            new = DB.PaymentDetails(label=Data.get('label'),
                                    name=Data.get('name'),
                                    bank=Data.get('bank'),
                                    IBAN=Data.get('IBAN'),
                                    BIC=Data.get('BIC'),
                                    )

            DB.PaymentDetails.create(new)
            redirect("/payment")
        else:
            print("Add Payment Form ...")
            return template("payment_edit.tpl", data=None)

    @ route("/payment_edit/<id>")
    @ route("/payment_edit/<id>", method="POST")
    def payment_edit(id=None):
        # We want to edit an existing expense
        # So we need to get the data based on the # ID
        if id:
            if request.method == 'POST':
                # Get the Form Data as Dict
                Data = request.forms
                # Prepare the Data for DB input
                dUpdate = {'label': Data.get('label'),
                           'name': Data.get('name'),
                           'bank': Data.get('bank'),
                           'IBAN': Data.get('IBAN'),
                           'BIC': Data.get('BIC'),
                           }

                DB.PaymentDetails.update(id, dUpdate)
                redirect("/payment")

            else:
                Data = DB.PaymentDetails.get(id)
                return template("payment_edit.tpl", data=Data)
        else:
            redirect("/payment")

    @ route("/payment_delete/<id>")
    def payment_delete(id=None):
        if id:
            print(f"Deleting Payment Details with ID : {id}")
            DB.PaymentDetails.delete(id)
            redirect("/payment")
        else:
            redirect("/payment")

    # =========================================
    # BASIC FUNCTIONS
    # =========================================

    @ route('/static/<filename>')
    def server_static(filename):
        return static_file(filename, root=r"F:\\Development\\Projects\\Invoice_Tracking\\src\\static")

    bottle.debug(True)
    run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    start()
