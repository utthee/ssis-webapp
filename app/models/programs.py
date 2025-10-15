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
    def check_existing_program_name(program_name, exclude_original_program_name=None):
        db = get_db()
        cursor = db.cursor()
        try:
            if exclude_original_program_name:
                cursor.execute(
                    "SELECT program_name FROM programs WHERE program_name = %s AND program_name != %s",
                    (program_name, exclude_original_program_name,)
                )
            else:
                cursor.execute(
                    "SELECT program_name FROM programs WHERE program_name = %s",
                    (program_name,)
                )
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    @staticmethod
    def register_program(program_code, program_name, college_code):
        if Program.check_existing_program_code(program_code):
            return False, "The program code you entered already exists. Please use a different code.", "program_code"
        if Program.check_existing_program_name(program_name):
            return False, "The program name you entered already exists. Please try a different one.", "program_name"

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
    def check_has_changes(program_code, program_name, college_code, original_program_code):
        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "SELECT * FROM programs WHERE program_code=%s",
                (original_program_code,)
            )
            current_data = cursor.fetchone()

            current_program_code, current_program_name, current_college_code = current_data

            if (program_code == current_program_code and program_name == current_program_name and college_code == current_college_code):
                return False, "No changes detected.", None
            
            return True, None, None
        finally:
            cursor.close()

    @staticmethod
    def edit_program(program_code, program_name, college_code, original_program_code, original_program_name):
        has_changes, message, field = Program.check_has_changes(program_code, program_name, college_code, original_program_code)

        if not has_changes:
            return False, message, field

        if Program.check_existing_program_code(program_code, exclude_original_program_code=original_program_code):
            return False, "The program code you entered already exists. Please use a different code.", "program_code"
        if Program.check_existing_program_name(program_name, exclude_original_program_name=original_program_name):
            return False, "The program name you entered already exists. Please try a different one.", "program_name"

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