from app.database import get_db

class Student:
    @staticmethod
    def get_all_programs():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM programs ORDER BY code ASC")
        programs = cursor.fetchall()
        cursor.close()
        return [{"code": column[0], "name": column[1], "college_code": column[2]} for column in programs]

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
                "program_code": column[5]} 
                for column in students_data]

    @staticmethod
    def register_student(id_number, first_name, last_name, gender, year_level, program_code):
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

    @staticmethod
    def edit_student(id_number, first_name, last_name, gender, year_level, program_code, original_id_number):
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

    @staticmethod
    def delete_student(id_number):
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