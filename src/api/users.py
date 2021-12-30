import logging

from database import DbConnection, User
from flask import render_template, request
from server import app

from .authentification import Container

log = logging.getLogger(__name__)

# =========================================
# User Related Functions
# =========================================


@app.route("/users")
def users():
    container = Container()
    with DbConnection() as db:
        container.users = db.query("user", order_by="name")
    return render_template("users.html", **container)


@app.route("/users/edit", methods=["POST"])
def user_edit():
    try:
        with DbConnection() as db:
            container = Container()
            id = request.form.get("id")
            # Get the expense we want to edit
            if request.form["action"] == "edit":
                user = db.get("user", id) if id else User()
            # delete the selected expense
            elif request.form["action"] == "delete":
                db.delete("user", id)
                return {"success": True}
            # TODO: How doe we rollback properly ?
            elif request.form["action"] == "restore":
                db.rollback()
                return {"success": True}

            # Create or Update the Jobtypes
            user.name = request.form.get("name")
            user.email = request.form.get("email")
            user.user_role = request.form.get("user_role")
            user.account = request.form.get("name")

            if user.id:
                db.merge(user)
            else:
                db.add(user)
            return {"success": True}
    except Exception as e:
        # response.status = 400
        return str(e)
