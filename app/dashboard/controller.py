from flask import Blueprint, render_template
from app.dashboard import models

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    total_students = models.get_total_students()
    total_programs = models.get_total_programs()
    total_colleges = models.get_total_colleges()
    top_programs = models.get_programs_with_most_students()
    programs_per_college = models.get_programs_per_college()

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
