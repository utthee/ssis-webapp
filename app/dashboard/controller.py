from flask import Blueprint, render_template, redirect, url_for
from app.models.dashboard import Dashboard
from app.auth import login_required

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    total_students = Dashboard.get_total_students()
    total_programs = Dashboard.get_total_programs()
    total_colleges = Dashboard.get_total_colleges()
    top_programs = Dashboard.get_programs_with_most_students()
    programs_per_college = Dashboard.get_programs_per_college()

    # ENUMERATE TOP RANKING PROGRAMS
    top_programs = list(enumerate(top_programs, start=1))

    # ENUMERATE COLLEGES WITH THE MOST NUMBER OF PROGRAMS
    programs_per_college = list(enumerate(programs_per_college, start=1))

    return render_template(
        "dashboard.html",
        page_title="Dashboard",
        total_students=total_students,
        total_programs=total_programs,
        total_colleges=total_colleges,
        top_programs=top_programs,
        programs_per_college=programs_per_college
    )
