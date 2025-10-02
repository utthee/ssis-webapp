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
                program.code,
                program.name,
                COUNT(student.id_number) AS student_count
            FROM programs program
            LEFT JOIN students student ON student.program_code = program.code
            GROUP BY program.code, program.name
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
            SELECT college.code, COUNT(program.code) AS program_count
            FROM colleges college
            LEFT JOIN programs program ON college.code = program.college_code
            GROUP BY college.code
            ORDER BY program_count DESC;
        """)
        program_data = cursor.fetchall()
        cursor.close()
        return program_data