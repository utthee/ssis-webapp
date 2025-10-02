from app.database import get_db

class Program:
    @staticmethod
    def get_all_colleges():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM colleges ORDER BY code ASC")
        colleges = cursor.fetchall()
        cursor.close()
        return [{"code": column[0], "name": column[1]} for column in colleges]

    @staticmethod
    def get_all_programs():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM programs ORDER BY code ASC")
        programs = cursor.fetchall()
        cursor.close()
        return [{"code": column[0], "name": column[1], "college_code": column[2]} for column in programs]

    @staticmethod
    def register_program(program_code, program_name, college_code):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO programs (code, name, college_code) VALUES (%s, %s, %s)",
                (program_code, program_name, college_code)
            )
            db.commit()
            return True, "Program registered successfully."
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()

    @staticmethod
    def edit_program(program_code, program_name, college_code, original_program_code):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "UPDATE programs SET code=%s, name=%s, college_code=%s WHERE code=%s",
                (program_code, program_name, college_code, original_program_code)
            )
            db.commit()
            return True, "Program updated successfully!"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()

    @staticmethod
    def delete_program(program_code):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM programs WHERE code = %s", (program_code,))
            db.commit()
            return True, "Program deleted successfully!"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()