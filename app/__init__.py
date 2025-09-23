import os
import psycopg2
import config

from dotenv import load_dotenv
from flask import Flask, render_template, url_for, request, redirect, session

from app.database import get_db, close_db

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    from app.user import user_bp
    app.register_blueprint(user_bp)

    from app.college import college_bp
    app.register_blueprint(college_bp)

    @app.route("/")
    def home():
        return redirect(url_for("user.login"))

    @app.route("/dashboard")
    def dashboard():
        if "user" not in session:
            return redirect(url_for("user.login"))
        return render_template("dashboard.html", page_title="Dashboard")

    @app.route("/students")
    def students():
        n = 10
        students_data = [
            {
                "id_number": f"2022-000{i+1}",
                "first_name": "Mark",
                "last_name": "Otto",
                "program_code": "BSCS",
                "year_level": "3",
                "gender": "Male"
            }
            for i in range(n)
        ]
        return render_template("students.html", page_title="Students", students=students_data)

    @app.route("/programs")
    def programs():
        n = 10
        programs_data = [
            {
                "code": "BSCS",
                "name": "Bachelor of Science in Computer Science",
                "college_code": "CCS",
            }
            for i in range(n)
        ]
        return render_template("programs.html", page_title="Programs", programs=programs_data)

    @app.route("/colleges")
    def colleges():
        n = 10
        colleges_data = [
            {"code": "CCS", "name": "College of Computer Studies"}
            for i in range(n)
        ]
        return render_template("colleges.html", page_title="Colleges", colleges=colleges_data)
    
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()
    
    return app