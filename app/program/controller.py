from flask import Blueprint, render_template, request, jsonify
from app.program.models import Program

program_bp = Blueprint("program", __name__, template_folder="templates")

@program_bp.route("/programs")
def programs():
    colleges_list = Program.get_all_colleges()
    programs_list = Program.get_all_programs()

    return render_template(
        "programs.html",
        page_title="Programs",
        programs=programs_list,
        colleges=colleges_list
    )

@program_bp.route("/programs/register", methods=["POST"])
def register_program():
    program_code = request.form.get("program_code", "").strip().upper()
    program_name = request.form.get("program_name", "").strip().title()
    college_code = request.form.get("college_code", "").strip().upper()

    if not program_code:
        return jsonify(success=False, field="program_code", message="Program code is required."), 400
    if not program_name:
        return jsonify(success=False, field="progam_name", message="Program name is required."), 400
    if not college_code:
        return jsonify(success=False, field="college_code", message="College code is required."), 400
    
    success, message = Program.register_program(program_code, program_name, college_code)

    if not success:
        return jsonify(success=False, field="code", message=message), 400

    return jsonify(success=True, message=message), 200

@program_bp.route("/programs/edit", methods=["POST"])
def edit_program():
    program_code = request.form.get("program_code", "").strip().upper()
    program_name = request.form.get("program_name", "").strip().title()
    college_code = request.form.get("college_code", "").strip().upper()
    original_program_code = request.form.get("original_program_code", "").strip().upper()

    if not program_code:
        return jsonify(success=False, field="code", message="Program code is required."), 400
    if not program_name:
        return jsonify(success=False, field="name", message="Program name is required."), 400
    if not college_code:
        return jsonify(success=False, field="college_code", message="College code is required."), 400
    if not original_program_code:
        return jsonify(success=False, message="Original code is missing."), 400
    
    success, message = Program.edit_program(program_code, program_name, college_code, original_program_code)

    if not success:
        return jsonify(success=False, field="code", message=message), 400

    return jsonify(success=True, message=message), 200

@program_bp.route("/programs/delete", methods=["POST"])
def delete_program():
    code = request.form.get("code", "").strip().upper()

    if not code:
        return jsonify(success=False, message="Program code is required to delete."), 400
    
    success, message = Program.delete_program(code)

    if not success:
        return jsonify(success=False, message=message), 400

    return jsonify(success=True, message=message), 200
