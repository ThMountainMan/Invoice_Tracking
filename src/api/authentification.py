from database import DbConnection, NotExists, User
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    with DbConnection() as db:
        user = db.query("user", filters={"email": email})
        user = user[0] if user else None
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            # if the user doesn't exist or password is wrong, reload the page
            flash("Please check your login details and try again.")
            return redirect(url_for("auth.login"))
    login_user(user, remember=remember)
    # return redirect(url_for("invoices.invoices"))
    return redirect(request.args.get("next"))


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    with DbConnection() as db:
        user = db.query("user", filters={"email": email})
        user = user[0] if user else None
        if user:
            # If a user is found, try again
            flash("Email address already exists")
            return redirect(url_for("auth.signup"))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User()
        new_user.name = name
        new_user.email = email
        new_user.account = name
        new_user.password = generate_password_hash(password, method="sha256")

        # add the new user to the database
        db.add(new_user)

    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
