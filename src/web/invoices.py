import logging

import export
from bottle import get, redirect, request, route, static_file, template, response, post
from database import DbConnection, Invoices, Invoices_Item
from dateutil import parser

from .helper import Container

log = logging.getLogger(__name__)


# =========================================
# Invoice Related Functions
# =========================================


@get("/")
@get("/invoices")
@get("/invoices/<year>")
def invoices(year=None):
    with DbConnection() as db:
        container = Container()
        invoices = db.query("invoices", reverse=True, order_by="invoice_id")
        expenses = db.query("expenses")
        if year:
            invoices = [res for res in invoices if res.date.year == int(year)]
            expenses = [res for res in expenses if res.date.year == int(year)]

        if not invoices:
            pass

        container.invoices = invoices
        container.expenses = expenses
        container.jobtypes = db.query("jobtypes")
        container.customers = db.query("customers", order_by="name")
        container.personas = db.query("personaldetails", order_by="label")
        container.agencys = db.query("agencys", order_by="name")

        # Calculations for the income overview
        # calculate the current income
        payed = [invoice for invoice in container.invoices if invoice.paydate]
        income = sum(invoice.get_total() for invoice in payed)
        # calculate the outstanding amount
        open = [invoice for invoice in container.invoices if not invoice.paydate]
        outstanding = sum(invoice.get_total() for invoice in open)

        sum_expenses = sum(res.cost for res in expenses)
        container.income = round(income, 2)
        container.outstanding = round(outstanding, 2)
        container.expenses = round(sum_expenses, 2)
        container.profit = round(income - sum_expenses, 2)

    return template("invoicesV2.tpl", **container)


@post("/invoice/edit")
def invoice_edit():
    try:
        with DbConnection() as db:
            container = Container()
            id = request.POST.get("id")
            # Get the expense we want to edit
            if request.POST["action"] == "edit":
                invoice = db.get("invoices", id) if id else Invoices()
            # delete the selected expense
            elif request.POST["action"] == "delete":
                db.delete("invoices", id)
                return {"success": True}

            elif request.POST["action"] == "pay":
                invoice = db.get("invoices", id)
                invoice.paydate = parser.parse(request.POST.get("paydate"))
                db.merge(invoice)
                return {"success": True}

            # TODO: How doe we rollback properly ?
            elif request.POST["action"] == "restore":
                db.rollback()
                return {"success": True}
            # Collect the Form Data
            form_data = request.forms
            # Create or Update the Jobtypes
            invoice.invoice_id = (
                invoice.generate_id() if not id else form_data.get("invoice_id")
            )
            invoice.date = parser.parse(form_data.get("date"))
            invoice.invoice_mwst = form_data.get("mwst")

            invoice.customer_id = form_data.get("customer_id")
            invoice.jobcode_id = form_data.get("jobcode_id")
            invoice.agency_id = form_data.get("agency_id")
            invoice.personal_id = form_data.get("personal_id")

            # Creat a joint list of the invoice items
            _itemID = request.POST.getall("item_id")
            _count = request.POST.getall("count")
            _cost = request.POST.getall("cost")
            _description = request.POST.getall("description")
            _items = map(list, zip(_itemID, _count, _cost, _description))

            invoice_items = []
            for item in _items:
                new_item = (
                    db.get("invoices_item", item[0]) if item[0] else Invoices_Item()
                )
                new_item.count = float(item[1])
                new_item.cost = float(item[2])
                new_item.description = item[3]
                new_item.parent_id = id if id else (invoice.get_latest_invoice_id() + 1)

                invoice_items.append(new_item)

            if invoice.id:
                db.merge(invoice)

                for item in invoice_items:
                    db.merge(item)

            else:
                db.add(invoice)

                for item in invoice_items:
                    db.add(item)

            return {"success": True}
    except Exception as e:
        response.status = 400
        return str(e)


@get("/invoice/display/<id>")
def invoice_display(id=None):
    try:
        with DbConnection() as db:
            container = Container()
            container.invoice = db.query("invoices", filters={"id": id})[0]
            container.items = container.invoice.items
            container.netto = container.invoice.get_sum()
            container.brutto = container.invoice.get_total()
            container.mwst = container.invoice.get_mwst()

            container.sum_mwst = container.invoice.get_sum_mwst()
            html_data = template("Invoice/Invoice_V1.tpl", **container)

            log.info(
                f"Show invoice -{container.invoice.invoice_id}- with id : {id} ..."
            )
            return html_data

    except Exception as e:
        response.status = 400
        return str(e)


@get("/invoice/download/<id>")
def invoice_download(id=None):
    try:
        with DbConnection() as db:
            container = Container()
            container.invoice = db.query("invoices", filters={"id": id})[0]
            container.items = container.invoice.items
            container.netto = container.invoice.get_sum()
            container.brutto = container.invoice.get_total()
            container.mwst = container.invoice.get_mwst()

            container.sum_mwst = container.invoice.get_sum_mwst()
            html_data = template("Invoice/Invoice_V1.tpl", **container)
            File, Path = export.export_to_pdf(html_data, container.invoice)
            return static_file(File, root=Path, download=File)

    except Exception as e:
        response.status = 400
        return str(e)
