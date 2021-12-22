import logging

from bottle import get, post, redirect, request, response, route, template
from database import Customers, DbConnection

log = logging.getLogger(__name__)


# =========================================
# Customer Related Functions
# =========================================


@get("/customers")
def customers():
    with DbConnection() as db:
        data = db.query("customers", order_by="name")
    return template("customers.tpl", input=data)


@post("/customers/edit")
def expense_edit():
    try:
        with DbConnection() as db:
            id = request.POST.get("id")
            # Get the expense we want to edit
            if request.POST["action"] == "edit":
                customer = db.get("customers", id) if id else Customers()
            # delete the selected expense
            elif request.POST["action"] == "delete":
                db.delete("customers", id)
                return {"success": True}
            # TODO: How doe we rollback properly ?
            elif request.POST["action"] == "restore":
                db.rollback()
                return {"success": True}
            # Collect the Form Data
            form_data = request.forms
            # Create or Update the agency
            customer.name = form_data.get("name").encode("iso-8859-1")
            customer.contact = form_data.get("contact").encode("iso-8859-1")
            customer.email = form_data.get("email").encode("iso-8859-1")
            customer.phone = form_data.get("phone")
            customer.street = form_data.get("street").encode("iso-8859-1")
            customer.postcode = form_data.get("postcode")
            customer.city = form_data.get("city").encode("iso-8859-1")
            customer.country = form_data.get("country").encode("iso-8859-1")

            if customer.id:
                db.merge(customer)
            else:
                db.add(customer)
            return {"success": True}
    except Exception as e:
        response.status = 400
        return str(e)
