from bottle import redirect, request, route, static_file, template
import database as DB
from dateutil import parser
import export
import logging

log = logging.getLogger(__name__)


# =========================================
# Agency Related Functions
# =========================================


@route("/agencys")
def agencys():
    print("Agencys ...")
    Data = DB.Agencys.get_all()
    return template("agencys.tpl", input=Data)


@route("/agency_add")
@route("/agency_add", method="POST")
@route("/agency_edit/<id>")
@route("/agency_edit/<id>", method="POST")
def agency_edit(id=None):
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
            DB.Agencys.update(id, fData.process_update_data_Agency(Data))

        else:
            # We want to create a new DB entry
            new = DB.Agencys(
                name=Data.get("name").encode("iso-8859-1"),
                percentage=Data.get("percentage"),
            )
            DB.Agencys.create(new)

        # get back to the overview
        redirect("/agencys")

    # If the reueast was to edit an agency
    else:
        Data = DB.Agencys.get(id) if id else None
        # Return the template with the DB data
        return template("agencys_edit.tpl", agency=Data)


@route("/agency_delete/<id>")
def agency_delete(id=None):
    print(f"Deleting Agency with ID : {id}")
    try:
        DB.Agencys.delete(id)
    except Exception:
        pass
    finally:
        redirect("/agencys")
