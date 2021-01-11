import sys
import os
from datetime import datetime
from database import _ParseConfig
import database as DB

import bottle
from bottle import route, run, template, static_file


def start():
    config = _ParseConfig()
    port = config['webserver'].get('port')

    # Invoice Related Functions
    @route("/")
    def home():
        print("Home ...")
        Data = DB.Invoices.get_all()
        return template("invoices.tpl", input=Data)

    @route("/invoices/<id>")
    def invoice_get(id=None):
        print("Home ...")
        Data = DB.Invoices.get(id)
        return template("invoices_detail.tpl", input=Data)

    @route("/invoices_add")
    def invoice_get(id=None):
        print("Add Invoice ...")

        NewInvoice = DB.Invoices(invoice_id="2021-001",
                                 date=datetime.now(),
                                 description="This was a super Job",
                                 invoice_ammount="2755.86",
                                 invoice_mwst="16",
                                 paydate=datetime.now(),
                                 customer_id=1,
                                 jobcode_id=1,
                                 agency_id=1)

        customers = DB.Customers.get_all()
        agencys = DB.Agencys.get_all()
        jobtypes = DB.Jobtypes.get_all()
        #Data = DB.Invoices.create(NewInvoice)
        return template("invoices_edit.tpl", input=NewInvoice, customers=customers, agencys=agencys, jobtypes=jobtypes)

    # Customer Related Functions
    @route("/customers")
    def customer():
        print("Customer ...")
        Data = DB.Customers.get_all()
        return template("customers.tpl", input=Data)

    # Jobtype Related Functions
    @route("/jobtypes")
    def jobtype():
        print("Jobtypes ...")
        Data = DB.Jobtypes.get_all()
        return template("jobtypes.tpl", input=Data)

    # Agency Related Functions
    @route("/agencys")
    def agency():
        print("Agencsy ...")
        Data = DB.Agencys.get_all()
        return template("agencys.tpl", input=Data)

    @route("/test")
    def test():
        return template("test.tpl")

    @route('/static/<filename>')
    def server_static(filename):
        return static_file(filename, root=r"F:\\Development\\Projects\\Invoice_Tracking\\src\\static")

    bottle.debug(True)
    run(host='localhost', port=port)


if __name__ == '__main__':
    start()
