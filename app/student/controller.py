from flask import Blueprint, render_template, request, jsonify
from app.models.students import Student
from app.auth import login_required
from app.storage import supabase_storage
from config import DEFAULT_PROFILE_URL

student_bp = Blueprint("student", __name__, template_folder="templates")

@student_bp.route("/students")
@login_required
def students():
    filter_year_level = request.args.get("year_level")
    filter_gender = request.args.get("gender")
    filter_program_code = request.args.get("program_code")

    programs_list = Student.get_all_programs()
    students_list = Student.get_all_students(filter_year_level, filter_gender, filter_program_code)
    genders_list = Student.get_all_genders()
    year_levels_list = Student.get_all_year_levels()

    return render_template(
        "students.html",
        page_title="Students",
        students=students_list,
        programs=programs_list,
        genders=genders_list,
        year_levels=year_levels_list,
        default_profile_url=DEFAULT_PROFILE_URL,
        current_filters={
            "year_level": filter_year_level,
            "gender": filter_gender,
            "program_code": filter_program_code
        }
    )


@student_bp.route("/students/register", methods=["POST"])
@login_required
def register_student():
    try:
        id_number = request.form.get("id_number", "").strip()
        first_name = request.form.get("first_name", "").strip().title()
        last_name = request.form.get("last_name", "").strip().title()
        gender = request.form.get("gender", "").strip().title()
        year_level = request.form.get("year_level", "").strip()
        program_code = request.form.get("program_code", "").strip().upper()
        student_photo = request.files.get("student_photo")

        if not id_number:
            return jsonify(success=False, field="id_number", message="ID number is required."), 400
        if not first_name:
            return jsonify(success=False, field="first_name", message="First name is required."), 400
        if not last_name:
            return jsonify(success=False, field="last_name", message="Last name is required."), 400
        if not gender:
            return jsonify(success=False, field="gender", message="Gender is required."), 400
        if not year_level:
            return jsonify(success=False, field="year_level", message="Year level is required."), 400
        if not program_code:
            return jsonify(success=False, field="program_code", message="Program code is required."), 400
        
        if Student.check_existing_id_number(id_number):
            return jsonify(success=False, field="id_number", message="The ID Number you just entered already exists. Please enter a different ID Number."), 409
        
        photo_url = DEFAULT_PROFILE_URL
        photo_uploaded = False
        
        if student_photo and student_photo.filename:
            try:
                photo_url = supabase_storage.upload_student_photo(student_photo, id_number)
                photo_uploaded = True
            except ValueError as e:
                return jsonify(success=False, field="student_photo", message=str(e)), 400
            except Exception as e:
                return jsonify(success=False, field="student_photo", message=f"Failed to upload photo: {str(e)}"), 500
        
        success, message, field = Student.register_student(
            id_number, first_name, last_name, gender, year_level, program_code, photo_url
        )

        if not success:
            if photo_uploaded:
                supabase_storage.delete_student_photo(id_number)
            
            if "already exists" in message.lower():
                return jsonify(success=False, field=field, message=message), 409
            return jsonify(success=False, field=field, message=message), 400

        return jsonify(success=True, message=message), 201
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify(success=False, message=f"Server error: {str(e)}"), 500


@student_bp.route("/students/edit", methods=["POST"])
@login_required
def edit_student():
    try:
        id_number = request.form.get("id_number", "").strip()
        first_name = request.form.get("first_name", "").strip().title()
        last_name = request.form.get("last_name", "").strip().title()
        gender = request.form.get("gender", "").strip().title()
        year_level = request.form.get("year_level", "").strip()
        program_code = request.form.get("program_code", "").strip().upper()
        original_id_number = request.form.get("original_id_number", "")
        remove_photo = request.form.get("remove_photo", "false") == "true"
        student_photo = request.files.get("student_photo")
        
        photo_url = "KEEP_EXISTING"
        photo_was_updated = False

        if not id_number:
            return jsonify(success=False, field="id_number", message="ID number is required."), 400
        if not first_name:
            return jsonify(success=False, field="first_name", message="First name is required."), 400
        if not last_name:
            return jsonify(success=False, field="last_name", message="Last name is required."), 400
        if not gender:
            return jsonify(success=False, field="gender", message="Gender is required."), 400
        if not year_level:
            return jsonify(success=False, field="year_level", message="Year level is required."), 400
        if not program_code:
            return jsonify(success=False, field="program_code", message="Program code is required."), 400
        
        if id_number != original_id_number:
            if Student.check_existing_id_number(id_number, original_id_number):
                return jsonify(success=False, field="id_number", message="The ID Number you just entered already exists. Please enter a different ID Number."), 409
        
        if remove_photo:
            try:
                supabase_storage.delete_student_photo(original_id_number)
                photo_url = DEFAULT_PROFILE_URL
                photo_was_updated = True
            except Exception as e:
                return jsonify(success=False, field="student_photo", message=f"Failed to remove photo: {str(e)}"), 500
        
        elif student_photo and student_photo.filename:
            try:
                photo_url = supabase_storage.update_student_photo(student_photo, id_number, original_id_number)
                photo_was_updated = True
            except ValueError as e:
                return jsonify(success=False, field="student_photo", message=str(e)), 400
            except Exception as e:
                return jsonify(success=False, field="student_photo", message=str(e)), 500
        
        elif id_number != original_id_number:
            try:
                photo_url = supabase_storage.rename_student_photo(original_id_number, id_number)
                if photo_url != "KEEP_EXISTING":
                    photo_was_updated = True
            except Exception as e:
                return jsonify(success=False, field="student_photo", message=f"Failed to rename photo: {str(e)}"), 500
        
        success, message, field = Student.edit_student(
            id_number, first_name, last_name, gender, year_level, program_code, original_id_number, photo_url
        )

        if not success and message == "No changes detected." and photo_was_updated:
            return jsonify(success=True, message="Student photo updated successfully."), 200

        if not success:
            if "already exists" in message.lower():
                return jsonify(success=False, field=field, message=message), 409
            return jsonify(success=False, field=field, message=message), 400

        return jsonify(success=True, message=message), 200
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify(success=False, message=f"Server error: {str(e)}"), 500


@student_bp.route("/students/delete", methods=["POST"])
@login_required
def delete_student():
    id_number = request.form.get("id_number", "").strip()

    if not id_number:
        return jsonify(success=False, field="id_number", message="ID number is required."), 400

    supabase_storage.delete_student_photo(id_number)
    
    success, message = Student.delete_student(id_number)

    if not success:
        return jsonify(success=False, message=message), 400

    return jsonify(success=True, message=message), 200