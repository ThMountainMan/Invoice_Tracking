import logging

from database import DbConnection, Jobtypes
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required


from .helper import Container

log = logging.getLogger(__name__)

setup_jobtypes = Blueprint("jobtypes", __name__)
# =========================================
# Jobtype Related Functions
# =========================================


@setup_jobtypes.route("/jobtypes")
@login_required
def jobtypes():
    container = Container()
    with DbConnection() as db:
        container.jobtypes = db.query(
            "jobtypes", filters={"user_id": current_user.id}, order_by="name"
        )
    return render_template("jobtypes.html", **container)


@setup_jobtypes.route("/jobtypes/edit", methods=["POST"])
@login_required
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
            jobtype.user_id = current_user.id

            if jobtype.id:
                db.merge(jobtype)
            else:
                db.add(jobtype)
            return {"success": True}
    except Exception as e:
        # response.status = 400
        return str(e)
