from flask import Blueprint, render_template, request, jsonify
from app.models.college_models import College

college_bp = Blueprint("college", __name__, template_folder="templates")

@college_bp.route("/colleges")
def colleges():
    colleges_list = College.get_all_colleges()
    return render_template(
        "colleges.html",
        page_title="Colleges",
        colleges=colleges_list,
    )

@college_bp.route("/colleges/register", methods=["POST"])
def register_college():
    college_code = request.form.get("college_code", "").strip().upper()
    college_name = request.form.get("college_name", "").strip().title()

    if not college_code:
        return jsonify(success=False, field="college_code", message="College code is required."), 400
    if not college_name:
        return jsonify(success=False, field="college_name", message="College name is required."), 400

    success, message, field = College.register_college(college_code, college_name)

    if not success:
        if "already exists" in message.lower():
            return jsonify(success=False, field=field, message=message), 409
        return jsonify(success=False, field=field, message=message), 400

    return jsonify(success=True, message=message), 201

@college_bp.route("/colleges/edit", methods=["POST"])
def edit_college():
    college_code = request.form.get("college_code", "").strip().upper()
    college_name = request.form.get("college_name", "").strip().title()
    original_college_code = request.form.get("original_code", "").strip().upper()

    if not college_code:
        return jsonify(success=False, field="college_code", message="College code is required."), 400
    if not college_name:
        return jsonify(success=False, field="college_name", message="College name is required."), 400
    if not original_college_code:
        return jsonify(success=False, message="Original code is missing."), 400

    success, message, field = College.edit_college(college_code, college_name, original_college_code)

    if not success:
        if "already exists" in message.lower():
            return jsonify(success=False, field=field, message=message), 409
        return jsonify(success=False, field=field, message=message), 400

    return jsonify(success=True, message=message), 200

@college_bp.route("/colleges/delete", methods=["POST"])
def delete_college():
    college_code = request.form.get("college_code", "").strip().upper()

    if not college_code:
        return jsonify(success=False, message="College code is required to delete."), 400

    success, message = College.delete_college(college_code)

    if not success:
        return jsonify(success=False, message=message), 400

    return jsonify(success=True, message=message), 200