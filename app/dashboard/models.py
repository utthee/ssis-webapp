from app.database import get_db

def get_total_students():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    total = cursor.fetchone()[0]
    cursor.close()
    return total

def get_total_programs():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM programs")
    total = cursor.fetchone()[0]
    cursor.close()
    return total

def get_total_colleges():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM colleges")
    total = cursor.fetchone()[0]
    cursor.close()
    return total
