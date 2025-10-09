from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from app.user.forms import SignupForm, LoginForm
from app.models.user_models import User

user_bp = Blueprint("user", __name__, template_folder="../templates")

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.get_by_username(username)
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash(f"Welcome, {user.username}!", "login")
            return redirect(url_for("dashboard.dashboard"))

        form.password.errors.append("Invalid username or password")

    return render_template("login.html", form=form)

@user_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if request.method == "POST":
        if form.validate_on_submit():
            User.create(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
            flash(f"Account created for {form.username.data}", "success")
            return redirect(url_for("user.login"))
        else:
            flash("Please correct the errors in the form.", "danger")

    return render_template("signup.html", form=form)


@user_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("user.login"))
