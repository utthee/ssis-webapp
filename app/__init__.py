from flask import Flask, render_template, url_for

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def dashboard():
        return render_template("dashboard.html", page_title="Dashboard")

    @app.route("/login")
    def login():
        return render_template("login.html", page_title="Login")

    @app.route("/register")
    def register():
        return render_template("register.html", page_title="Register")

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

    return app