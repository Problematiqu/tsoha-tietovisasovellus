from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList, SelectField, RadioField
from wtforms.validators import InputRequired, Length, EqualTo
import sql_commands

class RegisterForm(FlaskForm):
    username = StringField("Käyttäjänimi", validators=[InputRequired(message="Käyttäjänimi ei saa olla tyhjä"), Length(min=3, max=20, message="Käyttäjänimen tulee olla %(min)d - %(max)d merkin pituinen")])
    password = PasswordField("Salasana", validators=[InputRequired(message="Salasana ei saa olla tyhjä"), Length(min=3, max=20, message="Salasanan tulee olla %(min)d - %(max)d merkin pituinen")])
    repeated_password = PasswordField("Salasana uusiksi", validators=[InputRequired(message="Salasana uusiksi ei saa olla tyhjä"), EqualTo("password", message="Salasanat eivät olleet samoja")])
    submit = SubmitField("Rekisteröidy")

class LoginForm(FlaskForm):
    username = StringField("Käyttäjänimi", validators=[InputRequired(message="Käyttäjänimi ei saa olla tyhjä")])
    password = PasswordField("Salasana", validators=[InputRequired(message="Salasana ei saa olla tyhjä")])
    submit = SubmitField("Kirjaudu")

class AddForm(FlaskForm):
    question = StringField("Kysymys:", validators=[InputRequired(message="Kysymys ei saa olla tyhjä")])
    topics = sql_commands.get_topics()
    topics = [(topic[0], topic[1]) for topic in topics]
    topic = SelectField("Aihealue", validators=[InputRequired(message="Aihealue ei saa olla tyhjä")], choices=topics)
    correct = StringField("Oikea vastaus:", validators=[InputRequired(message="Vastaus ei saa olla tyhjä")])
    incorrect= FieldList(StringField("Väärä vastaus:", validators=[InputRequired(message="Vastaus ei saa olla tyhjä")]), min_entries=3)
    submit = SubmitField("Lähetä")

class QuizForm(FlaskForm):
    question = FieldList(RadioField(validators=[InputRequired(message="Valitse yksi")] ,coerce=int, choices=[]), min_entries=10)
    submit = SubmitField("Lähetä")

