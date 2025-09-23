from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators

class SignupForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired(), validators.Length(min=3, max=25)])
    email = StringField("Email", [validators.DataRequired(), validators.Length(min=6, max=50)])
    password = PasswordField("Password", [validators.DataRequired(), validators.Length(min=6)])
    confirm_password = PasswordField("Confirm Password", [validators.DataRequired(), validators.EqualTo("password")])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired(), validators.Length(min=3, max=25)])
    password = PasswordField("Password", [validators.DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
