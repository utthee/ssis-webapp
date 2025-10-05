import config

from flask import Flask

from app.database import close_db

# IMPORT ALL BLUEPRINTS
from app.user import user_bp
from app.college import college_bp
from app.program import program_bp
from app.student import student_bp
from app.dashboard import dashboard_bp
from flask_wtf.csrf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    # CSRFProtect(app)

    app.register_blueprint(user_bp)

    app.register_blueprint(college_bp)
    app.register_blueprint(program_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(dashboard_bp)
    
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()
    
    return app