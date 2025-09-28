from flask import Blueprint, render_template
from app.dashboard import models

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    total_students = models.get_total_students()
    total_programs = models.get_total_programs()
    total_colleges = models.get_total_colleges()

    return render_template(
        "dashboard.html",
        page_title="Dashboard",
        total_students=total_students,
        total_programs=total_programs,
        total_colleges=total_colleges
    )
