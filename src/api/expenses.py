import logging

from database import DbConnection, Expenses
from dateutil import parser
from flask import Blueprint, Response, render_template, request
from flask_login import current_user, login_required

from .helper import Container

log = logging.getLogger(__name__)

app_expenses = Blueprint("expenses", __name__)

# =========================================
# EXPENSES FUNCTIONS
# =========================================


@app_expenses.route("/expenses")
@login_required
def expenses():
    container = Container()
    with DbConnection() as db:
        container.expenses = db.query(
            "expenses",
            filters={"user_id": current_user.id},
            order_by="expense_id",
            reverse=True,
        )
    return render_template("expenses.html", **container)


@app_expenses.route("/expenses/edit", methods=["POST"])
@login_required
def expense_edit():
    try:
        with DbConnection() as db:
            id = request.form.get("id")
            # Get the expense we want to edit
            if request.form["action"] == "edit":
                expenses = db.get("expenses", id) if id else Expenses()
            # delete the selected expense
            elif request.form["action"] == "delete":
                db.delete("expenses", id)
                return {"success": True}
            # TODO: How doe we rollback properly ?
            elif request.form["action"] == "restore":
                db.rollback()
                return {"success": True}

            if not id:
                new_id = expenses.generate_id()
                expenses.expense_id = new_id
            # Collect the Form Data
            form_data = request.form
            # Create or Update the Expenses
            expenses.date = parser.parse(form_data.get("date"))
            expenses.cost = form_data.get("cost").replace(",", ".").replace("€", "")
            expenses.comment = form_data.get("comment")
            expenses.user_id = current_user.id

            if expenses.id:
                db.merge(expenses)
            else:
                db.add(expenses)
            return {"success": True}
    except Exception as e:
        return str(e)
