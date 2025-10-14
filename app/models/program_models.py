from app.database import get_db

class Program:
    @staticmethod
    def get_all_colleges():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM colleges ORDER BY college_code ASC")
        colleges = cursor.fetchall()
        cursor.close()
        return [{"college_code": column[0], "college_name": column[1]} for column in colleges]

    @staticmethod
    def get_all_programs():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM programs ORDER BY program_code ASC")
        programs = cursor.fetchall()
        cursor.close()
        return [{"program_code": column[0], "program_name": column[1], "college_code": column[2]} for column in programs]
    
    @staticmethod
    def check_existing_program_code(program_code, exclude_original_program_code=None):
        db = get_db()
        cursor = db.cursor()
        try:
            if exclude_original_program_code:
                cursor.execute(
                    "SELECT program_code FROM programs WHERE program_code = %s AND program_code != %s",
                    (program_code, exclude_original_program_code)
                )
            else:
                cursor.execute(
                    "SELECT program_code FROM programs WHERE program_code = %s",
                    (program_code,)
                )
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    @staticmethod
    def register_program(program_code, program_name, college_code):
        if Program.check_existing_program_code(program_code):
            return False, "Program Code already exists. Please use a different code.", "program_code"

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO programs (program_code, program_name, college_code) VALUES (%s, %s, %s)",
                (program_code, program_name, college_code)
            )
            db.commit()
            return True, "Program registered successfully.", None
        except Exception as e:
            db.rollback()
            return False, str(e), None
        finally:
            cursor.close()

    @staticmethod
    def edit_program(program_code, program_name, college_code, original_program_code):
        if Program.check_existing_program_code(program_code, original_program_code):
            return False, "Program Code already exists. Please use a different code.", "program_code"

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "UPDATE programs SET program_code=%s, program_name=%s, college_code=%s WHERE program_code=%s",
                (program_code, program_name, college_code, original_program_code)
            )
            db.commit()
            return True, "Program updated successfully.", None
        except Exception as e:
            db.rollback()
            return False, str(e), None
        finally:
            cursor.close()

    @staticmethod
    def delete_program(program_code):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM programs WHERE program_code = %s", (program_code,))
            db.commit()
            return True, "Program deleted successfully."
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()