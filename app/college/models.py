from app.database import get_db

class College:
    @staticmethod
    def get_all_colleges():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM colleges ORDER BY code ASC")
        colleges = cursor.fetchall()
        cursor.close()
        return [{"code": column[0], "name": column[1]} for column in colleges]

    @staticmethod
    def register_college(code, name):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO colleges (code, name) VALUES (%s, %s)", (code, name)
            )
            db.commit()
            return True, "College registered successfully."
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()

    @staticmethod
    def edit_college(original_code, code, name):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "UPDATE colleges SET code = %s, name = %s WHERE code = %s",
                (code, name, original_code),
            )
            db.commit()
            return True, "College updated successfully!"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()

    
    def delete_college(code):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM colleges WHERE code = %s", (code,))
            db.commit()
            return True, "College deleted successfully!"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()