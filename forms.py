from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, Length, EqualTo
import sql_commands

class RegisterForm(FlaskForm):
    username = StringField("Käyttäjänimi", validators=[DataRequired(message="Käyttäjänimi ei saa olla tyhjä"), Length(min=3, max=20, message="Käyttäjänimen tulee olla %(min)d - %(max)d merkin pituinen")])
    password = PasswordField("Salasana", validators=[DataRequired(message="Salasana ei saa olla tyhjä"), Length(min=3, max=20, message="Salasanan tulee olla %(min)d - %(max)d merkin pituinen")])
    repeated_password = PasswordField("Salasana uusiksi", validators=[DataRequired(message="Salasana uusiksi ei saa olla tyhjä"), EqualTo("password", message="Salasanat eivät olleet samoja")])
    submit = SubmitField("Rekisteröidy")

class LoginForm(FlaskForm):
    username = StringField("Käyttäjänimi", validators=[DataRequired(message="Käyttäjänimi ei saa olla tyhjä")])
    password = PasswordField("Salasana", validators=[DataRequired(message="Salasana ei saa olla tyhjä")])
    submit = SubmitField("Kirjaudu")

class AddForm(FlaskForm):
    question = StringField("Kysymys:", validators=[DataRequired(message="Kysymys ei saa olla tyhjä")])
    topics = sql_commands.get_topics()
    topics = [(topic[0], topic[1]) for topic in topics]
    topic = SelectField("Aihealue", validators=[DataRequired(message="Aihealue ei saa olla tyhjä")], choices=topics)
    correct = StringField("Oikea vastaus:", validators=[DataRequired(message="Vastaus ei saa olla tyhjä")])
    incorrect= FieldList(StringField("Väärä vastaus:", validators=[DataRequired(message="Vastaus ei saa olla tyhjä")]), min_entries=3)
    submit = SubmitField("Lähetä")

