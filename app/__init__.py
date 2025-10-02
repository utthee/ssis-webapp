import config

from flask import Flask, render_template, url_for, request, redirect, session

from app.database import get_db, close_db

from app.college import college_bp
from app.program import program_bp
from app.student import student_bp
from app.dashboard import dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    from app.user import user_bp
    app.register_blueprint(user_bp)

    app.register_blueprint(college_bp)
    app.register_blueprint(program_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(dashboard_bp)
    
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()
    
    return app