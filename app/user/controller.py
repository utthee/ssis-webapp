from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from app.user.forms import SignupForm, LoginForm
from app.models import User
from psycopg2.extras import RealDictCursor
from app.database import get_db

user_bp = Blueprint("user", __name__, template_folder="../templates")


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data

            user = User.get_by_username(username)
            if user and user.check_password(password):
                session["user_id"] = user.id
                session["username"] = user.username
                return redirect(url_for("dashboard"))

            flash("Invalid username or password", "danger")
        else:
            flash("Please correct the errors in the form.", "danger")

    return render_template("login.html", form=form)


@user_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if request.method == "POST":
        if form.validate():
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


@user_bp.route("/users")
def users():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT id, username, email FROM users ORDER BY id ASC")
    users_data = cur.fetchall()
    
    for user in users_data:
        user["password"] = "••••••"

    cur.close() 

    return render_template("users.html", page_title="Users", users=users_data)
