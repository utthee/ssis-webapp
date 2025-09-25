import os
import psycopg2
import config

from dotenv import load_dotenv
from flask import Flask, render_template, url_for, request, redirect, session

from app.database import get_db, close_db

from app.college import college_bp
from app.program import program_bp
from app.student import student_bp
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    from app.user import user_bp
    app.register_blueprint(user_bp)

    app.register_blueprint(college_bp)
    app.register_blueprint(program_bp)
    app.register_blueprint(student_bp)

    @app.route("/")
    def home():
        return redirect(url_for("user.login"))

    @app.route("/dashboard")
    def dashboard():
        if "user_id" not in session:
            return redirect(url_for("user.login"))
        return render_template("dashboard.html", page_title="Dashboard")
    
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()
    
    return app