from flask import Blueprint, render_template, request, redirect, url_for, session

user_bp = Blueprint("user", __name__, template_folder="../templates")

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "123":
            session["user"] = username
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@user_bp.route("/signup", methods=["GET", "POST"])
def signup():
    # later: handle POST to create a new user
    return render_template("signup.html")


@user_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("user.login"))


@user_bp.route("/users")
def users():
    n = 10
    users_data = [
        {"id": i + 1, "username": f"user{i+1}",
         "email": f"user{i+1}@example.com",
         "password": "••••••"}
        for i in range(n)
    ]
    return render_template("users.html", page_title="Users", users=users_data)
