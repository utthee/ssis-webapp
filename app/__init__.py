import config

from flask import Flask, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect

from app.database import close_db
from app.auth import login_required

# IMPORT ALL BLUEPRINTS
from app.user import user_bp
from app.college import college_bp
from app.program import program_bp
from app.student import student_bp
from app.dashboard import dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # INITIALIZE APP CROSS SITE REQUEST FORGERY (CSRF) PROTECTION
    CSRFProtect(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(college_bp)
    app.register_blueprint(program_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(dashboard_bp)

    @app.route("/")
    @login_required
    def index():
        if "user_id" in session:
            return redirect(url_for("dashboard.dashboard"))
        return redirect(url_for("user.login"))
    
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()
    
    return app