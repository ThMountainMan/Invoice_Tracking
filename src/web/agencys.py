import logging

from bottle import get, post, request, response, template
from database import Agencys, DbConnection

from .authentification import Container

log = logging.getLogger(__name__)


# =========================================
# Agency Related Functions
# =========================================


@get("/agencys")
def expenses():
    container = Container()
    with DbConnection() as db:

        container.agencys = db.query(
            "agencys", filters={"user_id": container.current_user.id}, order_by="name"
        )
    return template("agencys.tpl", **container)


@post("/agencys/edit")
def expense_edit():
    try:
        with DbConnection() as db:
            id = request.POST.get("id")
            # Get the expense we want to edit
            if request.POST["action"] == "edit":
                agency = db.get("agencys", id) if id else Agencys()
            # delete the selected expense
            elif request.POST["action"] == "delete":
                db.delete("agencys", id)
                return {"success": True}
            # TODO: How doe we rollback properly ?
            elif request.POST["action"] == "restore":
                db.rollback()
                return {"success": True}
            # Collect the Form Data
            form_data = request.forms
            # Create or Update the agency
            agency.name = form_data.get("name")
            agency.percentage = form_data.get("percentage")

            if agency.id:
                db.merge(agency)
            else:
                db.add(agency)
            return {"success": True}
    except Exception as e:
        response.status = 400
        return str(e)
