from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html", page_title="Dashboard")

# Students page
@app.route("/students")
def students():
    # DUMMY STUDENT DATA
    n = 10
    students = [
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
    return render_template("students.html",  page_title="Students", students=students)

# Programs page
@app.route("/programs")
def programs():
    # DUMMY PROGRAM DATA
    n = 10
    programs = [
        {
            "code": "BSCS",
            "name": "Bachelor of Science in Computer Science",
            "college_code": "CCS",
        }
        for i in range(n)
    ]
    return render_template("programs.html",  page_title="Programs", programs=programs)

# Colleges page
@app.route("/colleges")
def colleges():
    # DUMMY COLLEGE DATA
    n = 10
    colleges = [
        {
            "code": "CCS",
            "name": "College of Computer Studies"
        }
        for i in range(n)
    ]
    return render_template("colleges.html",  page_title="Colleges", colleges=colleges)

if __name__ == "__main__":
    app.run(debug=True)