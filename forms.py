from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField("Käyttäjänimi", validators=[DataRequired(message="Käyttäjänimi ei saa olla tyhjä"), Length(min=3, max=20, message="Käyttäjänimen tulee olla %(min)d - %(max)d merkin pituinen")])
    password = PasswordField("Salasana", validators=[DataRequired(message="Salasana ei saa olla tyhjä"), Length(min=3, max=20, message="Salasanan tulee olla %(min)d - %(max)d merkin pituinen")])
    repeated_password = PasswordField("Salasana uusiksi", validators=[DataRequired(message="Salasana uusiksi ei saa olla tyhjä"), EqualTo("password", message="Salasanat eivät olleet samoja")])
    submit = SubmitField("Rekisteröidy")

class LoginForm(FlaskForm):
    username = StringField("Käyttäjänimi", validators=[DataRequired(message="Käyttäjänimi ei saa olla tyhjä")])
    password = PasswordField("Salasana", validators=[DataRequired(message="Salasana ei saa olla tyhjä")])
    submit = SubmitField("Kirjaudu")

