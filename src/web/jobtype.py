import logging

from bottle import get, post, request, response, template
from database import DbConnection, Jobtypes

from .authentification import Container

log = logging.getLogger(__name__)

# =========================================
# Jobtype Related Functions
# =========================================


@get("/jobtypes")
def expenses():
    container = Container()
    with DbConnection() as db:
        container.jobtypes = db.query(
            "jobtypes", filters={"user_id": container.current_user.id}, order_by="name"
        )
    return template("jobtypes.tpl", **container)


@post("/jobtypes/edit")
def expense_edit():
    try:
        with DbConnection() as db:
            container = Container()
            id = request.POST.get("id")
            # Get the expense we want to edit
            if request.POST["action"] == "edit":
                jobtype = db.get("jobtypes", id) if id else Jobtypes()
            # delete the selected expense
            elif request.POST["action"] == "delete":
                db.delete("jobtypes", id)
                return {"success": True}
            # TODO: How doe we rollback properly ?
            elif request.POST["action"] == "restore":
                db.rollback()
                return {"success": True}
            # Collect the Form Data
            form_data = request.forms
            # Create or Update the Jobtypes
            jobtype.name = form_data.get("name")

            if jobtype.id:
                db.merge(jobtype)
            else:
                db.add(jobtype)
            return {"success": True}
    except Exception as e:
        response.status = 400
        return str(e)
