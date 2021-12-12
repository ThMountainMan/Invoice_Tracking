from bottle import redirect, request, route, static_file, template
import database as DB
from dateutil import parser
import export
import logging

log = logging.getLogger(__name__)

# =========================================
# Jobtype Related Functions
# =========================================


@route("/jobtypes")
def jobtypes():
    print("Jobtypes ...")
    Data = DB.Jobtypes.get_all()

    for i in Data:
        print(i.name)

    return template("jobtypes.tpl", input=Data)


@route("/jobtype_add")
@route("/jobtype_add", method="POST")
@route("/jobtype_edit/<id>")
@route("/jobtype_edit/<id>", method="POST")
def jobtype_edit(id=None):
    # Check what kind of request has beeing made
    # We can either update or create a new entry
    # The decission is made besed on the ID
    if request.method == "POST":
        # Receive the HTML form data as dictionary
        Data = request.forms
        # Prepare the Data for DB input
        # decide if we want to update or to creates
        if id:
            # We want to update an existion entry
            # Send the new data to the Database
            DB.Jobtypes.update(id, fData.process_update_data_Jobtype(Data))

        else:
            # We want to create a new DB entry
            new = DB.Jobtypes(name=Data.get("name").encode("iso-8859-1"))
            # Send the new data to the Database
            DB.Jobtypes.create(new)

        # get back to the overview
        redirect("/jobtypes")

    # If the reueast was to edit an agency
    else:
        Data = DB.Jobtypes.get(id) if id else None
        # Return the template with the DB data
        return template("jobtypes_edit.tpl", jobtype=Data)


@route("/jobtype_delete/<id>")
def jobtype_delete(id=None):
    print(f"Deleting Jobtype with ID : {id}")
    DB.Jobtypes.delete(id)
    redirect("/jobtypes")
