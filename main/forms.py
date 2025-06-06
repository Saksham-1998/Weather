from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo

from main.models import User 


class RegisterForm(FlaskForm):
    username= StringField(label="Username: ")
    email= StringField(label="Email: ", validators=[DataRequired(),Email()])
    password1= PasswordField(label="Enter Password: ", validators=[DataRequired(), Length(min=6)] )
    password2= PasswordField(label="Enter Password Again: ", validators=[DataRequired(), EqualTo('password1', message="password didn't match")])
    submit= SubmitField(label="Create Account")


    def validate_username(self, username_to_check):
        user= User.query.filter_by(username= username_to_check.data).first()
        if user:
            raise ValidationError("Username already exist")
        
    def validate_email(self, email_to_check):
        email= User.query.filter_by(email= email_to_check.data).first()
        if email:
            raise ValidationError("Email already exist")



class LoginForm(FlaskForm):
    username = StringField(label="Username:", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign in")