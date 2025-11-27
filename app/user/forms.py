from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators, ValidationError
from app.database import get_db

class SignupForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired(), validators.Length(min=3, max=50)])
    email = StringField("Email", [validators.DataRequired(), validators.Length(min=6, max=254)])
    password = PasswordField("Password", [validators.DataRequired(), validators.Length(min=5)])
    confirm_password = PasswordField("Confirm Password", [validators.DataRequired(), validators.EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", (username.data,))
        user = cur.fetchone()
        cur.close()

        if user:
            raise ValidationError("This username is already taken. Please choose a different one.")

    def validate_email(self, email):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s", (email.data,))
        user = cur.fetchone()
        cur.close()

        if user:
            raise ValidationError("This email is already registered. Please use a different one.")

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired(), validators.Length(min=3, max=25)])
    password = PasswordField("Password", [validators.DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")
