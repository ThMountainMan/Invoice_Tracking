import logging
import os

import export
from database import DbConnection, Invoices, Invoices_Item
from dateutil import parser
from flask import Blueprint, abort, redirect, render_template, request, send_file
from flask.wrappers import Response
from flask_login import current_user, login_required
from datetime import datetime

from .helper import Container

log = logging.getLogger(__name__)

app_invoices = Blueprint("invoices", __name__)

# =========================================
# Invoice Related Functions
# =========================================


@app_invoices.route("/", defaults={"year": datetime.now().year})
@app_invoices.route("/<year>")
@login_required
def invoices(year=None):
    container = Container()
    with DbConnection() as db:
        invoices = db.query(
            "invoices",
            filters={"user_id": current_user.id},
            reverse=True,
            order_by="invoice_id",
        )
        expenses = db.query("expenses", filters={"user_id": current_user.id})

        if year:
            invoices = [res for res in invoices if res.date.year == int(year)]
            expenses = [res for res in expenses if res.date.year == int(year)]

        container.invoices = invoices
        container.expenses = expenses
        container.jobtypes = db.query("jobtypes", filters={"user_id": current_user.id})
        container.customers = db.query(
            "customers", filters={"user_id": current_user.id}, order_by="name"
        )
        container.personas = db.query(
            "personaldetails",
            filters={"user_id": current_user.id},
            order_by="label",
        )
        container.agencys = db.query(
            "agencys", filters={"user_id": current_user.id}, order_by="name"
        )

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
        container.year = year

    return render_template("invoices.html", **container)


@app_invoices.route("/invoice/edit", methods=["POST"])
@login_required
def invoice_edit():
    try:
        container = Container()
        with DbConnection() as db:
            id = request.form.get("id")
            # Get the expense we want to edit
            if request.form["action"] == "edit":
                invoice = db.get("invoices", id) if id else Invoices()
            # delete the selected expense
            elif request.form["action"] == "delete":
                db.delete("invoices", id)
                return {"success": True}

            elif request.form["action"] == "pay":
                invoice = db.get("invoices", id)
                invoice.paydate = parser.parse(request.form.get("paydate"))
                db.merge(invoice)
                return {"success": True}

            # TODO: How doe we rollback properly ?
            elif request.form["action"] == "restore":
                db.rollback()
                return {"success": True}
            # Collect the Form Data
            form_data = request.form

            # Create or Update the Jobtypes
            invoice.invoice_id = (
                invoice.generate_id() if not id else form_data.get("invoice_id")
            )
            invoice.date = parser.parse(form_data.get("date"))
            invoice.invoice_mwst = form_data.get("mwst")

            invoice.customer_id = form_data.get("customer_id")
            invoice.jobcode_id = form_data.get("jobcode_id")
            invoice.agency_id = (
                form_data.get("agency_id")
                if form_data.get("agency_id") != "None"
                else None
            )
            invoice.personal_id = form_data.get("personal_id")

            # Creat a   joint list of the invoice items
            _itemID = request.form.get("item_id")
            _count = request.form.get("count", type=float)
            _cost = request.form.get("cost", type=float)
            _description = request.form.get("description", type=str)

            __list = [_itemID, _count, _cost, _description]
            # _items = map(list, zip(_itemID, _count, _cost, _description))
            _items = [__list]

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
                invoice.user_id = current_user.id
                db.add(invoice)

                for item in invoice_items:
                    db.add(item)

            return {"success": True}
    except Exception as e:
        # response.status = 400
        return str(e)


@app_invoices.route("/invoice/display/<id>")
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
            html_data = render_template("templates/Invoice_V1.html", **container)

            log.info(
                f"Show invoice -{container.invoice.invoice_id}- with id : {id} ..."
            )
            return html_data

    except Exception as e:
        # response.status = 400
        return str(e)


@app_invoices.route("/invoice/download/<id>")
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
            html_data = render_template("templates/Invoice_V1.html", **container)
            File, Path = export.export_to_pdf(html_data, container.invoice)
            # return send_file(File, root=Path, download=File)
            return send_file(os.path.join("..", Path, File), as_attachment=True)

    except Exception as e:
        # response.status = 400
        return str(e)
