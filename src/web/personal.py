from bottle import redirect, request, route, static_file, template
import database as DB
from dateutil import parser
import export
import logging
from . import process_form_data as fData

log = logging.getLogger(__name__)


# =========================================
# PERSONAL FUNCTIONS
# =========================================


@route("/personal")
def personals():
    print("Customer ...")
    Data = DB.PersonalDetails.get_all()
    return template("personal.tpl", input=Data)


@route("/personal_add")
@route("/personal_add", method="POST")
@route("/personal_edit/<id>")
@route("/personal_edit/<id>", method="POST")
def personal_edit(id=None):
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
            DB.PersonalDetails.update(id, fData.process_update_data_PersonalData(Data))

        else:
            # We want to create a new DB entry
            new = DB.PersonalDetails(
                label=Data.get("label").encode("iso-8859-1"),
                name_company=Data.get("company_name").encode("iso-8859-1"),
                name=Data.get("name").encode("iso-8859-1"),
                street=Data.get("street").encode("iso-8859-1"),
                postcode=Data.get("postcode"),
                city=Data.get("city").encode("iso-8859-1"),
                mail=Data.get("mail"),
                phone=Data.get("phone"),
                payment_id=Data.get("payment_details"),
                taxnumber=Data.get("taxnumber"),
            )
            # Send the new data to the Database
            DB.PersonalDetails.create(new)

        # get back to the overview
        redirect("/personal")

    # If the reueast was to edit an agency
    else:
        Data = DB.PersonalDetails.get(id) if id else None
        payment = DB.PaymentDetails.get_all()
        # Return the template with the DB data
        return template("personal_edit.tpl", data=Data, payment=payment)


@route("/personal_delete/<id>")
def personal_delete(id=None):
    print(f"Deleting expense with ID : {id}")
    DB.PersonalDetails.delete(id)
    redirect("/personal")


# =========================================
# BANK DETAILS FUNCTIONS
# =========================================


@route("/payment")
def payments():
    print("Customer ...")
    Data = DB.PaymentDetails.get_all()
    return template("payment.tpl", input=Data)


@route("/payment_add")
@route("/payment_add", method="POST")
@route("/payment_edit/<id>")
@route("/payment_edit/<id>", method="POST")
def payment_edit(id=None):
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
            DB.PaymentDetails.update(id, fData.process_update_data_PaymentDetails(Data))

        else:
            # We want to create a new DB entry
            new = DB.PaymentDetails(
                label=Data.get("label").encode("iso-8859-1"),
                name=Data.get("name").encode("iso-8859-1"),
                bank=Data.get("bank").encode("iso-8859-1"),
                IBAN=Data.get("IBAN"),
                BIC=Data.get("BIC"),
            )
            # Send the new data to the Database
            DB.PaymentDetails.create(new)

        # get back to the overview
        redirect("/payment")

    # If the reueast was to edit an agency
    else:
        Data = DB.PaymentDetails.get(id) if id else None
        # Return the template with the DB data
        return template("payment_edit.tpl", data=Data)


@route("/payment_delete/<id>")
def payment_delete(id=None):
    print(f"Deleting Payment Details with ID : {id}")
    DB.PaymentDetails.delete(id)
    redirect("/payment")
