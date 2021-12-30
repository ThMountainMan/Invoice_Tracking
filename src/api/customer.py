import logging

from database import Customers, DbConnection
from flask import render_template, request
from server import app

from .authentification import Container

log = logging.getLogger(__name__)


# =========================================
# Customer Related Functions
# =========================================


@app.route("/customers")
def customers():
    container = Container()
    with DbConnection() as db:
        data = db.query(
            "customers", filters={"user_id": container.current_user.id}, order_by="name"
        )
    return render_template("customers.html", input=data)


@app.route("/customers/edit", methods=["POST"])
def customer_edit():
    try:
        with DbConnection() as db:
            id = request.form.get("id")
            # Get the expense we want to edit
            if request.form["action"] == "edit":
                customer = db.get("customers", id) if id else Customers()
            # delete the selected expense
            elif request.form["action"] == "delete":
                db.delete("customers", id)
                return {"success": True}
            # TODO: How doe we rollback properly ?
            elif request.form["action"] == "restore":
                db.rollback()
                return {"success": True}
            # Collect the Form Data
            form_data = request.form
            # Create or Update the agency
            customer.name = form_data.get("name")
            customer.contact = form_data.get("contact")
            customer.email = form_data.get("email")
            customer.phone = form_data.get("phone")
            customer.street = form_data.get("street")
            customer.formcode = form_data.get("formcode")
            customer.city = form_data.get("city")
            customer.country = form_data.get("country")

            if customer.id:
                db.merge(customer)
            else:
                db.add(customer)
            return {"success": True}
    except Exception as e:
        # response.status = 400
        return str(e)
