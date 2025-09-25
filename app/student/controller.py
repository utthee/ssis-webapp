from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import get_db


student_bp = Blueprint("student", __name__, template_folder="templates")

@student_bp.route("/students")
def students():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT code, name FROM programs ORDER BY code ASC")
    programs_data = cursor.fetchall()
    cursor.close()

    programs_list = [{"code": c[0], "name": c[1]} for c in programs_data]

    cursor = db.cursor()
    cursor.execute("SELECT * FROM students ORDER BY last_name")
    students_data = cursor.fetchall()
    cursor.close()

    students_list = [{"id_number": s[0], "first_name": s[1], "last_name": s[2], "gender": s[3], "year_level": s[4], "program_code": s[5]} for s in students_data]

    return render_template(
        "students.html",
        page_title="Students",
        students=students_list,
        programs=programs_list
    )


@student_bp.route("/students/register", methods=["POST"])
def register_student():
    id_number = request.form.get("id_number", "").strip()
    first_name = request.form.get("first_name", "").strip().title()
    last_name = request.form.get("last_name", "").strip().title()
    gender = request.form.get("gender", "").strip().title()
    year_level = request.form.get("year_level", "").strip()
    program_code = request.form.get("program_code", "").strip().upper()

    if not id_number or not first_name or not last_name or not gender or not year_level or not program_code:
        return {"success": False, "message": "All fields are required."}, 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (id_number, first_name, last_name, gender, year_level, program_code) VALUES (%s, %s, %s, %s, %s, %s)",
            (id_number, first_name, last_name, gender, year_level, program_code)
        )
        db.commit()
        return {"success": True, "message": f"Program {id_number} registered successfully!"}
    except Exception as e:
        db.rollback()
        return {"success": False, "message": str(e)}, 500
    finally:
        cursor.close()

@student_bp.route("/students/edit", methods=["POST"])
def edit_student():
    id_number = request.form.get("id_number", "").strip()
    first_name = request.form.get("first_name", "").strip().title()
    last_name = request.form.get("last_name", "").strip().title()
    gender = request.form.get("gender", "").strip().title()
    year_level = request.form.get("year_level", "").strip()
    program_code = request.form.get("program_code", "").strip().upper()
    original_id_number = request.form.get("original_id_number", "").strip().upper()

    if not original_id_number:
        return {"success": False, "message": "ID number missing"}, 400
    
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE students SET id_number=%s, first_name=%s, last_name=%s, gender=%s, year_level=%s, program_code=%s WHERE id_number=%s",
            (id_number, first_name, last_name, gender, year_level, program_code, original_id_number)
        )
        db.commit()
        return {"success": True, "message": "Student updated successfully"}
    except Exception as e:
        db.rollback()
        return {"success": False, "message": str(e)}, 500
    finally:
        cursor.close()

@student_bp.route("/students/delete", methods=["POST"])
def delete_student():
    id_number = request.form.get("id_number", "").strip()

    if not id_number:
        return {"success": False, "message": "ID Number is required to delete."}, 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE id_number = %s", (id_number,))
        db.commit()
        cursor.close()
        return {"success": True, "message": "Student deleted successfully!"}
    except Exception as e:
        db.rollback()
        cursor.close()
        return {"success": False, "message": str(e)}, 500