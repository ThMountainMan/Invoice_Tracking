from bottle import redirect, request, route, static_file, template
import database as DB
from dateutil import parser
import export
import logging

log = logging.getLogger(__name__)


# =========================================
# Customer Related Functions
# =========================================


@route("/customers")
def customers():
    print("Customer ...")
    Data = DB.Customers.get_all()
    return template("customers.tpl", input=Data)


@route("/customer_add")
@route("/customer_add", method="POST")
@route("/customer_edit/<id>")
@route("/customer_edit/<id>", method="POST")
def customer_edit(id=None):
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
            DB.Customers.update(id, fData.process_update_data_Customer(Data))

        else:
            # We want to create a new DB entry
            new = DB.Customers(
                name=Data.get("name").encode("iso-8859-1"),
                contact=Data.get("contact").encode("iso-8859-1"),
                email=Data.get("email").encode("iso-8859-1"),
                phone=Data.get("phone"),
                street=Data.get("street").encode("iso-8859-1"),
                postcode=Data.get("postcode"),
                city=Data.get("city").encode("iso-8859-1"),
                country=Data.get("country").encode("iso-8859-1"),
            )
            # Send the new data to the Database
            DB.Customers.create(new)

        # get back to the overview
        redirect("/customers")

    # If the reueast was to edit an agency
    else:
        Data = DB.Customers.get(id) if id else None
        # Return the template with the DB data
        return template("customers_edit.tpl", customer=Data)


@route("/customer_delete/<id>")
def customer_delete(id=None):
    print(f"Deleting Customer with ID : {id}")
    DB.Customers.delete(id)
    redirect("/customers")
