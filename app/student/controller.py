from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.student import models
from app.database import get_db

student_bp = Blueprint("student", __name__, template_folder="templates")

@student_bp.route("/students")
def students():
    programs_list = models.get_all_programs()
    students_list = models.get_all_students()

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

    if not id_number:
        return jsonify(success=True, field="id_number", message="ID number is required."), 400
    if not first_name:
        return jsonify(success=True, field="first_name", message="First name is required."), 400
    if not last_name:
        return jsonify(success=True, field="last_name", message="Last name is required."), 400
    if not gender:
        return jsonify(success=True, field="gender", message="Gender is required."), 400
    if not year_level:
        return jsonify(success=True, field="year_level", message="Year level is required."), 400
    if not program_code:
        return jsonify(success=False, field="program_code", message="Program code is required."), 400
    
    success,message = models.register_student(id_number, first_name, last_name, gender, year_level, program_code)

    if not success:
        return jsonify(success=False, field="code", message=message), 400

    return jsonify(success=True, message=message), 200


@student_bp.route("/students/edit", methods=["POST"])
def edit_student():
    id_number = request.form.get("id_number", "").strip()
    first_name = request.form.get("first_name", "").strip().title()
    last_name = request.form.get("last_name", "").strip().title()
    gender = request.form.get("gender", "").strip().title()
    year_level = request.form.get("year_level", "").strip()
    program_code = request.form.get("program_code", "").strip().upper()
    original_id_number = request.form.get("original_id_number", "")

    if not id_number:
        return jsonify(success=True, field="id_number", message="ID number is required."), 400
    if not first_name:
        return jsonify(success=True, field="first_name", message="First name is required."), 400
    if not last_name:
        return jsonify(success=True, field="last_name", message="Last name is required."), 400
    if not gender:
        return jsonify(success=True, field="gender", message="Gender is required."), 400
    if not year_level:
        return jsonify(success=True, field="year_level", message="Year level is required."), 400
    if not program_code:
        return jsonify(success=False, field="program_code", message="Program code is required."), 400
    
    success,message = models.edit_student(id_number, first_name, last_name, gender, year_level, program_code, original_id_number)

    if not success:
        return jsonify(success=False, field="code", message=message), 400

    return jsonify(success=True, message=message), 200


@student_bp.route("/students/delete", methods=["POST"])
def delete_student():
    id_number = request.form.get("id_number", "").strip()

    if not id_number:
        return jsonify(success=True, field="id_number", message="ID number is required."), 400

    success,message = models.delete_student(id_number)

    if not success:
        return jsonify(success=False, message=message), 400

    return jsonify(success=True, message=message), 200