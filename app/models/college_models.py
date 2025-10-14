from app.database import get_db

class College:
    @staticmethod
    def get_all_colleges():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM colleges ORDER BY college_code ASC")
        colleges = cursor.fetchall()
        cursor.close()
        return [{"college_code": column[0], "college_name": column[1]} for column in colleges]
    
    @staticmethod
    def check_existing_college_code(college_code, exclude_original_college_code=None):
        db = get_db()
        cursor = db.cursor()
        try:
            if exclude_original_college_code:
                cursor.execute(
                    "SELECT college_code FROM colleges WHERE college_code = %s AND college_code != %s", 
                    (college_code, exclude_original_college_code)
                )
            else:
                cursor.execute(
                    "SELECT college_code FROM colleges WHERE college_code = %s", 
                    (college_code,)
                )
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    @staticmethod
    def register_college(college_code, college_name):
        if College.check_existing_college_code(college_code):
            return False, "College Code already exists. Please use a different code.", "college_code"

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO colleges (college_code, college_name) VALUES (%s, %s)", (college_code, college_name)
            )
            db.commit()
            return True, "College registered successfully.", None
        except Exception as e:
            db.rollback()
            return False, str(e), None
        finally:
            cursor.close()

    @staticmethod
    def edit_college(college_code, college_name, original_college_code):
        if College.check_existing_college_code(college_code, exclude_original_college_code=original_college_code):
            return False, "College Code already exists. Please use a different code.", "college_code"
        
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "UPDATE colleges SET college_code = %s, college_name = %s WHERE college_code = %s",
                (college_code, college_name, original_college_code),
            )
            db.commit()
            return True, "College updated successfully.", None
        except Exception as e:
            db.rollback()
            return False, str(e), None
        finally:
            cursor.close()
    
    def delete_college(college_code):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM colleges WHERE college_code = %s", (college_code,))
            db.commit()
            return True, "College deleted successfully."
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            cursor.close()