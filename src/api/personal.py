import json
import logging

from database import DbConnection, PaymentDetails, PersonalDetails
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from .helper import Container

log = logging.getLogger(__name__)

setup_personal = Blueprint("personal", __name__)
# =========================================
# PERSONAL FUNCTIONS
# =========================================


@setup_personal.route("/personal")
@login_required
def personal():
    container = Container()
    with DbConnection() as db:
        container.personaldetails = db.query(
            "personaldetails", filters={"user_id": current_user.id}
        )
        container.payment_data = db.query("paymentdetails")

        payment_options = {0: "-"}
        payment_options.update({p.id: str(p) for p in container.payment_data})
        container.payment_options = json.dumps(
            [[p] for i, p in payment_options.items()]
        )

    return render_template("personal.html", **container)


@setup_personal.route("/personal/edit", methods=["POST"])
@login_required
def personal_edit():
    try:
        with DbConnection() as db:
            id = request.form.get("id")
            # Get the expense we want to edit
            if request.form["action"] == "edit":
                personal = db.get("personaldetails", id) if id else PersonalDetails()
            # delete the selected expense
            elif request.form["action"] == "delete":
                db.delete("personaldetails", id)
                return {"success": True}
            # TODO: How doe we rollback properly ?
            elif request.form["action"] == "restore":
                db.rollback()
                return {"success": True}
            # Collect the Form Data
            form_data = request.form
            # Create or Update the agency
            personal.label = form_data.get("label")
            personal.name = form_data.get("name")
            personal.street = form_data.get("street")
            personal.postcode = form_data.get("postcode")
            personal.city = form_data.get("city")
            personal.mail = form_data.get("mail")
            personal.phone = form_data.get("phone")
            personal.payment_id = int(form_data.get("payment_id"))
            personal.taxnumber = form_data.get("taxnumber")
            personal.user_id = current_user.id

            if personal.id:
                db.merge(personal)
            else:
                db.add(personal)
            return {"success": True}
    except Exception as e:
        # response.status = 400
        return str(e)


# =========================================
# BANK DETAILS FUNCTIONS
# =========================================


@setup_personal.route("/payment")
def payment():
    container = Container()
    with DbConnection() as db:
        container.paymentdetails = db.query(
            "paymentdetails",
            filters={"user_id": current_user.id},
            order_by="label",
        )
    return render_template("payment.html", **container)


@setup_personal.route("/payment_edit/<id>", methods=["POST"])
@setup_personal.route("/payment_edit", methods=["POST"])
def payment_edit(id=None):
    try:
        with DbConnection() as db:
            # get the caller id
            id = request.form.get("id")

            # delete the selected expense
            if "action" in request.form.keys():
                if request.form["action"] == "delete":
                    db.delete("paymentdetails", id)
                    return {"success": True}

            # Get the expense we want to edit
            paymentdetails = db.get("paymentdetails", id) if id else PaymentDetails()

            # get the Form Data
            form_data = request.form
            # Create or Update the agency
            paymentdetails.label = form_data.get("label")
            paymentdetails.name = form_data.get("name")
            paymentdetails.bank = form_data.get("bank")
            paymentdetails.IBAN = form_data.get("IBAN")
            paymentdetails.BIC = form_data.get("BIC")
            paymentdetails.user_id = current_user.id

            if paymentdetails.id:
                db.merge(paymentdetails)
            else:
                db.add(paymentdetails)
            return {"success": True}

    except Exception as e:
        # response.status = 400
        return str(e)
