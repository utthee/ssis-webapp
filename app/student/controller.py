from flask import Blueprint, render_template, request, jsonify
from app.models.students import Student
from app.auth import login_required
from werkzeug.utils import secure_filename
import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_DB_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

student_bp = Blueprint("student", __name__, template_folder="templates")

@student_bp.route("/students")
@login_required
def students():
    programs_list = Student.get_all_programs()
    students_list = Student.get_all_students()

    return render_template(
        "students.html",
        page_title="Students",
        students=students_list,
        programs=programs_list
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

        photo = request.files.get("student_photo")
        
        photo_url = "https://kqcerjyubrhcakxebzwy.supabase.co/storage/v1/object/public/ssis-student-photos/default-profile.png"

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
        
        file_path = None
        
        if photo and photo.filename:
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
            filename = secure_filename(photo.filename)
            file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
            
            if file_ext not in allowed_extensions:
                return jsonify(success=False, field="student_photo", message="Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed."), 400
            
            try:
                storage_filename = f"{id_number}.{file_ext}"
                file_path = f"students/{storage_filename}"
                
                file_content = photo.read()
                
                response = supabase.storage.from_("ssis-student-photos").upload(
                    file_path,
                    file_content,
                    file_options={"content-type": photo.content_type}
                )
                
                photo_url = supabase.storage.from_("ssis-student-photos").get_public_url(file_path)
                
            except Exception as e:
                print(f"Upload error: {str(e)}")
                import traceback
                traceback.print_exc()
                return jsonify(success=False, field="student_photo", message=f"Failed to upload photo: {str(e)}"), 500
        
        success, message, field = Student.register_student(
            id_number, first_name, last_name, gender, year_level, program_code, photo_url
        )

        if not success:
            if photo and photo.filename and file_path:
                try:
                    supabase.storage.from_("ssis-student-photos").remove([file_path])
                except:
                    pass
            
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
    id_number = request.form.get("id_number", "").strip()
    first_name = request.form.get("first_name", "").strip().title()
    last_name = request.form.get("last_name", "").strip().title()
    gender = request.form.get("gender", "").strip().title()
    year_level = request.form.get("year_level", "").strip()
    program_code = request.form.get("program_code", "").strip().upper()
    original_id_number = request.form.get("original_id_number", "")
    
    photo = request.files.get("student_photo")
    photo_url = None

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
    
    if photo and photo.filename:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        filename = secure_filename(photo.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if file_ext not in allowed_extensions:
            return jsonify(success=False, field="student_photo", message="Invalid file type."), 400
        
        try:
            storage_filename = f"{id_number}.{file_ext}"
            file_path = f"students/{storage_filename}"
            file_content = photo.read()
            
            if original_id_number != id_number:
                try:
                    old_files = supabase.storage.from_("ssis-student-photos").list("students")
                    for file in old_files:
                        if file['name'].startswith(original_id_number + "."):
                            supabase.storage.from_("ssis-student-photos").remove([f"students/{file['name']}"])
                except:
                    pass
            
            response = supabase.storage.from_("ssis-student-photos").upload(
                file_path,
                file_content,
                file_options={"content-type": photo.content_type, "upsert": "true"}
            )
            
            photo_url = supabase.storage.from_("ssis-student-photos").get_public_url(file_path)
            
        except Exception as e:
            return jsonify(success=False, field="student_photo", message=f"Failed to upload photo: {str(e)}"), 500
    
    success, message, field = Student.edit_student(
        id_number, first_name, last_name, gender, year_level, program_code, original_id_number, photo_url
    )

    if not success:
        if "already exists" in message.lower():
            return jsonify(success=False, field=field, message=message), 409
        return jsonify(success=False, field=field, message=message), 400

    return jsonify(success=True, message=message), 200


@student_bp.route("/students/delete", methods=["POST"])
@login_required
def delete_student():
    id_number = request.form.get("id_number", "").strip()

    if not id_number:
        return jsonify(success=False, field="id_number", message="ID number is required."), 400

    success,message = Student.delete_student(id_number)

    if not success:
        return jsonify(success=False, message=message), 400

    return jsonify(success=True, message=message), 200