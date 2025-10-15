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
    def check_existing_college_name(college_name, exclude_original_college_name=None):
        db = get_db()
        cursor = db.cursor()
        try:
            if exclude_original_college_name:
                cursor.execute(
                    "SELECT college_name FROM colleges WHERE college_name =%s AND college_name != %s",
                    (college_name, exclude_original_college_name,)
                )
            else:
                cursor.execute(
                    "SELECT college_name FROM colleges WHERE college_name =%s",
                    (college_name,)
                )
            return cursor.fetchone()
        finally:
            cursor.close()

    @staticmethod
    def register_college(college_code, college_name):
        if College.check_existing_college_code(college_code):
            return False, "The college code you entered already exists. Please use a different code.", "college_code"
        if College.check_existing_college_name(college_name):
            return False, "The college name you entered already exists. Please use a different name.", "college_name"

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
    def check_has_changes(college_code, college_name, original_college_code):
        db = get_db()
        cursor = db.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM colleges WHERE college_code = %s",
                (original_college_code,)
            )
            current_data = cursor.fetchone()
            
            current_college_code, current_college_name = current_data
            
            if college_code == current_college_code and college_name == current_college_name:
                return False, "No changes detected.", None
            
            return True, None, None
        finally:
            cursor.close()

    @staticmethod
    def edit_college(college_code, college_name, original_college_code, original_college_name):
        has_changes, message, field = College.check_has_changes(college_code, college_name, original_college_code)
    
        if not has_changes:
            return False, message, field

        if College.check_existing_college_code(college_code, exclude_original_college_code=original_college_code):
            return False, "The college code you entered already exists. Please use a different code.", "college_code"
        if College.check_existing_college_name(college_name, exclude_original_college_name=original_college_name):
            return False, "The college name you entered already exists. Please use a different name.", "college_name"
        
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