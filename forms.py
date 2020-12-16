from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField

class SignUpForm(FlaskForm):
  username = StringField('Username')
  password = PasswordField('Password')
  file = FileField('File')
  submit = SubmitField('Sign up')