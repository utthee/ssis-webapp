from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db

class User(UserMixin):
    def __init__(self, id=None, username=None, email=None, password_hash=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create(cls, username, email, password):
        db = get_db()
        cur = db.cursor()
        hashed = generate_password_hash(password)
        cur.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, hashed),
        )
        db.commit()
        cur.close()

    @classmethod
    def get_by_username(cls, username):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT id, username, email, password_hash FROM users WHERE username = %s",
            (username,),
        )
        row = cur.fetchone()
        cur.close()
        if row:
            return cls(id=row[0], username=row[1], email=row[2], password_hash=row[3])
        return None
