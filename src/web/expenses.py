import logging

from bottle import get, post, request, response, template
from database import DbConnection, Expenses
from dateutil import parser

log = logging.getLogger(__name__)


# =========================================
# EXPENSES FUNCTIONS
# =========================================


@get("/expenses")
def expenses():
    with DbConnection() as db:
        data = db.query("expenses")
    return template("expenses.tpl", input=data)


@post("/expenses/edit")
def expense_edit():
    try:
        with DbConnection() as db:
            id = request.POST.get("id")
            # Get the expense we want to edit
            if request.POST["action"] == "edit":
                expenses = db.get("expenses", id) if id else Expenses()
            # delete the selected expense
            elif request.POST["action"] == "delete":
                db.delete("expenses", id)
                return {"success": True}
            # TODO: How doe we rollback properly ?
            elif request.POST["action"] == "restore":
                db.rollback()
                return {"success": True}
            # Collect the Form Data
            form_data = request.forms
            # Create or Update the Expenses
            expenses.expense_id = form_data.get("expense_id")
            expenses.date = parser.parse(form_data.get("date"))
            expenses.cost = form_data.get("cost").replace(",", ".")
            expenses.comment = form_data.get("comment").encode("iso-8859-1") or None

            if expenses.id:
                db.merge(expenses)
            else:
                db.add(expenses)
            return {"success": True}
    except Exception as e:
        response.status = 400
        return str(e)
