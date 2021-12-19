import logging

from bottle import get, post, request, response, template
from database import DbConnection, PaymentDetails, PersonalDetails
import json

log = logging.getLogger(__name__)


# =========================================
# PERSONAL FUNCTIONS
# =========================================


@get("/personal")
def personal():
    with DbConnection() as db:
        data = db.query("personaldetails")
        payment_data = db.query("paymentdetails")

        payment_options = {0: "-"}
        payment_options.update({p.id: str(p) for p in payment_data})
        payment_options = json.dumps([[p] for i, p in payment_options.items()])

    return template("personal.tpl", input=data, payment_options=payment_options)


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
            personal.payment_id = form_data.get("payment_id")
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
        data = db.query("payment")
    return template("payment.tpl", input=data)


@post("/payment/edit")
def payment_edit():
    try:
        with DbConnection() as db:
            id = request.POST.get("id")
            # Get the expense we want to edit
            if request.POST["action"] == "edit":
                paymentdetails = (
                    db.get("paymentdetails", id) if id else PaymentDetails()
                )
            # delete the selected expense
            elif request.POST["action"] == "delete":
                db.delete("paymentdetails", id)
                return {"success": True}
            # TODO: How doe we rollback properly ?
            elif request.POST["action"] == "restore":
                db.rollback()
                return {"success": True}
            # Collect the Form Data
            form_data = request.forms
            # Create or Update the agency
            paymentdetails.label = form_data.get("label").encode("iso-8859-1")
            paymentdetails.name = form_data.get("name").encode("iso-8859-1")
            paymentdetails.bank = form_data.get("bank").encode("iso-8859-1")
            paymentdetails.IBAN = form_data.get("IBAN")
            paymentdetails.BIC = form_data.get("BIC")
            if personal.id:
                db.merge(personal)
            else:
                db.add(personal)
            return {"success": True}
    except Exception as e:
        response.status = 400
        return str(e)
