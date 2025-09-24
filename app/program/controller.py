from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import get_db

program_bp = Blueprint("program", __name__, template_folder="templates")

@program_bp.route("/programs")
def programs():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT code, name FROM colleges ORDER BY code ASC")
    colleges_data = cursor.fetchall()
    cursor.close()

    colleges_list = [{"code": c[0], "name": c[1]} for c in colleges_data]

    cursor = db.cursor()
    cursor.execute("SELECT * FROM programs ORDER BY code ASC")
    programs_data = cursor.fetchall()
    cursor.close()

    programs_list = [{"code": p[0], "name": p[1], "college_code": p[2]} for p in programs_data]

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

    if not program_code or not program_name or not college_code:
        return {"success": False, "message": "All fields are required."}, 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO programs (code, name, college_code) VALUES (%s, %s, %s)",
            (program_code, program_name, college_code)
        )
        db.commit()
        return {"success": True, "message": f"Program {program_name} registered successfully!"}
    except Exception as e:
        db.rollback()
        return {"success": False, "message": str(e)}, 500
    finally:
        cursor.close()

@program_bp.route("/programs/edit", methods=["POST"])
def edit_program():
    program_code = request.form.get("program_code", "").strip().upper()
    program_name = request.form.get("program_name", "").strip().title()
    college_code = request.form.get("college_code", "").strip().upper()
    original_code = request.form.get("original_program_code", "").strip().upper()

    if not original_code:
        return {"success": False, "message": "Original program code missing"}, 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE programs SET code=%s, name=%s, college_code=%s WHERE code=%s",
            (program_code, program_name, college_code, original_code)
        )
        db.commit()
        return {"success": True, "message": "Program updated successfully"}
    except Exception as e:
        db.rollback()
        return {"success": False, "message": str(e)}, 500
    finally:
        cursor.close()

@program_bp.route("/programs/delete", methods=["POST"])
def delete_program():
    code = request.form.get("code", "").strip().upper()

    if not code:
        return {"success": False, "message": "Program code is required to delete."}, 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM programs WHERE code = %s", (code,))
        db.commit()
        cursor.close()
        return {"success": True, "message": "Program deleted successfully!"}
    except Exception as e:
        db.rollback()
        cursor.close()
        return {"success": False, "message": str(e)}, 500