import json
import logging

from bottle import get, post, request, response, template, put, redirect
from database import DbConnection, PaymentDetails, PersonalDetails

from .helper import Container

log = logging.getLogger(__name__)


# =========================================
# PERSONAL FUNCTIONS
# =========================================


@get("/personal")
def personal():
    with DbConnection() as db:
        container = Container()
        container.personaldetails = db.query("personaldetails")
        container.payment_data = db.query("paymentdetails")

        payment_options = {0: "-"}
        payment_options.update({p.id: str(p) for p in container.payment_data})
        container.payment_options = json.dumps(
            [[p] for i, p in payment_options.items()]
        )

    return template("personal.tpl", **container)


@post("/personal/edit")
def personal_edit():
    try:
        with DbConnection() as db:
            id = request.POST.get("id")
            # Get the expense we want to edit
            if request.POST["action"] == "edit":
                personal = db.get("personaldetails", id) if id else PersonalDetails()
            # delete the selected expense
            elif request.POST["action"] == "delete":
                db.delete("personaldetails", id)
                return {"success": True}
            # TODO: How doe we rollback properly ?
            elif request.POST["action"] == "restore":
                db.rollback()
                return {"success": True}
            # Collect the Form Data
            form_data = request.forms
            # Create or Update the agency
            personal.label = form_data.get("label").encode("iso-8859-1")
            personal.name = form_data.get("name").encode("iso-8859-1")
            personal.street = form_data.get("street").encode("iso-8859-1")
            personal.postcode = form_data.get("postcode")
            personal.city = form_data.get("city").encode("iso-8859-1")
            personal.mail = form_data.get("mail").encode("iso-8859-1")
            personal.phone = form_data.get("phone")
            personal.payment_id = int(form_data.get("payment_id"))
            personal.taxnumber = form_data.get("taxnumber")

            if personal.id:
                db.merge(personal)
            else:
                db.add(personal)
            return {"success": True}
    except Exception as e:
        response.status = 400
        return str(e)


# =========================================
# BANK DETAILS FUNCTIONS
# =========================================


@get("/payment")
def payment():
    with DbConnection() as db:
        data = db.query("paymentdetails")
    return template("payment.tpl", input=data)


@post("/payment_edit/<id>")
@post("/payment_edit")
def payment_edit(id=None):
    try:
        with DbConnection() as db:

            # delete the selected expense
            if "action" in request.POST.keys():
                if request.POST["action"] == "delete":
                    id = request.POST.get("id")
                    db.delete("paymentdetails", id)
                    return {"success": True}

            # get the caller id
            id = request.POST.get("id")
            # Get the expense we want to edit
            paymentdetails = db.get("paymentdetails", id) if id else PaymentDetails()

            # get the Form Data
            form_data = request.forms
            # Create or Update the agency
            paymentdetails.label = form_data.label.encode("iso-8859-1")
            paymentdetails.name = form_data.name.encode("iso-8859-1")
            paymentdetails.bank = form_data.bank.encode("iso-8859-1")
            paymentdetails.IBAN = form_data.IBAN
            paymentdetails.BIC = form_data.BIC
            if paymentdetails.id:
                db.merge(paymentdetails)
            else:
                db.add(paymentdetails)
            return {"success": True}

    except Exception as e:
        response.status = 400
        return str(e)
