import logging

from database import DbConnection, Jobtypes
from flask import render_template, request
from server import app

from .authentification import Container

log = logging.getLogger(__name__)

# =========================================
# Jobtype Related Functions
# =========================================


@app.route("/jobtypes")
def jobtypes():
    container = Container()
    with DbConnection() as db:
        container.jobtypes = db.query(
            "jobtypes", filters={"user_id": container.current_user.id}, order_by="name"
        )
    return render_template("jobtypes.html", **container)


@app.route("/jobtypes/edit", methods=["POST"])
def jobtype_edit():
    try:
        with DbConnection() as db:
            container = Container()
            id = request.form.get("id")
            # Get the expense we want to edit
            if request.form["action"] == "edit":
                jobtype = db.get("jobtypes", id) if id else Jobtypes()
            # delete the selected expense
            elif request.form["action"] == "delete":
                db.delete("jobtypes", id)
                return {"success": True}
            # TODO: How doe we rollback properly ?
            elif request.form["action"] == "restore":
                db.rollback()
                return {"success": True}
            # Collect the Form Data
            form_data = request.form
            # Create or Update the Jobtypes
            jobtype.name = form_data.get("name")

            if jobtype.id:
                db.merge(jobtype)
            else:
                db.add(jobtype)
            return {"success": True}
    except Exception as e:
        # response.status = 400
        return str(e)
