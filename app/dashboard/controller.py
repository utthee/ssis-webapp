from flask import Blueprint, render_template, redirect, url_for
from app.dashboard.models import Dashboard

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    total_students = Dashboard.get_total_students()
    total_programs = Dashboard.get_total_programs()
    total_colleges = Dashboard.get_total_colleges()
    top_programs = Dashboard.get_programs_with_most_students()
    programs_per_college = Dashboard.get_programs_per_college()

    # ENUMERATE TOP RANKING PROGRAMS
    top_programs = list(enumerate(top_programs, start=1))

    # LABELS AND DATA USED FOR THE DONUT CHART
    labels = [row[0] for row in programs_per_college]
    data = [row[1] for row in programs_per_college]

    return render_template(
        "dashboard.html",
        page_title="Dashboard",
        total_students=total_students,
        total_programs=total_programs,
        total_colleges=total_colleges,
        top_programs=top_programs,
        labels=labels,
        data=data
    )

@dashboard_bp.route("/")
def login():
    return redirect(url_for("user.login"))