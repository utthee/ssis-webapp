from functools import wraps
from flask import session, redirect, url_for, flash, request 

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("user.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def already_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" in session:
            return redirect(url_for("dashboard.dashboard"))
        return f(*args, **kwargs)
    return decorated_function