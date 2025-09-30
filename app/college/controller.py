from flask import Blueprint, render_template, request, jsonify
from app.college import models

college_bp = Blueprint("college", __name__, template_folder="templates")

@college_bp.route("/colleges")
def colleges():
    colleges_list = models.get_all_colleges()
    return render_template(
        "colleges.html",
        page_title="Colleges",
        colleges=colleges_list,
    )

@college_bp.route("/colleges/register", methods=["POST"])
def register_college():
    code = request.form.get("code", "").strip().upper()
    name = request.form.get("name", "").strip().title()

    if not code:
        return jsonify(success=False, field="code", message="College code is required."), 400
    if not name:
        return jsonify(success=False, field="name", message="College name is required."), 400

    success, message = models.register_college(code, name)

    if not success:
        return jsonify(success=False, field="code", message=message), 400

    return jsonify(success=True, message=message), 200

@college_bp.route("/colleges/edit", methods=["POST"])
def edit_college():
    code = request.form.get("code", "").strip().upper()
    name = request.form.get("name", "").strip().title()
    original_code = request.form.get("original_code", "").strip().upper()

    if not code:
        return jsonify(success=False, field="code", message="College code is required."), 400
    if not name:
        return jsonify(success=False, field="name", message="College name is required."), 400
    if not original_code:
        return jsonify(success=False, message="Original code is missing."), 400

    success, message = models.edit_college(original_code, code, name)

    if not success:
        return jsonify(success=False, field="code", message=message), 400

    return jsonify(success=True, message=message), 200

@college_bp.route("/colleges/delete", methods=["POST"])
def delete_college():
    code = request.form.get("code", "").strip().upper()

    if not code:
        return jsonify(success=False, message="College code is required to delete."), 400

    success, message = models.delete_college(code)

    if not success:
        return jsonify(success=False, message=message), 400

    return jsonify(success=True, message=message), 200