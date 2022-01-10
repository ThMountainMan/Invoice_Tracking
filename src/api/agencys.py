import logging

from database import Agencys, DbConnection
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from .helper import Container

log = logging.getLogger(__name__)

setup_agencys = Blueprint("agencys", __name__)

# =========================================
# Agency Related Functions
# =========================================


@setup_agencys.route("/agencys")
@login_required
def agencys():
    container = Container()
    with DbConnection() as db:

        container.agencys = db.query(
            "agencys", filters={"user_id": current_user.id}, order_by="name"
        )
    return render_template("agencys.html", **container)


@setup_agencys.route("/agencys/edit", methods=["POST"])
@login_required
def agency_edit():
    try:
        with DbConnection() as db:
            id = request.form.get("id")
            # Get the expense we want to edit
            if request.form["action"] == "edit":
                agency = db.get("agencys", id) if id else Agencys()
            # delete the selected expense
            elif request.form["action"] == "delete":
                db.delete("agencys", id)
                return {"success": True}
            # TODO: How doe we rollback properly ?
            elif request.form["action"] == "restore":
                db.rollback()
                return {"success": True}
            # Collect the Form Data
            form_data = request.form
            # Create or Update the agency
            agency.name = form_data.get("name")
            agency.percentage = form_data.get("percentage")
            agency.user_id = current_user.id

            if agency.id:
                db.merge(agency)
            else:
                db.add(agency)
            return {"success": True}
    except Exception as e:
        # response.status = 400
        return str(e)
