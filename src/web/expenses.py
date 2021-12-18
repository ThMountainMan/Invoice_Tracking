from bottle import redirect, request, route, static_file, template
import database as DB
from database import DbConnection
from dateutil import parser
import export
import logging

log = logging.getLogger(__name__)


# =========================================
# EXPENSES FUNCTIONS
# =========================================


@route("/expenses")
def expenses():
    print("Customer ...")
    Data = DB.Expenses.get_all()
    return template("expenses.tpl", input=Data)


@route("/expense_add")
@route("/expense_add", method="POST")
@route("/expense_edit/<id>")
@route("/expense_edit/<id>", method="POST")
def expense_edit(id=None):
    # Check what kind of request has beeing made
    # We can either update or create a new entry
    # The decission is made besed on the ID
    if request.method == "POST":
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
            new = DB.Expenses(
                expense_id=Data.get("expense_id"),
                date=parser.parse(Data.get("date")),
                cost=Data.get("cost"),
                comment=Data.get("comment").encode("iso-8859-1"),
            )
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


@route("/expense_delete/<id>")
def expense_delete(id=None):
    print(f"Deleting expense with ID : {id}")
    DB.Expenses.delete(id)
    redirect("/expenses")
