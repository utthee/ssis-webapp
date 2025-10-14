from app.database import get_db

class Dashboard:
    @staticmethod
    def get_total_students():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        total = cursor.fetchone()[0]
        cursor.close()
        return total

    @staticmethod
    def get_total_programs():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM programs")
        total = cursor.fetchone()[0]
        cursor.close()
        return total

    @staticmethod
    def get_total_colleges():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM colleges")
        total = cursor.fetchone()[0]
        cursor.close()
        return total

    @staticmethod
    def get_programs_with_most_students():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT 
                program.program_code,
                program.program_name,
                COUNT(student.id_number) AS student_count
            FROM programs program
            LEFT JOIN students student ON student.program_code = program.program_code
            GROUP BY program.program_code, program.program_name
            ORDER BY student_count DESC
            LIMIT 10;
        """)
        students_data = cursor.fetchall()
        cursor.close()

        return students_data

    @staticmethod
    def get_programs_per_college():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT college.college_code, COUNT(program.college_code) AS program_count
            FROM colleges college
            LEFT JOIN programs program ON college.college_code = program.college_code
            GROUP BY college.college_code
            ORDER BY program_count DESC;
        """)
        program_data = cursor.fetchall()
        cursor.close()
        return program_data