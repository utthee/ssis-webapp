from app.database import get_db

class Student:
    @staticmethod
    def get_all_programs():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM programs ORDER BY program_code ASC")
        programs = cursor.fetchall()
        cursor.close()
        return [{"program_code": column[0], "program_name": column[1], "college_code": column[2]} for column in programs]

    @staticmethod
    def get_all_students():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM students ORDER BY last_name")
        students_data = cursor.fetchall()
        cursor.close()

        return [{"id_number": column[0],
                "first_name": column[1],
                "last_name": column[2],
                "gender": column[3], 
                "year_level": column[4], 
                "program_code": column[5],
                "photo_url": column[6]} 
                for column in students_data]
    
    @staticmethod
    def check_existing_id_number(id_number, exclude_original_id_number=None):
        db = get_db()
        cursor = db.cursor()

        try:
            if exclude_original_id_number:
                cursor.execute(
                    "SELECT id_number FROM students WHERE id_number=%s AND id_number !=%s",
                    (id_number, exclude_original_id_number)
                )
            else:
                cursor.execute(
                    "SELECT id_number FROM students WHERE id_number=%s",
                    (id_number,)
                )
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    @staticmethod
    def register_student(id_number, first_name, last_name, gender, year_level, program_code, photo_url):
        if Student.check_existing_id_number(id_number):
            return False, "The ID Number you just entered already exists. Please enter a different ID Number.", "id_number"

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO students (id_number, first_name, last_name, gender, year_level, program_code, photo_url) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (id_number, first_name, last_name, gender, year_level, program_code, photo_url)
            )
            db.commit()
            return True, "Student registered successfully.", None
        except Exception as e:
            db.rollback()
            return False, str(e), None
        finally:
            cursor.close()

    @staticmethod
    def check_has_changes(id_number, first_name, last_name, gender, year_level, program_code, original_id_number, photo_url=None):
        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "SELECT id_number, first_name, last_name, gender, year_level, program_code, photo_url FROM students WHERE id_number=%s", 
                (original_id_number,)
            )
            current_data = cursor.fetchone()

            current_id_number, current_first_name, current_last_name, current_gender, current_year_level, current_program_code, current_photo_url = current_data

            if photo_url == "KEEP_EXISTING" or photo_url is None:
                photo_url = current_photo_url

            if (id_number == current_id_number and first_name == current_first_name and 
                last_name == current_last_name and gender == current_gender and
                str(year_level) == str(current_year_level) and program_code == current_program_code and
                photo_url == current_photo_url):
                return False, "No changes detected.", None
            
            return True, None, None
        except Exception as e:
            db.rollback()
            return False, str(e), None
        finally:
            cursor.close()

    @staticmethod
    def edit_student(id_number, first_name, last_name, gender, year_level, program_code, original_id_number, photo_url=None):
        has_changes, message, field = Student.check_has_changes(
            id_number, first_name, last_name, gender, year_level, program_code, original_id_number, photo_url
        )

        if not has_changes:
            return False, message, field
        
        if Student.check_existing_id_number(id_number, original_id_number):
            return False, "The ID Number you just entered already exists. Please enter a different ID Number.", "id_number"

        db = get_db()
        cursor = db.cursor()
        try:
            if photo_url == "KEEP_EXISTING":
                cursor.execute(
                    "UPDATE students SET id_number=%s, first_name=%s, last_name=%s, gender=%s, year_level=%s, program_code=%s WHERE id_number=%s",
                    (id_number, first_name, last_name, gender, year_level, program_code, original_id_number)
                )
            else:
                cursor.execute(
                    "UPDATE students SET id_number=%s, first_name=%s, last_name=%s, gender=%s, year_level=%s, program_code=%s, photo_url=%s WHERE id_number=%s",
                    (id_number, first_name, last_name, gender, year_level, program_code, photo_url, original_id_number)
                )
            db.commit()
            return True, "Student updated successfully.", None
        except Exception as e:
            db.rollback()
            return False, str(e), None
        finally:
            cursor.close()

    @staticmethod
    def delete_student(id_number):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM students WHERE id_number = %s", (id_number,))
            db.commit()
            cursor.close()
            return True, "Student deleted successfully."
        except Exception as e:
            db.rollback()
            cursor.close()
            return False, str(e)