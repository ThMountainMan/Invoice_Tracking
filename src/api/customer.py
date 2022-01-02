import logging

from database import Customers, DbConnection
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from .helper import Container

log = logging.getLogger(__name__)

setup_customers = Blueprint("customers", __name__)
# =========================================
# Customer Related Functions
# =========================================


@setup_customers.route("/customers")
@login_required
def customers():
    container = Container()
    with DbConnection() as db:
        data = db.query(
            "customers", filters={"user_id": current_user.id}, order_by="name"
        )
    return render_template("customers.html", input=data)


@setup_customers.route("/customers/edit", methods=["POST"])
@login_required
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
            customer.city = form_data.get("city")
            customer.country = form_data.get("country")
            customer.user_id = current_user.id

            if customer.id:
                db.merge(customer)
            else:
                db.add(customer)
            return {"success": True}
    except Exception as e:
        # response.status = 400
        return str(e)
