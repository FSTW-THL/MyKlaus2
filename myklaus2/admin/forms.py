from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    user = StringField("Username", validators=[DataRequired()])
    pwd = PasswordField("Passwort", validators=[DataRequired()])
    submit = SubmitField("Login")